import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Content Assistant App",
    page_icon="✍️",
    layout="centered",
)

# -----------------------------
# Modern MHS UI
# -----------------------------
# -----------------------------
# Professional responsive UI
# -----------------------------
st.markdown("""
<style>
/* Keep the existing desktop/laptop design unchanged.
   Only improve form-label visibility on small screens. */
@media (max-width: 768px) {
    .stApp [data-testid="stWidgetLabel"] p,
    .stApp [data-testid="stWidgetLabel"] label,
    .stApp [data-testid="stWidgetLabel"] div {
        color: #111827 !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        line-height: 1.3 !important;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <span class="badge">POWERED BY MHS</span>
    <h1>✍️ AI Content Assistant App</h1>
    <p>Turn your ideas into engaging, platform-ready content in seconds.</p>
</div>
""", unsafe_allow_html=True)
# -----------------------------
# API key
# -----------------------------
api_key = os.getenv("GROQ_API_KEY")

with st.sidebar:
    st.header("⚙️ Settings")
    sidebar_key = st.text_input(
        "AI API Key",
        type="password",
        help="Enter your API key, or set GROQ_API_KEY as an environment variable.",
    )

    model = st.selectbox(
        "AI Model",
        [
            "openai/gpt-oss-120b"
        ],
        index=0,
    )

api_key = sidebar_key.strip() or api_key

# -----------------------------
# User inputs
# -----------------------------
st.markdown("### 📝 Content Details")
st.markdown('<div class="section-title">🎯 Content Settings</div>', unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
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

with col2:
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
    height=110,
)

col3, col4 = st.columns(2)

with col3:
    target_audience = st.text_input(
        "Target Audience",
        placeholder="Example: University students and beginner programmers",
    )

with col4:
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

st.markdown('</div>', unsafe_allow_html=True)
st.write("")

generate = st.button("✨ Generate Content", type="primary", use_container_width=True)

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

        # Display result in separate cards
        st.markdown('<div class="section-title">✨ Your Generated Content</div>', unsafe_allow_html=True)

        def section(text, marker, next_marker=None):
            pos = text.find(marker)
            if pos == -1:
                return ""
            pos += len(marker)
            end = len(text) if not next_marker else text.find(next_marker, pos)
            if end == -1:
                end = len(text)
            return text[pos:end].strip()

        title_text = section(result, "TITLE:", "POST:")
        post_text = section(result, "POST:", "CAPTION:")
        caption_text = section(result, "CAPTION:", "HASHTAGS:")
        hashtags_text = section(result, "HASHTAGS:")

        if title_text:
            st.markdown('<div class="card"><b>🎯 TITLE</b></div>', unsafe_allow_html=True)
            st.code(title_text, language=None)

        if post_text:
            st.markdown('<div class="card"><b>📝 POST</b></div>', unsafe_allow_html=True)
            st.code(post_text, language=None)

        if caption_text:
            st.markdown('<div class="card"><b>💬 CAPTION</b></div>', unsafe_allow_html=True)
            st.code(caption_text, language=None)

        if hashtags_text:
            st.markdown('<div class="card"><b>#️⃣ HASHTAGS</b></div>', unsafe_allow_html=True)
            st.code(hashtags_text, language=None)

        if not any([title_text, post_text, caption_text, hashtags_text]):
            st.markdown('<div class="card"><b>📄 GENERATED CONTENT</b></div>', unsafe_allow_html=True)
            st.code(result, language=None)

        st.download_button(
            "📥 Download Complete Content",
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


st.markdown('<div class="footer">AI Content Assistant · POWERED BY MHS</div>', unsafe_allow_html=True)

        
   
      
   
