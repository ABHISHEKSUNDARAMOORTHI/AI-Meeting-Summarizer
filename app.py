import streamlit as st
import os
from dotenv import load_dotenv
from io import StringIO, BytesIO
import zipfile
import pandas as pd # Needed for potential dataframes (e.g., action items if structured)

# --- Import Custom Utility Modules ---
# Make sure these match your file names and are in the 'utils' directory
from utils.transcript_parser import parse_transcript_data
from utils.gemini_meeting_api import get_meeting_summary, extract_action_items, highlight_key_decisions
from utils.visualization import plot_discussion_topics # This is for topic visualization
from utils.styling import apply_base_styles, set_theme_js, get_theme_colors # Import get_theme_colors here too if needed elsewhere


# --- Configuration & Setup ---
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("🚨 GOOGLE_API_KEY not found in environment variables. Please set it in your .env file.")
    st.stop()

st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Theme Toggle Functionality ---
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

apply_base_styles(st.session_state.theme == 'dark')

def toggle_theme():
    """Toggles between dark and light themes."""
    if st.session_state.theme == 'dark':
        st.session_state.theme = 'light'
    else:
        st.session_state.theme = 'dark'
    set_theme_js(st.session_state.theme == 'dark')
    st.rerun()

# --- Initialize Session State for Data & Analysis Results ---
if 'transcript_text' not in st.session_state:
    st.session_state.transcript_text = ""
if 'file_type' not in st.session_state:
    st.session_state.file_type = None
if 'meeting_summary' not in st.session_state:
    st.session_state.meeting_summary = ""
if 'action_items' not in st.session_state:
    st.session_state.action_items = []
if 'key_decisions' not in st.session_state:
    st.session_state.key_decisions = []
if 'discussion_topics' not in st.session_state:
    st.session_state.discussion_topics = []
if 'analysis_completed' not in st.session_state:
    st.session_state.analysis_completed = False
if 'last_uploaded_file_name' not in st.session_state:
    st.session_state.last_uploaded_file_name = None

# --- Header ---
st.markdown("""
<div style='background-color: var(--bg-secondary); padding: 1rem 2rem; border-radius: 8px; margin-bottom: 2rem;'>
  <h1 style='color: var(--header-color); margin-top:0;'>🎙️ AI Meeting Assistant</h1>
  <p style='color: var(--text-color); margin-bottom:0;'>Upload your meeting transcripts for AI-powered summaries, action items, and key decisions.</p>
</div>
""", unsafe_allow_html=True)


# --- File Uploader and Theme Toggle ---
col1, col2 = st.columns([0.8, 0.2])

with col1:
    uploaded_file = st.file_uploader(
        "📤 Upload a Meeting Transcript (TXT or SRT)",
        type=["txt", "srt"],
        help="TXT (plain text, one utterance per line) or SRT (subtitle format)."
    )

with col2:
    st.button(
        "💡 Toggle Theme",
        on_click=toggle_theme,
        help=f"Switch to {'Light' if st.session_state.theme == 'dark' else 'Dark'} Mode"
    )

# --- Main Processing Logic ---
if uploaded_file is not None:
    if st.session_state.last_uploaded_file_name != uploaded_file.name:
        st.session_state.last_uploaded_file_name = uploaded_file.name
        
        st.session_state.transcript_text = ""
        st.session_state.meeting_summary = ""
        st.session_state.action_items = []
        st.session_state.key_decisions = []
        st.session_state.discussion_topics = []
        st.session_state.analysis_completed = False
        st.session_state.file_type = uploaded_file.name.split('.')[-1].lower()

        with st.spinner("Parsing and cleaning transcript data..."):
            try:
                file_content_str = StringIO(uploaded_file.getvalue().decode("utf-8"))
                
                # Checkbox for lemmatization
                lemmatize_option = st.checkbox("Apply Lemmatization (advanced text normalization)", value=False, key="lemmatize_upload")
                
                cleaned_utterances = parse_transcript_data(file_content_str, st.session_state.file_type, apply_lemmatization=lemmatize_option)
                
                st.session_state.transcript_text = " ".join(cleaned_utterances)

                st.success(f"✅ Transcript uploaded and parsed. Total utterances: **{len(cleaned_utterances)}**")
                
            except ValueError as ve:
                st.error(f"Transcript Parsing Error: {ve}. Please check file format and content.")
                st.session_state.transcript_text = ""
                st.session_state.last_uploaded_file_name = None
            except Exception as e:
                st.error(f"An unexpected error occurred during file parsing: {e}")
                st.session_state.transcript_text = ""
                st.session_state.last_uploaded_file_name = None
        
        st.rerun()

    if st.session_state.transcript_text and not st.session_state.analysis_completed:
        st.markdown("---")
        if st.button("🎯 Run AI Meeting Analysis", key="run_ai_analysis_button"):
            with st.spinner("Starting AI analysis (Summary, Action Items, Decisions)... This may take a few minutes for longer transcripts."):
                
                st.info("Generating Meeting Summary...")
                st.session_state.meeting_summary = get_meeting_summary(st.session_state.transcript_text)
                
                st.info("Extracting Action Items...")
                st.session_state.action_items = extract_action_items(st.session_state.transcript_text)

                st.info("Highlighting Key Decisions...")
                st.session_state.key_decisions = highlight_key_decisions(st.session_state.transcript_text)
                
                # Dynamic topics: In a real app, you might use Gemini to extract these,
                # For now, let's keep the dummy list but make it depend on some content
                if st.session_state.meeting_summary:
                    # This is a placeholder; you might add an AI call to get topics from the summary
                    st.session_state.discussion_topics = ["project progress", "design review", "content approval", "analytics dashboard", "budget allocation", "influencer outreach"]
                
                st.session_state.analysis_completed = True
                st.success("AI Meeting Analysis Complete!")
                st.rerun()
        else:
            st.info("Click '🎯 Run AI Meeting Analysis' to process the transcript with Gemini.")
    elif st.session_state.analysis_completed:
        st.success("✅ AI Analysis already completed for this transcript.")
        st.markdown("---")


# --- Display Results & Visualizations (if analysis results exist) ---
if st.session_state.analysis_completed:
    st.subheader("Results:")

    st.markdown("#### 📝 Meeting Summary")
    if st.session_state.meeting_summary:
        st.markdown(f"<div style='background-color: var(--bg-secondary); padding: 1rem; border-radius: 8px;'>", unsafe_allow_html=True)
        st.markdown(st.session_state.meeting_summary)
        st.markdown(f"</div>", unsafe_allow_html=True)
    else:
        st.info("Meeting summary not available. Run the analysis first.")

    st.markdown("#### ✅ Action Items")
    if st.session_state.action_items:
        for item in st.session_state.action_items:
            st.markdown(f"- {item}")
    else:
        st.info("No action items identified for this meeting.")

    st.markdown("#### 💡 Key Decisions")
    if st.session_state.key_decisions:
        for decision in st.session_state.key_decisions:
            st.markdown(f"- {decision}")
    else:
        st.info("No key decisions identified for this meeting.")
    
    st.markdown("---")
    st.subheader("📊 Visual Insights:")
    st.markdown("#### Top Discussion Topics")
    if st.session_state.discussion_topics:
        # Pass the current theme state to the visualization function
        plot_discussion_topics(st.session_state.discussion_topics, st.session_state.theme == 'dark')
    else:
        st.info("No discussion topics to visualize.")
    
    st.markdown("---")

    # --- Export Report and Reset Application ---
    col_actions1, col_actions2 = st.columns([1, 1])
    
    with col_actions1:
        report_text = f"""
# AI Meeting Analysis Report

## Meeting Summary
{st.session_state.meeting_summary or "N/A"}

## Action Items
{("\\n".join([f"- {item}" for item in st.session_state.action_items])) or "No action items identified."}

## Key Decisions
{("\\n".join([f"- {decision}" for decision in st.session_state.key_decisions])) or "No key decisions identified."}

## Discussion Topics
{", ".join(st.session_state.discussion_topics) or "No topics identified."}

---
Generated by AI Meeting Assistant.
"""
        st.download_button(
            label="📁 Export Analysis Report (Markdown)",
            data=report_text,
            file_name="meeting_analysis_report.md",
            mime="text/markdown",
            help="Download a Markdown file containing the summary, action items, and key decisions."
        )
    
    with col_actions2:
        if st.button("🔄 Reset Application", help="Clear all data and restart the application."):
            st.session_state.clear()
            st.experimental_rerun()

else:
    if uploaded_file is None:
        st.info("Please upload a meeting transcript file to begin the analysis.")
    elif st.session_state.transcript_text and not st.session_state.analysis_completed:
        st.info("Transcript loaded. Click '🎯 Run AI Meeting Analysis' to process it.")

st.markdown("---")
st.markdown("Powered by Google Gemini & Streamlit")

