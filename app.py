import streamlit as st
from openai import OpenAI
import os
from datetime import datetime
from supabase import create_client, Client
import json
import random
import time
import logging

# Set up logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')

# Helper function to get configuration
def get_config(key, default=None):
    return os.environ.get(key) or st.secrets.get(key, default)

# Load translations from JSON file
with open('translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Get the default language from config
default_language = get_config("DEFAULT_LANGUAGE", "Eesti")

# Remove emoji from title
title_without_emoji = translations[default_language]["title"].split()[1:]
title_without_emoji = " ".join(title_without_emoji)

# Set page config once at the beginning
st.set_page_config(
    page_title=title_without_emoji,
    page_icon="🌙" 
)

# Constants for OpenRouter
OPENROUTER_API_URL = "https://openrouter.ai/api/v1"
MODEL_ALIASES = {
    "claude": "anthropic/claude-sonnet-4",
    "claude-sonnet-4": "anthropic/claude-sonnet-4",
    "claude-3-5-sonnet-20240620": "anthropic/claude-3.5-sonnet",
    "claude-3.5-sonnet": "anthropic/claude-3.5-sonnet",
    "gpt-5": "openai/gpt-5",
    "gpt-4.1": "openai/gpt-4.1",
    "gpt-4o": "openai/gpt-4o",
    "o3-mini": "openai/o3-mini",
    "gemini": "google/gemini-2.5-pro",
    "gemini-2.5-pro": "google/gemini-2.5-pro",
    "gemini-1.5-pro": "google/gemini-1.5-pro",
    "grok": "x-ai/grok-4",
    "grok-4": "x-ai/grok-4",
    "llama": "meta-llama/llama-3.1-405b-instruct",
    "llama-3.2-90b-text-preview": "meta-llama/llama-3.1-405b-instruct",
}
DEFAULT_MODEL_POOL = [
    # Latest flagships from the leading providers on OpenRouter
    "openai/gpt-5",
    "anthropic/claude-sonnet-4",
    "google/gemini-2.5-pro",
    "x-ai/grok-4",
]


def resolve_model_choice(model_name: str | None) -> str:
    if not model_name:
        return random.choice(DEFAULT_MODEL_POOL)
    return MODEL_ALIASES.get(model_name, model_name)


selected_model = resolve_model_choice(get_config("MODEL"))

# Configure OpenRouter client
openrouter_api_key = get_config("OPENROUTER_API_KEY")
openrouter_client = None
if openrouter_api_key:
    default_headers = {}
    site_url = get_config("OPENROUTER_SITE_URL")
    if site_url:
        default_headers["HTTP-Referer"] = site_url
    app_name = get_config("OPENROUTER_APP_NAME", "Bedtime Storyteller")
    if app_name:
        default_headers["X-Title"] = app_name

    client_kwargs = {
        "base_url": OPENROUTER_API_URL,
        "api_key": openrouter_api_key,
    }
    if default_headers:
        client_kwargs["default_headers"] = default_headers

    openrouter_client = OpenAI(**client_kwargs)

# Set up Supabase client
supabase: Client = create_client(get_config("SUPABASE_URL"), get_config("SUPABASE_KEY"))

def get_text(key):
    return translations[st.session_state.language][key]

def generate_story(children_info, story_details, language):
    # Calculate average age of children
    ages = [int(info.split(',')[1].split()[0]) for info in children_info.split('\n')]
    avg_age = sum(ages) / len(ages)

    # Adjust complexity based on average age
    if avg_age < 5:
        complexity = "very simple with short sentences and basic vocabulary"
    elif avg_age < 8:
        complexity = "simple with easy-to-understand concepts and some new vocabulary"
    elif avg_age < 10:
        complexity = "moderately complex with some challenging words and concepts"
    else:
        complexity = "more sophisticated with advanced vocabulary and complex storylines"

    prompt = f"""You are a child-friendly storyteller. Your task is to create a 10 minute bedtime story based on the following information:

    Children: {children_info}
    
    Story details: {story_details if story_details else "Create an imaginative story suitable for children."}
    
    Before creating the story, please check if any of the inputs (names, activities, toys, or values) are inappropriate or too controversial for children. 
    If you find any such content, respond with "MODERATED_CONTENT" followed by a brief explanation.

    If the content is appropriate, don't mention the moderation, please just proceed to write the story in {language} language.
    
    The story should be {complexity}, as the average age of the children is {avg_age:.1f} years old and the story should be 10 minutes long. 
    Adjust the language, concepts, and storyline to be engaging and understandable for children of this age group.
    
    If the story details include toys, you should focus on them as the protagonists of the story.
    The story should be in a calm and gentle tone, clear and simple narrative and reassuring tone that addresses any fears or worries.
    Ensure the story has a clear beginning, middle, and end, with a positive message or lesson appropriate for children.
    If no specific details were provided, create an imaginative and engaging story that focuses on universal themes like friendship, kindness, courage, or curiosity.
    """

    start_time = time.time()  # Start timing

    try:
        if openrouter_client is None:
            logging.error("OpenRouter API key is not configured.")
            raise ValueError("Story generation is currently unavailable. Please contact the administrator.")

        response = openrouter_client.chat.completions.create(
            model=selected_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7,
        )
        story = response.choices[0].message.content
    except ValueError:
        raise
    except Exception as e:
        logging.error(f"Error generating story: {e}")
        raise ValueError("An error occurred while generating the story. Please try again later.")

    generation_time = round(time.time() - start_time, 1)  # End timing and round to 1 decimal place

    if story.startswith("MODERATED_CONTENT"):
        raise ValueError(story)
    
    return story, generation_time

def insert_usage_stats(selected_language, num_children, ages, values_to_teach, selected_model, generation_time, moderated=False, children_info=None, activities_and_toys=None):
    current_time = datetime.now().isoformat()
    data = {
        "datetime": current_time,
        "selected_language": selected_language,
        "num_children": num_children,
        "ages": ages,
        "values_to_teach": ("MODERATED: " + values_to_teach) if moderated else values_to_teach,
        "selected_model": selected_model,
        "generation_time": generation_time  # Add generation time to the data
    }
    
    if moderated:
        user_inputs = {
            "children_info": children_info,
            "activities_and_toys": activities_and_toys,
            "values_to_teach": values_to_teach
        }
        data["moderated_inputs"] = json.dumps(user_inputs)
    
    try:
        response = supabase.table("usage_stats").insert(data).execute()
        return response.data[0]['id']
    except Exception as e:
        logging.error(f"Error inserting usage stats: {e}")
        return None

def update_rating(row_id, rating):
    try:
        rating_str = str(rating)
        supabase.table("usage_stats").update({"rating": rating_str}).eq("id", row_id).execute()
    except Exception as e:
        logging.error(f"Error updating rating: {e}")

# Initialize session state variables
if 'story' not in st.session_state:
    st.session_state.story = None
if 'row_id' not in st.session_state:
    st.session_state.row_id = None

# Initialize session state for language
if 'language' not in st.session_state:
    st.session_state.language = default_language

# Language selection using selectbox
selected_language = st.sidebar.selectbox(
    get_text("language_select"),
    options=list(translations.keys()),
    index=list(translations.keys()).index(st.session_state.language)
)

if selected_language != st.session_state.language:
    st.session_state.language = selected_language
    st.rerun()  # This will rerun the script with the new language

# Update the page title using JavaScript
st.markdown(
    f"""
    <script>
        document.title = "{title_without_emoji}";
    </script>
    """,
    unsafe_allow_html=True
)

# Add header image
image_path = os.path.join("static", "images", "header.png")
st.image(image_path,use_container_width=True)

st.title(get_text("title"))

# Move input options to sidebar
with st.sidebar:
    st.header(get_text("story_settings"))

    num_children = st.number_input(get_text("num_children"), min_value=1, max_value=5, value=1)

    children_info = []
    for i in range(num_children):
        st.subheader(f"{get_text('child')} {i+1} 🧒")
        name = st.text_input(f"{get_text('name')} {i+1}", key=f"name_{i}")
        age = st.slider(get_text("age_of_child").format(name=name), min_value=1, max_value=12, value=6, key=f"age_{i}")
        children_info.append(f"{name}, {age} years old")

    activities_and_toys = st.text_area(
        get_text("activities_and_toys"),
        help=get_text("activities_help")
    )
    values_to_teach = st.text_input(
        get_text("values_to_teach"),
        help=get_text("values_help")
    )

    generate_button = st.button(get_text("generate_button"))

story_details = ""

if activities_and_toys.strip():
    story_details += f"Activities, toys, and events: {activities_and_toys}\n"

if values_to_teach.strip():
    story_details += f"Values to teach: {values_to_teach}\n"

if not story_details:
    story_details = ""

# Main area for displaying the story
if generate_button:
    with st.spinner(get_text("creating_story")):
        children_info_str = "\n".join(children_info)
        story_details = f"Activities and toys: {activities_and_toys}\nValues to teach: {values_to_teach}" if activities_and_toys or values_to_teach else ""
        try:
            st.session_state.story, generation_time = generate_story(children_info_str, story_details, st.session_state.language)
            # Insert usage stats immediately after generating the story
            ages = ",".join([info.split(',')[1].strip().split()[0] for info in children_info])
            st.session_state.row_id = insert_usage_stats(st.session_state.language, num_children, ages, values_to_teach, selected_model, generation_time)
        except ValueError as e:
            st.error(f"Error: {str(e)}")
            st.session_state.story = None
            # Log the moderated content case with all user inputs
            ages = ",".join([info.split(',')[1].strip().split()[0] for info in children_info])
            st.session_state.row_id = insert_usage_stats(
                st.session_state.language, 
                num_children, 
                ages, 
                values_to_teach, 
                selected_model,
                0,  # Set generation time to 0 for moderated content
                moderated=True,
                children_info=children_info,
                activities_and_toys=activities_and_toys
            )

if st.session_state.story:
    st.subheader(get_text("your_story"))
    
    # Display the story and values side by side only if values are provided
    if values_to_teach.strip():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(st.session_state.story)
        with col2:
            st.subheader(get_text("story_values"))
            for value in values_to_teach.split(','):
                st.write(f"• {value.strip()}")
    else:
        st.write(st.session_state.story)
    
    # Add feedback widget
    st.markdown("---")  # Add a horizontal line for separation
    st.markdown(f"<i>{get_text('rate_story')}</i>", unsafe_allow_html=True)  # Use italic text
    feedback = st.feedback(
        options="stars",
        key=f"feedback_{st.session_state.row_id}"
    )
    
    if feedback is not None:
        rating = feedback + 1  # Convert 0-4 scale to 1-5 scale
        update_rating(st.session_state.row_id, rating)
        st.success(get_text("thank_you_rating"))

else:
    st.write(get_text("instructions"))

# Add some space before the Buy Me a Coffee button
st.markdown("<br><br>", unsafe_allow_html=True)

# Buy Me a Coffee button
st.markdown(
    f"""
    <div style="text-align: center; margin-top: 20px;">
        <a href="https://www.buymeacoffee.com/raunou"><img src="https://img.buymeacoffee.com/button-api/?text={get_text('buy_coffee')}&emoji=☕&slug=raunou&button_colour=b89f00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=FFDD00" /></a>
    </div>
    """,
    unsafe_allow_html=True
)
# Add general help text using markdown with small font and italic styling
st.markdown(f"<br><p style='font-size: 12px; font-style: italic;'>{get_text('general_help_text')}</p>", unsafe_allow_html=True)