import streamlit as st
import requests
import time
st.set_page_config(page_title="Agent Ecole IA", page_icon="🎓", layout="wide")
st.title("🎓 Mon Agent Ecole IA - Version Ultime V2")
st.caption("Il se souvient de ta conversation comme ChatGPT")
# --- CONFIG ---
HF_TOKEN = st.secrets.get("HF_TOKEN", "")
MODEL = "mistralai/Mistral-7B-Instruct-v0.3"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"
# --- MEMOIRE ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Salut ! 👋 Je suis ton agent école. Colle ton exercice, je t'explique et je te donne la réponse avec la méthode."}
    ]
# --- BARRE LATERALE ---
with st.sidebar:
    st.header("⚙️ Réglages")
    matiere = st.selectbox("Matière", ["Maths", "Français", "Allemand", "Histoire", "Sciences", "Autre"])
    st.write(f"Modèle : {MODEL}")
    if st.button("🗑️ Effacer la conversation"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption("Astuce : Recopie avec tes mots pour apprendre !")
# --- AFFICHER LA CONVERSATION ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
# --- FONCTION IA ---
def demander_ia(question):
    if HF_TOKEN == "":
        return "⚠️ Ajoute ton token HF dans Streamlit Secrets : HF_TOKEN = \"hf_...\" Va dans share.streamlit.io -> Manage app -> Secrets"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    prompt = f"[INST] Tu es un prof génial pour un élève de 13 ans en Suisse. Matière : {matiere}. Sois simple, encourageant, donne la réponse étape par étape avec explication. Ne donne jamais juste le résultat sec. Question : {question} [/INST]"
    for essai in range(3):
        try:
            reponse = requests.post(API_URL, headers=headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 600, "temperature": 0.6}}, timeout=60)
            data = reponse.json()
            if isinstance(data, list) and len(data) > 0:
                texte = data[0].get("generated_text", "")
                # On enlève le prompt du texte
                if "[/INST]" in texte:
                    texte = texte.split("[/INST]")[-1]
                return texte.strip()
            elif "loading" in str(data).lower():
                time.sleep(5)
                continue
            else:
                return f"L'IA charge... réessaie dans 20 sec. Info : {data}"
        except Exception as e:
            return f"Erreur : {e}. Vérifie ton token."
    return "L'IA met trop longtemps, réessaie."
# --- ZONE DE SAISIE ---
if question := st.chat_input("Colle ton exercice ici..."):
    # On affiche ta question
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    # L'IA répond
    with st.chat_message("assistant"):
        with st.spinner("Je réfléchis..."):
            reponse = demander_ia(question)
            st.write(reponse)
    st.session_state.messages.append({"role": "assistant", "content": reponse})
