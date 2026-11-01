import streamlit as st
st.set_page_config(page_title="Mon Agent Ecole", page_icon="🎓")
st.title("🎓 Mon Agent Ecole")
st.write("Colle ton exo, je t'aide.")
matiere = st.selectbox("Matiere ?", ["Maths", "Francais", "Allemand", "Histoire", "Sciences"])
exo = st.text_area("Colle ton exercice ici :")
if st.button("Aide-moi !"):
    if exo.strip() == "":
        st.warning("Colle ton exo d'abord !")
    else:
        st.success(f"On le fait en {matiere} !")
        st.write(f"**Ton exo :** {exo}")
        st.write("**Etape 1 :** C'est quoi la question exacte ?")
        st.write("**Etape 2 :** Quelle regle du cours on utilise ?")
        st.write("Dis-moi et je te guide pour la suite.")
           
