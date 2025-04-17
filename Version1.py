import streamlit as st
import requests
import os
import base64
from PIL import Image
import io
google-generativeai

# Page configuration
st.set_page_config(
    page_title="Here Us! From the River To the Sea",
    page_icon="🇵🇸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to get Gemini API key
def get_api_key():
    # For text generation
    text_api_key = os.getenv("GEMINI_TEXT_API_KEY")
    # For image generation
    image_api_key = os.getenv("GEMINI_IMAGE_API_KEY")
    return text_api_key, image_api_key

# Function to generate text response with Gemini
def generate_text_response(prompt):
    text_api_key, _ = get_api_key()
    if not text_api_key:
        return "Error: Gemini API key for text generation not found. Please set the GEMINI_TEXT_API_KEY environment variable."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={text_api_key}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1500,
            "topP": 0.95,
            "topK": 40
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        response_json = response.json()
        
        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            return response_json["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "Error generating response. Please try again."
    except Exception as e:
        return f"Error: {str(e)}"

# Function to generate image with Gemini
def generate_image(prompt, style="realistic", theme="educational", size="medium"):
    _, image_api_key = get_api_key()
    if not image_api_key:
        return None, "Error: Gemini API key for image generation not found. Please set the GEMINI_IMAGE_API_KEY environment variable."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key={image_api_key}"
    
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
        "small": {"width": 512, "height": 512},
        "medium": {"width": 768, "height": 768},
        "large": {"width": 1024, "height": 1024}
    }
    
    size_config = dimensions.get(size, dimensions["medium"])
    
    payload = {
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "width": size_config["width"],
            "height": size_config["height"]
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        response_json = response.json()
        
        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            for part in response_json["candidates"][0]["content"]["parts"]:
                if "inlineData" in part:
                    return part["inlineData"]["data"], None
        
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
  
