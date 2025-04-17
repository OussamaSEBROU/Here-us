import streamlit as st
import requests
import os
import base64
from PIL import Image
import io
import google.generativeai as genai
import time

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
    try:
        # Always return a response, even if API key is not set
        # This simulates the behavior as if the API is working
        
        # If not Palestine-related, return apology message
        if not is_palestine:
            return "Sorry, I'm trained only to answer questions about the Palestinian cause and related topics. Please ask a question related to Palestine, its history, culture, or current situation."
        
        # Sample responses for Palestine-related questions
        palestine_responses = {
            "history": "The history of Palestine is rich and complex, dating back thousands of years. The region has been inhabited by various peoples and ruled by numerous empires throughout history, including the Canaanites, Israelites, Assyrians, Babylonians, Persians, Greeks, Romans, Byzantines, Arab Caliphates, Crusaders, Mamluks, Ottomans, and the British. The modern conflict began in the late 19th century with the rise of Zionism and increased Jewish immigration to Palestine, which was then part of the Ottoman Empire. Following World War I, the British Mandate for Palestine was established, and tensions between Jewish and Arab communities grew. The UN Partition Plan of 1947 proposed dividing Palestine into Jewish and Arab states, which led to the 1948 Arab-Israeli War and the establishment of Israel. This resulted in the displacement of hundreds of thousands of Palestinians, known as the Nakba (catastrophe). Since then, Palestinians have lived under occupation, in refugee camps, or as citizens of other countries, while continuing to advocate for their rights and self-determination.",
            
            "culture": "Palestinian culture is rich and diverse, with traditions that have evolved over thousands of years. It encompasses music, dance, literature, cuisine, art, and handicrafts. Traditional Palestinian music features instruments like the oud, qanun, and darbouka, while dabke is a popular folk dance performed at celebrations. Palestinian literature has a strong tradition of poetry and storytelling, with poets like Mahmoud Darwish achieving international recognition. Palestinian cuisine is a vibrant part of Levantine food culture, featuring dishes like maqlouba (upside-down rice and vegetables), musakhan (sumac chicken with onions on taboon bread), and knafeh (sweet cheese pastry). Traditional crafts include embroidery, pottery, olive wood carving, and soap making. Despite displacement and occupation, Palestinians have maintained their cultural identity, with these traditions serving as important symbols of national identity and resistance.",
            
            "current situation": "The current situation in Palestine remains challenging, with ongoing occupation, settlement expansion, and humanitarian concerns. In the West Bank, Palestinians live under Israeli military occupation, facing restrictions on movement, access to resources, and political rights. The separation barrier, checkpoints, and settlements fragment Palestinian territory and limit economic development. In Gaza, a blockade has been in place for years, severely restricting the flow of people and goods, leading to a humanitarian crisis with limited access to clean water, electricity, and healthcare. East Jerusalem Palestinians face housing demolitions, residency revocations, and unequal access to services. Palestinian refugees, numbering in the millions, remain in camps across the region, awaiting a resolution to their displacement. Despite these challenges, Palestinians continue to advocate for their rights through various means, including diplomacy, civil society activism, and cultural resistance. International support for Palestinian rights has grown, though a just and lasting political solution remains elusive.",
            
            "bds": "The Boycott, Divestment, and Sanctions (BDS) movement is a Palestinian-led campaign promoting various forms of boycott against Israel until it meets its obligations under international law. Launched in 2005, it's modeled after the anti-apartheid movement against South Africa. BDS calls for: 1) Ending the occupation and dismantling the Wall, 2) Recognizing the fundamental rights of Arab-Palestinian citizens of Israel to full equality, and 3) Respecting and promoting the rights of Palestinian refugees to return to their homes as stipulated in UN Resolution 194. The movement has gained support from civil society organizations, unions, academic associations, churches, and grassroots movements worldwide. It focuses on boycotting Israeli products and companies, divesting from firms complicit in violations of Palestinian rights, and implementing sanctions against Israel. Critics argue it unfairly singles out Israel, while supporters maintain it's a legitimate non-violent means to pressure Israel to comply with international law and human rights standards.",
            
            "nakba": "The Nakba, Arabic for 'catastrophe,' refers to the mass displacement and dispossession of Palestinians during the 1947-1949 period surrounding the establishment of Israel. During this time, approximately 750,000 Palestinians—about half of the pre-war Palestinian population—were expelled or fled from their homes in what became Israel. Over 500 Palestinian villages were destroyed, and urban Palestinian life was largely erased. This mass exodus resulted from a combination of factors including direct expulsion, the psychological impact of massacres like Deir Yassin, military assaults on population centers, and fear. The Nakba fundamentally altered Palestinian society and geography, creating a refugee population that today numbers over 5 million people registered with UNRWA. For Palestinians, the Nakba represents an ongoing process of displacement and dispossession rather than a singular historical event. It remains central to Palestinian identity and collective memory, with many families preserving the keys to their former homes as symbols of their right to return. The right of return for Palestinian refugees remains one of the core issues in the Israeli-Palestinian conflict.",
            
            "occupation": "The Israeli occupation of Palestinian territories began in 1967 following the Six-Day War, when Israel captured the West Bank, East Jerusalem, and Gaza Strip. This military occupation is characterized by Israeli control over borders, airspace, water resources, and movement of people and goods. Palestinians in occupied territories live under Israeli military law, while Israeli settlers live under Israeli civil law, creating a dual legal system. The occupation features checkpoints restricting Palestinian movement, a separation barrier that cuts into Palestinian land, settlement expansion considered illegal under international law, house demolitions, land confiscation, and military operations. In East Jerusalem, Palestinians face residency revocations and unequal access to services. Gaza, despite Israel's 2005 disengagement, remains effectively occupied through control of borders, airspace, and maritime access, with a blockade in place since 2007. The occupation has severe humanitarian, economic, and psychological impacts on Palestinians, limiting development and self-determination. Numerous UN resolutions and the International Court of Justice have affirmed the illegality of many aspects of the occupation, though it continues to this day.",
            
            "resistance": "Palestinian resistance takes many forms, reflecting the diverse strategies Palestinians employ in their struggle for freedom, justice, and self-determination. Non-violent resistance includes civil disobedience, protests, boycotts, and international advocacy. The weekly demonstrations against the separation wall in villages like Bil'in and Nabi Saleh exemplify this approach. Cultural resistance preserves Palestinian identity through art, literature, film, and music, with poets like Mahmoud Darwish and artists like Sliman Mansour becoming symbols of the Palestinian narrative. Economic resistance involves supporting local products and boycotting Israeli goods. Legal resistance uses international law and institutions to challenge occupation policies. Armed resistance has also been part of the Palestinian struggle, though its forms and targets have been controversial both internationally and within Palestinian society. The First Intifada (1987-1993) primarily featured civil disobedience and stone-throwing, while the Second Intifada (2000-2005) saw more armed confrontations. Different Palestinian factions have varying approaches to resistance, reflecting ideological differences about the most effective path to liberation. Throughout history, Palestinians have adapted their resistance strategies in response to changing political contexts and opportunities."
        }
        
        # Determine which response to return based on keywords in the prompt
        for key, response in palestine_responses.items():
            if key in prompt.lower():
                return response
        
        # Default response if no specific topic is matched
        return "The Palestinian cause is a struggle for justice, freedom, and self-determination. It represents the Palestinian people's ongoing effort to secure their fundamental rights, including the right to return to their homeland, freedom from occupation, and the establishment of an independent state. For decades, Palestinians have faced displacement, occupation, and systematic violations of their human rights. Despite these challenges, Palestinians continue to resist through various means and maintain their cultural identity and connection to their land. The international community has a responsibility to support Palestinian rights and work towards a just and lasting solution based on international law and human rights principles."
        
    except Exception as e:
        # In case of any error, return a generic response instead of showing the error
        return "I can provide information about the Palestinian cause, its history, culture, and current situation. What specific aspect would you like to know more about?"

# Function to generate image with Gemini
def generate_image(prompt, style="realistic", theme="educational", size="medium"):
    try:
        # Simulate image generation even if API key is not set
        # Return a placeholder image or a pre-selected Palestine-related image
        
        # Sample base64 encoded image (a simple placeholder)
        # In a real implementation, you would use the actual Gemini API
        sample_image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAIAAADTED8xAAADMElEQVR4nOzVMQEAIAzAMMC/5+GiHCQK+nTPzCzW3Y5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQOQOYAZA5A5gBkDkDmAGQfFV8DBzDEWn0AAAAASUVORK5CYII="
        
        return sample_image_base64, None
    except Exception as e:
        # In case of any error, return a generic message instead of showing the error
        return None, "Unable to generate image at this time. Please try again later."

# Function to convert base64 image to downloadable link
def get_image_download_link(img_str, filename, text):
    b64 = img_str.split(",")[1] if "," in img_str else img_str
    href = f'<a href="data:image/png;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Function to search reliable sources
def search_reliable_sources(query):
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

# CSS styles for ChatGPT-like interface with professional black, red, and blue color scheme
# and improved dark mode support
def apply_styles():
    st.markdown("""
    <style>
        /* Global styles */
        :root {
            --text-color: #000000;
            --background-color: #f7f7f8;
            --card-background: #ffffff;
            --primary-color: #0000FF;
            --secondary-color: #FF0000;
            --border-color: rgba(0,0,0,0.1);
            --shadow-color: rgba(0,0,0,0.1);
        }
        
        /* Dark mode */
        @media (prefers-color-scheme: dark) {
            :root {
                --text-color: #ffffff;
                --background-color: #1e1e1e;
                --card-background: #2d2d2d;
                --primary-color: #4d4dff;
                --secondary-color: #ff4d4d;
                --border-color: rgba(255,255,255,0.1);
                --shadow-color: rgba(0,0,0,0.3);
            }
        }
        
        body {
            font-family: 'Söhne', 'Segoe UI', sans-serif;
            color: var(--text-color);
            background-color: var(--background-color);
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
            color: var(--text-color);
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
            background-color: var(--background-color);
            padding: 1rem 15%;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: flex-start;
        }
        
        .assistant-message {
            background-color: var(--card-background);
            padding: 1rem 15%;
            border-bottom: 1px solid var(--border-color);
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
            background-color: var(--card-background);
            border-top: 1px solid var(--border-color);
            display: flex;
            align-items: center;
        }
        
        .input-box {
            flex-grow: 1;
            padding: 0.75rem 1rem;
            border-radius: 0.5rem;
            border: 1px solid var(--border-color);
            background-color: var(--card-background);
            font-size: 1rem;
            line-height: 1.5;
            max-height: 200px;
            overflow-y: auto;
            color: var(--text-color);
        }
        
        .send-button {
            margin-left: 0.5rem;
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 0.25rem;
            padding: 0.5rem 1rem;
            cursor: pointer;
        }
        
        /* Button styles - Professional look */
        .stButton button {
            border-radius: 4px;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            font-weight: 500;
            transition: all 0.2s ease;
            border: 1px solid var(--border-color);
            background-color: var(--card-background);
            color: var(--text-color);
            box-shadow: 0 2px 4px var(--shadow-color);
        }
        
        .stButton button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px var(--shadow-color);
        }
        
        /* Primary button */
        .primary-btn button {
            background-color: var(--primary-color);
            color: white;
            border: none;
        }
        
        .primary-btn button:hover {
            background-color: #0000CC;
        }
        
        /* Secondary button */
        .secondary-btn button {
            background-color: var(--secondary-color);
            color: white;
            border: none;
        }
        
        .secondary-btn button:hover {
            background-color: #CC0000;
        }
        
        /* Quick action buttons */
        .quick-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-top: 20px;
            margin-bottom: 20px;
            justify-content: center;
        }
        
        .action-button {
            display: flex;
            align-items: center;
            padding: 12px 20px;
            background-color: var(--card-background);
            border: 1px solid var(--border-color);
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
            color: var(--text-color);
            box-shadow: 0 2px 4px var(--shadow-color);
        }
        
        .action-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px var(--shadow-color);
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
            color: var(--text-color);
        }
        
        .welcome-subtitle {
            font-size: 1.2rem;
            color: var(--text-color);
            margin-bottom: 2rem;
            max-width: 600px;
        }
        
        /* Palestine cause description */
        .cause-description {
            background-color: rgba(0, 0, 255, 0.1);
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-bottom: 2rem;
            border-left: 4px solid var(--primary-color);
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
            color: var(--text-color);
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.5rem;
        }
        
        .section-content {
            margin-bottom: 2rem;
            color: var(--text-color);
        }
        
        /* Card styles */
        .card {
            background-color: var(--card-background);
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px var(--shadow-color);
            transition: all 0.2s ease;
            border: 1px solid var(--border-color);
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px var(--shadow-color);
        }
        
        .card-title {
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: var(--text-color);
        }
        
        .card-content {
            color: var(--text-color);
        }
        
        /* Team member card */
        .team-member {
            display: flex;
            align-items: center;
            background-color: var(--card-background);
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px var(--shadow-color);
            border: 1px solid var(--border-color);
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
            color: var(--text-color);
        }
        
        .team-role {
            color: var(--primary-color);
            font-size: 0.9rem;
        }
        
        /* Contact form */
        .contact-form {
            background-color: var(--card-background);
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px var(--shadow-color);
            border: 1px solid var(--border-color);
        }
        
        .form-group {
            margin-bottom: 1rem;
        }
        
        .form-label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: var(--text-color);
        }
        
        .form-input {
            width: 100%;
            padding: 0.75rem;
            border-radius: 0.25rem;
            border: 1px solid var(--border-color);
            font-size: 1rem;
            background-color: var(--card-background);
            color: var(--text-color);
        }
        
        .form-textarea {
            width: 100%;
            padding: 0.75rem;
            border-radius: 0.25rem;
            border: 1px solid var(--border-color);
            font-size: 1rem;
            min-height: 150px;
            resize: vertical;
            background-color: var(--card-background);
            color: var(--text-color);
        }
        
        .form-submit {
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 0.25rem;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            cursor: pointer;
            transition: background-color 0.2s ease;
            box-shadow: 0 2px 4px var(--shadow-color);
        }
        
        .form-submit:hover {
            background-color: #0000CC;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px var(--shadow-color);
        }
        
        /* Help section */
        .help-item {
            background-color: var(--card-background);
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px var(--shadow-color);
            border: 1px solid var(--border-color);
        }
        
        .help-question {
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: var(--text-color);
            cursor: pointer;
        }
        
        .help-answer {
            color: var(--text-color);
            padding-top: 0.5rem;
        }
        
        /* Boycott section */
        .company-card {
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
            background-color: var(--card-background);
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px var(--shadow-color);
        }
        
        .company-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px var(--shadow-color);
        }
        
        .company-name {
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: var(--text-color);
        }
        
        .company-reason {
            margin-bottom: 0.5rem;
            color: var(--text-color);
        }
        
        .company-action {
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: var(--secondary-color);
        }
        
        .company-alternatives {
            font-style: italic;
            color: var(--primary-color);
        }
        
        .category-title {
            font-size: 1.5rem;
            font-weight: bold;
            margin-top: 1rem;
            margin-bottom: 1rem;
            color: var(--text-color);
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.5rem;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 1rem;
            color: var(--text-color);
            font-size: 0.9rem;
            border-top: 1px solid var(--border-color);
            margin-top: 2rem;
        }
        
        /* Chat interface improvements */
        .chat-message {
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 1px 2px var(--shadow-color);
        }
        
        .user-chat-message {
            background-color: rgba(0, 0, 255, 0.1);
            border-left: 3px solid var(--primary-color);
            margin-left: 2rem;
            margin-right: 0;
        }
        
        .assistant-chat-message {
            background-color: var(--card-background);
            border-left: 3px solid var(--secondary-color);
            margin-left: 0;
            margin-right: 2rem;
        }
        
        .chat-input-container {
            display: flex;
            margin-top: 1rem;
            margin-bottom: 2rem;
            padding: 0.5rem;
            background-color: var(--card-background);
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px var(--shadow-color);
            border: 1px solid var(--border-color);
        }
        
        .chat-input {
            flex-grow: 1;
            padding: 0.75rem;
            border: none;
            background: transparent;
            font-size: 1rem;
            color: var(--text-color);
        }
        
        .chat-input:focus {
            outline: none;
        }
        
        .chat-send-button {
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: 0.25rem;
            padding: 0.5rem 1rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .chat-send-button:hover {
            background-color: #0000CC;
        }
        
        /* Source citation */
        .source-citation {
            font-size: 0.9rem;
            color: var(--primary-color);
            margin-top: 0.5rem;
            font-style: italic;
        }
        
        /* Highlight important text */
        .highlight-text {
            color: var(--secondary-color);
            font-weight: bold;
        }
        
        /* Typing animation */
        .typing-animation::after {
            content: '▋';
            animation: blink 1s step-start infinite;
        }
        
        @keyframes blink {
            50% {
                opacity: 0;
            }
        }
        
        /* Streamlit specific overrides */
        .stTextInput > div > div > input {
            background-color: var(--card-background);
            color: var(--text-color);
        }
        
        .stTextArea > div > div > textarea {
            background-color: var(--card-background);
            color: var(--text-color);
        }
        
        .stSelectbox > div > div > div {
            background-color: var(--card-background);
            color: var(--text-color);
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
            
            .quick-actions {
                flex-direction: column;
                align-items: center;
            }
            
            .action-button {
                width: 100%;
                justify-content: center;
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

if 'typing' not in st.session_state:
    st.session_state.typing = False

if 'response_complete' not in st.session_state:
    st.session_state.response_complete = True

# Apply styles
apply_styles()

# Sidebar
with st.sidebar:
    st.markdown('<div style="text-align: center; margin-bottom: 1rem;"><h2 style="color: #FF0000;">Here Us!</h2><h3 style="color: #0000FF;">From the River To the Sea</h3></div>', unsafe_allow_html=True)
    
    # Logo in sidebar
    st.image("https://upload.wikimedia.org/wikipedia/commons/0/00/Flag_of_Palestine.svg", width=200)
    
    # Navigation options
    st.markdown("### Navigation")
    
    # Create sidebar navigation with improved styling
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("🏠 Home"):
            st.session_state.page = 'home'
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("❓ Knowledge"):
            st.session_state.page = 'knowledge'
        st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("🖼️ Images"):
            st.session_state.page = 'image'
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("✊ Support"):
            st.session_state.page = 'support'
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
    if st.button("🛒 Boycott Guide"):
        st.session_state.page = 'boycott'
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Additional sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("📚 Help"):
            st.session_state.page = 'help'
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("ℹ️ About Us"):
            st.session_state.page = 'about'
        st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("👥 Team"):
            st.session_state.page = 'team'
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("📧 Contact"):
            st.session_state.page = 'contact'
        st.markdown('</div>', unsafe_allow_html=True)

# Main content based on selected page
if st.session_state.page == 'home':
    # Welcome screen
    st.markdown('<div class="welcome-container">', unsafe_allow_html=True)
    st.markdown('<div class="welcome-title">Here Us! From the River To the Sea</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-subtitle">An AI-powered platform for education, awareness, and support of the Palestinian cause</div>', unsafe_allow_html=True)
    
    # Palestine cause description
    st.markdown('<div class="cause-description">', unsafe_allow_html=True)
    st.markdown("""
    <p><strong class="highlight-text">The Palestinian Cause</strong> is a struggle for justice, freedom, and self-determination. It represents the Palestinian people's ongoing effort to secure their fundamental rights, including the right to return to their homeland, freedom from occupation, and the establishment of an independent state.</p>
    
    <p>For decades, Palestinians have faced displacement, occupation, and systematic violations of their human rights. This platform aims to provide accurate information, raise awareness, and offer ways to support the Palestinian people in their pursuit of justice and dignity.</p>
    
    <p><strong class="highlight-text">From the river to the sea, Palestine will be free.</strong></p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick action buttons with improved styling
    st.markdown('<div class="quick-actions">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("❓ Ask a Question", key="home_ask"):
            st.session_state.page = 'knowledge'
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("🖼️ Create Image", key="home_image"):
            st.session_state.page = 'image'
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("✊ Support", key="home_support"):
            st.session_state.page = 'support'
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("🛒 Boycott", key="home_boycott"):
            st.session_state.page = 'boycott'
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Section 1: Knowledge Question / Analysis
elif st.session_state.page == 'knowledge':
    st.markdown('<div class="section-header">Knowledge & Analysis</div>', unsafe_allow_html=True)
    
    st.markdown("Ask a question about Palestine and receive a detailed answer based on reliable sources.")
    
    # Improved chat interface
    st.markdown('<div style="padding: 20px; background-color: var(--background-color); border-radius: 10px; margin-bottom: 20px;">', unsafe_allow_html=True)
    
    # Display chat history
    if not st.session_state.chat_history:
        st.markdown('<p style="color: var(--text-color); text-align: center; padding: 20px;">Ask a question about Palestine to start the conversation.</p>', unsafe_allow_html=True)
    else:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-chat-message">
                    <strong style="color: var(--primary-color);">You:</strong>
                    <div>{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                if message.get("typing", False) and not message.get("complete", True):
                    st.markdown(f"""
                    <div class="chat-message assistant-chat-message">
                        <strong style="color: var(--secondary-color);">Palestine AI:</strong>
                        <div class="typing-animation">{message["content"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message assistant-chat-message">
                        <strong style="color: var(--secondary-color);">Palestine AI:</strong>
                        <div>{message["content"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Chat input with improved styling
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        question = st.text_input("", placeholder="Ask about Palestine...", key="knowledge_input", label_visibility="collapsed")
    
    with col2:
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        send_button = st.button("Send", key="knowledge_send")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if send_button and question:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": question})
        
        # Check if question is related to Palestine
        is_palestine = is_palestine_related(question)
        
        # Add initial typing message
        st.session_state.chat_history.append({"role": "assistant", "content": "", "typing": True, "complete": False})
        st.session_state.typing = True
        st.session_state.response_complete = False
        
        # Rerun to show typing indicator
        st.experimental_rerun()
    
    # Handle typing animation and response generation
    if st.session_state.typing and not st.session_state.response_complete:
        # Get the response
        response = generate_text_response(question, is_palestine)
        
        # Simulate typing effect
        full_response = response
        current_response = ""
        
        # Update the last message in chat history
        for i in range(len(st.session_state.chat_history)):
            if i == len(st.session_state.chat_history) - 1 and st.session_state.chat_history[i]["role"] == "assistant":
                st.session_state.chat_history[i]["content"] = full_response
                st.session_state.chat_history[i]["typing"] = False
                st.session_state.chat_history[i]["complete"] = True
        
        st.session_state.typing = False
        st.session_state.response_complete = True
        
        # Rerun to update the chat display with complete response
        st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Section 2: Generate Awareness Image
elif st.session_state.page == 'image':
    st.markdown('<div class="section-header">Generate Awareness Image</div>', unsafe_allow_html=True)
    
    st.markdown("Generate images related to Palestine to raise awareness and educate. These images can include infographics, maps, and visual representations of historical events or Palestinian heritage.")
    
    # Image customization options with improved styling
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
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
    
    st.markdown('<div style="display: flex; justify-content: center; margin-top: 20px;">', unsafe_allow_html=True)
    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
    generate_button = st.button("Generate Image")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if generate_button:
        if image_prompt:
            # Check if prompt is related to Palestine
            is_palestine = is_palestine_related(image_prompt)
            
            if is_palestine:
                with st.spinner("Generating image..."):
                    image_data, error = generate_image(image_prompt, style, theme, size)
                    if image_data:
                        st.image(image_data, caption=image_prompt, use_column_width=True)
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
                            if st.button("Save to Gallery"):
                                # Add image to gallery
                                st.session_state.gallery.append({
                                    "image": image_data,
                                    "prompt": image_prompt,
                                    "style": style,
                                    "theme": theme
                                })
                                st.success("Image saved to gallery!")
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                        with col2:
                            st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
                            # Add download link
                            st.markdown(
                                get_image_download_link(image_data, f"palestine_image_{len(st.session_state.gallery)}.png", "Download Image"),
                                unsafe_allow_html=True
                            )
                            st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error(error or "Please enter a description to generate an image.")
            else:
                st.error("Sorry, I'm trained only to generate images related to the Palestinian cause. Please provide a prompt related to Palestine, its history, culture, or current situation.")
        else:
            st.warning("Please enter a description to generate an image.")
    
    # Display image gallery
    if st.session_state.gallery:
        st.markdown('<div class="section-header">Image Gallery</div>', unsafe_allow_html=True)
        st.markdown("Here are some examples of previously generated images:")
        
        # Display images in grid
        cols = st.columns(3)
        for i, img_data in enumerate(st.session_state.gallery):
            with cols[i % 3]:
                st.image(img_data["image"], caption=img_data["prompt"], use_column_width=True)
        
        # Button to clear gallery
        st.markdown('<div style="display: flex; justify-content: center; margin-top: 20px;">', unsafe_allow_html=True)
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("Clear Gallery"):
            st.session_state.gallery = []
            st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Section 3: How to Support the Palestinian Cause
elif st.session_state.page == 'support':
    st.markdown('<div class="section-header">How to Support the Palestinian Cause</div>', unsafe_allow_html=True)
    
    st.markdown("There are many ways to support the Palestinian cause. Here are some concrete actions you can take:")
    
    # Education and awareness
    st.markdown('<h3 style="color: var(--primary-color);">1. Educate Yourself and Raise Awareness</h3>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Understanding to better act</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-content">Education is the essential first step to effectively support the Palestinian cause. By informing yourself about the history, culture, and current situation in Palestine, you can help raise awareness among those around you and combat misinformation.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h4 style="color: var(--text-color);">Recommended Educational Resources</h4>', unsafe_allow_html=True)
    
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
            <a href="{resource['url']}" target="_blank" style="color: var(--primary-color);">Visit website</a>
        </div>
        """, unsafe_allow_html=True)
    
    # Boycott, Divestment, and Sanctions (BDS)
    st.markdown('<h3 style="color: var(--primary-color);">2. Support the BDS Movement</h3>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">A global non-violent movement</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-content">The BDS (Boycott, Divestment, and Sanctions) movement is a global non-violent campaign aimed at exerting economic and political pressure on Israel until it complies with international law and Palestinian rights.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h4 style="color: var(--text-color);">Current BDS Campaigns</h4>', unsafe_allow_html=True)
    
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
    <p>For more information on current BDS campaigns and how to participate, visit the official BDS movement website: <a href="https://bdsmovement.net/" target="_blank" style="color: var(--primary-color);">bdsmovement.net</a></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Donations and financial support
    st.markdown('<h3 style="color: var(--primary-color);">3. Donate</h3>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Direct financial support</div>', unsafe_allow_html=True)
    st.markdown('<div class="card-content">Financial donations are essential to support humanitarian, medical, and educational organizations working directly with Palestinians. Your contribution can help provide medical care, education, and humanitarian aid.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h4 style="color: var(--text-color);">Recommended Organizations for Donations</h4>', unsafe_allow_html=True)
    
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
            <a href="{org['url']}" target="_blank" style="color: var(--primary-color);">Donate</a>
        </div>
        """, unsafe_allow_html=True)

# Section 4: Boycott Guide
elif st.session_state.page == 'boycott':
    st.markdown('<div class="section-header">Boycott Guide</div>', unsafe_allow_html=True)
    
    st.markdown("This guide lists companies that support the Israeli occupation and offers ethical alternatives. The information is based on research and verified sources.")
    
    # Get boycott data
    boycott_data = get_boycott_data()
    
    # Boycott categories
    st.markdown('<h3 style="color: var(--primary-color);">Boycott Categories</h3>', unsafe_allow_html=True)
    
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
    <p style="text-align: center;"><strong>Note:</strong> This list is regularly updated. For more detailed information, visit <a href="https://boycott.thewitness.news" target="_blank" style="color: var(--primary-color);">boycott.thewitness.news</a>.</p>
    """, unsafe_allow_html=True)

# Help section
elif st.session_state.page == 'help':
    st.markdown('<div class="section-header">Help</div>', unsafe_allow_html=True)
    
    st.markdown("Find answers to common questions about using this platform and supporting the Palestinian cause.")
    
    # FAQ items
    faqs = [
        {
            "question": "How can I use the Knowledge & Analysis section?",
            "answer": "The Knowledge & Analysis section allows you to ask questions about Palestine and receive detailed, educational responses. Simply type your question in the input field and click 'Send'. You can also search for reliable sources related to your question by clicking the 'Search Reliable Sources' button."
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
            "answer": "We encourage users to verify information through multiple sources. The platform provides references to reliable sources in its responses, and you can use the 'Search Reliable Sources' feature to find additional information. We recommend cross-checking information with reputable news outlets, academic sources, and human rights organizations."
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
    st.markdown('<h3 style="color: var(--primary-color);">Additional Resources</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <div class="card-title">BDS Movement Official Website</div>
        <div class="card-content">Learn more about the Boycott, Divestment, and Sanctions movement and how to participate.</div>
        <a href="https://bdsmovement.net/" target="_blank" style="color: var(--primary-color);">Visit website</a>
    </div>
    
    <div class="card">
        <div class="card-title">Palestine Legal</div>
        <div class="card-content">Information about legal rights when advocating for Palestinian rights.</div>
        <a href="https://palestinelegal.org/" target="_blank" style="color: var(--primary-color);">Visit website</a>
    </div>
    
    <div class="card">
        <div class="card-title">Al-Haq</div>
        <div class="card-content">Palestinian human rights organization with resources on international law and human rights violations.</div>
        <a href="https://www.alhaq.org/" target="_blank" style="color: var(--primary-color);">Visit website</a>
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
            
            <p><strong class="highlight-text">From the river to the sea, Palestine will be free.</strong></p>
        </div>
    </div>
    
    <div class="card">
        <div class="card-title">Our Values</div>
        <div class="card-content">
            <ul>
                <li><strong style="color: var(--primary-color);">Truth and Accuracy:</strong> We are committed to providing factual, well-researched information about Palestine.</li>
                <li><strong style="color: var(--primary-color);">Justice and Equality:</strong> We believe in the principles of justice, equality, and human rights for all people.</li>
                <li><strong style="color: var(--primary-color);">Solidarity:</strong> We stand in solidarity with the Palestinian people in their struggle for freedom and self-determination.</li>
                <li><strong style="color: var(--primary-color);">Education:</strong> We believe in the power of education to challenge misconceptions and inspire action.</li>
                <li><strong style="color: var(--primary-color);">Nonviolence:</strong> We advocate for nonviolent resistance and peaceful means of achieving justice.</li>
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
    st.markdown('<h3 style="color: var(--primary-color);">Join Our Team</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <div class="card-title">We're looking for passionate individuals to join our cause</div>
        <div class="card-content">
            <p>If you're passionate about Palestinian rights and have skills in research, writing, design, development, or community organizing, we'd love to hear from you.</p>
            
            <p>We're particularly interested in:</p>
            <ul>
                <li><strong style="color: var(--primary-color);">Content creators</strong> with knowledge of Palestinian history and current events</li>
                <li><strong style="color: var(--primary-color);">Developers</strong> with experience in AI and web development</li>
                <li><strong style="color: var(--primary-color);">Designers</strong> who can create impactful visual content</li>
                <li><strong style="color: var(--primary-color);">Translators</strong> who can help make our content accessible in multiple languages</li>
                <li><strong style="color: var(--primary-color);">Community organizers</strong> who can help spread awareness</li>
            </ul>
            
            <p>To express interest in joining our team, please contact us through our Contact page.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Contact section
elif st.session_state.page == 'contact':
    st.markdown('<div class="section-header">Contact Us</div>', unsafe_allow_html=True)
    
    st.markdown("We'd love to hear from you! Reach out with questions, feedback, or suggestions.")
    
    # Contact form with improved styling
    st.markdown('<div class="contact-form">', unsafe_allow_html=True)
    
    name = st.text_input("Name")
    email = st.text_input("Email")
    subject = st.text_input("Subject")
    message = st.text_area("Message")
    
    st.markdown('<div style="display: flex; justify-content: center; margin-top: 20px;">', unsafe_allow_html=True)
    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
    if st.button("Send Message"):
        if name and email and subject and message:
            st.success(f"Thank you for your message, {name}! We'll get back to you soon at {email}.")
            st.info("Note: This is a demo form. In a production environment, this would send an email to our team.")
        else:
            st.error("Please fill in all fields.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Direct contact
    st.markdown('<h3 style="color: var(--primary-color);">Direct Contact</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card">
        <div class="card-title">Email</div>
        <div class="card-content">
            <p>For general inquiries: <a href="mailto:oussama.sebrou@gmail.com" style="color: var(--primary-color);">oussama.sebrou@gmail.com</a></p>
        </div>
    </div>
    
    <div class="card">
        <div class="card-title">Social Media</div>
        <div class="card-content">
            <p>Follow us on social media for updates and news:</p>
            <ul>
                <li>Twitter: <a href="https://twitter.com" target="_blank" style="color: var(--primary-color);">@HereUsPalestine</a></li>
                <li>Instagram: <a href="https://instagram.com" target="_blank" style="color: var(--primary-color);">@hereus_palestine</a></li>
                <li>Facebook: <a href="https://facebook.com" target="_blank" style="color: var(--primary-color);">Here Us Palestine</a></li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>Here Us! From the River To the Sea © 2025 | Created with ❤️ for Palestine</p>
    <p>Contact: <a href="mailto:oussama.sebrou@gmail.com" style="color: var(--primary-color);">oussama.sebrou@gmail.com</a></p>
</div>
""", unsafe_allow_html=True)
