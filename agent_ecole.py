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

MATIERES_GENRES = {
    "📐 Maths": {
        "📐 Géométrie": ["C'est quoi le théorème de Pythagore ?", "C'est quoi Thales ?", "C'est quoi l'aire ?", "C'est quoi le perimetre ?", "C'est quoi le volume ?", "C'est quoi un angle ?"],
        "🧮 Calcul": ["Table de 7", "Toutes les tables de multiplication", "Table de division de 8", "C'est quoi la moyenne ?", "Calcule 12+8"],
        "🍕 Fractions / %": ["C'est quoi une fraction ?", "C'est quoi le pourcentage ?", "C'est quoi une equation ?"],
    },
    "🇫🇷 Français": {
        "📖 Grammaire": ["C'est quoi le COD ?", "C'est quoi le sujet ?", "C'est quoi un adjectif ?", "C'est quoi le pluriel ?", "C'est quoi le verbe ?"],
        "✍️ Verbes les plus connus": ["Conjugue ETRE", "Conjugue AVOIR", "Conjugue ALLER", "Conjugue FAIRE", "Conjugue DIRE", "Conjugue POUVOIR", "Conjugue VOULOIR", "Conjugue SAVOIR", "Conjugue DEVOIR", "Conjugue VENIR", "Conjugue VOIR", "Conjugue PRENDRE", "Conjugue METTRE", "Conjugue DONNER", "Conjugue PARLER", "Conjugue MANGER", "Conjugue DORMIR", "Conjugue ECRIRE", "Conjugue LIRE", "Conjugue PARTIR"],
        "📝 Orthographe": ["C'est quoi le pluriel ?", "C'est quoi a / à ?", "C'est quoi et / est ?", "C'est quoi son / sont ?"],
        "📚 Vocabulaire": ["C'est quoi un synonyme ?", "C'est quoi un antonyme ?", "C'est quoi un homonyme ?"],
    },
    "🇩🇪 Allemand": {
        "📖 Grammaire": ["C'est quoi der die das ?", "C'est quoi l'accusatif ?", "C'est quoi le datif ?"],
        "✍️ Verbes les plus connus": ["Conjugue SEIN", "Conjugue HABEN", "Conjugue GEHEN", "Conjugue MACHEN", "Conjugue KOMMEN", "Conjugue SEHEN", "Conjugue SPRECHEN", "Conjugue ESSEN", "Conjugue TRINKEN", "Conjugue LERNEN", "Conjugue WOHNEN", "Conjugue SPIELEN", "Conjugue ARBEITEN", "Conjugue KÖNNEN", "Conjugue WOLLEN", "Conjugue MÜSSEN", "Conjugue WISSEN", "Conjugue GEBEN", "Conjugue NEHMEN", "Conjugue SCHREIBEN"],
        "🌍 Vocabulaire": ["Traduis bonjour en allemand", "Traduis merci en allemand", "Traduis ecole en allemand", "Traduis chien en allemand"],
    },
    "🇬🇧 Anglais": {
        "📖 Grammaire": ["C'est quoi le present simple ?", "C'est quoi le present perfect ?", "C'est quoi le present continu ?"],
        "✍️ Verbes les plus connus": ["Conjugue TO BE", "Conjugue TO HAVE", "Conjugue TO GO", "Conjugue TO DO", "Conjugue TO SAY", "Conjugue TO SEE", "Conjugue TO COME", "Conjugue TO GET", "Conjugue TO MAKE", "Conjugue TO TAKE", "Conjugue TO GIVE", "Conjugue TO KNOW", "Conjugue TO THINK", "Conjugue TO SPEAK", "Conjugue TO EAT", "Conjugue TO DRINK", "Conjugue TO PLAY", "Conjugue TO LIVE", "Conjugue TO LOVE", "Conjugue TO WANT"],
        "🌍 Vocabulaire": ["Traduis bonjour en anglais", "Traduis merci en anglais", "Traduis ecole en anglais", "Traduis chien en anglais"],
    },
    "🇪🇸 Espagnol": {
        "📖 Grammaire": ["C'est quoi ser et estar ?", "C'est quoi el / la / los / las ?", "C'est quoi le pluriel en espagnol ?"],
        "✍️ Verbes les plus connus": ["Conjugue SER", "Conjugue ESTAR", "Conjugue TENER", "Conjugue IR", "Conjugue HACER", "Conjugue DECIR", "Conjugue PODER", "Conjugue QUERER", "Conjugue SABER", "Conjugue VENIR", "Conjugue VER", "Conjugue HABLAR", "Conjugue COMER", "Conjugue VIVIR", "Conjugue JUGAR"],
        "🌍 Vocabulaire": ["Traduis bonjour en espagnol", "Traduis merci en espagnol", "Traduis ecole en espagnol"],
    },
    "🇮🇹 Italien": {
        "📖 Grammaire": ["C'est quoi il / lo / la ?", "C'est quoi le pluriel en italien ?"],
        "✍️ Verbes les plus connus": ["Conjugue ESSERE", "Conjugue AVERE", "Conjugue ANDARE", "Conjugue FARE", "Conjugue DIRE", "Conjugue POTERE", "Conjugue VOLERE", "Conjugue SAPERE", "Conjugue VENIRE", "Conjugue VEDERE", "Conjugue PARLARE", "Conjugue MANGIARE", "Conjugue GIOCARE"],
        "🌍 Vocabulaire": ["Traduis bonjour en italien", "Traduis merci en italien"],
    },
    "📜 Histoire / Géo": {
        "📜 Histoire": ["C'est quoi la 2eme Guerre ?", "C'est quoi la 1ere Guerre ?", "C'est quoi la Revolution ?", "C'est quoi Rome ?", "C'est quoi le Moyen Age ?", "C'est quoi l'Egypte ?", "C'est quoi Napoleon ?"],
        "🌍 Géographie": ["C'est quoi les continents ?", "C'est quoi les oceans ?", "Capitale du Japon ?", "Capitale de la France ?"],
    },
    "🔬 Sciences": {
        "🧬 Biologie": ["C'est quoi la photosynthese ?", "C'est quoi le coeur ?", "C'est quoi l'ADN ?"],
        "🌍 Terre / Espace": ["C'est quoi un volcan ?", "C'est quoi les saisons ?", "C'est quoi la foudre ?", "C'est quoi le systeme solaire ?"],
        "⚡ Physique": ["C'est quoi la gravite ?", "Comment calculer la masse volumique ?", "C'est quoi la vitesse ?"],
    },
    "🧪 Chimie / Physique": {
        "⚛️ Chimie": ["C'est quoi un atome ?", "C'est quoi l'oxygene ?", "C'est quoi la chimie ?"],
        "⚡ Physique": ["C'est quoi l'electricite ?", "C'est quoi la masse volumique ?", "C'est quoi la vitesse ?"],
    },
    "💻 Code": {
        "🧠 Bases": ["C'est quoi une variable ?", "C'est quoi une boucle ?", "C'est quoi une condition ?", "C'est quoi une fonction ?"],
        "🌐 Langages": ["C'est quoi Python ?", "C'est quoi HTML ?", "C'est quoi CSS ?"],
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
    "✈️ Avions": ["Quel est l'avion de chasse le plus performant ?", "C'est quoi le F-22 ?", "C'est quoi le 【entity-F-35¦canonical_name=F-35】 ?", "C'est quoi le Rafale ?"],
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
        st.subheader(f"3️⃣ Verbes / Questions : {st.session_state.matiere} → {st.session_state.genre} - Clique :")
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
        st.info(f"👆 Choisis un genre dans {st.session_state.matiere} pour voir les verbes / questions")
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
    st.session_state.messages = [{"role": "assistant", "content": "Salut ! 👋 Moi c'est Agent IA V5 ! Maintenant pour les langues : choisis MATIERE → VERBES ! Ex : Français → Verbes les plus connus → Conjugue ETRE. Pareil pour Allemand, Anglais, Espagnol, Italien ! Essaie !"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

def nettoyer(txt):
    txt = txt.lower().strip()
    txt = txt.replace("é", "e").replace("è", "e").replace("ê", "e").replace("à", "a").replace("ç", "c").replace("ô", "o").replace("î", "i").replace("û", "u").replace("ö", "o").replace("ü", "u").replace("ä", "a")
    txt = re.sub(r"[^a-z0-9 +*/\-=?.]", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt

BASES = {
    "bonjour": "Bonjour ! 👋 Comment tu vas ? Choisis ta matière en haut : Français → Verbes les plus connus, ou Allemand → Verbes...",
    "salut": "Salut ! 👋 Ca va ? Choisis : Français → Verbes, Allemand → Verbes, Anglais → Verbes...",
    "slt": "Slt ! 👋 Ca va ?",
    "yo": "Yo ! 👋 Ca va ?",
    "coucou": "Coucou ! 👋 Ca va bien ?",
    "hello": "Hello ! 👋 Ca va ?",
    "merci": "De rien ! 😊 Avec plaisir ! Tu as un autre verbe à conjuguer ?",
    "mrc": "De rien ! 😊",
    "ca va": "Ca va super bien merci ! Et toi ? Tu révises quels verbes ?",
    "au revoir": "Au revoir ! 👋 A très vite ! Reviens réviser tes verbes quand tu veux ! 😊",
    "bye": "Bye ! 👋 A très vite !",
    "t appelles comment": "Moi je m'appelle Agent IA V5 ! 🤖 Et toi ?",
    "qui es tu": "Moi je suis Agent IA V5 ! 🤖 Je conjugue tous les verbes les plus connus en Français, Allemand, Anglais, Espagnol, Italien !",
    "aide moi": "Oui bien sûr ! 😊 Dis-moi : c'est pour quelle langue et quel verbe ? Ex : Français → Conjugue ETRE, ou Allemand → Conjugue SEIN",
    "j ai pas compris": "T'inquiète ! 😊 Dis-moi quel verbe tu n'as pas compris, je te réexplique plus simplement.",
    "quelle heure": f"Il est {datetime.datetime.now().strftime('%H:%M')} ! ⏰",
    "quelle date": f"On est le {datetime.datetime.now().strftime('%d/%m/%Y')} ! 📅",
}

BLAGUES = ["Pourquoi les plongeurs plongent-ils toujours en arrière ? Parce que sinon, ils tombent dans le bateau ! 😂","Que dit un zéro à un huit ? Belle ceinture ! 😂","Pourquoi les maths sont tristes ? Parce qu'elles ont trop de problèmes ! 😂","Pourquoi les poissons n'aiment pas jouer au foot ? Parce qu'ils ont peur des filets ! 😂"]
MOTIVATIONS = ["Tu peux le faire ! 💪 Chaque erreur, c'est une leçon. Ne lâche rien !","N'abandonne jamais ! 🔥 10 minutes par jour, et dans 1 mois tu seras trop fort !"]
TRADUCTIONS = {"bonjour en anglais": "Bonjour en anglais = Hello / Good morning ! 🇬🇧","bonjour en allemand": "Bonjour en allemand = Hallo / Guten Tag ! 🇩🇪","bonjour en espagnol": "Bonjour en espagnol = Hola / Buenos dias ! 🇪🇸","bonjour en italien": "Bonjour en italien = Ciao / Buongiorno ! 🇮🇹","merci en anglais": "Merci en anglais = Thank you / Thanks ! 🇬🇧","merci en allemand": "Merci en allemand = Danke ! 🇩🇪","merci en espagnol": "Merci en espagnol = Gracias ! 🇪🇸","merci en italien": "Merci en italien = Grazie ! 🇮🇹","au revoir en anglais": "Au revoir en anglais = Goodbye / Bye ! 🇬🇧","ecole en anglais": "Ecole en anglais = School ! 🇬🇧","chat en anglais": "Chat en anglais = Cat ! 🐱","chien en anglais": "Chien en anglais = Dog ! 🐶","maison en anglais": "Maison en anglais = House ! 🏠","ecole en allemand": "Ecole en allemand = Schule ! 🇩🇪","chien en allemand": "Chien en allemand = Hund ! 🇩🇪","ecole en espagnol": "Ecole en espagnol = Escuela ! 🇪🇸"}
CAPITALES = {"france": "Paris - Tour Eiffel, Louvre.","suisse": "Berne - Capitale de la Suisse depuis 1848.","allemagne": "Berlin - Mur de Berlin.","italie": "Rome - Colisée, Vatican.","espagne": "Madrid - 【entity-Real Madrid¦canonical_name=Real Madrid】.","angleterre": "Londres - Big Ben.","japon": "Tokyo - Sushi, Manga.","usa": "Washington D.C. - Maison Blanche.","canada": "Ottawa.","chine": "Pékin - Grande Muraille.","russie": "Moscou - Place Rouge.","bresil": "Brasilia - Rio = plus connue.","inde": "New Delhi - Taj Mahal.","australie": "Canberra - Sydney = plus connue.","egypte": "Le Caire - Pyramides.","maroc": "Rabat","portugal": "Lisbonne - 【entity-Cristiano Ronaldo¦canonical_name=Cristiano Ronaldo】 !","belgique": "Bruxelles - Frites !"}
PC = {
    "rapport qualite prix": "MEILLEUR RAPPORT PC 2026 : GAGNANT 1300 CHF : RTX 5070 + Ryzen 7 7800X3D + 32 Go + SSD 1 To = 1300 CHF. 1440p Ultra 180 FPS !",
    "pc 900": "PC 900 CHF : RTX 4060 + Ryzen 5 7600 + 16 Go + SSD 1 To = 900 CHF. 【entity-Fortnite¦canonical_name=Fortnite】 144 FPS !",
    "pc 1300": "PC 1300 CHF : RTX 5070 + Ryzen 7 7800X3D + 32 Go + SSD 1 To = 1300 CHF. 1440p Ultra 180 FPS !",
    "pc 2000": "PC 2000 CHF : RTX 5070 Ti + Ryzen 7 9800X3D + 32 Go + SSD 2 To = 2000 CHF. 240 FPS !",
    "meilleure gpu": "MEILLEURE GPU : 1. RTX 5090 - 32 Go, 2500 CHF. Meilleur rapport = RTX 5070 (600 CHF) !",
    "gpu": "GPU = Carte Graphique. Meilleure = RTX 5090. Meilleur rapport = RTX 5070.",
    "meilleur cpu": "MEILLEUR CPU : Meilleur rapport = Ryzen 7 7800X3D (350 CHF) !",
    "cpu": "CPU = Processeur. Meilleur rapport = Ryzen 7 7800X3D.",
    "meilleur ssd": "MEILLEUR SSD : 【entity-Samsung¦canonical_name=Samsung】 990 PRO 2 To. Meilleur rapport = WD Black 1 To (70 CHF).",
    "meilleure ram": "MEILLEURE RAM : 32 Go DDR5 6000 MHz CL30.",
}
CHANTEURS = {
    "werenoi": "WERENOI : Rappeur français, le plus écouté en France en 2024 et 2025 ! Albums : Pyramide, Diamant Noir. Sons : Solitaire, Ciao.",
    "ninho": "NINHO : Rappeur français, record de disques d'or et de diamant ! Albums : Jefe, NI. Son : Lettre à une femme.",
    "jul": "JUL : Rappeur de Marseille, le plus productif ! 2 albums par an.",
    " 【entity-gazo¦canonical_name=Gazo】": " 【entity-GAZO¦canonical_name=Gazo】 : Roi de la drill en France ! Album : KMT. Feat : La Melo avec 【entity-Tiakola¦canonical_name=Tiakola】.",
    " 【entity-tiakola¦canonical_name=Tiakola】": " 【entity-TIAKOLA¦canonical_name=Tiakola】 : Chanteur / rappeur, membre de 【entity-4Keus¦canonical_name=4Keus】. Album : Melo.",
    " 【entity-pnl¦canonical_name=PNL】": " 【entity-PNL¦canonical_name=PNL】 : Duo de frères Ademo et N.O.S. Albums : Dans la légende, Deux frères.",
    "sdm": "SDM : Rappeur français, signé chez Booba. Son : Bolide allemand avec Ninho.",
    " 【entity-drake¦canonical_name=Drake】": " 【entity-DRAKE¦canonical_name=Drake】 : Rappeur canadien, le plus streamé au monde ! Son : God's Plan.",
    " 【entity-taylor swift¦canonical_name=TAYLOR SWIFT】": " 【entity-TAYLOR SWIFT¦canonical_name=TAYLOR SWIFT】 : Chanteuse américaine, la plus écoutée au monde ! 14 Grammy.",
    " 【entity-eminem¦canonical_name=EMINEM】": " 【entity-EMINEM¦canonical_name=EMINEM】 : Rappeur américain, légende. Son : Lose Yourself, Rap God.",
}

# ============ VERBES - CONJUGAISONS COMPLETES ============
VERBES = {
    # FRANCAIS
    "etre": "🇫🇷 ETRE - VERBE LE PLUS IMPORTANT\n\n📌 Sens : être = exister, décrire. Ex : Je suis content, Il est à l'école.\n\n✅ PRÉSENT : je suis, tu es, il/elle est, nous sommes, vous êtes, ils/elles sont\n✅ PASSÉ COMPOSÉ : j'ai été, tu as été, il a été, nous avons été, vous avez été, ils ont été\n✅ IMPARFAIT : j'étais, tu étais, il était, nous étions, vous étiez, ils étaient\n✅ FUTUR : je serai, tu seras, il sera, nous serons, vous serez, ils seront\n\n💡 Astuce : ETRE sert pour le passé composé avec 14 verbes (aller, venir, partir...) : Je suis allé.",
    "avoir": "🇫🇷 AVOIR - VERBE LE PLUS IMPORTANT\n\n📌 Sens : posséder. Ex : J'ai 13 ans, J'ai un chien.\n\n✅ PRÉSENT : j'ai, tu as, il a, nous avons, vous avez, ils ont\n✅ PASSÉ COMPOSÉ : j'ai eu, tu as eu, il a eu, nous avons eu, vous avez eu, ils ont eu\n✅ IMPARFAIT : j'avais, tu avais, il avait, nous avions, vous aviez, ils avaient\n✅ FUTUR : j'aurai, tu auras, il aura, nous aurons, vous aurez, ils auront\n\n💡 Astuce : AVOIR sert pour presque tous les passés composés : J'ai mangé, J'ai joué.",
    "aller": "🇫🇷 ALLER\n\n📌 Sens : se déplacer. Ex : Je vais à l'école.\n\n✅ PRÉSENT : je vais, tu vas, il va, nous allons, vous allez, ils vont\n✅ PASSÉ COMPOSÉ : je suis allé(e), tu es allé(e), il est allé, nous sommes allés, vous êtes allés, ils sont allés\n✅ IMPARFAIT : j'allais, tu allais, il allait, nous allions, vous alliez, ils allaient\n✅ FUTUR : j'irai, tu iras, il ira, nous irons, vous irez, ils iront",
    "faire": "🇫🇷 FAIRE\n\n📌 Sens : créer, réaliser. Ex : Je fais mes devoirs.\n\n✅ PRÉSENT : je fais, tu fais, il fait, nous faisons, vous faites, ils font\n✅ PASSÉ COMPOSÉ : j'ai fait, tu as fait, il a fait, nous avons fait, vous avez fait, ils ont fait\n✅ IMPARFAIT : je faisais, tu faisais, il faisait, nous faisions, vous faisiez, ils faisaient\n✅ FUTUR : je ferai, tu feras, il fera, nous ferons, vous ferez, ils feront",
    "dire": "🇫🇷 DIRE\n\n📌 Sens : parler. Ex : Je dis bonjour.\n\n✅ PRÉSENT : je dis, tu dis, il dit, nous disons, vous dites, ils disent\n✅ PASSÉ COMPOSÉ : j'ai dit, tu as dit, il a dit, nous avons dit, vous avez dit, ils ont dit\n✅ IMPARFAIT : je disais, tu disais, il disait, nous disions, vous disiez, ils disaient\n✅ FUTUR : je dirai, tu diras, il dira, nous dirons, vous direz, ils diront",
    "pouvoir": "🇫🇷 POUVOIR\n\n📌 Sens : être capable. Ex : Je peux jouer.\n\n✅ PRÉSENT : je peux, tu peux, il peut, nous pouvons, vous pouvez, ils peuvent\n✅ PASSÉ COMPOSÉ : j'ai pu, tu as pu, il a pu, nous avons pu, vous avez pu, ils ont pu\n✅ IMPARFAIT : je pouvais, tu pouvais, il pouvait, nous pouvions, vous pouviez, ils pouvaient\n✅ FUTUR : je pourrai, tu pourras, il pourra, nous pourrons, vous pourrez, ils pourront",
    "vouloir": "🇫🇷 VOULOIR\n\n📌 Sens : désirer. Ex : Je veux jouer.\n\n✅ PRÉSENT : je veux, tu veux, il veut, nous voulons, vous voulez, ils veulent\n✅ PASSÉ COMPOSÉ : j'ai voulu, tu as voulu, il a voulu, nous avons voulu, vous avez voulu, ils ont voulu\n✅ IMPARFAIT : je voulais, tu voulais, il voulait, nous voulions, vous vouliez, ils voulaient\n✅ FUTUR : je voudrai, tu voudras, il voudra, nous voudrons, vous voudrez, ils voudront",
    "savoir": "🇫🇷 SAVOIR\n\n📌 Sens : connaître un fait. Ex : Je sais nager.\n\n✅ PRÉSENT : je sais, tu sais, il sait, nous savons, vous savez, ils savent\n✅ PASSÉ COMPOSÉ : j'ai su, tu as su, il a su, nous avons su, vous avez su, ils ont su\n✅ IMPARFAIT : je savais, tu savais, il savait, nous savions, vous saviez, ils savaient\n✅ FUTUR : je saurai, tu sauras, il saura, nous saurons, vous saurez, ils sauront",
    "devoir": "🇫🇷 DEVOIR\n\n📌 Sens : obligation. Ex : Je dois faire mes devoirs.\n\n✅ PRÉSENT : je dois, tu dois, il doit, nous devons, vous devez, ils doivent\n✅ PASSÉ COMPOSÉ : j'ai dû, tu as dû, il a dû, nous avons dû, vous avez dû, ils ont dû\n✅ IMPARFAIT : je devais, tu devais, il devait, nous devions, vous deviez, ils devaient\n✅ FUTUR : je devrai, tu devras, il devra, nous devrons, vous devrez, ils devront",
    "venir": "🇫🇷 VENIR\n\n📌 Sens : arriver. Ex : Je viens de l'école.\n\n✅ PRÉSENT : je viens, tu viens, il vient, nous venons, vous venez, ils viennent\n✅ PASSÉ COMPOSÉ : je suis venu(e), tu es venu(e), il est venu, nous sommes venus, vous êtes venus, ils sont venus\n✅ IMPARFAIT : je venais, tu venais, il venait, nous venions, vous veniez, ils venaient\n✅ FUTUR : je viendrai, tu viendras, il viendra, nous viendrons, vous viendrez, ils viendront",
    "voir": "🇫🇷 VOIR\n\n📌 Sens : regarder avec les yeux. Ex : Je vois un film.\n\n✅ PRÉSENT : je vois, tu vois, il voit, nous voyons, vous voyez, ils voient\n✅ PASSÉ COMPOSÉ : j'ai vu, tu as vu, il a vu, nous avons vu, vous avez vu, ils ont vu\n✅ IMPARFAIT : je voyais, tu voyais, il voyait, nous voyions, vous voyiez, ils voyaient\n✅ FUTUR : je verrai, tu verras, il verra, nous verrons, vous verrez, ils verront",
    "prendre": "🇫🇷 PRENDRE\n\n📌 Sens : attraper, choisir. Ex : Je prends le bus.\n\n✅ PRÉSENT : je prends, tu prends, il prend, nous prenons, vous prenez, ils prennent\n✅ PASSÉ COMPOSÉ : j'ai pris, tu as pris, il a pris, nous avons pris, vous avez pris, ils ont pris\n✅ IMPARFAIT : je prenais, tu prenais, il prenait, nous prenions, vous preniez, ils prenaient\n✅ FUTUR : je prendrai, tu prendras, il prendra, nous prendrons, vous prendrez, ils prendront",
    "mettre": "🇫🇷 METTRE\n\n📌 Sens : placer. Ex : Je mets mes chaussures.\n\n✅ PRÉSENT : je mets, tu mets, il met, nous mettons, vous mettez, ils mettent\n✅ PASSÉ COMPOSÉ : j'ai mis, tu as mis, il a mis, nous avons mis, vous avez mis, ils ont mis\n✅ IMPARFAIT : je mettais, tu mettais, il mettait, nous mettions, vous mettiez, ils mettaient\n✅ FUTUR : je mettrai, tu mettras, il mettra, nous mettrons, vous mettrez, ils mettront",
    "donner": "🇫🇷 DONNER\n\n📌 Sens : offrir. Ex : Je donne un cadeau.\n\n✅ PRÉSENT : je donne, tu donnes, il donne, nous donnons, vous donnez, ils donnent\n✅ PASSÉ COMPOSÉ : j'ai donné, tu as donné, il a donné, nous avons donné, vous avez donné, ils ont donné\n✅ IMPARFAIT : je donnais, tu donnais, il donnait, nous donnions, vous donniez, ils donnaient\n✅ FUTUR : je donnerai, tu donneras, il donnera, nous donnerons, vous donnerez, ils donneront",
    "parler": "🇫🇷 PARLER\n\n📌 Sens : dire avec la voix. Ex : Je parle français.\n\n✅ PRÉSENT : je parle, tu parles, il parle, nous parlons, vous parlez, ils parlent\n✅ PASSÉ COMPOSÉ : j'ai parlé, tu as parlé, il a parlé, nous avons parlé, vous avez parlé, ils ont parlé\n✅ IMPARFAIT : je parlais, tu parlais, il parlait, nous parlions, vous parliez, ils parlaient\n✅ FUTUR : je parlerai, tu parleras, il parlera, nous parlerons, vous parlerez, ils parleront",
    "manger": "🇫🇷 MANGER\n\n📌 Sens : avaler de la nourriture. Ex : Je mange une pizza.\n\n✅ PRÉSENT : je mange, tu manges, il mange, nous mangeons, vous mangez, ils mangent\n✅ PASSÉ COMPOSÉ : j'ai mangé, tu as mangé, il a mangé, nous avons mangé, vous avez mangé, ils ont mangé\n✅ IMPARFAIT : je mangeais, tu mangeais, il mangeait, nous mangions, vous mangiez, ils mangeaient\n✅ FUTUR : je mangerai, tu mangeras, il mangera, nous mangerons, vous mangerez, ils mangeront",
    "dormir": "🇫🇷 DORMIR\n\n📌 Sens : être endormi. Ex : Je dors bien.\n\n✅ PRÉSENT : je dors, tu dors, il dort, nous dormons, vous dormez, ils dorment\n✅ PASSÉ COMPOSÉ : j'ai dormi, tu as dormi, il a dormi, nous avons dormi, vous avez dormi, ils ont dormi\n✅ IMPARFAIT : je dormais, tu dormais, il dormait, nous dormions, vous dormiez, ils dormaient\n✅ FUTUR : je dormirai, tu dormiras, il dormira, nous dormirons, vous dormirez, ils dormiront",
    "ecrire": "🇫🇷 ECRIRE\n\n📌 Sens : écrire avec un stylo. Ex : J'écris une lettre.\n\n✅ PRÉSENT : j'écris, tu écris, il écrit, nous écrivons, vous écrivez, ils écrivent\n✅ PASSÉ COMPOSÉ : j'ai écrit, tu as écrit, il a écrit, nous avons écrit, vous avez écrit, ils ont écrit\n✅ IMPARFAIT : j'écrivais, tu écrivais, il écrivait, nous écrivions, vous écriviez, ils écrivaient\n✅ FUTUR : j'écrirai, tu écriras, il écrira, nous écrirons, vous écrirez, ils écriront",
    "lire": "🇫🇷 LIRE\n\n📌 Sens : lire un livre. Ex : Je lis Harry Potter.\n\n✅ PRÉSENT : je lis, tu lis, il lit, nous lisons, vous lisez, ils lisent\n✅ PASSÉ COMPOSÉ : j'ai lu, tu as lu, il a lu, nous avons lu, vous avez lu, ils ont lu\n✅ IMPARFAIT : je lisais, tu lisais, il lisait, nous lisions, vous lisiez, ils lisaient\n✅ FUTUR : je lirai, tu liras, il lira, nous lirons, vous lirez, ils liront",
    "partir": "🇫🇷 PARTIR\n\n📌 Sens : quitter. Ex : Je pars à l'école.\n\n✅ PRÉSENT : je pars, tu pars, il part, nous partons, vous partez, ils partent\n✅ PASSÉ COMPOSÉ : je suis parti(e), tu es parti(e), il est parti, nous sommes partis, vous êtes partis, ils sont partis\n✅ IMPARFAIT : je partais, tu partais, il partait, nous partions, vous partiez, ils partaient\n✅ FUTUR : je partirai, tu partiras, il partira, nous partirons, vous partirez, ils partiront",
    # ALLEMAND
    "sein": "🇩🇪 SEIN (= ÊTRE) - VERBE LE PLUS IMPORTANT EN ALLEMAND\n\n📌 Sens : être. Ex : Ich bin 13 Jahre alt = J'ai 13 ans.\n\n✅ PRÄSENS : ich bin, du bist, er/sie/es ist, wir sind, ihr seid, sie sind\n✅ PERFEKT : ich bin gewesen, du bist gewesen, er ist gewesen, wir sind gewesen, ihr seid gewesen, sie sind gewesen\n✅ PRÄTERITUM : ich war, du warst, er war, wir waren, ihr wart, sie waren\n✅ FUTUR : ich werde sein, du wirst sein, er wird sein, wir werden sein, ihr werdet sein, sie werden sein",
    "haben": "🇩🇪 HABEN (= AVOIR)\n\n📌 Sens : avoir. Ex : Ich habe einen Hund = J'ai un chien.\n\n✅ PRÄSENS : ich habe, du hast, er hat, wir haben, ihr habt, sie haben\n✅ PERFEKT : ich habe gehabt, du hast gehabt, er hat gehabt, wir haben gehabt, ihr habt gehabt, sie haben gehabt\n✅ PRÄTERITUM : ich hatte, du hattest, er hatte, wir hatten, ihr hattet, sie hatten\n✅ FUTUR : ich werde haben, du wirst haben, er wird haben, wir werden haben, ihr werdet haben, sie werden haben",
    "gehen": "🇩🇪 GEHEN (= ALLER)\n\n📌 Sens : aller. Ex : Ich gehe zur Schule = Je vais à l'école.\n\n✅ PRÄSENS : ich gehe, du gehst, er geht, wir gehen, ihr geht, sie gehen\n✅ PERFEKT : ich bin gegangen, du bist gegangen, er ist gegangen, wir sind gegangen, ihr seid gegangen, sie sind gegangen\n✅ PRÄTERITUM : ich ging, du gingst, er ging, wir gingen, ihr gingt, sie gingen\n✅ FUTUR : ich werde gehen, du wirst gehen, er wird gehen...",
    "machen": "🇩🇪 MACHEN (= FAIRE)\n\n📌 Sens : faire. Ex : Ich mache meine Hausaufgaben = Je fais mes devoirs.\n\n✅ PRÄSENS : ich mache, du machst, er macht, wir machen, ihr macht, sie machen\n✅ PERFEKT : ich habe gemacht, du hast gemacht, er hat gemacht...\n✅ PRÄTERITUM : ich machte, du machtest, er machte...\n✅ FUTUR : ich werde machen...",
    "kommen": "🇩🇪 KOMMEN (= VENIR)\n\n📌 Sens : venir. Ex : Ich komme aus der Schweiz = Je viens de Suisse.\n\n✅ PRÄSENS : ich komme, du kommst, er kommt, wir kommen, ihr kommt, sie kommen\n✅ PERFEKT : ich bin gekommen, du bist gekommen, er ist gekommen...\n✅ PRÄTERITUM : ich kam, du kamst, er kam...\n✅ FUTUR : ich werde kommen...",
    "sehen": "🇩🇪 SEHEN (= VOIR)\n\n📌 Sens : voir. Ex : Ich sehe einen Film = Je vois un film.\n\n✅ PRÄSENS : ich sehe, du siehst, er sieht, wir sehen, ihr seht, sie sehen\n✅ PERFEKT : ich habe gesehen, du hast gesehen...\n✅ PRÄTERITUM : ich sah, du sahst, er sah...\n✅ FUTUR : ich werde sehen...",
    "sprechen": "🇩🇪 SPRECHEN (= PARLER)\n\n📌 Sens : parler. Ex : Ich spreche Deutsch = Je parle allemand.\n\n✅ PRÄSENS : ich spreche, du sprichst, er spricht, wir sprechen, ihr sprecht, sie sprechen\n✅ PERFEKT : ich habe gesprochen...\n✅ PRÄTERITUM : ich sprach, du sprachst, er sprach...\n✅ FUTUR : ich werde sprechen...",
    "essen": "🇩🇪 ESSEN (= MANGER)\n\n📌 Sens : manger. Ex : Ich esse Pizza = Je mange une pizza.\n\n✅ PRÄSENS : ich esse, du isst, er isst, wir essen, ihr esst, sie essen\n✅ PERFEKT : ich habe gegessen...\n✅ PRÄTERITUM : ich aß, du aßest, er aß...\n✅ FUTUR : ich werde essen...",
    "trinken": "🇩🇪 TRINKEN (= BOIRE)\n\n📌 Sens : boire. Ex : Ich trinke Wasser = Je bois de l'eau.\n\n✅ PRÄSENS : ich trinke, du trinkst, er trinkt, wir trinken, ihr trinkt, sie trinken\n✅ PERFEKT : ich habe getrunken...\n✅ PRÄTERITUM : ich trank, du trankst, er trank...\n✅ FUTUR : ich werde trinken...",
    "lernen": "🇩🇪 LERNEN (= APPRENDRE)\n\n📌 Sens : apprendre. Ex : Ich lerne Deutsch = J'apprends l'allemand.\n\n✅ PRÄSENS : ich lerne, du lernst, er lernt, wir lernen, ihr lernt, sie lernen\n✅ PERFEKT : ich habe gelernt...\n✅ PRÄTERITUM : ich lernte...\n✅ FUTUR : ich werde lernen...",
    "wohnen": "🇩🇪 WOHNEN (= HABITER)\n\n📌 Sens : habiter. Ex : Ich wohne in Estavayer = J'habite à Estavayer.\n\n✅ PRÄSENS : ich wohne, du wohnst, er wohnt, wir wohnen, ihr wohnt, sie wohnen\n✅ PERFEKT : ich habe gewohnt...\n✅ PRÄTERITUM : ich wohnte...\n✅ FUTUR : ich werde wohnen...",
    "spielen": "🇩🇪 SPIELEN (= JOUER)\n\n📌 Sens : jouer. Ex : Ich spiele Fussball = Je joue au foot.\n\n✅ PRÄSENS : ich spiele, du spielst, er spielt, wir spielen, ihr spielt, sie spielen\n✅ PERFEKT : ich habe gespielt...\n✅ PRÄTERITUM : ich spielte...\n✅ FUTUR : ich werde spielen...",
    "arbeiten": "🇩🇪 ARBEITEN (= TRAVAILLER)\n\n📌 Sens : travailler. Ex : Ich arbeite viel = Je travaille beaucoup.\n\n✅ PRÄSENS : ich arbeite, du arbeitest, er arbeitet, wir arbeiten, ihr arbeitet, sie arbeiten\n✅ PERFEKT : ich habe gearbeitet...\n✅ PRÄTERITUM : ich arbeitete...\n✅ FUTUR : ich werde arbeiten...",
    "konnen": "🇩🇪 KÖNNEN (= POUVOIR)\n\n📌 Sens : pouvoir. Ex : Ich kann schwimmen = Je peux nager.\n\n✅ PRÄSENS : ich kann, du kannst, er kann, wir können, ihr könnt, sie können\n✅ PERFEKT : ich habe gekonnt / ich konnte...\n✅ PRÄTERITUM : ich konnte, du konntest, er konnte...\n✅ FUTUR : ich werde können...",
    "wollen": "🇩🇪 WOLLEN (= VOULOIR)\n\n📌 Sens : vouloir. Ex : Ich will spielen = Je veux jouer.\n\n✅ PRÄSENS : ich will, du willst, er will, wir wollen, ihr wollt, sie wollen\n✅ PERFEKT : ich habe gewollt...\n✅ PRÄTERITUM : ich wollte...\n✅ FUTUR : ich werde wollen...",
    "mussen": "🇩🇪 MÜSSEN (= DEVOIR)\n\n📌 Sens : devoir. Ex : Ich muss lernen = Je dois apprendre.\n\n✅ PRÄSENS : ich muss, du musst, er muss, wir müssen, ihr müsst, sie müssen\n✅ PERFEKT : ich habe gemusst...\n✅ PRÄTERITUM : ich musste...\n✅ FUTUR : ich werde müssen...",
    "wissen": "🇩🇪 WISSEN (= SAVOIR)\n\n📌 Sens : savoir. Ex : Ich weiß das = Je sais ça.\n\n✅ PRÄSENS : ich weiß, du weißt, er weiß, wir wissen, ihr wisst, sie wissen\n✅ PERFEKT : ich habe gewusst...\n✅ PRÄTERITUM : ich wusste...\n✅ FUTUR : ich werde wissen...",
    "geben": "🇩🇪 GEBEN (= DONNER)\n\n📌 Sens : donner. Ex : Ich gebe dir ein Buch = Je te donne un livre.\n\n✅ PRÄSENS : ich gebe, du gibst, er gibt, wir geben, ihr gebt, sie geben\n✅ PERFEKT : ich habe gegeben...\n✅ PRÄTERITUM : ich gab, du gabst, er gab...\n✅ FUTUR : ich werde geben...",
    "nehmen": "🇩🇪 NEHMEN (= PRENDRE)\n\n📌 Sens : prendre. Ex : Ich nehme den Bus = Je prends le bus.\n\n✅ PRÄSENS : ich nehme, du nimmst, er nimmt, wir nehmen, ihr nehmt, sie nehmen\n✅ PERFEKT : ich habe genommen...\n✅ PRÄTERITUM : ich nahm, du nahmst, er nahm...\n✅ FUTUR : ich werde nehmen...",
    "schreiben": "🇩🇪 SCHREIBEN (= ECRIRE)\n\n📌 Sens : écrire. Ex : Ich schreibe einen Brief = J'écris une lettre.\n\n✅ PRÄSENS : ich schreibe, du schreibst, er schreibt, wir schreiben, ihr schreibt, sie schreiben\n✅ PERFEKT : ich habe geschrieben...\n✅ PRÄTERITUM : ich schrieb...\n✅ FUTUR : ich werde schreiben...",
    # ANGLAIS
    "to be": "🇬🇧 TO BE (= ÊTRE) - VERBE LE PLUS IMPORTANT EN ANGLAIS\n\n📌 Sens : être. Ex : I am happy = Je suis content.\n\n✅ PRESENT : I am, You are, He/She/It is, We are, You are, They are\n✅ PAST : I was, You were, He was, We were, You were, They were\n✅ PRESENT PERFECT : I have been, You have been, He has been...\n✅ FUTURE : I will be, You will be, He will be, We will be, You will be, They will be",
    "to have": "🇬🇧 TO HAVE (= AVOIR)\n\n📌 Sens : avoir. Ex : I have a dog = J'ai un chien.\n\n✅ PRESENT : I have, You have, He has, We have, You have, They have\n✅ PAST : I had, You had, He had, We had...\n✅ PRESENT PERFECT : I have had...\n✅ FUTURE : I will have...",
    "to go": "🇬🇧 TO GO (= ALLER)\n\n📌 Sens : aller. Ex : I go to school = Je vais à l'école.\n\n✅ PRESENT : I go, You go, He goes, We go, You go, They go\n✅ PAST : I went, You went, He went...\n✅ PRESENT PERFECT : I have gone...\n✅ FUTURE : I will go...",
    "to do": "🇬🇧 TO DO (= FAIRE)\n\n📌 Sens : faire. Ex : I do my homework = Je fais mes devoirs.\n\n✅ PRESENT : I do, You do, He does, We do, You do, They do\n✅ PAST : I did...\n✅ PRESENT PERFECT : I have done...\n✅ FUTURE : I will do...",
    "to say": "🇬🇧 TO SAY (= DIRE)\n\n📌 Sens : dire. Ex : I say hello = Je dis bonjour.\n\n✅ PRESENT : I say, You say, He says, We say, You say, They say\n✅ PAST : I said...\n✅ PRESENT PERFECT : I have said...\n✅ FUTURE : I will say...",
    "to see": "🇬🇧 TO SEE (= VOIR)\n\n📌 Sens : voir. Ex : I see a film = Je vois un film.\n\n✅ PRESENT : I see, You see, He sees, We see, You see, They see\n✅ PAST : I saw...\n✅ PRESENT PERFECT : I have seen...\n✅ FUTURE : I will see...",
    "to come": "🇬🇧 TO COME (= VENIR)\n\n📌 Sens : venir. Ex : I come from Switzerland = Je viens de Suisse.\n\n✅ PRESENT : I come, You come, He comes, We come...\n✅ PAST : I came...\n✅ PRESENT PERFECT : I have come...\n✅ FUTURE : I will come...",
    "to get": "🇬🇧 TO GET (= OBTENIR / DEVENIR)\n\n📌 Sens : obtenir, devenir. Ex : I get up = Je me lève.\n\n✅ PRESENT : I get, You get, He gets, We get...\n✅ PAST : I got...\n✅ PRESENT PERFECT : I have got...\n✅ FUTURE : I will get...",
    "to make": "🇬🇧 TO MAKE (= FAIRE / FABRIQUER)\n\n📌 Sens : fabriquer. Ex : I make a cake = Je fais un gâteau.\n\n✅ PRESENT : I make, You make, He makes...\n✅ PAST : I made...\n✅ PRESENT PERFECT : I have made...\n✅ FUTURE : I will make...",
    "to take": "🇬🇧 TO TAKE (= PRENDRE)\n\n📌 Sens : prendre. Ex : I take the bus = Je prends le bus.\n\n✅ PRESENT : I take, You take, He takes...\n✅ PAST : I took...\n✅ PRESENT PERFECT : I have taken...\n✅ FUTURE : I will take...",
    "to give": "🇬🇧 TO GIVE (= DONNER)\n\n📌 Sens : donner. Ex : I give a gift = Je donne un cadeau.\n\n✅ PRESENT : I give, You give, He gives...\n✅ PAST : I gave...\n✅ PRESENT PERFECT : I have given...\n✅ FUTURE : I will give...",
    "to know": "🇬🇧 TO KNOW (= SAVOIR / CONNAITRE)\n\n📌 Sens : savoir. Ex : I know you = Je te connais.\n\n✅ PRESENT : I know, You know, He knows...\n✅ PAST : I knew...\n✅ PRESENT PERFECT : I have known...\n✅ FUTURE : I will know...",
    "to think": "🇬🇧 TO THINK (= PENSER)\n\n📌 Sens : penser. Ex : I think it's cool = Je pense que c'est cool.\n\n✅ PRESENT : I think, You think, He thinks...\n✅ PAST : I thought...\n✅ PRESENT PERFECT : I have thought...\n✅ FUTURE : I will think...",
    "to speak": "🇬🇧 TO SPEAK (= PARLER)\n\n📌 Sens : parler. Ex : I speak English = Je parle anglais.\n\n✅ PRESENT : I speak, You speak, He speaks...\n✅ PAST : I spoke...\n✅ PRESENT PERFECT : I have spoken...\n✅ FUTURE : I will speak...",
    "to eat": "🇬🇧 TO EAT (= MANGER)\n\n📌 Sens : manger. Ex : I eat pizza = Je mange une pizza.\n\n✅ PRESENT : I eat, You eat, He eats...\n✅ PAST : I ate...\n✅ PRESENT PERFECT : I have eaten...\n✅ FUTURE : I will eat...",
    "to drink": "🇬🇧 TO DRINK (= BOIRE)\n\n📌 Sens : boire. Ex : I drink water = Je bois de l'eau.\n\n✅ PRESENT : I drink, You drink, He drinks...\n✅ PAST : I drank...\n✅ PRESENT PERFECT : I have drunk...\n✅ FUTURE : I will drink...",
    "to play": "🇬🇧 TO PLAY (= JOUER)\n\n📌 Sens : jouer. Ex : I play football = Je joue au foot.\n\n✅ PRESENT : I play, You play, He plays...\n✅ PAST : I played...\n✅ PRESENT PERFECT : I have played...\n✅ FUTURE : I will play...",
    "to live": "🇬🇧 TO LIVE (= VIVRE / HABITER)\n\n📌 Sens : vivre. Ex : I live in Switzerland = J'habite en Suisse.\n\n✅ PRESENT : I live, You live, He lives...\n✅ PAST : I lived...\n✅ PRESENT PERFECT : I have lived...\n✅ FUTURE : I will live...",
    "to love": "🇬🇧 TO LOVE (= AIMER)\n\n📌 Sens : aimer. Ex : I love football = J'aime le foot.\n\n✅ PRESENT : I love, You love, He loves...\n✅ PAST : I loved...\n✅ PRESENT PERFECT : I have loved...\n✅ FUTURE : I will love...",
    "to want": "🇬🇧 TO WANT (= VOULOIR)\n\n📌 Sens : vouloir. Ex : I want to play = Je veux jouer.\n\n✅ PRESENT : I want, You want, He wants...\n✅ PAST : I wanted...\n✅ PRESENT PERFECT : I have wanted...\n✅ FUTURE : I will want...",
    # ESPAGNOL
    "ser": "🇪🇸 SER (= ÊTRE - pour l'identité)\n\n📌 Sens : être (permanent). Ex : Soy de Suiza = Je suis de Suisse.\n\n✅ PRESENTE : yo soy, tú eres, él es, nosotros somos, vosotros sois, ellos son\n✅ PRETÉRITO : yo fui, tú fuiste, él fue, nosotros fuimos, vosotros fuisteis, ellos fueron\n✅ IMPERFECTO : yo era, tú eras, él era, nosotros éramos, vosotros erais, ellos eran\n✅ FUTURO : yo seré, tú serás, él será, nosotros seremos, vosotros seréis, ellos serán",
    "estar": "🇪🇸 ESTAR (= ÊTRE - pour l'état)\n\n📌 Sens : être (temporaire, lieu). Ex : Estoy en casa = Je suis à la maison.\n\n✅ PRESENTE : yo estoy, tú estás, él está, nosotros estamos, vosotros estáis, ellos están\n✅ PRETÉRITO : yo estuve, tú estuviste, él estuvo, nosotros estuvimos, vosotros estuvisteis, ellos estuvieron\n✅ IMPERFECTO : yo estaba, tú estabas, él estaba, nosotros estábamos, vosotros estabais, ellos estaban\n✅ FUTURO : yo estaré, tú estarás, él estará...",
    "tener": "🇪🇸 TENER (= AVOIR)\n\n📌 Sens : avoir. Ex : Tengo 13 años = J'ai 13 ans.\n\n✅ PRESENTE : yo tengo, tú tienes, él tiene, nosotros tenemos, vosotros tenéis, ellos tienen\n✅ PRETÉRITO : yo tuve, tú tuviste, él tuvo, nosotros tuvimos, vosotros tuvisteis, ellos tuvieron\n✅ IMPERFECTO : yo tenía, tú tenías, él tenía...\n✅ FUTURO : yo tendré, tú tendrás, él tendrá...",
    "ir": "🇪🇸 IR (= ALLER)\n\n📌 Sens : aller. Ex : Voy a la escuela = Je vais à l'école.\n\n✅ PRESENTE : yo voy, tú vas, él va, nosotros vamos, vosotros vais, ellos van\n✅ PRETÉRITO : yo fui, tú fuiste, él fue, nosotros fuimos, vosotros fuisteis, ellos fueron\n✅ IMPERFECTO : yo iba, tú ibas, él iba...\n✅ FUTURO : yo iré, tú irás, él irá...",
    "hacer": "🇪🇸 HACER (= FAIRE)\n\n📌 Sens : faire. Ex : Hago mis deberes = Je fais mes devoirs.\n\n✅ PRESENTE : yo hago, tú haces, él hace, nosotros hacemos, vosotros hacéis, ellos hacen\n✅ PRETÉRITO : yo hice, tú hiciste, él hizo...\n✅ IMPERFECTO : yo hacía...\n✅ FUTURO : yo haré...",
    "decir": "🇪🇸 DECIR (= DIRE)\n\n📌 Sens : dire. Ex : Digo hola = Je dis bonjour.\n\n✅ PRESENTE : yo digo, tú dices, él dice, nosotros decimos, vosotros decís, ellos dicen\n✅ PRETÉRITO : yo dije, tú dijiste, él dijo...\n✅ IMPERFECTO : yo decía...\n✅ FUTURO : yo diré...",
    "poder": "🇪🇸 PODER (= POUVOIR)\n\n📌 Sens : pouvoir. Ex : Puedo jugar = Je peux jouer.\n\n✅ PRESENTE : yo puedo, tú puedes, él puede, nosotros podemos, vosotros podéis, ellos pueden\n✅ PRETÉRITO : yo pude...\n✅ IMPERFECTO : yo podía...\n✅ FUTURO : yo podré...",
    "querer": "🇪🇸 QUERER (= VOULOIR / AIMER)\n\n📌 Sens : vouloir. Ex : Quiero jugar = Je veux jouer.\n\n✅ PRESENTE : yo quiero, tú quieres, él quiere, nosotros queremos, vosotros queréis, ellos quieren\n✅ PRETÉRITO : yo quise...\n✅ IMPERFECTO : yo quería...\n✅ FUTURO : yo querré...",
    "saber": "🇪🇸 SABER (= SAVOIR)\n\n📌 Sens : savoir. Ex : Sé nadar = Je sais nager.\n\n✅ PRESENTE : yo sé, tú sabes, él sabe, nosotros sabemos, vosotros sabéis, ellos saben\n✅ PRETÉRITO : yo supe...\n✅ IMPERFECTO : yo sabía...\n✅ FUTURO : yo sabré...",
    "venir": "🇪🇸 VENIR (= VENIR)\n\n📌 Sens : venir. Ex : Vengo de Suiza = Je viens de Suisse.\n\n✅ PRESENTE : yo vengo, tú vienes, él viene, nosotros venimos, vosotros venís, ellos vienen\n✅ PRETÉRITO : yo vine...\n✅ IMPERFECTO : yo venía...\n✅ FUTURO : yo vendré...",
    "ver": "🇪🇸 VER (= VOIR)\n\n📌 Sens : voir. Ex : Veo una película = Je vois un film.\n\n✅ PRESENTE : yo veo, tú ves, él ve, nosotros vemos, vosotros veis, ellos ven\n✅ PRETÉRITO : yo vi...\n✅ IMPERFECTO : yo veía...\n✅ FUTURO : yo veré...",
    "hablar": "🇪🇸 HABLAR (= PARLER)\n\n📌 Sens : parler. Ex : Hablo español = Je parle espagnol.\n\n✅ PRESENTE : yo hablo, tú hablas, él habla, nosotros hablamos, vosotros habláis, ellos hablan\n✅ PRETÉRITO : yo hablé...\n✅ IMPERFECTO : yo hablaba...\n✅ FUTURO : yo hablaré...",
    "comer": "🇪🇸 COMER (= MANGER)\n\n📌 Sens : manger. Ex : Como pizza = Je mange une pizza.\n\n✅ PRESENTE : yo como, tú comes, él come, nosotros comemos, vosotros coméis, ellos comen\n✅ PRETÉRITO : yo comí...\n✅ IMPERFECTO : yo comía...\n✅ FUTURO : yo comeré...",
    "vivir": "🇪🇸 VIVIR (= VIVRE)\n\n📌 Sens : vivre. Ex : Vivo en Suiza = J'habite en Suisse.\n\n✅ PRESENTE : yo vivo, tú vives, él vive, nosotros vivimos, vosotros vivís, ellos viven\n✅ PRETÉRITO : yo viví...\n✅ IMPERFECTO : yo vivía...\n✅ FUTURO : yo viviré...",
    "jugar": "🇪🇸 JUGAR (= JOUER)\n\n📌 Sens : jouer. Ex : Juego al fútbol = Je joue au foot.\n\n✅ PRESENTE : yo juego, tú juegas, él juega, nosotros jugamos, vosotros jugáis, ellos juegan\n✅ PRETÉRITO : yo jugué...\n✅ IMPERFECTO : yo jugaba...\n✅ FUTURO : yo jugaré...",
    # ITALIEN
    "essere": "🇮🇹 ESSERE (= ÊTRE)\n\n📌 Sens : être. Ex : Sono contento = Je suis content.\n\n✅ PRESENTE : io sono, tu sei, lui è, noi siamo, voi siete, loro sono\n✅ PASSATO : io sono stato, tu sei stato, lui è stato...\n✅ IMPERFETTO : io ero, tu eri, lui era, noi eravamo, voi eravate, loro erano\n✅ FUTURO : io sarò, tu sarai, lui sarà, noi saremo, voi sarete, loro saranno",
    "avere": "🇮🇹 AVERE (= AVOIR)\n\n📌 Sens : avoir. Ex : Ho 13 anni = J'ai 13 ans.\n\n✅ PRESENTE : io ho, tu hai, lui ha, noi abbiamo, voi avete, loro hanno\n✅ PASSATO : io ho avuto...\n✅ IMPERFETTO : io avevo, tu avevi, lui aveva...\n✅ FUTURO : io avrò, tu avrai, lui avrà...",
    "andare": "🇮🇹 ANDARE (= ALLER)\n\n📌 Sens : aller. Ex : Vado a scuola = Je vais à l'école.\n\n✅ PRESENTE : io vado, tu vai, lui va, noi andiamo, voi andate, loro vanno\n✅ PASSATO : io sono andato...\n✅ IMPERFETTO : io andavo...\n✅ FUTURO : io andrò...",
    "fare": "🇮🇹 FARE (= FAIRE)\n\n📌 Sens : faire. Ex : Faccio i compiti = Je fais mes devoirs.\n\n✅ PRESENTE : io faccio, tu fai, lui fa, noi facciamo, voi fate, loro fanno\n✅ PASSATO : io ho fatto...\n✅ IMPERFETTO : io facevo...\n✅ FUTURO : io farò...",
    "dire": "🇮🇹 DIRE (= DIRE)\n\n📌 Sens : dire. Ex : Dico ciao = Je dis bonjour.\n\n✅ PRESENTE : io dico, tu dici, lui dice, noi diciamo, voi dite, loro dicono\n✅ PASSATO : io ho detto...\n✅ IMPERFETTO : io dicevo...\n✅ FUTURO : io dirò...",
    "potere": "🇮🇹 POTERE (= POUVOIR)\n\n📌 Sens : pouvoir. Ex : Posso giocare = Je peux jouer.\n\n✅ PRESENTE : io posso, tu puoi, lui può, noi possiamo, voi potete, loro possono\n✅ PASSATO : io ho potuto...\n✅ IMPERFETTO : io potevo...\n✅ FUTURO : io potrò...",
    "volere": "🇮🇹 VOLERE (= VOULOIR)\n\n📌 Sens : vouloir. Ex : Voglio giocare = Je veux jouer.\n\n✅ PRESENTE : io voglio, tu vuoi, lui vuole, noi vogliamo, voi volete, loro vogliono\n✅ PASSATO : io ho voluto...\n✅ IMPERFETTO : io volevo...\n✅ FUTURO : io vorrò...",
    "sapere": "🇮🇹 SAPERE (= SAVOIR)\n\n📌 Sens : savoir. Ex : So nuotare = Je sais nager.\n\n✅ PRESENTE : io so, tu sai, lui sa, noi sappiamo, voi sapete, loro sanno\n✅ PASSATO : io ho saputo...\n✅ IMPERFETTO : io sapevo...\n✅ FUTURO : io saprò...",
    "venire": "🇮🇹 VENIRE (= VENIR)\n\n📌 Sens : venir. Ex : Vengo dalla Svizzera = Je viens de Suisse.\n\n✅ PRESENTE : io vengo, tu vieni, lui viene, noi veniamo, voi venite, loro vengono\n✅ PASSATO : io sono venuto...\n✅ IMPERFETTO : io venivo...\n✅ FUTURO : io verrò...",
    "vedere": "🇮🇹 VEDERE (= VOIR)\n\n📌 Sens : voir. Ex : Vedo un film = Je vois un film.\n\n✅ PRESENTE : io vedo, tu vedi, lui vede, noi vediamo, voi vedete, loro vedono\n✅ PASSATO : io ho visto...\n✅ IMPERFETTO : io vedevo...\n✅ FUTURO : io vedrò...",
    "parlare": "🇮🇹 PARLARE (= PARLER)\n\n📌 Sens : parler. Ex : Parlo italiano = Je parle italien.\n\n✅ PRESENTE : io parlo, tu parli, lui parla, noi parliamo, voi parlate, loro parlano\n✅ PASSATO : io ho parlato...\n✅ IMPERFETTO : io parlavo...\n✅ FUTURO : io parlerò...",
    "mangiare": "🇮🇹 MANGIARE (= MANGER)\n\n📌 Sens : manger. Ex : Mangio la pizza = Je mange une pizza.\n\n✅ PRESENTE : io mangio, tu mangi, lui mangia, noi mangiamo, voi mangiate, loro mangiano\n✅ PASSATO : io ho mangiato...\n✅ IMPERFETTO : io mangiavo...\n✅ FUTURO : io mangerò...",
    "giocare": "🇮🇹 GIOCARE (= JOUER)\n\n📌 Sens : jouer. Ex : Gioco a calcio = Je joue au foot.\n\n✅ PRESENTE : io gioco, tu giochi, lui gioca, noi giochiamo, voi giocate, loro giocano\n✅ PASSATO : io ho giocato...\n✅ IMPERFETTO : io giocavo...\n✅ FUTURO : io giocherò...",
}

TOUT = {
    "pythagore": "THEOREME DE PYTHAGORE : a² + b² = c². UNIQUEMENT triangle rectangle. Ex : 3-4-5, 6-8-10.",
    "thales": "THALES : AB / AD = AC / AE = BC / DE.",
    "moyenne": "MOYENNE : somme / nombre. Ex : (12+15+18)/3 = 15",
    "aire": "AIRE : Rectangle = L x l, Triangle = (b x h)/2, Cercle = pi x r²",
    "perimetre": "PERIMETRE : Carré = 4 x côté, Rectangle = 2 x (L+l), Cercle = 2 x pi x r",
    "volume": "VOLUME : Cube = côté³, Pavé = L x l x h.",
    "angle": "ANGLES : Droit = 90°, Plat = 180°, Plein = 360°. Triangle = 180°.",
    "fraction": "FRACTION : 1/2 + 1/4 = 3/4.",
    "pourcentage": "POURCENTAGE : 20% de 50 = 10. Formule : (partie / total) x 100.",
    "equation": "EQUATION : 2x + 3 = 7 -> 2x = 4 -> x = 2.",
    "cod": "COD - GRAMMAIRE : COD = Complément d'Objet Direct. Il répond à Qui ? ou Quoi ? Ex : Je mange une pomme. Je mange quoi ? Une pomme = COD.",
    "sujet": "SUJET : C'est qui fait l'action. Ex : Lenny mange. Qui mange ? Lenny = sujet.",
    "adjectif": "ADJECTIF : Il décrit un nom, il s'accorde. Ex : grand garçon / grande fille.",
    "pluriel": "PLURIEL : +s : chat -> chats. -eau : bateau -> bateaux. -al : cheval -> chevaux.",
    "verbe": "VERBE : C'est l'action. Ex : Je mange, Tu cours, Il dort.",
    "a / a": "A / À : a = verbe avoir (Il a 13 ans). à = préposition (Je vais à l'école).",
    "et / est": "ET / EST : et = liaison (Lenny et 【entity-Hugo¦canonical_name=Hugo】). est = verbe être (Il est gentil).",
    "son / sont": "SON / SONT : son = à lui (son chien). sont = verbe être (Ils sont gentils).",
    "synonyme": "SYNONYME : Mot qui veut dire la même chose. Ex : content = heureux.",
    "antonyme": "ANTONYME : Mot qui veut dire le contraire. Ex : grand ≠ petit.",
    "homonyme": "HOMONYME : Mots qui se prononcent pareil. Ex : a / à, et / est, son / sont.",
    "passe compose": "PASSE COMPOSE : avoir/être + participe passé. Ex : J'ai mangé, Je suis allé.",
    "imparfait": "IMPARFAIT : Pour une habitude. Terminaisons : -ais, -ais, -ait, -ions, -iez, -aient. Ex : Quand j'étais petit, je jouais.",
    "futur": "FUTUR : -ai, -as, -a, -ons, -ez, -ont. Ex : Je mangerai.",
    "der": "DER DIE DAS : der = masculin, die = féminin, das = neutre. Pluriel = die.",
    "accusatif": "ACCUSATIF : C'est le cas du COD. der → den. Ex : Ich sehe den Hund.",
    "datif": "DATIF : C'est le cas du COI (à qui ?). der → dem, die → der, das → dem.",
    "nominatif": "NOMINATIF : C'est le cas du sujet. der, die, das.",
    "present simple": "PRESENT SIMPLE : Pour les habitudes. I play, He plays (avec -s !).",
    "present perfect": "Present Perfect : have + participe. I have eaten = J'ai mangé.",
    "present continu": "PRESENT CONTINU : be + -ing. I am playing = Je suis en train de jouer.",
    "ser et estar": "SER et ESTAR : SER = être permanent (Soy de Suiza). ESTAR = être temporaire / lieu (Estoy en casa).",
    "el / la": "EL / LA : el = masculin, la = féminin, los / las = pluriel. Ex : el perro, la casa.",
    "pluriel en espagnol": "PLURIEL EN ESPAGNOL : +s : casa -> casas. -z : lápiz -> lápices.",
    "il / lo / la": "IL / LO / LA - ITALIEN : il = masculin, lo = masculin devant s+consonne, la = féminin.",
    "pluriel en italien": "PLURIEL EN ITALIEN : -o -> -i : libro -> libri. -a -> -e : casa -> case. -e -> -i : cane -> cani.",
    "photosynthese": "PHOTOSYNTHESE : Soleil + Eau + CO2 = Oxygène + Sucre.",
    "gravite": "GRAVITE : Nous attire vers la Terre. Newton + pomme.",
    "coeur": "COEUR : Pompe le sang, 100 000 battements par jour !",
    "volcan": "VOLCAN : Magma qui sort. Lave = magma dehors.",
    "foudre": "FOUDRE : 30 000 degrés, 5x plus chaud que le Soleil.",
    "saison": "SAISONS : C'est l'inclinaison de la Terre (23,5°) qui fait les saisons.",
    "masse volumique": "MASSE VOLUMIQUE : Rho = m / V. Ex : 100g / 100 cm³ = 1 g/cm³ = eau. Huile 0,9 flotte, Fer 7,8 coule.",
    "atome": "ATOME : Proton (+), Neutron (0), Electron (-).",
    "oxygene": "OXYGENE : O2. On respire O2, on rejette CO2. 21% de l'air.",
    "chimie": "CHIMIE : Etude de la matière. H2O = eau, CO2 = dioxyde de carbone.",
    "electricite": "ELECTRICITE : P = U x I. En série : tout s'éteint. En parallèle : les autres restent allumées.",
    "vitesse": "VITESSE : v = d / t. Ex : 100m en 10 sec = 10 m/s = 36 km/h.",
    "energie": "ENERGIE : Cinétique, potentielle, thermique, électrique, solaire.",
    "adn": "ADN : Ton code génétique. 50% père, 50% mère.",
    "trou noir": "TROU NOIR : Objet tellement lourd que même la lumière ne peut pas sortir.",
    "big bang": "BIG BANG : Début de l'univers il y a 13,8 milliards d'années.",
    "mars": "MARS : Planète rouge. Un jour = 24h37.",
    "iss": "ISS : Station spatiale à 400 km, 28 000 km/h.",
    "systeme solaire": "SYSTEME SOLAIRE : 8 planètes : Mercure, Vénus, Terre, Mars, Jupiter, Saturne, Uranus, Neptune.",
    "boucle": "BOUCLE : for i in range(1,6): print(i) -> 1,2,3,4,5",
    "variable": "VARIABLE : age = 13. Boîte qui stocke une valeur.",
    "condition": "CONDITION : if age >= 18: print('Majeur') else: print('Mineur')",
    "fonction": "FONCTION : def dire_bonjour(): print('Bonjour')",
    "python": "PYTHON : Langage facile, celui de ton agent.",
    "html": "HTML : Squelette d'un site. <h1>Titre</h1>",
    "css": "CSS : Style d'un site : couleurs, tailles.",
    " messi": " MESSI : Argentin, 8 Ballons d'Or, meilleur de tous les temps. Coupe du Monde 2022.",
    " 【entity-ronaldo¦canonical_name=Ronaldo】": " 【entity-CR7¦canonical_name=CR7】 : Portugais, 5 Ballons d'Or. Meilleur buteur de l'histoire.",
    " 【entity-mbappe¦canonical_name=Mbappe】": " 【entity-MBAPPE¦canonical_name=Mbappe】 : Français, 36 km/h ! 【entity-Real Madrid¦canonical_name=Real Madrid】, Champion du monde 2018.",
    "coupe du monde": "COUPE DU MONDE : Tous les 4 ans. 2022 = Argentine. 2026 = USA / Canada / Mexique.",
    " 【entity-minecraft¦canonical_name=Minecraft】": " 【entity-MINECRAFT¦canonical_name=Minecraft】 : Jeu de cubes, 300M de copies !",
    " 【entity-fortnite¦canonical_name=Fortnite】": " 【entity-FORTNITE¦canonical_name=Fortnite】 : Battle Royale 100 joueurs, dernier vivant gagne.",
    " 【entity-roblox¦canonical_name=Roblox】": " 【entity-ROBLOX¦canonical_name=Roblox】 : Des millions de jeux créés par les joueurs.",
    "gta": "GTA V : 190M de copies !",
    "tour eiffel": "TOUR EIFFEL : Paris, 330m, 1889, Gustave Eiffel. 7M de visiteurs par an.",
    " 【entity-titanic¦canonical_name=Titanic】": " 【entity-TITANIC¦canonical_name=Titanic】 : Coule en 1912, iceberg. Film 1997.",
    "millionnaire": "COMMENT DEVENIR MILLIONNAIRE ? : 1. Salarié + investissement : 1000 CHF / mois en bourse, en 30 ans tu as 1M. 2. Entrepreneur. 3. Créateur.",
    "salaire": "SALAIRE : En Suisse : moyen = 6500 CHF / mois. Développeur = 8000 CHF.",
    "gagner de l argent": "GAGNER DE L'ARGENT A 13 ANS ? : Petits services = 10-20 CHF. Créer un projet et montrer à tes parents.",
    "plus grand animal": "PLUS GRAND ANIMAL : Baleine bleue ! 30m, 200 tonnes.",
    "plus rapide": "PLUS RAPIDE : Guépard = 110 km/h. Faucon pèlerin = 390 km/h !",
    "chien": "CHIEN : Meilleur ami de l'homme depuis 15 000 ans. 400 races.",
    "chat": "CHAT : Il dort 16h par jour ! Il peut sauter 6x sa hauteur.",
    "conseil pour reviser": "CONSEIL POUR REVISER : 1. Pomodoro : 25 min, 5 min pause. 2. Teste-toi. 3. Explique à quelqu'un. 4. Dors bien. 5. Pas de téléphone.",
}

AVIONS = {
    "f-22": "F-22 Raptor (USA) - LE PLUS PERFORMANT EN COMBAT. Mach 2.25. Furtif, jamais battu.",
    " f-35": " F-35 Lightning II (USA) - LE PLUS MODERNE. Mach 1.6. La Suisse en a acheté 36 !",
    "rafale": "Rafale (France). Mach 1.8. Polyvalent.",
    "sr-71": "SR-71 Blackbird. Mach 3.3 = 3500 km/h ! Plus rapide de tous les temps.",
    "concorde": "Concorde : Paris-New York en 3h30. Mach 2.",
    "f-16": "F-16. Mach 2.0. Plus produit : 4600 exemplaires !",
    "f-15": "F-15 Eagle. Mach 2.5 ! 104 victoires à 0 défaite.",
}

TRAIN_FACILE = [("C'est quoi 2+2 ?", "4"), ("C'est quoi 5x2 ?", "10"), ("C'est quoi la capitale de la France ?", "paris")]
TRAIN_MOYEN = [("C'est quoi 7x8 ?", "56"), ("C'est quoi la capitale du Japon ?", "tokyo"), ("C'est quoi 15+25 ?", "40"), ("Qui a gagné la Coupe du Monde 2022 ?", "argentine")]
TRAIN_DIFFICILE = [("C'est quoi 12x12 ?", "144"), ("C'est quoi la capitale de l'Australie ?", "canberra"), ("Combien de Ballons d'Or a Messi ?", "8")]

def toutes_tables():
    txt = "TOUTES LES TABLES 1 à 12 :\n\n"
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
        return f"Ok, entraînement arrêté ! 🏁 Score : {st.session_state.score}/{st.session_state.total_quiz} ! 🔥 Best streak : {st.session_state.best_streak} ! Bravo ! 💪"
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
            rep = f"❌ Pas tout à fait... La bonne réponse c'était '{st.session_state.train_a}'. Score : {st.session_state.score}/{st.session_state.total_quiz}"
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
        return f"🎯 ENTRAINEMENT FACILE ! 🟢 Ecris 'stop' pour arrêter.\n\nPremière question : {nq}"
    if "entrainement difficile" in q_low:
        st.session_state.mode_train = True
        st.session_state.niveau = "difficile"
        nq, na = random.choice(TRAIN_DIFFICILE)
        st.session_state.train_q = nq
        st.session_state.train_a = na
        return f"🎯 ENTRAINEMENT DIFFICILE ! 🔴\n\nPremière question : {nq}"
    if "entraine" in q_low or "entrainement" in q_low or q_low == "quiz moi":
        st.session_state.mode_train = True
        st.session_state.niveau = "moyen"
        nq, na = random.choice(TRAIN_MOYEN)
        st.session_state.train_q = nq
        st.session_state.train_a = na
        return f"🎯 ENTRAINEMENT MOYEN ! Ecris 'stop' pour arrêter.\n\nPremière question : {nq}"
    if "mon score" in q_low or q_low == "score":
        return f"🏆 Score : {st.session_state.score} / {st.session_state.total_quiz} ! 🔥 Streak : {st.session_state.streak} | Best : {st.session_state.best_streak} !"
    if q_brut.startswith("apprends") or q_brut.startswith("apprend") or "retient que" in q_brut:
        try:
            texte = q_brut.replace("apprends :", "").replace("apprends", "").replace("apprend :", "").replace("apprend", "").replace("retient que", "").strip()
            if "=" in texte:
                cle, val = texte.split("=", 1)
                cle = nettoyer(cle)
                val = val.strip()
                st.session_state.learned[cle] = val
                return f"✅ MERCI ! J'ai appris ! 🧠 '{cle}' = '{val}' ! J'ai appris {len(st.session_state.learned)} choses !"
            else:
                st.session_state.learned[nettoyer(texte)] = texte
                return f"✅ Merci ! J'ai retenu : '{texte}' ! 🧠"
        except:
            return "Ecris : Apprends : c'est quoi le foot = le foot c'est un sport avec un ballon"
    if "montre ce que tu as appris" in q_low or "ce que tu as appris" in q_low:
        if len(st.session_state.learned) == 0:
            return "Je n'ai encore rien appris... 😅 Apprends-moi : Apprends : c'est quoi le foot = ..."
        txt = f"🧠 CE QUE TU M'AS APPRIS ({len(st.session_state.learned)}) :\n\n"
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
        return "Je peux traduire : bonjour, merci, au revoir, école, chat, chien, maison en anglais / allemand / espagnol / italien. Essaie : Traduis bonjour en anglais"
    q = q_low
    for mot in ["conjugue", "conjuguer", "c est quoi", "c est", "comment", "pourquoi", "donne moi", "c est qui", "qui est", "quel est", "quelle est", "comment calculer", "c koi", "c quoi"]:
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
        return "AVION LE PLUS PERFORMANT ? 1. Combat : F-22. 2. Moderne : F-35. 3. Vitesse : SR-71 - 3500 km/h. Mon choix : F-22 = le roi."
    if "capitale" in q:
        for pays, cap in CAPITALES.items():
            if nettoyer(pays) in q:
                return "Capitale de " + pays.capitalize() + " = " + cap
        return "J'ai plein de capitales ! Essaie : capitale du Japon..."
    # VERBES EN PRIORITE
    for cle, rep in VERBES.items():
        if nettoyer(cle) == q or nettoyer(cle) in q or q == nettoyer(cle):
            return rep
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
    return f"🤔 Hmm, je ne connais pas encore : '{q_orig}'...\n\nMais tu peux M'APPRENDRE ! Ecris :\n\nApprends : {q_orig} = ta réponse ici\n\n💡 Essaie :\n- Français → Verbes → Conjugue ETRE\n- Allemand → Verbes → Conjugue SEIN\n- Anglais → Verbes → Conjugue TO BE\n- Espagnol → Verbes → Conjugue SER\n- Italien → Verbes → Conjugue ESSERE"

if "auto_q" in st.session_state and st.session_state.auto_q:
    q_auto = st.session_state.auto_q
    st.session_state.auto_q = ""
    r_auto = trouver(q_auto)
    st.session_state.messages.append({"role": "assistant", "content": r_auto})
    with st.chat_message("assistant"):
        st.write(r_auto)

if question := st.chat_input("Pose ta question, ou choisis Matière → Genre → Verbe !"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        r = trouver(question)
        st.write(r)
    st.session_state.messages.append({"role": "assistant", "content": r})
