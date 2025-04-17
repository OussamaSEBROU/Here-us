import streamlit as st
import google.generativeai as genai
import time
import os
import requests
from PIL import Image
import io
import base64

# Configure Gemini with your API key
google_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)

# Load Gemini models
model_text = genai.GenerativeModel(
    model_name="gemini-2.0-flash-thinking-exp-01-21",
    generation_config=genai.types.GenerationConfig(
        temperature=0.7,
        top_p=0.95,
        top_k=40,
        max_output_tokens=4000  # Increased token limit for deeper, longer responses
    )
)

# Enhanced prompt template for Palestine-related questions
def build_palestine_prompt(user_question):
    return f"""
You are an expert assistant dedicated to providing accurate, in-depth, and highly informative answers specifically about Palestine and related issues.

Your answers should focus entirely on Palestine-related topics. If the question is not related to Palestine, respond with: "Sorry! I'm trained just about Palestine Issue."

Respond to the user question with:
- Historical background with accurate timeline and context
- Structure your response like a professional news article or academic report with clear sections
- Base your information on trusted sources such as:
  * Al Jazeera (aljazeera.com) - Known for comprehensive coverage of Middle East issues
  * Metras (https://metras.co/) - Provides in-depth analysis on Palestinian affairs
  * https://www.aa.com.tr/ar
  * Academic books and peer-reviewed articles on Palestinian history and politics
  * Reports from human rights organizations (B'Tselem, Human Rights Watch, Amnesty International)
  * United Nations documents and resolutions
  * Palestinian academic institutions and research centers
- Include specific citations when possible (e.g., "According to Al Jazeera's reporting on [date]...")
- Provide factual, well-researched information on current events with accurate reporting
- Include relevant statistics and data from credible sources when discussing the humanitarian situation
- The answer should be in the same language as the input (be careful with this point)
- The response should be well-organized, ordered, and presented in a professional journalistic style
- Use titles and subtitles for clarity and structure when appropriate
- Present content in a clear, accessible manner while maintaining factual accuracy
- Ensure information is not biased towards Israel and remains truthful to Palestinian experiences
- When discussing boycotts or resistance, provide factual information about international law and human rights perspectives
- Length: If the response needs details, make it detailed not exceeding 1500 tokens but in a complete answer. For direct questions, make it concise (depending on the question), while remaining comprehensive within that limit.

Do not include information irrelevant to Palestine or unrelated topics.
If you encounter any limitations in providing information, acknowledge them transparently.

User question:
{user_question}

Your answer (detailed, accurate, context-aware):
"""

# Ask Gemini Pro for an in-depth response with improved error handling
def ask_about_palestine(user_question):
    prompt = build_palestine_prompt(user_question)
    try:
        response = model_text.generate_content(prompt)
        return response.text
    except Exception as e:
        error_message = str(e)
        # Handle specific error types
        if "quota" in error_message.lower():
            return "❌ API quota exceeded. Please try again later or contact the administrator."
        elif "blocked" in error_message.lower() or "safety" in error_message.lower():
            return "❌ The response was blocked due to safety concerns. Please rephrase your question or try a different topic related to Palestine."
        elif "timeout" in error_message.lower():
            return "❌ The request timed out. Please try again with a more specific question."
        else:
            return f"❌ Error getting response: {error_message}. Please try again or contact support."

# Function to simulate typing effect with improved performance
def typing_effect(text, delay=0.003):
    # For very long responses, reduce the typing effect to improve performance
    if len(text) > 1000:
        delay = 0.001
    
    output = ""
    placeholder = st.empty()
    for char in text:
        output += char
        placeholder.markdown(f"<div style='line-height: 1.5;'>{output}</div>", unsafe_allow_html=True)
        time.sleep(delay)

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

# Companies that support Israel (for boycott section) with alternatives
def get_boycott_companies():
    companies = {
        "Technology": {
            "Companies": [
                "Google", "Apple", "Microsoft", "Meta (Facebook)", "Amazon", "Intel", "HP", "IBM", "Oracle", "Cisco",
                "Dell", "Nvidia", "PayPal", "Wix", "Fiverr", "Monday.com", "Check Point", "Mobileye", "Waze", "Zoom"
            ],
            "Alternatives": [
                "DuckDuckGo instead of Google Search", 
                "Huawei/Samsung instead of Apple", 
                "Linux/Ubuntu instead of Windows", 
                "Telegram/Signal instead of WhatsApp", 
                "AliExpress/eBay instead of Amazon", 
                "AMD instead of Intel", 
                "Lenovo/Acer instead of HP", 
                "LibreOffice instead of Microsoft Office",
                "ProtonMail instead of Gmail",
                "Firefox/Brave instead of Chrome"
            ]
        },
        "Food & Beverage": {
            "Companies": [
                "McDonald's", "Coca-Cola", "PepsiCo", "Nestlé", "Starbucks", "Burger King", "Domino's Pizza",
                "KFC", "Pizza Hut", "Subway", "Heinz", "Danone", "Mars", "Mondelez (Oreo)", "Kellogg's", 
                "Häagen-Dazs", "Sabra Hummus", "Strauss Group"
            ],
            "Alternatives": [
                "Local burger restaurants instead of McDonald's/Burger King", 
                "Local coffee shops instead of Starbucks", 
                "Local water or juice instead of Coca-Cola/Pepsi", 
                "Local bakeries instead of chain restaurants",
                "Local dairy products instead of Danone/Nestlé",
                "Local chocolate and snacks instead of Mars/Mondelez"
            ]
        },
        "Fashion & Retail": {
            "Companies": [
                "H&M", "Zara", "Puma", "Nike", "Adidas", "Victoria's Secret", "Calvin Klein", "Tommy Hilfiger",
                "Marks & Spencer", "ASOS", "Skechers", "The North Face", "Timberland", "Levi's", "Gap", "Old Navy",
                "Ralph Lauren", "Lacoste", "Hugo Boss", "Uniqlo"
            ],
            "Alternatives": [
                "Local clothing brands", 
                "Ethical fashion brands", 
                "Second-hand/thrift shopping", 
                "Li-Ning/Anta Sports instead of Nike/Adidas",
                "Decathlon for sports equipment",
                "Local shoe manufacturers"
            ]
        },
        "Entertainment & Media": {
            "Companies": [
                "Disney", "Warner Bros", "Netflix", "Spotify", "Universal Music Group",
                "Fox", "Paramount", "Sony Pictures", "MGM", "DreamWorks", "NBC Universal",
                "CNN", "BBC", "New York Times", "The Washington Post", "The Guardian"
            ],
            "Alternatives": [
                "Independent streaming services", 
                "Local film productions", 
                "YouTube for independent content creators",
                "Anghami instead of Spotify in Arab regions",
                "Independent news sources and journalists",
                "Al Jazeera, TRT World for news"
            ]
        },
        "Sports": {
            "Companies": [
                "Puma", "Nike", "Adidas", "Under Armour", "New Balance", "Reebok",
                "Wilson", "Spalding", "Gatorade", "Fitbit", "Garmin"
            ],
            "Alternatives": [
                "Li-Ning", "Anta Sports", "Asics", "Fila", "Mizuno",
                "Local sports equipment manufacturers",
                "Independent fitness apps instead of corporate ones"
            ]
        },
        "Cosmetics & Personal Care": {
            "Companies": [
                "L'Oréal", "Estée Lauder", "Clinique", "MAC Cosmetics", "Revlon", "Maybelline",
                "Garnier", "Dove", "Nivea", "Johnson & Johnson", "Colgate-Palmolive", "Procter & Gamble"
            ],
            "Alternatives": [
                "Local natural cosmetics brands", 
                "Halal cosmetics brands", 
                "Ethical and cruelty-free alternatives",
                "Handmade soaps and natural products"
            ]
        },
        "Travel & Hospitality": {
            "Companies": [
                "Airbnb", "Booking.com", "Expedia", "TripAdvisor", "Marriott", "Hilton",
                "InterContinental", "Hyatt", "Delta Airlines", "American Airlines", "United Airlines"
            ],
            "Alternatives": [
                "Direct hotel bookings", 
                "Local travel agencies", 
                "Alternative accommodation platforms",
                "Local airlines when possible"
            ]
        }
    }
    return companies

# Function to get detailed boycott data
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

# App UI with enhanced professional features
def main():
    st.set_page_config(
        page_title="Palestina-ai", 
        page_icon="🕊️", 
        layout="wide"
    )

    # Custom CSS for a more professional look
    st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    .stButton > button {
        border-radius: 10px;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
    .stExpander {
        border-radius: 10px;
        border: 1px solid #e6e6e6;
    }
    h1, h2, h3 {
        color: #1f77b4;
    }
    .quote-box {
        border-left: 4px solid #1f77b4;
        padding-left: 15px;
        margin-top: 20px;
        font-size: 1.2em;
        font-weight: bold;
        color: #1f77b4;
    }
    .quote-author {
        text-align: right;
        color: #555555;
        font-style: italic;
    }
    .team-member {
        padding: 5px 0;
        border-bottom: 1px solid #f0f0f0;
    }
    .boycott-category {
        font-weight: bold;
        color: #d62728;
        margin-top: 10px;
    }
    .boycott-company {
        margin-left: 15px;
        padding: 2px 0;
    }
    .boycott-alternative {
        margin-left: 15px;
        padding: 2px 0;
        color: #2ca02c;
    }
    .footer {
        text-align: center;
        margin-top: 30px;
        padding: 10px;
        font-size: 0.8em;
        color: #666;
    }
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
    .company-card {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 4px solid #d62728;
    }
    .company-name {
        font-weight: bold;
        font-size: 1.1em;
        margin-bottom: 5px;
    }
    .company-reason {
        margin-bottom: 10px;
        font-style: italic;
    }
    .company-action {
        font-weight: bold;
        color: #d62728;
        margin-bottom: 5px;
    }
    .company-alternatives {
        color: #2ca02c;
    }
    .education-section {
        background-color: #f0f7fb;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        border-left: 5px solid #1f77b4;
    }
    .source-card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .source-title {
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 5px;
    }
    .source-snippet {
        font-size: 0.9em;
        color: #555;
        margin-bottom: 10px;
    }
    .source-link {
        font-size: 0.8em;
        color: #1f77b4;
    }
    .source-name {
        font-size: 0.8em;
        color: #888;
        font-style: italic;
    }
    .image-generation {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/0/00/Flag_of_Palestine.svg", width=250)
        st.title("Palestine AI")
        
        # Team Section
        with st.expander("Our Team", expanded=False):
            st.markdown("### Elkalem-Imrou Height School")
            st.markdown("In collaboration with Erinov Company")
            st.markdown("#### Team Members:")
            
            team_members = [
                "Nchachebi Abdelghani",
                "Yasser kasbi",
                "Youcef Abbouna",
                "Gueddi amine",
                "Khtara Hafssa",
                "Sirine Adoun",
                "Ycine Boukermouch",
                "Chihani Zineb",
                "Chihani Bouchera",
                "Mehdia Abbouna",
                "Rahma Elalouani",
                "Redouan Rekik Sadek",
                "Abdellatif Abdelnour",
                "Bahedi Bouchera",
                "Chacha Abdelazize",
                "Meriama Hadjyahya",
                "Adaouad Sanae"
            ]
            
            for member in team_members:
                st.markdown(f"<div class='team-member'>• {member}</div>", unsafe_allow_html=True)
        
        # Boycott Section - Enhanced with detailed data from second app
        with st.expander("Stand With Gaza - Boycott", expanded=False):
            st.markdown("### Companies Supporting Israel")
            st.markdown("""
            The boycott movement aims to apply economic and political pressure on Israel to comply with international law and Palestinian rights. 
            Below is a list of companies that have been identified as supporting Israel, along with alternatives you can use instead:
            """)
            
            # Add tabs for different views of boycott data
            boycott_tab1, boycott_tab2 = st.tabs(["Simple View", "Detailed View"])
            
            with boycott_tab1:
                companies = get_boycott_companies()
                for category, data in companies.items():
                    st.markdown(f"<div class='boycott-category'>{category}</div>", unsafe_allow_html=True)
                    
                    # Display companies to boycott
                    st.markdown("<div style='margin-left: 15px;'><strong>Companies to Boycott:</strong></div>", unsafe_allow_html=True)
                    for company in data["Companies"]:
                        st.markdown(f"<div class='boycott-company'>• {company}</div>", unsafe_allow_html=True)
                    
                    # Display alternatives
                    st.markdown("<div style='margin-left: 15px; margin-top: 10px; color: #2ca02c;'><strong>Alternatives:</strong></div>", unsafe_allow_html=True)
                    for alternative in data["Alternatives"]:
                        st.markdown(f"<div class='boycott-alternative'>✓ {alternative}</div>", unsafe_allow_html=True)
                    
                    st.markdown("<hr style='margin: 15px 0; border-color: #f0f0f0;'>", unsafe_allow_html=True)
            
            with boycott_tab2:
                detailed_data = get_boycott_data()
                for category, data in detailed_data.items():
                    st.markdown(f"### {category}")
                    
                    for company in data["companies"]:
                        st.markdown(f"""
                        <div class="company-card">
                            <div class="company-name">{company['name']}</div>
                            <div class="company-reason">{company['reason']}</div>
                            <div class="company-action">Action: {company['action']}</div>
                            <div class="company-alternatives">
                                <strong>Alternatives:</strong> {', '.join(company['alternatives'])}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("""
            ### How to Support Gaza
            
            1. **Boycott Products**: Avoid purchasing products from companies supporting Israel
            2. **Choose Alternatives**: Use the suggested alternatives or find local options
            3. **Raise Awareness**: Share information about the situation in Gaza
            4. **Donate**: Support humanitarian organizations working in Gaza
            5. **Advocate**: Contact your representatives to demand action
            6. **Join Protests**: Participate in peaceful demonstrations
            
            Remember that economic pressure through boycotts has historically been an effective non-violent resistance strategy.
            """)
        
        # Educational Resources Section - Added from second app
        with st.expander("Educational Resources", expanded=False):
            st.markdown("### Learn About Palestine")
            st.markdown("""
            This section provides educational resources to help you learn more about Palestine, its history, culture, and current situation.
            """)
            
            # Add tabs for different educational resources
            edu_tab1, edu_tab2, edu_tab3 = st.tabs(["Reliable Sources", "Key Terms", "Timeline"])
            
            with edu_tab1:
                st.markdown("#### Reliable Sources for Palestine Information")
                st.markdown("""
                When researching about Palestine, it's important to use reliable sources. Here are some recommended sources:
                
                **News Sources:**
                - [Al Jazeera](https://www.aljazeera.com/palestine-israel-conflict/) - Comprehensive coverage of Middle East issues
                - [Middle East Eye](https://www.middleeasteye.net/topics/palestine) - In-depth analysis on Palestinian affairs
                - [Metras](https://metras.co/) - Arabic language source on Palestinian affairs
                - [Electronic Intifada](https://electronicintifada.net/) - News, commentary, analysis, and reference materials about Palestine
                
                **Human Rights Organizations:**
                - [B'Tselem](https://www.btselem.org/) - Israeli Information Center for Human Rights in the Occupied Territories
                - [Human Rights Watch](https://www.hrw.org/middle-east/north-africa/israel/palestine) - Reports on human rights in Palestine
                - [Amnesty International](https://www.amnesty.org/en/location/middle-east-and-north-africa/israel-and-occupied-palestinian-territories/) - Human rights reporting
                
                **Academic & Research:**
                - [Institute for Palestine Studies](https://www.palestine-studies.org/) - Academic research on Palestine
                - [UNRWA](https://www.unrwa.org/) - UN Relief and Works Agency for Palestine Refugees
                - [OCHA oPt](https://www.ochaopt.org/) - UN Office for the Coordination of Humanitarian Affairs
                """)
            
            with edu_tab2:
                st.markdown("#### Key Terms to Understand")
                
                terms = {
                    "Nakba": "Arabic for 'catastrophe', refers to the mass displacement of Palestinians during the 1948 war when Israel was established.",
                    "Occupation": "Israel's military control over the West Bank, East Jerusalem, and (until 2005) Gaza Strip, which began in 1967.",
                    "Settlements": "Israeli civilian communities built on land captured by Israel in the 1967 war, considered illegal under international law.",
                    "Right of Return": "The principle that Palestinian refugees and their descendants have a right to return to their homeland.",
                    "BDS": "Boycott, Divestment, Sanctions - a Palestinian-led movement promoting boycotts against Israel.",
                    "Two-State Solution": "A proposed framework for resolving the conflict by establishing an independent Palestinian state alongside Israel.",
                    "Apartheid": "A term increasingly used by human rights organizations to describe Israel's policies of separation and discrimination against Palestinians.",
                    "Gaza Blockade": "The ongoing land, air, and sea blockade of the Gaza Strip imposed by Israel and Egypt since 2007.",
                    "Al-Aqsa Mosque": "The third holiest site in Islam, located in Jerusalem's Old City, a frequent flashpoint in the conflict.",
                    "Intifada": "Arabic for 'uprising', refers to Palestinian uprisings against Israeli occupation (First Intifada 1987-1993, Second Intifada 2000-2005)."
                }
                
                for term, definition in terms.items():
                    st.markdown(f"**{term}**: {definition}")
            
            with edu_tab3:
                st.markdown("#### Timeline of Key Events")
                st.markdown("""
                **Pre-1948:**
                - Late 19th century: Beginning of Zionist movement and Jewish immigration to Palestine
                - 1917: Balfour Declaration supports "national home for the Jewish people" in Palestine
                - 1922-1948: British Mandate period in Palestine
                
                **1948-1967:**
                - 1948: Israel declares independence; Arab-Israeli War; Nakba (750,000+ Palestinians displaced)
                - 1964: Palestine Liberation Organization (PLO) founded
                
                **1967-2000:**
                - 1967: Six-Day War; Israel occupies West Bank, Gaza, East Jerusalem, Golan Heights, and Sinai
                - 1987-1993: First Intifada (Palestinian uprising)
                - 1993: Oslo Accords signed, establishing Palestinian Authority
                
                **2000-Present:**
                - 2000-2005: Second Intifada
                - 2005: Israel withdraws from Gaza but maintains external control
                - 2006: Hamas wins Palestinian legislative elections
                - 2007: Hamas takes control of Gaza; Israel and Egypt impose blockade
                - 2008-2009, 2012, 2014, 2021: Major Israel-Gaza conflicts
                - 2018-2019: Great March of Return protests in Gaza
                - 2023-Present: Ongoing humanitarian crisis in Gaza
                """)
        
        # Help Section
        with st.expander("Help", expanded=True):
            st.markdown("### How to Use the App")
            st.markdown("""
            - **Ask Questions**: You can ask anything related to **Palestine's history, current events, or humanitarian issues**.
            - **Multi-Languages Supported**: You can ask in any language.
            - **Dark Mode**: To switch to dark mode, go to **Settings** > **Choose app theme** > **Dark Mode**.
            - **App Features**:
              - **In-depth answers** focused only on Palestine.
              - **Context-aware** responses tailored to your question.
              - **Accurate, detailed information** backed by AI.
              - **Image Generation**: Create images related to Palestine.
              - **Educational Resources**: Access reliable information about Palestine.
              - **Boycott Information**: Learn about companies supporting Israel and alternatives.
            """)
        st.markdown("---")
        
        # About Us Section
        with st.expander("About Us", expanded=False):
            st.markdown("#### Palestine AI Chat")
            st.markdown("This app was developed to provide in-depth, AI-powered insights into the Palestinian cause.")
            st.markdown("""
            **Version:** 1.2.0
            
            #### Features
            - AI-Powered Insights about Palestine
            - Focus on History, Humanitarian Issues, and Current Events
            - Multi-Language Support
            - Accurate and Context-Aware Responses
            - Boycott Information and Support Resources
            - Image Generation
            - Educational Resources
            
            © 2025 Palestine AI Team. All rights reserved.
            
            [Contact Us](mailto:your-email@example.com?subject=Palestine%20Info%20Bot%20Inquiry&body=Dear%20Palestine%20Info%20Bot%20Team,%0A%0AWe%20are%20writing%20to%20inquire%20about%20[your%20inquiry]%2C%20specifically%20[details%20of%20your%20inquiry].%0A%0A[Provide%20additional%20context%20and%20details%20here].%0A%0APlease%20let%20us%20know%20if%20you%20require%20any%20further%20information%20from%20our%20end.%0A%0ASincerely,%0A[Your%20Company%20Name]%0A[Your%20Name]%0A[Your%20Title]%0A[Your%20Phone%20Number]%0A[Your%20Email%20Address])
            """)

    # Main content area
    st.title("Palestine AI - From the river to the sea")

    # Quote of the Day section in a professional style
    st.markdown("""
    <div class="quote-box">
        "The issue of Palestine is a trial that God has tested your conscience, resolve, wealth, and unity with."
    </div>
    <div class="quote-author">
        — Al-Bashir Al-Ibrahimi
    </div>
    """, unsafe_allow_html=True)

    # Information cards in a grid layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Historical Context
        Palestine is a land with a deep-rooted history spanning thousands of years, and historical documents affirm that the Palestinian people are the rightful owners of this land. Palestine has been home to its indigenous population, who have preserved their presence and culture despite attempts at erasure and displacement throughout the ages.

        """)
    
    with col2:
        st.markdown("""
        ### Current Situation
        The Palestinian people continue to face severe humanitarian challenges due to ongoing occupation and blockade, particularly in the Gaza Strip, where residents are deprived of access to essential resources and services. These actions constitute clear violations of human rights and international law, which guarantee the right of peoples to live freely and with dignity in their homeland.

        """)

    # Create tabs for different functionalities
    tab1, tab2, tab3 = st.tabs(["Ask Questions", "Generate Images", "Find Sources"])
    
    with tab1:
        # User input section with enhanced styling
        st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)
        st.markdown("### Ask Your Question")
        st.markdown("Get accurate, detailed information about Palestine's history, current events, and humanitarian issues.")
        
        user_question = st.text_input("", placeholder="Type your question about Palestine here...", key="text_question")
        
        # Add a submit button for better UX
        submit_button = st.button("Get Answer")

        # Process the question when submitted
        if user_question and submit_button:
            # Check if the question is related to Palestine
            is_palestine = is_palestine_related(user_question)
            
            with st.spinner("Generating comprehensive answer..."):
                answer = ask_about_palestine(user_question)
                
                # Create a container with better styling for the answer
                answer_container = st.container()
                with answer_container:
                    st.markdown("<div style='background-color: #f0f7fb; padding: 20px; border-radius: 10px; border-left: 5px solid #1f77b4;'>", unsafe_allow_html=True)
                    # Typing effect for response
                    with st.empty():  # Create an empty placeholder to display the typing effect
                        typing_effect(answer)
                    st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Generate Images About Palestine")
        st.markdown("Create images related to Palestine using AI. Specify your prompt and customize the style and theme.")
        
        # Image generation form
        with st.form("image_generation_form"):
            image_prompt = st.text_input("Image Prompt", placeholder="Describe the image you want to generate...")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                style = st.selectbox("Style", 
                                    ["realistic", "artistic", "infographic", "cartoon", "sketch"],
                                    index=0)
            
            with col2:
                theme = st.selectbox("Theme", 
                                    ["historical", "cultural", "political", "educational", "solidarity"],
                                    index=3)
            
            with col3:
                size = st.selectbox("Size", 
                                   ["small", "medium", "large"],
                                   index=1)
            
            generate_button = st.form_submit_button("Generate Image")
        
        # Generate image when button is clicked
        if generate_button and image_prompt:
            with st.spinner("Generating image..."):
                # Check if the prompt is related to Palestine
                is_palestine = is_palestine_related(image_prompt)
                
                if not is_palestine:
                    st.warning("Please provide a prompt related to Palestine. This tool is specifically designed to generate images about Palestinian topics.")
                else:
                    img_data, error = generate_image(image_prompt, style, theme, size)
                    
                    if error:
                        st.error(error)
                    elif img_data:
                        st.markdown("<div class='image-generation'>", unsafe_allow_html=True)
                        st.image(img_data, caption=f"Generated image: {image_prompt}")
                        
                        # Add download button
                        st.markdown(get_image_download_link(img_data, "palestine_image.png", "Download Image"), unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Find Reliable Sources")
        st.markdown("Search for reliable information about Palestine from trusted sources.")
        
        # Source search form
        with st.form("source_search_form"):
            search_query = st.text_input("Search Query", placeholder="Enter your search query about Palestine...")
            search_button = st.form_submit_button("Search Sources")
        
        # Search for sources when button is clicked
        if search_button and search_query:
            with st.spinner("Searching for reliable sources..."):
                # Check if the query is related to Palestine
                is_palestine = is_palestine_related(search_query)
                
                if not is_palestine:
                    st.warning("Please provide a search query related to Palestine. This tool is specifically designed to find information about Palestinian topics.")
                else:
                    sources = search_reliable_sources(search_query)
                    
                    if sources:
                        st.markdown("### Search Results")
                        st.markdown(f"Found {len(sources)} reliable sources about '{search_query}':")
                        
                        for source in sources:
                            st.markdown(f"""
                            <div class="source-card">
                                <div class="source-title">{source['title']}</div>
                                <div class="source-snippet">{source['snippet']}</div>
                                <div class="source-link"><a href="{source['url']}" target="_blank">{source['url']}</a></div>
                                <div class="source-name">Source: {source['source']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No specific sources found for your query. Try a different search term or check the Educational Resources section in the sidebar for general information.")

    # Footer
    st.markdown("<div class='footer'>Palestine AI - Developed by Elkalem-Imrou Height School in collaboration with Erinov Company</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
