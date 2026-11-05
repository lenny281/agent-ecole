import streamlit as st
import random
import datetime

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

if "theme" not in st.session_state:
    st.session_state.theme = "📐 Ecole"

MATIERES = {
    "📐 Maths": ["C'est quoi le théorème de Pythagore ?", "Table de 7", "Toutes les tables de multiplication", "Table de division de 8", "C'est quoi Thales ?", "C'est quoi la moyenne ?", "C'est quoi l'aire ?", "C'est quoi le perimetre ?", "C'est quoi une fraction ?", "C'est quoi le pourcentage ?", "C'est quoi une equation ?", "Calcule 12+8", "Calcule 15x7"],
    "🇫🇷 Français": ["Conjugue ETRE", "Conjugue AVOIR", "Conjugue ALLER", "C'est quoi le passe compose ?", "C'est quoi l'imparfait ?", "C'est quoi le futur ?", "C'est quoi le pluriel ?", "C'est quoi un adjectif ?", "C'est quoi le COD ?", "C'est quoi le sujet ?"],
    "🇩🇪 Allemand": ["C'est quoi der die das ?", "Conjugue SEIN", "Conjugue HABEN", "C'est quoi GEHEN ?", "Traduis bonjour en allemand"],
    "🇬🇧 Anglais": ["Conjugue TO BE", "Conjugue TO HAVE", "C'est quoi TO GO ?", "C'est quoi le present perfect ?", "Traduis bonjour en anglais", "Traduis merci en anglais"],
    "📜 Histoire / Géo": ["C'est quoi la 2eme Guerre ?", "C'est quoi la Revolution ?", "C'est quoi Rome ?", "C'est quoi le Moyen Age ?", "C'est quoi l'Egypte ?", "C'est quoi Napoleon ?", "C'est quoi les continents ?", "C'est quoi les oceans ?", "C'est quoi la 1ere Guerre ?", "C'est quoi les pyramides ?"],
    "🔬 Sciences": ["Comment calculer la masse volumique ?", "C'est quoi la photosynthese ?", "C'est quoi la gravite ?", "C'est quoi le coeur ?", "C'est quoi un volcan ?", "C'est quoi les saisons ?", "C'est quoi la foudre ?", "C'est quoi le systeme solaire ?", "C'est quoi l'ADN ?"],
    "🧪 Chimie / Physique": ["C'est quoi un atome ?", "C'est quoi l'oxygene ?", "C'est quoi la chimie ?", "C'est quoi l'electricite ?", "C'est quoi la masse volumique ?", "C'est quoi la densite ?", "C'est quoi la vitesse ?", "C'est quoi l'energie ?"],
    "💻 Code": ["C'est quoi une variable ?", "C'est quoi une boucle ?", "C'est quoi une condition ?", "C'est quoi Python ?", "C'est quoi HTML ?", "C'est quoi CSS ?", "C'est quoi une fonction ?", "C'est quoi une liste ?"],
}

THEMES = {
    "📐 Ecole": ["Voir toutes les matières 👇"],
    "👋 Bases": ["Bonjour", "Ca va ?", "Merci", "Au revoir", "Tu t'appelles comment ?", "Tu peux m'aider ?", "Raconte une blague", "Motive moi"],
    "🧮 Calculatrice": ["Calcule 12+8", "Calcule 15x7", "Calcule 100-35", "Calcule 144/12"],
    "🌍 Traductions": ["Traduis bonjour en anglais", "Traduis merci en anglais", "Traduis bonjour en allemand", "Traduis bonjour en espagnol"],
    "🎲 Fun": ["Raconte une blague", "Motive moi", "Quiz moi", "Conseil pour reviser", "Quelle heure il est ?"],
    "🌍 Capitales": ["Capitale du Japon ?", "Capitale du Bresil ?", "Capitale de l'Egypte ?", "Capitale de la Suisse ?"],
    "✈️ Avions": ["Quel est l'avion de chasse le plus performant ?", "C'est quoi le F-22 ?", "C'est quoi le 【entity-F-35¦canonical_name=F-35】 ?", "C'est quoi le Rafale ?", "C'est quoi le SR-71 ?", "C'est quoi le Concorde ?"],
    "💻 PC": ["C'est quoi le meilleur rapport qualite prix ?", "C'est quoi la meilleure GPU ?", "C'est quoi le meilleur CPU ?", "C'est quoi le meilleur SSD ?", "C'est quoi la meilleure RAM ?", "PC 2000 CHF", "PC 1300 CHF", "PC 900 CHF"],
    "⚽ Foot / Sport": ["C'est qui 【entity-Messi¦canonical_name=Messi】 ?", "C'est qui 【entity-Ronaldo¦canonical_name=Ronaldo】 ?", "C'est qui 【entity-Mbappe¦canonical_name=Mbappe】 ?", "C'est quoi la Coupe du Monde ?", "C'est quoi la Ligue des Champions ?", "C'est quoi le Ballon d'Or ?"],
    "🎮 Jeux Video": ["C'est quoi 【entity-Minecraft¦canonical_name=Minecraft】 ?", "C'est quoi 【entity-Fortnite¦canonical_name=Fortnite】 ?", "C'est quoi 【entity-Roblox¦canonical_name=Roblox】 ?", "C'est quoi GTA ?", "C'est quoi 【entity-Brawl Stars¦canonical_name=Brawl Stars】 ?", "C'est quoi 【entity-Pokemon¦canonical_name=Pokemon】 ?"],
    "🚀 Espace": ["C'est quoi un trou noir ?", "C'est quoi le Big Bang ?", "C'est quoi Mars ?", "C'est quoi l'ISS ?", "C'est quoi le Soleil ?", "C'est quoi une galaxie ?"],
    "🧪 Science": ["Comment calculer la masse volumique ?", "C'est quoi un atome ?", "C'est quoi la gravite ?", "C'est quoi la photosynthese ?", "C'est quoi l'ADN ?"],
    "🧠 Culture G": ["C'est qui Werenoi ?", "C'est qui Ninho ?", "C'est qui Jul ?", "C'est quoi la Tour Eiffel ?", "C'est quoi le 【entity-Titanic¦canonical_name=Titanic】 ?", "C'est quoi 【entity-Harry Potter¦canonical_name=Harry Potter】 ?"],
    "🎤 Chanteurs": ["C'est qui Werenoi ?", "C'est qui Ninho ?", "C'est qui Jul ?", "C'est qui 【entity-Gazo¦canonical_name=Gazo】 ?", "C'est qui 【entity-Tiakola¦canonical_name=Tiakola】 ?", "C'est qui 【entity-PNL¦canonical_name=PNL】 ?", "C'est qui SDM ?", "C'est qui 【entity-Drake¦canonical_name=Drake】 ?", "C'est qui 【entity-Taylor Swift¦canonical_name=Taylor Swift】 ?", "C'est qui 【entity-Eminem¦canonical_name=Eminem】 ?"],
    "💰 Argent / Metiers": ["Comment devenir millionnaire ?", "C'est quoi un salaire ?", "C'est quoi un metier ?", "C'est quoi un entrepreneur ?", "Comment gagner de l'argent a 13 ans ?"],
    "🐾 Animaux": ["C'est quoi le plus grand animal ?", "C'est quoi le plus rapide ?", "C'est quoi un chien ?", "C'est quoi un chat ?"],
}

with st.sidebar:
    st.title("Agent IA V5")
    st.write("Clique sur un thème")
    for t in THEMES.keys():
        if st.button(t, key="side_"+t, use_container_width=True):
            st.session_state.theme = t
            st.rerun()
    st.divider()
    st.write("MATIERES ECOLE :")
    for m in MATIERES.keys():
        if st.button(m, key="side_m_"+m, use_container_width=True):
            st.session_state.theme = m
            st.rerun()
    st.divider()
    if st.button("Effacer"):
        st.session_state.messages = []
        st.rerun()

st.title("Agent IA V5")
st.caption("Fond noir discret - Tout inclus : Ecole + Bases + Calculatrice + Traductions + Fun + PC + Chanteurs + Avions + ...")

cols = st.columns(3)
for i, t in enumerate(list(THEMES.keys())):
    with cols[i % 3]:
        if st.button(t, key="top_"+t, use_container_width=True):
            st.session_state.theme = t
            st.rerun()

if st.session_state.theme == "📐 Ecole":
    st.subheader("TOUTES LES MATIERES ECOLE - Clique sur une matière :")
    cols2 = st.columns(4)
    for i, m in enumerate(list(MATIERES.keys())):
        with cols2[i % 4]:
            if st.button(m, key="mat_"+m, use_container_width=True):
                st.session_state.theme = m
                st.rerun()
    st.info("Clique sur une matière : Maths, Français, Allemand, Anglais, Histoire, Sciences, Chimie, Code")
else:
    if st.session_state.theme in MATIERES:
        st.subheader(f"Questions {st.session_state.theme} - Clique :")
        for q in MATIERES[st.session_state.theme]:
            if st.button(q, key="q_"+q, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": q})
                st.session_state.auto_q = q
                st.rerun()
        if st.button("Retour à toutes les matières", use_container_width=True):
            st.session_state.theme = "📐 Ecole"
            st.rerun()
    else:
        st.subheader(f"Questions {st.session_state.theme} - Clique :")
        for q in THEMES.get(st.session_state.theme, []):
            if st.button(q, key="q_"+q, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": q})
                st.session_state.auto_q = q
                st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Salut ! 👋 Moi c'est Agent IA V5. Je sais tout faire : Bonjour, Merci, Calculs (tape 12+8), Traductions, Blagues, Ecole, PC, Chanteurs, Avions... Essaie : Bonjour / Calcule 15x7 / Raconte une blague / C'est qui Werenoi ?"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ===== BASES / POLITESSE + FUN =====
BASES = {
    "bonjour": "Bonjour ! 👋 Comment tu vas ? Moi je vais super bien, merci ! Tu veux que je t'aide pour quoi aujourd'hui ? Tu peux me demander : une question d'école, un calcul, une traduction, une capitale, un chanteur, un PC, un avion... Essaie : C'est quoi Pythagore ? ou Calcule 12+8",
    "bonjoure": "Bonjour ! 👋 Comment tu vas ? Moi je vais super bien, merci ! Tu veux que je t'aide pour quoi aujourd'hui ?",
    "salut": "Salut ! 👋 Ca va ? Moi oui, je suis là pour t'aider ! Tu veux quoi ? Ecole, PC, chanteurs, avions, foot, calcul, traduction ? Dis-moi !",
    "yo": "Yo ! 👋 Ca va ? Tu veux que je t'aide pour quoi ?",
    "coucou": "Coucou ! 👋 Ca va bien ? Moi oui ! Tu veux que je t'aide pour l'école ou autre chose ?",
    "hello": "Hello ! 👋 Ca va ? Moi je parle français et anglais ! Tu peux me dire Bonjour, Merci, ou me poser une question d'école !",
    "hi": "Hi ! 👋 How are you ? Moi je vais bien ! Tu veux que je t'aide en français ou en anglais ?",
    "bonsoir": "Bonsoir ! 🌙 Comment tu vas ? Tu as passé une bonne journée ? Tu veux que je t'aide pour tes devoirs avant de dormir ?",
    "merci": "De rien ! 😊 Avec plaisir ! C'est normal, je suis là pour t'aider. Tu as une autre question ? Essaie : C'est qui Werenoi ? ou C'est quoi la masse volumique ?",
    "merci beaucoup": "De rien, avec grand plaisir ! 😊 Tu es trop gentil ! Si tu as une autre question, je suis là !",
    "mrc": "De rien ! 😊 T'inquiète, je suis là pour ça !",
    "thx": "You're welcome ! 😊 De rien !",
    "ca va": "Ca va super bien merci ! Et toi, ça va ? Tu as passé une bonne journée ? Tu veux que je t'aide pour tes devoirs ou pour autre chose ?",
    "cv": "Ca va super bien merci ! Et toi ? 😊",
    "comment ca va": "Ca va super bien merci ! Et toi, comment tu vas ? Tu as passé une bonne journée à l'école ?",
    "comment tu vas": "Je vais super bien merci ! Et toi ? 😊 Tu veux que je t'aide pour quoi ?",
    "au revoir": "Au revoir ! 👋 A très vite ! J'espère que je t'ai aidé ! Reviens quand tu veux, je suis là H24 ! Bonne journée ! 😊",
    "bye": "Bye ! 👋 A très vite ! Reviens quand tu veux !",
    "a plus": "A plus ! 👋 Bonne journée ! Reviens me voir quand tu veux !",
    "bonne nuit": "Bonne nuit ! 😴 Dors bien ! A demain ! Reviens me voir quand tu veux !",
    "bonne journee": "Bonne journée à toi aussi ! 😊 Merci ! A très vite !",
    "t appelles comment": "Moi je m'appelle Agent IA V5 ! 🤖 Et toi, tu t'appelles comment ? Moi je suis là pour t'aider pour l'école, les PC, les chanteurs, les avions, le foot... Tu veux que je t'aide pour quoi ?",
    "tu t appelles": "Moi c'est Agent IA V5 ! 🤖 Et toi, tu t'appelles comment ?",
    "c est quoi ton nom": "Mon nom c'est Agent IA V5 ! 🤖 Je suis ton assistant pour l'école et tout le reste ! Et toi, c'est quoi ton prénom ?",
    "qui es tu": "Moi je suis Agent IA V5 ! 🤖 Ton assistant créé par Lenny. Je peux t'aider pour : l'école (Maths, Français, Allemand, Anglais, Sciences...), les capitales, les avions, les PC, le foot, les jeux vidéo, les chanteurs, les calculs, les traductions... Tu veux quoi ?",
    "tu peux m aider": "Oui bien sûr ! 😊 Je peux t'aider pour tout : école, Maths, Français, PC, chanteurs, avions, foot, jeux vidéo, calculs, traductions... Dis-moi ta question ! Par exemple : C'est quoi Pythagore ? ou C'est qui Werenoi ?",
    "aide moi": "Oui bien sûr ! 😊 Dis-moi, c'est pour quoi ? Ecole ? PC ? Chanteurs ? Pose-moi ta question, je t'explique tout en détail !",
    "t es nul": "Ohh... 😅 Désolé si je t'ai pas aidé ! Dis-moi ce que tu voulais, je vais essayer de mieux t'expliquer. C'était pour quelle question ?",
    "t es trop fort": "Merciii ! 😊 Ca me fait trop plaisir ! Tu es trop gentil ! Tu as une autre question ?",
    "trop bien": "Merciii ! 😊 Content que ça te plaise ! Tu veux que je t'explique autre chose ?",
    "j ai compris": "Trop bien ! 😊 Bravo ! Tu as compris, c'est le plus important ! Tu veux que je te pose une question pour vérifier ou on passe à autre chose ?",
    "j ai pas compris": "T'inquiète, c'est normal ! 😊 Dis-moi ce que tu n'as pas compris, je vais te réexpliquer plus simplement, avec un autre exemple. C'était pour quelle question ?",
    "ok": "Ok ! 😊 Tu veux quoi maintenant ? Une autre question ?",
    "lol": "Haha 😂 ! Tu es marrant ! Tu as une question ou on rigole ?",
    "mdr": "Mdr 😂 ! Tu veux que je t'aide pour quoi ?",
    "tu as quel age": "Moi je n'ai pas d'âge, je suis un robot ! 🤖 Je suis né en 2025, grâce à Lenny ! Et toi, tu as quel âge ?",
    "t es un robot": "Oui ! 🤖 Je suis un robot, un Agent IA créé par Lenny. Je suis là pour t'aider H24, même quand ton PC est éteint !",
    "quelle heure": f"Il est {datetime.datetime.now().strftime('%H:%M')} ! ⏰ En Suisse !",
    "heure": f"Il est {datetime.datetime.now().strftime('%H:%M')} ! ⏰",
    "quelle date": f"On est le {datetime.datetime.now().strftime('%d/%m/%Y')} ! 📅",
}

BLAGUES = [
    "Pourquoi les plongeurs plongent-ils toujours en arrière ? Parce que sinon, ils tombent dans le bateau ! 😂",
    "Que dit un zéro à un huit ? Belle ceinture ! 😂",
    "Pourquoi les maths sont tristes ? Parce qu'elles ont trop de problèmes ! 😂",
    "Que dit une imprimante à une autre ? Tu as du papier ? 😂",
    "Pourquoi le livre de maths est déprimé ? Parce qu'il a trop de problèmes ! 😂",
    "Qu'est-ce qu'un chat dit à un autre chat ? Miaou, on joue ? 😂",
    "Pourquoi les poissons n'aiment pas jouer au foot ? Parce qu'ils ont peur des filets ! 😂",
    "Que fait une fraise sur un cheval ? Tagada tagada ! 🍓🐴😂",
    "Pourquoi les squelettes ne se battent pas ? Parce qu'ils n'ont pas de tripes ! 💀😂",
    "Comment appelle-t-on un chien qui n'a pas de pattes ? On ne l'appelle pas, on va le chercher ! 🐶😂",
]

MOTIVATIONS = [
    "Tu peux le faire ! 💪 Chaque erreur, c'est une leçon. Les plus grands ont tous échoué avant de réussir. Messi a été rejeté petit, il est devenu le meilleur ! Ne lâche rien !",
    "N'abandonne jamais ! 🔥 Si c'est dur, c'est que tu es en train d'apprendre. 10 minutes par jour, tous les jours, et dans 1 mois tu seras trop fort !",
    "Tu es capable de beaucoup plus que tu crois ! 🚀 Commence petit, 1 exercice, 1 page, et tu verras, ça va venir tout seul. Allez, on y va ensemble !",
    "Le succès, c'est 1% de talent et 99% de travail ! 💪 Tu as déjà fait le plus dur : tu es venu demander de l'aide. Maintenant, on continue !",
    "Rappelle-toi : Werenoi a commencé à 27 ans, Jul a été moqué au début, Eminem était pauvre. Ils n'ont jamais lâché. Toi aussi, tu peux réussir ! 🔥",
]

QUIZS = [
    "QUIZ 📚 : C'est quoi 7x8 ? Réponds-moi : 54, 56 ou 64 ?",
    "QUIZ 🌍 : C'est quoi la capitale du Japon ? Tokyo, Pékin ou Séoul ?",
    "QUIZ 🧮 : C'est quoi 15+25 ? 30, 40 ou 50 ?",
    "QUIZ ⚽ : Qui a gagné la Coupe du Monde 2022 ? France, 【entity-Argentine¦canonical_name=Argentine】 ou Brésil ?",
    "QUIZ 🔬 : C'est quoi la formule de la masse volumique ? m/V, m x V ou m+V ?",
    "QUIZ 🎤 : C'est qui qui a chanté Solitaire ? Werenoi, Ninho ou Jul ?",
    "QUIZ ✈️ : C'est quoi l'avion le plus performant en combat ? F-22, 【entity-F-35¦canonical_name=F-35】 ou Rafale ?",
    "QUIZ 📐 : C'est quoi a² + b² = c² ? Pythagore, Thales ou Newton ?",
]

TRADUCTIONS = {
    "bonjour en anglais": "Bonjour en anglais = Hello / Good morning ! 🇬🇧 Ex : Hello, how are you ? = Bonjour, comment tu vas ?",
    "bonjour en allemand": "Bonjour en allemand = Hallo / Guten Tag ! 🇩🇪 Ex : Hallo, wie geht's ? = Salut, ça va ?",
    "bonjour en espagnol": "Bonjour en espagnol = Hola / Buenos dias ! 🇪🇸 Ex : Hola, como estas ? = Salut, ça va ?",
    "bonjour en italien": "Bonjour en italien = Ciao / Buongiorno ! 🇮🇹",
    "merci en anglais": "Merci en anglais = Thank you / Thanks ! 🇬🇧 Ex : Thank you very much ! = Merci beaucoup !",
    "merci en allemand": "Merci en allemand = Danke ! 🇩🇪 Ex : Danke schön ! = Merci beaucoup !",
    "merci en espagnol": "Merci en espagnol = Gracias ! 🇪🇸",
    "merci en italien": "Merci en italien = Grazie ! 🇮🇹",
    "au revoir en anglais": "Au revoir en anglais = Goodbye / Bye ! 🇬🇧",
    "au revoir en allemand": "Au revoir en allemand = Auf Wiedersehen / Tschüss ! 🇩🇪",
    "ecole en anglais": "Ecole en anglais = School ! 🇬🇧 Ex : I go to school = Je vais à l'école.",
    "chat en anglais": "Chat en anglais = Cat ! 🐱 Chien = Dog 🐶",
    "chien en anglais": "Chien en anglais = Dog ! 🐶",
    "maison en anglais": "Maison en anglais = House ! 🏠",
    "pomme en anglais": "Pomme en anglais = Apple ! 🍎",
    "eau en anglais": "Eau en anglais = Water ! 💧",
}

CAPITALES = {
    "france": "Paris - 2,1M d'habitants, Tour Eiffel, Louvre, 330m. La France = 68M d'habitants, fromage, baguette, Paris = capitale depuis 987 !", "suisse": "Berne - Capitale de la Suisse depuis 1848. 140 000 habitants. Le Palais fédéral = là où on vote les lois. La Suisse = 8,9M d'habitants, 4 langues !", "allemagne": "Berlin - 3,6M d'habitants, Mur de Berlin tombé en 1989, Porte de Brandebourg.", "italie": "Rome - 2,8M d'habitants, fondée en -753, Colisée, Vatican, Pâtes, Pizza !", "espagne": "Madrid - 3,2M d'habitants, 【entity-Real Madrid¦canonical_name=Real Madrid】, Prado, Tapas.",
    "angleterre": "Londres - 9M d'habitants, Big Ben, Buckingham Palace, 2 000 ans d'histoire.", "japon": "Tokyo - 14M d'habitants, la plus grande ville du monde ! Sushi, Manga, Anime, Cerisiers, Mont Fuji.", "usa": "Washington D.C. - Capitale des USA, Maison Blanche, 700 000 habitants. New York = plus grande ville, pas la capitale !", "canada": "Ottawa - Capitale du Canada. Toronto = plus grande ville. 2 langues : français + anglais.", "chine": "Pékin - 21M d'habitants, Grande Muraille, Cité Interdite. Chine = 1,4 milliard d'habitants, le 2eme pays le plus peuplé !",
    "russie": "Moscou - 12M d'habitants, Place Rouge, Kremlin, -20° en hiver !", "bresil": "Brasilia - Capitale du Brésil. Rio = plus connue, avec le Christ Rédempteur, le Carnaval, le foot !", "inde": "New Delhi - Inde = 1,4 milliard d'habitants, le pays le plus peuplé du monde ! Taj Mahal à Agra.", "australie": "Canberra - Capitale de l'Australie. Sydney = plus connue, avec l'Opéra. Kangourous, Koalas !", "egypte": "Le Caire - 21M d'habitants, Pyramides de Gizeh à côté, Nil, Pharaons, 4500 ans d'histoire !",
    "maroc": "Rabat - Maroc, Couscous, Tajine, Marrakech, Sahara.", "algerie": "Alger - Algérie = plus grand pays d'Afrique !", "tunisie": "Tunis - Tunisie, Carthage, Plages.", "portugal": "Lisbonne - Portugal, Pastéis de Nata, 【entity-Cristiano Ronaldo¦canonical_name=CRISTIANO RONALDO】 !", "belgique": "Bruxelles - Belgique, Frites, Chocolat, Gaufres, Tintin !",
    "pays-bas": "Amsterdam - Pays-Bas, Canaux, Vélos, Tulipes.", "autriche": "Vienne - Autriche, Mozart, Valses, Alpes.", "suede": "Stockholm - Suède, IKEA, ABBA, Zlatan !", "norvege": "Oslo - Norvège, Fjords, Aurores boréales, Haaland !", "danemark": "Copenhague - Danemark, LEGO, La Petite Sirène.",
    "finlande": "Helsinki - Finlande, Père Noël, Saunas, 188 000 lacs !", "pologne": "Varsovie - Pologne, Chopin, Lewandowski.", "grece": "Athènes - Grèce, Démocratie née là, Jeux Olympiques, Zeus, Acropole !", "turquie": "Ankara - Turquie, Istanbul = plus grande ville, 2 continents : Europe + Asie !", "coree": "Séoul - Corée du Sud, K-Pop (【entity-BTS¦canonical_name=BTS】, 【entity-Blackpink¦canonical_name=Blackpink】), 【entity-Samsung¦canonical_name=Samsung】, Kimchi.",
    "thailande": "Bangkok - Thaïlande, Temples, Pad Thaï, Plages.", "vietnam": "Hanoï - Vietnam, Phở, Baie d'Ha Long.", "mexique": "Mexico - Mexique, Tacos, Aztèques, Frida Kahlo.", "【entity-argentine¦canonical_name=Argentine】": "Buenos Aires - 【entity-Argentine¦canonical_name=Argentine】, Tango, 【entity-Messi¦canonical_name=Messi】, Maradona, Steaks !", "chili": "Santiago - Chili, le plus long pays du monde, 4300 km !",
    "perou": "Lima - Pérou, Machu Picchu, Incas.", "colombie": "Bogota - Colombie, Café, 【entity-Shakira¦canonical_name=Shakira】.", "kenya": "Nairobi - Kenya, Safaris, Lions, Elephants.", "nigeria": "Abuja - Nigeria, 220M d'habitants, le plus peuplé d'Afrique !", "islande": "Reykjavik - Islande, Volcans, Aurores boréales, Geysers.",
    "irlande": "Dublin - Irlande, Trèfle, Saint-Patrick, 【entity-U2¦canonical_name=U2】.", "ukraine": "Kyiv - Ukraine, 38M d'habitants.", "roumanie": "Bucarest - Roumanie, Dracula, Transylvanie.", "hongrie": "Budapest - Hongrie, Danube, Bains thermaux.", "croatie": "Zagreb - Croatie, Mer Adriatique, 【entity-Modric¦canonical_name=Modric】.",
    "serbie": "Belgrade - Serbie, 【entity-Djokovic¦canonical_name=Djokovic】 !", "bulgarie": "Sofia - Bulgarie, Yaourt.", "israel": "Jérusalem - Israël, Ville sainte pour 3 religions.", "liban": "Beyrouth - Liban, Cèdres.", "irak": "Bagdad - Irak, Mésopotamie, première écriture !",
    "iran": "Téhéran - Iran, Perse, Tapis.", "arabie": "Riyad - Arabie Saoudite, Pétrole, La Mecque à côté.", "qatar": "Doha - Qatar, Coupe du Monde 2022 !", "monaco": "Monaco - 2 km², le 2eme plus petit pays ! Grand Prix F1, Casinos, Riches.", "luxembourg": "Luxembourg - Petit pays riche, 3 langues.",
    "malte": "La Valette - Malte, petite île en Méditerranée.", "andorre": "Andorre-la-Vieille - Andorre, entre France et Espagne, ski !", "liechtenstein": "Vaduz - Liechtenstein, 40 000 habitants, entre Suisse et Autriche.", "cuba": "La Havane - Cuba, Salsa, Cigares, Vieilles voitures.",
    "mali": "Bamako - Mali, Tombouctou, Musique.", "senegal": "Dakar - Sénégal, 【entity-Sadio Mané¦canonical_name=Sadio Mané】, Teranga.", "ghana": "Accra - Ghana, Cacao, Chocolat.", "cameroun": "Yaoundé - Cameroun, Lions Indomptables.", "madagascar": "Antananarivo - Madagascar, Lémuriens, Baobabs.",
    "pakistan": "Islamabad - Pakistan, 240M d'habitants.", "nepal": "Katmandou - Népal, Everest, 8848m, le plus haut sommet du monde !", "mongolie": "Oulan-Bator - Mongolie, Gengis Khan, Steppes, Chevaux.", "indonesie": "Jakarta - Indonésie, 270M d'habitants, 17 000 îles !", "philippines": "Manille - Philippines, 7000 îles.",
    "singapour": "Singapour - Ville-pays, la plus propre, la plus riche d'Asie !", "malaisie": "Kuala Lumpur - Malaisie, Tours Petronas.", "nouvelle-zelande": "Wellington - Nouvelle-Zélande, Seigneur des Anneaux, Kiwis, 【entity-All Blacks¦canonical_name=All Blacks】 !", "costa rica": "San José - Costa Rica, Pura Vida, Paresseux, Volcans.",
    "panama": "Panama - Canal de Panama, relie Atlantique et Pacifique !", "venezuela": "Caracas - Venezuela, Angel Falls, la plus haute cascade du monde (979m) !", "uruguay": "Montevideo - Uruguay, 1ère Coupe du Monde 1930.", "paraguay": "Asuncion - Paraguay.", "equateur": "Quito - Equateur, Galapagos, Darwin, Tortues géantes.",
    "bolivie": "Sucre - Bolivie, Salar d'Uyuni, le plus grand désert de sel !", "haiti": "Port-au-Prince - Haïti, première république noire.", "jamaique": "Kingston - Jamaïque, Bob Marley, Reggae, 【entity-Usain Bolt¦canonical_name=Usain Bolt】 !", "soudan": "Khartoum - Soudan, Nil.", "libye": "Tripoli - Libye, Sahara.", "ethiopie": "Addis-Abeba - Ethiopie, Café né là, Lucy, 3000 ans d'histoire.",
}

PC = {
    "rapport qualite prix": "MEILLEUR RAPPORT QUALITE / PRIX PC 2026 - EXPLICATION COMPLETE : Le rapport qualite / prix, c'est combien de FPS tu as pour chaque franc. Un PC a 4000 CHF est plus puissant, mais tu paies 2x plus cher pour seulement 20% de FPS en plus. Donc pas rentable. 1. GAGNANT 1300 CHF : RTX 5070 (600) + Ryzen 7 7800X3D (350) + 32 Go (120) + SSD 1 To (70) = 1300 CHF. Resultat : 1440p Ultra 180 FPS 【entity-Fortnite¦canonical_name=Fortnite】, 120 FPS GTA V, 100 FPS Warzone. 2. PETIT BUDGET 900 CHF : RTX 4060 + Ryzen 5 7600 = 900 CHF, 1080p 144 FPS. 3. GROS BUDGET 2000 CHF : RTX 5070 Ti + 9800X3D = 2000 CHF, 240 FPS, 4K 120 FPS. MON CONSEIL : Prends le 1300 CHF. C'est celui que 90% des gamers prennent.",
    "meilleur rapport": "MEILLEUR RAPPORT : PC 1300 CHF = RTX 5070 + 7800X3D = meilleur ! 900 CHF = RTX 4060 = pour debuter. 2000 CHF = RTX 5070 Ti = le roi.",
    "pc 900": "PC 900 CHF - DETAIL : GPU RTX 4060 (350 CHF) : 8 Go, 1080p Ultra, Fortnite 144 FPS. CPU Ryzen 5 7600 (180 CHF) : 6 coeurs. RAM 16 Go DDR5 (60 CHF). SSD 1 To NVMe (70 CHF) : Windows en 5 sec. Carte mere + Alim + Boitier (240 CHF). Total 900 CHF. Parfait pour debuter, Fortnite, Roblox, Minecraft, GTA V en 1080p.",
    "pc 1300": "PC 1300 CHF - DETAIL : GPU RTX 5070 (600 CHF) : 12 Go, 1440p Ultra, 180 FPS Fortnite, Ray Tracing. CPU Ryzen 7 7800X3D (350 CHF) : 8 coeurs + cache 3D, +30 FPS. RAM 32 Go DDR5 6000 MHz (120 CHF) : jeu + Discord + Chrome + Stream sans lag. SSD 1 To (70 CHF). Total 1300 CHF. C'est le meilleur rapport qualite prix en 2026.",
    "pc 2000": "PC 2000 CHF - DETAIL : GPU RTX 5070 Ti (850 CHF) : 16 Go, 4K 120 FPS, 1440p 240 FPS. CPU Ryzen 7 9800X3D (450 CHF) : le CPU gaming le plus rapide du monde. RAM 32 Go (120 CHF). SSD Samsung 990 PRO 2 To (180 CHF) : 7450 Mo/s. Carte mere B850 (180 CHF), Alim 850W Gold (110 CHF), Boitier (110 CHF). Total 2000 CHF. Pour le max, 240 FPS, 4K, streaming pro.",
    "meilleure gpu": "MEILLEURE GPU 2026 : 1. RTX 5090 - LA PLUS PUISSANTE, 32 Go, 4K Ultra 200 FPS, 2500 CHF. Pour pros / IA. 2. RTX 5080 - 16 Go, 4K 150 FPS, 1200 CHF. 3. RTX 5070 Ti - 16 Go, 1440p 200 FPS, 850 CHF. 4. RTX 5070 - MEILLEUR RAPPORT : 12 Go, 1440p 180 FPS, 600 CHF. 5. RTX 4060 - POUR DEBUTER : 8 Go, 1080p 144 FPS, 350 CHF. Conseil : RTX 5070 si tu as 600 CHF, RTX 4060 si tu as 350 CHF.",
    "gpu": "GPU = Carte Graphique. Elle calcule toutes les images de tes jeux, 60 a 240 fois par seconde. 【entity-NVIDIA¦canonical_name=NVIDIA】 = RTX (meilleures pour Ray Tracing et IA), 【entity-AMD¦canonical_name=AMD】 = RX (moins cheres). La GPU decide de tes FPS : RTX 4060 = 144 FPS en 1080p, RTX 5070 = 180 FPS en 1440p, RTX 5090 = 200 FPS en 4K. Sans bonne GPU, ton jeu lag meme avec un bon CPU.",
    "rtx 5090": "RTX 5090 : Plus puissante du monde, 32 Go, 4K Ultra, 2500 CHF. Pour pros, 3D, IA.",
    "rtx 5080": "RTX 5080 : 2eme, 16 Go, 4K fluide, 1200 CHF.",
    "rtx 5070": "RTX 5070 : MEILLEUR RAPPORT GPU ! 12 Go, 1440p Ultra, 600 CHF.",
    "rtx 4060": "RTX 4060 : Pour commencer, 8 Go, 【entity-Fortnite¦canonical_name=Fortnite】 144 FPS, 350 CHF.",
    "meilleur cpu": "MEILLEUR CPU 2026 : 1. Ryzen 9 9950X3D - ROI, 16 coeurs, jeux + montage, 700 CHF. 2. Ryzen 7 9800X3D - ROI GAMING, 8 coeurs + cache 3D, 450 CHF. 3. Ryzen 7 7800X3D - MEILLEUR RAPPORT, 8 coeurs + cache 3D, 350 CHF. Le cache 3D donne +30 FPS dans 【entity-Fortnite¦canonical_name=Fortnite】, 【entity-Minecraft¦canonical_name=Minecraft】, GTA. C'est pour ca que 【entity-AMD¦canonical_name=AMD】 est devant 【entity-Intel¦canonical_name=Intel】 en 2026 pour les jeux.",
    "cpu": "CPU = Processeur, cerveau du PC. Il calcule physique, IA, positions. 【entity-AMD¦canonical_name=AMD】 Ryzen ou 【entity-Intel¦canonical_name=Intel】 Core. En 2026, 【entity-AMD¦canonical_name=AMD】 est devant pour les jeux grace au cache 3D. Meilleur rapport = Ryzen 7 7800X3D (350 CHF).",
    "meilleur ssd": "MEILLEUR SSD : 1. 【entity-Samsung¦canonical_name=Samsung】 990 PRO 2 To - 7450 Mo/s, Windows en 5 sec, jeux en 2 sec, 180 CHF. 2. WD Black SN850X 1 To - 7300 Mo/s, 70 CHF, meilleur rapport. 3. Crucial T705 - PCIe 5.0, encore plus rapide. Conseil : prends toujours SSD NVMe, jamais HDD (1 min a demarrer). 1 To = 100 jeux, 2 To = 200 jeux.",
    "ssd": "SSD = Disque qui stocke Windows + jeux. NVMe = le plus rapide. HDD = vieux disque qui tourne, lent, a eviter. Avec SSD, PC demarre en 5 sec, sans SSD en 1 min. 【entity-Samsung¦canonical_name=Samsung】 990 PRO = meilleur, WD Black = meilleur rapport.",
    "meilleure ram": "MEILLEURE RAM : 32 Go DDR5 6000 MHz CL30. Parfait en 2026 : jeu + Discord + Chrome + Stream sans lag. 16 Go = minimum, ca lag si tu ouvres Discord + Chrome. 64 Go = montage video pro / IA. Marques : Corsair Vengeance, G.Skill Trident Z5. Prends toujours 2 barrettes de 16 Go, pas 1 de 32 Go, c'est 2x plus rapide (dual channel).",
    "ram": "RAM = Memoire vive. Elle stocke ce que ton PC utilise en ce moment. Si pas assez de RAM, ton PC rame. 16 Go = minimum. 32 Go DDR5 = parfait. 64 Go = pro.",
    "meilleur pc": "MEILLEUR PC ABSOLU : RTX 5090 + Ryzen 9 9950X3D + 32 Go + SSD 990 PRO 2 To = 4000 CHF, 4K Ultra 200 FPS. MEILLEUR RAPPORT = PC 1300 CHF : RTX 5070 + 7800X3D = 1300 CHF, 1440p Ultra 180 FPS. Difference de FPS petite, difference de prix enorme.",
    "pc gamer": "PC GAMER : 900 CHF = RTX 4060 = 144 FPS en 1080p, parfait pour debuter. 1300 CHF = RTX 5070 = 180 FPS en 1440p, LE MEILLEUR RAPPORT. 2000 CHF = RTX 5070 Ti = 240 FPS en 1440p / 120 FPS en 4K, le roi.",
    "ecran": "MEILLEUR ECRAN : 27 pouces 1440p 180Hz IPS (250 CHF) = parfait, net, fluide. 1080p 144Hz (150 CHF) = pas cher, bien pour debuter. 4K 240Hz OLED (800 CHF) = le top, couleurs parfaites, mais tres cher. Conseil : prends 1440p 180Hz.",
    "clavier": "MEILLEUR CLAVIER : Mecanique = chaque touche a son switch, plus rapide, plus agreable. Switches rouges = silencieux, bleus = clic. Redragon K552 (40 CHF) = mecanique pas cher et tres bon, meilleur rapport. 【entity-Logitech¦canonical_name=Logitech】 G Pro X (150 CHF) = meilleur absolu.",
    "souris": "MEILLEURE SOURIS : 【entity-Logitech¦canonical_name=Logitech】 G Pro X Superlight 2 - 60g, sans fil, souris des pros (150 CHF). Meilleur rapport = 【entity-Logitech¦canonical_name=Logitech】 G305 (40 CHF) = sans fil, legere, capteur tres bon. Une bonne souris, c'est 60g max, sans fil, capteur 25 000 DPI.",
    "fps": "FPS = Images par seconde. 30 FPS = ca lag, 60 FPS = fluide, 144 FPS = super fluide, 240 FPS = pro. Plus ta GPU est forte, plus tu as de FPS. Pour Fortnite competitif, il faut 144 FPS minimum. Pour jouer chill, 60 FPS suffit.",
    "ping": "PING = Temps de reponse internet. 10 ms = parfait, 30 ms = tres bien, 100 ms = ca lag, 200 ms = injouable. Pour baisser ton ping : cable Ethernet (pas WiFi), fibre, serveur proche. En Suisse, fibre = 5-10 ms.",
    "stream": "STREAM : Pour streamer : PC 1300 CHF suffit, OBS Studio (gratuit), micro Blue Yeti (100 CHF), camera 【entity-Logitech¦canonical_name=Logitech】 C920 (70 CHF), 2 ecrans (1 pour jouer, 1 pour le chat). Internet : 20 Mbps en upload minimum.",
}

CHANTEURS = {
    "werenoi": "WERENOI - HISTOIRE COMPLETE : Vrai nom Jeremy Bana Owona. Ne en 1994 a Melun. Il a commence le rap tard, en 2021, avec Guadalajara. Il a explose en 2023 avec Pyramide (diamant) et Solitaire. Style : Drill melodique, voix grave, textes sur la rue, la famille, l'argent, la melancolie. Albums : Pyramide (2023), Pyramide 2 (2024), Diamant Noir (2025). Le plus ecoute en France en 2024 et 2025, devant Ninho et Jul. Sons cultes : Solitaire, Ciao, La vie de luxe, Pyramide, Diamant Noir, Pétrole avec 【entity-Gazo¦canonical_name=Gazo】. Decede le 17 mai 2025 a 31 ans, d'un arret cardiaque. Il reste une legende, meme avec une carriere tres courte (4 ans).",
    "ninho": "NINHO - HISTOIRE COMPLETE : Vrai nom 【entity-William Nzobazola¦canonical_name=William Nzobazola】. Ne en 1996 a Villeneuve-Saint-Georges, grandi a Nemours. Il a commence a 15 ans, avec des freestyles sur YouTube. Il est le rappeur avec le plus de disques d'or et de diamant en France ! Record absolu. Albums : M.I.L.S (2016), M.I.L.S 2.0, Comme prevu, Destin, Jefe (2021), NI (2023). Style : Flow melodique, punchlines, trap + melodie. Feats : Lettre a une femme avec 【entity-Niska¦canonical_name=Niska】 = diamant, Tout en 1, Bolide allemand avec SDM. Sons cultes : Jefe, Lettre a une femme, Maman ne le sait pas, No Love. Il a fait Bercy plein 2 fois. C'est le boss du rap francais depuis 2018.",
    "jul": "JUL - HISTOIRE COMPLETE : Vrai nom 【entity-Julien Mari¦canonical_name=Julien Mari】. Ne en 1990 a Marseille. Il a commence en 2013 avec Sort le cross volé. C'est le rappeur le plus productif de France : 2 albums par an, parfois 3 ! Plus de 20 albums en 10 ans. Albums : Dans ma paranoïa, Je trouve pas le sommeil, La machine, C'est pas des LOL, La zone en personne, Decennie, Mise a jour... Style : Marseille, autotune, sons pour la voiture, l'ete, la rue. Il est tres proche de ses fans, il fait des feats avec des jeunes inconnus pour les aider. Sons cultes : Tchikita, JCVD, Bande organisee (avec SCH, Naps, 【entity-Kofs¦canonical_name=Kofs】...), 1 2 3, J'ai tout su. Son signe : la main en l'air. Il a vendu plus de 5M d'albums. C'est le rappeur prefere des jeunes en France.",
    " 【entity-gazo¦canonical_name=Gazo】": " 【entity-GAZO¦canonical_name=Gazo】 - HISTOIRE COMPLETE : Vrai nom Ibrahima Diakite. Ne en 1994 a Chateau Rouge, Paris. Il a commence avec Freeze Corleone dans le groupe 667. C'est lui qui a ramene la drill en France ! La drill, c'est un style de Chicago / Londres, sombre, basses lourdes. Albums : Drill FR (2021), KMT (2022), Apocalypse (2024). Style : Voix grave, flow drill, textes sombres. Collabs : 【entity-Tiakola¦canonical_name=Tiakola】, Ninho, Gims, Hamza. Sons cultes : Haine et Sex, Die, La Melo avec 【entity-Tiakola¦canonical_name=Tiakola】 (300M de vues !), Apocalypse, Tiki Taka. Il est devenu le roi de la drill.",
    " 【entity-tiakola¦canonical_name=Tiakola】": " 【entity-TIAKOLA¦canonical_name=Tiakola】 - HISTOIRE COMPLETE : Vrai nom 【entity-Tiakola¦canonical_name=Tiakola】 Diakite. Ne en 1996 a Bondy, membre de 4Keus. Il a commence avec 4Keus, puis en solo en 2022. Albums : Melo (2022) - diamant, BDLM (2024). Sa voix melodique est unique, il fait du afro, melodique, rap doux. Sons cultes : La Melo avec Gazo (tube de l'ete 2023), Gasolina avec Rsko, Meuda avec Ninho, Pona nini, Si j'savais avec Ninho et 【entity-Niska¦canonical_name=Niska】. Il est tres apprecie pour sa voix, sa douceur, ses melodies. Il a fait Bercy plein. L'un des plus ecoutes en France en 2024.",
    " 【entity-pnl¦canonical_name=PNL】": " 【entity-PNL¦canonical_name=PNL】 - HISTOIRE COMPLETE : 【entity-PNL¦canonical_name=PNL】 = Peace N Lovés. Duo de freres : Ademo (Tarik) et N.O.S (Nabil), de Corbeil-Essonnes, quartier des Tarterêts. Albums : Le monde Chico (2015), Dans la legende (2016), Deux freres (2019). Ils ne font presque jamais d'interviews, pas de reseaux, pas de feats. Ils restent mysterieux. Style : Cloud rap, planant, autotune, sons qui te font voyager. Textes sur la famille, la rue, la quete, la vie. Sons cultes : Le monde ou rien, DA, Naha, Au DD, Deux freres, 91's, Onizuka. Ils ont fait 2 Bercy pleins sans aucune promo. Le groupe le plus influent du rap francais des annees 2010.",
    "sdm": "SDM - HISTOIRE COMPLETE : Vrai nom Beni Mosabu. Ne en 1995 a Clamart. Repere par Booba qui l'a signe dans son label 92i. Albums : Ocho (2021), Liens du 100, A vie (2023), A nos corps (2024). Il a explose avec Bolide allemand avec Ninho (diamant). Style : Flow rapide, technique, punchlines, voix aigue. Tres fort en freestyle. Sons cultes : Bolide allemand, Jack Fuego, La zone, Cartier, Redescends. L'un des meilleurs techniciens du rap francais actuel.",
    " 【entity-maes¦canonical_name=MAES】": " 【entity-MAES¦canonical_name=MAES】 - HISTOIRE : Rappeur de Sevran. Album : Pure, Les derniers salopards, Omerta. Style : trap melodique, street. Sons cultes : Street, Dybala, Madrina avec Booba. Il a fait de la prison, puis il est revenu plus fort.",
    "sch": "SCH - HISTOIRE : Rappeur de Marseille, vrai nom 【entity-Julien Schwarzer¦canonical_name=Julien Mari】. Albums : Anarchie, JVLIVS, Autobahn. Style : sombre, technique, univers mafieux. Son culte : Bande organisee avec Jul, Naps, 【entity-Kofs¦canonical_name=Kofs】... = tube de l'ete 2020, 400M de vues. Il a aussi fait Mere, A7, Otto. L'un des meilleurs techniciens.",
    "booba": "BOOBA - HISTOIRE : Le Duc de Boulogne, legende du rap francais depuis 1995 avec Lunatic. Albums : Temps mort, Ouest Side, Ultra, Trone. Il a lance Ninho, SDM, 【entity-Gazo¦canonical_name=Gazo】, Damso, 【entity-Maes¦canonical_name=MAES】... Connu pour ses clashs, son label 92i, ses punchlines. Sons : DKR, Mona Lisa, Ratpi World.",
    "koba la d": "KOBA LA D - HISTOIRE : Rappeur francais, flow rapide, argot. Albums : VII, L'Affranchi. Sons : Train de vie, Dernier jour, Coffre plein.",
    " damso": " DAMSO - HISTOIRE : Rappeur belge / congolais. Albums : Batterie Faible, Ipséité, Lithopédion, QALF. Style : sombre, technique, punchlines. Sons cultes : Macarena (diamant), BruxellesVie, Feu de bois. Il a fait une pause, puis il est revenu avec QALF Infinity.",
    "dinos": "DINOS - HISTOIRE : Rappeur francais, tres technique. Albums : Imany, Taciturne, Stamina. Sons : Presque, Ciel pleure, Madone.",
    " laylow": " LAYLOW - HISTOIRE : Rappeur francais, univers futuriste. Albums : Trinity, L'Etrange Histoire de Mr Anderson. Style : autotune, electrique.",
    "nekfeu": "NEKFEU - HISTOIRE : Rappeur francais, membre de 1995 et S-Crew. Albums : Feu, Cyborg, Les etoiles vagabondes. Sons : On verra, Tricheur, Egotrip.",
    " lacrim": " LACRIM - HISTOIRE : Rappeur francais, style street. Albums : Force et Honneur, R.I.P.R.O. Sons : Corleone, Oh bah oui, Trahison.",
    " drake": " DRAKE - HISTOIRE : Rappeur canadien, le plus streamé au monde. Albums : Take Care, Nothing Was The Same, Scorpion, Her Loss. Sons cultes : God's Plan, One Dance, Hotline Bling, Started From The Bottom. Il a commence comme acteur dans Degrassi. Il a son label OVO.",
    " taylor swift": " TAYLOR SWIFT - HISTOIRE : Chanteuse americaine, la plus ecoutee au monde. Albums : 1989, Reputation, Midnights, The Tortured Poets Department. Elle a gagne 14 Grammy. Ses fans = les Swifties. Elle a commence en country, puis pop. Son Eras Tour = tournee la plus rentable de l'histoire (2 milliards $).",
    "weeknd": " THE WEEKND - HISTOIRE : Chanteur canadien, vrai nom Abel Tesfaye. Albums : After Hours, Starboy, Dawn FM. Son : Blinding Lights = chanson la plus ecoutee de tous les temps sur Spotify (4 milliards). Il a fait le Super Bowl en 2021.",
    "bad bunny": "BAD BUNNY - HISTOIRE : Chanteur portoricain, roi du reggaeton. Album : Un Verano Sin Ti. Son : Tití Me Preguntó, Dakiti. Il a fait le Super Bowl 2026 !",
    "billie eilish": "BILLIE EILISH - HISTOIRE : Chanteuse americaine, elle a commence a 14 ans avec Ocean Eyes. Albums : When We All Fall Asleep, Happier Than Ever, Hit Me Hard and Soft. Sons : Bad Guy, Birds of a Feather, What Was I Made For (Barbie). Elle a gagne 9 Grammy avant 22 ans.",
    "ed sheeran": "ED SHEERAN - HISTOIRE : Chanteur anglais, guitare + loop. Albums : Divide, =. Sons : Shape of You, Perfect, Thinking Out Loud. Shape of You = 4 milliards de streams.",
    "rihanna": "RIHANNA - HISTOIRE : Chanteuse de la Barbade. Albums : Anti, Good Girl Gone Bad. Sons : Diamonds, Umbrella, Work. Elle a aussi sa marque Fenty (maquillage + vetements), milliardaire !",
    "beyonce": "BEYONCE - HISTOIRE : Queen B, chanteuse americaine, ex Destiny's Child. Albums : Renaissance, Lemonade. 32 Grammy, record ! Sons : Crazy In Love, Single Ladies, Halo.",
    " eminem": " EMINEM - HISTOIRE : Rappeur americain, legende. Albums : The Slim Shady LP, The Marshall Mathers LP, Recovery. Sons : Lose Yourself (Oscar), Rap God (7 mots par seconde), Mockingbird, Without Me. Il a vendu 220M d'albums. C'est le rappeur le plus vendu de l'histoire.",
    "soprano": "SOPRANO - HISTOIRE : Chanteur / rappeur de Marseille. Albums : La Colombe, L'Everest, Chasseur d'etoiles. Sons : Cosmo, En feu, A la vie, a l'amour, Mon Everest avec Marina Kaye. Tres positif, famille, espoir. Il a commence dans le groupe Psy 4 de la Rime.",
    "m pokora": "M. POKORA - HISTOIRE : Chanteur francais, ex Popstars. Albums : R.E.D, Pyramide, Epicentre. Sons : Juste une photo de toi, Les planetes, Tombé.",
    "stromae": "STROMAE - HISTOIRE : Chanteur belge, vrai nom Paul Van Haver. Albums : Cheese, Racine carree, Multitude. Sons : Alors on danse, Papaoutai, Formidable, L'enfer. Il melange electro et chansons tristes sur la famille, la depression, la vie. Il a fait une pause de 7 ans pour sa sante mentale.",
}

TOUT = {
    "pythagore": "THEOREME DE PYTHAGORE - COURS COMPLET : Formule : a² + b² = c². Ca marche UNIQUEMENT pour un triangle rectangle (avec un angle droit de 90°). a et b = les 2 petits cotes (qui forment l'angle droit). c = l'hypotenuse, le plus grand cote, en face de l'angle droit. Exemple : Triangle 3-4-5. 3² + 4² = 9 + 16 = 25. Et 5² = 25. Donc ca marche ! Exemple pour trouver l'hypotenuse : Si a=6, b=8, alors c² = 36 + 64 = 100, donc c = 10. Exemple pour trouver un petit cote : Si c=13, b=5, alors a² = 169 - 25 = 144, donc a = 12. A quoi ca sert ? Pour construire une maison, pour savoir si un angle est droit, pour calculer une distance sans mesurer. Les Egyptiens l'utilisaient deja il y a 4000 ans pour les pyramides.",
    "thales": "THALES - COURS : Si 2 droites paralleles coupent 2 secantes, alors les rapports sont egaux. Formule : AB / AD = AC / AE = BC / DE. Ex : Si tu as un triangle avec une droite parallele a la base, tu peux calculer la longueur sans mesurer. Ca sert pour les ombres, les hauteurs d'arbres, les pyramides.",
    "moyenne": "MOYENNE - COURS : Moyenne = somme / nombre. Ex : Notes 12, 15, 18. Somme = 45. Nombre = 3. Moyenne = 45 / 3 = 15. Astuce : Si tu as une mauvaise note, il faut une bonne note pour compenser. Ex : 8 + 18 = 26 / 2 = 13. Moyenne pondérée : si le controle compte double, tu comptes 2 fois la note.",
    "aire": "AIRE - COURS COMPLET : Aire = surface. Rectangle = Longueur x largeur. Carre = cote x cote. Triangle = (base x hauteur) / 2. Cercle = pi x rayon² (pi = 3,14). Parallelogramme = base x hauteur. Trapeze = (grande base + petite base) x hauteur / 2. Ex : Cercle rayon 5 = 3,14 x 25 = 78,5 cm². Pour un terrain, une chambre, un jardin, tu calcules l'aire.",
    "perimetre": "PERIMETRE - COURS : Perimetre = tour. Carre = 4 x cote. Rectangle = 2 x (Longueur + largeur). Cercle = 2 x pi x rayon. Triangle = somme des 3 cotes. Ex : Carre 5 cm = 20 cm de tour. Ca sert pour une cloture, un cadre.",
    "volume": "VOLUME - COURS : Volume = place que ca prend. Cube = cote³. Pave = Longueur x largeur x hauteur. Cylindre = pi x rayon² x hauteur. Sphere = 4/3 x pi x rayon³. Ex : Boite 2x3x4 = 24 cm³. Ca sert pour une piscine, un carton, une bouteille.",
    "fraction": "FRACTION - COURS : Fraction = part d'un tout. 1/2 = la moitie, 1/4 = le quart. Pour additionner : il faut le meme denominateur. 1/2 + 1/4 = 2/4 + 1/4 = 3/4. Pour comparer : 1/2 > 1/3 car 1/2 = 3/6, 1/3 = 2/6. Pour multiplier : 2/3 x 3/4 = 6/12 = 1/2. Pour diviser : on multiplie par l'inverse.",
    "pourcentage": "POURCENTAGE - COURS : Pourcentage = pour 100. Formule : (partie / total) x 100. Ex : 20% de 50 = 0,20 x 50 = 10. Ex : Tu as 15/20 en controle : (15/20) x 100 = 75%. Les soldes : -30% sur 100 CHF = 70 CHF. Augmentation : +10% sur 50 CHF = 55 CHF.",
    "equation": "EQUATION - COURS : Equation = egalite avec un x a trouver. Methode : tu mets les x d'un cote, les chiffres de l'autre. Ex : 2x + 3 = 7. Tu enleves 3 des 2 cotes : 2x = 4. Tu divises par 2 : x = 2. Verif : 2x2+3 = 7, ca marche ! Ex 2 : 3x - 5 = 10 -> 3x = 15 -> x = 5.",
    "angle": "ANGLES - COURS : Droit = 90°, Plat = 180°, Plein = 360°. Triangle = 180° au total. Ex : Si un triangle a 90° et 60°, le 3eme = 180 - 90 - 60 = 30°. Angles complementaires = 90° a 2. Angles supplementaires = 180° a 2. Angles alternes-internes = egaux si paralleles.",
    "etre": "ETRE - CONJUGAISON COMPLETE : Present : je suis, tu es, il est, nous sommes, vous etes, ils sont. Passe compose : j'ai ete, tu as ete... Imparfait : j'etais, tu etais, il etait... Futur : je serai, tu seras, il sera... Ex : Je suis a l'ecole, Je suis content.",
    "avoir": "AVOIR - CONJUGAISON : Present : j'ai, tu as, il a, nous avons, vous avez, ils ont. Passe compose : j'ai eu. Imparfait : j'avais. Futur : j'aurai. Ex : J'ai 13 ans, J'ai un chien.",
    "aller": "ALLER - CONJUGAISON : Present : je vais, tu vas, il va, nous allons, vous allez, ils vont. Passe compose : je suis alle. Futur : j'irai. Ex : Je vais a l'ecole, Je vais au foot.",
    "faire": "FAIRE - CONJUGAISON : Present : je fais, tu fais, il fait, nous faisons, vous faites, ils font. Passe compose : j'ai fait. Futur : je ferai. Ex : Je fais mes devoirs, Je fais du foot.",
    "pluriel": "PLURIEL - REGLES : En general +s : chat -> chats. En -eau : bateau -> bateaux. En -al : cheval -> chevaux, journal -> journaux. En -ou : genou -> genoux, caillou -> cailloux, mais trou -> trous. Exceptions a apprendre par coeur.",
    "adjectif": "ADJECTIF - COURS : L'adjectif decrit un nom, il s'accorde en genre et nombre. Ex : grand garcon / grande fille / grands garcons / grandes filles. Beau -> belle, blanc -> blanche, nouveau -> nouvelle. Il se place avant ou apres le nom : un grand garcon, un garcon sympa.",
    "passe compose": "PASSE COMPOSE - COURS : Formule : avoir/etre au present + participe passe. Ex : J'ai mange, Je suis alle, Tu as joue, Nous avons fini. Avec etre (aller, venir, partir, arriver...) : Je suis alle, Elle est venue. Participe : mange, fini, pris, vu, bu, dit...",
    "imparfait": "IMPARFAIT - COURS : Pour une habitude, une description, une action longue dans le passe. Terminaisons : -ais, -ais, -ait, -ions, -iez, -aient. Ex : Quand j'etais petit, je jouais au foot. Il faisait beau. Je dormais. Contraire du passe compose qui est pour une action courte : Hier, j'ai joue au foot (passe compose, une fois).",
    "futur": "FUTUR - COURS : Pour parler de demain. Terminaisons : -ai, -as, -a, -ons, -ez, -ont. Ex : Je mangerai, tu mangeras, il mangera, nous mangerons... Pour -er : je parlerai. Pour -ir : je finirai. Pour irreguliers : je serai (etre), j'aurai (avoir), j'irai (aller).",
    "cod": "COD - COURS : COD = Complement d'Objet Direct. Il repond a la question Qui ? ou Quoi ? apres le verbe, sans preposition. Ex : Je mange une pomme. Je mange quoi ? Une pomme = COD. Je vois Lenny. Je vois qui ? Lenny = COD. Astuce : tu peux le remplacer par le, la, les : Je la mange.",
    "sujet": "SUJET - COURS : Le sujet, c'est qui fait l'action. Il repond a Qui est-ce qui ? Ex : Lenny mange. Qui est-ce qui mange ? Lenny = sujet. Le chat dort. Qui dort ? Le chat = sujet. Il peut etre un nom, un pronom, un groupe.",
    "der": "ALLEMAND - DER DIE DAS : der = masculin (der Mann = l'homme), die = feminin (die Frau = la femme), das = neutre (das Kind = l'enfant). Pluriel = die (die Kinder = les enfants). Il faut apprendre le genre par coeur avec chaque mot. Astuce : -chen = das (das Mädchen).",
    "sein": "SEIN (ETRE) - ALLEMAND : ich bin, du bist, er/sie/es ist, wir sind, ihr seid, sie sind. Ex : Ich bin 13 Jahre alt = J'ai 13 ans. Ich bin müde = Je suis fatigué.",
    "haben": "HABEN (AVOIR) - ALLEMAND : ich habe, du hast, er hat, wir haben, ihr habt, sie haben. Ex : Ich habe einen Hund = J'ai un chien.",
    "gehen": "GEHEN (ALLER) - ALLEMAND : ich gehe, du gehst, er geht, wir gehen, ihr geht, sie gehen. Ex : Ich gehe zur Schule = Je vais à l'école.",
    "to be": "TO BE - ANGLAIS : I am, You are, He/She/It is, We are, You are, They are. Ex : I am 13, He is happy, They are friends. Passe : I was, You were. Futur : I will be.",
    "to have": "TO HAVE - ANGLAIS : I have, You have, He has, We have, You have, They have. Ex : I have a dog.",
    "to go": "TO GO - ANGLAIS : I go, You go, He goes, We go, You go, They go. Passe : I went. Ex : I go to school.",
    "present perfect": "Present Perfect : have + participe. I have eaten = J'ai mange. I have played = J'ai joué. On l'utilise pour une action qui a un lien avec le present.",
    "photosynthese": "PHOTOSYNTHESE - COURS COMPLET : Formule : Soleil + Eau + CO2 = Oxygene + Sucre (glucose). Comment ? Les feuilles ont de la chlorophylle (pigment vert) qui capte la lumiere du Soleil. Les racines prennent l'eau dans le sol. Les feuilles prennent le CO2 dans l'air. Resultat : La plante fabrique son sucre pour grandir, et elle rejette de l'oxygene qu'on respire ! Pourquoi c'est important ? Sans photosynthese, pas d'oxygene, pas de vie sur Terre. C'est les plantes, les arbres, les algues qui font tout notre oxygene. C'est pour ca qu'il faut proteger les forets.",
    "planete": "PLANETES - COURS : 8 planetes : Mercure (la plus proche du Soleil, tres chaude), Venus (la plus chaude, 460°), Terre (la seule avec vie), Mars (rouge), Jupiter (la plus grosse, 1300x Terre), Saturne (anneaux), Uranus (bleue, couchee), Neptune (la plus loin, vent 2000 km/h). Pluton = planete naine depuis 2006. Astuce : Me Voici, Tout Mouillé, J'ai Suivi Un Nuage.",
    "gravite": "GRAVITE - COURS : La gravite nous attire vers la Terre. C'est Newton qui l'a decouverte en voyant une pomme tomber. Sur Terre, tout tombe a 9,81 m/s². Sur la Lune, tu es 6x plus leger car la Lune est plus petite. Sans gravite, on flotterait dans l'espace. C'est la gravite qui fait tourner la Lune autour de la Terre, et la Terre autour du Soleil.",
    "ciel bleu": "CIEL BLEU - COURS : La lumiere du Soleil est blanche, mais elle est composee de toutes les couleurs. L'air diffuse surtout le bleu (c'est la diffusion de Rayleigh). Donc on voit le ciel bleu. Le soir, le Soleil est bas, la lumiere traverse plus d'air, le bleu est deja parti, il ne reste que le rouge/orange, donc coucher de soleil rouge.",
    "coeur": "COEUR - COURS : Le coeur pompe le sang dans tout le corps. 100 000 battements par jour, 7 000 litres de sang par jour, 3 milliards de battements dans une vie ! Il a 4 parties : 2 oreillettes, 2 ventricules. Le sang rouge = avec oxygene, le sang bleu = sans oxygene. Sport = coeur plus fort.",
    "volcan": "VOLCAN - COURS : Un volcan, c'est une ouverture dans la Terre par ou sort du magma (roche fondue). Quand le magma sort, ca devient de la lave. Il y a 2 types : effusif (lave qui coule doucement, comme en Hawai) et explosif (ca explose, comme le Vesuve). Le plus actif d'Europe = Etna en Italie. Le plus dangereux = Yellowstone aux USA.",
    "saison": "SAISONS - COURS : Les saisons, ce n'est pas la distance au Soleil, c'est l'inclinaison de la Terre (23,5°). En ete, l'hemisphere Nord est penche vers le Soleil, donc jours longs, chaud. En hiver, il est penche loin, donc jours courts, froid. En Australie, c'est l'inverse ! Quand c'est l'ete chez nous, c'est l'hiver chez eux.",
    "foudre": "FOUDRE - COURS : La foudre, c'est une decharge electrique entre un nuage et le sol. Temperature : 30 000°C, 5x plus chaud que le Soleil ! Elle tombe quand le nuage est tres charge. Regle de securite : si tu entends le tonnerre, rentre. Pas sous un arbre, pas dans l'eau, pas pres d'un poteau. Compte les secondes entre eclair et tonnerre : 3 secondes = 1 km.",
    "continent": "CONTINENTS - COURS : 6 continents : Europe (44 pays), Afrique (54 pays, le plus chaud), Asie (le plus grand, 4,7 milliards d'habitants), Amerique (Nord + Sud), Oceanie (Australie + iles), Antarctique (glace, pas d'habitants, que des scientifiques). Il y a 195 pays dans le monde.",
    "ocean": "OCEANS - COURS : 5 oceans : Pacifique (le plus grand, 165M km²), Atlantique, Indien, Arctique (glace), Antarctique. L'ocean le plus profond = fosse des Mariannes, 11 km de profond, dans le Pacifique. On connait mieux la Lune que le fond des oceans !",
    "2eme guerre": "2EME GUERRE MONDIALE - COURS COMPLET : 1939-1945. 60M de morts. Causes : Hitler arrive au pouvoir en 1933 en Allemagne, il veut conquérir l'Europe. Il envahit la Pologne le 1er septembre 1939, la France et l'Angleterre declarent la guerre. Camp : Axe (Allemagne, Italie, Japon) vs Alliés (France, Angleterre, URSS, USA). Evenements : Debarquement en Normandie le 6 juin 1944, Liberation de Paris en aout 1944, Bombe atomique sur Hiroshima et Nagasaki en aout 1945, Capitulation allemande le 8 mai 1945, japonaise le 2 septembre 1945. En Suisse, on est resté neutre, on n'a pas fait la guerre.",
    "1ere guerre": "1ERE GUERRE MONDIALE - COURS : 1914-1918. 18M de morts. Cause : assassinat de l'archiduc François-Ferdinand a Sarajevo. Guerre des tranchées, gaz, Verdun, Somme. Fin : Armistice le 11 novembre 1918. Traité de Versailles en 1919.",
    "revolution": "REVOLUTION FRANCAISE - COURS : 1789. Le peuple en a marre du roi Louis XVI, des impots, de la faim. 14 juillet 1789 : Prise de la Bastille. 26 aout 1789 : Declaration des Droits de l'Homme (liberté, égalité, fraternité). 1793 : le roi est guillotiné. 1799 : Napoléon prend le pouvoir. Devise de la France : Liberté, Egalité, Fraternité.",
    "rome": "ROME - COURS : Rome fondée en -753 par Romulus et Remus (légende : élevés par une louve). Empire romain : le plus grand de l'Antiquité, de l'Angleterre à l'Egypte. Colisée, Aqueducs, Routes, Droit romain, Latin (qui donne le français, l'italien, l'espagnol). Chute en 476. Jules César, assassiné en -44.",
    "moyen age": "MOYEN AGE - COURS : 476-1492. Châteaux, chevaliers, croisades, peste noire (1347, 25M de morts), Jeanne d'Arc (1429, elle sauve Orléans, brûlée en 1431), Gutenberg invente l'imprimerie en 1450. Fin : 1492, Christophe Colomb découvre l'Amérique.",
    "egypte": "EGYPTE - COURS : Pyramides, Pharaons, Nil, Hiéroglyphes, Momies, Toutankhamon. Pyramide de Khéops : 146m, 2,3M de blocs, 20 ans de travail. Le Nil = fleuve qui donne la vie, crues qui fertilisent les champs. Cléopâtre = dernière reine.",
    "napoleon": "NAPOLEON - COURS : Napoléon Bonaparte, né en 1769 en Corse. Empereur de 1804 à 1815. Il a conquis presque toute l'Europe (Austerlitz 1805 = sa plus grande victoire). Il a créé le Code civil (les lois), les lycées, le franc, la Légion d'honneur. Défaite à Waterloo en 1815 contre les Anglais et Prussiens. Exilé à Sainte-Hélène, mort en 1821.",
    "masse volumique": "MASSE VOLUMIQUE - COURS COMPLET : Formule : masse volumique = masse / volume. On ecrit : Rho = m / V. Rho = lettre grecque rho. m = masse, en grammes (g) ou kg. Tu la mesures avec une balance. V = volume, en cm³ ou mL ou L. Tu le mesures avec une eprouvette graduee ou avec Longueur x largeur x hauteur pour un cube. Unites : g/cm³ ou kg/m³. 1 g/cm³ = 1000 kg/m³. Exemples : Eau = 1 g/cm³. 100g d'eau dans 100 cm³ = 100 / 100 = 1. Huile = 0,9 g/cm³. Elle flotte sur l'eau car 0,9 < 1. Fer = 7,8 g/cm³. Il coule car 7,8 > 1. Or = 19,3 g/cm³. Tres lourd ! Regle : Si masse volumique < 1, ca flotte. Si > 1, ca coule. C'est pour ca que le bois flotte (0,6) et le caillou coule (2,5). Exercice : Tu as un objet de 200g et 50 cm³. Masse volumique = 200 / 50 = 4 g/cm³. Il coule. Pour le controle : Apprends la formule, les unites, et 3 exemples (eau, huile, fer).",
    "densite": "DENSITE / MASSE VOLUMIQUE : Rho = m / V. Masse / Volume. Ex : 100g / 100 cm³ = 1 g/cm³ = eau. Huile 0,9 flotte, Fer 7,8 coule. Si < 1 ca flotte, si > 1 ca coule. C'est la meme chose que masse volumique, juste un autre nom.",
    "chimie": "CHIMIE - COURS : La chimie, c'est l'etude de la matiere. Atome = brique de base. Molecule = plusieurs atomes ensemble. H2O = eau (2 hydrogene + 1 oxygene). CO2 = dioxyde de carbone (1 carbone + 2 oxygene). O2 = oxygene qu'on respire. Tableau periodique = 118 elements : H, O, C, Fe (fer), Au (or)...",
    "atome": "ATOME - COURS : L'atome, c'est la plus petite brique de la matiere. Il a un noyau avec des protons (+) et des neutrons (0), et autour des electrons (-) qui tournent. Ex : Atome d'hydrogene = 1 proton + 1 electron. Atome d'oxygene = 8 protons + 8 electrons. Tout ce que tu vois est fait d'atomes !",
    "oxygene": "OXYGENE - COURS : O2. On respire O2, on rejette CO2. Sans oxygene, on meurt en 3 minutes. L'oxygene vient des plantes (photosynthese) et des algues dans l'ocean. 21% de l'air = oxygene, 78% = azote. Dans l'espace, pas d'oxygene, il faut une bouteille.",
    "electricite": "ELECTRICITE - COURS : Tension en Volts (V), Intensité en Ampères (A), Puissance en Watts (W). Formule : P = U x I. Circuit = pile + lampe + interrupteur + fils. En série : si une lampe grille, tout s'éteint. En parallèle : si une lampe grille, les autres restent allumées (c'est comme dans ta maison). Danger : 220V = mortel, ne jamais toucher une prise avec les doigts mouillés.",
    "vitesse": "VITESSE - COURS : Vitesse = distance / temps. v = d / t. Ex : Tu fais 100m en 10 sec, vitesse = 10 m/s = 36 km/h. Pour passer de m/s à km/h : x 3,6. Pour passer de km/h à m/s : / 3,6. Usain Bolt = 44 km/h max, Guépard = 110 km/h, Avion = 900 km/h.",
    "energie": "ENERGIE - COURS : Il y a plusieurs énergies : cinétique (mouvement), potentielle (hauteur), thermique (chaleur), électrique, chimique, solaire, éolienne. On ne crée pas d'énergie, on la transforme. Ex : Panneau solaire : lumière -> électricité. Centrale : charbon -> chaleur -> électricité.",
    "adn": "ADN - COURS : ADN = Acide Désoxyribonucléique. C'est ton code génétique, dans toutes tes cellules. Il dit si tu as les yeux bleus, bruns, si tu es grand, petit... Il est en forme de double hélice (2 brins qui s'enroulent). Tu as 50% de l'ADN de ton père, 50% de ta mère. Les jumeaux ont le même ADN. La police utilise l'ADN pour identifier les criminels.",
    "trou noir": "TROU NOIR - COURS COMPLET : Un trou noir, c'est un objet tellement lourd et tellement petit que meme la lumiere ne peut pas en sortir. Sa gravite est tellement forte qu'elle aspire tout. Comment ca se forme ? Quand une tres grosse etoile meurt, elle explose (supernova) puis elle s'ecrase sur elle-meme. Elle devient tellement dense que sa gravite devient infinie. Au centre de notre galaxie (Voie Lactee), il y a un trou noir super massif : Sagittarius A*, 4 millions de fois la masse du Soleil. Si tu tombes dans un trou noir, tu es etire comme un spaghetti (spaghettification) puis tu disparais. Personne ne sait ce qu'il y a dedans. En 2019, on a pris la premiere photo d'un trou noir (M87) avec un telescope geant.",
    "soleil": "SOLEIL - COURS : Le Soleil est une etoile, pas une planete. Temperature au centre : 15 millions de degres, a la surface : 5500°. Il est compose d'hydrogene et d'helium. Il nous donne lumiere et chaleur. Il va mourir dans 5 milliards d'annees en devenant une geante rouge, puis une naine blanche. Sans Soleil, pas de vie.",
    "galaxie": "GALAXIE - COURS : Une galaxie, c'est un groupe de milliards d'etoiles. Notre galaxie = Voie Lactee, 200 milliards d'etoiles, 100 000 annees-lumiere de diametre. La voisine = Andromede, 2,5 millions d'annees-lumiere, elle va nous percuter dans 5 milliards d'annees. Il y a 200 milliards de galaxies dans l'univers !",
    "big bang": "BIG BANG - COURS : Le Big Bang, c'est le debut de l'univers il y a 13,8 milliards d'annees. Tout etait concentre en un point minuscule, puis ca a explose et ca s'etend encore aujourd'hui. Au debut, il faisait des milliards de degres. Puis ca a refroidi, les atomes se sont formes, puis les etoiles, puis les galaxies, puis la Terre il y a 4,5 milliards d'annees.",
    "mars": "MARS - COURS : Mars = planete rouge, a cause du fer oxyde (rouille). Un jour sur Mars = 24h37, presque comme nous. Une annee = 687 jours. Temperature : -60° en moyenne. On y a envoye des robots : Perseverance, 【entity-Curiosity¦canonical_name=Curiosity】. Un jour, des humains iront. 【entity-Elon Musk¦canonical_name=Elon Musk】 veut y aller avec 【entity-SpaceX¦canonical_name=SpaceX】.",
    "iss": "ISS - COURS : ISS = Station Spatiale Internationale. Elle tourne autour de la Terre a 400 km d'altitude, a 28 000 km/h (tour de Terre en 90 min). 16 levers de soleil par jour ! Il y a 6 astronautes dedans en permanence. Ils font des experiences, ils cultivent des plantes, ils font du sport 2h par jour pour ne pas perdre leurs muscles.",
    "dinosaure": "DINOSAURES - COURS : Les dinosaures ont vecu il y a 230M a 66M d'annees. T-Rex = carnivore, 12m, dents de 15 cm. Diplodocus = herbivore, 25m, 30 tonnes. Ils ont disparu il y a 66M d'annees a cause d'une meteorite de 10 km qui a frappe le Mexique (Chicxulub). Les oiseaux sont les descendants des dinosaures !",
    "boucle": "BOUCLE - COURS : Une boucle, c'est pour repeter sans recopier. Ex : for i in range(1,6): print(i) -> affiche 1,2,3,4,5. Sans boucle, il faudrait ecrire 5 print. Avec boucle, 2 lignes. Ca sert pour les jeux, les tables, les listes.",
    "condition": "CONDITION - COURS : Une condition, c'est si... sinon... Ex : if age >= 18: print('Majeur') else: print('Mineur'). Si la condition est vraie, on fait la 1ere action, sinon la 2eme. Ca sert pour les jeux : si tu as 100 points, tu gagnes.",
    "variable": "VARIABLE - COURS : Une variable, c'est une boite qui stocke une valeur. Ex : age = 13, prenom = 'Lenny', note = 15. Tu peux la changer : age = 14. Ca sert pour tout en code.",
    "fonction": "FONCTION - COURS : Une fonction, c'est un bloc de code qu'on peut réutiliser. Ex : def dire_bonjour(): print('Bonjour'). Tu l'appelles avec dire_bonjour(). Ca évite de recopier le même code 10 fois. C'est comme une recette.",
    "liste": "LISTE - COURS : Une liste, c'est plusieurs valeurs dans une boite. Ex : notes = [12, 15, 18]. notes[0] = 12, notes[1] = 15. Tu peux ajouter : notes.append(20). Ca sert pour les scores, les joueurs, les inventaires dans les jeux.",
    "python": "PYTHON - COURS : Langage facile, celui de ton agent. Créé en 1991 par Guido van Rossum. Il est utilisé pour l'IA, les sites web, les jeux, les robots. Ex : print('Bonjour'). C'est le langage le plus appris au monde en 2026.",
    "html": "HTML - COURS : HTML = HyperText Markup Language. C'est le squelette d'un site. <h1>Titre</h1> <p>Texte</p> <img src='photo.jpg'> <a href='https://...'>Lien</a>. Sans HTML, pas de site.",
    "css": "CSS - COURS : CSS = Cascading Style Sheets. C'est le style d'un site : couleurs, tailles, positions. Ex : body { background-color: black; color: white; }. Sans CSS, ton site est tout blanc et moche.",
    " 【entity-messi¦canonical_name=Messi】": " 【entity-MESSI¦canonical_name=Messi】 - HISTOIRE COMPLETE : 【entity-Lionel Messi¦canonical_name=Lionel Messi】, ne en 1987 a Rosario, Argentine. Il a commence au 【entity-FC Barcelone¦canonical_name=FC Barcelone】 a 13 ans, apres que le club ait paye son traitement pour grandir (il ne grandissait pas). Carriere : Barcelone (2004-2021) : 672 buts, 35 trophees, dont 10 Liga, 4 Ligues des Champions. 【entity-PSG¦canonical_name=PSG】 (2021-2023). 【entity-Inter Miami¦canonical_name=Inter Miami】 (2023-...). Records : 8 Ballons d'Or (record), 91 buts en une annee civile (2012, record), 6 Souliers d'Or, 1 Coupe du Monde 2022 avec l'Argentine (enfin !). Style : Petit (1m70), gaucher, dribbles courts, vision incroyable, passes decisives, coups francs. Il est considere comme le meilleur joueur de tous les temps par beaucoup. Vie : Marié a Antonela, 3 enfants. Il est tres discret, pas de clash.",
    " 【entity-ronaldo¦canonical_name=Ronaldo】": " CRISTIANO 【entity-RONALDO¦canonical_name=Ronaldo】 - HISTOIRE COMPLETE : Cristiano 【entity-Ronaldo¦canonical_name=Ronaldo】, ne en 1985 a Madere, Portugal. Il a commence au Sporting, puis Manchester United, 【entity-Real Madrid¦canonical_name=Real Madrid】, Juventus, Al-Nassr. Records : 5 Ballons d'Or, meilleur buteur de l'histoire en selection (130 buts avec le Portugal), meilleur buteur de l'histoire de la Ligue des Champions (140 buts), 900 buts en carriere. Style : Grand (1m87), physique, vitesse, saut incroyable (2,93m de saut !), frappe puissante, coups francs, penaltys. Il est une machine a travailler. Il a gagne l'Euro 2016 avec le Portugal. Il est tres populaire sur Instagram (600M de followers, le plus suivi au monde).",
    " 【entity-mbappe¦canonical_name=Mbappe】": " 【entity-MBAPPE¦canonical_name=Mbappe】 - HISTOIRE COMPLETE : Kylian 【entity-Mbappe¦canonical_name=Mbappe】, ne en 1998 a Bondy, France. Il a commence a Monaco, puis 【entity-PSG¦canonical_name=PSG】, puis 【entity-Real Madrid¦canonical_name=Real Madrid】 en 2024. Records : Champion du Monde 2018 a 19 ans (il a marque en finale), meilleur buteur de la Coupe du Monde 2022 (8 buts, triplé en finale contre l'Argentine), meilleur buteur de l'histoire du 【entity-PSG¦canonical_name=PSG】 (256 buts). Style : Vitesse incroyable (36 km/h, le plus rapide du foot), dribbles, finition. Il est droitier mais joue a gauche pour rentrer et tirer. Il est le capitaine de l'equipe de France depuis 2023. Il veut gagner le Ballon d'Or et la Ligue des Champions avec le Real.",
    "ballon d'or": "BALLON D'OR - COURS : Trophee du meilleur joueur du monde chaque annee, vote par des journalistes. Cree en 1956. 【entity-Messi¦canonical_name=Messi】 en a 8 (record), 【entity-Ronaldo¦canonical_name=Ronaldo】 5, Cruyff 3, Platini 3, Van Basten 3. En 2024, c'est Rodri qui a gagne. En 2023, c'est 【entity-Messi¦canonical_name=Messi】.",
    "coupe du monde": "COUPE DU MONDE - COURS : Competition tous les 4 ans, 32 equipes avant, 48 equipes en 2026 (USA / Canada / Mexique). 2022 = Argentine gagne contre France en finale (3-3, tirs au but). 2018 = France gagne. 2014 = Allemagne. Le Bresil a gagne 5 fois, record. La prochaine : 2026, 104 matchs, 16 villes.",
    "ligue des champions": "LIGUE DES CHAMPIONS - COURS : Meilleure competition de clubs en Europe. 【entity-Real Madrid¦canonical_name=Real Madrid】 a gagne 15 fois, record ! Milan 7, Bayern 6, Liverpool 6, Barcelone 5. Finale 2024 : Real gagne contre Dortmund. Musique : la musique de la Ligue des Champions, tout le monde la connait !",
    "basket": "BASKET - COURS : 5 vs 5, panier a 3,05m, match 4x12 min en NBA. Michael Jordan = GOAT (6 titres NBA). LeBron James = 40 000 points, record. En France : Victor Wembanyama, 2m24, joue aux Spurs, futur MVP !",
    "tennis": "TENNIS - COURS : Federer (20 Grands Chelems, Suisse !), Nadal (22, roi de Roland-Garros, 14 fois !), Djokovic (24, record). Grand Chelem = 4 tournois : Open d'Australie, Roland-Garros, Wimbledon, US Open. Match en 3 sets gagnants.",
    "formule 1": "FORMULE 1 - COURS : 350 km/h ! 20 pilotes, 10 équipes. Verstappen (Red Bull) a gagné 2021, 2022, 2023, 2024. Hamilton (Ferrari) = 7 titres, record avec Schumacher. Leclerc (Monaco, Ferrari). Grand Prix de Monaco = le plus prestigieux. En Suisse, pas de GP depuis 1954.",
    " minecraft": " MINECRAFT - COURS COMPLET : Minecraft, cree par Notch (Markus Persson) en 2011, rachete par Microsoft en 2014 pour 2,5 milliards $. C'est le jeu le plus vendu au monde : 300M de copies ! Principe : monde infini en cubes, tu mines (tu casses des blocs), tu construis, tu survis. Modes : Survie (tu as faim, tu as des coeurs, les monstres t'attaquent la nuit : creeper, zombie, squelette, enderman), Creatif (tu as tout illimite, tu voles), Aventure, Spectateur. Mobs : Creeper (il explose, BOOM), Enderman (il se teleporte), Ender Dragon (boss final dans l'End), Wither. Pourquoi c'est genial ? Tu peux tout construire : maison, chateau, ville, ordinateur, meme un autre jeu dedans ! C'est utilise a l'ecole pour apprendre a coder (Minecraft Education).",
    " fortnite": " FORTNITE - COURS COMPLET : Fortnite, cree par Epic Games en 2017. Battle Royale : 100 joueurs sur une ile, le dernier vivant gagne. Modes : Battle Royale (avec construction), Zero Construction (sans construction, plus facile), Sauver le monde, Lego Fortnite, Rocket Racing, Festival (musique). Principe : Tu tombes en parachute, tu ramasses des armes (gris, vert, bleu, violet, orange = du moins fort au plus fort), tu construis des murs, tu te bats, la zone se retrecit. Skins : 2000+ skins, dont des collabs : Marvel, Star Wars, Dragon Ball, Naruto, Messi, Neymar, Ariana Grande... Esport : Fortnite World Cup 2019, Bugha a gagne 3M $ a 16 ans ! C'est le jeu le plus joue par les jeunes en France.",
    " roblox": " ROBLOX - COURS : Roblox, c'est pas un jeu, c'est une plateforme avec des millions de jeux crees par les joueurs. Cree en 2006. Jeux cultes : Brookhaven (tu vis une vie), Blox Fruits (tu deviens pirate), Pet Simulator, Doors, Murder Mystery 2. Tu peux creer ton propre jeu avec Roblox Studio et gagner des Robux (monnaie). 300M de joueurs par mois, surtout des jeunes.",
    "gta": "GTA V - COURS : Grand Theft Auto V, sorti en 2013, 190M de copies, 2eme jeu le plus vendu de l'histoire (apres Minecraft). Monde ouvert : Los Santos (Los Angeles). 3 personnages : Michael, Franklin, Trevor. Tu conduis, tu fais des missions, tu peux tout faire. GTA VI sort en 2026, a Vice City (Miami), avec Lucia et Jason. C'est le jeu le plus attendu de tous les temps.",
    "brawl stars": "BRAWL STARS - COURS : Jeu mobile de Supercell (Clash of Clans, Clash Royale). 3v3, tu choisis un Brawler (Shelly, Colt, Spike, Leon...). Modes : Gem Grab, Showdown (battle royale), Brawl Ball (foot). Gratuit, mais tu peux acheter des gems. 500M de téléchargements !",
    " mario": " MARIO - COURS : Plombier Nintendo, sauve Peach. Cree en 1981 par Shigeru Miyamoto. Jeux : Super Mario Bros, Mario Kart, Mario Party, Super Mario Odyssey. Frere : Luigi. Ennemi : Bowser. 800M de jeux vendus !",
    " pokemon": " POKEMON - COURS : Attrape-les tous ! Cree en 1996 au Japon par Satoshi Tajiri. 1000+ Pokemons. Pikachu = mascotte. Jeux : Pokemon Rouge, Or, Diamant, Ecarlate, Violet. Cartes Pokemon = les plus collectionnées au monde, une carte Dracaufeu = 500 000 $ ! Anime : Sacha et Pikachu, 25 ans d'aventure.",
    "tour eiffel": "TOUR EIFFEL - COURS COMPLET : A Paris, 330 metres (avec antenne), construite en 1889 par Gustave Eiffel pour l'Exposition Universelle. Au debut, les Parisiens la detestaient, ils voulaient la demolir ! Elle devait rester que 20 ans. Elle a 3 etages : 1er a 57m (resto), 2eme a 115m (vue), 3eme a 276m (vue panoramique). 10 100 tonnes de fer, 2,5 millions de rivets. Anecdotes : Elle grandit de 15 cm en ete (le fer se dilate avec la chaleur), elle est repeinte tous les 7 ans (60 tonnes de peinture), elle scintille la nuit avec 20 000 ampoules. C'est le monument le plus visite au monde : 7M de visiteurs par an. Symbole de la France.",
    "pyramide": "PYRAMIDES - COURS : En Egypte, construites il y a 4500 ans pour les Pharaons (rois). La plus grande = Kheops, 146m, 2,3 millions de blocs de pierre de 2,5 tonnes chacun ! Comment ils ont fait sans grues ? Avec des rampes, des cordes, 20 000 ouvriers pendant 20 ans. Dedans : chambres, couloirs, tresors. Les pyramides etaient blanches et brillantes au debut !",
    " titanic": " TITANIC - HISTOIRE COMPLETE : Le Titanic, paquebot anglais, le plus grand du monde en 1912. 269m, 46 000 tonnes, 2200 passagers. Il devait etre insubmersible. Le 14 avril 1912, il heurte un iceberg dans l'Atlantique Nord, a 23h40. Il coule en 2h40, a 2h20 le 15 avril. 1517 morts, 706 survivants. Pas assez de canots de sauvetage (20 pour 2200 personnes). Film 【entity-Titanic¦canonical_name=Titanic】 en 1997 avec 【entity-Leonardo DiCaprio¦canonical_name=Leonardo DiCaprio】 et Kate Winslet, 11 【entity-Oscars¦canonical_name=Oscars】, 2 milliards $ de recettes. C'est le film d'amour le plus connu. L'epave a ete retrouvee en 1985 a 3800m de profondeur. Elle est en train de disparaitre a cause des bacteries.",
    " 【entity-harry potter¦canonical_name=Harry Potter】": "【entity-HARRY POTTER¦canonical_name=Harry Potter】 - COURS : Sorcier avec une cicatrice en eclair, ecrit par J.K. Rowling. 7 livres, 8 films, 500M de livres vendus. Histoire : Harry, orphelin, decouvre qu'il est sorcier a 11 ans, il va a Poudlard, il se bat contre Voldemort. Maisons : Gryffondor, Serpentard, Poufsouffle, Serdaigle. Personnages : Hermione, Ron, Dumbledore, Hagrid, Rogue.",
    "one piece": "ONE PIECE - COURS : Manga le plus vendu au monde (500M de tomes). Luffy veut devenir Roi des Pirates. Il a mangé le Fruit du Démon, il est en caoutchouc. Equipage : Zoro, Nami, Usopp, Sanji, Chopper, Robin, Franky, Brook, Jinbe. Auteur : Eiichiro Oda, depuis 1997, 1100+ chapitres !",
    "naruto": "NARUTO - COURS : Ninja qui veut devenir Hokage. Rasengan, Chidori, Kyubi (démon renard à 9 queues). Auteur : Masashi Kishimoto. Suite : Boruto (son fils).",
    "dragon ball": "DRAGON BALL - COURS : Goku, Super Saiyan, Kamehameha ! Auteur : Akira Toriyama. Goku ramasse 7 Dragon Balls pour exaucer un voeu. Transformations : Super Saiyan 1, 2, 3, Blue, Ultra Instinct. Ennemis : Vegeta (puis ami), Freezer, Cell, Buu.",
    "millionnaire": "COMMENT DEVENIR MILLIONNAIRE ? - COURS COMPLET : Il y a 4 chemins : 1. Salarié + investissement : tu gagnes 5000 CHF / mois, tu mets 1000 CHF / mois en bourse (ETF), en 30 ans tu as 1M. C'est le plus sûr. 2. Entrepreneur : tu crées un business (agent IA, boutique, appli...), tu vends à beaucoup de gens. C'est le plus rapide, mais le plus dur. 3. Créateur : YouTube, TikTok, 【entity-Twitch¦canonical_name=Twitch】, tu crées du contenu, tu gagnes avec les pubs et sponsors. 4. Sport / Art : footballeur, chanteur, acteur. Le plus dur. Conseils : Apprends une compétence (code, vente, design), épargne 20% de ce que tu gagnes, investis tôt, ne dépense pas pour impressionner. A 13 ans, tu ne peux pas encore investir, mais tu peux apprendre à coder, à vendre, à créer. C'est ce que tu fais avec ton agent !",
    "salaire": "SALAIRE - COURS : Salaire = argent que tu gagnes chaque mois pour ton travail. En Suisse : salaire moyen = 6500 CHF / mois. Serveur = 4500 CHF, Enseignant = 7000 CHF, Médecin = 12 000 CHF, Développeur = 8000 CHF, Footballeur pro = 100 000 CHF / mois ! Brut = avant impôts, Net = après impôts (ce que tu touches vraiment).",
    "metier": "METIER - IDEES : Développeur (code, 8000 CHF / mois), Médecin (12 000 CHF), Avocat (9000 CHF), Pilote (10 000 CHF), Ingénieur (8500 CHF), Enseignant (7000 CHF), Infirmier (6500 CHF), Electricien (6000 CHF), Cuisinier (5500 CHF), Youtubeur (0 à 1M, variable). Le meilleur métier, c'est celui que tu aimes + qui paie bien + qui est utile.",
    "entrepreneur": "ENTREPRENEUR - COURS : Entrepreneur = quelqu'un qui crée son entreprise. Ex : 【entity-Elon Musk¦canonical_name=Elon Musk】 (【entity-Tesla¦canonical_name=Tesla】, 【entity-SpaceX¦canonical_name=SpaceX】), 【entity-Jeff Bezos¦canonical_name=Jeff Bezos】 (【entity-Amazon¦canonical_name=Amazon】), 【entity-Mark Zuckerberg¦canonical_name=Mark Zuckerberg】 (【entity-Facebook¦canonical_name=Facebook】). Qualités : ne pas avoir peur d'échouer, travailler beaucoup, écouter les clients, apprendre tous les jours. En Suisse, à 13 ans tu ne peux pas créer d'entreprise seul, il faut 16 ans + autorisation parents. Mais tu peux déjà apprendre, créer des projets, comme ton agent !",
    "gagner de l argent": "COMMENT GAGNER DE L'ARGENT A 13 ANS EN SUISSE ? : Tu ne peux pas encore facturer seul, ni ouvrir Stripe, ni créer une entreprise. Solutions : 1. Petits services : aider voisins (tondre, promener chien, aider ordi) = 10-20 CHF. 2. Vendre ce que tu n'utilises plus (jeux, vêtements). 3. Créer un projet (agent IA, site, chaîne YouTube) et montrer à tes parents, ils peuvent facturer pour toi. 4. Apprendre une compétence (code, design, montage vidéo) pour être prêt à 16 ans. A 16 ans, tu peux t'inscrire comme indépendant AVS avec autorisation parents.",
    "plus grand animal": "PLUS GRAND ANIMAL : Baleine bleue ! 30m, 200 tonnes, coeur = 600 kg (taille d'une voiture), langue = 4 tonnes ! Elle mange du krill (petites crevettes), 4 tonnes par jour. Elle est plus grande qu'un dinosaure !",
    "plus rapide": "PLUS RAPIDE : Guépard = 110 km/h sur terre. Faucon pèlerin = 390 km/h en piqué (l'animal le plus rapide du monde !). Poisson voilier = 110 km/h dans l'eau. 【entity-Usain Bolt¦canonical_name=Usain Bolt】 = 44 km/h (humain le plus rapide).",
    "chien": "CHIEN - COURS : Meilleur ami de l'homme depuis 15 000 ans. 400 races : Labrador (gentil), Berger Allemand (police), Chihuahua (petit), Husky (neige). Un chien comprend 150 mots, il sent 100 000x mieux que nous, il entend 4x mieux. Il vit 10-15 ans.",
    "chat": "CHAT - COURS : Chat domestique depuis 9000 ans en Egypte. Il dort 16h par jour ! Il a 32 muscles dans chaque oreille, il peut sauter 6x sa hauteur, il retombe toujours sur ses pattes. Il ronronne quand il est content, mais aussi quand il a mal. Il vit 12-18 ans.",
    "conseil pour reviser": "CONSEIL POUR REVISER - TOP 5 : 1. Pomodoro : 25 min de travail, 5 min de pause, 4 fois, puis 30 min de pause. 2. Relis pas, teste-toi : fais des quiz, cache tes notes, essaie de te rappeler. 3. Explique à quelqu'un : si tu peux l'expliquer, tu as compris. 4. Dors bien : ton cerveau range ce que tu as appris pendant la nuit. 5. Pas de téléphone pendant que tu révises, mets-le en mode avion. Tu vas réussir ! 💪",
    "systeme solaire": "SYSTEME SOLAIRE - COURS : 8 planètes autour du Soleil : Mercure, Vénus, Terre, Mars, Jupiter, Saturne, Uranus, Neptune. Le Soleil = 99% de la masse du système. La Terre = 150M km du Soleil, 1 an = 365 jours. Jupiter = la plus grosse, Saturne = anneaux. Il y a aussi des astéroïdes, des comètes, des lunes (la Lune pour nous, 79 lunes pour Jupiter !).",
    "vitesse lumiere": "VITESSE DE LA LUMIERE : 300 000 km / seconde ! C'est la vitesse la plus rapide de l'univers. En 1 seconde, la lumière fait 7 fois le tour de la Terre ! Soleil -> Terre = 8 minutes. Soleil -> Neptune = 4 heures. Proxima Centauri (étoile la plus proche) = 4,2 années-lumière.",
}

AVIONS = {
    "f-22": "F-22 RAPTOR - COURS COMPLET : Pays : USA. Premier vol : 1997. Prix : 150M $ par avion. Nombre : 195 exemplaires seulement, jamais vendu a d'autres pays, trop secret ! Vitesse : Mach 2.25 (2400 km/h). Plafond : 20 000m. Furtif : presque invisible au radar, grace a sa forme et sa peinture speciale. Pourquoi c'est le plus performant en combat ? 1. Furtif : l'ennemi ne le voit pas. 2. Super maniable : il peut tourner a 60° par seconde, faire des cobra. 3. Super croisiere : il vole a Mach 1,5 sans postcombustion (il economise du carburant). 4. Capteurs : il voit l'ennemi a 200 km. En dogfight, il n'a jamais ete battu en exercice. Contre le F-35, il gagne 90% du temps en combat aerien pur.",
    " f-35": " F-35 LIGHTNING II - COURS COMPLET : Pays : USA. Premier vol : 2006. Prix : 80M $. Nombre : 1000+ exemplaires, vendu a 20 pays, dont la Suisse (36 exemplaires pour 6 milliards CHF) ! Vitesse : Mach 1.6 (1900 km/h). Furtif, mais moins que le F-22. Son point fort : ses capteurs et son informatique. Il voit tout a 360°, il partage les infos avec les autres avions. Il existe en 3 versions : 【entity-F-35A¦canonical_name=F-35】 (classique), 【entity-F-35B¦canonical_name=F-35】 (il peut decoller verticalement, comme un helicoptere), 【entity-F-35C¦canonical_name=F-35】 (pour les porte-avions). Role : Attaque au sol, reconnaissance, furtif, guerre electronique. C'est l'avion le plus moderne, le plus intelligent. C'est celui que la Suisse a choisi en 2021.",
    "su-57": "SU-57 FELON - COURS : Chasseur furtif russe, premier vol 2010. Vitesse Mach 2.0. Tres maniable, il peut faire le cobra (nez en l'air a 120°). Mais peu produit : 30 exemplaires seulement, car trop cher pour la Russie. Il est moins furtif que le F-22 / 【entity-F-35¦canonical_name=F-35】.",
    "j-20": "J-20 MIGHTY DRAGON - COURS : Chasseur furtif chinois, premier vol 2011. Vitesse Mach 2.0. Gros, furtif, pour attaquer de loin avec des missiles longue portee. La Chine en a 200+. Il est moins maniable que le F-22, mais il est bon pour attaquer les avions ravitailleurs et les AWACS.",
    "rafale": "RAFALE - COURS COMPLET : Pays : France, par 【entity-Dassault Aviation¦canonical_name=Dassault Aviation】. Premier vol : 1986, en service depuis 2001. Prix : 100M €. Vitesse : Mach 1.8 (1900 km/h). Polyvalent : il peut tout faire : combat aerien, attaque au sol, attaque en mer, reconnaissance, dissuasion nucleaire (il peut larguer une bombe nucleaire). Pays utilisateurs : France, Inde (36), Grece, Croatie, Egypte, Qatar, Emirats, Indonesie... Pourquoi il est aime ? Parce qu'il est tres maniable, tres fiable, et il peut decoller d'un porte-avions (Charles de Gaulle). C'est le meilleur avion polyvalent europeen. En exercice contre le F-22, il a deja reussi a le verrouiller (a le viser) une fois, ce qui est un exploit.",
    "eurofighter": "EUROFIGHTER TYPHOON - COURS : Construit par Allemagne, UK, Italie, Espagne. Vitesse Mach 2.0. Tres rapide en combat aerien, tres maniable. Il est moins furtif que le 【entity-F-35¦canonical_name=F-35】, mais il est plus rapide. Utilise par 9 pays.",
    "f-16": "F-16 FIGHTING FALCON - COURS : Le chasseur le plus produit au monde : 4600 exemplaires ! Vitesse Mach 2.0. Petit, agile, pas cher (30M $). Utilise par 25 pays, dont la Belgique, les Pays-Bas, l'Ukraine. Il a 50 ans mais il est encore utilise car il est fiable et facile a entretenir.",
    "f-15": "F-15 EAGLE - COURS : Vitesse Mach 2.5 ! 104 victoires a 0 defaite en combat reel, legende ! C'est le seul avion avec un ratio parfait. Il a ete utilise par les USA, Israel, Japon, Arabie Saoudite. Il peut porter 10 tonnes de missiles.",
    "f-18": "F/A-18 HORNET - COURS : Avion embarque sur porte-avions. Vitesse Mach 1.8. La Suisse l'utilise aussi (30 F/A-18 Hornet suisses, achetes en 1996). Il va etre remplace par le 【entity-F-35¦canonical_name=F-35】 en Suisse des 2028. Il peut atterrir sur un porte-avions avec un crochet.",
    "gripen": "GRIPEN - COURS : Suede. Vitesse Mach 2.0. Petit, pas cher (50M $), peut atterrir sur une autoroute ! La Suede l'a concu pour la guerre : si les aeroports sont detruits, il peut decoller d'une route. Il est utilise par la Suede, le Bresil, l'Afrique du Sud.",
    "su-35": "SU-35 - COURS : Russie. Vitesse Mach 2.25. Super maniable, il peut faire le cobra (nez en l'air a 120°) et le kulbit (looping complet). Il est tres impressionnant en meeting aerien. Mais il n'est pas furtif.",
    "mig-29": "MiG-29 - COURS : Russie. Vitesse Mach 2.25. Rival du F-16 pendant la Guerre Froide (USA vs URSS). Il est encore utilise par 20 pays, dont l'Inde, l'Ukraine.",
    "a-10": "A-10 WARTHOG - COURS : USA. Vitesse lente, 700 km/h, mais avec un canon geant de 30mm qui tire 3900 balles par minute et detruit les tanks ! Surnom : le sanglier, car il est moche mais tres efficace. Il vole bas, il est blinde, il peut rentrer avec une aile cassee.",
    "sr-71": "SR-71 BLACKBIRD - COURS : USA. Vitesse Mach 3.3 = 3500 km/h ! L'avion le plus rapide de tous les temps. Aucun missile ne l'a jamais touche. Il volait a 25 000m, tellement haut que les pilotes voyaient la courbure de la Terre. Il etait utilise pour espionner l'URSS. Retire en 1998.",
    "a380": " AIRBUS A380 - COURS : Le plus gros avion de passagers. 2 etages, 850 passagers max ! Longueur 73m, envergure 80m. 【entity-Emirates¦canonical_name=Emirates】 en a le plus (116). Il a 4 moteurs. Il a arrete d'etre produit en 2021 car trop gros, trop cher en carburant. Mais il est encore utilise pour les gros vols (Dubai - Londres).",
    "concorde": "CONCORDE - COURS : Avion supersonique ! Paris-New York en 3h30 au lieu de 8h. Mach 2 = 2x vitesse du son (2150 km/h). Il volait a 18 000m. Billet : 10 000 € aller-retour ! Arrete en 2003 apres le crash de Gonesse en 2000 et le 11 septembre. C'etait le seul avion de ligne supersonique avec le Tupolev Tu-144 russe.",
    "comment vole": "COMMENT VOLE UN AVION ? - COURS : L'aile est courbee en haut, plate en bas. L'air va plus vite au-dessus, donc pression plus faible au-dessus, pression plus forte en dessous. Ca cree une force vers le haut = portance. C'est le principe de Bernoulli. Pour decoller, il faut aller vite (250 km/h pour un A380). Pour atterrir, on sort les volets pour augmenter la portance a basse vitesse.",
    "pilote": "PILOTE - COURS : Pour devenir pilote, il faut 200h de vol, licence PPL puis CPL, beaucoup de maths / physique, anglais parfait, et etre en super forme. Formation : 2 ans, 100 000 CHF. Salaire : 8000-15000 CHF / mois en Suisse (SWISS), 5000 CHF au debut. Tu peux devenir pilote de ligne, pilote de chasse, pilote d'helicoptere, pilote prive.",
}

def toutes_tables():
    txt = "TOUTES LES TABLES DE MULTIPLICATION 1 a 12 :\n\n"
    for n in range(1, 13):
        txt += f"Table de {n} : " + ", ".join([f"{n}x{i}={n*i}" for i in range(1, 11)]) + "\n\n"
    txt += "\nASTUCE : Pour apprendre, dis-les a voix haute 3 fois, puis cache et recite. 7x8=56, 6x7=42, 8x8=64 sont les plus durs !"
    return txt

def table_division(n):
    txt = f"TABLE DE DIVISION DE {n} :\n"
    for i in range(1, 11):
        txt += f"{n*i} / {n} = {i}  |  "
    return txt

def calculer(q):
    try:
        # Nettoie
        txt = q.lower().replace("calcule", "").replace("calcul", "").replace("=", "").replace("?", "").strip()
        txt = txt.replace("x", "*").replace("×", "*").replace(",", ".")
        # Securite : que des chiffres et +-*/(). 
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in txt) or txt == "":
            return None
        res = eval(txt)
        return f"🧮 Calcul : {q} = {res} ! Bravo !"
    except:
        return None

def trouver(q_orig):
    q_low = q_orig.lower().strip()
    # --- CALCULATRICE EN PRIORITE ---
    if any(c in q_low for c in ["+", "x", "*", "/", "-"]) and any(c.isdigit() for c in q_low):
        calc = calculer(q_low)
        if calc:
            return calc
    # --- BASES ---
    q_net = q_low.replace("!", "").replace("?", "").replace(".", "").strip()
    for cle, rep in BASES.items():
        if cle in q_net or q_net == cle:
            return rep
    if "merci" in q_net:
        return BASES["merci"]
    if "bonjour" in q_net or "salut" in q_net:
        return BASES["bonjour"]
    # --- FUN ---
    if "blague" in q_net:
        return random.choice(BLAGUES)
    if "motive" in q_net or "motivation" in q_net or "je suis nul" in q_net or "j y arrive pas" in q_net:
        return random.choice(MOTIVATIONS)
    if "quiz" in q_net:
        return random.choice(QUIZS)
    if "conseil" in q_net and "revis" in q_net:
        return TOUT["conseil pour reviser"]
    if "heure" in q_net:
        return BASES["quelle heure"]
    if "date" in q_net:
        return BASES["quelle date"]
    # --- TRADUCTIONS ---
    if "traduis" in q_net or "traduction" in q_net or "en anglais" in q_net or "en allemand" in q_net or "en espagnol" in q_net:
        for cle, rep in TRADUCTIONS.items():
            if cle in q_net:
                return rep
        return "Je peux traduire : bonjour, merci, au revoir, école, chat, chien, maison, pomme, eau en anglais / allemand / espagnol / italien. Essaie : Traduis bonjour en anglais"

    q = q_low
    for mot in ["c'est quoi", "c est quoi", "c'est", "comment", "pourquoi", "donne-moi", "donne moi", "c'est qui", "qui est", "quel est", "quelle est", "comment calculer", "?"]:
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
        return "AVION LE PLUS PERFORMANT ? 1. Combat : F-22 Raptor - meilleur, furtif, jamais battu. 2. Moderne : F-35 - fait tout, Suisse a choisi. 3. Vitesse : SR-71 - 3500 km/h. Mon choix : F-22 = le roi."
    if "capitale" in q:
        for pays, cap in CAPITALES.items():
            if pays in q:
                return "Capitale de " + pays.capitalize() + " = " + cap
        return "J'ai 195 capitales ! Essaie : capitale du Japon..."
    for cle, rep in PC.items():
        if cle in q:
            return rep
    for cle, rep in CHANTEURS.items():
        if cle in q:
            return rep
    for cle, rep in AVIONS.items():
        if cle in q:
            return rep
    for mot, rep in TOUT.items():
        if mot in q:
            return rep
    for pays, cap in CAPITALES.items():
        if q == pays:
            return pays.capitalize() + " -> Capitale = " + cap
    return "Je ne connais pas encore : " + q_orig + ". Essaie : Bonjour, Merci, Calcule 12+8, Traduis bonjour en anglais, Raconte une blague, ou clique sur une matiere !"

if "auto_q" in st.session_state and st.session_state.auto_q:
    q_auto = st.session_state.auto_q
    st.session_state.auto_q = ""
    r_auto = trouver(q_auto)
    st.session_state.messages.append({"role": "assistant", "content": r_auto})
    with st.chat_message("assistant"):
        st.write(r_auto)

if question := st.chat_input("Dis Bonjour, Calcule 12+8, Traduis bonjour en anglais... ou pose ta question !"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        r = trouver(question)
        st.write(r)
    st.session_state.messages.append({"role": "assistant", "content": r})
