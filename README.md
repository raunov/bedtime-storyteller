# Bedtime Story Generator

This Streamlit app generates personalized bedtime stories for children using AI language models. It supports multiple languages and allows users to input details about the children, their interests, and values to be taught in the story.

## Features

- 🌍 Supports multiple languages: English, Spanish, Estonian, Finnish, Russian, and Arabic
- 👧👦 Customizable for multiple children
- 🧸 Incorporates children's favorite toys and activities
- 📚 Focuses on specific values you want to teach
- 🎨 Adjusts story complexity based on the child's age
- 🖊️ Powered by a wide variety of language models via [OpenRouter](https://openrouter.ai/) for creative and engaging stories
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
   MODEL = "your_selected_model"  # Optional: specify a model from OpenRouter, e.g., "openai/gpt-4o"
   SUPABASE_URL = "your_supabase_project_url"
   SUPABASE_KEY = "your_supabase_api_key"
   DEFAULT_LANGUAGE = "English"
   PUBLIC_APP_URL = "https://your-app-domain.example.com"  # Public base URL used for social sharing metadata
   ```
   Replace the placeholder values with your actual API keys and URLs.

   The value of `PUBLIC_APP_URL` should be the fully qualified domain where your Streamlit app is publicly reachable (including the protocol, typically `https://`). For example, if your deployment lives at `https://stories.example.com`, set `PUBLIC_APP_URL = "https://stories.example.com"`. Streamlit will use this base URL to build absolute Open Graph and Twitter card links for social sharing previews.

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