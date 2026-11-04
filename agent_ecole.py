import streamlit as st

st.set_page_config(page_title="Agent V5 - 1000 Lignes", page_icon="🚀", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #0a0a0a; color: white; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #1a0033, #000000); }
[data-testid="stSidebar"] * { color: white !important; }
.stChatMessage { background-color: #1a1a1a !important; color: white !important; border: 1px solid #7c3aed; border-radius: 15px; }
h1 { background: linear-gradient(90deg, #a855f7, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🚀 Agent V5")
    st.success("Structure 1000 lignes !")
    st.write("Chaque ligne = 1 question")
    st.write("Tu as déjà 150 questions dedans.")
    st.write("Pour aller à 1000, copie une ligne et change la question.")
    if st.button("🗑️ Effacer"):
        st.session_state.messages = []
        st.rerun()

st.title("🚀 Agent V5 - 1000 Lignes")
st.caption("Le même style, mais prêt pour 1000 questions.")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Salut ! 👋 V5 avec structure 1000 lignes. Pose-moi n'importe quoi, j'ai 150 réponses déjà, et tu peux en ajouter 850 en 1 minute."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- BASE DE DONNÉES : 1 LIGNE = 1 QUESTION ---
# Pour arriver à 1000 lignes, tu copies une ligne et tu changes le mot-clé et la réponse.
# Exemple : "napoleon": "Napoléon...",

BASE = {
    # MATHS - 30 questions
    "pythagore": "📐 Pythagore : a² + b² = c². Ex: 3-4-5",
    "thales": "📐 Thalès : Rapports égaux si droites parallèles.",
    "moyenne": "📐 Moyenne = somme / nombre. Ex: (12+15+18)/3=15",
    "mediane": "📐 Médiane = valeur du milieu triée.",
    "aire": "📐 Aire : Rectangle=Lxl, Carré=c², Triangle=(b×h)/2, Cercle=pi×r²",
    "perimetre": "📐 Périmètre : Carré=4×côté, Rectangle=2×(L+l), Cercle=2×pi×r",
    "volume": "📐 Volume : Cube=c³, Pavé=L×l×h",
    "fraction": "📐 Fraction : 1/2+1/4=3/4. Même dénominateur.",
    "pourcentage": "📐 Pourcentage : 20% de 50 = 10",
    "equation": "📐 Equation : 2x+3=7 -> x=2",
    "pair": "📐 Pair : 8 pair, 7 impair",
    "table": "📐 Table de 7 : 7,14,21,28,35,42,49,56,63,70",
    "division": "📐 Division : 17/5 = 3 reste 2",
    "puissance": "📐 Puissance : 2³=8",
    "racine": "📐 Racine : √25=5",
    "angle": "📐 Angle droit=90°, Plat=180°, Triangle=180° total",
    "symetrie": "📐 Symétrie : comme un miroir",
    "probabilite": "📐 Probabilité : 1/2 = 50% pour pile ou face",
    "proportion": "📐 Proportion : 3 stylos=6CHF donc 6 stylos=12CHF",
    "decimal": "📐 Décimal : 0.5=1/2, 0.25=1/4",
    "multiple": "📐 Multiple : 12 est multiple de 3 et 4",
    "diviseur": "📐 Diviseur : 3 divise 12",
    "nombre premier": "📐 Nombre premier : divisible que par 1 et lui-même. Ex: 2,3,5,7,11",
    "pgcd": "📐 PGCD : Plus Grand Diviseur Commun",
    "ppcm": "📐 PPCM : Plus Petit Multiple Commun",
    "fonction": "📐 Fonction : f(x)=2x+1. Si x=3, f=7",
    "coordonnees": "📐 Coordonnées : (x,y). Ex: (2,3)",
    "vecteur": "📐 Vecteur : Flèche avec direction et longueur",
    "probabilité": "📐 Probabilité : Chance / Total",
    "statistique": "📐 Statistique : On étudie des données avec moyenne, médiane...",

    # FRANCAIS - 30
    "etre": "🇫🇷 ÊTRE : je suis, tu es, il est, nous sommes, vous êtes, ils sont",
    "avoir": "🇫🇷 AVOIR : j'ai, tu as, il a, nous avons, vous avez, ils ont",
    "aller": "🇫🇷 ALLER : je vais, tu vas, il va, nous allons, vous allez, ils vont",
    "faire": "🇫🇷 FAIRE : je fais, tu fais, il fait, nous faisons, vous faites, ils font",
    "pluriel": "🇫🇷 Pluriel : chat->chats, cheval->chevaux",
    "adjectif": "🇫🇷 Adjectif : Décrit un nom. grand garçon / grande fille",
    "verbe": "🇫🇷 Verbe : Mot d'action. 1er -er, 2ème -ir, 3ème irrégulier",
    "sujet": "🇫🇷 Sujet : Qui fait l'action ?",
    "complement": "🇫🇷 COD=Quoi ? COI=À qui ?",
    "passe compose": "🇫🇷 Passé composé : avoir/être + participe. J'ai mangé.",
    "imparfait": "🇫🇷 Imparfait : Habitude. Je jouais. -ais, -ais, -ait...",
    "futur": "🇫🇷 Futur : Je mangerai, tu mangeras...",
    "synonyme": "🇫🇷 Synonyme : Même sens. grand = immense",
    "antonyme": "🇫🇷 Antonyme : Contraire. grand <-> petit",
    "homophone": "🇫🇷 a=avoir, à=lieu. son=possessif, sont=être. et=liaison, est=être",
    "feminin": "🇫🇷 Féminin : grand->grande, beau->belle",
    "masculin": "🇫🇷 Masculin : C'est le genre de base. Ex: un garçon",
    "phrase": "🇫🇷 Phrase : Majuscule + point. Sujet + Verbe + Complément",
    "ponctuation": "🇫🇷 Ponctuation : . ? ! , ; : ...",
    "dialogue": "🇫🇷 Dialogue : Avec des guillemets et des tirets. Ex: - Bonjour !",
    "description": "🇫🇷 Description : On décrit avec des adjectifs et des détails.",
    "resume": "🇫🇷 Résumé : Raconter l'essentiel en plus court.",
    "dictée": "🇫🇷 Dictée : Écoute et écris sans faute. Astuce : relis 2 fois.",
    "poesie": "🇫🇷 Poésie : Avec des rimes et des vers. Ex: Alexandrin = 12 syllabes.",
    "conte": "🇫🇷 Conte : Il était une fois... Histoire imaginaire avec morale.",
    "fable": "🇫🇷 Fable : Histoire avec des animaux qui donne une leçon. La Fontaine.",
    "theatre": "🇫🇷 Théâtre : Dialogue à jouer sur scène. Molière.",
    "roman": "🇫🇷 Roman : Longue histoire inventée. Chapitres.",
    "auteur": "🇫🇷 Auteur : Celui qui écrit le livre.",
    "narrateur": "🇫🇷 Narrateur : Celui qui raconte l'histoire.",

    # ALLEMAND + ANGLAIS - 30
    "der": "🇩🇪 der=masculin, die=féminin, das=neutre",
    "sein": "🇩🇪 SEIN : ich bin, du bist, er ist, wir sind, ihr seid, sie sind",
    "haben": "🇩🇪 HABEN : ich habe, du hast, er hat, wir haben, ihr habt, sie haben",
    "to be": "🇬🇧 TO BE : I am, You are, He is, We are, You are, They are",
    "to have": "🇬🇧 TO HAVE : I have, You have, He has, We have, You have, They have",
    "hello": "🇬🇧 Hello = Bonjour. Hi = Salut.",
    "hallo": "🇩🇪 Hallo = Bonjour. Danke = Merci.",
    "famille anglais": "🇬🇧 Famille : Mother, Father, Brother, Sister",
    "famille allemand": "🇩🇪 Familie : Mutter, Vater, Bruder, Schwester",
    "couleur anglais": "🇬🇧 Couleurs : red, blue, green, yellow, black",
    "couleur allemand": "🇩🇪 Farben : rot, blau, grün, gelb, schwarz",
    "chiffre anglais": "🇬🇧 one=1, two=2, three=3, four=4, five=5",
    "chiffre allemand": "🇩🇪 eins=1, zwei=2, drei=3, vier=4, fünf=5",
    "animal anglais": "🇬🇧 Dog=chien, Cat=chat, Horse=cheval",
    "animal allemand": "🇩🇪 Hund=chien, Katze=chat, Pferd=cheval",
    "ecole anglais": "🇬🇧 School=école, Teacher=prof, Book=livre",
    "ecole allemand": "🇩🇪 Schule=école, Lehrer=prof, Buch=livre",
    "manger anglais": "🇬🇧 to eat=manger, to drink=boire",
    "manger allemand": "🇩🇪 essen=manger, trinken=boire",
    "heure anglais": "🇬🇧 What time is it ? = Quelle heure ?",
    "heure allemand": "🇩🇪 Wie spät ist es ? = Quelle heure ?",
    "aimer anglais": "🇬🇧 to like=aimer, to love=adorer",
    "aimer allemand": "🇩🇪 mögen=aimer, lieben=adorer",
    "present anglais": "🇬🇧 Present Simple : I play, He plays (+s)",
    "bonjour anglais": "🇬🇧 Hello=Bonjour, Thank you=Merci",
    "bonjour allemand": "🇩🇪 Hallo=Bonjour, Danke=Merci",
    "au revoir anglais": "🇬🇧 Goodbye=Au revoir",
    "au revoir allemand": "🇩🇪 Tschüss=Au revoir",
    "oui anglais": "🇬🇧 Yes=Oui, No=Non",
    "oui allemand": "🇩🇪 Ja=Oui, Nein=Non",

    # GEO HISTOIRE - 20
    "capitale": "🌍 Capitales : France=Paris, Suisse=Berne, Allemagne=Berlin, Italie=Rome, Japon=Tokyo",
    "canton": "🌍 Suisse : 26 cantons",
    "guerre": "📜 2ème Guerre : 1939-1945. Suisse neutre.",
    "revolution": "📜 Révolution : 1789, Bastille 14 juillet",
    "continent": "🌍 Continents : Europe, Afrique, Asie, Amérique, Océanie, Antarctique",
    "ocean": "🌍 Océans : Pacifique, Atlantique, Indien, Arctique, Antarctique",
    "rome": "📜 Rome : Fondée -753, Colisée, Jules César",
    "moyen age": "📜 Moyen Âge : 476-1492, Châteaux, chevaliers",
    "dinosaure": "🦖 Dinosaures : T-Rex carnivore, disparus il y a 66M ans",
    "egypte": "📜 Egypte : Pyramides, Pharaons, Nil",
    "napoleon": "📜 Napoléon : Empereur 1804-1815, Waterloo 1815",
    "drapeau": "🌍 Drapeau Suisse : Croix blanche sur rouge, carré",
    "europe": "🌍 Europe : 44 pays, UE = 27 pays",
    "fleuve": "🌍 Fleuves Suisse : Rhône, Rhin, Aar",
    "suisse histoire": "📜 Suisse : Fondée 1291, neutre depuis 1515",
    "viking": "📜 Vikings : Explorateurs du Nord, drakkars, 800-1100",
    "renaissance": "📜 Renaissance : 1400-1600, Léonard de Vinci, art",
    "invention": "📜 Inventions : Imprimerie 1450, Téléphone 1876, Internet 1969",
    "lune histoire": "🌙 Premier pas sur la Lune : 1969, Neil Armstrong",
    "decouverte": "🌍 Découverte Amérique : 1492, Christophe Colomb",

    # SCIENCES - 20
    "photosynthese": "🔬 Photosynthèse : Soleil + Eau + CO2 = Oxygène + Sucre",
    "planete": "🔬 Planètes : Mercure, Vénus, Terre, Mars, Jupiter, Saturne, Uranus, Neptune",
    "gravite": "🔬 Gravité : Nous attire vers la Terre. Newton + pomme.",
    "ciel bleu": "🔬 Ciel bleu : L'air diffuse le bleu du Soleil.",
    "coeur": "🔬 Cœur : Pompe le sang, 100 000 battements / jour",
    "electricite": "🔬 Électricité : Volts, Ampères. Circuit = pile + lampe",
    "lune": "🔬 Lune : Tourne autour de la Terre en 27 jours",
    "solaire": "🔬 Solaire : Soleil = étoile. Terre tourne en 365 jours",
    "animal": "🔬 Animaux : Mammifère, Oiseau, Reptile, Poisson",
    "plante": "🔬 Plante : Racine + Tige + Feuilles + Fleur",
    "eau": "🔬 Eau=H2O, Sel=NaCl, Oxygène=O2",
    "foudre": "⚡ Foudre : 30 000°C, 5x plus chaud que le Soleil",
    "volcan": "🌋 Volcan : Magma qui sort. Lave = magma dehors.",
    "saison": "🔬 Saisons : C'est l'inclinaison de la Terre.",
    "evolution": "🔬 Évolution : Darwin. Espèces qui s'adaptent.",
    "adn": "🔬 ADN : Code dans nos cellules qui dit qui on est.",
    "energie": "🔬 Énergie : Solaire, éolienne, hydraulique, nucléaire.",
    "climat": "🌍 Climat : Météo sur longtemps. Réchauffement = planète qui chauffe.",
    "recyclage": "♻️ Recyclage : Trier pour réutiliser. Papier, verre, plastique.",
    "espace": "🚀 Espace : Vide, sans air. ISS = station spatiale.",

    # CODE - 20
    "bonjour code": "💻 Code : prenom = input('Ton prénom ?') print(f'Bonjour {prenom} !')",
    "boucle": "💻 Boucle : for i in range(1,6): print(i)",
    "condition": "💻 Condition : if age >= 18: print('Majeur') else: print('Mineur')",
    "liste": "💻 Liste : notes = [12,15,18]",
    "variable": "💻 Variable : age = 13. C'est une boîte qui stocke.",
    "jeu": "💻 Jeu : import random, secret = random.randint(1,10)",
    "html": "💻 HTML : <h1>Titre</h1> <p>Texte</p>",
    "css": "💻 CSS : body { background-color: black; }",
    "python": "💻 Python : Langage facile, celui de ton agent.",
    "erreur": "💻 Erreur : 99% parenthèse ou guillemet oublié.",
    "print": "💻 Print : print('Salut') affiche Salut.",
    "input": "💻 Input : input('Ton prénom ?') demande à l'utilisateur.",
    "random": "💻 Random : random.randint(1,10) = nombre au hasard.",
    "streamlit": "💻 Streamlit : Ce qui fait ton agent. streamlit run agent_ecole.py",
    "fonction code": "💻 Fonction : def bonjour(): print('Salut')",
    "commentaire": "💻 Commentaire : # C'est pour expliquer, Python l'ignore.",
    "if": "💻 If : Si condition vraie, on fait ça.",
    "for": "💻 For : Pour répéter. for i in range(5):",
    "while": "💻 While : Tant que c'est vrai, on répète.",
    "debug": "💻 Debug : Chercher et corriger les bugs.",
}

def trouver(q):
    q2 = q.lower()
    for mot, rep in BASE.items():
        if mot in q2:
            return rep
    return f"Je ne connais pas encore : **{q}**. Essaie : pythagore, moyenne, conjuguer, der, to be, capitale, photosynthese, foudre, boucle... J'ai 150 réponses, et tu peux en ajouter 850 en copiant une ligne dans BASE."

if question := st.chat_input("Pose ta question..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        r = trouver(question)
        st.write(r)
    st.session_state.messages.append({"role": "assistant", "content": r})

