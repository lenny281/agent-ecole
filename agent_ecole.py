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

for k,v in {"learned":{},"theme":"📐 Ecole","matiere":None,"genre":None,"score":0,"total_quiz":0,"streak":0,"best_streak":0,"train_q":None,"train_a":None,"mode_train":False,"niveau":"moyen","train_matiere":None}.items():
    if k not in st.session_state: st.session_state[k]=v

MATIERES_GENRES = {
    "📐 Maths": {
        "📐 Géométrie": ["C'est quoi le théorème de Pythagore ?", "C'est quoi Thales ?", "C'est quoi l'aire ?", "C'est quoi le perimetre ?", "C'est quoi le volume ?", "C'est quoi un angle ?", "C'est quoi un triangle ?", "C'est quoi un cercle ?"],
        "🧮 Calcul": ["Table de 7", "Toutes les tables de multiplication", "Table de division de 8", "C'est quoi la moyenne ?", "Calcule 12+8", "Calcule 15x7", "Calcule 144/12", "C'est quoi la division ?"],
        "🍕 Fractions / % / Algèbre": ["C'est quoi une fraction ?", "C'est quoi le pourcentage ?", "C'est quoi une equation ?", "C'est quoi le nombre decimal ?", "C'est quoi la proportionnalité ?", "C'est quoi la racine carrée ?"],
    },
    "🇫🇷 Français": {
        "📖 Grammaire": ["C'est quoi le COD ?", "C'est quoi le COI ?", "C'est quoi le sujet ?", "C'est quoi un adjectif ?", "C'est quoi le pluriel ?", "C'est quoi le verbe ?", "C'est quoi le pronom ?", "C'est quoi le complément circonstanciel ?"],
        "✍️ Verbes les plus connus": ["Conjugue ETRE", "Conjugue AVOIR", "Conjugue ALLER", "Conjugue FAIRE", "Conjugue DIRE", "Conjugue POUVOIR", "Conjugue VOULOIR", "Conjugue SAVOIR", "Conjugue DEVOIR", "Conjugue VENIR", "Conjugue VOIR", "Conjugue PRENDRE", "Conjugue METTRE", "Conjugue DONNER", "Conjugue PARLER", "Conjugue MANGER", "Conjugue DORMIR", "Conjugue ECRIRE", "Conjugue LIRE", "Conjugue PARTIR", "Conjugue SORTIR", "Conjugue FINIR", "Conjugue JOUER", "Conjugue TRAVAILLER", "Conjugue APPRENDRE"],
        "📝 Orthographe": ["C'est quoi a / à ?", "C'est quoi et / est ?", "C'est quoi son / sont ?", "C'est quoi ces / ses ?", "C'est quoi ou / où ?", "C'est quoi la / là ?", "C'est quoi se / ce ?"],
        "📚 Vocabulaire": ["C'est quoi un synonyme ?", "C'est quoi un antonyme ?", "C'est quoi un homonyme ?", "C'est quoi une famille de mots ?", "C'est quoi le champ lexical ?"],
    },
    "🇩🇪 Allemand": {
        "📖 Grammaire": ["C'est quoi der die das ?", "C'est quoi l'accusatif ?", "C'est quoi le datif ?", "C'est quoi le nominatif ?", "C'est quoi le genitif ?"],
        "✍️ Verbes les plus connus": ["Conjugue SEIN", "Conjugue HABEN", "Conjugue GEHEN", "Conjugue MACHEN", "Conjugue KOMMEN", "Conjugue SEHEN", "Conjugue SPRECHEN", "Conjugue ESSEN", "Conjugue TRINKEN", "Conjugue LERNEN", "Conjugue WOHNEN", "Conjugue SPIELEN", "Conjugue ARBEITEN", "Conjugue KÖNNEN", "Conjugue WOLLEN", "Conjugue MÜSSEN", "Conjugue WISSEN", "Conjugue GEBEN", "Conjugue NEHMEN", "Conjugue SCHREIBEN", "Conjugue LESEN", "Conjugue FAHREN", "Conjugue SCHLAFEN"],
        "🌍 Vocabulaire": ["Traduis bonjour en allemand", "Traduis merci en allemand", "Traduis ecole en allemand", "Traduis chien en allemand", "Traduis maison en allemand", "Traduis pomme en allemand"],
    },
    "🇬🇧 Anglais": {
        "📖 Grammaire": ["C'est quoi le present simple ?", "C'est quoi le present perfect ?", "C'est quoi le present continu ?", "C'est quoi le preterit ?", "C'est quoi le futur ?", "C'est quoi le pluriel en anglais ?", "C'est quoi le comparatif ?"],
        "✍️ Verbes les plus connus": ["Conjugue TO BE", "Conjugue TO HAVE", "Conjugue TO GO", "Conjugue TO DO", "Conjugue TO SAY", "Conjugue TO SEE", "Conjugue TO COME", "Conjugue TO GET", "Conjugue TO MAKE", "Conjugue TO TAKE", "Conjugue TO GIVE", "Conjugue TO KNOW", "Conjugue TO THINK", "Conjugue TO SPEAK", "Conjugue TO EAT", "Conjugue TO DRINK", "Conjugue TO PLAY", "Conjugue TO LIVE", "Conjugue TO LOVE", "Conjugue TO WANT", "Conjugue TO WORK", "Conjugue TO LEARN", "Conjugue TO READ", "Conjugue TO WRITE"],
        "🌍 Vocabulaire": ["Traduis bonjour en anglais", "Traduis merci en anglais", "Traduis ecole en anglais", "Traduis chien en anglais", "Traduis maison en anglais", "Traduis pomme en anglais", "Traduis eau en anglais"],
    },
    "🇪🇸 Espagnol": {
        "📖 Grammaire": ["C'est quoi ser et estar ?", "C'est quoi el / la / los / las ?", "C'est quoi le pluriel en espagnol ?", "C'est quoi le genre en espagnol ?"],
        "✍️ Verbes les plus connus": ["Conjugue SER", "Conjugue ESTAR", "Conjugue TENER", "Conjugue IR", "Conjugue HACER", "Conjugue DECIR", "Conjugue PODER", "Conjugue QUERER", "Conjugue SABER", "Conjugue VENIR", "Conjugue VER", "Conjugue HABLAR", "Conjugue COMER", "Conjugue VIVIR", "Conjugue JUGAR", "Conjugue TRABAJAR", "Conjugue APRENDER"],
        "🌍 Vocabulaire": ["Traduis bonjour en espagnol", "Traduis merci en espagnol", "Traduis ecole en espagnol", "Traduis chien en espagnol"],
    },
    "🇮🇹 Italien": {
        "📖 Grammaire": ["C'est quoi il / lo / la ?", "C'est quoi le pluriel en italien ?", "C'est quoi le genre en italien ?"],
        "✍️ Verbes les plus connus": ["Conjugue ESSERE", "Conjugue AVERE", "Conjugue ANDARE", "Conjugue FARE", "Conjugue DIRE", "Conjugue POTERE", "Conjugue VOLERE", "Conjugue SAPERE", "Conjugue VENIRE", "Conjugue VEDERE", "Conjugue PARLARE", "Conjugue MANGIARE", "Conjugue GIOCARE", "Conjugue VIVERE"],
        "🌍 Vocabulaire": ["Traduis bonjour en italien", "Traduis merci en italien", "Traduis ecole en italien"],
    },
    "📜 Histoire / Géo": {
        "📜 Histoire": ["C'est quoi la 2eme Guerre ?", "C'est quoi la 1ere Guerre ?", "C'est quoi la Revolution ?", "C'est quoi Rome ?", "C'est quoi le Moyen Age ?", "C'est quoi l'Egypte ?", "C'est quoi Napoleon ?", "C'est quoi la Guerre Froide ?", "C'est quoi la Prehistoire ?", "C'est quoi les dinosaures ?"],
        "🌍 Géographie": ["C'est quoi les continents ?", "C'est quoi les oceans ?", "C'est quoi le climat ?", "C'est quoi la population ?", "Capitale du Japon ?", "Capitale de la France ?", "Capitale de la Suisse ?", "Capitale du Bresil ?"],
    },
    "🔬 Sciences": {
        "🧬 Biologie": ["C'est quoi la photosynthese ?", "C'est quoi le coeur ?", "C'est quoi l'ADN ?", "C'est quoi le corps humain ?", "C'est quoi le cerveau ?", "C'est quoi les cellules ?"],
        "🌍 Terre / Espace": ["C'est quoi un volcan ?", "C'est quoi les saisons ?", "C'est quoi la foudre ?", "C'est quoi le systeme solaire ?", "C'est quoi un trou noir ?", "C'est quoi Mars ?", "C'est quoi le Big Bang ?", "C'est quoi le Soleil ?"],
        "⚡ Physique": ["C'est quoi la gravite ?", "Comment calculer la masse volumique ?", "C'est quoi la vitesse ?", "C'est quoi l'energie ?", "C'est quoi la lumiere ?", "C'est quoi le son ?"],
    },
    "🧪 Chimie / Physique": {
        "⚛️ Chimie": ["C'est quoi un atome ?", "C'est quoi l'oxygene ?", "C'est quoi la chimie ?", "C'est quoi une molecule ?", "C'est quoi le tableau periodique ?", "C'est quoi l'eau ?", "C'est quoi le CO2 ?"],
        "⚡ Physique": ["C'est quoi l'electricite ?", "C'est quoi la masse volumique ?", "C'est quoi la vitesse ?", "C'est quoi la force ?", "C'est quoi la pression ?"],
    },
    "💻 Code": {
        "🧠 Bases": ["C'est quoi une variable ?", "C'est quoi une boucle ?", "C'est quoi une condition ?", "C'est quoi une fonction ?", "C'est quoi une liste ?", "C'est quoi un algorithme ?"],
        "🌐 Langages": ["C'est quoi Python ?", "C'est quoi HTML ?", "C'est quoi CSS ?", "C'est quoi JavaScript ?", "C'est quoi Scratch ?", "C'est quoi l'IA ?"],
    },
    "🎨 Arts / Musique": {
        "🎨 Arts": ["C'est quoi la Joconde ?", "C'est quoi Van Gogh ?", "C'est quoi Picasso ?", "C'est quoi l'art ?"],
        "🎵 Musique": ["C'est quoi le rap ?", "C'est quoi le piano ?", "C'est quoi la guitare ?", "C'est quoi une note ?"],
    },
    "🏃 Sport / Santé": {
        "⚽ Sports": ["C'est quoi le foot ?", "C'est quoi le basket ?", "C'est quoi le tennis ?", "C'est quoi la Formule 1 ?", "C'est quoi les JO ?"],
        "❤️ Santé": ["C'est quoi le coeur ?", "C'est quoi le sport ?", "C'est quoi manger sain ?", "C'est quoi le sommeil ?", "C'est quoi le cerveau ?"],
    },
}

THEMES = {
    "📐 Ecole": ["Voir toutes les matières 👇"],
    "👋 Bases": ["Bonjour", "Ca va ?", "Merci", "Au revoir", "Tu t'appelles comment ?", "Raconte une blague", "Motive moi", "Conseil pour reviser"],
    "🧠 Apprends-moi": ["Entraine moi", "Entrainement facile", "Entrainement difficile", "Entrainement verbes", "Mon score", "Montre ce que tu as appris", "Quiz Maths", "Quiz Francais", "Quiz Capitales"],
    "🧮 Calculatrice": ["Calcule 12+8", "Calcule 15x7", "Calcule 144/12", "Calcule 9x9", "Calcule 100-37"],
    "🌍 Traductions": ["Traduis bonjour en anglais", "Traduis merci en anglais", "Traduis bonjour en allemand", "Traduis bonjour en espagnol", "Traduis bonjour en italien"],
    "🎲 Fun": ["Raconte une blague", "Motive moi", "Conseil pour reviser", "Quelle heure il est ?", "Quelle date on est ?", "Devinette", "Fait moi rire"],
    "🌍 Capitales": ["Capitale du Japon ?", "Capitale du Bresil ?", "Capitale de l'Egypte ?", "Capitale de la Suisse ?", "Capitale de la France ?", "Capitale du Canada ?"],
    "✈️ Avions": ["Quel est l'avion de chasse le plus performant ?", "C'est quoi le F-22 ?", "C'est quoi le 【entity-F-35¦canonical_name=F-35】 ?", "C'est quoi le Rafale ?", "C'est quoi le SR-71 ?", "C'est quoi le Concorde ?", "C'est quoi le A380 ?", "Comment vole un avion ?"],
    "💻 PC": ["C'est quoi le meilleur rapport qualite prix ?", "C'est quoi la meilleure GPU ?", "C'est quoi le meilleur CPU ?", "C'est quoi le meilleur SSD ?", "C'est quoi la meilleure RAM ?", "C'est quoi un PC gamer ?", "PC 2000 CHF", "PC 1300 CHF", "PC 900 CHF", "C'est quoi les FPS ?", "C'est quoi le ping ?"],
    "⚽ Foot / Sport": ["C'est qui 【entity-Messi¦canonical_name=Messi】 ?", "C'est qui 【entity-Ronaldo¦canonical_name=Ronaldo】 ?", "C'est qui 【entity-Mbappe¦canonical_name=Mbappe】 ?", "C'est quoi la Coupe du Monde ?", "C'est quoi la Ligue des Champions ?", "C'est quoi le Ballon d'Or ?", "C'est quoi le basket ?", "C'est quoi la Formule 1 ?"],
    "🎮 Jeux Video": ["C'est quoi 【entity-Minecraft¦canonical_name=Minecraft】 ?", "C'est quoi 【entity-Fortnite¦canonical_name=Fortnite】 ?", "C'est quoi Roblox ?", "C'est quoi GTA ?", "C'est quoi Brawl Stars ?", "C'est quoi Pokemon ?", "C'est quoi Mario ?", "C'est quoi One Piece ?"],
    "🚀 Espace": ["C'est quoi un trou noir ?", "C'est quoi le Big Bang ?", "C'est quoi Mars ?", "C'est quoi l'ISS ?", "C'est quoi le Soleil ?", "C'est quoi une galaxie ?", "C'est quoi la Lune ?"],
    "🧠 Culture G": ["C'est qui Werenoi ?", "C'est qui Ninho ?", "C'est qui Jul ?", "C'est quoi la Tour Eiffel ?", "C'est quoi le 【entity-Titanic¦canonical_name=Titanic】 ?", "C'est quoi 【entity-Harry Potter¦canonical_name=Harry Potter】 ?", "C'est quoi les pyramides ?"],
    "🎤 Chanteurs": ["C'est qui Werenoi ?", "C'est qui Ninho ?", "C'est qui Jul ?", "C'est qui Gazo ?", "C'est qui Tiakola ?", "C'est qui 【entity-PNL¦canonical_name=PNL】 ?", "C'est qui SDM ?", "C'est qui 【entity-Drake¦canonical_name=DRAKE】 ?", "C'est qui 【entity-Taylor Swift¦canonical_name=taylor swift】 ?", "C'est qui 【entity-Eminem¦canonical_name=Eminem】 ?", "C'est qui Stromae ?", "C'est qui Soprano ?"],
    "💰 Argent / Metiers": ["Comment devenir millionnaire ?", "C'est quoi un salaire ?", "C'est quoi un entrepreneur ?", "Comment gagner de l'argent a 13 ans ?", "C'est quoi un metier ?", "C'est quoi la bourse ?"],
    "🐾 Animaux": ["C'est quoi le plus grand animal ?", "C'est quoi le plus rapide ?", "C'est quoi un chien ?", "C'est quoi un chat ?", "C'est quoi un lion ?", "C'est quoi un dauphin ?"],
    "🍔 Cuisine": ["C'est quoi une recette facile ?", "C'est quoi les pates ?", "C'est quoi un gateau au chocolat ?", "C'est quoi manger sain ?"],
}

with st.sidebar:
    st.title("Agent IA V5 - ULTIME")
    st.write(f"🧠 Appris : {len(st.session_state.learned)}")
    st.write(f"🏆 Score : {st.session_state.score} / {st.session_state.total_quiz}")
    st.write(f"🔥 Streak : {st.session_state.streak} | Best : {st.session_state.best_streak}")
    st.divider()
    st.write("🚀 ACCES RAPIDE :")
    for t in ["📐 Ecole","🧠 Apprends-moi","🎲 Fun","💻 PC","✈️ Avions","🎤 Chanteurs"]:
        if st.button(t, key="side_quick_"+t, use_container_width=True):
            st.session_state.theme = t; st.session_state.matiere=None; st.session_state.genre=None; st.rerun()
    st.divider()
    st.write("📚 MATIERES :")
    for m in MATIERES_GENRES.keys():
        if st.button(m, key="side_m_"+m, use_container_width=True):
            st.session_state.theme="📐 Ecole"; st.session_state.matiere=m; st.session_state.genre=None; st.rerun()
    st.divider()
    st.write("🎯 AUTRES :")
    for t in THEMES.keys():
        if t not in ["📐 Ecole","🧠 Apprends-moi","🎲 Fun","💻 PC","✈️ Avions","🎤 Chanteurs"]:
            if st.button(t, key="side_"+t, use_container_width=True):
                st.session_state.theme=t; st.session_state.matiere=None; st.session_state.genre=None; st.rerun()
    st.divider()
    if st.button("🗑️ Effacer la conversation"):
        st.session_state.messages=[]; st.rerun()
    if st.button("🧠 Oublier ce que j'ai appris"):
        st.session_state.learned={}; st.session_state.score=0; st.session_state.total_quiz=0; st.session_state.streak=0; st.rerun()

st.title("Agent IA V5 - ULTIME 🖤")
st.caption(f"🧠 {len(st.session_state.learned)} appris | 🏆 {st.session_state.score}/{st.session_state.total_quiz} | 🔥 Streak {st.session_state.streak} | 📚 10 matières • 32 genres • 400+ questions • 85 verbes • 100+ capitales | Fond noir discret")

if st.session_state.mode_train:
    st.success(f"🎯 ENTRAINEMENT {st.session_state.niveau.upper()} {st.session_state.train_matiere or ''} - Score : {st.session_state.score}/{st.session_state.total_quiz} - 🔥 Streak : {st.session_state.streak} - Ecris 'stop' pour arreter")

if st.session_state.theme == "📐 Ecole":
    st.subheader("1️⃣ Choisis ta MATIERE :")
    cols2 = st.columns(4)
    for i, m in enumerate(list(MATIERES_GENRES.keys())):
        with cols2[i % 4]:
            sel = "✅ " if st.session_state.matiere == m else ""
            if st.button(sel + m, key="mat_"+m, use_container_width=True):
                st.session_state.matiere=m; st.session_state.genre=None; st.rerun()
    if st.session_state.matiere:
        st.subheader(f"2️⃣ Choisis ton GENRE dans {st.session_state.matiere} :")
        genres = list(MATIERES_GENRES[st.session_state.matiere].keys())
        colsG = st.columns(len(genres))
        for i, g in enumerate(genres):
            with colsG[i]:
                sel = "✅ " if st.session_state.genre == g else ""
                if st.button(sel + g, key="genre_"+g, use_container_width=True):
                    st.session_state.genre=g; st.rerun()
        if st.button(f"🎯 Entrainement {st.session_state.matiere} !", use_container_width=True):
            st.session_state.messages.append({"role":"user","content":f"Quiz {st.session_state.matiere}"})
            st.session_state.auto_q = f"Quiz {st.session_state.matiere}"; st.rerun()
    if st.session_state.matiere and st.session_state.genre:
        st.subheader(f"3️⃣ {st.session_state.matiere} → {st.session_state.genre} - Clique :")
        for q in MATIERES_GENRES[st.session_state.matiere][st.session_state.genre]:
            if st.button(q, key="q_"+q, use_container_width=True):
                st.session_state.messages.append({"role":"user","content":q}); st.session_state.auto_q=q; st.rerun()
        c1,c2 = st.columns(2)
        with c1:
            if st.button("↩️ Changer de genre", use_container_width=True):
                st.session_state.genre=None; st.rerun()
        with c2:
            if st.button("↩️ Changer de matière", use_container_width=True):
                st.session_state.matiere=None; st.session_state.genre=None; st.rerun()
    elif st.session_state.matiere:
        st.info(f"👆 Choisis un genre dans {st.session_state.matiere}")
else:
    cols = st.columns(3)
    for i, t in enumerate(list(THEMES.keys())):
        with cols[i % 3]:
            if st.button(t, key="top_"+t, use_container_width=True):
                st.session_state.theme=t; st.session_state.matiere=None; st.session_state.genre=None; st.rerun()
    if st.session_state.theme != "📐 Ecole":
        st.subheader(f"Questions {st.session_state.theme} - Clique :")
        for q in THEMES.get(st.session_state.theme, []):
            if st.button(q, key="q2_"+q, use_container_width=True):
                st.session_state.messages.append({"role":"user","content":q}); st.session_state.auto_q=q; st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant","content":"Salut ! 👋 Bienvenue dans la version ULTIME ! 🎉\n\nTu peux tout faire ici :\n📚 Choisis MATIERE → GENRE → QUESTION en haut (ex : Français → Verbes → Conjugue ETRE)\n🗣️ 85 verbes en 5 langues\n🌍 100+ capitales, PC, avions, chanteurs, foot, jeux...\n🎯 Entrainement par matière : écris 'Quiz Maths' ou 'Quiz Français'\n🧠 Apprends-moi : 'Apprends : c'est quoi le foot = ...'\n\nEssaie : Bonjour / Conjugue ETRE / C'est quoi Pythagore ? / Entraine moi"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

def nettoyer(txt):
    txt = txt.lower().strip()
    txt = txt.replace("é","e").replace("è","e").replace("ê","e").replace("à","a").replace("ç","c").replace("ô","o").replace("î","i").replace("û","u").replace("ö","o").replace("ü","u").replace("ä","a").replace("ï","i")
    txt = re.sub(r"[^a-z0-9 +*/\-=?.]", " ", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt

BASES = {
    "bonjour": "Bonjour ! 👋 Comment tu vas ? Moi je vais super bien ! Tu veux réviser quoi ? Choisis en haut : Matière → Genre → Question. Ex : Français → Verbes → Conjugue ETRE. Ou écris-moi ta question !",
    "bonsoir": "Bonsoir ! 🌙 Comment tu vas ? Tu veux réviser quelle matière avant de dormir ?",
    "salut": "Salut ! 👋 Ca va ? Choisis ta matière en haut ou pose-moi ta question !",
    "slt": "Slt ! 👋 Ca va ?",
    "yo": "Yo ! 👋 Ca va ? Tu veux réviser quoi ?",
    "coucou": "Coucou ! 👋 Ca va bien ?",
    "hello": "Hello ! 👋 Ca va ? I can help you in English too !",
    "hi": "Hi ! 👋 How are you ?",
    "merci": "De rien ! 😊 Avec plaisir ! C'est normal, je suis là pour t'aider. Tu as une autre question ? Choisis une autre matière / genre en haut !",
    "merci beaucoup": "De rien, avec grand plaisir ! 😊 Tu es trop gentil !",
    "mrc": "De rien ! 😊",
    "thx": "You're welcome ! 😊 De rien !",
    "ca va": "Ca va super bien merci ! Et toi, ca va ? Tu révises quelle matière ?",
    "cv": "Ca va super bien merci ! Et toi ? 😊",
    "comment tu vas": "Je vais super bien merci ! Et toi ? 😊",
    "au revoir": "Au revoir ! 👋 A très vite ! J'espère que je t'ai aidé ! Reviens quand tu veux, je suis là H24 ! 😊",
    "bye": "Bye ! 👋 A très vite !",
    "a plus": "A plus ! 👋 Bonne journée !",
    "bonne nuit": "Bonne nuit ! 😴 Dors bien ! A demain !",
    "bonne journee": "Bonne journée à toi aussi ! 😊 Merci !",
    "t appelles comment": "Moi je m'appelle Agent IA V5 - ULTIME ! 🤖 Et toi, tu t'appelles comment ?",
    "qui es tu": "Moi je suis Agent IA V5 ULTIME ! 🤖 Ton assistant créé par Lenny. Je connais 10 matières, 32 genres, 400+ questions, 85 verbes en 5 langues, 100+ capitales, PC, avions, chanteurs... et J'APPRENDS ce que tu m'apprends !",
    "tu peux m aider": "Oui bien sûr ! 😊 Dis-moi ta question ! Ou choisis Matière → Genre en haut !",
    "aide moi": "Oui bien sûr ! 😊 C'est pour quelle matière et quel genre ? Ex : Français → Grammaire, ou Maths → Géométrie ? Choisis en haut, ou écris ta question !",
    "j ai pas compris": "T'inquiète, c'est normal ! 😊 Dis-moi ce que tu n'as pas compris, je vais te réexpliquer plus simplement, avec un autre exemple.",
    "j ai compris": "Trop bien ! 😊 Bravo ! Tu veux que je te pose une question pour vérifier ou on passe à autre chose ?",
    "t es trop fort": "Merciii ! 😊 Ca me fait trop plaisir !",
    "trop bien": "Merciii ! 😊 Content que ça te plaise !",
    "t es nul": "Ohh... 😅 Désolé si je t'ai pas aidé ! Dis-moi ce que tu voulais, je vais essayer de mieux t'expliquer.",
    "ok": "Ok ! 😊 Tu veux quoi maintenant ? Une autre question ?",
    "lol": "Haha 😂 ! Tu es marrant !",
    "mdr": "Mdr 😂 ! Tu veux que je t'aide pour quoi ?",
    "tu as quel age": "Moi je n'ai pas d'âge, je suis un robot ! 🤖 Je suis né en 2025, grâce à Lenny ! Et toi, tu as quel âge ?",
    "t es un robot": "Oui ! 🤖 Je suis un robot, un Agent IA créé par Lenny. Je suis là pour t'aider H24 !",
    "quelle heure": f"Il est {datetime.datetime.now().strftime('%H:%M')} ! ⏰ En Suisse !",
    "quelle date": f"On est le {datetime.datetime.now().strftime('%d/%m/%Y')} ! 📅",
    "devinette": "Devinette 🧩 : Je suis toujours devant toi mais tu ne peux jamais me voir. Qui suis-je ?\n\nRéponse : Ton avenir ! 😊\n\nUne autre : Qu'est-ce qui monte mais ne descend jamais ? Réponse : Ton âge ! 😂",
    "fait moi rire": "Pourquoi les plongeurs plongent-ils toujours en arrière ? Parce que sinon, ils tombent dans le bateau ! 😂",
}

BLAGUES = ["Pourquoi les plongeurs plongent-ils toujours en arrière ? Parce que sinon, ils tombent dans le bateau ! 😂","Que dit un zéro à un huit ? Belle ceinture ! 😂","Pourquoi les maths sont tristes ? Parce qu'elles ont trop de problèmes ! 😂","Pourquoi les poissons n'aiment pas jouer au foot ? Parce qu'ils ont peur des filets ! 😂","Que fait une fraise sur un cheval ? Tagada tagada ! 🍓🐴😂","Pourquoi les squelettes ne se battent pas ? Parce qu'ils n'ont pas de tripes ! 💀😂","Comment appelle-t-on un chien qui n'a pas de pattes ? On ne l'appelle pas, on va le chercher ! 🐶😂","Que dit une imprimante à une autre ? Tu as du papier ? 😂","Pourquoi le livre de maths est déprimé ? Parce qu'il a trop de problèmes ! 😂","Que dit un chat à un autre chat ? Miaou, on joue ? 😂","Pourquoi les oiseaux volent en V ? Parce que si ils volaient en U, ce serait trop long ! 🐦😂","Quel est le comble pour un électricien ? De ne pas être au courant ! ⚡😂"]
MOTIVATIONS = ["Tu peux le faire ! 💪 Chaque erreur, c'est une leçon. Messi a été rejeté petit, il est devenu le meilleur ! Ne lâche rien !","N'abandonne jamais ! 🔥 Si c'est dur, c'est que tu es en train d'apprendre. 10 minutes par jour, tous les jours, et dans 1 mois tu seras trop fort !","Tu es capable de beaucoup plus que tu crois ! 🚀 Commence petit, 1 exercice, et ça va venir !","Le succès, c'est 1% de talent et 99% de travail ! 💪 Tu as déjà fait le plus dur : tu es venu demander de l'aide !","Rappelle-toi : Werenoi a commencé à 27 ans, Jul a été moqué au début, Eminem était pauvre. Ils n'ont jamais lâché. Toi aussi, tu peux réussir ! 🔥"]
TRADUCTIONS = {"bonjour en anglais": "Bonjour en anglais = Hello / Good morning ! 🇬🇧 Ex : Hello, how are you ? = Bonjour, comment tu vas ?","bonjour en allemand": "Bonjour en allemand = Hallo / Guten Tag ! 🇩🇪 Ex : Hallo, wie geht's ? = Salut, ça va ?","bonjour en espagnol": "Bonjour en espagnol = Hola / Buenos dias ! 🇪🇸","bonjour en italien": "Bonjour en italien = Ciao / Buongiorno ! 🇮🇹","merci en anglais": "Merci en anglais = Thank you / Thanks ! 🇬🇧","merci en allemand": "Merci en allemand = Danke ! 🇩🇪","merci en espagnol": "Merci en espagnol = Gracias ! 🇪🇸","merci en italien": "Merci en italien = Grazie ! 🇮🇹","au revoir en anglais": "Au revoir en anglais = Goodbye / Bye ! 🇬🇧","au revoir en allemand": "Au revoir en allemand = Auf Wiedersehen / Tschüss ! 🇩🇪","ecole en anglais": "Ecole en anglais = School ! 🇬🇧 Ex : I go to school = Je vais à l'école.","chat en anglais": "Chat en anglais = Cat ! 🐱 Chien = Dog 🐶","chien en anglais": "Chien en anglais = Dog ! 🐶","maison en anglais": "Maison en anglais = House ! 🏠","pomme en anglais": "Pomme en anglais = Apple ! 🍎","eau en anglais": "Eau en anglais = Water ! 💧","ecole en allemand": "Ecole en allemand = Schule ! 🇩🇪","chien en allemand": "Chien en allemand = Hund ! 🇩🇪","maison en allemand": "Maison en allemand = Haus ! 🇩🇪","pomme en allemand": "Pomme en allemand = Apfel ! 🍎","ecole en espagnol": "Ecole en espagnol = Escuela ! 🇪🇸","chien en espagnol": "Chien en espagnol = Perro ! 🇪🇸","ecole en italien": "Ecole en italien = Scuola ! 🇮🇹"}
CAPITALES = {"france": "Paris - 2,1M d'habitants, Tour Eiffel, Louvre, 330m. France = 68M d'habitants.","suisse": "Berne - Capitale de la Suisse depuis 1848. Palais fédéral. Suisse = 8,9M d'habitants, 4 langues !","allemagne": "Berlin - 3,6M d'habitants, Mur de Berlin tombé en 1989.","italie": "Rome - 2,8M d'habitants, Colisée, Vatican, Pâtes, Pizza !","espagne": "Madrid - 3,2M d'habitants, 【entity-Real Madrid¦canonical_name=Real Madrid】.","angleterre": "Londres - 9M d'habitants, Big Ben, Buckingham Palace.","japon": "Tokyo - 14M d'habitants, plus grande ville du monde ! Sushi, Manga, Anime.","usa": "Washington D.C. - Maison Blanche. New York = plus grande ville, pas la capitale !","canada": "Ottawa - Toronto = plus grande ville. 2 langues : français + anglais.","chine": "Pékin - 21M d'habitants, Grande Muraille. Chine = 1,4 milliard !","russie": "Moscou - 12M d'habitants, Place Rouge, Kremlin.","bresil": "Brasilia - Rio = plus connue, Christ Rédempteur, Carnaval.","inde": "New Delhi - Inde = 1,4 milliard, pays le plus peuplé ! Taj Mahal.","australie": "Canberra - Sydney = plus connue, Opéra. Kangourous !","egypte": "Le Caire - 21M d'habitants, Pyramides de Gizeh, Nil, Pharaons.","maroc": "Rabat - Maroc, Couscous, Marrakech.","algerie": "Alger - Algérie = plus grand pays d'Afrique !","tunisie": "Tunis - Tunisie, Carthage.","portugal": "Lisbonne - Portugal, 【entity-Cristiano Ronaldo¦canonical_name=Cristiano Ronaldo】 !","belgique": "Bruxelles - Belgique, Frites, Chocolat, Gaufres !","pays-bas": "Amsterdam - Pays-Bas, Canaux, Vélos, Tulipes.","autriche": "Vienne - Autriche, Mozart.","suede": "Stockholm - Suède, 【entity-IKEA¦canonical_name=IKEA】, 【entity-ABBA¦canonical_name=ABBA】.","norvege": "Oslo - Norvège, Fjords, 【entity-Haaland¦canonical_name=Haaland】 !","danemark": "Copenhague - Danemark, 【entity-LEGO¦canonical_name=LEGO】.","finlande": "Helsinki - Finlande, Père Noël.","pologne": "Varsovie - Pologne, 【entity-Lewandowski¦canonical_name=Lewandowski】.","grece": "Athènes - Grèce, Démocratie, Jeux Olympiques, Zeus.","turquie": "Ankara - Turquie, Istanbul = plus grande ville, 2 continents !","coree": "Séoul - Corée du Sud, K-Pop (【entity-BTS¦canonical_name=BTS】), 【entity-Samsung¦canonical_name=Samsung】.","thailande": "Bangkok - Thaïlande, Temples, Pad Thai.","vietnam": "Hanoï - Vietnam, Pho.","mexique": "Mexico - Mexique, Tacos, Aztèques."," argentine": "Buenos Aires - Argentine, Tango, 【entity-Messi¦canonical_name=Messi】.","chili": "Santiago - Chili, pays le plus long du monde, 4300 km !","perou": "Lima - Pérou, Machu Picchu, Incas.","colombie": "Bogota - Colombie, Café, 【entity-Shakira¦canonical_name=Shakira】.","kenya": "Nairobi - Kenya, Safaris, Lions.","nigeria": "Abuja - Nigeria, 220M d'habitants, plus peuplé d'Afrique !","islande": "Reykjavik - Islande, Volcans, Aurores boréales.","irlande": "Dublin - Irlande, Trèfle, Saint-Patrick.","ukraine": "Kyiv - Ukraine.","roumanie": "Bucarest - Roumanie, Dracula.","hongrie": "Budapest - Hongrie, Danube.","croatie": "Zagreb - Croatie, 【entity-Modric¦canonical_name=Modric】.","serbie": "Belgrade - Serbie, 【entity-Djokovic¦canonical_name=Djokovic】 !","bulgarie": "Sofia - Bulgarie.","israel": "Jérusalem - Ville sainte pour 3 religions.","liban": "Beyrouth - Liban, Cèdres.","irak": "Bagdad - Irak, Mésopotamie, première écriture !","iran": "Téhéran - Iran, Perse.","arabie": "Riyad - Arabie Saoudite, Pétrole.","qatar": "Doha - Qatar, Coupe du Monde 2022 !","monaco": "Monaco - 2 km2, 2ème plus petit pays ! Grand Prix F1.","luxembourg": "Luxembourg - Petit pays riche.","malte": "La Valette - Malte, petite île en Méditerranée.","andorre": "Andorre-la-Vieille - Andorre, ski !","liechtenstein": "Vaduz - Liechtenstein, 40 000 habitants.","cuba": "La Havane - Cuba, Salsa, Vieilles voitures.","mali": "Bamako - Mali, Tombouctou.","senegal": "Dakar - Sénégal, 【entity-Sadio Mané¦canonical_name=Sadio Mané】.","ghana": "Accra - Ghana, Cacao.","cameroun": "Yaoundé - Cameroun, Lions Indomptables.","madagascar": "Antananarivo - Madagascar, Lémuriens.","pakistan": "Islamabad - Pakistan, 240M d'habitants.","nepal": "Katmandou - Népal, Everest, 8848m, plus haut sommet du monde !","mongolie": "Oulan-Bator - Mongolie, Gengis Khan.","indonesie": "Jakarta - Indonésie, 270M d'habitants, 17 000 îles !","philippines": "Manille - Philippines, 7000 îles.","singapour": "Singapour - Ville-pays, la plus propre, la plus riche d'Asie !","malaisie": "Kuala Lumpur - Malaisie, Tours Petronas.","nouvelle-zelande": "Wellington - Nouvelle-Zélande, Seigneur des Anneaux, All Blacks !","costa rica": "San José - Costa Rica, Pura Vida.","panama": "Panama - Canal de Panama !","venezuela": "Caracas - Venezuela, Angel Falls, plus haute cascade (979m) !","uruguay": "Montevideo - Uruguay, 1ère Coupe du Monde 1930.","equateur": "Quito - Equateur, Galapagos, Darwin.","bolivie": "Sucre - Bolivie, Salar d'Uyuni, plus grand désert de sel !","haiti": "Port-au-Prince - Haïti.","jamaique": "Kingston - Jamaïque, Bob Marley, 【entity-Usain Bolt¦canonical_name=Usain Bolt】 !","soudan": "Khartoum - Soudan, Nil.","libye": "Tripoli - Libye, Sahara.","ethiopie": "Addis-Abeba - Ethiopie, Café né là, Lucy."}
PC = {
    "rapport qualite prix": "MEILLEUR RAPPORT QUALITE / PRIX PC 2026 : GAGNANT 1300 CHF : RTX 5070 (600) + Ryzen 7 7800X3D (350) + 32 Go (120) + SSD 1 To (70) = 1300 CHF. 1440p Ultra 180 FPS 【entity-Fortnite¦canonical_name=Fortnite】, 120 FPS GTA V. PETIT BUDGET 900 CHF : RTX 4060 + Ryzen 5 7600 = 900 CHF, 1080p 144 FPS. GROS BUDGET 2000 CHF : RTX 5070 Ti + 9800X3D = 2000 CHF, 240 FPS, 4K 120 FPS. MON CONSEIL : Prends le 1300 CHF !",
    "pc 900": "PC 900 CHF : RTX 4060 (350) + Ryzen 5 7600 (180) + 16 Go (60) + SSD 1 To (70) + Carte mère + Alim + Boîtier (240) = 900 CHF. Fortnite 144 FPS, 1080p Ultra !",
    "pc 1300": "PC 1300 CHF - MEILLEUR RAPPORT : RTX 5070 (600) + Ryzen 7 7800X3D (350) + 32 Go DDR5 (120) + SSD 1 To (70) + reste (160) = 1300 CHF. 1440p Ultra 180 FPS !",
    "pc 2000": "PC 2000 CHF : RTX 5070 Ti (850) + Ryzen 7 9800X3D (450) + 32 Go (120) + SSD 2 To (180) + Carte mère + Alim + Boîtier (400) = 2000 CHF. 240 FPS, 4K !",
    "meilleure gpu": "MEILLEURE GPU 2026 : 1. RTX 5090 - 32 Go, 4K Ultra 200 FPS, 2500 CHF. 2. RTX 5080 - 16 Go, 1200 CHF. 3. RTX 5070 Ti - 850 CHF. 4. RTX 5070 - MEILLEUR RAPPORT : 12 Go, 1440p 180 FPS, 600 CHF. 5. RTX 4060 - POUR DEBUTER : 350 CHF.",
    "gpu": "GPU = Carte Graphique. Elle calcule toutes les images de tes jeux, 60 à 240 fois par seconde. 【entity-NVIDIA¦canonical_name=NVIDIA】 = RTX, 【entity-AMD¦canonical_name=AMD】 = RX. RTX 4060 = 144 FPS en 1080p, RTX 5070 = 180 FPS en 1440p, RTX 5090 = 200 FPS en 4K.",
    "meilleur cpu": "MEILLEUR CPU 2026 : 1. Ryzen 9 9950X3D - ROI, 700 CHF. 2. Ryzen 7 9800X3D - ROI GAMING, 450 CHF. 3. Ryzen 7 7800X3D - MEILLEUR RAPPORT, 350 CHF. Le cache 3D donne +30 FPS !",
    "cpu": "CPU = Processeur, cerveau du PC. 【entity-AMD¦canonical_name=AMD】 Ryzen ou 【entity-Intel¦canonical_name=Intel】 Core. En 2026, 【entity-AMD¦canonical_name=AMD】 est devant pour les jeux grâce au cache 3D. Meilleur rapport = Ryzen 7 7800X3D.",
    "meilleur ssd": "MEILLEUR SSD : 【entity-Samsung¦canonical_name=Samsung】 990 PRO 2 To - 7450 Mo/s, Windows en 5 sec, 180 CHF. Meilleur rapport = WD Black SN850X 1 To - 70 CHF.",
    "ssd": "SSD = Disque qui stocke Windows + jeux. NVMe = le plus rapide. HDD = vieux, lent, à éviter. Avec SSD, PC démarre en 5 sec, sans SSD en 1 min.",
    "meilleure ram": "MEILLEURE RAM : 32 Go DDR5 6000 MHz CL30. Jeu + Discord + Chrome + Stream sans lag. 16 Go = minimum. 64 Go = montage pro.",
    "ram": "RAM = Mémoire vive. 16 Go = minimum. 32 Go DDR5 = parfait. 64 Go = pro.",
    "meilleur pc": "MEILLEUR PC ABSOLU : RTX 5090 + Ryzen 9 9950X3D + 32 Go + 【entity-SSD 990 PRO¦canonical_name=Samsung】 2 To = 4000 CHF, 4K Ultra 200 FPS. MEILLEUR RAPPORT = PC 1300 CHF.",
    "pc gamer": "PC GAMER : 900 CHF = RTX 4060 = 144 FPS en 1080p. 1300 CHF = RTX 5070 = 180 FPS en 1440p, LE MEILLEUR RAPPORT. 2000 CHF = RTX 5070 Ti = 240 FPS.",
    "ecran": "MEILLEUR ECRAN : 27 pouces 1440p 180Hz IPS (250 CHF) = parfait. 1080p 144Hz (150 CHF) = pas cher. 4K 240Hz OLED (800 CHF) = le top.",
    "clavier": "MEILLEUR CLAVIER : Mécanique = plus rapide. Redragon K552 (40 CHF) = mécanique pas cher, meilleur rapport. Logitech G Pro X (150 CHF) = meilleur absolu.",
    "souris": "MEILLEURE SOURIS : Logitech G Pro X Superlight 2 - 60g, sans fil, souris des pros (150 CHF). Meilleur rapport = Logitech G305 (40 CHF).",
    "fps": "FPS = Images par seconde. 30 FPS = ça lag, 60 FPS = fluide, 144 FPS = super fluide, 240 FPS = pro. Pour 【entity-Fortnite¦canonical_name=Fortnite】 compétitif, il faut 144 FPS minimum.",
    "ping": "PING = Temps de réponse internet. 10 ms = parfait, 30 ms = très bien, 100 ms = ça lag, 200 ms = injouable. Pour baisser ton ping : câble Ethernet (pas WiFi), fibre, serveur proche.",
    "stream": "STREAM : Pour streamer : PC 1300 CHF suffit, OBS Studio (gratuit), micro Blue Yeti (100 CHF), caméra Logitech C920 (70 CHF), 2 écrans. Internet : 20 Mbps en upload minimum.",
}
CHANTEURS = {
    "werenoi": "WERENOI - HISTOIRE COMPLÈTE : Vrai nom 【entity-Jeremy Bana Owona¦canonical_name=Jeremy Bana Owona】. Né en 1994 à Melun. Il a commencé le rap tard, en 2021, avec Guadalajara. Il a explosé en 2023 avec Pyramide (diamant) et Solitaire. Style : Drill mélodique, voix grave. Albums : Pyramide (2023), Pyramide 2 (2024), Diamant Noir (2025). Le plus écouté en France en 2024 et 2025 ! Sons cultes : Solitaire, Ciao, La vie de luxe, Pyramide, Diamant Noir, Pétrole avec Gazo. Décédé le 17 mai 2025 à 31 ans. Il reste une légende.",
    "ninho": "NINHO : Vrai nom William Nzobazola. Né en 1996. Le rappeur avec le plus de disques d'or et de diamant en France ! Albums : M.I.L.S, Jefe, NI. Feats : Lettre à une femme avec Niska = diamant, Bolide allemand avec SDM. Sons : Jefe, Maman ne le sait pas, No Love.",
    "jul": "JUL : Vrai nom Julien Mari. Né en 1990 à Marseille. Le plus productif : 2 albums par an ! Albums : Dans ma paranoia, La machine, C'est pas des LOL. Sons : Tchikita, JCVD, Bande organisée, 1 2 3. Il a vendu plus de 5M d'albums. Signe : la main en l'air.",
    " gazo": " GAZO : Vrai nom Ibrahima Diakite. Né en 1994 à Château Rouge, Paris. C'est lui qui a ramené la drill en France ! Albums : Drill FR, KMT, Apocalypse. Sons : Haine et Sex, Die, La Melo avec Tiakola (300M de vues !).",
    " tiakola": " TIAKOLA : Vrai nom Tiakola Diakite. Né en 1996 à Bondy, membre de 4Keus. Albums : Melo (diamant), BDLM. Sa voix mélodique est unique. Sons : La Melo, Gasolina, Meuda, Pona nini.",
    " pnl": " PNL : Duo de frères Ademo et N.O.S, de Corbeil-Essonnes. Albums : Le monde Chico, Dans la légende, Deux frères. Ils ne font presque jamais d'interviews. Style : Cloud rap, planant. Sons : Le monde ou rien, DA, Naha, Au DD.",
    "sdm": "SDM : Vrai nom Beni Mosabu. Né en 1995 à Clamart. Repéré par Booba, signé chez 92i. Albums : Ocho, A vie. Il a explosé avec Bolide allemand avec Ninho. Style : Flow rapide, technique.",
    " maes": " MAES : Rappeur de Sevran. Albums : Pure, Les derniers salopards, Omerta. Sons : Street, Dybala, Madrina avec Booba.",
    "sch": "SCH : Rappeur de Marseille. Albums : Anarchie, JVLIVS, Autobahn. Son culte : Bande organisée avec Jul, Naps, Kofs... = 400M de vues.",
    "booba": "BOOBA : Le Duc de Boulogne, légende du rap français depuis 1995 avec Lunatic. Albums : Temps mort, Ouest Side, Ultra, Trône. Il a lancé Ninho, SDM, Gazo, Damso, Maes... Sons : DKR, Mona Lisa, Ratpi World.",
    "koba la d": "KOBA LA D : Rappeur français, flow rapide, argot. Albums : VII, L'Affranchi. Sons : Train de vie, Dernier jour, Coffre plein.",
    " damso": " DAMSO : Rappeur belge / congolais. Albums : Batterie Faible, Ipseite, Lithopedion, QALF. Sons : Macarena (diamant), BruxellesVie, Feu de bois.",
    "dinos": "DINOS : Rappeur français, très technique. Albums : Imany, Taciturne, Stamina. Sons : Presque, Ciel pleure, Madone.",
    " laylow": " LAYLOW : Rappeur français, univers futuriste. Albums : Trinity, L'Etrange Histoire de Mr Anderson.",
    "nekfeu": "NEKFEU : Rappeur français, membre de 1995 et S-Crew. Albums : Feu, Cyborg, Les étoiles vagabondes. Sons : On verra, Tricheur.",
    " lacrim": " LACRIM : Rappeur français, style street. Albums : Force et Honneur, R.I.P.R.O. Sons : Corleone, Oh bah oui.",
    " drake": " DRAKE : Rappeur canadien, le plus streamé au monde. Albums : Take Care, Scorpion. Sons : God's Plan, One Dance, Hotline Bling. Il a commencé comme acteur dans Degrassi.",
    " taylor swift": " TAYLOR SWIFT : Chanteuse américaine, la plus écoutée au monde. Albums : 1989, Midnights. 14 Grammy. Fans = Swifties. Son Eras Tour = tournée la plus rentable de l'histoire (2 milliards $).",
    " weeknd": " THE WEEKND : Chanteur canadien, vrai nom Abel Tesfaye. Albums : After Hours, Starboy. Son : Blinding Lights = chanson la plus écoutée de tous les temps sur Spotify (4 milliards).",
    "bad bunny": "BAD BUNNY : Chanteur portoricain, roi du reggaeton. Album : Un Verano Sin Ti. Son : Titi Me Pregunto, Dakiti. Il a fait le Super Bowl 2026 !",
    "billie eilish": "BILLIE EILISH : Chanteuse américaine, elle a commencé à 14 ans avec Ocean Eyes. Albums : When We All Fall Asleep, Hit Me Hard and Soft. Sons : Bad Guy, Birds of a Feather. 9 Grammy avant 22 ans.",
    "ed sheeran": "ED SHEERAN : Chanteur anglais, guitare + loop. Albums : Divide, =. Sons : Shape of You, Perfect, Thinking Out Loud. Shape of You = 4 milliards de streams.",
    "rihanna": "RIHANNA : Chanteuse de la Barbade. Albums : Anti. Sons : Diamonds, Umbrella, Work. Elle a aussi sa marque Fenty (maquillage), milliardaire !",
    "beyonce": "BEYONCE : Queen B, chanteuse américaine, ex Destiny's Child. Albums : Renaissance, Lemonade. 32 Grammy, record ! Sons : Crazy In Love, Single Ladies, Halo.",
    " eminem": " EMINEM : Rappeur américain, légende. Albums : The Slim Shady LP, Recovery. Sons : Lose Yourself (Oscar), Rap God (7 mots par seconde), Mockingbird. 220M d'albums vendus.",
    "soprano": "SOPRANO : Chanteur / rappeur de Marseille. Albums : La Colombe, L'Everest, Chasseur d'étoiles. Sons : Cosmo, En feu, A la vie, a l'amour, Mon Everest. Très positif, famille, espoir.",
    "m pokora": "M. POKORA : Chanteur français, ex Popstars. Albums : R.E.D, Pyramide, Epicentre. Sons : Juste une photo de toi, Les planètes, Tombé.",
    "stromae": "STROMAE : Chanteur belge, vrai nom Paul Van Haver. Albums : Cheese, Racine carrée, Multitude. Sons : Alors on danse, Papaoutai, Formidable, L'enfer. Il mélange electro et chansons tristes.",
}

VERBES = {
    "etre": "🇫🇷 ETRE\n📌 Sens : être, décrire. Ex : Je suis content.\n✅ PRÉSENT : je suis, tu es, il est, nous sommes, vous êtes, ils sont\n✅ PASSÉ COMPOSÉ : j'ai été, tu as été, il a été, nous avons été, vous avez été, ils ont été\n✅ IMPARFAIT : j'étais, tu étais, il était, nous étions, vous étiez, ils étaient\n✅ FUTUR : je serai, tu seras, il sera, nous serons, vous serez, ils seront\n💡 Astuce : ETRE sert pour 14 verbes au passé composé (aller, venir...) : Je suis allé.",
    "avoir": "🇫🇷 AVOIR\n📌 Sens : posséder. Ex : J'ai 13 ans.\n✅ PRÉSENT : j'ai, tu as, il a, nous avons, vous avez, ils ont\n✅ PASSÉ COMPOSÉ : j'ai eu, tu as eu, il a eu, nous avons eu, vous avez eu, ils ont eu\n✅ IMPARFAIT : j'avais, tu avais, il avait, nous avions, vous aviez, ils avaient\n✅ FUTUR : j'aurai, tu auras, il aura, nous aurons, vous aurez, ils auront",
    "aller": "🇫🇷 ALLER\n📌 Sens : se déplacer. Ex : Je vais à l'école.\n✅ PRÉSENT : je vais, tu vas, il va, nous allons, vous allez, ils vont\n✅ PASSÉ COMPOSÉ : je suis allé(e), tu es allé(e), il est allé, nous sommes allés, vous êtes allés, ils sont allés\n✅ IMPARFAIT : j'allais, tu allais, il allait, nous allions, vous alliez, ils allaient\n✅ FUTUR : j'irai, tu iras, il ira, nous irons, vous irez, ils iront",
    "faire": "🇫🇷 FAIRE\n📌 Sens : créer. Ex : Je fais mes devoirs.\n✅ PRÉSENT : je fais, tu fais, il fait, nous faisons, vous faites, ils font\n✅ PASSÉ COMPOSÉ : j'ai fait, tu as fait, il a fait, nous avons fait, vous avez fait, ils ont fait\n✅ IMPARFAIT : je faisais, tu faisais, il faisait, nous faisions, vous faisiez, ils faisaient\n✅ FUTUR : je ferai, tu feras, il fera, nous ferons, vous ferez, ils feront",
    "dire": "🇫🇷 DIRE\n📌 Sens : parler. Ex : Je dis bonjour.\n✅ PRÉSENT : je dis, tu dis, il dit, nous disons, vous dites, ils disent\n✅ PASSÉ COMPOSÉ : j'ai dit, tu as dit, il a dit, nous avons dit, vous avez dit, ils ont dit\n✅ IMPARFAIT : je disais, tu disais, il disait, nous disions, vous disiez, ils disaient\n✅ FUTUR : je dirai, tu diras, il dira, nous dirons, vous direz, ils diront",
    "pouvoir": "🇫🇷 POUVOIR\n📌 Sens : être capable. Ex : Je peux jouer.\n✅ PRÉSENT : je peux, tu peux, il peut, nous pouvons, vous pouvez, ils peuvent\n✅ PASSÉ COMPOSÉ : j'ai pu, tu as pu, il a pu, nous avons pu, vous avez pu, ils ont pu\n✅ IMPARFAIT : je pouvais, tu pouvais, il pouvait, nous pouvions, vous pouviez, ils pouvaient\n✅ FUTUR : je pourrai, tu pourras, il pourra, nous pourrons, vous pourrez, ils pourront",
    "vouloir": "🇫🇷 VOULOIR\n📌 Sens : désirer. Ex : Je veux jouer.\n✅ PRÉSENT : je veux, tu veux, il veut, nous voulons, vous voulez, ils veulent\n✅ PASSÉ COMPOSÉ : j'ai voulu, tu as voulu, il a voulu, nous avons voulu, vous avez voulu, ils ont voulu\n✅ IMPARFAIT : je voulais, tu voulais, il voulait, nous voulions, vous vouliez, ils voulaient\n✅ FUTUR : je voudrai, tu voudras, il voudra, nous voudrons, vous voudrez, ils voudront",
    "savoir": "🇫🇷 SAVOIR\n📌 Sens : connaître un fait. Ex : Je sais nager.\n✅ PRÉSENT : je sais, tu sais, il sait, nous savons, vous savez, ils savent\n✅ PASSÉ COMPOSÉ : j'ai su, tu as su, il a su, nous avons su, vous avez su, ils ont su\n✅ IMPARFAIT : je savais, tu savais, il savait, nous savions, vous saviez, ils savaient\n✅ FUTUR : je saurai, tu sauras, il saura, nous saurons, vous saurez, ils sauront",
    "devoir": "🇫🇷 DEVOIR\n📌 Sens : obligation. Ex : Je dois faire mes devoirs.\n✅ PRÉSENT : je dois, tu dois, il doit, nous devons, vous devez, ils doivent\n✅ PASSÉ COMPOSÉ : j'ai dû, tu as dû, il a dû, nous avons dû, vous avez dû, ils ont dû\n✅ IMPARFAIT : je devais, tu devais, il devait, nous devions, vous deviez, ils devaient\n✅ FUTUR : je devrai, tu devras, il devra, nous devrons, vous devrez, ils devront",
    "venir": "🇫🇷 VENIR\n📌 Sens : arriver. Ex : Je viens de l'école.\n✅ PRÉSENT : je viens, tu viens, il vient, nous venons, vous venez, ils viennent\n✅ PASSÉ COMPOSÉ : je suis venu(e), tu es venu(e), il est venu, nous sommes venus, vous êtes venus, ils sont venus\n✅ IMPARFAIT : je venais, tu venais, il venait, nous venions, vous veniez, ils venaient\n✅ FUTUR : je viendrai, tu viendras, il viendra, nous viendrons, vous viendrez, ils viendront",
    "voir": "🇫🇷 VOIR\n📌 Sens : regarder. Ex : Je vois un film.\n✅ PRÉSENT : je vois, tu vois, il voit, nous voyons, vous voyez, ils voient\n✅ PASSÉ COMPOSÉ : j'ai vu, tu as vu, il a vu, nous avons vu, vous avez vu, ils ont vu\n✅ IMPARFAIT : je voyais, tu voyais, il voyait, nous voyions, vous voyiez, ils voyaient\n✅ FUTUR : je verrai, tu verras, il verra, nous verrons, vous verrez, ils verront",
    "prendre": "🇫🇷 PRENDRE\n📌 Sens : attraper. Ex : Je prends le bus.\n✅ PRÉSENT : je prends, tu prends, il prend, nous prenons, vous prenez, ils prennent\n✅ PASSÉ COMPOSÉ : j'ai pris, tu as pris, il a pris, nous avons pris, vous avez pris, ils ont pris\n✅ IMPARFAIT : je prenais, tu prenais, il prenait, nous prenions, vous preniez, ils prenaient\n✅ FUTUR : je prendrai, tu prendras, il prendra, nous prendrons, vous prendrez, ils prendront",
    "mettre": "🇫🇷 METTRE\n📌 Sens : placer. Ex : Je mets mes chaussures.\n✅ PRÉSENT : je mets, tu mets, il met, nous mettons, vous mettez, ils mettent\n✅ PASSÉ COMPOSÉ : j'ai mis, tu as mis, il a mis, nous avons mis, vous avez mis, ils ont mis\n✅ IMPARFAIT : je mettais, tu mettais, il mettait, nous mettions, vous mettiez, ils mettaient\n✅ FUTUR : je mettrai, tu mettras, il mettra, nous mettrons, vous mettrez, ils mettront",
    "donner": "🇫🇷 DONNER\n📌 Sens : offrir. Ex : Je donne un cadeau.\n✅ PRÉSENT : je donne, tu donnes, il donne, nous donnons, vous donnez, ils donnent\n✅ PASSÉ COMPOSÉ : j'ai donné, tu as donné, il a donné, nous avons donné, vous avez donné, ils ont donné\n✅ IMPARFAIT : je donnais, tu donnais, il donnait, nous donnions, vous donniez, ils donnaient\n✅ FUTUR : je donnerai, tu donneras, il donnera, nous donnerons, vous donnerez, ils donneront",
    "parler": "🇫🇷 PARLER\n📌 Sens : dire avec la voix. Ex : Je parle français.\n✅ PRÉSENT : je parle, tu parles, il parle, nous parlons, vous parlez, ils parlent\n✅ PASSÉ COMPOSÉ : j'ai parlé, tu as parlé, il a parlé, nous avons parlé, vous avez parlé, ils ont parlé\n✅ IMPARFAIT : je parlais, tu parlais, il parlait, nous parlions, vous parliez, ils parlaient\n✅ FUTUR : je parlerai, tu parleras, il parlera, nous parlerons, vous parlerez, ils parleront",
    "manger": "🇫🇷 MANGER\n📌 Sens : avaler. Ex : Je mange une pizza.\n✅ PRÉSENT : je mange, tu manges, il mange, nous mangeons, vous mangez, ils mangent\n✅ PASSÉ COMPOSÉ : j'ai mangé, tu as mangé, il a mangé, nous avons mangé, vous avez mangé, ils ont mangé\n✅ IMPARFAIT : je mangeais, tu mangeais, il mangeait, nous mangions, vous mangiez, ils mangeaient\n✅ FUTUR : je mangerai, tu mangeras, il mangera, nous mangerons, vous mangerez, ils mangeront",
    "dormir": "🇫🇷 DORMIR\n📌 Sens : être endormi. Ex : Je dors bien.\n✅ PRÉSENT : je dors, tu dors, il dort, nous dormons, vous dormez, ils dorment\n✅ PASSÉ COMPOSÉ : j'ai dormi, tu as dormi, il a dormi, nous avons dormi, vous avez dormi, ils ont dormi\n✅ IMPARFAIT : je dormais, tu dormais, il dormait, nous dormions, vous dormiez, ils dormaient\n✅ FUTUR : je dormirai, tu dormiras, il dormira, nous dormirons, vous dormirez, ils dormiront",
    "ecrire": "🇫🇷 ECRIRE\n📌 Sens : écrire. Ex : J'écris une lettre.\n✅ PRÉSENT : j'écris, tu écris, il écrit, nous écrivons, vous écrivez, ils écrivent\n✅ PASSÉ COMPOSÉ : j'ai écrit, tu as écrit, il a écrit, nous avons écrit, vous avez écrit, ils ont écrit\n✅ IMPARFAIT : j'écrivais, tu écrivais, il écrivait, nous écrivions, vous écriviez, ils écrivaient\n✅ FUTUR : j'écrirai, tu écriras, il écrira, nous écrirons, vous écrirez, ils écriront",
    "lire": "🇫🇷 LIRE\n📌 Sens : lire un livre. Ex : Je lis Harry Potter.\n✅ PRÉSENT : je lis, tu lis, il lit, nous lisons, vous lisez, ils lisent\n✅ PASSÉ COMPOSÉ : j'ai lu, tu as lu, il a lu, nous avons lu, vous avez lu, ils ont lu\n✅ IMPARFAIT : je lisais, tu lisais, il lisait, nous lisions, vous lisiez, ils lisaient\n✅ FUTUR : je lirai, tu liras, il lira, nous lirons, vous lirez, ils liront",
    "partir": "🇫🇷 PARTIR\n📌 Sens : quitter. Ex : Je pars à l'école.\n✅ PRÉSENT : je pars, tu pars, il part, nous partons, vous partez, ils partent\n✅ PASSÉ COMPOSÉ : je suis parti(e), tu es parti(e), il est parti, nous sommes partis, vous êtes partis, ils sont partis\n✅ IMPARFAIT : je partais, tu partais, il partait, nous partions, vous partiez, ils partaient\n✅ FUTUR : je partirai, tu partiras, il partira, nous partirons, vous partirez, ils partiront",
    "sortir": "🇫🇷 SORTIR\n📌 Sens : aller dehors. Ex : Je sors avec mes amis.\n✅ PRÉSENT : je sors, tu sors, il sort, nous sortons, vous sortez, ils sortent\n✅ PASSÉ COMPOSÉ : je suis sorti(e), tu es sorti(e), il est sorti...\n✅ IMPARFAIT : je sortais...\n✅ FUTUR : je sortirai...",
    "finir": "🇫🇷 FINIR\n📌 Sens : terminer. Ex : Je finis mes devoirs.\n✅ PRÉSENT : je finis, tu finis, il finit, nous finissons, vous finissez, ils finissent\n✅ PASSÉ COMPOSÉ : j'ai fini...\n✅ IMPARFAIT : je finissais...\n✅ FUTUR : je finirai...",
    "jouer": "🇫🇷 JOUER\n📌 Sens : jouer. Ex : Je joue au foot.\n✅ PRÉSENT : je joue, tu joues, il joue, nous jouons, vous jouez, ils jouent\n✅ PASSÉ COMPOSÉ : j'ai joué...\n✅ IMPARFAIT : je jouais...\n✅ FUTUR : je jouerai...",
    "travailler": "🇫🇷 TRAVAILLER\n📌 Sens : travailler. Ex : Je travaille bien.\n✅ PRÉSENT : je travaille, tu travailles, il travaille, nous travaillons, vous travaillez, ils travaillent\n✅ PASSÉ COMPOSÉ : j'ai travaillé...\n✅ IMPARFAIT : je travaillais...\n✅ FUTUR : je travaillerai...",
    "apprendre": "🇫🇷 APPRENDRE\n📌 Sens : apprendre. Ex : J'apprends l'allemand.\n✅ PRÉSENT : j'apprends, tu apprends, il apprend, nous apprenons, vous apprenez, ils apprennent\n✅ PASSÉ COMPOSÉ : j'ai appris...\n✅ IMPARFAIT : j'apprenais...\n✅ FUTUR : j'apprendrai...",
    "sein": "🇩🇪 SEIN (= ÊTRE)\n📌 Sens : être. Ex : Ich bin 13 Jahre alt = J'ai 13 ans.\n✅ PRÄSENS : ich bin, du bist, er ist, wir sind, ihr seid, sie sind\n✅ PERFEKT : ich bin gewesen...\n✅ PRÄTERITUM : ich war, du warst, er war, wir waren, ihr wart, sie waren\n✅ FUTUR : ich werde sein...",
    "haben": "🇩🇪 HABEN (= AVOIR)\n📌 Sens : avoir. Ex : Ich habe einen Hund = J'ai un chien.\n✅ PRÄSENS : ich habe, du hast, er hat, wir haben, ihr habt, sie haben\n✅ PERFEKT : ich habe gehabt...\n✅ PRÄTERITUM : ich hatte...\n✅ FUTUR : ich werde haben...",
    "gehen": "🇩🇪 GEHEN (= ALLER)\n📌 Sens : aller. Ex : Ich gehe zur Schule.\n✅ PRÄSENS : ich gehe, du gehst, er geht, wir gehen, ihr geht, sie gehen\n✅ PERFEKT : ich bin gegangen...\n✅ PRÄTERITUM : ich ging...\n✅ FUTUR : ich werde gehen...",
    "machen": "🇩🇪 MACHEN (= FAIRE)\n📌 Sens : faire. Ex : Ich mache meine Hausaufgaben.\n✅ PRÄSENS : ich mache, du machst, er macht, wir machen, ihr macht, sie machen\n✅ PERFEKT : ich habe gemacht...\n✅ PRÄTERITUM : ich machte...\n✅ FUTUR : ich werde machen...",
    "kommen": "🇩🇪 KOMMEN (= VENIR)\n📌 Sens : venir. Ex : Ich komme aus der Schweiz.\n✅ PRÄSENS : ich komme, du kommst, er kommt, wir kommen, ihr kommt, sie kommen\n✅ PERFEKT : ich bin gekommen...\n✅ PRÄTERITUM : ich kam...\n✅ FUTUR : ich werde kommen...",
    "sehen": "🇩🇪 SEHEN (= VOIR)\n📌 Sens : voir. Ex : Ich sehe einen Film.\n✅ PRÄSENS : ich sehe, du siehst, er sieht, wir sehen, ihr seht, sie sehen\n✅ PERFEKT : ich habe gesehen...\n✅ PRÄTERITUM : ich sah...\n✅ FUTUR : ich werde sehen...",
    "sprechen": "🇩🇪 SPRECHEN (= PARLER)\n📌 Sens : parler. Ex : Ich spreche Deutsch.\n✅ PRÄSENS : ich spreche, du sprichst, er spricht, wir sprechen, ihr sprecht, sie sprechen\n✅ PERFEKT : ich habe gesprochen...\n✅ PRÄTERITUM : ich sprach...\n✅ FUTUR : ich werde sprechen...",
    "essen": "🇩🇪 ESSEN (= MANGER)\n📌 Sens : manger. Ex : Ich esse Pizza.\n✅ PRÄSENS : ich esse, du isst, er isst, wir essen, ihr esst, sie essen\n✅ PERFEKT : ich habe gegessen...\n✅ PRÄTERITUM : ich aß...\n✅ FUTUR : ich werde essen...",
    "trinken": "🇩🇪 TRINKEN (= BOIRE)\n📌 Sens : boire. Ex : Ich trinke Wasser.\n✅ PRÄSENS : ich trinke, du trinkst, er trinkt, wir trinken, ihr trinkt, sie trinken\n✅ PERFEKT : ich habe getrunken...\n✅ PRÄTERITUM : ich trank...\n✅ FUTUR : ich werde trinken...",
    "lernen": "🇩🇪 LERNEN (= APPRENDRE)\n📌 Sens : apprendre. Ex : Ich lerne Deutsch.\n✅ PRÄSENS : ich lerne, du lernst, er lernt, wir lernen, ihr lernt, sie lernen\n✅ PERFEKT : ich habe gelernt...\n✅ PRÄTERITUM : ich lernte...\n✅ FUTUR : ich werde lernen...",
    "wohnen": "🇩🇪 WOHNEN (= HABITER)\n📌 Sens : habiter. Ex : Ich wohne in Estavayer.\n✅ PRÄSENS : ich wohne, du wohnst, er wohnt, wir wohnen, ihr wohnt, sie wohnen\n✅ PERFEKT : ich habe gewohnt...\n✅ PRÄTERITUM : ich wohnte...\n✅ FUTUR : ich werde wohnen...",
    "spielen": "🇩🇪 SPIELEN (= JOUER)\n📌 Sens : jouer. Ex : Ich spiele Fussball.\n✅ PRÄSENS : ich spiele, du spielst, er spielt, wir spielen, ihr spielt, sie spielen\n✅ PERFEKT : ich habe gespielt...\n✅ PRÄTERITUM : ich spielte...\n✅ FUTUR : ich werde spielen...",
    "arbeiten": "🇩🇪 ARBEITEN (= TRAVAILLER)\n📌 Sens : travailler. Ex : Ich arbeite viel.\n✅ PRÄSENS : ich arbeite, du arbeitest, er arbeitet, wir arbeiten, ihr arbeitet, sie arbeiten\n✅ PERFEKT : ich habe gearbeitet...\n✅ PRÄTERITUM : ich arbeitete...\n✅ FUTUR : ich werde arbeiten...",
    "konnen": "🇩🇪 KÖNNEN (= POUVOIR)\n📌 Sens : pouvoir. Ex : Ich kann schwimmen.\n✅ PRÄSENS : ich kann, du kannst, er kann, wir können, ihr könnt, sie können\n✅ PERFEKT : ich habe gekonnt...\n✅ PRÄTERITUM : ich konnte...\n✅ FUTUR : ich werde können...",
    "wollen": "🇩🇪 WOLLEN (= VOULOIR)\n📌 Sens : vouloir. Ex : Ich will spielen.\n✅ PRÄSENS : ich will, du willst, er will, wir wollen, ihr wollt, sie wollen\n✅ PERFEKT : ich habe gewollt...\n✅ PRÄTERITUM : ich wollte...\n✅ FUTUR : ich werde wollen...",
    "mussen": "🇩🇪 MÜSSEN (= DEVOIR)\n📌 Sens : devoir. Ex : Ich muss lernen.\n✅ PRÄSENS : ich muss, du musst, er muss, wir müssen, ihr müsst, sie müssen\n✅ PERFEKT : ich habe gemusst...\n✅ PRÄTERITUM : ich musste...\n✅ FUTUR : ich werde müssen...",
    "wissen": "🇩🇪 WISSEN (= SAVOIR)\n📌 Sens : savoir. Ex : Ich weiß das.\n✅ PRÄSENS : ich weiß, du weißt, er weiß, wir wissen, ihr wisst, sie wissen\n✅ PERFEKT : ich habe gewusst...\n✅ PRÄTERITUM : ich wusste...\n✅ FUTUR : ich werde wissen...",
    "geben": "🇩🇪 GEBEN (= DONNER)\n📌 Sens : donner. Ex : Ich gebe dir ein Buch.\n✅ PRÄSENS : ich gebe, du gibst, er gibt, wir geben, ihr gebt, sie geben\n✅ PERFEKT : ich habe gegeben...\n✅ PRÄTERITUM : ich gab...\n✅ FUTUR : ich werde geben...",
    "nehmen": "🇩🇪 NEHMEN (= PRENDRE)\n📌 Sens : prendre. Ex : Ich nehme den Bus.\n✅ PRÄSENS : ich nehme, du nimmst, er nimmt, wir nehmen, ihr nehmt, sie nehmen\n✅ PERFEKT : ich habe genommen...\n✅ PRÄTERITUM : ich nahm...\n✅ FUTUR : ich werde nehmen...",
    "schreiben": "🇩🇪 SCHREIBEN (= ECRIRE)\n📌 Sens : écrire. Ex : Ich schreibe einen Brief.\n✅ PRÄSENS : ich schreibe, du schreibst, er schreibt, wir schreiben, ihr schreibt, sie schreiben\n✅ PERFEKT : ich habe geschrieben...\n✅ PRÄTERITUM : ich schrieb...\n✅ FUTUR : ich werde schreiben...",
    "lesen": "🇩🇪 LESEN (= LIRE)\n📌 Sens : lire. Ex : Ich lese Harry Potter.\n✅ PRÄSENS : ich lese, du liest, er liest, wir lesen, ihr lest, sie lesen\n✅ PERFEKT : ich habe gelesen...\n✅ PRÄTERITUM : ich las...\n✅ FUTUR : ich werde lesen...",
    "fahren": "🇩🇪 FAHREN (= ALLER EN VEHICULE / CONDUIRE)\n📌 Sens : conduire, aller en voiture / vélo. Ex : Ich fahre mit dem Velo.\n✅ PRÄSENS : ich fahre, du fährst, er fährt, wir fahren, ihr fahrt, sie fahren\n✅ PERFEKT : ich bin gefahren...\n✅ PRÄTERITUM : ich fuhr...\n✅ FUTUR : ich werde fahren...",
    "schlafen": "🇩🇪 SCHLAFEN (= DORMIR)\n📌 Sens : dormir. Ex : Ich schlafe gut.\n✅ PRÄSENS : ich schlafe, du schläfst, er schläft, wir schlafen, ihr schlaft, sie schlafen\n✅ PERFEKT : ich habe geschlafen...\n✅ PRÄTERITUM : ich schlief...\n✅ FUTUR : ich werde schlafen...",
    "to be": "🇬🇧 TO BE (= ÊTRE)\n📌 Sens : être. Ex : I am happy.\n✅ PRESENT : I am, You are, He is, We are, You are, They are\n✅ PAST : I was, You were, He was, We were, You were, They were\n✅ PRESENT PERFECT : I have been...\n✅ FUTURE : I will be...",
    "to have": "🇬🇧 TO HAVE (= AVOIR)\n📌 Sens : avoir. Ex : I have a dog.\n✅ PRESENT : I have, You have, He has, We have, You have, They have\n✅ PAST : I had...\n✅ PRESENT PERFECT : I have had...\n✅ FUTURE : I will have...",
    "to go": "🇬🇧 TO GO (= ALLER)\n📌 Sens : aller. Ex : I go to school.\n✅ PRESENT : I go, You go, He goes, We go, You go, They go\n✅ PAST : I went...\n✅ PRESENT PERFECT : I have gone...\n✅ FUTURE : I will go...",
    "to do": "🇬🇧 TO DO (= FAIRE)\n📌 Sens : faire. Ex : I do my homework.\n✅ PRESENT : I do, You do, He does, We do, You do, They do\n✅ PAST : I did...\n✅ PRESENT PERFECT : I have done...\n✅ FUTURE : I will do...",
    "to say": "🇬🇧 TO SAY (= DIRE)\n📌 Sens : dire. Ex : I say hello.\n✅ PRESENT : I say, You say, He says, We say, You say, They say\n✅ PAST : I said...\n✅ PRESENT PERFECT : I have said...\n✅ FUTURE : I will say...",
    "to see": "🇬🇧 TO SEE (= VOIR)\n📌 Sens : voir. Ex : I see a film.\n✅ PRESENT : I see, You see, He sees, We see, You see, They see\n✅ PAST : I saw...\n✅ PRESENT PERFECT : I have seen...\n✅ FUTURE : I will see...",
    "to come": "🇬🇧 TO COME (= VENIR)\n📌 Sens : venir. Ex : I come from Switzerland.\n✅ PRESENT : I come, You come, He comes, We come...\n✅ PAST : I came...\n✅ PRESENT PERFECT : I have come...\n✅ FUTURE : I will come...",
    "to get": "🇬🇧 TO GET (= OBTENIR / DEVENIR)\n📌 Sens : obtenir. Ex : I get up = Je me lève.\n✅ PRESENT : I get, You get, He gets...\n✅ PAST : I got...\n✅ PRESENT PERFECT : I have got...\n✅ FUTURE : I will get...",
    "to make": "🇬🇧 TO MAKE (= FABRIQUER)\n📌 Sens : fabriquer. Ex : I make a cake.\n✅ PRESENT : I make, You make, He makes...\n✅ PAST : I made...\n✅ PRESENT PERFECT : I have made...\n✅ FUTURE : I will make...",
    "to take": "🇬🇧 TO TAKE (= PRENDRE)\n📌 Sens : prendre. Ex : I take the bus.\n✅ PRESENT : I take, You take, He takes...\n✅ PAST : I took...\n✅ PRESENT PERFECT : I have taken...\n✅ FUTURE : I will take...",
    "to give": "🇬🇧 TO GIVE (= DONNER)\n📌 Sens : donner. Ex : I give a gift.\n✅ PRESENT : I give, You give, He gives...\n✅ PAST : I gave...\n✅ PRESENT PERFECT : I have given...\n✅ FUTURE : I will give...",
    "to know": "🇬🇧 TO KNOW (= SAVOIR)\n📌 Sens : savoir. Ex : I know you.\n✅ PRESENT : I know, You know, He knows...\n✅ PAST : I knew...\n✅ PRESENT PERFECT : I have known...\n✅ FUTURE : I will know...",
    "to think": "🇬🇧 TO THINK (= PENSER)\n📌 Sens : penser. Ex : I think it's cool.\n✅ PRESENT : I think, You think, He thinks...\n✅ PAST : I thought...\n✅ PRESENT PERFECT : I have thought...\n✅ FUTURE : I will think...",
    "to speak": "🇬🇧 TO SPEAK (= PARLER)\n📌 Sens : parler. Ex : I speak English.\n✅ PRESENT : I speak, You speak, He speaks...\n✅ PAST : I spoke...\n✅ PRESENT PERFECT : I have spoken...\n✅ FUTURE : I will speak...",
    "to eat": "🇬🇧 TO EAT (= MANGER)\n📌 Sens : manger. Ex : I eat pizza.\n✅ PRESENT : I eat, You eat, He eats...\n✅ PAST : I ate...\n✅ PRESENT PERFECT : I have eaten...\n✅ FUTURE : I will eat...",
    "to drink": "🇬🇧 TO DRINK (= BOIRE)\n📌 Sens : boire. Ex : I drink water.\n✅ PRESENT : I drink, You drink, He drinks...\n✅ PAST : I drank...\n✅ PRESENT PERFECT : I have drunk...\n✅ FUTURE : I will drink...",
    "to play": "🇬🇧 TO PLAY (= JOUER)\n📌 Sens : jouer. Ex : I play football.\n✅ PRESENT : I play, You play, He plays...\n✅ PAST : I played...\n✅ PRESENT PERFECT : I have played...\n✅ FUTURE : I will play...",
    "to live": "🇬🇧 TO LIVE (= VIVRE / HABITER)\n📌 Sens : vivre. Ex : I live in Switzerland.\n✅ PRESENT : I live, You live, He lives...\n✅ PAST : I lived...\n✅ PRESENT PERFECT : I have lived...\n✅ FUTURE : I will live...",
    "to love": "🇬🇧 TO LOVE (= AIMER)\n📌 Sens : aimer. Ex : I love football.\n✅ PRESENT : I love, You love, He loves...\n✅ PAST : I loved...\n✅ PRESENT PERFECT : I have loved...\n✅ FUTURE : I will love...",
    "to want": "🇬🇧 TO WANT (= VOULOIR)\n📌 Sens : vouloir. Ex : I want to play.\n✅ PRESENT : I want, You want, He wants...\n✅ PAST : I wanted...\n✅ PRESENT PERFECT : I have wanted...\n✅ FUTURE : I will want...",
    "to work": "🇬🇧 TO WORK (= TRAVAILLER)\n📌 Sens : travailler. Ex : I work hard.\n✅ PRESENT : I work, You work, He works...\n✅ PAST : I worked...\n✅ PRESENT PERFECT : I have worked...\n✅ FUTURE : I will work...",
    "to learn": "🇬🇧 TO LEARN (= APPRENDRE)\n📌 Sens : apprendre. Ex : I learn German.\n✅ PRESENT : I learn, You learn, He learns...\n✅ PAST : I learnt / learned...\n✅ PRESENT PERFECT : I have learnt...\n✅ FUTURE : I will learn...",
    "to read": "🇬🇧 TO READ (= LIRE)\n📌 Sens : lire. Ex : I read Harry Potter.\n✅ PRESENT : I read, You read, He reads...\n✅ PAST : I read (prononcé red)...\n✅ PRESENT PERFECT : I have read...\n✅ FUTURE : I will read...",
    "to write": "🇬🇧 TO WRITE (= ECRIRE)\n📌 Sens : écrire. Ex : I write a letter.\n✅ PRESENT : I write, You write, He writes...\n✅ PAST : I wrote...\n✅ PRESENT PERFECT : I have written...\n✅ FUTURE : I will write...",
    "ser": "🇪🇸 SER (= ÊTRE - identité)\n📌 Sens : être permanent. Ex : Soy de Suiza.\n✅ PRESENTE : yo soy, tú eres, él es, nosotros somos, vosotros sois, ellos son\n✅ PRETÉRITO : yo fui, tú fuiste, él fue, nosotros fuimos, vosotros fuisteis, ellos fueron\n✅ IMPERFECTO : yo era, tú eras, él era, nosotros éramos, vosotros erais, ellos eran\n✅ FUTURO : yo seré, tú serás, él será...",
    "estar": "🇪🇸 ESTAR (= ÊTRE - état / lieu)\n📌 Sens : être temporaire. Ex : Estoy en casa.\n✅ PRESENTE : yo estoy, tú estás, él está, nosotros estamos, vosotros estáis, ellos están\n✅ PRETÉRITO : yo estuve...\n✅ IMPERFECTO : yo estaba...\n✅ FUTURO : yo estaré...",
    "tener": "🇪🇸 TENER (= AVOIR)\n📌 Sens : avoir. Ex : Tengo 13 años.\n✅ PRESENTE : yo tengo, tú tienes, él tiene, nosotros tenemos, vosotros tenéis, ellos tienen\n✅ PRETÉRITO : yo tuve...\n✅ IMPERFECTO : yo tenía...\n✅ FUTURO : yo tendré...",
    "ir": "🇪🇸 IR (= ALLER)\n📌 Sens : aller. Ex : Voy a la escuela.\n✅ PRESENTE : yo voy, tú vas, él va, nosotros vamos, vosotros vais, ellos van\n✅ PRETÉRITO : yo fui...\n✅ IMPERFECTO : yo iba...\n✅ FUTURO : yo iré...",
    "hacer": "🇪🇸 HACER (= FAIRE)\n📌 Sens : faire. Ex : Hago mis deberes.\n✅ PRESENTE : yo hago, tú haces, él hace, nosotros hacemos, vosotros hacéis, ellos hacen\n✅ PRETÉRITO : yo hice...\n✅ IMPERFECTO : yo hacía...\n✅ FUTURO : yo haré...",
    "decir": "🇪🇸 DECIR (= DIRE)\n📌 Sens : dire. Ex : Digo hola.\n✅ PRESENTE : yo digo, tú dices, él dice, nosotros decimos, vosotros decís, ellos dicen\n✅ PRETÉRITO : yo dije...\n✅ IMPERFECTO : yo decía...\n✅ FUTURO : yo diré...",
    "poder": "🇪🇸 PODER (= POUVOIR)\n📌 Sens : pouvoir. Ex : Puedo jugar.\n✅ PRESENTE : yo puedo, tú puedes, él puede, nosotros podemos, vosotros podéis, ellos pueden\n✅ PRETÉRITO : yo pude...\n✅ IMPERFECTO : yo podía...\n✅ FUTURO : yo podré...",
    "querer": "🇪🇸 QUERER (= VOULOIR)\n📌 Sens : vouloir. Ex : Quiero jugar.\n✅ PRESENTE : yo quiero, tú quieres, él quiere, nosotros queremos, vosotros queréis, ellos quieren\n✅ PRETÉRITO : yo quise...\n✅ IMPERFECTO : yo quería...\n✅ FUTURO : yo querré...",
    "saber": "🇪🇸 SABER (= SAVOIR)\n📌 Sens : savoir. Ex : Sé nadar.\n✅ PRESENTE : yo sé, tú sabes, él sabe, nosotros sabemos, vosotros sabéis, ellos saben\n✅ PRETÉRITO : yo supe...\n✅ IMPERFECTO : yo sabía...\n✅ FUTURO : yo sabré...",
    "hablar": "🇪🇸 HABLAR (= PARLER)\n📌 Sens : parler. Ex : Hablo español.\n✅ PRESENTE : yo hablo, tú hablas, él habla, nosotros hablamos, vosotros habláis, ellos hablan\n✅ PRETÉRITO : yo hablé...\n✅ IMPERFECTO : yo hablaba...\n✅ FUTURO : yo hablaré...",
    "comer": "🇪🇸 COMER (= MANGER)\n📌 Sens : manger. Ex : Como pizza.\n✅ PRESENTE : yo como, tú comes, él come, nosotros comemos, vosotros coméis, ellos comen\n✅ PRETÉRITO : yo comí...\n✅ IMPERFECTO : yo comía...\n✅ FUTURO : yo comeré...",
    "vivir": "🇪🇸 VIVIR (= VIVRE)\n📌 Sens : vivre. Ex : Vivo en Suiza.\n✅ PRESENTE : yo vivo, tú vives, él vive, nosotros vivimos, vosotros vivís, ellos viven\n✅ PRETÉRITO : yo viví...\n✅ IMPERFECTO : yo vivía...\n✅ FUTURO : yo viviré...",
    "jugar": "🇪🇸 JUGAR (= JOUER)\n📌 Sens : jouer. Ex : Juego al fútbol.\n✅ PRESENTE : yo juego, tú juegas, él juega, nosotros jugamos, vosotros jugáis, ellos juegan\n✅ PRETÉRITO : yo jugué...\n✅ IMPERFECTO : yo jugaba...\n✅ FUTURO : yo jugaré...",
    "essere": "🇮🇹 ESSERE (= ÊTRE)\n📌 Sens : être. Ex : Sono contento.\n✅ PRESENTE : io sono, tu sei, lui è, noi siamo, voi siete, loro sono\n✅ PASSATO : io sono stato...\n✅ IMPERFETTO : io ero, tu eri, lui era, noi eravamo, voi eravate, loro erano\n✅ FUTURO : io sarò, tu sarai, lui sarà...",
    "avere": "🇮🇹 AVERE (= AVOIR)\n📌 Sens : avoir. Ex : Ho 13 anni.\n✅ PRESENTE : io ho, tu hai, lui ha, noi abbiamo, voi avete, loro hanno\n✅ PASSATO : io ho avuto...\n✅ IMPERFETTO : io avevo...\n✅ FUTURO : io avrò...",
    "andare": "🇮🇹 ANDARE (= ALLER)\n📌 Sens : aller. Ex : Vado a scuola.\n✅ PRESENTE : io vado, tu vai, lui va, noi andiamo, voi andate, loro vanno\n✅ PASSATO : io sono andato...\n✅ IMPERFETTO : io andavo...\n✅ FUTURO : io andrò...",
    "fare": "🇮🇹 FARE (= FAIRE)\n📌 Sens : faire. Ex : Faccio i compiti.\n✅ PRESENTE : io faccio, tu fai, lui fa, noi facciamo, voi fate, loro fanno\n✅ PASSATO : io ho fatto...\n✅ IMPERFETTO : io facevo...\n✅ FUTURO : io farò...",
    "potere": "🇮🇹 POTERE (= POUVOIR)\n📌 Sens : pouvoir. Ex : Posso giocare.\n✅ PRESENTE : io posso, tu puoi, lui può, noi possiamo, voi potete, loro possono\n✅ PASSATO : io ho potuto...\n✅ IMPERFETTO : io potevo...\n✅ FUTURO : io potrò...",
    "volere": "🇮🇹 VOLERE (= VOULOIR)\n📌 Sens : vouloir. Ex : Voglio giocare.\n✅ PRESENTE : io voglio, tu vuoi, lui vuole, noi vogliamo, voi volete, loro vogliono\n✅ PASSATO : io ho voluto...\n✅ IMPERFETTO : io volevo...\n✅ FUTURO : io vorrò...",
    "sapere": "🇮🇹 SAPERE (= SAVOIR)\n📌 Sens : savoir. Ex : So nuotare.\n✅ PRESENTE : io so, tu sai, lui sa, noi sappiamo, voi sapete, loro sanno\n✅ PASSATO : io ho saputo...\n✅ IMPERFETTO : io sapevo...\n✅ FUTURO : io saprò...",
    "venire": "🇮🇹 VENIRE (= VENIR)\n📌 Sens : venir. Ex : Vengo dalla Svizzera.\n✅ PRESENTE : io vengo, tu vieni, lui viene, noi veniamo, voi venite, loro vengono\n✅ PASSATO : io sono venuto...\n✅ IMPERFETTO : io venivo...\n✅ FUTURO : io verrò...",
    "vedere": "🇮🇹 VEDERE (= VOIR)\n📌 Sens : voir. Ex : Vedo un film.\n✅ PRESENTE : io vedo, tu vedi, lui vede, noi vediamo, voi vedete, loro vedono\n✅ PASSATO : io ho visto...\n✅ IMPERFETTO : io vedevo...\n✅ FUTURO : io vedrò...",
    "parlare": "🇮🇹 PARLARE (= PARLER)\n📌 Sens : parler. Ex : Parlo italiano.\n✅ PRESENTE : io parlo, tu parli, lui parla, noi parliamo, voi parlate, loro parlano\n✅ PASSATO : io ho parlato...\n✅ IMPERFETTO : io parlavo...\n✅ FUTURO : io parlerò...",
    "mangiare": "🇮🇹 MANGIARE (= MANGER)\n📌 Sens : manger. Ex : Mangio la pizza.\n✅ PRESENTE : io mangio, tu mangi, lui mangia, noi mangiamo, voi mangiate, loro mangiano\n✅ PASSATO : io ho mangiato...\n✅ IMPERFETTO : io mangiavo...\n✅ FUTURO : io mangerò...",
    "giocare": "🇮🇹 GIOCARE (= JOUER)\n📌 Sens : jouer. Ex : Gioco a calcio.\n✅ PRESENTE : io gioco, tu giochi, lui gioca, noi giochiamo, voi giocate, loro giocano\n✅ PASSATO : io ho giocato...\n✅ IMPERFETTO : io giocavo...\n✅ FUTURO : io giocherò...",
}

TOUT = {
    "pythagore": "THEOREME DE PYTHAGORE - COURS COMPLET : Formule : a² + b² = c². UNIQUEMENT pour un triangle rectangle. a et b = les 2 petits côtés, c = l'hypoténuse. Ex : 3-4-5 car 9+16=25. Ex pour trouver l'hypoténuse : Si a=6, b=8, alors c² = 36+64=100, donc c=10. Ex pour trouver un petit côté : Si c=13, b=5, alors a² = 169-25=144, donc a=12. A quoi ça sert ? Construire une maison, vérifier un angle droit, calculer une distance.",
    "thales": "THALES : Si 2 droites parallèles coupent 2 sécantes, rapports égaux. Formule : AB / AD = AC / AE = BC / DE. Ex : pour calculer la hauteur d'un arbre avec son ombre.",
    "moyenne": "MOYENNE : Moyenne = somme / nombre. Ex : Notes 12, 15, 18. Somme = 45. Nombre = 3. Moyenne = 45 / 3 = 15.",
    "aire": "AIRE : Rectangle = L x l, Carré = côté x côté, Triangle = (base x hauteur) / 2, Cercle = pi x rayon² (pi = 3,14). Ex : Cercle rayon 5 = 3,14 x 25 = 78,5 cm².",
    "perimetre": "PERIMETRE : Carré = 4 x côté, Rectangle = 2 x (L+l), Cercle = 2 x pi x rayon, Triangle = somme des 3 côtés.",
    "volume": "VOLUME : Cube = côté³, Pavé = L x l x h, Cylindre = pi x r² x h. Ex : Boîte 2x3x4 = 24 cm³.",
    "angle": "ANGLES : Droit = 90°, Plat = 180°, Plein = 360°. Triangle = 180° au total. Ex : Si un triangle a 90° et 60°, le 3ème = 30°.",
    "triangle": "TRIANGLE : 3 côtés, 3 angles, somme = 180°. Types : Equilatéral (3 côtés égaux), Isocèle (2 côtés égaux), Rectangle (1 angle droit), Scalène (3 côtés différents). Aire = (base x hauteur) / 2.",
    "cercle": "CERCLE : Centre, rayon, diamètre = 2 x rayon. Périmètre = 2 x pi x rayon. Aire = pi x rayon². Pi = 3,14.",
    "fraction": "FRACTION : 1/2 = la moitié, 1/4 = le quart. Pour additionner : même dénominateur. 1/2 + 1/4 = 2/4 + 1/4 = 3/4. Pour multiplier : 2/3 x 3/4 = 6/12 = 1/2.",
    "pourcentage": "POURCENTAGE : Pourcentage = pour 100. Formule : (partie / total) x 100. Ex : 20% de 50 = 10. Ex : Tu as 15/20 : (15/20) x 100 = 75%. Soldes : -30% sur 100 CHF = 70 CHF.",
    "equation": "EQUATION : 2x + 3 = 7. Tu enlèves 3 : 2x = 4. Tu divises par 2 : x = 2. Vérif : 2x2+3 = 7, ça marche !",
    "nombre decimal": "NOMBRE DECIMAL : Nombre avec virgule. Ex : 1,5 = 1 + 0,5. 0,5 = 1/2. 0,25 = 1/4. 0,1 = 1/10.",
    "proportionnalité": "PROPORTIONNALITÉ : Si tu achètes 1 croissant = 2 CHF, 3 croissants = 6 CHF. C'est proportionnel. Tableau de proportionnalité : tu multiplies / divises par le même nombre. Produit en croix : 2/1 = x/3 -> x = 6.",
    "racine carrée": "RACINE CARRÉE : √9 = 3 car 3x3 = 9. √16 = 4. √25 = 5. √100 = 10. La racine carrée, c'est l'inverse du carré.",
    "division": "DIVISION : Division = partage. Ex : 12 / 3 = 4. 12 = dividende, 3 = diviseur, 4 = quotient. Reste : 13 / 4 = 3 reste 1 car 3x4=12, 13-12=1.",
    "cod": "COD - GRAMMAIRE : COD = Complément d'Objet Direct. Il répond à Qui ? ou Quoi ? après le verbe, sans préposition. Ex : Je mange une pomme. Je mange quoi ? Une pomme = COD. Astuce : remplace par le, la, les : Je la mange.",
    "coi": "COI - GRAMMAIRE : COI = Complément d'Objet Indirect. Il répond à A qui ? A quoi ? De qui ? De quoi ? Avec préposition à / de. Ex : Je parle à Lenny. Je parle à qui ? A Lenny = COI. Je pense à mes vacances.",
    "sujet": "SUJET : Le sujet, c'est qui fait l'action. Il répond à Qui est-ce qui ? Ex : Lenny mange. Qui mange ? Lenny = sujet.",
    "adjectif": "ADJECTIF : Il décrit un nom, il s'accorde en genre et nombre. Ex : grand garçon / grande fille / grands garçons / grandes filles. Beau -> belle, blanc -> blanche.",
    "pluriel": "PLURIEL : En général +s : chat -> chats. En -eau : bateau -> bateaux. En -al : cheval -> chevaux. En -ou : genou -> genoux, mais trou -> trous.",
    "verbe": "VERBE : C'est l'action dans la phrase. Ex : Je mange, Tu cours, Il dort. Il se conjugue avec le temps : présent, passé, futur.",
    "pronom": "PRONOM : Il remplace un nom. Ex : Lenny mange. Il mange. Je, tu, il, elle, nous, vous, ils, elles, le, la, les, lui, leur...",
    "complement circonstanciel": "COMPLÉMENT CIRCONSTANCIEL : Il dit où, quand, comment, pourquoi. Ex : Je vais à l'école (où ?). Hier, je suis allé au foot (quand ?). Je mange vite (comment ?). Il répond à Où ? Quand ? Comment ? Pourquoi ?",
    "a / a": "A / À : a = verbe avoir (Il a 13 ans). à = préposition (Je vais à l'école). Astuce : remplace par avait : Il avait 13 ans = a.",
    "et / est": "ET / EST : et = liaison (Lenny et Hugo). est = verbe être (Il est gentil). Astuce : remplace par était : Il était gentil = est.",
    "son / sont": "SON / SONT : son = à lui (son chien). sont = verbe être (Ils sont gentils). Astuce : remplace par étaient : Ils étaient gentils = sont.",
    "ces / ses": "CES / SES : ces = ce, cette, ces (ces chiens). ses = à lui, à elle (ses chiens = les chiens de Lenny).",
    "ou / ou": "OU / OÙ : ou = choix (Tu veux thé ou café ?). où = lieu (Où es-tu ?). Astuce : où a un accent, comme lieu.",
    "la / la": "LA / LÀ : la = article (la maison) ou pronom (Je la vois). là = lieu (Je suis là). Astuce : là a un accent.",
    "se / ce": "SE / CE : se = pronom (Il se lève). ce = démonstratif (Ce chien). Astuce : ce = cet, cette, ces.",
    "synonyme": "SYNONYME : Mot qui veut dire la même chose. Ex : content = heureux, rapide = vite, grand = immense.",
    "antonyme": "ANTONYME : Mot qui veut dire le contraire. Ex : grand ≠ petit, chaud ≠ froid, content ≠ triste.",
    "homonyme": "HOMONYME : Mots qui se prononcent pareil mais s'écrivent différemment. Ex : a / à, et / est, son / sont, vert / verre / vers.",
    "famille de mots": "FAMILLE DE MOTS : Mots qui ont la même racine. Ex : fleur, fleuri, fleuriste, floraison. Terre, terrain, terrien, terrestre.",
    "champ lexical": "CHAMP LEXICAL : Ensemble de mots sur le même thème. Ex : Champ lexical de l'école : professeur, élève, cahier, tableau, récréation, devoirs, notes...",
    "passe compose": "PASSE COMPOSE : avoir/être au présent + participe passé. Ex : J'ai mangé, Je suis allé, Tu as joué. Avec être (aller, venir, partir...) : Je suis allé, Elle est venue.",
    "imparfait": "IMPARFAIT : Pour une habitude, une description, une action longue. Terminaisons : -ais, -ais, -ait, -ions, -iez, -aient. Ex : Quand j'étais petit, je jouais au foot. Il faisait beau.",
    "futur": "FUTUR : Pour parler de demain. Terminaisons : -ai, -as, -a, -ons, -ez, -ont. Ex : Je mangerai, tu mangeras, il mangera...",
    "der": "DER DIE DAS : der = masculin (der Mann), die = féminin (die Frau), das = neutre (das Kind). Pluriel = die (die Kinder).",
    "accusatif": "ACCUSATIF : C'est le cas du COD. der → den, die → die, das → das. Ex : Ich sehe den Hund (Je vois le chien).",
    "datif": "DATIF : C'est le cas du COI (à qui ?). der → dem, die → der, das → dem. Ex : Ich gebe dem Mann ein Buch.",
    "nominatif": "NOMINATIF : C'est le cas du sujet. der, die, das. Ex : Der Mann ist gut (L'homme est gentil).",
    "genitif": "GENITIF : C'est le cas de la possession (de qui ?). der → des, die → der, das → des. Ex : Das Buch des Mannes = Le livre de l'homme.",
    "to be": "TO BE - ANGLAIS : I am, You are, He is, We are, You are, They are.",
    "present simple": "PRESENT SIMPLE : Pour les habitudes. I play, You play, He plays (avec -s !), We play... Ex : He plays football every day.",
    "present perfect": "Present Perfect : have + participe. I have eaten = J'ai mangé. I have played = J'ai joué.",
    "present continu": "PRESENT CONTINU : be + -ing. I am playing = Je suis en train de jouer.",
    "preterit": "PRETERIT - ANGLAIS : Pour le passé terminé. Verbes réguliers +ed : I played. Verbes irréguliers : I went, I saw, I ate. Ex : Yesterday, I played football.",
    "futur": "FUTUR - ANGLAIS : will + verbe. I will go = J'irai. I will play = Je jouerai.",
    "comparatif": "COMPARATIF - ANGLAIS : Plus... que = -er + than. Ex : bigger than = plus grand que. More + adjectif long : more beautiful than = plus beau que. Superlatif : the biggest = le plus grand.",
    "pluriel en anglais": "PLURIEL EN ANGLAIS : +s : cat -> cats. En -s, -x, -ch, -sh : +es : box -> boxes. En -y : baby -> babies.",
    "ser et estar": "SER et ESTAR : SER = être permanent (Soy de Suiza). ESTAR = être temporaire / lieu (Estoy en casa, Estoy cansado).",
    "el / la": "EL / LA : el = masculin, la = féminin, los / las = pluriel. Ex : el perro, la casa, los perros, las casas.",
    "pluriel en espagnol": "PLURIEL EN ESPAGNOL : +s : casa -> casas. -z : lápiz -> lápices.",
    "genre en espagnol": "GENRE EN ESPAGNOL : -o = masculin (el libro), -a = féminin (la casa). Exceptions : el día (masculin), la mano (féminin).",
    "il / lo / la": "IL / LO / LA - ITALIEN : il = masculin, lo = masculin devant s+consonne / z, la = féminin. Ex : il libro, lo studente, la casa.",
    "pluriel en italien": "PLURIEL EN ITALIEN : -o -> -i : libro -> libri. -a -> -e : casa -> case. -e -> -i : cane -> cani.",
    "genre en italien": "GENRE EN ITALIEN : -o = masculin, -a = féminin, -e = masculin ou féminin (il cane / la notte).",
    "photosynthese": "PHOTOSYNTHESE : Soleil + Eau + CO2 = Oxygène + Sucre. Les feuilles ont de la chlorophylle (vert) qui capte la lumière. La plante fabrique son sucre et rejette de l'oxygène qu'on respire ! Sans photosynthèse, pas de vie.",
    "gravite": "GRAVITE : La gravité nous attire vers la Terre. C'est Newton qui l'a découverte en voyant une pomme tomber. Sur la Lune, tu es 6x plus léger. Sans gravité, on flotterait.",
    "coeur": "COEUR : Pompe le sang dans tout le corps. 100 000 battements par jour, 7 000 litres de sang par jour, 3 milliards de battements dans une vie ! 4 parties : 2 oreillettes, 2 ventricules.",
    "volcan": "VOLCAN : Ouverture dans la Terre par où sort du magma. Quand le magma sort, ça devient de la lave. 2 types : effusif (lave qui coule, Hawai) et explosif (Vésuve). Le plus actif d'Europe = Etna.",
    "foudre": "FOUDRE : Décharge électrique entre un nuage et le sol. Température : 30 000°C, 5x plus chaud que le Soleil ! Règle : si tu entends le tonnerre, rentre. Pas sous un arbre, pas dans l'eau.",
    "saison": "SAISONS : Ce n'est pas la distance au Soleil, c'est l'inclinaison de la Terre (23,5°). En été, l'hémisphère Nord est penché vers le Soleil, jours longs, chaud. En Australie, c'est l'inverse !",
    "corps humain": "CORPS HUMAIN : 206 os, 600 muscles, 5 litres de sang, 37 000 milliards de cellules. Le cerveau = 86 milliards de neurones !",
    "cerveau": "CERVEAU : 1,4 kg, 86 milliards de neurones. Il contrôle tout : pensées, mouvements, émotions. Il consomme 20% de ton énergie. Pour le garder en forme : dors bien, lis, fais du sport, apprends !",
    "cellule": "CELLULES : La cellule, c'est la plus petite brique du vivant. Tu en as 37 000 milliards ! Chaque cellule a un noyau avec ton ADN, des mitochondries (centrales d'énergie), une membrane.",
    "masse volumique": "MASSE VOLUMIQUE - COURS COMPLET : Formule : masse volumique = masse / volume. Rho = m / V. m = masse, en grammes (balance). V = volume, en cm³ (éprouvette). Ex : 100g / 100 cm³ = 1 g/cm³ = eau. Huile = 0,9 flotte, Fer = 7,8 coule. Règle : Si < 1 ça flotte, si > 1 ça coule. Exercice : 200g / 50 cm³ = 4 g/cm³, il coule.",
    "atome": "ATOME : La plus petite brique de la matière. Noyau avec protons (+) et neutrons (0), et autour des électrons (-) qui tournent. Ex : Hydrogène = 1 proton + 1 électron.",
    "oxygene": "OXYGENE : O2. On respire O2, on rejette CO2. Sans oxygène, on meurt en 3 minutes. 21% de l'air = oxygène, 78% = azote. Dans l'espace, pas d'oxygène, il faut une bouteille.",
    "chimie": "CHIMIE : Etude de la matière. Atome = brique, Molécule = plusieurs atomes. H2O = eau (2 hydrogène + 1 oxygène). CO2 = dioxyde de carbone. Tableau périodique = 118 éléments.",
    "electricite": "ELECTRICITE : Tension en Volts (V), Intensité en Ampères (A), Puissance en Watts (W). Formule : P = U x I. En série : si une lampe grille, tout s'éteint. En parallèle : les autres restent allumées (comme dans ta maison). Danger : 220V = mortel.",
    "vitesse": "VITESSE : Vitesse = distance / temps. v = d / t. Ex : 100m en 10 sec = 10 m/s = 36 km/h. Pour m/s → km/h : x 3,6. Usain Bolt = 44 km/h, Guépard = 110 km/h, Avion = 900 km/h.",
    "energie": "ENERGIE : Cinétique (mouvement), potentielle (hauteur), thermique (chaleur), électrique, chimique, solaire, éolienne. On ne crée pas d'énergie, on la transforme. Ex : Panneau solaire : lumière -> électricité.",
    "force": "FORCE : En Newtons (N). Poids = masse x gravité. Ex : 50 kg sur Terre = 500 N. La force fait bouger les objets.",
    "pression": "PRESSION : Force sur une surface. Ex : Tu appuies avec ton doigt, ça fait mal, avec ta main, ça fait moins mal, car la force est répartie. En montagne, la pression est plus faible, l'eau bout à 95° au lieu de 100°.",
    "lumiere": "LUMIERE : Elle va à 300 000 km / seconde ! C'est la vitesse la plus rapide de l'univers. En 1 seconde, elle fait 7 fois le tour de la Terre ! Soleil -> Terre = 8 minutes.",
    "son": "SON : Le son, c'est une vibration de l'air. Il va à 340 m / seconde dans l'air. Dans le vide, pas de son (dans l'espace, on n'entend rien). Plus c'est grave, plus c'est lent. Plus c'est aigu, plus c'est rapide.",
    "adn": "ADN : Ton code génétique, dans toutes tes cellules. Il dit si tu as les yeux bleus, bruns, si tu es grand, petit... En forme de double hélice. Tu as 50% de l'ADN de ton père, 50% de ta mère.",
    "trou noir": "TROU NOIR : Objet tellement lourd et petit que même la lumière ne peut pas en sortir. Comment ça se forme ? Quand une très grosse étoile meurt, elle explose puis s'écrase. Au centre de notre galaxie, un trou noir de 4 millions de fois la masse du Soleil.",
    "big bang": "BIG BANG : Début de l'univers il y a 13,8 milliards d'années. Tout était concentré en un point minuscule, puis ça a explosé et ça s'étend encore aujourd'hui.",
    "mars": "MARS : Planète rouge, à cause du fer oxydé (rouille). Un jour sur Mars = 24h37. Une année = 687 jours. Température : -60°. Robots : Perseverance, 【entity-Curiosity¦canonical_name=Curiosity】. Un jour, des humains iront.",
    "iss": "ISS : Station Spatiale Internationale. Elle tourne autour de la Terre à 400 km, à 28 000 km/h (tour de Terre en 90 min). 16 levers de soleil par jour ! 6 astronautes dedans.",
    "systeme solaire": "SYSTEME SOLAIRE : 8 planètes autour du Soleil : Mercure, Vénus, Terre, Mars, Jupiter, Saturne, Uranus, Neptune. Astuce : Me Voici, Tout Mouillé, J'ai Suivi Un Nuage.",
    "soleil": "SOLEIL : C'est une étoile, pas une planète. Température au centre : 15 millions de degrés, à la surface : 5500°. Il est composé d'hydrogène et d'hélium. Il va mourir dans 5 milliards d'années.",
    "galaxie": "GALAXIE : Groupe de milliards d'étoiles. Notre galaxie = Voie Lactée, 200 milliards d'étoiles, 100 000 années-lumière. La voisine = Andromède, 2,5 millions d'années-lumière. Il y a 200 milliards de galaxies !",
    "lune": "LUNE : Notre satellite. Distance : 384 000 km. Elle tourne autour de la Terre en 27 jours. Premier homme dessus : Neil Armstrong, 1969. Elle fait les marées. Elle s'éloigne de 3,8 cm par an !",
    "boucle": "BOUCLE : Pour répéter sans recopier. Ex : for i in range(1,6): print(i) -> affiche 1,2,3,4,5. Sans boucle, il faudrait écrire 5 print.",
    "variable": "VARIABLE : Boîte qui stocke une valeur. Ex : age = 13, prenom = 'Lenny', note = 15. Tu peux la changer : age = 14.",
    "condition": "CONDITION : Si... sinon... Ex : if age >= 18: print('Majeur') else: print('Mineur'). Si la condition est vraie, on fait la 1ère action, sinon la 2ème.",
    "fonction": "FONCTION : Bloc de code qu'on peut réutiliser. Ex : def dire_bonjour(): print('Bonjour'). Tu l'appelles avec dire_bonjour().",
    "liste": "LISTE : Plusieurs valeurs dans une boîte. Ex : notes = [12, 15, 18]. notes[0] = 12. Tu peux ajouter : notes.append(20).",
    "algorithme": "ALGORITHME : Suite d'étapes pour résoudre un problème. Ex : Recette de cuisine = algorithme. Pour faire un gâteau : 1. Mélanger, 2. Mettre au four, 3. Attendre, 4. Manger !",
    "python": "PYTHON : Langage facile, celui de ton agent. Créé en 1991 par Guido van Rossum. Utilisé pour l'IA, les sites web, les jeux, les robots. Ex : print('Bonjour').",
    "html": "HTML : Squelette d'un site. <h1>Titre</h1> <p>Texte</p> <img src='photo.jpg'> <a href='https://...'>Lien</a>. Sans HTML, pas de site.",
    "css": "CSS : Style d'un site : couleurs, tailles, positions. Ex : body { background-color: black; color: white; }. Sans CSS, ton site est tout blanc et moche.",
    "javascript": "JAVASCRIPT : Langage pour rendre un site interactif : boutons, animations, jeux. HTML = squelette, CSS = style, JS = cerveau.",
    "scratch": "SCRATCH : Pour apprendre à coder en glissant des blocs. Créé par le MIT. Parfait pour commencer à 8-13 ans. Tu peux faire des jeux, des animations.",
    "ia": "IA - INTELLIGENCE ARTIFICIELLE : Programme qui apprend avec des données. Ex : ChatGPT, ton agent, les voitures autonomes, les filtres TikTok. Elle ne pense pas comme nous, elle prédit le mot / l'image la plus probable. Elle a besoin de beaucoup de données et d'électricité.",
    "joconde": "JOCONDE : Peinture de Léonard de Vinci, 1503-1506. Au Louvre à Paris. La plus célèbre au monde. Elle sourit bizarrement, on ne sait pas si elle est contente ou triste. 7M de personnes la voient chaque année. Elle vaut 860M € !",
    "van gogh": "VAN GOGH : Peintre néerlandais, 1853-1890. Il a peint 900 tableaux en 10 ans. Il s'est coupé l'oreille. Son tableau le plus célèbre : La Nuit étoilée, Les Tournesols. Il n'a vendu qu'1 tableau de son vivant, maintenant ses tableaux valent 80M € !",
    "picasso": "PICASSO : Peintre espagnol, 1881-1973. Il a inventé le cubisme (visages de face et de profil en même temps). Il a peint Guernica (1937) contre la guerre. Il a fait 50 000 œuvres !",
    "art": "ART : L'art, c'est exprimer une émotion avec une œuvre : peinture, sculpture, musique, photo, danse, cinéma... Il n'y a pas de bonne ou mauvaise réponse, c'est ce que tu ressens.",
    "rap": "RAP : Musique née dans le Bronx à New York dans les années 70. On parle / on chante vite sur un rythme. En France, c'est la musique la plus écoutée. Artistes : Werenoi, Ninho, Jul, PNL, Booba...",
    "piano": "PIANO : Instrument avec 88 touches (52 blanches, 36 noires). Inventé en 1700 par Bartolomeo Cristofori en Italie. Les plus grands : Mozart, Beethoven, Chopin. Pour apprendre : 30 min par jour, tous les jours.",
    "guitare": "GUITARE : Instrument avec 6 cordes. Il y a la classique, l'acoustique, l'électrique. Accords de base : Do, Sol, La mineur, Mi mineur. Avec 4 accords, tu peux jouer 100 chansons !",
    "note": "NOTE DE MUSIQUE : 7 notes : Do, Ré, Mi, Fa, Sol, La, Si. Puis ça recommence : Do... Les notes blanches du piano. Les notes noires = dièses / bémols. Une octave = 8 notes.",
    "foot": "FOOT : Sport le plus joué au monde, 3,5 milliards de fans ! 2 équipes de 11, 90 minutes, 1 ballon. But = mettre le ballon dans le but adverse. Coupe du Monde tous les 4 ans. Meilleurs : 【entity-Messi¦canonical_name=Messi】, 【entity-Ronaldo¦canonical_name=Ronaldo】, 【entity-Mbappé¦canonical_name=Mbappe】.",
    "basket": "BASKET : 5 vs 5, panier à 3,05m, match 4x12 min en 【entity-NBA¦canonical_name=NBA】. Michael Jordan = GOAT (6 titres 【entity-NBA¦canonical_name=NBA】). LeBron James = 40 000 points, record. En France : Victor Wembanyama, 2m24, joue aux Spurs !",
    "tennis": "TENNIS : Federer (20 Grands Chelems, Suisse !), Nadal (22, roi de Roland-Garros, 14 fois !), 【entity-Djokovic¦canonical_name=Djokovic】 (24, record). Grand Chelem = 4 tournois : Open d'Australie, Roland-Garros, Wimbledon, US Open.",
    "formule 1": "FORMULE 1 : 350 km/h ! 20 pilotes, 10 équipes. Verstappen (Red Bull) a gagné 2021, 2022, 2023, 2024. Hamilton (Ferrari) = 7 titres, record avec Schumacher. Grand Prix de Monaco = le plus prestigieux.",
    "jo": "JO - JEUX OLYMPIQUES : Tous les 4 ans. Antiquité : en Grèce, -776. Modernes : depuis 1896. 2024 = Paris, 2028 = Los Angeles. Sports : athlétisme, natation, foot, basket, judo, skate... Devise : Plus vite, plus haut, plus fort.",
    "manger sain": "MANGER SAIN : 5 fruits et légumes par jour, boire 1,5L d'eau, moins de sucre, moins de fast-food. Ton cerveau a besoin de bon carburant : poisson, fruits, légumes, noix. Si tu manges mal, tu es fatigué, tu te concentres moins.",
    "sommeil": "SOMMEIL : A 13 ans, il faut 9-10h de sommeil ! Pendant que tu dors, ton cerveau range ce que tu as appris, ton corps grandit (hormone de croissance). Pas d'écran 1h avant de dormir, sinon tu t'endors mal.",
    " 【entity-messi¦canonical_name=Messi】": " 【entity-MESSI¦canonical_name=Messi】 : 【entity-Lionel Messi¦canonical_name=Lionel Messi】, né en 1987 à Rosario, Argentine. 8 Ballons d'Or (record), 91 buts en une année (2012, record). 【entity-Barça¦canonical_name=Barça】 (672 buts), 【entity-PSG¦canonical_name=PSG】, 【entity-Miami¦canonical_name=Inter Miami CF】. Coupe du Monde 2022 avec l'Argentine. Petit (1m70), gaucher, dribbles courts, vision incroyable. Considéré comme le meilleur de tous les temps.",
    " 【entity-ronaldo¦canonical_name=Ronaldo】": " 【entity-CRISTIANO RONALDO¦canonical_name=Cristiano Ronaldo】 : Né en 1985 à Madère, Portugal. 5 Ballons d'Or, meilleur buteur de l'histoire en sélection (130 buts), meilleur buteur de la Ligue des Champions (140 buts), 900 buts en carrière. Grand (1m87), physique, saut incroyable (2,93m !). 600M de followers sur Instagram, le plus suivi au monde.",
    " 【entity-mbappe¦canonical_name=Mbappe】": " 【entity-MBAPPE¦canonical_name=Mbappe】 : Kylian 【entity-Mbappé¦canonical_name=Mbappe】, né en 1998 à Bondy, France. Champion du Monde 2018 à 19 ans, meilleur buteur de la Coupe du Monde 2022 (8 buts, triplé en finale). Meilleur buteur de l'histoire du 【entity-PSG¦canonical_name=PSG】 (256 buts). Vitesse : 36 km/h, le plus rapide du foot. 【entity-Real Madrid¦canonical_name=Real Madrid】 depuis 2024, capitaine de l'équipe de France.",
    "ballon d'or": "BALLON D'OR : Trophée du meilleur joueur du monde chaque année, voté par des journalistes. Créé en 1956. 【entity-Messi¦canonical_name=Messi】 en a 8 (record), 【entity-Ronaldo¦canonical_name=Ronaldo】 5, Cruyff 3, Platini 3. En 2024, c'est Rodri qui a gagné.",
    "coupe du monde": "COUPE DU MONDE : Tous les 4 ans, 48 équipes en 2026 (USA / Canada / Mexique). 2022 = Argentine gagne contre France (3-3, tirs au but). 2018 = France gagne. Le Brésil a gagné 5 fois, record. Prochaine : 2026, 104 matchs, 16 villes.",
    "ligue des champions": "LIGUE DES CHAMPIONS : Meilleure compétition de clubs en Europe. 【entity-Real Madrid¦canonical_name=Real Madrid】 a gagné 15 fois, record ! 【entity-Milan¦canonical_name=AC Milan】 7, 【entity-Bayern¦canonical_name=Bayern】 6, 【entity-Liverpool¦canonical_name=Liverpool】 6, Barcelone 5. Finale 2024 : Real gagne contre 【entity-Dortmund¦canonical_name=Dortmund】.",
    " 【entity-minecraft¦canonical_name=Minecraft】": " 【entity-MINECRAFT¦canonical_name=Minecraft】 : Créé par Notch en 2011, racheté par 【entity-Microsoft¦canonical_name=Microsoft】 pour 2,5 milliards $. Jeu le plus vendu au monde : 300M de copies ! Monde infini en cubes, tu mines, tu construis, tu survis. Modes : Survie (creeper, zombie), Créatif (tout illimité), Aventure. Mobs : Creeper (BOOM), Enderman, Ender Dragon (boss final).",
    " 【entity-fortnite¦canonical_name=Fortnite】": " 【entity-FORTNITE¦canonical_name=Fortnite】 : Créé par Epic Games en 2017. Battle Royale : 100 joueurs sur une île, le dernier vivant gagne. Modes : Battle Royale (avec construction), Zéro Construction, 【entity-Lego¦canonical_name=LEGO】 【entity-Fortnite¦canonical_name=Fortnite】, Festival. Armes : gris, vert, bleu, violet, orange (du moins fort au plus fort). Esport : Bugha a gagné 3M $ à 16 ans en 2019 !",
    " roblox": " ROBLOX : Plateforme avec des millions de jeux créés par les joueurs. Créé en 2006. Jeux cultes : Brookhaven, Blox Fruits, Pet Simulator, Doors, Murder Mystery 2. Tu peux créer ton propre jeu avec Roblox Studio et gagner des Robux. 300M de joueurs par mois !",
    "gta": "GTA V : Sorti en 2013, 190M de copies, 2ème jeu le plus vendu (après 【entity-Minecraft¦canonical_name=Minecraft】). Monde ouvert : Los Santos (Los Angeles). 3 personnages : Michael, Franklin, Trevor. GTA VI sort en 2026, à Vice City (【entity-Miami¦canonical_name=Inter Miami CF】), avec Lucia et Jason. Jeu le plus attendu de tous les temps.",
    "brawl stars": "BRAWL STARS : Jeu mobile de Supercell (Clash of Clans). 3v3, tu choisis un Brawler (Shelly, Colt, Spike, Leon...). Modes : Gem Grab, Showdown (battle royale), Brawl Ball (foot). Gratuit, 500M de téléchargements !",
    " mario": " MARIO : Plombier Nintendo, sauve Peach. Créé en 1981 par Shigeru Miyamoto. Jeux : Super Mario Bros, Mario Kart, Mario Party, Super Mario Odyssey. Frère : Luigi. Ennemi : Bowser. 800M de jeux vendus !",
    " pokemon": " POKEMON : Attrape-les tous ! Créé en 1996 au Japon. 1000+ Pokémons. Pikachu = mascotte. Jeux : Rouge, Or, Diamant, Ecarlate, Violet. Cartes Pokémon = les plus collectionnées au monde, une carte Dracaufeu = 500 000 $ ! Anime : Sacha et Pikachu, 25 ans d'aventure.",
    "one piece": "ONE PIECE : Manga le plus vendu au monde (500M de tomes). Luffy veut devenir Roi des Pirates. Il a mangé le Fruit du Démon, il est en caoutchouc. Equipage : Zoro, Nami, Usopp, Sanji, Chopper, Robin, Franky, Brook, Jinbe. Auteur : Eiichiro Oda, depuis 1997, 1100+ chapitres !",
    "naruto": "NARUTO : Ninja quiVoilà la **suite** à coller juste après là où ça s'est coupé, pour avoir le code complet en 1 seul fichier. Tu ne dois rien effacer, tu colles juste ça à la fin :

```python
    "naruto": "NARUTO : Ninja qui veut devenir Hokage. Rasengan, Chidori, Kyubi (demon renard a 9 queues). Auteur : Masashi Kishimoto. Suite : 【entity-Boruto¦canonical_name=Boruto】 (son fils).",
    "dragon ball": "DRAGON BALL : Goku, Super Saiyan, Kamehameha ! Auteur : Akira Toriyama. Goku ramasse 7 Dragon Balls pour exaucer un voeu. Transformations : Super Saiyan 1, 2, 3, Blue, Ultra Instinct.",
    "tour eiffel": "TOUR EIFFEL : Paris, 330m, 1889, Gustave Eiffel. 7M de visiteurs par an. Elle grandit de 15 cm en ete ! Au debut, les Parisiens la detestaient !",
    "pyramide": "PYRAMIDES : En Egypte, il y a 4500 ans pour les Pharaons. La plus grande = Kheops, 146m, 2,3 millions de blocs de 2,5 tonnes ! 20 000 ouvriers pendant 20 ans.",
    " titanic": " TITANIC : Paquebot anglais, le plus grand du monde en 1912. Il heurte un iceberg le 14 avril 1912, il coule en 2h40. 1517 morts, 706 survivants. Film 1997, 11 Oscars.",
    " 【entity-harry potter¦canonical_name=Harry Potter】": " 【entity-HARRY POTTER¦canonical_name=Harry Potter】 : Sorcier avec une cicatrice en eclair, par J.K. Rowling. 7 livres, 8 films, 500M de livres vendus. Maisons : Gryffondor, Serpentard, Poufsouffle, Serdaigle. Personnages : Hermione, Ron, Dumbledore, Hagrid.",
    "millionnaire": "COMMENT DEVENIR MILLIONNAIRE ? : 1. Salarie + investissement : tu mets une partie de ton salaire en bourse (ETF), sur le long terme ca grandit. 2. Entrepreneur : tu crees un business. 3. Createur : YouTube, TikTok. Conseils : Apprends une competence, epargne une partie de ce que tu gagnes, investis tot, ne depense pas pour impressionner.",
    "salaire": "SALAIRE : Salaire = argent que tu gagnes chaque mois pour ton travail. En Suisse : salaire moyen autour de 6500 CHF / mois. Brut = avant impots, Net = apres impots (ce que tu touches vraiment).",
    "metier": "METIER - IDEES : Developpeur, Medecin, Avocat, Pilote, Ingenieur, Enseignant, Infirmier, Electricien, Cuisinier, Youtubeur. Le meilleur metier, c'est celui que tu aimes + qui paie bien + qui est utile.",
    "entrepreneur": "ENTREPRENEUR : Quelqu'un qui cree son entreprise. Ex : Elon Musk (Tesla, SpaceX), Jeff Bezos (Amazon), Mark Zuckerberg (Facebook). Qualites : ne pas avoir peur d'echouer, travailler beaucoup, ecouter les clients, apprendre tous les jours.",
    "gagner de l argent": "COMMENT GAGNER DE L'ARGENT A 13 ANS EN SUISSE ? : Tu ne peux pas encore facturer seul. Solutions : 1. Petits services : aider voisins (tondre, promener chien, aider ordi). 2. Vendre ce que tu n'utilises plus. 3. Creer un projet (agent IA, site, chaine) et montrer a tes parents, ils peuvent facturer pour toi. 4. Apprendre une competence (code, design, montage) pour etre pret a 16 ans.",
    "bourse": "BOURSE : La bourse, c'est acheter une petite partie d'une entreprise (une action). Si l'entreprise gagne, ton action monte. Si elle perd, elle baisse. ETF = panier de beaucoup d'entreprises, moins risque qu'une seule. Ne jamais mettre tout son argent au meme endroit.",
    "plus grand animal": "PLUS GRAND ANIMAL : Baleine bleue ! 30m, 200 tonnes, coeur = 600 kg ! Elle mange du krill, 4 tonnes par jour. Plus grande qu'un dinosaure !",
    "plus rapide": "PLUS RAPIDE : Guepard = 110 km/h sur terre. Faucon pelerin = 390 km/h en pique ! Poisson voilier = 110 km/h dans l'eau. Usain Bolt = 44 km/h.",
    "chien": "CHIEN : Meilleur ami de l'homme depuis 15 000 ans. 400 races : Labrador (gentil), Berger Allemand (police), Chihuahua (petit), Husky (neige). Il comprend 150 mots, il sent beaucoup mieux que nous.",
    "chat": "CHAT : Il dort 16h par jour ! Il a 32 muscles dans chaque oreille, il peut sauter 6x sa hauteur, il retombe toujours sur ses pattes. Il ronronne quand il est content.",
    "lion": "LION : Roi des animaux. Il vit en Afrique. Le male a une crinière, la femelle chasse. Il dort 20h par jour ! Il rugit si fort qu'on l'entend a 8 km.",
    "dauphin": "DAUPHIN : Animal tres intelligent, il communique avec des sons, il dort avec un oeil ouvert et un demi-cerveau eveillé pour respirer. Il peut nager a 60 km/h.",
    "recette facile": "RECETTE FACILE - PATES : 1. Fais bouillir de l'eau salee. 2. Mets les pates 8-10 min. 3. Egoutte. 4. Ajoute sauce tomate + fromage. C'est pret !",
    "pates": "PATES : Pates = farine + eau + oeufs. Types : spaghetti, penne, fusilli, tagliatelle. Cuisson : 8-10 min dans l'eau bouillante salee. Sauce : tomate, carbonara, pesto.",
    "gateau au chocolat": "GATEAU AU CHOCOLAT - RECETTE : 200g chocolat, 200g beurre, 4 oeufs, 150g sucre, 100g farine. 1. Fais fondre chocolat + beurre. 2. Melange oeufs + sucre. 3. Ajoute tout + farine. 4. Four 180° pendant 25 min. C'est pret !",
    "conseil pour reviser": "CONSEIL POUR REVISER - TOP 5 : 1. Pomodoro : 25 min de travail, 5 min de pause. 2. Relis pas, teste-toi : fais des quiz. 3. Explique a quelqu'un. 4. Dors bien : ton cerveau range ce que tu as appris pendant la nuit. 5. Pas de telephone pendant que tu revises.",
}

AVIONS = {
    "f-22": "F-22 RAPTOR (USA) - LE PLUS PERFORMANT EN COMBAT. Mach 2.25 (2400 km/h). Furtif, jamais battu en exercice. 195 exemplaires, jamais vendu a d'autres pays, trop secret !",
    " f-35": " F-35 LIGHTNING II (USA) - LE PLUS MODERNE. Mach 1.6. La Suisse en a achete 36 ! Il voit tout a 360°, il partage les infos avec les autres avions.",
    "rafale": "RAFALE (France). Mach 1.8. Polyvalent : air, sol, mer. Il peut decoller d'un porte-avions. Utilise par France, Inde, Grece, Egypte, Qatar...",
    "sr-71": "SR-71 BLACKBIRD. Mach 3.3 = 3500 km/h ! Plus rapide de tous les temps. Aucun missile ne l'a jamais touche. Il volait a 25 000m.",
    "concorde": "CONCORDE : Paris-New York en 3h30. Mach 2. Billet : tres cher. Arrete en 2003.",
    "f-16": "F-16. Mach 2.0. Plus produit : 4600 exemplaires ! Petit, agile, pas cher. Utilise par 25 pays.",
    "f-15": "F-15 EAGLE. Mach 2.5 ! 104 victoires a 0 defaite en combat reel, legende !",
    "a380": "【entity-AIRBUS¦canonical_name=AIRBUS】 A380 : Le plus gros avion de passagers. 2 etages, 850 passagers max ! 73m de long, 80m d'envergure. 【entity-Emirates¦canonical_name=Emirates】 en a le plus.",
    "comment vole": "COMMENT VOLE UN AVION ? : L'aile est courbee en haut, plate en bas. L'air va plus vite au-dessus, donc pression plus faible au-dessus, pression plus forte en dessous. Ca cree une force vers le haut = portance. Pour decoller, il faut aller vite (250 km/h pour un A380).",
}

TRAIN_FACILE = [("C'est quoi 2+2 ?", "4"), ("C'est quoi 5x2 ?", "10"), ("C'est quoi la capitale de la France ?", "paris"), ("C'est quoi 3x3 ?", "9"), ("C'est quoi 10-3 ?", "7")]
TRAIN_MOYEN = [("C'est quoi 7x8 ?", "56"), ("C'est quoi la capitale du Japon ?", "tokyo"), ("C'est quoi 15+25 ?", "40"), ("Qui a gagne la Coupe du Monde 2022 ?", "argentine"), ("C'est quoi la formule de la masse volumique ?", "m/v"), ("Qui a chante Solitaire ?", "werenoi"), ("C'est quoi a2 + b2 = c2 ?", "pythagore"), ("C'est quoi la capitale de la Suisse ?", "berne")]
TRAIN_DIFFICILE = [("C'est quoi 12x12 ?", "144"), ("C'est quoi la capitale de l'Australie ?", "canberra"), ("C'est quoi 144 / 12 ?", "12"), ("Combien de Ballons d'Or a Messi ?", "8"), ("En quelle annee a coule le Titanic ?", "1912")]
TRAIN_VERBES = [("Conjugue ETRE au present : je ... ?", "suis"), ("Conjugue AVOIR au present : tu ... ?", "as"), ("Conjugue TO BE : I ... ?", "am"), ("Conjugue SEIN : ich ... ?", "bin"), ("Conjugue ALLER : il ... ?", "va")]
TRAIN_MATHS = [("C'est quoi 7x8 ?", "56"), ("C'est quoi 9x9 ?", "81"), ("C'est quoi 12+15 ?", "27"), ("C'est quoi 100-37 ?", "63")]
TRAIN_FRANCAIS = [("C'est quoi le COD ?", "cod"), ("Conjugue ETRE : je ... ?", "suis"), ("C'est quoi le pluriel de cheval ?", "chevaux")]
TRAIN_CAPITALES = [("C'est quoi la capitale du Japon ?", "tokyo"), ("C'est quoi la capitale de la France ?", "paris"), ("C'est quoi la capitale de la Suisse ?", "berne"), ("C'est quoi la capitale du Bresil ?", "brasilia")]

def toutes_tables():
    txt = "TOUTES LES TABLES DE MULTIPLICATION 1 a 12 :\n\n"
    for n in range(1, 13):
        txt += f"Table de {n} : " + ", ".join([f"{n}x{i}={n*i}" for i in range(1, 11)]) + "\n\n"
    txt += "ASTUCE : Dis-les a voix haute 3 fois, puis cache et recite. Les plus durs : 7x8=56, 6x7=42, 8x8=64 !"
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
        return f"Ok, entrainement arrete ! 🏁 Ton score final : {st.session_state.score}/{st.session_state.total_quiz} ! 🔥 Meilleur streak : {st.session_state.best_streak} ! Bravo, tu as bien travaille ! 💪"
    if st.session_state.mode_train and st.session_state.train_q is not None:
        bonne = nettoyer(st.session_state.train_a)
        st.session_state.total_quiz += 1
        if bonne in q_low or q_low in bonne or q_low == bonne:
            st.session_state.score += 1
            st.session_state.streak += 1
            if st.session_state.streak > st.session_state.best_streak:
                st.session_state.best_streak = st.session_state.streak
            rep = f"✅ BRAVO ! Bonne reponse ! C'etait bien '{st.session_state.train_a}' ! 🎉 Score : {st.session_state.score}/{st.session_state.total_quiz} | 🔥 Streak : {st.session_state.streak}"
        else:
            st.session_state.streak = 0
            rep = f"❌ Pas tout a fait... La bonne reponse c'etait '{st.session_state.train_a}'. C'est pas grave, on apprend ! Score : {st.session_state.score}/{st.session_state.total_quiz}"
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
        return rep + f"\n\n🎯 Question suivante ({st.session_state.niveau}) : {nq}"
    if "entrainement facile" in q_low or q_low == "quiz facile":
        st.session_state.mode_train = True; st.session_state.niveau = "facile"; st.session_state.train_matiere = ""
        nq, na = random.choice(TRAIN_FACILE); st.session_state.train_q = nq; st.session_state.train_a = na
        return f"🎯 C'EST PARTI - ENTRAINEMENT FACILE ! 🟢 Ecris 'stop' pour arreter.\n\nPremiere question : {nq}"
    if "entrainement difficile" in q_low:
        st.session_state.mode_train = True; st.session_state.niveau = "difficile"; st.session_state.train_matiere = ""
        nq, na = random.choice(TRAIN_DIFFICILE); st.session_state.train_q = nq; st.session_state.train_a = na
        return f"🎯 C'EST PARTI - ENTRAINEMENT DIFFICILE ! 🔴 Pour les champions !\n\nPremiere question : {nq}"
    if "entrainement verbes" in q_low or "quiz verbes" in q_low:
        st.session_state.mode_train = True; st.session_state.niveau = "verbes"; st.session_state.train_matiere = "Verbes"
        nq, na = random.choice(TRAIN_VERBES); st.session_state.train_q = nq; st.session_state.train_a = na
        return f"🎯 ENTRAINEMENT VERBES ! ✍️ Conjugue ! Ecris 'stop' pour arreter.\n\nPremiere question : {nq}"
    if "quiz maths" in q_low:
        st.session_state.mode_train = True; st.session_state.niveau = "maths"; st.session_state.train_matiere = "Maths"
        nq, na = random.choice(TRAIN_MATHS); st.session_state.train_q = nq; st.session_state.train_a = na
        return f"🎯 QUIZ MATHS ! 🧮 Ecris 'stop' pour arreter.\n\nPremiere question : {nq}"
    if "quiz francais" in q_low:
        st.session_state.mode_train = True; st.session_state.niveau = "francais"; st.session_state.train_matiere = "Francais"
        nq, na = random.choice(TRAIN_FRANCAIS); st.session_state.train_q = nq; st.session_state.train_a = na
        return f"🎯 QUIZ FRANCAIS ! 🇫🇷 Ecris 'stop' pour arreter.\n\nPremiere question : {nq}"
    if "quiz capitales" in q_low or "quiz capital" in q_low:
        st.session_state.mode_train = True; st.session_state.niveau = "capitales"; st.session_state.train_matiere = "Capitales"
        nq, na = random.choice(TRAIN_CAPITALES); st.session_state.train_q = nq; st.session_state.train_a = na
        return f"🎯 QUIZ CAPITALES ! 🌍 Ecris 'stop' pour arreter.\n\nPremiere question : {nq}"
    if "quiz" in q_low and "maths" not in q_low and "francais" not in q_low and "capitales" not in q_low and "verbes" not in q_low:
        st.session_state.mode_train = True; st.session_state.niveau = "moyen"; st.session_state.train_matiere = ""
        nq, na = random.choice(TRAIN_MOYEN); st.session_state.train_q = nq; st.session_state.train_a = na
        return f"🎯 C'EST PARTI POUR L'ENTRAINEMENT ! Ecris 'stop' pour arreter.\n\nPremiere question : {nq}"
    if "entraine" in q_low or "entrainement" in q_low or q_low == "quiz moi":
        st.session_state.mode_train = True; st.session_state.niveau = "moyen"; st.session_state.train_matiere = ""
        nq, na = random.choice(TRAIN_MOYEN); st.session_state.train_q = nq; st.session_state.train_a = na
        return f"🎯 C'EST PARTI POUR L'ENTRAINEMENT MOYEN ! Je te pose des questions, tu reponds, je te corrige ! Ecris 'stop' pour arreter. Essaie aussi : Entrainement facile / difficile / verbes / Quiz Maths / Quiz Francais / Quiz Capitales.\n\nPremiere question : {nq}"
    if "mon score" in q_low or q_low == "score":
        return f"🏆 Ton score : {st.session_state.score} / {st.session_state.total_quiz} ! 🔥 Streak : {st.session_state.streak} | Best : {st.session_state.best_streak} ! Ecris 'Entraine moi' pour continuer !"
    if q_brut.startswith("apprends") or q_brut.startswith("apprend") or "retient que" in q_brut:
        try:
            texte = q_brut.replace("apprends :", "").replace("apprends", "").replace("apprend :", "").replace("apprend", "").replace("retient que", "").strip()
            if "=" in texte:
                cle, val = texte.split("=", 1)
                cle = nettoyer(cle); val = val.strip()
                st.session_state.learned[cle] = val
                return f"✅ MERCI ! J'ai appris ! 🧠 Maintenant je sais que '{cle}' = '{val}' ! J'ai appris {len(st.session_state.learned)} choses !"
            else:
                st.session_state.learned[nettoyer(texte)] = texte
                return f"✅ Merci ! J'ai retenu : '{texte}' ! 🧠"
        except:
            return "Pour m'apprendre, ecris : Apprends : c'est quoi le foot = le foot c'est un sport avec un ballon"
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
    return f"🤔 Hmm, je ne connais pas encore : '{q_orig}'...\n\nMais tu peux M'APPRENDRE ! Ecris :\n\nApprends : {q_orig} = ta reponse ici\n\n💡 Essaie :\n- Francais → Verbes → Conjugue ETRE\n- Maths → Geometrie → C'est quoi Pythagore ?\n- C'est qui Werenoi ?\n- Entraine moi\n- Quiz Maths / Quiz Francais / Quiz Capitales"

if "auto_q" in st.session_state and st.session_state.auto_q:
    q_auto = st.session_state.auto_q
    st.session_state.auto_q = ""
    r_auto = trouver(q_auto)
    st.session_state.messages.append({"role": "assistant", "content": r_auto})
    with st.chat_message("assistant"):
        st.write(r_auto)

if question := st.chat_input("Pose ta question, ou choisis Matiere → Genre → Question en haut !"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        r = trouver(question)
        st.write(r)
    st.session_state.messages.append({"role": "assistant", "content": r})
