import streamlit as st
st.set_page_config(page_title="Agent Ecole V2 Noir", page_icon="🖤", layout="wide")
# --- STYLE NOIR ---
st.markdown("""
<style>
.stApp { background-color: #000000; color: white; }
[data-testid="stSidebar"] { background-color: #111111; }
[data-testid="stSidebar"] * { color: white !important; }
.stChatMessage { background-color: #1a1a1a !important; color: white !important; border: 1px solid #333333; }
input { background-color: #222222 !important; color: white !important; }
h1, h2, h3, p { color: white !important; }
</style>
""", unsafe_allow_html=True)
with st.sidebar:
    st.title("🖤 Agent Ecole V2")
    st.write("**Mode Noir**")
    st.write("✅ Maths")
    st.write("✅ Français")
    st.write("✅ Allemand")
    st.write("✅ Anglais")
    st.write("✅ Histoire / Géo")
    st.write("✅ Sciences")
    st.write("✅ Code")
    st.divider()
    st.caption("Sans IA, juste du code.")
    if st.button("🗑️ Effacer"):
        st.session_state.messages = []
        st.rerun()
st.title("🖤 Mon Agent Ecole - Mode Noir")
st.caption("Pose ta question en bas")
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Salut ! 👋 Mode noir activé. Essaie : moyenne, capitale, conjuguer, photosynthese, bonjour..."}
    ]
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
def trouver_reponse(q):
    q = q.lower()
    if "moyenne" in q:
        return "📐 **Moyenne** = (12+15+18) / 3 = 15"
    if "table" in q or "multiplication" in q:
        return "📐 **Table de 7 :** 7, 14, 21, 28, 35, 42, 49, 56, 63, 70"
    if "aire" in q:
        return "📐 **Aire :** Rectangle = longueur x largeur. Triangle = (base x hauteur) / 2"
    if "pythagore" in q:
        return "📐 **Pythagore :** a² + b² = c². Exemple : 3-4-5"
    if "pair" in q:
        return "📐 **Pair :** 8 est pair, 7 est impair."
    if "conjuguer" in q or "etre" in q:
        return "🇫🇷 **ÊTRE :** je suis, tu es, il est, nous sommes, vous êtes, ils sont"
    if "avoir" in q:
        return "🇫🇷 **AVOIR :** j'ai, tu as, il a, nous avons, vous avez, ils ont"
    if "pluriel" in q:
        return "🇫🇷 **Pluriel :** un chat -> des chats. cheval -> chevaux"
    if "allemand" in q or "der" in q:
        return "🇩🇪 **Allemand :** der = masculin, die = féminin, das = neutre"
    if "anglais" in q or "to be" in q:
        return "🇬🇧 **TO BE :** I am, You are, He is, We are, You are, They are"
    if "capitale" in q:
        return "🌍 **Capitales :** France=Paris, Suisse=Berne, Allemagne=Berlin, Italie=Rome"
    if "canton" in q:
        return "🌍 **Suisse :** 26 cantons. Zurich, Berne, Vaud, Genève, Fribourg."
    if "guerre" in q:
        return "📜 **2ème Guerre :** 1939-1945. La Suisse est restée neutre."
    if "photosynthese" in q:
        return "🔬 **Photosynthèse :** Soleil + Eau + CO2 = Oxygène + Sucre"
    if "planete" in q:
        return "🔬 **Planètes :** Mercure, Vénus, Terre, Mars, Jupiter, Saturne, Uranus, Neptune"
    if "bonjour" in q or "prenom" in q:
        return "💻 **Code :** prenom = input('Ton prénom ?') puis print(f'Bonjour {prenom} !')"
    if "boucle" in q:
        return "💻 **Boucle :** for i in range(1,6): print(i)"
    if "condition" in q:
        return "💻 **Condition :** if age >= 18: print('Majeur') else: print('Mineur')"
    return "Je ne connais pas ce mot. Essaie : moyenne, table, aire, pythagore, conjuguer, avoir, pluriel, allemand, anglais, capitale, canton, guerre, photosynthese, planete, bonjour, boucle"
if question := st.chat_input("Pose ta question..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        rep = trouver_reponse(question)
        st.write(rep)
    st.session_state.messages.append({"role": "assistant", "content": rep})
