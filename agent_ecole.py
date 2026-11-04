import streamlit as st
st.set_page_config(page_title="Agent Ecole V4 Finale", page_icon="🚀", layout="wide")
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
    st.title("🚀 Agent V4 Finale")
    st.success("100+ réponses !")
    st.write("📐 Maths : 20")
    st.write("🇫🇷 Français : 18")
    st.write("🇩🇪 Allemand : 12")
    st.write("🇬🇧 Anglais : 12")
    st.write("🌍 Géo / Histoire : 15")
    st.write("🔬 Sciences : 15")
    st.write("💻 Code : 15")
    st.divider()
    st.caption("Pose comme tu parles : C'est quoi... ?")
    if st.button("🗑️ Effacer"):
        st.session_state.messages = []
        st.rerun()
st.title("🚀 Agent Ecole V4 - Finale")
st.caption("Le max de questions. Pose comme tu parles.")
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Salut ! 👋 V4 finale. Pose-moi n'importe quoi : `C'est quoi le théorème de Pythagore ?`, `Comment on conjugue avoir ?`, `Pourquoi le ciel est bleu ?`, `C'est quoi la capitale du Japon ?`..."}]
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
def rep(q_orig):
    q = q_orig.lower()
    # Nettoyage pour comprendre les vraies phrases
    for mot in ["c'est quoi", "c est quoi", "c'est", "comment", "pourquoi", "donne-moi", "donne moi", "explique", "?", "le ", "la ", "les ", "un ", "une ", "des "]:
        q = q.replace(mot, " ")
    q = " ".join(q.split())
    # MATHS - 20
    if "pythagore" in q: return """**📐 C'est quoi le théorème de Pythagore ?**
Formule : **a² + b² = c²**
Exemple : 3-4-5 car 9+16=25. Ça sert à calculer le côté manquant d'un triangle rectangle.
```python
import math
print(math.sqrt(3**2 + 4**2)) # 5.0
```"""
    if "thales" in q: return "**📐 Thalès :** Si 2 droites parallèles coupent 2 sécantes, les rapports sont égaux. Pour les triangles emboîtés."
    if "moyenne" in q: return "📐 **Moyenne** = somme / nombre. Ex: (12+15+18)/3 = 15"
    if "mediane" in q: return "📐 **Médiane** = valeur du milieu triée. Ex: 5, 9, 12 -> 9"
    if "aire" in q: return "📐 **Aire :** Rectangle = L x l. Carré = c². Triangle = (b x h)/2. Cercle = pi x r²"
    if "perimetre" in q: return "📐 **Périmètre :** Carré = 4 x côté. Rectangle = 2x(L+l). Cercle = 2 x pi x r"
    if "volume" in q: return "📐 **Volume :** Cube = c³. Pavé = L x l x h. Cylindre = pi x r² x h"
    if "fraction" in q: return "📐 **Fraction :** 1/2 + 1/4 = 3/4. On met au même dénominateur."
    if "pourcentage" in q: return "📐 **Pourcentage :** 20% de 50 = 10. On fait 50 x 0.20"
    if "equation" in q: return "📐 **Equation :** 2x+3=7 -> 2x=4 -> x=2. On isole x."
    if "pair" in q: return "📐 **Pair :** 8 pair, 7 impair. Reste de /2 = 0 = pair."
    if "table" in q or "multiplication" in q: return "📐 **Table de 7 :** 7, 14, 21, 28, 35, 42, 49, 56, 63, 70"
    if "division" in q: return "📐 **Division :** Dividende / Diviseur = Quotient + Reste. Ex: 17/5 = 3 reste 2"
    if "puissance" in q: return "📐 **Puissance :** 2³ = 2x2x2 = 8. 10² = 100."
    if "racine" in q: return "📐 **Racine carrée :** √25 = 5 car 5x5=25. √16 = 4"
    if "angle" in q: return "📐 **Angles :** Droit = 90°. Plat = 180°. Aigu < 90°. Obtus > 90°. Somme triangle = 180°."
    if "symetrie" in q: return "📐 **Symétrie :** C'est comme un miroir. L'axe de symétrie coupe en 2 parties identiques."
    if "probabilite" in q: return "📐 **Probabilité :** Chance sur total. Ex: pile ou face = 1/2 = 50%."
    if "proportion" in q: return "📐 **Proportion :** Si 3 stylos = 6 CHF, 6 stylos = 12 CHF. C'est x2."
    if "decimal" in q: return "📐 **Décimal :** 0.5 = 1/2. 0.25 = 1/4. 0.75 = 3/4."
    # FRANCAIS - 18
    if "etre" in q: return "🇫🇷 **ÊTRE :** je suis, tu es, il est, nous sommes, vous êtes, ils sont"
    if "avoir" in q: return "🇫🇷 **AVOIR :** j'ai, tu as, il a, nous avons, vous avez, ils ont"
    if "aller" in q: return "🇫🇷 **ALLER :** je vais, tu vas, il va, nous allons, vous allez, ils vont"
    if "faire" in q: return "🇫🇷 **FAIRE :** je fais, tu fais, il fait, nous faisons, vous faites, ils font"
    if "pluriel" in q: return "🇫🇷 **Pluriel :** chat->chats. cheval->chevaux. bateau->bateaux. hibou->hiboux"
    if "adjectif" in q: return "🇫🇷 **Adjectif :** Décrit un nom. grand garçon / grande fille. Il s'accorde."
    if "verbe" in q: return "🇫🇷 **Verbe :** Mot d'action. 1er groupe -er, 2ème -ir, 3ème irréguliers."
    if "sujet" in q: return "🇫🇷 **Sujet :** Qui fait l'action ? *Le chat* mange. Le chat = sujet."
    if "complement" in q: return "🇫🇷 **COD = Quoi ? COI = À qui ?** Ex: Je mange *une pomme* (COD). Je parle *à Paul* (COI)."
    if "homophone" in q or "a" in q and "à" in q: return "🇫🇷 **a / à :** a = avoir (il a). à = lieu (je vais à l'école). Remplace par avait."
    if "son" in q and "sont" in q: return "🇫🇷 **son / sont :** son = possessif (son chien). sont = être (ils sont)."
    if "et" in q and "est" in q: return "🇫🇷 **et / est :** et = liaison (toi et moi). est = être (il est)."
    if "feminin" in q: return "🇫🇷 **Féminin :** On ajoute e. grand->grande. beau->belle. blanc->blanche."
    if "passe compose" in q: return "🇫🇷 **Passé composé :** Auxiliaire être/avoir + participe passé. Ex: J'ai mangé. Je suis allé."
    if "imparfait" in q: return "🇫🇷 **Imparfait :** Pour une habitude. Ex: Quand j'étais petit, je jouais. Terminaisons : -ais, -ais, -ait, -ions, -iez, -aient."
    if "futur" in q: return "🇫🇷 **Futur :** Je mangerai, tu mangeras, il mangera... On ajoute -ai, -as, -a..."
    if "synonyme" in q: return "🇫🇷 **Synonyme :** Mot qui veut dire pareil. Ex: grand = immense. Contraire = antonyme."
    if "antonyme" in q: return "🇫🇷 **Antonyme :** Contraire. Ex: grand <-> petit. chaud <-> froid."
    # ALLEMAND - 12
    if "der" in q or "die das" in q: return "🇩🇪 **der die das :** der=masculin, die=féminin, das=neutre. Pluriel = die"
    if "sein" in q: return "🇩🇪 **SEIN :** ich bin, du bist, er ist, wir sind, ihr seid, sie sind"
    if "haben" in q: return "🇩🇪 **HABEN :** ich habe, du hast, er hat, wir haben, ihr habt, sie haben"
    if "bonjour" in q and "allemand" in q: return "🇩🇪 **Bonjour = Hallo. Merci = Danke. Au revoir = Tschüss. S'il te plaît = Bitte.**"
    if "chiffre" in q and "allemand" in q: return "🇩🇪 **Chiffres :** eins=1, zwei=2, drei=3, vier=4, fünf=5, sechs=6, sieben=7, acht=8, neun=9, zehn=10"
    if "couleur" in q and "allemand" in q: return "🇩🇪 **Couleurs :** rot=rouge, blau=bleu, grün=vert, gelb=jaune, schwarz=noir, weiß=blanc"
    if "famille" in q and "allemand" in q: return "🇩🇪 **Famille :** Mutter=maman, Vater=papa, Bruder=frère, Schwester=sœur"
    if "ecole" in q and "allemand" in q: return "🇩🇪 **Ecole :** die Schule, der Lehrer=prof, das Buch=livre, der Stift=stylo"
    if "animal" in q and "allemand" in q: return "🇩🇪 **Animaux :** der Hund=chien, die Katze=chat, das Pferd=cheval, der Vogel=oiseau"
    if "manger" in q and "allemand" in q: return "🇩🇪 **Manger = essen. Boire = trinken. J'ai faim = Ich habe Hunger.**"
    if "aimer" in q and "allemand" in q: return "🇩🇪 **Aimer = lieben / mögen. J'aime = Ich mag. J'adore = Ich liebe.**"
    if "heure" in q and "allemand" in q: return "🇩🇪 **Heure :** Wie spät ist es ? = Quelle heure est-il ? Es ist 3 Uhr = Il est 3h"
    # ANGLAIS - 12
    if "to be" in q: return "🇬🇧 **TO BE :** I am, You are, He is, We are, You are, They are"
    if "to have" in q or "have" in q: return "🇬🇧 **TO HAVE :** I have, You have, He has, We have, You have, They have"
    if "vocabulaire" in q and "anglais" in q: return "🇬🇧 **Vocab :** Hello=Bonjour, Thank you=Merci, Friend=Ami, School=Ecole, Dog=Chien"
    if "couleur" in q and "anglais" in q: return "🇬🇧 **Couleurs :** red=rouge, blue=bleu, green=vert, yellow=jaune, black=noir"
    if "chiffre" in q and "anglais" in q: return "🇬🇧 **Chiffres :** one=1, two=2, three=3, four=4, five=5, six=6, seven=7, eight=8, nine=9, ten=10"
    if "present" in q and "anglais" in q: return "🇬🇧 **Present Simple :** I play, He plays (+s). Ex: He plays football."
    if "famille" in q and "anglais" in q: return "🇬🇧 **Famille :** Mother=maman, Father=papa, Brother=frère, Sister=sœur"
    if "heure" in q and "anglais" in q: return "🇬🇧 **Heure :** What time is it ? = Quelle heure ? It is 3 o'clock = Il est 3h"
    if "animal" in q and "anglais" in q: return "🇬🇧 **Animaux :** Dog=chien, Cat=chat, Horse=cheval, Bird=oiseau, Fish=poisson"
    if "manger" in q and "anglais" in q: return "🇬🇧 **Manger = to eat. Boire = to drink. I am hungry = J'ai faim.**"
    if "ecole" in q and "anglais" in q: return "🇬🇧 **Ecole :** School=école, Teacher=prof, Book=livre, Pen=stylo"
    if "bonjour" in q and "anglais" in q: return "🇬🇧 **Bonjour = Hello / Hi. Merci = Thank you. Au revoir = Goodbye.**"
    # GEO / HISTOIRE - 15
    if "capitale" in q:
        if "france" in q: return "🌍 **Capitale France = Paris**"
        if "suisse" in q: return "🌍 **Capitale Suisse = Berne**"
        if "allemagne" in q: return "🌍 **Capitale Allemagne = Berlin**"
        if "italie" in q: return "🌍 **Capitale Italie = Rome**"
        if "japon" in q: return "🌍 **Capitale Japon = Tokyo**"
        if "espagne" in q: return "🌍 **Capitale Espagne = Madrid**"
        return "🌍 **Capitales :** France=Paris, Suisse=Berne, Allemagne=Berlin, Italie=Rome, Espagne=Madrid, Angleterre=Londres, Japon=Tokyo, USA=Washington"
    if "canton" in q: return "🌍 **Suisse :** 26 cantons. Zurich, Berne, Vaud, Genève, Fribourg, Valais..."
    if "guerre" in q: return "📜 **2ème Guerre :** 1939-1945. Suisse neutre. 1ère Guerre : 1914-1918."
    if "revolution" in q: return "📜 **Révolution française :** 1789. Prise de la Bastille le 14 juillet 1789."
    if "continent" in q: return "🌍 **Continents :** Europe, Afrique, Asie, Amérique, Océanie, Antarctique."
    if "ocean" in q: return "🌍 **Océans :** Pacifique (plus grand), Atlantique, Indien, Arctique, Antarctique."
    if "fleuve" in q: return "🌍 **Fleuves Suisse :** Rhône, Rhin, Aar. Lac Léman = plus grand lac."
    if "rome" in q: return "📜 **Rome :** Fondée en -753. Colisée, Jules César, Empire romain."
    if "moyen age" in q: return "📜 **Moyen Âge :** 476-1492. Châteaux, chevaliers, cathédrales."
    if "dinosaure" in q: return "🦖 **Dinosaures :** T-Rex=carnivore. Diplodocus=herbivore géant. Disparus il y a 66M d'années."
    if "egypte" in q: return "📜 **Egypte :** Pyramides, Pharaons, Hiéroglyphes, Nil. Cléopâtre."
    if "napoleon" in q: return "📜 **Napoléon :** Empereur français 1804-1815. Bataille de Waterloo 1815."
    if "suisse" in q and "histoire" in q: return "📜 **Suisse :** Fondée en 1291. Neutre depuis 1515. 26 cantons."
    if "drapeau" in q: return "🌍 **Drapeau Suisse :** Croix blanche sur fond rouge. Carré, le seul drapeau carré au monde avec le Vatican."
    if "europe" in q: return "🌍 **Europe :** 44 pays. Union Européenne = 27 pays. Euro = monnaie."
    # SCIENCES - 15
    if "photosynthese" in q: return "🔬 **Photosynthèse :** Soleil + Eau + CO2 = Oxygène + Sucre"
    if "planete" in q: return "🔬 **Planètes :** Mercure, Vénus, Terre, Mars, Jupiter, Saturne, Uranus, Neptune"
    if "gravite" in q: return "🔬 **Gravité :** Ce qui nous attire vers la Terre. Newton + pomme."
    if "ciel bleu" in q or "ciel" in q: return "🔬 **Pourquoi le ciel est bleu ?** La lumière du Soleil est diffusée par l'air. Le bleu est le plus diffusé."
    if "coeur" in q or "corps" in q: return "🔬 **Corps :** Cœur pompe le sang. Cerveau commande. Poumons respirent. 206 os."
    if "electricite" in q: return "🔬 **Électricité :** Tension en Volts, Courant en Ampères. Circuit = pile + lampe + interrupteur."
    if "lune" in q: return "🔬 **Lune :** Tourne autour de la Terre en 27 jours. Elle reflète le Soleil."
    if "solaire" in q: return "🔬 **Solaire :** Soleil = étoile. Terre tourne autour en 365 jours = 1 an."
    if "animal" in q: return "🔬 **Animaux :** Mammifère=allaite, Oiseau=plumes, Reptile=écailles, Poisson=nageoires."
    if "plante" in q: return "🔬 **Plante :** Racine + Tige + Feuilles + Fleur. Besoin de soleil et d'eau."
    if "eau" in q: return "🔬 **Eau = H2O. Sel = NaCl. Oxygène = O2. CO2 = dioxyde de carbone.**"
    if "foudre" in q: return "⚡ **Foudre :** Décharge électrique à 30 000°C, 5x plus chaud que le Soleil. Elle tombe car l'air devient conducteur."
    if "volcan" in q: return "🌋 **Volcan :** Magma qui sort. Lave = magma dehors. Cendres + gaz."
    if "saison" in q: return "🔬 **Saisons :** C'est l'inclinaison de la Terre qui fait les saisons, pas la distance au Soleil."
    if "evolution" in q: return "🔬 **Évolution :** Darwin. Les espèces changent avec le temps pour s'adapter."
    # CODE - 15
    if "bonjour" in q or "prenom" in q: return "💻 **Code Bonjour :**\n```python\nprenom = input('Ton prénom ? ')\nprint(f'Bonjour {prenom} !')\n```"
    if "boucle" in q: return "💻 **Boucle :** `for i in range(1,6): print(i)` -> 1,2,3,4,5"
    if "condition" in q: return "💻 **Condition :** `if age >= 18: print('Majeur') else: print('Mineur')`"
    if "liste" in q: return "💻 **Liste :** `notes = [12, 15, 18]` puis `print(notes[0])` -> 12"
    if "fonction" in q: return "💻 **Fonction :** `def bonjour(): print('Salut')` puis `bonjour()`"
    if "variable" in q: return "💻 **Variable :** `age = 13` `nom = 'Lenny'` C'est une boîte qui stocke."
    if "jeu" in q: return "💻 **Jeu devinette :** `import random` `secret = random.randint(1,10)`"
    if "html" in q: return "💻 **HTML :** `<h1>Titre</h1> <p>Texte</p> <button>Clique</button>`"
    if "css" in q: return "💻 **CSS :** `body { background-color: black; color: white; }` C'est le style."
    if "python" in q: return "💻 **Python :** Langage facile et puissant. C'est celui de ton agent."
    if "erreur" in q: return "💻 **Erreur :** 99% c'est une parenthèse ou un guillemet oublié. Lis le message rouge."
    if "print" in q: return "💻 **Print :** `print('Salut')` affiche Salut. C'est la base."
    if "input" in q: return "💻 **Input :** `prenom = input('Ton prénom ?')` Demande à l'utilisateur."
    if "random" in q: return "💻 **Random :** `import random` `print(random.randint(1,10))` Nombre au hasard."
    if "streamlit" in q: return "💻 **Streamlit :** C'est ce qui fait ton agent. `streamlit run agent_ecole.py` pour lancer."
    return f"Je ne connais pas encore : **{q_orig}**. Essaie : C'est quoi le théorème de Pythagore ?, C'est quoi la photosynthèse ?, C'est quoi un adjectif ?, Pourquoi le ciel est bleu ?, C'est quoi la capitale du Japon ?"
if question := st.chat_input("Pose ta question comme tu parles..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        r = rep(question)
        st.write(r)
    st.session_state.messages.append({"role": "assistant", "content": r})
