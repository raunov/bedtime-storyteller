# Bedtime Storyteller

🌙 A multilingual, personalized bedtime story generator powered by OpenAI's GPT-4.

## Overview

This Streamlit app creates customized bedtime stories for children based on their age, interests, and the values you want to teach. It supports multiple languages and adapts the story complexity to the child's age.

## Features

- 🌍 Supports multiple languages: English, Spanish, Estonian, Latvian, Finnish, and Russian
- 👧👦 Customizable for multiple children
- 🧸 Incorporates children's favorite toys and activities
- 📚 Focuses on specific values you want to teach
- 🎨 Adjusts story complexity based on the child's age
- 🖊️ Powered by OpenAI's GPT-4 for creative and engaging stories

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/raunov/bedtime-storyteller.git
   cd bedtime-story-generator
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   - Create a file named `.streamlit/secrets.toml` in the project directory
   - Add your OpenAI API key to this file:
     ```
     OPENAI_API_KEY = "your-api-key-here"
     ```

4. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Usage

1. Select your preferred language from the dropdown menu.
2. Enter the number of children, their names, and ages.
3. Input favorite toys, activities, and events from today.
4. Specify the values you want the story to teach.
5. Click the "Generate Story" button to create your personalized bedtime story.

## Contributing

Contributions to improve the Bedtime Story Generator are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).

## Acknowledgements

- OpenAI for providing the GPT-4 API
- Streamlit for the web app framework
- Flag CDN for providing flag images