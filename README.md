<div align="center">
  <!-- Banner Placeholder -->
  <img src="https://via.placeholder.com/1200x300.png?text=Snap2Cook+AI+Banner" alt="Snap2Cook AI Banner">
  
  <!-- Logo Placeholder -->
  <img src="https://via.placeholder.com/150x150.png?text=Logo" alt="Snap2Cook Logo" width="150" height="150">
  
  # Snap2Cook AI 🍳📸
  
  **Snap Any Dish. Cook It With What You Already Have.**
  
  <p align="center">
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9+-blue.svg?logo=python&logoColor=white" alt="Python"></a>
    <a href="https://developers.google.com/workspace/agents"><img src="https://img.shields.io/badge/Google-ADK-orange.svg?logo=google&logoColor=white" alt="Google ADK"></a>
    <a href="https://deepmind.google/technologies/gemini/"><img src="https://img.shields.io/badge/AI-Gemini_2.5_Flash-00A9E0.svg?logo=googlebard&logoColor=white" alt="Gemini"></a>
    <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Streamlit-UI-FF4B4B.svg?logo=streamlit&logoColor=white" alt="Streamlit"></a>
    <a href="https://modelcontextprotocol.io/"><img src="https://img.shields.io/badge/Architecture-MCP-4CAF50.svg" alt="MCP"></a>
    <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/Open%20Source-%E2%9D%A4-green.svg" alt="Open Source"></a>
  </p>
</div>

---

## 📖 Project Overview
Snap2Cook AI is an intelligent, multi-agent culinary assistant designed to bridge the gap between food discovery and home cooking. By leveraging state-of-the-art vision models and the **Google Agent Development Kit (ADK)**, Snap2Cook reverse-engineers a complete, cookbook-quality recipe from a single photo of a cooked dish. It then intelligently adapts that recipe based on a visual scan of your pantry, ensuring you can cook delicious meals without unnecessary grocery runs.

## ❗ Problem Statement
Food discovery often happens visually—through social media, menus, or cookbooks. However, translating a photo into a cookable recipe is difficult. Even when a recipe is found, home cooks frequently face the "missing ingredient" dilemma, leading to abandoned cooking plans or last-minute shopping trips.

## 💡 Solution
Snap2Cook AI eliminates culinary friction by providing an end-to-end, vision-driven cooking pipeline:
1. **Discover:** Snap a photo of a dish to generate an authentic recipe.
2. **Adapt:** Snap a photo of your fridge/pantry to dynamically rewrite the recipe using only what you have on hand.

---

## ✨ Features
- **👁️ AI Dish Recognition**: Accurately detects cuisine, distinct textures, and hidden ingredients from a single image.
- **👨‍🍳 Recipe Reconstruction**: Generates granular, step-by-step cooking instructions complete with estimated times and expected outcomes.
- **🥫 Pantry Analysis**: Identifies available ingredients from chaotic fridge or pantry photos.
- **🔀 Smart Ingredient Substitution**: Dynamically rewrites recipes, swapping out missing items with culinary-appropriate alternatives from your inventory.
- **📊 Deterministic Nutrition Analysis**: Calculates macros per serving using a strict, algorithmic Model Context Protocol (MCP) server integration.

---

## 🛠️ Tech Stack
- **Language**: Python 3.9+
- **Agent Framework**: Google Agent Development Kit (ADK) Architectures
- **Intelligence**: OpenRouter / Google Gemini 2.5 Flash / Meta Llama 3.1
- **UI/UX**: Streamlit
- **Validation**: Pydantic Strict Typing
- **Resiliency**: Tenacity (Exponential Backoff Retries)

---

## 🏗️ Architecture

### 1. Google ADK Workflow
Snap2Cook avoids the unreliability of autonomous "agent swarms" by implementing a strict, centralized orchestration pattern inspired by the **Google ADK**.
- **ADKRunner**: A centralized state machine that routes data sequentially.
- **ADKSession**: Provides immutable telemetry and logs every agent interaction.
- **Event Callbacks**: Hooks into Streamlit to provide real-time UI updates (`on_agent_start`, `on_agent_end`).
- **Chain of Thought (CoT)**: Enforced via Pydantic; agents must "think out loud" before finalizing their JSON outputs.

<!-- Architecture Diagram Placeholder -->
<div align="center">
  <img src="https://via.placeholder.com/800x400.png?text=System+Architecture+Diagram" alt="Architecture Diagram">
</div>

### 2. Model Context Protocol (MCP) Workflow
To ensure accuracy, the application decouples non-linguistic tasks from the LLM. Using a simulated **MCP Server**, the AI requests rigid, deterministic calculations:
- `get_nutrition()`: Algorithmic macronutrient calculation based on ingredient categories.
- `scale_recipe()`: Strict mathematical unit conversions and yield scaling.

---

## 📁 Folder Structure

```text
📦 snap2cook-ai
 ┣ 📂 agents/                # Core AI Agents (Vision, Pantry, Recipe, Adaptation)
 ┃ ┣ 📜 base_agent.py        # Abstract agent class
 ┃ ┣ 📜 callbacks.py         # ADK Event listeners for UI telemetry
 ┃ ┣ 📜 orchestrator.py      # Central state manager (ADK Runner)
 ┃ ┣ 📜 prompts.py           # Chain-of-Thought injected prompts
 ┃ ┗ 📜 sessions.py          # ADK Session logging
 ┣ 📂 config/                # Environment and app settings
 ┣ 📂 frontend/              # Streamlit User Interface
 ┃ ┣ 📜 app.py               # Home Landing Page
 ┃ ┗ 📂 pages/               # Upload Dish & My Pantry interfaces
 ┣ 📂 mcp_server/            # Simulated Model Context Protocol Server
 ┃ ┣ 📜 server.py            # MCP tool registry
 ┃ ┗ 📂 tools/               # Deterministic nutrition and conversion tools
 ┣ 📂 schemas/               # Strict Pydantic Data Models
 ┣ 📂 tests/                 # Pytest verification suites
 ┣ 📂 utils/                 # Resiliency wrappers and exporters
 ┣ 📜 requirements.txt       # Project dependencies
 ┗ 📜 README.md              # Project documentation
```

---

## 📸 Screenshots

<div align="center">
  <!-- Screenshot 1 Placeholder -->
  <img src="https://via.placeholder.com/800x450.png?text=Home+Page+Showcase" alt="Home Page">
  <br><br>
  <!-- Screenshot 2 Placeholder -->
  <img src="https://via.placeholder.com/800x450.png?text=Upload+Dish+Workflow" alt="Upload Dish">
  <br><br>
  <!-- Screenshot 3 Placeholder -->
  <img src="https://via.placeholder.com/800x450.png?text=Smart+Pantry+Adaptation" alt="My Pantry">
</div>

---

## ⚙️ Installation & Running Locally

### 1. Prerequisites
- **Python 3.9+**
- Git installed on your system

### 2. Clone the Repository
```bash
git clone https://github.com/mrudulap01/Snap2cook-ai.git
cd Snap2cook-ai
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the root directory. The application is completely provider-independent.

```env
# Primary API Key
AI_API_KEY=your_openrouter_or_gemini_key_here

# Base URL (Default: OpenRouter)
AI_BASE_URL=https://openrouter.ai/api/v1

# Model Selection
VISION_MODEL=google/gemini-2.5-flash
TEXT_MODEL=google/gemini-2.5-flash
FALLBACK_TEXT_MODEL=meta-llama/llama-3.1-70b-instruct
```

### 5. Start the Application
```bash
python -m streamlit run frontend/app.py
```
The app will launch in your browser at `http://localhost:8501`.

---

## ☁️ Deployment (Streamlit Community Cloud)
Snap2Cook is production-ready for immediate deployment.
1. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/).
2. Create a **New App** and select your GitHub repository.
3. Set the **Main file path** to `frontend/app.py`.
4. In **Advanced Settings**, add your environment variables as Streamlit Secrets:
   ```toml
   AI_API_KEY = "..."
   VISION_MODEL = "google/gemini-2.5-flash"
   TEXT_MODEL = "google/gemini-2.5-flash"
   ```
5. Click **Deploy!**

---

## 🚀 Future Scope
- **Multi-Modal Output**: Generate AI audio guides that read the recipe steps aloud while cooking.
- **Grocery Integration**: 1-click integration with Instacart or Amazon Fresh for the missing items shopping list.
- **Dietary Restrictions**: Strict toggle modes for Vegan, Keto, or Gluten-Free adaptations.

---

## 🤝 Contributing
Contributions are always welcome! 
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
