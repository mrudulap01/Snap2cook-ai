# Snap2Cook AI Architecture

This document contains detailed architectural diagrams for the Snap2Cook AI project, demonstrating the complete end-to-end multi-agent workflow, ADK orchestration, Model Context Protocol (MCP) interactions, and overall data flow.

## 1. Overall System Architecture

```mermaid
graph TD
    %% User Inputs
    User([User])
    
    %% UI Layer
    subgraph UI [Streamlit Frontend]
        DishUpload[Dish Image Upload]
        PantryUpload[Pantry Image Upload]
        FinalOutput[Adapted Recipe & Shopping List]
    end

    %% ADK Orchestrator
    subgraph Core [Google ADK Orchestrator]
        VA[Vision Analysis Agent]
        RA[Recipe Reconstruction Agent]
        PA[Pantry Inventory Agent]
        AA[Recipe Adaptation Agent]
    end

    %% MCP Server
    subgraph MCP [Model Context Protocol]
        Nutrition[Nutrition Calculator]
        Substitution[Smart Substitution]
        Scaling[Recipe Scaling]
        Cooking[Cooking Helper]
    end

    %% Flow
    User --> DishUpload
    DishUpload --> VA
    VA --> RA
    
    User --> PantryUpload
    PantryUpload --> PA
    
    RA --> AA
    PA --> AA
    
    RA -.->|Invokes| MCP
    AA -.->|Invokes| MCP
    
    AA --> FinalOutput
    FinalOutput --> User

    %% Styling
    classDef ui fill:#f9f,stroke:#333,stroke-width:2px;
    classDef agent fill:#bbf,stroke:#333,stroke-width:2px;
    classDef mcp fill:#dfd,stroke:#333,stroke-width:2px;
    
    class DishUpload,PantryUpload,FinalOutput ui;
    class VA,RA,PA,AA agent;
    class Nutrition,Substitution,Scaling,Cooking mcp;
```

---

## 2. Google ADK Workflow

```mermaid
flowchart TD
    %% ADK Core
    Runner[[ADK Runner]]
    Session[(ADK Session History)]
    
    %% Agents
    VA[Vision Agent]
    RA[Recipe Agent]
    PA[Pantry Agent]
    AA[Adaptation Agent]

    %% Flow
    Runner -->|Initialize| Session
    Runner -->|Step 1: Execute| VA
    VA -->|Log Input/Output| Session
    
    Runner -->|Step 2: Handoff| RA
    RA -->|Log Input/Output| Session
    
    Runner -->|Step 3: Execute| PA
    PA -->|Log Input/Output| Session
    
    Runner -->|Step 4: Merge Data| AA
    AA -->|Log Input/Output| Session
    
    Session -.->|Provide Context| Runner
```

---

## 3. Agent Communication Diagram

```mermaid
sequenceDiagram
    participant Frontend
    participant Runner as ADK Runner
    participant VA as Vision Agent
    participant RA as Recipe Agent
    participant PA as Pantry Agent
    participant AA as Adaptation Agent

    Frontend->>Runner: Submit Dish Image
    Runner->>VA: process(image_path)
    VA-->>Runner: return DishAnalysis (JSON)
    
    Runner->>RA: process(DishAnalysis)
    RA-->>Runner: return Recipe (JSON)
    Runner-->>Frontend: Render Recipe UI
    
    Frontend->>Runner: Submit Pantry Image
    Runner->>PA: process(image_path)
    PA-->>Runner: return PantryInventory (JSON)
    
    Runner->>AA: process(Recipe + PantryInventory)
    AA-->>Runner: return AdaptationResult (JSON)
    Runner-->>Frontend: Render Adapted UI & Shopping List
```

---

## 4. MCP Interaction Diagram

```mermaid
graph LR
    %% Agents
    RA(Recipe Agent)
    AA(Adaptation Agent)
    
    %% MCP Server
    subgraph MCPServer [Model Context Protocol Server]
        direction TB
        N[Nutrition Tool<br/>'get_nutrition']
        S[Substitution Tool<br/>'get_substitution']
        R[Scaling Tool<br/>'scale_recipe']
        C[Cooking Tool<br/>'cooking_helper']
    end
    
    %% Interactions
    RA -.->|Calculates Macros| N
    RA -.->|Yield Conversions| R
    
    AA -.->|Validates Swaps| S
    AA -.->|Calculates Macros| N
    AA -.->|Method Adjustments| C
```

---

## 5. Deployment Diagram

```mermaid
graph TD
    User([End User])
    
    subgraph Cloud [Streamlit Community Cloud]
        Streamlit[Streamlit Web App]
        ADK[Google ADK Runner]
    end
    
    subgraph AIProviders [AI Intelligence APIs]
        OpenRouter[OpenRouter API Gateway]
        Gemini[Google Gemini 2.5 Flash]
        Llama[Meta Llama 3.1 70B]
    end
    
    subgraph LocalServers [Backend Services]
        MCPServer[[Simulated MCP Server]]
    end
    
    User -->|HTTPS| Streamlit
    Streamlit --> ADK
    
    ADK -->|REST API| OpenRouter
    OpenRouter --> Gemini
    OpenRouter --> Llama
    
    ADK -->|Function Calls| MCPServer
```

---

## 6. Data Flow Diagram

```mermaid
stateDiagram-v2
    [*] --> RawDishImage: User Upload
    RawDishImage --> VisionAgent
    
    VisionAgent --> StructuredDishJSON: Object Detection & Classification
    
    StructuredDishJSON --> RecipeAgent
    RecipeAgent --> OriginalRecipeJSON: Culinary Reconstruction
    
    OriginalRecipeJSON --> PantryAgent: Await Inventory
    
    RawPantryImage --> PantryAgent: User Upload
    PantryAgent --> PantryInventoryJSON: Ingredient Extraction
    
    OriginalRecipeJSON --> AdaptationAgent
    PantryInventoryJSON --> AdaptationAgent
    
    AdaptationAgent --> AdaptedRecipeJSON: Smart Substitution Merge
    AdaptedRecipeJSON --> FinalOutput
    
    FinalOutput --> [*]: Render PDF & UI
```
