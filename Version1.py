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

# Function to get detailed boycott data
def get_boycott_data():
    # Predefined boycott data based on research
    boycott_data = {
        "Food & Beverages": {
            "companies": [
                {
                    "name": "Starbucks",
                    "reason": "Howard Schultz, fondateur et actionnaire principal de Starbucks, est un fervent soutien d'Israël qui investit massivement dans l'économie israélienne, notamment un récent investissement de 1,7 milliard de dollars dans la startup de cybersécurité Wiz.",
                    "action": "Ne pas acheter de produits Starbucks. Ne pas vendre de produits Starbucks. Ne pas travailler pour Starbucks.",
                    "alternatives": ["Caffe Nero", "Cafés indépendants locaux", "Cafés arabes locaux"]
                },
                {
                    "name": "Coca-Cola",
                    "reason": "Coca-Cola possède une usine d'embouteillage dans la zone industrielle d'Atarot, une colonie israélienne illégale à Jérusalem-Est occupée. L'entreprise continue de soutenir l'économie israélienne malgré les violations des droits humains.",
                    "action": "Boycotter tous les produits Coca-Cola, y compris Sprite, Fanta et autres marques associées.",
                    "alternatives": ["Marques de boissons locales", "Eau gazeuse maison", "Jus naturels"]
                },
                {
                    "name": "McDonald's",
                    "reason": "McDonald's Israël a fourni des milliers de repas gratuits aux soldats israéliens pendant les opérations militaires à Gaza. La franchise israélienne a ouvertement soutenu les actions militaires contre les Palestiniens.",
                    "action": "Ne pas manger chez McDonald's.",
                    "alternatives": ["Restaurants locaux", "Chaînes de restauration rapide locales"]
                },
                {
                    "name": "Nestlé",
                    "reason": "Nestlé opère en Israël depuis 1995 et possède des installations de production dans des zones contestées. L'entreprise a été critiquée pour son exploitation des ressources en eau palestiniennes.",
                    "action": "Éviter les produits Nestlé, y compris l'eau en bouteille, les céréales et les produits laitiers.",
                    "alternatives": ["Marques locales", "Produits artisanaux", "Eau du robinet filtrée"]
                },
                {
                    "name": "PepsiCo",
                    "reason": "PepsiCo opère en Israël et a des installations dans des territoires contestés. L'entreprise continue ses activités malgré les appels au boycott.",
                    "action": "Éviter tous les produits PepsiCo, y compris les chips Lay's, Doritos, et les boissons Pepsi.",
                    "alternatives": ["Boissons locales", "Snacks de fabrication locale"]
                },
                {
                    "name": "Sabra Hummus",
                    "reason": "Sabra est une coentreprise entre PepsiCo et le Groupe Strauss, une entreprise israélienne qui fournit des soutiens aux unités d'élite de l'armée israélienne impliquées dans des violations des droits humains.",
                    "action": "Ne pas acheter de houmous Sabra.",
                    "alternatives": ["Houmous fait maison", "Marques arabes locales de houmous"]
                }
            ]
        },
        "Technology": {
            "companies": [
                {
                    "name": "HP (Hewlett-Packard)",
                    "reason": "HP fournit des technologies utilisées dans le système de contrôle et de surveillance d'Israël, notamment pour les points de contrôle militaires. Ses technologies sont utilisées pour maintenir le système d'apartheid et de ségrégation.",
                    "action": "Ne pas acheter de produits HP, y compris les ordinateurs, imprimantes et fournitures.",
                    "alternatives": ["Lenovo", "Brother", "Epson", "Marques asiatiques"]
                },
                {
                    "name": "Microsoft",
                    "reason": "Microsoft a investi 1,5 milliard de dollars dans une entreprise israélienne d'IA et possède un important centre de R&D en Israël. L'entreprise collabore étroitement avec l'armée israélienne pour le développement de technologies militaires.",
                    "action": "Utiliser des alternatives open source dans la mesure du possible.",
                    "alternatives": ["Linux", "LibreOffice", "Alternatives open source"]
                },
                {
                    "name": "Google",
                    "reason": "Google a signé un contrat de cloud computing de 1,2 milliard de dollars avec le gouvernement israélien (Projet Nimbus). Cette technologie est utilisée pour la surveillance et le ciblage des Palestiniens.",
                    "action": "Utiliser des moteurs de recherche et des services alternatifs.",
                    "alternatives": ["DuckDuckGo", "ProtonMail", "Firefox"]
                },
                {
                    "name": "Apple",
                    "reason": "Apple a d'importants investissements en Israël et collabore avec des entreprises israéliennes impliquées dans la surveillance et la technologie militaire.",
                    "action": "Envisager des alternatives aux produits Apple.",
                    "alternatives": ["Samsung", "Xiaomi", "Huawei", "Téléphones Android"]
                },
                {
                    "name": "Intel",
                    "reason": "Intel est l'un des plus grands employeurs dans le secteur technologique israélien avec plusieurs usines et centres de R&D. L'entreprise contribue significativement à l'économie israélienne.",
                    "action": "Privilégier les processeurs AMD lorsque possible.",
                    "alternatives": ["AMD", "ARM", "Autres fabricants de processeurs"]
                }
            ]
        },
        "Fashion & Clothing": {
            "companies": [
                {
                    "name": "Puma",
                    "reason": "Puma sponsorise l'Association israélienne de football, qui inclut des équipes dans des colonies illégales. Ce soutien légitime l'occupation et les violations du droit international.",
                    "action": "Ne pas acheter de produits Puma.",
                    "alternatives": ["Adidas", "New Balance", "Marques locales", "Li-Ning"]
                },
                {
                    "name": "Skechers",
                    "reason": "Skechers possède des magasins dans des colonies israéliennes illégales et maintient des partenariats commerciaux en Israël, contribuant à l'économie de l'occupation.",
                    "action": "Boycotter les chaussures et vêtements Skechers.",
                    "alternatives": ["Brooks", "ASICS", "Marques éthiques"]
                },
                {
                    "name": "H&M",
                    "reason": "H&M opère des magasins en Israël, y compris dans des zones contestées. L'entreprise a ignoré les appels à cesser ses activités dans les territoires occupés.",
                    "action": "Ne pas faire ses achats chez H&M.",
                    "alternatives": ["Marques de mode éthiques", "Vêtements d'occasion"]
                },
                {
                    "name": "Zara",
                    "reason": "Zara possède des magasins en Israël et s'approvisionne auprès de fournisseurs israéliens. La marque a été critiquée pour son manque de position éthique concernant l'occupation.",
                    "action": "Éviter de faire ses achats chez Zara.",
                    "alternatives": ["Marques locales", "Boutiques indépendantes"]
                },
                {
                    "name": "Victoria's Secret",
                    "reason": "Victoria's Secret est détenue par L Brands, qui a des investissements significatifs en Israël et des magasins dans des zones contestées.",
                    "action": "Boycotter les produits Victoria's Secret.",
                    "alternatives": ["Marques de lingerie éthiques", "Marques locales"]
                }
            ]
        },
        "Cosmetics": {
            "companies": [
                {
                    "name": "L'Oréal",
                    "reason": "L'Oréal opère en Israël et a acquis des entreprises cosmétiques israéliennes. L'entreprise a des installations dans des territoires contestés et bénéficie de l'occupation.",
                    "action": "Boycotter les produits L'Oréal et ses marques associées.",
                    "alternatives": ["The Body Shop", "Lush", "Marques naturelles", "Cosmétiques halal"]
                },
                {
                    "name": "Estée Lauder",
                    "reason": "Le président d'Estée Lauder, Ronald Lauder, est un fervent soutien d'Israël et finance des organisations pro-israéliennes. Il a publiquement défendu les actions militaires israéliennes contre les Palestiniens.",
                    "action": "Ne pas acheter de produits Estée Lauder et ses marques associées.",
                    "alternatives": ["Marques de cosmétiques éthiques", "Produits naturels"]
                },
                {
                    "name": "Yves Saint Laurent Beauty / YSL Beauty",
                    "reason": "YSL Beauty appartient au Groupe L'Oréal, qui opère en Israël et a des liens avec des entreprises israéliennes impliquées dans l'occupation.",
                    "action": "Éviter les produits YSL Beauty.",
                    "alternatives": ["Marques de cosmétiques éthiques", "Produits naturels"]
                },
                {
                    "name": "Garnier",
                    "reason": "Garnier est une filiale de L'Oréal qui a fourni des produits gratuits aux soldats israéliens pendant les opérations militaires à Gaza.",
                    "action": "Ne pas acheter de produits Garnier.",
                    "alternatives": ["Produits capillaires naturels", "Marques locales"]
                }
            ]
        },
        "Finance": {
            "companies": [
                {
                    "name": "eToro",
                    "reason": "eToro est une entreprise israélienne de trading en ligne qui soutient l'économie israélienne et contribue aux taxes qui financent l'occupation.",
                    "action": "Utiliser d'autres plateformes de trading et d'investissement.",
                    "alternatives": ["Plateformes de trading alternatives", "Banques éthiques"]
                },
                {
                    "name": "PayPal",
                    "reason": "PayPal opère en Israël mais refuse de fournir ses services aux Palestiniens dans les territoires occupés, créant une discrimination économique flagrante.",
                    "action": "Utiliser des alternatives à PayPal dans la mesure du possible.",
                    "alternatives": ["Wise", "Services bancaires locaux", "Virement bancaire"]
                },
                {
                    "name": "Citibank",
                    "reason": "Citibank a d'importants investissements en Israël et finance des projets dans les territoires occupés, contribuant à l'expansion des colonies illégales.",
                    "action": "Éviter d'utiliser les services de Citibank.",
                    "alternatives": ["Banques locales", "Coopératives de crédit", "Banques éthiques"]
                }
            ]
        },
        "Other": {
            "companies": [
                {
                    "name": "SodaStream",
                    "reason": "SodaStream a exploité une usine dans une colonie israélienne illégale en Cisjordanie occupée avant de déménager suite à des pressions. L'entreprise continue de bénéficier de politiques discriminatoires.",
                    "action": "Ne pas acheter de produits SodaStream.",
                    "alternatives": ["Eau gazeuse en bouteille", "Autres systèmes de carbonatation"]
                },
                {
                    "name": "Volvo Heavy Machinery",
                    "reason": "Les équipements lourds Volvo sont utilisés pour démolir des maisons palestiniennes et construire des colonies illégales. Ces machines sont des outils essentiels de l'occupation.",
                    "action": "Sensibiliser à l'utilisation des équipements Volvo dans les territoires occupés.",
                    "alternatives": ["Autres fabricants d'équipements lourds"]
                },
                {
                    "name": "Caterpillar",
                    "reason": "Les bulldozers Caterpillar sont utilisés pour démolir des maisons palestiniennes et construire le mur de séparation illégal. Ces machines sont spécialement modifiées pour les démolitions militaires.",
                    "action": "Boycotter les produits Caterpillar et sensibiliser à leur utilisation.",
                    "alternatives": ["Autres fabricants d'équipements de construction"]
                },
                {
                    "name": "Airbnb",
                    "reason": "Airbnb liste des propriétés dans des colonies israéliennes illégales en territoire palestinien occupé, légitimant ainsi l'occupation et profitant des terres volées.",
                    "action": "Ne pas utiliser Airbnb pour vos réservations de voyage.",
                    "alternatives": ["Booking.com (avec vigilance)", "Hôtels locaux", "Auberges indépendantes"]
                },
                {
                    "name": "TripAdvisor",
                    "reason": "TripAdvisor promeut des attractions touristiques dans des colonies illégales sans mentionner leur statut illégal selon le droit international.",
                    "action": "Éviter d'utiliser TripAdvisor, particulièrement pour des voyages au Moyen-Orient.",
                    "alternatives": ["Guides de voyage indépendants", "Recommandations locales"]
                }
            ]
        }
    }
    
    return boycott_data

# Function to get educational resources about Palestine
def get_educational_resources():
    resources = {
        "Histoire": [
            {
                "title": "La Nakba : L'exode palestinien de 1948",
                "description": "La Nakba (catastrophe en arabe) fait référence à l'expulsion massive et à la dépossession des Palestiniens lors de la création de l'État d'Israël en 1948. Plus de 750 000 Palestiniens ont été forcés de quitter leurs foyers, et plus de 500 villages palestiniens ont été détruits.",
                "sources": ["Institut d'études palestiniennes", "Archives de l'ONU", "Témoignages de survivants"],
                "key_facts": [
                    "Plus de 750 000 Palestiniens déplacés",
                    "Plus de 500 villages palestiniens détruits",
                    "Confiscation de 78% des terres palestiniennes historiques",
                    "Création de la plus longue crise de réfugiés non résolue au monde"
                ]
            },
            {
                "title": "L'occupation de 1967 et ses conséquences",
                "description": "En juin 1967, Israël a occupé la Cisjordanie, Jérusalem-Est, la bande de Gaza, le plateau du Golan et la péninsule du Sinaï lors de la guerre des Six Jours. Cette occupation, qui se poursuit aujourd'hui (sauf pour le Sinaï), a entraîné l'expansion des colonies israéliennes illégales et un système de contrôle militaire sur la population palestinienne.",
                "sources": ["Nations Unies", "B'Tselem", "Human Rights Watch"],
                "key_facts": [
                    "Plus de 600 000 colons israéliens vivent illégalement en Cisjordanie et à Jérusalem-Est",
                    "Plus de 60% de la Cisjordanie est sous contrôle total israélien (Zone C)",
                    "Plus de 700 km de mur de séparation, déclaré illégal par la Cour internationale de Justice",
                    "Plus de 65 résolutions de l'ONU condamnant l'occupation, toutes ignorées par Israël"
                ]
            },
            {
                "title": "Les accords d'Oslo et l'échec du processus de paix",
                "description": "Les accords d'Oslo, signés en 1993-1995, étaient censés mener à une solution à deux États dans un délai de cinq ans. Cependant, ils ont échoué en raison de l'expansion continue des colonies israéliennes, des violations des accords et de l'absence de volonté politique pour résoudre les questions fondamentales comme Jérusalem, les réfugiés et les frontières.",
                "sources": ["Documents des accords d'Oslo", "Nations Unies", "Analyses diplomatiques"],
                "key_facts": [
                    "Division de la Cisjordanie en zones A, B et C avec différents niveaux de contrôle",
                    "Création de l'Autorité palestinienne comme gouvernement intérimaire",
                    "Triplement du nombre de colons israéliens depuis les accords d'Oslo",
                    "Fragmentation territoriale rendant un État palestinien viable de plus en plus impossible"
                ]
            },
            {
                "title": "Le blocus de Gaza depuis 2007",
                "description": "Depuis 2007, la bande de Gaza est soumise à un blocus terrestre, aérien et maritime imposé par Israël et l'Égypte. Ce blocus a créé une crise humanitaire catastrophique, limitant l'accès à la nourriture, aux médicaments, à l'électricité et à l'eau potable pour plus de 2 millions de Palestiniens vivant dans cette enclave côtière.",
                "sources": ["UNRWA", "OMS", "OCHA", "Oxfam"],
                "key_facts": [
                    "Plus de 2 millions de personnes vivent dans une zone de 365 km²",
                    "Plus de 95% de l'eau est impropre à la consommation",
                    "Taux de chômage dépassant 45%, l'un des plus élevés au monde",
                    "Électricité disponible seulement 4-12 heures par jour en moyenne",
                    "Plus de 80% de la population dépend de l'aide humanitaire"
                ]
            }
        ],
        "Droits humains": [
            {
                "title": "Le système d'apartheid en Palestine occupée",
                "description": "De nombreuses organisations de défense des droits humains, dont Amnesty International, Human Rights Watch et B'Tselem, ont conclu qu'Israël pratique l'apartheid contre les Palestiniens. Ce système comprend des lois discriminatoires, la ségrégation territoriale, les restrictions de mouvement, et l'allocation inégale des ressources.",
                "sources": ["Amnesty International", "Human Rights Watch", "B'Tselem", "Al-Haq"],
                "key_facts": [
                    "Deux systèmes juridiques distincts en Cisjordanie: droit civil pour les colons, droit militaire pour les Palestiniens",
                    "Plus de 65 lois discriminatoires contre les citoyens palestiniens d'Israël",
                    "Système de permis complexe limitant la liberté de mouvement des Palestiniens",
                    "Accès inégal à l'eau: les colons reçoivent 3 à 5 fois plus d'eau que les Palestiniens"
                ]
            },
            {
                "title": "Détention administrative et prisonniers politiques",
                "description": "Israël utilise largement la détention administrative pour emprisonner des Palestiniens sans inculpation ni procès, sur la base de 'preuves secrètes'. Des milliers de Palestiniens, y compris des enfants, sont détenus dans des conditions qui violent souvent le droit international.",
                "sources": ["Addameer", "Comité international de la Croix-Rouge", "UNICEF"],
                "key_facts": [
                    "Plus de 800 000 Palestiniens détenus depuis 1967",
                    "Environ 500-700 enfants palestiniens arrêtés chaque année",
                    "Taux de condamnation de 99,7% devant les tribunaux militaires israéliens",
                    "Torture et mauvais traitements systématiques documentés par les organisations de droits humains"
                ]
            },
            {
                "title": "Restrictions à la liberté de mouvement",
                "description": "Les Palestiniens font face à un système complexe de restrictions de mouvement comprenant des checkpoints, le mur de séparation, des routes réservées aux colons, et un système de permis qui limite sévèrement leur capacité à se déplacer librement sur leur propre territoire.",
                "sources": ["OCHA", "B'Tselem", "Machsom Watch"],
                "key_facts": [
                    "Plus de 700 obstacles physiques en Cisjordanie (checkpoints, barrières routières, etc.)",
                    "Le mur de séparation s'étend sur 712 km, dont 85% à l'intérieur de la Cisjordanie",
                    "Des milliers de Palestiniens séparés de leurs terres agricoles par le mur",
                    "Système de permis complexe nécessaire pour entrer à Jérusalem-Est, voyager entre Gaza et la Cisjordanie, ou accéder aux 'zones de jointure'"
                ]
            },
            {
                "title": "Démolitions de maisons et déplacements forcés",
                "description": "Israël pratique régulièrement la démolition de maisons palestiniennes, soit comme mesure punitive, soit sous prétexte d'absence de permis de construire (qui sont systématiquement refusés aux Palestiniens). Ces pratiques constituent des violations graves du droit international humanitaire.",
                "sources": ["OCHA", "B'Tselem", "Al-Haq", "Norwegian Refugee Council"],
                "key_facts": [
                    "Plus de 55 000 maisons palestiniennes démolies depuis 1967",
                    "Moins de 2% des demandes de permis de construire approuvées pour les Palestiniens en Zone C",
                    "Jérusalem-Est particulièrement ciblée pour les démolitions et l'expansion des colonies",
                    "Politique de 'transfert silencieux' visant à réduire la présence palestinienne dans certaines zones stratégiques"
                ]
            }
        ],
        "Culture et société": [
            {
                "title": "Patrimoine culturel palestinien",
                "description": "La culture palestinienne est riche et diverse, avec des traditions remontant à des milliers d'années. Elle comprend une cuisine distinctive, des arts traditionnels comme la broderie, la poterie et la calligraphie, ainsi qu'une riche tradition littéraire et musicale.",
                "sources": ["Institut du monde arabe", "Musée palestinien", "UNESCO"],
                "key_facts": [
                    "La broderie palestinienne (tatreez) est inscrite au patrimoine culturel immatériel de l'UNESCO",
                    "L'olivier est un symbole central de l'identité et de la résistance palestiniennes",
                    "La dabke est une danse traditionnelle pratiquée lors des célébrations",
                    "La poésie de résistance est une forme d'expression culturelle importante, avec des poètes comme Mahmoud Darwich"
                ]
            },
            {
                "title": "Diaspora palestinienne",
                "description": "Suite à la Nakba de 1948 et à l'occupation continue, une importante diaspora palestinienne s'est formée à travers le monde. Ces communautés maintiennent des liens forts avec leur patrie et jouent un rôle crucial dans la préservation de l'identité palestinienne et la défense des droits des Palestiniens.",
                "sources": ["UNRWA", "Institut d'études palestiniennes", "Badil"],
                "key_facts": [
                    "Plus de 7 millions de réfugiés et déplacés palestiniens dans le monde",
                    "Importantes communautés palestiniennes en Jordanie, Liban, Syrie, Chili et États-Unis",
                    "La clé (miftah) est un symbole du droit au retour des réfugiés",
                    "Transmission intergénérationnelle de la mémoire et de l'identité palestiniennes"
                ]
            },
            {
                "title": "Résistance culturelle et artistique",
                "description": "Face à l'occupation, les Palestiniens ont développé diverses formes de résistance culturelle et artistique. L'art, la musique, la littérature et le cinéma palestiniens servent à préserver l'identité nationale, documenter les réalités de l'occupation et exprimer les aspirations à la liberté et à l'autodétermination.",
                "sources": ["Festival du film palestinien", "Dar Yusuf Nasri Jacir pour l'Art et la Recherche", "Institut Edward Said"],
                "key_facts": [
                    "Émergence d'un cinéma palestinien reconnu internationalement (Elia Suleiman, Hany Abu-Assad)",
                    "Street art et graffiti sur le mur de séparation comme forme de protestation visuelle",
                    "Développement de festivals culturels comme Palest'In & Out et le Festival de littérature palestinienne",
                    "Utilisation des médias sociaux pour documenter et partager les réalités de l'occupation"
                ]
            },
            {
                "title": "Éducation et résistance académique",
                "description": "Malgré les obstacles imposés par l'occupation, les Palestiniens accordent une grande valeur à l'éducation. Les universités palestiniennes sont des centres de production de connaissances et de résistance intellectuelle, bien qu'elles soient souvent ciblées par les forces israéliennes.",
                "sources": ["Université de Birzeit", "Right to Education Campaign", "PACBI"],
                "key_facts": [
                    "Taux d'alphabétisation parmi les plus élevés du monde arabe malgré l'occupation",
                    "Universités palestiniennes régulièrement soumises à des raids, fermetures et restrictions",
                    "Développement des études palestiniennes comme discipline académique",
                    "Mouvement de boycott académique contre les institutions complices de l'occupation"
                ]
            }
        ],
        "Résistance et solidarité": [
            {
                "title": "Le mouvement BDS (Boycott, Désinvestissement, Sanctions)",
                "description": "Lancé en 2005 par la société civile palestinienne, le mouvement BDS appelle à des mesures non-violentes pour faire pression sur Israël afin qu'il respecte le droit international et les droits des Palestiniens. Inspiré par le mouvement anti-apartheid sud-africain, il a gagné un soutien mondial significatif.",
                "sources": ["Comité national BDS", "Campagne palestinienne pour le boycott académique et culturel d'Israël (PACBI)"],
                "key_facts": [
                    "Trois demandes principales: fin de l'occupation, égalité pour les Palestiniens citoyens d'Israël, droit au retour des réfugiés",
                    "Succès notables incluant le désinvestissement de fonds de pension et d'universités",
                    "Soutenu par des syndicats, églises, mouvements sociaux et personnalités du monde entier",
                    "Cible les institutions complices de l'occupation, non les individus"
                ]
            },
            {
                "title": "Résistance populaire non-violente",
                "description": "Les Palestiniens ont une longue tradition de résistance populaire non-violente contre l'occupation, incluant des manifestations pacifiques, des sit-ins, et des actions directes non-violentes. Ces mouvements sont souvent réprimés violemment par les forces israéliennes.",
                "sources": ["Popular Struggle Coordination Committee", "Stop the Wall Campaign", "Al-Haq"],
                "key_facts": [
                    "Villages comme Bil'in, Ni'lin et Nabi Saleh connus pour leurs manifestations hebdomadaires contre le mur",
                    "Utilisation de la documentation vidéo et des médias sociaux pour exposer les violations",
                    "Participation internationale via des mouvements comme l'International Solidarity Movement",
                    "Répression systématique incluant arrestations, détentions et parfois tirs à balles réelles contre manifestants non armés"
                ]
            },
            {
                "title": "Solidarité internationale",
                "description": "Le mouvement de solidarité avec la Palestine s'est développé à l'échelle mondiale, impliquant des organisations de la société civile, des syndicats, des groupes religieux, des étudiants et des militants des droits humains qui soutiennent la lutte palestinienne pour la justice et l'autodétermination.",
                "sources": ["Palestine Solidarity Campaign", "Jewish Voice for Peace", "BDS Movement"],
                "key_facts": [
                    "Journée internationale de solidarité avec le peuple palestinien célébrée le 29 novembre",
                    "Campagnes de désinvestissement dans les universités et institutions religieuses",
                    "Flottilles pour Gaza tentant de briser le blocus maritime",
                    "Mouvements de solidarité incluant des juifs progressistes opposés aux politiques israéliennes"
                ]
            },
            {
                "title": "Reconnaissance internationale de l'État de Palestine",
                "description": "La lutte diplomatique pour la reconnaissance de l'État de Palestine est une forme importante de résistance politique. À ce jour, plus de 140 pays ont reconnu l'État de Palestine, bien que la plupart des puissances occidentales ne l'aient pas encore fait.",
                "sources": ["Nations Unies", "Organisation de libération de la Palestine", "Ministère palestinien des Affaires étrangères"],
                "key_facts": [
                    "En 2012, la Palestine a obtenu le statut d'État observateur non-membre à l'ONU",
                    "Adhésion à diverses organisations internationales, dont la Cour pénale internationale",
                    "Reconnaissance par plus de 140 pays sur 193 États membres de l'ONU",
                    "Campagnes continues pour la reconnaissance par les pays occidentaux"
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
                "DuckDuckGo au lieu de Google Search", 
                "Huawei/Samsung au lieu d'Apple", 
                "Linux/Ubuntu au lieu de Windows", 
                "Telegram/Signal au lieu de WhatsApp", 
                "AliExpress/eBay au lieu d'Amazon", 
                "AMD au lieu d'Intel", 
                "Lenovo/Acer au lieu de HP", 
                "LibreOffice au lieu de Microsoft Office",
                "ProtonMail au lieu de Gmail",
                "Firefox/Brave au lieu de Chrome"
            ]
        },
        "Food & Beverage": {
            "Companies": [
                "McDonald's", "Coca-Cola", "PepsiCo", "Nestlé", "Starbucks", "Burger King", "Domino's Pizza",
                "KFC", "Pizza Hut", "Subway", "Heinz", "Danone", "Mars", "Mondelez (Oreo)", "Kellogg's", 
                "Häagen-Dazs", "Sabra Hummus", "Strauss Group"
            ],
            "Alternatives": [
                "Restaurants de burgers locaux au lieu de McDonald's/Burger King", 
                "Cafés locaux au lieu de Starbucks", 
                "Eau locale ou jus au lieu de Coca-Cola/Pepsi", 
                "Boulangeries locales au lieu des chaînes de restauration",
                "Produits laitiers locaux au lieu de Danone/Nestlé",
                "Chocolat et snacks locaux au lieu de Mars/Mondelez"
            ]
        },
        "Fashion & Retail": {
            "Companies": [
                "H&M", "Zara", "Puma", "Nike", "Adidas", "Victoria's Secret", "Calvin Klein", "Tommy Hilfiger",
                "Marks & Spencer", "ASOS", "Skechers", "The North Face", "Timberland", "Levi's", "Gap", "Old Navy",
                "Ralph Lauren", "Lacoste", "Hugo Boss", "Uniqlo"
            ],
            "Alternatives": [
                "Marques de vêtements locales", 
                "Marques de mode éthiques", 
                "Achats de seconde main/friperies", 
                "Li-Ning/Anta Sports au lieu de Nike/Adidas",
                "Decathlon pour l'équipement sportif",
                "Fabricants de chaussures locaux"
            ]
        },
        "Entertainment & Media": {
            "Companies": [
                "Disney", "Warner Bros", "Netflix", "Spotify", "Universal Music Group",
                "Fox", "Paramount", "Sony Pictures", "MGM", "DreamWorks", "NBC Universal",
                "CNN", "BBC", "New York Times", "The Washington Post", "The Guardian"
            ],
            "Alternatives": [
                "Services de streaming indépendants", 
                "Productions cinématographiques locales", 
                "YouTube pour les créateurs de contenu indépendants",
                "Anghami au lieu de Spotify dans les régions arabes",
                "Sources d'information indépendantes et journalistes",
                "Al Jazeera, TRT World pour les actualités"
            ]
        },
        "Sports": {
            "Companies": [
                "Puma", "Nike", "Adidas", "Under Armour", "New Balance", "Reebok",
                "Wilson", "Spalding", "Gatorade", "Fitbit", "Garmin"
            ],
            "Alternatives": [
                "Li-Ning", "Anta Sports", "Asics", "Fila", "Mizuno",
                "Fabricants locaux d'équipements sportifs",
                "Applications de fitness indépendantes au lieu de celles des grandes entreprises"
            ]
        },
        "Cosmetics & Personal Care": {
            "Companies": [
                "L'Oréal", "Estée Lauder", "Clinique", "MAC Cosmetics", "Revlon", "Maybelline",
                "Garnier", "Dove", "Nivea", "Johnson & Johnson", "Colgate-Palmolive", "Procter & Gamble"
            ],
            "Alternatives": [
                "Marques locales de cosmétiques naturels", 
                "Marques de cosmétiques halal", 
                "Alternatives éthiques et sans cruauté",
                "Savons artisanaux et produits naturels"
            ]
        },
        "Travel & Hospitality": {
            "Companies": [
                "Airbnb", "Booking.com", "Expedia", "TripAdvisor", "Marriott", "Hilton",
                "InterContinental", "Hyatt", "Delta Airlines", "American Airlines", "United Airlines"
            ],
            "Alternatives": [
                "Réservations directes auprès des hôtels", 
                "Agences de voyage locales", 
                "Plateformes alternatives d'hébergement",
                "Compagnies aériennes locales quand c'est possible"
            ]
        }
    }
    return companies

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
    .main-button {
        background-color: #1f77b4;
        color: white;
        border-radius: 10px;
        padding: 15px 25px;
        font-weight: bold;
        margin: 10px 0;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s;
    }
    .main-button:hover {
        background-color: #145a8d;
        transform: translateY(-2px);
    }
    .resource-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #1f77b4;
    }
    .resource-title {
        color: #1f77b4;
        font-size: 1.3em;
        margin-bottom: 10px;
    }
    .resource-description {
        margin-bottom: 15px;
        line-height: 1.6;
    }
    .resource-facts {
        background-color: #f0f7fb;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .resource-sources {
        font-style: italic;
        color: #666;
        font-size: 0.9em;
    }
    .fact-item {
        margin-bottom: 5px;
        padding-left: 20px;
        position: relative;
    }
    .fact-item:before {
        content: "•";
        position: absolute;
        left: 0;
        color: #1f77b4;
    }
    .section-title {
        color: #1f77b4;
        font-size: 2em;
        margin: 30px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #e6e6e6;
    }
    .subsection-title {
        color: #333;
        font-size: 1.5em;
        margin: 25px 0 15px 0;
    }
    .chat-container {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/0/00/Flag_of_Palestine.svg", width=250)
        st.title("Palestine AI")
        
        # Team Section
        with st.expander("Notre Équipe", expanded=False):
            st.markdown("### Elkalem-Imrou Height School")
            st.markdown("En collaboration avec Erinov Company")
            st.markdown("#### Membres de l'équipe:")
            
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
        
        # Navigation buttons for main area
        st.markdown("### Navigation")
        
        # Create session state variables if they don't exist
        if 'show_chat' not in st.session_state:
            st.session_state.show_chat = True
        if 'show_boycott' not in st.session_state:
            st.session_state.show_boycott = False
        if 'show_education' not in st.session_state:
            st.session_state.show_education = False
        
        # Button to show chat
        if st.button("💬 Discuter avec l'IA"):
            st.session_state.show_chat = True
            st.session_state.show_boycott = False
            st.session_state.show_education = False
        
        # Button to show boycott information
        if st.button("🚫 Informations sur le Boycott"):
            st.session_state.show_chat = False
            st.session_state.show_boycott = True
            st.session_state.show_education = False
        
        # Button to show educational resources
        if st.button("📚 Ressources Éducatives"):
            st.session_state.show_chat = False
            st.session_state.show_boycott = False
            st.session_state.show_education = True
        
        # Help Section
        with st.expander("Aide", expanded=True):
            st.markdown("### Comment utiliser l'application")
            st.markdown("""
            - Poser des questions : Vous pouvez poser n'importe quelle question liée à l'histoire de la Palestine, aux événements actuels ou aux questions humanitaires.
            - Multilinguisme : Vous pouvez poser des questions dans n'importe quelle langue.
            - Mode sombre : Pour passer en mode sombre, allez dans Paramètres > Choisir le thème de l'application > Mode sombre.
            - Fonctionnalités de l'application :
              - Réponses approfondies axées uniquement sur la Palestine.
              - Réponses contextuelles adaptées à votre question.
              - Informations précises et détaillées soutenues par l'IA.
              - Ressources éducatives : Accédez à des informations fiables sur la Palestine.
              - Informations sur le boycott : Découvrez les entreprises qui soutiennent Israël et les alternatives.
            """)
        st.markdown("---")
        
        # About Us Section
        with st.expander("À propos", expanded=False):
            st.markdown("#### Palestine AI Chat")
            st.markdown("Cette application a été développée pour fournir des informations approfondies sur la cause palestinienne, alimentées par l'IA.")
            st.markdown("""
            Version: 1.2.0
            
            #### Fonctionnalités
            - Informations sur la Palestine alimentées par l'IA
            - Focus sur l'histoire, les questions humanitaires et les événements actuels
            - Support multilingue
            - Réponses précises et contextuelles
            - Informations sur le boycott et ressources de soutien
            - Ressources éducatives
            
            © 2025 Palestine AI Team. Tous droits réservés.
            
            [Contactez-nous](mailto:your-email@example.com?subject=Palestine%20Info%20Bot%20Inquiry&body=Dear%20Palestine%20Info%20Bot%20Team,%0A%0AWe%20are%20writing%20to%20inquire%20about%20[your%20inquiry]%2C%20specifically%20[details%20of%20your%20inquiry].%0A%0A[Provide%20additional%20context%20and%20details%20here].%0A%0APlease%20let%20us%20know%20if%20you%20require%20any%20further%20information%20from%20our%20end.%0A%0ASincerely,%0A[Your%20Company%20Name]%0A[Your%20Name]%0A[Your%20Title]%0A[Your%20Phone%20Number]%0A[Your%20Email%20Address])
            """)

    # Main content area
    st.title("Palestine AI - De la rivière à la mer")

    # Quote of the Day section in a professional style
    st.markdown("""
    <div class="quote-box">
        "La question de la Palestine est une épreuve par laquelle Dieu a testé votre conscience, votre détermination, votre richesse et votre unité."
    </div>
    <div class="quote-author">
        — Al-Bashir Al-Ibrahimi
    </div>
    """, unsafe_allow_html=True)

    # Information cards in a grid layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Contexte historique
        La Palestine est une terre avec une histoire profondément enracinée s'étendant sur des milliers d'années, et les documents historiques affirment que le peuple palestinien est le propriétaire légitime de cette terre. La Palestine a été le foyer de sa population autochtone, qui a préservé sa présence et sa culture malgré les tentatives d'effacement et de déplacement à travers les âges.
        """)
    
    with col2:
        st.markdown("""
        ### Situation actuelle
        Le peuple palestinien continue de faire face à de graves défis humanitaires en raison de l'occupation continue et du blocus, particulièrement dans la bande de Gaza, où les résidents sont privés d'accès aux ressources et services essentiels. Ces actions constituent des violations flagrantes des droits humains et du droit international, qui garantissent le droit des peuples à vivre librement et avec dignité dans leur patrie.
        """)

    # Display content based on session state
    if st.session_state.show_chat:
        st.markdown("<div class='section-title'>Discuter avec l'IA sur la Palestine</div>", unsafe_allow_html=True)
        
        # User input section with enhanced styling
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        st.markdown("### Posez votre question")
        st.markdown("Obtenez des informations précises et détaillées sur l'histoire de la Palestine, les événements actuels et les questions humanitaires.")
        
        user_question = st.text_input("", placeholder="Tapez votre question sur la Palestine ici...", key="text_question")
        
        # Add a submit button for better UX
        submit_button = st.button("Obtenir une réponse")

        # Process the question when submitted
        if user_question and submit_button:
            # Check if the question is related to Palestine
            is_palestine = is_palestine_related(user_question)
            
            with st.spinner("Génération d'une réponse complète..."):
                answer = ask_about_palestine(user_question)
                
                # Create a container with better styling for the answer
                answer_container = st.container()
                with answer_container:
                    st.markdown("<div style='background-color: #f0f7fb; padding: 20px; border-radius: 10px; border-left: 5px solid #1f77b4;'>", unsafe_allow_html=True)
                    # Typing effect for response
                    with st.empty():  # Create an empty placeholder to display the typing effect
                        typing_effect(answer)
                    st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif st.session_state.show_boycott:
        st.markdown("<div class='section-title'>Informations sur le Boycott</div>", unsafe_allow_html=True)
        
        st.markdown("""
        Le mouvement de boycott vise à exercer une pression économique et politique sur Israël pour qu'il se conforme au droit international et respecte les droits des Palestiniens. 
        Cette forme de résistance non-violente s'inspire du mouvement anti-apartheid sud-africain et a gagné un soutien mondial significatif.
        
        Voici une liste détaillée des entreprises qui soutiennent Israël, avec des explications sur leurs implications et des alternatives que vous pouvez utiliser à la place.
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
                        <div class="company-action">Action recommandée: {company['action']}</div>
                        <div class="company-alternatives">
                            <strong>Alternatives:</strong> {', '.join(company['alternatives'])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("""
        ### Comment soutenir Gaza
        
        1. **Boycotter les produits**: Évitez d'acheter des produits des entreprises qui soutiennent Israël
        2. **Choisir des alternatives**: Utilisez les alternatives suggérées ou trouvez des options locales
        3. **Sensibiliser**: Partagez des informations sur la situation à Gaza
        4. **Faire des dons**: Soutenez les organisations humanitaires travaillant à Gaza
        5. **Plaider**: Contactez vos représentants pour exiger des actions
        6. **Participer aux manifestations**: Participez à des manifestations pacifiques
        
        N'oubliez pas que la pression économique par le biais des boycotts a historiquement été une stratégie de résistance non-violente efficace.
        """)
        
        # Add information about the BDS movement
        st.markdown("""
        ### Le mouvement BDS (Boycott, Désinvestissement, Sanctions)
        
        Le mouvement BDS a été lancé en 2005 par la société civile palestinienne. Il appelle à trois actions principales:
        
        1. **Boycott**: Refuser d'acheter des produits et services des entreprises complices de l'occupation
        2. **Désinvestissement**: Retirer les investissements des entreprises et institutions qui profitent de l'occupation
        3. **Sanctions**: Faire pression pour des sanctions contre Israël jusqu'à ce qu'il respecte le droit international
        
        Le mouvement BDS a trois demandes fondamentales:
        1. Mettre fin à l'occupation et à la colonisation de toutes les terres arabes
        2. Reconnaître les droits fondamentaux des citoyens arabes-palestiniens d'Israël à une pleine égalité
        3. Respecter, protéger et promouvoir les droits des réfugiés palestiniens à retourner dans leurs foyers et propriétés
        
        Pour plus d'informations, visitez [le site officiel du mouvement BDS](https://bdsmovement.net/).
        """)
    
    elif st.session_state.show_education:
        st.markdown("<div class='section-title'>Ressources Éducatives sur la Palestine</div>", unsafe_allow_html=True)
        
        st.markdown("""
        Cette section fournit des ressources éducatives pour vous aider à en apprendre davantage sur la Palestine, son histoire, sa culture et sa situation actuelle.
        Les informations présentées ici sont basées sur des sources fiables, notamment des rapports d'organisations de défense des droits humains, des documents des Nations Unies, des études académiques et des témoignages directs.
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
                            <strong>Faits clés:</strong>
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
        ### Lectures et visionnages recommandés
        
        #### Livres
        - **"La Question de Palestine"** par Edward Said
        - **"Palestine: Une histoire moderne"** par Ilan Pappé
        - **"Le Nettoyage ethnique de la Palestine"** par Ilan Pappé
        - **"Gaza en crise"** par Noam Chomsky et Ilan Pappé
        - **"Un Siècle de colonialisme en Palestine"** par Rashid Khalidi
        
        #### Documentaires
        - **"5 Caméras Brisées"** (2011) de Emad Burnat et Guy Davidi
        - **"Le Sel de la mer"** (2008) de Annemarie Jacir
        - **"Gaza Fight for Freedom"** (2019) de Abby Martin
        - **"Occupation 101"** (2006) de Sufyan Omeish et Abdallah Omeish
        - **"The Wanted 18"** (2014) de Amer Shomali et Paul Cowan
        
        #### Sites web fiables
        - [Al Jazeera](https://www.aljazeera.com/palestine-israel-conflict/) - Couverture complète des questions du Moyen-Orient
        - [B'Tselem](https://www.btselem.org/) - Centre d'information israélien pour les droits humains dans les territoires occupés
        - [Institut d'études palestiniennes](https://www.palestine-studies.org/) - Recherche académique sur la Palestine
        - [UNRWA](https://www.unrwa.org/) - Office de secours et de travaux des Nations Unies pour les réfugiés de Palestine
        - [Electronic Intifada](https://electronicintifada.net/) - Actualités, commentaires et analyses sur la Palestine
        """)

    # Footer
    st.markdown("<div class='footer'>Palestine AI - Développé par Elkalem-Imrou Height School en collaboration avec Erinov Company</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
