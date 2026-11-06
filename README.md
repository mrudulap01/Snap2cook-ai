# 🍳 Snap2Cook AI
### Snap Any Dish. Recreate It. Adapt It. Cook It.

**An AI-powered Multi-Agent Culinary Assistant for Recipe Reconstruction and Smart Pantry-Based Adaptation.**

Snap2Cook AI transforms the way people discover and prepare food. By combining computer vision, Large Language Models (LLMs), multi-agent orchestration, and deterministic tools, it turns a picture of a cooked dish into a structured recipe and intelligently adapts that recipe using ingredients available in your pantry.

Instead of simply identifying food, Snap2Cook AI attempts to answer two practical questions:

- How can I recreate this dish?
- Can I make it with the ingredients I already have?

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Our Solution](#-our-solution)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Multi-Agent Workflow](#-multi-agent-workflow)
- [MCP Tools](#-model-context-protocol-mcp-tools)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation and Setup](#-installation-and-setup)
- [Running the Application](#-running-the-application)
- [Testing](#-testing)
- [Future Scope](#-future-scope)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📖 Overview

Snap2Cook AI is an intelligent, vision-driven cooking assistant that reconstructs recipes from food images and adapts them according to the ingredients available at home.

The application follows a structured multi-agent architecture orchestrated using Google Agent Development Kit (ADK)-based workflow patterns.

Users provide two inputs:

1. **Dish Image:** An image of a prepared dish that needs to be recreated.
2. **Pantry Image:** An image of available ingredients in the kitchen.

The system processes these inputs through specialized AI agents, reconstructs the original recipe, analyzes pantry availability, and generates an adapted recipe with ingredient substitutions and actionable cooking information.

The goal is to make cooking more accessible, reduce unnecessary grocery purchases, and help users make better use of available ingredients.

---

## ❗ Problem Statement

People frequently discover interesting dishes through social media, restaurants, food blogs, and photographs.

However, recreating these dishes at home presents several challenges:

- A food photograph does not provide the actual recipe.
- Identifying hidden ingredients and their quantities is difficult.
- Finding suitable substitutes for unavailable ingredients can be confusing.
- Existing ingredients at home are often overlooked.
- Nutritional information and cooking measurements may require additional research.

**Snap2Cook AI addresses these challenges by connecting visual food recognition with intelligent recipe reconstruction and pantry-aware adaptation.**

---

## 💡 Our Solution

Snap2Cook AI provides an end-to-end AI-powered cooking workflow.

| Stage | Functionality |
|---|---|
| 1. Upload | Upload a photograph of the desired dish. |
| 2. Analyze | Identify the dish, cuisine, visible ingredients, and cooking techniques. |
| 3. Reconstruct | Generate ingredients, estimated quantities, and step-by-step instructions. |
| 4. Analyze Pantry | Identify available ingredients from the pantry image. |
| 5. Adapt | Compare ingredients and suggest intelligent substitutions. |
| 6. Generate Output | Produce an adapted recipe, nutrition information, shopping list, and compatibility score. |

---

## ✨ Key Features

### 👁️ 1. AI-Powered Vision Analysis
- Identifies the dish from an uploaded image.
- Detects cuisine type and visible ingredients.
- Extracts visual cooking characteristics and techniques.

### 👨‍🍳 2. Recipe Reconstruction
- Reconstructs a structured recipe from a dish photograph.
- Generates ingredient lists and estimated quantities.
- Provides step-by-step cooking instructions.
- Estimates preparation time, cooking time, and servings.
- Generates nutritional information and chef recommendations.

### 🥫 3. Intelligent Pantry Inventory
- Analyzes uploaded pantry photographs.
- Detects available ingredients.
- Normalizes ingredient names.
- Estimates quantities where visually possible.
- Converts the detected ingredients into structured pantry data.

### 🔄 4. Smart Recipe Adaptation
- Compares reconstructed recipes with available pantry ingredients.
- Identifies missing and available ingredients.
- Suggests suitable ingredient substitutions.
- Adapts recipes according to pantry availability.
- Generates a shopping list for missing ingredients.
- Calculates a recipe compatibility score.

### 📊 5. Nutrition Analysis
- Provides nutritional information for ingredients and recipes.
- Calculates nutritional values per serving using dedicated tools.

### ⚖️ 6. Measurement Conversion and Scaling
- Converts ingredient measurements.
- Scales ingredient quantities based on the required servings.

---

## 🏗️ System Architecture

Snap2Cook AI uses a centralized multi-agent workflow instead of relying on independent, uncoordinated AI agents.

The orchestrator manages the execution sequence, maintains session context, and coordinates interactions between specialized agents and external tools.

### Architecture Diagram

## 🏗️ System Architecture

![Snap2Cook AI Architecture](docs/assets/snap2cook-architecture.png)

### Architecture Components

| Component | Responsibility |
|---|---|
| User Interface | Accepts dish and pantry image uploads. |
| ADK-Based Orchestrator | Coordinates agents and manages workflow execution. |
| Vision Analysis Agent | Analyzes dish images and extracts visual information. |
| Recipe Reconstruction Agent | Generates structured recipes and cooking instructions. |
| Pantry Inventory Agent | Detects and structures available ingredients. |
| Recipe Adaptation Agent | Adapts recipes using available ingredients and substitutions. |
| MCP Tool Server | Provides dedicated tools for nutrition, substitutions, and conversions. |
| Session Management | Maintains workflow context and execution state. |
| Pydantic Models | Enforces structured data validation. |

---

## 🤖 Multi-Agent Workflow

The system consists of four specialized agents working sequentially.

### 1. Vision Analysis Agent
**Input:** Dish photograph.

Responsibilities:
- Identify the dish name.
- Detect cuisine type.
- Extract visible ingredients.
- Identify cooking techniques and visual characteristics.

**Output:** Structured dish analysis.

### 2. Recipe Reconstruction Agent
**Input:** Vision analysis results.

Responsibilities:
- Reconstruct ingredients and estimated quantities.
- Generate step-by-step cooking instructions.
- Estimate preparation and cooking time.
- Estimate servings.
- Generate nutrition information.
- Provide cooking tips and suggestions.

**Output:** Structured reconstructed recipe.

### 3. Pantry Inventory Agent
**Input:** Pantry photograph.

Responsibilities:
- Detect available ingredients.
- Normalize ingredient names.
- Estimate quantities when possible.
- Generate structured pantry information.

**Output:** Structured pantry inventory.

### 4. Recipe Adaptation Agent
**Input:** Reconstructed recipe and pantry inventory.

Responsibilities:
- Compare required ingredients with available ingredients.
- Identify missing ingredients.
- Find suitable alternatives.
- Adapt the recipe.
- Generate a shopping list.
- Calculate a compatibility score.

**Output:** Pantry-adapted recipe and actionable cooking information.

---

## 🔌 Model Context Protocol (MCP) Tools

Snap2Cook AI separates deterministic operations from LLM-based reasoning through dedicated MCP-style tool integrations.

This helps keep mathematical calculations and structured operations separate from generative AI responses.

### Implemented Tool Categories

| Tool | Purpose |
|---|---|
| Nutrition Tool | Calculates nutritional information for ingredients and recipes. |
| Substitution Tool | Suggests suitable alternatives for unavailable ingredients. |
| Conversion / Scaling Tool | Converts measurements and scales ingredient quantities based on servings. |

The tools are coordinated through the recipe adaptation workflow to provide structured and actionable results.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python 3.9+ |
| Agent Orchestration | Google Agent Development Kit (ADK)-based workflow |
| AI Models | Google Gemini 2.5 Flash, Meta Llama 3.1 |
| Model Access | OpenRouter / Gemini API |
| User Interface | Streamlit |
| Data Validation | Pydantic |
| Tool Integration | Model Context Protocol (MCP)-style tool server |
| Reliability | Tenacity |
| Testing | Pytest |
| Version Control | Git and GitHub |

---

## 📂 Project Structure

```text
Snap2cook-ai/
│
├── agents/
│   ├── base_agent.py
│   ├── callbacks.py
│   ├── orchestrator.py
│   ├── prompts.py
│   └── sessions.py
│
├── config/
│   └── Application configuration
│
├── docs/
│   └── assets/
│       └── snap2cook-architecture.png
│
├── frontend/
│   ├── app.py
│   └── pages/
│
├── mcp_server/
│   ├── server.py
│   └── tools/
│
├── schemas/
│
├── tests/
│
├── utils/
│
├── .env.example
├── requirements.txt
├── test_pantry.py
├── test_pantry_err.py
├── test_workflow.py
└── README.md
```

---

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.9 or higher.
- Git.
- An API key for a supported AI provider.

### Step 1: Clone the Repository

```bash
git clone https://github.com/mrudulap01/Snap2cook-ai.git

cd Snap2cook-ai
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the root directory.

```env
AI_API_KEY=your_api_key_here

AI_BASE_URL=https://openrouter.ai/api/v1

VISION_MODEL=google/gemini-2.5-flash

TEXT_MODEL=google/gemini-2.5-flash

FALLBACK_TEXT_MODEL=meta-llama/llama-3.1-70b-instruct
```

Configure the appropriate API key and model settings for your chosen provider.

**Important:** Never commit your actual API keys or `.env` file to GitHub.

---

## ▶️ Running the Application

Start the Streamlit application:

```bash
python -m streamlit run frontend/app.py
```

Open the application in your browser:

```text
http://localhost:8501
```

Upload a dish image and a pantry image to explore the recipe reconstruction and adaptation workflow.

---

## 🧪 Testing

Run the test suite using:

```bash
pytest
```

To run individual test files:

```bash
pytest test_pantry.py
pytest test_pantry_err.py
pytest test_workflow.py
```

---

## 🔮 Future Scope

Some potential enhancements include:

- **Dietary Personalization:** Adapt recipes according to dietary preferences and restrictions.
- **Voice-Assisted Cooking:** Provide hands-free, step-by-step cooking guidance.
- **Advanced Food Recognition:** Improve ingredient detection and quantity estimation.
- **Smart Grocery Integration:** Integrate shopping services for missing ingredients.
- **Recipe History:** Save and revisit previously generated recipes.
- **Allergy-Aware Adaptation:** Provide ingredient recommendations while accounting for declared allergies.
- **Improved Nutrition Estimation:** Incorporate more comprehensive ingredient-level nutritional databases.

---

## 🤝 Contributing

Contributions and suggestions are welcome!

1. Fork this repository.
2. Create a feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

---

## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for details.

---

## 👩‍💻 Author

**Mrudula Pimparwar**

GitHub: [@mrudulap01](https://github.com/mrudulap01)

Project Repository: [Snap2Cook AI](https://github.com/mrudulap01/Snap2cook-ai)

---

⭐ If you find this project interesting, consider giving the repository a star!

**Snap2Cook AI — From a Picture to a Possibility.** 🍳
