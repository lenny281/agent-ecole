import streamlit as st
import random
import datetime
import re
import json
import os
import difflib

st.set_page_config(page_title="Agent IA V9 - COMPLET", page_icon="🤖", layout="wide")
st.markdown("""<style>.stApp{background-color:#0a0a0a;color:#e5e5e5}[data-testid="stSidebar"]{background-color:#111}[data-testid="stSidebar"] *{color:#e5e5e5!important}.stChatMessage{background-color:#161616!important;color:#e5e5e5!important;border:1px solid #2a2a2a;border-radius:12px}h1{color:#f0f0f0!important}button{background-color:#1e1e1e!important;color:#e5e5e5!important;border:1px solid #2e2e2e!important;border-radius:10px!important}</style>""", unsafe_allow_html=True)

# ============ SAUVEGARDE ============
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

JSON_Q = """{"facile": [["C est quoi 2+2 ?", "4"], ["C est quoi 5x2 ?", "10"], ["C est quoi la capitale de la France ?", "paris"], ["C est quoi 3x3 ?", "9"], ["C est quoi 10-3 ?", "7"]], "moyen": [["C est quoi 7x8 ?", "56"], ["C est quoi la capitale du Japon ?", "tokyo"], ["C est quoi 15+25 ?", "40"], ["Qui a gagne la Coupe du Monde 2022 ?", "argentine"], ["C est quoi 9x9 ?", "81"]], "difficile": [["C est quoi 12x12 ?", "144"], ["C est quoi la capitale de l Australie ?", "canberra"], ["C est quoi 144 / 12 ?", "12"], ["Combien de Ballons d Or a 【entity-Messi¦canonical_name=Messi】 ?", "8"]], "verbes": [["Conjugue ETRE : je ... ?", "suis"], ["Conjugue AVOIR : tu ... ?", "as"], ["Conjugue TO BE : I ... ?", "am"], ["Conjugue SEIN : ich ... ?", "bin"]], "maths": [["C est quoi 7x8 ?", "56"], ["C est quoi 9x9 ?", "81"], ["C est quoi PI ?", "3.14"]], "francais": [["C est quoi le COD ?", "cod"], ["C est quoi le pluriel de cheval ?", "chevaux"]], "capitales": [["C est quoi la capitale du Japon ?", "tokyo"], ["C est quoi la capitale de la France ?", "paris"]], "10h": [["C est quoi une fonction affine ?", "affine"], ["C est quoi PI ?", "3.14"], ["C est quoi le COD ?", "cod"]]}"""
TRAIN = json.loads(JSON_Q)

# ============ TOUTES LES MATIERES ECOLE ============
MATIERES_GENRES = {
"📐 10H Maths": {"📈 Fonctions": ["C est quoi une fonction ?", "C est quoi une fonction affine ?", "C est quoi la pente ?", "C est quoi l ordonnee a l origine ?", "C est quoi l image ?", "C est quoi l antecedent ?"], "📐 Geometrie 10H": ["C est quoi PI ?", "C est quoi le theoreme de Pythagore ?", "C est quoi Thales ?", "C est quoi l aire ?", "C est quoi le perimetre ?", "C est quoi le volume ?", "C est quoi le cosinus ?", "C est quoi le sinus ?", "C est quoi la tangente ?"], "🧮 Calcul 10H": ["Table de 7", "Toutes les tables de multiplication", "Table de division de 8", "C est quoi la moyenne ?", "C est quoi les puissances ?", "C est quoi les racines ?"], "🍕 Fractions": ["C est quoi une fraction ?", "C est quoi le pourcentage ?", "C est quoi une equation ?", "C est quoi le produit en croix ?"], "📊 Stats": ["C est quoi la moyenne ?", "C est quoi la mediane ?", "C est quoi le mode ?", "C est quoi une probabilite ?"]},
"🇫🇷 10H Francais": {"📖 Grammaire 10H": ["C est quoi le COD ?", "C est quoi le COI ?", "C est quoi le sujet ?", "C est quoi un adjectif ?", "C est quoi le participe passe ?", "C est quoi l accord du participe passe ?"], "✍️ Verbes": ["Conjugue ETRE", "Conjugue AVOIR", "Conjugue ALLER", "Conjugue FAIRE", "Conjugue DIRE", "Conjugue POUVOIR", "Conjugue VOULOIR", "Conjugue SAVOIR", "Conjugue VENIR", "Conjugue VOIR", "Conjugue PRENDRE", "Conjugue MANGER", "Conjugue DORMIR", "Conjugue ECRIRE", "Conjugue LIRE"], "📝 Orthographe": ["C est quoi a / a ?", "C est quoi et / est ?", "C est quoi son / sont ?", "C est quoi le passe compose ?", "C est quoi l imparfait ?", "C est quoi le futur simple ?", "C est quoi le conditionnel ?", "C est quoi le subjonctif ?"], "📚 Vocabulaire": ["C est quoi un synonyme ?", "C est quoi un antonyme ?", "C est quoi une metaphore ?", "C est quoi une comparaison ?", "C est quoi un champ lexical ?", "C est quoi l argumentation ?"]},
"🇩🇪 10H Allemand": {"📖 Grammaire": ["C est quoi der die das ?", "C est quoi l accusatif ?", "C est quoi le datif ?", "C est quoi le nominatif ?", "C est quoi le genitif ?", "C est quoi le Perfekt ?", "C est quoi weil / dass / wenn ?"], "✍️ Verbes": ["Conjugue SEIN", "Conjugue HABEN", "Conjugue GEHEN", "Conjugue MACHEN", "Conjugue KOMMEN", "Conjugue SEHEN", "Conjugue SPRECHEN", "Conjugue ESSEN", "Conjugue LERNEN", "Conjugue KONNEN"], "🌍 Vocabulaire": ["Traduis bonjour en allemand", "Traduis merci en allemand", "Vocabulaire allemand ecole", "Vocabulaire allemand famille", "Vocabulaire allemand maison"]},
"🇬🇧 10H Anglais": {"📖 Grammaire": ["C est quoi le present simple ?", "C est quoi le present perfect ?", "C est quoi le preterit ?", "C est quoi le comparatif ?", "C est quoi some / any ?", "C est quoi much / many ?"], "✍️ Verbes": ["Conjugue TO BE", "Conjugue TO HAVE", "Conjugue TO GO", "Conjugue TO DO", "Conjugue TO SAY", "Conjugue TO SEE", "Conjugue TO COME", "Conjugue TO MAKE", "Conjugue TO TAKE", "Conjugue TO GIVE"], "🌍 Vocabulaire": ["Traduis bonjour en anglais", "Traduis merci en anglais", "Vocabulaire anglais ecole", "Vocabulaire anglais famille", "Vocabulaire anglais maison"]},
"🇪🇸 Espagnol": {"✍️ Verbes": ["Conjugue SER", "Conjugue ESTAR", "Conjugue TENER", "Conjugue IR", "Conjugue HACER", "Conjugue HABLAR", "Conjugue COMER"], "🌍 Vocabulaire": ["Traduis bonjour en espagnol", "Traduis merci en espagnol"]},
"🇮🇹 Italien": {"✍️ Verbes": ["Conjugue ESSERE", "Conjugue AVERE", "Conjugue ANDARE", "Conjugue FARE", "Conjugue PARLARE", "Conjugue MANGIARE"], "🌍 Vocabulaire": ["Traduis bonjour en italien", "Traduis merci en italien"]},
"📜 10H Histoire": {"📜 Suisse": ["C est quoi la Suisse ?", "C est quoi le pacte de 1291 ?", "C est quoi Guillaume Tell ?", "C est quoi la neutralite suisse ?", "C est quoi la democratie directe ?", "C est quoi l ONU ?", "C est quoi l 【entity-UE¦canonical_name=UE】 ?"], "🌍 Monde": ["C est quoi Rome ?", "C est quoi le Moyen Age ?", "C est quoi l Egypte ?", "C est quoi Napoleon ?", "C est quoi la 1ere Guerre ?", "C est quoi la 2eme Guerre ?", "C est quoi la Guerre Froide ?", "C est quoi la Revolution ?"]},
"🌍 10H Geographie": {"🌍 Suisse": ["C est quoi les continents ?", "C est quoi les oceans ?", "Capitale du Japon ?", "Capitale de la France ?", "Capitale de la Suisse ?", "C est quoi les cantons suisses ?", "C est quoi les Alpes ?", "C est quoi la migration ?", "C est quoi le developpement durable ?", "C est quoi le rechauffement climatique ?"], "🗺️ Cartes": ["C est quoi une carte ?", "C est quoi l echelle ?", "C est quoi la latitude ?", "C est quoi la longitude ?", "C est quoi le climat ?"]},
"🔬 10H Sciences": {"🧬 Biologie": ["C est quoi la photosynthese ?", "C est quoi le coeur ?", "C est quoi l ADN ?", "C est quoi le cerveau ?", "C est quoi la digestion ?", "C est quoi la respiration ?", "C est quoi la puberte ?", "C est quoi le systeme immunitaire ?", "C est quoi l evolution ?"], "🌍 Terre": ["C est quoi un volcan ?", "C est quoi les saisons ?", "C est quoi la foudre ?", "C est quoi le systeme solaire ?", "C est quoi un trou noir ?", "C est quoi Mars ?", "C est quoi les seismes ?", "C est quoi le cycle de l eau ?"], "⚡ Physique": ["C est quoi la gravite ?", "Comment calculer la masse volumique ?", "C est quoi la vitesse ?", "C est quoi l energie ?"]},
"🧪 10H Chimie": {"⚛️ Chimie": ["C est quoi un atome ?", "C est quoi l oxygene ?", "C est quoi le tableau periodique ?", "C est quoi le pH ?", "C est quoi un acide ?", "C est quoi une base ?", "C est quoi la combustion ?", "C est quoi le CO2 ?"], "⚡ Physique": ["C est quoi l electricite ?", "C est quoi un circuit electrique ?", "C est quoi la loi Ohm ?", "C est quoi un aimant ?", "C est quoi la tension ?", "C est quoi l intensite ?"]},
"💻 10H Informatique": {"🧠 Bases": ["C est quoi une variable ?", "C est quoi une boucle ?", "C est quoi une condition ?", "C est quoi un algorithme ?", "C est quoi un bit ?", "C est quoi le binaire ?", "C est quoi Internet ?", "C est quoi le cloud ?", "C est quoi un virus informatique ?", "C est quoi le cyberharcelement ?"], "🌐 Langages": ["C est quoi Python ?", "C est quoi HTML ?", "C est quoi CSS ?", "C est quoi JavaScript ?", "C est quoi l IA ?"]},
"💰 10H Economie / Droit": {"💰 Economie": ["C est quoi un salaire ?", "C est quoi un budget ?", "C est quoi un impot ?", "C est quoi la TVA ?", "C est quoi l inflation ?", "C est quoi le chomage ?", "C est quoi l offre et la demande ?", "C est quoi une entreprise ?", "C est quoi la bourse ?", "Comment devenir millionnaire ?"], "⚖️ Droit": ["C est quoi une loi ?", "C est quoi la democratie ?", "C est quoi voter ?", "C est quoi la majorite ?", "C est quoi les droits de l enfant ?", "C est quoi un contrat ?"]},
"🎨 Arts / Musique": {"🎨 Arts": ["C est quoi la Joconde ?", "C est quoi Van Gogh ?", "C est quoi Picasso ?", "C est quoi la perspective ?", "C est quoi les couleurs primaires ?"], "🎵 Musique": ["C est quoi le rap ?", "C est quoi le piano ?", "C est quoi la guitare ?", "C est quoi une note ?", "C est quoi le rythme ?", "C est quoi la melodie ?"]},
"🏃 10H Sport / Sante": {"⚽ Sports": ["C est quoi le foot ?", "C est quoi le basket ?", "C est quoi le tennis ?", "C est quoi la Formule 1 ?", "C est quoi les JO ?", "C est quoi le fair-play ?"], "❤️ Sante": ["C est quoi manger sain ?", "C est quoi le sommeil ?", "C est quoi les addictions ?", "C est quoi le stress ?", "C est quoi les premiers secours ?", "C est quoi le 144 ?"]},
"🏠 Ecole de la vie": {"🧠 Methodes": ["Conseil pour reviser", "Comment apprendre par coeur ?", "Comment faire un expose ?", "Comment gerer son temps ?", "Comment ne pas stresser avant un test ?"], "💬 Vie": ["Comment gerer un conflit ?", "Comment se faire des amis ?", "Comment dire non ?", "Comment avoir confiance en soi ?", "C est quoi un stage ?", "C est quoi un apprentissage ?", "C est quoi le gymnase ?"]},
}

# ============ TOUS LES AUTRES THEMES ============
THEMES = {
"📐 Ecole": ["Voir toutes les matieres"],
"🎮 Jeux": ["Jeu Clicker", "Jeu Devine le nombre", "Jeu Pierre Papier Ciseaux", "Jeu Reflexe"],
"👋 Bases": ["Bonjour", "Ca va ?", "Merci", "Au revoir", "Tu t appelles comment ?", "Raconte une blague", "Motive moi", "Conseil pour reviser"],
"🧮 Calculatrice": ["Calcule 12+8", "Calcule 15x7", "Calcule 144/12"],
"🌍 Traductions": ["Traduis bonjour en anglais", "Traduis merci en anglais", "Traduis bonjour en allemand", "Traduis bonjour en espagnol", "Traduis bonjour en italien"],
"🎲 Fun": ["Raconte une blague", "Motive moi", "Quelle heure il est ?", "Quelle date on est ?", "Devinette"],
"🌍 Capitales": ["Capitale du Japon ?", "Capitale du Bresil ?", "Capitale de l Egypte ?", "Capitale de la Suisse ?", "Capitale de la France ?", "Capitale du Canada ?", "Capitale de l Australie ?"],
"✈️ Avions": ["Quel est l avion de chasse le plus performant ?", "C est quoi le F-22 ?", "C est quoi le F-35 ?", "C est quoi le Rafale ?", "C est quoi le SR-71 ?", "C est quoi le Concorde ?", "C est quoi le A380 ?", "Comment vole un avion ?", "C est quoi le F-16 ?", "C est quoi le Mirage ?"],
"💻 PC": ["C est quoi le meilleur rapport qualite prix ?", "C est quoi la meilleure GPU ?", "C est quoi le meilleur CPU ?", "C est quoi le meilleur SSD ?", "PC 2000 CHF", "PC 1300 CHF", "PC 900 CHF", "C est quoi les FPS ?", "C est quoi le ping ?", "C est quoi le meilleur clavier ?", "C est quoi le meilleur ecran ?"],
"⚽ Foot / Sport": ["C est qui 【entity-Messi¦canonical_name=Messi】 ?", "C est qui 【entity-Ronaldo¦canonical_name=RONALDO】 ?", "C est qui 【entity-Mbappe¦canonical_name=MBAPPE】 ?", "C est qui 【entity-Haaland¦canonical_name=HAALAND】 ?", "C est qui 【entity-Bellingham¦canonical_name=BELLINGHAM】 ?", "C est quoi la Coupe du Monde ?", "C est quoi la Ligue des Champions ?", "C est quoi le Ballon d Or ?"],
"🎮 Jeux Video": ["C est quoi Minecraft ?", "C est quoi Fortnite ?", "C est quoi Roblox ?", "C est quoi GTA ?", "C est quoi Brawl Stars ?", "C est quoi Pokemon ?", "C est quoi Mario ?", "C est quoi One Piece ?", "C est quoi Naruto ?", "C est quoi Dragon Ball ?", "C est quoi Clash Royale ?", "C est quoi Stumble Guys ?"],
"🚀 Espace": ["C est quoi un trou noir ?", "C est quoi le Big Bang ?", "C est quoi Mars ?", "C est quoi l ISS ?", "C est quoi le Soleil ?", "C est quoi la Lune ?", "C est quoi une galaxie ?"],
"🎤 Chanteurs": ["C est qui Werenoi ?", "C est qui Ninho ?", "C est qui Jul ?", "C est qui Gazo ?", "C est qui Tiakola ?", "C est qui PNL ?", "C est qui SDM ?", "C est qui Drake ?", "C est qui Taylor Swift ?", "C est qui Eminem ?", "C est qui Stromae ?", "C est qui Soprano ?", "C est qui Maes ?", "C est qui SCH ?", "C est qui Damso ?", "C est qui Booba ?"],
"💰 Argent / Metiers": ["Comment devenir millionnaire ?", "C est quoi un salaire ?", "C est quoi un entrepreneur ?", "Comment gagner de l argent a 13 ans ?", "C est quoi la bourse ?", "C est quoi un ETF ?"],
"🐾 Animaux": ["C est quoi le plus grand animal ?", "C est quoi le plus rapide ?", "C est quoi un chien ?", "C est quoi un chat ?", "C est quoi un lion ?", "C est quoi un dauphin ?", "C est quoi un requin ?", "C est quoi un aigle ?"],
"🍔 Cuisine": ["C est quoi une recette facile ?", "C est quoi un gateau au chocolat ?", "C est quoi manger sain ?", "C est quoi une pizza maison ?"],
}

@st.cache_data
def get_tout():
    return {"pi":"PI = 3.14 ! Perimetre = 2 x PI x rayon. Aire = PI x rayon x rayon. Ex : Rayon 5 : Perimetre = 31.4 cm, Aire = 78.5 cm2. Rayon 10 : Perimetre = 62.8, Aire = 314. Le 14 mars = journee de PI !","pythagore":"PYTHAGORE 10H : a2 + b2 = c2. Ex : 3-4-5 car 9+16=25.","thales":"THALES 10H : AB / AD = AC / AE = BC / DE.","aire":"AIRE 10H : Rectangle = L x l, Carre = cote x cote, Triangle = (base x hauteur) / 2, Cercle = PI x rayon2.","perimetre":"PERIMETRE 10H : Carre = 4 x cote, Rectangle = 2 x (L+l), Cercle = 2 x PI x rayon.","volume":"VOLUME 10H : Cube = cote3, Pave = L x l x h, Cylindre = PI x r2 x h.","cod":"COD 10H : Complement d Objet Direct. Repond a Qui ? ou Quoi ? Ex : Je mange une pomme. Une pomme = COD.","coi":"COI 10H : Repond a A qui ? A quoi ? Ex : Je parle a Lenny. A Lenny = COI.","sujet":"SUJET 10H : Qui fait l action. Ex : Lenny mange. Lenny = sujet.","photosynthese":"PHOTOSYNTHESE 10H : Soleil + Eau + CO2 = Oxygene + Sucre.","coeur":"COEUR 10H : Pompe le sang dans tout le corps.","gravite":"GRAVITE 10H : Nous attire vers la Terre. Decouverte par Newton.","atome":"ATOME 10H : Noyau (protons + neutrons) + electrons.","ph":"PH 10H : 0-6 = acide (citron = 2), 7 = neutre (eau), 8-14 = basique (savon = 10).","loi ohm":"LOI OHM 10H : U = R x I. Ex : R=10, I=2, U=20V.","salaire":"SALAIRE 10H : En Suisse, median environ 6500 CHF brut.","tva":"TVA 10H : Suisse : 8.1% general, 2.6% nourriture, 3.8% hotel.","democratie":"DEMOCRATIE 10H : Le peuple decide. Suisse = democratie directe.","foot":"FOOT 10H : 2 equipes de 11, 90 minutes. Sport le plus joue au monde.","【entity-messi¦canonical_name=Messi】":"【entity-MESSI¦canonical_name=Messi】 : 8 Ballons d Or (record), Coupe du Monde 2022.","【entity-ronaldo¦canonical_name=RONALDO】":"【entity-RONALDO¦canonical_name=RONALDO】 : 5 Ballons d Or, meilleur buteur de l histoire.","【entity-mbappe¦canonical_name=MBAPPE】":"【entity-MBAPPE¦canonical_name=MBAPPE】 : Champion du Monde 2018 a 19 ans. Vitesse 36 km/h. 【entity-Real Madrid¦canonical_name=Real Madrid】 depuis 2024.","【entity-haaland¦canonical_name=HAALAND】":"【entity-HAALAND¦canonical_name=HAALAND】 : Attaquant de 【entity-Manchester City¦canonical_name=Manchester City】. Machine a buts, celebration meditation.","【entity-bellingham¦canonical_name=BELLINGHAM】":"【entity-BELLINGHAM¦canonical_name=BELLINGHAM】 : Milieu du 【entity-Real Madrid¦canonical_name=Real Madrid】, ne en 2003. Deja parmi les meilleurs.","ballon d or":"BALLON D OR : 【entity-Messi¦canonical_name=Messi】 8 (record), 【entity-Ronaldo¦canonical_name=RONALDO】 5.","coupe du monde":"COUPE DU MONDE : Tous les 4 ans, 48 equipes en 2026. 2022 = Argentine gagne contre France.","ligue des champions":"LIGUE DES CHAMPIONS : 【entity-Real Madrid¦canonical_name=Real Madrid】 15 fois, record !","minecraft":"MINECRAFT : Jeu le plus vendu au monde. Monde en cubes, Creeper, Ender Dragon.","fortnite":"FORTNITE : Battle Royale : 100 joueurs, le dernier gagne.","roblox":"ROBLOX : Des millions de jeux crees par les joueurs. Brookhaven, Blox Fruits, Doors.","gta":"GTA V : Beaucoup de millions de copies. Los Santos. GTA VI sort en 2026, a Vice City.","brawl stars":"BRAWL STARS : Jeu mobile de Supercell. 3v3, Shelly, Colt, Spike, Leon...","pokemon":"POKEMON : Attrape-les tous ! 1000+ Pokemons. Pikachu = mascotte.","mario":"MARIO : Plombier Nintendo, sauve Peach. Mario Kart, Mario Party.","one piece":"ONE PIECE : Manga le plus vendu. Luffy veut devenir Roi des Pirates.","naruto":"NARUTO : Ninja qui veut devenir Hokage. Rasengan, Chidori, Kyubi.","dragon ball":"DRAGON BALL : Goku, Super Saiyan, Kamehameha !","clash royale":"CLASH ROYALE : Jeu de cartes de Supercell. Defends tes tours, attaque celles de l ennemi.","stumble guys":"STUMBLE GUYS : Comme Fall Guys. 32 joueurs, parcours, le dernier gagne.","trou noir":"TROU NOIR 10H : Tellement lourd que meme la lumiere ne peut pas en sortir.","big bang":"BIG BANG : Debut de l univers il y a 13.8 milliards d annees.","mars":"MARS : Planete rouge. Jour = 24h37. Temperature -60 degres. Robots : Perseverance.","iss":"ISS : Station Spatiale a 400 km, a 28 000 km/h.","soleil":"SOLEIL : C est une etoile, pas une planete. 5500 degres a la surface.","lune":"LUNE : Distance 384 000 km. Premier homme : Neil Armstrong, 1969. Elle fait les marees.","galaxie":"GALAXIE : Groupe de milliards d etoiles. Notre galaxie = Voie Lactee.","werenoi":"WERENOI : Jeremy Bana Owona. Albums : Pyramide, Diamant Noir.","ninho":"NINHO : William Nzobazola. Le plus de disques d or en France !","jul":"JUL : Julien Mari, Marseille. Le plus productif : 2 albums par an ! Tchikita, Bande organisee.","gazo":"GAZO : Roi de la drill en France ! Albums : KMT, Apocalypse. La Melo avec Tiakola.","tiakola":"TIAKOLA : Membre de 4Keus. Albums : Melo, BDLM. La Melo, Gasolina.","pnl":"PNL : Duo de freres Ademo et N.O.S. Dans la legende, Deux freres. Le monde ou rien.","sdm":"SDM : Repere par Booba. Albums : Ocho, A vie. Bolide allemand avec Ninho.","drake":"DRAKE : Rappeur canadien, le plus streame au monde. God s Plan, One Dance.","taylor swift":"TAYLOR SWIFT : La plus ecoutee au monde. 14 Grammy. Eras Tour = tournee la plus rentable.","eminem":"EMINEM : Legende. Lose Yourself, Rap God, Mockingbird.","stromae":"STROMAE : Chanteur belge. Alors on danse, Papaoutai, Formidable.","soprano":"SOPRANO : Chanteur de Marseille. Cosmo, En feu."," maes":" MAES : Rappeur de Sevran. Les derniers salopards. Distant avec Ninho.","sch":"SCH : Rappeur de Marseille. A7, JVLIVS. Bande organisee.","damso":"DAMSO : Rappeur belge. Batterie faible, Ipseité, QALF. Macarena.","booba":"BOOBA : Duc de Boulogne. Temps mort, Lunatic. DKR.","millionnaire":"COMMENT DEVENIR MILLIONNAIRE ? 1. Salarie + investissement. 2. Entrepreneur. 3. Createur. Apprends une competence, epargne, investis tot.","gagner de l argent":"GAGNER DE L ARGENT A 13 ANS : Petits services, vendre ce que tu n utilises plus, creer un projet, apprendre une competence.","bourse":"BOURSE : Acheter une partie d une entreprise. ETF = panier de 500 entreprises, moins risque.","etf":"ETF : Panier de beaucoup d actions. Moins risque, parfait pour debuter.","entrepreneur":"ENTREPRENEUR : Personne qui cree sa propre entreprise. Ex : 【entity-Elon Musk¦canonical_name=Elon Musk】, Steve Jobs.","plus grand animal":"PLUS GRAND ANIMAL : Baleine bleue ! 30m, 200 tonnes !","plus rapide":"PLUS RAPIDE : Guepard = 110 km/h. Faucon pelerin = 390 km/h en pique !","chien":"CHIEN : Meilleur ami de l homme depuis 15 000 ans. 400 races. Il comprend 150 mots.","chat":"CHAT : Il dort 16h par jour ! Il peut sauter 6x sa hauteur.","lion":"LION : Roi des animaux. Il dort 20h par jour ! Rugit a 8 km.","dauphin":"DAUPHIN : Tres intelligent. Il dort avec un oeil ouvert. 60 km/h.","requin":"REQUIN : Depuis 450 millions d annees, avant les dinosaures ! 5 a 7 rangees de dents.","aigle":"AIGLE : Il voit 8x mieux que nous. 160 km/h en pique. Symbole des USA.","recette facile":"RECETTE FACILE - PATES : 1. Eau salee bouillante. 2. Pates 8-10 min. 3. Egoutte. 4. Sauce tomate + fromage.","gateau au chocolat":"GATEAU AU CHOCOLAT : 200g chocolat, 200g beurre, 4 oeufs, 150g sucre, 100g farine. Four 180 degres, 25 min.","pizza maison":"PIZZA MAISON : Pate + sauce tomate + fromage + ce que tu aimes. Four 220 degres, 12-15 min.","fonction affine":"FONCTION AFFINE : f(x) = a x + b. a = pente, b = ordonnee a l origine.","moyenne":"MOYENNE : somme / nombre. Ex : 12, 15, 18 -> Moyenne = 15.","fraction":"FRACTION : 1/2 = moitie, 1/4 = quart. 1/2 + 1/4 = 3/4.","pourcentage":"POURCENTAGE : (partie / total) x 100. Ex : 20% de 50 = 10.","equation":"EQUATION : 2x + 3 = 7 -> 2x = 4 -> x = 2.","passe compose":"PASSE COMPOSE : ETRE ou AVOIR + participe passe. Ex : J ai mange, Je suis alle.","imparfait":"IMPARFAIT : Action longue dans le passe. Ex : Quand j etais petit, je jouais au foot.","suisse":"SUISSE : 26 cantons, 4 langues, Capitale Berne, 8.9 millions, CHF, Neutralite depuis 1515.","pacte de 1291":"PACTE DE 1291 : 1er aout 1291, Uri, Schwyz, Unterwald. Naissance de la Suisse.","foudre":"FOUDRE : Tres chaud, plus chaud que le Soleil ! Si tu entends le tonnerre, rentre.","systeme solaire":"SYSTEME SOLAIRE : 8 planetes : Mercure, Venus, Terre, Mars, Jupiter, Saturne, Uranus, Neptune.","electricite":"ELECTRICITE : Tension (V), Intensite (A), Puissance (W). P = U x I.","vitesse":"VITESSE : v = d / t. Ex : 100m en 10 sec = 10 m/s = 36 km/h.","adn":"ADN : Ton code genetique. 50% pere, 50% mere.","python":"PYTHON : Langage facile, celui de ton agent. Pour l IA, les sites, les jeux.","ia":"IA : Programme qui apprend avec des donnees. Ex : ChatGPT, ton agent.","internet":"INTERNET : Reseau mondial d ordinateurs relies.","budget":"BUDGET : Regle 50/30/20 : 50 besoins, 30 envies, 20 epargne.","rapport qualite prix":"MEILLEUR RAPPORT PC : 1300 CHF : RTX 5070 + Ryzen 7 7800X3D + 32 Go + SSD 1 To. 1440p Ultra 180 FPS. 900 CHF : RTX 4060 + Ryzen 5 7600. 2000 CHF : RTX 5070 Ti + 9800X3D.","meilleure gpu":"MEILLEURE GPU : 1. RTX 5090 - 32 Go, 4K 200 FPS, 2500 CHF. 2. RTX 5070 - MEILLEUR RAPPORT : 12 Go, 1440p 180 FPS, 600 CHF.","meilleur cpu":"MEILLEUR CPU : Ryzen 7 7800X3D - MEILLEUR RAPPORT, 350 CHF. Ryzen 7 9800X3D - ROI GAMING, 450 CHF.","meilleur ssd":"MEILLEUR SSD : 【entity-Samsung¦canonical_name=Samsung】 990 PRO 2 To - Windows en 5 sec, 180 CHF.","fps":"FPS : 30 = ca lag, 60 = fluide, 144 = super fluide, 240 = pro.","ping":"PING : 10 ms = parfait, 30 ms = tres bien, 100 ms = ca lag, 200 ms = injouable.","meilleur clavier":"MEILLEUR CLAVIER : 【entity-Logitech¦canonical_name=Logitech】 G Pro X - 150 CHF. Ou 【entity-Keychron¦canonical_name=Keychron】 K2 - 100 CHF.","meilleur ecran":"MEILLEUR ECRAN : 27 pouces 1440p 165Hz - 250 CHF.","f-22":"F-22 RAPTOR (USA) - LE PLUS PERFORMANT EN COMBAT. Mach 2.25. Furtif, jamais battu.","f-35":"F-35 LIGHTNING II (USA) - LE PLUS MODERNE. Mach 1.6. La Suisse en a achete 36 !","rafale":"RAFALE (France). Mach 1.8. Polyvalent : air, sol, mer.","sr-71":"SR-71 BLACKBIRD. Mach 3.3 = 3500 km/h ! Plus rapide de tous les temps.","concorde":"CONCORDE : Paris-New York en 3h30. Mach 2. Arrete en 2003.","a380":"AIRBUS A380 : Le plus gros avion de passagers. 2 etages, 850 passagers max !","f-16":"F-16. Mach 2.0. Plus produit : 4600 exemplaires !","mirage":"MIRAGE 2000 (France). Mach 2.2. Utilise par la France, l Inde, les Emirats.","comment vole":"COMMENT VOLE UN AVION ? L aile est courbee en haut, plate en bas. L air va plus vite au-dessus, donc pression plus faible. Ca cree la portance."}
@st.cache_data
def get_capitales():
    return {"france":"Paris - Tour Eiffel","suisse":"Berne - Capitale depuis 1848","japon":"Tokyo - Plus grande ville","bresil":"Brasilia - Rio plus connue","allemagne":"Berlin - Mur tombe 1989","italie":"Rome - Colisee","espagne":"Madrid - Real Madrid","angleterre":"Londres - Big Ben","usa":"Washington - Maison Blanche","canada":"Ottawa - Toronto plus grande","chine":"Pekin - Grande Muraille","australie":"Canberra - Sydney plus connue","egypte":"Le Caire - Pyramides","maroc":"Rabat","portugal":"Lisbonne - Ronaldo","belgique":"Bruxelles - Frites","grece":"Athenes - JO","mexique":"Mexico - Tacos","argentine":"Buenos Aires - Messi","inde":"New Delhi - Taj Mahal","russie":"Moscou - Place Rouge","qatar":"Doha - Mondial 2022","nepal":"Katmandou - Everest"}
@st.cache_data
def get_all_q():
    base = list(get_tout().keys()) + list(get_capitales().keys())
    for v in TRAIN.values():
        for q,a in v: base.append(q)
    return base
TOUT = get_tout(); CAPITALES = get_capitales(); ALL_Q = get_all_q()
VERBES = {"etre":"ETRE : je suis, tu es, il est, nous sommes, vous etes, ils sont. Passe : j ai ete. Futur : je serai.","avoir":"AVOIR : j ai, tu as, il a, nous avons, vous avez, ils ont. Passe : j ai eu. Futur : j aurai.","aller":"ALLER : je vais, tu vas, il va, nous allons, vous allez, ils vont. Passe : je suis alle. Futur : j irai.","faire":"FAIRE : je fais, tu fais, il fait, nous faisons, vous faites, ils font. Passe : j ai fait.","dire":"DIRE : je dis, tu dis, il dit, nous disons, vous dites, ils disent. Passe : j ai dit.","pouvoir":"POUVOIR : je peux, tu peux, il peut, nous pouvons, vous pouvez, ils peuvent.","vouloir":"VOULOIR : je veux, tu veux, il veut, nous voulons, vous voulez, ils veulent.","savoir":"SAVOIR : je sais, tu sais, il sait, nous savons, vous savez, ils savent.","sein":"SEIN = ETRE en Allemand. ich bin, du bist, er ist, wir sind, ihr seid, sie sind.","haben":"HABEN = AVOIR en Allemand. ich habe, du hast, er hat, wir haben, ihr habt, sie haben.","gehen":"GEHEN = ALLER en Allemand. ich gehe, du gehst, er geht, wir gehen, ihr geht, sie gehen.","to be":"TO BE = ETRE en Anglais. I am, You are, He is, We are, You are, They are.","to have":"TO HAVE = AVOIR en Anglais. I have, You have, He has.","to go":"TO GO = ALLER en Anglais. I go, He goes. Passe : I went.","ser":"SER = ETRE en Espagnol. yo soy, tu eres, el es, nosotros somos.","estar":"ESTAR = ETRE en Espagnol. yo estoy, tu estas, el esta.","tener":"TENER = AVOIR en Espagnol. yo tengo, tu tienes, el tiene.","essere":"ESSERE = ETRE en Italien. io sono, tu sei, lui e.","avere":"AVERE = AVOIR en Italien. io ho, tu hai, lui ha."}
BASES = {"bonjour":"Bonjour ! V9 COMPLETE ! Ecole + Jeux + Avions + PC + Foot + Chanteurs + Tout !","salut":"Salut ! Ca va ?","merci":"De rien !","ca va":"Ca va super ! Et toi ?","au revoir":"Au revoir ! A tres vite !"}
BLAGUES = ["Pourquoi les plongeurs plongent-ils toujours en arriere ? Parce que sinon, ils tombent dans le bateau !","Que dit un zero a un huit ? Belle ceinture !","Pourquoi les maths sont tristes ? Parce qu elles ont trop de problemes !","Pourquoi PI est trop fort ? Parce qu il ne s arrete jamais !"]
MOTIVATIONS = ["Tu peux le faire ! Chaque erreur, c est une lecon. Ne lache rien !","N abandonne jamais ! 10 minutes par jour, et dans 1 mois tu seras trop fort !"]
TRAD = {"bonjour en anglais":"Bonjour en anglais = Hello !","merci en anglais":"Merci en anglais = Thank you !","bonjour en allemand":"Bonjour en allemand = Hallo !","merci en allemand":"Merci en allemand = Danke !","bonjour en espagnol":"Bonjour en espagnol = Hola !","merci en espagnol":"Merci en espagnol = Gracias !","bonjour en italien":"Bonjour en italien = Ciao !","merci en italien":"Merci en italien = Grazie !"}

if "learned" not in st.session_state: st.session_state.learned = charger()
if "messages" not in st.session_state: st.session_state.messages = [{"role":"assistant","content":"Salut ! V9 COMPLETE ! Ecole + Jeux + Avions + PC + Foot + Chanteurs + Tout ! Essaie : recherche pi en haut !"}]
for k,v in [("score",0),("total_quiz",0),("streak",0),("best_streak",0),("train_q",None),("train_a",None),("mode_train",False),("niveau","moyen"),("auto_q",""),("cookies",0),("click_power",1),("nombre_secret",random.randint(1,100)),("coups",0),("xp",0),("theme","📐 Ecole"),("matiere",None),("genre",None)]:
    if k not in st.session_state: st.session_state[k]=v

def nettoyer(txt):
    txt=txt.lower().strip(); txt=txt.replace("é","e").replace("è","e").replace("ê","e").replace("à","a").replace("ç","c").replace("ô","o").replace("î","i")
    txt=re.sub(r"[^a-z0-9 +*/\-=?.]", " ", txt); txt=re.sub(r"\s+"," ",txt).strip(); return txt
def ajouter_cookie(): st.session_state.cookies += st.session_state.click_power; st.session_state.xp += 1
def acheter_click():
    if st.session_state.cookies >= 50: st.session_state.cookies -= 50; st.session_state.click_power += 1
def lancer(niveau):
    st.session_state.mode_train=True; st.session_state.niveau=niveau
    nq,na = random.choice(TRAIN[niveau]); st.session_state.train_q=nq; st.session_state.train_a=na
    st.session_state.messages.append({"role":"assistant","content":"C EST PARTI - "+niveau.upper()+" ! Question : "+nq})
def quitter():
    st.session_state.mode_train=False; st.session_state.train_q=None
    st.session_state.messages.append({"role":"assistant","content":"Entrainement termine ! Score : "+str(st.session_state.score)+"/"+str(st.session_state.total_quiz)})

st.title("Agent IA V9 - COMPLET 🤖 - Ecole + Tout + Jeux")
st.caption(f"XP : {st.session_state.xp} | Score : {st.session_state.score}/{st.session_state.total_quiz} | Streak : {st.session_state.streak} 🔥 | Appris : {len(st.session_state.learned)} | Cookies : {st.session_state.cookies} 🍪")

# ============ RECHERCHE ============
recherche = st.text_input("🔍 RECHERCHE - Tape ici, je trouve tout : pi, cod, japon, messi, f-22, rtx, minecraft...", key="rech_v9")
if recherche:
    qn = nettoyer(recherche); res = []
    for cle, rep in TOUT.items():
        if qn in nettoyer(cle): res.append((cle, rep))
    for pays, cap in CAPITALES.items():
        if qn in pays: res.append((f"Capitale de {pays}", cap))
    if res:
        st.success(f"✅ {len(res)} resultat(s) pour : {recherche}")
        for titre, rep in res[:5]:
            if st.button(f"👉 {titre}", key="rch_"+titre, use_container_width=True):
                st.session_state.messages.append({"role":"user","content":titre}); st.session_state.auto_q = titre
    else:
        proches = difflib.get_close_matches(recherche, ALL_Q, n=5, cutoff=0.35)
        if proches:
            st.info("Tu voulais dire ?")
            for p in proches:
                if st.button(f"💡 {p}", key="sugg_"+p, use_container_width=True):
                    st.session_state.messages.append({"role":"user","content":p}); st.session_state.auto_q = p
        else: st.warning(f"Rien pour : {recherche}. Essaie : pi, cod, japon...")

# ============ SIDEBAR ============
with st.sidebar:
    st.title("Agent V9 COMPLET")
    st.write(f"XP : {st.session_state.xp} | Score : {st.session_state.score}/{st.session_state.total_quiz}")
    st.divider()
    if st.button("📐 ECOLE", use_container_width=True): st.session_state.theme="📐 Ecole"; st.session_state.matiere=None; st.session_state.genre=None
    if st.button("🎮 JEUX", use_container_width=True): st.session_state.theme="🎮 Jeux"
    if st.button("✈️ AVIONS", use_container_width=True): st.session_state.theme="✈️ Avions"
    if st.button("💻 PC", use_container_width=True): st.session_state.theme="💻 PC"
    if st.button("⚽ FOOT", use_container_width=True): st.session_state.theme="⚽ Foot / Sport"
    if st.button("🎤 CHANTEURS", use_container_width=True): st.session_state.theme="🎤 Chanteurs"
    if st.button("🎮 JEUX VIDEO", use_container_width=True): st.session_state.theme="🎮 Jeux Video"
    if st.button("🚀 ESPACE", use_container_width=True): st.session_state.theme="🚀 Espace"
    if st.button("🌍 CAPITALES", use_container_width=True): st.session_state.theme="🌍 Capitales"
    if st.button("💰 ARGENT", use_container_width=True): st.session_state.theme="💰 Argent / Metiers"
    if st.button("🐾 ANIMAUX", use_container_width=True): st.session_state.theme="🐾 Animaux"
    if st.button("🍔 CUISINE", use_container_width=True): st.session_state.theme="🍔 Cuisine"
    st.divider(); st.write("MATIERES ECOLE :")
    for m in MATIERES_GENRES.keys():
        if st.button(m, key="side_m_"+m, use_container_width=True): st.session_state.theme="📐 Ecole"; st.session_state.matiere=m; st.session_state.genre=None
    st.divider()
    if not st.session_state.mode_train:
        if st.button("🎯 ENTRAINEMENT", use_container_width=True): lancer("moyen")
    else:
        st.success(f"EN TRAIN : {st.session_state.train_q}"); st.button("❌ QUITTER", on_click=quitter, use_container_width=True)

# ============ ENTRAINEMENT ============
if not st.session_state.mode_train:
    st.subheader("🎯 MODE ENTRAINEMENT")
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
    st.success(f"🎯 ENTRAINEMENT {st.session_state.niveau.upper()} - Score : {st.session_state.score}/{st.session_state.total_quiz}")
    st.info(f"❓ QUESTION : {st.session_state.train_q}")
    st.button("❌ QUITTER ENTRAINEMENT", on_click=quitter, use_container_width=True)

# ============ JEUX ============
if st.session_state.theme == "🎮 Jeux":
    st.subheader("🎮 JEUX")
    jeu = st.selectbox("Choisis :", ["Jeu Clicker","Jeu Devine le nombre","Jeu Pierre Papier Ciseaux","Jeu Reflexe"])
    if jeu == "Jeu Clicker":
        st.write(f"🍪 Cookies : {st.session_state.cookies} | Puissance : +{st.session_state.click_power}")
        st.button("🍪 CLIQUER !", on_click=ajouter_cookie, use_container_width=True)
        st.button("Acheter +1 - 50 cookies", on_click=acheter_click, use_container_width=True)
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
            elif (toi=="Pierre" and o=="Ciseaux") or (toi=="Papier" and o=="Pierre") or (toi=="Ciseaux" and o=="Papier"): st.success("TU GAGNES !")
            else: st.error("TU PERDS...")
    if jeu == "Jeu Reflexe":
        st.write("Clique le plus vite possible !")
        if st.button("⚡ CLIQUE VITE !", use_container_width=True): st.session_state.xp += 1; st.success(f"Bien joue ! XP : {st.session_state.xp}")

# ============ ECOLE ============
elif st.session_state.theme == "📐 Ecole":
    st.subheader("1 - Choisis ta MATIERE 10H :")
    cols2 = st.columns(4); lm = list(MATIERES_GENRES.keys())
    for i in range(len(lm)):
        m = lm[i]
        with cols2[i%4]:
            sel = "✅ " if st.session_state.matiere == m else ""
            if st.button(sel+m, key="mat_"+m, use_container_width=True): st.session_state.matiere=m; st.session_state.genre=None
    if st.session_state.matiere:
        st.subheader("2 - Choisis ton GENRE :")
        genres = list(MATIERES_GENRES[st.session_state.matiere].keys()); colsG = st.columns(len(genres))
        for i in range(len(genres)):
            g = genres[i]
            with colsG[i]:
                sel = "✅ " if st.session_state.genre == g else ""
                if st.button(sel+g, key="genre_"+g, use_container_width=True): st.session_state.genre=g
    if st.session_state.matiere and st.session_state.genre:
        st.subheader("3 - Clique sur une question :")
        for q in MATIERES_GENRES[st.session_state.matiere][st.session_state.genre]:
            if st.button(q, key="q_"+q, use_container_width=True): st.session_state.messages.append({"role":"user","content":q}); st.session_state.auto_q=q

# ============ AUTRES THEMES ============
else:
    if st.session_state.theme not in ["📐 Ecole","🎮 Jeux"]:
        st.subheader(f"Questions - {st.session_state.theme} - Clique :")
        for q in THEMES.get(st.session_state.theme, []):
            if st.button(q, key="q2_"+q, use_container_width=True): st.session_state.messages.append({"role":"user","content":q}); st.session_state.auto_q=q

# ============ MESSAGES ============
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.write(msg["content"])

def trouver(q_orig):
    q_low = nettoyer(q_orig)
    if st.session_state.mode_train and st.session_state.train_q is not None:
        bonne = nettoyer(st.session_state.train_a); rep_net = q_low
        for mot in ["c est","la reponse c est","reponse","je pense que c est","c"]: rep_net = rep_net.replace(mot, " ")
        rep_net = " ".join(rep_net.split()); st.session_state.total_quiz += 1
        if rep_net == bonne:
            st.session_state.score += 1; st.session_state.streak += 1; st.session_state.xp += 10
            if st.session_state.streak > st.session_state.best_streak: st.session_state.best_streak = st.session_state.streak
            rep = f"BRAVO ! C etait bien {st.session_state.train_a} ! Score : {st.session_state.score}/{st.session_state.total_quiz} | Streak : {st.session_state.streak} 🔥 | +10 XP !"
        else:
            st.session_state.streak = 0; rep = f"Pas tout a fait... Tu as ecrit : {q_orig}. La bonne reponse c etait : {st.session_state.train_a}. Score : {st.session_state.score}/{st.session_state.total_quiz}"
        nq, na = random.choice(TRAIN[st.session_state.niveau]); st.session_state.train_q = nq; st.session_state.train_a = na
        return rep + f"\n\nQuestion suivante : {nq}"
    if q_low in ["stop","quitter","exit"]:
        if st.session_state.mode_train: quitter(); return "Entrainement termine !"
        return "Tu n es pas en entrainement."
    if "mon score" in q_low: return f"Score : {st.session_state.score}/{st.session_state.total_quiz} | XP : {st.session_state.xp}"
    if q_orig.lower().strip().startswith("apprends"):
        try:
            texte = q_orig.lower().replace("apprends :","").replace("apprends","").strip()
            if "=" in texte:
                cle, val = texte.split("=",1); cle = nettoyer(cle); val = val.strip(); st.session_state.learned[cle] = val; sauver(st.session_state.learned)
                return f"MERCI ! J ai appris ET sauvegarde ! {cle} = {val} !"
        except: return "Ecris : Apprends : question = reponse"
    if "montre ce que tu as appris" in q_low:
        if not st.session_state.learned: return "Rien appris..."
        txt = f"CE QUE TU M AS APPRIS ({len(st.session_state.learned)}) :\n\n"
        for k,v in st.session_state.learned.items(): txt += f"- {k} = {v}\n"
        return txt
    for cle,val in st.session_state.learned.items():
        if cle == q_low: return f"Ce que TU m as appris : {val}"
    if any(c in q_orig for c in ["+","x","*","/","-"]) and any(c.isdigit() for c in q_orig):
        try:
            txt = q_orig.lower().replace("calcule","").replace("=","").replace("?","").strip().replace("x","*").replace(",",".")
            if all(c in "0123456789+-*/(). " for c in txt): return f"Calcul : {q_orig} = {eval(txt)} !"
        except: pass
    for cle,rep in BASES.items():
        if nettoyer(cle) in q_low: return rep
    if "blague" in q_low: return random.choice(BLAGUES)
    if "motive" in q_low: return random.choice(MOTIVATIONS)
    if "heure" in q_low: return "Il est "+datetime.datetime.now().strftime("%H:%M")+" !"
    if "date" in q_low: return "On est le "+datetime.datetime.now().strftime("%d/%m/%Y")+" !"
    if "traduis" in q_low:
        for cle,rep in TRAD.items():
            if nettoyer(cle) in q_low: return rep
    if "table de" in q_low or "table du" in q_low:
        try:
            n = int("".join(filter(str.isdigit, q_low))); res = ", ".join([str(n)+"x"+str(i)+"="+str(n*i) for i in range(1,11)]); return f"Table de {n} : {res}"
        except: pass
    if "toutes les tables" in q_low:
        txt = "TOUTES LES TABLES 1 a 12 :\n\n"
        for n in range(1,13): txt += f"Table de {n} : " + ", ".join([f"{n}x{i}={n*i}" for i in range(1,11)]) + "\n\n"
        return txt
    if "capitale" in q_low:
        for pays,cap in CAPITALES.items():
            if pays in q_low: return f"Capitale de {pays.capitalize()} = {cap}"
    for cle,rep in VERBES.items():
        if nettoyer(cle) == q_low or nettoyer(cle) in q_low: return rep
    for mot,rep in TOUT.items():
        if nettoyer(mot) in q_low: return rep
    proches = difflib.get_close_matches(q_low, list(TOUT.keys()) + list(CAPITALES.keys()), n=1, cutoff=0.6)
    if proches: return f"Tu voulais dire : {proches[0]} ? Tape-le dans la recherche en haut !"
    return f"Hmm je ne connais pas : {q_orig}. Apprends-moi : Apprends : {q_orig} = ta reponse"

if st.session_state.auto_q:
    qa = st.session_state.auto_q; st.session_state.auto_q = ""
    ra = trouver(qa); st.session_state.messages.append({"role":"assistant","content":ra})
    with st.chat_message("assistant"): st.write(ra)
if question := st.chat_input("Pose ta question ici !"):
    st.session_state.messages.append({"role":"user","content":question})
    with st.chat_message("user"): st.write(question)
    with st.chat_message("assistant"):
        r = trouver(question); st.write(r)
    st.session_state.messages.append({"role":"assistant","content":r}); st.session_state.xp += 1
