import streamlit as st
import random
import datetime
import re

st.set_page_config(page_title="Agent IA V5 - ULTIME 1000 - 10H", page_icon="🖤", layout="wide")

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
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Salut ! Version FINALE 1000 lignes - 10H Suisse avec PI ! Clique sur MODE ENTRAINEMENT ou choisis : 10H Maths -> Geometrie -> C est quoi PI ?"}]
if "auto_q" not in st.session_state:
    st.session_state.auto_q = ""

MATIERES_GENRES = {
    "📐 10H Maths": {
        "📈 Fonctions": ["C est quoi une fonction ?", "C est quoi une fonction affine ?", "C est quoi la pente ?", "C est quoi l ordonnee a l origine ?", "C est quoi un graphique ?", "C est quoi l image ?", "C est quoi l antecedent ?", "C est quoi une fonction lineaire ?", "C est quoi une proportionnalite ?"],
        "📐 Geometrie 10H": ["C est quoi PI ?", "C est quoi le theoreme de Pythagore ?", "C est quoi Thales ?", "C est quoi l aire ?", "C est quoi le perimetre ?", "C est quoi le volume ?", "C est quoi un angle ?", "C est quoi un triangle ?", "C est quoi un cercle ?", "C est quoi la similitude ?", "C est quoi le cosinus ?", "C est quoi le sinus ?", "C est quoi la tangente ?", "C est quoi la trigonometrie ?"],
        "🧮 Calcul 10H": ["Table de 7", "Toutes les tables de multiplication", "Table de division de 8", "C est quoi la moyenne ?", "Calcule 12+8", "Calcule 15x7", "C est quoi la division ?", "C est quoi les puissances ?", "C est quoi les racines ?", "C est quoi la notation scientifique ?", "C est quoi PI ?"],
        "🍕 Fractions / Pourcentages": ["C est quoi une fraction ?", "C est quoi le pourcentage ?", "C est quoi une equation ?", "C est quoi la racine carree ?", "C est quoi une equation du 1er degre ?", "C est quoi une inequation ?", "C est quoi la proportionnalite ?", "C est quoi le produit en croix ?"],
        "📊 Stats / Proba 10H": ["C est quoi la moyenne ?", "C est quoi la mediane ?", "C est quoi le mode ?", "C est quoi l etendue ?", "C est quoi la frequence ?", "C est quoi une probabilite ?", "C est quoi un diagramme en batons ?", "C est quoi un diagramme circulaire ?"],
    },
    "🇫🇷 10H Francais": {
        "📖 Grammaire 10H": ["C est quoi le COD ?", "C est quoi le COI ?", "C est quoi le sujet ?", "C est quoi un adjectif ?", "C est quoi le pluriel ?", "C est quoi le verbe ?", "C est quoi le pronom ?", "C est quoi le complement circonstanciel ?", "C est quoi la proposition subordonnee ?", "C est quoi la proposition relative ?", "C est quoi le groupe nominal ?", "C est quoi l attribut du sujet ?", "C est quoi le participe passe ?", "C est quoi l accord du participe passe ?"],
        "✍️ Verbes les plus connus": ["Conjugue ETRE", "Conjugue AVOIR", "Conjugue ALLER", "Conjugue FAIRE", "Conjugue DIRE", "Conjugue POUVOIR", "Conjugue VOULOIR", "Conjugue SAVOIR", "Conjugue DEVOIR", "Conjugue VENIR", "Conjugue VOIR", "Conjugue PRENDRE", "Conjugue METTRE", "Conjugue DONNER", "Conjugue PARLER", "Conjugue MANGER", "Conjugue DORMIR", "Conjugue ECRIRE", "Conjugue LIRE", "Conjugue PARTIR", "Conjugue JOUER", "Conjugue APPRENDRE"],
        "📝 Orthographe / Conjugaison 10H": ["C est quoi a / a ?", "C est quoi et / est ?", "C est quoi son / sont ?", "C est quoi ces / ses ?", "C est quoi ou / ou ?", "C est quoi le passe compose ?", "C est quoi l imparfait ?", "C est quoi le passe simple ?", "C est quoi le futur simple ?", "C est quoi le conditionnel ?", "C est quoi le subjonctif ?", "C est quoi le plus-que-parfait ?", "C est quoi l infinitif ?"],
        "📚 Vocabulaire / Lecture 10H": ["C est quoi un synonyme ?", "C est quoi un antonyme ?", "C est quoi un homonyme ?", "C est quoi une famille de mots ?", "C est quoi une metaphore ?", "C est quoi une comparaison ?", "C est quoi une personnification ?", "C est quoi une hyperbole ?", "C est quoi un champ lexical ?", "C est quoi le registre de langue ?", "C est quoi l argumentation ?", "C est quoi une these ?", "C est quoi un argument ?", "C est quoi un resume ?", "C est quoi une lettre ?", "C est quoi un texte narratif ?", "C est quoi un texte descriptif ?", "C est quoi un texte explicatif ?"],
    },
    "🇩🇪 10H Allemand": {
        "📖 Grammaire 10H": ["C est quoi der die das ?", "C est quoi l accusatif ?", "C est quoi le datif ?", "C est quoi le nominatif ?", "C est quoi le genitif ?", "C est quoi les prepositions ?", "C est quoi les verbes modaux ?", "C est quoi le Perfekt ?", "C est quoi le Prateritum ?", "C est quoi le Futur en allemand ?", "C est quoi le comparatif en allemand ?", "C est quoi weil / dass / wenn ?"],
        "✍️ Verbes les plus connus": ["Conjugue SEIN", "Conjugue HABEN", "Conjugue GEHEN", "Conjugue MACHEN", "Conjugue KOMMEN", "Conjugue SEHEN", "Conjugue SPRECHEN", "Conjugue ESSEN", "Conjugue TRINKEN", "Conjugue LERNEN", "Conjugue WOHNEN", "Conjugue SPIELEN", "Conjugue ARBEITEN", "Conjugue KONNEN", "Conjugue WOLLEN", "Conjugue MUSSEN", "Conjugue WISSEN", "Conjugue GEBEN", "Conjugue NEHMEN", "Conjugue SCHREIBEN"],
        "🌍 Vocabulaire 10H": ["Traduis bonjour en allemand", "Traduis merci en allemand", "Traduis ecole en allemand", "Traduis chien en allemand", "Vocabulaire allemand ecole", "Vocabulaire allemand famille", "Vocabulaire allemand maison", "Vocabulaire allemand loisirs", "Vocabulaire allemand nourriture", "Vocabulaire allemand voyage", "Vocabulaire allemand corps", "Vocabulaire allemand metiers"],
    },
    "🇬🇧 10H Anglais": {
        "📖 Grammaire 10H": ["C est quoi le present simple ?", "C est quoi le present perfect ?", "C est quoi le present continu ?", "C est quoi le preterit ?", "C est quoi le comparatif ?", "C est quoi le past perfect ?", "C est quoi le futur will / going to ?", "C est quoi le conditionnel en anglais ?", "C est quoi le passif en anglais ?", "C est quoi les verbes irreguliers ?", "C est quoi some / any ?", "C est quoi much / many ?", "C est quoi for / since ?", "C est quoi les phrasal verbs ?"],
        "✍️ Verbes les plus connus": ["Conjugue TO BE", "Conjugue TO HAVE", "Conjugue TO GO", "Conjugue TO DO", "Conjugue TO SAY", "Conjugue TO SEE", "Conjugue TO COME", "Conjugue TO GET", "Conjugue TO MAKE", "Conjugue TO TAKE", "Conjugue TO GIVE", "Conjugue TO KNOW", "Conjugue TO THINK", "Conjugue TO SPEAK", "Conjugue TO EAT", "Conjugue TO DRINK", "Conjugue TO PLAY", "Conjugue TO LIVE", "Conjugue TO LOVE", "Conjugue TO WANT"],
        "🌍 Vocabulaire 10H": ["Traduis bonjour en anglais", "Traduis merci en anglais", "Traduis ecole en anglais", "Traduis chien en anglais", "Vocabulaire anglais ecole", "Vocabulaire anglais famille", "Vocabulaire anglais maison", "Vocabulaire anglais loisirs", "Vocabulaire anglais nourriture", "Vocabulaire anglais voyage", "Vocabulaire anglais corps", "Vocabulaire anglais metiers"],
    },
    "🇪🇸 Espagnol": {
        "📖 Grammaire": ["C est quoi ser et estar ?", "C est quoi el / la / los / las ?", "C est quoi le pluriel en espagnol ?"],
        "✍️ Verbes les plus connus": ["Conjugue SER", "Conjugue ESTAR", "Conjugue TENER", "Conjugue IR", "Conjugue HACER", "Conjugue DECIR", "Conjugue PODER", "Conjugue QUERER", "Conjugue SABER", "Conjugue VENIR", "Conjugue VER", "Conjugue HABLAR", "Conjugue COMER", "Conjugue VIVIR", "Conjugue JUGAR"],
        "🌍 Vocabulaire": ["Traduis bonjour en espagnol", "Traduis merci en espagnol"],
    },
    "🇮🇹 Italien": {
        "📖 Grammaire": ["C est quoi il / lo / la ?", "C est quoi le pluriel en italien ?"],
        "✍️ Verbes les plus connus": ["Conjugue ESSERE", "Conjugue AVERE", "Conjugue ANDARE", "Conjugue FARE", "Conjugue DIRE", "Conjugue POTERE", "Conjugue VOLERE", "Conjugue SAPERE", "Conjugue VENIRE", "Conjugue VEDERE", "Conjugue PARLARE", "Conjugue MANGIARE", "Conjugue GIOCARE"],
        "🌍 Vocabulaire": ["Traduis bonjour en italien", "Traduis merci en italien"],
    },
    "📜 10H Histoire": {
        "📜 Histoire Suisse 10H": ["C est quoi la Suisse ?", "C est quoi le pacte de 1291 ?", "C est quoi Guillaume Tell ?", "C est quoi la neutralite suisse ?", "C est quoi la 2eme Guerre ?", "C est quoi la 1ere Guerre ?", "C est quoi la Guerre Froide ?", "C est quoi la Revolution ?", "C est quoi la Revolution industrielle ?", "C est quoi la democratie directe ?", "C est quoi le federalisme ?", "C est quoi la Constitution suisse ?", "C est quoi l ONU ?", "C est quoi l 【entity-UE¦canonical_name=UE】 ?"],
        "🌍 Histoire Monde 10H": ["C est quoi Rome ?", "C est quoi le Moyen Age ?", "C est quoi l Egypte ?", "C est quoi Napoleon ?", "C est quoi les dinosaures ?", "C est quoi la colonisation ?", "C est quoi l esclavage ?", "C est quoi la decolonisation ?", "C est quoi la chute du mur de Berlin ?", "C est quoi le 11 septembre ?"],
    },
    "🌍 10H Geographie": {
        "🌍 Geographie Suisse 10H": ["C est quoi les continents ?", "C est quoi les oceans ?", "Capitale du Japon ?", "Capitale de la France ?", "Capitale de la Suisse ?", "Capitale du Bresil ?", "C est quoi les cantons suisses ?", "C est quoi les Alpes ?", "C est quoi le climat suisse ?", "C est quoi le relief ?", "C est quoi la population suisse ?", "C est quoi la migration ?", "C est quoi l urbanisation ?", "C est quoi le developpement durable ?", "C est quoi le rechauffement climatique ?", "C est quoi les energies renouvelables ?", "C est quoi la mondialisation ?"],
        "🗺️ Cartes / Climat": ["C est quoi une carte ?", "C est quoi l echelle ?", "C est quoi la latitude ?", "C est quoi la longitude ?", "C est quoi le climat ?", "C est quoi la meteo ?", "C est quoi un biome ?", "C est quoi la deforestation ?"],
    },
    "🔬 10H Sciences": {
        "🧬 Biologie 10H": ["C est quoi la photosynthese ?", "C est quoi le coeur ?", "C est quoi l ADN ?", "C est quoi le cerveau ?", "C est quoi les cellules ?", "C est quoi la digestion ?", "C est quoi la respiration ?", "C est quoi la reproduction ?", "C est quoi la puberte ?", "C est quoi le systeme immunitaire ?", "C est quoi les microbes ?", "C est quoi les virus ?", "C est quoi l evolution ?", "C est quoi la biodiversite ?", "C est quoi la chaine alimentaire ?", "C est quoi un ecosysteme ?"],
        "🌍 Terre / Espace 10H": ["C est quoi un volcan ?", "C est quoi les saisons ?", "C est quoi la foudre ?", "C est quoi le systeme solaire ?", "C est quoi un trou noir ?", "C est quoi Mars ?", "C est quoi les seismes ?", "C est quoi les plaques tectoniques ?", "C est quoi l erosion ?", "C est quoi le cycle de l eau ?", "C est quoi les marees ?"],
        "⚡ Physique 10H": ["C est quoi la gravite ?", "Comment calculer la masse volumique ?", "C est quoi la vitesse ?", "C est quoi l energie ?", "C est quoi la lumiere ?", "C est quoi la force ?", "C est quoi la pression ?", "C est quoi le poids ?", "C est quoi la masse ?"],
    },
    "🧪 10H Chimie / Physique": {
        "⚛️ Chimie 10H": ["C est quoi un atome ?", "C est quoi l oxygene ?", "C est quoi la chimie ?", "C est quoi une molecule ?", "C est quoi l eau ?", "C est quoi le tableau periodique ?", "C est quoi le pH ?", "C est quoi un acide ?", "C est quoi une base ?", "C est quoi une reaction chimique ?", "C est quoi la combustion ?", "C est quoi l oxydation ?", "C est quoi le CO2 ?", "C est quoi le dioxygene ?", "C est quoi les melanges ?", "C est quoi la dissolution ?"],
        "⚡ Physique 10H": ["C est quoi l electricite ?", "C est quoi la masse volumique ?", "C est quoi la vitesse ?", "C est quoi la force ?", "C est quoi un circuit electrique ?", "C est quoi en serie / en parallele ?", "C est quoi la tension ?", "C est quoi l intensite ?", "C est quoi la resistance ?", "C est quoi la loi Ohm ?", "C est quoi un aimant ?", "C est quoi le magnetisme ?"],
    },
    "💻 10H Informatique": {
        "🧠 Bases": ["C est quoi une variable ?", "C est quoi une boucle ?", "C est quoi une condition ?", "C est quoi une fonction ?", "C est quoi une liste ?", "C est quoi un algorithme ?", "C est quoi un bug ?", "C est quoi un octet ?", "C est quoi un bit ?", "C est quoi le binaire ?", "C est quoi Internet ?", "C est quoi un reseau ?", "C est quoi le cloud ?", "C est quoi un mot de passe ?", "C est quoi un virus informatique ?", "C est quoi le cyberharcelement ?"],
        "🌐 Langages": ["C est quoi Python ?", "C est quoi HTML ?", "C est quoi CSS ?", "C est quoi JavaScript ?", "C est quoi l IA ?", "C est quoi Scratch ?", "C est quoi un site web ?", "C est quoi une application ?"],
    },
    "💰 10H Economie / Droit": {
        "💰 Economie 10H": ["C est quoi un salaire ?", "C est quoi un budget ?", "C est quoi un impot ?", "C est quoi la TVA ?", "C est quoi l inflation ?", "C est quoi le chomage ?", "C est quoi l offre et la demande ?", "C est quoi une entreprise ?", "C est quoi un benefice ?", "C est quoi un cout ?", "C est quoi la consommation ?", "C est quoi l epargne ?", "C est quoi un credit ?", "C est quoi un interet ?", "C est quoi la bourse ?", "C est quoi un metier ?", "Comment devenir millionnaire ?"],
        "⚖️ Droit / Citoyennete 10H": ["C est quoi une loi ?", "C est quoi la democratie ?", "C est quoi voter ?", "C est quoi la majorite ?", "C est quoi les droits de l enfant ?", "C est quoi la Constitution ?", "C est quoi un citoyen ?", "C est quoi la justice ?", "C est quoi un contrat ?", "C est quoi la liberte d expression ?"],
    },
    "🎨 Arts / Musique 10H": {
        "🎨 Arts 10H": ["C est quoi la Joconde ?", "C est quoi Van Gogh ?", "C est quoi Picasso ?", "C est quoi l art ?", "C est quoi la perspective ?", "C est quoi les couleurs primaires ?", "C est quoi les couleurs chaudes / froides ?", "C est quoi un portrait ?", "C est quoi un paysage ?", "C est quoi l art abstrait ?", "C est quoi la photographie ?", "C est quoi le cinema ?"],
        "🎵 Musique 10H": ["C est quoi le rap ?", "C est quoi le piano ?", "C est quoi la guitare ?", "C est quoi une note ?", "C est quoi le rythme ?", "C est quoi la melodie ?", "C est quoi un tempo ?", "C est quoi une gamme ?", "C est quoi le solfege ?", "C est quoi un orchestre ?", "C est quoi la musique classique ?", "C est quoi le jazz ?", "C est quoi le rock ?"],
    },
    "🏃 10H Sport / Sante": {
        "⚽ Sports 10H": ["C est quoi le foot ?", "C est quoi le basket ?", "C est quoi le tennis ?", "C est quoi la Formule 1 ?", "C est quoi les JO ?", "C est quoi le fair-play ?", "C est quoi l echauffement ?", "C est quoi l endurance ?", "C est quoi la force ?", "C est quoi la souplesse ?", "C est quoi la coordination ?", "C est quoi le dopage ?"],
        "❤️ Sante 10H": ["C est quoi le coeur ?", "C est quoi manger sain ?", "C est quoi le sommeil ?", "C est quoi les addictions ?", "C est quoi le tabac ?", "C est quoi l alcool ?", "C est quoi les ecrans ?", "C est quoi le stress ?", "C est quoi la hygiene ?", "C est quoi les premiers secours ?", "C est quoi le 144 ?", "C est quoi une alimentation equilibree ?"],
    },
    "🏠 10H Ecole de la vie": {
        "🧠 Methodes": ["Conseil pour reviser", "Comment apprendre par coeur ?", "Comment faire un expose ?", "Comment gerer son temps ?", "Comment faire ses devoirs plus vite ?", "Comment ne pas stresser avant un test ?", "Comment prendre des notes ?", "Comment faire une fiche de revision ?"],
        "💬 Vie": ["Comment gerer un conflit ?", "Comment se faire des amis ?", "Comment dire non ?", "Comment avoir confiance en soi ?", "Comment choisir son metier ?", "C est quoi un stage ?", "C est quoi un apprentissage ?", "C est quoi le gymnase ?", "C est quoi l universite ?"],
    },
}

THEMES = {
    "📐 Ecole": ["Voir toutes les matieres"],
    "👋 Bases": ["Bonjour", "Ca va ?", "Merci", "Au revoir", "Tu t appelles comment ?", "Raconte une blague", "Motive moi", "Conseil pour reviser"],
    "🧮 Calculatrice": ["Calcule 12+8", "Calcule 15x7", "Calcule 144/12", "Calcule 9x9"],
    "🌍 Traductions": ["Traduis bonjour en anglais", "Traduis merci en anglais", "Traduis bonjour en allemand", "Traduis bonjour en espagnol"],
    "🎲 Fun": ["Raconte une blague", "Motive moi", "Conseil pour reviser", "Quelle heure il est ?", "Quelle date on est ?", "Devinette"],
    "🌍 Capitales": ["Capitale du Japon ?", "Capitale du Bresil ?", "Capitale de l Egypte ?", "Capitale de la Suisse ?", "Capitale de la France ?"],
    "✈️ Avions": ["Quel est l avion de chasse le plus performant ?", "C est quoi le F-22 ?", "C est quoi le 【entity-F-35¦canonical_name=F-35】 ?", "C est quoi le Rafale ?", "C est quoi le SR-71 ?", "C est quoi le Concorde ?", "C est quoi le A380 ?", "Comment vole un avion ?"],
    "💻 PC": ["C est quoi le meilleur rapport qualite prix ?", "C est quoi la meilleure GPU ?", "C est quoi le meilleur CPU ?", "C est quoi le meilleur SSD ?", "PC 2000 CHF", "PC 1300 CHF", "PC 900 CHF", "C est quoi les FPS ?", "C est quoi le ping ?"],
    "⚽ Foot / Sport": ["C est qui 【entity-Messi¦canonical_name=Messi】 ?", "C est qui 【entity-Ronaldo¦canonical_name=RONALDO】 ?", "C est qui 【entity-Mbappe¦canonical_name=MBAPPE】 ?", "C est quoi la Coupe du Monde ?", "C est quoi la Ligue des Champions ?", "C est quoi le Ballon d Or ?"],
    "🎮 Jeux Video": ["C est quoi Minecraft ?", "C est quoi 【entity-Fortnite¦canonical_name=Fortnite】 ?", "C est quoi Roblox ?", "C est quoi GTA ?", "C est quoi Brawl Stars ?", "C est quoi Pokemon ?", "C est quoi Mario ?", "C est quoi One Piece ?", "C est quoi Naruto ?", "C est quoi Dragon Ball ?"],
    "🚀 Espace": ["C est quoi un trou noir ?", "C est quoi le Big Bang ?", "C est quoi Mars ?", "C est quoi l ISS ?", "C est quoi le Soleil ?"],
    "🎤 Chanteurs": ["C est qui Werenoi ?", "C est qui Ninho ?", "C est qui Jul ?", "C est qui Gazo ?", "C est qui Tiakola ?", "C est qui PNL ?", "C est qui SDM ?", "C est qui Drake ?", "C est qui Taylor Swift ?", "C est qui Eminem ?", "C est qui Stromae ?", "C est qui Soprano ?"],
    "💰 Argent / Metiers": ["Comment devenir millionnaire ?", "C est quoi un salaire ?", "C est quoi un entrepreneur ?", "Comment gagner de l argent a 13 ans ?", "C est quoi la bourse ?"],
    "🐾 Animaux": ["C est quoi le plus grand animal ?", "C est quoi le plus rapide ?", "C est quoi un chien ?", "C est quoi un chat ?", "C est quoi un lion ?", "C est quoi un dauphin ?"],
    "🍔 Cuisine": ["C est quoi une recette facile ?", "C est quoi un gateau au chocolat ?", "C est quoi manger sain ?"],
}

TRAIN_FACILE = [("C est quoi 2+2 ?", "4"), ("C est quoi 5x2 ?", "10"), ("C est quoi la capitale de la France ?", "paris"), ("C est quoi 3x3 ?", "9"), ("C est quoi 10-3 ?", "7"), ("Conjugue ETRE : je ... ?", "suis"), ("C est quoi PI ?", "3.14")]
TRAIN_MOYEN = [("C est quoi 7x8 ?", "56"), ("C est quoi la capitale du Japon ?", "tokyo"), ("C est quoi 15+25 ?", "40"), ("Qui a gagne la Coupe du Monde 2022 ?", "argentine"), ("C est quoi la capitale de la Suisse ?", "berne"), ("C est quoi 9x9 ?", "81")]
TRAIN_DIFFICILE = [("C est quoi 12x12 ?", "144"), ("C est quoi la capitale de l Australie ?", "canberra"), ("C est quoi 144 / 12 ?", "12"), ("Combien de Ballons d Or a 【entity-Messi¦canonical_name=Messi】 ?", "8"), ("En quelle annee a coule le Titanic ?", "1912")]
TRAIN_VERBES = [("Conjugue ETRE au present : je ... ?", "suis"), ("Conjugue AVOIR au present : tu ... ?", "as"), ("Conjugue TO BE : I ... ?", "am"), ("Conjugue SEIN : ich ... ?", "bin"), ("Conjugue ALLER : il ... ?", "va")]
TRAIN_MATHS = [("C est quoi 7x8 ?", "56"), ("C est quoi 9x9 ?", "81"), ("C est quoi 12+15 ?", "27"), ("C est quoi PI ?", "3.14"), ("C est quoi 100-37 ?", "63")]
TRAIN_FRANCAIS = [("C est quoi le COD ?", "cod"), ("Conjugue ETRE : je ... ?", "suis"), ("C est quoi le pluriel de cheval ?", "chevaux")]
TRAIN_CAPITALES = [("C est quoi la capitale du Japon ?", "tokyo"), ("C est quoi la capitale de la France ?", "paris"), ("C est quoi la capitale de la Suisse ?", "berne"), ("C est quoi la capitale du Bresil ?", "brasilia")]
TRAIN_10H = [("C est quoi une fonction affine ?", "affine"), ("C est quoi la formule de Pythagore ?", "a2"), ("C est quoi le COD ?", "cod"), ("C est quoi PI ?", "3.14"), ("C est quoi le pacte de 1291 ?", "1291")]

def lancer_entrainement(niveau, liste):
    st.session_state.mode_train = True
    st.session_state.niveau = niveau
    nq, na = random.choice(liste)
    st.session_state.train_q = nq
    st.session_state.train_a = na
    st.session_state.messages.append({"role": "assistant", "content": "C EST PARTI - ENTRAINEMENT " + niveau.upper() + " ! Reponds juste en bas, je te corrige ! Pour quitter, clique sur le bouton rouge QUITTER. Premiere question : " + nq})
    st.rerun()

with st.sidebar:
    st.title("Agent IA V5 - ULTIME 1000")
    st.write("10H Suisse - Toutes branches")
    st.write("Appris : " + str(len(st.session_state.learned)))
    st.write("Score : " + str(st.session_state.score) + " / " + str(st.session_state.total_quiz))
    st.write("Streak : " + str(st.session_state.streak) + " | Best : " + str(st.session_state.best_streak))
    st.divider()
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
    st.write("MATIERES 10H :")
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

st.title("Agent IA V5 - ULTIME 1000 LIGNES - 10H SUISSE 🇨🇭")
st.caption("1000 lignes | 10H Toutes branches | PI inclus | Appris : " + str(len(st.session_state.learned)) + " | Score : " + str(st.session_state.score) + "/" + str(st.session_state.total_quiz))

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
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        if st.button("🧮 MATHS", key="train_maths", use_container_width=True):
            lancer_entrainement("maths", TRAIN_MATHS)
    with c6:
        if st.button("🇫🇷 FRANCAIS", key="train_francais", use_container_width=True):
            lancer_entrainement("francais", TRAIN_FRANCAIS)
    with c7:
        if st.button("🌍 CAPITALES", key="train_capitales", use_container_width=True):
            lancer_entrainement("capitales", TRAIN_CAPITALES)
    with c8:
        if st.button("🇨🇭 10H", key="train_10h", use_container_width=True):
            lancer_entrainement("10h", TRAIN_10H)
else:
    st.success("🎯 TU ES EN MODE ENTRAINEMENT " + st.session_state.niveau.upper() + " - Score : " + str(st.session_state.score) + "/" + str(st.session_state.total_quiz) + " - Streak : " + str(st.session_state.streak))
    st.info("❓ QUESTION ACTUELLE : " + str(st.session_state.train_q) + " - Ecris ta reponse en bas dans le chat !")
    if st.button("❌ QUITTER ENTRAINEMENT", key="main_train_stop", use_container_width=True):
        st.session_state.mode_train = False
        st.session_state.train_q = None
        st.session_state.messages.append({"role": "assistant", "content": "Entrainement termine ! Score final : " + str(st.session_state.score) + "/" + str(st.session_state.total_quiz) + " | Meilleur streak : " + str(st.session_state.best_streak) + " ! Bravo !"})
        st.rerun()

if st.session_state.theme == "📐 Ecole":
    st.subheader("1 - Choisis ta MATIERE 10H :")
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
    "bonjour": "Bonjour ! Version FINALE 1000 lignes 10H avec PI ! Clique sur MODE ENTRAINEMENT ou choisis ta matiere 10H en haut.",
    "salut": "Salut ! Ca va ? Clique sur MODE ENTRAINEMENT ou pose-moi ta question 10H !",
    "slt": "Slt ! Ca va ?",
    "yo": "Yo ! Ca va ? Tu veux reviser quoi en 10H ?",
    "coucou": "Coucou ! Ca va bien ?",
    "hello": "Hello ! Ca va ? I can help you in English too !",
    "merci": "De rien ! Avec plaisir ! Tu as une autre question ?",
    "mrc": "De rien !",
    "ca va": "Ca va super bien merci ! Et toi, ca va ? Tu revises quelle matiere 10H ?",
    "au revoir": "Au revoir ! A tres vite !",
    "bye": "Bye ! A tres vite !",
    "bonne nuit": "Bonne nuit ! Dors bien ! A demain !",
    "t appelles comment": "Moi je m appelle Agent IA V5 - ULTIME 1000 LIGNES 10H ! Et toi ?",
    "qui es tu": "Moi je suis Agent IA V5 ULTIME 1000 LIGNES ! Programme 10H Suisse complet avec PI : Maths, Francais, Allemand, Anglais, Histoire, Geo, Sciences, Chimie, Physique, Bio, Eco, Droit, Info, Sport, Arts... + 85 verbes, 100+ capitales, PC, avions, chanteurs, entrainement, apprentissage !",
    "aide moi": "Oui bien sur ! Clique sur MODE ENTRAINEMENT en haut, ou choisis une matiere 10H !",
    "j ai pas compris": "T inquiete ! Dis-moi ce que tu n as pas compris, je vais te reexpliquer plus simplement, avec un autre exemple.",
    "t es trop fort": "Merciii ! Ca me fait trop plaisir !",
    "quelle heure": "Il est " + datetime.datetime.now().strftime("%H:%M") + " !",
    "quelle date": "On est le " + datetime.datetime.now().strftime("%d/%m/%Y") + " !",
    "devinette": "Devinette : Je suis toujours devant toi mais tu ne peux jamais me voir. Qui suis-je ? Reponse : Ton avenir ! Une autre : Qu est-ce qui monte mais ne descend jamais ? Reponse : Ton age !",
}
BLAGUES = ["Pourquoi les plongeurs plongent-ils toujours en arriere ? Parce que sinon, ils tombent dans le bateau !", "Que dit un zero a un huit ? Belle ceinture !", "Pourquoi les maths sont tristes ? Parce qu elles ont trop de problemes !", "Pourquoi les poissons n aiment pas jouer au foot ? Parce qu ils ont peur des filets !", "Que fait une fraise sur un cheval ? Tagada tagada !", "Pourquoi PI est trop fort ? Parce qu il ne s arrete jamais !"]
MOTIVATIONS = ["Tu peux le faire ! Chaque erreur, c est une lecon. Ne lache rien !", "N abandonne jamais ! 10 minutes par jour, tous les jours, et dans 1 mois tu seras trop fort !", "Tu es capable de beaucoup plus que tu crois ! Commence petit, 1 exercice, et ca va venir !"]
TRADUCTIONS = {"bonjour en anglais": "Bonjour en anglais = Hello / Good morning !", "bonjour en allemand": "Bonjour en allemand = Hallo / Guten Tag !", "bonjour en espagnol": "Bonjour en espagnol = Hola / Buenos dias !", "bonjour en italien": "Bonjour en italien = Ciao / Buongiorno !", "merci en anglais": "Merci en anglais = Thank you / Thanks !", "merci en allemand": "Merci en allemand = Danke !", "merci en espagnol": "Merci en espagnol = Gracias !", "merci en italien": "Merci en italien = Grazie !", "ecole en anglais": "Ecole en anglais = School !", "chien en anglais": "Chien en anglais = Dog !", "ecole en allemand": "Ecole en allemand = Schule !", "chien en allemand": "Chien en allemand = Hund !", "ecole en espagnol": "Ecole en espagnol = Escuela !"}
CAPITALES = {"france": "Paris - Tour Eiffel, Louvre.", "suisse": "Berne - Capitale de la Suisse depuis 1848.", "allemagne": "Berlin - Mur de Berlin tombe en 1989.", "italie": "Rome - Colisee, Vatican.", "espagne": "Madrid - 【entity-Real Madrid¦canonical_name=Real Madrid】.", "angleterre": "Londres - Big Ben.", "japon": "Tokyo - Plus grande ville du monde !", "usa": "Washington D.C. - Maison Blanche.", "canada": "Ottawa - Toronto = plus grande ville.", "chine": "Pekin - Grande Muraille.", "russie": "Moscou - Place Rouge.", "bresil": "Brasilia - Rio = plus connue.", "inde": "New Delhi - Taj Mahal.", "australie": "Canberra - Sydney = plus connue.", "egypte": "Le Caire - Pyramides de Gizeh.", "maroc": "Rabat - Maroc.", "portugal": "Lisbonne - 【entity-Cristiano Ronaldo¦canonical_name=Cristiano Ronaldo】 !", "belgique": "Bruxelles - Frites, Chocolat !", "pays-bas": "Amsterdam - Canaux, Velos.", "suede": "Stockholm - 【entity-IKEA¦canonical_name=IKEA】, 【entity-ABBA¦canonical_name=ABBA】.", "norvege": "Oslo - Fjords, 【entity-Haaland¦canonical_name=Haaland】 !", "grece": "Athenes - Democratie, Jeux Olympiques.", "mexique": "Mexico - Tacos, Azteques.", "argentine": "Buenos Aires - Tango, 【entity-Messi¦canonical_name=Messi】.", "monaco": "Monaco - 2 km2, Grand Prix F1.", "qatar": "Doha - Qatar, Coupe du Monde 2022 !", "nepal": "Katmandou - Nepal, Everest, 8848m !", "jamaique": "Kingston - Jamaique, Bob Marley, 【entity-Usain Bolt¦canonical_name=Usain Bolt】 !", "turquie": "Ankara - Turquie, Istanbul = plus grande ville.", "coree": "Seoul - Coree du Sud, K-Pop, 【entity-Samsung¦canonical_name=Samsung】.", "colombie": "Bogota - Colombie, Cafe.", "senegal": "Dakar - Senegal, 【entity-Sadio Mane¦canonical_name=Sadio Mane】.", "madagascar": "Antananarivo - Madagascar, Lemuriens.", "indonesie": "Jakarta - Indonesie, 17000 iles !", "singapour": "Singapour - Ville-pays, la plus propre !", "nouvelle-zelande": "Wellington - Nouvelle-Zelande, Seigneur des Anneaux !", "irlande": "Dublin - Irlande, Saint-Patrick.", "islande": "Reykjavik - Islande, Volcans, Aurores boreales.", "finlande": "Helsinki - Finlande, Pere Noel.", "pologne": "Varsovie - Pologne, Lewandowski.", "danemark": "Copenhague - Danemark, 【entity-LEGO¦canonical_name=LEGO】.", "autriche": "Vienne - Autriche, Mozart.", "cuba": "La Havane - Cuba, Salsa."}
PC = {
    "rapport qualite prix": "MEILLEUR RAPPORT PC 2026 : GAGNANT 1300 CHF : RTX 5070 + Ryzen 7 7800X3D + 32 Go + SSD 1 To = 1300 CHF. 1440p Ultra 180 FPS. PETIT BUDGET 900 CHF : RTX 4060 + Ryzen 5 7600 = 900 CHF. GROS BUDGET 2000 CHF : RTX 5070 Ti + 9800X3D = 2000 CHF.",
    "pc 900": "PC 900 CHF : RTX 4060 + Ryzen 5 7600 + 16 Go + SSD 1 To = 900 CHF. 【entity-Fortnite¦canonical_name=Fortnite】 144 FPS !",
    "pc 1300": "PC 1300 CHF - MEILLEUR RAPPORT : RTX 5070 + Ryzen 7 7800X3D + 32 Go + SSD 1 To = 1300 CHF. 1440p Ultra 180 FPS !",
    "pc 2000": "PC 2000 CHF : RTX 5070 Ti + Ryzen 7 9800X3D + 32 Go + SSD 2 To = 2000 CHF. 240 FPS, 4K !",
    "meilleure gpu": "MEILLEURE GPU : 1. RTX 5090 - 32 Go, 4K Ultra 200 FPS, 2500 CHF. 2. RTX 5070 - MEILLEUR RAPPORT : 12 Go, 1440p 180 FPS, 600 CHF.",
    "gpu": "GPU = Carte Graphique. RTX 4060 = 144 FPS en 1080p, RTX 5070 = 180 FPS en 1440p, RTX 5090 = 200 FPS en 4K.",
    "meilleur cpu": "MEILLEUR CPU : Ryzen 7 7800X3D - MEILLEUR RAPPORT, 350 CHF. Ryzen 7 9800X3D - ROI GAMING, 450 CHF.",
    "cpu": "CPU = Processeur, cerveau du PC. AMD Ryzen ou Intel Core.",
    "meilleur ssd": "MEILLEUR SSD : 【entity-Samsung¦canonical_name=Samsung】 990 PRO 2 To - Windows en 5 sec, 180 CHF.",
    "meilleure ram": "MEILLEURE RAM : 32 Go DDR5 6000 MHz. 16 Go = minimum. 64 Go = montage pro.",
    "fps": "FPS = Images par seconde. 30 FPS = ca lag, 60 FPS = fluide, 144 FPS = super fluide, 240 FPS = pro.",
    "ping": "PING = Temps de reponse internet. 10 ms = parfait, 30 ms = tres bien, 100 ms = ca lag, 200 ms = injouable.",
}
CHANTEURS = {
    "werenoi": "WERENOI : Vrai nom Jeremy Bana Owona. Ne en 1994 a Melun. Il a explose en 2023 avec Pyramide et Solitaire. Albums : Pyramide, Diamant Noir. Le plus ecoute en France en 2024 et 2025 !",
    "ninho": "NINHO : Vrai nom William Nzobazola. Le rappeur avec le plus de disques d or et de diamant en France ! Albums : Jefe, NI.",
    "jul": "JUL : Vrai nom Julien Mari. Ne en 1990 a Marseille. Le plus productif : 2 albums par an ! Sons : Tchikita, Bande organisee.",
    "gazo": "GAZO : Roi de la drill en France ! Albums : KMT, Apocalypse. Sons : La Melo avec Tiakola.",
    "tiakola": "TIAKOLA : Membre de 4Keus. Albums : Melo, BDLM. Sons : La Melo, Gasolina.",
    "pnl": "PNL : Duo de freres Ademo et N.O.S. Albums : Dans la legende, Deux freres. Sons : Le monde ou rien, DA.",
    "sdm": "SDM : Repere par Booba. Albums : Ocho, A vie. Son : Bolide allemand avec Ninho.",
    "drake": "DRAKE : Rappeur canadien, le plus streame au monde. Sons : God s Plan, One Dance.",
    "taylor swift": "TAYLOR SWIFT : Chanteuse americaine, la plus ecoutee au monde. 14 Grammy. Son Eras Tour = tournee la plus rentable.",
    "eminem": "EMINEM : Rappeur americain, legende. Sons : Lose Yourself, Rap God, Mockingbird.",
    "stromae": "STROMAE : Chanteur belge. Sons : Alors on danse, Papaoutai, Formidable.",
    "soprano": "SOPRANO : Chanteur de Marseille. Sons : Cosmo, En feu, A la vie, a l amour.",
}
VERBES = {
    "etre": "ETRE - Francais. PRESENT : je suis, tu es, il est, nous sommes, vous etes, ils sont. PASSE COMPOSE : j ai ete, tu as ete, il a ete, nous avons ete, vous avez ete, ils ont ete. IMPARFAIT : j etais, tu etais, il etait, nous etions, vous etiez, ils etaient. FUTUR : je serai, tu seras, il sera, nous serons, vous serez, ils seront.",
    "avoir": "AVOIR - Francais. PRESENT : j ai, tu as, il a, nous avons, vous avez, ils ont. PASSE COMPOSE : j ai eu, tu as eu, il a eu, nous avons eu, vous avez eu, ils ont eu. IMPARFAIT : j avais, tu avais, il avait, nous avions, vous aviez, ils avaient. FUTUR : j aurai, tu auras, il aura, nous aurons, vous aurez, ils auront.",
    "aller": "ALLER - Francais. PRESENT : je vais, tu vas, il va, nous allons, vous allez, ils vont. PASSE COMPOSE : je suis alle, tu es alle, il est alle, nous sommes alles, vous etes alles, ils sont alles. IMPARFAIT : j allais, tu allais, il allait, nous allions, vous alliez, ils allaient. FUTUR : j irai, tu iras, il ira, nous irons, vous irez, ils iront.",
    "faire": "FAIRE - Francais. PRESENT : je fais, tu fais, il fait, nous faisons, vous faites, ils font. PASSE COMPOSE : j ai fait, tu as fait, il a fait, nous avons fait, vous avez fait, ils ont fait. IMPARFAIT : je faisais, tu faisais, il faisait, nous faisions, vous faisiez, ils faisaient. FUTUR : je ferai, tu feras, il fera, nous ferons, vous ferez, ils feront.",
    "dire": "DIRE - Francais. PRESENT : je dis, tu dis, il dit, nous disons, vous dites, ils disent. PASSE COMPOSE : j ai dit, tu as dit, il a dit, nous avons dit, vous avez dit, ils ont dit. IMPARFAIT : je disais, tu disais, il disait, nous disions, vous disiez, ils disaient. FUTUR : je dirai, tu diras, il dira, nous dirons, vous direz, ils diront.",
    "pouvoir": "POUVOIR - Francais. PRESENT : je peux, tu peux, il peut, nous pouvons, vous pouvez, ils peuvent. PASSE COMPOSE : j ai pu, tu as pu, il a pu, nous avons pu, vous avez pu, ils ont pu. IMPARFAIT : je pouvais, tu pouvais, il pouvait, nous pouvions, vous pouviez, ils pouvaient. FUTUR : je pourrai, tu pourras, il pourra, nous pourrons, vous pourrez, ils pourront.",
    "vouloir": "VOULOIR - Francais. PRESENT : je veux, tu veux, il veut, nous voulons, vous voulez, ils veulent. PASSE COMPOSE : j ai voulu, tu as voulu, il a voulu, nous avons voulu, vous avez voulu, ils ont voulu. IMPARFAIT : je voulais, tu voulais, il voulait, nous voulions, vous vouliez, ils voulaient. FUTUR : je voudrai, tu voudras, il voudra, nous voudrons, vous voudrez, ils voudront.",
    "savoir": "SAVOIR - Francais. PRESENT : je sais, tu sais, il sait, nous savons, vous savez, ils savent. PASSE COMPOSE : j ai su, tu as su, il a su, nous avons su, vous avez su, ils ont su. IMPARFAIT : je savais, tu savais, il savait, nous savions, vous saviez, ils savaient. FUTUR : je saurai, tu sauras, il saura, nous saurons, vous saurez, ils sauront.",
    "devoir": "DEVOIR - Francais. PRESENT : je dois, tu dois, il doit, nous devons, vous devez, ils doivent. PASSE COMPOSE : j ai du, tu as du, il a du, nous avons du, vous avez du, ils ont du. IMPARFAIT : je devais, tu devais, il devait, nous devions, vous deviez, ils devaient. FUTUR : je devrai, tu devras, il devra, nous devrons, vous devrez, ils devront.",
    "venir": "VENIR - Francais. PRESENT : je viens, tu viens, il vient, nous venons, vous venez, ils viennent. PASSE COMPOSE : je suis venu, tu es venu, il est venu, nous sommes venus, vous etes venus, ils sont venus. IMPARFAIT : je venais, tu venais, il venait, nous venions, vous veniez, ils venaient. FUTUR : je viendrai, tu viendras, il viendra, nous viendrons, vous viendrez, ils viendront.",
    "voir": "VOIR - Francais. PRESENT : je vois, tu vois, il voit, nous voyons, vous voyez, ils voient. PASSE COMPOSE : j ai vu, tu as vu, il a vu, nous avons vu, vous avez vu, ils ont vu. IMPARFAIT : je voyais, tu voyais, il voyait, nous voyions, vous voyiez, ils voyaient. FUTUR : je verrai, tu verras, il verra, nous verrons, vous verrez, ils verront.",
    "prendre": "PRENDRE - Francais. PRESENT : je prends, tu prends, il prend, nous prenons, vous prenez, ils prennent. PASSE COMPOSE : j ai pris, tu as pris, il a pris, nous avons pris, vous avez pris, ils ont pris. IMPARFAIT : je prenais, tu prenais, il prenait, nous prenions, vous preniez, ils prenaient. FUTUR : je prendrai, tu prendras, il prendra, nous prendrons, vous prendrez, ils prendront.",
    "mettre": "METTRE - Francais. PRESENT : je mets, tu mets, il met, nous mettons, vous mettez, ils mettent. PASSE COMPOSE : j ai mis, tu as mis, il a mis, nous avons mis, vous avez mis, ils ont mis. IMPARFAIT : je mettais, tu mettais, il mettait, nous mettions, vous mettiez, ils mettaient. FUTUR : je mettrai, tu mettras, il mettra, nous mettrons, vous mettrez, ils mettront.",
    "donner": "DONNER - Francais. PRESENT : je donne, tu donnes, il donne, nous donnons, vous donnez, ils donnent. PASSE COMPOSE : j ai donne, tu as donne, il a donne, nous avons donne, vous avez donne, ils ont donne. IMPARFAIT : je donnais, tu donnais, il donnait, nous donnions, vous donniez, ils donnaient. FUTUR : je donnerai, tu donneras, il donnera, nous donnerons, vous donnerez, ils donneront.",
    "parler": "PARLER - Francais. PRESENT : je parle, tu parles, il parle, nous parlons, vous parlez, ils parlent. PASSE COMPOSE : j ai parle, tu as parle, il a parle, nous avons parle, vous avez parle, ils ont parle. IMPARFAIT : je parlais, tu parlais, il parlait, nous parlions, vous parliez, ils parlaient. FUTUR : je parlerai, tu parleras, il parlera, nous parlerons, vous parlerez, ils parleront.",
    "manger": "MANGER - Francais. PRESENT : je mange, tu manges, il mange, nous mangeons, vous mangez, ils mangent. PASSE COMPOSE : j ai mange, tu as mange, il a mange, nous avons mange, vous avez mange, ils ont mange. IMPARFAIT : je mangeais, tu mangeais, il mangeait, nous mangions, vous mangiez, ils mangeaient. FUTUR : je mangerai, tu mangeras, il mangera, nous mangerons, vous mangerez, ils mangeront.",
    "dormir": "DORMIR - Francais. PRESENT : je dors, tu dors, il dort, nous dormons, vous dormez, ils dorment. PASSE COMPOSE : j ai dormi, tu as dormi, il a dormi, nous avons dormi, vous avez dormi, ils ont dormi. IMPARFAIT : je dormais, tu dormais, il dormait, nous dormions, vous dormiez, ils dormaient. FUTUR : je dormirai, tu dormiras, il dormira, nous dormirons, vous dormirez, ils dormiront.",
    "ecrire": "ECRIRE - Francais. PRESENT : j ecris, tu ecris, il ecrit, nous ecrivons, vous ecrivez, ils ecrivent. PASSE COMPOSE : j ai ecrit, tu as ecrit, il a ecrit, nous avons ecrit, vous avez ecrit, ils ont ecrit. IMPARFAIT : j ecrivais, tu ecrivais, il ecrivait, nous ecrivions, vous ecriviez, ils ecrivaient. FUTUR : j ecrirai, tu ecriras, il ecrira, nous ecrirons, vous ecrirez, ils ecriront.",
    "lire": "LIRE - Francais. PRESENT : je lis, tu lis, il lit, nous lisons, vous lisez, ils lisent. PASSE COMPOSE : j ai lu, tu as lu, il a lu, nous avons lu, vous avez lu, ils ont lu. IMPARFAIT : je lisais, tu lisais, il lisait, nous lisions, vous lisiez, ils lisaient. FUTUR : je lirai, tu liras, il lira, nous lirons, vous lirez, ils liront.",
    "partir": "PARTIR - Francais. PRESENT : je pars, tu pars, il part, nous partons, vous partez, ils partent. PASSE COMPOSE : je suis parti, tu es parti, il est parti, nous sommes partis, vous etes partis, ils sont partis. IMPARFAIT : je partais, tu partais, il partait, nous partions, vous partiez, ils partaient. FUTUR : je partirai, tu partiras, il partira, nous partirons, vous partirez, ils partiront.",
    "jouer": "JOUER - Francais. PRESENT : je joue, tu joues, il joue, nous jouons, vous jouez, ils jouent. PASSE COMPOSE : j ai joue, tu as joue, il a joue, nous avons joue, vous avez joue, ils ont joue. IMPARFAIT : je jouais, tu jouais, il jouait, nous jouions, vous jouiez, ils jouaient. FUTUR : je jouerai, tu joueras, il jouera, nous jouerons, vous jouerez, ils joueront.",
    "apprendre": "APPRENDRE - Francais. PRESENT : j apprends, tu apprends, il apprend, nous apprenons, vous apprenez, ils apprennent. PASSE COMPOSE : j ai appris, tu as appris, il a appris, nous avons appris, vous avez appris, ils ont appris. IMPARFAIT : j apprenais, tu apprenais, il apprenait, nous apprenions, vous appreniez, ils apprenaient. FUTUR : j apprendrai, tu apprendras, il apprendra, nous apprendrons, vous apprendrez, ils apprendront.",
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
    "ser": "SER = ETRE en Espagnol. PRESENTE : yo soy, tu eres, el es, nosotros somos, vosotros sois, ellos son. PRETERITO : yo fui, tu fuiste, el fue, nosotros fuimos, vosotros fuisteis, ellos fueron. IMPERFECTO : yo era, tu eras, el era, nosotros eramos, vosotros erais, ellos eran. FUTURO : yo sere, tu seras, el sera.",
    "estar": "ESTAR = ETRE en Espagnol. PRESENTE : yo estoy, tu estas, el esta, nosotros estamos, vosotros estais, ellos estan. PRETERITO : yo estuve. IMPERFECTO : yo estaba. FUTURO : yo estare.",
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
    "pi": "PI = 3.14 ! PI c est le nombre qui sert pour tous les cercles. Valeur exacte : 3.14159265... Ca ne s arrete jamais, c est infini ! FORMULES AVEC PI : Perimetre du cercle = 2 x PI x rayon. Aire du cercle = PI x rayon x rayon. Ex : Rayon = 5. Perimetre = 2 x 3.14 x 5 = 31.4 cm. Aire = 3.14 x 5 x 5 = 78.5 cm2. Ex : Rayon = 10. Perimetre = 62.8 cm. Aire = 314 cm2. Volume du cylindre = PI x rayon2 x hauteur. Ex : rayon 3, hauteur 10 : 3.14 x 9 x 10 = 282.6 cm3. ASTUCE : Pour retenir PI : 3.14159 = 3 - 1 - 4 - 1 - 5 - 9. Le 14 mars, c est la journee de PI (3/14 aux USA) !",
    "fonction": "FONCTION 10H : Une fonction, c est une machine : tu mets un nombre x, elle te sort un nombre y. Ex : f(x) = 2x + 3. Si x = 2, f(2) = 7. On note f : x -> 2x+3.",
    "fonction affine": "FONCTION AFFINE 10H : f(x) = a x + b. a = pente, b = ordonnee a l origine. Ex : f(x) = 2x + 1. Pente = 2, ca monte. Si x=0, y=1. Si a > 0 ca monte, si a < 0 ca descend.",
    "pente": "PENTE 10H : La pente, c est a dans f(x) = a x + b. Formule : pente = (y2 - y1) / (x2 - x1). Ex : Points (0,1) et (2,5) : pente = (5-1)/(2-0) = 2.",
    "ordonnee a l origine": "ORDONNEE A L ORIGINE 10H : C est b dans f(x) = a x + b. C est ou la droite coupe l axe y quand x = 0. Ex : f(x) = 3x + 2. Quand x=0, y=2.",
    "graphique": "GRAPHIQUE 10H : Pour tracer f(x) = 2x + 1 : Tableau : x=0 -> y=1, x=1 -> y=3, x=2 -> y=5. Mets les points (0,1), (1,3), (2,5). Relie avec une regle.",
    "image": "IMAGE 10H : L image, c est le resultat. Si f(x) = 2x + 3 et x = 4, l image de 4 c est f(4) = 11.",
    "antecedent": "ANTECEDENT 10H : L antecedent, c est le x de depart. Si f(x) = 2x + 3 et f(x) = 11, l antecedent de 11 c est 4 car 2x4+3=11.",
    "fonction lineaire": "FONCTION LINEAIRE 10H : f(x) = a x. Elle passe toujours par (0,0). Ex : f(x) = 3x. C est une proportionnalite.",
    "proportionnalite": "PROPORTIONNALITE 10H : Deux grandeurs sont proportionnelles si quand l une double, l autre double. Tableau : 1 -> 5, 2 -> 10, 3 -> 15. Coefficient = 5.",
    "pythagore": "THEOREME DE PYTHAGORE 10H : a2 + b2 = c2. UNIQUEMENT pour un triangle rectangle. c = hypotenuse. Ex : 3-4-5 car 9+16=25. Ex : Si a=6, b=8, c2 = 36+64=100, donc c=10.",
    "thales": "THALES 10H : Si 2 droites paralleles coupent 2 secantes, rapports egaux. Formule : AB / AD = AC / AE = BC / DE.",
    "similitude": "SIMILITUDE 10H : Deux figures sont semblables si elles ont la meme forme mais pas la meme taille. Les angles sont egaux, les cotes sont proportionnels.",
    "cosinus": "COSINUS 10H : Dans un triangle rectangle : cos(angle) = cote adjacent / hypotenuse. Ex : Hypotenuse 10, adjacent 6, cos = 0.6. Sur ta calculatrice : cos-1(0.6) = 53 degres.",
    "sinus": "SINUS 10H : sin(angle) = cote oppose / hypotenuse. Ex : Hypotenuse 10, oppose 8, sin = 0.8. Astuce : SOH-CAH-TOA : Sinus = Oppose / Hypotenuse, Cosinus = Adjacent / Hypotenuse, Tangente = Oppose / Adjacent.",
    "tangente": "TANGENTE 10H : tan(angle) = cote oppose / cote adjacent. Ex : Oppose 6, adjacent 8, tan = 0.75. tan-1(0.75) = 37 degres.",
    "trigonometrie": "TRIGONOMETRIE 10H : SOH-CAH-TOA. Sinus = Oppose / Hypotenuse, Cosinus = Adjacent / Hypotenuse, Tangente = Oppose / Adjacent.",
    "puissances": "PUISSANCES 10H : 2 puissance 3 = 2x2x2 = 8. 2 puissance 0 = 1. 2 puissance -1 = 1/2 = 0.5. Regles : a^m x a^n = a^(m+n). a^m / a^n = a^(m-n).",
    "racines": "RACINES 10H : Racine de 9 = 3 car 3x3 = 9. Racine de 16 = 4. Racine de 2 = 1.41...",
    "notation scientifique": "NOTATION SCIENTIFIQUE 10H : 3 000 000 = 3 x 10^6. 0.000005 = 5 x 10^-6.",
    "equation du 1er degre": "EQUATION DU 1ER DEGRE 10H : 2x + 3 = 7. Tu enleves 3 : 2x = 4. Tu divises par 2 : x = 2. Verif : 2x2+3 = 7.",
    "inequation": "INEQUATION 10H : Comme une equation mais avec < ou >. Ex : 2x + 3 < 7. 2x < 4. x < 2. ATTENTION : Si tu multiplies par un nombre negatif, tu dois retourner le signe !",
    "produit en croix": "PRODUIT EN CROIX 10H : Si 2/3 = x/9, alors 2x9 = 3x x. Donc 18 = 3x, x = 6.",
    "moyenne": "MOYENNE 10H : Moyenne = somme / nombre. Ex : Notes 12, 15, 18. Somme = 45. Nombre = 3. Moyenne = 15.",
    "mediane": "MEDIANE 10H : C est le nombre du milieu quand tu ranges dans l ordre. Ex : 5, 8, 12, 15, 20. Mediane = 12.",
    "mode": "MODE 10H : C est la valeur qui revient le plus souvent. Ex : Notes 12, 15, 12, 18, 12. Mode = 12.",
    "etendue": "ETENDUE 10H : Etendue = plus grand - plus petit. Ex : Notes 8, 12, 15, 20. Etendue = 12.",
    "frequence": "FREQUENCE 10H : Frequence = effectif / total. Ex : Dans une classe de 20, 5 ont 12. Frequence = 5/20 = 0.25 = 25%.",
    "probabilite": "PROBABILITE 10H : Probabilite = cas favorables / cas possibles. Ex : De a 6 faces, proba d avoir 6 = 1/6. Proba d avoir un nombre pair = 3/6 = 1/2 = 50%.",
    "diagramme en batons": "DIAGRAMME EN BATONS 10H : Tu fais des batons, plus le baton est haut, plus il y en a.",
    "diagramme circulaire": "DIAGRAMME CIRCULAIRE 10H : C est un camembert. 360 degres = 100%. Si 50% aiment le foot, ca fait 180 degres.",
    "aire": "AIRE 10H : Rectangle = L x l, Carre = cote x cote, Triangle = (base x hauteur) / 2, Cercle = PI x rayon2. PI = 3.14. Ex : Cercle rayon 5 = 3.14 x 25 = 78.5 cm2. Parallelogramme = base x hauteur.",
    "perimetre": "PERIMETRE 10H : Carre = 4 x cote, Rectangle = 2 x (L+l), Cercle = 2 x PI x rayon. PI = 3.14. Ex : Cercle rayon 5 = 2 x 3.14 x 5 = 31.4 cm. Triangle = somme des 3 cotes.",
    "volume": "VOLUME 10H : Cube = cote3, Pave = L x l x h, Cylindre = PI x r2 x h. Ex : Boite 2x3x4 = 24 cm3. Cylindre rayon 3 hauteur 10 = 3.14 x 9 x 10 = 282.6 cm3.",
    "angle": "ANGLES 10H : Droit = 90 degres, Plat = 180 degres, Plein = 360 degres. Triangle = 180 degres au total.",
    "triangle": "TRIANGLE 10H : 3 cotes, 3 angles, somme = 180 degres. Types : Equilateral, Isocele, Rectangle, Scalene. Aire = (base x hauteur) / 2.",
    "cercle": "CERCLE 10H : Centre, rayon, diametre = 2 x rayon. Perimetre = 2 x PI x rayon. Aire = PI x rayon2. PI = 3.14. Ex : Rayon 7 : Perimetre = 43.96 cm, Aire = 153.86 cm2.",
    "fraction": "FRACTION 10H : 1/2 = la moitie, 1/4 = le quart. 1/2 + 1/4 = 2/4 + 1/4 = 3/4.",
    "pourcentage": "POURCENTAGE 10H : (partie / total) x 100. Ex : 20% de 50 = 10. Tu as 15/20 : (15/20) x 100 = 75%.",
    "equation": "EQUATION 10H : 2x + 3 = 7. Tu enleves 3 : 2x = 4. Tu divises par 2 : x = 2.",
    "racine carree": "RACINE CARREE 10H : Racine de 9 = 3 car 3x3 = 9. Racine de 16 = 4. Racine de 25 = 5.",
    "division": "DIVISION 10H : 12 / 3 = 4. 13 / 4 = 3 reste 1.",
    "cod": "COD 10H : Complement d Objet Direct. Il repond a Qui ? ou Quoi ? apres le verbe, sans preposition. Ex : Je mange une pomme. Je mange quoi ? Une pomme = COD.",
    "coi": "COI 10H : Complement d Objet Indirect. Il repond a A qui ? A quoi ? Ex : Je parle a Lenny. Je parle a qui ? A Lenny = COI.",
    "sujet": "SUJET 10H : Le sujet, c est qui fait l action. Ex : Lenny mange. Qui mange ? Lenny = sujet.",
    "adjectif": "ADJECTIF 10H : Il decrit un nom, il s accorde en genre et nombre. Ex : grand garcon / grande fille.",
    "pluriel": "PLURIEL 10H : +s : chat -> chats. En -eau : bateau -> bateaux. En -al : cheval -> chevaux.",
    "verbe": "VERBE 10H : C est l action dans la phrase. Ex : Je mange, Tu cours, Il dort.",
    "pronom": "PRONOM 10H : Il remplace un nom. Ex : Lenny mange. Il mange.",
    "complement circonstanciel": "COMPLEMENT CIRCONSTANCIEL 10H : Il repond a Ou ? Quand ? Comment ? Pourquoi ? Ex : Je vais a l ecole (ou), demain (quand), en bus (comment).",
    "proposition subordonnee": "PROPOSITION SUBORDONNEE 10H : Proposition qui depend d une autre. Ex : Je sais que tu viens. Que tu viens = subordonnee.",
    "proposition relative": "PROPOSITION RELATIVE 10H : Elle complete un nom, introduite par qui, que, dont, ou. Ex : Le garcon qui joue au foot est mon ami.",
    "groupe nominal": "GROUPE NOMINAL 10H : Groupe avec un nom au centre. Ex : Le grand chien noir. Nom = chien, Determinant = Le, Adjectifs = grand, noir.",
    "attribut du sujet": "ATTRIBUT DU SUJET 10H : Apres un verbe d etat (etre, sembler, devenir...), il decrit le sujet. Ex : Lenny est content. Content = attribut du sujet.",
    "participe passe": "PARTICIPE PASSE 10H : Forme du verbe au passe. Ex : mange, fini, pris, vu, ecrit. Avec etre, il s accorde avec le sujet : Elle est allee.",
    "accord du participe passe": "ACCORD DU PARTICIPE PASSE 10H : Avec ETRE : il s accorde avec le sujet. Elle est allee. Avec AVOIR : il s accorde avec le COD si le COD est avant. Les lettres que j ai ecrites.",
    "passe compose": "PASSE COMPOSE 10H : Auxiliaire ETRE ou AVOIR au present + participe passe. Ex : J ai mange, Je suis alle.",
    "imparfait": "IMPARFAIT 10H : Pour une action longue, repetee, ou une description dans le passe. Ex : Quand j etais petit, je jouais au foot.",
    "passe simple": "PASSE SIMPLE 10H : Pour une action courte, terminee dans le passe, surtout dans les livres. Ex : Il entra, il vit, il prit.",
    "futur simple": "FUTUR SIMPLE 10H : Pour le futur. Ex : Je mangerai, Tu iras, Il sera. Formation : infinitif + -ai, -as, -a, -ons, -ez, -ont.",
    "conditionnel": "CONDITIONNEL 10H : Pour dire ce qui pourrait arriver, ou pour etre poli. Ex : Je voudrais un jus. Si j avais de l argent, j acheterais un velo.",
    "subjonctif": "SUBJONCTIF 10H : Apres il faut que, je veux que, je suis content que... Ex : Il faut que tu viennes, Je veux que tu fasses tes devoirs.",
    "plus-que-parfait": "PLUS-QUE-PARFAIT 10H : Pour une action qui s est passee avant une autre action au passe. Ex : Quand je suis arrive, il avait deja mange.",
    "infinitif": "INFINITIF 10H : Forme non conjuguee du verbe. Ex : manger, finir, prendre, etre, avoir.",
    "synonyme": "SYNONYME 10H : Mot qui veut dire la meme chose. Ex : content = heureux.",
    "antonyme": "ANTONYME 10H : Mot qui veut dire le contraire. Ex : grand = petit, chaud = froid.",
    "homonyme": "HOMONYME 10H : Mots qui se prononcent pareil mais s ecrivent differemment. Ex : a / a, et / est, son / sont.",
    "famille de mots": "FAMILLE DE MOTS 10H : Mots qui ont la meme racine. Ex : fleur, fleuri, fleuriste.",
    "metaphore": "METAPHORE 10H : Comparaison sans comme. Ex : Lenny est un lion. La mer est un miroir.",
    "comparaison": "COMPARAISON 10H : Comparaison avec comme, tel, pareil a. Ex : Il est fort comme un lion.",
    "personnification": "PERSONNIFICATION 10H : Donner des qualites humaines a un objet ou un animal. Ex : Le vent chantait. La lune nous regardait.",
    "hyperbole": "HYPERBOLE 10H : Exageration. Ex : Je t ai dit 1000 fois ! J ai une faim de loup !",
    "champ lexical": "CHAMP LEXICAL 10H : Tous les mots qui parlent du meme theme. Ex : Champ lexical de l ecole : professeur, eleve, cahier, tableau, devoir, note, classe...",
    "registre de langue": "REGISTRE DE LANGUE 10H : Familier (wesh, trop cool), Courant (salut, c est bien), Soutenu (bonjour, c est excellent).",
    "argumentation": "ARGUMENTATION 10H : Pour convaincre. Structure : These + Arguments + Exemples + Conclusion.",
    "these": "THESE 10H : C est ton avis, ton idee principale. Ex : Je pense que les devoirs sont utiles.",
    "argument": "ARGUMENT 10H : C est une raison pour prouver ta these. Ex : These : Le sport est bon. Argument : Ca rend en forme.",
    "resume": "RESUME 10H : Raconter un texte en plus court, avec tes mots, sans changer le sens, sans donner ton avis.",
    "lettre": "LETTRE 10H : Structure : Ton adresse + date en haut a droite. Bonjour. Introduction. Developpement. Conclusion + Formule de politesse. Signature.",
    "texte narratif": "TEXTE NARRATIF 10H : Il raconte une histoire. Structure : Situation initiale, Element declencheur, Peripeties, Denouement, Situation finale.",
    "texte descriptif": "TEXTE DESCRIPTIF 10H : Il decrit un lieu, une personne, un objet. On utilise des adjectifs, des comparaisons, des details.",
    "texte explicatif": "TEXTE EXPLICATIF 10H : Il explique comment ca marche, pourquoi. Ex : Comment vole un avion ? Pourquoi il y a des saisons ?",
    "der": "DER DIE DAS 10H : der = masculin, die = feminin, das = neutre. Pluriel = die.",
    "accusatif": "ACCUSATIF 10H : C est le cas du COD. der devient den. Ex : Ich sehe den Hund.",
    "datif": "DATIF 10H : C est le cas du COI. der devient dem, die devient der, das devient dem.",
    "nominatif": "NOMINATIF 10H : C est le cas du sujet. der, die, das.",
    "genitif": "GENITIF 10H : C est le cas de la possession. der devient des, die devient der, das devient des. Ex : Das Buch des Mannes = Le livre de l homme.",
    "prepositions": "PREPOSITIONS 10H - ALLEMAND : Accusatif : durch, fur, gegen, ohne, um. Datif : mit, nach, bei, von, zu, aus, seit. Accusatif ou Datif : in, an, auf, vor, hinter, uber, unter, neben, zwischen.",
    "verbes modaux": "VERBES MODAUX 10H - ALLEMAND : konnen, mussen, wollen, sollen, durfen, mogen. Ex : Ich kann schwimmen, Ich muss lernen.",
    "perfekt": "PERFEKT 10H - ALLEMAND : Passe compose. Auxiliaire HABEN ou SEIN + participe passe a la fin. Ex : Ich habe gespielt, Ich bin gegangen.",
    "prateritum": "PRATERITUM 10H - ALLEMAND : Passe simple, surtout a l ecrit. Ex : Ich war, Ich hatte, Ich konnte, Ich musste.",
    "futur en allemand": "FUTUR EN ALLEMAND 10H : werden + infinitif a la fin. Ex : Ich werde lernen, Du wirst kommen.",
    "comparatif en allemand": "COMPARATIF EN ALLEMAND 10H : Plus... que = -er + als. Ex : grosser als = plus grand que. gut -> besser als.",
    "weil / dass / wenn": "WEIL / DASS / WENN 10H : weil = parce que. dass = que. wenn = quand / si. Ex : Ich bleibe zu Hause, weil ich krank bin.",
    "present simple": "PRESENT SIMPLE 10H - ANGLAIS : Pour les habitudes. I play, He plays (avec -s !). Ex : He plays football every day.",
    "present perfect": "PRESENT PERFECT 10H - ANGLAIS : have / has + participe passe. Ex : I have lived here for 5 years. I have just eaten.",
    "present continu": "PRESENT CONTINU 10H - ANGLAIS : be + -ing. Ex : I am playing now. I am going to school tomorrow.",
    "preterit": "PRETERIT 10H - ANGLAIS : Pour le passe termine. Verbes reguliers +ed : I played. Verbes irreguliers : I went, I saw, I ate.",
    "comparatif": "COMPARATIF 10H - ANGLAIS : Plus... que = -er + than. Ex : bigger than = plus grand que. More + adjectif long : more beautiful than.",
    "past perfect": "PAST PERFECT 10H - ANGLAIS : had + participe passe. Ex : When I arrived, he had already eaten.",
    "futur will / going to": "FUTUR WILL / GOING TO 10H : Will = decision spontanee. I will help you. Going to = deja prevu. I am going to play football tomorrow.",
    "conditionnel en anglais": "CONDITIONNEL EN ANGLAIS 10H : If + present, will + infinitif. Ex : If it rains, I will stay home. If + preterit, would + infinitif. Ex : If I had money, I would buy a bike.",
    "passif en anglais": "PASSIF EN ANGLAIS 10H : be + participe passe. Ex : The book is read by Lenny. Present : is read, Preterit : was read, Futur : will be read.",
    "verbes irreguliers": "VERBES IRREGULIERS 10H - ANGLAIS : be-was-been, have-had-had, go-went-gone, do-did-done, see-saw-seen, come-came-come, take-took-taken, give-gave-given.",
    "some / any": "SOME / ANY 10H - ANGLAIS : Some = phrases affirmatives. I have some apples. Any = phrases negatives et questions. I do not have any apples.",
    "much / many": "MUCH / MANY 10H - ANGLAIS : Much = pour ce qu on ne peut pas compter (much water). Many = pour ce qu on peut compter (many books).",
    "for / since": "FOR / SINCE 10H - ANGLAIS : For = depuis une duree. I have lived here for 5 years. Since = depuis un moment precis. I have lived here since 2020.",
    "phrasal verbs": "PHRASAL VERBS 10H - ANGLAIS : Verbe + particule = nouveau sens. Ex : get up = se lever, look for = chercher, turn off = eteindre, give up = abandonner.",
    "vocabulaire allemand ecole": "VOCABULAIRE ALLEMAND - ECOLE 10H : die Schule = ecole, der Lehrer = prof, die Klasse = classe, das Buch = livre, das Heft = cahier, der Stift = crayon, die Prufung = test, die Hausaufgaben = devoirs, die Note = note.",
    "vocabulaire allemand famille": "VOCABULAIRE ALLEMAND - FAMILLE 10H : die Familie = famille, der Vater = pere, die Mutter = mere, der Bruder = frere, die Schwester = soeur, der Onkel = oncle, die Tante = tante.",
    "vocabulaire allemand maison": "VOCABULAIRE ALLEMAND - MAISON 10H : das Haus = maison, die Wohnung = appartement, das Zimmer = chambre, die Kuche = cuisine, das Bad = salle de bain, das Wohnzimmer = salon, der Garten = jardin.",
    "vocabulaire allemand loisirs": "VOCABULAIRE ALLEMAND - LOISIRS 10H : Fussball spielen = jouer au foot, Musik horen = ecouter de la musique, lesen = lire, schwimmen = nager, Rad fahren = faire du velo.",
    "vocabulaire allemand nourriture": "VOCABULAIRE ALLEMAND - NOURRITURE 10H : das Brot = pain, die Pizza = pizza, die Schokolade = chocolat, das Wasser = eau, die Milch = lait, der Apfel = pomme, die Banane = banane.",
    "vocabulaire allemand voyage": "VOCABULAIRE ALLEMAND - VOYAGE 10H : reisen = voyager, der Zug = train, der Bus = bus, das Flugzeug = avion, das Hotel = hotel, der Bahnhof = gare, der Flughafen = aeroport.",
    "vocabulaire allemand corps": "VOCABULAIRE ALLEMAND - CORPS 10H : der Kopf = tete, das Auge = oeil, die Nase = nez, der Mund = bouche, das Ohr = oreille, die Hand = main, der Fuss = pied, das Herz = coeur.",
    "vocabulaire allemand metiers": "VOCABULAIRE ALLEMAND - METIERS 10H : der Lehrer = prof, der Arzt = medecin, der Polizist = policier, der Koch = cuisinier, der Fahrer = chauffeur, der Ingenieur = ingenieur.",
    "vocabulaire anglais ecole": "VOCABULAIRE ANGLAIS - ECOLE 10H : school = ecole, teacher = prof, pupil = eleve, class = classe, book = livre, notebook = cahier, pen = stylo, test = test, homework = devoirs, mark = note, break = recreation.",
    "vocabulaire anglais famille": "VOCABULAIRE ANGLAIS - FAMILLE 10H : family = famille, father = pere, mother = mere, brother = frere, sister = soeur, grandfather = grand-pere, grandmother = grand-mere, uncle = oncle, aunt = tante.",
    "vocabulaire anglais maison": "VOCABULAIRE ANGLAIS - MAISON 10H : house = maison, flat = appartement, bedroom = chambre, kitchen = cuisine, bathroom = salle de bain, living room = salon, garden = jardin, table = table, chair = chaise, bed = lit.",
    "vocabulaire anglais loisirs": "VOCABULAIRE ANGLAIS - LOISIRS 10H : play football = jouer au foot, listen to music = ecouter de la musique, read = lire, swim = nager, ride a bike = faire du velo, meet friends = voir des amis.",
    "vocabulaire anglais nourriture": "VOCABULAIRE ANGLAIS - NOURRITURE 10H : bread = pain, pizza = pizza, chocolate = chocolat, water = eau, milk = lait, apple = pomme, banana = banane, meat = viande, vegetables = legumes, breakfast = petit-dejeuner.",
    "vocabulaire anglais voyage": "VOCABULAIRE ANGLAIS - VOYAGE 10H : travel = voyager, train = train, bus = bus, plane = avion, hotel = hotel, station = gare, airport = aeroport, ticket = billet, holidays = vacances.",
    "vocabulaire anglais corps": "VOCABULAIRE ANGLAIS - CORPS 10H : head = tete, eye = oeil, nose = nez, mouth = bouche, ear = oreille, hand = main, foot = pied, leg = jambe, arm = bras, heart = coeur.",
    "vocabulaire anglais metiers": "VOCABULAIRE ANGLAIS - METIERS 10H : teacher = prof, doctor = medecin, policeman = policier, cook = cuisinier, driver = chauffeur, engineer = ingenieur, farmer = paysan.",
    "suisse": "SUISSE 10H : 26 cantons, 4 langues : francais, allemand, italien, romanche. Capitale : Berne. Population : 8.9 millions. Monnaie : Franc suisse (CHF). Neutralite depuis 1515. Democratie directe : le peuple vote souvent. Federalisme : chaque canton a ses lois. Pacte de 1291 = naissance de la Suisse.",
    "pacte de 1291": "PACTE DE 1291 10H : Le 1er aout 1291, 3 cantons (Uri, Schwyz, Unterwald) signent un pacte pour s entraider contre les Habsbourg. C est la naissance de la Suisse. Fete nationale : 1er aout.",
    "guillaume tell": "GUILLAUME TELL 10H : Heros suisse legendaire. Il aurait refuse de saluer le chapeau du bailli Gessler. Gessler l oblige a tirer une pomme sur la tete de son fils. Il reussit ! Puis il tue Gessler. Symbole de liberte.",
    "neutralite suisse": "NEUTRALITE SUISSE 10H : La Suisse ne fait pas la guerre depuis 1515. Elle ne prend pas parti. Elle accueille la Croix-Rouge, l ONU a Geneve. Elle a une armee, mais pour se defendre.",
    "guerre froide": "GUERRE FROIDE 10H : 1947-1991. USA contre URSS, sans guerre directe, mais avec des espions, des armes nucleaires, la course a l espace. Fin : chute du mur de Berlin 1989.",
    "revolution industrielle": "REVOLUTION INDUSTRIELLE 10H : Au 19eme siecle, en Angleterre puis en Suisse. Machines a vapeur, usines, trains. Les gens quittent la campagne pour la ville.",
    "democratie directe": "DEMOCRATIE DIRECTE 10H - SUISSE : En Suisse, le peuple vote directement sur les lois (votations). Il peut lancer une initiative (100 000 signatures) ou un referendum (50 000 signatures).",
    "federalisme": "FEDERALISME 10H - SUISSE : La Suisse est divisee en 26 cantons. Chaque canton a son gouvernement, ses lois, ses ecoles. Le gouvernement central (Berne) s occupe de l armee, de la monnaie.",
    "constitution suisse": "CONSTITUTION SUISSE 10H : C est la loi la plus importante. Elle dit les droits, l organisation. Derniere version : 1999.",
    "onu": "ONU 10H : Organisation des Nations Unies. Cree en 1945 apres la 2eme Guerre pour eviter une 3eme Guerre. Siege a New York, et a Geneve en Europe. 193 pays membres. La Suisse y est entree en 2002.",
    "ue": "UE 10H : Union Europeenne. 27 pays en Europe qui cooperent : meme monnaie (euro) pour 20 pays, pas de frontieres (Schengen). La Suisse n est PAS dans l UE, mais elle a des accords avec elle.",
    "colonisation": "COLONISATION 10H : Au 19eme siecle, les pays europeens conquierent l Afrique, l Asie. Ils prennent les ressources, imposent leur langue, leur religion.",
    "esclavage": "ESCLAVAGE 10H : Des millions d Africains ont ete deplaces de force en Amerique pour travailler dans les plantations du 16eme au 19eme siecle. Aboli en France en 1848, aux USA en 1865.",
    "decolonisation": "DECOLONISATION 10H : Apres 1945, les pays colonises deviennent independants. Ex : Inde 1947, Algerie 1962, beaucoup de pays africains en 1960.",
    "chute du mur de berlin": "CHUTE DU MUR DE BERLIN 10H : Le 9 novembre 1989, le mur qui separait Berlin en 2 tombe. L Allemagne est reunifiee en 1990. Fin de la Guerre Froide.",
    "11 septembre": "11 SEPTEMBRE 10H : Le 11 septembre 2001, des terroristes detruisent les tours jumelles a New York avec 2 avions. 3000 morts. Les USA attaquent l Afghanistan.",
    "cantons suisses": "CANTONS SUISSES 10H : Il y en a 26 : Zurich, Berne, Lucerne, Uri, Schwyz, Obwald, Nidwald, Glaris, Zoug, Fribourg, Soleure, Bale-Ville, Bale-Campagne, Schaffhouse, Appenzell, Saint-Gall, Grisons, Argovie, Thurgovie, Tessin, Vaud, Valais, Neuchatel, Geneve, Jura.",
    "alpes": "ALPES 10H : Chaine de montagnes en Suisse, France, Italie, Autriche. Plus haut sommet suisse : Pointe Dufour, 4634m. Plus haut d Europe : Mont-Blanc, 4808m.",
    "climat suisse": "CLIMAT SUISSE 10H : Climat tempere. Ete : 20-25 degres, Hiver : 0-5 degres en plaine, -10 en montagne. Il pleut toute l annee, plus en ete. Avec le rechauffement, les etes sont plus chauds, les glaciers fondent.",
    "relief": "RELIEF 10H : Relief = formes du terrain. En Suisse : Jura (ouest), Plateau (milieu, ou vivent la plupart des gens), Alpes (sud, hautes montagnes).",
    "population suisse": "POPULATION SUISSE 10H : 8.9 millions d habitants. 25% sont etrangers. Les plus grandes villes : Zurich, Geneve, Bale, Lausanne, Berne.",
    "migration": "MIGRATION 10H : Migration = deplacement de personnes. Immigration = arriver dans un pays, Emigration = quitter un pays. Raisons : travail, guerre, etudes, famille, climat.",
    "urbanisation": "URBANISATION 10H : De plus en plus de gens vivent en ville. En Suisse, 85% vivent en ville. Consequences : plus de logements, plus de transports, moins de nature, pollution.",
    "developpement durable": "DEVELOPPEMENT DURABLE 10H : Repondre aux besoins d aujourd hui sans empecher les generations futures de repondre aux leurs. 3 piliers : Economie, Social, Environnement. Ex : recycler, prendre le velo, acheter local, ne pas gaspiller.",
    "rechaffement climatique": "RECHAUFFEMENT CLIMATIQUE 10H : La Terre se rechauffe a cause des gaz a effet de serre (CO2 des voitures, usines...). Consequences : glaciers qui fondent, mer qui monte, canicules, secheresses, inondations.",
    "energies renouvelables": "ENERGIES RENOUVELABLES 10H : Energies qui ne s epuisent pas : solaire, eolien, hydraulique (barrages), geothermie, biomasse. En Suisse, l hydraulique fait plus de la moitie de l electricite.",
    "mondialisation": "MONDIALISATION 10H : Le monde est de plus en plus connecte : commerce, Internet, voyages, films, musique. Ex : Un telephone est fabrique en Chine, avec des pieces du Japon, vendu en Suisse.",
    "carte": "CARTE 10H : Representation d un territoire a plat. Elements : titre, legende, echelle, fleche du nord. Types : carte physique, carte politique, carte thematique.",
    "echelle": "ECHELLE 10H : Echelle = rapport entre la carte et la realite. Ex : 1:25 000 = 1 cm sur la carte = 250 m en vrai.",
    "latitude": "LATITUDE 10H : Position nord-sud. Equateur = 0 degres, Pole Nord = 90 degres Nord, Pole Sud = 90 degres Sud. La Suisse est a environ 47 degres Nord.",
    "longitude": "LONGITUDE 10H : Position est-ouest. Greenwich (Londres) = 0 degre. La Suisse est a environ 7-8 degres Est.",
    "climat": "CLIMAT 10H : Le temps qu il fait en moyenne sur une longue periode (30 ans) dans un endroit. Different de la meteo (temps d un jour).",
    "meteo": "METEO 10H : Le temps qu il fait aujourd hui : pluie, soleil, vent, neige, temperature. On la prevoit avec des satellites, des radars, des modeles informatiques.",
    "biome": "BIOME 10H : Grande zone avec le meme climat et les memes plantes / animaux. Ex : foret tropicale, desert, toundra, savane, foret temperee.",
    "deforestation": "DEFORESTATION 10H : On coupe les forets, surtout en Amazonie, pour l agriculture, le bois, l huile de palme. Consequences : moins d oxygene, plus de CO2, animaux qui perdent leur maison.",
    "digestion": "DIGESTION 10H : Transformer la nourriture en energie. Etapes : Bouche, Oesophage, Estomac, Intestin grele, Gros intestin, Anus. Ca dure 24-72h.",
    "respiration": "RESPIRATION 10H : On inspire O2, on expire CO2. Air -> Nez / Bouche -> Trachee -> Bronches -> Poumons -> Sang. On respire environ 20 000 fois par jour.",
    "reproduction": "REPRODUCTION 10H : Pour avoir un bebe, il faut un spermatozoide (homme) + un ovule (femme). Ca forme un oeuf qui grandit dans l uterus pendant 9 mois. Pose tes questions a ton prof ou a tes parents pour les details.",
    "puberte": "PUBERTE 10H : Periode ou le corps change pour devenir adulte. En general entre 10 et 15 ans. Changements : grandir vite, voix qui change, poils, regles, boutons. C est normal, tout le monde passe par la, a son rythme.",
    "systeme immunitaire": "SYSTEME IMMUNITAIRE 10H : L armee de ton corps. Globules blancs = soldats qui tuent les microbes. Anticorps = memoire. Vaccins = entrainent ton systeme immunitaire sans te rendre malade.",
    "microbes": "MICROBES 10H : Petits etres vivants qu on ne voit pas a l oeil nu. Bons microbes : yaourts, pain, digestion. Mauvais microbes : angine, gastro. Pour se proteger : se laver les mains.",
    "virus": "VIRUS 10H : Plus petit qu une bacterie, il a besoin d une cellule pour se multiplier. Ex : grippe, rhume, COVID. Antibiotiques = contre les bacteries, pas contre les virus.",
    "evolution": "EVOLUTION 10H : Les especes changent avec le temps. Darwin : les mieux adaptes survivent et se reproduisent. Ex : Girafes avec un long cou = atteignent les feuilles hautes.",
    "biodiversite": "BIODIVERSITE 10H : Diversite du vivant : especes, genes, ecosystemes. Plus il y a de biodiversite, plus la nature est forte. Menaces : pollution, deforestation, rechauffement, pesticides.",
    "chaine alimentaire": "CHAINE ALIMENTAIRE 10H : Qui mange qui. Ex : Herbe -> Sauterelle -> Grenouille -> Serpent -> Aigle. Producteur, Consommateurs, Decomposeurs.",
    "ecosysteme": "ECOSYSTEME 10H : Un milieu + les etres vivants qui y vivent + leurs interactions. Ex : Foret, Lac, Ocean, Desert.",
    "seismes": "SEISMES 10H : Tremblement de terre. Cause : plaques tectoniques qui bougent. Epicentre = point a la surface au-dessus du seisme. Magnitude = force.",
    "plaques tectoniques": "PLAQUES TECTONIQUES 10H : La Terre est coupee en plaques qui bougent lentement (quelques cm par an). Quand elles se cognent, ca fait des montagnes, des seismes, des volcans.",
    "erosion": "EROSION 10H : L eau, le vent, la glace usent les roches petit a petit. Ex : Une riviere creuse une vallee, le vent use une falaise.",
    "cycle de l eau": "CYCLE DE L EAU 10H : Evaporation (mer -> nuage), Condensation (nuage), Precipitation (pluie / neige), Infiltration (dans le sol), Ruissellement (rivieres -> mer).",
    "marees": "MAREES 10H : La mer monte et descend 2 fois par jour a cause de la Lune. Maree haute = pleine mer, Maree basse = basse mer.",
    "force": "FORCE 10H : En Newtons (N). Poids = masse x gravite. Ex : 50 kg sur Terre = 500 N.",
    "pression": "PRESSION 10H : Force / surface. Ex : Un couteau coupe car la force est sur une petite surface. Pression de l air = 1 bar.",
    "poids": "POIDS 10H : Poids = masse x gravite. Masse = en kg, ne change pas. Poids = en N, change selon la planete. Sur Terre, 50 kg = 500 N. Sur la Lune, 50 kg = 80 N.",
    "masse": "MASSE 10H : Quantite de matiere, en kg. Elle ne change pas ou que tu sois. Tu as la meme masse sur Terre et sur la Lune, mais pas le meme poids.",
    "tableau periodique": "TABLEAU PERIODIQUE 10H : Tableau avec tous les elements chimiques. H = Hydrogene, O = Oxygene, C = Carbone, Fe = Fer, Au = Or.",
    "ph": "PH 10H : Mesure si c est acide ou basique. Echelle de 0 a 14. 0-6 = acide (citron = 2, vinaigre = 3), 7 = neutre (eau pure), 8-14 = basique (savon = 10, javel = 12).",
    "acide": "ACIDE 10H : pH < 7. Gout aigre. Ex : citron, vinaigre, jus d orange. Acide + Base = Sel + Eau.",
    "base": "BASE 10H : pH > 7. Gout amer, glissant. Ex : savon, javel, bicarbonate. Base + Acide = Sel + Eau.",
    "reaction chimique": "REACTION CHIMIQUE 10H : Des reactifs se transforment en produits. Ex : Bois + Oxygene -> CO2 + Eau + Chaleur.",
    "combustion": "COMBUSTION 10H : Bruler quelque chose avec de l oxygene. Ex : Bois + O2 -> CO2 + H2O + chaleur. Il faut 3 choses : combustible, oxygene, chaleur.",
    "oxydation": "OXYDATION 10H : Reaction avec l oxygene. Ex : Le fer rouille : Fer + Oxygene + Eau -> Rouille. La pomme brunit quand on la coupe.",
    "co2": "CO2 10H : Dioxyde de carbone. On l expire, les plantes l absorbent pour la photosynthese. On en produit en brulant du bois, de l essence, du charbon. Trop de CO2 = rechauffement.",
    "dioxygene": "DIOXYGENE 10H : O2. Le gaz qu on respire. 21% de l air. Produit par les plantes (photosynthese). Sans O2, on meurt en 3 minutes.",
    "melanges": "MELANGES 10H : Homogene = on ne voit pas les composants (eau + sel). Heterogene = on voit les composants (eau + sable). On peut separer : filtration, evaporation, decantation.",
    "dissolution": "DISSOLUTION 10H : Quand un solide disparait dans un liquide. Ex : Sel dans l eau. Le sel est le solute, l eau est le solvant, l eau salee est la solution.",
    "circuit electrique": "CIRCUIT ELECTRIQUE 10H : Boucle avec : Pile, Fils, Interrupteur, Lampe. Pour que ca marche, le circuit doit etre ferme.",
    "en serie / en parallele": "EN SERIE / EN PARALLELE 10H : En serie : les lampes sont l une apres l autre. Si une grille, tout s eteint. En parallele : chaque lampe a son propre circuit. Si une grille, les autres restent allumees.",
    "tension": "TENSION 10H : En Volts (V). C est la pression qui pousse les electrons. Pile = 1.5V, Prise suisse = 230V.",
    "intensite": "INTENSITE 10H : En Amperes (A). C est le debit d electrons. Plus il y a de lampes en parallele, plus l intensite augmente.",
    "resistance": "RESISTANCE 10H : En Ohms. Elle freine le courant. Plus la resistance est grande, moins il y a de courant. Loi Ohm : U = R x I.",
    "loi ohm": "LOI OHM 10H : U = R x I. U = tension en Volts, R = resistance en Ohms, I = intensite en Amperes. Ex : R = 10, I = 2, U = 20V.",
    "aimant": "AIMANT 10H : Il attire le fer, le nickel, le cobalt. Il a 2 poles : Nord et Sud. Nord attire Sud, Nord repousse Nord. La Terre est un gros aimant.",
    "magnetisme": "MAGNETISME 10H : Force des aimants. Autour d un aimant, il y a un champ magnetique. Un fil avec du courant cree aussi un champ magnetique.",
    "bug": "BUG 10H - INFO : Erreur dans un programme. Ex : tu oublies une parenthese, tu mets un mauvais nom. Pour corriger : lis l erreur, verifie ligne par ligne, teste petit a petit.",
    "octet": "OCTET 10H - INFO : 1 octet = 8 bits. 1 Ko = 1000 octets, 1 Mo = 1 million, 1 Go = 1 milliard. Une photo = 2-5 Mo, un film = 1-2 Go.",
    "bit": "BIT 10H - INFO : Plus petite unite : 0 ou 1. 8 bits = 1 octet. Tout dans un ordi, c est des 0 et des 1 : texte, photos, musique, videos.",
    "binaire": "BINAIRE 10H - INFO : Systeme avec 0 et 1. Ex : 1 = 1, 10 = 2, 11 = 3, 100 = 4, 101 = 5. Ton ordi ne comprend que ca.",
    "internet": "INTERNET 10H : Reseau mondial d ordinateurs relies. Cree dans les annees 60 pour l armee, ouvert au public dans les annees 90. Services : Web, mail, videos, jeux.",
    "reseau": "RESEAU 10H - INFO : Ordinateurs relies pour partager. LAN = petit reseau (maison, ecole), WAN = grand reseau (Internet). WiFi = sans fil, Ethernet = avec cable.",
    "cloud": "CLOUD 10H : Stocker sur Internet au lieu de sur ton ordi. Ex : Google Drive, iCloud. Avantages : accessible partout, pas perdu si ton ordi casse.",
    "mot de passe": "MOT DE PASSE 10H : Pour proteger tes comptes. Regles : long (12+ caracteres), avec majuscules, chiffres, symboles, different pour chaque site, jamais partage.",
    "virus informatique": "VIRUS INFORMATIQUE 10H : Programme qui abime ton ordi ou vole tes donnees. Comment l attraper : cliquer sur un lien bizarre, telecharger un fichier douteux. Protection : antivirus, mises a jour.",
    "cyberharcelement": "CYBERHARCELEMENT 10H : Harceler quelqu un sur Internet : insultes, moqueries, rumeurs, photos sans accord. C est interdit, c est puni par la loi. Si ca t arrive : ne reponds pas, garde les preuves, parles-en a un adulte, bloque, signale.",
    "scratch": "SCRATCH 10H : Logiciel pour apprendre a coder avec des blocs. Tu deplaces des blocs comme un puzzle : bouger, parler, repeter... Ideal pour debuter avant Python.",
    "site web": "SITE WEB 10H : Ensemble de pages sur Internet. 3 langages : HTML (squelette), CSS (style), JavaScript (interactions). Ton agent, c est un site web fait avec Streamlit et Python.",
    "application": "APPLICATION 10H : Programme pour telephone ou ordi. Ex : WhatsApp, TikTok, Fortnite. On la telecharge sur App Store / Play Store.",
    "budget": "BUDGET 10H - ECO : Prevoir ce que tu gagnes et ce que tu depenses. Ex : Tu as 100 CHF. Tu mets 50 pour manger, 20 pour loisirs, 30 en epargne. Regle 50/30/20.",
    "impot": "IMPOT 10H - ECO : Argent qu on donne a l Etat pour payer ecoles, hopitaux, routes, police. En Suisse, on paie impot federal + cantonal + communal.",
    "tva": "TVA 10H- ECO : Taxe sur la Valeur Ajoutee. En Suisse : 8.1% en general, 2.6% pour la nourriture, 3.8% pour l hotel. Quand tu achetes un jeu a 100 CHF, environ 8 CHF vont a l Etat.",
    "inflation": "INFLATION 10H - ECO : Quand les prix montent. Ex : Une pizza a 10 CHF, l annee d apres a 11 CHF = inflation de 10%. Causes : plus de demande, plus de couts. Consequences : ton argent vaut moins.",
    "chomage": "CHOMAGE 10H - ECO : Quand quelqu un veut travailler mais ne trouve pas de travail. Causes : crise, robotisation, manque de formation. Solutions : formation, apprentissage, aide de l Etat.",
    "offre et demande": "OFFRE ET DEMANDE 10H - ECO : Si beaucoup de gens veulent acheter et peu de produits, le prix monte. Si peu de gens veulent acheter et beaucoup de produits, le prix baisse. Ex : PS5 au debut = tres demandee, peu de stock = prix tres haut.",
    "entreprise": "ENTREPRISE 10H - ECO : Organisation qui produit ou vend. Ex : 【entity-Nestle¦canonical_name=Nestle】, 【entity-Rolex¦canonical_name=Rolex】, 【entity-Migros¦canonical_name=Migros】, Coop. Types : petite (boulangerie), moyenne, grande (multinationale). But : gagner de l argent en repondant a un besoin.",
    "benefice": "BENEFICE 10H - ECO : Benefice = Recettes - Couts. Ex : Tu vends des limonades pour 100 CHF, ca t a coute 40 CHF. Benefice = 60 CHF. Si couts > recettes, c est une perte.",
    "cout": "COUT 10H - ECO : Ce que ca coute pour produire. Cout fixe : loyer, meme si tu ne vends rien. Cout variable : ingredients, ca change avec ce que tu produis.",
    "consommation": "CONSOMMATION 10H - ECO : Acheter et utiliser. On consomme : nourriture, vetements, loisirs, energie. Consommation responsable : acheter moins, acheter local, reparer, recycler, ne pas gaspiller.",
    "epargne": "EPARGNE 10H - ECO : Mettre de l argent de cote pour plus tard. Ex : Tu as 50 CHF, tu en mets 20 en epargne pour ton futur PC. Regle : epargne d abord, depense apres.",
    "credit": "CREDIT 10H - ECO : Emprunter de l argent a la banque. Tu dois rembourser + des interets. Ex : Tu empruntes 1000 CHF, tu rembourses 1100 CHF. Attention : un credit, ca coute cher.",
    "interet": "INTERET 10H - ECO : Prix de l argent. Si tu pretes 100 CHF a 5% pendant 1 an, tu recois 105 CHF. Si tu empruntes 100 CHF a 5%, tu rembourses 105 CHF.",
    "metier": "METIER 10H - ECO : Developpeur, Medecin, Avocat, Pilote, Ingenieur, Enseignant, Infirmier, Electricien, Cuisinier, Youtubeur. Le meilleur metier, c est celui que tu aimes + qui paie bien + qui est utile.",
    "loi": "LOI 10H - DROIT : Regle obligatoire pour tous. Si tu ne la respectes pas, tu es puni. Ex : ne pas voler, ne pas rouler trop vite, aller a l ecole jusqu a 15 ans. Les lois sont votees par le Parlement.",
    "democratie": "DEMOCRATIE 10H - DROIT : Le peuple decide. En Suisse : democratie directe (votations). En France : democratie representative (on vote pour des deputes). Principes : egalite, liberte, vote libre et secret.",
    "voter": "VOTER 10H : Choisir. En Suisse, on vote a partir de 18 ans. On vote pour : elire des gens, accepter ou refuser des lois (votations). Voter, c est un droit et un devoir.",
    "majorite": "MAJORITE 10H : A 18 ans en Suisse, tu es majeur. Tu peux voter, conduire, signer un contrat, etre responsable de tes actes. Avant 18 ans, tu es mineur, tes parents sont responsables.",
    "droits de l enfant": "DROITS DE L ENFANT 10H : Convention de l ONU 1989. Droits : aller a l ecole, etre protege, avoir un nom, une famille, jouer, donner ton avis, ne pas etre maltraite.",
    "constitution": "CONSTITUTION 10H : C est la loi la plus importante. Elle dit les droits, l organisation du pays. En Suisse : Constitution de 1999.",
    "citoyen": "CITOYEN 10H : Habitant d un pays avec des droits et des devoirs. Droits : voter, aller a l ecole, etre soigne. Devoirs : respecter les lois, payer des impots, respecter les autres.",
    "justice": "JUSTICE 10H : Elle dit qui a raison, qui a tort, et punit. Tribunaux : juge, avocat, procureur. Si tu es accuse, tu as droit a un avocat, a te defendre, a etre presume innocent.",
    "contrat": "CONTRAT 10H : Accord entre 2 personnes. Ex : contrat d apprentissage, contrat de travail, contrat de location. Il dit : qui fait quoi, combien, pendant combien de temps. Lis toujours avant de signer !",
    "liberte d expression": "LIBERTE D EXPRESSION 10H : Droit de dire ce que tu penses. Mais limites : pas d insultes, pas de mensonges qui font du mal, pas de racisme, pas d appels a la violence. Sur Internet aussi, tu es responsable de ce que tu ecris.",
    "art": "ART 10H : Creer quelque chose de beau ou qui fait reflechir. Peinture, sculpture, photo, cinema, musique, danse, theatre. L art n a pas de bonne ou mauvaise reponse, c est ton regard.",
    "perspective": "PERSPECTIVE 10H - ARTS : Technique pour donner l impression de profondeur sur une feuille plate. Les lignes se rejoignent a un point de fuite. Plus c est loin, plus c est petit.",
    "couleurs primaires": "COULEURS PRIMAIRES 10H : Rouge, Bleu, Jaune. Avec ces 3, tu peux faire toutes les autres. Rouge + Jaune = Orange. Bleu + Jaune = Vert. Rouge + Bleu = Violet.",
    "couleurs chaudes / froides": "COULEURS CHAUDES / FROIDES 10H : Chaudes : rouge, orange, jaune = feu, soleil, energie. Froides : bleu, vert, violet = mer, glace, calme.",
    "portrait": "PORTRAIT 10H - ARTS : Dessin / photo d une personne. On regarde : visage, expression, vetements, fond. Pour reussir : bien placer les yeux (au milieu), le nez, la bouche.",
    "paysage": "PAYSAGE 10H - ARTS : Dessin / photo d un lieu. On regarde : premier plan, arriere-plan, ciel, lumiere. Astuce : ne pas mettre l horizon au milieu.",
    "art abstrait": "ART ABSTRAIT 10H : Art qui ne represente pas quelque chose de reel. Que des formes, des couleurs, des lignes. Ex : Kandinsky, Mondrian.",
    "photographie": "PHOTOGRAPHIE 10H : Prendre une photo, c est choisir : cadrage, lumiere, moment. Regles : regle des tiers, lumiere naturelle, fond simple.",
    "cinema": "CINEMA 10H : 24 images par seconde = impression de mouvement. Metiers : realisateur, acteur, cameraman, monteur, scenariste. Genres : comedie, drame, action, animation, documentaire.",
    "rythme": "RYTHME 10H - MUSIQUE : Le rythme, c est quand on tape dans les mains. Il est regulier : 1-2-3-4, 1-2-3-4. Sans rythme, la musique est bizarre.",
    "melodie": "MELODIE 10H - MUSIQUE : Suite de notes qu on peut chanter. Ex : Joyeux Anniversaire. La melodie + le rythme = une chanson.",
    "tempo": "TEMPO 10H - MUSIQUE : Vitesse de la musique. Lent = calme, Rapide = danse. On le mesure avec un metronome.",
    "gamme": "GAMME 10H - MUSIQUE : Suite de notes dans l ordre. Gamme de Do majeur : Do, Re, Mi, Fa, Sol, La, Si, Do. Majeur = joyeux, Mineur = triste.",
    "solfege": "SOLFEGE 10H - MUSIQUE : Apprendre a lire les notes sur une portee (5 lignes). Cle de Sol pour les aigus, Cle de Fa pour les graves. Notes : Do, Re, Mi, Fa, Sol, La, Si.",
    "orchestre": "ORCHESTRE 10H - MUSIQUE : Grand groupe de musiciens. Cordes (violon, violoncelle), Vents (flute, trompette), Percussions (batterie, tambour). Chef d orchestre = celui qui dirige.",
    "musique classique": "MUSIQUE CLASSIQUE 10H : Musique de Mozart, Beethoven, Bach, Chopin. Pas de paroles, souvent avec un orchestre.",
    "jazz": "JAZZ 10H : Musique nee aux USA, avec beaucoup d improvisation (on invente sur le moment). Instruments : saxophone, trompette, piano, contrebasse.",
    "rock": "ROCK 10H : Musique avec guitare electrique, basse, batterie. Nee dans les annees 50. Groupes : 【entity-Queen¦canonical_name=Queen】, 【entity-AC/DC¦canonical_name=AC/DC】, Nirvana.",
    "fair-play": "FAIR-PLAY 10H - SPORT : Jouer honnetement, respecter l adversaire, l arbitre, les regles. Gagner, c est bien, mais gagner en trichant, ce n est pas gagner.",
    "echauffement": "ECHAUFFEMENT 10H - SPORT : Avant le sport, il faut echauffer les muscles 5-10 min : courir doucement, tourner les bras, les jambes, les chevilles. Ca evite les blessures.",
    "endurance": "ENDURANCE 10H - SPORT : Pouvoir courir longtemps sans etre trop fatigue. On l entraine en courant lentement longtemps, en faisant du velo, de la natation.",
    "souplesse": "SOUPLESSE 10H - SPORT : Pouvoir bouger facilement sans se faire mal. On l entraine avec des etirements, du yoga, de la gymnastique.",
    "coordination": "COORDINATION 10H - SPORT : Faire bouger plusieurs parties du corps en meme temps. Ex : jongler, dribbler au foot, faire du velo.",
    "dopage": "DOPAGE 10H - SPORT : Prendre des produits interdits pour etre plus fort. C est de la triche, c est dangereux pour la sante, c est puni. Les vrais champions ne se dopent pas.",
    "addictions": "ADDICTIONS 10H - SANTE : Quand tu ne peux plus t arreter : jeux video, telephone, cigarette, alcool, drogues, sucre. Signes : tu y penses tout le temps, tu es enerve sans, tu mens pour en avoir. Solution : en parler a un adulte.",
    "tabac": "TABAC 10H - SANTE : La cigarette contient beaucoup de produits toxiques, dont la nicotine (addiction) et le goudron (cancer). Fumer = cancer du poumon, dents jaunes, souffle court, ca coute cher.",
    "alcool": "ALCOOL 10H - SANTE : L alcool rend malade, fait faire des betises, detruit le foie, le cerveau. Pour les jeunes, c est encore plus dangereux car le cerveau grandit.",
    "ecrans": "ECRANS 10H - SANTE : Trop d ecrans = mal aux yeux, mal a dormir, moins de sport, moins d amis en vrai. Regles : pas d ecran 1h avant de dormir, pas d ecran a table, faire des pauses toutes les 30 min.",
    "stress": "STRESS 10H - SANTE : Quand tu es stresse, ton coeur bat vite, tu as mal au ventre, tu dors mal. C est normal avant un test. Pour gerer : respirer lentement, preparer a l avance, en parler, faire du sport, dormir.",
    "hygiene": "HYGIENE 10H - SANTE : Se laver les mains, se brosser les dents 2x par jour, se doucher, changer de vetements, se couper les ongles. Ca evite les maladies, les caries.",
    "premiers secours": "PREMIERS SECOURS 10H : Si quelqu un se blesse : 1. Securise. 2. Appelle le 144. 3. Parle a la personne, rassure-la. 4. Si elle saigne, appuie avec un linge propre. 5. Ne deplace pas quelqu un qui s est fait mal au dos / a la tete.",
    "144": "144 10H : Numero d urgence en Suisse pour l ambulance. 117 = police, 118 = pompiers, 144 = ambulance, 147 = aide pour les jeunes. Si tu appelles : dis qui tu es, ou tu es, ce qui s est passe, combien de blesses.",
    "alimentation equilibree": "ALIMENTATION EQUILIBREE 10H : Manger de tout, en quantites raisonnables. Beaucoup d eau, fruits, legumes, cereales, un peu de viande / poisson / oeufs, peu de sucre, peu de gras, peu de sel.",
    "apprendre par coeur": "APPRENDRE PAR COEUR 10H : 1. Lis 3 fois a voix haute. 2. Cache et recite. 3. Repete le lendemain. 4. Utilise des images, des rimes, des histoires. 5. Dors bien, ton cerveau range la nuit.",
    "expose": "EXPOSE 10H : Pour reussir un expose : 1. Choisis un sujet que tu aimes. 2. Cherche 3-4 idees principales. 3. Fais un plan (intro, parties, conclusion). 4. Fais des diapos simples. 5. Entraine-toi a voix haute 3 fois.",
    "gerer son temps": "GERER SON TEMPS 10H : 1. Fais une liste de ce que tu dois faire. 2. Fais d abord le plus important. 3. Utilise un agenda. 4. Pomodoro : 25 min de travail, 5 min de pause. 5. Pas de telephone pendant le travail.",
    "faire ses devoirs plus vite": "FAIRE SES DEVOIRS PLUS VITE 10H : 1. Commence tout de suite apres l ecole. 2. Fais un coin calme, sans telephone. 3. Fais d abord le plus dur. 4. Si tu bloques 5 min, passe a autre chose et reviens apres.",
    "ne pas stresser avant un test": "NE PAS STRESSER AVANT UN TEST 10H : 1. Revise a l avance, pas la veille au soir. 2. Dors bien la veille. 3. Mange un bon petit-dejeuner. 4. Respire lentement avant le test. 5. Lis toutes les questions d abord, commence par les faciles.",
    "prendre des notes": "PRENDRE DES NOTES 10H : N ecris pas tout, ecris les mots importants, les exemples, les dates. Utilise des abreviations. Laisse des espaces pour completer apres. Relis tes notes le soir meme.",
    "fiche de revision": "FICHE DE REVISION 10H : Une feuille A4 par chapitre. Recto : titre, definitions, formules, exemples. Verso : exercices + reponses. Couleurs : bleu = titre, rouge = important, vert = exemple.",
    "gerer un conflit": "GERER UN CONFLIT 10H : 1. Calme-toi (respire). 2. Ecoute l autre sans couper. 3. Dis ce que tu ressens avec je : Je suis enerve quand... 4. Cherche une solution gagnant-gagnant. 5. Si ca ne marche pas, demande a un adulte.",
    "se faire des amis": "SE FAIRE DES AMIS 10H : 1. Souris, dis bonjour. 2. Pose des questions, ecoute. 3. Propose une activite. 4. Sois toi-meme, ne fais pas semblant. 5. Sois gentil, aide. Un vrai ami, c est quelqu un qui te respecte.",
    "dire non": "DIRE NON 10H : Tu as le droit de dire non, meme a tes amis. Ex : Non, je ne veux pas fumer, Non, je ne veux pas tricher. Dis-le calmement, avec une raison, propose autre chose.",
    "confiance en soi": "CONFIANCE EN SOI 10H : Personne n est bon en tout. 1. Note tes reussites. 2. Compare-toi a toi-meme d hier, pas aux autres. 3. Parle-toi gentiment. 4. Essaie des choses nouvelles, meme si tu as peur.",
    "choisir son metier": "CHOISIR SON METIER 10H : 1. Qu est-ce que tu aimes faire ? 2. Qu est-ce que tu sais faire ? 3. Quels metiers existent ? 4. Essaie : stage, journee portes ouvertes. Tu as le droit de changer d avis.",
    "stage": "STAGE 10H : Tu vas voir un vrai metier pendant 1-5 jours. Tu observes, tu poses des questions, tu essaies. Ca t aide a choisir. Pour trouver : demande a ta famille, a tes profs, ecris a des entreprises.",
    "apprentissage": "APPRENTISSAGE 10H : En Suisse, apres la 11H, beaucoup font un apprentissage (CFC). Tu apprends un metier en travaillant 3-4 jours en entreprise + 1-2 jours a l ecole. Tu es paye. Duree : 2-4 ans.",
    "gymnase": "GYMNASE 10H : Apres la 11H, si tu as de bonnes notes, tu peux aller au gymnase. 4 ans. Tu etudies beaucoup. A la fin, tu as une maturite, tu peux aller a l universite.",
    "universite": "UNIVERSITE 10H : Apres la maturite, tu peux aller a l universite (Lausanne, Geneve, Fribourg, Zurich...). Tu choisis une branche. Tu etudies 3 ans pour un Bachelor, + 2 ans pour un Master.",
    "conseil pour reviser": "CONSEIL POUR REVISER 10H : 1. Pomodoro : 25 min, 5 min pause. 2. Teste-toi, ne relis pas. 3. Explique a quelqu un. 4. Dors bien. 5. Pas de telephone. 6. Fais des fiches. 7. Commence 1 semaine avant, pas la veille.",
    "2eme guerre": "2EME GUERRE MONDIALE 10H : 1939-1945. Allemagne contre Allies (France, Angleterre, USA, URSS). Beaucoup de morts. Fin : 1945, debarquement en Normandie 1944, bombes sur Hiroshima et Nagasaki.",
    "1ere guerre": "1ERE GUERRE MONDIALE 10H : 1914-1918. France, Angleterre contre Allemagne, Autriche. Guerre des tranchees, beaucoup de morts. Fin : Armistice 11 novembre 1918.",
    "revolution": "REVOLUTION FRANCAISE 10H : 1789. Le peuple se revolte contre le roi Louis XVI. Prise de la Bastille 14 juillet 1789. Declaration des Droits de l Homme.",
    "rome": "ROME 10H : Empire romain, il y a 2000 ans. Colisee, gladiateurs, Jules Cesar, Auguste. Rome a conquis toute l Europe. Langue : latin, ancetre du francais, espagnol, italien.",
    "moyen age": "MOYEN AGE 10H : 500-1500. Chateaux forts, chevaliers, rois, paysans, eglise. Guerre de Cent Ans. Peste noire en 1348. Fin : decouverte de l Amerique en 1492.",
    "egypte": "EGYPTE 10H : Pharaons, pyramides, Nil, hieroglyphes. Pharaons celebres : Toutankhamon, Ramses II, Cleopatre. Dieux : Ra (Soleil), Anubis (mort), Horus (faucon).",
    "napoleon": "NAPOLEON 10H : Empereur francais 1804-1815. Il a conquis presque toute l Europe. Il a cree le Code Civil. Batailles : Austerlitz (victoire), Waterloo (defaite, 1815).",
    "dinosaures": "DINOSAURES 10H : Ils ont vecu il y a 230 a 66 millions d annees. T-Rex, Diplodocus, Triceratops. Ils ont disparu il y a 66M d annees a cause d un asteroide.",
    "continents": "CONTINENTS 10H : Il y en a 7 : Afrique, Amerique du Nord, Amerique du Sud, Antarctique, Asie, Europe, Oceanie. Le plus grand = Asie, le plus petit = Oceanie.",
    "oceans": "OCEANS 10H : Il y en a 5 : Pacifique (le plus grand), Atlantique, Indien, Arctique, Austral.",
    "photosynthese": "PHOTOSYNTHESE 10H : Soleil + Eau + CO2 = Oxygene + Sucre. Les feuilles ont de la chlorophylle (vert) qui capte la lumiere.",
    "gravite": "GRAVITE 10H : La gravite nous attire vers la Terre. C est Newton qui l a decouverte en voyant une pomme tomber. Sur la Lune, tu es 6x plus leger.",
    "coeur": "COEUR 10H : Pompe le sang dans tout le corps. Beaucoup de battements par jour, beaucoup de litres de sang par jour !",
    "volcan": "VOLCAN 10H : Ouverture dans la Terre par ou sort du magma. Le plus actif d Europe = Etna.",
    "foudre": "FOUDRE 10H : Tres chaud, plusieurs fois plus chaud que le Soleil ! Si tu entends le tonnerre, rentre.",
    "saison": "SAISONS 10H : Ce n est pas la distance au Soleil, c est l inclinaison de la Terre (23.5 degres). En ete, l hemisphere Nord est penche vers le Soleil.",
    "cerveau": "CERVEAU 10H : 1.4 kg, beaucoup de milliards de neurones. Il controle tout : pensees, mouvements, emotions. Il consomme beaucoup d energie.",
    "cellule": "CELLULES 10H : La cellule, c est la plus petite brique du vivant. Tu en as beaucoup de milliards ! Chaque cellule a un noyau avec ton ADN.",
    "masse volumique": "MASSE VOLUMIQUE 10H : Formule : masse / volume. Rho = m / V. Ex : 100g / 100 cm3 = 1 = eau. Huile = 0.9 flotte, Fer = 7.8 coule.",
    "atome": "ATOME 10H : Noyau avec protons (+) et neutrons (0), et autour des electrons (-) qui tournent.",
    "oxygene": "OXYGENE 10H : O2. On respire O2, on rejette CO2. 21% de l air = oxygene.",
    "chimie": "CHIMIE 10H : Etude de la matiere. Atome = brique, Molecule = plusieurs atomes. H2O = eau. CO2 = dioxyde de carbone.",
    "electricite": "ELECTRICITE 10H : Tension en Volts (V), Intensite en Amperes (A), Puissance en Watts (W). Formule : P = U x I. En serie : si une lampe grille, tout s eteint. En parallele : les autres restent allumees.",
    "vitesse": "VITESSE 10H : Vitesse = distance / temps. v = d / t. Ex : 100m en 10 sec = 10 m/s = 36 km/h. Pour m/s vers km/h : x 3.6.",
    "energie": "ENERGIE 10H : Cinetique (mouvement), potentielle (hauteur), thermique (chaleur), electrique, chimique, solaire, eolienne. On ne cree pas d energie, on la transforme.",
    "adn": "ADN 10H : Ton code genetique. 50% pere, 50% mere.",
    "trou noir": "TROU NOIR 10H : Objet tellement lourd que meme la lumiere ne peut pas en sortir.",
    "big bang": "BIG BANG 10H : Debut de l univers il y a tres longtemps, environ 13.8 milliards d annees.",
    "mars": "MARS 10H : Planete rouge. Un jour = 24h37. Temperature : -60 degres. Robots : Perseverance, 【entity-Curiosity¦canonical_name=Curiosity】.",
    "iss": "ISS 10H : Station Spatiale a 400 km, a 28 000 km/h. Beaucoup de levers de soleil par jour !",
    "systeme solaire": "SYSTEME SOLAIRE 10H : 8 planetes : Mercure, Venus, Terre, Mars, Jupiter, Saturne, Uranus, Neptune. Astuce : Me Voici, Tout Mouille, J ai Suivi Un Nuage.",
    "soleil": "SOLEIL 10H : C est une etoile, pas une planete. Temperature : 5500 degres a la surface.",
    "galaxie": "GALAXIE 10H : Groupe de milliards d etoiles. Notre galaxie = Voie Lactee, beaucoup de milliards d etoiles.",
    "lune": "LUNE 10H : Distance : environ 384 000 km. Premier homme dessus : Neil Armstrong, 1969. Elle fait les marees.",
    "boucle": "BOUCLE 10H : for i in range(1,6): print(i) -> affiche 1,2,3,4,5.",
    "variable": "VARIABLE 10H : Boite qui stocke une valeur. Ex : age = 13, prenom = Lenny.",
    "condition": "CONDITION 10H : if age >= 18: print(Majeur) else: print(Mineur).",
    "fonction info": "FONCTION 10H - INFO : def dire_bonjour(): print(Bonjour). Tu l appelles avec dire_bonjour().",
    "liste": "LISTE 10H : notes = [12, 15, 18]. notes[0] = 12.",
    "algorithme": "ALGORITHME 10H : Suite d etapes pour resoudre un probleme. Ex : Recette de cuisine.",
    "python": "PYTHON 10H : Langage facile, celui de ton agent. Utilise pour l IA, les sites web, les jeux.",
    "html": "HTML 10H : Squelette d un site. h1 = Titre, p = Texte.",
    "css": "CSS 10H : Style d un site : couleurs, tailles.",
    "javascript": "JAVASCRIPT 10H : Pour rendre un site interactif : boutons, animations, jeux.",
    "ia": "IA 10H : Programme qui apprend avec des donnees. Ex : ChatGPT, ton agent.",
    "joconde": "JOCONDE 10H : Peinture de Leonard de Vinci. Au Louvre a Paris. La plus celebre au monde.",
    "van gogh": "VAN GOGH 10H : Peintre neerlandais. Tableaux : La Nuit etoilee, Les Tournesols.",
    "picasso": "PICASSO 10H : Peintre espagnol. Il a invente le cubisme. Il a peint Guernica.",
    "rap": "RAP 10H : Musique nee dans le Bronx a New York. En France, c est la musique la plus ecoutee.",
    "piano": "PIANO 10H : Instrument avec 88 touches. Les plus grands : Mozart, Beethoven, Chopin.",
    "guitare": "GUITARE 10H : Instrument avec 6 cordes. Accords de base : Do, Sol, La mineur, Mi mineur.",
    "note": "NOTE DE MUSIQUE 10H : 7 notes : Do, Re, Mi, Fa, Sol, La, Si.",
    "foot": "FOOT 10H : Sport le plus joue au monde, beaucoup de milliards de fans ! 2 equipes de 11, 90 minutes.",
    "basket": "BASKET 10H : 5 vs 5, panier a 3.05m. Michael Jordan = GOAT. Wembanyama = 2m24 !",
    "tennis": "TENNIS 10H : Federer (20 Grands Chelems, Suisse !), Nadal (22), Djokovic (24, record).",
    "formule 1": "FORMULE 1 10H : 350 km/h ! Verstappen a gagne 2021, 2022, 2023, 2024. Hamilton = 7 titres.",
    "jo": "JO 10H : Tous les 4 ans. 2024 = Paris, 2028 = Los Angeles. Devise : Plus vite, plus haut, plus fort.",
    "manger sain": "MANGER SAIN 10H : 5 fruits et legumes par jour, boire 1.5L d eau, moins de sucre.",
    "sommeil": "SOMMEIL 10H : A 13 ans, il faut 9-10h de sommeil ! Pas d ecran 1h avant de dormir.",
    "【entity-messi¦canonical_name=Messi】": "【entity-MESSI¦canonical_name=Messi】 : 8 Ballons d Or (record), 91 buts en une annee. Coupe du Monde 2022.",
    "ronaldo": "RONALDO : 5 Ballons d Or, meilleur buteur de l histoire (beaucoup de buts).",
    "mbappe": "MBAPPE : Champion du Monde 2018 a 19 ans. Vitesse : 36 km/h. Real Madrid depuis 2024.",
    "ballon d or": "BALLON D OR 10H : Trophee du meilleur joueur du monde. Messi en a 8 (record), Ronaldo 5.",
    "coupe du monde": "COUPE DU MONDE 10H : Tous les 4 ans, 48 equipes en 2026. 2022 = Argentine gagne contre France.",
    "ligue des champions": "LIGUE DES CHAMPIONS 10H : 【entity-Real Madrid¦canonical_name=Real Madrid】 a gagne 15 fois, record !",
    "minecraft": "MINECRAFT 10H : Jeu le plus vendu au monde : beaucoup de millions de copies ! Monde en cubes, Creeper, Ender Dragon.",
    "fortnite": "FORTNITE 10H : Battle Royale : 100 joueurs, le dernier vivant gagne.",
    "roblox": "ROBLOX 10H : Des millions de jeux crees par les joueurs. Jeux cultes : Brookhaven, Blox Fruits, Doors.",
    "gta": "GTA V 10H : Beaucoup de millions de copies. Monde ouvert : Los Santos. GTA VI sort en 2026, a Vice City.",
    "brawl stars": "BRAWL STARS 10H : Jeu mobile de Supercell. 3v3, Brawlers : Shelly, Colt, Spike, Leon...",
    "mario": "MARIO 10H : Plombier Nintendo, sauve Peach. Jeux : Super Mario Bros, Mario Kart, Mario Party.",
    "pokemon": "POKEMON 10H : Attrape-les tous ! 1000+ Pokemons. Pikachu = mascotte.",
    "one piece": "ONE PIECE 10H : Manga le plus vendu au monde (beaucoup de millions de tomes). Luffy veut devenir Roi des Pirates.",
    "naruto": "NARUTO 10H : Ninja qui veut devenir Hokage. Rasengan, Chidori, Kyubi (demon renard a 9 queues).",
    "dragon ball": "DRAGON BALL 10H : Goku, Super Saiyan, Kamehameha !",
    "tour eiffel": "TOUR EIFFEL 10H : Paris, 330m, 1889, Gustave Eiffel. Beaucoup de millions de visiteurs par an.",
    "pyramide": "PYRAMIDES 10H : En Egypte, il y a 4500 ans pour les Pharaons. La plus grande = Kheops, 146m.",
    "titanic": "TITANIC 10H : Paquebot anglais, 1912. Il heurte un iceberg, il coule en 2h40. Film 1997, 11 Oscars.",
    "harry potter": "HARRY POTTER 10H : Sorcier avec une cicatrice en eclair, par J.K. Rowling. 7 livres, 8 films.",
    "millionnaire": "COMMENT DEVENIR MILLIONNAIRE ? 10H : 1. Salarie + investissement. 2. Entrepreneur. 3. Createur. Conseils : Apprends une competence, epargne, investis tot.",
    "gagner de l argent": "GAGNER DE L ARGENT A 13 ANS 10H : Petits services, vendre ce que tu n utilises plus, creer un projet et montrer a tes parents, apprendre une competence.",
    "bourse": "BOURSE 10H : Acheter une petite partie d une entreprise. ETF = panier de beaucoup d entreprises, moins risque.",
    "plus grand animal": "PLUS GRAND ANIMAL 10H : Baleine bleue ! 30m, 200 tonnes !",
    "plus rapide": "PLUS RAPIDE 10H : Guepard = 110 km/h. Faucon pelerin = 390 km/h en pique !",
    "chien": "CHIEN 10H : Meilleur ami de l homme depuis 15 000 ans. 400 races. Il comprend 150 mots.",
    "chat": "CHAT 10H : Il dort 16h par jour ! Il peut sauter 6x sa hauteur.",
    "lion": "LION 10H : Roi des animaux. Il dort 20h par jour ! Il rugit si fort qu on l entend a 8 km.",
    "dauphin": "DAUPHIN 10H : Animal tres intelligent. Il dort avec un oeil ouvert. Il peut nager a 60 km/h.",
    "recette facile": "RECETTE FACILE - PATES 10H : 1. Fais bouillir de l eau salee. 2. Mets les pates 8-10 min. 3. Egoutte. 4. Ajoute sauce tomate + fromage.",
    "gateau au chocolat": "GATEAU AU CHOCOLAT 10H : 200g chocolat, 200g beurre, 4 oeufs, 150g sucre, 100g farine. Four 180 degres pendant 25 min.",
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
    "comment vole": "COMMENT VOLE UN AVION ? : L aile est courbee en haut, plate en bas. L air va plus vite au-dessus, donc pression plus faible au-dessus. Ca cree une force vers le haut = portance.",
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
    if q_low in ["stop", "arrete", "arreter", "stop entrainement", "quitter", "quitter entrainement", "exit", "sortir"]:
        if st.session_state.mode_train:
            st.session_state.mode_train = False
            st.session_state.train_q = None
            return "Entrainement termine ! Score final : " + str(st.session_state.score) + "/" + str(st.session_state.total_quiz) + " | Meilleur streak : " + str(st.session_state.best_streak) + " ! Bravo !"
        else:
            return "Tu n es pas en entrainement. Clique sur MODE ENTRAINEMENT en haut pour commencer !"
    if st.session_state.mode_train and st.session_state.train_q is not None:
        bonne = nettoyer(st.session_state.train_a)
        st.session_state.total_quiz += 1
        if bonne in q_low or q_low in bonne or q_low == bonne:
            st.session_state.score += 1
            st.session_state.streak += 1
            if st.session_state.streak > st.session_state.best_streak:
                st.session_state.best_streak = st.session_state.streak
            rep = "BRAVO ! Bonne reponse ! C etait bien " + st.session_state.train_a + " ! Score : " + str(st.session_state.score) + "/" + str(st.session_state.total_quiz) + " | Streak : " + str(st.session_state.streak)
        else:
            st.session_state.streak = 0
            rep = "Pas tout a fait... La bonne reponse c etait " + st.session_state.train_a + ". Score : " + str(st.session_state.score) + "/" + str(st.session_state.total_quiz)
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
        elif st.session_state.niveau == "10h":
            nq, na = random.choice(TRAIN_10H)
        else:
            nq, na = random.choice(TRAIN_MOYEN)
        st.session_state.train_q = nq
        st.session_state.train_a = na
        return rep + "\n\nQuestion suivante (" + st.session_state.niveau + ") : " + nq + "\n\nPour quitter, clique sur QUITTER ENTRAINEMENT ou ecris stop."
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
                return "MERCI ! J ai appris ! " + cle + " = " + val + " ! J ai appris " + str(len(st.session_state.learned)) + " choses !"
            else:
                st.session_state.learned[nettoyer(texte)] = texte
                return "Merci ! J ai retenu : " + texte + " !"
        except:
            return "Pour m apprendre, ecris : Apprends : c est quoi le foot = le foot c est un sport avec un ballon"
    if "montre ce que tu as appris" in q_low or "ce que tu as appris" in q_low:
        if len(st.session_state.learned) == 0:
            return "Je n ai encore rien appris... Apprends-moi : Apprends : c est quoi le foot = ..."
        txt = "CE QUE TU M AS APPRIS (" + str(len(st.session_state.learned)) + ") :\n\n"
        for k, v in st.session_state.learned.items():
            txt += "- " + k + " = " + v + "\n"
        return txt
    for cle, val in st.session_state.learned.items():
        if cle in q_low or q_low in cle:
            return "Ce que TU m as appris : " + val + " (merci !)"
    if any(c in q_brut for c in ["+", "x", "*", "/", "-"]) and any(c.isdigit() for c in q_brut):
        calc = calculer(q_brut)
        if calc:
            return calc
    for cle, rep in BASES.items():
        if nettoyer(cle) in q_low or q_low == nettoyer(cle):
            return rep
    if "merci" in q_low:
        return BASES["merci"]
    if "bonjour" in q_low or "salut" in q_low or "slt" in q_low:
        return BASES["bonjour"]
    if "blague" in q_low:
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
            n = int("".join(filter(str.isdigit, q)))
            return table_division(n)
        except:
            return "Essaie : Table de division de 8"
    if "table de" in q or "table du" in q:
        try:
            n = int("".join(filter(str.isdigit, q)))
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
        return "J ai plein de capitales ! Essaie : capitale du Japon..."
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
    return "Hmm, je ne connais pas encore : " + q_orig + " ... Mais tu peux M APPRENDRE ! Ecris : Apprends : " + q_orig + " = ta reponse ici. Essaie : MODE ENTRAINEMENT / Conjugue ETRE / C est quoi Pythagore ? / C est quoi PI ?"

if st.session_state.auto_q:
    q_auto = st.session_state.auto_q
    st.session_state.auto_q = ""
    r_auto = trouver(q_auto)
    st.session_state.messages.append({"role": "assistant", "content": r_auto})
    with st.chat_message("assistant"):
        st.write(r_auto)

if question := st.chat_input("Pose ta question 10H, ou reponds a la question d entrainement ici !"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        r = trouver(question)
        st.write(r)
    st.session_state.messages.append({"role": "assistant", "content": r})
