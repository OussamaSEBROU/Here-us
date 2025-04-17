import streamlit as st
import requests
import os
import base64
from PIL import Image
import io
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="Here Us! From the River To the Sea",
    page_icon="🇵🇸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure Gemini with your API key
google_api_key = os.getenv("GOOGLE_API_KEY")
if google_api_key:
    genai.configure(api_key=google_api_key)

# Function to check if query is related to Palestine
def is_palestine_related(query):
    # List of keywords related to Palestine
    palestine_keywords = [
        "palestine", "palestinian", "gaza", "west bank", "jerusalem", "al-quds", 
        "israel", "israeli", "occupation", "intifada", "nakba", "hamas", "fatah", 
        "plo", "bds", "boycott", "settlement", "settler", "zionism", "zionist",
        "al-aqsa", "dome of rock", "hebron", "ramallah", "bethlehem", "nablus",
        "jenin", "rafah", "khan younis", "unrwa", "refugee", "right of return",
        "oslo", "two-state", "one-state", "apartheid", "wall", "barrier",
        "checkpoint", "blockade", "olive", "resistance", "martyr", "shahid",
        "idf", "arab", "middle east", "levant", "holy land", "balfour",
        "1948", "1967", "intifada", "uprising", "protest", "demonstration",
        "solidarity", "human rights", "international law", "un resolution",
        "occupation", "colonization", "annexation", "displacement", "demolition",
        "prisoner", "detention", "administrative detention", "hunger strike",
        "flotilla", "aid", "humanitarian", "ceasefire", "peace process",
        "negotiation", "mediation", "conflict", "war", "attack", "bombing",
        "airstrike", "rocket", "tunnel", "border", "crossing", "siege",
        "sanction", "embargo", "economy", "water", "electricity", "infrastructure",
        "education", "health", "culture", "heritage", "identity", "diaspora",
        "return", "citizenship", "stateless", "nationality", "flag", "keffiyeh",
        "olive tree", "key", "map", "border", "1948", "1967", "partition",
        "resolution", "un", "unesco", "icj", "icc", "amnesty", "hrw", "btselem",
        "pchr", "al haq", "adalah", "badil", "passia", "miftah", "pngo",
        "pflp", "dflp", "jihad", "islamic", "christian", "muslim", "jew",
        "holy site", "temple mount", "haram al-sharif", "church of nativity",
        "ibrahimi mosque", "cave of patriarchs", "rachel's tomb", "joseph's tomb",
        "from the river to the sea", "free palestine", "save palestine"
    ]
    
    query_lower = query.lower()
    
    # Check if any of the keywords are in the query
    for keyword in palestine_keywords:
        if keyword in query_lower:
            return True
    
    return False

# Function to generate text response with Gemini
def generate_text_response(prompt, is_palestine=True):
    if not google_api_key:
        return "Error: Gemini API key not found. Please set the GOOGLE_API_KEY environment variable."
    
    try:
        # Load Gemini model for text
        model_text = genai.GenerativeModel(
            model_name="gemini-2.0-flash-thinking-exp-01-21",
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=0.95,
                top_k=40,
                max_output_tokens=4000  # Increased token limit for deeper, longer responses
            )
        )
        
        if not is_palestine:
            return "Sorry, I'm trained only to answer questions about the Palestinian cause and related topics. Please ask a question related to Palestine, its history, culture, or current situation."
        
        # Generate response
        response = model_text.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Function to generate image with Gemini
def generate_image(prompt, style="realistic", theme="educational", size="medium"):
    if not google_api_key:
        return None, "Error: Gemini API key not found. Please set the GOOGLE_API_KEY environment variable."
    
    try:
        # Load Gemini model for image generation
        model_image = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp-image-generation"
        )
        
        # Style descriptions
        style_prompts = {
            "realistic": "a realistic and detailed image",
            "artistic": "an artistic and expressive image",
            "infographic": "an informative and clear infographic",
            "cartoon": "a cartoon-style illustration",
            "sketch": "an expressive line sketch"
        }
        
        # Theme descriptions
        theme_prompts = {
            "historical": "with Palestinian historical context",
            "cultural": "highlighting Palestinian culture and heritage",
            "political": "illustrating the Palestinian political situation",
            "educational": "for educational purposes about Palestine",
            "solidarity": "expressing solidarity with Palestine"
        }
        
        # Get style and theme descriptions
        style_desc = style_prompts.get(style, style_prompts["realistic"])
        theme_desc = theme_prompts.get(theme, theme_prompts["educational"])
        
        # Build complete prompt
        full_prompt = f"Generate {style_desc} about Palestine {theme_desc}: {prompt}"
        
        # Define dimensions based on size
        dimensions = {
            "small": (512, 512),
            "medium": (768, 768),
            "large": (1024, 1024)
        }
        
        size_config = dimensions.get(size, dimensions["medium"])
        
        # Generate image
        response = model_image.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7
            )
        )
        
        # Extract image data
        if hasattr(response, 'candidates') and len(response.candidates) > 0:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    return part.inline_data.data, None
        
        return None, "Error generating image. Please try again."
    except Exception as e:
        return None, f"Error: {str(e)}"

# Function to convert base64 image to downloadable link
def get_image_download_link(img_str, filename, text):
    b64 = img_str.split(",")[1] if "," in img_str else img_str
    href = f'<a href="data:image/png;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Function to search reliable sources
def search_reliable_sources(query):
    # List of reliable domains
    reliable_domains = [
        "aljazeera.com", "middleeasteye.net", "metras.co",
        "aa.com.tr", "palestinechronicle.com", "electronicintifada.net",
        "btselem.org", "amnesty.org", "hrw.org", "un.org", "unrwa.org",
        "ochaopt.org", "palestinestudies.org", "mondoweiss.net"
    ]
    
    # Search query
    search_query = f"Palestine {query} site:aljazeera.com OR site:middleeasteye.net OR site:aa.com.tr"
    
    # Sample sources for demonstration
    sample_sources = [
        {
            "title": "The history of Palestine: A chronology of key events",
            "url": "https://www.aljazeera.com/news/2023/5/15/the-history-of-palestine-a-chronology-of-key-events",
            "snippet": "A look at the major events that have shaped Palestinian history...",
            "source": "Al Jazeera"
        },
        {
            "title": "Palestine and Israel: Mapping an annexation",
            "url": "https://www.aljazeera.com/news/2020/7/2/palestine-and-israel-mapping-an-annexation",
            "snippet": "Interactive map of Palestine showing the effects of Israel's annexation plans...",
            "source": "Al Jazeera"
        },
        {
            "title": "What's the history of the Israel-Palestinian conflict?",
            "url": "https://www.middleeasteye.net/news/israel-palestine-conflict-history-explained",
            "snippet": "The roots of the Israel-Palestinian conflict explained...",
            "source": "Middle East Eye"
        },
        {
            "title": "Timeline: Israel's attacks on Gaza and the Palestinian resistance",
            "url": "https://www.aa.com.tr/en/middle-east/timeline-israels-attacks-on-gaza-and-the-palestinian-resistance/2866227",
            "snippet": "A comprehensive timeline of the recent events in Gaza...",
            "source": "Anadolu Agency"
        }
    ]
    
    # Filter sources based on query (simulation)
    filtered_sources = []
    query_terms = query.lower().split()
    
    for source in sample_sources:
        relevance_score = 0
        for term in query_terms:
            if term in source["title"].lower() or term in source["snippet"].lower():
                relevance_score += 1
        
        if relevance_score > 0:
            filtered_sources.append(source)
    
    return filtered_sources

# Function to get boycott data
def get_boycott_data():
    # Predefined boycott data based on research
    boycott_data = {
        "Food & Beverages": {
            "companies": [
                {
                    "name": "Starbucks",
                    "reason": "Howard Schultz is the largest private owner of Starbucks shares and is a staunch zionist who invests heavily in Israel's economy, including a recent $1.7 billion investment in cybersecurity startup Wiz.",
                    "action": "Don't buy Starbucks. Don't sell Starbucks On the Go. Don't work for Starbucks.",
                    "alternatives": ["Caffe Nero", "Local independent cafes"]
                },
                {
                    "name": "Coca-Cola",
                    "reason": "Coca-Cola has a bottling plant in the Atarot Industrial Zone, an illegal Israeli settlement in occupied East Jerusalem.",
                    "action": "Boycott all Coca-Cola products, including Sprite, Fanta, and other associated brands.",
                    "alternatives": ["Local beverage brands", "Homemade sparkling water"]
                },
                {
                    "name": "McDonald's",
                    "reason": "McDonald's Israel provided thousands of free meals to Israeli soldiers during military operations in Gaza.",
                    "action": "Don't eat at McDonald's.",
                    "alternatives": ["Local restaurants", "Local fast food chains"]
                },
                {
                    "name": "Nestlé",
                    "reason": "Nestlé has been operating in Israel since 1995 and has production facilities in contested areas.",
                    "action": "Avoid Nestlé products, including bottled water, cereals, and dairy products.",
                    "alternatives": ["Local brands", "Artisanal products"]
                }
            ]
        },
        "Technology": {
            "companies": [
                {
                    "name": "HP (Hewlett-Packard)",
                    "reason": "HP provides technologies used in Israel's control and surveillance system, including for military checkpoints.",
                    "action": "Don't buy HP products, including computers, printers, and supplies.",
                    "alternatives": ["Lenovo", "Brother", "Epson"]
                },
                {
                    "name": "Microsoft",
                    "reason": "Microsoft invested $1.5 billion in an Israeli AI company and has a major R&D center in Israel.",
                    "action": "Use open source alternatives when possible.",
                    "alternatives": ["Linux", "LibreOffice", "Open source alternatives"]
                },
                {
                    "name": "Google",
                    "reason": "Google signed a $1.2 billion cloud computing contract with the Israeli government (Project Nimbus).",
                    "action": "Use alternative search engines and services.",
                    "alternatives": ["DuckDuckGo", "ProtonMail", "Firefox"]
                },
                {
                    "name": "Siemens",
                    "reason": "Siemens provides technologies used in Israeli infrastructure, including in occupied territories.",
                    "action": "Avoid Siemens products when alternatives are available.",
                    "alternatives": ["Bosch", "Other appliance manufacturers"]
                }
            ]
        },
        "Fashion & Clothing": {
            "companies": [
                {
                    "name": "Puma",
                    "reason": "Puma sponsors the Israel Football Association, which includes teams in illegal settlements.",
                    "action": "Don't buy Puma products.",
                    "alternatives": ["Adidas", "New Balance", "Local brands"]
                },
                {
                    "name": "Skechers",
                    "reason": "Skechers has stores in illegal Israeli settlements and maintains business partnerships in Israel.",
                    "action": "Boycott Skechers shoes and clothing.",
                    "alternatives": ["Brooks", "ASICS", "Ethical brands"]
                },
                {
                    "name": "H&M",
                    "reason": "H&M operates stores in Israel, including in contested areas.",
                    "action": "Don't shop at H&M.",
                    "alternatives": ["Ethical fashion brands", "Second-hand clothing"]
                },
                {
                    "name": "Zara",
                    "reason": "Zara has stores in Israel and sources from Israeli suppliers.",
                    "action": "Avoid shopping at Zara.",
                    "alternatives": ["Local brands", "Independent boutiques"]
                }
            ]
        },
        "Cosmetics": {
            "companies": [
                {
                    "name": "L'Oréal",
                    "reason": "L'Oréal operates in Israel and has acquired Israeli cosmetics companies.",
                    "action": "Boycott L'Oréal products and its associated brands.",
                    "alternatives": ["The Body Shop", "Lush", "Natural brands"]
                },
                {
                    "name": "Estée Lauder",
                    "reason": "Estée Lauder chairman, Ronald Lauder, is a strong supporter of Israel and funds pro-Israel organizations.",
                    "action": "Don't buy Estée Lauder products and its associated brands.",
                    "alternatives": ["Ethical cosmetics brands", "Natural products"]
                },
                {
                    "name": "Yves Saint Laurent Beauty / YSL Beauty",
                    "reason": "YSL Beauty is owned by L'Oréal Group, which operates in Israel and has ties to Israeli companies.",
                    "action": "Avoid YSL Beauty products.",
                    "alternatives": ["Ethical cosmetics brands", "Natural products"]
                }
            ]
        },
        "Finance": {
            "companies": [
                {
                    "name": "eToro",
                    "reason": "eToro is an Israeli online trading company that supports Israel's economy.",
                    "action": "Use other trading and investment platforms.",
                    "alternatives": ["Alternative trading platforms", "Ethical banks"]
                },
                {
                    "name": "PayPal",
                    "reason": "PayPal operates in Israel but refuses to provide its services to Palestinians in the occupied territories.",
                    "action": "Use alternatives to PayPal when possible.",
                    "alternatives": ["Wise", "Local banking services"]
                }
            ]
        },
        "Other": {
            "companies": [
                {
                    "name": "SodaStream",
                    "reason": "SodaStream operated a factory in an illegal Israeli settlement in the occupied West Bank before relocating due to pressure.",
                    "action": "Don't buy SodaStream products.",
                    "alternatives": ["Bottled sparkling water", "Other carbonation systems"]
                },
                {
                    "name": "Volvo Heavy Machinery",
                    "reason": "Volvo heavy equipment is used for demolishing Palestinian homes and building illegal settlements.",
                    "action": "Raise awareness about the use of Volvo equipment in occupied territories.",
                    "alternatives": ["Other heavy equipment manufacturers"]
                },
                {
                    "name": "Caterpillar",
                    "reason": "Caterpillar bulldozers are used to demolish Palestinian homes and build the illegal separation wall.",
                    "action": "Boycott Caterpillar products and raise awareness about their use.",
                    "alternatives": ["Other construction equipment manufacturers"]
                }
            ]
        }
    }
    
    return boycott_data

# CSS styles for ChatGPT-like interface
def apply_styles():
    st.markdown("""
    <style>
        /* Global styles */
        body {
            font-family: 'Söhne', 'Segoe UI', sans-serif;
            color: #1a1a1a;
            background-color: #f7f7f8;
        }
        
        /* Main container */
        .main {
            padding: 0 !important;
            max-width: 100% !important;
        }
        
        /* Header styles */
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 2rem;
            color: #202123;
        }
        
        /* Sidebar styles */
        .css-1d391kg {
            background-color: #202123;
        }
        
        /* Chat container */
        .chat-container {
            display: flex;
            flex-direction: column;
            height: calc(100vh - 180px);
            overflow-y: auto;
            padding: 0 15%;
            margin-bottom: 80px;
        }
        
        /* Message styles */
        .user-message {
            background-color: #f7f7f8;
            padding: 1rem 15%;
            border-bottom: 1px solid rgba(0,0,0,0.1);
            display: flex;
            align-items: flex-start;
        }
        
        .assistant-message {
            background-color: #ffffff;
            padding: 1rem 15%;
            border-bottom: 1px solid rgba(0,0,0,0.1);
            display: flex;
            align-items: flex-start;
        }
        
        .message-avatar {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            margin-right: 15px;
            flex-shrink: 0;
        }
        
        .message-content {
            flex-grow: 1;
            overflow-wrap: break-word;
        }
        
        /* Input area */
        .input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 1rem 15%;
            background-color: #ffffff;
            border-top: 1px solid rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
        }
        
        .input-box {
            flex-grow: 1;
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            border: 1px solid rgba(0,0,0,0.1);
            background-color: #ffffff;
            font-size: 1rem;
            line-height: 1.5;
            max-height: 200px;
            overflow-y: auto;
        }
        
        .send-button {
            margin-left: 0.5rem;
            background-color: #10a37f;
            color: white;
            border: none;
            border-radius: 0.25rem;
            padding: 0.5rem 1rem;
            cursor: pointer;
        }
        
        /* Button styles */
        .stButton button {
            border-radius: 0.5rem;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            font-weight: 500;
            transition: all 0.2s ease;
            border: 1px solid rgba(0,0,0,0.1);
            background-color: #ffffff;
        }
        
        .stButton button:hover {
            background-color: #f0f0f0;
        }
        
        /* Quick action buttons */
        .quick-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 20px;
            margin-bottom: 20px;
            justify-content: center;
        }
        
        .action-button {
            display: flex;
            align-items: center;
            padding: 12px 20px;
            background-color: #ffffff;
            border: 1px solid rgba(0,0,0,0.1);
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
            color: #202123;
        }
        
        .action-button:hover {
            background-color: #f0f0f0;
            transform: translateY(-2px);
        }
        
        .action-icon {
            margin-right: 10px;
            font-size: 1.2rem;
        }
        
        /* Welcome screen */
        .welcome-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: calc(100vh - 100px);
            text-align: center;
            padding: 0 15%;
        }
        
        .welcome-title {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #202123;
        }
        
        .welcome-subtitle {
            font-size: 1.2rem;
            color: #6e6e80;
            margin-bottom: 2rem;
            max-width: 600px;
        }
        
        /* Palestine cause description */
        .cause-description {
            background-color: rgba(16, 163, 127, 0.1);
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-bottom: 2rem;
            border-left: 4px solid #10a37f;
        }
        
        /* Sidebar navigation */
        .sidebar-nav {
            padding: 1rem;
        }
        
        .sidebar-nav-item {
            display: flex;
            align-items: center;
            padding: 0.75rem 1rem;
            border-radius: 0.25rem;
            cursor: pointer;
            transition: background-color 0.2s ease;
            color: #ececf1;
            text-decoration: none;
            margin-bottom: 0.5rem;
        }
        
        .sidebar-nav-item:hover {
            background-color: rgba(255,255,255,0.1);
        }
        
        .sidebar-nav-item.active {
            background-color: rgba(255,255,255,0.2);
        }
        
        .sidebar-icon {
            margin-right: 0.75rem;
            width: 16px;
            text-align: center;
        }
        
        /* Section styles */
        .section-header {
            font-size: 1.8rem;
            font-weight: bold;
            margin-top: 1rem;
            margin-bottom: 1rem;
            color: #202123;
            border-bottom: 1px solid rgba(0,0,0,0.1);
            padding-bottom: 0.5rem;
        }
        
        .section-content {
            margin-bottom: 2rem;
        }
        
        /* Card styles */
        .card {
            background-color: #ffffff;
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: all 0.2s ease;
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .card-title {
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: #202123;
        }
        
        .card-content {
            color: #353740;
        }
        
        /* Team member card */
        .team-member {
            display: flex;
            align-items: center;
            background-color: #ffffff;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .team-avatar {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            margin-right: 1rem;
        }
        
        .team-info {
            flex-grow: 1;
        }
        
        .team-name {
            font-weight: bold;
            margin-bottom: 0.25rem;
        }
        
        .team-role {
            color: #6e6e80;
            font-size: 0.9rem;
        }
        
        /* Contact form */
        .contact-form {
            background-color: #ffffff;
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .form-group {
            margin-bottom: 1rem;
        }
        
        .form-label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        .form-input {
            width: 100%;
            padding: 0.75rem;
            border-radius: 0.25rem;
            border: 1px solid rgba(0,0,0,0.1);
            font-size: 1rem;
        }
        
        .form-textarea {
            width: 100%;
            padding: 0.75rem;
            border-radius: 0.25rem;
            border: 1px solid rgba(0,0,0,0.1);
            font-size: 1rem;
            min-height: 150px;
            resize: vertical;
        }
        
        .form-submit {
            background-color: #10a37f;
            color: white;
            border: none;
            border-radius: 0.25rem;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            cursor: pointer;
            transition: background-color 0.2s ease;
        }
        
        .form-submit:hover {
            background-color: #0d8c6d;
        }
        
        /* Help section */
        .help-item {
            background-color: #ffffff;
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .help-question {
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: #202123;
            cursor: pointer;
        }
        
        .help-answer {
            color: #353740;
            padding-top: 0.5rem;
        }
        
        /* Boycott section */
        .company-card {
            border: 1px solid rgba(0,0,0,0.1);
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
            background-color: #FFFFFF;
            transition: all 0.3s ease;
        }
        
        .company-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .company-name {
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: #202123;
        }
        
        .company-reason {
            margin-bottom: 0.5rem;
        }
        
        .company-action {
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .company-alternatives {
            font-style: italic;
        }
        
        .category-title {
            font-size: 1.5rem;
            font-weight: bold;
            margin-top: 1rem;
            margin-bottom: 1rem;
            color: #202123;
            border-bottom: 1px solid rgba(0,0,0,0.1);
            padding-bottom: 0.5rem;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 1rem;
            color: #6e6e80;
            font-size: 0.9rem;
            border-top: 1px solid rgba(0,0,0,0.1);
            margin-top: 2rem;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .chat-container, .input-container {
                padding: 1rem 5%;
            }
            
            .user-message, .assistant-message {
                padding: 1rem 5%;
            }
            
            .welcome-container {
                padding: 0 5%;
            }
            
            .welcome-title {
                font-size: 2rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'sources' not in st.session_state:
    st.session_state.sources = []

if 'gallery' not in st.session_state:
    st.session_state.gallery = []

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Apply styles
apply_styles()

# Sidebar
with st.sidebar:
    st.markdown('<div style="text-align: center; margin-bottom: 1rem;"><h2>Here Us!</h2><h3>From the River To the Sea</h3></div>', unsafe_allow_html=True)
    
    # Logo in sidebar
    st.image("https://upload.wikimedia.org/wikipedia/commons/0/00/Flag_of_Palestine.svg", width=200)
    
    # Navigation options
    st.markdown("### Navigation")
    
    # Create sidebar navigation
    if st.button("🏠 Home"):
        st.session_state.page = 'home'
    
    if st.button("❓ Knowledge & Analysis"):
        st.session_state.page = 'knowledge'
    
    if st.button("🖼️ Generate Image"):
        st.session_state.page = 'image'
    
    if st.button("✊ How to Support"):
        st.session_state.page = 'support'
    
    if st.button("🛒 Boycott Guide"):
        st.session_state.page = 'boycott'
    
    st.markdown("---")
    
    # Additional sections
    if st.button("📚 Help"):
        st.session_state.page = 'help'
    
    if st.button("ℹ️ About Us"):
        st.session_state.page = 'about'
    
    if st.button("👥 Team"):
        st.session_state.page = 'team'
    
    if st.button("📧 Contact"):
        st.session_state.page = 'contact'

# Main content based on selected page
if st.session_state.page == 'home':
    # Welcome screen
    st.markdown('<div class="welcome-container">', unsafe_allow_html=True)
    st.markdown('<div class="welcome-title">Here Us! From the River To the Sea</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-subtitle">An AI-powered platform for education, awareness, and support of the Palestinian cause</div>', unsafe_allow_html=True)
    
    # Palestine cause description
    st.markdown('<div class="cause-description">', unsafe_allow_html=True)
    st.markdown("""
    <p><strong>The Palestinian Cause</strong> is a struggle for justice, freedom, and self-determination. It represents the Palestinian people's ongoing effort to secure their fundamental rights, including the right to return to their homeland, freedom from occupation, and the establishment of an independent state.</p>
    
    <p>For decades, Palestinians have faced displacement, occupation, and systematic violations of their human rights. This platform aims to provide accurate information, raise awareness, and offer ways to support the Palestinian people in their pursuit of justice and dignity.</p>
    
    <p>From the river to the sea, Palestine will be free.</p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick action buttons
    st.markdown('<div class="quick-actions">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("❓ Ask a Question"):
            st.session_state.page = 'knowledge'
    
    with col2:
        if st.button("🖼️ Create Image"):
            st.session_state.page = 'image'
    
    with col3:
        if st.button("✊ Support"):
            st.session_state.page = 'support'
    
    with col4:
        if st.button("🛒 Boycott"):
            st.session_state.page = 'boycott'
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Section 1: Knowledge Question / Analysis
elif st.session_state.page == 'knowledge':
    st.markdown('<div class="section-header">Knowledge & Analysis</div>', unsafe_allow_html=True)
    
    st.markdown("Ask a question about Palestine and receive a detailed answer based on reliable sources.")
    
    # Check if API key is configured
    if not google_api_key:
        st.error("Gemini API key missing. Please set the GOOGLE_API_KEY environment variable.")
        st.markdown("### Instructions to set up API key:")
        st.markdown("1. Set the environment variable GOOGLE_API_KEY with your Gemini API key")
        st.markdown("2. Restart the application")
    else:
        # ChatGPT-like interface
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Display chat history
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <div class="message-avatar" style="background-color: #5436DA;">👤</div>
                    <div class="message-content">{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message">
                    <div class="message-avatar" style="background-color: #10a37f;">🇵🇸</div>
                    <div class="message-content">{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Input area
        question = st.text_input("Ask about Palestine:", placeholder="Example: What is the history of Palestine?", key="knowledge_input")
        
        if st.button("Send", key="knowledge_send"):
            if question:
                # Add user message to chat history
                st.session_state.chat_history.append({"role": "user", "content": question})
                
                # Check if question is related to Palestine
                is_palestine = is_palestine_related(question)
                
                with st.spinner("Generating answer..."):
                    if is_palestine:
                        # Prompt for Gemini with specific instructions
                        prompt = f"""
                        As an educational assistant on the Palestinian cause, provide a detailed, 
                        historical, and factual answer to the following question: "{question}"
                        
                        Your answer should:
                        1. Be informative and based on verifiable historical facts
                        2. Include references to reliable sources like Al Jazeera, Metras, and AA.com
                        3. Present different perspectives when relevant
                        4. Be structured in a clear and educational manner
                        5. Avoid bias or misinformation
                        
                        Also provide a list of recommended sources at the end.
                        """
                    else:
                        prompt = question  # Not used, but needed for function call
                    
                    response = generate_text_response(prompt, is_palestine)
                    
                    # Add assistant response to chat history
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                # Rerun to update the chat display
                st.experimental_rerun()
        
        # Search sources button
        if st.button("Search Sources", key="search_sources"):
            if question:
                # Check if question is related to Palestine
                is_palestine = is_palestine_related(question)
                
                if is_palestine:
                    with st.spinner("Searching for sources..."):
                        sources = search_reliable_sources(question)
                        st.session_state.sources = sources
                        
                        # Format sources as a message
                        if sources:
                            sources_text = "### Reliable Sources\n\n"
                            for source in sources:
                                sources_text += f"**{source['title']}**\n"
                                sources_text += f"{source['snippet']}\n"
                                sources_text += f"*{source['source']}* - [View Source]({source['url']})\n\n"
                            
                            # Add assistant response to chat history
                            st.session_state.chat_history.append({"role": "assistant", "content": sources_text})
                        else:
                            # Add assistant response to chat history
                            st.session_state.chat_history.append({"role": "assistant", "content": "No sources found. Try rephrasing your question."})
                else:
                    # Add assistant response to chat history
                    st.session_state.chat_history.append({"role": "assistant", "content": "Sorry, I'm trained only to answer questions about the Palestinian cause and related topics. Please ask a question related to Palestine, its history, culture, or current situation."})
                
                # Rerun to update the chat display
                st.experimental_rerun()

# Section 2: Generate Awareness Image
elif st.session_state.page == 'image':
    st.markdown('<div class="section-header">Generate Awareness Image</div>', unsafe_allow_html=True)
    
    st.markdown("Generate images related to Palestine to raise awareness and educate. These images can include infographics, maps, and visual representations of historical events or Palestinian heritage.")
    
    # Check if API key is configured
    if not google_api_key:
        st.error("Gemini API key missing. Please set the GOOGLE_API_KEY environment variable.")
        st.markdown("### Instructions to set up API key:")
        st.markdown("1. Set the environment variable GOOGLE_API_KEY with your Gemini API key")
        st.markdown("2. Restart the application")
    else:
        # Image customization options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            style = st.selectbox(
                "Image Style",
                options=["realistic", "artistic", "infographic", "cartoon", "sketch"],
                format_func=lambda x: {
                    "realistic": "Realistic",
                    "artistic": "Artistic",
                    "infographic": "Infographic",
                    "cartoon": "Cartoon",
                    "sketch": "Sketch"
                }[x]
            )
        
        with col2:
            theme = st.selectbox(
                "Image Theme",
                options=["historical", "cultural", "political", "educational", "solidarity"],
                format_func=lambda x: {
                    "historical": "Historical",
                    "cultural": "Cultural",
                    "political": "Political",
                    "educational": "Educational",
                    "solidarity": "Solidarity"
                }[x]
            )
        
        with col3:
            size = st.selectbox(
                "Image Size",
                options=["small", "medium", "large"],
                format_func=lambda x: {
                    "small": "Small",
                    "medium": "Medium",
                    "large": "Large"
                }[x]
            )
        
        image_prompt = st.text_input(
            "Describe the image you want to generate:", 
            placeholder="Example: A historical map of Palestine showing territorial changes over time"
        )
        
        if st.button("Generate Image"):
            if image_prompt:
                # Check if prompt is related to Palestine
                is_palestine = is_palestine_related(image_prompt)
                
                if is_palestine:
                    with st.spinner("Generating image..."):
                        image_data, error = generate_image(image_prompt, style, theme, size)
                        if image_data:
                            st.image(image_data, caption=image_prompt, use_column_width=True)
                            
                            # Add button to save image to gallery
                            if st.button("Save to Gallery"):
                                # Add image to gallery
                                st.session_state.gallery.append({
                                    "image": image_data,
                                    "prompt": image_prompt,
                                    "style": style,
                                    "theme": theme
                                })
                                st.success("Image saved to gallery!")
                                
                            # Add download link
                            st.markdown(
                                get_image_download_link(image_data, f"palestine_image_{len(st.session_state.gallery)}.png", "Download Image"),
                                unsafe_allow_html=True
                            )
                        else:
                            st.error(error or "Please enter a description to generate an image.")
                else:
                    st.error("Sorry, I'm trained only to generate images related to the Palestinian cause. Please provide a prompt related to Palestine, its history, culture, or current situation.")
            else:
                st.warning("Please enter a description to generate an image.")
        
        # Display image gallery
        if st.session_state.gallery:
            st.markdown("### Image Gallery")
            st.markdown("Here are some examples of previously generated images:")
            
            # Display images in grid
            cols = st.columns(3)
            for i, img_data in enumerate(st.session_state.gallery):
                with cols[i % 3]:
                    st.image(img_data["image"], caption=img_data["prompt"], use_column_width=True)
            
            # Button to clear gallery
            if st.button("Clear Gallery"):
                st.session_state.gallery = []
                st.experimental_rerun()

# Section 3: How to Support the Palestinian Cause
elif st.session_state.page == 'support':
    st.markdown('<div class="section-header">How to Support the Palestinian Cause</div>', unsafe_allow_html=True)
    
    st.markdown("There are many ways to support the Palestinian cause. Here are some concrete actions you can take:")
    
    # Education and awareness
    st.markdown("### 1. Educate Yourself and Raise Awareness")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Understanding to better act</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-content">Education is the essential first step to effectively support the Palestinian cause. By informing yourself about the history, culture, and current situation in Palestine, you can help raise awareness among those around you and combat misinformation.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("#### Recommended Educational Resources")
    
    # Educational resources
    education_resources = [
        {
            "title": "Palestine Remix",
            "url": "https://interactive.aljazeera.com/aje/palestineremix/",
            "description": "An interactive collection of documentaries on Palestinian history by Al Jazeera."
        },
        {
            "title": "Institute for Palestine Studies",
            "url": "https://www.palestine-studies.org/",
            "description": "An academic organization dedicated to documenting and analyzing Palestinian history."
        },
        {
            "title": "Palestine Open Maps",
            "url": "https://palopenmaps.org/",
            "description": "An interactive mapping platform showing historical Palestine before 1948."
        },
        {
            "title": "Visualizing Palestine",
            "url": "https://visualizingpalestine.org/",
            "description": "Infographics and data visualizations about Palestinian realities."
        },
        {
            "title": "The Electronic Intifada",
            "url": "https://electronicintifada.net/",
            "description": "An independent news site focused on Palestine, with in-depth analysis."
        }
    ]
    
    for resource in education_resources:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">{resource['title']}</div>
            <div class="card-content">{resource['description']}</div>
            <a href="{resource['url']}" target="_blank">Visit website</a>
        </div>
        """, unsafe_allow_html=True)
    
    # Boycott, Divestment, and Sanctions (BDS)
    st.markdown("### 2. Support the BDS Movement")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">A global non-violent movement</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-content">The BDS (Boycott, Divestment, and Sanctions) movement is a global non-violent campaign aimed at exerting economic and political pressure on Israel until it complies with international law and Palestinian rights.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("#### Current BDS Campaigns")
    
    # Current BDS campaigns
    bds_campaigns = [
        {
            "title": "Boycott Israeli products",
            "description": "Avoid buying products made in Israel or by companies that support the occupation.",
            "icon": "🛒"
        },
        {
            "title": "Puma campaign",
            "description": "Puma sponsors the Israel Football Association, which includes teams in illegal settlements.",
            "icon": "👟"
        },
        {
            "title": "HP campaign",
            "description": "HP provides technologies used in Israel's control and surveillance system.",
            "icon": "💻"
        },
        {
            "title": "Academic divestment",
            "description": "Encourage universities to divest from companies complicit in the occupation.",
            "icon": "🎓"
        },
        {
            "title": "Cultural campaign",
            "description": "Ask artists to respect the cultural boycott of Israel until it complies with international law.",
            "icon": "🎭"
        }
    ]
    
    for campaign in bds_campaigns:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">{campaign['icon']} {campaign['title']}</div>
            <div class="card-content">{campaign['description']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
    <p>For more information on current BDS campaigns and how to participate, visit the official BDS movement website: <a href="https://bdsmovement.net/" target="_blank">bdsmovement.net</a></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Donations and financial support
    st.markdown("### 3. Donate")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Direct financial support</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-content">Financial donations are essential to support humanitarian, medical, and educational organizations working directly with Palestinians. Your contribution can help provide medical care, education, and humanitarian aid.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("#### Recommended Organizations for Donations")
    
    # Recommended organizations for donations
    donation_orgs = [
        {
            "title": "Palestine Children's Relief Fund (PCRF)",
            "url": "https://www.pcrf.net/",
            "description": "Provides medical and humanitarian care to injured and sick Palestinian children."
        },
        {
            "title": "Medical Aid for Palestinians (MAP)",
            "url": "https://www.map.org.uk/",
            "description": "Provides essential medical care to Palestinians living under occupation and as refugees."
        },
        {
            "title": "UNRWA",
            "url": "https://www.unrwa.org/",
            "description": "The United Nations Relief and Works Agency for Palestine Refugees."
        },
        {
            "title": "Palestinian Red Crescent Society",
            "url": "https://www.palestinercs.org/",
            "description": "Provides emergency medical services, healthcare, and humanitarian services."
        },
        {
            "title": "Defense for Children International - Palestine",
            "url": "https://www.dci-palestine.org/",
            "description": "Defends and promotes the rights of Palestinian children in accordance with the UN Convention on the Rights of the Child."
        }
    ]
    
    for org in donation_orgs:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">{org['title']}</div>
            <div class="card-content">{org['description']}</div>
            <a href="{org['url']}" target="_blank">Donate</a>
        </div>
        """, unsafe_allow_html=True)

# Section 4: Boycott Guide
elif st.session_state.page == 'boycott':
    st.markdown('<div class="section-header">Boycott Guide</div>', unsafe_allow_html=True)
    
    st.markdown("This guide lists companies that support the Israeli occupation and offers ethical alternatives. The information is based on research and verified sources.")
    
    # Get boycott data
    boycott_data = get_boycott_data()
    
    # Boycott categories
    st.markdown("### Boycott Categories")
    
    # Category selection
    category_options = list(boycott_data.keys())
    category = st.selectbox(
        "Select a category:",
        options=category_options
    )
    
    if category and category in boycott_data:
        # Display companies in selected category
        st.markdown(f'<div class="category-title">{category}</div>', unsafe_allow_html=True)
        
        for company in boycott_data[category]["companies"]:
            st.markdown(f"""
            <div class="company-card">
                <div class="company-name">{company['name']}</div>
                <div class="company-reason"><strong>Boycott Reason:</strong> {company['reason']}</div>
                <div class="company-action"><strong>Recommended Action:</strong> {company['action']}</div>
                <div class="company-alternatives"><strong>Alternatives:</strong> {', '.join(company['alternatives'])}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    **Note: This list is regularly updated. For more detailed information, visit** [boycott.thewitness.news](https://boycott.thewitness.news).
    """)

# Help section
elif st.session_state.page == 'help':
    st.markdown('<div class="section-header">Help</div>', unsafe_allow_html=True)
    
    st.markdown("Find answers to common questions about using this platform and supporting the Palestinian cause.")
    
    # FAQ items
    faqs = [
        {
            "question": "How can I use the Knowledge & Analysis section?",
            "answer": "The Knowledge & Analysis section allows you to ask questions about Palestine and receive detailed, educational responses. Simply type your question in the input field and click 'Send'. You can also search for reliable sources related to your question by clicking the 'Search Sources' button."
        },
        {
            "question": "How does the image generation work?",
            "answer": "The image generation feature uses AI to create custom images related to Palestine. You can specify the style, theme, and size of the image, and provide a description of what you want to see. The AI will then generate an image based on your inputs. You can save generated images to your gallery or download them."
        },
        {
            "question": "What is the BDS movement?",
            "answer": "BDS stands for Boycott, Divestment, and Sanctions. It is a Palestinian-led movement promoting boycotts, divestments, and economic sanctions against Israel until it meets its obligations under international law. The movement is inspired by the South African anti-apartheid movement and aims to pressure Israel to comply with international law."
        },
        {
            "question": "How can I verify the information provided by this platform?",
            "answer": "We encourage users to verify information through multiple sources. The platform provides references to reliable sources in its responses, and you can use the 'Search Sources' feature to find additional information. We recommend cross-checking information with reputable news outlets, academic sources, and human rights organizations."
        },
        {
            "question": "How can I contribute to this platform?",
            "answer": "You can contribute by providing feedback, suggesting improvements, or reporting inaccuracies. Use the Contact section to reach out to the team. You can also help by sharing the platform with others who might benefit from its resources."
        }
    ]
    
    # Display FAQs
    for i, faq in enumerate(faqs):
        st.markdown(f"""
        <div class="help-item">
            <div class="help-question" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none'">
                {i+1}. {faq['question']}
            </div>
            <div class="help-answer">
                {faq['answer']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional help resources
    st.markdown("### Additional Resources")
    
    st.markdown("""
    <div class="card">
        <div class="card-title">BDS Movement Official Website</div>
        <div class="card-content">Learn more about the Boycott, Divestment, and Sanctions movement and how to participate.</div>
        <a href="https://bdsmovement.net/" target="_blank">Visit website</a>
    </div>
    
    <div class="card">
        <div class="card-title">Palestine Legal</div>
        <div class="card-content">Information about legal rights when advocating for Palestinian rights.</div>
        <a href="https://palestinelegal.org/" target="_blank">Visit website</a>
    </div>
    
    <div class="card">
        <div class="card-title">Al-Haq</div>
        <div class="card-content">Palestinian human rights organization with resources on international law and human rights violations.</div>
        <a href="https://www.alhaq.org/" target="_blank">Visit website</a>
    </div>
    """, unsafe_allow_html=True)

# About Us section
elif st.session_state.page == 'about':
    st.markdown('<div class="section-header">About Us</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <div class="card-title">Here Us! From the River To the Sea</div>
        <div class="card-content">
            <p>We are a dedicated team of activists, educators, and technologists committed to raising awareness about the Palestinian cause and providing accurate information to counter misinformation and bias in mainstream media.</p>
            
            <p>Our mission is to amplify Palestinian voices and stories, educate the public about the historical and current realities of Palestine, and provide practical ways for people to support the Palestinian struggle for freedom, justice, and equality.</p>
            
            <p>This platform uses AI technology to make information about Palestine more accessible and to help people engage with the cause in meaningful ways. We believe that education and awareness are powerful tools for change, and we are committed to using technology to advance the Palestinian cause.</p>
            
            <p>From the river to the sea, Palestine will be free.</p>
        </div>
    </div>
    
    <div class="card">
        <div class="card-title">Our Values</div>
        <div class="card-content">
            <ul>
                <li><strong>Truth and Accuracy:</strong> We are committed to providing factual, well-researched information about Palestine.</li>
                <li><strong>Justice and Equality:</strong> We believe in the principles of justice, equality, and human rights for all people.</li>
                <li><strong>Solidarity:</strong> We stand in solidarity with the Palestinian people in their struggle for freedom and self-determination.</li>
                <li><strong>Education:</strong> We believe in the power of education to challenge misconceptions and inspire action.</li>
                <li><strong>Nonviolence:</strong> We advocate for nonviolent resistance and peaceful means of achieving justice.</li>
            </ul>
        </div>
    </div>
    
    <div class="card">
        <div class="card-title">Our Approach</div>
        <div class="card-content">
            <p>We use AI technology to provide educational resources, generate awareness-raising images, offer guidance on supporting the Palestinian cause, and provide information about ethical consumer choices through our boycott guide.</p>
            
            <p>Our platform is designed to be accessible, informative, and action-oriented, providing users with both knowledge and practical ways to make a difference.</p>
            
            <p>We are constantly updating and improving our platform based on user feedback and the evolving situation in Palestine.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Team section
elif st.session_state.page == 'team':
    st.markdown('<div class="section-header">Our Team</div>', unsafe_allow_html=True)
    
    st.markdown("Meet the dedicated individuals behind Here Us! From the River To the Sea.")
    
    # Team members
    team_members = [
        {
            "name": "Oussama Sebrou",
            "role": "Founder & Lead Developer",
            "bio": "Oussama is a passionate advocate for Palestinian rights and a skilled developer who created this platform to make information about Palestine more accessible.",
            "image": "https://t4.ftcdn.net/jpg/02/15/84/43/360_F_215844325_ttX9YiIIyeaR7Ne6EaLLjMAmy4GvPC69.jpg"
        },
        {
            "name": "Sarah Al-Najjar",
            "role": "Content Director",
            "bio": "Sarah is a Palestinian journalist and educator who oversees the content on our platform, ensuring its accuracy and educational value.",
            "image": "https://t4.ftcdn.net/jpg/02/15/84/43/360_F_215844325_ttX9YiIIyeaR7Ne6EaLLjMAmy4GvPC69.jpg"
        },
        {
            "name": "Ahmed Khalidi",
            "role": "Research Coordinator",
            "bio": "Ahmed is a historian specializing in Palestinian history who leads our research efforts and ensures the historical accuracy of our content.",
            "image": "https://t4.ftcdn.net/jpg/02/15/84/43/360_F_215844325_ttX9YiIIyeaR7Ne6EaLLjMAmy4GvPC69.jpg"
        },
        {
            "name": "Leila Hammad",
            "role": "Outreach Coordinator",
            "bio": "Leila is an activist and community organizer who manages our outreach efforts and builds partnerships with other organizations.",
            "image": "https://t4.ftcdn.net/jpg/02/15/84/43/360_F_215844325_ttX9YiIIyeaR7Ne6EaLLjMAmy4GvPC69.jpg"
        },
        {
            "name": "Karim Nasser",
            "role": "Technical Advisor",
            "bio": "Karim is a software engineer who provides technical guidance and helps maintain and improve our platform.",
            "image": "https://t4.ftcdn.net/jpg/02/15/84/43/360_F_215844325_ttX9YiIIyeaR7Ne6EaLLjMAmy4GvPC69.jpg"
        }
    ]
    
    # Display team members
    for member in team_members:
        st.markdown(f"""
        <div class="team-member">
            <img src="{member['image']}" class="team-avatar" alt="{member['name']}">
            <div class="team-info">
                <div class="team-name">{member['name']}</div>
                <div class="team-role">{member['role']}</div>
                <div>{member['bio']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Join the team
    st.markdown("### Join Our Team")
    
    st.markdown("""
    <div class="card">
        <div class="card-title">We're looking for passionate individuals to join our cause</div>
        <div class="card-content">
            <p>If you're passionate about Palestinian rights and have skills in research, writing, design, development, or community organizing, we'd love to hear from you.</p>
            
            <p>We're particularly interested in:</p>
            <ul>
                <li>Content creators with knowledge of Palestinian history and current events</li>
                <li>Developers with experience in AI and web development</li>
                <li>Designers who can create impactful visual content</li>
                <li>Translators who can help make our content accessible in multiple languages</li>
                <li>Community organizers who can help spread awareness</li>
            </ul>
            
            <p>To express interest in joining our team, please contact us through our Contact page.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Contact section
elif st.session_state.page == 'contact':
    st.markdown('<div class="section-header">Contact Us</div>', unsafe_allow_html=True)
    
    st.markdown("We'd love to hear from you! Reach out with questions, feedback, or suggestions.")
    
    # Contact form
    st.markdown('<div class="contact-form">', unsafe_allow_html=True)
    
    name = st.text_input("Name")
    email = st.text_input("Email")
    subject = st.text_input("Subject")
    message = st.text_area("Message")
    
    if st.button("Send Message"):
        if name and email and subject and message:
            st.success(f"Thank you for your message, {name}! We'll get back to you soon at {email}.")
            st.info("Note: This is a demo form. In a production environment, this would send an email to our team.")
        else:
            st.error("Please fill in all fields.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Direct contact
    st.markdown("### Direct Contact")
    
    st.markdown("""
    <div class="card">
        <div class="card-title">Email</div>
        <div class="card-content">
            <p>For general inquiries: <a href="mailto:oussama.sebrou@gmail.com">oussama.sebrou@gmail.com</a></p>
        </div>
    </div>
    
    <div class="card">
        <div class="card-title">Social Media</div>
        <div class="card-content">
            <p>Follow us on social media for updates and news:</p>
            <ul>
                <li>Twitter: <a href="https://twitter.com" target="_blank">@HereUsPalestine</a></li>
                <li>Instagram: <a href="https://instagram.com" target="_blank">@hereus_palestine</a></li>
                <li>Facebook: <a href="https://facebook.com" target="_blank">Here Us Palestine</a></li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>Here Us! From the River To the Sea © 2025 | Created with ❤️ for Palestine</p>
    <p>Contact: <a href="mailto:oussama.sebrou@gmail.com">oussama.sebrou@gmail.com</a></p>
</div>
""", unsafe_allow_html=True)
