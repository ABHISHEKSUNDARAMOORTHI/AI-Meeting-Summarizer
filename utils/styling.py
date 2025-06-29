import streamlit as st

# Function to get theme colors
def get_theme_colors(is_dark_theme: bool):
    """
    Returns a dictionary of theme-dependent color values.
    """
    if is_dark_theme:
        return {
            "bg_primary": "#0d1117",
            "bg_secondary": "#161b22",
            "text_color": "#e6edf3",
            "header_color": "#58a6ff",
            "accent_color": "#21262d",
            "plot_bar_color": "#0ea5e9", # Specific color for plot bars
            "plot_grid_color": "#555555"
        }
    else:
        return {
            "bg_primary": "#ffffff",
            "bg_secondary": "#f0f2f6",
            "text_color": "#303030",
            "header_color": "#0056b3",
            "accent_color": "#e0e0e0",
            "plot_bar_color": "#007bff", # Blue for light theme plots
            "plot_grid_color": "#cccccc"
        }

def apply_base_styles(is_dark_theme: bool):
    """
    Applies base CSS styles to the Streamlit app, adapting to the selected theme.
    This uses Streamlit's markdown with unsafe_allow_html to inject CSS.
    """
    colors = get_theme_colors(is_dark_theme)

    # Inject CSS using the actual hex values
    st.markdown(
        f"""
        <style>
        :root {{
            --bg-primary: {colors["bg_primary"]};
            --bg-secondary: {colors["bg_secondary"]};
            --text-color: {colors["text_color"]};
            --header-color: {colors["header_color"]};
            --accent-color: {colors["accent_color"]};
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            color: var(--text-color);
            background-color: var(--bg-primary);
        }}

        .stApp {{
            background-color: var(--bg-primary);
            color: var(--text-color);
        }}

        /* Apply background to main content and sidebar */
        .main .block-container {{
            background-color: var(--bg-primary);
            color: var(--text-color);
        }}
        .stSidebar {{
            background-color: var(--bg-secondary);
        }}
        .stSidebar > div:first-child {{
            background-color: var(--bg-secondary); /* Ensure sidebar background applies */
        }}

        /* Header styling */
        h1, h2, h3, h4, h5, h6 {{
            color: var(--header-color);
        }}

        /* Text elements */
        p, label, .stMarkdown, .stText {{
            color: var(--text-color);
        }}

        /* Buttons */
        .stButton>button {{
            background-color: var(--accent-color);
            color: var(--text-color);
            border-radius: 8px;
            border: 1px solid var(--text-color);
            padding: 0.5rem 1rem;
            transition: all 0.2s ease-in-out;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        }}
        .stButton>button:hover {{
            background-color: var(--header-color);
            color: white;
            border-color: var(--header-color);
            transform: translateY(-2px);
            box-shadow: 3px 3px 7px rgba(0,0,0,0.3);
        }}

        /* File Uploader */
        .stFileUploader > div > div {{
            background-color: var(--bg-secondary);
            border-radius: 8px;
            border: 1px dashed var(--text-color);
            padding: 1rem;
        }}
        .stFileUploader label {{
            color: var(--text-color);
        }}

        /* Input Fields (Text Area, Text Input) */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
            background-color: var(--bg-secondary);
            color: var(--text-color);
            border: 1px solid var(--text-color);
            border-radius: 8px;
            padding: 0.5rem;
        }}
        .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {{
            border-color: var(--header-color);
            box-shadow: 0 0 0 0.2rem rgba(88, 166, 255, 0.25); /* Focus glow */
        }}

        /* Spinner */
        .stSpinner > div > span {{
            color: var(--header-color);
        }}

        /* Info/Success/Warning/Error boxes */
        .stAlert {{
            border-radius: 8px;
        }}
        .stAlert.info-alert {{
            background-color: rgba(100, 149, 237, 0.2); /* CornflowerBlue with transparency */
            border-left: 5px solid #6495ed;
            color: var(--text-color);
        }}
        .stAlert.success-alert {{
            background-color: rgba(40, 167, 69, 0.2); /* Green with transparency */
            border-left: 5px solid #28a745;
            color: var(--text-color);
        }}
        .stAlert.warning-alert {{
            background-color: rgba(255, 193, 7, 0.2); /* Yellow with transparency */
            border-left: 5px solid #ffc107;
            color: var(--text-color);
        }}
        .stAlert.error-alert {{
            background-color: rgba(220, 53, 69, 0.2); /* Red with transparency */
            border-left: 5px solid #dc3545;
            color: var(--text-color);
        }}

        /* Chat messages */
        .stChatMessage {{
            background-color: var(--bg-secondary);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 0.5rem;
        }}
        .stChatMessage.st-chat-message-user {{
            background-color: rgba(88, 166, 255, 0.1); /* Lighter blue for user messages */
            border: 1px solid rgba(88, 166, 255, 0.2);
            align-self: flex-end;
        }}
        .stChatMessage.st-chat-message-assistant {{
            background-color: var(--bg-secondary);
            border: 1px solid var(--text-color);
            align-self: flex-start;
        }}

        /* Dataframes */
        .stDataFrame {{
            background-color: var(--bg-secondary);
            color: var(--text-color);
            border-radius: 8px;
        }}
        .stDataFrame .css-1dp5o7x {{ /* Header row */
            background-color: var(--accent-color);
        }}
        .stDataFrame .css-1dp5o7x .css-1dp5o7x {{ /* Cell background */
            background-color: var(--bg-secondary);
        }}
        .stDataFrame .css-1dp5o7x .css-1dp5o7x > div {{ /* Cell text */
            color: var(--text-color);
        }}

        /* Progress Bar */
        .stProgress > div > div > div > div {{
            background-color: var(--header-color);
        }}

        /* Checkbox */
        .stCheckbox span {{
            color: var(--text-color);
        }}
        .stCheckbox div[data-testid="stCheckbox"] {{
            border-radius: 4px;
            border: 1px solid var(--text-color);
            background-color: var(--bg-secondary);
        }}
        .stCheckbox div[data-testid="stCheckbox"]:hover {{
            border-color: var(--header-color);
        }}
        .stCheckbox div[data-testid="stCheckbox"] > div {{
             background-color: var(--header-color); /* Checkmark color */
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

def set_theme_js(is_dark_theme: bool):
    """
    Sets the Streamlit theme using JavaScript to persist across reruns.
    This helps Streamlit's internal components align with the custom CSS.
    """
    theme_name = "dark" if is_dark_theme else "light"
    st.markdown(
        f"""
        <script>
            const body = window.parent.document.querySelector('body');
            if (body) {{
                if ('{theme_name}' === 'dark') {{
                    body.classList.remove('light');
                    body.classList.add('dark');
                }} else {{
                    body.classList.remove('dark');
                    body.classList.add('light');
                }}
            }}
        </script>
        """,
        unsafe_allow_html=True
    )
