import streamlit as st
import random
import datetime
import re

st.set_page_config(page_title="Agent IA V5 - ULTIME", page_icon="🖤", layout="wide")

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
if "train_matiere" not in st.session_state:
    st.session_state.train_matiere = ""
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Salut ! Bienvenue dans la version ULTIME ! Choisis Matiere -> Genre -> Question en haut. Ex : Francais -> Verbes -> Conjugue ETRE. Ou ecris-moi ta question !"}]
if "auto_q" not in st.session_state:
    st.session_state.auto_q = ""

MATIERES_GENRES = {
    "📐 Maths": {
        "📐 Geometrie": ["C'est quoi le theoreme de Pythagore ?", "C'est quoi Thales ?", "C'est quoi l'aire ?", "C'est quoi le perimetre ?", "C'est quoi le volume ?", "C'est quoi un angle ?", "C'est quoi un triangle ?", "C'est quoi un cercle ?"],
        "🧮 Calcul": ["Table de 7", "Toutes les tables de multiplication", "Table de division de 8", "C'est quoi la moyenne ?", "Calcule 12+8", "Calcule 15x7", "C'est quoi la division ?"],
        "🍕 Fractions": ["C'est quoi une fraction ?", "C'est quoi le pourcentage ?", "C'est quoi une equation ?", "C'est quoi la racine carree ?"],
    },
    "🇫🇷 Français": {
        "📖 Grammaire": ["C'est quoi le COD ?", "C'est quoi le COI ?", "C'est quoi le sujet ?", "C'est quoi un adjectif ?", "C'est quoi le pluriel ?", "C'est quoi le verbe ?", "C'est quoi le pronom ?"],
        "✍️ Verbes les plus connus": ["Conjugue ETRE", "Conjugue AVOIR", "Conjugue ALLER", "Conjugue FAIRE", "Conjugue DIRE", "Conjugue POUVOIR", "Conjugue VOULOIR", "Conjugue SAVOIR", "Conjugue DEVOIR", "Conjugue VENIR", "Conjugue VOIR", "Conjugue PRENDRE", "Conjugue METTRE", "Conjugue DONNER", "Conjugue PARLER", "Conjugue MANGER", "Conjugue DORMIR", "Conjugue ECRIRE", "Conjugue LIRE", "Conjugue PARTIR", "Conjugue JOUER", "Conjugue APPRENDRE"],
        "📝 Orthographe": ["C'est quoi a / a ?", "C'est quoi et / est ?", "C'est quoi son / sont ?", "C'est quoi ces / ses ?", "C'est quoi ou / ou ?"],
        "📚 Vocabulaire": ["C'est quoi un synonyme ?", "C'est quoi un antonyme ?", "C'est quoi un homonyme ?", "C'est quoi une famille de mots ?"],
    },
    "🇩🇪 Allemand": {
        "📖 Grammaire": ["C'est quoi der die das ?", "C'est quoi l'accusatif ?", "C'est quoi le datif ?", "C'est quoi le nominatif ?"],
        "✍️ Verbes les plus connus": ["Conjugue SEIN", "Conjugue HABEN", "Conjugue GEHEN", "Conjugue MACHEN", "Conjugue KOMMEN", "Conjugue SEHEN", "Conjugue SPRECHEN", "Conjugue ESSEN", "Conjugue TRINKEN", "Conjugue LERNEN", "Conjugue WOHNEN", "Conjugue SPIELEN", "Conjugue ARBEITEN", "Conjugue KONNEN", "Conjugue WOLLEN", "Conjugue MUSSEN", "Conjugue WISSEN", "Conjugue GEBEN", "Conjugue NEHMEN", "Conjugue SCHREIBEN"],
        "🌍 Vocabulaire": ["Traduis bonjour en allemand", "Traduis merci en allemand", "Traduis ecole en allemand", "Traduis chien en allemand"],
    },
    "🇬🇧 Anglais": {
        "📖 Grammaire": ["C'est quoi le present simple ?", "C'est quoi le present perfect ?", "C'est quoi le present continu ?", "C'est quoi le preterit ?", "C'est quoi le comparatif ?"],
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
    "📜 Histoire / Geo": {
        "📜 Histoire": ["C'est quoi la 2eme Guerre ?", "C'est quoi la 1ere Guerre ?", "C'est quoi la Revolution ?", "C'est quoi Rome ?", "C'est quoi le Moyen Age ?", "C'est quoi l'Egypte ?", "C'est quoi Napoleon ?", "C'est quoi les dinosaures ?"],
        "🌍 Geographie": ["C'est quoi les continents ?", "C'est quoi les oceans ?", "Capitale du Japon ?", "Capitale de la France ?", "Capitale de la Suisse ?", "Capitale du Bresil ?"],
    },
    "🔬 Sciences": {
        "🧬 Biologie": ["C'est quoi la photosynthese ?", "C'est quoi le coeur ?", "C'est quoi l'ADN ?", "C'est quoi le cerveau ?", "C'est quoi les cellules ?"],
        "🌍 Terre / Espace": ["C'est quoi un volcan ?", "C'est quoi les saisons ?", "C'est quoi la foudre ?", "C'est quoi le systeme solaire ?", "C'est quoi un trou noir ?", "C'est quoi Mars ?", "C'est quoi le Big Bang ?"],
        "⚡ Physique": ["C'est quoi la gravite ?", "Comment calculer la masse volumique ?", "C'est quoi la vitesse ?", "C'est quoi l'energie ?", "C'est quoi la lumiere ?"],
    },
    "🧪 Chimie / Physique": {
        "⚛️ Chimie": ["C'est quoi un atome ?", "C'est quoi l'oxygene ?", "C'est quoi la chimie ?", "C'est quoi une molecule ?", "C'est quoi l'eau ?"],
        "⚡ Physique": ["C'est quoi l'electricite ?", "C'est quoi la masse volumique ?", "C'est quoi la vitesse ?", "C'est quoi la force ?"],
    },
    "💻 Code": {
        "🧠 Bases": ["C'est quoi une variable ?", "C'est quoi une boucle ?", "C'est quoi une condition ?", "C'est quoi une fonction ?", "C'est quoi une liste ?", "C'est quoi un algorithme ?"],
        "🌐 Langages": ["C'est quoi Python ?", "C'est quoi HTML ?", "C'est quoi CSS ?", "C'est quoi JavaScript ?", "C'est quoi l'IA ?"],
    },
    "🎨 Arts / Musique": {
        "🎨 Arts": ["C'est quoi la Joconde ?", "C'est quoi Van Gogh ?", "C'est quoi Picasso ?"],
        "🎵 Musique": ["C'est quoi le rap ?", "C'est quoi le piano ?", "C'est quoi la guitare ?", "C'est quoi une note ?"],
    },
    "🏃 Sport / Sante": {
        "⚽ Sports": ["C'est quoi le foot ?", "C'est quoi le basket ?", "C'est quoi le tennis ?", "C'est quoi la Formule 1 ?", "C'est quoi les JO ?"],
        "❤️ Sante": ["C'est quoi le coeur ?", "C'est quoi manger sain ?", "C'est quoi le sommeil ?"],
    },
}

THEMES = {
    "📐 Ecole": ["Voir toutes les matieres"],
    "👋 Bases": ["Bonjour", "Ca va ?", "Merci", "Au revoir", "Tu t'appelles comment ?", "Raconte une blague", "Motive moi", "Conseil pour reviser"],
    "🧠 Apprends-moi": ["Entraine moi", "Entrainement facile", "Entrainement difficile", "Entrainement verbes", "Mon score", "Montre ce que tu as appris", "Quiz Maths", "Quiz Francais", "Quiz Capitales"],
    "🧮 Calculatrice": ["Calcule 12+8", "Calcule 15x7", "Calcule 144/12", "Calcule 9x9"],
    "🌍 Traductions": ["Traduis bonjour en anglais", "Traduis merci en anglais", "Traduis bonjour en allemand", "Traduis bonjour en espagnol", "Traduis bonjour en italien"],
    "🎲 Fun": ["Raconte une blague", "Motive moi", "Conseil pour reviser", "Quelle heure il est ?", "Quelle date on est ?", "Devinette"],
    "🌍 Capitales": ["Capitale du Japon ?", "Capitale du Bresil ?", "Capitale de l'Egypte ?", "Capitale de la Suisse ?", "Capitale de la France ?", "Capitale du Canada ?"],
    "✈️ Avions": ["Quel est l'avion de chasse le plus performant ?", "C'est quoi le F-22 ?", "C'est quoi le 【entity-F-35¦canonical_name=F-35】 ?", "C'est quoi le Rafale ?", "C'est quoi le SR-71 ?", "C'est quoi le Concorde ?", "C'est quoi le A380 ?", "Comment vole un avion ?"],
    "💻 PC": ["C'est quoi le meilleur rapport qualite prix ?", "C'est quoi la meilleure GPU ?", "C'est quoi le meilleur CPU ?", "C'est quoi le meilleur SSD ?", "C'est quoi la meilleure RAM ?", "PC 2000 CHF", "PC 1300 CHF", "PC 900 CHF", "C'est quoi les FPS ?", "C'est quoi le ping ?"],
    "⚽ Foot / Sport": ["C'est qui 【entity-Messi¦canonical_name=Messi】 ?", "C'est qui 【entity-Ronaldo¦canonical_name=Ronaldo】 ?", "C'est qui 【entity-Mbappe¦canonical_name=Mbappe】 ?", "C'est quoi la Coupe du Monde ?", "C'est quoi la Ligue des Champions ?", "C'est quoi le Ballon d'Or ?", "C'est quoi le basket ?", "C'est quoi la Formule 1 ?"],
    "🎮 Jeux Video": ["C'est quoi 【entity-Minecraft¦canonical_name=MINECRAFT】 ?", "C'est quoi Fortnite ?", "C'est quoi Roblox ?", "C'est quoi GTA ?", "C'est quoi Brawl Stars ?", "C'est quoi Pokemon ?", "C'est quoi Mario ?", "C'est quoi One Piece ?", "C'est quoi Naruto ?", "C'est quoi Dragon Ball ?"],
    "🚀 Espace": ["C'est quoi un trou noir ?", "C'est quoi le Big Bang ?", "C'est quoi Mars ?", "C'est quoi l'ISS ?", "C'est quoi le Soleil ?", "C'est quoi une galaxie ?", "C'est quoi la Lune ?"],
    "🧠 Culture G": ["C'est qui Werenoi ?", "C'est qui Ninho ?", "C'est qui Jul ?", "C'est quoi la Tour Eiffel ?", "C'est quoi le Titanic ?", "C'est quoi 【entity-Harry Potter¦canonical_name=Harry Potter】 ?", "C'est quoi les pyramides ?"],
    "🎤 Chanteurs": ["C'est qui Werenoi ?", "C'est qui Ninho ?", "C'est qui Jul ?", "C'est qui Gazo ?", "C'est qui Tiakola ?", "C'est qui 【entity-PNL¦canonical_name=PNL】 ?", "C'est qui SDM ?", "C'est qui 【entity-Drake¦canonical_name=DRAKE】 ?", "C'est qui 【entity-Taylor Swift¦canonical_name=TAYLOR SWIFT】 ?", "C'est qui 【entity-Eminem¦canonical_name=EMINEM】 ?", "C'est qui 【entity-Stromae¦canonical_name=STROMAE】 ?", "C'est qui Soprano ?"],
    "💰 Argent / Metiers": ["Comment devenir millionnaire ?", "C'est quoi un salaire ?", "C'est quoi un entrepreneur ?", "Comment gagner de l'argent a 13 ans ?", "C'est quoi la bourse ?"],
    "🐾 Animaux": ["C'est quoi le plus grand animal ?", "C'est quoi le plus rapide ?", "C'est quoi un chien ?", "C'est quoi un chat ?", "C'est quoi un lion ?", "C'est quoi un dauphin ?"],
    "🍔 Cuisine": ["C'est quoi une recette facile ?", "C'est quoi un gateau au chocolat ?", "C'est quoi manger sain ?"],
}

with st.sidebar:
    st.title("Agent IA V5 - ULTIME")
    st.write("Appris : " + str(len(st.session_state.learned)))
    st.write("Score : " + str(st.session_state.score) + " / " + str(st.session_state.total_quiz))
    st.write("Streak : " + str(st.session_state.streak) + " | Best : " + str(st.session_state.best_streak))
    st.divider()
    st.write("MATIERES :")
    for m in MATIERES_GENRES.keys():
        if st.button(m, key="side_m_" + m, use_container_width=True):
            st.session_state.theme = "📐 Ecole"
            st.session_state.matiere = m
            st.session_state.genre = None
            st.rerun()
    st.divider()
    st.write("AUTRES :")
    for t in THEMES.keys():
        if t != "📐 Ecole":
            if st.button(t, key="side_" + t, use_container_width=True):
                st.session_state.theme = t
                st.session_state.matiere = None
                st.session_state.genre = None
                st.rerun()
    st.divider()
    if st.button("Effacer la conversation"):
        st.session_state.messages = []
        st.rerun()
    if st.button("Oublier ce que j'ai appris"):
        st.session_state.learned = {}
        st.session_state.score = 0
        st.session_state.total_quiz = 0
        st.session_state.streak = 0
        st.rerun()

st.title("Agent IA V5 - ULTIME")
st.caption("Appris : " + str(len(st.session_state.learned)) + " | Score : " + str(st.session_state.score) + "/" + str(st.session_state.total_quiz) + " | Streak : " + str(st.session_state.streak) + " | Fond noir discret")

if st.session_state.mode_train:
    st.success("ENTRAINEMENT " + st.session_state.niveau.upper() + " - Score : " + str(st.session_state.score) + "/" + str(st.session_state.total_quiz) + " - Streak : " + str(st.session_state.streak) + " - Ecris stop pour arreter")

if st.session_state.theme == "📐 Ecole":
    st.subheader("1 - Choisis ta MATIERE :")
    cols2 = st.columns(4)
    liste_matieres = list(MATIERES_GENRES.keys())
    for i in range(len(liste_matieres)):
        m = liste_matieres[i]
        with cols2[i % 4]:
            sel = "✅ " if st.session_state.matiere == m else ""
            if st.button(sel + m, key="mat_" + m, use_container_width=True):
                st.session_state.matiere = m
                st.session_state.genre = None
                st.rerun()
    if st.session_state.matiere:
        st.subheader("2 - Choisis ton GENRE :")
        genres = list(MATIERES_GENRES[st.session_state.matiere].keys())
        colsG = st.columns(len(genres))
        for i in range(len(genres)):
            g = genres[i]
            with colsG[i]:
                sel = "✅ " if st.session_state.genre == g else ""
                if st.button(sel + g, key="genre_" + g, use_container_width=True):
                    st.session_state.genre = g
                    st.rerun()
    if st.session_state.matiere and st.session_state.genre:
        st.subheader("3 - Clique sur une question :")
        for q in MATIERES_GENRES[st.session_state.matiere][st.session_state.genre]:
            if st.button(q, key="q_" + q, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": q})
                st.session_state.auto_q = q
                st.rerun()
        if st.button("Changer de genre / matiere", use_container_width=True):
            st.session_state.matiere = None
            st.session_state.genre = None
            st.rerun()
else:
    cols = st.columns(3)
    liste_themes = list(THEMES.keys())
    for i in range(len(liste_themes)):
        t = liste_themes[i]
        with cols[i % 3]:
            if st.button(t, key="top_" + t, use_container_width=True):
                st.session_state.theme = t
                st.session_state.matiere = None
                st.session_state.genre = None
                st.rerun()
    if st.session_state.theme != "📐 Ecole":
        st.subheader("Questions - Clique :")
        for q in THEMES.get(st.session_state.theme, []):
            if st.button(q, key="q2_" + q, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": q})
                st.session_state.auto_q = q
                st.rerun()

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
    "bonjour": "Bonjour ! Comment tu vas ? Choisis en haut : Matiere -> Genre -> Question. Ex : Francais -> Verbes -> Conjugue ETRE.",
    "salut": "Salut ! Ca va ? Choisis ta matiere en haut ou pose-moi ta question !",
    "slt": "Slt ! Ca va ?",
    "yo": "Yo ! Ca va ? Tu veux reviser quoi ?",
    "coucou": "Coucou ! Ca va bien ?",
    "hello": "Hello ! Ca va ? I can help you in English too !",
    "merci": "De rien ! Avec plaisir ! Tu as une autre question ?",
    "mrc": "De rien !",
    "ca va": "Ca va super bien merci ! Et toi, ca va ? Tu revises quelle matiere ?",
    "au revoir": "Au revoir ! A tres vite ! Reviens quand tu veux, je suis la !",
    "bye": "Bye ! A tres vite !",
    "bonne nuit": "Bonne nuit ! Dors bien ! A demain !",
    "t appelles comment": "Moi je m'appelle Agent IA V5 - ULTIME ! Et toi ?",
    "qui es tu": "Moi je suis Agent IA V5 ULTIME ! Ton assistant cree par Lenny. Je connais 10 matieres, 32 genres, 400+ questions, 85 verbes en 5 langues, 100+ capitales, PC, avions, chanteurs... et J'APPRENDS ce que tu m'apprends !",
    "aide moi": "Oui bien sur ! C'est pour quelle matiere ? Choisis en haut, ou ecris ta question !",
    "j ai pas compris": "T'inquiete ! Dis-moi ce que tu n'as pas compris, je vais te reexpliquer plus simplement, avec un autre exemple.",
    "t es trop fort": "Merciii ! Ca me fait trop plaisir !",
    "quelle heure": "Il est " + datetime.datetime.now().strftime("%H:%M") + " !",
    "quelle date": "On est le " + datetime.datetime.now().strftime("%d/%m/%Y") + " !",
    "devinette": "Devinette : Je suis toujours devant toi mais tu ne peux jamais me voir. Qui suis-je ? Reponse : Ton avenir ! Une autre : Qu'est-ce qui monte mais ne descend jamais ? Reponse : Ton age !",
}

BLAGUES = ["Pourquoi les plongeurs plongent-ils toujours en arriere ? Parce que sinon, ils tombent dans le bateau !", "Que dit un zero a un huit ? Belle ceinture !", "Pourquoi les maths sont tristes ? Parce qu'elles ont trop de problemes !", "Pourquoi les poissons n'aiment pas jouer au foot ? Parce qu'ils ont peur des filets !", "Que fait une fraise sur un cheval ? Tagada tagada !", "Pourquoi le livre de maths est deprime ? Parce qu'il a trop de problemes !"]
MOTIVATIONS = ["Tu peux le faire ! Chaque erreur, c'est une lecon. Ne lache rien !", "N'abandonne jamais ! 10 minutes par jour, tous les jours, et dans 1 mois tu seras trop fort !", "Tu es capable de beaucoup plus que tu crois ! Commence petit, 1 exercice, et ca va venir !"]
TRADUCTIONS = {"bonjour en anglais": "Bonjour en anglais = Hello / Good morning ! Ex : Hello, how are you ? = Bonjour, comment tu vas ?", "bonjour en allemand": "Bonjour en allemand = Hallo / Guten Tag ! Ex : Hallo, wie geht's ? = Salut, ca va ?", "bonjour en espagnol": "Bonjour en espagnol = Hola / Buenos dias !", "bonjour en italien": "Bonjour en italien = Ciao / Buongiorno !", "merci en anglais": "Merci en anglais = Thank you / Thanks !", "merci en allemand": "Merci en allemand = Danke !", "merci en espagnol": "Merci en espagnol = Gracias !", "merci en italien": "Merci en italien = Grazie !", "au revoir en anglais": "Au revoir en anglais = Goodbye / Bye !", "ecole en anglais": "Ecole en anglais = School ! Ex : I go to school = Je vais a l'ecole.", "chat en anglais": "Chat en anglais = Cat ! Chien = Dog", "chien en anglais": "Chien en anglais = Dog !", "maison en anglais": "Maison en anglais = House !", "ecole en allemand": "Ecole en allemand = Schule !", "chien en allemand": "Chien en allemand = Hund !", "ecole en espagnol": "Ecole en espagnol = Escuela !", "chien en espagnol": "Chien en espagnol = Perro !", "ecole en italien": "Ecole en italien = Scuola !"}
CAPITALES = {"france": "Paris - Tour Eiffel, Louvre. France = 68M d'habitants.", "suisse": "Berne - Capitale de la Suisse depuis 1848. Suisse = 8,9M d'habitants, 4 langues !", "allemagne": "Berlin - Mur de Berlin tombe en 1989.", "italie": "Rome - Colisee, Vatican, Pates, Pizza !", "espagne": "Madrid - 【entity-Real Madrid¦canonical_name=Real Madrid】.", "angleterre": "Londres - Big Ben, Buckingham Palace.", "japon": "Tokyo - Plus grande ville du monde ! Sushi, Manga, Anime.", "usa": "Washington D.C. - Maison Blanche. New York = plus grande ville, pas la capitale !", "canada": "Ottawa - Toronto = plus grande ville. 2 langues : francais + anglais.", "chine": "Pekin - Grande Muraille. Chine = 1,4 milliard !", "russie": "Moscou - Place Rouge, Kremlin.", "bresil": "Brasilia - Rio = plus connue, Christ Redempteur, Carnaval.", "inde": "New Delhi - Inde = 1,4 milliard, pays le plus peuple ! Taj Mahal.", "australie": "Canberra - Sydney = plus connue, 【entity-Opera¦canonical_name=Opera】. Kangourous !", "egypte": "Le Caire - Pyramides de Gizeh, Nil, Pharaons.", "maroc": "Rabat - Maroc, Couscous, Marrakech.", "portugal": "Lisbonne - Portugal, Cristiano 【entity-Ronaldo¦canonical_name=Ronaldo】 !", "belgique": "Bruxelles - Belgique, Frites, Chocolat, Gaufres !", "pays-bas": "Amsterdam - Pays-Bas, Canaux, Velos, Tulipes.", "autriche": "Vienne - Autriche, Mozart.", "suede": "Stockholm - Suede, 【entity-IKEA¦canonical_name=IKEA】, 【entity-ABBA¦canonical_name=ABBA】.", "norvege": "Oslo - Norvege, Fjords, 【entity-Haaland¦canonical_name=Haaland】 !", "danemark": "Copenhague - Danemark, 【entity-LEGO¦canonical_name=LEGO】.", "finlande": "Helsinki - Finlande, Pere Noel.", "pologne": "Varsovie - Pologne, Lewandowski.", "grece": "Athenes - Grece, Democratie, Jeux Olympiques, Zeus.", "turquie": "Ankara - Turquie, Istanbul = plus grande ville.", "coree": "Seoul - Coree du Sud, K-Pop (BTS), Samsung.", "mexique": "Mexico - Mexique, Tacos, Azteques.", "argentine": "Buenos Aires - Argentine, Tango, 【entity-Messi¦canonical_name=Messi】.", "colombie": "Bogota - Colombie, Cafe, Shakira.", "islande": "Reykjavik - Islande, Volcans, Aurores boreales.", "irlande": "Dublin - Irlande, Trefle, Saint-Patrick.", "monaco": "Monaco - 2 km2, 2eme plus petit pays ! Grand Prix F1.", "qatar": "Doha - Qatar, Coupe du Monde 2022 !", "cuba": "La Havane - Cuba, Salsa, Vieilles voitures.", "senegal": "Dakar - Senegal, Sadio Mane.", "madagascar": "Antananarivo - Madagascar, Lemuriens.", "nepal": "Katmandou - Nepal, Everest, 8848m, plus haut sommet du monde !", "indonesie": "Jakarta - Indonesie, 270M d'habitants, 17000 iles !", "singapour": "Singapour - Ville-pays, la plus propre, la plus riche d'Asie !", "nouvelle-zelande": "Wellington - Nouvelle-Zelande, Seigneur des Anneaux, All Blacks !", "jamaique": "Kingston - Jamaique, Bob Marley, 【entity-Usain Bolt¦canonical_name=Usain Bolt】 !"}
PC = {
    "rapport qualite prix": "MEILLEUR RAPPORT QUALITE / PRIX PC 2026 : GAGNANT 1300 CHF : RTX 5070 + Ryzen 7 7800X3D + 32 Go + SSD 1 To = 1300 CHF. 1440p Ultra 180 FPS. PETIT BUDGET 900 CHF : RTX 4060 + Ryzen 5 7600 = 900 CHF, 1080p 144 FPS. GROS BUDGET 2000 CHF : RTX 5070 Ti + 9800X3D = 2000 CHF, 240 FPS. MON CONSEIL : Prends le 1300 CHF !",
    "pc 900": "PC 900 CHF : RTX 4060 + Ryzen 5 7600 + 16 Go + SSD 1 To = 900 CHF. Fortnite 144 FPS, 1080p Ultra !",
    "pc 1300": "PC 1300 CHF - MEILLEUR RAPPORT : RTX 5070 + Ryzen 7 7800X3D + 32 Go DDR5 + SSD 1 To = 1300 CHF. 1440p Ultra 180 FPS !",
    "pc 2000": "PC 2000 CHF : RTX 5070 Ti + Ryzen 7 9800X3D + 32 Go + SSD 2 To = 2000 CHF. 240 FPS, 4K !",
    "meilleure gpu": "MEILLEURE GPU 2026 : 1. RTX 5090 - 32 Go, 4K Ultra 200 FPS, 2500 CHF. 2. RTX 5080 - 16 Go, 1200 CHF. 3. RTX 5070 - MEILLEUR RAPPORT : 12 Go, 1440p 180 FPS, 600 CHF.",
    "gpu": "GPU = Carte Graphique. Elle calcule toutes les images de tes jeux. RTX 4060 = 144 FPS en 1080p, RTX 5070 = 180 FPS en 1440p, RTX 5090 = 200 FPS en 4K.",
    "meilleur cpu": "MEILLEUR CPU 2026 : 1. Ryzen 9 9950X3D - ROI, 700 CHF. 2. Ryzen 7 9800X3D - ROI GAMING, 450 CHF. 3. Ryzen 7 7800X3D - MEILLEUR RAPPORT, 350 CHF.",
    "cpu": "CPU = Processeur, cerveau du PC. AMD Ryzen ou Intel Core. En 2026, AMD est devant pour les jeux.",
    "meilleur ssd": "MEILLEUR SSD : Samsung 990 PRO 2 To - 7450 Mo/s, Windows en 5 sec, 180 CHF. Meilleur rapport = WD Black 1 To - 70 CHF.",
    "meilleure ram": "MEILLEURE RAM : 32 Go DDR5 6000 MHz. Jeu + Discord + Chrome sans lag. 16 Go = minimum. 64 Go = montage pro.",
    "fps": "FPS = Images par seconde. 30 FPS = ca lag, 60 FPS = fluide, 144 FPS = super fluide, 240 FPS = pro. Pour Fortnite competitif, il faut 144 FPS minimum.",
    "ping": "PING = Temps de reponse internet. 10 ms = parfait, 30 ms = tres bien, 100 ms = ca lag, 200 ms = injouable. Pour baisser ton ping : cable Ethernet, fibre, serveur proche.",
}
CHANTEURS = {
    "werenoi": "WERENOI : Vrai nom Jeremy Bana Owona. Ne en 1994 a Melun. Il a commence le rap en 2021 avec Guadalajara. Il a explose en 2023 avec Pyramide et Solitaire. Albums : Pyramide, Pyramide 2, Diamant Noir. Le plus ecoute en France en 2024 et 2025 ! Sons : Solitaire, Ciao, Pyramide, Diamant Noir.",
    "ninho": "NINHO : Vrai nom William Nzobazola. Ne en 1996. Le rappeur avec le plus de disques d'or et de diamant en France ! Albums : M.I.L.S, Jefe, NI. Sons : Jefe, Lettre a une femme, Bolide allemand avec SDM.",
    "jul": "JUL : Vrai nom Julien Mari. Ne en 1990 a Marseille. Le plus productif : 2 albums par an ! Sons : Tchikita, JCVD, Bande organisee, 1 2 3. Il a vendu plus de 5M d'albums.",
    "gazo": "GAZO : Vrai nom Ibrahima Diakite. Ne en 1994 a Chateau Rouge, Paris. C'est lui qui a ramene la drill en France ! Albums : Drill FR, KMT, Apocalypse. Sons : Haine et Sex, Die, La Melo avec Tiakola.",
    "tiakola": "TIAKOLA : Vrai nom Tiakola Diakite. Ne en 1996 a Bondy, membre de 4Keus. Albums : Melo, BDLM. Sa voix melodique est unique. Sons : La Melo, Gasolina, Meuda.",
    "【entity-pnl¦canonical_name=PNL】": "【entity-PNL¦canonical_name=PNL】 : Duo de freres Ademo et N.O.S, de Corbeil-Essonnes. Albums : Le monde Chico, Dans la legende, Deux freres. Style : Cloud rap, planant. Sons : Le monde ou rien, DA, Au DD.",
    "sdm": "SDM : Vrai nom Beni Mosabu. Ne en 1995 a Clamart. Repere par Booba, signe chez 92i. Albums : Ocho, A vie. Il a explose avec Bolide allemand avec Ninho.",
    "【entity-drake¦canonical_name=DRAKE】": "【entity-DRAKE¦canonical_name=DRAKE】 : Rappeur canadien, le plus streame au monde. Albums : Take Care, Scorpion. Sons : God's Plan, One Dance, Hotline Bling.",
    "【entity-taylor swift¦canonical_name=TAYLOR SWIFT】": "【entity-TAYLOR SWIFT¦canonical_name=TAYLOR SWIFT】 : Chanteuse americaine, la plus ecoutee au monde. Albums : 1989, Midnights. 14 Grammy. Fans = Swifties. Son Eras Tour = tournee la plus rentable de l'histoire.",
    "【entity-eminem¦canonical_name=EMINEM】": "【entity-EMINEM¦canonical_name=EMINEM】 : Rappeur americain, legende. Albums : The Slim Shady LP, Recovery. Sons : Lose Yourself, Rap God, Mockingbird. 220M d'albums vendus.",
    "【entity-stromae¦canonical_name=STROMAE】": "【entity-STROMAE¦canonical_name=STROMAE】 : Chanteur belge, vrai nom Paul Van Haver. Albums : Cheese, Racine carree, Multitude. Sons : Alors on danse, Papaoutai, Formidable, L'enfer.",
    "soprano": "SOPRANO : Chanteur / rappeur de Marseille. Albums : La Colombe, L'Everest, Chasseur d'etoiles. Sons : Cosmo, En feu, A la vie, a l'amour, Mon Everest.",
}

VERBES = {
    "etre": "ETRE - Francais. Sens : etre, decrire. Ex : Je suis content. PRESENT : je suis, tu es, il est, nous sommes, vous etes, ils sont. PASSE COMPOSE : j'ai ete, tu as ete, il a ete, nous avons ete, vous avez ete, ils ont ete. IMPARFAIT : j'etais, tu etais, il etait, nous etions, vous etiez, ils etaient. FUTUR : je serai, tu seras, il sera, nous serons, vous serez, ils seront.",
    "avoir": "AVOIR - Francais. Sens : posseder. Ex : J'ai 13 ans. PRESENT : j'ai, tu as, il a, nous avons, vous avez, ils ont. PASSE COMPOSE : j'ai eu, tu as eu, il a eu, nous avons eu, vous avez eu, ils ont eu. IMPARFAIT : j'avais, tu avais, il avait, nous avions, vous aviez, ils avaient. FUTUR : j'aurai, tu auras, il aura, nous aurons, vous aurez, ils auront.",
    "aller": "ALLER - Francais. Sens : se deplacer. Ex : Je vais a l'ecole. PRESENT : je vais, tu vas, il va, nous allons, vous allez, ils vont. PASSE COMPOSE : je suis alle, tu es alle, il est alle, nous sommes alles, vous etes alles, ils sont alles. IMPARFAIT : j'allais, tu allais, il allait, nous allions, vous alliez, ils allaient. FUTUR : j'irai, tu iras, il ira, nous irons, vous irez, ils iront.",
    "faire": "FAIRE - Francais. Sens : creer. Ex : Je fais mes devoirs. PRESENT : je fais, tu fais, il fait, nous faisons, vous faites, ils font. PASSE COMPOSE : j'ai fait, tu as fait, il a fait, nous avons fait, vous avez fait, ils ont fait. IMPARFAIT : je faisais, tu faisais, il faisait, nous faisions, vous faisiez, ils faisaient. FUTUR : je ferai, tu feras, il fera, nous ferons, vous ferez, ils feront.",
    "dire": "DIRE - Francais. Sens : parler. Ex : Je dis bonjour. PRESENT : je dis, tu dis, il dit, nous disons, vous dites, ils disent. PASSE COMPOSE : j'ai dit, tu as dit, il a dit, nous avons dit, vous avez dit, ils ont dit. IMPARFAIT : je disais, tu disais, il disait, nous disions, vous disiez, ils disaient. FUTUR : je dirai, tu diras, il dira, nous dirons, vous direz, ils diront.",
    "pouvoir": "POUVOIR - Francais. Sens : etre capable. Ex : Je peux jouer. PRESENT : je peux, tu peux, il peut, nous pouvons, vous pouvez, ils peuvent. PASSE COMPOSE : j'ai pu, tu as pu, il a pu, nous avons pu, vous avez pu, ils ont pu. IMPARFAIT : je pouvais, tu pouvais, il pouvait, nous pouvions, vous pouviez, ils pouvaient. FUTUR : je pourrai, tu pourras, il pourra, nous pourrons, vous pourrez, ils pourront.",
    "vouloir": "VOULOIR - Francais. Sens : desirer. Ex : Je veux jouer. PRESENT : je veux, tu veux, il veut, nous voulons, vous voulez, ils veulent. PASSE COMPOSE : j'ai voulu, tu as voulu, il a voulu, nous avons voulu, vous avez voulu, ils ont voulu. IMPARFAIT : je voulais, tu voulais, il voulait, nous voulions, vous vouliez, ils voulaient. FUTUR : je voudrai, tu voudras, il voudra, nous voudrons, vous voudrez, ils voudront.",
    "savoir": "SAVOIR - Francais. Sens : connaitre un fait. Ex : Je sais nager. PRESENT : je sais, tu sais, il sait, nous savons, vous savez, ils savent. PASSE COMPOSE : j'ai su, tu as su, il a su, nous avons su, vous avez su, ils ont su. IMPARFAIT : je savais, tu savais, il savait, nous savions, vous saviez, ils savaient. FUTUR : je saurai, tu sauras, il saura, nous saurons, vous saurez, ils sauront.",
    "devoir": "DEVOIR - Francais. Sens : obligation. Ex : Je dois faire mes devoirs. PRESENT : je dois, tu dois, il doit, nous devons, vous devez, ils doivent. PASSE COMPOSE : j'ai du, tu as du, il a du, nous avons du, vous avez du, ils ont du. IMPARFAIT : je devais, tu devais, il devait, nous devions, vous deviez, ils devaient. FUTUR : je devrai, tu devras, il devra, nous devrons, vous devrez, ils devront.",
    "venir": "VENIR - Francais. Sens : arriver. Ex : Je viens de l'ecole. PRESENT : je viens, tu viens, il vient, nous venons, vous venez, ils viennent. PASSE COMPOSE : je suis venu, tu es venu, il est venu, nous sommes venus, vous etes venus, ils sont venus. IMPARFAIT : je venais, tu venais, il venait, nous venions, vous veniez, ils venaient. FUTUR : je viendrai, tu viendras, il viendra, nous viendrons, vous viendrez, ils viendront.",
    "voir": "VOIR - Francais. Sens : regarder. Ex : Je vois un film. PRESENT : je vois, tu vois, il voit, nous voyons, vous voyez, ils voient. PASSE COMPOSE : j'ai vu, tu as vu, il a vu, nous avons vu, vous avez vu, ils ont vu. IMPARFAIT : je voyais, tu voyais, il voyait, nous voyions, vous voyiez, ils voyaient. FUTUR : je verrai, tu verras, il verra, nous verrons, vous verrez, ils verront.",
    "prendre": "PRENDRE - Francais. Sens : attraper. Ex : Je prends le bus. PRESENT : je prends, tu prends, il prend, nous prenons, vous prenez, ils prennent. PASSE COMPOSE : j'ai pris, tu as pris, il a pris, nous avons pris, vous avez pris, ils ont pris. IMPARFAIT : je prenais, tu prenais, il prenait, nous prenions, vous preniez, ils prenaient. FUTUR : je prendrai, tu prendras, il prendra, nous prendrons, vous prendrez, ils prendront.",
    "mettre": "METTRE - Francais. Sens : placer. Ex : Je mets mes chaussures. PRESENT : je mets, tu mets, il met, nous mettons, vous mettez, ils mettent. PASSE COMPOSE : j'ai mis, tu as mis, il a mis, nous avons mis, vous avez mis, ils ont mis. IMPARFAIT : je mettais, tu mettais, il mettait, nous mettions, vous mettiez, ils mettaient. FUTUR : je mettrai, tu mettras, il mettra, nous mettrons, vous mettrez, ils mettront.",
    "donner": "DONNER - Francais. Sens : offrir. Ex : Je donne un cadeau. PRESENT : je donne, tu donnes, il donne, nous donnons, vous donnez, ils donnent. PASSE COMPOSE : j'ai donne, tu as donne, il a donne, nous avons donne, vous avez donne, ils ont donne. IMPARFAIT : je donnais, tu donnais, il donnait, nous donnions, vous donniez, ils donnaient. FUTUR : je donnerai, tu donneras, il donnera, nous donnerons, vous donnerez, ils donneront.",
    "parler": "PARLER - Francais. Sens : dire avec la voix. Ex : Je parle francais. PRESENT : je parle, tu parles, il parle, nous parlons, vous parlez, ils parlent. PASSE COMPOSE : j'ai parle, tu as parle, il a parle, nous avons parle, vous avez parle, ils ont parle. IMPARFAIT : je parlais, tu parlais, il parlait, nous parlions, vous parliez, ils parlaient. FUTUR : je parlerai, tu parleras, il parlera, nous parlerons, vous parlerez, ils parleront.",
    "manger": "MANGER - Francais. Sens : avaler. Ex : Je mange une pizza. PRESENT : je mange, tu manges, il mange, nous mangeons, vous mangez, ils mangent. PASSE COMPOSE : j'ai mange, tu as mange, il a mange, nous avons mange, vous avez mange, ils ont mange. IMPARFAIT : je mangeais, tu mangeais, il mangeait, nous mangions, vous mangiez, ils mangeaient. FUTUR : je mangerai, tu mangeras, il mangera, nous mangerons, vous mangerez, ils mangeront.",
    "dormir": "DORMIR - Francais. Sens : etre endormi. Ex : Je dors bien. PRESENT : je dors, tu dors, il dort, nous dormons, vous dormez, ils dorment. PASSE COMPOSE : j'ai dormi, tu as dormi, il a dormi, nous avons dormi, vous avez dormi, ils ont dormi. IMPARFAIT : je dormais, tu dormais, il dormait, nous dormions, vous dormiez, ils dormaient. FUTUR : je dormirai, tu dormiras, il dormira, nous dormirons, vous dormirez, ils dormiront.",
    "ecrire": "ECRIRE - Francais. Sens : ecrire. Ex : J'ecris une lettre. PRESENT : j'ecris, tu ecris, il ecrit, nous ecrivons, vous ecrivez, ils ecrivent. PASSE COMPOSE : j'ai ecrit, tu as ecrit, il a ecrit, nous avons ecrit, vous avez ecrit, ils ont ecrit. IMPARFAIT : j'ecrivais, tu ecrivais, il ecrivait, nous ecrivions, vous ecriviez, ils ecrivaient. FUTUR : j'ecrirai, tu ecriras, il ecrira, nous ecrirons, vous ecrirez, ils ecriront.",
    "lire": "LIRE - Francais. Sens : lire un livre. Ex : Je lis Harry Potter. PRESENT : je lis, tu lis, il lit, nous lisons, vous lisez, ils lisent. PASSE COMPOSE : j'ai lu, tu as lu, il a lu, nous avons lu, vous avez lu, ils ont lu. IMPARFAIT : je lisais, tu lisais, il lisait, nous lisions, vous lisiez, ils lisaient. FUTUR : je lirai, tu liras, il lira, nous lirons, vous lirez, ils liront.",
    "partir": "PARTIR - Francais. Sens : quitter. Ex : Je pars a l'ecole. PRESENT : je pars, tu pars, il part, nous partons, vous partez, ils partent. PASSE COMPOSE : je suis parti, tu es parti, il est parti, nous sommes partis, vous etes partis, ils sont partis. IMPARFAIT : je partais, tu partais, il partait, nous partions, vous partiez, ils partaient. FUTUR : je partirai, tu partiras, il partira, nous partirons, vous partirez, ils partiront.",
    "jouer": "JOUER - Francais. Sens : jouer. Ex : Je joue au foot. PRESENT : je joue, tu joues, il joue, nous jouons, vous jouez, ils jouent. PASSE COMPOSE : j'ai joue, tu as joue, il a joue, nous avons joue, vous avez joue, ils ont joue. IMPARFAIT : je jouais, tu jouais, il jouait, nous jouions, vous jouiez, ils jouaient. FUTUR : je jouerai, tu joueras, il jouera, nous jouerons, vous jouerez, ils joueront.",
    "apprendre": "APPRENDRE - Francais. Sens : apprendre. Ex : J'apprends l'allemand. PRESENT : j'apprends, tu apprends, il apprend, nous apprenons, vous apprenez, ils apprennent. PASSE COMPOSE : j'ai appris, tu as appris, il a appris, nous avons appris, vous avez appris, ils ont appris. IMPARFAIT : j'apprenais, tu apprenais, il apprenait, nous apprenions, vous appreniez, ils apprenaient. FUTUR : j'apprendrai, tu apprendras, il apprendra, nous apprendrons, vous apprendrez, ils apprendront.",
    "sein": "SEIN = ETRE en Allemand. Sens : etre. Ex : Ich bin 13 Jahre alt = J'ai 13 ans. PRASENS : ich bin, du bist, er ist, wir sind, ihr seid, sie sind. PERFEKT : ich bin gewesen. PRATERITUM : ich war, du warst, er war, wir waren, ihr wart, sie waren. FUTUR : ich werde sein.",
    "haben": "HABEN = AVOIR en Allemand. Sens : avoir. Ex : Ich habe einen Hund = J'ai un chien. PRASENS : ich habe, du hast, er hat, wir haben, ihr habt, sie haben. PERFEKT : ich habe gehabt. PRATERITUM : ich hatte. FUTUR : ich werde haben.",
    "gehen": "GEHEN = ALLER en Allemand. Sens : aller. Ex : Ich gehe zur Schule. PRASENS : ich gehe, du gehst, er geht, wir gehen, ihr geht, sie gehen. PERFEKT : ich bin gegangen. PRATERITUM : ich ging. FUTUR : ich werde gehen.",
    "machen": "MACHEN = FAIRE en Allemand. Sens : faire. Ex : Ich mache meine Hausaufgaben. PRASENS : ich mache, du machst, er macht, wir machen, ihr macht, sie machen. PERFEKT : ich habe gemacht. PRATERITUM : ich machte. FUTUR : ich werde machen.",
    "kommen": "KOMMEN = VENIR en Allemand. Sens : venir. Ex : Ich komme aus der Schweiz. PRASENS : ich komme, du kommst, er kommt, wir kommen, ihr kommt, sie kommen. PERFEKT : ich bin gekommen. PRATERITUM : ich kam. FUTUR : ich werde kommen.",
    "sehen": "SEHEN = VOIR en Allemand. Sens : voir. Ex : Ich sehe einen Film. PRASENS : ich sehe, du siehst, er sieht, wir sehen, ihr seht, sie sehen. PERFEKT : ich habe gesehen. PRATERITUM : ich sah. FUTUR : ich werde sehen.",
    "sprechen": "SPRECHEN = PARLER en Allemand. Sens : parler. Ex : Ich spreche Deutsch. PRASENS : ich spreche, du sprichst, er spricht, wir sprechen, ihr sprecht, sie sprechen. PERFEKT : ich habe gesprochen. PRATERITUM : ich sprach. FUTUR : ich werde sprechen.",
    "essen": "ESSEN = MANGER en Allemand. Sens : manger. Ex : Ich esse Pizza. PRASENS : ich esse, du isst, er isst, wir essen, ihr esst, sie essen. PERFEKT : ich habe gegessen. PRATERITUM : ich ass. FUTUR : ich werde essen.",
    "trinken": "TRINKEN = BOIRE en Allemand. Sens : boire. Ex : Ich trinke Wasser. PRASENS : ich trinke, du trinkst, er trinkt, wir trinken, ihr trinkt, sie trinken. PERFEKT : ich habe getrunken. PRATERITUM : ich trank. FUTUR : ich werde trinken.",
    "lernen": "LERNEN = APPRENDRE en Allemand. Sens : apprendre. Ex : Ich lerne Deutsch. PRASENS : ich lerne, du lernst, er lernt, wir lernen, ihr lernt, sie lernen. PERFEKT : ich habe gelernt. PRATERITUM : ich lernte. FUTUR : ich werde lernen.",
    "wohnen": "WOHNEN = HABITER en Allemand. Sens : habiter. Ex : Ich wohne in Estavayer. PRASENS : ich wohne, du wohnst, er wohnt, wir wohnen, ihr wohnt, sie wohnen. PERFEKT : ich habe gewohnt. PRATERITUM : ich wohnte. FUTUR : ich werde wohnen.",
    "spielen": "SPIELEN = JOUER en Allemand. Sens : jouer. Ex : Ich spiele Fussball. PRASENS : ich spiele, du spielst, er spielt, wir spielen, ihr spielt, sie spielen. PERFEKT : ich habe gespielt. PRATERITUM : ich spielte. FUTUR : ich werde spielen.",
    "arbeiten": "ARBEITEN = TRAVAILLER en Allemand. Sens : travailler. PRASENS : ich arbeite, du arbeitest, er arbeitet, wir arbeiten, ihr arbeitet, sie arbeiten. PERFEKT : ich habe gearbeitet. PRATERITUM : ich arbeitete. FUTUR : ich werde arbeiten.",
    "konnen": "KONNEN = POUVOIR en Allemand. Sens : pouvoir. Ex : Ich kann schwimmen. PRASENS : ich kann, du kannst, er kann, wir konnen, ihr konnt, sie konnen. PERFEKT : ich habe gekonnt. PRATERITUM : ich konnte. FUTUR : ich werde konnen.",
    "wollen": "WOLLEN = VOULOIR en Allemand. Sens : vouloir. Ex : Ich will spielen. PRASENS : ich will, du willst, er will, wir wollen, ihr wollt, sie wollen. PERFEKT : ich habe gewollt. PRATERITUM : ich wollte. FUTUR : ich werde wollen.",
    "mussen": "MUSSEN = DEVOIR en Allemand. Sens : devoir. Ex : Ich muss lernen. PRASENS : ich muss, du musst, er muss, wir mussen, ihr musst, sie mussen. PERFEKT : ich habe gemusst. PRATERITUM : ich musste. FUTUR : ich werde mussen.",
    "wissen": "WISSEN = SAVOIR en Allemand. Sens : savoir. Ex : Ich weiss das. PRASENS : ich weiss, du weisst, er weiss, wir wissen, ihr wisst, sie wissen. PERFEKT : ich habe gewusst. PRATERITUM : ich wusste. FUTUR : ich werde wissen.",
    "geben": "GEBEN = DONNER en Allemand. Sens : donner. Ex : Ich gebe dir ein Buch. PRASENS : ich gebe, du gibst, er gibt, wir geben, ihr gebt, sie geben. PERFEKT : ich habe gegeben. PRATERITUM : ich gab. FUTUR : ich werde geben.",
    "nehmen": "NEHMEN = PRENDRE en Allemand. Sens : prendre. Ex : Ich nehme den Bus. PRASENS : ich nehme, du nimmst, er nimmt, wir nehmen, ihr nehmt, sie nehmen. PERFEKT : ich habe genommen. PRATERITUM : ich nahm. FUTUR : ich werde nehmen.",
    "schreiben": "SCHREIBEN = ECRIRE en Allemand. Sens : ecrire. Ex : Ich schreibe einen Brief. PRASENS : ich schreibe, du schreibst, er schreibt, wir schreiben, ihr schreibt, sie schreiben. PERFEKT : ich habe geschrieben. PRATERITUM : ich schrieb. FUTUR : ich werde schreiben.",
    "to be": "TO BE = ETRE en Anglais. Sens : etre. Ex : I am happy. PRESENT : I am, You are, He is, We are, You are, They are. PAST : I was, You were, He was, We were, You were, They were. PERFECT : I have been. FUTURE : I will be.",
    "to have": "TO HAVE = AVOIR en Anglais. Sens : avoir. Ex : I have a dog. PRESENT : I have, You have, He has, We have, You have, They have. PAST : I had. PERFECT : I have had. FUTURE : I will have.",
    "to go": "TO GO = ALLER en Anglais. Sens : aller. Ex : I go to school. PRESENT : I go, You go, He goes, We go, You go, They go. PAST : I went. PERFECT : I have gone. FUTURE : I will go.",
    "to do": "TO DO = FAIRE en Anglais. Sens : faire. Ex : I do my homework. PRESENT : I do, You do, He does, We do, You do, They do. PAST : I did. PERFECT : I have done. FUTURE : I will do.",
    "to say": "TO SAY = DIRE en Anglais. Sens : dire. Ex : I say hello. PRESENT : I say, You say, He says, We say, You say, They say. PAST : I said. PERFECT : I have said. FUTURE : I will say.",
    "to see": "TO SEE = VOIR en Anglais. Sens : voir. Ex : I see a film. PRESENT : I see, You see, He sees, We see, You see, They see. PAST : I saw. PERFECT : I have seen. FUTURE : I will see.",
    "to come": "TO COME = VENIR en Anglais. Sens : venir. Ex : I come from Switzerland. PRESENT : I come, You come, He comes, We come. PAST : I came. PERFECT : I have come. FUTURE : I will come.",
    "to get": "TO GET = OBTENIR en Anglais. Sens : obtenir. Ex : I get up = Je me leve. PRESENT : I get, You get, He gets. PAST : I got. PERFECT : I have got. FUTURE : I will get.",
    "to make": "TO MAKE = FABRIQUER en Anglais. Sens : fabriquer. Ex : I make a cake. PRESENT : I make, You make, He makes. PAST : I made. PERFECT : I have made. FUTURE : I will make.",
    "to take": "TO TAKE = PRENDRE en Anglais. Sens : prendre. Ex : I take the bus. PRESENT : I take, You take, He takes. PAST : I took. PERFECT : I have taken. FUTURE : I will take.",
    "to give": "TO GIVE = DONNER en Anglais. Sens : donner. Ex : I give a gift. PRESENT : I give, You give, He gives. PAST : I gave. PERFECT : I have given. FUTURE : I will give.",
    "to know": "TO KNOW = SAVOIR en Anglais. Sens : savoir. Ex : I know you. PRESENT : I know, You know, He knows. PAST : I knew. PERFECT : I have known. FUTURE : I will know.",
    "to think": "TO THINK = PENSER en Anglais. Sens : penser. Ex : I think it's cool. PRESENT : I think, You think, He thinks. PAST : I thought. PERFECT : I have thought. FUTURE : I will think.",
    "to speak": "TO SPEAK = PARLER en Anglais. Sens : parler. Ex : I speak English. PRESENT : I speak, You speak, He speaks. PAST : I spoke. PERFECT : I have spoken. FUTURE : I will speak.",
    "to eat": "TO EAT = MANGER en Anglais. Sens : manger. Ex : I eat pizza. PRESENT : I eat, You eat, He eats. PAST : I ate. PERFECT : I have eaten. FUTURE : I will eat.",
    "to drink": "TO DRINK = BOIRE en Anglais. Sens : boire. Ex : I drink water. PRESENT : I drink, You drink, He drinks. PAST : I drank. PERFECT : I have drunk. FUTURE : I will drink.",
    "to play": "TO PLAY = JOUER en Anglais. Sens : jouer. Ex : I play football. PRESENT : I play, You play, He plays. PAST : I played. PERFECT : I have played. FUTURE : I will play.",
    "to live": "TO LIVE = VIVRE en Anglais. Sens : vivre. Ex : I live in Switzerland. PRESENT : I live, You live, He lives. PAST : I lived. PERFECT : I have lived. FUTURE : I will live.",
    "to love": "TO LOVE = AIMER en Anglais. Sens : aimer. Ex : I love football. PRESENT : I love, You love, He loves. PAST : I loved. PERFECT : I have loved. FUTURE : I will love.",
    "to want": "TO WANT = VOULOIR en Anglais. Sens : vouloir. Ex : I want to play. PRESENT : I want, You want, He wants. PAST : I wanted. PERFECT : I have wanted. FUTURE : I will want.",
    "ser": "SER = ETRE en Espagnol (identite). Sens : etre permanent. Ex : Soy de Suiza. PRESENTE : yo soy, tu eres, el es, nosotros somos, vosotros sois, ellos son. PRETERITO : yo fui, tu fuiste, el fue, nosotros fuimos, vosotros fuisteis, ellos fueron. IMPERFECTO : yo era, tu eras, el era, nosotros eramos, vosotros erais, ellos eran. FUTURO : yo sere, tu seras, el sera.",
    "estar": "ESTAR = ETRE en Espagnol (etat / lieu). Sens : etre temporaire. Ex : Estoy en casa. PRESENTE : yo estoy, tu estas, el esta, nosotros estamos, vosotros estais, ellos estan. PRETERITO : yo estuve. IMPERFECTO : yo estaba. FUTURO : yo estare.",
    "tener": "TENER = AVOIR en Espagnol. Sens : avoir. Ex : Tengo 13 anos. PRESENTE : yo tengo, tu tienes, el tiene, nosotros tenemos, vosotros teneis, ellos tienen. PRETERITO : yo tuve. IMPERFECTO : yo tenia. FUTURO : yo tendre.",
    "ir": "IR = ALLER en Espagnol. Sens : aller. Ex : Voy a la escuela. PRESENTE : yo voy, tu vas, el va, nosotros vamos, vosotros vais, ellos van. PRETERITO : yo fui. IMPERFECTO : yo iba. FUTURO : yo ire.",
    "hacer": "HACER = FAIRE en Espagnol. Sens : faire. Ex : Hago mis deberes. PRESENTE : yo hago, tu haces, el hace, nosotros hacemos, vosotros haceis, ellos hacen. PRETERITO : yo hice. IMPERFECTO : yo hacia. FUTURO : yo hare.",
    "decir": "DECIR = DIRE en Espagnol. Sens : dire. Ex : Digo hola. PRESENTE : yo digo, tu dices, el dice, nosotros decimos, vosotros decis, ellos dicen. PRETERITO : yo dije. IMPERFECTO : yo decia. FUTURO : yo dire.",
    "poder": "PODER = POUVOIR en Espagnol. Sens : pouvoir. Ex : Puedo jugar. PRESENTE : yo puedo, tu puedes, el puede, nosotros podemos, vosotros podeis, ellos pueden. PRETERITO : yo pude. IMPERFECTO : yo podia. FUTURO : yo podre.",
    "querer": "QUERER = VOULOIR en Espagnol. Sens : vouloir. Ex : Quiero jugar. PRESENTE : yo quiero, tu quieres, el quiere, nosotros queremos, vosotros quereis, ellos quieren. PRETERITO : yo quise. IMPERFECTO : yo queria. FUTURO : yo querre.",
    "saber": "SABER = SAVOIR en Espagnol. Sens : savoir. Ex : Se nadar. PRESENTE : yo se, tu sabes, el sabe, nosotros sabemos, vosotros sabeis, ellos saben. PRETERITO : yo supe. IMPERFECTO : yo sabia. FUTURO : yo sabre.",
    "hablar": "HABLAR = PARLER en Espagnol. Sens : parler. Ex : Hablo espanol. PRESENTE : yo hablo, tu hablas, el habla, nosotros hablamos, vosotros hablais, ellos hablan. PRETERITO : yo hable. IMPERFECTO : yo hablaba. FUTURO : yo hablare.",
    "comer": "COMER = MANGER en Espagnol. Sens : manger. Ex : Como pizza. PRESENTE : yo como, tu comes, el come, nosotros comemos, vosotros comeis, ellos comen. PRETERITO : yo comi. IMPERFECTO : yo comia. FUTURO : yo comere.",
    "vivir": "VIVIR = VIVRE en Espagnol. Sens : vivre. Ex : Vivo en Suiza. PRESENTE : yo vivo, tu vives, el vive, nosotros vivimos, vosotros vivis, ellos viven. PRETERITO : yo vivi. IMPERFECTO : yo vivia. FUTURO : yo vivire.",
    "jugar": "JUGAR = JOUER en Espagnol. Sens : jouer. Ex : Juego al futbol. PRESENTE : yo juego, tu juegas, el juega, nosotros jugamos, vosotros jugais, ellos juegan. PRETERITO : yo jugue. IMPERFECTO : yo jugaba. FUTURO : yo jugare.",
    "essere": "ESSERE = ETRE en Italien. Sens : etre. Ex : Sono contento. PRESENTE : io sono, tu sei, lui e, noi siamo, voi siete, loro sono. PASSATO : io sono stato. IMPERFETTO : io ero, tu eri, lui era, noi eravamo, voi eravate, loro erano. FUTURO : io saro, tu sarai, lui sara.",
    "avere": "AVERE = AVOIR en Italien. Sens : avoir. Ex : Ho 13 anni. PRESENTE : io ho, tu hai, lui ha, noi abbiamo, voi avete, loro hanno. PASSATO : io ho avuto. IMPERFETTO : io avevo. FUTURO : io avro.",
    "andare": "ANDARE = ALLER en Italien. Sens : aller. Ex : Vado a scuola. PRESENTE : io vado, tu vai, lui va, noi andiamo, voi andate, loro vanno. PASSATO : io sono andato. IMPERFETTO : io andavo. FUTURO : io andro.",
    "fare": "FARE = FAIRE en Italien. Sens : faire. Ex : Faccio i compiti. PRESENTE : io faccio, tu fai, lui fa, noi facciamo, voi fate, loro fanno. PASSATO : io ho fatto. IMPERFETTO : io facevo. FUTURO : io faro.",
    "potere": "POTERE = POUVOIR en Italien. Sens : pouvoir. Ex : Posso giocare. PRESENTE : io posso, tu puoi, lui puo, noi possiamo, voi potete, loro possono. PASSATO : io ho potuto. IMPERFETTO : io potevo. FUTURO : io potro.",
    "volere": "VOLERE = VOULOIR en Italien. Sens : vouloir. Ex : Voglio giocare. PRESENTE : io voglio, tu vuoi, lui vuole, noi vogliamo, voi volete, loro vogliono. PASSATO : io ho voluto. IMPERFETTO : io volevo. FUTURO : io vorro.",
    "sapere": "SAPERE = SAVOIR en Italien. Sens : savoir. Ex : So nuotare. PRESENTE : io so, tu sai, lui sa, noi sappiamo, voi sapete, loro sanno. PASSATO : io ho saputo. IMPERFETTO : io sapevo. FUTURO : io sapro.",
    "venire": "VENIRE = VENIR en Italien. Sens : venir. Ex : Vengo dalla Svizzera. PRESENTE : io vengo, tu vieni, lui viene, noi veniamo, voi venite, loro vengono. PASSATO : io sono venuto. IMPERFETTO : io venivo. FUTURO : io verro.",
    "vedere": "VEDERE = VOIR en Italien. Sens : voir. Ex : Vedo un film. PRESENTE : io vedo, tu vedi, lui vede, noi vediamo, voi vedete, loro vedono. PASSATO : io ho visto. IMPERFETTO : io vedevo. FUTURO : io vedro.",
    "parlare": "PARLARE = PARLER en Italien. Sens : parler. Ex : Parlo italiano. PRESENTE : io parlo, tu parli, lui parla, noi parliamo, voi parlate, loro parlano. PASSATO : io ho parlato. IMPERFETTO : io parlavo. FUTURO : io parlero.",
    "mangiare": "MANGIARE = MANGER en Italien. Sens : manger. Ex : Mangio la pizza. PRESENTE : io mangio, tu mangi, lui mangia, noi mangiamo, voi mangiate, loro mangiano. PASSATO : io ho mangiato. IMPERFETTO : io mangiavo. FUTURO : io mangero.",
    "giocare": "GIOCARE = JOUER en Italien. Sens : jouer. Ex : Gioco a calcio. PRESENTE : io gioco, tu giochi, lui gioca, noi giochiamo, voi giocate, loro giocano. PASSATO : io ho giocato. IMPERFETTO : io giocavo. FUTURO : io giochero.",
}

TOUT = {
    "pythagore": "THEOREME DE PYTHAGORE : Formule : a2 + b2 = c2. UNIQUEMENT pour un triangle rectangle. Ex : 3-4-5 car 9+16=25. Ex : Si a=6, b=8, alors c2 = 36+64=100, donc c=10.",
    "thales": "THALES : Si 2 droites paralleles coupent 2 secantes, rapports egaux. Formule : AB / AD = AC / AE = BC / DE.",
    "moyenne": "MOYENNE : Moyenne = somme / nombre. Ex : Notes 12, 15, 18. Somme = 45. Nombre = 3. Moyenne = 45 / 3 = 15.",
    "aire": "AIRE : Rectangle = L x l, Carre = cote x cote, Triangle = (base x hauteur) / 2, Cercle = pi x rayon2 (pi = 3,14). Ex : Cercle rayon 5 = 3,14 x 25 = 78,5 cm2.",
    "perimetre": "PERIMETRE : Carre = 4 x cote, Rectangle = 2 x (L+l), Cercle = 2 x pi x rayon, Triangle = somme des 3 cotes.",
    "volume": "VOLUME : Cube = cote3, Pave = L x l x h, Cylindre = pi x r2 x h. Ex : Boite 2x3x4 = 24 cm3.",
    "angle": "ANGLES : Droit = 90 degres, Plat = 180 degres, Plein = 360 degres. Triangle = 180 degres au total.",
    "triangle": "TRIANGLE : 3 cotes, 3 angles, somme = 180 degres. Types : Equilateral (3 cotes egaux), Isocele (2 cotes egaux), Rectangle (1 angle droit), Scalene (3 cotes differents). Aire = (base x hauteur) / 2.",
    "cercle": "CERCLE : Centre, rayon, diametre = 2 x rayon. Perimetre = 2 x pi x rayon. Aire = pi x rayon2. Pi = 3,14.",
    "fraction": "FRACTION : 1/2 = la moitie, 1/4 = le quart. Pour additionner : meme denominateur. 1/2 + 1/4 = 2/4 + 1/4 = 3/4.",
    "pourcentage": "POURCENTAGE : Pourcentage = pour 100. Formule : (partie / total) x 100. Ex : 20% de 50 = 10. Ex : Tu as 15/20 : (15/20) x 100 = 75%.",
    "equation": "EQUATION : 2x + 3 = 7. Tu enleves 3 : 2x = 4. Tu divises par 2 : x = 2. Verif : 2x2+3 = 7, ca marche !",
    "racine carree": "RACINE CARREE : Racine de 9 = 3 car 3x3 = 9. Racine de 16 = 4. Racine de 25 = 5. Racine de 100 = 10.",
    "division": "DIVISION : Division = partage. Ex : 12 / 3 = 4. 12 = dividende, 3 = diviseur, 4 = quotient. Reste : 13 / 4 = 3 reste 1.",
    "cod": "COD : Complement d'Objet Direct. Il repond a Qui ? ou Quoi ? apres le verbe, sans preposition. Ex : Je mange une pomme. Je mange quoi ? Une pomme = COD.",
    "coi": "COI : Complement d'Objet Indirect. Il repond a A qui ? A quoi ? Avec preposition a / de. Ex : Je parle a Lenny. Je parle a qui ? A Lenny = COI.",
    "sujet": "SUJET : Le sujet, c'est qui fait l'action. Il repond a Qui est-ce qui ? Ex : Lenny mange. Qui mange ? Lenny = sujet.",
    "adjectif": "ADJECTIF : Il decrit un nom, il s'accorde en genre et nombre. Ex : grand garcon / grande fille / grands garcons / grandes filles.",
    "pluriel": "PLURIEL : En general +s : chat -> chats. En -eau : bateau -> bateaux. En -al : cheval -> chevaux.",
    "verbe": "VERBE : C'est l'action dans la phrase. Ex : Je mange, Tu cours, Il dort. Il se conjugue avec le temps : present, passe, futur.",
    "pronom": "PRONOM : Il remplace un nom. Ex : Lenny mange. Il mange. Je, tu, il, elle, nous, vous, ils, elles, le, la, les, lui, leur...",
    "synonyme": "SYNONYME : Mot qui veut dire la meme chose. Ex : content = heureux, rapide = vite, grand = immense.",
    "antonyme": "ANTONYME : Mot qui veut dire le contraire. Ex : grand = petit, chaud = froid, content = triste.",
    "homonyme": "HOMONYME : Mots qui se prononcent pareil mais s'ecrivent differemment. Ex : a / a, et / est, son / sont, vert / verre / vers.",
    "famille de mots": "FAMILLE DE MOTS : Mots qui ont la meme racine. Ex : fleur, fleuri, fleuriste, floraison. Terre, terrain, terrien, terrestre.",
    "der": "DER DIE DAS : der = masculin (der Mann), die = feminin (die Frau), das = neutre (das Kind). Pluriel = die (die Kinder).",
    "accusatif": "ACCUSATIF : C'est le cas du COD. der devient den, die reste die, das reste das. Ex : Ich sehe den Hund (Je vois le chien).",
    "datif": "DATIF : C'est le cas du COI (a qui ?). der devient dem, die devient der, das devient dem. Ex : Ich gebe dem Mann ein Buch.",
    "nominatif": "NOMINATIF : C'est le cas du sujet. der, die, das. Ex : Der Mann ist gut (L'homme est gentil).",
    "present simple": "PRESENT SIMPLE : Pour les habitudes. I play, You play, He plays (avec -s !), We play. Ex : He plays football every day.",
    "present perfect": "PRESENT PERFECT : have + participe. I have eaten = J'ai mange. I have played = J'ai joue.",
    "present continu": "PRESENT CONTINU : be + -ing. I am playing = Je suis en train de jouer.",
    "preterit": "PRETERIT - ANGLAIS : Pour le passe termine. Verbes reguliers +ed : I played. Verbes irreguliers : I went, I saw, I ate.",
    "comparatif": "COMPARATIF - ANGLAIS : Plus... que = -er + than. Ex : bigger than = plus grand que. More + adjectif long : more beautiful than = plus beau que.",
    "ser et estar": "SER et ESTAR : SER = etre permanent (Soy de Suiza). ESTAR = etre temporaire / lieu (Estoy en casa, Estoy cansado).",
    "el / la": "EL / LA : el = masculin, la = feminin, los / las = pluriel. Ex : el perro, la casa, los perros, las casas.",
    "pluriel en espagnol": "PLURIEL EN ESPAGNOL : +s : casa -> casas. -z : lapiz -> lapices.",
    "il / lo / la": "IL / LO / LA - ITALIEN : il = masculin, lo = masculin devant s+consonne / z, la = feminin. Ex : il libro, lo studente, la casa.",
    "pluriel en italien": "PLURIEL EN ITALIEN : -o devient -i : libro -> libri. -a devient -e : casa -> case. -e devient -i : cane -> cani.",
    "photosynthese": "PHOTOSYNTHESE : Soleil + Eau + CO2 = Oxygene + Sucre. Les feuilles ont de la chlorophylle (vert) qui capte la lumiere.",
    "gravite": "GRAVITE : La gravite nous attire vers la Terre. C'est Newton qui l'a decouverte en voyant une pomme tomber. Sur la Lune, tu es 6x plus leger.",
    "coeur": "COEUR : Pompe le sang dans tout le corps. 100 000 battements par jour, 7 000 litres de sang par jour !",
    "volcan": "VOLCAN : Ouverture dans la Terre par ou sort du magma. Quand le magma sort, ca devient de la lave. Le plus actif d'Europe = Etna.",
    "foudre": "FOUDRE : Decharge electrique entre un nuage et le sol. Temperature : 30 000 degres, 5x plus chaud que le Soleil ! Regle : si tu entends le tonnerre, rentre.",
    "saison": "SAISONS : Ce n'est pas la distance au Soleil, c'est l'inclinaison de la Terre (23,5 degres). En ete, l'hemisphere Nord est penche vers le Soleil.",
    "cerveau": "CERVEAU : 1,4 kg, 86 milliards de neurones. Il controle tout : pensees, mouvements, emotions. Il consomme 20% de ton energie.",
    "cellule": "CELLULES : La cellule, c'est la plus petite brique du vivant. Tu en as 37 000 milliards ! Chaque cellule a un noyau avec ton ADN.",
    "masse volumique": "MASSE VOLUMIQUE : Formule : masse volumique = masse / volume. Rho = m / V. Ex : 100g / 100 cm3 = 1 g/cm3 = eau. Huile = 0,9 flotte, Fer = 7,8 coule. Regle : Si plus petit que 1 ca flotte, si plus grand que 1 ca coule.",
    "atome": "ATOME : La plus petite brique de la matiere. Noyau avec protons (+) et neutrons (0), et autour des electrons (-) qui tournent.",
    "oxygene": "OXYGENE : O2. On respire O2, on rejette CO2. Sans oxygene, on meurt en 3 minutes. 21% de l'air = oxygene.",
    "chimie": "CHIMIE : Etude de la matiere. Atome = brique, Molecule = plusieurs atomes. H2O = eau. CO2 = dioxyde de carbone.",
    "electricite": "ELECTRICITE : Tension en Volts (V), Intensite en Amperes (A), Puissance en Watts (W). Formule : P = U x I. En serie : si une lampe grille, tout s'eteint. En parallele : les autres restent allumees.",
    "vitesse": "VITESSE : Vitesse = distance / temps. v = d / t. Ex : 100m en 10 sec = 10 m/s = 36 km/h. Pour m/s vers km/h : x 3,6.",
    "energie": "ENERGIE : Cinetique (mouvement), potentielle (hauteur), thermique (chaleur), electrique, chimique, solaire, eolienne. On ne cree pas d'energie, on la transforme.",
    "force": "FORCE : En Newtons (N). Poids = masse x gravite. Ex : 50 kg sur Terre = 500 N.",
    "lumiere": "LUMIERE : Elle va a 300 000 km / seconde ! C'est la vitesse la plus rapide de l'univers. Soleil -> Terre = 8 minutes.",
    "adn": "ADN : Ton code genetique, dans toutes tes cellules. Il dit si tu as les yeux bleus, bruns, si tu es grand, petit... Tu as 50% de l'ADN de ton pere, 50% de ta mere.",
    "trou noir": "TROU NOIR : Objet tellement lourd et petit que meme la lumiere ne peut pas en sortir. Au centre de notre galaxie, un trou noir de 4 millions de fois la masse du Soleil.",
    "big bang": "BIG BANG : Debut de l'univers il y a 13,8 milliards d'annees. Tout etait concentre en un point minuscule, puis ca a explose et ca s'etend encore aujourd'hui.",
    "mars": "MARS : Planete rouge, a cause du fer oxyde (rouille). Un jour sur Mars = 24h37. Une annee = 687 jours. Temperature : -60 degres. Robots : Perseverance, 【entity-Curiosity¦canonical_name=Curiosity】.",
    "iss": "ISS : Station Spatiale Internationale. Elle tourne autour de la Terre a 400 km, a 28 000 km/h (tour de Terre en 90 min). 16 levers de soleil par jour !",
    "systeme solaire": "SYSTEME SOLAIRE : 8 planetes autour du Soleil : Mercure, Venus, Terre, Mars, Jupiter, Saturne, Uranus, Neptune. Astuce : Me Voici, Tout Mouille, J'ai Suivi Un Nuage.",
    "soleil": "SOLEIL : C'est une etoile, pas une planete. Temperature au centre : 15 millions de degres, a la surface : 5500 degres. Il va mourir dans 5 milliards d'annees.",
    "galaxie": "GALAXIE : Groupe de milliards d'etoiles. Notre galaxie = Voie Lactee, 200 milliards d'etoiles. La voisine = Andromede, 2,5 millions d'annees-lumiere.",
    "lune": "LUNE : Notre satellite. Distance : 384 000 km. Elle tourne autour de la Terre en 27 jours. Premier homme dessus : Neil Armstrong, 1969. Elle fait les marees.",
    "boucle": "BOUCLE : Pour repeter sans recopier. Ex : for i in range(1,6): print(i) -> affiche 1,2,3,4,5.",
    "variable": "VARIABLE : Boite qui stocke une valeur. Ex : age = 13, prenom = Lenny, note = 15. Tu peux la changer : age = 14.",
    "condition": "CONDITION : Si... sinon... Ex : if age >= 18: print('Majeur') else: print('Mineur').",
    "fonction": "FONCTION : Bloc de code qu'on peut reutiliser. Ex : def dire_bonjour(): print('Bonjour'). Tu l'appelles avec dire_bonjour().",
    "liste": "LISTE : Plusieurs valeurs dans une boite. Ex : notes = [12, 15, 18]. notes[0] = 12. Tu peux ajouter : notes.append(20).",
    "algorithme": "ALGORITHME : Suite d'etapes pour resoudre un probleme. Ex : Recette de cuisine = algorithme. Pour faire un gateau : 1. Melanger, 2. Mettre au four, 3. Attendre, 4. Manger !",
    "python": "PYTHON : Langage facile, celui de ton agent. Cree en 1991 par Guido van Rossum. Utilise pour l'IA, les sites web, les jeux, les robots. Ex : print('Bonjour').",
    "html": "HTML : Squelette d'un site. h1 = Titre, p = Texte, img = image, a = lien. Sans HTML, pas de site.",
    "css": "CSS : Style d'un site : couleurs, tailles, positions. Ex : body { background-color: black; color: white; }. Sans CSS, ton site est tout blanc et moche.",
    "javascript": "JAVASCRIPT : Langage pour rendre un site interactif : boutons, animations, jeux. HTML = squelette, CSS = style, JS = cerveau.",
    "ia": "IA - INTELLIGENCE ARTIFICIELLE : Programme qui apprend avec des donnees. Ex : ChatGPT, ton agent, les voitures autonomes, les filtres TikTok. Elle ne pense pas comme nous, elle predit le mot le plus probable.",
    "joconde": "JOCONDE : Peinture de Leonard de Vinci, 1503-1506. Au Louvre a Paris. La plus celebre au monde. 7M de personnes la voient chaque annee. Elle vaut 860M euros !",
    "van gogh": "VAN GOGH : Peintre neerlandais, 1853-1890. Il a peint 900 tableaux en 10 ans. Son tableau le plus celebre : La Nuit etoilee, Les Tournesols.",
    "picasso": "PICASSO : Peintre espagnol, 1881-1973. Il a invente le cubisme. Il a peint Guernica (1937) contre la guerre. Il a fait 50 000 oeuvres !",
    "rap": "RAP : Musique nee dans le Bronx a New York dans les annees 70. On parle / on chante vite sur un rythme. En France, c'est la musique la plus ecoutee. Artistes : Werenoi, Ninho, Jul, PNL, Booba...",
    "piano": "PIANO : Instrument avec 88 touches (52 blanches, 36 noires). Invente en 1700 par Bartolomeo Cristofori en Italie. Les plus grands : Mozart, Beethoven, Chopin.",
    "guitare": "GUITARE : Instrument avec 6 cordes. Il y a la classique, l'acoustique, l'electrique. Accords de base : Do, Sol, La mineur, Mi mineur. Avec 4 accords, tu peux jouer 100 chansons !",
    "note": "NOTE DE MUSIQUE : 7 notes : Do, Re, Mi, Fa, Sol, La, Si. Puis ca recommence : Do... Une octave = 8 notes.",
    "foot": "FOOT : Sport le plus joue au monde, 3,5 milliards de fans ! 2 equipes de 11, 90 minutes, 1 ballon. But = mettre le ballon dans le but adverse. Coupe du Monde tous les 4 ans. Meilleurs : 【entity-Messi¦canonical_name=Messi】, 【entity-Ronaldo¦canonical_name=Ronaldo】, 【entity-Mbappe¦canonical_name=Mbappe】.",
    "basket": "BASKET : 5 vs 5, panier a 3,05m, match 4x12 min en 【entity-NBA¦canonical_name=NBA】. Michael Jordan = GOAT (6 titres 【entity-NBA¦canonical_name=NBA】). 【entity-LeBron James¦canonical_name=LeBron James】 = 40 000 points, record. En France : 【entity-Victor Wembanyama¦canonical_name=Victor Wembanyama】, 2m24, joue aux 【entity-Spurs¦canonical_name=Spurs】 !",
    "tennis": "TENNIS : 【entity-Federer¦canonical_name=Roger Federer】 (20 Grands Chelems, Suisse !), Nadal (22, roi de Roland-Garros, 14 fois !), Djokovic (24, record). Grand Chelem = 4 tournois : Open d'Australie, Roland-Garros, Wimbledon, US Open.",
    "formule 1": "FORMULE 1 : 350 km/h ! 20 pilotes, 10 equipes. Verstappen (Red Bull) a gagne 2021, 2022, 2023, 2024. Hamilton (Ferrari) = 7 titres, record avec Schumacher. Grand Prix de Monaco = le plus prestigieux.",
    "jo": "JO - JEUX OLYMPIQUES : Tous les 4 ans. Antiquite : en Grece, -776. Modernes : depuis 1896. 2024 = Paris, 2028 = Los Angeles. Devise : Plus vite, plus haut, plus fort.",
    "manger sain": "MANGER SAIN : 5 fruits et legumes par jour, boire 1,5L d'eau, moins de sucre, moins de fast-food. Ton cerveau a besoin de bon carburant : poisson, fruits, legumes, noix.",
    "sommeil": "SOMMEIL : A 13 ans, il faut 9-10h de sommeil ! Pendant que tu dors, ton cerveau range ce que tu as appris, ton corps grandit. Pas d'ecran 1h avant de dormir.",
    "【entity-messi¦canonical_name=Messi】": "【entity-MESSI¦canonical_name=Messi】 : Lionel 【entity-Messi¦canonical_name=Messi】, ne en 1987 a Rosario, Argentine. 8 Ballons d'Or (record), 91 buts en une annee (2012, record). Barca (672 buts), PSG, Miami. Coupe du Monde 2022 avec l'Argentine. Considere comme le meilleur de tous les temps.",
    "【entity-ronaldo¦canonical_name=Ronaldo】": "【entity-CRISTIANO RONALDO¦canonical_name=Cristiano Ronaldo】 : Ne en 1985 a Madere, Portugal. 5 Ballons d'Or, meilleur buteur de l'histoire en selection (130 buts), meilleur buteur de la Ligue des Champions (140 buts), 900 buts en carriere. 600M de followers sur Instagram.",
    "【entity-mbappe¦canonical_name=Mbappe】": "【entity-MBAPPE¦canonical_name=Mbappe】 : Kylian 【entity-Mbappe¦canonical_name=Mbappe】, ne en 1998 a Bondy, France. Champion du Monde 2018 a 19 ans, meilleur buteur de la Coupe du Monde 2022 (8 buts, triple en finale). Vitesse : 36 km/h, le plus rapide du foot. 【entity-Real Madrid¦canonical_name=Real Madrid】 depuis 2024.",
    "ballon d'or": "BALLON D'OR : Trophee du meilleur joueur du monde chaque annee, vote par des journalistes. Cree en 1956. 【entity-Messi¦canonical_name=Messi】 en a 8 (record), 【entity-Ronaldo¦canonical_name=Ronaldo】 5. En 2024, c'est Rodri qui a gagne.",
    "coupe du monde": "COUPE DU MONDE : Tous les 4 ans, 48 equipes en 2026 (USA / Canada / Mexique). 2022 = Argentine gagne contre France (3-3, tirs au but). 2018 = France gagne. Le Bresil a gagne 5 fois, record.",
    "ligue des champions": "LIGUE DES CHAMPIONS : Meilleure competition de clubs en Europe. 【entity-Real Madrid¦canonical_name=Real Madrid】 a gagne 15 fois, record ! Milan 7, Bayern 6, Liverpool 6, Barcelone 5.",
    "minecraft": "MINECRAFT : Cree par Notch en 2011, rachete par Microsoft pour 2,5 milliards $. Jeu le plus vendu au monde : 300M de copies ! Monde infini en cubes, tu mines, tu construis, tu survis. Modes : Survie, Creatif, Aventure. Mobs : Creeper (BOOM), Enderman, Ender Dragon (boss final).",
    "fortnite": "FORTNITE : Cree par Epic Games en 2017. Battle Royale : 100 joueurs sur une ile, le dernier vivant gagne. Modes : Battle Royale, Zero Construction, Lego Fortnite, Festival. Armes : gris, vert, bleu, violet, orange (du moins fort au plus fort).",
    "roblox": "ROBLOX : Plateforme avec des millions de jeux crees par les joueurs. Cree en 2006. Jeux cultes : Brookhaven, Blox Fruits, Pet Simulator, Doors, Murder Mystery 2. 300M de joueurs par mois !",
    "gta": "GTA V : Sorti en 2013, 190M de copies, 2eme jeu le plus vendu (apres Minecraft). Monde ouvert : Los Santos (Los Angeles). 3 personnages : Michael, Franklin, Trevor. GTA VI sort en 2026, a Vice City (Miami), avec Lucia et Jason.",
    "brawl stars": "BRAWL STARS : Jeu mobile de Supercell (Clash of Clans). 3v3, tu choisis un Brawler (Shelly, Colt, Spike, Leon...). Modes : Gem Grab, Showdown (battle royale), Brawl Ball (foot). 500M de telechargements !",
    "mario": "MARIO : Plombier Nintendo, sauve Peach. Cree en 1981 par Shigeru Miyamoto. Jeux : Super Mario Bros, Mario Kart, Mario Party, Super Mario Odyssey. Frere : Luigi. Ennemi : Bowser. 800M de jeux vendus !",
    "pokemon": "POKEMON : Attrape-les tous ! Cree en 1996 au Japon. 1000+ Pokemons. Pikachu = mascotte. Jeux : Rouge, Or, Diamant, Ecarlate, Violet. Cartes Pokemon = les plus collectionnees au monde.",
    "one piece": "ONE PIECE : Manga le plus vendu au monde (500M de tomes). Luffy veut devenir Roi des Pirates. Il a mange le Fruit du Demon, il est en caoutchouc. Equipage : Zoro, Nami, Usopp, Sanji, Chopper, Robin, Franky, Brook, Jinbe. Auteur : Eiichiro Oda, depuis 1997.",
    "naruto": "NARUTO : Ninja qui veut devenir Hokage. Rasengan, Chidori, Kyubi (demon renard a 9 queues). Auteur : Masashi Kishimoto. Suite : Boruto (son fils).",
    "dragon ball": "DRAGON BALL : Goku, Super Saiyan, Kamehameha ! Auteur : Akira Toriyama. Goku ramasse 7 Dragon Balls pour exaucer un voeu. Transformations : Super Saiyan 1, 2, 3, Blue, Ultra Instinct.",
    "tour eiffel": "TOUR EIFFEL : Paris, 330m, 1889, Gustave Eiffel. 7M de visiteurs par an. Elle grandit de 15 cm en ete ! Au debut, les Parisiens la detestaient !",
    "pyramide": "PYRAMIDES : En Egypte, il y a 4500 ans pour les Pharaons. La plus grande = Kheops, 146m, 2,3 millions de blocs de 2,5 tonnes ! 20 000 ouvriers pendant 20 ans.",
    "titanic": "TITANIC : Paquebot anglais, le plus grand du monde en 1912. Il heurte un iceberg le 14 avril 1912, il coule en 2h40. 1517 morts, 706 survivants. Film 1997, 11 Oscars.",
    "harry potter": "HARRY POTTER : Sorcier avec une cicatrice en eclair, par J.K. Rowling. 7 livres, 8 films, 500M de livres vendus. Maisons : Gryffondor, Serpentard, Poufsouffle, Serdaigle. Personnages : Hermione, Ron, Dumbledore, Hagrid.",
    "millionnaire": "COMMENT DEVENIR MILLIONNAIRE ? : 1. Salarie + investissement : tu mets une partie de ton salaire en bourse (ETF), sur le long terme ca grandit. 2. Entrepreneur : tu crees un business. 3. Createur : YouTube, TikTok. Conseils : Apprends une competence, epargne une partie de ce que tu gagnes, investis tot.",
    "salaire": "SALAIRE : Salaire = argent que tu gagnes chaque mois pour ton travail. En Suisse : salaire moyen autour de 6500 CHF / mois. Brut = avant impots, Net = apres impots.",
    "metier": "METIER - IDEES : Developpeur, Medecin, Avocat, Pilote, Ingenieur, Enseignant, Infirmier, Electricien, Cuisinier, Youtubeur. Le meilleur metier, c'est celui que tu aimes + qui paie bien + qui est utile.",
    "entrepreneur": "ENTREPRENEUR : Quelqu'un qui cree son entreprise. Ex : Elon Musk (Tesla, SpaceX), Jeff Bezos (Amazon), Mark Zuckerberg (Facebook). Qualites : ne pas avoir peur d'echouer, travailler beaucoup, ecouter les clients.",
    "gagner de l argent": "COMMENT GAGNER DE L'ARGENT A 13 ANS EN SUISSE ? : Tu ne peux pas encore facturer seul. Solutions : 1. Petits services : aider voisins (tondre, promener chien, aider ordi). 2. Vendre ce que tu n'utilises plus. 3. Creer un projet (agent IA, site, chaine) et montrer a tes parents, ils peuvent facturer pour toi. 4. Apprendre une competence (code, design, montage).",
    "bourse": "BOURSE : La bourse, c'est acheter une petite partie d'une entreprise (une action). Si l'entreprise gagne, ton action monte. Si elle perd, elle baisse. ETF = panier de beaucoup d'entreprises, moins risque qu'une seule.",
    "plus grand animal": "PLUS GRAND ANIMAL : Baleine bleue ! 30m, 200 tonnes, coeur = 600 kg ! Elle mange du krill, 4 tonnes par jour. Plus grande qu'un dinosaure !",
    "plus rapide": "PLUS RAPIDE : Guepard = 110 km/h sur terre. Faucon pelerin = 390 km/h en pique ! Poisson voilier = 110 km/h dans l'eau. 【entity-Usain Bolt¦canonical_name=Usain Bolt】 = 44 km/h.",
    "chien": "CHIEN : Meilleur ami de l'homme depuis 15 000 ans. 400 races : Labrador (gentil), Berger Allemand (police), Chihuahua (petit), Husky (neige). Il comprend 150 mots.",
    "chat": "CHAT : Il dort 16h par jour ! Il a 32 muscles dans chaque oreille, il peut sauter 6x sa hauteur, il retombe toujours sur ses pattes. Il ronronne quand il est content.",
    "lion": "LION : Roi des animaux. Il vit en Afrique. Le male a une criniere, la femelle chasse. Il dort 20h par jour ! Il rugit si fort qu'on l'entend a 8 km.",
    "dauphin": "DAUPHIN : Animal tres intelligent, il communique avec des sons, il dort avec un oeil ouvert et un demi-cerveau eveille pour respirer. Il peut nager a 60 km/h.",
    "recette facile": "RECETTE FACILE - PATES : 1. Fais bouillir de l'eau salee. 2. Mets les pates 8-10 min. 3. Egoutte. 4. Ajoute sauce tomate + fromage. C'est pret !",
    "gateau au chocolat": "GATEAU AU CHOCOLAT - RECETTE : 200g chocolat, 200g beurre, 4 oeufs, 150g sucre, 100g farine. 1. Fais fondre chocolat + beurre. 2. Melange oeufs + sucre. 3. Ajoute tout + farine. 4. Four 180 degres pendant 25 min. C'est pret !",
    "conseil pour reviser": "CONSEIL POUR REVISER - TOP 5 : 1. Pomodoro : 25 min de travail, 5 min de pause. 2. Relis pas, teste-toi : fais des quiz. 3. Explique a quelqu'un. 4. Dors bien : ton cerveau range ce que tu as appris pendant la nuit. 5. Pas de telephone pendant que tu revises.",
    "2eme guerre": "2EME GUERRE MONDIALE : 1939-1945. Allemagne (Hitler) contre Allies (France, Angleterre, USA, URSS). 60 millions de morts. Fin : 1945, debarquement en Normandie 1944, bombes sur Hiroshima et Nagasaki.",
    "1ere guerre": "1ERE GUERRE MONDIALE : 1914-1918. France, Angleterre contre Allemagne, Autriche. Guerre des tranchees, 18 millions de morts. Fin : Armistice 11 novembre 1918.",
    "revolution": "REVOLUTION FRANCAISE : 1789. Le peuple se revolte contre le roi Louis XVI. Prise de la Bastille 14 juillet 1789. Declaration des Droits de l'Homme. Le roi est decapite en 1793.",
    "rome": "ROME : Empire romain, il y a 2000 ans. Colisee, gladiateurs, Jules Cesar, Auguste. Rome a conquis toute l'Europe, l'Afrique du Nord, le Moyen-Orient. Langue : latin, ancetre du francais, espagnol, italien.",
    "moyen age": "MOYEN AGE : 500-1500. Chateaux forts, chevaliers, rois, paysans, eglise. Guerre de Cent Ans (France vs Angleterre). Peste noire en 1348, 1/3 de l'Europe meurt. Fin : decouverte de l'Amerique en 1492.",
    "egypte": "EGYPTE : Pharaons, pyramides, Nil, hieroglyphes. Pharaons celebres : Toutankhamon, Ramses II, Cleopatre. Momies, dieux : Ra (Soleil), Anubis (mort), Horus (faucon).",
    "napoleon": "NAPOLEON : Empereur francais 1804-1815. Il a conquis presque toute l'Europe. Il a cree le Code Civil (lois). Batailles : Austerlitz (victoire), Waterloo (defaite, 1815). Il meurt a Sainte-Helene en 1821.",
    "dinosaures": "DINOSAURES : Ils ont vecu il y a 230 a 66 millions d'annees. T-Rex (roi, 12m), Diplodocus (30m, le plus long), Triceratops (3 cornes). Ils ont disparu il y a 66M d'annees a cause d'un asteroide.",
    "continents": "CONTINENTS : Il y en a 7 : Afrique, Amerique du Nord, Amerique du Sud, Antarctique, Asie, Europe, Oceanie. Le plus grand = Asie, le plus petit = Oceanie. L'Antarctique = que de la glace, -80 degres !",
    "oceans": "OCEANS : Il y en a 5 : Pacifique (le plus grand), Atlantique, Indien, Arctique, Austral. Le Pacifique = 165M km2, plus grand que toutes les terres ! Fosse des Mariannes = 11 km de profondeur, le point le plus profond.",
}

AVIONS = {
    "f-22": "F-22 RAPTOR (USA) - LE PLUS PERFORMANT EN COMBAT. Mach 2.25 (2400 km/h). Furtif, jamais battu en exercice. 195 exemplaires, jamais vendu a d'autres pays, trop secret !",
    "f-35": "F-35 LIGHTNING II (USA) - LE PLUS MODERNE. Mach 1.6. La Suisse en a achete 36 ! Il voit tout a 360 degres, il partage les infos avec les autres avions.",
    "rafale": "RAFALE (France). Mach 1.8. Polyvalent : air, sol, mer. Il peut decoller d'un porte-avions. Utilise par France, Inde, Grece, Egypte, Qatar...",
    "sr-71": "SR-71 BLACKBIRD. Mach 3.3 = 3500 km/h ! Plus rapide de tous les temps. Aucun missile ne l'a jamais touche. Il volait a 25 000m.",
    "concorde": "CONCORDE : Paris-New York en 3h30. Mach 2. Billet : tres cher. Arrete en 2003.",
    "f-16": "F-16. Mach 2.0. Plus produit : 4600 exemplaires ! Petit, agile, pas cher. Utilise par 25 pays.",
    "f-15": "F-15 EAGLE. Mach 2.5 ! 104 victoires a 0 defaite en combat reel, legende !",
    "a380": "【entity-AIRBUS¦canonical_name=AIRBUS】 A380 : Le plus gros avion de passagers. 2 etages, 850 passagers max ! 73m de long, 80m d'envergure. 【entity-Emirates¦canonical_name=Emirates】 en a le plus.",
    "comment vole": "COMMENT VOLE UN AVION ? : L'aile est courbee en haut, plate en bas. L'air va plus vite au-dessus, donc pression plus faible au-dessus, pression plus forte en dessous. Ca cree une force vers le haut = portance. Pour decoller, il faut aller vite (250 km/h pour un A380).",
}

TRAIN_FACILE = [("C'est quoi 2+2 ?", "4"), ("C'est quoi 5x2 ?", "10"), ("C'est quoi la capitale de la France ?", "paris"), ("C'est quoi 3x3 ?", "9"), ("C'est quoi 10-3 ?", "7")]
TRAIN_MOYEN = [("C'est quoi 7x8 ?", "56"), ("C'est quoi la capitale du Japon ?", "tokyo"), ("C'est quoi 15+25 ?", "40"), ("Qui a gagne la Coupe du Monde 2022 ?", "argentine"), ("C'est quoi la capitale de la Suisse ?", "berne")]
TRAIN_DIFFICILE = [("C'est quoi 12x12 ?", "144"), ("C'est quoi la capitale de l'Australie ?", "canberra"), ("C'est quoi 144 / 12 ?", "12"), ("Combien de Ballons d'Or a Messi ?", "8"), ("En quelle annee a coule le Titanic ?", "1912")]
TRAIN_VERBES = [("Conjugue ETRE au present : je ... ?", "suis"), ("Conjugue AVOIR au present : tu ... ?", "as"), ("Conjugue TO BE : I ... ?", "am"), ("Conjugue SEIN : ich ... ?", "bin"), ("Conjugue ALLER : il ... ?", "va")]
TRAIN_MATHS = [("C'est quoi 7x8 ?", "56"), ("C'est quoi 9x9 ?", "81"), ("C'est quoi 12+15 ?", "27"), ("C'est quoi 100-37 ?", "63")]
TRAIN_FRANCAIS = [("C'est quoi le COD ?", "cod"), ("Conjugue ETRE : je ... ?", "suis"), ("C'est quoi le pluriel de cheval ?", "chevaux")]
TRAIN_CAPITALES = [("C'est quoi la capitale du Japon ?", "tokyo"), ("C'est quoi la capitale de la France ?", "paris"), ("C'est quoi la capitale de la Suisse ?", "berne"), ("C'est quoi la capitale du Bresil ?", "brasilia")]

def toutes_tables():
    txt = "TOUTES LES TABLES DE MULTIPLICATION 1 a 12 :\n\n"
    for n in range(1, 13):
        txt += "Table de " + str(n) + " : " + ", ".join([str(n) + "x" + str(i) + "=" + str(n * i) for i in range(1, 11)]) + "\n\n"
    txt += "ASTUCE : Dis-les a voix haute 3 fois, puis cache et recite. Les plus durs : 7x8=56, 6x7=42, 8x8=64 !"
    return txt

def table_division(n):
    txt = "TABLE DE DIVISION DE " + str(n) + " :\n"
    for i in range(1, 11):
        txt += str(n * i) + " / " + str(n) + " = " + str(i) + "  |  "
    return txt

def calculer(q):
    try:
        txt = q.lower().replace("calcule", "").replace("calcul", "").replace("=", "").replace("?", "").strip()
        txt = txt.replace("x", "*").replace(",", ".")
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in txt) or txt == "":
            return None
        res = eval(txt)
        return "Calcul : " + q + " = " + str(res) + " ! Bravo !"
    except:
        return None

def trouver(q_orig):
    q_low = nettoyer(q_orig)
    q_brut = q_orig.lower().strip()
    if q_low in ["stop", "arrete", "arreter", "stop entrainement"]:
        st.session_state.mode_train = False
        st.session_state.train_q = None
        return "Ok, entrainement arrete ! Ton score final : " + str(st.session_state.score) + "/" + str(st.session_state.total_quiz) + " ! Meilleur streak : " + str(st.session_state.best_streak) + " ! Bravo !"
    if st.session_state.mode_train and st.session_state.train_q is not None:
        bonne = nettoyer(st.session_state.train_a)
        st.session_state.total_quiz += 1
        if bonne in q_low or q_low in bonne or q_low == bonne:
            st.session_state.score += 1
            st.session_state.streak += 1
            if st.session_state.streak > st.session_state.best_streak:
                st.session_state.best_streak = st.session_state.streak
            rep = "BRAVO ! Bonne reponse ! C'etait bien '" + st.session_state.train_a + "' ! Score : " + str(st.session_state.score) + "/" + str(st.session_state.total_quiz) + " | Streak : " + str(st.session_state.streak)
        else:
            st.session_state.streak = 0
            rep = "Pas tout a fait... La bonne reponse c'etait '" + st.session_state.train_a + "'. C'est pas grave, on apprend ! Score : " + str(st.session_state.score) + "/" + str(st.session_state.total_quiz)
        if st.session_state.niveau == "facile":
            nq, na = random.choice(TRAIN_FACILE)
        elif st.session_state.niveau == "difficile":
            nq, na = random.choice(TRAIN_DIFFICILE)
        elif st.session_state.niveau == "verbes":
            nq, na = random.choice(TRAIN_VERBES)
        elif st.session_state.niveau == "maths":
            nq, na = random.choice(TRAIN_MATHS)
        elif st.session_state.niveau == "francais":
            nq, na = random.choice(TRAIN_FRANCAIS)
        elif st.session_state.niveau == "capitales":
            nq, na = random.choice(TRAIN_CAPITALES)
        else:
            nq, na = random.choice(TRAIN_MOYEN)
        st.session_state.train_q = nq
        st.session_state.train_a = na
        return rep + "\n\nQuestion suivante (" + st.session_state.niveau + ") : " + nq
    if "entrainement facile" in q_low:
        st.session_state.mode_train = True
        st.session_state.niveau = "facile"
        st.session_state.train_matiere = ""
        nq, na = random.choice(TRAIN_FACILE)
        st.session_state.train_q = nq
        st.session_state.train_a = na
        return "C'EST PARTI - ENTRAINEMENT FACILE ! Ecris 'stop' pour arreter.\n\nPremiere question : " + nq
    if "entrainement difficile" in q_low:
        st.session_state.mode_train = True
        st.session_state.niveau = "difficile"
        st.session_state.train_matiere = ""
        nq, na = random.choice(TRAIN_DIFFICILE)
        st.session_state.train_q = nq
        st.session_state.train_a = na
        return "C'EST PARTI - ENTRAINEMENT DIFFICILE ! Pour les champions !\n\nPremiere question : " + nq
    if "entrainement verbes" in q_low or "quiz verbes" in q_low:
        st.session_state.mode_train = True
        st.session_state.niveau = "verbes"
        st.session_state.train_matiere = "Verbes"
        nq, na = random.choice(TRAIN_VERBES)
        st.session_state.train_q = nq
        st.session_state.train_a = na
        return "ENTRAINEMENT VERBES ! Conjugue ! Ecris 'stop' pour arreter.\n\nPremiere question : " + nq
    if "quiz maths" in q_low:
        st.session_state.mode_train = True
        st.session_state.niveau = "maths"
        st.session_state.train_matiere = "Maths"
        nq, na = random.choice(TRAIN_MATHS)
        st.session_state.train_q = nq
        st.session_state.train_a = na
        return "QUIZ MATHS ! Ecris 'stop' pour arreter.\n\nPremiere question : " + nq
    if "quiz francais" in q_low:
        st.session_state.mode_train = True
        st.session_state.niveau = "francais"
        st.session_state.train_matiere = "Francais"
        nq, na = random.choice(TRAIN_FRANCAIS)
        st.session_state.train_q = nq
        st.session_state.train_a = na
        return "QUIZ FRANCAIS ! Ecris 'stop' pour arreter.\n\nPremiere question : " + nq
    if "quiz capitales" in q_low or "quiz capital" in q_low:
        st.session_state.mode_train = True
        st.session_state.niveau = "capitales"
        st.session_state.train_matiere = "Capitales"
        nq, na = random.choice(TRAIN_CAPITALES)
        st.session_state.train_q = nq
        st.session_state.train_a = na
        return "QUIZ CAPITALES ! Ecris 'stop' pour arreter.\n\nPremiere question : " + nq
    if "quiz" in q_low:
        st.session_state.mode_train = True
        st.session_state.niveau = "moyen"
        st.session_state.train_matiere = ""
        nq, na = random.choice(TRAIN_MOYEN)
        st.session_state.train_q = nq
        st.session_state.train_a = na
        return "C'EST PARTI POUR L'ENTRAINEMENT ! Ecris 'stop' pour arreter.\n\nPremiere question : " + nq
    if "entraine" in q_low or "entrainement" in q_low:
        st.session_state.mode_train = True
        st.session_state.niveau = "moyen"
        st.session_state.train_matiere = ""
        nq, na = random.choice(TRAIN_MOYEN)
        st.session_state.train_q = nq
        st.session_state.train_a = na
        return "C'EST PARTI POUR L'ENTRAINEMENT MOYEN ! Ecris 'stop' pour arreter. Essaie aussi : Entrainement facile / difficile / verbes / Quiz Maths / Quiz Francais / Quiz Capitales.\n\nPremiere question : " + nq
    if "mon score" in q_low or q_low == "score":
        return "Ton score : " + str(st.session_state.score) + " / " + str(st.session_state.total_quiz) + " ! Streak : " + str(st.session_state.streak) + " | Best : " + str(st.session_state.best_streak) + " ! Ecris 'Entraine moi' pour continuer !"
    if q_brut.startswith("apprends") or q_brut.startswith("apprend") or "retient que" in q_brut:
        try:
            texte = q_brut.replace("apprends :", "").replace("apprends", "").replace("apprend :", "").replace("apprend", "").replace("retient que", "").strip()
            if "=" in texte:
                cle, val = texte.split("=", 1)
                cle = nettoyer(cle)
                val = val.strip()
                st.session_state.learned[cle] = val
                return "MERCI ! J'ai appris ! Maintenant je sais que '" + cle + "' = '" + val + "' ! J'ai appris " + str(len(st.session_state.learned)) + " choses !"
            else:
                st.session_state.learned[nettoyer(texte)] = texte
                return "Merci ! J'ai retenu : '" + texte + "' !"
        except:
            return "Pour m'apprendre, ecris : Apprends : c'est quoi le foot = le foot c'est un sport avec un ballon"
    if "montre ce que tu as appris" in q_low or "ce que tu as appris" in q_low:
        if len(st.session_state.learned) == 0:
            return "Je n'ai encore rien appris... Apprends-moi : Apprends : c'est quoi le foot = ..."
        txt = "CE QUE TU M'AS APPRIS (" + str(len(st.session_state.learned)) + ") :\n\n"
        for k, v in st.session_state.learned.items():
            txt += "- " + k + " = " + v + "\n"
        return txt
    for cle, val in st.session_state.learned.items():
        if cle in q_low or q_low in cle:
            return "Ce que TU m'as appris : " + val + " (merci !)"
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
    if "blague" in q_low or "fait moi rire" in q_low or "fais moi rire" in q_low:
        return random.choice(BLAGUES)
    if "motive" in q_low or "motivation" in q_low:
        return random.choice(MOTIVATIONS)
    if "conseil" in q_low and "revis" in q_low:
        return TOUT["conseil pour reviser"]
    if "devinette" in q_low:
        return BASES["devinette"]
    if "heure" in q_low:
        return BASES["quelle heure"]
    if "date" in q_low:
        return BASES["quelle date"]
    if "traduis" in q_low or "traduction" in q_low or "en anglais" in q_low or "en allemand" in q_low or "en espagnol" in q_low or "en italien" in q_low:
        for cle, rep in TRADUCTIONS.items():
            if nettoyer(cle) in q_low:
                return rep
        return "Je peux traduire : bonjour, merci, au revoir, ecole, chat, chien, maison, pomme, eau en anglais / allemand / espagnol / italien. Essaie : Traduis bonjour en anglais"
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
            res = ", ".join([str(n) + "x" + str(i) + "=" + str(n * i) for i in range(1, 11)])
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
    for cle, rep in VERBES.items():
        if nettoyer(cle) == q or nettoyer(cle) in q:
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
    return "Hmm, je ne connais pas encore : '" + q_orig + "'...\n\nMais tu peux M'APPRENDRE ! Ecris :\n\nApprends : " + q_orig + " = ta reponse ici\n\nEssaie :\n- Francais -> Verbes -> Conjugue ETRE\n- Maths -> Geometrie -> C'est quoi Pythagore ?\n- C'est qui Werenoi ?\n- Entraine moi\n- Quiz Maths / Quiz Francais / Quiz Capitales"

if st.session_state.auto_q:
    q_auto = st.session_state.auto_q
    st.session_state.auto_q = ""
    r_auto = trouver(q_auto)
    st.session_state.messages.append({"role": "assistant", "content": r_auto})
    with st.chat_message("assistant"):
        st.write(r_auto)

if question := st.chat_input("Pose ta question, ou choisis Matiere -> Genre -> Question en haut !"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        r = trouver(question)
        st.write(r)
    st.session_state.messages.append({"role": "assistant", "content": r})
