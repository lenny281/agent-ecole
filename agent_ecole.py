import streamlit as st
st.set_page_config(page_title="Mon Agent École", page_icon="🎓", layout="centered")
st.title("🎓 Mon Agent École - H24")
st.caption("Il marche même quand ton PC est éteint !")
# Mémoire de l'agent
if "historique" not in st.session_state:
    st.session_state.historique = []
matiere = st.selectbox("📚 Matière ?", ["Maths", "Français", "Allemand", "Histoire", "Sciences", "Autre"])
exo = st.text_area("📝 Colle ton exercice ici :", height=150)
col1, col2 = st.columns(2)
with col1:
    btn_aide = st.button("🚀 Aide-moi !", use_container_width=True)
with col2:
    btn_effacer = st.button("🗑️ Effacer", use_container_width=True)
if btn_effacer:
    st.session_state.historique = []
    st.rerun()
if btn_aide:
    if exo.strip() == "":
        st.warning("Colle d'abord ton exercice !")
    else:
        # On garde en mémoire
        st.session_state.historique.append({"matiere": matiere, "exo": exo})
        st.success(f"C'est parti pour les {matiere} !")
        st.markdown(f"""
        ### Exercice reçu :
        > {exo}
        ### 🧠 Méthode de ton agent :
        **1. Je comprends la question :**
        Qu'est-ce qu'on te demande exactement ? Entoure le verbe de la consigne (calculer, expliquer, conjuguer...)
        **2. Je cherche dans le cours :**
        Quelle règle / formule de ton cours correspond ? (ex: en maths : Pythagore, en allemand : Akkusativ...)
        **3. Je te guide :**
        Essaie de faire l'étape 1 tout seul et écris-moi ce que tu trouves. Je te dis si c'est juste et on passe à la suite.
        ---
        *Astuce : Ne copie pas la réponse, apprends la méthode. C'est comme ça que tu auras 6 à l'exam.*
        """)
# Affiche l'historique
if st.session_state.historique:
    st.divider()
    st.subheader(f"📜 Tu as déjà fait {len(st.session_state.historique)} exos avec moi")
    for i, h in enumerate(reversed(st.session_state.historique[-3:]), 1):
        st.text(f"{i}. [{h['matiere']}] {h['exo'][:60]}...")