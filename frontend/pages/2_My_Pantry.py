import streamlit as st
import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from agents.orchestrator import Snap2CookOrchestrator
from utils.exporter import generate_recipe_pdf

st.set_page_config(page_title="My Pantry - Snap2Cook", page_icon="🥫", layout="wide")

# Inject Custom CSS for premium feel
st.markdown("""
<style>
    .pantry-card {
        background-color: #1e1e1e;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        border: 1px solid #333;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .score-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: #2b2b2b;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        text-align: center;
    }
    .score-value {
        font-size: 3.5rem;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 8px;
    }
    .st-emotion-cache-1wivap2 {
        border-radius: 12px; /* rounded images */
    }
    .sub-item {
        background: #2b2b2b;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 4px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

st.title("My Pantry 🥫")
st.markdown("<p style='color: #a0a0a0; font-size: 1.1rem;'>Upload an image of your fridge or pantry to adapt your generated recipe based on what you actually have.</p>", unsafe_allow_html=True)

recipe = st.session_state.get("recipe")

if not recipe:
    st.warning("⚠️ No target recipe found! Please go to **Upload Dish** first to generate a recipe.")
else:
    st.info(f"🎯 **Target Recipe:** {recipe.dish_name}")
    
    uploaded_file = st.file_uploader(
        "Drag and drop your pantry image here...", 
        type=["jpg", "jpeg", "png"],
        help="Open your fridge or pantry and snap a photo. Make sure ingredients are visible."
    )
    
    if uploaded_file is not None:
        if "pantry_uploaded" not in st.session_state:
            st.toast("Pantry image uploaded!", icon="🎉")
            st.session_state["pantry_uploaded"] = True
            
        col1, col2 = st.columns([1.2, 2])
        
        with col1:
            st.markdown("<div class='pantry-card'>", unsafe_allow_html=True)
            st.image(uploaded_file, caption="Your Uploaded Pantry", use_container_width=True)
            
            if st.button("❌ Clear & Upload New Image", use_container_width=True):
                st.session_state.pop("pantry_uploaded", None)
                st.session_state.pop("adaptation_result", None)
                st.session_state.pop("pantry_processed", None)
                st.rerun()
                
            st.markdown("</div>", unsafe_allow_html=True)
            
            analyze_btn = st.button("✨ Analyze Pantry & Adapt Recipe", type="primary", use_container_width=True)
            
        if analyze_btn:
            temp_path = "temp_pantry.jpg"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            orchestrator = Snap2CookOrchestrator()
            
            with col2:
                st.markdown("### Processing Workflow")
                progress_bar = st.progress(0)
                status_container = st.container()
                
                # UX: ADK Event Callbacks
                def ui_start_callback(agent_name, payload):
                    st.toast(f"🤖 {agent_name} is processing...", icon="⚙️")
                    with status_container:
                        st.markdown(f"⏳ **Processing:** {agent_name}...")
                        
                def ui_end_callback(agent_name, result, time):
                    st.toast(f"✅ {agent_name} completed in {time:.1f}s!", icon="✨")
                    with status_container:
                        st.markdown(f"✔ **Success:** {agent_name} completed!")
                        
                orchestrator.runner.callbacks.register_callback("agent_start", ui_start_callback)
                orchestrator.runner.callbacks.register_callback("agent_end", ui_end_callback)
                
                try:
                    with status_container:
                        st.markdown("✔ **Success:** Pantry Image Uploaded")
                        
                    result_dict = asyncio.run(orchestrator.run_adaptation_workflow(temp_path, recipe))
                    
                    progress_bar.progress(100)
                    with status_container:
                        st.markdown("✔ **Success:** Recipe Successfully Adapted!")
                    st.balloons()
                    
                    st.session_state["adaptation_result"] = result_dict["adaptation_result"]
                    st.session_state["pantry_processed"] = True
                            
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                            
        if st.session_state.get("pantry_processed") and "adaptation_result" in st.session_state:
            result = st.session_state["adaptation_result"]
            adapted = result.adapted_recipe
            
            with col2:
                st.markdown("<div class='pantry-card'>", unsafe_allow_html=True)
                
                # Compatibility Score Visualizer
                score = result.compatibility_score
                color = "#4CAF50" if score >= 80 else "#FF9800" if score >= 50 else "#F44336"
                
                st.markdown(f"""
                <div class='score-container'>
                    <div style='color: #a0a0a0; font-size: 1.1rem; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px;'>Compatibility Score</div>
                    <div class='score-value' style='color: {color};'>{score}%</div>
                    <div style='color: #ccc; max-width: 80%;'>{result.compatibility_explanation}</div>
                </div>
                """, unsafe_allow_html=True)
                
                tab_adapted, tab_shop, tab_sub, tab_avail = st.tabs([
                    "🔄 Adapted Recipe",
                    "📝 Shopping List",
                    "🔀 Substitutions",
                    "✅ Available Items"
                ])
                
                with tab_adapted:
                    st.markdown(f"### 🍽️ {adapted.dish_name}")
                    st.markdown(f"*{adapted.description}*")
                    
                    m1, m2, m3 = st.columns(3)
                    m1.metric("🍽️ Servings", adapted.servings)
                    m2.metric("⏱️ Total Time", f"{adapted.total_time} min")
                    m3.metric("🔥 Calories", f"{adapted.nutrition.per_serving.calories}")
                    
                    st.divider()
                    st.markdown("#### 🛒 Ingredients")
                    for ing in adapted.ingredients:
                        st.markdown(f"- **{ing.quantity} {ing.unit}** {ing.name}")
                        
                    st.markdown("#### 👨‍🍳 Instructions")
                    for step in adapted.steps:
                        st.markdown(f"**Step {step.step_number}**")
                        st.write(step.instruction)
                        st.markdown("---")
                
                with tab_shop:
                    st.markdown("### 📝 Missing Items to Buy")
                    if result.shopping_list:
                        for item in result.shopping_list:
                            st.markdown(f"- [ ] {item}")
                    else:
                        st.success("🎉 You have everything you need! (including substitutes)")
                        
                with tab_sub:
                    st.markdown("### 🔀 Smart Substitutions Made")
                    if result.substitutions:
                        for sub in result.substitutions:
                            st.markdown(f"""
                            <div class='sub-item'>
                                <div style='font-size: 1.1rem; font-weight: 600;'>{sub.original_ingredient} ➔ {sub.substitute}</div>
                                <div style='color: #aaa; font-size: 0.9rem; margin-top: 4px;'>💡 {sub.reason}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No substitutions were necessary.")
                        
                with tab_avail:
                    st.markdown("### ✅ Found in your Pantry")
                    if result.available_ingredients:
                        for item in result.available_ingredients:
                            st.markdown(f"- {item}")
                    else:
                        st.warning("No original ingredients were found in your pantry.")
                        
                st.divider()
                
                # EXPORT BUTTONS
                st.markdown("### 📤 Export & Share")
                e1, e2 = st.columns(2)
                
                with e1:
                    pdf_bytes = generate_recipe_pdf(adapted)
                    st.download_button("📥 Download Adapted Recipe (PDF)", data=pdf_bytes, file_name=f"Adapted_{adapted.dish_name.replace(' ', '_')}.pdf", mime="application/pdf", use_container_width=True)
                    
                with e2:
                    shop_export = "# Shopping List\n\n"
                    for item in result.shopping_list: shop_export += f"- [ ] {item}\n"
                    
                    with st.expander("📋 Copy Shopping List"):
                        st.code(shop_export, language="markdown")

                st.markdown("</div>", unsafe_allow_html=True)
