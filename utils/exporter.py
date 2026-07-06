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
        
        # Helper to forcefully reset X and render text
        def render_text(text, font, style, size, h=6, align='L'):
            pdf.set_font(font, style, size)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(0, h, txt=sanitize(text), align=align)

        # Title
        render_text(recipe.dish_name, "Helvetica", "B", 24, h=10, align='C')
        pdf.ln(5)
        
        # Description
        render_text(recipe.description, "Helvetica", "I", 12, h=8)
        pdf.ln(5)
        
        # Meta
        render_text(f"Cuisine: {recipe.cuisine} | Servings: {recipe.servings} | Difficulty: {recipe.difficulty}", "Helvetica", "", 12, h=8)
        render_text(f"Prep Time: {recipe.prep_time}m | Cook Time: {recipe.cook_time}m | Total Time: {recipe.total_time}m", "Helvetica", "", 12, h=8)
        pdf.ln(5)
        
        # Ingredients
        render_text("Ingredients", "Helvetica", "B", 16, h=10)
        for ing in recipe.ingredients:
            render_text(f"- {ing.name}: {ing.quantity} {ing.unit}", "Helvetica", "", 12, h=6)
        pdf.ln(5)
        
        # Instructions
        render_text("Instructions", "Helvetica", "B", 16, h=10)
        for step in recipe.steps:
            render_text(f"Step {step.step_number}: {step.instruction}", "Helvetica", "", 12, h=6)
            render_text(f"Duration: ~{step.duration_minutes}m | Outcome: {step.expected_outcome}", "Helvetica", "", 12, h=6)
            pdf.ln(3)
            
        out = pdf.output(dest="S")
        if isinstance(out, str):
            # PyFPDF (older) returns a latin-1 encoded string
            return out.encode("latin1", "replace")
        elif isinstance(out, bytearray):
            # fpdf2 >= 2.8 returns a bytearray
            return bytes(out)
        else:
            return bytes(out)
    except Exception as e:
        # Fallback if PDF generation completely fails, return a text file posing as a PDF so it doesn't crash the UI
        import logging
        logging.error(f"PDF Generation failed: {e}")
        return b"Error generating PDF. Please view the recipe on the web page."
