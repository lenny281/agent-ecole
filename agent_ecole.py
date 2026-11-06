import streamlit as st
import random
import datetime
import re
import json
import os
import difflib

st.set_page_config(page_title="Agent IA V8 - PERFECTIONNE", page_icon="🤖", layout="wide")
st.markdown("""<style>.stApp{background-color:#0a0a0a;color:#e5e5e5}[data-testid="stSidebar"]{background-color:#111}[data-testid="stSidebar"] *{color:#e5e5e5!important}.stChatMessage{background-color:#161616!important;color:#e5e5e5!important;border:1px solid #2a2a2a;border-radius:12px}h1{color:#f0f0f0!important}button{background-color:#1e1e1e!important;color:#e5e5e5!important;border:1px solid #2e2e2e!important;border-radius:10px!important}</style>""", unsafe_allow_html=True)

# ============ PERF 1 : FICHIER learned.json ============
FICHIER = "learned.json"
def charger():
    if os.path.exists(FICHIER):
        try:
            with open(FICHIER, "r", encoding="utf-8") as f: return json.load(f)
        except: return {}
    return {}
def sauver(d):
    try:
        with open(FICHIER, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=2)
    except: pass

# ============ PERF 2 : TOUT EN JSON ============
JSON_Q = """{"facile": [["C est quoi 2+2 ?", "4"], ["C est quoi 5x2 ?", "10"], ["C est quoi la capitale de la France ?", "paris"], ["C est quoi 3x3 ?", "9"], ["C est quoi 10-3 ?", "7"], ["C est quoi 4+4 ?", "8"], ["C est quoi la capitale de la Suisse ?", "berne"], ["Conjugue ETRE : je ... ?", "suis"], ["C est quoi 6x6 ?", "36"], ["C est quoi 20-5 ?", "15"]], "moyen": [["C est quoi 7x8 ?", "56"], ["C est quoi la capitale du Japon ?", "tokyo"], ["C est quoi 15+25 ?", "40"], ["Qui a gagne la Coupe du Monde 2022 ?", "argentine"], ["C est quoi 9x9 ?", "81"], ["C est quoi 12x3 ?", "36"], ["C est quoi 100 / 4 ?", "25"], ["C est quoi PI ?", "3.14"]], "difficile": [["C est quoi 12x12 ?", "144"], ["C est quoi la capitale de l Australie ?", "canberra"], ["C est quoi 144 / 12 ?", "12"], ["Combien de Ballons d Or a 【entity-Messi¦canonical_name=Messi】 ?", "8"], ["En quelle annee a coule le Titanic ?", "1912"], ["C est quoi 17x6 ?", "102"]], "verbes": [["Conjugue ETRE : je ... ?", "suis"], ["Conjugue AVOIR : tu ... ?", "as"], ["Conjugue TO BE : I ... ?", "am"], ["Conjugue SEIN : ich ... ?", "bin"], ["Conjugue ALLER : il ... ?", "va"]], "maths": [["C est quoi 7x8 ?", "56"], ["C est quoi 9x9 ?", "81"], ["C est quoi 12+15 ?", "27"], ["C est quoi PI ?", "3.14"], ["C est quoi 100-37 ?", "63"]], "francais": [["C est quoi le COD ?", "cod"], ["Conjugue ETRE : je ... ?", "suis"], ["C est quoi le pluriel de cheval ?", "chevaux"]], "capitales": [["C est quoi la capitale du Japon ?", "tokyo"], ["C est quoi la capitale de la France ?", "paris"], ["C est quoi la capitale de la Suisse ?", "berne"], ["C est quoi la capitale du Bresil ?", "brasilia"]], "10h": [["C est quoi une fonction affine ?", "affine"], ["C est quoi Pythagore ?", "a2"], ["C est quoi le COD ?", "cod"], ["C est quoi PI ?", "3.14"], ["C est quoi le pacte de 1291 ?", "1291"]]}"""
TRAIN = json.loads(JSON_Q)

# ============ PERF 3 : cache_data = charge 1 fois, pas a chaque clic ============
@st.cache_data
def get_tout():
    return {"pi":"PI = 3.14 ! Perimetre = 2 x PI x rayon. Aire = PI x rayon x rayon. Ex : Rayon 5 : Perimetre = 31.4 cm, Aire = 78.5 cm2. Rayon 10 : Perimetre = 62.8, Aire = 314. Le 14 mars = journee de PI !","pythagore":"PYTHAGORE 10H : a2 + b2 = c2. Ex : 3-4-5 car 9+16=25. Si a=6, b=8, c=10.","thales":"THALES 10H : AB / AD = AC / AE = BC / DE.","aire":"AIRE 10H : Rectangle = L x l, Carre = cote x cote, Triangle = (base x hauteur) / 2, Cercle = PI x rayon2.","perimetre":"PERIMETRE 10H : Carre = 4 x cote, Rectangle = 2 x (L+l), Cercle = 2 x PI x rayon. PI = 3.14.","volume":"VOLUME 10H : Cube = cote3, Pave = L x l x h, Cylindre = PI x r2 x h.","cod":"COD 10H : Complement d Objet Direct. Repond a Qui ? ou Quoi ? Ex : Je mange une pomme. Une pomme = COD.","coi":"COI 10H : Repond a A qui ? A quoi ? Ex : Je parle a Lenny. A Lenny = COI.","sujet":"SUJET 10H : Qui fait l action. Ex : Lenny mange. Lenny = sujet.","photosynthese":"PHOTOSYNTHESE 10H : Soleil + Eau + CO2 = Oxygene + Sucre.","coeur":"COEUR 10H : Pompe le sang dans tout le corps.","gravite":"GRAVITE 10H : Nous attire vers la Terre. Decouverte par Newton avec une pomme.","atome":"ATOME 10H : Noyau (protons + neutrons) + electrons qui tournent.","ph":"PH 10H : 0-6 = acide (citron = 2), 7 = neutre (eau), 8-14 = basique (savon = 10).","loi ohm":"LOI OHM 10H : U = R x I. Ex : R=10, I=2, U=20V.","salaire":"SALAIRE 10H : En Suisse, median environ 6500 CHF brut.","tva":"TVA 10H : Suisse : 8.1% general, 2.6% nourriture, 3.8% hotel. Sur 100 CHF, environ 8 CHF vont a l Etat.","democratie":"DEMOCRATIE 10H : Le peuple decide. Suisse = democratie directe (votations).","foot":"FOOT 10H : 2 equipes de 11, 90 minutes. Sport le plus joue au monde.","【entity-messi¦canonical_name=Messi】":"【entity-MESSI¦canonical_name=Messi】 : 8 Ballons d Or (record), Coupe du Monde 2022.","【entity-ronaldo¦canonical_name=RONALDO】":"【entity-RONALDO¦canonical_name=RONALDO】 : 5 Ballons d Or, meilleur buteur de l histoire.","【entity-minecraft¦canonical_name=MINECRAFT】":"【entity-MINECRAFT¦canonical_name=MINECRAFT】 : Jeu le plus vendu au monde. Monde en cubes, Creeper, Ender Dragon.","fortnite":"FORTNITE : Battle Royale : 100 joueurs, le dernier gagne.","trou noir":"TROU NOIR 10H : Tellement lourd que meme la lumiere ne peut pas en sortir.","werenoi":"WERENOI : 【entity-Jeremy Bana Owona¦canonical_name=Jeremy Bana Owona】. Albums : Pyramide, Diamant Noir.","【entity-ninho¦canonical_name=NINHO】":"【entity-NINHO¦canonical_name=NINHO】 : 【entity-William Nzobazola¦canonical_name=William Nzobazola】. Le plus de disques d or en France !","millionnaire":"COMMENT DEVENIR MILLIONNAIRE ? 1. Salarie + investissement. 2. Entrepreneur. 3. Createur. Apprends une competence, epargne, investis tot.","fonction affine":"FONCTION AFFINE 10H : f(x) = a x + b. a = pente, b = ordonnee a l origine. Ex : f(x) = 2x + 1.","moyenne":"MOYENNE 10H : somme / nombre. Ex : 12, 15, 18 -> Moyenne = 15.","fraction":"FRACTION 10H : 1/2 = moitie, 1/4 = quart. 1/2 + 1/4 = 3/4.","pourcentage":"POURCENTAGE 10H : (partie / total) x 100. Ex : 20% de 50 = 10.","equation":"EQUATION 10H : 2x + 3 = 7 -> 2x = 4 -> x = 2.","passe compose":"PASSE COMPOSE 10H : ETRE ou AVOIR + participe passe. Ex : J ai mange, Je suis alle.","imparfait":"IMPARFAIT 10H : Action longue dans le passe. Ex : Quand j etais petit, je jouais au foot.","suisse":"SUISSE 10H : 26 cantons, 4 langues, Capitale Berne, 8.9 millions, CHF, Neutralite depuis 1515.","pacte de 1291":"PACTE DE 1291 : 1er aout 1291, Uri, Schwyz, Unterwald signent. Naissance de la Suisse.","foudre":"FOUDRE 10H : Tres chaud, plus chaud que le Soleil ! Si tu entends le tonnerre, rentre.","systeme solaire":"SYSTEME SOLAIRE : 8 planetes : Mercure, Venus, Terre, Mars, Jupiter, Saturne, Uranus, Neptune.","big bang":"BIG BANG : Debut de l univers il y a 13.8 milliards d annees.","electricite":"ELECTRICITE : Tension (V), Intensite (A), Puissance (W). P = U x I.","vitesse":"VITESSE : v = d / t. Ex : 100m en 10 sec = 10 m/s = 36 km/h.","adn":"ADN : Ton code genetique. 50% pere, 50% mere.","python":"PYTHON : Langage facile, celui de ton agent. Pour l IA, les sites, les jeux.","ia":"IA : Programme qui apprend avec des donnees. Ex : ChatGPT, ton agent.","internet":"INTERNET : Reseau mondial d ordinateurs relies.","budget":"BUDGET : Regle 50/30/20 : 50 besoins, 30 envies, 20 epargne.","bourse":"BOURSE : Acheter une partie d une entreprise. ETF = panier de 500 entreprises, moins risque."}
@st.cache_data
def get_capitales():
    return {"france":"Paris - Tour Eiffel","suisse":"Berne - Capitale depuis 1848","japon":"Tokyo - Plus grande ville","bresil":"Brasilia - Rio plus connue","allemagne":"Berlin - Mur tombe 1989","italie":"Rome - Colisee","espagne":"Madrid - 【entity-Real Madrid¦canonical_name=Real Madrid】","angleterre":"Londres - Big Ben","usa":"Washington - Maison Blanche","canada":"Ottawa - Toronto plus grande","chine":"Pekin - Grande Muraille","australie":"Canberra - Sydney plus connue","egypte":"Le Caire - Pyramides","maroc":"Rabat","portugal":"Lisbonne - 【entity-Ronaldo¦canonical_name=RONALDO】","belgique":"Bruxelles - Frites","grece":"Athenes - JO","mexique":"Mexico - Tacos","argentine":"Buenos Aires - 【entity-Messi¦canonical_name=Messi】","inde":"New Delhi - Taj Mahal","russie":"Moscou - Place Rouge","qatar":"Doha - Mondial 2022","nepal":"Katmandou - Everest"}
@st.cache_data
def get_all_questions():
    base = list(get_tout().keys()) + list(get_capitales().keys())
    for v in TRAIN.values():
        for q,a in v: base.append(q)
    base += ["Conjugue ETRE","Conjugue AVOIR","Conjugue SEIN","Conjugue TO BE","C est quoi le COD ?","C est quoi PI ?"]
    return base

TOUT = get_tout(); CAPITALES = get_capitales(); ALL_Q = get_all_questions()
VERBES = {"etre":"ETRE : je suis, tu es, il est, nous sommes, vous etes, ils sont. Passe : j ai ete. Futur : je serai.","avoir":"AVOIR : j ai, tu as, il a, nous avons, vous avez, ils ont. Passe : j ai eu. Futur : j aurai.","aller":"ALLER : je vais, tu vas, il va, nous allons, vous allez, ils vont. Passe : je suis alle. Futur : j irai.","sein":"SEIN = ETRE en Allemand. ich bin, du bist, er ist, wir sind, ihr seid, sie sind.","to be":"TO BE = ETRE en Anglais. I am, You are, He is, We are, You are, They are."}
BASES = {"bonjour":"Bonjour ! V8 PERFECTIONNEE ! Tape dans la recherche en haut !","salut":"Salut ! Ca va ?","merci":"De rien !","ca va":"Ca va super ! Et toi ?","au revoir":"Au revoir ! A tres vite !"}

# ============ SESSION ============
if "learned" not in st.session_state: st.session_state.learned = charger()
if "messages" not in st.session_state: st.session_state.messages = [{"role":"assistant","content":"Salut ! V8 PERFECTIONNEE AU MAX ! Recherche instantanee + 0 lag + Entrainement parfait ! Essaie : pi"}]
for k,v in [("score",0),("total_quiz",0),("streak",0),("best_streak",0),("train_q",None),("train_a",None),("mode_train",False),("niveau","moyen"),("auto_q",""),("cookies",0),("click_power",1),("nombre_secret",random.randint(1,100)),("coups",0),("xp",0),("theme","📐 Ecole")]:
    if k not in st.session_state: st.session_state[k]=v

def nettoyer(txt):
    txt=txt.lower().strip(); txt=txt.replace("é","e").replace("è","e").replace("ê","e").replace("à","a").replace("ç","c").replace("ô","o").replace("î","i")
    txt=re.sub(r"[^a-z0-9 +*/\-=?.]", " ", txt); txt=re.sub(r"\s+"," ",txt).strip(); return txt

# ============ PERF 4 : on_click, ZERO rerun en boucle ============
def ajouter_cookie(): st.session_state.cookies += st.session_state.click_power; st.session_state.xp += 1
def acheter_click():
    if st.session_state.cookies >= 50: st.session_state.cookies -= 50; st.session_state.click_power += 1
def lancer(niveau):
    st.session_state.mode_train=True; st.session_state.niveau=niveau
    nq,na = random.choice(TRAIN[niveau]); st.session_state.train_q=nq; st.session_state.train_a=na
    st.session_state.messages.append({"role":"assistant","content":"C EST PARTI - "+niveau.upper()+" ! Question : "+nq})
def quitter():
    st.session_state.mode_train=False; st.session_state.train_q=None
    st.session_state.messages.append({"role":"assistant","content":"Entrainement termine ! Score : "+str(st.session_state.score)+"/"+str(st.session_state.total_quiz)+" | XP : "+str(st.session_state.xp)})

# ============ TITRE + STATS ============
st.title("Agent IA V8 - PERFECTIONNE AU MAX 🤖")
st.caption(f"XP : {st.session_state.xp} | Score : {st.session_state.score}/{st.session_state.total_quiz} | Streak : {st.session_state.streak} 🔥 | Best : {st.session_state.best_streak} | Appris : {len(st.session_state.learned)} (sauvegarde auto) | Cookies : {st.session_state.cookies} 🍪")

# ============ PERF 5 : RECHERCHE INSTANTANEE + SUGGESTIONS ============
recherche = st.text_input("🔍 RECHERCHE INSTANTANEE - Tape 2 lettres, je trouve tout seul ! Ex : pi, cod, japon, messi...", key="recherche_v8")
if recherche:
    qn = nettoyer(recherche)
    res = []
    for cle, rep in TOUT.items():
        if qn in nettoyer(cle): res.append((cle, rep))
    for pays, cap in CAPITALES.items():
        if qn in pays: res.append((f"Capitale de {pays}", cap))
    if res:
        st.success(f"✅ {len(res)} resultat(s) pour : {recherche}")
        for titre, rep in res[:4]:
            if st.button(f"👉 {titre}", key="rch_"+titre, use_container_width=True):
                st.session_state.messages.append({"role":"user","content":titre}); st.session_state.auto_q = titre
    else:
        proches = difflib.get_close_matches(recherche, ALL_Q, n=5, cutoff=0.35)
        if proches:
            st.info("Tu voulais dire ? Clique :")
            for p in proches:
                if st.button(f"💡 {p}", key="sugg_"+p, use_container_width=True):
                    st.session_state.messages.append({"role":"user","content":p}); st.session_state.auto_q = p
        else:
            st.warning(f"Rien pour : {recherche}. Essaie : pi, cod, japon...")

# ============ SIDEBAR ============
with st.sidebar:
    st.title("Agent V8 PERFECTIONNE")
    st.write(f"XP : {st.session_state.xp} | Score : {st.session_state.score}/{st.session_state.total_quiz}")
    st.write(f"🔥 Streak : {st.session_state.streak} | Best : {st.session_state.best_streak}")
    st.divider()
    if st.button("🎮 JEUX", use_container_width=True): st.session_state.theme = "🎮 Jeux"
    if st.button("📐 ECOLE", use_container_width=True): st.session_state.theme = "📐 Ecole"
    st.divider()
    st.write("ENTRAINEMENT (JSON) :")
    for niv in ["facile","moyen","difficile","verbes","maths","francais","capitales","10h"]:
        if st.button(niv.upper(), key="t_"+niv, use_container_width=True): lancer(niv)
    if st.session_state.mode_train:
        st.success(f"EN TRAIN : {st.session_state.train_q}")
        st.button("❌ QUITTER", on_click=quitter, use_container_width=True)

# ============ ENTRAINEMENT ============
if not st.session_state.mode_train:
    st.subheader("🎯 MODE ENTRAINEMENT - 1 clic = c est parti !")
    c1,c2,c3,c4 = st.columns(4)
    with c1:
        if st.button("🟢 FACILE", use_container_width=True): lancer("facile")
    with c2:
        if st.button("🟡 MOYEN", use_container_width=True): lancer("moyen")
    with c3:
        if st.button("🔴 DIFFICILE", use_container_width=True): lancer("difficile")
    with c4:
        if st.button("🌍 CAPITALES", use_container_width=True): lancer("capitales")
else:
    st.success(f"🎯 ENTRAINEMENT {st.session_state.niveau.upper()} - Score : {st.session_state.score}/{st.session_state.total_quiz} | XP : {st.session_state.xp}")
    st.info(f"❓ QUESTION : {st.session_state.train_q}")
    st.button("❌ QUITTER ENTRAINEMENT", on_click=quitter, use_container_width=True)

# ============ JEUX ============
if st.session_state.theme == "🎮 Jeux":
    st.subheader("🎮 JEUX - Sans lag !")
    jeu = st.selectbox("Choisis :", ["Jeu Clicker","Jeu Devine le nombre","Jeu Pierre Papier Ciseaux"])
    if jeu == "Jeu Clicker":
        st.write(f"🍪 Cookies : {st.session_state.cookies} | Puissance : +{st.session_state.click_power}")
        st.button("🍪 CLIQUER !", on_click=ajouter_cookie, use_container_width=True)
        st.button("Acheter +1 - 50 cookies", on_click=acheter_click, use_container_width=True)
        st.progress(min(st.session_state.cookies/1000, 1.0)); st.write("Prochain niveau a 1000 cookies !")
    if jeu == "Jeu Devine le nombre":
        st.write(f"Je pense a un nombre entre 1 et 100. Coups : {st.session_state.coups}")
        guess = st.number_input("Ton nombre :", min_value=1, max_value=100, value=50)
        if st.button("DEVINER !", use_container_width=True):
            st.session_state.coups += 1
            if guess < st.session_state.nombre_secret: st.warning("C est PLUS grand !")
            elif guess > st.session_state.nombre_secret: st.warning("C est PLUS petit !")
            else: st.success(f"BRAVO en {st.session_state.coups} coups ! +10 XP"); st.session_state.xp += 10; st.session_state.nombre_secret = random.randint(1,100); st.session_state.coups = 0
    if jeu == "Jeu Pierre Papier Ciseaux":
        c1,c2,c3 = st.columns(3); ordi = random.choice(["Pierre","Papier","Ciseaux"])
        with c1:
            if st.button("🪨 Pierre", use_container_width=True): st.session_state.dernier = ("Pierre", ordi)
        with c2:
            if st.button("📄 Papier", use_container_width=True): st.session_state.dernier = ("Papier", ordi)
        with c3:
            if st.button("✂️ Ciseaux", use_container_width=True): st.session_state.dernier = ("Ciseaux", ordi)
        if "dernier" in st.session_state:
            toi, o = st.session_state.dernier; st.write(f"Toi : {toi} | Ordi : {o}")
            if toi == o: st.info("EGALITE !")
            elif (toi=="Pierre" and o=="Ciseaux") or (toi=="Papier" and o=="Pierre") or (toi=="Ciseaux" and o=="Papier"): st.success("TU GAGNES ! +5 XP"); st.session_state.xp += 5
            else: st.error("TU PERDS... Rejoue !")

# ============ MESSAGES ============
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.write(msg["content"])

def trouver(q_orig):
    q_low = nettoyer(q_orig)
    # --- ENTRAINEMENT : == EXACT ---
    if st.session_state.mode_train and st.session_state.train_q is not None:
        bonne = nettoyer(st.session_state.train_a)
        rep_net = q_low
        for mot in ["c est","la reponse c est","reponse","je pense que c est","c"]: rep_net = rep_net.replace(mot, " ")
        rep_net = " ".join(rep_net.split())
        st.session_state.total_quiz += 1
        if rep_net == bonne:  # ✅ ==, pas "in" ! "par" != "paris"
            st.session_state.score += 1; st.session_state.streak += 1; st.session_state.xp += 10
            if st.session_state.streak > st.session_state.best_streak: st.session_state.best_streak = st.session_state.streak
            rep = f"BRAVO ! C etait bien {st.session_state.train_a} ! Score : {st.session_state.score}/{st.session_state.total_quiz} | Streak : {st.session_state.streak} 🔥 | +10 XP !"
        else:
            st.session_state.streak = 0
            rep = f"Pas tout a fait... Tu as ecrit : {q_orig}. La bonne reponse c etait : {st.session_state.train_a}. (Avant 'par' etait accepte pour 'paris', maintenant il faut ecrire en entier !) Score : {st.session_state.score}/{st.session_state.total_quiz}"
        nq, na = random.choice(TRAIN[st.session_state.niveau]); st.session_state.train_q = nq; st.session_state.train_a = na
        return rep + f"\n\nQuestion suivante : {nq}\n\nEcris stop pour quitter."
    if q_low in ["stop","quitter","exit"]:
        if st.session_state.mode_train: quitter(); return "Entrainement termine !"
        return "Tu n es pas en entrainement."
    if "mon score" in q_low or q_low == "score": return f"Score : {st.session_state.score}/{st.session_state.total_quiz} | Streak : {st.session_state.streak} | Best : {st.session_state.best_streak} | XP : {st.session_state.xp}"
    if q_orig.lower().strip().startswith("apprends"):
        try:
            texte = q_orig.lower().replace("apprends :","").replace("apprends","").strip()
            if "=" in texte:
                cle, val = texte.split("=",1); cle = nettoyer(cle); val = val.strip()
                st.session_state.learned[cle] = val; sauver(st.session_state.learned)
                return f"MERCI ! J ai appris ET sauvegarde dans learned.json ! {cle} = {val} ! J ai appris {len(st.session_state.learned)} choses, ca reste meme apres refresh ! +5 XP"
        except: return "Ecris : Apprends : question = reponse"
    if "montre ce que tu as appris" in q_low:
        if not st.session_state.learned: return "Rien appris... Apprends-moi : Apprends : question = reponse"
        txt = f"CE QUE TU M AS APPRIS ({len(st.session_state.learned)}) - sauvegarde dans learned.json :\n\n"
        for k,v in st.session_state.learned.items(): txt += f"- {k} = {v}\n"
        return txt
    for cle,val in st.session_state.learned.items():
        if cle == q_low: return f"Ce que TU m as appris : {val}"
    if any(c in q_orig for c in ["+","x","*","/","-"]) and any(c.isdigit() for c in q_orig):
        try:
            txt = q_orig.lower().replace("calcule","").replace("=","").replace("?","").strip().replace("x","*").replace(",",".")
            if all(c in "0123456789+-*/(). " for c in txt): return f"Calcul : {q_orig} = {eval(txt)} ! Bravo !"
        except: pass
    for cle,rep in BASES.items():
        if nettoyer(cle) in q_low: return rep
    if "capitale" in q_low:
        for pays,cap in CAPITALES.items():
            if pays in q_low: return f"Capitale de {pays.capitalize()} = {cap}"
    for cle,rep in VERBES.items():
        if nettoyer(cle) == q_low or nettoyer(cle) in q_low: return rep
    for mot,rep in TOUT.items():
        if nettoyer(mot) in q_low: return rep
    proches = difflib.get_close_matches(q_low, list(TOUT.keys()) + list(CAPITALES.keys()), n=1, cutoff=0.6)
    if proches: return f"Tu voulais dire : {proches[0]} ? Tape-le dans la recherche en haut !"
    return f"Hmm je ne connais pas : {q_orig}. Apprends-moi : Apprends : {q_orig} = ta reponse. Ou tape dans la recherche en haut !"

if st.session_state.auto_q:
    qa = st.session_state.auto_q; st.session_state.auto_q = ""
    ra = trouver(qa); st.session_state.messages.append({"role":"assistant","content":ra})
    with st.chat_message("assistant"): st.write(ra)
if question := st.chat_input("Pose ta question ici, ou reponds a l entrainement !"):
    st.session_state.messages.append({"role":"user","content":question})
    with st.chat_message("user"): st.write(question)
    with st.chat_message("assistant"):
        r = trouver(question); st.write(r)
    st.session_state.messages.append({"role":"assistant","content":r}); st.session_state.xp += 1
