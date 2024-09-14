import streamlit as st
import openai
import anthropic  # New import for Anthropic's API
import os

# Set page config
st.set_page_config(
    page_title="Bedtime Story Generator",
    page_icon="🌙" 
)

# Set up API keys
openai.api_key = st.secrets["OPENAI_API_KEY"]
anthropic_api_key = st.secrets["ANTHROPIC_API_KEY"]  # New line for Anthropic API key

# Get the model from secrets.toml
selected_model = st.secrets["MODEL"]


# Define translations with flag image URLs
translations = {
    "English": {
        "title": "🌙 Bedtime Storyteller",
        "story_settings": "📚 Story Settings",
        "language_select": "🌍 Language",
        "num_children": "👧👦 Number of children",
        "child": "Child",
        "name": "Name of child",
        "age": "Age",
        "activities_and_toys": "🧸🎨 Favorite toys, activities, and today's events",
        "activities_help": "E.g., teddy bear, coloring books, played in the park, had ice cream",
        "generate_button": "✨ Generate Story",
        "creating_story": "🖊️ Creating your magical story...",
        "your_story": "🌟 Your Personalized Bedtime Story",
        "instructions": "👈 Enter the details in the sidebar and click 'Generate Story' to create your personalized bedtime story.",
        "values_to_teach": "📚 Values or lessons to teach",
        "story_values": "Lessons taught in the story:",
        "buy_coffee": "Buy Me a Coffee"
    },
    "Español": {
        "title": "🌙 Narrador de Cuentos para Dormir",
        "story_settings": "📚 Configuración del Cuento",
        "language_select": "🌍 Idioma",
        "num_children": "👧👦 Número de niños",
        "child": "Niño",
        "name": "Nombre del niño",
        "age": "Edad",
        "activities_and_toys": "🧸🎨 Juguetes favoritos, actividades y eventos de hoy",
        "activities_help": "Por ejemplo, oso de peluche, libros para colorear, jugó en el parque, comió helado",
        "generate_button": "✨ Generar Cuento",
        "creating_story": "🖊️ Creando tu cuento mágico...",
        "your_story": "🌟 Tu Cuento Personalizado para Dormir",
        "instructions": "👈 Ingresa los detalles en la barra lateral y haz clic en 'Generar Cuento' para crear tu cuento personalizado para dormir.",
        "values_to_teach": "📚 Valores o lecciones para enseñar",
        "story_values": "Lecciones enseñadas en el cuento:",
        "buy_coffee": "Cómprame un Café"
    },
    "Eesti": {
        "title": "🌙 Unejutuvestja",
        "story_settings": "📚 Loo Seaded",
        "language_select": "🌍 Keel",
        "num_children": "👧👦 Laste arv",
        "child": "Laps",
        "name": "Lapse nimi",
        "age": "Vanus",
        "activities_and_toys": "🧸🎨 Lemmikmänguasjad, tegevused ja tänased sündmused",
        "activities_help": "Nt. kaisukaru, värvimisraamatud, mängis pargis, sõi jäätist",
        "generate_button": "✨ Loo Jutt",
        "creating_story": "🖊️ Loome sinu maagilist lugu...",
        "your_story": "🌟 Sinu Personaliseeritud Unejutt",
        "instructions": "👈 Sisesta üksikasjad külgribal ja klõpsa 'Loo Jutt', et luua oma personaliseeritud unejutt.",
        "values_to_teach": "📚 Õpetatavad väärtused või õppetunnid",
        "story_values": "Loos õpetatud õppetunnid:",
        "buy_coffee": "Osta mulle tass kohvi"
    },
    "Latviešu": {
        "title": "🌙 Vakara Pasaku Stāstītājs",
        "story_settings": "📚 Stāsta Iestatījumi",
        "language_select": "🌍 Valoda",
        "num_children": "👧👦 Bērnu skaits",
        "child": "Bērns",
        "name": "Bērna vārds",
        "age": "Vecums",
        "activities_and_toys": "🧸🎨 Mīļākās rotaļlietas, aktivitātes un šodienas notikumi",
        "activities_help": "Piemēram, lācītis, krāsojamās grāmatas, spēlējās parkā, ēda saldējumu",
        "generate_button": "✨ Ģenerēt Stāstu",
        "creating_story": "🖊️ Veidojam jūsu brīnumaino stāstu...",
        "your_story": "🌟 Jūsu Personalizētā Vakara Pasaka",
        "instructions": "👈 Ievadiet detaļas sānu joslā un noklikšķiniet uz 'Ģenerēt Stāstu', lai izveidotu savu personalizēto vakara pasaku.",
        "values_to_teach": "📚 Vērtības vai mācības, ko pasniegt",
        "story_values": "Stāstā mācītās mācības:",
        "buy_coffee": "Nopērc man kafiju"
    },
    "Suomi": {
        "title": "🌙 Iltasadun Kertoja",
        "story_settings": "📚 Tarinan Asetukset",
        "language_select": "🌍 Kieli",
        "num_children": "👧👦 Lasten lukumäärä",
        "child": "Lapsi",
        "name": "Lapsen nimi",
        "age": "Ikä",
        "activities_and_toys": "🧸🎨 Lempilelut, aktiviteetit ja päivän tapahtumat",
        "activities_help": "Esim. nalle, värityskirjat, leikki puistossa, söi jäätelöä",
        "generate_button": "✨ Luo Tarina",
        "creating_story": "🖊️ Luomme taianomaista tarinaasi...",
        "your_story": "🌟 Sinun Personoitu Iltasatusi",
        "instructions": "👈 Syötä tiedot sivupalkissa ja napsauta 'Luo Tarina' luodaksesi personoidun iltasatusi.",
        "values_to_teach": "📚 Opetettavat arvot tai opetukset",
        "story_values": "Tarinassa opetetut opetukset:",
        "buy_coffee": "Osta minulle kahvi"
    },
    "Русский": {
        "title": "🌙 Рассказчик Сказок на Ночь",
        "story_settings": "📚 Настройки Сказки",
        "language_select": "🌍 Язык",
        "num_children": "👧👦 Количество детей",
        "child": "Ребенок",
        "name": "Имя ребенка",
        "age": "Возраст",
        "activities_and_toys": "🧸🎨 Любимые игрушки, занятия и события сегодняшнего дня",
        "activities_help": "Например, плюшевый мишка, раскраски, играл в парке, ел мороженое",
        "generate_button": "✨ Создать Сказку",
        "creating_story": "🖊️ Создаем вашу волшебную сказку...",
        "your_story": "🌟 Ваша Персонализированная Сказка на Ночь",
        "instructions": "👈 Введите детали в боковой панели и нажмите 'Создать Сказку', чтобы создать свою персонализированную сказку на ночь.",
        "values_to_teach": "📚 Ценности или уроки для обучения",
        "story_values": "Уроки, преподанные в сказке:",
        "buy_coffee": "Купи мне кофе"
    }
}
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

    prompt = f"""Create a bedtime story for the following children:
    {children_info}
    
    Story details: {story_details}
    
    The story should be educational and specifically teach the following values: {values_to_teach}.
    Make sure these values are central to the story's plot and characters' actions.
    Incorporate the mentioned activities, toys, and events into the story.
    Please write the story in {language}.
    
    The story should be {complexity}, as the average age of the children is {avg_age:.1f} years old.
    Adjust the language, concepts, and storyline to be engaging and understandable for children of this age group."""

    if selected_model == "gpt-4o" or selected_model == "gpt-4o-mini":
        response = openai.ChatCompletion.create(
            model=selected_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message.content
    elif selected_model == "claude-3-5-sonnet-20240620":
        client = anthropic.Anthropic(api_key=anthropic_api_key)
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    else:
        raise ValueError(f"Unsupported model: {selected_model}")


# Initialize session state for language
if 'language' not in st.session_state:
    st.session_state.language = 'Eesti'

# Language selection using selectbox
selected_language = st.sidebar.selectbox(
    get_text("language_select"),
    options=list(translations.keys()),
    index=list(translations.keys()).index(st.session_state.language)
)

if selected_language != st.session_state.language:
    st.session_state.language = selected_language
    st.experimental_rerun()

# Add header image
image_path = os.path.join("static", "images", "header.png")
st.image(image_path, use_column_width=True)

st.title(get_text("title"))

# Move input options to sidebar
with st.sidebar:
    st.header(get_text("story_settings"))

    num_children = st.number_input(get_text("num_children"), min_value=1, max_value=5, value=1)

    children_info = []
    for i in range(num_children):
        st.subheader(f"{get_text('child')} {i+1} 🧒")
        name = st.text_input(f"{get_text('name')} {i+1}", key=f"name_{i}")
        age = st.slider(f"{get_text('age')} {name}", min_value=1, max_value=12, value=6, key=f"age_{i}")
        children_info.append(f"{name}, {age} years old")

    activities_and_toys = st.text_area(
        get_text("activities_and_toys"),
        help=get_text("activities_help")
    )
    values_to_teach = st.text_input(get_text("values_to_teach"))

    generate_button = st.button(get_text("generate_button"))

story_details = f"""
Activities, toys, and events: {activities_and_toys}
Values to teach: {values_to_teach}
"""

# Main area for displaying the story
if generate_button:
    with st.spinner(get_text("creating_story")):
        children_info_str = "\n".join(children_info)
        story = generate_story(children_info_str, story_details, st.session_state.language)
    st.subheader(get_text("your_story"))
    
    # Display the story and values side by side
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(story)
    with col2:
        st.subheader(get_text("story_values"))
        for value in values_to_teach.split(','):
            st.write(f"• {value.strip()}")
else:
    st.write(get_text("instructions"))
# Buy Me a Coffee button
st.markdown(
    f"""
    <div style="text-align: center; margin-top: 20px;">
        <a href="https://www.buymeacoffee.com/raunou"><img src="https://img.buymeacoffee.com/button-api/?text={get_text('buy_coffee')}&emoji=☕&slug=raunou&button_colour=b89f00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=FFDD00" /></a>
    </div>
    """,
    unsafe_allow_html=True
)
