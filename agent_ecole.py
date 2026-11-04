import streamlit as st
st.set_page_config(page_title="Agent Ecole V3.1", page_icon="🚀", layout="wide")
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
    st.title("🚀 Agent V3.1")
    st.write("**Il comprend les vraies questions**")
    st.success("Essaie :")
    st.write("• C'est quoi le théorème de Pythagore ?")
    st.write("• C'est quoi la photosynthèse ?")
    st.write("• C'est quoi un adjectif ?")
    st.write("• C'est quoi la capitale de la France ?")
    if st.button("🗑️ Effacer"):
        st.session_state.messages = []
        st.rerun()
st.title("🚀 Agent Ecole V3.1")
st.caption("Pose ta question comme tu parles, il comprend.")
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Salut ! 👋 Pose-moi une vraie question comme : `C'est quoi le théorème de Pythagore ?` ou `C'est quoi la photosynthèse ?`"}]
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
def rep(q):
    q = q.lower()
    # On enlève les mots de question pour mieux comprendre
    q = q.replace("c'est quoi", "").replace("c est quoi", "").replace("c'est", "").replace("?", "").replace("le ", "").replace("la ", "").replace("un ", "").replace("une ", "").strip()
    # THEORÈME DE PYTHAGORE - VERSION COMPLÈTE
    if "pythagore" in q or "theoreme" in q:
        return """**📐 C'est quoi le théorème de Pythagore ?**
C'est la règle la plus célèbre des maths pour les triangles rectangles.
**La formule :**
> **a² + b² = c²**
**Exemple concret :**
Si ton triangle a un côté de 3 cm et un autre de 4 cm, l'hypoténuse c'est 5 cm.
Parce que : 3² + 4² = 9 + 16 = 25 et √25 = 5
**À quoi ça sert ?**
À calculer le côté qu'il te manque dans un triangle rectangle.
```python
import math
a = 3
b = 4
c = math.sqrt(a**2 + b**2)
print(c) # 5.0
```"""
    if "thales" in q:
        return """**📐 C'est quoi le théorème de Thalès ?**
Si deux droites parallèles coupent deux autres droites, alors les morceaux sont proportionnels.
**Exemple :** Si tu as un petit triangle dans un grand triangle, les côtés sont dans le même rapport."""
    if "photosynthese" in q:
        return """**🔬 C'est quoi la photosynthèse ?**
C'est comment la plante fabrique sa nourriture.
**La recette :**
Soleil + Eau + CO2 = Oxygène + Sucre
C'est grâce à ça que tu peux respirer ! Les plantes rejettent l'oxygène qu'on respire."""
    if "adjectif" in q:
        return """**🇫🇷 C'est quoi un adjectif ?**
C'est un mot qui décrit un nom.
Exemple : *Un **grand** garçon, une **belle** maison.*
Il s'accorde : grand garçon / grande fille / grands garçons."""
    if "capitale" in q:
        if "france" in q: return "🌍 **C'est quoi la capitale de la France ?** C'est **Paris**."
        if "suisse" in q: return "🌍 **C'est quoi la capitale de la Suisse ?** C'est **Berne**."
        if "allemagne" in q: return "🌍 **C'est quoi la capitale de l'Allemagne ?** C'est **Berlin**."
        if "italie" in q: return "🌍 **C'est quoi la capitale de l'Italie ?** C'est **Rome**."
        return "🌍 **Capitales :** France=Paris, Suisse=Berne, Allemagne=Berlin, Italie=Rome, Espagne=Madrid, Japon=Tokyo"
    if "moyenne" in q:
        return "📐 **C'est quoi une moyenne ?** On additionne tout et on divise. Ex: (12+15+18)/3 = 15"
    if "aire" in q:
        return "📐 **C'est quoi l'aire ?** C'est la surface. Rectangle = L x l. Carré = c x c. Triangle = (b x h)/2"
    if "perimetre" in q or "périmètre" in q:
        return "📐 **C'est quoi le périmètre ?** C'est le tour. Carré = 4 x côté. Rectangle = 2 x (L+l)"
    if "fraction" in q:
        return "📐 **C'est quoi une fraction ?** C'est une partie d'un tout. Ex: 1/2 c'est la moitié. 1/2 + 1/4 = 3/4"
    if "pourcentage" in q:
        return "📐 **C'est quoi un pourcentage ?** 20% de 50 = 10. On fait 50 x 0.20"
    if "volume" in q:
        return "📐 **C'est quoi un volume ?** Cube = c³. Pavé = L x l x h."
    if "equation" in q:
        return "📐 **C'est quoi une équation ?** 2x + 3 = 7 -> 2x = 4 -> x = 2. On cherche x."
    if "pair" in q:
        return "📐 **C'est quoi pair / impair ?** 8 est pair, 7 est impair. Si /2 tombe juste, c'est pair."
    if "conjuguer" in q or "etre" in q:
        return "🇫🇷 **ÊTRE au présent :** je suis, tu es, il est, nous sommes, vous êtes, ils sont"
    if "avoir" in q:
        return "🇫🇷 **AVOIR au présent :** j'ai, tu as, il a, nous avons, vous avez, ils ont"
    if "pluriel" in q:
        return "🇫🇷 **C'est quoi le pluriel ?** On ajoute s. chat -> chats. Exception : cheval -> chevaux"
    if "verbe" in q:
        return "🇫🇷 **C'est quoi un verbe ?** C'est le mot qui dit l'action. Ex: manger, courir, chanter."
    if "sujet" in q:
        return "🇫🇷 **C'est quoi le sujet ?** C'est qui fait l'action. Ex: *Le chat* mange. Le chat = sujet."
    if "der" in q or "die das" in q or "allemand" in q and "article" in q:
        return "🇩🇪 **C'est quoi der die das ?** der = masculin, die = féminin, das = neutre. der Hund, die Katze, das Haus"
    if "sein" in q:
        return "🇩🇪 **SEIN (être) :** ich bin, du bist, er ist, wir sind, ihr seid, sie sind"
    if "haben" in q:
        return "🇩🇪 **HABEN (avoir) :** ich habe, du hast, er hat, wir haben, ihr habt, sie haben"
    if "to be" in q or "anglais" in q:
        return "🇬🇧 **TO BE :** I am, You are, He is, We are, You are, They are. Ex: I am 13."
    if "guerre" in q:
        return "📜 **C'est quoi la 2ème Guerre Mondiale ?** 1939-1945. La plus grande guerre. La Suisse est restée neutre."
    if "revolution" in q:
        return "📜 **C'est quoi la Révolution française ?** 1789. Prise de la Bastille le 14 juillet 1789."
    if "continent" in q:
        return "🌍 **C'est quoi un continent ?** Europe, Afrique, Asie, Amérique, Océanie, Antarctique. Le plus grand = Asie."
    if "dinosaure" in q:
        return "🦖 **C'est quoi un dinosaure ?** T-Rex = carnivore. Diplodocus = herbivore géant. Disparus il y a 66M d'années."
    if "planete" in q:
        return "🔬 **C'est quoi une planète ?** Mercure, Vénus, Terre, Mars, Jupiter, Saturne, Uranus, Neptune. On vit sur la Terre."
    if "gravite" in q or "gravité" in q:
        return "🔬 **C'est quoi la gravité ?** C'est ce qui nous attire vers la Terre. Newton l'a découverte avec une pomme."
    if "coeur" in q or "corps" in q:
        return "🔬 **C'est quoi le cœur ?** Il pompe le sang dans tout ton corps. Il bat environ 100 000 fois par jour."
    if "bonjour" in q or "prenom" in q:
        return "💻 **Code Bonjour :**\n```python\nprenom = input('Ton prénom ? ')\nprint(f'Bonjour {prenom} !')\n```"
    if "boucle" in q:
        return "💻 **C'est quoi une boucle ?** Ça répète. `for i in range(1,6): print(i)` affiche 1,2,3,4,5"
    if "fonction" in q:
        return "💻 **C'est quoi une fonction ?** `def bonjour(): print('Salut')` C'est une boîte qui fait un travail quand on l'appelle."
    if "variable" in q:
        return "💻 **C'est quoi une variable ?** `age = 13` C'est une boîte qui stocke une info."
    return f"Je ne connais pas encore : **{q}**. Essaie : `C'est quoi le théorème de Pythagore ?`, `C'est quoi la photosynthèse ?`, `C'est quoi un adjectif ?`, `C'est quoi la capitale de la France ?`"
if question := st.chat_input("Pose ta question comme tu parles..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        r = rep(question)
        st.write(r)
    st.session_state.messages.append({"role": "assistant", "content": r})
