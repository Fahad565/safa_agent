# safa_agent

Safa Glow-Up Coach - AI-powered organic beauty and home care assistant powered by Streamlit and Gemini.

## Features
- **Product Recommender**: Recommends Safa products based on user skin/hair/beard concerns or goals.
- **30-Day Routine Builder**: Creates customized week-by-week plans.
- **Ingredient Safety Checker**: Scans ingredient lists for harsh chemicals and suggests natural alternatives.
- **Symptom Troubleshooter**: Provides coaching advice during transition periods.

## Setup & Running
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure Streamlit Secrets in `.streamlit/secrets.toml`:
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run safa_app.py
   ```
