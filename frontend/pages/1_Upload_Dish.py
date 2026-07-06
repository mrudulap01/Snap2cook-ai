import streamlit as st
import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from agents.orchestrator import Snap2CookOrchestrator
from utils.exporter import generate_recipe_pdf

st.set_page_config(page_title="Upload Dish - Snap2Cook", page_icon="📷", layout="wide")

st.title("Upload a Dish 📷")
st.write("Upload an image of a cooked dish to reverse-engineer its recipe.")

uploaded_file = st.file_uploader("Choose a dish image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(uploaded_file, caption="Uploaded Dish", use_container_width=True)
    
    if st.button("Analyze Dish & Generate Recipe", type="primary"):
        temp_path = "temp_dish.jpg"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        orchestrator = Snap2CookOrchestrator()
        
        try:
            with st.status("Running ADK Orchestrator...", expanded=True) as status:
                st.write("📷 Vision Agent analyzing image...")
                # We're running async inside sync Streamlit using asyncio.run
                result = asyncio.run(orchestrator.run_full_workflow(temp_path))
                status.update(label="Analysis Complete!", state="complete", expanded=False)
            
            dish = result.get("dish_analysis")
            recipe = result.get("original_recipe")
            
            # Save to session state for Pantry page to use
            st.session_state["recipe"] = recipe
            if "adaptation_result" in st.session_state:
                del st.session_state["adaptation_result"]
            
            with col2:
                st.success("Recipe Successfully Reconstructed!")
                
                st.header(f"🍽️ {recipe.dish_name}")
                st.markdown(f"*{recipe.description}*")
                
                # Recipe Metrics
                m1, m2, m3, m4, m5 = st.columns(5)
                m1.metric("Cuisine", recipe.cuisine)
                m2.metric("Difficulty", recipe.difficulty)
                m3.metric("Servings", recipe.servings)
                m4.metric("Prep Time", f"{recipe.prep_time}m")
                m5.metric("Cook Time", f"{recipe.cook_time}m")
                
                st.divider()
                
                # Nutrition
                st.subheader("📊 Nutrition (Per Serving)")
                n1, n2, n3, n4, n5, n6, n7 = st.columns(7)
                n1.metric("Cal", f"{recipe.nutrition.per_serving.calories}")
                n2.metric("Pro", f"{recipe.nutrition.per_serving.protein}g")
                n3.metric("Carb", f"{recipe.nutrition.per_serving.carbs}g")
                n4.metric("Fat", f"{recipe.nutrition.per_serving.fat}g")
                n5.metric("Fib", f"{recipe.nutrition.per_serving.fiber}g")
                n6.metric("Sug", f"{recipe.nutrition.per_serving.sugar}g")
                n7.metric("Sod", f"{recipe.nutrition.per_serving.sodium}mg")
                
                st.divider()
                
                # Ingredients & Steps
                tab1, tab2, tab3 = st.tabs(["🛒 Ingredients", "👨‍🍳 Cooking Instructions", "💡 Chef's Tips & Storage"])
                
                with tab1:
                    for ing in recipe.ingredients:
                        st.markdown(f"- **{ing.name}** - {ing.quantity} {ing.unit}")
                        
                with tab2:
                    for step in recipe.steps:
                        st.markdown(f"**Step {step.step_number}** (_{step.duration_minutes}m_)")
                        st.markdown(step.instruction)
                        st.info(f"**Expected Outcome:** {step.expected_outcome}")
                        st.markdown("---")
                
                with tab3:
                    with st.expander("Chef Tips", expanded=True):
                        for tip in recipe.chef_tips:
                            st.markdown(f"- 💡 {tip}")
                    with st.expander("Common Mistakes"):
                        for mistake in recipe.common_mistakes:
                            st.markdown(f"- ⚠️ {mistake}")
                    with st.expander("Storage"):
                        st.write(recipe.storage_instructions)
                        
                st.divider()
                pdf_bytes = generate_recipe_pdf(recipe)
                st.download_button("📥 Download Recipe as PDF", data=pdf_bytes, file_name=f"{recipe.dish_name.replace(' ', '_')}.pdf", mime="application/pdf")
                    
        except Exception as e:
            st.error(f"An error occurred during analysis: {str(e)}")
