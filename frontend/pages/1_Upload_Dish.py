import streamlit as st
import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from agents.orchestrator import Snap2CookOrchestrator
from utils.exporter import generate_recipe_pdf

st.set_page_config(page_title="Upload Dish - Snap2Cook", page_icon="📷", layout="wide")

# Inject Custom CSS for premium feel
st.markdown("""
<style>
    .recipe-card {
        background-color: #1e1e1e;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        border: 1px solid #333;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-container {
        display: flex;
        justify-content: space-between;
        background-color: #2b2b2b;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 16px;
    }
    .st-emotion-cache-1wivap2 {
        border-radius: 12px; /* rounded images */
    }
</style>
""", unsafe_allow_html=True)

st.title("Upload a Dish 📷")
st.markdown("<p style='color: #a0a0a0; font-size: 1.1rem;'>Upload an image of a cooked dish. Our AI will instantly reverse-engineer the ingredients and provide a cookbook-quality recipe.</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drag and drop your dish image here...", 
    type=["jpg", "jpeg", "png"], 
    help="We recommend well-lit photos where the ingredients are clearly visible."
)

if uploaded_file is not None:
    # Upload Success Animation
    if "dish_uploaded" not in st.session_state:
        st.toast("Image successfully uploaded!", icon="🎉")
        st.session_state["dish_uploaded"] = True

    col1, col2 = st.columns([1.2, 2])
    
    with col1:
        st.markdown("<div class='recipe-card'>", unsafe_allow_html=True)
        st.image(uploaded_file, caption="Your Uploaded Dish", use_container_width=True)
        
        # Remove Image Option (Streamlit native way is 'X' on uploader, but we add a visual reset)
        if st.button("❌ Clear & Upload New Image", use_container_width=True):
            st.session_state.clear()
            st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        analyze_btn = st.button("✨ Analyze Dish & Generate Recipe", type="primary", use_container_width=True)
    
    if analyze_btn:
        temp_path = "temp_dish.jpg"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        orchestrator = Snap2CookOrchestrator()
        
        with col2:
            st.markdown("### Processing Workflow")
            progress_bar = st.progress(0)
            status_container = st.container()
            
            # UX: ADK Event Callbacks for dynamic steps
            def ui_start_callback(agent_name, payload):
                st.toast(f"🤖 {agent_name} is thinking...", icon="⚙️")
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
                    st.markdown("✔ **Success:** Image Uploaded")
                
                # We're running async inside sync Streamlit using asyncio.run
                result = asyncio.run(orchestrator.run_full_workflow(temp_path))
                
                progress_bar.progress(100)
                with status_container:
                    st.markdown("✔ **Success:** Final Recipe Ready!")
                st.balloons()
                
                dish = result.get("dish_analysis")
                recipe = result.get("original_recipe")
                
                # Save to session state
                st.session_state["recipe"] = recipe
                st.session_state["dish_processed"] = True
                if "adaptation_result" in st.session_state:
                    del st.session_state["adaptation_result"]
                    
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")

    # Show Recipe if Processed
    if st.session_state.get("dish_processed") and "recipe" in st.session_state:
        recipe = st.session_state["recipe"]
        
        with col2:
            st.markdown("<div class='recipe-card'>", unsafe_allow_html=True)
            st.success("Recipe Successfully Reconstructed!")
            
            st.header(f"🍽️ {recipe.dish_name}")
            st.markdown(f"*{recipe.description}*")
            
            # Overview Metrics
            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("🌍 Cuisine", recipe.cuisine)
            m2.metric("⭐ Diff", recipe.difficulty)
            m3.metric("🍽️ Serves", recipe.servings)
            m4.metric("🔪 Prep", f"{recipe.prep_time}m")
            m5.metric("🔥 Cook", f"{recipe.cook_time}m")
            
            st.divider()
            
            # Nutrition Row
            st.markdown("#### 📊 Nutrition (Per Serving)")
            n1, n2, n3, n4, n5, n6 = st.columns(6)
            n1.metric("🔥 Cal", f"{recipe.nutrition.per_serving.calories}")
            n2.metric("🥩 Pro", f"{recipe.nutrition.per_serving.protein}g")
            n3.metric("🥖 Carb", f"{recipe.nutrition.per_serving.carbs}g")
            n4.metric("🧈 Fat", f"{recipe.nutrition.per_serving.fat}g")
            n5.metric("🥦 Fib", f"{recipe.nutrition.per_serving.fiber}g")
            n6.metric("🍬 Sug", f"{recipe.nutrition.per_serving.sugar}g")
            
            st.divider()
            
            tab_ing, tab_inst, tab_tips = st.tabs(["🛒 Ingredients", "👨‍🍳 Instructions", "💡 Tips & Storage"])
            
            with tab_ing:
                for ing in recipe.ingredients:
                    st.markdown(f"- **{ing.quantity} {ing.unit}** {ing.name}")
                    
            with tab_inst:
                for step in recipe.steps:
                    st.markdown(f"#### Step {step.step_number} ⏱️ {step.duration_minutes}m")
                    st.write(step.instruction)
                    st.info(f"**🎯 Expected Outcome:** {step.expected_outcome}")
            
            with tab_tips:
                with st.expander("👨‍🍳 Chef's Tips", expanded=True):
                    for tip in recipe.chef_tips:
                        st.markdown(f"- 💡 {tip}")
                with st.expander("⚠️ Common Mistakes"):
                    for mistake in recipe.common_mistakes:
                        st.markdown(f"- 🚫 {mistake}")
                with st.expander("🥡 Storage & Serving"):
                    st.write(f"**Storage:** {recipe.storage_instructions}")
                    st.write(f"**Serving:** {recipe.serving_suggestions}")
            
            st.divider()
            
            # EXPORT BUTTONS
            st.markdown("### 📤 Export & Share")
            e1, e2 = st.columns(2)
            
            with e1:
                pdf_bytes = generate_recipe_pdf(recipe)
                st.download_button("📥 Download Recipe (PDF)", data=pdf_bytes, file_name=f"{recipe.dish_name.replace(' ', '_')}.pdf", mime="application/pdf", use_container_width=True)
                
            with e2:
                # Format a nice markdown block for the user to copy
                md_export = f"# {recipe.dish_name}\n\n{recipe.description}\n\n## Ingredients\n"
                for i in recipe.ingredients: md_export += f"- {i.quantity} {i.unit} {i.name}\n"
                md_export += "\n## Instructions\n"
                for s in recipe.steps: md_export += f"{s.step_number}. {s.instruction}\n"
                
                with st.expander("📋 Copy Recipe to Clipboard"):
                    st.code(md_export, language="markdown")
            
            st.markdown("</div>", unsafe_allow_html=True)
