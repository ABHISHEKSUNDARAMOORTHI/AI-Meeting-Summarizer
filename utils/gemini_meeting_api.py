import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from google.api_core import exceptions
import time
from dotenv import load_dotenv

load_dotenv()

# Configure API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")

genai.configure(api_key=GOOGLE_API_KEY)

# --- Function to get a supported model name ---
def get_supported_model(preferred_models=['gemini-1.5-flash', 'gemini-1.0-pro'], fallback_model='gemini-1.0-pro'):
    """
    Attempts to find a supported Gemini model for generateContent,
    preferring a list of models, then falling back to a default.
    """
    print("Checking available models for GeminiMeetingAPI...")
    try:
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        print(f"Models supporting generateContent: {available_models}")

        for p_model in preferred_models:
            full_model_name = f"models/{p_model}" 
            if full_model_name in available_models:
                print(f"Using preferred model: {p_model}")
                return p_model
        
        full_fallback_name = f"models/{fallback_model}"
        if full_fallback_name in available_models:
            print(f"Preferred models not found. Falling back to: {fallback_model}")
            return fallback_model
        
        raise ValueError(f"No suitable Gemini model found. Available: {available_models}. Please check your model names or API access.")

    except Exception as e:
        print(f"Error listing models in get_supported_model: {e}")
        print(f"Attempting to proceed with hardcoded fallback model '{fallback_model}' (might still fail).")
        return fallback_model


# Initialize gemini_model using the helper function for the meeting assistant
model_to_use = get_supported_model(preferred_models=['gemini-1.5-flash', 'gemini-1.0-pro'])

try:
    gemini_model = genai.GenerativeModel(model_to_use)
    # Perform a quick test to ensure the model is responsive
    gemini_model.generate_content("test", safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE
    })
    print(f"Successfully initialized Gemini model for Meeting Assistant: {model_to_use}")
except Exception as e:
    # If the initial model fails, try a very basic fallback
    print(f"Failed to initialize or use '{model_to_use}': {e}. Attempting fallback to 'gemini-1.0-pro'.")
    try:
        gemini_model = genai.GenerativeModel('gemini-1.0-pro')
        gemini_model.generate_content("test", safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE
        })
        print("Successfully fell back to gemini-1.0-pro for Meeting Assistant.")
    except Exception as fallback_e:
        raise RuntimeError(f"Critical Error: Could not initialize any Gemini model for Meeting Assistant. Last attempt failed with: {fallback_e}")


# --- Helper Function for Robust API Calls with Exponential Backoff ---
def make_gemini_call_with_retry(prompt: str, model_instance: genai.GenerativeModel, max_retries: int = 7, initial_delay: float = 1.0) -> str:
    """
    Makes a Gemini API call with exponential backoff for quota/rate limit (429) errors.

    Args:
        prompt (str): The prompt to send to the Gemini model.
        model_instance (genai.GenerativeModel): The configured Gemini GenerativeModel instance.
        max_retries (int): Maximum number of retry attempts.
        initial_delay (float): Initial delay in seconds before the first retry.

    Returns:
        str: The generated text response, or an error message if all retries fail.
    """
    retries = 0
    delay = initial_delay
    while retries < max_retries:
        try:
            response = model_instance.generate_content(
                prompt,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }
            )
            if response and response.text:
                return response.text.strip()
            else:
                print(f"AI response was empty or blocked for input. Prompt feedback: {response.prompt_feedback}")
                return "AI response was empty or blocked, possibly due to safety settings."

        except exceptions.ResourceExhausted as e:
            retries += 1
            if retries < max_retries:
                print(f"Quota/Rate Limit Exceeded (429). Retrying in {delay:.2f}s... (Attempt {retries}/{max_retries})")
                time.sleep(delay)
                delay *= 2
            else:
                return f"Failed to get response after {max_retries} retries due to quota/rate limit: {e}"
        except Exception as e:
            print(f"An unexpected API error occurred during generate_content call: {e}")
            return f"An unexpected API error occurred: {e}"
    
    return "Failed to get response after multiple retries (unknown reason)."


# --- Core Meeting Assistant Functions ---

def get_meeting_summary(full_transcript_text: str) -> str:
    """
    Generates a concise summary of the meeting transcript using Gemini.

    Args:
        full_transcript_text (str): The entire cleaned meeting transcript as a single string.

    Returns:
        str: The AI-generated summary.
    """
    prompt = f"""
    You are an AI assistant specialized in summarizing meeting transcripts.
    Read the following meeting transcript and provide a concise, high-level summary.
    Focus on the main topics discussed, key outcomes, and overall purpose of the meeting.

    Meeting Transcript:
    {full_transcript_text}

    Summary:
    """
    return make_gemini_call_with_retry(prompt, gemini_model)


def extract_action_items(full_transcript_text: str) -> list[str]:
    """
    Extracts action items (tasks, responsibilities, deadlines) from the meeting transcript.

    Args:
        full_transcript_text (str): The entire cleaned meeting transcript as a single string.

    Returns:
        list[str]: A list of identified action items. Each item should be a clear,
                   single-line description. Return an empty list if none found.
    """
    prompt = f"""
    From the following meeting transcript, identify all action items, tasks, or follow-up activities.
    For each action item, state what needs to be done, who is responsible (if mentioned), and any deadlines (if mentioned).
    List each action item on a new line, starting with a dash "- ". If no action items are present, state "No action items identified."

    Meeting Transcript:
    {full_transcript_text}

    Action Items:
    """
    raw_response = make_gemini_call_with_retry(prompt, gemini_model)
    if "No action items identified" in raw_response:
        return []
    # Parse the bulleted list
    action_items = [item.strip() for item in raw_response.split('- ') if item.strip()]
    return action_items


def highlight_key_decisions(full_transcript_text: str) -> list[str]:
    """
    Identifies and highlights key decisions made during the meeting from the transcript.

    Args:
        full_transcript_text (str): The entire cleaned meeting transcript as a single string.

    Returns:
        list[str]: A list of key decisions. Each decision should be a clear,
                   single-line description. Return an empty list if none found.
    """
    prompt = f"""
    Review the following meeting transcript and identify all significant decisions that were made.
    List each key decision on a new line, starting with a dash "- ". If no decisions are present, state "No key decisions identified."

    Meeting Transcript:
    {full_transcript_text}

    Key Decisions:
    """
    raw_response = make_gemini_call_with_retry(prompt, gemini_model)
    if "No key decisions identified" in raw_response:
        return []
    # Parse the bulleted list
    decisions = [item.strip() for item in raw_response.split('- ') if item.strip()]
    return decisions

# You can add other functions here for speaker analysis or specific topic deep-dives
