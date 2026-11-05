import streamlit as st
import random
import datetime
import re

st.set_page_config(page_title="Agent IA V5", page_icon="🖤", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #0a0a0a; color: #e5e5e5; }
[data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #222222; }
[data-testid="stSidebar"] * { color: #e5e5e5 !important; }
.stChatMessage { background-color: #161616 !important; color: #e5e5e5 !important; border: 1px solid #2a2a2a; border-radius: 12px; }
h1 { color: #f0f0f0 !important; }
.stChatInput input { background-color: #161616 !important; color: #e5e5e5 !important; border: 1px solid #2a2a2a !important; }
button { background-color: #1e1e1e !important; color: #e5e5e5 !important; border: 1px solid #2e2e2e !important; border-radius: 10px !important; box-shadow: none !important; font-weight: 500 !important; }
button:hover { background-color: #2a2a2a !important; border-color: #3a3a3a !important; color: white !important; }
[data-testid="stCaption"] { color: #888888 !important; }
</style>
""", unsafe_allow_html=True)

if "learned" not in st.session_state:
    st.session_state.learned = {}
if "theme" not in st.session_state:
    st.session_state.theme = "📐 Ecole"
if "matiere" not in st.session_state:
    st.session_state.matiere = None
if "genre" not in st.session_state:
    st.session_state.genre = None
if "score" not in st.session_state:
    st.session_state.score = 0
if "total_quiz" not in st.session_state:
    st.session_state.total_quiz = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "best_streak" not in st.session_state:
    st.session_state.best_streak = 0
if "train_q" not in st.session_state:
    st.session_state.train_q = None
if "train_a" not in st.session_state:
    st.session_state.train_a = None
if "mode_train" not in st.session_state:
    st.session_state.mode_train = False
if "niveau" not in st.session_state:
    st.session_state.niveau = "moyen"

# ============ MATIERE -> GENRE -> QUESTIONS ============
MATIERES_GENRES = {
    "📐 Maths": {
        "📐 Géométrie": ["C'est quoi le théorème de Pythagore ?", "C'est quoi Thales ?", "C'est quoi l'aire ?", "C'est quoi le perimetre ?", "C'est quoi le volume ?", "C'est quoi un angle ?"],
        "🧮 Calcul": ["Table de 7", "Toutes les tables de multiplication", "Table de division de 8", "C'est quoi la moyenne ?", "Calcule 12+8", "Calcule 15x7"],
        "🍕 Fractions / %": ["C'est quoi une fraction ?", "C'est quoi le pourcentage ?", "C'est quoi une equation ?", "C'est quoi le nombre decimal ?"],
    },
    "🇫🇷 Français": {
        "📖 Grammaire": ["C'est quoi le COD ?", "C'est quoi le sujet ?", "C'est quoi un adjectif ?", "C'est quoi le pluriel ?", "C'est quoi le verbe ?", "C'est quoi le pronom ?"],
        "✍️ Conjugaison": ["Conjugue ETRE", "Conjugue AVOIR", "Conjugue ALLER", "Conjugue FAIRE", "C'est quoi le passe compose ?", "C'est quoi l'imparfait ?", "C'est quoi le futur ?"],
        "📝 Orthographe": ["C'est quoi le pluriel ?", "C'est quoi a / à ?", "C'est quoi et / est ?", "C'est quoi son / sont ?", "C'est quoi ces / ses ?"],
        "📚 Vocabulaire": ["C'est quoi un synonyme ?", "C'est quoi un antonyme ?", "C'est quoi un homonyme ?", "C'est quoi une famille de mots ?"],
    },
    "🇩🇪 Allemand": {
        "📖 Grammaire": ["C'est quoi der die das ?", "C'est quoi l'accusatif ?", "C'est quoi le datif ?", "C'est quoi le nominatif ?"],
        "✍️ Conjugaison": ["Conjugue SEIN", "Conjugue HABEN", "C'est quoi GEHEN ?", "Conjugue MACHEN"],
        "🌍 Vocabulaire": ["Traduis bonjour en allemand", "Traduis merci en allemand", "Traduis ecole en allemand", "Traduis chien en allemand"],
    },
    "🇬🇧 Anglais": {
        "📖 Grammaire": ["C'est quoi le present simple ?", "C'est quoi le present perfect ?", "C'est quoi le present continu ?", "C'est quoi le pluriel en anglais ?"],
        "✍️ Conjugaison": ["Conjugue TO BE", "Conjugue TO HAVE", "C'est quoi TO GO ?", "Conjugue TO DO"],
        "🌍 Vocabulaire": ["Traduis bonjour en anglais", "Traduis merci en anglais", "Traduis ecole en anglais", "Traduis chien en anglais", "Traduis maison en anglais"],
    },
    "📜 Histoire / Géo": {
        "📜 Histoire": ["C'est quoi la 2eme Guerre ?", "C'est quoi la 1ere Guerre ?", "C'est quoi la Revolution ?", "C'est quoi Rome ?", "C'est quoi le Moyen Age ?", "C'est quoi l'Egypte ?", "C'est quoi Napoleon ?"],
        "🌍 Géographie": ["C'est quoi les continents ?", "C'est quoi les oceans ?", "Capitale du Japon ?", "Capitale de la France ?", "Capitale de la Suisse ?"],
    },
    "🔬 Sciences": {
        "🧬 Biologie": ["C'est quoi la photosynthese ?", "C'est quoi le coeur ?", "C'est quoi l'ADN ?", "C'est quoi le corps humain ?"],
        "🌍 Terre / Espace": ["C'est quoi un volcan ?", "C'est quoi les saisons ?", "C'est quoi la foudre ?", "C'est quoi le systeme solaire ?", "C'est quoi un trou noir ?", "C'est quoi Mars ?"],
        "⚡ Physique": ["C'est quoi la gravite ?", "Comment calculer la masse volumique ?", "C'est quoi la vitesse ?", "C'est quoi l'energie ?"],
    },
    "🧪 Chimie / Physique": {
        "⚛️ Chimie": ["C'est quoi un atome ?", "C'est quoi l'oxygene ?", "C'est quoi la chimie ?", "C'est quoi une molecule ?", "C'est quoi le tableau periodique ?"],
        "⚡ Physique": ["C'est quoi l'electricite ?", "C'est quoi la masse volumique ?", "C'est quoi la vitesse ?", "C'est quoi la force ?"],
    },
    "💻 Code": {
        "🧠 Bases": ["C'est quoi une variable ?", "C'est quoi une boucle ?", "C'est quoi une condition ?", "C'est quoi une fonction ?", "C'est quoi une liste ?"],
        "🌐 Langages": ["C'est quoi Python ?", "C'est quoi HTML ?", "C'est quoi CSS ?", "C'est quoi JavaScript ?"],
    },
}

THEMES = {
    "📐 Ecole": ["Voir toutes les matières 👇"],
    "👋 Bases": ["Bonjour", "Ca va ?", "Merci", "Au revoir", "Tu t'appelles comment ?", "Raconte une blague", "Motive moi"],
    "🧠 Apprends-moi": ["Entraine moi", "Entrainement facile", "Entrainement difficile", "Mon score", "Montre ce que tu as appris"],
    "🧮 Calculatrice": ["Calcule 12+8", "Calcule 15x7", "Calcule 144/12"],
    "🌍 Traductions": ["Traduis bonjour en anglais", "Traduis merci en anglais", "Traduis bonjour en allemand"],
    "🎲 Fun": ["Raconte une blague", "Motive moi", "Conseil pour reviser", "Quelle heure il est ?"],
    "🌍 Capitales": ["Capitale du Japon ?", "Capitale du Bresil ?", "Capitale de l'Egypte ?", "Capitale de la Suisse ?"],
    "✈️ Avions": ["Quel est l'avion de chasse le plus performant ?", "C'est quoi le F-22 ?", "C'est quoi le 【entity-F-35¦canonical_name=F-35】 ?", "C'est quoi le Rafale ?", "C'est quoi le SR-71 ?"],
    "💻 PC": ["C'est quoi le meilleur rapport qualite prix ?", "C'est quoi la meilleure GPU ?", "C'est quoi le meilleur CPU ?", "PC 2000 CHF", "PC 1300 CHF", "PC 900 CHF"],
    "⚽ Foot / Sport": ["C'est qui 【entity-Messi¦canonical_name=Messi】 ?", "C'est qui 【entity-Ronaldo¦canonical_name=Ronaldo】 ?", "C'est qui 【entity-Mbappe¦canonical_name=Mbappe】 ?", "C'est quoi la Coupe du Monde ?"],
    "🎮 Jeux Video": ["C'est quoi 【entity-Minecraft¦canonical_name=Minecraft】 ?", "C'est quoi 【entity-Fortnite¦canonical_name=Fortnite】 ?", "C'est quoi 【entity-Roblox¦canonical_name=Roblox】 ?", "C'est quoi GTA ?"],
    "🚀 Espace": ["C'est quoi un trou noir ?", "C'est quoi le Big Bang ?", "C'est quoi Mars ?", "C'est quoi l'ISS ?"],
    "🧠 Culture G": ["C'est qui Werenoi ?", "C'est qui Ninho ?", "C'est qui Jul ?", "C'est quoi la Tour Eiffel ?", "C'est quoi le 【entity-Titanic¦canonical_name=Titanic】 ?"],
    "🎤 Chanteurs": ["C'est qui Werenoi ?", "C'est qui Ninho ?", "C'est qui Jul ?", "C'est qui 【entity-Gazo¦canonical_name=Gazo】 ?", "C'est qui 【entity-Tiakola¦canonical_name=Tiakola】 ?", "C'est qui 【entity-PNL¦canonical_name=PNL】 ?", "C'est qui SDM ?", "C'est qui 【entity-Drake¦canonical_name=Drake】 ?"],
    "💰 Argent / Metiers": ["Comment devenir millionnaire ?", "C'est quoi un salaire ?", "Comment gagner de l'argent a 13 ans ?"],
    "🐾 Animaux": ["C'est quoi le plus grand animal ?", "C'est quoi le plus rapide ?", "C'est quoi un chien ?", "C'est quoi un chat ?"],
}

with st.sidebar:
    st.title("Agent IA V5")
    st.write(f"🧠 Appris : {len(st.session_state.learned)}")
    st.write(f"🏆 Score : {st.session_state.score} / {st.session_state.total_quiz}")
    st.write(f"🔥 Streak : {st.session_state.streak} | Best : {st.session_state.best_streak}")
    for t in THEMES.keys():
        if st.button(t, key="side_"+t, use_container_width=True):
            st.session_state.theme = t
            st.session_state.matiere = None
            st.session_state.genre = None
            st.rerun()
    st.divider()
    st.write("MATIERES ECOLE :")
    for m in MATIERES_GENRES.keys():
        if st.button(m, key="side_m_"+m, use_container_width=True):
            st.session_state.theme = "📐 Ecole"
            st.session_state.matiere = m
            st.session_state.genre = None
            st.rerun()
    st.divider()
    if st.button("Effacer"):
        st.session_state.messages = []
        st.rerun()
    if st.button("Oublier ce que j'ai appris"):
        st.session_state.learned = {}
        st.session_state.score = 0
        st.session_state.total_quiz = 0
        st.session_state.streak = 0
        st.rerun()

st.title("Agent IA V5")
st.caption(f"🧠 Il apprend ! | {len(st.session_state.learned)} appris | Score : {st.session_state.score}/{st.session_state.total_quiz} | 🔥 Streak : {st.session_state.streak} | Fond noir discret")

if st.session_state.mode_train:
    st.success(f"🎯 ENTRAINEMENT {st.session_state.niveau.upper()} - Score : {st.session_state.score}/{st.session_state.total_quiz} - 🔥 Streak : {st.session_state.streak} - Ecris 'stop' pour arreter")

# ---- NAVIGATION MATIERE -> GENRE -> QUESTIONS ----
if st.session_state.theme == "📐 Ecole":
    st.subheader("1️⃣ Choisis ta MATIERE :")
    cols2 = st.columns(4)
    for i, m in enumerate(list(MATIERES_GENRES.keys())):
        with cols2[i % 4]:
            sel = "✅ " if st.session_state.matiere == m else ""
            if st.button(sel + m, key="mat_"+m, use_container_width=True):
                st.session_state.matiere = m
                st.session_state.genre = None
                st.rerun()
    if st.session_state.matiere:
        st.subheader(f"2️⃣ Choisis ton GENRE dans {st.session_state.matiere} :")
        genres = list(MATIERES_GENRES[st.session_state.matiere].keys())
        colsG = st.columns(len(genres))
        for i, g in enumerate(genres):
            with colsG[i]:
                sel = "✅ " if st.session_state.genre == g else ""
                if st.button(sel + g, key="genre_"+g, use_container_width=True):
                    st.session_state.genre = g
                    st.rerun()
    if st.session_state.matiere and st.session_state.genre:
        st.subheader(f"3️⃣ Questions : {st.session_state.matiere} → {st.session_state.genre} - Clique :")
        for q in MATIERES_GENRES[st.session_state.matiere][st.session_state.genre]:
            if st.button(q, key="q_"+q, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": q})
                st.session_state.auto_q = q
                st.rerun()
        if st.button("↩️ Changer de genre / matière", use_container_width=True):
            st.session_state.matiere = None
            st.session_state.genre = None
            st.rerun()
    elif st.session_state.matiere:
        st.info(f"👆 Choisis un genre dans {st.session_state.matiere} pour voir les questions")
else:
    cols = st.columns(3)
    for i, t in enumerate(list(THEMES.keys())):
        with cols[i % 3]:
            if st.button(t, key="top_"+t, use_container_width=True):
                st.session_state.theme = t
                st.session_state.matiere = None
                st.session_state.genre = None
                st.rerun()
    if st.session_state.theme != "📐 Ecole":
        st.subheader(f"Questions {st.session_state.theme} - Clique :")
        for q in THEMES.get(st.session_state.theme, []):
            if st.button(q, key="q2_"+q, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": q})
                st.session_state.auto_q = q
                st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Salut ! 👋 Moi c'est Agent IA V5 ! Maintenant tu peux choisir : MATIERE → GENRE → QUESTION ! Ex : Français → Grammaire → C'est quoi le COD ? Essaie en haut ! Ou écris : Bonjour / Entraine moi / Apprends : c'est quoi le foot = ..."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

def nettoyer(txt):
    txt = txt.lower().strip()
    txt = txt.replace("é", "e").replace("è", "e").replace("ê", "e").replace("à", "a").replace("ç", "c").replace("ô", "o").replace("î", "i").replace("û", "u")
    txt = re.sub(r"[^a-z0-9 +*/\-=?.]", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt

BASES = {
    "bonjour": "Bonjour ! 👋 Comment tu vas ? Moi je vais super bien, merci ! Tu veux que je t'aide pour quoi ? Choisis ta matière en haut : Français → Grammaire, ou Maths → Géométrie... Ou écris-moi ta question !",
    "bonsoir": "Bonsoir ! 🌙 Comment tu vas ? Tu veux réviser quelle matière ? Français → Grammaire, ou Maths → Calcul ?",
    "salut": "Salut ! 👋 Ca va ? Choisis ta matière en haut : Français → Grammaire, Maths → Géométrie... Ou pose-moi ta question !",
    "slt": "Slt ! 👋 Ca va ?",
    "yo": "Yo ! 👋 Ca va ? Tu veux réviser quoi ? Français → Grammaire ?",
    "coucou": "Coucou ! 👋 Ca va bien ?",
    "hello": "Hello ! 👋 Ca va ?",
    "merci": "De rien ! 😊 Avec plaisir ! Tu as une autre question ? Choisis une autre matière / genre en haut !",
    "mrc": "De rien ! 😊",
    "ca va": "Ca va super bien merci ! Et toi, ca va ? Tu révises quelle matière ?",
    "cv": "Ca va super bien merci ! Et toi ? 😊",
    "au revoir": "Au revoir ! 👋 A très vite ! J'espère que je t'ai aidé ! Reviens quand tu veux, je suis là H24 ! 😊",
    "bye": "Bye ! 👋 A très vite !",
    "a plus": "A plus ! 👋 Bonne journée !",
    "bonne nuit": "Bonne nuit ! 😴 Dors bien ! A demain !",
    "t appelles comment": "Moi je m'appelle Agent IA V5 ! 🤖 Et toi, tu t'appelles comment ? Moi je t'aide pour toutes les matières : Français → Grammaire, Maths → Géométrie...",
    "qui es tu": "Moi je suis Agent IA V5 ! 🤖 Ton assistant créé par Lenny. Maintenant tu peux choisir Matière → Genre → Question ! Ex : Français → Grammaire → C'est quoi le COD ?",
    "aide moi": "Oui bien sûr ! 😊 Dis-moi, c'est pour quelle matière et quel genre ? Ex : Français → Grammaire, ou Maths → Géométrie ? Choisis en haut, ou écris ta question !",
    "j ai pas compris": "T'inquiète, c'est normal ! 😊 Dis-moi ce que tu n'as pas compris, je vais te réexpliquer plus simplement, avec un autre exemple.",
    "j ai compris": "Trop bien ! 😊 Bravo ! Tu veux que je te pose une question pour vérifier ou on passe à une autre matière / genre ?",
    "t es trop fort": "Merciii ! 😊 Ca me fait trop plaisir !",
    "quelle heure": f"Il est {datetime.datetime.now().strftime('%H:%M')} ! ⏰ En Suisse !",
    "quelle date": f"On est le {datetime.datetime.now().strftime('%d/%m/%Y')} ! 📅",
}

BLAGUES = ["Pourquoi les plongeurs plongent-ils toujours en arrière ? Parce que sinon, ils tombent dans le bateau ! 😂","Que dit un zéro à un huit ? Belle ceinture ! 😂","Pourquoi les maths sont tristes ? Parce qu'elles ont trop de problèmes ! 😂","Pourquoi les poissons n'aiment pas jouer au foot ? Parce qu'ils ont peur des filets ! 😂","Que fait une fraise sur un cheval ? Tagada tagada ! 🍓🐴😂","Pourquoi les squelettes ne se battent pas ? Parce qu'ils n'ont pas de tripes ! 💀😂"]
MOTIVATIONS = ["Tu peux le faire ! 💪 Chaque erreur, c'est une leçon. Ne lâche rien !","N'abandonne jamais ! 🔥 10 minutes par jour, tous les jours, et dans 1 mois tu seras trop fort !","Tu es capable de beaucoup plus que tu crois ! 🚀 Commence petit, 1 exercice, et ça va venir !"]
TRADUCTIONS = {"bonjour en anglais": "Bonjour en anglais = Hello / Good morning ! 🇬🇧 Ex : Hello, how are you ?","bonjour en allemand": "Bonjour en allemand = Hallo / Guten Tag ! 🇩🇪 Ex : Hallo, wie geht's ?","bonjour en espagnol": "Bonjour en espagnol = Hola / Buenos dias ! 🇪🇸","bonjour en italien": "Bonjour en italien = Ciao / Buongiorno ! 🇮🇹","merci en anglais": "Merci en anglais = Thank you / Thanks ! 🇬🇧","merci en allemand": "Merci en allemand = Danke ! 🇩🇪","merci en espagnol": "Merci en espagnol = Gracias ! 🇪🇸","au revoir en anglais": "Au revoir en anglais = Goodbye / Bye ! 🇬🇧","ecole en anglais": "Ecole en anglais = School ! 🇬🇧","chat en anglais": "Chat en anglais = Cat ! 🐱","chien en anglais": "Chien en anglais = Dog ! 🐶","maison en anglais": "Maison en anglais = House ! 🏠","pomme en anglais": "Pomme en anglais = Apple ! 🍎","eau en anglais": "Eau en anglais = Water ! 💧","ecole en allemand": "Ecole en allemand = Schule ! 🇩🇪","chien en allemand": "Chien en allemand = Hund ! 🇩🇪"}
CAPITALES = {"france": "Paris - 2,1M d'habitants, Tour Eiffel, Louvre. La France = 68M d'habitants.","suisse": "Berne - Capitale de la Suisse depuis 1848. Le Palais fédéral.","allemagne": "Berlin - 3,6M d'habitants, Mur de Berlin tombé en 1989.","italie": "Rome - 2,8M d'habitants, Colisée, Vatican.","espagne": "Madrid - 3,2M d'habitants, 【entity-Real Madrid¦canonical_name=Real Madrid】.","angleterre": "Londres - 9M d'habitants, Big Ben.","japon": "Tokyo - 14M d'habitants, Sushi, Manga, Anime.","usa": "Washington D.C. - Maison Blanche. New York = plus grande ville, pas la capitale !","canada": "Ottawa - Toronto = plus grande ville.","chine": "Pékin - Grande Muraille.","russie": "Moscou - Place Rouge.","bresil": "Brasilia - Rio = plus connue, Christ Rédempteur.","inde": "New Delhi - Taj Mahal.","australie": "Canberra - Sydney = plus connue.","egypte": "Le Caire - Pyramides de Gizeh.","maroc": "Rabat","algerie": "Alger","tunisie": "Tunis","portugal": "Lisbonne - 【entity-Cristiano Ronaldo¦canonical_name=Cristiano Ronaldo】 !","belgique": "Bruxelles - Frites, Chocolat !","pays-bas": "Amsterdam - Canaux, Vélos.","autriche": "Vienne - Mozart.","suede": "Stockholm - 【entity-IKEA¦canonical_name=IKEA】, 【entity-ABBA¦canonical_name=ABBA】.","norvege": "Oslo - Fjords, 【entity-Haaland¦canonical_name=Haaland】 !","danemark": "Copenhague - 【entity-LEGO¦canonical_name=LEGO】.","finlande": "Helsinki - Père Noël.","pologne": "Varsovie - 【entity-Lewandowski¦canonical_name=Lewandowski】.","grece": "Athènes - Jeux Olympiques, Zeus.","turquie": "Ankara - Istanbul = plus grande ville.","coree": "Séoul - K-Pop (【entity-BTS¦canonical_name=BTS】).","thailande": "Bangkok - Temples.","mexique": "Mexico - Tacos, Aztèques."," argentine": "Buenos Aires - 【entity-Messi¦canonical_name=Messi】, Tango.","kenya": "Nairobi - Safaris."}

PC = {
    "rapport qualite prix": "MEILLEUR RAPPORT QUALITE / PRIX PC 2026 : GAGNANT 1300 CHF : RTX 5070 (600) + Ryzen 7 7800X3D (350) + 32 Go (120) + SSD 1 To (70) = 1300 CHF. 1440p Ultra 180 FPS ! PETIT BUDGET 900 CHF : RTX 4060 + Ryzen 5 7600 = 900 CHF, 1080p 144 FPS. GROS BUDGET 2000 CHF : RTX 5070 Ti + 9800X3D = 2000 CHF, 240 FPS.",
    "pc 900": "PC 900 CHF : RTX 4060 + Ryzen 5 7600 + 16 Go + SSD 1 To = 900 CHF. 【entity-Fortnite¦canonical_name=Fortnite】 144 FPS !",
    "pc 1300": "PC 1300 CHF - MEILLEUR RAPPORT : RTX 5070 + Ryzen 7 7800X3D + 32 Go + SSD 1 To = 1300 CHF. 1440p Ultra 180 FPS !",
    "pc 2000": "PC 2000 CHF : RTX 5070 Ti + Ryzen 7 9800X3D + 32 Go + SSD 2 To = 2000 CHF. 240 FPS !",
    "meilleure gpu": "MEILLEURE GPU 2026 : 1. RTX 5090 - 32 Go, 2500 CHF. 2. RTX 5080 - 1200 CHF. 3. RTX 5070 Ti - 850 CHF. Meilleur rapport = RTX 5070 (600 CHF) !",
    "gpu": "GPU = Carte Graphique. Elle calcule les images des jeux. Meilleure = RTX 5090. Meilleur rapport = RTX 5070.",
    "meilleur cpu": "MEILLEUR CPU 2026 : 1. Ryzen 9 9950X3D. 2. Ryzen 7 9800X3D. 3. Meilleur rapport = Ryzen 7 7800X3D (350 CHF) !",
    "cpu": "CPU = Processeur, cerveau du PC. Meilleur rapport = Ryzen 7 7800X3D (350 CHF).",
    "meilleur ssd": "MEILLEUR SSD : 【entity-Samsung¦canonical_name=Samsung】 990 PRO 2 To - 7450 Mo/s. Meilleur rapport = WD Black SN850X 1 To (70 CHF) !",
    "meilleure ram": "MEILLEURE RAM : 32 Go DDR5 6000 MHz CL30. Parfait : jeu + Discord + Chrome sans lag.",
    "ram": "RAM = Mémoire vive. 16 Go = minimum. 32 Go DDR5 = parfait.",
}

CHANTEURS = {
    "werenoi": "WERENOI : Rappeur français, le plus écouté en France en 2024 et 2025 ! Albums : Pyramide, Diamant Noir. Style : drill mélodique, voix grave. Sons : Solitaire, Ciao, Pyramide. Décédé en mai 2025, il reste une légende.",
    "ninho": "NINHO : Rappeur français, record de disques d'or et de diamant en France ! Albums : M.I.L.S, Jefe, NI. Son feat : Lettre à une femme = diamant.",
    "jul": "JUL : Rappeur de Marseille, le plus productif ! 2 albums par an. Albums : La machine, C'est pas des LOL. Son signe : la main.",
    " 【entity-gazo¦canonical_name=Gazo】": " 【entity-GAZO¦canonical_name=Gazo】 : Roi de la drill en France ! Album : KMT, Apocalypse. Feat avec 【entity-Tiakola¦canonical_name=Tiakola】 : La Melo = énorme tube.",
    " 【entity-tiakola¦canonical_name=Tiakola】": " 【entity-TIAKOLA¦canonical_name=Tiakola】 : Chanteur / rappeur, membre de 4Keus. Album : Melo, BDLM. Sa voix mélodique est unique.",
    " 【entity-pnl¦canonical_name=PNL】": " 【entity-PNL¦canonical_name=PNL】 : Duo de frères Ademo et N.O.S, de Corbeil-Essonnes. Albums : Le monde Chico, Dans la légende, Deux frères. Style : cloud rap, planant.",
    "sdm": "SDM : Rappeur français, signé chez Booba (92i). Album : Ocho, A vie. Il a explosé avec Bolide allemand avec Ninho.",
    " 【entity-drake¦canonical_name=Drake】": " 【entity-DRAKE¦canonical_name=Drake】 : Rappeur canadien, le plus streamé au monde ! Album : Take Care, Scorpion. Son : God's Plan, One Dance.",
    " taylor swift": " TAYLOR SWIFT : Chanteuse américaine, la plus écoutée au monde ! Album : 1989, Midnights. 14 Grammy. Fans = Swifties.",
    " eminem": " EMINEM : Rappeur américain, légende. Son : Lose Yourself, Rap God, Mockingbird.",
}

TOUT = {
    "pythagore": "THEOREME DE PYTHAGORE - COURS COMPLET : Formule : a² + b² = c². UNIQUEMENT pour un triangle rectangle. a et b = les 2 petits côtés, c = l'hypoténuse, le plus grand côté. Ex : 3-4-5 car 9+16=25. Ex pour trouver l'hypoténuse : Si a=6, b=8, alors c² = 36+64=100, donc c=10. Ex pour trouver un petit côté : Si c=13, b=5, alors a² = 169-25=144, donc a=12. A quoi ça sert ? Pour construire une maison, savoir si un angle est droit, calculer une distance sans mesurer.",
    "thales": "THALES : Si 2 droites parallèles coupent 2 sécantes, rapports égaux. Formule : AB / AD = AC / AE = BC / DE.",
    "moyenne": "MOYENNE : Moyenne = somme / nombre. Ex : (12+15+18)/3 = 15",
    "aire": "AIRE : Rectangle = L x l, Triangle = (b x h)/2, Cercle = pi x r²",
    "perimetre": "PERIMETRE : Carré = 4 x côté, Rectangle = 2 x (L+l), Cercle = 2 x pi x r",
    "volume": "VOLUME : Cube = côté³, Pavé = L x l x h, Cylindre = pi x r² x h. Ex : Boîte 2x3x4 = 24 cm³.",
    "angle": "ANGLES : Droit = 90°, Plat = 180°, Plein = 360°. Triangle = 180° au total. Ex : Si un triangle a 90° et 60°, le 3ème = 30°.",
    "fraction": "FRACTION : 1/2 + 1/4 = 3/4. Même dénominateur. Pour multiplier : 2/3 x 3/4 = 1/2.",
    "pourcentage": "POURCENTAGE : 20% de 50 = 10. Formule : (partie / total) x 100. Ex : 15/20 = 75%.",
    "equation": "EQUATION : 2x + 3 = 7. Tu enlèves 3 : 2x = 4. Tu divises par 2 : x = 2.",
    "nombre decimal": "NOMBRE DECIMAL : Nombre avec virgule. Ex : 1,5 = 1 + 0,5. 0,5 = 1/2.",
    "etre": "ETRE : je suis, tu es, il est, nous sommes, vous êtes, ils sont",
    "avoir": "AVOIR : j'ai, tu as, il a, nous avons, vous avez, ils ont",
    "aller": "ALLER : je vais, tu vas, il va, nous allons, vous allez, ils vont",
    "faire": "FAIRE : je fais, tu fais, il fait, nous faisons, vous faites, ils font",
    "machen": "MACHEN (FAIRE) - ALLEMAND : ich mache, du machst, er macht, wir machen, ihr macht, sie machen.",
    "pluriel": "PLURIEL : En général +s : chat -> chats. En -eau : bateau -> bateaux. En -al : cheval -> chevaux. En -ou : genou -> genoux, mais trou -> trous.",
    "adjectif": "ADJECTIF : Il décrit un nom, il s'accorde en genre et nombre. Ex : grand garçon / grande fille / grands garçons / grandes filles.",
    "verbe": "VERBE : C'est l'action dans la phrase. Ex : Je mange, Tu cours, Il dort. Il se conjugue avec le temps : présent, passé, futur.",
    "pronom": "PRONOM : Il remplace un nom pour éviter de le répéter. Ex : Lenny mange. Il mange. Je, tu, il, elle, nous, vous, ils, elles, le, la, les, lui, leur...",
    "a / a": "A / À : a = verbe avoir (Il a 13 ans). à = préposition (Je vais à l'école). Astuce : tu peux remplacer a par avait : Il avait 13 ans = a. Sinon c'est à.",
    "et / est": "ET / EST : et = liaison (Lenny et Hugo). est = verbe être (Il est gentil). Astuce : remplace par était : Il était gentil = est.",
    "son / sont": "SON / SONT : son = à lui (son chien). sont = verbe être (Ils sont gentils). Astuce : remplace par étaient : Ils étaient gentils = sont.",
    "ces / ses": "CES / SES : ces = ce, cette, ces (ces chiens). ses = à lui, à elle (ses chiens = les chiens de Lenny).",
    "synonyme": "SYNONYME : Mot qui veut dire la même chose. Ex : content = heureux, rapide = vite, grand = immense.",
    "antonyme": "ANTONYME : Mot qui veut dire le contraire. Ex : grand ≠ petit, chaud ≠ froid, content ≠ triste.",
    "homonyme": "HOMONYME : Mots qui se prononcent pareil mais s'écrivent différemment. Ex : a / à, et / est, son / sont, vert / verre / vers.",
    "famille de mots": "FAMILLE DE MOTS : Mots qui ont la même racine. Ex : fleur, fleuri, fleuriste, floraison. Terre, terrain, terrien, terrestre.",
    "passe compose": "PASSE COMPOSE : avoir/être au présent + participe passé. Ex : J'ai mangé, Je suis allé, Tu as joué. Avec être (aller, venir...) : Je suis allé, Elle est venue.",
    "imparfait": "IMPARFAIT : Pour une habitude, une description, une action longue. Terminaisons : -ais, -ais, -ait, -ions, -iez, -aient. Ex : Quand j'étais petit, je jouais au foot. Il faisait beau.",
    "futur": "FUTUR : Pour parler de demain. Terminaisons : -ai, -as, -a, -ons, -ez, -ont. Ex : Je mangerai, tu mangeras, il mangera...",
    "cod": "COD - GRAMMAIRE : COD = Complément d'Objet Direct. Il répond à Qui ? ou Quoi ? après le verbe, sans préposition. Ex : Je mange une pomme. Je mange quoi ? Une pomme = COD. Je vois Lenny. Je vois qui ? Lenny = COD. Astuce : remplace par le, la, les : Je la mange.",
    "sujet": "SUJET - GRAMMAIRE : Le sujet, c'est qui fait l'action. Il répond à Qui est-ce qui ? Ex : Lenny mange. Qui mange ? Lenny = sujet.",
    "der": "ALLEMAND - DER DIE DAS : der = masculin (der Mann), die = féminin (die Frau), das = neutre (das Kind). Pluriel = die.",
    "sein": "SEIN (ETRE) - ALLEMAND : ich bin, du bist, er ist, wir sind, ihr seid, sie sind. Ex : Ich bin 13 Jahre alt.",
    "haben": "HABEN (AVOIR) - ALLEMAND : ich habe, du hast, er hat, wir haben, ihr habt, sie haben. Ex : Ich habe einen Hund.",
    "gehen": "GEHEN (ALLER) - ALLEMAND : ich gehe, du gehst, er geht, wir gehen, ihr geht, sie gehen. Ex : Ich gehe zur Schule.",
    "accusatif": "ACCUSATIF - ALLEMAND : C'est le cas du COD. der → den, die → die, das → das. Ex : Ich sehe den Hund (Je vois le chien). Le chien = COD = accusatif.",
    "datif": "DATIF - ALLEMAND : C'est le cas du COI (à qui ?). der → dem, die → der, das → dem. Ex : Ich gebe dem Mann ein Buch (Je donne un livre à l'homme).",
    "nominatif": "NOMINATIF - ALLEMAND : C'est le cas du sujet. der, die, das. Ex : Der Mann ist gut (L'homme est gentil). Der Mann = sujet = nominatif.",
    "to be": "TO BE - ANGLAIS : I am, You are, He is, We are, You are, They are. Ex : I am 13, He is happy.",
    "to have": "TO HAVE - ANGLAIS : I have, You have, He has, We have, You have, They have. Ex : I have a dog.",
    "to go": "TO GO - ANGLAIS : I go, You go, He goes, We go, You go, They go. Ex : I go to school.",
    "to do": "TO DO - ANGLAIS : I do, You do, He does, We do, You do, They do. Ex : I do my homework = Je fais mes devoirs.",
    "present simple": "PRESENT SIMPLE - ANGLAIS : Pour les habitudes. I play, You play, He plays (avec -s !), We play... Ex : He plays football every day.",
    "present perfect": "Present Perfect : have + participe. I have eaten = J'ai mangé. I have played = J'ai joué.",
    "present continu": "PRESENT CONTINU - ANGLAIS : Pour une action en train de se passer. be + -ing. Ex : I am playing = Je suis en train de jouer.",
    "pluriel en anglais": "PLURIEL EN ANGLAIS : En général +s : cat -> cats. En -s, -x, -ch, -sh : +es : box -> boxes. En -y : baby -> babies.",
    "photosynthese": "PHOTOSYNTHESE : Soleil + Eau + CO2 = Oxygène + Sucre. Les feuilles captent la lumière, la plante fabrique son sucre et rejette de l'oxygène qu'on respire !",
    "gravite": "GRAVITE : Nous attire vers la Terre. Newton + pomme. Sur la Lune, tu es 6x plus léger.",
    "coeur": "COEUR : Pompe le sang, 100 000 battements par jour, 7 000 litres par jour !",
    "volcan": "VOLCAN : Magma qui sort. Lave = magma dehors. Etna = le plus actif d'Europe.",
    "foudre": "FOUDRE : 30 000 degrés, 5x plus chaud que le Soleil. Si tu entends le tonnerre, rentre !",
    "saison": "SAISONS : C'est l'inclinaison de la Terre (23,5°) qui fait les saisons, pas la distance au Soleil. En Australie, c'est l'inverse !",
    "corps humain": "CORPS HUMAIN : 206 os, 600 muscles, 5 litres de sang, 37 000 milliards de cellules. Le cerveau = 86 milliards de neurones !",
    "masse volumique": "MASSE VOLUMIQUE : Formule = masse / volume. Rho = m / V. m en grammes (balance), V en cm³ (éprouvette). Ex : 100g / 100 cm³ = 1 g/cm³ = eau. Huile 0,9 flotte, Fer 7,8 coule. Si < 1 ça flotte, si > 1 ça coule !",
    "atome": "ATOME : Proton (+), Neutron (0), Electron (-). Tout est fait d'atomes !",
    "molecule": "MOLECULE : Plusieurs atomes ensemble. Ex : H2O = eau (2 hydrogène + 1 oxygène). CO2 = dioxyde de carbone.",
    "tableau periodique": "TABLEAU PERIODIQUE : 118 éléments : H, O, C, Fe (fer), Au (or)... Créé par Mendeleïev en 1869.",
    "oxygene": "OXYGENE : O2. On respire O2, on rejette CO2. 21% de l'air = oxygène.",
    "chimie": "CHIMIE : Etude de la matière. Atome = brique, Molécule = plusieurs atomes. H2O = eau, CO2 = dioxyde de carbone.",
    "electricite": "ELECTRICITE : Tension en Volts (V), Intensité en Ampères (A), Puissance en Watts (W). Formule : P = U x I. En série : si une lampe grille, tout s'éteint. En parallèle : les autres restent allumées.",
    "vitesse": "VITESSE : Vitesse = distance / temps. v = d / t. Ex : 100m en 10 sec = 10 m/s = 36 km/h. Pour m/s → km/h : x 3,6.",
    "energie": "ENERGIE : Cinétique (mouvement), potentielle (hauteur), thermique (chaleur), électrique, solaire, éolienne. On ne crée pas d'énergie, on la transforme.",
    "force": "FORCE : En Newtons (N). Poids = masse x gravité. Ex : 50 kg sur Terre = 500 N. La force fait bouger les objets.",
    "adn": "ADN : Ton code génétique, dans toutes tes cellules. Il dit si tu as les yeux bleus, bruns... 50% père, 50% mère.",
    "trou noir": "TROU NOIR : Objet tellement lourd que même la lumière ne peut pas sortir. Au centre de notre galaxie, un trou noir de 4 millions de fois la masse du Soleil.",
    "big bang": "BIG BANG : Début de l'univers il y a 13,8 milliards d'années. Tout était concentré en un point, puis ça a explosé.",
    "mars": "MARS : Planète rouge. Un jour sur Mars = 24h37. Robots : Perseverance, 【entity-Curiosity¦canonical_name=Curiosity】.",
    "iss": "ISS : Station spatiale à 400 km, 28 000 km/h. 16 levers de soleil par jour !",
    "systeme solaire": "SYSTEME SOLAIRE : 8 planètes : Mercure, Vénus, Terre, Mars, Jupiter, Saturne, Uranus, Neptune. Astuce : Me Voici, Tout Mouillé, J'ai Suivi Un Nuage.",
    "boucle": "BOUCLE : for i in range(1,6): print(i) -> affiche 1,2,3,4,5",
    "variable": "VARIABLE : age = 13. Boîte qui stocke une valeur.",
    "condition": "CONDITION : if age >= 18: print('Majeur') else: print('Mineur')",
    "fonction": "FONCTION : def dire_bonjour(): print('Bonjour'). Tu l'appelles avec dire_bonjour(). Ca évite de recopier.",
    "liste": "LISTE : notes = [12, 15, 18]. notes[0] = 12. Tu peux ajouter : notes.append(20).",
    "python": "PYTHON : Langage facile, celui de ton agent. Créé en 1991. Utilisé pour l'IA, les sites, les jeux.",
    "html": "HTML : Squelette d'un site. <h1>Titre</h1> <p>Texte</p> <img src='photo.jpg'>",
    "css": "CSS : Style d'un site : couleurs, tailles, positions. Ex : body { background-color: black; }",
    "javascript": "JAVASCRIPT : Langage pour rendre un site interactif : boutons, animations, jeux. HTML = squelette, CSS = style, JS = cerveau.",
    " messi": " MESSI : Argentin, 8 Ballons d'Or, meilleur de tous les temps. Barça, PSG, Miami. Coupe du Monde 2022.",
    " ronaldo": " CR7 : Portugais, 5 Ballons d'Or, Real, Man United, Al-Nassr. Meilleur buteur de l'histoire.",
    " mbappe": " MBAPPE : Français, 36 km/h ! Real Madrid, Champion du monde 2018.",
    "coupe du monde": "COUPE DU MONDE : Tous les 4 ans. 2022 = Argentine. 2026 = USA / Canada / Mexique. 48 équipes !",
    " minecraft": " MINECRAFT : Jeu de cubes, 300M de copies ! Construis, mine, survis aux creepers.",
    " fortnite": " FORTNITE : Battle Royale 100 joueurs, dernier vivant gagne.",
    " roblox": " ROBLOX : Des millions de jeux créés par les joueurs.",
    "gta": "GTA V : 190M de copies ! Monde ouvert.",
    "tour eiffel": "TOUR EIFFEL : Paris, 330m, 1889, Gustave Eiffel. 7M de visiteurs par an. Elle grandit de 15 cm en été !",
    " titanic": " TITANIC : Coule en 1912, iceberg. Film 1997, 11 Oscars.",
    "millionnaire": "COMMENT DEVENIR MILLIONNAIRE ? : 1. Salarié + investissement : 1000 CHF / mois en bourse (ETF), en 30 ans tu as 1M. 2. Entrepreneur : tu crées un business. 3. Créateur : YouTube, TikTok. Conseils : Apprends une compétence, épargne 20%, investis tôt.",
    "salaire": "SALAIRE : En Suisse : salaire moyen = 6500 CHF / mois. Serveur = 4500 CHF, Enseignant = 7000 CHF, Médecin = 12 000 CHF, Développeur = 8000 CHF.",
    "gagner de l argent": "COMMENT GAGNER DE L'ARGENT A 13 ANS ? : Petits services (tondre, promener chien) = 10-20 CHF. Vendre ce que tu n'utilises plus. Créer un projet (agent IA) et montrer à tes parents, ils peuvent facturer pour toi. A 16 ans, tu peux t'inscrire comme indépendant AVS.",
    "plus grand animal": "PLUS GRAND ANIMAL : Baleine bleue ! 30m, 200 tonnes, coeur = 600 kg !",
    "plus rapide": "PLUS RAPIDE : Guépard = 110 km/h sur terre. Faucon pèlerin = 390 km/h en piqué !",
    "chien": "CHIEN : Meilleur ami de l'homme depuis 15 000 ans. 400 races. Il comprend 150 mots.",
    "chat": "CHAT : Il dort 16h par jour ! Il peut sauter 6x sa hauteur. Il retombe toujours sur ses pattes.",
    "conseil pour reviser": "CONSEIL POUR REVISER : 1. Pomodoro : 25 min de travail, 5 min de pause. 2. Teste-toi, ne relis pas. 3. Explique à quelqu'un. 4. Dors bien. 5. Pas de téléphone pendant que tu révises.",
}

AVIONS = {
    "f-22": "F-22 Raptor (USA) - LE PLUS PERFORMANT EN COMBAT. Mach 2.25 (2400 km/h). Furtif, jamais battu.",
    " f-35": " F-35 Lightning II (USA) - LE PLUS MODERNE. Mach 1.6. La Suisse en a acheté 36 !",
    "rafale": "Rafale (France). Mach 1.8. Polyvalent : air, sol, mer.",
    "sr-71": "SR-71 Blackbird. Mach 3.3 = 3500 km/h ! Plus rapide de tous les temps.",
    "concorde": "Concorde : Paris-New York en 3h30. Mach 2. Arrêté en 2003.",
    "f-16": "F-16. Mach 2.0. Plus produit : 4600 exemplaires !",
    "f-15": "F-15 Eagle. Mach 2.5 ! 104 victoires à 0 défaite.",
}

TRAIN_FACILE = [("C'est quoi 2+2 ?", "4"), ("C'est quoi 5x2 ?", "10"), ("C'est quoi la capitale de la France ?", "paris"), ("C'est quoi 3x3 ?", "9")]
TRAIN_MOYEN = [("C'est quoi 7x8 ?", "56"), ("C'est quoi la capitale du Japon ?", "tokyo"), ("C'est quoi 15+25 ?", "40"), ("Qui a gagné la Coupe du Monde 2022 ?", "argentine"), ("C'est quoi la formule de la masse volumique ?", "m/v"), ("Qui a chanté Solitaire ?", "werenoi")]
TRAIN_DIFFICILE = [("C'est quoi 12x12 ?", "144"), ("C'est quoi la capitale de l'Australie ?", "canberra"), ("C'est quoi 144 / 12 ?", "12"), ("Combien de Ballons d'Or a Messi ?", "8"), ("En quelle année a coulé le Titanic ?", "1912")]

def toutes_tables():
    txt = "TOUTES LES TABLES DE MULTIPLICATION 1 à 12 :\n\n"
    for n in range(1, 13):
        txt += f"Table de {n} : " + ", ".join([f"{n}x{i}={n*i}" for i in range(1, 11)]) + "\n\n"
    return txt

def table_division(n):
    txt = f"TABLE DE DIVISION DE {n} :\n"
    for i in range(1, 11):
        txt += f"{n*i} / {n} = {i}  |  "
    return txt

def calculer(q):
    try:
        txt = q.lower().replace("calcule", "").replace("calcul", "").replace("=", "").replace("?", "").strip()
        txt = txt.replace("x", "*").replace("×", "*").replace(",", ".")
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in txt) or txt == "":
            return None
        res = eval(txt)
        return f"🧮 Calcul : {q} = {res} ! Bravo !"
    except:
        return None

def trouver(q_orig):
    q_low = nettoyer(q_orig)
    q_brut = q_orig.lower().strip()
    if q_low in ["stop", "arrete", "arreter", "stop entrainement"]:
        st.session_state.mode_train = False
        st.session_state.train_q = None
        return f"Ok, entraînement arrêté ! 🏁 Ton score final : {st.session_state.score}/{st.session_state.total_quiz} ! 🔥 Meilleur streak : {st.session_state.best_streak} ! Bravo ! 💪"
    if st.session_state.mode_train and st.session_state.train_q is not None:
        bonne = nettoyer(st.session_state.train_a)
        st.session_state.total_quiz += 1
        if bonne in q_low or q_low in bonne or q_low == bonne:
            st.session_state.score += 1
            st.session_state.streak += 1
            if st.session_state.streak > st.session_state.best_streak:
                st.session_state.best_streak = st.session_state.streak
            rep = f"✅ BRAVO ! Bonne réponse ! C'était bien '{st.session_state.train_a}' ! 🎉 Score : {st.session_state.score}/{st.session_state.total_quiz} | 🔥 Streak : {st.session_state.streak}"
        else:
            st.session_state.streak = 0
            rep = f"❌ Pas tout à fait... La bonne réponse c'était '{st.session_state.train_a}'. C'est pas grave, on apprend ! Score : {st.session_state.score}/{st.session_state.total_quiz}"
        if st.session_state.niveau == "facile":
            nq, na = random.choice(TRAIN_FACILE)
        elif st.session_state.niveau == "difficile":
            nq, na = random.choice(TRAIN_DIFFICILE)
        else:
            nq, na = random.choice(TRAIN_MOYEN)
        st.session_state.train_q = nq
        st.session_state.train_a = na
        return rep + f"\n\n🎯 Question suivante ({st.session_state.niveau}) : {nq}"
    if "entrainement facile" in q_low:
        st.session_state.mode_train = True
        st.session_state.niveau = "facile"
        nq, na = random.choice(TRAIN_FACILE)
        st.session_state.train_q = nq
        st.session_state.train_a = na
        return f"🎯 C'EST PARTI - ENTRAINEMENT FACILE ! 🟢 Ecris 'stop' pour arrêter.\n\nPremière question : {nq}"
    if "entrainement difficile" in q_low:
        st.session_state.mode_train = True
        st.session_state.niveau = "difficile"
        nq, na = random.choice(TRAIN_DIFFICILE)
        st.session_state.train_q = nq
        st.session_state.train_a = na
        return f"🎯 C'EST PARTI - ENTRAINEMENT DIFFICILE ! 🔴 Pour les champions !\n\nPremière question : {nq}"
    if "entraine" in q_low or "entrainement" in q_low or q_low == "quiz moi":
        st.session_state.mode_train = True
        st.session_state.niveau = "moyen"
        nq, na = random.choice(TRAIN_MOYEN)
        st.session_state.train_q = nq
        st.session_state.train_a = na
        return f"🎯 C'EST PARTI POUR L'ENTRAINEMENT MOYEN ! Je te pose des questions, tu réponds, je te corrige ! Ecris 'stop' pour arrêter.\n\nPremière question : {nq}"
    if "mon score" in q_low or q_low == "score":
        return f"🏆 Ton score : {st.session_state.score} / {st.session_state.total_quiz} ! 🔥 Streak : {st.session_state.streak} | Best : {st.session_state.best_streak} ! Ecris 'Entraine moi' pour continuer !"
    if q_brut.startswith("apprends") or q_brut.startswith("apprend") or "retient que" in q_brut:
        try:
            texte = q_brut.replace("apprends :", "").replace("apprends", "").replace("apprend :", "").replace("apprend", "").replace("retient que", "").strip()
            if "=" in texte:
                cle, val = texte.split("=", 1)
                cle = nettoyer(cle)
                val = val.strip()
                st.session_state.learned[cle] = val
                return f"✅ MERCI ! J'ai appris ! 🧠 Maintenant je sais que '{cle}' = '{val}' ! J'ai appris {len(st.session_state.learned)} choses !"
            else:
                st.session_state.learned[nettoyer(texte)] = texte
                return f"✅ Merci ! J'ai retenu : '{texte}' ! 🧠"
        except:
            return "Pour m'apprendre, écris : Apprends : c'est quoi le foot = le foot c'est un sport avec un ballon"
    if "montre ce que tu as appris" in q_low or "ce que tu as appris" in q_low:
        if len(st.session_state.learned) == 0:
            return "Je n'ai encore rien appris... 😅 Apprends-moi un truc : Apprends : c'est quoi le foot = ..."
        txt = f"🧠 VOICI CE QUE TU M'AS APPRIS ({len(st.session_state.learned)} choses) :\n\n"
        for k, v in st.session_state.learned.items():
            txt += f"- {k} = {v}\n"
        return txt
    for cle, val in st.session_state.learned.items():
        if cle in q_low or q_low in cle:
            return f"🧠 Ce que TU m'as appris : {val} (merci !)"
    if any(c in q_brut for c in ["+", "x", "*", "/", "-"]) and any(c.isdigit() for c in q_brut):
        calc = calculer(q_brut)
        if calc:
            return calc
    for cle, rep in BASES.items():
        if nettoyer(cle) in q_low or q_low == nettoyer(cle):
            return rep
    if "merci" in q_low:
        return BASES["merci"]
    if "bonjour" in q_low or "salut" in q_low or "slt" in q_low or "bonjoure" in q_low:
        return BASES["bonjour"]
    if "blague" in q_low:
        return random.choice(BLAGUES)
    if "motive" in q_low or "motivation" in q_low:
        return random.choice(MOTIVATIONS)
    if "conseil" in q_low and "revis" in q_low:
        return TOUT["conseil pour reviser"]
    if "heure" in q_low:
        return BASES["quelle heure"]
    if "date" in q_low:
        return BASES["quelle date"]
    if "traduis" in q_low or "traduction" in q_low or "en anglais" in q_low or "en allemand" in q_low or "en espagnol" in q_low or "en italien" in q_low:
        for cle, rep in TRADUCTIONS.items():
            if nettoyer(cle) in q_low:
                return rep
        return "Je peux traduire : bonjour, merci, au revoir, école, chat, chien, maison, pomme, eau en anglais / allemand / espagnol / italien. Essaie : Traduis bonjour en anglais"
    q = q_low
    for mot in ["c est quoi", "c est", "comment", "pourquoi", "donne moi", "c est qui", "qui est", "quel est", "quelle est", "comment calculer", "c koi", "c quoi"]:
        q = q.replace(mot, " ")
    q = " ".join(q.split())
    if "toutes les tables" in q or "toutes tables" in q:
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
            return "Table de " + str(n) + " : " + res
        except:
            pass
    if "performant" in q or "meilleur avion" in q:
        return "AVION LE PLUS PERFORMANT ? 1. Combat : F-22 Raptor. 2. Moderne : F-35. 3. Vitesse : SR-71 - 3500 km/h. Mon choix : F-22 = le roi."
    if "capitale" in q:
        for pays, cap in CAPITALES.items():
            if nettoyer(pays) in q:
                return "Capitale de " + pays.capitalize() + " = " + cap
        return "J'ai plein de capitales ! Essaie : capitale du Japon..."
    for cle, rep in PC.items():
        if nettoyer(cle) in q:
            return rep
    for cle, rep in CHANTEURS.items():
        if nettoyer(cle) in q:
            return rep
    for cle, rep in AVIONS.items():
        if nettoyer(cle) in q:
            return rep
    for mot, rep in TOUT.items():
        if nettoyer(mot) in q:
            return rep
    for pays, cap in CAPITALES.items():
        if q == nettoyer(pays):
            return pays.capitalize() + " -> Capitale = " + cap
    return f"🤔 Hmm, je ne connais pas encore : '{q_orig}'...\n\nMais tu peux M'APPRENDRE ! Ecris :\n\nApprends : {q_orig} = ta réponse ici\n\n💡 Tu voulais peut-être dire :\n- Français → Grammaire → C'est quoi le COD ?\n- Maths → Géométrie → C'est quoi Pythagore ?\n- C'est qui Werenoi ?\n- Entraine moi\n\nChoisis ta matière → genre en haut, ou apprends-moi ! 🧠"

if "auto_q" in st.session_state and st.session_state.auto_q:
    q_auto = st.session_state.auto_q
    st.session_state.auto_q = ""
    r_auto = trouver(q_auto)
    st.session_state.messages.append({"role": "assistant", "content": r_auto})
    with st.chat_message("assistant"):
        st.write(r_auto)

if question := st.chat_input("Pose ta question, ou choisis Matière → Genre en haut !"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        r = trouver(question)
        st.write(r)
    st.session_state.messages.append({"role": "assistant", "content": r})
