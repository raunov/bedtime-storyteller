# Bedtime Story Generator

This Streamlit app generates personalized bedtime stories for children using AI language models. It supports multiple languages and allows users to input details about the children, their interests, and values to be taught in the story.

## Features

- 🌍 Supports multiple languages: English, Spanish, Estonian, Finnish, Russian, and Arabic
- 👧👦 Customizable for multiple children
- 🧸 Incorporates children's favorite toys and activities
- 📚 Focuses on specific values you want to teach
- 🎨 Adjusts story complexity based on the child's age
- 🖊️ Powered by OpenRouter so you can use top-tier models like GPT-5, Claude Sonnet 4, Gemini 2.5 Pro, and Grok 4
- 📊 Stores usage statistics in a Supabase database
- 🌟 Allows users to rate generated stories

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/raunov/bedtime-storyteller.git
   cd bedtime-storyteller
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up a Supabase project:
   - Go to [Supabase](https://supabase.com/) and create a new project
   - In the SQL Editor, run the SQL script from `create_table.sql` to create the necessary table

4. Set up your `.streamlit/secrets.toml` file with the following content:
   ```toml
   OPENROUTER_API_KEY = "your_openrouter_api_key"
   OPENROUTER_SITE_URL = "https://yourapp.example.com"  # Optional but recommended for rate-limits
   OPENROUTER_APP_NAME = "Bedtime Storyteller"           # Optional title shown in OpenRouter analytics
   MODEL = "anthropic/claude-sonnet-4"                   # Or any other OpenRouter model slug/alias
   SUPABASE_URL = "your_supabase_project_url"
   SUPABASE_KEY = "your_supabase_api_key"
   DEFAULT_LANGUAGE = "English"
   ```
   Replace the placeholder values with your actual API key, site URL, and Supabase credentials. You can provide either a full OpenRouter model slug (e.g. `openai/gpt-5`) or one of the supported aliases (`gpt-5`, `claude`, `gemini`, `grok`, `llama`).

5. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Testing

Run the test suite with [pytest](https://pytest.org):

```bash
pytest
```

## Usage

1. Select your preferred language from the dropdown menu.
2. Enter the number of children, their names, and ages.
3. Input their favorite toys, activities, and any events from today.
4. Specify the values or lessons you want to teach in the story.
5. Click the "Generate Story" button to create a personalized bedtime story.
6. After reading the story, you can rate it using the feedback widget.

## License

This project is licensed under the MIT License.
