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
    st.session_state.messages = [{"role": "assistant", "content": "Salut ! Bienvenue ! Clique sur 🎯 MODE ENTRAINEMENT en haut pour que je te pose des questions ! Ou choisis Matiere -> Genre -> Question. Ex : Francais -> Verbes -> Conjugue ETRE."}]
if "auto_q" not in st.session_state:
    st.session_state.auto_q = ""

MATIERES_GENRES = {
    "📐 Maths": {
        "📐 Geometrie": ["C'est quoi le theoreme de Pythagore ?", "C'est quoi Thales ?", "C'est quoi l'aire ?", "C'est quoi le perimetre ?", "C'est quoi le volume ?", "C'est quoi un angle ?", "C'est quoi un triangle ?", "C'est quoi un cercle ?"],
        "🧮 Calcul": ["Table de 7", "Toutes les tables de multiplication", "Table de division de 8", "C'est quoi la moyenne ?", "Calcule 12+8", "Calcule 15x7", "C'est quoi la division ?"],
        "🍕 Fractions": ["C'est quoi une fraction ?", "C'est quoi le pourcentage ?", "C'est quoi une equation ?", "C'est quoi la racine carree ?"],
    },
    "🇫🇷 Français": {
        "📖 Grammaire": ["C'est quoi le COD ?", "C'est quoi le COI ?", "C'est quoi le sujet ?", "C'est quoi un adjectif ?", "C'est quoi le pluriel ?", "C'est quoi le verbe ?"],
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
        "📖 Grammaire": ["C'est quoi le present simple ?", "C'est quoi le present perfect ?", "C'est quoi le present continu ?", "C'est quoi le preterit ?"],
        "✍️ Verbes les plus connus": ["Conjugue TO BE", "Conjugue TO HAVE", "Conjugue TO GO", "Conjugue TO DO", "Conjugue TO SAY", "Conjugue TO SEE", "Conjugue TO COME", "Conjugue TO GET", "Conjugue TO MAKE", "Conjugue TO TAKE", "Conjugue TO GIVE", "Conjugue TO KNOW", "Conjugue TO THINK", "Conjugue TO SPEAK", "Conjugue TO EAT", "Conjugue TO DRINK", "Conjugue TO PLAY", "Conjugue TO LIVE", "Conjugue TO LOVE", "Conjugue TO WANT"],
        "🌍 Vocabulaire": ["Traduis bonjour en anglais", "Traduis merci en anglais", "Traduis ecole en anglais", "Traduis chien en anglais"],
    },
    "🇪🇸 Espagnol": {
        "📖 Grammaire": ["C'est quoi ser et estar ?", "C'est quoi el / la / los / las ?", "C'est quoi le pluriel en espagnol ?"],
        "✍️ Verbes les plus connus": ["Conjugue SER", "Conjugue ESTAR", "Conjugue TENER", "Conjugue IR", "Conjugue HACER", "Conjugue DECIR", "Conjugue PODER", "Conjugue QUERER", "Conjugue SABER", "Conjugue VENIR", "Conjugue VER", "Conjugue HABLAR", "Conjugue COMER", "Conjugue VIVIR", "Conjugue JUGAR"],
        "🌍 Vocabulaire": ["Traduis bonjour en espagnol", "Traduis merci en espagnol"],
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
        "🧬 Biologie": ["C'est quoi la photosynthese ?", "C'est quoi le coeur ?", "C'est quoi l'ADN ?", "C'est quoi le cerveau ?"],
        "🌍 Terre / Espace": ["C'est quoi un volcan ?", "C'est quoi les saisons ?", "C'est quoi la foudre ?", "C'est quoi le systeme solaire ?", "C'est quoi un trou noir ?", "C'est quoi Mars ?"],
        "⚡ Physique": ["C'est quoi la gravite ?", "Comment calculer la masse volumique ?", "C'est quoi la vitesse ?", "C'est quoi l'energie ?"],
    },
    "🧪 Chimie / Physique": {
        "⚛️ Chimie": ["C'est quoi un atome ?", "C'est quoi l'oxygene ?", "C'est quoi la chimie ?", "C'est quoi une molecule ?"],
        "⚡ Physique": ["C'est quoi l'electricite ?", "C'est quoi la masse volumique ?", "C'est quoi la vitesse ?"],
    },
    "💻 Code": {
        "🧠 Bases": ["C'est quoi une variable ?", "C'est quoi une boucle ?", "C'est quoi une condition ?", "C'est quoi une fonction ?", "C'est quoi une liste ?"],
        "🌐 Langages": ["C'est quoi Python ?", "C'est quoi HTML ?", "C'est quoi CSS ?", "C'est quoi JavaScript ?", "C'est quoi l'IA ?"],
    },
    "🎨 Arts / Musique": {
        "🎨 Arts": ["C'est quoi la Joconde ?", "C'est quoi Van Gogh ?", "C'est quoi Picasso ?"],
        "🎵 Musique": ["C'est quoi le rap ?", "C'est quoi le piano ?", "C'est quoi la guitare ?"],
    },
    "🏃 Sport / Sante": {
        "⚽ Sports": ["C'est quoi le foot ?", "C'est quoi le basket ?", "C'est quoi le tennis ?", "C'est quoi la Formule 1 ?", "C'est quoi les JO ?"],
        "❤️ Sante": ["C'est quoi le coeur ?", "C'est quoi manger sain ?", "C'est quoi le sommeil ?"],
    },
}

THEMES = {
    "📐 Ecole": ["Voir toutes les matieres"],
    "👋 Bases": ["Bonjour", "Ca va ?", "Merci", "Au revoir", "Tu t'appelles comment ?", "Raconte une blague", "Motive moi", "Conseil pour reviser"],
    "🧮 Calculatrice": ["Calcule 12+8", "Calcule 15x7", "Calcule 144/12", "Calcule 9x9"],
    "🌍 Traductions": ["Traduis bonjour en anglais", "Traduis merci en anglais", "Traduis bonjour en allemand", "Traduis bonjour en espagnol"],
    "🎲 Fun": ["Raconte une blague", "Motive moi", "Conseil pour reviser", "Quelle heure il est ?", "Quelle date on est ?", "Devinette"],
    "🌍 Capitales": ["Capitale du Japon ?", "Capitale du Bresil ?", "Capitale de l'Egypte ?", "Capitale de la Suisse ?", "Capitale de la France ?"],
    "✈️ Avions": ["Quel est l'avion de chasse le plus performant ?", "C'est quoi le F-22 ?", "C'est quoi le 【entity-F-35¦canonical_name=F-35】 ?", "C'est quoi le Rafale ?", "C'est quoi le SR-71 ?", "C'est quoi le Concorde ?", "C'est quoi le A380 ?", "Comment vole un avion ?"],
    "💻 PC": ["C'est quoi le meilleur rapport qualite prix ?", "C'est quoi la meilleure GPU ?", "C'est quoi le meilleur CPU ?", "C'est quoi le meilleur SSD ?", "PC 2000 CHF", "PC 1300 CHF", "PC 900 CHF", "C'est quoi les FPS ?", "C'est quoi le ping ?"],
    "⚽ Foot / Sport": ["C'est qui 【entity-Messi¦canonical_name=Messi】 ?", "C'est qui 【entity-Ronaldo¦canonical_name=RONALDO】 ?", "C'est qui Mbappe ?", "C'est quoi la Coupe du Monde ?", "C'est quoi la Ligue des Champions ?", "C'est quoi le Ballon d'Or ?"],
    "🎮 Jeux Video": ["C'est quoi Minecraft ?", "C'est quoi Fortnite ?", "C'est quoi Roblox ?", "C'est quoi GTA ?", "C'est quoi Brawl Stars ?", "C'est quoi Pokemon ?", "C'est quoi Mario ?", "C'est quoi One Piece ?", "C'est quoi Naruto ?", "C'est quoi Dragon Ball ?"],
    "🚀 Espace": ["C'est quoi un trou noir ?", "C'est quoi le Big Bang ?", "C'est quoi Mars ?", "C'est quoi l'ISS ?", "C'est quoi le Soleil ?"],
    "🎤 Chanteurs": ["C'est qui Werenoi ?", "C'est qui Ninho ?", "C'est qui Jul ?", "C'est qui Gazo ?", "C'est qui Tiakola ?", "C'est qui PNL ?", "C'est qui SDM ?", "C'est qui 【entity-Drake¦canonical_name=DRAKE】 ?", "C'est qui 【entity-Taylor Swift¦canonical_name=TAYLOR SWIFT】 ?", "C'est qui 【entity-Eminem¦canonical_name=EMINEM】 ?", "C'est qui 【entity-Stromae¦canonical_name=STROMAE】 ?", "C'est qui Soprano ?"],
    "💰 Argent / Metiers": ["Comment devenir millionnaire ?", "C'est quoi un salaire ?", "C'est quoi un entrepreneur ?", "Comment gagner de l'argent a 13 ans ?", "C'est quoi la bourse ?"],
    "🐾 Animaux": ["C'est quoi le plus grand animal ?", "C'est quoi le plus rapide ?", "C'est quoi un chien ?", "C'est quoi un chat ?", "C'est quoi un lion ?", "C'est quoi un dauphin ?"],
    "🍔 Cuisine": ["C'est quoi une recette facile ?", "C'est quoi un gateau au chocolat ?", "C'est quoi manger sain ?"],
}

# ===== LISTES ENTRAINEMENT =====
TRAIN_FACILE = [("C'est quoi 2+2 ?", "4"), ("C'est quoi 5x2 ?", "10"), ("C'est quoi la capitale de la France ?", "paris"), ("C'est quoi 3x3 ?", "9"), ("C'est quoi 10-3 ?", "7"), ("Conjugue ETRE : je ... ?", "suis"), ("C'est quoi 4+4 ?", "8")]
TRAIN_MOYEN = [("C'est quoi 7x8 ?", "56"), ("C'est quoi la capitale du Japon ?", "tokyo"), ("C'est quoi 15+25 ?", "40"), ("Qui a gagne la Coupe du Monde 2022 ?", "argentine"), ("C'est quoi la capitale de la Suisse ?", "berne"), ("C'est quoi 9x9 ?", "81")]
TRAIN_DIFFICILE = [("C'est quoi 12x12 ?", "144"), ("C'est quoi la capitale de l'Australie ?", "canberra"), ("C'est quoi 144 / 12 ?", "12"), ("Combien de Ballons d'Or a 【entity-Messi¦canonical_name=Messi】 ?", "8"), ("En quelle annee a coule le Titanic ?", "1912")]
TRAIN_VERBES = [("Conjugue ETRE au present : je ... ?", "suis"), ("Conjugue AVOIR au present : tu ... ?", "as"), ("Conjugue TO BE : I ... ?", "am"), ("Conjugue SEIN : ich ... ?", "bin"), ("Conjugue ALLER : il ... ?", "va"), ("Conjugue FAIRE : je ... ?", "fais")]
TRAIN_MATHS = [("C'est quoi 7x8 ?", "56"), ("C'est quoi 9x9 ?", "81"), ("C'est quoi 12+15 ?", "27"), ("C'est quoi 100-37 ?", "63"), ("C'est quoi 12x12 ?", "144")]
TRAIN_FRANCAIS = [("C'est quoi le COD ?", "cod"), ("Conjugue ETRE : je ... ?", "suis"), ("C'est quoi le pluriel de cheval ?", "chevaux"), ("Conjugue AVOIR : j'... ?", "ai")]
TRAIN_CAPITALES = [("C'est quoi la capitale du Japon ?", "tokyo"), ("C'est quoi la capitale de la France ?", "paris"), ("C'est quoi la capitale de la Suisse ?", "berne"), ("C'est quoi la capitale du Bresil ?", "brasilia")]

def lancer_entrainement(niveau, liste):
    st.session_state.mode_train = True
    st.session_state.niveau = niveau
    st.session_state.train_matiere = niveau
    nq, na = random.choice(liste)
    st.session_state.train_q = nq
    st.session_state.train_a = na
    st.session_state.messages.append({"role": "assistant", "content": "C'EST PARTI - ENTRAINEMENT " + niveau.upper() + " ! Reponds juste en bas, je te corrige ! Pour quitter, clique sur le bouton rouge QUITTER.\n\nPremiere question : " + nq})
    st.rerun()

# ===== SIDEBAR =====
with st.sidebar:
    st.title("Agent IA V5 - ULTIME")
    st.write("Appris : " + str(len(st.session_state.learned)))
    st.write("Score : " + str(st.session_state.score) + " / " + str(st.session_state.total_quiz))
    st.write("Streak : " + str(st.session_state.streak) + " | Best : " + str(st.session_state.best_streak))
    st.divider()
    # BOUTON ENTRAINEMENT DANS SIDEBAR
    if not st.session_state.mode_train:
        if st.button("🎯 MODE ENTRAINEMENT", key="side_train_start", use_container_width=True):
            lancer_entrainement("moyen", TRAIN_MOYEN)
    else:
        st.success("🎯 TU ES EN ENTRAINEMENT")
        st.write("Question : " + str(st.session_state.train_q))
        if st.button("❌ QUITTER ENTRAINEMENT", key="side_train_stop", use_container_width=True):
            st.session_state.mode_train = False
            st.session_state.train_q = None
            st.session_state.messages.append({"role": "assistant", "content": "Entrainement termine ! Score final : " + str(st.session_state.score) + "/" + str(st.session_state.total_quiz) + " | Meilleur streak : " + str(st.session_state.best_streak) + " ! Bravo !"})
            st.rerun()
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

# ===== GROS BOUTON ENTRAINEMENT EN HAUT =====
if not st.session_state.mode_train:
    st.subheader("🎯 MODE ENTRAINEMENT - Je te pose les questions, tu reponds !")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🟢 FACILE", key="train_facile", use_container_width=True):
            lancer_entrainement("facile", TRAIN_FACILE)
    with c2:
        if st.button("🟡 MOYEN", key="train_moyen", use_container_width=True):
            lancer_entrainement("moyen", TRAIN_MOYEN)
    with c3:
        if st.button("🔴 DIFFICILE", key="train_difficile", use_container_width=True):
            lancer_entrainement("difficile", TRAIN_DIFFICILE)
    with c4:
        if st.button("✍️ VERBES", key="train_verbes", use_container_width=True):
            lancer_entrainement("verbes", TRAIN_VERBES)
    c5, c6, c7 = st.columns(3)
    with c5:
        if st.button("🧮 MATHS", key="train_maths", use_container_width=True):
            lancer_entrainement("maths", TRAIN_MATHS)
    with c6:
        if st.button("🇫🇷 FRANCAIS", key="train_francais", use_container_width=True):
            lancer_entrainement("francais", TRAIN_FRANCAIS)
    with c7:
        if st.button("🌍 CAPITALES", key="train_capitales", use_container_width=True):
            lancer_entrainement("capitales", TRAIN_CAPITALES)
else:
    # MODE ENTRAINEMENT ACTIF - PANNEAU + BOUTON QUITTER
    st.success("🎯 TU ES EN MODE ENTRAINEMENT " + st.session_state.niveau.upper() + " - Score : " + str(st.session_state.score) + "/" + str(st.session_state.total_quiz) + " - Streak : " + str(st.session_state.streak))
    st.info("❓ QUESTION ACTUELLE : " + str(st.session_state.train_q) + "\n\nEcris ta reponse en bas dans le chat !")
    col_q1, col_q2 = st.columns([3, 1])
    with col_q1:
        st.write("Tu veux changer de niveau ?")
    with col_q2:
        if st.button("❌ QUITTER ENTRAINEMENT", key="main_train_stop", use_container_width=True):
            st.session_state.mode_train = False
            st.session_state.train_q = None
            st.session_state.messages.append({"role": "assistant", "content": "Entrainement termine ! Score final : " + str(st.session_state.score) + "/" + str(st.session_state.total_quiz) + " | Meilleur streak : " + str(st.session_state.best_streak) + " ! Bravo, tu as bien travaille !"})
            st.rerun()
    # Petits boutons pour changer de niveau sans quitter
    cc1, cc2, cc3, cc4 = st.columns(4)
    with cc1:
        if st.button("Changer -> Facile", key="change_facile"):
            lancer_entrainement("facile", TRAIN_FACILE)
    with cc2:
        if st.button("Changer -> Moyen", key="change_moyen"):
            lancer_entrainement("moyen", TRAIN_MOYEN)
    with cc3:
        if st.button("Changer -> Difficile", key="change_difficile"):
            lancer_entrainement("difficile", TRAIN_DIFFICILE)
    with cc4:
        if st.button("Changer -> Verbes", key="change_verbes"):
            lancer_entrainement("verbes", TRAIN_VERBES)

# ===== MATIERES / THEMES =====
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
    "bonjour": "Bonjour ! Comment tu vas ? Clique sur MODE ENTRAINEMENT en haut pour que je te pose des questions, ou choisis Matiere -> Genre -> Question. Ex : Francais -> Verbes -> Conjugue ETRE.",
    "salut": "Salut ! Ca va ? Clique sur MODE ENTRAINEMENT ou pose-moi ta question !",
    "slt": "Slt ! Ca va ?",
    "yo": "Yo ! Ca va ? Tu veux reviser quoi ?",
    "coucou": "Coucou ! Ca va bien ?",
    "hello": "Hello ! Ca va ? I can help you in English too !",
    "merci": "De rien ! Avec plaisir ! Tu as une autre question ?",
    "mrc": "De rien !",
    "ca va": "Ca va super bien merci ! Et toi, ca va ? Tu revises quelle matiere ?",
    "au revoir": "Au revoir ! A tres vite ! Reviens quand tu veux !",
    "bye": "Bye ! A tres vite !",
    "bonne nuit": "Bonne nuit ! Dors bien ! A demain !",
    "t appelles comment": "Moi je m'appelle Agent IA V5 - ULTIME ! Et toi ?",
    "qui es tu": "Moi je suis Agent IA V5 ULTIME ! Ton assistant cree par Lenny. Je connais 10 matieres, 32 genres, 400+ questions, 85 verbes en 5 langues, 100+ capitales, PC, avions, chanteurs... et J'APPRENDS ce que tu m'apprends !",
    "aide moi": "Oui bien sur ! Clique sur MODE ENTRAINEMENT en haut, ou choisis une matiere !",
    "j ai pas compris": "T'inquiete ! Dis-moi ce que tu n'as pas compris, je vais te reexpliquer plus simplement, avec un autre exemple.",
    "t es trop fort": "Merciii ! Ca me fait trop plaisir !",
    "quelle heure": "Il est " + datetime.datetime.now().strftime("%H:%M") + " !",
    "quelle date": "On est le " + datetime.datetime.now().strftime("%d/%m/%Y") + " !",
    "devinette": "Devinette : Je suis toujours devant toi mais tu ne peux jamais me voir. Qui suis-je ? Reponse : Ton avenir ! Une autre : Qu'est-ce qui monte mais ne descend jamais ? Reponse : Ton age !",
}
BLAGUES = ["Pourquoi les plongeurs plongent-ils toujours en arriere ? Parce que sinon, ils tombent dans le bateau !", "Que dit un zero a un huit ? Belle ceinture !", "Pourquoi les maths sont tristes ? Parce qu'elles ont trop de problemes !", "Pourquoi les poissons n'aiment pas jouer au foot ? Parce qu'ils ont peur des filets !", "Que fait une fraise sur un cheval ? Tagada tagada !"]
MOTIVATIONS = ["Tu peux le faire ! Chaque erreur, c'est une lecon. Ne lache rien !", "N'abandonne jamais ! 10 minutes par jour, tous les jours, et dans 1 mois tu seras trop fort !", "Tu es capable de beaucoup plus que tu crois ! Commence petit, 1 exercice, et ca va venir !"]
TRADUCTIONS = {"bonjour en anglais": "Bonjour en anglais = Hello / Good morning !", "bonjour en allemand": "Bonjour en allemand = Hallo / Guten Tag !", "bonjour en espagnol": "Bonjour en espagnol = Hola / Buenos dias !", "bonjour en italien": "Bonjour en italien = Ciao / Buongiorno !", "merci en anglais": "Merci en anglais = Thank you / Thanks !", "merci en allemand": "Merci en allemand = Danke !", "merci en espagnol": "Merci en espagnol = Gracias !", "merci en italien": "Merci en italien = Grazie !", "ecole en anglais": "Ecole en anglais = School !", "chien en anglais": "Chien en anglais = Dog !", "ecole en allemand": "Ecole en allemand = Schule !", "chien en allemand": "Chien en allemand = Hund !", "ecole en espagnol": "Ecole en espagnol = Escuela !"}
CAPITALES = {"france": "Paris - Tour Eiffel, Louvre.", "suisse": "Berne - Capitale de la Suisse depuis 1848.", "allemagne": "Berlin - Mur de Berlin tombe en 1989.", "italie": "Rome - Colisee, Vatican.", "espagne": "Madrid - 【entity-Real Madrid¦canonical_name=Real Madrid】.", "angleterre": "Londres - Big Ben.", "japon": "Tokyo - Plus grande ville du monde ! Sushi, Manga.", "usa": "Washington D.C. - Maison Blanche.", "canada": "Ottawa - Toronto = plus grande ville.", "chine": "Pekin - Grande Muraille.", "russie": "Moscou - Place Rouge.", "bresil": "Brasilia - Rio = plus connue.", "inde": "New Delhi - Taj Mahal.", "australie": "Canberra - Sydney = plus connue.", "egypte": "Le Caire - Pyramides de Gizeh.", "maroc": "Rabat - Maroc.", "portugal": "Lisbonne - Cristiano Ronaldo !", "belgique": "Bruxelles - Frites, Chocolat !", "pays-bas": "Amsterdam - Canaux, Velos.", "suede": "Stockholm - 【entity-IKEA¦canonical_name=IKEA】, 【entity-ABBA¦canonical_name=ABBA】.", "norvege": "Oslo - Fjords, 【entity-Haaland¦canonical_name=Haaland】 !", "grece": "Athenes - Democratie, 【entity-Jeux Olympiques¦canonical_name=Jeux Olympiques】.", "mexique": "Mexico - Tacos, Azteques.", "argentine": "Buenos Aires - Tango, 【entity-Messi¦canonical_name=Messi】.", "monaco": "Monaco - 2 km2, Grand Prix F1.", "qatar": "Doha - Qatar, Coupe du Monde 2022 !", "nepal": "Katmandou - Nepal, Everest, 8848m !", "jamaique": "Kingston - Jamaique, Bob Marley, 【entity-Usain Bolt¦canonical_name=Usain Bolt】 !"}
PC = {
    "rapport qualite prix": "MEILLEUR RAPPORT PC 2026 : GAGNANT 1300 CHF : RTX 5070 + Ryzen 7 7800X3D + 32 Go + SSD 1 To = 1300 CHF. 1440p Ultra 180 FPS. PETIT BUDGET 900 CHF : RTX 4060 + Ryzen 5 7600 = 900 CHF. GROS BUDGET 2000 CHF : RTX 5070 Ti + 9800X3D = 2000 CHF.",
    "pc 900": "PC 900 CHF : RTX 4060 + Ryzen 5 7600 + 16 Go + SSD 1 To = 900 CHF. Fortnite 144 FPS !",
    "pc 1300": "PC 1300 CHF - MEILLEUR RAPPORT : RTX 5070 + Ryzen 7 7800X3D + 32 Go + SSD 1 To = 1300 CHF. 1440p Ultra 180 FPS !",
    "pc 2000": "PC 2000 CHF : RTX 5070 Ti + Ryzen 7 9800X3D + 32 Go + SSD 2 To = 2000 CHF. 240 FPS, 4K !",
    "meilleure gpu": "MEILLEURE GPU : 1. RTX 5090 - 32 Go, 4K Ultra 200 FPS, 2500 CHF. 2. RTX 5070 - MEILLEUR RAPPORT : 12 Go, 1440p 180 FPS, 600 CHF.",
    "gpu": "GPU = Carte Graphique. RTX 4060 = 144 FPS en 1080p, RTX 5070 = 180 FPS en 1440p, RTX 5090 = 200 FPS en 4K.",
    "meilleur cpu": "MEILLEUR CPU : Ryzen 7 7800X3D - MEILLEUR RAPPORT, 350 CHF. Ryzen 7 9800X3D - ROI GAMING, 450 CHF.",
    "cpu": "CPU = Processeur, cerveau du PC. 【entity-AMD¦canonical_name=AMD】 Ryzen ou 【entity-Intel¦canonical_name=Intel】 Core.",
    "meilleur ssd": "MEILLEUR SSD : 【entity-Samsung¦canonical_name=Samsung】 990 PRO 2 To - Windows en 5 sec, 180 CHF. Meilleur rapport = WD Black 1 To - 70 CHF.",
    "meilleure ram": "MEILLEURE RAM : 32 Go DDR5 6000 MHz. 16 Go = minimum. 64 Go = montage pro.",
    "fps": "FPS = Images par seconde. 30 FPS = ca lag, 60 FPS = fluide, 144 FPS = super fluide, 240 FPS = pro.",
    "ping": "PING = Temps de reponse internet. 10 ms = parfait, 30 ms = tres bien, 100 ms = ca lag, 200 ms = injouable. Pour baisser ton ping : cable Ethernet, fibre.",
}
CHANTEURS = {
    "werenoi": "WERENOI : Vrai nom Jeremy Bana Owona. Ne en 1994 a Melun. Il a explose en 2023 avec Pyramide et Solitaire. Albums : Pyramide, Diamant Noir. Le plus ecoute en France en 2024 et 2025 !",
    "ninho": "NINHO : Vrai nom William Nzobazola. Le rappeur avec le plus de disques d'or et de diamant en France ! Albums : Jefe, NI. Sons : Jefe, Lettre a une femme.",
    "jul": "JUL : Vrai nom Julien Mari. Ne en 1990 a Marseille. Le plus productif : 2 albums par an ! Sons : Tchikita, Bande organisee.",
    "gazo": "GAZO : Roi de la drill en France ! Albums : KMT, Apocalypse. Sons : La Melo avec Tiakola.",
    "tiakola": "TIAKOLA : Membre de 4Keus. Albums : Melo, BDLM. Sons : La Melo, Gasolina.",
    " pnl": " PNL : Duo de freres Ademo et N.O.S. Albums : Dans la legende, Deux freres. Sons : Le monde ou rien, DA.",
    "sdm": "SDM : Repere par Booba. Albums : Ocho, A vie. Son : Bolide allemand avec Ninho.",
    " drake": " DRAKE : Rappeur canadien, le plus streame au monde. Sons : God's Plan, One Dance.",
    " taylor swift": " TAYLOR SWIFT : Chanteuse americaine, la plus ecoutee au monde. 14 Grammy. Son Eras Tour = tournee la plus rentable de l'histoire.",
    " eminem": " EMINEM : Rappeur americain, legende. Sons : Lose Yourself, Rap God, Mockingbird.",
    " stromae": " STROMAE : Chanteur belge. Sons : Alors on danse, Papaoutai, Formidable.",
    "soprano": "SOPRANO : Chanteur de Marseille. Sons : Cosmo, En feu, A la vie, a l'amour.",
}
VERBES = {
    "etre": "ETRE - Francais. PRESENT : je suis, tu es, il est, nous sommes, vous etes, ils sont. PASSE COMPOSE : j'ai ete, tu as ete, il a ete, nous avons ete, vous avez ete, ils ont ete. IMPARFAIT : j'etais, tu etais, il etait, nous etions, vous etiez, ils etaient. FUTUR : je serai, tu seras, il sera, nous serons, vous serez, ils seront.",
    "avoir": "AVOIR - Francais. PRESENT : j'ai, tu as, il a, nous avons, vous avez, ils ont. PASSE COMPOSE : j'ai eu, tu as eu, il a eu, nous avons eu, vous avez eu, ils ont eu. IMPARFAIT : j'avais, tu avais, il avait, nous avions, vous aviez, ils avaient. FUTUR : j'aurai, tu auras, il aura, nous aurons, vous aurez, ils auront.",
    "aller": "ALLER - Francais. PRESENT : je vais, tu vas, il va, nous allons, vous allez, ils vont. PASSE COMPOSE : je suis alle, tu es alle, il est alle, nous sommes alles, vous etes alles, ils sont alles. IMPARFAIT : j'allais, tu allais, il allait, nous allions, vous alliez, ils allaient. FUTUR : j'irai, tu iras, il ira, nous irons, vous irez, ils iront.",
    "faire": "FAIRE - Francais. PRESENT : je fais, tu fais, il fait, nous faisons, vous faites, ils font. PASSE COMPOSE : j'ai fait, tu as fait, il a fait, nous avons fait, vous avez fait, ils ont fait. IMPARFAIT : je faisais, tu faisais, il faisait, nous faisions, vous faisiez, ils faisaient. FUTUR : je ferai, tu feras, il fera, nous ferons, vous ferez, ils feront.",
    "dire": "DIRE - Francais. PRESENT : je dis, tu dis, il dit, nous disons, vous dites, ils disent. PASSE COMPOSE : j'ai dit, tu as dit, il a dit, nous avons dit, vous avez dit, ils ont dit. IMPARFAIT : je disais, tu disais, il disait, nous disions, vous disiez, ils disaient. FUTUR : je dirai, tu diras, il dira, nous dirons, vous direz, ils diront.",
    "pouvoir": "POUVOIR - Francais. PRESENT : je peux, tu peux, il peut, nous pouvons, vous pouvez, ils peuvent. PASSE COMPOSE : j'ai pu, tu as pu, il a pu, nous avons pu, vous avez pu, ils ont pu. IMPARFAIT : je pouvais, tu pouvais, il pouvait, nous pouvions, vous pouviez, ils pouvaient. FUTUR : je pourrai, tu pourras, il pourra, nous pourrons, vous pourrez, ils pourront.",
    "vouloir": "VOULOIR - Francais. PRESENT : je veux, tu veux, il veut, nous voulons, vous voulez, ils veulent. PASSE COMPOSE : j'ai voulu, tu as voulu, il a voulu, nous avons voulu, vous avez voulu, ils ont voulu. IMPARFAIT : je voulais, tu voulais, il voulait, nous voulions, vous vouliez, ils voulaient. FUTUR : je voudrai, tu voudras, il voudra, nous voudrons, vous voudrez, ils voudront.",
    "savoir": "SAVOIR - Francais. PRESENT : je sais, tu sais, il sait, nous savons, vous savez, ils savent. PASSE COMPOSE : j'ai su, tu as su, il a su, nous avons su, vous avez su, ils ont su. IMPARFAIT : je savais, tu savais, il savait, nous savions, vous saviez, ils savaient. FUTUR : je saurai, tu sauras, il saura, nous saurons, vous saurez, ils sauront.",
    "devoir": "DEVOIR - Francais. PRESENT : je dois, tu dois, il doit, nous devons, vous devez, ils doivent. PASSE COMPOSE : j'ai du, tu as du, il a du, nous avons du, vous avez du, ils ont du. IMPARFAIT : je devais, tu devais, il devait, nous devions, vous deviez, ils devaient. FUTUR : je devrai, tu devras, il devra, nous devrons, vous devrez, ils devront.",
    "venir": "VENIR - Francais. PRESENT : je viens, tu viens, il vient, nous venons, vous venez, ils viennent. PASSE COMPOSE : je suis venu, tu es venu, il est venu, nous sommes venus, vous etes venus, ils sont venus. IMPARFAIT : je venais, tu venais, il venait, nous venions, vous veniez, ils venaient. FUTUR : je viendrai, tu viendras, il viendra, nous viendrons, vous viendrez, ils viendront.",
    "voir": "VOIR - Francais. PRESENT : je vois, tu vois, il voit, nous voyons, vous voyez, ils voient. PASSE COMPOSE : j'ai vu, tu as vu, il a vu, nous avons vu, vous avez vu, ils ont vu. IMPARFAIT : je voyais, tu voyais, il voyait, nous voyions, vous voyiez, ils voyaient. FUTUR : je verrai, tu verras, il verra, nous verrons, vous verrez, ils verront.",
    "prendre": "PRENDRE - Francais. PRESENT : je prends, tu prends, il prend, nous prenons, vous prenez, ils prennent. PASSE COMPOSE : j'ai pris, tu as pris, il a pris, nous avons pris, vous avez pris, ils ont pris. IMPARFAIT : je prenais, tu prenais, il prenait, nous prenions, vous preniez, ils prenaient. FUTUR : je prendrai, tu prendras, il prendra, nous prendrons, vous prendrez, ils prendront.",
    "mettre": "METTRE - Francais. PRESENT : je mets, tu mets, il met, nous mettons, vous mettez, ils mettent. PASSE COMPOSE : j'ai mis, tu as mis, il a mis, nous avons mis, vous avez mis, ils ont mis. IMPARFAIT : je mettais, tu mettais, il mettait, nous mettions, vous mettiez, ils mettaient. FUTUR : je mettrai, tu mettras, il mettra, nous mettrons, vous mettrez, ils mettront.",
    "donner": "DONNER - Francais. PRESENT : je donne, tu donnes, il donne, nous donnons, vous donnez, ils donnent. PASSE COMPOSE : j'ai donne, tu as donne, il a donne, nous avons donne, vous avez donne, ils ont donne. IMPARFAIT : je donnais, tu donnais, il donnait, nous donnions, vous donniez, ils donnaient. FUTUR : je donnerai, tu donneras, il donnera, nous donnerons, vous donnerez, ils donneront.",
    "parler": "PARLER - Francais. PRESENT : je parle, tu parles, il parle, nous parlons, vous parlez, ils parlent. PASSE COMPOSE : j'ai parle, tu as parle, il a parle, nous avons parle, vous avez parle, ils ont parle. IMPARFAIT : je parlais, tu parlais, il parlait, nous parlions, vous parliez, ils parlaient. FUTUR : je parlerai, tu parleras, il parlera, nous parlerons, vous parlerez, ils parleront.",
    "manger": "MANGER - Francais. PRESENT : je mange, tu manges, il mange, nous mangeons, vous mangez, ils mangent. PASSE COMPOSE : j'ai mange, tu as mange, il a mange, nous avons mange, vous avez mange, ils ont mange. IMPARFAIT : je mangeais, tu mangeais, il mangeait, nous mangions, vous mangiez, ils mangeaient. FUTUR : je mangerai, tu mangeras, il mangera, nous mangerons, vous mangerez, ils mangeront.",
    "dormir": "DORMIR - Francais. PRESENT : je dors, tu dors, il dort, nous dormons, vous dormez, ils dorment. PASSE COMPOSE : j'ai dormi, tu as dormi, il a dormi, nous avons dormi, vous avez dormi, ils ont dormi. IMPARFAIT : je dormais, tu dormais, il dormait, nous dormions, vous dormiez, ils dormaient. FUTUR : je dormirai, tu dormiras, il dormira, nous dormirons, vous dormirez, ils dormiront.",
    "ecrire": "ECRIRE - Francais. PRESENT : j'ecris, tu ecris, il ecrit, nous ecrivons, vous ecrivez, ils ecrivent. PASSE COMPOSE : j'ai ecrit, tu as ecrit, il a ecrit, nous avons ecrit, vous avez ecrit, ils ont ecrit. IMPARFAIT : j'ecrivais, tu ecrivais, il ecrivait, nous ecrivions, vous ecriviez, ils ecrivaient. FUTUR : j'ecrirai, tu ecriras, il ecrira, nous ecrirons, vous ecrirez, ils ecriront.",
    "lire": "LIRE - Francais. PRESENT : je lis, tu lis, il lit, nous lisons, vous lisez, ils lisent. PASSE COMPOSE : j'ai lu, tu as lu, il a lu, nous avons lu, vous avez lu, ils ont lu. IMPARFAIT : je lisais, tu lisais, il lisait, nous lisions, vous lisiez, ils lisaient. FUTUR : je lirai, tu liras, il lira, nous lirons, vous lirez, ils liront.",
    "partir": "PARTIR - Francais. PRESENT : je pars, tu pars, il part, nous partons, vous partez, ils partent. PASSE COMPOSE : je suis parti, tu es parti, il est parti, nous sommes partis, vous etes partis, ils sont partis. IMPARFAIT : je partais, tu partais, il partait, nous partions, vous partiez, ils partaient. FUTUR : je partirai, tu partiras, il partira, nous partirons, vous partirez, ils partiront.",
    "jouer": "JOUER - Francais. PRESENT : je joue, tu joues, il joue, nous jouons, vous jouez, ils jouent. PASSE COMPOSE : j'ai joue, tu as joue, il a joue, nous avons joue, vous avez joue, ils ont joue. IMPARFAIT : je jouais, tu jouais, il jouait, nous jouions, vous jouiez, ils jouaient. FUTUR : je jouerai, tu joueras, il jouera, nous jouerons, vous jouerez, ils joueront.",
    "apprendre": "APPRENDRE - Francais. PRESENT : j'apprends, tu apprends, il apprend, nous apprenons, vous apprenez, ils apprennent. PASSE COMPOSE : j'ai appris, tu as appris, il a appris, nous avons appris, vous avez appris, ils ont appris. IMPARFAIT : j'apprenais, tu apprenais, il apprenait, nous apprenions, vous appreniez, ils apprenaient. FUTUR : j'apprendrai, tu apprendras, il apprendra, nous apprendrons, vous apprendrez, ils apprendront.",
    "sein": "SEIN = ETRE en Allemand. PRASENS : ich bin, du bist, er ist, wir sind, ihr seid, sie sind. PERFEKT : ich bin gewesen. PRATERITUM : ich war, du warst, er war, wir waren, ihr wart, sie waren. FUTUR : ich werde sein.",
    "haben": "HABEN = AVOIR en Allemand. PRASENS : ich habe, du hast, er hat, wir haben, ihr habt, sie haben. PERFEKT : ich habe gehabt. PRATERITUM : ich hatte. FUTUR : ich werde haben.",
    "gehen": "GEHEN = ALLER en Allemand. PRASENS : ich gehe, du gehst, er geht, wir gehen, ihr geht, sie gehen. PERFEKT : ich bin gegangen. PRATERITUM : ich ging. FUTUR : ich werde gehen.",
    "machen": "MACHEN = FAIRE en Allemand. PRASENS : ich mache, du machst, er macht, wir machen, ihr macht, sie machen. PERFEKT : ich habe gemacht. PRATERITUM : ich machte. FUTUR : ich werde machen.",
    "kommen": "KOMMEN = VENIR en Allemand. PRASENS : ich komme, du kommst, er kommt, wir kommen, ihr kommt, sie kommen. PERFEKT : ich bin gekommen. PRATERITUM : ich kam. FUTUR : ich werde kommen.",
    "sehen": "SEHEN = VOIR en Allemand. PRASENS : ich sehe, du siehst, er sieht, wir sehen, ihr seht, sie sehen. PERFEKT : ich habe gesehen. PRATERITUM : ich sah. FUTUR : ich werde sehen.",
    "sprechen": "SPRECHEN = PARLER en Allemand. PRASENS : ich spreche, du sprichst, er spricht, wir sprechen, ihr sprecht, sie sprechen. PERFEKT : ich habe gesprochen. PRATERITUM : ich sprach. FUTUR : ich werde sprechen.",
    "essen": "ESSEN = MANGER en Allemand. PRASENS : ich esse, du isst, er isst, wir essen, ihr esst, sie essen. PERFEKT : ich habe gegessen. PRATERITUM : ich ass. FUTUR : ich werde essen.",
    "trinken": "TRINKEN = BOIRE en Allemand. PRASENS : ich trinke, du trinkst, er trinkt, wir trinken, ihr trinkt, sie trinken. PERFEKT : ich habe getrunken. PRATERITUM : ich trank. FUTUR : ich werde trinken.",
    "lernen": "LERNEN = APPRENDRE en Allemand. PRASENS : ich lerne, du lernst, er lernt, wir lernen, ihr lernt, sie lernen. PERFEKT : ich habe gelernt. PRATERITUM : ich lernte. FUTUR : ich werde lernen.",
    "wohnen": "WOHNEN = HABITER en Allemand. PRASENS : ich wohne, du wohnst, er wohnt, wir wohnen, ihr wohnt, sie wohnen. PERFEKT : ich habe gewohnt. PRATERITUM : ich wohnte. FUTUR : ich werde wohnen.",
    "spielen": "SPIELEN = JOUER en Allemand. PRASENS : ich spiele, du spielst, er spielt, wir spielen, ihr spielt, sie spielen. PERFEKT : ich habe gespielt. PRATERITUM : ich spielte. FUTUR : ich werde spielen.",
    "arbeiten": "ARBEITEN = TRAVAILLER en Allemand. PRASENS : ich arbeite, du arbeitest, er arbeitet, wir arbeiten, ihr arbeitet, sie arbeiten. PERFEKT : ich habe gearbeitet. PRATERITUM : ich arbeitete. FUTUR : ich werde arbeiten.",
    "konnen": "KONNEN = POUVOIR en Allemand. PRASENS : ich kann, du kannst, er kann, wir konnen, ihr konnt, sie konnen. PERFEKT : ich habe gekonnt. PRATERITUM : ich konnte. FUTUR : ich werde konnen.",
    "wollen": "WOLLEN = VOULOIR en Allemand. PRASENS : ich will, du willst, er will, wir wollen, ihr wollt, sie wollen. PERFEKT : ich habe gewollt. PRATERITUM : ich wollte. FUTUR : ich werde wollen.",
    "mussen": "MUSSEN = DEVOIR en Allemand. PRASENS : ich muss, du musst, er muss, wir mussen, ihr musst, sie mussen. PERFEKT : ich habe gemusst. PRATERITUM : ich musste. FUTUR : ich werde mussen.",
    "wissen": "WISSEN = SAVOIR en Allemand. PRASENS : ich weiss, du weisst, er weiss, wir wissen, ihr wisst, sie wissen. PERFEKT : ich habe gewusst. PRATERITUM : ich wusste. FUTUR : ich werde wissen.",
    "geben": "GEBEN = DONNER en Allemand. PRASENS : ich gebe, du gibst, er gibt, wir geben, ihr gebt, sie geben. PERFEKT : ich habe gegeben. PRATERITUM : ich gab. FUTUR : ich werde geben.",
    "nehmen": "NEHMEN = PRENDRE en Allemand. PRASENS : ich nehme, du nimmst, er nimmt, wir nehmen, ihr nehmt, sie nehmen. PERFEKT : ich habe genommen. PRATERITUM : ich nahm. FUTUR : ich werde nehmen.",
    "schreiben": "SCHREIBEN = ECRIRE en Allemand. PRASENS : ich schreibe, du schreibst, er schreibt, wir schreiben, ihr schreibt, sie schreiben. PERFEKT : ich habe geschrieben. PRATERITUM : ich schrieb. FUTUR : ich werde schreiben.",
    "to be": "TO BE = ETRE en Anglais. PRESENT : I am, You are, He is, We are, You are, They are. PAST : I was, You were, He was, We were, You were, They were. PERFECT : I have been. FUTURE : I will be.",
    "to have": "TO HAVE = AVOIR en Anglais. PRESENT : I have, You have, He has, We have, You have, They have. PAST : I had. PERFECT : I have had. FUTURE : I will have.",
    "to go": "TO GO = ALLER en Anglais. PRESENT : I go, You go, He goes, We go, You go, They go. PAST : I went. PERFECT : I have gone. FUTURE : I will go.",
    "to do": "TO DO = FAIRE en Anglais. PRESENT : I do, You do, He does, We do, You do, They do. PAST : I did. PERFECT : I have done. FUTURE : I will do.",
    "to say": "TO SAY = DIRE en Anglais. PRESENT : I say, You say, He says, We say, You say, They say. PAST : I said. PERFECT : I have said. FUTURE : I will say.",
    "to see": "TO SEE = VOIR en Anglais. PRESENT : I see, You see, He sees, We see, You see, They see. PAST : I saw. PERFECT : I have seen. FUTURE : I will see.",
    "to come": "TO COME = VENIR en Anglais. PRESENT : I come, You come, He comes, We come. PAST : I came. PERFECT : I have come. FUTURE : I will come.",
    "to get": "TO GET = OBTENIR en Anglais. PRESENT : I get, You get, He gets. PAST : I got. PERFECT : I have got. FUTURE : I will get.",
    "to make": "TO MAKE = FABRIQUER en Anglais. PRESENT : I make, You make, He makes. PAST : I made. PERFECT : I have made. FUTURE : I will make.",
    "to take": "TO TAKE = PRENDRE en Anglais. PRESENT : I take, You take, He takes. PAST : I took. PERFECT : I have taken. FUTURE : I will take.",
    "to give": "TO GIVE = DONNER en Anglais. PRESENT : I give, You give, He gives. PAST : I gave. PERFECT : I have given. FUTURE : I will give.",
    "to know": "TO KNOW = SAVOIR en Anglais. PRESENT : I know, You know, He knows. PAST : I knew. PERFECT : I have known. FUTURE : I will know.",
    "to think": "TO THINK = PENSER en Anglais. PRESENT : I think, You think, He thinks. PAST : I thought. PERFECT : I have thought. FUTURE : I will think.",
    "to speak": "TO SPEAK = PARLER en Anglais. PRESENT : I speak, You speak, He speaks. PAST : I spoke. PERFECT : I have spoken. FUTURE : I will speak.",
    "to eat": "TO EAT = MANGER en Anglais. PRESENT : I eat, You eat, He eats. PAST : I ate. PERFECT : I have eaten. FUTURE : I will eat.",
    "to drink": "TO DRINK = BOIRE en Anglais. PRESENT : I drink, You drink, He drinks. PAST : I drank. PERFECT : I have drunk. FUTURE : I will drink.",
    "to play": "TO PLAY = JOUER en Anglais. PRESENT : I play, You play, He plays. PAST : I played. PERFECT : I have played. FUTURE : I will play.",
    "to live": "TO LIVE = VIVRE en Anglais. PRESENT : I live, You live, He lives. PAST : I lived. PERFECT : I have lived. FUTURE : I will live.",
    "to love": "TO LOVE = AIMER en Anglais. PRESENT : I love, You love, He loves. PAST : I loved. PERFECT : I have loved. FUTURE : I will love.",
    "to want": "TO WANT = VOULOIR en Anglais. PRESENT : I want, You want, He wants. PAST : I wanted. PERFECT : I have wanted. FUTURE : I will want.",
    "ser": "SER = ETRE en Espagnol (identite). PRESENTE : yo soy, tu eres, el es, nosotros somos, vosotros sois, ellos son. PRETERITO : yo fui, tu fuiste, el fue, nosotros fuimos, vosotros fuisteis, ellos fueron. IMPERFECTO : yo era, tu eras, el era, nosotros eramos, vosotros erais, ellos eran. FUTURO : yo sere, tu seras, el sera.",
    "estar": "ESTAR = ETRE en Espagnol (etat / lieu). PRESENTE : yo estoy, tu estas, el esta, nosotros estamos, vosotros estais, ellos estan. PRETERITO : yo estuve. IMPERFECTO : yo estaba. FUTURO : yo estare.",
    "tener": "TENER = AVOIR en Espagnol. PRESENTE : yo tengo, tu tienes, el tiene, nosotros tenemos, vosotros teneis, ellos tienen. PRETERITO : yo tuve. IMPERFECTO : yo tenia. FUTURO : yo tendre.",
    "ir": "IR = ALLER en Espagnol. PRESENTE : yo voy, tu vas, el va, nosotros vamos, vosotros vais, ellos van. PRETERITO : yo fui. IMPERFECTO : yo iba. FUTURO : yo ire.",
    "hacer": "HACER = FAIRE en Espagnol. PRESENTE : yo hago, tu haces, el hace, nosotros hacemos, vosotros haceis, ellos hacen. PRETERITO : yo hice. IMPERFECTO : yo hacia. FUTURO : yo hare.",
    "decir": "DECIR = DIRE en Espagnol. PRESENTE : yo digo, tu dices, el dice, nosotros decimos, vosotros decis, ellos dicen. PRETERITO : yo dije. IMPERFECTO : yo decia. FUTURO : yo dire.",
    "poder": "PODER = POUVOIR en Espagnol. PRESENTE : yo puedo, tu puedes, el puede, nosotros podemos, vosotros podeis, ellos pueden. PRETERITO : yo pude. IMPERFECTO : yo podia. FUTURO : yo podre.",
    "querer": "QUERER = VOULOIR en Espagnol. PRESENTE : yo quiero, tu quieres, el quiere, nosotros queremos, vosotros quereis, ellos quieren. PRETERITO : yo quise. IMPERFECTO : yo queria. FUTURO : yo querre.",
    "saber": "SABER = SAVOIR en Espagnol. PRESENTE : yo se, tu sabes, el sabe, nosotros sabemos, vosotros sabeis, ellos saben. PRETERITO : yo supe. IMPERFECTO : yo sabia. FUTURO : yo sabre.",
    "hablar": "HABLAR = PARLER en Espagnol. PRESENTE : yo hablo, tu hablas, el habla, nosotros hablamos, vosotros hablais, ellos hablan. PRETERITO : yo hable. IMPERFECTO : yo hablaba. FUTURO : yo hablare.",
    "comer": "COMER = MANGER en Espagnol. PRESENTE : yo como, tu comes, el come, nosotros comemos, vosotros comeis, ellos comen. PRETERITO : yo comi. IMPERFECTO : yo comia. FUTURO : yo comere.",
    "vivir": "VIVIR = VIVRE en Espagnol. PRESENTE : yo vivo, tu vives, el vive, nosotros vivimos, vosotros vivis, ellos viven. PRETERITO : yo vivi. IMPERFECTO : yo vivia. FUTURO : yo vivire.",
    "jugar": "JUGAR = JOUER en Espagnol. PRESENTE : yo juego, tu juegas, el juega, nosotros jugamos, vosotros jugais, ellos juegan. PRETERITO : yo jugue. IMPERFECTO : yo jugaba. FUTURO : yo jugare.",
    "essere": "ESSERE = ETRE en Italien. PRESENTE : io sono, tu sei, lui e, noi siamo, voi siete, loro sono. PASSATO : io sono stato. IMPERFETTO : io ero, tu eri, lui era, noi eravamo, voi eravate, loro erano. FUTURO : io saro, tu sarai, lui sara.",
    "avere": "AVERE = AVOIR en Italien. PRESENTE : io ho, tu hai, lui ha, noi abbiamo, voi avete, loro hanno. PASSATO : io ho avuto. IMPERFETTO : io avevo. FUTURO : io avro.",
    "andare": "ANDARE = ALLER en Italien. PRESENTE : io vado, tu vai, lui va, noi andiamo, voi andate, loro vanno. PASSATO : io sono andato. IMPERFETTO : io andavo. FUTURO : io andro.",
    "fare": "FARE = FAIRE en Italien. PRESENTE : io faccio, tu fai, lui fa, noi facciamo, voi fate, loro fanno. PASSATO : io ho fatto. IMPERFETTO : io facevo. FUTURO : io faro.",
    "potere": "POTERE = POUVOIR en Italien. PRESENTE : io posso, tu puoi, lui puo, noi possiamo, voi potete, loro possono. PASSATO : io ho potuto. IMPERFETTO : io potevo. FUTURO : io potro.",
    "volere": "VOLERE = VOULOIR en Italien. PRESENTE : io voglio, tu vuoi, lui vuole, noi vogliamo, voi volete, loro vogliono. PASSATO : io ho voluto. IMPERFETTO : io volevo. FUTURO : io vorro.",
    "sapere": "SAPERE = SAVOIR en Italien. PRESENTE : io so, tu sai, lui sa, noi sappiamo, voi sapete, loro sanno. PASSATO : io ho saputo. IMPERFETTO : io sapevo. FUTURO : io sapro.",
    "venire": "VENIRE = VENIR en Italien. PRESENTE : io vengo, tu vieni, lui viene, noi veniamo, voi venite, loro vengono. PASSATO : io sono venuto. IMPERFETTO : io venivo. FUTURO : io verro.",
    "vedere": "VEDERE = VOIR en Italien. PRESENTE : io vedo, tu vedi, lui vede, noi vediamo, voi vedete, loro vedono. PASSATO : io ho visto. IMPERFETTO : io vedevo. FUTURO : io vedro.",
    "parlare": "PARLARE = PARLER en Italien. PRESENTE : io parlo, tu parli, lui parla, noi parliamo, voi parlate, loro parlano. PASSATO : io ho parlato. IMPERFETTO : io parlavo. FUTURO : io parlero.",
    "mangiare": "MANGIARE = MANGER en Italien. PRESENTE : io mangio, tu mangi, lui mangia, noi mangiamo, voi mangiate, loro mangiano. PASSATO : io ho mangiato. IMPERFETTO : io mangiavo. FUTURO : io mangero.",
    "giocare": "GIOCARE = JOUER en Italien. PRESENTE : io gioco, tu giochi, lui gioca, noi giochiamo, voi giocate, loro giocano. PASSATO : io ho giocato. IMPERFETTO : io giocavo. FUTURO : io giochero.",
}
TOUT = {
    "pythagore": "THEOREME DE PYTHAGORE : Formule : a2 + b2 = c2. UNIQUEMENT pour un triangle rectangle. Ex : 3-4-5 car 9+16=25. Ex : Si a=6, b=8, alors c2 = 36+64=100, donc c=10.",
    "thales": "THALES : Si 2 droites paralleles coupent 2 secantes, rapports egaux. Formule : AB / AD = AC / AE = BC / DE.",
    "moyenne": "MOYENNE : Moyenne = somme / nombre. Ex : Notes 12, 15, 18. Somme = 45. Nombre = 3. Moyenne = 45 / 3 = 15.",
    "aire": "AIRE : Rectangle = L x l, Carre = cote x cote, Triangle = (base x hauteur) / 2, Cercle = pi x rayon2 (pi = 3,14).",
    "perimetre": "PERIMETRE : Carre = 4 x cote, Rectangle = 2 x (L+l), Cercle = 2 x pi x rayon.",
    "volume": "VOLUME : Cube = cote3, Pave = L x l x h. Ex : Boite 2x3x4 = 24 cm3.",
    "angle": "ANGLES : Droit = 90 degres, Plat = 180 degres, Plein = 360 degres. Triangle = 180 degres au total.",
    "triangle": "TRIANGLE : 3 cotes, 3 angles, somme = 180 degres. Types : Equilateral, Isocele, Rectangle, Scalene. Aire = (base x hauteur) / 2.",
    "cercle": "CERCLE : Centre, rayon, diametre = 2 x rayon. Perimetre = 2 x pi x rayon. Aire = pi x rayon2.",
    "fraction": "FRACTION : 1/2 = la moitie, 1/4 = le quart. 1/2 + 1/4 = 2/4 + 1/4 = 3/4.",
    "pourcentage": "POURCENTAGE : (partie / total) x 100. Ex : 20% de 50 = 10. Tu as 15/20 : (15/20) x 100 = 75%.",
    "equation": "EQUATION : 2x + 3 = 7. Tu enleves 3 : 2x = 4. Tu divises par 2 : x = 2.",
    "racine carree": "RACINE CARREE : Racine de 9 = 3 car 3x3 = 9. Racine de 16 = 4. Racine de 25 = 5.",
    "division": "DIVISION : 12 / 3 = 4. 13 / 4 = 3 reste 1.",
    "cod": "COD : Complement d'Objet Direct. Il repond a Qui ? ou Quoi ? Ex : Je mange une pomme. Je mange quoi ? Une pomme = COD.",
    "coi": "COI : Complement d'Objet Indirect. Il repond a A qui ? A quoi ? Ex : Je parle a Lenny. Je parle a qui ? A Lenny = COI.",
    "sujet": "SUJET : C'est qui fait l'action. Ex : Lenny mange. Qui mange ? Lenny = sujet.",
    "adjectif": "ADJECTIF : Il decrit un nom, il s'accorde. Ex : grand garcon / grande fille.",
    "pluriel": "PLURIEL : +s : chat -> chats. En -eau : bateau -> bateaux. En -al : cheval -> chevaux.",
    "verbe": "VERBE : C'est l'action dans la phrase. Ex : Je mange, Tu cours, Il dort.",
    "pronom": "PRONOM : Il remplace un nom. Ex : Lenny mange. Il mange.",
    "synonyme": "SYNONYME : Mot qui veut dire la meme chose. Ex : content = heureux.",
    "antonyme": "ANTONYME : Mot qui veut dire le contraire. Ex : grand = petit, chaud = froid.",
    "homonyme": "HOMONYME : Mots qui se prononcent pareil mais s'ecrivent differemment. Ex : a / a, et / est, son / sont.",
    "famille de mots": "FAMILLE DE MOTS : Mots qui ont la meme racine. Ex : fleur, fleuri, fleuriste.",
    "der": "DER DIE DAS : der = masculin, die = feminin, das = neutre. Pluriel = die.",
    "accusatif": "ACCUSATIF : C'est le cas du COD. der devient den. Ex : Ich sehe den Hund.",
    "datif": "DATIF : C'est le cas du COI (a qui ?). der devient dem, die devient der, das devient dem.",
    "nominatif": "NOMINATIF : C'est le cas du sujet. der, die, das.",
    "present simple": "PRESENT SIMPLE : Pour les habitudes. I play, He plays (avec -s !).",
    "present perfect": "PRESENT PERFECT : have + participe. I have eaten = J'ai mange.",
    "present continu": "PRESENT CONTINU : be + -ing. I am playing = Je suis en train de jouer.",
    "preterit": "PRETERIT : Pour le passe termine. I played. Verbes irreguliers : I went, I saw, I ate.",
    "ser et estar": "SER et ESTAR : SER = etre permanent (Soy de Suiza). ESTAR = etre temporaire / lieu (Estoy en casa).",
    "el / la": "EL / LA : el = masculin, la = feminin, los / las = pluriel.",
    "pluriel en espagnol": "PLURIEL EN ESPAGNOL : +s : casa -> casas. -z : lapiz -> lapices.",
    "il / lo / la": "IL / LO / LA - ITALIEN : il = masculin, lo = masculin devant s+consonne, la = feminin.",
    "pluriel en italien": "PLURIEL EN ITALIEN : -o devient -i : libro -> libri. -a devient -e : casa -> case.",
    "photosynthese": "PHOTOSYNTHESE : Soleil + Eau + CO2 = Oxygene + Sucre.",
    "gravite": "GRAVITE : La gravite nous attire vers la Terre. C'est Newton qui l'a decouverte.",
    "coeur": "COEUR : Pompe le sang. 100 000 battements par jour !",
    "volcan": "VOLCAN : Ouverture dans la Terre par ou sort du magma. Le plus actif d'Europe = Etna.",
    "foudre": "FOUDRE : 30 000 degres, 5x plus chaud que le Soleil ! Si tu entends le tonnerre, rentre.",
    "saison": "SAISONS : C'est l'inclinaison de la Terre (23,5 degres) qui fait les saisons.",
    "cerveau": "CERVEAU : 1,4 kg, 86 milliards de neurones. Il controle tout.",
    "masse volumique": "MASSE VOLUMIQUE : Formule : masse / volume. Rho = m / V. Ex : 100g / 100 cm3 = 1 = eau. Huile = 0,9 flotte, Fer = 7,8 coule.",
    "atome": "ATOME : Noyau avec protons (+) et neutrons (0), et autour des electrons (-).",
    "oxygene": "OXYGENE : O2. On respire O2, on rejette CO2. 21% de l'air = oxygene.",
    "chimie": "CHIMIE : Etude de la matiere. H2O = eau. CO2 = dioxyde de carbone.",
    "electricite": "ELECTRICITE : P = U x I. En serie : si une lampe grille, tout s'eteint. En parallele : les autres restent allumees.",
    "vitesse": "VITESSE : v = d / t. Ex : 100m en 10 sec = 10 m/s = 36 km/h.",
    "energie": "ENERGIE : Cinetique, potentielle, thermique, electrique, solaire. On ne cree pas d'energie, on la transforme.",
    "adn": "ADN : Ton code genetique. 50% pere, 50% mere.",
    "trou noir": "TROU NOIR : Objet tellement lourd que meme la lumiere ne peut pas en sortir.",
    "big bang": "BIG BANG : Debut de l'univers il y a 13,8 milliards d'annees.",
    "mars": "MARS : Planete rouge. Un jour = 24h37. Temperature : -60 degres.",
    "iss": "ISS : Station Spatiale a 400 km, a 28 000 km/h. 16 levers de soleil par jour !",
    "systeme solaire": "SYSTEME SOLAIRE : 8 planetes : Mercure, Venus, Terre, Mars, Jupiter, Saturne, Uranus, Neptune.",
    "soleil": "SOLEIL : C'est une etoile, pas une planete. Temperature : 5500 degres a la surface.",
    "galaxie": "GALAXIE : Groupe de milliards d'etoiles. Notre galaxie = Voie Lactee.",
    "lune": "LUNE : Distance : 384 000 km. Premier homme dessus : Neil Armstrong, 1969.",
    "boucle": "BOUCLE : for i in range(1,6): print(i) -> affiche 1,2,3,4,5.",
    "variable": "VARIABLE : Boite qui stocke une valeur. Ex : age = 13, prenom = Lenny.",
    "condition": "CONDITION : if age >= 18: print('Majeur') else: print('Mineur').",
    "fonction": "FONCTION : Bloc de code qu'on peut reutiliser. def dire_bonjour(): print('Bonjour').",
    "liste": "LISTE : notes = [12, 15, 18]. notes[0] = 12.",
    "algorithme": "ALGORITHME : Suite d'etapes pour resoudre un probleme. Ex : Recette de cuisine.",
    "python": "PYTHON : Langage facile, celui de ton agent. Utilise pour l'IA, les sites web, les jeux.",
    "html": "HTML : Squelette d'un site. h1 = Titre, p = Texte.",
    "css": "CSS : Style d'un site : couleurs, tailles.",
    "javascript": "JAVASCRIPT : Pour rendre un site interactif : boutons, animations, jeux.",
    "ia": "IA : Programme qui apprend avec des donnees. Ex : ChatGPT, ton agent.",
    "joconde": "JOCONDE : Peinture de Leonard de Vinci. Au Louvre a Paris. La plus celebre au monde.",
    "van gogh": "VAN GOGH : Peintre neerlandais. Tableaux : La Nuit etoilee, Les Tournesols.",
    "picasso": "PICASSO : Peintre espagnol. Il a invente le cubisme. Il a peint Guernica.",
    "rap": "RAP : Musique nee dans le Bronx a New York. En France, c'est la musique la plus ecoutee.",
    "piano": "PIANO : Instrument avec 88 touches. Les plus grands : Mozart, Beethoven, Chopin.",
    "guitare": "GUITARE : Instrument avec 6 cordes. Accords de base : Do, Sol, La mineur, Mi mineur.",
    "foot": "FOOT : Sport le plus joue au monde, 3,5 milliards de fans ! 2 equipes de 11, 90 minutes.",
    "basket": "BASKET : 5 vs 5, panier a 3,05m. Michael Jordan = GOAT. 【entity-Wembanyama¦canonical_name=Wembanyama】 = 2m24 !",
    "tennis": "TENNIS : 【entity-Federer¦canonical_name=Roger Federer】 (20 Grands Chelems, Suisse !), 【entity-Nadal¦canonical_name=Nadal】 (22), 【entity-Djokovic¦canonical_name=Djokovic】 (24, record).",
    "formule 1": "FORMULE 1 : 350 km/h ! 【entity-Verstappen¦canonical_name=Verstappen】 a gagne 2021, 2022, 2023, 2024. 【entity-Hamilton¦canonical_name=Hamilton】 = 7 titres.",
    "jo": "JO : Tous les 4 ans. 2024 = Paris, 2028 = Los Angeles. Devise : Plus vite, plus haut, plus fort.",
    "manger sain": "MANGER SAIN : 5 fruits et legumes par jour, boire 1,5L d'eau, moins de sucre.",
    "sommeil": "SOMMEIL : A 13 ans, il faut 9-10h de sommeil ! Pas d'ecran 1h avant de dormir.",
    " 【entity-messi¦canonical_name=Messi】": " 【entity-MESSI¦canonical_name=Messi】 : 8 Ballons d'Or (record), 91 buts en une annee. Coupe du Monde 2022. Meilleur de tous les temps.",
    " 【entity-ronaldo¦canonical_name=RONALDO】": " 【entity-RONALDO¦canonical_name=RONALDO】 : 5 Ballons d'Or, meilleur buteur de l'histoire (900 buts). 600M de followers.",
    " mbappe": " MBAPPE : Champion du Monde 2018 a 19 ans. Vitesse : 36 km/h. 【entity-Real Madrid¦canonical_name=Real Madrid】 depuis 2024.",
    "ballon d'or": "BALLON D'OR : Trophee du meilleur joueur du monde. 【entity-Messi¦canonical_name=Messi】 en a 8 (record), 【entity-Ronaldo¦canonical_name=RONALDO】 5.",
    "coupe du monde": "COUPE DU MONDE : Tous les 4 ans, 48 equipes en 2026. 2022 = Argentine gagne contre France.",
    "ligue des champions": "LIGUE DES CHAMPIONS : 【entity-Real Madrid¦canonical_name=Real Madrid】 a gagne 15 fois, record !",
    "minecraft": "MINECRAFT : Jeu le plus vendu au monde : 300M de copies ! Monde en cubes, Creeper, Ender Dragon.",
    "fortnite": "FORTNITE : Battle Royale : 100 joueurs, le dernier vivant gagne. Modes : Battle Royale, Zero Construction, Lego.",
    "roblox": "ROBLOX : Des millions de jeux crees par les joueurs. Jeux cultes : Brookhaven, Blox Fruits, Doors.",
    "gta": "GTA V : 190M de copies. Monde ouvert : Los Santos. GTA VI sort en 2026, a Vice City.",
    "brawl stars": "BRAWL STARS : Jeu mobile de Supercell. 3v3, Brawlers : Shelly, Colt, Spike, Leon...",
    "mario": "MARIO : Plombier Nintendo, sauve Peach. Jeux : Super Mario Bros, Mario Kart, Mario Party.",
    "pokemon": "POKEMON : Attrape-les tous ! 1000+ Pokemons. Pikachu = mascotte. Cartes Pokemon = les plus collectionnees.",
    "one piece": "ONE PIECE : Manga le plus vendu au monde (500M de tomes). Luffy veut devenir Roi des Pirates.",
    "naruto": "NARUTO : Ninja qui veut devenir Hokage. Rasengan, Chidori, Kyubi (demon renard a 9 queues).",
    "dragon ball": "DRAGON BALL : Goku, Super Saiyan, Kamehameha ! Transformations : Super Saiyan 1, 2, 3, Blue, Ultra Instinct.",
    "tour eiffel": "TOUR EIFFEL : Paris, 330m, 1889, Gustave Eiffel. 7M de visiteurs par an.",
    "pyramide": "PYRAMIDES : En Egypte, il y a 4500 ans pour les Pharaons. La plus grande = Kheops, 146m.",
    "titanic": "TITANIC : Paquebot anglais, 1912. Il heurte un iceberg, il coule en 2h40. Film 1997, 11 Oscars.",
    "harry potter": "HARRY POTTER : Sorcier avec une cicatrice en eclair, par J.K. Rowling. 7 livres, 8 films. Maisons : Gryffondor, Serpentard, Poufsouffle, Serdaigle.",
    "millionnaire": "COMMENT DEVENIR MILLIONNAIRE ? : 1. Salarie + investissement. 2. Entrepreneur. 3. Createur. Conseils : Apprends une competence, epargne, investis tot.",
    "salaire": "SALAIRE : Argent que tu gagnes chaque mois. En Suisse : salaire moyen autour de 6500 CHF / mois.",
    "entrepreneur": "ENTREPRENEUR : Quelqu'un qui cree son entreprise. Ex : Elon Musk, Jeff Bezos, Mark Zuckerberg.",
    "gagner de l argent": "GAGNER DE L'ARGENT A 13 ANS : Petits services, vendre ce que tu n'utilises plus, creer un projet et montrer a tes parents, apprendre une competence.",
    "bourse": "BOURSE : Acheter une petite partie d'une entreprise. ETF = panier de beaucoup d'entreprises, moins risque.",
    "plus grand animal": "PLUS GRAND ANIMAL : Baleine bleue ! 30m, 200 tonnes !",
    "plus rapide": "PLUS RAPIDE : Guepard = 110 km/h. Faucon pelerin = 390 km/h en pique !",
    "chien": "CHIEN : Meilleur ami de l'homme depuis 15 000 ans. 400 races. Il comprend 150 mots.",
    "chat": "CHAT : Il dort 16h par jour ! Il peut sauter 6x sa hauteur.",
    "lion": "LION : Roi des animaux. Il dort 20h par jour ! Il rugit si fort qu'on l'entend a 8 km.",
    "dauphin": "DAUPHIN : Animal tres intelligent. Il dort avec un oeil ouvert. Il peut nager a 60 km/h.",
    "recette facile": "RECETTE FACILE - PATES : 1. Fais bouillir de l'eau salee. 2. Mets les pates 8-10 min. 3. Egoutte. 4. Ajoute sauce tomate + fromage.",
    "gateau au chocolat": "GATEAU AU CHOCOLAT : 200g chocolat, 200g beurre, 4 oeufs, 150g sucre, 100g farine. Four 180 degres pendant 25 min.",
    "conseil pour reviser": "CONSEIL POUR REVISER : 1. Pomodoro : 25 min, 5 min pause. 2. Teste-toi. 3. Explique a quelqu'un. 4. Dors bien. 5. Pas de telephone.",
    "2eme guerre": "2EME GUERRE : 1939-1945. Allemagne contre Allies. 60 millions de morts.",
    "1ere guerre": "1ERE GUERRE : 1914-1918. Guerre des tranchees, 18 millions de morts.",
    "revolution": "REVOLUTION FRANCAISE : 1789. Prise de la Bastille 14 juillet 1789.",
    "rome": "ROME : Empire romain, il y a 2000 ans. Colisee, gladiateurs, Jules Cesar.",
    "moyen age": "MOYEN AGE : 500-1500. Chateaux forts, chevaliers, rois.",
    "egypte": "EGYPTE : Pharaons, pyramides, Nil, hieroglyphes. Cleopatre.",
    "napoleon": "NAPOLEON : Empereur francais 1804-1815. Il a conquis presque toute l'Europe. Waterloo 1815.",
    "dinosaures": "DINOSAURES : Ils ont vecu il y a 230 a 66 millions d'annees. T-Rex, Diplodocus. Ils ont disparu a cause d'un asteroide.",
    "continents": "CONTINENTS : Il y en a 7 : Afrique, Amerique du Nord, Amerique du Sud, Antarctique, Asie, Europe, Oceanie.",
    "oceans": "OCEANS : Il y en a 5 : Pacifique (le plus grand), Atlantique, Indien, Arctique, Austral.",
}
AVIONS = {
    "f-22": "F-22 RAPTOR (USA) - LE PLUS PERFORMANT EN COMBAT. Mach 2.25. Furtif, jamais battu.",
    "f-35": "F-35 LIGHTNING II (USA) - LE PLUS MODERNE. Mach 1.6. La Suisse en a achete 36 !",
    "rafale": "RAFALE (France). Mach 1.8. Polyvalent : air, sol, mer.",
    "sr-71": "SR-71 BLACKBIRD. Mach 3.3 = 3500 km/h ! Plus rapide de tous les temps.",
    "concorde": "CONCORDE : Paris-New York en 3h30. Mach 2. Arrete en 2003.",
    "f-16": "F-16. Mach 2.0. Plus produit : 4600 exemplaires !",
    "f-15": "F-15 EAGLE. Mach 2.5 ! 104 victoires a 0 defaite !",
    "a380": "【entity-AIRBUS¦canonical_name=AIRBUS】 A380 : Le plus gros avion de passagers. 2 etages, 850 passagers max !",
    "comment vole": "COMMENT VOLE UN AVION ? : L'aile est courbee en haut, plate en bas. L'air va plus vite au-dessus, donc pression plus faible au-dessus. Ca cree une force vers le haut = portance.",
}

def toutes_tables():
    txt = "TOUTES LES TABLES 1 a 12 :\n\n"
    for n in range(1, 13):
        txt += "Table de " + str(n) + " : " + ", ".join([str(n) + "x" + str(i) + "=" + str(n * i) for i in range(1, 11)]) + "\n\n"
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
    # QUITTER PAR TEXTE AUSSI
    if q_low in ["stop", "arrete", "arreter", "stop entrainement", "quitter", "quitter entrainement", "exit", "sortir"]:
        if st.session_state.mode_train:
            st.session_state.mode_train = False
            st.session_state.train_q = None
            return "Entrainement termine ! Score final : " + str(st.session_state.score) + "/" + str(st.session_state.total_quiz) + " | Meilleur streak : " + str(st.session_state.best_streak) + " ! Bravo ! Clique sur MODE ENTRAINEMENT pour recommencer quand tu veux !"
        else:
            return "Tu n'es pas en entrainement. Clique sur MODE ENTRAINEMENT en haut pour commencer !"
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
            rep = "Pas tout a fait... La bonne reponse c'etait '" + st.session_state.train_a + "'. Score : " + str(st.session_state.score) + "/" + str(st.session_state.total_quiz)
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
        return rep + "\n\nQuestion suivante (" + st.session_state.niveau + ") : " + nq + "\n\nPour quitter, clique sur QUITTER ENTRAINEMENT ou ecris 'stop'."
    if "entrainement facile" in q_low:
        lancer_entrainement("facile", TRAIN_FACILE)
        return "Entrainement facile lance !"
    if "entrainement difficile" in q_low:
        lancer_entrainement("difficile", TRAIN_DIFFICILE)
        return "Entrainement difficile lance !"
    if "entrainement verbes" in q_low or "quiz verbes" in q_low:
        lancer_entrainement("verbes", TRAIN_VERBES)
        return "Entrainement verbes lance !"
    if "quiz maths" in q_low:
        lancer_entrainement("maths", TRAIN_MATHS)
        return "Quiz maths lance !"
    if "quiz francais" in q_low:
        lancer_entrainement("francais", TRAIN_FRANCAIS)
        return "Quiz francais lance !"
    if "quiz capitales" in q_low:
        lancer_entrainement("capitales", TRAIN_CAPITALES)
        return "Quiz capitales lance !"
    if "entraine" in q_low or "entrainement" in q_low or "mode entrainement" in q_low:
        lancer_entrainement("moyen", TRAIN_MOYEN)
        return "Entrainement moyen lance !"
    if "mon score" in q_low or q_low == "score":
        return "Ton score : " + str(st.session_state.score) + " / " + str(st.session_state.total_quiz) + " ! Streak : " + str(st.session_state.streak) + " | Best : " + str(st.session_state.best_streak) + " !"
    if q_brut.startswith("apprends") or q_brut.startswith("apprend") or "retient que" in q_brut:
        try:
            texte = q_brut.replace("apprends :", "").replace("apprends", "").replace("apprend :", "").replace("apprend", "").replace("retient que", "").strip()
            if "=" in texte:
                cle, val = texte.split("=", 1)
                cle = nettoyer(cle)
                val = val.strip()
                st.session_state.learned[cle] = val
                return "MERCI ! J'ai appris ! '" + cle + "' = '" + val + "' ! J'ai appris " + str(len(st.session_state.learned)) + " choses !"
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
    if "blague" in q_low or "fait moi rire" in q_low:
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
    if "traduis" in q_low or "en anglais" in q_low or "en allemand" in q_low or "en espagnol" in q_low or "en italien" in q_low:
        for cle, rep in TRADUCTIONS.items():
            if nettoyer(cle) in q_low:
                return rep
        return "Je peux traduire : bonjour, merci, ecole, chien en anglais / allemand / espagnol / italien."
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
        return "AVION LE PLUS PERFORMANT ? 1. Combat : F-22 Raptor. 2. Moderne : F-35. 3. Vitesse : SR-71 - 3500 km/h."
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
    return "Hmm, je ne connais pas encore : '" + q_orig + "'...\n\nMais tu peux M'APPRENDRE ! Ecris :\n\nApprends : " + q_orig + " = ta reponse ici\n\nEssaie : MODE ENTRAINEMENT / Conjugue ETRE / C'est quoi Pythagore ?"

if st.session_state.auto_q:
    q_auto = st.session_state.auto_q
    st.session_state.auto_q = ""
    r_auto = trouver(q_auto)
    st.session_state.messages.append({"role": "assistant", "content": r_auto})
    with st.chat_message("assistant"):
        st.write(r_auto)

if question := st.chat_input("Pose ta question, ou reponds a la question d'entrainement ici !"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        r = trouver(question)
        st.write(r)
    st.session_state.messages.append({"role": "assistant", "content": r})
