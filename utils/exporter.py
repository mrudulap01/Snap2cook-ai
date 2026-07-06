from fpdf import FPDF
import io

def sanitize(text) -> str:
    if text is None: return "N/A"
    return str(text).encode('latin-1', 'replace').decode('latin-1')

def generate_recipe_pdf(recipe) -> bytes:
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Calculate effective page width manually since older fpdf/fpdf2 might not have .epw
        epw = pdf.w - pdf.l_margin - pdf.r_margin
        
        # Title
        pdf.set_font("Helvetica", "B", 24)
        pdf.multi_cell(epw, 10, txt=sanitize(recipe.dish_name), align='C')
        pdf.ln(5)
        
        # Description
        pdf.set_font("Helvetica", "I", 12)
        pdf.multi_cell(epw, 8, txt=sanitize(recipe.description))
        pdf.ln(5)
        
        # Meta
        pdf.set_font("Helvetica", "", 12)
        pdf.multi_cell(epw, 8, txt=sanitize(f"Cuisine: {recipe.cuisine} | Servings: {recipe.servings} | Difficulty: {recipe.difficulty}"))
        pdf.multi_cell(epw, 8, txt=sanitize(f"Prep Time: {recipe.prep_time}m | Cook Time: {recipe.cook_time}m | Total Time: {recipe.total_time}m"))
        pdf.ln(5)
        
        # Ingredients
        pdf.set_font("Helvetica", "B", 16)
        pdf.multi_cell(epw, 10, txt="Ingredients")
        pdf.set_font("Helvetica", "", 12)
        for ing in recipe.ingredients:
            pdf.multi_cell(epw, 6, txt=sanitize(f"- {ing.name}: {ing.quantity} {ing.unit}"))
        pdf.ln(5)
        
        # Instructions
        pdf.set_font("Helvetica", "B", 16)
        pdf.multi_cell(epw, 10, txt="Instructions")
        pdf.set_font("Helvetica", "", 12)
        for step in recipe.steps:
            pdf.multi_cell(epw, 6, txt=sanitize(f"Step {step.step_number}: {step.instruction}"))
            pdf.multi_cell(epw, 6, txt=sanitize(f"Duration: ~{step.duration_minutes}m | Outcome: {step.expected_outcome}"))
            pdf.ln(3)
            
        return pdf.output(dest="S").encode("latin1", "replace")
    except Exception as e:
        # Fallback if PDF generation completely fails, return a text file posing as a PDF so it doesn't crash the UI
        import logging
        logging.error(f"PDF Generation failed: {e}")
        return b"Error generating PDF. Please view the recipe on the web page."
