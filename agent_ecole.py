import streamlit as st
st.set_page_config(page_title="Agent Ecole V2", page_icon="🎓")
st.title("🎓 Agent Ecole V2 - Toutes Branches")
st.write("Ecris un mot et je te donne la reponse.")
question = st.text_input("Ta question :")
bouton = st.button("Donner la reponse !")
if bouton:
    q = question.lower()
    reponse = ""
    # MATHS
    if "moyenne" in q:
        reponse = "Moyenne = (note1 + note2 + note3) / 3. Exemple : (12+15+18)/3 = 15"
    elif "table" in q or "multiplication" in q:
        reponse = "Table de 7 : 7x1=7, 7x2=14, 7x3=21, 7x4=28, 7x5=35, 7x6=42, 7x7=49, 7x8=56, 7x9=63, 7x10=70"
    elif "aire" in q:
        reponse = "Aire rectangle = longueur x largeur. Aire carre = cote x cote. Aire triangle = (base x hauteur) / 2"
    elif "pythagore" in q:
        reponse = "Pythagore : a2 + b2 = c2. Exemple : 3-4-5 car 9+16=25"
    elif "pair" in q:
        reponse = "Pair = reste 0 quand on divise par 2. Exemple : 8 est pair, 7 est impair."
    # FRANCAIS
    elif "conjuguer" in q or "etre" in q:
        reponse = "ETRE present : je suis, tu es, il est, nous sommes, vous etes, ils sont"
    elif "avoir" in q:
        reponse = "AVOIR present : j'ai, tu as, il a, nous avons, vous avez, ils ont"
    elif "pluriel" in q:
        reponse = "Pluriel : on ajoute s. Exemple : un chat -> des chats. Exception : cheval -> chevaux"
    elif "adjectif" in q:
        reponse = "Adjectif s'accorde : grand garcon / grande fille / grands garcons"
    # ALLEMAND
    elif "allemand" in q or "der" in q:
        reponse = "Allemand : der = masculin, die = feminin, das = neutre. Exemple : der Hund, die Katze, das Haus"
    elif "sein" in q:
        reponse = "SEIN : ich bin, du bist, er ist, wir sind, ihr seid, sie sind"
    # ANGLAIS
    elif "anglais" in q or "to be" in q:
        reponse = "TO BE : I am, You are, He is, We are, You are, They are. Exemple : I am 13"
    # GEO / HISTOIRE
    elif "capitale" in q:
        reponse = "Capitales : France=Paris, Suisse=Berne, Allemagne=Berlin, Italie=Rome, Espagne=Madrid, Angleterre=Londres, Japon=Tokyo"
    elif "canton" in q:
        reponse = "Suisse : 26 cantons. Les plus connus : Zurich, Berne, Vaud, Geneve, Fribourg"
    elif "guerre" in q:
        reponse = "2eme Guerre Mondiale : 1939-1945. La Suisse est restee neutre."
    # SCIENCES
    elif "photosynthese" in q:
        reponse = "Photosynthese : Soleil + Eau + CO2 = Oxygene + Sucre. C'est comme ca qu'on respire."
    elif "planete" in q:
        reponse = "Planetes : Mercure, Venus, Terre, Mars, Jupiter, Saturne, Uranus, Neptune"
    elif "eau" in q:
        reponse = "Eau = H2O. Sel = NaCl. Oxygene = O2. CO2 = dioxyde de carbone"
    # CODE
    elif "bonjour" in q or "prenom" in q:
        reponse = "Code Python : prenom = input('Ton prenom ? ') puis print(f'Bonjour {prenom} !')"
    elif "boucle" in q:
        reponse = "Code boucle : for i in range(1,6): print(i) -> affiche 1,2,3,4,5"
    elif "condition" in q or "if" in q:
        reponse = "Code if : if age >= 18: print('Majeur') else: print('Mineur')"
    else:
        reponse = "Je ne connais pas encore ce mot. Essaie : moyenne, table, aire, pythagore, conjuguer, avoir, pluriel, allemand, anglais, capitale, canton, guerre, photosynthese, planete, bonjour, boucle"
    st.success(reponse)
st.write("---")
st.write("Mots qui marchent : moyenne, table, aire, pythagore, pair, conjuguer, avoir, pluriel, adjectif, allemand, anglais, capitale, canton, guerre, photosynthese, planete, eau, bonjour, boucle, condition")

