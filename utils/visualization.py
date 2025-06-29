import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter
# Import the function to get theme colors
from utils.styling import get_theme_colors

def plot_discussion_topics(topics: list[str], is_dark_theme: bool):
    """
    Generates and displays a bar chart of the most common discussion topics.

    Args:
        topics (list[str]): A list of discussion topics extracted from the meeting.
                            Each element in the list is expected to be a single topic string.
        is_dark_theme (bool): True if the dark theme is active, False otherwise.
    """
    if not topics:
        st.info("No topics available to generate a chart.")
        return

    # Get the current theme colors
    colors = get_theme_colors(is_dark_theme)

    # Count the frequency of each topic
    topic_counts = Counter(topics)

    num_top_topics = min(len(topic_counts), 10) # Display top 10 or fewer if less are available
    top_n_topics = topic_counts.most_common(num_top_topics)

    if not top_n_topics:
        st.info("Not enough distinct topics to generate a meaningful chart.")
        return

    # Prepare data for plotting
    labels = [item[0].title() for item in top_n_topics]
    values = [item[1] for item in top_n_topics]

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Use color from theme
    ax.bar(labels, values, color=colors["plot_bar_color"]) 
    
    # Set text colors using theme colors
    ax.set_title('Top Discussion Topics', color=colors["text_color"])
    ax.set_xlabel('Topics', color=colors["text_color"])
    ax.set_ylabel('Frequency', color=colors["text_color"])
    
    plt.xticks(rotation=45, ha='right', color=colors["text_color"])
    plt.yticks(color=colors["text_color"])
    
    # Grid lines and their color
    plt.grid(axis='y', linestyle='--', alpha=0.7, color=colors["plot_grid_color"])
    
    plt.tight_layout()

    # Set plot and axes background colors using theme colors
    fig.patch.set_facecolor(colors["bg_primary"])
    ax.set_facecolor(colors["bg_secondary"])
    
    # Set spine (border) colors
    ax.spines['top'].set_color(colors["text_color"])
    ax.spines['right'].set_color(colors["text_color"])
    ax.spines['bottom'].set_color(colors["text_color"])
    ax.spines['left'].set_color(colors["text_color"])

    st.pyplot(fig)
