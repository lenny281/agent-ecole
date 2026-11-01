import streamlit as st
st.set_page_config(page_title="Mon Agent Ecole", page_icon="🎓")
st.title("🎓 Mon Agent Ecole - avec reponses")
matiere = st.selectbox("Matiere ?", ["Maths", "Francais", "Allemand", "Histoire", "Sciences"])
exo = st.text_area("Colle ton exercice ici :")
mode = st.radio("Tu veux quoi ?", ["Expliquer la methode", "Donner la reponse + explication"])
if st.button("Go !"):
    if exo.strip() == "":
        st.warning("Colle ton exo d'abord !")
    else:
        st.divider()
        st.write(f"**Exo :** {exo}")
        st.write(f"**Matiere :** {matiere}")
        if mode == "Expliquer la methode":
            st.info("""
            **Etape 1 :** Quelle est la question exacte ?
            **Etape 2 :** Quelle regle du cours on utilise ?
            **Etape 3 :** Essaie et je corrige.
            """)
        else:
            st.success("Voici la reponse avec l'explication :")
            st.write("""
            **1. On comprend la question**
            On lit bien ce qui est demande.
            **2. On applique la regle du cours**
            On utilise la formule ou la regle vue en classe.
            **3. On calcule / On redige**
            On fait le calcul etape par etape.
            *Astuce : Recopie l'explication avec tes mots, pas juste la reponse.*
            """)
            st.write(f"**Pour ton exo : {exo}**")
            st.write("Si tu me dis un exemple precis, je te fais le calcul exact ici.")
