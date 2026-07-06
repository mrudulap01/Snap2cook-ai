from fpdf import FPDF
import io

def sanitize(text) -> str:
    if text is None: return ""
    # FPDF core fonts only support latin-1. Replace unknown chars (like emojis) with '?'
    return str(text).encode('latin-1', 'replace').decode('latin-1')

def generate_recipe_pdf(recipe) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Helvetica", "B", 24)
    pdf.cell(0, 10, txt=sanitize(recipe.dish_name), ln=True, align='C')
    pdf.ln(5)
    
    # Description
    pdf.set_font("Helvetica", "I", 12)
    pdf.multi_cell(0, 10, txt=sanitize(recipe.description))
    pdf.ln(5)
    
    # Meta
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 8, txt=sanitize(f"Cuisine: {recipe.cuisine} | Servings: {recipe.servings} | Difficulty: {recipe.difficulty}"))
    pdf.multi_cell(0, 8, txt=sanitize(f"Prep Time: {recipe.prep_time}m | Cook Time: {recipe.cook_time}m | Total Time: {recipe.total_time}m"))
    pdf.ln(5)
    
    # Ingredients
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, txt="Ingredients", ln=True)
    pdf.set_font("Helvetica", "", 12)
    for ing in recipe.ingredients:
        pdf.multi_cell(0, 6, txt=sanitize(f"- {ing.name}: {ing.quantity} {ing.unit}"))
    pdf.ln(5)
    
    # Instructions
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, txt="Instructions", ln=True)
    pdf.set_font("Helvetica", "", 12)
    for step in recipe.steps:
        pdf.multi_cell(0, 6, txt=sanitize(f"Step {step.step_number}: {step.instruction}"))
        pdf.multi_cell(0, 6, txt=sanitize(f"Duration: ~{step.duration_minutes}m | Outcome: {step.expected_outcome}"))
        pdf.ln(3)
        
    return pdf.output(dest="S").encode("latin1", "replace") # FPDF outputs as byte string in S mode
