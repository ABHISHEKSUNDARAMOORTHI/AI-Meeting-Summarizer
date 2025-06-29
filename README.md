# 🤖 AI Meeting Assistant: Summarizer & Action Item Extractor

Welcome to the **AI Meeting Assistant**!  
This Streamlit application transforms raw meeting transcripts into **concise summaries**, **actionable task lists**, and **highlighted decisions** using **Google's Gemini AI**.

Say goodbye to manual note-taking and missed follow-ups. 📋✅

---

## ✨ Feature Overview

### 📂 Transcript Handling

- **Multi-format Upload**: Supports `.txt` (plain text) and `.srt` (SubRip subtitle) files.
- **Advanced Preprocessing**:
  - Cleans and normalizes raw text.
  - Optional **lemmatization** toggle for NLP enhancement.
  - Smart fallback for inconsistent formats.

---

### 🧠 AI-Powered Analysis (via Google Gemini)

- 🔍 **Summarization**  
  Generates executive-style summaries of meeting discussions.

- ✅ **Action Item Extraction**  
  Identifies tasks, owners, and deadlines from your transcript.

- 📌 **Key Decision Highlights**  
  Extracts major decisions made during the meeting.

---

### 📊 Visualization & Insights

- **Top Discussion Topics**  
  - Displays a placeholder bar chart.  
  - Ready for integration with LDA or NER for dynamic topic modeling.

---

### 🎨 UI & Usability

- 🌙 **Theme Toggle**  
  Switch between dark and light modes seamlessly.

- 📌 **Session State Management**  
  Retains uploads and results across reruns for smoother user experience.

---

### 💾 Export & Report Generation

- 📝 **Downloadable Markdown Report**  
  Includes:
  - Summary  
  - Action Items  
  - Key Decisions  
  - Topics

---

### 🧹 Reset & Feedback

- 🔄 **Reset Button**  
  Clears the session state and resets the app.

- ⏳ **Progress Indicators**  
  Displays real-time spinners and info messages during parsing and AI analysis.

---

### 🚧 Future Enhancements (Planned)

- 📅 Calendar/Event Integration  
- 🔗 Slack/Teams Summary Sharing  
- 📈 Topic Modeling from Transcript Content  
- 🧠 Multi-Speaker Attribution & Talk Time Analytics

---

## ⚙️ How It Works (Simplified)

### 1. 📥 Upload & Preprocess Transcript

- Upload your `.txt` or `.srt` transcript.
- The app cleans and processes the text for AI input.

### 2. 🤖 AI Analysis (Google Gemini)

- Transcript is chunked or sent whole to Gemini AI.
- Gemini returns:
  - 📋 A summary of key points
  - ✅ Actionable tasks
  - 📌 Highlighted decisions

### 3. 📊 Display & Interaction

- Results shown in a clear, structured format.
- (Optional) Speaker visualizations based on transcript patterns.

### 4. 🔁 Reliable Processing

- Uses **exponential backoff** to handle rate limits.
- Automatically retries until AI response is received (up to quota limits).

---

## 🚀 Setup & Run Locally

### 🧱 Prerequisites

- Python 3.8+
- Google Gemini API key (from [Google AI Studio](https://aistudio.google.com))

> ⚠️ Free-tier API keys have strict daily quotas. Enable billing for large/long transcripts.

---

### 🛠 Installation Steps

#### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/ai-meeting-assistant.git
cd ai-meeting-assistant
````

#### 2. Create and Activate Virtual Environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### 3. Install Dependencies

Create a `requirements.txt` with:

```
streamlit
google-generativeai
python-dotenv
pandas
nltk
beautifulsoup4
tqdm
matplotlib
wordcloud
```

Then install:

```bash
pip install -r requirements.txt
```

#### 4. Configure Your API Key

Create a `.env` file in the root of your project:

```
GOOGLE_API_KEY="YOUR_GEMINI_API_KEY_HERE"
```

---

### ▶️ Running the App

Ensure your virtual environment is active and run:

```bash
streamlit run app.py
```

The app will launch at `http://localhost:8501` by default.

---

## 🗂️ Project Structure

```
.
├── app.py                     # Main Streamlit app
├── requirements.txt           # Python dependencies
├── .env                       # API key storage
└── utils/
    ├── __init__.py
    ├── transcript_parser.py   # Cleaning/parsing logic
    ├── gemini_meeting_api.py  # Gemini interaction, retry logic
    ├── styling.py             # Dark/light theme and CSS
    └── visualization.py       # Charting & topic display
```

---

## 🧪 Troubleshooting

### ❌ `ModuleNotFoundError`

* Ensure `__init__.py` exists in `utils/`
* Check file/folder casing
* Always run from the root directory: `streamlit run app.py`

---

### ❌ 429 Quota Exceeded

* Wait 24 hours OR enable billing in Google Cloud

---

### ❌ Model Not Found (404)

* Your key may not support the specified Gemini model
* Use `genai.list_models()` to auto-detect compatible models in `gemini_meeting_api.py`

---

## 👥 Contributing

PRs are welcome! Fork the repo → create a branch → code → push → open a PR.

---

## 📄 License

MIT License – See the `LICENSE` file for details.

---

## 🙌 Built By

**Abhishek Sundaramoorthi** – Always learning, always building.
