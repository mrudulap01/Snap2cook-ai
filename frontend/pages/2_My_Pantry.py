import streamlit as st
import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from agents.orchestrator import Snap2CookOrchestrator
from utils.exporter import generate_recipe_pdf

st.set_page_config(page_title="My Pantry - Snap2Cook", page_icon="🥫", layout="wide")

st.title("My Pantry 🥫")
st.write("Upload an image of your fridge or pantry to adapt your generated recipe.")

recipe = st.session_state.get("recipe")

if not recipe:
    st.warning("⚠️ No recipe found! Please go to **Upload Dish** first to generate a recipe before coming here.")
else:
    st.info(f"Target Recipe: **{recipe.dish_name}**")
    
    uploaded_file = st.file_uploader("Choose a pantry image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(uploaded_file, caption="Uploaded Pantry", use_container_width=True)
            
            if st.button("Analyze Pantry & Adapt Recipe", type="primary"):
                temp_path = "temp_pantry.jpg"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                orchestrator = Snap2CookOrchestrator()
                
                try:
                    with st.status("Running ADK Adaptation...", expanded=True) as status:
                        st.write("🥫 Scanning pantry image...")
                        result_dict = asyncio.run(orchestrator.run_adaptation_workflow(temp_path, recipe))
                        result = result_dict["adaptation_result"]
                        
                        st.session_state["adaptation_result"] = result
                        status.update(label="Adaptation Complete!", state="complete", expanded=False)
                        st.success("Recipe Successfully Adapted!")
                        
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                        
        if "adaptation_result" in st.session_state:
            result = st.session_state["adaptation_result"]
            adapted = result.adapted_recipe
            
            with col2:
                # Compatibility Score
                st.subheader("🎯 Compatibility Score")
                score = result.compatibility_score
                color = "green" if score >= 80 else "orange" if score >= 50 else "red"
                st.markdown(f"<h2 style='color: {color};'>{score}% Pantry Match</h2>", unsafe_allow_html=True)
                st.write(result.compatibility_explanation)
                
                tab1, tab2, tab3, tab4 = st.tabs([
                    "🔄 Adapted Recipe",
                    "📝 Shopping List",
                    "🔀 Substitutions",
                    "✅ Available Items"
                ])
                
                with tab1:
                    st.markdown(f"### {adapted.dish_name}")
                    st.markdown(f"*{adapted.description}*")
                    
                    m1, m2, m3 = st.columns(3)
                    m1.metric("Servings", adapted.servings)
                    m2.metric("Total Time", f"{adapted.total_time} min")
                    m3.metric("Calories", f"{adapted.nutrition.per_serving.calories} kcal")
                    
                    st.markdown("#### Ingredients")
                    for ing in adapted.ingredients:
                        st.markdown(f"- **{ing.name}** - {ing.quantity} {ing.unit}")
                        
                    st.markdown("#### Instructions")
                    for step in adapted.steps:
                        st.markdown(f"**Step {step.step_number}**")
                        st.markdown(step.instruction)
                        st.markdown("---")
                        
                    pdf_bytes = generate_recipe_pdf(adapted)
                    st.download_button("📥 Download Adapted Recipe PDF", data=pdf_bytes, file_name=f"Adapted_{adapted.dish_name.replace(' ', '_')}.pdf", mime="application/pdf")
                
                with tab2:
                    if result.shopping_list:
                        for item in result.shopping_list:
                            st.markdown(f"- 🛒 {item}")
                    else:
                        st.success("You have everything you need! (including substitutes)")
                        
                with tab3:
                    if result.substitutions:
                        for sub in result.substitutions:
                            st.markdown(f"- **{sub.original_ingredient}** ➡️ **{sub.substitute}**")
                            st.markdown(f"  *Reason: {sub.reason}*")
                    else:
                        st.info("No substitutions were necessary.")
                        
                with tab4:
                    if result.available_ingredients:
                        for item in result.available_ingredients:
                            st.markdown(f"- {item}")
                    else:
                        st.warning("No original ingredients were found in your pantry.")
