import streamlit as st
import openai
import anthropic
import os
from datetime import datetime
from supabase import create_client, Client

# Set page config
st.set_page_config(
    page_title="Bedtime Story Generator",
    page_icon="🌙" 
)

# Set up API keys
openai.api_key = st.secrets["OPENAI_API_KEY"]
anthropic_api_key = st.secrets["ANTHROPIC_API_KEY"]

# Get the model from secrets.toml
selected_model = st.secrets["MODEL"]

# Set up Supabase client
supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

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
        "buy_coffee": "Buy Me a Coffee",
        "rate_story": "Rate this story",
        "thank_you_rating": "Thank you for your rating!",
        "submit_rating": "Submit Rating",
        "general_help_text": "📝 This app generates AI-powered bedtime stories based on your input. The stories are unique, created in real-time and are not stored. Head to bed with a smile!"
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
        "buy_coffee": "Cómprame un Café",
        "rate_story": "Califica esta historia",
        "thank_you_rating": "¡Gracias por tu calificación!",
        "submit_rating": "Enviar Calificación",
        "general_help_text": "📝 Esta aplicación genera cuentos para dormir impulsados por IA basados en tu entrada. Las historias son únicas, creadas en tiempo real y no se almacenan. ¡Duerme con una sonrisa!"
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
        "activities_help": "Nt. kaisukaru Peeter, meeldivad puzled, mängisid pargis, sõi jäätist",
        "generate_button": "✨ Loo Jutt",
        "creating_story": "🖊️ Loome sinu maagilist lugu...",
        "your_story": "🌟 Sinu Personaliseeritud Unejutt",
        "instructions": "👈 Sisesta üksikasjad külgribal ja klõpsa 'Loo Jutt', et luua oma personaliseeritud unejutt.",
        "values_to_teach": "📚 Õpetatavad väärtused või õppetunnid",
        "story_values": "Loo õppetunnid:",
        "buy_coffee": "Osta mulle tass kohvi",
        "rate_story": "Hinda seda lugu",
        "thank_you_rating": "Täname tagasiside eest!",
        "submit_rating": "Esita Hinnang",
        "general_help_text": "📝 See rakendus genereerib tehisintellekti abil unejutte vastavalt teie sisendile. Lood on unikaalsed, need luuakse reaalajas ja neid ei salvestata. Head Und!"
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
        "buy_coffee": "Nopērc man kafiju",
        "rate_story": "Vērtējiet šo stāstu",
        "thank_you_rating": "Paldies par jūsu vērtējumu!",
        "submit_rating": "Iesniegt Vērtējumu",
        "general_help_text": "📝 Šī lietotne ģenerē mākslīgā intelekta radītus vakara stāstus, pamatojoties uz jūsu ievadi. Stāsti ir unikāli, tiek veidoti reālajā laikā un netiek saglabāti. Iesiet mājās ar vienmērīgu smieklu!"
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
        "buy_coffee": "Osta minulle kahvi",
        "rate_story": "Arvioi tämä tarina",
        "thank_you_rating": "Kiitos arvostelustasi!",
        "submit_rating": "Lähetä Arvostelu",
        "general_help_text": "📝 Tämä sovellus luo tekoälyllä tuotettuja iltasatuja antamiesi tietojen perusteella. Tarinat ovat unikkaita, luodaan reaaliajassa eikä niitä tallenneta. "
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
        "buy_coffee": "Купи мне кофе",
        "rate_story": "Оцените эту сказку",
        "thank_you_rating": "Спасибо за вашу оценку!",
        "submit_rating": "Отправить Оценку",
        "general_help_text": "📝 Это приложение генерирует сказки на ночь с помощью ИИ на основе вашего ввода. Истории уникальны, создаются в реальном времени и не сохраняются. "
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
    
    {story_details if story_details else "Create an imaginative story suitable for children."}
    
    Please write the story in {language}.
    
    The story should be {complexity}, as the average age of the children is {avg_age:.1f} years old.
    Adjust the language, concepts, and storyline to be engaging and understandable for children of this age group.
    
    If no specific details were provided, create an imaginative and engaging story that focuses on universal themes like friendship, kindness, or curiosity. Use the children's names and ages to personalize the story.
    
    Ensure the story has a clear beginning, middle, and end, with a positive message or lesson appropriate for children."""

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

def insert_usage_stats(selected_language, num_children, ages, values_to_teach, selected_model):
    current_time = datetime.now().isoformat()
    data = {
        "datetime": current_time,
        "selected_language": selected_language,
        "num_children": num_children,
        "ages": ages,
        "values_to_teach": values_to_teach,
        "selected_model": selected_model
    }
    try:
        response = supabase.table("usage_stats").insert(data).execute()
        return response.data[0]['id']
    except Exception:
        return None

def update_rating(row_id, rating):
    try:
        rating_str = str(rating)
        supabase.table("usage_stats").update({"rating": rating_str}).eq("id", row_id).execute()
    except Exception:
        pass

# Initialize session state variables
if 'story' not in st.session_state:
    st.session_state.story = None
if 'row_id' not in st.session_state:
    st.session_state.row_id = None

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
    st.rerun()  # Use st.rerun() instead of st.experimental_rerun()

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
        st.session_state.story = generate_story(children_info_str, story_details, st.session_state.language)
    
    # Insert usage stats immediately after generating the story
    ages = ",".join([info.split(',')[1].strip().split()[0] for info in children_info])
    st.session_state.row_id = insert_usage_stats(st.session_state.language, num_children, ages, values_to_teach, selected_model)

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

