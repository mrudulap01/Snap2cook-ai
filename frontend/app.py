import streamlit as st

st.set_page_config(
    page_title="Snap2Cook AI",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global CSS for Premium UI
st.markdown("""
<style>
    /* Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Premium Headers */
    h1 {
        font-weight: 700;
        letter-spacing: -1px;
    }
    
    h2, h3 {
        font-weight: 600;
        letter-spacing: -0.5px;
    }

    /* Cards */
    .feature-card {
        background-color: #1e1e1e;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border: 1px solid #333;
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.2);
        border-color: #4CAF50;
    }
    
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 16px;
    }
    
    .feature-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 8px;
        color: #ffffff;
    }
    
    .feature-desc {
        color: #a0a0a0;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    /* Workflow */
    .workflow-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 20px;
        margin: 40px 0;
        flex-wrap: wrap;
    }
    .workflow-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .workflow-icon {
        background-color: #2b2b2b;
        border-radius: 50%;
        width: 80px;
        height: 80px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 2rem;
        margin-bottom: 12px;
        border: 2px solid #4CAF50;
    }
    .workflow-arrow {
        font-size: 1.5rem;
        color: #4CAF50;
    }
    
    /* Tagline */
    .tagline {
        font-size: 1.5rem;
        color: #888;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Metrics Override */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    /* Make st.info and st.success pop */
    .stAlert {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-bottom: 0;'>Snap2Cook AI 🍳📸</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;' class='tagline'>Snap Any Dish. Cook It With What You Already Have.</p>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; max-width: 800px; margin: 0 auto 3rem auto; color: #bbb; font-size: 1.1rem; line-height: 1.6;'>
    Welcome to the ultimate culinary AI assistant. Powered by Google's Agent Development Kit (ADK), Snap2Cook reverse-engineers recipes directly from photos and dynamically adapts them to the ingredients sitting in your fridge.
</div>
""", unsafe_allow_html=True)

# Workflow Section
st.markdown("""
<div class="workflow-container">
    <div class="workflow-step">
        <div class="workflow-icon">📷</div>
        <div style="font-weight:600">Upload Dish</div>
    </div>
    <div class="workflow-arrow">➜</div>
    <div class="workflow-step">
        <div class="workflow-icon">📝</div>
        <div style="font-weight:600">Generate Recipe</div>
    </div>
    <div class="workflow-arrow">➜</div>
    <div class="workflow-step">
        <div class="workflow-icon">🥫</div>
        <div style="font-weight:600">Upload Pantry</div>
    </div>
    <div class="workflow-arrow">➜</div>
    <div class="workflow-step">
        <div class="workflow-icon">🔄</div>
        <div style="font-weight:600">Adapt Recipe</div>
    </div>
    <div class="workflow-arrow">➜</div>
    <div class="workflow-step">
        <div class="workflow-icon">🛒</div>
        <div style="font-weight:600">Shopping List</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# Features Section
st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>Premium AI Capabilities</h2>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">👁️</div>
        <div class="feature-title">AI Dish Recognition</div>
        <div class="feature-desc">State-of-the-art vision models analyze your food photos to detect cuisine, hidden ingredients, and preparation techniques with striking accuracy.</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">👨‍🍳</div>
        <div class="feature-title">Recipe Reconstruction</div>
        <div class="feature-desc">Generates cookbook-quality recipes complete with accurate measurements, precise step-by-step instructions, and chef's tips.</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Nutrition Analysis</div>
        <div class="feature-desc">Deterministically calculates macros per serving (Calories, Protein, Fat, Carbs, Sugar) using algorithmic MCP server tools.</div>
    </div>
    """, unsafe_allow_html=True)

st.write("") # Spacer

c4, c5 = st.columns([1, 1])
with c4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🥫</div>
        <div class="feature-title">Pantry Analysis</div>
        <div class="feature-desc">Simply upload a picture of your chaotic fridge or pantry shelves. The AI will extract all visible, usable ingredients for your recipe.</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔀</div>
        <div class="feature-title">Smart Substitution</div>
        <div class="feature-desc">Missing something? The AI adapts the recipe around what you have, swapping ingredients dynamically while preserving flavor profiles.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br><div style='text-align: center;'><a href='/Upload_Dish' target='_self' style='background-color: #4CAF50; color: white; padding: 14px 28px; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 1.1rem; transition: background 0.3s;'>Get Started Now 🚀</a></div>", unsafe_allow_html=True)
