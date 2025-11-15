Perfect! Îți fac un plan complet pentru hackathon cu arhitectură modulară.
🏋️ FITNESS AI AGENT - Plan Complet Hackathon
📋 PLANUL PROIECTULUI
Numele: FitCoach AI - Personal Fitness & Nutrition Assistant
Funcționalități Principale:
1.	Profile Analysis - Analiză corp (body fat din poză, date fizice)
2.	Nutrition Planning - Meal plan personalizat + tracking calorii
3.	Workout Planning - Plan antrenament + tracking progres
4.	Route Mapping - Trasee running personalizate (Google Maps)
5.	Data Integration - Import Hevy, Strava, frigider
6.	Progress Tracking - Transformare vizuală + rapoarte
7.	Export Reports - PDF/Excel cu planuri

🏗️ ARHITECTURA (Structura de fișiere)
fitness_agent/
│
├── main.py                          # Entry point
├── requirements.txt
├── .env                             # API keys
│
├── agent/
│   ├── __init__.py
│   └── fitness_agent.py             # Clasa principală agent
│
├── tools/
│   ├── __init__.py
│   ├── nutrition_tools.py           # Meal planning, calorie tracking
│   ├── workout_tools.py             # Workout plans, Hevy integration
│   ├── body_analysis_tools.py       # Body fat estimation din poză
│   ├── route_tools.py               # Google Maps route generation
│   ├── data_integration_tools.py    # Strava, Hevy, frigider data
│   └── export_tools.py              # PDF/Excel generation
│
├── utils/
│   ├── __init__.py
│   ├── validators.py                # Input validation
│   ├── formatters.py                # Data formatting
│   └── database.py                  # SQLite pentru user data
│
├── data/
│   ├── users/                       # User profiles & history
│   ├── templates/                   # PDF templates
│   └── cache/                       # API response cache
│
└── config/
    ├── __init__.py
    └── tools_config.py              # Tool definitions pentru GPT



🔧 TOOLS DETALIATE
1. nutrition_tools.py
•	Tools:
•	- calculate_tdee(weight, height, age, gender, activity_level)
•	- generate_meal_plan(calories, diet_preference, restrictions)
•	- track_calories(meal_description_or_photo)
•	- check_fridge_inventory(products_list, expiry_dates)
•	- suggest_meals_from_fridge()
2. workout_tools.py
Tools:
- generate_workout_plan(goal, experience, days_per_week, equipment)
- import_hevy_data(hevy_export_file)
- analyze_workout_progress(workout_history)
- suggest_progressive_overload(current_exercises)
3. body_analysis_tools.py
•	Tools:
•	- estimate_body_fat(image_path)  # Computer Vision API
•	- calculate_bmi(weight, height)
•	- track_measurements(chest, waist, arms, etc)
•	- visualize_transformation(before_after_photos)
4. route_tools.py
Tools:
- generate_running_routes(location, distance, terrain_preference)
  # → Returnează 2-3 opțiuni (stadion, parc, cartier)
- find_nearby_gyms(location, radius)
- calculate_route_elevation(route_coordinates)
5. data_integration_tools.py
•	Tools:
•	- import_strava_data(auth_token)
•	- import_hevy_workout(csv_file)
•	- sync_health_data(source: "apple_health", "google_fit")
6. export_tools.py
Tools:
- export_meal_plan_pdf(meal_plan_data)
- export_workout_plan_pdf(workout_data)
- export_progress_report_excel(user_data, date_range)
- generate_transformation_pdf(before_after, stats)
 CONVERSAȚIE EXEMPLU
User: "Salut, am 70kg, sunt activ, merg de 5 ori pe săptămână la sală. 
       Vreau să slăbesc 5kg."

Agent: 
  🤔 Analyzing your profile...
  🔧 Using tools: calculate_tdee, generate_workout_plan
  
  "Perfect! Pentru a-ți personaliza planul, mai am nevoie de câteva detalii:
   - Înălțime?
   - Vârstă?
   - Gen?
   - Ai restricții alimentare?
   - Poți face poză la ceea ce ai în frigider?"

User: "1.75m, 25 ani, bărbat, nu mănânc lactate. Iată poza cu frigiderul."

Agent:
  🔧 Using tools: calculate_tdee, generate_meal_plan, 
                  analyze_fridge_inventory, generate_running_routes
  
  "✅ Calculat TDEE: 2400 cal/zi
   📉 Pentru -5kg: 1900 cal/zi (deficit 500 cal)
   
   📄 Meal plan generat (PDF atașat)
   🏋️ Workout plan 5x/săpt (PDF atașat)
   🏃 3 rute de alergare în zona ta:
      1. Parc Herăstrău - 5km buclă
      2. Stadion Național - pistă atletism
      3. Cartier buclă - 7km variație
   
   Vrei să-mi trimiți și datele Hevy pentru a-ți personaliza antrenamentele?"

🚀 IMPLEMENTARE PAS CU PAS
Faza 1: Setup & Structură (Ziua 1 dimineață)
# Creezi structura de foldere
# Instalezi dependințe:
pip install openai pillow google-maps-services reportlab pandas openpyxl python-dotenv
Faza 2: Agent Core (Ziua 1 după-amiază)
# fitness_agent.py - similar cu simple_agent.py
# Dar cu toate tools-urile definite	

Faza 3: Tools Implementation (Ziua 2)
•	Nutrition tools (3-4 ore)
•	Workout tools + Hevy integration (2-3 ore)
•	Body analysis (2 ore)
•	Route mapping (2 ore)

1. nutrition_tools.py (3-4 ore) ← ÎNCEPEM AICI
   ├── calculate_tdee() 
   ├── generate_meal_plan()
   └── TESTĂM

2. body_analysis_tools.py (1-2 ore)
   ├── calculate_bmi()
   ├── track_measurements()
   └── TESTĂM

3. workout_tools.py (2-3 ore)
   ├── generate_workout_plan()
   ├── analyze_workout_progress()
   └── TESTĂM

4. route_tools.py (2 ore) - necesită Google Maps API
   ├── generate_running_routes()
   ├── find_nearby_gyms()
   └── TESTĂM

5. export_tools.py (1-2 ore)
   ├── export_meal_plan_pdf()
   ├── export_workout_plan_pdf()
   └── TESTĂM

6. data_integration_tools.py (2 ore) - opțional
   └── import_hevy_data()
   
Faza 4: Data & Export (Ziua 3 dimineață)
•	Database pentru user profiles
•	PDF/Excel generation
•	Template design
Faza 5: Integration & Testing (Ziua 3 după-amiază)
•	Conectare toate modulele
•	Testing conversational flow
•	Bug fixes
Faza 6: UI/Polish (Opțional - dacă mai ai timp)
•	Streamlit/Gradio interface
•	SAU Telegram bot
•	SAU rămâi cu CLI
📦 requirements.txt
openai>=1.0.0
python-dotenv>=1.0.0
Pillow>=10.0.0
google-maps-services>=4.10.0
reportlab>=4.0.0
pandas>=2.0.0
openpyxl>=3.1.0
requests>=2.31.0
anthropic  # dacă vrei Claude alternativ
ollama     # dacă vrei local LLM________________________________________
🎯 API-uri Necesare
1.	OpenAI - Agent core (GPT-4)
2.	Google Maps API - Route generation
3.	Vision API (OpenAI Vision sau Anthropic Claude) - Body fat analysis
4.	Nutritionix API (opțional) - Calorie database
5.	Strava API (opțional) - Workout data import
________________________________________
💡 MVP vs FULL VERSION
MVP (minimum pentru demo - 2 zile):
•	✅ Conversație inteligentă cu colectare date
•	✅ TDEE calculation
•	✅ Basic meal plan (template-based)
•	✅ Basic workout plan (template-based)
•	✅ 1-2 Google Maps routes
•	✅ Export PDF simplu
FULL (dacă ai timp - 3+ zile):
•	✅ Body fat analysis din poză
•	✅ Hevy/Strava integration
•	✅ Frigider inventory cu expiry tracking
•	✅ Advanced meal suggestions
•	✅ Progress tracking cu grafice
•	✅ Excel reports cu statistici
________________________________________
📊 EXEMPLE DE COD
Vreau să încep cu codul template pentru arhitectură?
Îți generez:
1.	fitness_agent.py (agent principal)
2.	nutrition_tools.py (tools nutriție)
3.	route_tools.py (Google Maps)
4.	export_tools.py (PDF generation)
5.	main.py (entry point)
Confirmă și încep să codez! 🚀


