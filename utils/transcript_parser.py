import re
from io import StringIO
from bs4 import BeautifulSoup
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from tqdm import tqdm # For local progress bars, if needed

# --- NLTK Downloads (ensure these run only once, e.g., at app startup or first import) ---
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)
try:
    nltk.data.find('corpora/omw-1.4')
except LookupError:
    nltk.download('omw-1.4', quiet=True)

lemmatizer = WordNetLemmatizer()

# --- Text Preprocessing Functions (similar to clean.py but adapted for transcripts) ---

def remove_html_tags(text):
    """Removes HTML tags from a string."""
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()

def remove_punctuation(text):
    """Removes punctuation from a string."""
    return re.sub(r'[^\w\s]', '', text)

def remove_urls(text):
    """Removes URLs from a string."""
    return re.sub(r'http\S+|www.\S+', '', text)

def tokenize_and_lemmatize(text):
    """Tokenizes text and applies lemmatization."""
    tokens = word_tokenize(text)
    lemmas = [lemmatizer.lemmatize(token) for token in tokens]
    return " ".join(lemmas)

def preprocess_text(text, apply_lemmatization=False):
    """
    Applies a series of preprocessing steps to a single string for transcripts.
    """
    if not isinstance(text, str):
        return ""
    
    text = text.lower()
    text = remove_urls(text)
    text = remove_html_tags(text)
    text = remove_punctuation(text)
    
    if apply_lemmatization:
        text = tokenize_and_lemmatize(text)
        
    text = text.strip()
    return text

# --- Transcript Parsing Functions ---

def parse_txt_transcript(file_object, apply_lemmatization=False):
    """
    Parses a plain text transcript file. Each line is treated as a separate utterance.
    
    Args:
        file_object: A file-like object (e.g., io.StringIO) containing the transcript.
        apply_lemmatization (bool): Whether to apply lemmatization during preprocessing.

    Returns:
        list[str]: A list of cleaned utterance strings.
    """
    utterances = []
    for line in tqdm(file_object, desc="Parsing TXT Transcript"):
        cleaned_line = preprocess_text(line.strip(), apply_lemmatization)
        if cleaned_line: # Only add non-empty lines
            utterances.append(cleaned_line)
    return utterances

def parse_srt_transcript(file_object, apply_lemmatization=False):
    """
    Parses an SRT (SubRip Subtitle) file. Extracts text, removes timestamps/indices.
    
    Args:
        file_object: A file-like object (e.g., io.StringIO) containing the transcript.
        apply_lemmatization (bool): Whether to apply lemmatization during preprocessing.

    Returns:
        list[str]: A list of cleaned utterance strings.
    """
    content = file_object.read()
    # SRT pattern: Index, Timestamp, Text (can be multiline)
    # Example:
    # 1
    # 00:00:00,000 --> 00:00:02,500
    # Hello world.
    #
    # 2
    # 00:00:03,000 --> 00:00:05,000
    # This is a test.
    
    # Regex to capture the text block for each subtitle entry
    # It looks for lines that DON'T start with a digit (index) or a timestamp (XX:XX:XX,)
    # and captures everything until an empty line or next entry
    
    # This simpler approach extracts all lines that are not indices or timestamps
    lines = content.split('\n')
    utterances = []
    current_utterance_lines = []

    for line in tqdm(lines, desc="Parsing SRT Transcript"):
        line = line.strip()
        if not line: # Empty line indicates end of a subtitle block
            if current_utterance_lines:
                combined_utterance = " ".join(current_utterance_lines)
                cleaned_utterance = preprocess_text(combined_utterance, apply_lemmatization)
                if cleaned_utterance:
                    utterances.append(cleaned_utterance)
                current_utterance_lines = [] # Reset for next block
            continue # Skip empty line

        # Skip lines that look like numbers (index) or timestamps
        if re.fullmatch(r'\d+', line): # Only digits
            continue
        if re.fullmatch(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', line): # Timestamp format
            continue

        current_utterance_lines.append(line)

    # Add the last utterance if any remains
    if current_utterance_lines:
        combined_utterance = " ".join(current_utterance_lines)
        cleaned_utterance = preprocess_text(combined_utterance, apply_lemmatization)
        if cleaned_utterance:
            utterances.append(cleaned_utterance)

    return utterances


def parse_transcript_data(file_object, file_type: str, apply_lemmatization=False):
    """
    Dispatches to the correct parsing function based on file type.

    Args:
        file_object: The uploaded file-like object.
        file_type (str): The extension of the file ('txt', 'srt').
        apply_lemmatization (bool): Whether to apply lemmatization during preprocessing.

    Returns:
        list[str]: A list of cleaned transcript utterances.
    """
    if file_type == 'txt':
        return parse_txt_transcript(file_object, apply_lemmatization)
    elif file_type == 'srt':
        return parse_srt_transcript(file_object, apply_lemmatization)
    else:
        raise ValueError(f"Unsupported transcript file type: {file_type}. Only TXT and SRT are supported.")

