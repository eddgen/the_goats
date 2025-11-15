# FitCoach AI - Personal Fitness & Nutrition Assistant

Proiect pentru Hackathon - Un agent AI inteligent pentru fitness și nutriție.

## 📁 Structura Proiectului

```
fitness_agent/
├── main.py                      # Entry point
├── requirements.txt             # Dependențe Python
├── .env.example                 # Template pentru variabile de mediu
│
├── agent/
│   ├── __init__.py
│   └── fitness_agent.py         # Agent principal
│
├── tools/
│   ├── __init__.py
│   ├── nutrition_tools.py       # Meal planning, calorie tracking
│   ├── workout_tools.py         # Workout plans, Hevy integration
│   ├── body_analysis_tools.py   # Body fat estimation din poză
│   ├── route_tools.py           # Google Maps route generation
│   ├── data_integration_tools.py # Strava, Hevy, frigider data
│   └── export_tools.py          # PDF/Excel generation
│
├── utils/
│   ├── __init__.py
│   ├── validators.py            # Input validation
│   ├── formatters.py            # Data formatting
│   └── database.py              # SQLite pentru user data
│
├── data/
│   ├── users/                   # User profiles & history
│   ├── templates/               # PDF templates
│   └── cache/                   # API response cache
│
└── config/
    ├── __init__.py
    └── tools_config.py          # Tool definitions pentru GPT
```

## 🚀 Setup

1. **Instalează dependențele:**
```bash
pip install -r requirements.txt
```

2. **Configurează variabilele de mediu:**
```bash
# Copiază template-ul
cp .env.example .env

# Editează .env și adaugă API keys
```

3. **Rulează aplicația:**
```bash
python main.py
```

## 🔧 Funcționalități (În dezvoltare)

### ✅ Implementat (Structură)
- [x] Arhitectură modulară
- [x] Agent core cu OpenAI function calling
- [x] Tool templates pentru toate funcționalitățile
- [x] Sistem de configurare
- [x] Validatori și formatters

### 🚧 De implementat
- [ ] TDEE calculation (nutrition_tools)
- [ ] Meal plan generation (nutrition_tools)
- [ ] Workout plan generation (workout_tools)
- [ ] Body analysis cu vision AI (body_analysis_tools)
- [ ] Google Maps integration (route_tools)
- [ ] Hevy/Strava data import (data_integration_tools)
- [ ] PDF/Excel export (export_tools)
- [ ] Database operations (utils/database)

## 📊 Tool-uri Disponibile

1. **Nutrition Tools**
   - `calculate_tdee` - Calculează necesarul caloric zilnic
   - `generate_meal_plan` - Generează plan alimentar personalizat
   - `track_calories` - Tracking calorii din descriere

2. **Workout Tools**
   - `generate_workout_plan` - Plan antrenament personalizat
   - `analyze_workout_progress` - Analiză progres

3. **Body Analysis**
   - `calculate_bmi` - Calculează BMI
   - `estimate_body_fat` - Estimare body fat din poză

4. **Route Tools**
   - `generate_running_routes` - Generează trasee alergare
   - `find_nearby_gyms` - Găsește săli în apropiere

5. **Data Integration**
   - `import_strava_data` - Import date Strava
   - `import_hevy_workout` - Import date Hevy

6. **Export Tools**
   - `export_meal_plan_pdf` - Export PDF meal plan
   - `export_workout_plan_pdf` - Export PDF workout plan
   - `export_progress_report_excel` - Export raport Excel

## 🎯 Next Steps

1. **Implementează TDEE calculation** - Prima funcționalitate de bază
2. **Testează conversația** - Verifică flow-ul de dialog
3. **Adaugă Google Maps integration** - Pentru route generation
4. **Implementează PDF export** - Pentru meal/workout plans
5. **Integrează Hevy data** - Import workout history

## 📝 API Keys Necesare

- `OPENAI_API_KEY` - Pentru agent core (obligatoriu)
- `GOOGLE_MAPS_API_KEY` - Pentru route generation (opțional)
- `NUTRITIONIX_APP_ID` și `NUTRITIONIX_APP_KEY` - Pentru calorie database (opțional)
- `STRAVA_CLIENT_ID` și `STRAVA_CLIENT_SECRET` - Pentru Strava integration (opțional)

## 💡 Cum să Continui

Structura de bază este gata! Acum poți:

1. **Începe cu implementarea tool-urilor** - Fiecare are TODO-uri clare
2. **Testează pe măsură ce implementezi** - Rulează `main.py` și verifică conversația
3. **Integrează API-urile externe** - Google Maps, Nutritionix, etc.
4. **Adaugă export-uri** - PDF/Excel pentru planuri

Succes la hackathon! 🚀

---

## 📚 Original Simple Agent Demo

A demonstration of a basic AI agent built with Python and OpenAI's API.

### What is an AI Agent?

An **AI agent** is an autonomous system that can:

1. **Perceive**: Receive and understand inputs from users or environment
2. **Reason**: Use an LLM to decide what actions to take
3. **Act**: Execute tools/functions to accomplish tasks
4. **Learn**: Maintain conversation context and improve responses

### Agent Architecture

```
User Input → Agent (LLM) → Decision → Tool Execution → Response
                ↑                            ↓
                └────── Feedback Loop ───────┘
```

## This Agent's Capabilities

- **Conversational AI**: Natural language understanding and responses
- **Tool Use**: Can call functions to perform specific tasks
- **Calculator**: Performs mathematical calculations
- **Weather Checker**: Simulates weather queries (mock data)
- **Memory**: Maintains conversation history

## Installation

1. Install Python 3.8 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

Run the agent:
```bash
python simple_agent.py
```


### Example Interactions

```
You: What's 234 * 56?
Agent: [uses calculator] Result: 13104

You: What's the weather in Paris?
Agent: [checks weather] Weather in Paris: Sunny, 22°C

You: What's the capital of France?
Agent: The capital of France is Paris.
```

## How It Works

1. **User sends a message** to the agent
2. **Agent (GPT-4) analyzes** the message
3. **If tools are needed**, agent calls appropriate functions
4. **Tool results** are sent back to the LLM
5. **Agent formulates** a final response
6. **Response is returned** to the user

## Key Concepts

### Tools/Functions
Functions the agent can call to perform specific tasks. Each tool has:
- **Name**: Identifier for the function
- **Description**: What it does (helps LLM decide when to use it)
- **Parameters**: What inputs it needs

### Conversation History
The agent maintains a list of all messages, allowing it to:
- Remember context
- Provide coherent multi-turn conversations
- Reference previous interactions

### LLM Reasoning
The language model decides:
- Whether to use tools
- Which tools to use
- How to respond based on tool results

## Extending This Agent

You can add more tools:
- Web search
- Database queries
- File operations
- API integrations
- Email sending
- Task scheduling

## Learn More

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)
