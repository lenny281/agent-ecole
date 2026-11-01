import streamlit as st
st.set_page_config(page_title="Mon Agent École", page_icon="🎓")
st.title("🎓 Mon Agent École - qui donne les réponses")
matiere = st.selectbox("Matière ?", ["Maths", "Français", "Allemand", "Histoire", "Sciences"])
exo = st.text_area("Colle ton exercice :")
mode = st.radio("Tu veux quoi ?", ["Juste m'expliquer la méthode", "Donner la réponse + explication"])
if st.button("Go !"):
    if exo.strip() == "":
        st.warning("Colle ton exo d'abord")
    else:
        st.divider()
        if mode == "Juste m'expliquer la méthode":
            st.info(f"""
            **Exo :** {exo}
            **1. Ce qu'on cherche :** Relis la consigne
            **2. Règle à utiliser :** Cherche dans ton cours {matiere}
            **3. Essaie toi-même d'abord, je corrige après**
            """)
        else:
            # ICI c'est là où ton agent donnera la vraie réponse
            # Pour l'instant version simple, après on branche une vraie IA
            st.success("Voici comment on le résout :")
            if matiere == "Maths":
                st.write(f"""
                **Exercice :** {exo}
                **Réponse de l'agent :**
                Pour résoudre ça, on fait étape par étape :
                1. On identifie les nombres
                2. On applique la formule
                3. On calcule
                *Exemple : si c'est 2x + 3 = 7, on fait 2x = 4 donc x = 2*
                Colle ton vrai exo de maths et je te fais le calcul exact.
                """)
            else:
                st.write(f"""
                **Exercice :** {exo}
                **Réponse de ton agent :**
                Je vais te donner la réponse, mais avec l'explication pour que tu comprennes.
                Pour avoir la VRAIE réponse automatique avec une IA, il faut brancher un cerveau.
                """)
            st.warning("💡 Astuce : Copie pas bêtement. Recopie l'explication avec tes mots, le prof voit direct si c'est du copié-collé d'IA.")
# Pour avoir les VRAIES réponses automatiques (niveau 3)
st.divider()
st.caption("Niveau 3 : Pour que ça réponde tout seul avec une IA, il faut ajouter un cerveau comme Ollama ou Hugging Face. Tu veux que je te montre ?"
           
