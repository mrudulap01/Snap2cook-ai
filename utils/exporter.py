from fpdf import FPDF
import io

def generate_recipe_pdf(recipe) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Helvetica", "B", 24)
    pdf.cell(200, 10, txt=recipe.dish_name, ln=True, align='C')
    pdf.ln(5)
    
    # Description
    pdf.set_font("Helvetica", "I", 12)
    pdf.multi_cell(0, 10, txt=recipe.description)
    pdf.ln(5)
    
    # Meta
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(200, 10, txt=f"Cuisine: {recipe.cuisine} | Servings: {recipe.servings} | Difficulty: {recipe.difficulty}", ln=True)
    pdf.cell(200, 10, txt=f"Prep Time: {recipe.prep_time}m | Cook Time: {recipe.cook_time}m | Total Time: {recipe.total_time}m", ln=True)
    pdf.ln(5)
    
    # Ingredients
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(200, 10, txt="Ingredients", ln=True)
    pdf.set_font("Helvetica", "", 12)
    for ing in recipe.ingredients:
        pdf.cell(200, 8, txt=f"- {ing.name}: {ing.quantity} {ing.unit}", ln=True)
    pdf.ln(5)
    
    # Instructions
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(200, 10, txt="Instructions", ln=True)
    pdf.set_font("Helvetica", "", 12)
    for step in recipe.steps:
        pdf.multi_cell(0, 8, txt=f"Step {step.step_number}: {step.instruction}")
        pdf.multi_cell(0, 8, txt=f"Duration: ~{step.duration_minutes}m | Outcome: {step.expected_outcome}")
        pdf.ln(3)
        
    return pdf.output(dest="S").encode("latin1", "replace") # FPDF outputs as byte string in S mode
