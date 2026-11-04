Python
import streamlit as st
import random
st.set_page_config(page_title="Agent Ecole V2 - Toutes Branches", page_icon="🎓", layout="wide")
st.title("🎓 Agent Ecole V2 - Toutes les branches")
st.caption("Sans IA, sans token, juste du code. Il répond à tout.")
# --- MEMOIRE ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Salut ! 👋 Je connais toutes les branches. Écris par exemple : `moyenne`, `conjuguer être`, `table multiplication`, `capitale France`, `photosynthèse`, `code bonjour`..."}
    ]
with st.sidebar:
    st.header("📚 Branches")
    st.write("✅ Maths\n✅ Français\n✅ Allemand\n✅ Anglais\n✅ Histoire\n✅ Géographie\n✅ Sciences\n✅ Informatique")
    if st.button("🗑️ Effacer"):
        st.session_state.messages = []
        st.rerun()
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
def reponse_v2(q):
    q = q.lower()
    # ========== MATHS ==========
    if "moyenne" in q:
        return """**📐 Maths - Moyenne**
```python
notes = [12, 15, 18]
moyenne = sum(notes) / len(notes)
print(moyenne) # = 15.0
n = 7
for i in range(1, 11):
    print(f"{n} x {i} = {n*i}")
    print(10 * 5) # 50
```"""
    if "périmètre" in q or "perimetre" in q:
        return """**📐 Maths - Périmètre**
- Carré : `4 x côté`
- Rectangle : `2 x (longueur + largeur)`
- Cercle : `2 x pi x rayon`"""
    if "pythagore" in q:
        return """**📐 Maths - Pythagore**
Dans un triangle rectangle : `a² + b² = c²`
```python
# Exemple : a=3, b=4 -> c=5
import math
c = math.sqrt(3**2 + 4**2)
print(c) # 5.0
```"""
    if "pair" in q or "impair" in q:
        return """**📐 Maths - Pair / Impair**
```python
n = 7
if n % 2 == 0:
    print("Pair")
else:
    print("Impair")
    capitales = {"France": "Paris", "Suisse": "Berne"}
print(capitales["France"])
```"""
    if "suisse" in q and "canton" in q:
        return """**🌍 Suisse - Cantons**
Il y a 26 cantons. Les plus grands : Zurich, Berne, Vaud, Genève, Fribourg.
Fribourg, ton canton, sa capitale est Fribourg."""
    if "seconde guerre" in q or "guerre" in q:
        return """**📜 Histoire - 2ème Guerre Mondiale**
1939-1945. C'est la guerre la plus meurtrière.
- 1939 : L'Allemagne envahit la Pologne
- 1945 : Fin de la guerre
La Suisse est restée neutre pendant la guerre."""
    # ========== SCIENCES ==========
    if "photosynth" in q:
        return """**🔬 Sciences - Photosynthèse**
La plante fabrique sa nourriture avec :
`Soleil + Eau + CO2 = Oxygène + Sucre`
C'est grâce à ça qu'on peut respirer !"""
    if "eau" in q and "formule" in q:
        return """**🔬 Sciences - Formules**
- Eau : H2O
- Sel : NaCl
- Oxygène : O2
- Dioxyde de carbone : CO2"""
    if "planète" in q or "système solaire" in q:
        return """**🔬 Sciences - Système solaire**
Dans l'ordre : Mercure, Vénus, Terre, Mars, Jupiter, Saturne, Uranus, Neptune.
**Astuce :** Me Voici Tout Mouillé, J'ai Suivi Un Nuage."""
    # ========== INFORMATIQUE / CODE ==========
    if "bonjour" in q or "prenom" in q or "code" in q and "bonjour" in q:
        return """**💻 Code - Demander le prénom**
```python
prenom = input("Ton prénom ? ")
print(f"Bonjour {prenom} !")
for i in range(1, 6):
    print(f"Nombre {i}")
    age = 13
if age >= 18:
    print("Majeur")
else:
    print("Mineur")
    
