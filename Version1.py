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

# Enhanced prompt template for Palestine-related questions with more reliable sources
def build_palestine_prompt(user_question):
    return f"""
You are an expert assistant dedicated to providing accurate, in-depth, and highly informative answers specifically about Palestine and related issues.

Your answers should focus entirely on Palestine-related topics. If the question is not related to Palestine, respond with: "Sorry! I'm trained just about Palestine Issue."

Respond to the user question with:
- Historical background with accurate timeline and context
- Structure your response like a professional news article or academic report with clear sections
- Base your information on trusted sources such as:
  * Al Jazeera (aljazeera.com) - Known for comprehensive coverage of Middle East issues
  * Middle East Eye (middleeasteye.net) - Independent coverage of Middle East affairs
  * Metras (https://metras.co/) - Provides in-depth analysis on Palestinian affairs
  * Electronic Intifada (electronicintifada.net) - News and analysis on Palestine
  * Anadolu Agency (aa.com.tr) - Turkish state-run news agency with Middle East coverage
  * Palestine Chronicle (palestinechronicle.com) - Palestinian perspective on news
  * Institute for Palestine Studies (palestine-studies.org) - Academic research
  * B'Tselem (btselem.org) - Israeli human rights organization documenting abuses
  * Human Rights Watch (hrw.org) - International human rights monitoring
  * Amnesty International (amnesty.org) - Global human rights organization
  * United Nations Relief and Works Agency (unrwa.org) - UN agency for Palestinian refugees
  * UN Office for the Coordination of Humanitarian Affairs (ochaopt.org) - UN humanitarian reports
  * Academic books by scholars like Ilan Pappé, Edward Said, Rashid Khalidi, and Noam Chomsky
  * Peer-reviewed journals on Middle Eastern studies and international relations
  * Palestinian academic institutions and research centers
  * Historical archives and primary source documents

- Include specific citations when possible (e.g., "According to Al Jazeera's reporting on [date]..." or "As documented by Human Rights Watch in their 2023 report...")
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

# Function to get detailed boycott data
def get_boycott_data():
    # Predefined boycott data based on research
    boycott_data = {
        "Food & Beverages": {
            "companies": [
                {
                    "name": "Starbucks",
                    "reason": "Howard Schultz, founder and major shareholder of Starbucks, is a staunch supporter of Israel who invests heavily in Israel's economy, including a recent $1.7 billion investment in cybersecurity startup Wiz.",
                    "action": "Don't buy Starbucks products. Don't sell Starbucks products. Don't work for Starbucks.",
                    "alternatives": ["Caffe Nero", "Local independent cafes", "Local Arab cafes"]
                },
                {
                    "name": "Coca-Cola",
                    "reason": "Coca-Cola has a bottling plant in the Atarot Industrial Zone, an illegal Israeli settlement in occupied East Jerusalem. The company continues to support Israel's economy despite human rights violations.",
                    "action": "Boycott all Coca-Cola products, including Sprite, Fanta, and other associated brands.",
                    "alternatives": ["Local beverage brands", "Homemade sparkling water", "Natural juices"]
                },
                {
                    "name": "McDonald's",
                    "reason": "McDonald's Israel provided thousands of free meals to Israeli soldiers during military operations in Gaza. The Israeli franchise has openly supported military actions against Palestinians.",
                    "action": "Don't eat at McDonald's.",
                    "alternatives": ["Local restaurants", "Local fast food chains"]
                },
                {
                    "name": "Nestlé",
                    "reason": "Nestlé has been operating in Israel since 1995 and has production facilities in contested areas. The company has been criticized for exploiting Palestinian water resources.",
                    "action": "Avoid Nestlé products, including bottled water, cereals, and dairy products.",
                    "alternatives": ["Local brands", "Artisanal products", "Filtered tap water"]
                },
                {
                    "name": "PepsiCo",
                    "reason": "PepsiCo operates in Israel and has facilities in contested territories. The company continues its activities despite calls for boycott.",
                    "action": "Avoid all PepsiCo products, including Lay's chips, Doritos, and Pepsi beverages.",
                    "alternatives": ["Local beverages", "Locally manufactured snacks"]
                },
                {
                    "name": "Sabra Hummus",
                    "reason": "Sabra is a joint venture between PepsiCo and the Strauss Group, an Israeli company that provides support to elite units of the Israeli military involved in human rights violations.",
                    "action": "Don't buy Sabra hummus.",
                    "alternatives": ["Homemade hummus", "Local Arab hummus brands"]
                }
            ]
        },
        "Technology": {
            "companies": [
                {
                    "name": "HP (Hewlett-Packard)",
                    "reason": "HP provides technologies used in Israel's control and surveillance system, including for military checkpoints. Its technologies are used to maintain the apartheid and segregation system.",
                    "action": "Don't buy HP products, including computers, printers, and supplies.",
                    "alternatives": ["Lenovo", "Brother", "Epson", "Asian brands"]
                },
                {
                    "name": "Microsoft",
                    "reason": "Microsoft invested $1.5 billion in an Israeli AI company and has a major R&D center in Israel. The company works closely with the Israeli military to develop military technologies.",
                    "action": "Use open source alternatives when possible.",
                    "alternatives": ["Linux", "LibreOffice", "Open source alternatives"]
                },
                {
                    "name": "Google",
                    "reason": "Google signed a $1.2 billion cloud computing contract with the Israeli government (Project Nimbus). This technology is used for surveillance and targeting of Palestinians.",
                    "action": "Use alternative search engines and services.",
                    "alternatives": ["DuckDuckGo", "ProtonMail", "Firefox"]
                },
                {
                    "name": "Apple",
                    "reason": "Apple has significant investments in Israel and collaborates with Israeli companies involved in surveillance and military technology.",
                    "action": "Consider alternatives to Apple products.",
                    "alternatives": ["Samsung", "Xiaomi", "Huawei", "Android phones"]
                },
                {
                    "name": "Intel",
                    "reason": "Intel is one of the largest employers in the Israeli tech sector with several plants and R&D centers. The company contributes significantly to Israel's economy.",
                    "action": "Prefer AMD processors when possible.",
                    "alternatives": ["AMD", "ARM", "Other processor manufacturers"]
                }
            ]
        },
        "Fashion & Clothing": {
            "companies": [
                {
                    "name": "Puma",
                    "reason": "Puma sponsors the Israel Football Association, which includes teams in illegal settlements. This support legitimizes the occupation and violations of international law.",
                    "action": "Don't buy Puma products.",
                    "alternatives": ["Adidas", "New Balance", "Local brands", "Li-Ning"]
                },
                {
                    "name": "Skechers",
                    "reason": "Skechers has stores in illegal Israeli settlements and maintains business partnerships in Israel, contributing to the occupation economy.",
                    "action": "Boycott Skechers shoes and clothing.",
                    "alternatives": ["Brooks", "ASICS", "Ethical brands"]
                },
                {
                    "name": "H&M",
                    "reason": "H&M operates stores in Israel, including in contested areas. The company has ignored calls to cease operations in occupied territories.",
                    "action": "Don't shop at H&M.",
                    "alternatives": ["Ethical fashion brands", "Second-hand clothing"]
                },
                {
                    "name": "Zara",
                    "reason": "Zara has stores in Israel and sources from Israeli suppliers. The brand has been criticized for its lack of ethical stance regarding the occupation.",
                    "action": "Avoid shopping at Zara.",
                    "alternatives": ["Local brands", "Independent boutiques"]
                },
                {
                    "name": "Victoria's Secret",
                    "reason": "Victoria's Secret is owned by L Brands, which has significant investments in Israel and stores in contested areas.",
                    "action": "Boycott Victoria's Secret products.",
                    "alternatives": ["Ethical lingerie brands", "Local brands"]
                }
            ]
        },
        "Cosmetics": {
            "companies": [
                {
                    "name": "L'Oréal",
                    "reason": "L'Oréal operates in Israel and has acquired Israeli cosmetics companies. The company has facilities in contested territories and benefits from the occupation.",
                    "action": "Boycott L'Oréal products and its associated brands.",
                    "alternatives": ["The Body Shop", "Lush", "Natural brands", "Halal cosmetics"]
                },
                {
                    "name": "Estée Lauder",
                    "reason": "Estée Lauder chairman, Ronald Lauder, is a strong supporter of Israel and funds pro-Israel organizations. He has publicly defended Israeli military actions against Palestinians.",
                    "action": "Don't buy Estée Lauder products and its associated brands.",
                    "alternatives": ["Ethical cosmetics brands", "Natural products"]
                },
                {
                    "name": "Yves Saint Laurent Beauty / YSL Beauty",
                    "reason": "YSL Beauty is owned by L'Oréal Group, which operates in Israel and has ties to Israeli companies involved in the occupation.",
                    "action": "Avoid YSL Beauty products.",
                    "alternatives": ["Ethical cosmetics brands", "Natural products"]
                },
                {
                    "name": "Garnier",
                    "reason": "Garnier is a subsidiary of L'Oréal that provided free products to Israeli soldiers during military operations in Gaza.",
                    "action": "Don't buy Garnier products.",
                    "alternatives": ["Natural hair products", "Local brands"]
                }
            ]
        },
        "Finance": {
            "companies": [
                {
                    "name": "eToro",
                    "reason": "eToro is an Israeli online trading company that supports Israel's economy and contributes to taxes that fund the occupation.",
                    "action": "Use other trading and investment platforms.",
                    "alternatives": ["Alternative trading platforms", "Ethical banks"]
                },
                {
                    "name": "PayPal",
                    "reason": "PayPal operates in Israel but refuses to provide its services to Palestinians in the occupied territories, creating blatant economic discrimination.",
                    "action": "Use alternatives to PayPal when possible.",
                    "alternatives": ["Wise", "Local banking services", "Bank transfers"]
                },
                {
                    "name": "Citibank",
                    "reason": "Citibank has significant investments in Israel and finances projects in occupied territories, contributing to the expansion of illegal settlements.",
                    "action": "Avoid using Citibank services.",
                    "alternatives": ["Local banks", "Credit unions", "Ethical banks"]
                }
            ]
        },
        "Other": {
            "companies": [
                {
                    "name": "SodaStream",
                    "reason": "SodaStream operated a factory in an illegal Israeli settlement in the occupied West Bank before relocating due to pressure. The company continues to benefit from discriminatory policies.",
                    "action": "Don't buy SodaStream products.",
                    "alternatives": ["Bottled sparkling water", "Other carbonation systems"]
                },
                {
                    "name": "Volvo Heavy Machinery",
                    "reason": "Volvo heavy equipment is used for demolishing Palestinian homes and building illegal settlements. These machines are essential tools of the occupation.",
                    "action": "Raise awareness about the use of Volvo equipment in occupied territories.",
                    "alternatives": ["Other heavy equipment manufacturers"]
                },
                {
                    "name": "Caterpillar",
                    "reason": "Caterpillar bulldozers are used to demolish Palestinian homes and build the illegal separation wall. These machines are specially modified for military demolitions.",
                    "action": "Boycott Caterpillar products and raise awareness about their use.",
                    "alternatives": ["Other construction equipment manufacturers"]
                },
                {
                    "name": "Airbnb",
                    "reason": "Airbnb lists properties in illegal Israeli settlements in occupied Palestinian territory, thus legitimizing the occupation and profiting from stolen land.",
                    "action": "Don't use Airbnb for your travel bookings.",
                    "alternatives": ["Booking.com (with vigilance)", "Local hotels", "Independent hostels"]
                },
                {
                    "name": "TripAdvisor",
                    "reason": "TripAdvisor promotes tourist attractions in illegal settlements without mentioning their illegal status under international law.",
                    "action": "Avoid using TripAdvisor, particularly for Middle East travel.",
                    "alternatives": ["Independent travel guides", "Local recommendations"]
                }
            ]
        }
    }
    
    return boycott_data

# Function to get educational resources about Palestine
def get_educational_resources():
    resources = {
        "History": [
            {
                "title": "The Nakba: Palestinian Exodus of 1948",
                "description": "The Nakba (catastrophe in Arabic) refers to the mass expulsion and dispossession of Palestinians during the creation of the State of Israel in 1948. Over 750,000 Palestinians were forced to leave their homes, and more than 500 Palestinian villages were destroyed.",
                "sources": ["Institute for Palestine Studies", "UN Archives", "Survivor testimonies"],
                "key_facts": [
                    "Over 750,000 Palestinians displaced",
                    "More than 500 Palestinian villages destroyed",
                    "Confiscation of 78% of historical Palestinian lands",
                    "Creation of the world's longest unresolved refugee crisis"
                ]
            },
            {
                "title": "The 1967 Occupation and Its Consequences",
                "description": "In June 1967, Israel occupied the West Bank, East Jerusalem, the Gaza Strip, the Golan Heights, and the Sinai Peninsula during the Six-Day War. This occupation, which continues today (except for Sinai), has led to the expansion of illegal Israeli settlements and a system of military control over the Palestinian population.",
                "sources": ["United Nations", "B'Tselem", "Human Rights Watch"],
                "key_facts": [
                    "Over 600,000 Israeli settlers live illegally in the West Bank and East Jerusalem",
                    "More than 60% of the West Bank is under full Israeli control (Area C)",
                    "Over 700 km of separation wall, declared illegal by the International Court of Justice",
                    "More than 65 UN resolutions condemning the occupation, all ignored by Israel"
                ]
            },
            {
                "title": "The Oslo Accords and the Failure of the Peace Process",
                "description": "The Oslo Accords, signed in 1993-1995, were supposed to lead to a two-state solution within a five-year timeframe. However, they failed due to continued Israeli settlement expansion, violations of the agreements, and lack of political will to resolve fundamental issues such as Jerusalem, refugees, and borders.",
                "sources": ["Oslo Accords documents", "United Nations", "Diplomatic analyses"],
                "key_facts": [
                    "Division of the West Bank into Areas A, B, and C with different levels of control",
                    "Creation of the Palestinian Authority as an interim government",
                    "Tripling of Israeli settler numbers since the Oslo Accords",
                    "Territorial fragmentation making a viable Palestinian state increasingly impossible"
                ]
            },
            {
                "title": "The Gaza Blockade Since 2007",
                "description": "Since 2007, the Gaza Strip has been under a land, air, and sea blockade imposed by Israel and Egypt. This blockade has created a catastrophic humanitarian crisis, limiting access to food, medicine, electricity, and clean water for more than 2 million Palestinians living in this coastal enclave.",
                "sources": ["UNRWA", "WHO", "OCHA", "Oxfam"],
                "key_facts": [
                    "Over 2 million people live in an area of 365 km²",
                    "More than 95% of water is unfit for human consumption",
                    "Unemployment rate exceeding 45%, one of the highest in the world",
                    "Electricity available only 4-12 hours per day on average",
                    "More than 80% of the population depends on humanitarian aid"
                ]
            }
        ],
        "Human Rights": [
            {
                "title": "The Apartheid System in Occupied Palestine",
                "description": "Numerous human rights organizations, including Amnesty International, Human Rights Watch, and B'Tselem, have concluded that Israel practices apartheid against Palestinians. This system includes discriminatory laws, territorial segregation, movement restrictions, and unequal allocation of resources.",
                "sources": ["Amnesty International", "Human Rights Watch", "B'Tselem", "Al-Haq"],
                "key_facts": [
                    "Two separate legal systems in the West Bank: civil law for settlers, military law for Palestinians",
                    "More than 65 discriminatory laws against Palestinian citizens of Israel",
                    "Complex permit system limiting Palestinians' freedom of movement",
                    "Unequal access to water: settlers receive 3-5 times more water than Palestinians"
                ]
            },
            {
                "title": "Administrative Detention and Political Prisoners",
                "description": "Israel extensively uses administrative detention to imprison Palestinians without charge or trial, based on 'secret evidence.' Thousands of Palestinians, including children, are detained in conditions that often violate international law.",
                "sources": ["Addameer", "International Committee of the Red Cross", "UNICEF"],
                "key_facts": [
                    "More than 800,000 Palestinians detained since 1967",
                    "Approximately 500-700 Palestinian children arrested each year",
                    "99.7% conviction rate in Israeli military courts",
                    "Systematic torture and mistreatment documented by human rights organizations"
                ]
            },
            {
                "title": "Restrictions on Freedom of Movement",
                "description": "Palestinians face a complex system of movement restrictions including checkpoints, the separation wall, settler-only roads, and a permit system that severely limits their ability to move freely in their own territory.",
                "sources": ["OCHA", "B'Tselem", "Machsom Watch"],
                "key_facts": [
                    "More than 700 physical obstacles in the West Bank (checkpoints, roadblocks, etc.)",
                    "The separation wall extends for 712 km, 85% of which is inside the West Bank",
                    "Thousands of Palestinians separated from their agricultural lands by the wall",
                    "Complex permit system required to enter East Jerusalem, travel between Gaza and the West Bank, or access 'seam zones'"
                ]
            },
            {
                "title": "Home Demolitions and Forced Displacement",
                "description": "Israel regularly practices Palestinian home demolitions, either as punitive measures or under the pretext of lacking building permits (which are systematically denied to Palestinians). These practices constitute serious violations of international humanitarian law.",
                "sources": ["OCHA", "B'Tselem", "Al-Haq", "Norwegian Refugee Council"],
                "key_facts": [
                    "More than 55,000 Palestinian homes demolished since 1967",
                    "Less than 2% of building permit applications approved for Palestinians in Area C",
                    "East Jerusalem particularly targeted for demolitions and settlement expansion",
                    "'Silent transfer' policy aimed at reducing Palestinian presence in strategic areas"
                ]
            }
        ],
        "Culture and Society": [
            {
                "title": "Palestinian Cultural Heritage",
                "description": "Palestinian culture is rich and diverse, with traditions dating back thousands of years. It includes distinctive cuisine, traditional arts such as embroidery, pottery, and calligraphy, as well as a rich literary and musical tradition.",
                "sources": ["Arab World Institute", "Palestinian Museum", "UNESCO"],
                "key_facts": [
                    "Palestinian embroidery (tatreez) is inscribed on UNESCO's Intangible Cultural Heritage list",
                    "The olive tree is a central symbol of Palestinian identity and resistance",
                    "Dabke is a traditional dance performed at celebrations",
                    "Resistance poetry is an important form of cultural expression, with poets like Mahmoud Darwish"
                ]
            },
            {
                "title": "Palestinian Diaspora",
                "description": "Following the 1948 Nakba and ongoing occupation, a significant Palestinian diaspora has formed worldwide. These communities maintain strong ties to their homeland and play a crucial role in preserving Palestinian identity and advocating for Palestinian rights.",
                "sources": ["UNRWA", "Institute for Palestine Studies", "Badil"],
                "key_facts": [
                    "More than 7 million Palestinian refugees and displaced persons worldwide",
                    "Significant Palestinian communities in Jordan, Lebanon, Syria, Chile, and the United States",
                    "The key (miftah) is a symbol of refugees' right of return",
                    "Intergenerational transmission of Palestinian memory and identity"
                ]
            },
            {
                "title": "Cultural and Artistic Resistance",
                "description": "In the face of occupation, Palestinians have developed various forms of cultural and artistic resistance. Palestinian art, music, literature, and cinema serve to preserve national identity, document the realities of occupation, and express aspirations for freedom and self-determination.",
                "sources": ["Palestinian Film Festival", "Dar Yusuf Nasri Jacir for Art and Research", "Edward Said Institute"],
                "key_facts": [
                    "Emergence of internationally recognized Palestinian cinema (Elia Suleiman, Hany Abu-Assad)",
                    "Street art and graffiti on the separation wall as a form of visual protest",
                    "Development of cultural festivals such as Palest'In & Out and the Palestine Literature Festival",
                    "Use of social media to document and share occupation realities"
                ]
            },
            {
                "title": "Education and Academic Resistance",
                "description": "Despite obstacles imposed by the occupation, Palestinians place high value on education. Palestinian universities are centers of knowledge production and intellectual resistance, although they are often targeted by Israeli forces.",
                "sources": ["Birzeit University", "Right to Education Campaign", "PACBI"],
                "key_facts": [
                    "Literacy rates among the highest in the Arab world despite occupation",
                    "Palestinian universities regularly subjected to raids, closures, and restrictions",
                    "Development of Palestine Studies as an academic discipline",
                    "Academic boycott movement against institutions complicit in the occupation"
                ]
            }
        ],
        "Resistance and Solidarity": [
            {
                "title": "The BDS Movement (Boycott, Divestment, Sanctions)",
                "description": "Launched in 2005 by Palestinian civil society, the BDS movement calls for non-violent measures to pressure Israel to comply with international law and Palestinian rights. Inspired by the South African anti-apartheid movement, it has gained significant global support.",
                "sources": ["BDS National Committee", "Palestinian Campaign for the Academic and Cultural Boycott of Israel (PACBI)"],
                "key_facts": [
                    "Three main demands: end of occupation, equality for Palestinian citizens of Israel, right of return for refugees",
                    "Notable successes including divestment by pension funds and universities",
                    "Supported by unions, churches, social movements, and personalities worldwide",
                    "Targets institutions complicit in the occupation, not individuals"
                ]
            },
            {
                "title": "Non-violent Popular Resistance",
                "description": "Palestinians have a long tradition of non-violent popular resistance against occupation, including peaceful demonstrations, sit-ins, and non-violent direct actions. These movements are often violently suppressed by Israeli forces.",
                "sources": ["Popular Struggle Coordination Committee", "Stop the Wall Campaign", "Al-Haq"],
                "key_facts": [
                    "Villages like Bil'in, Ni'lin, and Nabi Saleh known for their weekly demonstrations against the wall",
                    "Use of video documentation and social media to expose violations",
                    "International participation through movements like the International Solidarity Movement",
                    "Systematic repression including arrests, detentions, and sometimes live fire against unarmed protesters"
                ]
            },
            {
                "title": "International Solidarity",
                "description": "The solidarity movement with Palestine has developed globally, involving civil society organizations, unions, religious groups, students, and human rights activists who support the Palestinian struggle for justice and self-determination.",
                "sources": ["Palestine Solidarity Campaign", "Jewish Voice for Peace", "BDS Movement"],
                "key_facts": [
                    "International Day of Solidarity with the Palestinian People celebrated on November 29",
                    "Divestment campaigns in universities and religious institutions",
                    "Gaza flotillas attempting to break the maritime blockade",
                    "Solidarity movements including progressive Jews opposed to Israeli policies"
                ]
            },
            {
                "title": "International Recognition of the State of Palestine",
                "description": "The diplomatic struggle for recognition of the State of Palestine is an important form of political resistance. To date, more than 140 countries have recognized the State of Palestine, although most Western powers have not yet done so.",
                "sources": ["United Nations", "Palestine Liberation Organization", "Palestinian Ministry of Foreign Affairs"],
                "key_facts": [
                    "In 2012, Palestine obtained non-member observer state status at the UN",
                    "Membership in various international organizations, including the International Criminal Court",
                    "Recognition by more than 140 countries out of 193 UN member states",
                    "Ongoing campaigns for recognition by Western countries"
                ]
            }
        ]
    }
    return resources

# Function to get companies that support Israel (for boycott section) with alternatives
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

# App UI with enhanced professional features
def main():
    st.set_page_config(
        page_title="Palestina-AI", 
        page_icon="🕊️", 
        layout="wide"
    )

    # Custom CSS for a more professional look with dark mode compatibility
    st.markdown("""
    <style>
    .main {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    
    :root {
        --primary-color: #1f77b4;
        --secondary-color: #2ca02c;
        --danger-color: #d62728;
        --background-color: #f8f9fa;
        --card-background: #ffffff;
        --text-color: #333333;
        --border-color: #f0f0f0;
        --quote-color: #1f77b4;
        --footer-color: #666666;
    }
    
    [data-theme="dark"] {
        --primary-color: #4a9ced;
        --secondary-color: #5fd35f;
        --danger-color: #ff5b5b;
        --background-color: #f8f9fa;
        --card-background: #1e2129;
        --text-color: #f0f2f6;
        --border-color: #f0f0f0;
        --quote-color: #4a9ced;
        --footer-color: #cccccc;
    }
    
    .stApp {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    
    .stButton > button {
        border-radius: 10px;
        background-color: var(--primary-color);
        color: white;
        font-weight: bold;
    }
    
    .stExpander {
        border-radius: 10px;
        border: 1px solid var(--border-color);
        background-color: var(--card-background);
    }
    
    h1, h2, h3 {
        color: var(--primary-color);
    }
    
    .quote-box {
        border-left: 4px solid var(--quote-color);
        padding-left: 15px;
        margin-top: 20px;
        font-size: 1.2em;
        font-weight: bold;
        color: var(--quote-color);
    }
    
    .quote-author {
        text-align: right;
        color: var(--text-color);
        font-style: italic;
    }
    
    .team-member {
        padding: 5px 0;
        border-bottom: 1px solid var(--border-color);
        color: var(--text-color);
    }
    
    .boycott-category {
        font-weight: bold;
        color: var(--danger-color);
        margin-top: 10px;
    }
    
    .boycott-company {
        margin-left: 15px;
        padding: 2px 0;
        color: var(--text-color);
    }
    
    .boycott-alternative {
        margin-left: 15px;
        padding: 2px 0;
        color: var(--secondary-color);
    }
    
    .footer {
        text-align: center;
        margin-top: 30px;
        padding: 10px;
        font-size: 0.8em;
        color: var(--footer-color);
    }
    
    .company-card {
        background-color: var(--card-background);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 4px solid var(--danger-color);
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .company-name {
        font-weight: bold;
        font-size: 1.1em;
        margin-bottom: 5px;
        color: var(--text-color);
    }
    
    .company-reason {
        margin-bottom: 10px;
        font-style: italic;
        color: var(--text-color);
    }
    
    .company-action {
        font-weight: bold;
        color: var(--danger-color);
        margin-bottom: 5px;
    }
    
    .company-alternatives {
        color: var(--secondary-color);
    }
    
    .resource-card {
        background-color: var(--card-background);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid var(--primary-color);
    }
    
    .resource-title {
        color: var(--primary-color);
        font-size: 1.3em;
        margin-bottom: 10px;
    }
    
    .resource-description {
        margin-bottom: 15px;
        line-height: 1.6;
        color: var(--text-color);
    }
    
    .resource-facts {
        background-color: rgba(31, 119, 180, 0.1);
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        color: var(--text-color);
    }
    
    .resource-sources {
        font-style: italic;
        color: var(--footer-color);
        font-size: 0.9em;
    }
    
    .fact-item {
        margin-bottom: 5px;
        padding-left: 20px;
        position: relative;
        color: var(--text-color);
    }
    
    .fact-item:before {
        content: "•";
        position: absolute;
        left: 0;
        color: var(--primary-color);
    }
    
    .section-title {
        color: var(--primary-color);
        font-size: 2em;
        margin: 30px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid var(--border-color);
    }
    
    .subsection-title {
        color: var(--text-color);
        font-size: 1.5em;
        margin: 25px 0 15px 0;
    }
    
    .chat-container {
        background-color: var(--card-background);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }
    
    /* Improved sidebar button styling */
    .sidebar-button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 10px;
        padding: 12px 20px;
        font-weight: bold;
        margin: 8px 0;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
        width: 100%;
        border: none;
        display: inline-block;
        font-size: 16px;
    }
    
    .sidebar-button:hover {
        background-color: #145a8d;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Language selector styling */
    .language-selector {
        margin-top: 15px;
        margin-bottom: 25px;
        padding: 10px;
        border-radius: 10px;
        background-color: var(--card-background);
        border: 1px solid var(--border-color);
    }
    
    .language-title {
        font-weight: bold;
        margin-bottom: 10px;
        color: var(--primary-color);
    }
    </style>
    """, unsafe_allow_html=True)

    # Create session state variables if they don't exist
    if 'show_chat' not in st.session_state:
        st.session_state.show_chat = True
    if 'show_boycott' not in st.session_state:
        st.session_state.show_boycott = False
    if 'show_education' not in st.session_state:
        st.session_state.show_education = False
    if 'language' not in st.session_state:
        st.session_state.language = 'english'

    # Sidebar
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/0/00/Flag_of_Palestine.svg", width=250)
        st.title("Palestine AI")
        
        # Language selector
        st.markdown('<div class="language-title">Select Language</div>', unsafe_allow_html=True)
        language_options = {
            'english': 'English / الإنجليزية',
            'arabic': 'Arabic / العربية'
        }
        
        # Create language buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button('English', key='en_button', use_container_width=True):
                st.session_state.language = 'english'
        with col2:
            if st.button('العربية', key='ar_button', use_container_width=True):
                st.session_state.language = 'arabic'
        
        st.markdown("---")
        
        # Navigation buttons for main area with improved styling
        st.markdown("### Navigation")
        
        # Button to show chat
        if st.button('Chat with Palestina Ai', key='chat_button', use_container_width=True):
            st.session_state.show_chat = True
            st.session_state.show_boycott = False
            st.session_state.show_education = False
        
        # Button to show boycott information
        if st.button('Boycott Information', key='boycott_button', use_container_width=True):
            st.session_state.show_chat = False
            st.session_state.show_boycott = True
            st.session_state.show_education = False
        
        # Button to show educational resources
        if st.button('Educational Resources', key='education_button', use_container_width=True):
            st.session_state.show_chat = False
            st.session_state.show_boycott = False
            st.session_state.show_education = True
        
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
        
        # Help Section
        with st.expander("Help", expanded=True):
            st.markdown("### How to Use the App")
            st.markdown("""
            - Ask Questions: You can ask anything related to Palestine's history, current events, or humanitarian issues.
            - Multi-Languages Supported: You can ask in English or Arabic.
            - Dark Mode: To switch to dark mode, go to Settings > Choose app theme > Dark Mode.
            - App Features:
              - In-depth answers focused only on Palestine.
              - Context-aware responses tailored to your question.
              - Accurate, detailed information backed by AI.
              - Educational Resources: Access reliable information about Palestine.
              - Boycott Information: Learn about companies supporting Israel and alternatives.
            """)
        st.markdown("---")
        
        # About Us Section
        with st.expander("About Us", expanded=False):
            st.markdown("#### Palestina AI")
            st.markdown("This app was developed to provide in-depth, AI-powered insights into the Palestinian cause.")
            st.markdown("""
            Version: 1.2.0
            
            #### Features
            - AI-Powered Insights about Palestine
            - Focus on History, Humanitarian Issues, and Current Events
            - Multi-Language Support
            - Accurate and Context-Aware Responses
            - Boycott Information and Support Resources
            - Educational Resources
            
            © 2025 Palestine AI Team. All rights reserved.
            
            [Contact Us](mailto:your-email@example.com?subject=Palestine%20Info%20Bot%20Inquiry&body=Dear%20Palestine%20Info%20Bot%20Team,%0A%0AWe%20are%20writing%20to%20inquire%20about%20[your%20inquiry]%2C%20specifically%20[details%20of%20your%20inquiry].%0A%0A[Provide%20additional%20context%20and%20details%20here].%0A%0APlease%20let%20us%20know%20if%20you%20require%20any%20further%20information%20from%20our%20end.%0A%0ASincerely,%0A[Your%20Company%20Name]%0A[Your%20Name]%0A[Your%20Title]%0A[Your%20Phone%20Number]%0A[Your%20Email%20Address])
            """)

    # Main content area
    if st.session_state.language == 'english':
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
    else:  # Arabic
        st.title("Palestina AI - From the River To the sea")
        
        # Quote of the Day section in Arabic
        st.markdown("""
        <div class="quote-box" dir="rtl">
            "إن قضية فلسطين محنةٌ امتحن الله بها ضمائركم وهممكم وأموالكم ووحدتكم."
        </div>
        <div class="quote-author" dir="rtl">
            — البشير الإبراهيمي
        </div>
        """, unsafe_allow_html=True)
        
        # Information cards in a grid layout in Arabic
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div dir="rtl">
            ###السياق التاريخي
            فلسطين أرض ذات تاريخ عريق يمتد لآلاف السنين، وتؤكد الوثائق التاريخية أن الشعب الفلسطيني هو المالك الشرعي لهذه الأرض. كانت فلسطين موطنًا لسكانها الأصليين، الذين حافظوا على وجودهم وثقافتهم رغم محاولات المحو والتهجير على مر العصور.
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div dir="rtl">
            ###الوضع الحالي
            يستمر الشعب الفلسطيني في مواجهة تحديات إنسانية خطيرة بسبب الاحتلال المستمر والحصار، خاصة في قطاع غزة، حيث يُحرم السكان من الوصول إلى الموارد والخدمات الأساسية. تشكل هذه الإجراءات انتهاكات واضحة لحقوق الإنسان والقانون الدولي، الذي يضمن حق الشعوب في العيش بحرية وكرامة في وطنهم.
            </div>
            """, unsafe_allow_html=True)

    # Display content based on session state
    if st.session_state.show_chat:
        if st.session_state.language == 'english':
            st.markdown("<div class='section-title'>Chat with AI about Palestine</div>", unsafe_allow_html=True)
            
            # User input section with enhanced styling
            st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
            st.markdown("### Ask Your Question")
            st.markdown("Get accurate, detailed information about Palestine's history, current events, and humanitarian issues.")
            
            user_question = st.text_input("", placeholder="Type your question about Palestine here...", key="text_question")
            
            # Add a submit button for better UX
            submit_button = st.button("Get Answer")
        else:  # Arabic
            st.markdown("<div class='section-title' dir='rtl'>تحدث مع الذكاء الاصطناعي حول فلسطين</div>", unsafe_allow_html=True)
            
            # User input section with enhanced styling
            st.markdown("<div class='chat-container' dir='rtl'>", unsafe_allow_html=True)
            st.markdown("<h3>Ask your question about plastine</h3>", unsafe_allow_html=True)
            st.markdown("احصل على معلومات دقيقة ومفصلة حول تاريخ فلسطين والأحداث الجارية والقضية المركزية.", unsafe_allow_html=True)
            
            user_question = st.text_input("", placeholder="Put your question (Multi-language answes)", key="text_question_ar")
            
            # Add a submit button for better UX
            submit_button = st.button("Get answer")

        # Process the question when submitted
        if user_question and submit_button:
            # Check if the question is related to Palestine
            is_palestine = is_palestine_related(user_question)
            
            with st.spinner("Generating comprehensive answer..." if st.session_state.language == 'english' else "Generating comprehensive answer..."):
                answer = ask_about_palestine(user_question)
                
                # Create a container with better styling for the answer
                answer_container = st.container()
                with answer_container:
                    st.markdown("<div style='background-color: rgba(31, 119, 180, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid var(--primary-color);'>", unsafe_allow_html=True)
                    # Typing effect for response
                    with st.empty():  # Create an empty placeholder to display the typing effect
                        typing_effect(answer)
                    st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif st.session_state.show_boycott:
        if st.session_state.language == 'english':
            st.markdown("<div class='section-title'>Boycott Information</div>", unsafe_allow_html=True)
            
            st.markdown("""
            The boycott movement aims to apply economic and political pressure on Israel to comply with international law and Palestinian rights. 
            This form of non-violent resistance is inspired by the South African anti-apartheid movement and has gained significant global support.
            
            Below is a detailed list of companies that support Israel, with explanations of their involvement and alternatives you can use instead.
            """)
            
            # Get boycott data
            boycott_data = get_boycott_data()
            
            # Create tabs for different categories
            boycott_tabs = st.tabs(list(boycott_data.keys()))
            
            # Display detailed boycott information for each category
            for i, (category, tab) in enumerate(zip(boycott_data.keys(), boycott_tabs)):
                with tab:
                    st.markdown(f"### {category}")
                    
                    for company in boycott_data[category]["companies"]:
                        st.markdown(f"""
                        <div class="company-card">
                            <div class="company-name">{company['name']}</div>
                            <div class="company-reason">{company['reason']}</div>
                            <div class="company-action">Recommended action: {company['action']}</div>
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
            
            # Add information about the BDS movement
            st.markdown("""
            ### The BDS Movement (Boycott, Divestment, Sanctions)
            
            The BDS movement was launched in 2005 by Palestinian civil society. It calls for three main actions:
            
            1. **Boycott**: Refusing to purchase products and services from companies complicit in the occupation
            2. **Divestment**: Withdrawing investments from companies and institutions that profit from the occupation
            3. **Sanctions**: Pressuring for sanctions against Israel until it complies with international law
            
            The BDS movement has three fundamental demands:
            1. End the occupation and colonization of all Arab lands
            2. Recognize the fundamental rights of Arab-Palestinian citizens of Israel to full equality
            3. Respect, protect, and promote the rights of Palestinian refugees to return to their homes and properties
            
            For more information, visit [the official BDS movement website](https://bdsmovement.net/).
            """)
        else:  # Arabic
            st.markdown("<div class='section-title' dir='rtl'>معلومات المقاطعة</div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div dir="rtl">
            تهدف حركة المقاطعة إلى ممارسة ضغط اقتصادي وسياسي على إسرائيل للامتثال للقانون الدولي وحقوق الفلسطينيين.
            هذا الشكل من المقاومة اللاعنفية مستوحى من حركة مناهضة الفصل العنصري في جنوب أفريقيا وقد اكتسب دعمًا عالميًا كبيرًا.
            
            فيما يلي قائمة مفصلة بالشركات التي تدعم إسرائيل، مع شرح لتورطها والبدائل التي يمكنك استخدامها بدلاً منها.
            </div>
            """, unsafe_allow_html=True)
            
            # Get boycott data
            boycott_data = get_boycott_data()
            
            # Create tabs for different categories
            boycott_tabs = st.tabs(list(boycott_data.keys()))
            
            # Display detailed boycott information for each category
            for i, (category, tab) in enumerate(zip(boycott_data.keys(), boycott_tabs)):
                with tab:
                    st.markdown(f"<h3 dir='rtl'>{category}</h3>", unsafe_allow_html=True)
                    
                    for company in boycott_data[category]["companies"]:
                        st.markdown(f"""
                        <div class="company-card" dir="rtl">
                            <div class="company-name">{company['name']}</div>
                            <div class="company-reason">{company['reason']}</div>
                            <div class="company-action">الإجراء الموصى به: {company['action']}</div>
                            <div class="company-alternatives">
                                <strong>البدائل:</strong> {', '.join(company['alternatives'])}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("""
            <div dir="rtl">
            ###كيفية دعم غزة
            
            1. **مقاطعة المنتجات**: تجنب شراء منتجات من الشركات التي تدعم إسرائيل
            2. **اختيار البدائل**: استخدم البدائل المقترحة أو ابحث عن خيارات محلية
            3. **نشر الوعي**: شارك المعلومات حول الوضع في غزة
            4. **التبرع**: دعم المنظمات الإنسانية العاملة في غزة
            5. **المناصرة**: اتصل بممثليك للمطالبة باتخاذ إجراءات
            6. **الانضمام إلى الاحتجاجات**: المشاركة في المظاهرات السلمية
            
            تذكر أن الضغط الاقتصادي من خلال المقاطعة كان تاريخياً استراتيجية مقاومة لاعنفية فعالة.
            </div>
            """, unsafe_allow_html=True)
            
            # Add information about the BDS movement in Arabic
            st.markdown("""
            <div dir="rtl">
            ###حركة المقاطعة وسحب الاستثمارات وفرض العقوبات (BDS)
            
            تم إطلاق حركة المقاطعة في عام 2005 من قبل المجتمع المدني الفلسطيني. وهي تدعو إلى ثلاثة إجراءات رئيسية:
            
            1. **المقاطعة**: رفض شراء المنتجات والخدمات من الشركات المتواطئة في الاحتلال
            2. **سحب الاستثمارات**: سحب الاستثمارات من الشركات والمؤسسات التي تستفيد من الاحتلال
            3. **العقوبات**: الضغط من أجل فرض عقوبات على إسرائيل حتى تمتثل للقانون الدولي
            
            لحركة المقاطعة ثلاثة مطالب أساسية:
            1. إنهاء الاحتلال والاستعمار لجميع الأراضي العربية
            2. الاعتراف بالحقوق الأساسية للمواطنين العرب الفلسطينيين في إسرائيل للمساواة الكاملة
            3. احترام وحماية وتعزيز حقوق اللاجئين الفلسطينيين في العودة إلى ديارهم وممتلكاتهم
            
            لمزيد من المعلومات، قم بزيارة [الموقع الرسمي لحركة المقاطعة](https://bdsmovement.net/).
            </div>
            """, unsafe_allow_html=True)
    
    elif st.session_state.show_education:
        if st.session_state.language == 'english':
            st.markdown("<div class='section-title'>Educational Resources on Palestine</div>", unsafe_allow_html=True)
            
            st.markdown("""
            This section provides educational resources to help you learn more about Palestine, its history, culture, and current situation.
            The information presented here is based on reliable sources, including reports from human rights organizations, United Nations documents, academic studies, and direct testimonies.
            """)
            
            # Get educational resources
            resources = get_educational_resources()
            
            # Create tabs for different categories
            education_tabs = st.tabs(list(resources.keys()))
            
            # Display educational resources for each category
            for i, (category, tab) in enumerate(zip(resources.keys(), education_tabs)):
                with tab:
                    st.markdown(f"### {category}")
                    
                    for resource in resources[category]:
                        st.markdown(f"""
                        <div class="resource-card">
                            <div class="resource-title">{resource['title']}</div>
                            <div class="resource-description">{resource['description']}</div>
                            <div class="resource-facts">
                                <strong>Key Facts:</strong>
                                <div style="margin-top: 10px;">
                        """, unsafe_allow_html=True)
                        
                        for fact in resource['key_facts']:
                            st.markdown(f'<div class="fact-item">{fact}</div>', unsafe_allow_html=True)
                        
                        st.markdown(f"""
                                </div>
                            </div>
                            <div class="resource-sources">
                                <strong>Sources:</strong> {', '.join(resource['sources'])}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Add recommended reading and viewing section
            st.markdown("""
            ### Recommended Reading and Viewing
            
            #### Books
            - **"The Question of Palestine"** by Edward Said
            - **"Palestine: A Modern History"** by Ilan Pappé
            - **"The Ethnic Cleansing of Palestine"** by Ilan Pappé
            - **"Gaza in Crisis"** by Noam Chomsky and Ilan Pappé
            - **"The Hundred Years' War on Palestine"** by Rashid Khalidi
            
            #### Documentaries
            - **"5 Broken Cameras"** (2011) by Emad Burnat and Guy Davidi
            - **"The Salt of This Sea"** (2008) by Annemarie Jacir
            - **"Gaza Fight for Freedom"** (2019) by Abby Martin
            - **"Occupation 101"** (2006) by Sufyan Omeish and Abdallah Omeish
            - **"The Wanted 18"** (2014) by Amer Shomali and Paul Cowan
            
            #### Reliable Websites
            - [Al Jazeera](https://www.aljazeera.com/palestine-israel-conflict/) - Comprehensive coverage of Middle East issues
            - [B'Tselem](https://www.btselem.org/) - Israeli Information Center for Human Rights in the Occupied Territories
            - [Institute for Palestine Studies](https://www.palestine-studies.org/) - Academic research on Palestine
            - [UNRWA](https://www.unrwa.org/) - UN Relief and Works Agency for Palestine Refugees
            - [Electronic Intifada](https://electronicintifada.net/) - News, commentary, analysis, and reference materials about Palestine
            """)
        else:  # Arabic
            st.markdown("<div class='section-title' dir='rtl'>موارد تعليمية عن فلسطين</div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div dir="rtl">
            يوفر هذا القسم موارد تعليمية لمساعدتك على معرفة المزيد عن فلسطين وتاريخها وثقافتها ووضعها الحالي.
            تستند المعلومات المقدمة هنا إلى مصادر موثوقة، بما في ذلك تقارير من منظمات حقوق الإنسان، ووثائق الأمم المتحدة، والدراسات الأكاديمية، والشهادات المباشرة.
            </div>
            """, unsafe_allow_html=True)
            
            # Get educational resources
            resources = get_educational_resources()
            
            # Create tabs for different categories
            education_tabs = st.tabs(list(resources.keys()))
            
            # Display educational resources for each category
            for i, (category, tab) in enumerate(zip(resources.keys(), education_tabs)):
                with tab:
                    st.markdown(f"<h3 dir='rtl'>{category}</h3>", unsafe_allow_html=True)
                    
                    for resource in resources[category]:
                        st.markdown(f"""
                        <div class="resource-card" dir="rtl">
                            <div class="resource-title">{resource['title']}</div>
                            <div class="resource-description">{resource['description']}</div>
                            <div class="resource-facts">
                                <strong>حقائق رئيسية:</strong>
                                <div style="margin-top: 10px;">
                        """, unsafe_allow_html=True)
                        
                        for fact in resource['key_facts']:
                            st.markdown(f'<div class="fact-item">{fact}</div>', unsafe_allow_html=True)
                        
                        st.markdown(f"""
                                </div>
                            </div>
                            <div class="resource-sources">
                                <strong>المصادر:</strong> {', '.join(resource['sources'])}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Add recommended reading and viewing section in Arabic
            st.markdown("""
            <div dir="rtl">
            ### قراءات ومشاهدات موصى بها
            
            #### كتب
            - **"مسألة فلسطين"** لإدوارد سعيد
            - ** الموسوعة اليهودية والصهيونية وإسرائيل لـ عبد الوهاب المسيرى.
            - **"التطهير العرقي في فلسطين"** لإيلان بابيه
            - **"غزة في أزمة"** لنعوم تشومسكي وإيلان بابيه
            - **"حرب المائة عام على فلسطين"** لرشيد الخالدي
            
            #### أفلام وثائقية
            - **"خمس كاميرات محطمة"** (2011) لعماد برناط وغاي دافيدي
            - **"ملح هذا البحر"** (2008) لآن ماري جاسر
            - **"غزة تقاتل من أجل الحرية"** (2019) لآبي مارتن
            - **"احتلال 101"** (2006) لسفيان عميش وعبد الله عميش
            - **"المطلوبون الـ18"** (2014) لعامر الشوملي وبول كوان
            
            #### مواقع موثوقة
            - [الجزيرة](https://www.aljazeera.com/palestine-israel-conflict/) - تغطية شاملة لقضايا الشرق الأوسط
            - [بتسيلم](https://www.btselem.org/) - مركز المعلومات الإسرائيلي لحقوق الإنسان في الأراضي المحتلة
            - [معهد الدراسات الفلسطينية](https://www.palestine-studies.org/) - أبحاث أكاديمية حول فلسطين
            - [الأونروا](https://www.unrwa.org/) - وكالة الأمم المتحدة لإغاثة وتشغيل اللاجئين الفلسطينيين
            - [الانتفاضة الإلكترونية](https://electronicintifada.net/) - أخبار وتعليقات وتحليلات ومواد مرجعية حول فلسطين
            </div>
            """, unsafe_allow_html=True)

    # Footer
    if st.session_state.language == 'english':
        st.markdown("<div class='footer'>Palestine AI - Developed by Elkalem-Imrou Height School in collaboration with Erinov Company</div>", unsafe_allow_html=True)
    else:  # Arabic
        st.markdown("<div class='footer'>Palestina AI - Developed by Elkalem-Imrou Height School in collaboration with Erinov Company</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
