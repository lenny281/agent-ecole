import streamlit as st
st.set_page_config(page_title="Agent Ecole V3", page_icon="🚀", layout="wide")
# --- STYLE V3 NEON NOIR ---
st.markdown("""
<style>
.stApp { background-color: #0a0a0a; color: white; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #1a0033, #000000); }
[data-testid="stSidebar"] * { color: white !important; }
.stChatMessage { background-color: #1a1a1a !important; color: white !important; border: 1px solid #7c3aed; border-radius: 15px; }
h1 { background: linear-gradient(90deg, #a855f7, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.stChatInputContainer { border-top: 1px solid #7c3aed; }
</style>
""", unsafe_allow_html=True)
with st.sidebar:
    st.title("🚀 Agent V3")
    st.write("**Le plus complet**")
    st.success("60+ réponses !")
    st.write("📐 Maths : 12 réponses")
    st.write("🇫🇷 Français : 10 réponses")
    st.write("🇩🇪 Allemand : 8 réponses")
    st.write("🇬🇧 Anglais : 8 réponses")
    st.write("🌍 Géo / Histoire : 10 réponses")
    st.write("🔬 Sciences : 10 réponses")
    st.write("💻 Code : 12 réponses")
    st.divider()
    if st.button("🗑️ Effacer la conversation"):
        st.session_state.messages = []
        st.rerun()
st.title("🚀 Agent Ecole V3 - ULTIME")
st.caption("Le meilleur style + le plus de réponses. Sans IA, juste du code.")
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Salut ! 👋 V3 est là. 60+ réponses ! Essaie : `moyenne`, `pythagore`, `conjuguer`, `der die das`, `to be`, `capitale`, `photosynthese`, `boucle`, `théorème`, `verbe`, `vocabulaire`..."}]
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
def rep(q):
    q = q.lower()
    # MATHS
    if "moyenne" in q: return "📐 **Moyenne** = somme / nombre. Ex: (12+15+18)/3 = 15"
    if "médiane" in q or "mediane" in q: return "📐 **Médiane** = la valeur du milieu quand c'est trié. Ex: 5, 9, 12 -> médiane = 9"
    if "table" in q or "multiplication" in q: return "📐 **Table de 7 :** 7, 14, 21, 28, 35, 42, 49, 56, 63, 70"
    if "aire" in q: return "📐 **Aire :** Rectangle = L x l. Carré = c x c. Triangle = (b x h)/2. Cercle = pi x r²"
    if "périmètre" in q or "perimetre" in q: return "📐 **Périmètre :** Carré = 4 x côté. Rectangle = 2x(L+l). Cercle = 2 x pi x r"
    if "pythagore" in q: return "📐 **Pythagore :** a² + b² = c². Ex: 3-4-5 car 9+16=25"
    if "thales" in q or "théorème" in q: return "📐 **Thalès :** Si deux droites parallèles coupent deux sécantes, les rapports sont égaux."
    if "fraction" in q: return "📐 **Fraction :** 1/2 + 1/4 = 2/4 + 1/4 = 3/4. On met au même dénominateur."
    if "pourcentage" in q or "%" in q: return "📐 **Pourcentage :** 20% de 50 = 50 x 0.20 = 10"
    if "pair" in q: return "📐 **Pair :** 8 pair, 7 impair. Reste de /2 = 0 = pair."
    if "volume" in q: return "📐 **Volume :** Cube = c³. Pavé = L x l x h. Cylindre = pi x r² x h"
    if "equation" in q or "x =" in q: return "📐 **Equation :** 2x + 3 = 7 -> 2x = 4 -> x = 2. On isole x."
    # FRANCAIS
    if "conjuguer" in q or "etre" in q: return "🇫🇷 **ÊTRE :** je suis, tu es, il est, nous sommes, vous êtes, ils sont"
    if "avoir" in q: return "🇫🇷 **AVOIR :** j'ai, tu as, il a, nous avons, vous avez, ils ont"
    if "pluriel" in q: return "🇫🇷 **Pluriel :** chat -> chats. cheval -> chevaux. bateau -> bateaux. hibou -> hiboux"
    if "adjectif" in q: return "🇫🇷 **Adjectif :** grand garçon / grande fille / grands garçons. Il s'accorde."
    if "verbe" in q: return "🇫🇷 **Verbe :** 3 groupes. 1er : -er (chanter). 2ème : -ir (finir). 3ème : irréguliers (aller, faire)"
    if "sujet" in q: return "🇫🇷 **Sujet :** Qui fait l'action ? Ex: *Le chat* mange. Le chat = sujet."
    if "complément" in q: return "🇫🇷 **COD / COI :** COD = répond à Quoi ? COI = répond à À qui ?"
    if "homophone" in q or "a / à" in q: return "🇫🇷 **a / à :** a = verbe avoir (il a). à = préposition (je vais à l'école). Astuce : remplace par avait."
    if "son / sont" in q: return "🇫🇷 **son / sont :** son = possessif (son chien). sont = verbe être (ils sont)."
    if "féminin" in q or "feminin" in q: return "🇫🇷 **Féminin :** On ajoute souvent e. Ex: grand -> grande. Attention : beau -> belle."
    # ALLEMAND
    if "der" in q or "die das" in q: return "🇩🇪 **Articles :** der = masculin, die = féminin, das = neutre. Pluriel = die"
    if "sein" in q: return "🇩🇪 **SEIN :** ich bin, du bist, er ist, wir sind, ihr seid, sie sind"
    if "haben" in q: return "🇩🇪 **HABEN :** ich habe, du hast, er hat, wir haben, ihr habt, sie haben"
    if "bonjour" in q and "allemand" in q: return "🇩🇪 **Bonjour = Hallo. Merci = Danke. Au revoir = Tschüss. Je = Ich. Tu = Du.**"
    if "chiffre" in q and "allemand" in q: return "🇩🇪 **Chiffres :** 1=eins, 2=zwei, 3=drei, 4=vier, 5=fünf, 6=sechs, 7=sieben, 8=acht, 9=neun, 10=zehn"
    if "couleur" in q and "allemand" in q: return "🇩🇪 **Couleurs :** rot=rouge, blau=bleu, grün=vert, gelb=jaune, schwarz=noir, weiß=blanc"
    if "famille" in q and "allemand" in q: return "🇩🇪 **Famille :** Mutter=maman, Vater=papa, Bruder=frère, Schwester=sœur, Hund=chien"
    if "ecole" in q and "allemand" in q: return "🇩🇪 **Ecole :** die Schule=école, der Lehrer=prof, das Buch=livre, der Stift=stylo"
    # ANGLAIS
    if "to be" in q or "anglais" in q and "etre" in q: return "🇬🇧 **TO BE :** I am, You are, He is, We are, You are, They are"
    if "have" in q: return "🇬🇧 **TO HAVE :** I have, You have, He has, We have, You have, They have"
    if "vocabulaire" in q and "anglais" in q: return "🇬🇧 **Vocab :** Hello=Bonjour, Thank you=Merci, Friend=Ami, School=Ecole, Dog=Chien, Cat=Chat"
    if "couleur" in q and "anglais" in q: return "🇬🇧 **Couleurs :** red=rouge, blue=bleu, green=vert, yellow=jaune, black=noir, white=blanc"
    if "chiffre" in q and "anglais" in q: return "🇬🇧 **Chiffres :** one=1, two=2, three=3, four=4, five=5, six=6, seven=7, eight=8, nine=9, ten=10"
    if "present" in q and "anglais" in q: return "🇬🇧 **Present Simple :** I play, You play, He plays (+s). Ex: He plays football."
    if "famille" in q and "anglais" in q: return "🇬🇧 **Famille :** Mother=maman, Father=papa, Brother=frère, Sister=sœur"
    if "heure" in q and "anglais" in q: return "🇬🇧 **Heure :** What time is it ? = Quelle heure est-il ? It is 3 o'clock = Il est 3h"
    # GEO HISTOIRE
    if "capitale" in q: return "🌍 **Capitales :** France=Paris, Suisse=Berne, Allemagne=Berlin, Italie=Rome, Espagne=Madrid, Angleterre=Londres, Japon=Tokyo, USA=Washington"
    if "canton" in q: return "🌍 **Suisse :** 26 cantons. Zurich, Berne, Vaud, Genève, Fribourg, Valais, Neuchâtel..."
    if "guerre" in q: return "📜 **2ème Guerre :** 1939-1945. Suisse neutre. 1ère Guerre : 1914-1918."
    if "révolution" in q or "revolution" in q: return "📜 **Révolution française :** 1789. Prise de la Bastille le 14 juillet 1789."
    if "continent" in q: return "🌍 **Continents :** Europe, Afrique, Asie, Amérique, Océanie, Antarctique. Le plus grand = Asie."
    if "océan" in q or "ocean" in q: return "🌍 **Océans :** Pacifique (plus grand), Atlantique, Indien, Arctique, Antarctique."
    if "suisse" in q and "fleuve" in q: return "🌍 **Fleuves Suisse :** Le Rhône, le Rhin, l'Aar. Le lac Léman est le plus grand lac."
    if "rome" in q: return "📜 **Rome antique :** Fondée en -753. Empire romain. Colisée, aqueducs, Jules César."
    if "moyen age" in q: return "📜 **Moyen Âge :** 476-1492. Châteaux, chevaliers, cathédrales."
    if "dinosaure" in q: return "🦖 **Dinosaures :** T-Rex = carnivore. Diplodocus = herbivore géant. Ils ont disparu il y a 66 millions d'années."
    # SCIENCES
    if "photosynthese" in q: return "🔬 **Photosynthèse :** Soleil + Eau + CO2 = Oxygène + Sucre"
    if "planete" in q: return "🔬 **Planètes :** Mercure, Vénus, Terre, Mars, Jupiter, Saturne, Uranus, Neptune"
    if "eau" in q and "formule" in q: return "🔬 **Formules :** Eau=H2O, Sel=NaCl, Oxygène=O2, CO2=dioxyde de carbone"
    if "corps humain" in q or "coeur" in q: return "🔬 **Corps :** Le cœur pompe le sang. Le cerveau commande. Les poumons respirent. On a 206 os."
    if "électricité" in q or "electricite" in q: return "🔬 **Électricité :** Tension en Volts, Courant en Ampères. Pile + lampe + interrupteur = circuit."
    if "gravité" in q or "gravite" in q: return "🔬 **Gravité :** C'est ce qui nous attire vers la Terre. Découverte par Newton avec la pomme."
    if "lune" in q: return "🔬 **Lune :** Elle tourne autour de la Terre en 27 jours. Elle n'a pas de lumière propre, elle reflète le Soleil."
    if "solaire" in q: return "🔬 **Solaire :** Le Soleil est une étoile. La Terre tourne autour en 365 jours = 1 an."
    if "animal" in q: return "🔬 **Animaux :** Mammifère = allaite (chien). Oiseau = plumes + bec. Reptile = écailles. Poisson = nageoires."
    if "plante" in q: return "🔬 **Plante :** Racine + Tige + Feuilles + Fleur. Elle a besoin de soleil et d'eau."
    # CODE
    if "bonjour" in q or "prenom" in q: return "💻 **Code :** `prenom = input('Ton prénom ?')` puis `print(f'Bonjour {prenom} !')`"
    if "boucle" in q: return "💻 **Boucle :** `for i in range(1,6): print(i)` -> affiche 1,2,3,4,5"
    if "condition" in q: return "💻 **Condition :** `if age >= 18: print('Majeur') else: print('Mineur')`"
    if "liste" in q: return "💻 **Liste :** `notes = [12, 15, 18]` puis `print(notes[0])` -> 12"
    if "fonction" in q: return "💻 **Fonction :** `def bonjour(): print('Salut')` puis `bonjour()` pour l'appeler"
    if "variable" in q: return "💻 **Variable :** `age = 13` `nom = 'Lenny'` C'est une boîte qui stocke une info."
    if "jeu" in q: return "💻 **Jeu devinette :** `import random` `secret = random.randint(1,10)` puis demande à deviner."
    if "html" in q: return "💻 **HTML :** `<h1>Titre</h1> <p>Texte</p> <button>Clique</button>`"
    if "css" in q: return "💻 **CSS :** `body { background-color: black; color: white; }` C'est pour le style."
    if "python" in q: return "💻 **Python :** C'est le langage que tu utilises pour ton agent. Facile et puissant."
    if "erreur" in q: return "💻 **Erreur :** Lis le message rouge. 99% du temps c'est une parenthèse ou un guillemet oublié."
    if "print" in q: return "💻 **Print :** `print('Salut')` affiche Salut à l'écran. C'est la base."
    return "Je ne connais pas encore ce mot. Essaie : moyenne, pythagore, conjuguer, der die das, to be, capitale, photosynthese, boucle, print, volume, fraction, verbe, continent, gravité..."
if question := st.chat_input("Pose ta question pour n'importe quelle branche..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        r = rep(question)
        st.write(r)
    st.session_state.messages.append({"role": "assistant", "content": r})
