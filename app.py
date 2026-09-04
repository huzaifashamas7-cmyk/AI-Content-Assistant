import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✍️",
    layout="centered",
)

st.title("✍️ AI Content Assistant")
st.caption("Create platform-ready social media content with a free Groq model.")

# -----------------------------
# API key
# -----------------------------
api_key = os.getenv("GROQ_API_KEY")

with st.sidebar:
    st.header("⚙️ Settings")
    sidebar_key = st.text_input(
        "Groq API Key",
        type="password",
        help="You can also set GROQ_API_KEY as an environment variable.",
    )

    model = st.selectbox(
        "Groq Model",
        [
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
        ],
        index=0,
    )

api_key = sidebar_key.strip() or api_key

# -----------------------------
# User inputs
# -----------------------------
content_type = st.selectbox(
    "Content Type",
    [
        "Social Media Post",
        "Educational Post",
        "Promotional Post",
        "Product Announcement",
        "Storytelling Post",
        "Motivational Post",
        "Question / Engagement Post",
        "Event Announcement",
    ],
)

platform = st.selectbox(
    "Platform",
    [
        "Instagram",
        "Facebook",
        "LinkedIn",
        "X (Twitter)",
        "TikTok",
        "YouTube Community",
    ],
)

topic = st.text_area(
    "Topic",
    placeholder="Example: Benefits of learning Python for beginners",
    height=100,
)

target_audience = st.text_input(
    "Target Audience",
    placeholder="Example: University students and beginner programmers",
)

tone = st.selectbox(
    "Tone",
    [
        "Professional",
        "Friendly",
        "Casual",
        "Educational",
        "Funny",
        "Inspirational",
        "Persuasive",
        "Creative",
    ],
)

generate = st.button("🚀 Generate Content", type="primary", use_container_width=True)

# -----------------------------
# Generate content
# -----------------------------
if generate:
    if not api_key:
        st.error("Please enter your Groq API key in the sidebar or set GROQ_API_KEY.")
        st.stop()

    if not topic.strip():
        st.warning("Please enter a topic.")
        st.stop()

    if not target_audience.strip():
        st.warning("Please enter the target audience.")
        st.stop()

    try:
        client = Groq(api_key=api_key)

        system_prompt = """
You are an expert social media content writer and content strategist.

Create high-quality, original social media content based strictly on the
user's selected content type, platform, topic, target audience, and tone.

Return the result using EXACTLY this structure:

TITLE:
A short, attention-grabbing title.

POST:
The complete ready-to-publish post. Make it appropriate for the selected
platform and target audience. Use natural formatting, short paragraphs,
and emojis only when they fit the tone.

CAPTION:
A concise, engaging caption suitable for the selected platform.

HASHTAGS:
Provide 8-12 relevant hashtags. Do not use generic or unrelated hashtags.

Do not include explanations, notes, or markdown code fences outside these sections.
"""

        user_prompt = f"""
Content Type: {content_type}
Platform: {platform}
Topic: {topic.strip()}
Target Audience: {target_audience.strip()}
Tone: {tone}

Generate the complete content now.
"""

        with st.spinner("Creating your content..."):
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=1200,
            )

        result = response.choices[0].message.content.strip()

        st.success("Content generated successfully!")

        # Display result
        st.subheader("✨ Generated Content")
        st.text_area(
            "Ready to copy",
            value=result,
            height=500,
        )

        st.download_button(
            "📥 Download as TXT",
            data=result,
            file_name="ai_content.txt",
            mime="text/plain",
            use_container_width=True,
        )

    except Exception as e:
        st.error(f"Something went wrong: {e}")
        st.info(
            "Check that your Groq API key is valid and that you have internet access."
        )
