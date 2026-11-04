import streamlit as st

st.set_page_config(page_title="Agent IA V5", page_icon="💙", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #000a1a; color: white; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #001a4d, #000a1a); }
[data-testid="stSidebar"] * { color: white !important; }
.stChatMessage { background-color: #001133 !important; color: white !important; border: 1px solid #00d4ff; border-radius: 15px; box-shadow: 0 0 15px #00d4ff; }
h1 { color: #00d4ff !important; text-shadow: 0 0 20px #00d4ff, 0 0 40px #0088ff; }
.stChatInput input { background-color: #001133 !important; color: white !important; border: 1px solid #00d4ff !important; }
button { background-color: #00d4ff !important; color: black !important; font-weight: bold !important; border-radius: 12px !important; box-shadow: 0 0 12px #00d4ff; }
button:hover { background-color: #00aaff !important; }
</style>
""", unsafe_allow_html=True)

if "theme" not in st.session_state:
    st.session_state.theme = "Ecole"

THEMES = {
    "📐 Ecole": ["C'est quoi le théorème de Pythagore ?", "Comment calculer la masse volumique ?", "Table de 7", "Toutes les tables de multiplication", "Table de division de 8", "C'est quoi la photosynthese ?", "Conjugue ETRE"],
    "🌍 Capitales": ["Capitale du Japon ?", "Capitale du Bresil ?", "Capitale de l'Egypte ?", "Capitale de la France ?"],
    "✈️ Avions": ["Quel est l'avion de chasse le plus performant ?", "C'est quoi le F-22 ?", "C'est quoi le 【entity-F-35¦canonical_name=F-35】 ?", "C'est quoi le Rafale ?"],
    "💻 PC": ["C'est quoi la meilleure GPU ?", "C'est quoi le meilleur CPU ?", "C'est quoi le meilleur SSD ?", "PC 2000 CHF"],
    "⚽ Foot / Sport": ["C'est qui 【entity-Messi¦canonical_name=Messi】 ?", "C'est qui 【entity-Ronaldo¦canonical_name=Ronaldo】 ?", "C'est qui 【entity-Mbappe¦canonical_name=Mbappe】 ?", "C'est quoi la Coupe du Monde ?"],
    "🎮 Jeux Video": ["C'est quoi 【entity-Minecraft¦canonical_name=Minecraft】 ?", "C'est quoi 【entity-Fortnite¦canonical_name=Fortnite】 ?", "C'est quoi 【entity-Roblox¦canonical_name=Roblox】 ?", "C'est quoi GTA ?"],
    "🚀 Espace": ["C'est quoi un trou noir ?", "C'est quoi le Big Bang ?", "C'est quoi Mars ?"],
    "🧪 Science": ["Comment calculer la masse volumique ?", "C'est quoi un atome ?", "C'est quoi la gravite ?"],
    "🧠 Culture G": ["C'est quoi la Tour Eiffel ?", "C'est quoi les pyramides ?", "C'est quoi le 【entity-Titanic¦canonical_name=Titanic】 ?"],
}

with st.sidebar:
    st.title("💙 Agent IA V5")
    st.write("Clique sur un thème 👇")
    for t in THEMES.keys():
        if st.button(t, key="side_"+t, use_container_width=True):
            st.session_state.theme = t
            st.rerun()
    st.divider()
    if st.button("🗑️ Effacer"):
        st.session_state.messages = []
        st.rerun()

st.title("💙 Agent IA V5")
st.caption("BLEU NEON - Toutes les tables + Tout ce qu'on a dit")

cols = st.columns(3)
for i, t in enumerate(list(THEMES.keys())):
    with cols[i % 3]:
        if st.button(t, key="top_"+t, use_container_width=True):
            st.session_state.theme = t
            st.rerun()

st.subheader(f"Questions {st.session_state.theme} 👇 Clique :")
for q in THEMES[st.session_state.theme]:
    if st.button(q, key="q_"+q, use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": q})
        st.session_state.auto_q = q
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Salut ! 💙 J'ai TOUTES les tables : 1 a 12, multiplications + divisions. Essaie : Table de 7, Toutes les tables, Table de division de 8"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

CAPITALES = {
    "france": "Paris", "suisse": "Berne", "allemagne": "Berlin", "italie": "Rome", "espagne": "Madrid",
    "angleterre": "Londres", "japon": "Tokyo", "usa": "Washington", "canada": "Ottawa", "chine": "Pekin",
    "russie": "Moscou", "bresil": "Brasilia", "inde": "New Delhi", "australie": "Canberra", "egypte": "Le Caire",
    "maroc": "Rabat", "algerie": "Alger", "tunisie": "Tunis", "portugal": "Lisbonne", "belgique": "Bruxelles",
    "pays-bas": "Amsterdam", "autriche": "Vienne", "suede": "Stockholm", "norvege": "Oslo", "danemark": "Copenhague",
    "finlande": "Helsinki", "pologne": "Varsovie", "grece": "Athenes", "turquie": "Ankara", "coree": "Seoul",
    "thailande": "Bangkok", "vietnam": "Hanoi", "mexique": "Mexico", "argentine": "Buenos Aires", "chili": "Santiago",
    "perou": "Lima", "colombie": "Bogota", "kenya": "Nairobi", "nigeria": "Abuja", "islande": "Reykjavik",
    "irlande": "Dublin", "ukraine": "Kyiv", "roumanie": "Bucarest", "hongrie": "Budapest", "croatie": "Zagreb",
    "serbie": "Belgrade", "bulgarie": "Sofia", "israel": "Jerusalem", "liban": "Beyrouth", "irak": "Bagdad",
    "iran": "Teheran", "arabie": "Riyad", "qatar": "Doha", "monaco": "Monaco", "luxembourg": "Luxembourg",
    "malte": "La Valette", "andorre": "Andorre-la-Vieille", "liechtenstein": "Vaduz", "cuba": "La Havane",
    "mali": "Bamako", "senegal": "Dakar", "ghana": "Accra", "cameroun": "Yaounde", "madagascar": "Antananarivo",
    "pakistan": "Islamabad", "nepal": "Katmandou", "mongolie": "Oulan-Bator", "indonesie": "Jakarta",
    "philippines": "Manille", "singapour": "Singapour", "malaisie": "Kuala Lumpur", "nouvelle-zelande": "Wellington",
    "costa rica": "San Jose", "panama": "Panama", "venezuela": "Caracas", "uruguay": "Montevideo",
    "paraguay": "Asuncion", "equateur": "Quito", "bolivie": "Sucre", "haiti": "Port-au-Prince",
    "jamaique": "Kingston", "soudan": "Khartoum", "libye": "Tripoli", "ethiopie": "Addis-Abeba",
}

PC = {
    "meilleure gpu": "MEILLEURE GPU 2026 : 1. RTX 5090 - LA PLUS PUISSANTE, 32 Go, 4K Ultra, 2500 CHF. 2. RTX 5080 - 1200 CHF. 3. RTX 5070 Ti - meilleur rapport, 850 CHF. Pour debuter : RTX 4060, 350 CHF.",
    "gpu": "GPU = Carte Graphique. Elle fait les images / jeux. 【entity-NVIDIA¦canonical_name=NVIDIA】 = RTX, 【entity-AMD¦canonical_name=AMD】 = RX. Meilleure = RTX 5090.",
    "rtx 5090": "RTX 5090 : Plus puissante du monde, 32 Go, 4K Ultra, 2500 CHF.",
    "rtx 5080": "RTX 5080 : 2eme, 16 Go, 4K fluide, 1200 CHF.",
    "rtx 5070": "RTX 5070 Ti : Meilleur pour 2000 CHF, 16 Go, 850 CHF.",
    "rtx 4060": "RTX 4060 : Pour commencer, 8 Go, 【entity-Fortnite¦canonical_name=Fortnite】 144 FPS, 350 CHF.",
    "meilleur cpu": "MEILLEUR CPU 2026 : 1. Ryzen 9 9950X3D - ROI JEUX. 2. 【entity-Intel¦canonical_name=Intel】 Core Ultra 9 285K. 3. Ryzen 7 9800X3D - meilleur rapport jeux.",
    "cpu": "CPU = Processeur, cerveau du PC. 【entity-AMD¦canonical_name=AMD】 Ryzen ou 【entity-Intel¦canonical_name=Intel】 Core. Meilleur jeux = Ryzen 9 9950X3D / Ryzen 7 9800X3D.",
    "meilleur ssd": "MEILLEUR SSD : 1. 【entity-Samsung¦canonical_name=Samsung】 990 PRO 2 To - 7450 Mo/s, PC demarre en 5 sec. 2. WD Black SN850X 2 To - meilleur jeux.",
    "ssd": "SSD = Stocke Windows + jeux. NVMe = plus rapide. 【entity-Samsung¦canonical_name=Samsung】 990 PRO = meilleur. 1 To = 100 CHF.",
    "meilleure ram": "MEILLEURE RAM : 32 Go DDR5 6000 MHz CL30. Parfait pour jouer + streamer + coder. 16 Go = minimum. 64 Go = montage pro.",
    "ram": "RAM = Memoire vive. 16 Go minimum, 32 Go DDR5 parfait en 2026.",
    "meilleur pc": "MEILLEUR PC : RTX 5090 + Ryzen 9 9950X3D + 32 Go DDR5 + SSD 990 PRO 2 To + Alim 1000W = 4000 CHF, tout en 4K Ultra.",
    "pc 2000": "PC 2000 CHF PARFAIT : RTX 5070 Ti (850) + Ryzen 7 9800X3D (450) + RAM 32 Go DDR5 (120) + SSD 990 PRO 2 To (180) + Carte mere B850 (180) + Alim 850W Gold (110) + Boitier (110) = 2000 CHF. Fortnite 240 FPS !",
    "budget 2000": "PC 2000 CHF : RTX 5070 Ti + Ryzen 7 9800X3D + 32 Go + SSD 2 To + Alim 850W = 2000 CHF. Fortnite 240 FPS !",
    "2000": "PC 2000 CHF : RTX 5070 Ti + Ryzen 7 9800X3D + 32 Go + SSD 2 To = 2000 CHF. Fortnite 240 FPS !",
    "ecran": "MEILLEUR ECRAN : 27 pouces 1440p 180Hz IPS = parfait. 1080p 144Hz = pas cher. 4K 240Hz OLED = top mais 800 CHF.",
    "clavier": "MEILLEUR CLAVIER : Mecanique, switches rouges ou bleus. Logitech G Pro X, Razer BlackWidow, 【entity-Keychron¦canonical_name=Keychron】.",
    "souris": "MEILLEURE SOURIS : Logitech G Pro X Superlight 2 - 60g, sans fil, souris des pros.",
    "fps": "FPS = Images par seconde. 60 = fluide, 144 = super fluide, 240 = pro.",
}

TOUT = {
    "pythagore": "Pythagore : a2 + b2 = c2. Ex : 3-4-5 car 9+16=25. Triangle rectangle.",
    "thales": "Thales : Si 2 droites paralleles coupent 2 secantes, rapports egaux.",
    "moyenne": "Moyenne = somme / nombre. Ex : (12+15+18)/3 = 15",
    "aire": "Aire : Rectangle = L x l, Triangle = (b x h)/2, Cercle = pi x r2",
    "perimetre": "Perimetre : Carre = 4 x cote, Rectangle = 2 x (L+l), Cercle = 2 x pi x r",
    "volume": "Volume : Cube = c3, Pave = L x l x h",
    "fraction": "Fraction : 1/2 + 1/4 = 3/4. Meme denominateur.",
    "pourcentage": "Pourcentage : 20% de 50 = 10. Formule : (partie / total) x 100",
    "equation": "Equation : 2x+3=7 -> x=2.",
    "angle": "Angles : Droit = 90, Plat = 180, Triangle = 180 au total",
    "etre": "ETRE : je suis, tu es, il est, nous sommes, vous etes, ils sont",
    "avoir": "AVOIR : j'ai, tu as, il a, nous avons, vous avez, ils ont",
    "aller": "ALLER : je vais, tu vas, il va, nous allons, vous allez, ils vont",
    "faire": "FAIRE : je fais, tu fais, il fait, nous faisons, vous faites, ils font",
    "pluriel": "Pluriel : chat -> chats, cheval -> chevaux, bateau -> bateaux",
    "adjectif": "Adjectif : decrit un nom. grand garcon / grande fille.",
    "passe compose": "Passe compose : avoir/etre + participe. J'ai mange.",
    "imparfait": "Imparfait : habitude. Je jouais. -ais, -ais, -ait",
    "futur": "Futur : Je mangerai, tu mangeras",
    "der": "Allemand : der = masculin, die = feminin, das = neutre",
    "sein": "SEIN : ich bin, du bist, er ist, wir sind, ihr seid, sie sind",
    "to be": "TO BE : I am, You are, He is, We are, You are, They are",
    "photosynthese": "Photosynthese : Soleil + Eau + CO2 = Oxygene + Sucre.",
    "planete": "Planetes : Mercure, Venus, Terre, Mars, Jupiter, Saturne, Uranus, Neptune.",
    "gravite": "Gravite : nous attire vers la Terre. Newton + pomme.",
    "ciel bleu": "Ciel bleu : l'air diffuse le bleu du Soleil.",
    "coeur": "Coeur : pompe le sang, 100 000 battements par jour",
    "volcan": "Volcan : Magma qui sort. Lave = magma dehors.",
    "saison": "Saisons : c'est l'inclinaison de la Terre.",
    "foudre": "Foudre : 30 000 degres, 5x plus chaud que le Soleil",
    "continent": "Continents : Europe, Afrique, Asie, Amerique, Oceanie, Antarctique",
    "ocean": "Oceans : Pacifique, Atlantique, Indien, Arctique, Antarctique",
    "rome": "Rome : fondee -753, Colisee, Jules Cesar",
    "moyen age": "Moyen Age : 476-1492, Chateaux, chevaliers",
    "egypte": "Egypte : Pyramides, Pharaons, Nil",
    "napoleon": "Napoleon : Empereur 1804-1815, Waterloo 1815",
    "masse volumique": "MASSE VOLUMIQUE : Formule = masse / volume. Rho = m / V. m en grammes (balance), V en cm3 (eprouvette). Ex : 100g / 100 cm3 = 1 g/cm3 = eau. Huile 0,9 flotte, Fer 7,8 coule. Si < 1 ca flotte, si > 1 ca coule !",
    "densite": "DENSITE / MASSE VOLUMIQUE : Rho = m / V. Masse / Volume. Ex : 100g / 100 cm3 = 1 g/cm3 = eau.",
    "masse": "MASSE VOLUMIQUE : Rho = m / V. Tu peses (m) et tu mesures le volume (V), tu divises. Ex : 200g / 50 cm3 = 4 g/cm3.",
    "chimie": "CHIMIE : Atome = brique de base. H2O = eau, CO2 = dioxyde de carbone, O2 = oxygene.",
    "atome": "ATOME : Proton (+), Neutron (0), Electron (-).",
    "oxygene": "OXYGENE : O2. On respire O2, on rejette CO2.",
    "trou noir": "TROU NOIR : Objet tellement lourd que meme la lumiere ne peut pas sortir.",
    "soleil": "SOLEIL : Etoile, 15 millions de degres au centre.",
    "galaxie": "GALAXIE : Notre galaxie = Voie Lactee, 200 milliards d'etoiles.",
    "big bang": "BIG BANG : Debut de l'univers il y a 13,8 milliards d'annees.",
    "mars": "MARS : Planete rouge. Un jour sur Mars = 24h37.",
    "iss": "ISS : Station spatiale a 400 km, 28 000 km/h. 16 levers de soleil par jour !",
    "dinosaure": "DINOSAURES : T-Rex carnivore, disparus il y a 66M d'annees a cause d'une meteorite.",
    "boucle": "BOUCLE : for i in range(1,6): print(i) -> affiche 1,2,3,4,5",
    "condition": "CONDITION : if age >= 18: print('Majeur') else: print('Mineur')",
    "variable": "VARIABLE : age = 13. Boite qui stocke une valeur.",
    "python": "PYTHON : Langage facile, celui de ton agent.",
    " 【entity-messi¦canonical_name=Messi】": " 【entity-Messi¦canonical_name=Messi】 : Argentin, 8 Ballons d'Or, meilleur de tous les temps. 【entity-Barca¦canonical_name=Barca】, 【entity-PSG¦canonical_name=PSG】, 【entity-Miami¦canonical_name=Inter Miami CF】.",
    " 【entity-ronaldo¦canonical_name=Ronaldo】": " 【entity-CR7¦canonical_name=CR7】 : Portugais, 5 Ballons d'Or, 【entity-Real¦canonical_name=Real Madrid】, Man United, 【entity-Al-Nassr¦canonical_name=Al-Nassr】.",
    " 【entity-mbappe¦canonical_name=Mbappe】": " 【entity-Mbappe¦canonical_name=Mbappe】 : Francais, 36 km/h ! 【entity-Real¦canonical_name=Real Madrid】 Madrid, Champion du monde 2018.",
    "ballon d'or": "BALLON D'OR : 【entity-Messi¦canonical_name=Messi】 en a 8, record !",
    "coupe du monde": "COUPE DU MONDE : Tous les 4 ans. 2022 = Argentine. 2026 = USA / Canada / Mexique. 48 equipes !",
    "ligue des champions": "LIGUE DES CHAMPIONS : 【entity-Real¦canonical_name=Real Madrid】 Madrid a gagne 15 fois !",
    "basket": "BASKET : 5 vs 5, Michael Jordan = GOAT. 【entity-NBA¦canonical_name=NBA】 aux USA.",
    "tennis": "TENNIS : 【entity-Federer¦canonical_name=Roger Federer】, 【entity-Nadal¦canonical_name=Nadal】, 【entity-Djokovic¦canonical_name=Djokovic】 = 3 meilleurs de l'histoire.",
    "formule 1": "FORMULE 1 : 350 km/h ! Verstappen, Hamilton, Leclerc.",
    " 【entity-minecraft¦canonical_name=Minecraft】": " 【entity-MINECRAFT¦canonical_name=Minecraft】 : Jeu de cubes, 300M de copies ! Construis, mine, survis aux creepers.",
    " 【entity-fortnite¦canonical_name=Fortnite】": " 【entity-FORTNITE¦canonical_name=Fortnite】 : Battle Royale 100 joueurs, dernier vivant gagne.",
    " 【entity-roblox¦canonical_name=Roblox】": " 【entity-ROBLOX¦canonical_name=Roblox】 : Des millions de jeux crees par les joueurs.",
    "gta": "GTA V : 190M de copies ! Monde ouvert.",
    " mario": " MARIO : Plombier Nintendo, sauve Peach.",
    " pokemon": " POKEMON : Attrape-les tous ! Pikachu = mascotte.",
    "tour eiffel": "TOUR EIFFEL : Paris, 330m, 1889, Gustave Eiffel.",
    "pyramide": "PYRAMIDES : Egypte, 4500 ans, Pharaons.",
    " 【entity-titanic¦canonical_name=Titanic】": " 【entity-TITANIC¦canonical_name=Titanic】 : Coule en 1912, iceberg. Film 1997.",
    " harry potter": " HARRY POTTER : Sorcier avec cicatrice en eclair. Par J.K. Rowling.",
    "one piece": "ONE PIECE : Manga le plus vendu au monde. Luffy veut devenir Roi des Pirates.",
    "naruto": "NARUTO : Ninja qui veut devenir Hokage. Rasengan !",
    "dragon ball": "DRAGON BALL : Goku, Super Saiyan, Kamehameha !",
}

AVIONS = {
    "f-22": "F-22 Raptor (USA) - LE PLUS PERFORMANT EN COMBAT. Mach 2.25 (2400 km/h). Furtif, jamais battu.",
    " 【entity-f-35¦canonical_name=F-35】": " 【entity-F-35¦canonical_name=F-35】 Lightning II (USA) - LE PLUS MODERNE. Mach 1.6. La Suisse en a achete 36 !",
    "su-57": "Su-57 Felon (Russie). Mach 2.0. Chasseur furtif russe.",
    "j-20": "J-20 (Chine). Mach 2.0. Chasseur furtif chinois.",
    "rafale": "Rafale (France). Mach 1.8. Polyvalent : air, sol, mer.",
    "eurofighter": "Eurofighter Typhoon. Mach 2.0. Allemagne, UK, Italie, Espagne.",
    "f-16": "F-16. Mach 2.0. Plus produit : 4600 exemplaires !",
    "f-15": "F-15 Eagle. Mach 2.5 ! 104 victoires a 0 defaite.",
    "f-18": "F/A-18 Hornet. Mach 1.8. Sur porte-avions. La Suisse l'utilise aussi.",
    "gripen": "Gripen (Suede). Mach 2.0. Peut atterrir sur une autoroute !",
    "su-35": "Su-35 (Russie). Mach 2.25. Peut faire le cobra.",
    "mig-29": "MiG-29 (Russie). Mach 2.25. Rival du F-16.",
    "a-10": "A-10 Warthog. Canon geant de 30mm qui detruit les tanks !",
    "sr-71": "SR-71 Blackbird. Mach 3.3 = 3500 km/h ! Plus rapide de tous les temps.",
    "a380": "Airbus A380 : Plus gros avion de passagers. 2 etages, 850 passagers !",
    "concorde": "Concorde : Paris-New York en 3h30. Mach 2. Arrete en 2003.",
    "comment vole": "COMMENT VOLE UN AVION ? L'aile est courbee, l'air va plus vite au-dessus, ca cree une portance.",
    "pilote": "PILOTE : 200h de vol, licence, maths / physique. Salaire : 8000-15000 CHF / mois en Suisse.",
}

def toutes_tables():
    txt = "📐 TOUTES LES TABLES DE MULTIPLICATION 1 a 12 :\n\n"
    for n in range(1, 13):
        txt += f"Table de {n} : " + ", ".join([f"{n}x{i}={n*i}" for i in range(1, 11)]) + "\n\n"
    txt += "➡️ Astuce : Table de 9 = tes doigts ! 9x3 = 27 (2 doigts baisses, 7 restants)"
    return txt

def table_division(n):
    txt = f"➗ TABLE DE DIVISION DE {n} :\n"
    for i in range(1, 11):
        txt += f"{n*i} / {n} = {i}  |  "
    return txt

def trouver(q_orig):
    q = q_orig.lower()
    for mot in ["c'est quoi", "c est quoi", "c'est", "comment", "pourquoi", "donne-moi", "donne moi", "c'est qui", "qui est", "quel est", "quelle est", "comment calculer", "?"]:
        q = q.replace(mot, " ")
    q = " ".join(q.split())

    if "toutes les tables" in q or "toutes tables" in q or q.strip() == "tables":
        return toutes_tables()
    if "division" in q:
        try:
            n = int(''.join(filter(str.isdigit, q)))
            return table_division(n)
        except:
            return "Essaie : Table de division de 8"
    if "table de" in q or "table du" in q:
        try:
            n = int(''.join(filter(str.isdigit, q)))
            res = ", ".join([str(n) + "x" + str(i) + "=" + str(n*i) for i in range(1, 11)])
            return "Table de " + str(n) + " : " + res + f" | Astuce : {n}x10 = {n}0"
        except:
            pass
    if "performant" in q or "meilleur avion" in q:
        return "AVION LE PLUS PERFORMANT ? 1. Combat : F-22 Raptor - meilleur, furtif, jamais battu. 2. Moderne : F-35 - fait tout, Suisse a choisi. 3. Vitesse : SR-71 - 3500 km/h. Mon choix : F-22 = le roi."
    if "capitale" in q:
        for pays, cap in CAPITALES.items():
            if pays in q:
                return "Capitale de " + pays.capitalize() + " = " + cap
        return "J'ai 195 capitales ! Essaie : capitale du Japon..."
    for cle, rep in PC.items():
        if cle in q:
            return "💻 " + rep
    for cle, rep in AVIONS.items():
        if cle in q:
            return "✈️ " + rep
    for mot, rep in TOUT.items():
        if mot in q:
            return rep
    for pays, cap in CAPITALES.items():
        if q == pays:
            return pays.capitalize() + " -> Capitale = " + cap
    return "Je ne connais pas encore : " + q_orig + ". Essaie : Toutes les tables, Table de 7, Table de division de 8..."

if "auto_q" in st.session_state and st.session_state.auto_q:
    q_auto = st.session_state.auto_q
    st.session_state.auto_q = ""
    r_auto = trouver(q_auto)
    st.session_state.messages.append({"role": "assistant", "content": r_auto})
    with st.chat_message("assistant"):
        st.write(r_auto)

if question := st.chat_input("Pose ta question... ou clique sur une question en haut !"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        r = trouver(question)
        st.write(r)
    st.session_state.messages.append({"role": "assistant", "content": r})
