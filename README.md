# Snap2Cook AI 🍳📸

![Snap2Cook Header](https://raw.githubusercontent.com/example/snap2cook/main/assets/header.png)

**Snap2Cook AI** is an intelligent, multi-agent cooking assistant that reverse-engineers a full recipe from a single photo of a cooked dish, and then dynamically adapts that recipe based on what you currently have in your pantry!

Built on the Google Agent Development Kit (ADK) architecture, this application utilizes **OpenRouter** and `google/gemini-2.5-flash` to execute advanced vision analysis, nutritional estimation, and intelligent culinary reasoning.

---

## 🌟 Key Features

1. **Upload Dish (Vision Analysis)**
   - Upload a photo of any cooked meal.
   - The AI identifies the dish, cuisine, visible ingredients, and cooking techniques.
   - It instantly reconstructs a cookbook-quality recipe with granular preparation steps, cook times, and chef's tips.
   - Generates a detailed nutritional breakdown (macros per serving and for the entire dish).
   
2. **My Pantry (Recipe Adaptation)**
   - Once a recipe is generated, upload a photo of your fridge or pantry.
   - The AI scans your available ingredients.
   - It calculates a **Compatibility Score** between your recipe and your pantry.
   - It completely rewrites the recipe, making intelligent substitutions (e.g., swapping heavy cream for cashew milk) and generates a missing items shopping list.

3. **PDF Export**
   - Instantly download your generated or adapted recipes as neatly formatted PDF files for easy printing or sharing.

---

## 🚀 How to Use the App

### Step 1: Discover a Recipe
1. Navigate to the **Upload Dish** page.
2. Click "Browse files" and upload a clear photo of a dish you want to cook (`.jpg` or `.png`).
3. Click **Analyze Dish & Generate Recipe**.
4. Review the generated ingredients, instructions, and nutrition facts. You can download it as a PDF!

### Step 2: Adapt to Your Pantry
1. With your recipe generated, navigate to the **My Pantry** page on the sidebar.
2. Upload a photo of your fridge, pantry shelves, or a countertop with ingredients.
3. Click **Analyze Pantry & Adapt Recipe**.
4. The AI will provide a new, adapted recipe using only what you have (or suggesting the closest substitutes), alongside a shopping list for what you're completely missing.

---

## 🛠️ Local Installation & Setup

If you want to run Snap2Cook AI on your own machine, follow these steps:

### Prerequisites
- Python 3.9 or higher
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/mrudulap01/Snap2cook-ai.git
cd Snap2cook-ai
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a file named `.env` in the root of the project directory. Add your AI API key and model preferences:
```env
AI_API_KEY=your_api_key_here
VISION_MODEL=google/gemini-2.5-flash
TEXT_MODEL=google/gemini-2.5-flash
```
*(You can obtain an API key by signing up at [OpenRouter.ai](https://openrouter.ai/) or your preferred provider)*

### 4. Run the Application
Start the Streamlit development server:
```bash
python -m streamlit run frontend/app.py
```
The app will automatically open in your web browser at `http://localhost:8501`.

---

## 🤖 Model Configuration (Provider Independence)

Snap2Cook is completely provider-independent. You can switch to DeepSeek, Qwen, Llama, Groq, or native OpenAI simply by editing your `.env` file! No code changes are required.

**Example 1: Using DeepSeek and Qwen via OpenRouter (Default)**
```env
AI_BASE_URL=https://openrouter.ai/api/v1
VISION_MODEL=qwen/qwen-2-vl-72b-instruct
TEXT_MODEL=deepseek/deepseek-chat
```

**Example 2: Using Native Google AI Studio**
```env
AI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
VISION_MODEL=gemini-2.5-flash
TEXT_MODEL=gemini-2.5-flash
```

**Example 3: Using Local Models via Ollama**
```env
AI_BASE_URL=http://localhost:11434/v1
VISION_MODEL=llava
TEXT_MODEL=llama3
```

---

## ☁️ Deployment Guide (Streamlit Community Cloud)

Snap2Cook is completely deployment-ready for Streamlit Community Cloud.

1. Create an account at [share.streamlit.io](https://share.streamlit.io/).
2. Click **New app** and connect your GitHub account.
3. Select the `mrudulap01/Snap2cook-ai` repository and the `main` branch.
4. Set the **Main file path** to: `frontend/app.py`.
5. Click **Advanced settings...** and add your Secrets:
   ```toml
   AI_API_KEY = "your_api_key_here"
   VISION_MODEL = "google/gemini-2.5-flash"
   TEXT_MODEL = "google/gemini-2.5-flash"
   ```
6. Click **Deploy!**

---

## 🏗️ Architecture

Snap2Cook employs a sophisticated multi-agent pipeline:

1. **Vision Analysis Agent**: Extracts entities and ingredients from images.
2. **Recipe Reconstruction Agent**: Formats culinary data into structured JSON models.
3. **Pantry Inventory Agent**: Detects available items from noisy environment images.
4. **Recipe Adaptation Agent**: Merges the original recipe with the available inventory to generate a new culinary path.

All communication is facilitated by a central **ADK Runner** that manages state and logging.
