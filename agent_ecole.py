import streamlit as st

st.set_page_config(page_title="Agent IA V5", page_icon="🖤", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #0a0a0a; color: #e5e5e5; }
[data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #222222; }
[data-testid="stSidebar"] * { color: #e5e5e5 !important; }
.stChatMessage { background-color: #161616 !important; color: #e5e5e5 !important; border: 1px solid #2a2a2a; border-radius: 12px; }
h1 { color: #f0f0f0 !important; }
.stChatInput input { background-color: #161616 !important; color: #e5e5e5 !important; border: 1px solid #2a2a2a !important; }
button { background-color: #1e1e1e !important; color: #e5e5e5 !important; border: 1px solid #2e2e2e !important; border-radius: 10px !important; box-shadow: none !important; font-weight: 500 !important; }
button:hover { background-color: #2a2a2a !important; border-color: #3a3a3a !important; color: white !important; }
[data-testid="stCaption"] { color: #888888 !important; }
</style>
""", unsafe_allow_html=True)

if "theme" not in st.session_state:
    st.session_state.theme = "📐 Ecole"

MATIERES = {
    "📐 Maths": ["C'est quoi le théorème de Pythagore ?", "Table de 7", "Toutes les tables de multiplication", "Table de division de 8", "C'est quoi Thales ?", "C'est quoi la moyenne ?", "C'est quoi l'aire ?", "C'est quoi le perimetre ?", "C'est quoi une fraction ?", "C'est quoi le pourcentage ?"],
    "🇫🇷 Français": ["Conjugue ETRE", "Conjugue AVOIR", "Conjugue ALLER", "C'est quoi le passe compose ?", "C'est quoi l'imparfait ?", "C'est quoi le futur ?", "C'est quoi le pluriel ?", "C'est quoi un adjectif ?"],
    "🇩🇪 Allemand": ["C'est quoi der die das ?", "Conjugue SEIN", "Conjugue HABEN", "C'est quoi GEHEN ?"],
    "🇬🇧 Anglais": ["Conjugue TO BE", "Conjugue TO HAVE", "C'est quoi TO GO ?", "C'est quoi le present perfect ?"],
    "📜 Histoire / Géo": ["C'est quoi la 2eme Guerre ?", "C'est quoi la Revolution ?", "C'est quoi Rome ?", "C'est quoi le Moyen Age ?", "C'est quoi l'Egypte ?", "C'est quoi Napoleon ?", "C'est quoi les continents ?", "C'est quoi les oceans ?"],
    "🔬 Sciences": ["Comment calculer la masse volumique ?", "C'est quoi la photosynthese ?", "C'est quoi la gravite ?", "C'est quoi le coeur ?", "C'est quoi un volcan ?", "C'est quoi les saisons ?", "C'est quoi la foudre ?"],
    "🧪 Chimie / Physique": ["C'est quoi un atome ?", "C'est quoi l'oxygene ?", "C'est quoi la chimie ?", "C'est quoi l'electricite ?", "C'est quoi la masse volumique ?", "C'est quoi la densite ?"],
    "💻 Code": ["C'est quoi une variable ?", "C'est quoi une boucle ?", "C'est quoi une condition ?", "C'est quoi Python ?", "C'est quoi HTML ?", "C'est quoi CSS ?"],
}

THEMES = {
    "📐 Ecole": ["Voir toutes les matières 👇"],
    "🌍 Capitales": ["Capitale du Japon ?", "Capitale du Bresil ?", "Capitale de l'Egypte ?"],
    "✈️ Avions": ["Quel est l'avion de chasse le plus performant ?", "C'est quoi le F-22 ?", "C'est quoi le 【entity-F-35¦canonical_name=F-35】 ?", "C'est quoi le Rafale ?"],
    "💻 PC": ["C'est quoi le meilleur rapport qualite prix ?", "C'est quoi la meilleure GPU ?", "C'est quoi le meilleur CPU ?", "PC 2000 CHF", "PC 1300 CHF", "PC 900 CHF"],
    "⚽ Foot / Sport": ["C'est qui 【entity-Messi¦canonical_name=Messi】 ?", "C'est qui 【entity-Ronaldo¦canonical_name=Ronaldo】 ?", "C'est qui Mbappe ?", "C'est quoi la Coupe du Monde ?"],
    "🎮 Jeux Video": ["C'est quoi 【entity-Minecraft¦canonical_name=Minecraft】 ?", "C'est quoi 【entity-Fortnite¦canonical_name=Fortnite】 ?", "C'est quoi 【entity-Roblox¦canonical_name=Roblox】 ?", "C'est quoi GTA ?"],
    "🚀 Espace": ["C'est quoi un trou noir ?", "C'est quoi le Big Bang ?", "C'est quoi Mars ?", "C'est quoi l'ISS ?"],
    "🧪 Science": ["Comment calculer la masse volumique ?", "C'est quoi un atome ?", "C'est quoi la gravite ?"],
    "🧠 Culture G": ["C'est qui Werenoi ?", "C'est qui Ninho ?", "C'est qui Jul ?", "C'est quoi la Tour Eiffel ?", "C'est quoi le 【entity-Titanic¦canonical_name=Titanic】 ?"],
    "🎤 Chanteurs": ["C'est qui Werenoi ?", "C'est qui Ninho ?", "C'est qui Jul ?", "C'est qui 【entity-Gazo¦canonical_name=Gazo】 ?", "C'est qui 【entity-Tiakola¦canonical_name=Tiakola】 ?", "C'est qui 【entity-PNL¦canonical_name=PNL】 ?", "C'est qui SDM ?", "C'est qui 【entity-Drake¦canonical_name=Drake】 ?", "C'est qui 【entity-Taylor Swift¦canonical_name=Taylor Swift】 ?"],
}

with st.sidebar:
    st.title("Agent IA V5")
    st.write("Clique sur un thème")
    for t in THEMES.keys():
        if st.button(t, key="side_"+t, use_container_width=True):
            st.session_state.theme = t
            st.rerun()
    st.divider()
    st.write("MATIERES ECOLE :")
    for m in MATIERES.keys():
        if st.button(m, key="side_m_"+m, use_container_width=True):
            st.session_state.theme = m
            st.rerun()
    st.divider()
    if st.button("Effacer"):
        st.session_state.messages = []
        st.rerun()

st.title("Agent IA V5")
st.caption("Fond noir discret - Reponses developpees et approfondies")

cols = st.columns(3)
for i, t in enumerate(list(THEMES.keys())):
    with cols[i % 3]:
        if st.button(t, key="top_"+t, use_container_width=True):
            st.session_state.theme = t
            st.rerun()

if st.session_state.theme == "📐 Ecole":
    st.subheader("TOUTES LES MATIERES ECOLE - Clique sur une matière :")
    cols2 = st.columns(4)
    for i, m in enumerate(list(MATIERES.keys())):
        with cols2[i % 4]:
            if st.button(m, key="mat_"+m, use_container_width=True):
                st.session_state.theme = m
                st.rerun()
    st.info("Clique sur une matière pour voir ses questions : Maths, Français, Allemand, Anglais, Histoire, Sciences, Chimie, Code")
else:
    if st.session_state.theme in MATIERES:
        st.subheader(f"Questions {st.session_state.theme} - Clique :")
        for q in MATIERES[st.session_state.theme]:
            if st.button(q, key="q_"+q, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": q})
                st.session_state.auto_q = q
                st.rerun()
        if st.button("Retour à toutes les matières", use_container_width=True):
            st.session_state.theme = "📐 Ecole"
            st.rerun()
    else:
        st.subheader(f"Questions {st.session_state.theme} - Clique :")
        for q in THEMES.get(st.session_state.theme, []):
            if st.button(q, key="q_"+q, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": q})
                st.session_state.auto_q = q
                st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Salut ! Maintenant mes reponses sont beaucoup plus developpees. Pose-moi : Pythagore, Masse volumique, Werenoi, F-22, Meilleur rapport qualite prix PC..."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

CAPITALES = {
    "france": "Paris", "suisse": "Berne", "allemagne": "Berlin", "italie": "Rome", "espagne": "Madrid",
    "angleterre": "Londres", "japon": "Tokyo", "usa": "Washington", "canada": "Ottawa", "chine": "Pekin",
    "russie": "Moscou", "bresil": "Brasilia", "inde": "New Delhi", "australie": "Canberra", "egypte": "Le Caire",
    "maroc": "Rabat", "algerie": "Alger", "tunisie": "Tunis", "portugal": "Lisbonne", "belgique": "Bruxelles",
    "pays-bas": "Amsterdam", "autriche": "Vienne", "suede": "Stockholm", "norvege": "Oslo", "danemark": "Copenhague",
    "finlande": "Helsinki", "pologne": "Varsovie", "grece": "Athenes", "turquie": "Ankara", "coree": "Seoul",
    "thailande": "Bangkok", "vietnam": "Hanoi", "mexique": "Mexico", "argentine": "Buenos Aires", "chili": "Santiago",
    "perou": "Lima", "colombie": "Bogota", "kenya": "Nairobi", "nigeria": "Abuja", "islande": "Reykjavik",
    "irlande": "Dublin", "ukraine": "Kyiv", "roumanie": "Bucarest", "hongrie": "Budapest", "croatie": "Zagreb",
    "serbie": "Belgrade", "bulgarie": "Sofia", "israel": "Jerusalem", "liban": "Beyrouth", "irak": "Bagdad",
    "iran": "Teheran", "arabie": "Riyad", "qatar": "Doha", "【entity-monaco¦canonical_name=AS Monaco】": "【entity-Monaco¦canonical_name=AS Monaco】", "luxembourg": "Luxembourg",
    "malte": "La Valette", "andorre": "Andorre-la-Vieille", "liechtenstein": "Vaduz", "cuba": "La Havane",
    "mali": "Bamako", "senegal": "Dakar", "ghana": "Accra", "cameroun": "Yaounde", "madagascar": "Antananarivo",
    "pakistan": "Islamabad", "nepal": "Katmandou", "mongolie": "Oulan-Bator", "indonesie": "Jakarta",
    "philippines": "Manille", "singapour": "Singapour", "malaisie": "Kuala Lumpur", "nouvelle-zelande": "Wellington",
    "costa rica": "San Jose", "panama": "Panama", "venezuela": "Caracas", "uruguay": "Montevideo",
    "paraguay": "Asuncion", "equateur": "Quito", "bolivie": "Sucre", "haiti": "Port-au-Prince",
    "jamaique": "Kingston", "soudan": "Khartoum", "libye": "Tripoli", "ethiopie": "Addis-Abeba",
}

PC = {
    "rapport qualite prix": """MEILLEUR RAPPORT QUALITE / PRIX PC 2026 - EXPLICATION COMPLETE :

Le rapport qualite / prix, c'est combien de FPS tu as pour chaque franc depense. Un PC a 4000 CHF est plus puissant, mais tu paies 2x plus cher pour seulement 20% de FPS en plus. Donc ce n'est pas rentable.

1. GAGNANT 1300 CHF - LE MEILLEUR :
GPU RTX 5070 (600 CHF) + CPU Ryzen 7 7800X3D (350 CHF) + RAM 32 Go DDR5 (120 CHF) + SSD 1 To (70 CHF) + Carte mere + Alim + Boitier (160 CHF) = 1300 CHF.
Resultat : 1440p Ultra 180 FPS sur Fortnite, 120 FPS sur GTA V, 100 FPS sur Warzone. Tu peux jouer, streamer et coder sans lag.
Pourquoi c'est le meilleur ? Parce que la RTX 5070 est presque aussi forte que la 5080 mais coute 2x moins cher. Et le 7800X3D a le cache 3D qui donne +30 FPS dans les jeux.

2. PETIT BUDGET 900 CHF - POUR DEBUTER :
RTX 4060 (350 CHF) + Ryzen 5 7600 (180 CHF) + 16 Go (60 CHF) + SSD 1 To (70 CHF) + Reste (240 CHF) = 900 CHF.
Resultat : 1080p Ultra 144 FPS 【entity-Fortnite¦canonical_name=Fortnite】, 60 FPS GTA V Ultra. Parfait pour commencer, pour 【entity-Roblox¦canonical_name=Roblox】, 【entity-Minecraft RTX¦canonical_name=Minecraft】, 【entity-Fortnite¦canonical_name=Fortnite】.

3. GROS BUDGET 2000 CHF - LE ROI :
RTX 5070 Ti (850 CHF) + Ryzen 7 9800X3D (450 CHF) + 32 Go (120 CHF) + SSD 2 To (180 CHF) + Reste (400 CHF) = 2000 CHF.
Resultat : 1440p Ultra 240 FPS, 4K 120 FPS. Tu peux tout faire en max.

MON CONSEIL : Prends le 1300 CHF. C'est celui que 90% des gamers prennent en 2026. Tu economises 700 CHF par rapport au 2000 CHF pour presque les memes FPS.""",
    "meilleur rapport": "MEILLEUR RAPPORT QUALITE / PRIX : GAGNANT = PC 1300 CHF : RTX 5070 + Ryzen 7 7800X3D + 32 Go + SSD 1 To = 1300 CHF, 1440p Ultra 180 FPS. C'est celui qui donne le plus de FPS par franc. Le 900 CHF est bien pour debuter, le 2000 CHF est pour ceux qui veulent du 240 FPS en 4K, mais le 1300 CHF est le plus intelligent.",
    "qualite prix": "MEILLEUR RAPPORT : 1300 CHF = RTX 5070 + 7800X3D = meilleur ! 900 CHF = RTX 4060 = pour debuter. 2000 CHF = RTX 5070 Ti = le roi. Le rapport qualite prix, c'est le FPS par franc. Le 1300 CHF gagne.",
    "pc 900": "PC 900 CHF - DETAIL : GPU RTX 4060 (350 CHF) : 8 Go, 1080p Ultra, Fortnite 144 FPS, Minecraft RTX. CPU Ryzen 5 7600 (180 CHF) : 6 coeurs, suffisant pour jouer. RAM 16 Go DDR5 (60 CHF) : minimum pour jouer en 2026. SSD 1 To NVMe (70 CHF) : Windows demarre en 5 sec, jeux chargent vite. Carte mere B650 + Alim 650W + Boitier (240 CHF). Total 900 CHF. Parfait pour debuter, pour Fortnite, Roblox, Minecraft, GTA V en 1080p.",
    "pc 1300": "PC 1300 CHF - DETAIL : GPU RTX 5070 (600 CHF) : 12 Go, 1440p Ultra, 180 FPS Fortnite, Ray Tracing. CPU Ryzen 7 7800X3D (350 CHF) : 8 coeurs + cache 3D, le CPU prefere des gamers, +30 FPS. RAM 32 Go DDR5 6000 MHz (120 CHF) : tu peux jouer + 【entity-Discord¦canonical_name=Discord】 + Chrome + Stream sans lag. SSD 1 To (70 CHF) : rapide. Total 1300 CHF. C'est le meilleur rapport qualite prix en 2026.",
    "pc 2000": "PC 2000 CHF - DETAIL : GPU RTX 5070 Ti (850 CHF) : 16 Go, 4K 120 FPS, 1440p 240 FPS. CPU Ryzen 7 9800X3D (450 CHF) : le CPU gaming le plus rapide du monde en 2026. RAM 32 Go DDR5 (120 CHF). SSD 【entity-Samsung¦canonical_name=Samsung】 990 PRO 2 To (180 CHF) : 7450 Mo/s, le plus rapide. Carte mere B850 (180 CHF), Alim 850W Gold (110 CHF), Boitier (110 CHF). Total 2000 CHF. Pour ceux qui veulent le max, du 240 FPS, du 4K, du streaming pro.",
    "meilleure gpu": """MEILLEURE GPU 2026 - COMPARAISON COMPLETE :

1. RTX 5090 - LA PLUS PUISSANTE DU MONDE : 32 Go VRAM, 4K Ultra 200 FPS, Ray Tracing max, IA. Prix 2500 CHF. Pour qui ? Les pros, les riches, ceux qui font de la 3D / IA. Rapport qualite prix : mauvais, trop chere.

2. RTX 5080 - 2EME : 16 Go, 4K 150 FPS, 1200 CHF. Tres forte, mais encore chere.

3. RTX 5070 Ti - TRES BONNE : 16 Go, 1440p Ultra 200 FPS, 4K 100 FPS, 850 CHF. C'est celle du PC 2000 CHF.

4. RTX 5070 - MEILLEUR RAPPORT : 12 Go, 1440p Ultra 180 FPS, 600 CHF. C'est celle du PC 1300 CHF. C'est celle que je te conseille.

5. RTX 4060 - POUR DEBUTER : 8 Go, 1080p Ultra 144 FPS, 350 CHF. Parfaite pour commencer.

Conclusion : Si tu as 600 CHF pour la GPU, prends la RTX 5070. Si tu as 350 CHF, prends la RTX 4060.""",
    "gpu": "GPU = Carte Graphique. C'est elle qui calcule toutes les images de tes jeux, 60 a 240 fois par seconde. 【entity-NVIDIA¦canonical_name=NVIDIA】 = RTX (les meilleures pour le Ray Tracing et l'IA), 【entity-AMD¦canonical_name=AMD】 = RX (moins cheres). La GPU decide de tes FPS : une RTX 4060 = 144 FPS en 1080p, une RTX 5070 = 180 FPS en 1440p, une RTX 5090 = 200 FPS en 4K. Sans bonne GPU, ton jeu lag meme si tu as un bon CPU.",
    "meilleur cpu": """MEILLEUR CPU 2026 - EXPLICATION :

Le CPU, c'est le cerveau du PC. Il calcule la physique, l'IA des ennemis, les positions.

1. Ryzen 9 9950X3D - LE ROI : 16 coeurs, cache 3D, le plus rapide en jeux + montage video. Prix 700 CHF. Pour les pros.

2. Ryzen 7 9800X3D - LE ROI GAMING : 8 coeurs + cache 3D, le plus rapide en jeux seul. Prix 450 CHF. C'est celui du PC 2000 CHF.

3. Ryzen 7 7800X3D - MEILLEUR RAPPORT : 8 coeurs + cache 3D, presque aussi rapide que le 9800X3D mais 100 CHF moins cher. Prix 350 CHF. C'est celui du PC 1300 CHF. C'est celui que je te conseille.

Le cache 3D, c'est une memoire en plus sur le CPU qui donne +30 FPS dans 【entity-Fortnite¦canonical_name=Fortnite】, 【entity-Minecraft¦canonical_name=Minecraft】, GTA. C'est pour ca que AMD est devant Intel en 2026 pour les jeux.""",
    "cpu": "CPU = Processeur, le cerveau du PC. Il fait les calculs : physique, IA, positions. AMD Ryzen ou Intel Core. En 2026, AMD est devant pour les jeux grace au cache 3D. Meilleur rapport = Ryzen 7 7800X3D (350 CHF). Meilleur absolu = Ryzen 9 9950X3D.",
    "meilleur ssd": "MEILLEUR SSD : 1. 【entity-Samsung¦canonical_name=Samsung】 990 PRO 2 To - 7450 Mo/s, Windows demarre en 5 secondes, jeux chargent en 2 secondes. Prix 180 CHF. C'est le plus rapide. 2. WD Black SN850X 1 To - 7300 Mo/s, 70 CHF, meilleur rapport. 3. Crucial T705 - PCIe 5.0, encore plus rapide mais plus cher. Conseil : prends toujours un SSD NVMe, jamais un vieux disque dur HDD qui met 1 minute a demarrer. 1 To = 100 jeux, 2 To = 200 jeux.",
    "ssd": "SSD = Disque qui stocke Windows + tes jeux. NVMe = le plus rapide, il se branche directement sur la carte mere. HDD = vieux disque qui tourne, lent, a eviter. Avec un SSD, ton PC demarre en 5 sec, sans SSD en 1 minute. 【entity-Samsung¦canonical_name=Samsung】 990 PRO = meilleur, WD Black = meilleur rapport.",
    "meilleure ram": "MEILLEURE RAM : 32 Go DDR5 6000 MHz CL30. C'est le parfait en 2026 : tu peux jouer + 【entity-Discord¦canonical_name=Discord】 + Chrome + Stream sans lag. 16 Go = minimum, ca suffit pour Fortnite seul mais ca lag si tu ouvres 【entity-Discord¦canonical_name=Discord】 + Chrome. 64 Go = pour montage video pro / IA. Marque : Corsair Vengeance, G.Skill Trident Z5. Prends toujours 2 barrettes de 16 Go, pas 1 de 32 Go, c'est 2x plus rapide (dual channel).",
    "ram": "RAM = Memoire vive. Elle stocke ce que ton PC utilise en ce moment : jeu + 【entity-Discord¦canonical_name=Discord】 + Chrome. Si tu n'as pas assez de RAM, ton PC rame. 16 Go = minimum pour jouer. 32 Go DDR5 = parfait en 2026. 64 Go = pro.",
    "meilleur pc": "MEILLEUR PC ABSOLU : RTX 5090 + Ryzen 9 9950X3D + 32 Go DDR5 + SSD 990 PRO 2 To + Alim 1000W = 4000 CHF, tout en 4K Ultra 200 FPS. MEILLEUR RAPPORT = PC 1300 CHF : RTX 5070 + 7800X3D + 32 Go = 1300 CHF, 1440p Ultra 180 FPS. La difference de FPS est petite, la difference de prix est enorme.",
    "pc gamer": "PC GAMER RAPPORT : 900 CHF = RTX 4060 + Ryzen 5 7600 = 144 FPS en 1080p, parfait pour debuter. 1300 CHF = RTX 5070 + 7800X3D = 180 FPS en 1440p, LE MEILLEUR RAPPORT. 2000 CHF = RTX 5070 Ti + 9800X3D = 240 FPS en 1440p / 120 FPS en 4K, le roi.",
    "ecran": "MEILLEUR ECRAN : 27 pouces 1440p 180Hz IPS (250 CHF) = parfait, net, fluide. 1080p 144Hz (150 CHF) = pas cher, bien pour debuter. 4K 240Hz OLED (800 CHF) = le top, couleurs parfaites, mais tres cher. Conseil : prends 1440p 180Hz, c'est le meilleur rapport.",
    "clavier": "MEILLEUR CLAVIER : Mecanique = chaque touche a son propre switch, plus rapide, plus agreable. Switches rouges = silencieux, bleus = clic. Redragon K552 (40 CHF) = mecanique pas cher et tres bon, meilleur rapport. Logitech G Pro X (150 CHF) = meilleur absolu, switches changeables.",
    "souris": "MEILLEURE SOURIS : Logitech G Pro X Superlight 2 - 60g, sans fil, capteur parfait, souris des pros (150 CHF). Meilleur rapport = Logitech G305 (40 CHF) = sans fil, legere, capteur tres bon. Une bonne souris, c'est 60g max, sans fil, capteur 25 000 DPI.",
    "fps": "FPS = Images par seconde. 30 FPS = ca lag, 60 FPS = fluide, 144 FPS = super fluide, 240 FPS = pro. Plus ta GPU est forte, plus tu as de FPS. Pour Fortnite competitif, il faut 144 FPS minimum. Pour jouer chill, 60 FPS suffit.",
}

CHANTEURS = {
    "werenoi": """WERENOI - HISTOIRE COMPLETE :

Vrai nom : 【entity-Jeremy Bana Owona¦canonical_name=Jeremy Bana Owona】. Ne en 1994 a Melun. Il a commence le rap tard, en 2021, avec le son Guadalajara. Il a explose en 2023 avec l'album Pyramide (diamant) et le son Solitaire.

Style : Drill melodique, voix grave, textes sur la rue, la famille, l'argent, la melancolie. Il ne montrait presque jamais son visage au debut, il restait mysterieux.

Albums : Pyramide (2023), Pyramide 2 (2024), Diamant Noir (2025). Il est devenu le rappeur le plus ecoute en France en 2024 et 2025, devant Ninho et Jul.

Sons cultes : Solitaire, Ciao, La vie de luxe, Pyramide, Diamant Noir, Pétrole avec 【entity-Gazo¦canonical_name=Gazo】.

Decede le 17 mai 2025 a 31 ans, d'un arret cardiaque. Toute la France a ete choquee. Il reste une legende du rap francais, meme avec une carriere tres courte (4 ans).""",
    "ninho": """NINHO - HISTOIRE COMPLETE :

Vrai nom : 【entity-William Nzobazola¦canonical_name=William Nzobazola】. Ne en 1996 a Villeneuve-Saint-Georges, grandi a Nemours. Il a commence a 15 ans, avec des freestyles sur YouTube.

Il est le rappeur avec le plus de disques d'or et de diamant en France ! Record absolu. Albums : M.I.L.S (2016), M.I.L.S 2.0, Comme prevu, Destin, Jefe (2021), NI (2023).

Style : Flow melodique, punchlines, il melange trap et melodie. Il est tres fort en feat : Lettre a une femme avec 【entity-Niska¦canonical_name=Niska】 = diamant, Tout en 1 avec 【entity-Niska¦canonical_name=Niska】, Bolide allemand avec SDM.

Sons cultes : Jefe, Lettre a une femme, Tout en 1, Maman ne le sait pas, 【entity-No Love¦canonical_name=No Love】, La vie qu'on mene.

Il a fait Bercy (Accor Arena) plein 2 fois. C'est le boss du rap francais depuis 2018.""",
    "jul": """JUL - HISTOIRE COMPLETE :

Vrai nom : 【entity-Julien Mari¦canonical_name=Julien Mari】. Ne en 1990 a Marseille. Il a commence en 2013 avec le son Sort le cross volé.

C'est le rappeur le plus productif de France : il sort 2 albums par an, parfois 3 ! Il a sorti plus de 20 albums en 10 ans. Albums : Dans ma paranoïa, Je trouve pas le sommeil, La machine, C'est pas des LOL, La zone en personne, Decennie, Mise a jour...

Style : Marseille, autotune, sons pour la voiture, pour l'ete, pour la rue. Il est tres proche de ses fans, il fait des feats avec des jeunes inconnus pour les aider.

Sons cultes : Tchikita, JCVD, Bande organisee (avec SCH, Naps, 【entity-Kofs¦canonical_name=Kofs】...), 1 2 3, J'ai tout su, C'est pas des LOL.

Son signe : la main en l'air. Il a vendu plus de 5 millions d'albums. Il est le rappeur prefere des jeunes en France.""",
    " 【entity-gazo¦canonical_name=Gazo】": """【entity-GAZO¦canonical_name=Gazo】 - HISTOIRE COMPLETE :

Vrai nom : Ibrahima Diakite. Ne en 1994 a Chateau Rouge, Paris. Il a commence avec 【entity-Freeze Corleone¦canonical_name=Freeze Corleone】 dans le groupe 667.

C'est lui qui a ramene la drill en France ! La drill, c'est un style de rap de Chicago / Londres, sombre, avec des basses lourdes. Album : Drill FR (2021), KMT (2022), Apocalypse (2024).

Style : Voix grave, flow drill, textes sombres. Il a collabore avec tout le monde : 【entity-Tiakola¦canonical_name=Tiakola】, Ninho, 【entity-Gims¦canonical_name=Gims】, Hamza...

Sons cultes : Haine et Sex, Die, La Melo avec 【entity-Tiakola¦canonical_name=Tiakola】 (300M de vues !), Apocalypse, Tiki Taka.

Il a fait la premiere partie de la drill francaise et il est devenu le roi de la drill.""",
    " 【entity-tiakola¦canonical_name=Tiakola】": """【entity-TIAKOLA¦canonical_name=Tiakola】 - HISTOIRE COMPLETE :

Vrai nom : 【entity-Tiakola Diakite¦canonical_name=Tiakola】. Ne en 1996 a Bondy, membre du groupe 【entity-4Keus¦canonical_name=4Keus】. Il a commence avec 【entity-4Keus¦canonical_name=4Keus】, puis en solo en 2022.

Album : Melo (2022) - diamant, BDLM (2024). Sa voix melodique est unique, il fait du afro, du melodique, du rap doux.

Sons cultes : La Melo avec 【entity-Gazo¦canonical_name=Gazo】 (tube de l'ete 2023), Gasolina avec Rsko, Meuda avec Ninho, Pona nini, Si j'savais avec Ninho et 【entity-Niska¦canonical_name=Niska】.

Il est tres apprecie pour sa voix, sa douceur, ses melodies. Il a fait Bercy plein. C'est l'un des chanteurs les plus ecoutes en France en 2024.""",
    " 【entity-pnl¦canonical_name=PNL】": """【entity-PNL¦canonical_name=PNL】 - HISTOIRE COMPLETE :

【entity-PNL¦canonical_name=PNL】 = Peace N Lovés. Duo de freres : Ademo (Tarik) et N.O.S (Nabil), de Corbeil-Essonnes, quartier des Tarterêts.

Albums : Le monde Chico (2015), Dans la legende (2016), Deux freres (2019). Ils ne font presque jamais d'interviews, pas de reseaux, pas de feats. Ils restent mysterieux.

Style : Cloud rap, planant, autotune, sons qui te font voyager. Textes sur la famille, la rue, la quete, la vie.

Sons cultes : Le monde ou rien, DA, Naha, Au DD, Deux freres, 91's, Onizuka.

Ils ont fait 2 Bercy pleins sans aucune promo. Ils sont consideres comme le groupe le plus influent du rap francais des annees 2010.""",
    "sdm": """SDM - HISTOIRE COMPLETE :

Vrai nom : Beni Mosabu. Ne en 1995 a Clamart. Il a ete repere par Booba qui l'a signe dans son label 92i.

Albums : Ocho (2021), Liens du 100, A vie (2023), A nos corps (2024). Il a explose avec le son Bolide allemand avec Ninho (diamant).

Style : Flow rapide, technique, punchlines, voix aigue. Il est tres fort en freestyle.

Sons cultes : Bolide allemand, Jack Fuego, La zone, Cartier, Redescends.

Il est considere comme l'un des meilleurs techniciens du rap francais actuel.""",
    " maes": "MAES - HISTOIRE : Rappeur de Sevran. Album : Pure, Les derniers salopards, Omerta. Style : trap melodique, street. Sons cultes : Street, Dybala, Madrina avec Booba. Il a fait de la prison, puis il est revenu plus fort.",
    "sch": """SCH - HISTOIRE : Rappeur de Marseille, vrai nom Julien Schwarzer. Albums : Anarchie, JVLIVS, Autobahn. Style : sombre, technique, univers mafieux. Son culte : Bande organisee avec Jul, Naps, Kofs... = tube de l'ete 2020, 400M de vues. Il a aussi fait Mere, A7, Otto. C'est un des meilleurs techniciens.""",
    "booba": "BOOBA - HISTOIRE : Le Duc de Boulogne, legende du rap francais depuis 1995 avec Lunatic. Albums : Temps mort, Ouest Side, Ultra, Trone. Il a lance Ninho, SDM, Gazo, Damso, Maes... Il est connu pour ses clashs, son label 92i, et ses punchlines. Son son : DKR, Mona Lisa, Ratpi World.",
    "damso": "DAMSO - HISTOIRE : Rappeur belge / congolais. Albums : Batterie Faible, Ipséité, Lithopédion, QALF. Style : sombre, technique, punchlines. Sons cultes : Macarena (diamant), BruxellesVie, Feu de bois. Il a fait une pause, puis il est revenu avec QALF Infinity.",
    " drake": "DRAKE - HISTOIRE : Rappeur canadien, le plus streamé au monde. Albums : Take Care, Nothing Was The Same, Scorpion, Her Loss. Sons cultes : God's Plan, One Dance, Hotline Bling, Started From The Bottom. Il a commence comme acteur dans 【entity-Degrassi¦canonical_name=Degrassi】. Il a son label OVO.",
    " 【entity-taylor swift¦canonical_name=Taylor Swift】": "【entity-TAYLOR SWIFT¦canonical_name=Taylor Swift】 - HISTOIRE : Chanteuse americaine, la plus ecoutee au monde. Albums : 1989, Reputation, Midnights, The Tortured Poets Department. Elle a gagne 14 Grammy. Ses fans = les Swifties. Elle a commence en country, puis pop. Son Eras Tour = tournee la plus rentable de l'histoire (2 milliards $).",
    "weeknd": "【entity-THE WEEKND¦canonical_name=THE WEEKND】 - HISTOIRE : Chanteur canadien, vrai nom 【entity-Abel Tesfaye¦canonical_name=Abel Tesfaye】. Albums : After Hours, Starboy, Dawn FM. Son : Blinding Lights = chanson la plus ecoutee de tous les temps sur Spotify (4 milliards). Il a fait le Super Bowl en 2021.",
    "【entity-eminem¦canonical_name=EMINEM】": "【entity-EMINEM¦canonical_name=EMINEM】 - HISTOIRE : Rappeur americain, legende. Albums : The Slim Shady LP, The Marshall Mathers LP, Recovery. Sons : Lose Yourself (Oscar), Rap God (7 mots par seconde), Mockingbird, Without Me. Il a vendu 220M d'albums. C'est le rappeur le plus vendu de l'histoire.",
    "billie eilish": "BILLIE EILISH - HISTOIRE : Chanteuse americaine, elle a commence a 14 ans avec Ocean Eyes. Albums : When We All Fall Asleep, Happier Than Ever, Hit Me Hard and Soft. Sons : Bad Guy, Birds of a Feather, What Was I Made For (Barbie). Elle a gagne 9 Grammy avant 22 ans.",
    "stromae": "STROMAE - HISTOIRE : Chanteur belge, vrai nom Paul Van Haver. Albums : Cheese, Racine carree, Multitude. Sons : Alors on danse, Papaoutai, Formidable, L'enfer. Il melange electro et chansons tristes sur la famille, la depression, la vie. Il a fait une pause de 7 ans pour sa sante mentale.",
    "soprano": "SOPRANO - HISTOIRE : Chanteur / rappeur de Marseille. Albums : La Colombe, L'Everest, Chasseur d'etoiles. Sons : Cosmo, En feu, A la vie, a l'amour, Mon Everest avec Marina Kaye. Tres positif, famille, espoir. Il a commence dans le groupe Psy 4 de la Rime.",
}

TOUT = {
    "pythagore": """THEOREME DE PYTHAGORE - EXPLICATION COMPLETE :

Formule : a² + b² = c². Ca marche UNIQUEMENT pour un triangle rectangle (avec un angle droit de 90°).

a et b = les 2 petits cotes (qui forment l'angle droit). c = l'hypotenuse, le plus grand cote, en face de l'angle droit.

Exemple : Triangle 3-4-5. 3² + 4² = 9 + 16 = 25. Et 5² = 25. Donc ca marche !

Exemple pour trouver l'hypotenuse : Si a=6, b=8, alors c² = 36 + 64 = 100, donc c = 10.

Exemple pour trouver un petit cote : Si c=13, b=5, alors a² = 169 - 25 = 144, donc a = 12.

A quoi ca sert ? Pour construire une maison, pour savoir si un angle est droit, pour calculer une distance sans mesurer. Les Egyptiens l'utilisaient deja il y a 4000 ans pour les pyramides.""",
    "thales": "THALES - EXPLICATION : Si 2 droites paralleles coupent 2 secantes, alors les rapports sont egaux. Ex : Si tu as un triangle avec une droite parallele a la base, tu peux calculer la longueur sans mesurer. Formule : AB / AD = AC / AE = BC / DE. Ca sert pour les ombres, les hauteurs d'arbres, les pyramides.",
    "moyenne": "MOYENNE - EXPLICATION : Moyenne = somme / nombre. Ex : Notes 12, 15, 18. Somme = 45. Nombre = 3. Moyenne = 45 / 3 = 15. Astuce : Si tu as une mauvaise note, il faut une bonne note pour compenser. Ex : 8 + 18 = 26 / 2 = 13.",
    "aire": "AIRE - EXPLICATION COMPLETE : Aire = surface. Rectangle = Longueur x largeur. Carre = cote x cote. Triangle = (base x hauteur) / 2. Cercle = pi x rayon² (pi = 3,14). Ex : Cercle rayon 5 = 3,14 x 25 = 78,5 cm². Pour un terrain, une chambre, un jardin, tu calcules l'aire.",
    "perimetre": "PERIMETRE - EXPLICATION : Perimetre = tour. Carre = 4 x cote. Rectangle = 2 x (Longueur + largeur). Cercle = 2 x pi x rayon. Ex : Carre 5 cm = 20 cm de tour. Ca sert pour une cloture, un cadre.",
    "volume": "VOLUME - EXPLICATION : Volume = place que ca prend. Cube = cote³. Pave = Longueur x largeur x hauteur. Cylindre = pi x rayon² x hauteur. Ex : Boite 2x3x4 = 24 cm³. Ca sert pour une piscine, un carton, une bouteille.",
    "fraction": "FRACTION - EXPLICATION : Fraction = part d'un tout. 1/2 = la moitie, 1/4 = le quart. Pour additionner : il faut le meme denominateur. 1/2 + 1/4 = 2/4 + 1/4 = 3/4. Pour comparer : 1/2 > 1/3 car 1/2 = 3/6, 1/3 = 2/6.",
    "pourcentage": "POURCENTAGE - EXPLICATION : Pourcentage = pour 100. Formule : (partie / total) x 100. Ex : 20% de 50 = 0,20 x 50 = 10. Ex : Tu as 15/20 en controle : (15/20) x 100 = 75%. Les soldes : -30% sur 100 CHF = 70 CHF.",
    "equation": "EQUATION - EXPLICATION : Equation = egalite avec un x a trouver. Methode : tu mets les x d'un cote, les chiffres de l'autre. Ex : 2x + 3 = 7. Tu enleves 3 des 2 cotes : 2x = 4. Tu divises par 2 : x = 2. Verif : 2x2+3 = 7, ca marche !",
    "angle": "ANGLES - EXPLICATION : Droit = 90°, Plat = 180°, Plein = 360°. Triangle = 180° au total. Ex : Si un triangle a 90° et 60°, le 3eme = 180 - 90 - 60 = 30°. Angles complementaires = 90° a 2. Angles supplementaires = 180° a 2.",
    "etre": "ETRE - CONJUGAISON COMPLETE : Present : je suis, tu es, il est, nous sommes, vous etes, ils sont. Passe compose : j'ai ete, tu as ete... Imparfait : j'etais, tu etais, il etait... Futur : je serai, tu seras, il sera... Ex : Je suis a l'ecole, Je suis content.",
    "avoir": "AVOIR - CONJUGAISON : Present : j'ai, tu as, il a, nous avons, vous avez, ils ont. Passe compose : j'ai eu. Imparfait : j'avais. Futur : j'aurai. Ex : J'ai 13 ans, J'ai un chien.",
    "aller": "ALLER - CONJUGAISON : Present : je vais, tu vas, il va, nous allons, vous allez, ils vont. Passe compose : je suis alle. Futur : j'irai. Ex : Je vais a l'ecole, Je vais au foot.",
    "faire": "FAIRE - CONJUGAISON : Present : je fais, tu fais, il fait, nous faisons, vous faites, ils font. Passe compose : j'ai fait. Futur : je ferai. Ex : Je fais mes devoirs, Je fais du foot.",
    "pluriel": "PLURIEL - REGLES : En general +s : chat -> chats. En -eau : bateau -> bateaux. En -al : cheval -> chevaux, journal -> journaux. En -ou : genou -> genoux, caillou -> cailloux, mais trou -> trous. Exceptions a apprendre par coeur.",
    "adjectif": "ADJECTIF - EXPLICATION : L'adjectif decrit un nom, il s'accorde en genre et nombre. Ex : grand garcon / grande fille / grands garcons / grandes filles. Beau -> belle, blanc -> blanche, nouveau -> nouvelle. Il se place avant ou apres le nom : un grand garcon, un garcon sympa.",
    "passe compose": "PASSE COMPOSE - EXPLICATION : Formule : avoir/etre au present + participe passe. Ex : J'ai mange, Je suis alle, Tu as joue, Nous avons fini. Avec etre (aller, venir, partir, arriver...) : Je suis alle, Elle est venue. Participe : mange, fini, pris, vu, bu, dit...",
    "imparfait": "IMPARFAIT - EXPLICATION : Pour une habitude, une description, une action longue dans le passe. Terminaisons : -ais, -ais, -ait, -ions, -iez, -aient. Ex : Quand j'etais petit, je jouais au foot. Il faisait beau. Je dormais. Contraire du passe compose qui est pour une action courte : Hier, j'ai joue au foot (passe compose, une fois).",
    "futur": "FUTUR - EXPLICATION : Pour parler de demain. Terminaisons : -ai, -as, -a, -ons, -ez, -ont. Ex : Je mangerai, tu mangeras, il mangera, nous mangerons... Pour -er : je parlerai. Pour -ir : je finirai. Pour irreguliers : je serai (etre), j'aurai (avoir), j'irai (aller).",
    "der": "ALLEMAND - DER DIE DAS : der = masculin (der Mann = l'homme), die = feminin (die Frau = la femme), das = neutre (das Kind = l'enfant). Pluriel = die (die Kinder = les enfants). Il faut apprendre le genre par coeur avec chaque mot. Astuce : -chen = das (das Mädchen).",
    "sein": "SEIN (ETRE) - ALLEMAND : ich bin, du bist, er/sie/es ist, wir sind, ihr seid, sie sind. Ex : Ich bin 13 Jahre alt = J'ai 13 ans. Ich bin müde = Je suis fatigué.",
    "to be": "TO BE - ANGLAIS : I am, You are, He/She/It is, We are, You are, They are. Ex : I am 13, He is happy, They are friends. Passe : I was, You were. Futur : I will be.",
    "photosynthese": """PHOTOSYNTHESE - EXPLICATION COMPLETE :

Formule : Soleil + Eau + CO2 = Oxygene + Sucre (glucose).

Comment ? Les feuilles ont de la chlorophylle (pigment vert) qui capte la lumiere du Soleil. Les racines prennent l'eau dans le sol. Les feuilles prennent le CO2 dans l'air.

Resultat : La plante fabrique son sucre pour grandir, et elle rejette de l'oxygene qu'on respire !

Pourquoi c'est important ? Sans photosynthese, pas d'oxygene, pas de vie sur Terre. C'est les plantes, les arbres, les algues qui font tout notre oxygene. C'est pour ca qu'il faut proteger les forets.""",
    "planete": "PLANETES - EXPLICATION : 8 planetes : Mercure (la plus proche du Soleil, tres chaude), Venus (la plus chaude, 460°), Terre (la seule avec vie), Mars (rouge), Jupiter (la plus grosse, 1300x Terre), Saturne (anneaux), Uranus (bleue, couchee), Neptune (la plus loin, vent 2000 km/h). Pluton = planete naine depuis 2006. Astuce : Me Voici, Tout Mouillé, J'ai Suivi Un Nuage.",
    "gravite": "GRAVITE - EXPLICATION : La gravite nous attire vers la Terre. C'est Newton qui l'a decouverte en voyant une pomme tomber. Sur Terre, tout tombe a 9,81 m/s². Sur la Lune, tu es 6x plus leger car la Lune est plus petite. Sans gravite, on flotterait dans l'espace. C'est la gravite qui fait tourner la Lune autour de la Terre, et la Terre autour du Soleil.",
    "ciel bleu": "CIEL BLEU - EXPLICATION : La lumiere du Soleil est blanche, mais elle est composee de toutes les couleurs. L'air diffuse surtout le bleu (c'est la diffusion de Rayleigh). Donc on voit le ciel bleu. Le soir, le Soleil est bas, la lumiere traverse plus d'air, le bleu est deja parti, il ne reste que le rouge/orange, donc coucher de soleil rouge.",
    "coeur": "COEUR - EXPLICATION : Le coeur pompe le sang dans tout le corps. 100 000 battements par jour, 7 000 litres de sang par jour, 3 milliards de battements dans une vie ! Il a 4 parties : 2 oreillettes, 2 ventricules. Le sang rouge = avec oxygene, le sang bleu = sans oxygene. Sport = coeur plus fort.",
    "volcan": "VOLCAN - EXPLICATION : Un volcan, c'est une ouverture dans la Terre par ou sort du magma (roche fondue). Quand le magma sort, ca devient de la lave. Il y a 2 types : effusif (lave qui coule doucement, comme en Hawai) et explosif (ca explose, comme le Vesuve). Le plus actif d'Europe = Etna en Italie. Le plus dangereux = Yellowstone aux USA.",
    "saison": "SAISONS - EXPLICATION : Les saisons, ce n'est pas la distance au Soleil, c'est l'inclinaison de la Terre (23,5°). En ete, l'hemisphere Nord est penche vers le Soleil, donc jours longs, chaud. En hiver, il est penche loin, donc jours courts, froid. En Australie, c'est l'inverse ! Quand c'est l'ete chez nous, c'est l'hiver chez eux.",
    "foudre": "FOUDRE - EXPLICATION : La foudre, c'est une decharge electrique entre un nuage et le sol. Temperature : 30 000°C, 5x plus chaud que le Soleil ! Elle tombe quand le nuage est tres charge. Regle de securite : si tu entends le tonnerre, rentre. Pas sous un arbre, pas dans l'eau, pas pres d'un poteau. Compte les secondes entre eclair et tonnerre : 3 secondes = 1 km.",
    "continent": "CONTINENTS - EXPLICATION : 6 continents : Europe (44 pays), Afrique (54 pays, le plus chaud), Asie (le plus grand, 4,7 milliards d'habitants), Amerique (Nord + Sud), Oceanie (Australie + iles), Antarctique (glace, pas d'habitants, que des scientifiques). Il y a 195 pays dans le monde.",
    "ocean": "OCEANS - EXPLICATION : 5 oceans : Pacifique (le plus grand, 165M km²), Atlantique, Indien, Arctique (glace), Antarctique. L'ocean le plus profond = fosse des Mariannes, 11 km de profond, dans le Pacifique. On connait mieux la Lune que le fond des oceans !",
    "masse volumique": """MASSE VOLUMIQUE - COURS COMPLET :

Formule : masse volumique = masse / volume. On ecrit : Rho = m / V. Rho = lettre grecque rho.

m = masse, en grammes (g) ou kg. Tu la mesures avec une balance.
V = volume, en cm³ ou mL ou L. Tu le mesures avec une eprouvette graduee ou avec Longueur x largeur x hauteur pour un cube.

Unites : g/cm³ ou kg/m³. 1 g/cm³ = 1000 kg/m³.

Exemples :
- Eau = 1 g/cm³. 100g d'eau dans 100 cm³ = 100 / 100 = 1.
- Huile = 0,9 g/cm³. Elle flotte sur l'eau car 0,9 < 1.
- Fer = 7,8 g/cm³. Il coule car 7,8 > 1.
- Or = 19,3 g/cm³. Tres lourd !

Regle : Si masse volumique < 1, ca flotte. Si > 1, ca coule. C'est pour ca que le bois flotte (0,6) et le caillou coule (2,5).

Exercice : Tu as un objet de 200g et 50 cm³. Masse volumique = 200 / 50 = 4 g/cm³. Il coule.

Pour le controle : Apprends la formule, les unites, et 3 exemples (eau, huile, fer).""",
    "densite": "DENSITE / MASSE VOLUMIQUE : Rho = m / V. Masse / Volume. Ex : 100g / 100 cm³ = 1 g/cm³ = eau. Huile 0,9 flotte, Fer 7,8 coule. Si < 1 ca flotte, si > 1 ca coule. C'est la meme chose que masse volumique, juste un autre nom.",
    "chimie": "CHIMIE - EXPLICATION : La chimie, c'est l'etude de la matiere. Atome = brique de base. Molecule = plusieurs atomes ensemble. H2O = eau (2 hydrogene + 1 oxygene). CO2 = dioxyde de carbone (1 carbone + 2 oxygene). O2 = oxygene qu'on respire. Tableau periodique = 118 elements : H, O, C, Fe (fer), Au (or)...",
    "atome": "ATOME - EXPLICATION : L'atome, c'est la plus petite brique de la matiere. Il a un noyau avec des protons (+) et des neutrons (0), et autour des electrons (-) qui tournent. Ex : Atome d'hydrogene = 1 proton + 1 electron. Atome d'oxygene = 8 protons + 8 electrons. Tout ce que tu vois est fait d'atomes !",
    "oxygene": "OXYGENE - EXPLICATION : O2. On respire O2, on rejette CO2. Sans oxygene, on meurt en 3 minutes. L'oxygene vient des plantes (photosynthese) et des algues dans l'ocean. 21% de l'air = oxygene, 78% = azote. Dans l'espace, pas d'oxygene, il faut une bouteille.",
    "trou noir": """TROU NOIR - EXPLICATION COMPLETE :

Un trou noir, c'est un objet tellement lourd et tellement petit que meme la lumiere ne peut pas en sortir. Sa gravite est tellement forte qu'elle aspire tout.

Comment ca se forme ? Quand une tres grosse etoile meurt, elle explose (supernova) puis elle s'ecrase sur elle-meme. Elle devient tellement dense que sa gravite devient infinie.

Au centre de notre galaxie (Voie Lactee), il y a un trou noir super massif : Sagittarius A*, 4 millions de fois la masse du Soleil.

Si tu tombes dans un trou noir, tu es etire comme un spaghetti (spaghettification) puis tu disparais. Personne ne sait ce qu'il y a dedans.

En 2019, on a pris la premiere photo d'un trou noir (M87) avec un telescope geant.""",
    "soleil": "SOLEIL - EXPLICATION : Le Soleil est une etoile, pas une planete. Temperature au centre : 15 millions de degres, a la surface : 5500°. Il est compose d'hydrogene et d'helium. Il nous donne lumiere et chaleur. Il va mourir dans 5 milliards d'annees en devenant une geante rouge, puis une naine blanche. Sans Soleil, pas de vie.",
    "galaxie": "GALAXIE - EXPLICATION : Une galaxie, c'est un groupe de milliards d'etoiles. Notre galaxie = Voie Lactee, 200 milliards d'etoiles, 100 000 annees-lumiere de diametre. La voisine = Andromede, 2,5 millions d'annees-lumiere, elle va nous percuter dans 5 milliards d'annees. Il y a 200 milliards de galaxies dans l'univers !",
    "big bang": "BIG BANG - EXPLICATION : Le Big Bang, c'est le debut de l'univers il y a 13,8 milliards d'annees. Tout etait concentre en un point minuscule, puis ca a explose et ca s'etend encore aujourd'hui. Au debut, il faisait des milliards de degres. Puis ca a refroidi, les atomes se sont formes, puis les etoiles, puis les galaxies, puis la Terre il y a 4,5 milliards d'annees.",
    "mars": "MARS - EXPLICATION : Mars = planete rouge, a cause du fer oxyde (rouille). Un jour sur Mars = 24h37, presque comme nous. Une annee = 687 jours. Temperature : -60° en moyenne. On y a envoye des robots : Perseverance, 【entity-Curiosity¦canonical_name=Curiosity】. Un jour, des humains iront. 【entity-Elon Musk¦canonical_name=Elon Musk】 veut y aller avec 【entity-SpaceX¦canonical_name=SpaceX】.",
    "iss": "ISS - EXPLICATION : ISS = Station Spatiale Internationale. Elle tourne autour de la Terre a 400 km d'altitude, a 28 000 km/h (tour de Terre en 90 min). 16 levers de soleil par jour ! Il y a 6 astronautes dedans en permanence. Ils font des experiences, ils cultivent des plantes, ils font du sport 2h par jour pour ne pas perdre leurs muscles.",
    "dinosaure": "DINOSAURES - EXPLICATION : Les dinosaures ont vecu il y a 230M a 66M d'annees. T-Rex = carnivore, 12m, dents de 15 cm. Diplodocus = herbivore, 25m, 30 tonnes. Ils ont disparu il y a 66M d'annees a cause d'une meteorite de 10 km qui a frappe le Mexique (Chicxulub). Les oiseaux sont les descendants des dinosaures !",
    "boucle": "BOUCLE - EXPLICATION : Une boucle, c'est pour repeter sans recopier. Ex : for i in range(1,6): print(i) -> affiche 1,2,3,4,5. Sans boucle, il faudrait ecrire 5 print. Avec boucle, 2 lignes. Ca sert pour les jeux, les tables, les listes.",
    "condition": "CONDITION - EXPLICATION : Une condition, c'est si... sinon... Ex : if age >= 18: print('Majeur') else: print('Mineur'). Si la condition est vraie, on fait la 1ere action, sinon la 2eme. Ca sert pour les jeux : si tu as 100 points, tu gagnes.",
    "variable": "VARIABLE - EXPLICATION : Une variable, c'est une boite qui stocke une valeur. Ex : age = 13, prenom = 'Lenny', note = 15. Tu peux la changer : age = 14. Ca sert pour tout en code.",
    " 【entity-messi¦canonical_name=Messi】": """【entity-MESSI¦canonical_name=Messi】 - HISTOIRE COMPLETE :

【entity-Lionel Messi¦canonical_name=Lionel Messi】, ne en 1987 a Rosario, Argentine. Il a commence au 【entity-FC Barcelone¦canonical_name=FC Barcelone】 a 13 ans, apres que le club ait paye son traitement pour grandir (il ne grandissait pas).

Carriere : Barcelone (2004-2021) : 672 buts, 35 trophees, dont 10 Liga, 4 Ligues des Champions. 【entity-PSG¦canonical_name=PSG】 (2021-2023). 【entity-Inter Miami¦canonical_name=Inter Miami】 (2023-...).

Records : 8 Ballons d'Or (record), 91 buts en une annee civile (2012, record), 6 Souliers d'Or, 1 Coupe du Monde 2022 avec l'Argentine (enfin !).

Style : Petit (1m70), gaucher, dribbles courts, vision incroyable, passes decisives, coups francs. Il est considere comme le meilleur joueur de tous les temps par beaucoup.

Vie : Marié a Antonela, 3 enfants. Il est tres discret, pas de clash.""",
    " 【entity-ronaldo¦canonical_name=Ronaldo】": """CRISTIANO 【entity-RONALDO¦canonical_name=Ronaldo】 - HISTOIRE COMPLETE :

【entity-Cristiano Ronaldo¦canonical_name=Cristiano Ronaldo】, ne en 1985 a Madere, Portugal. Il a commence au 【entity-Sporting¦canonical_name=Sporting CP】, puis 【entity-Manchester United¦canonical_name=Manchester United】, 【entity-Real Madrid¦canonical_name=Real Madrid】, 【entity-Juventus¦canonical_name=Juventus】, 【entity-Al-Nassr¦canonical_name=Al-Nassr】.

Records : 5 Ballons d'Or, meilleur buteur de l'histoire en selection (130 buts avec le Portugal), meilleur buteur de l'histoire de la Ligue des Champions (140 buts), 900 buts en carriere.

Style : Grand (1m87), physique, vitesse, saut incroyable (2,93m de saut !), frappe puissante, coups francs, penaltys. Il est une machine a travailler.

Il a gagne l'Euro 2016 avec le Portugal. Il est tres populaire sur Instagram (600M de followers, le plus suivi au monde).""",
    " mbappe": """MBAPPE - HISTOIRE COMPLETE :

【entity-Kylian Mbappe¦canonical_name=Kylian Mbappe】, ne en 1998 a Bondy, France. Il a commence a 【entity-Monaco¦canonical_name=AS Monaco】, puis 【entity-PSG¦canonical_name=PSG】, puis 【entity-Real Madrid¦canonical_name=Real Madrid】 en 2024.

Records : Champion du Monde 2018 a 19 ans (il a marque en finale), meilleur buteur de la Coupe du Monde 2022 (8 buts, triplé en finale contre l'Argentine), meilleur buteur de l'histoire du PSG (256 buts).

Style : Vitesse incroyable (36 km/h, le plus rapide du foot), dribbles, finition. Il est droitier mais joue a gauche pour rentrer et tirer.

Il est le capitaine de l'equipe de France depuis 2023. Il veut gagner le Ballon d'Or et la Ligue des Champions avec le Real.""",
    "ballon d'or": "BALLON D'OR - EXPLICATION : Trophee du meilleur joueur du monde chaque annee, vote par des journalistes. Cree en 1956. 【entity-Messi¦canonical_name=Messi】 en a 8 (record), 【entity-Ronaldo¦canonical_name=Ronaldo】 5, 【entity-Cruyff¦canonical_name=Cruyff】 3, Platini 3, 【entity-Van Basten¦canonical_name=Marco van Basten】 3. En 2024, c'est Rodri qui a gagne. En 2023, c'est 【entity-Messi¦canonical_name=Messi】.",
    "coupe du monde": "COUPE DU MONDE - EXPLICATION : Competition tous les 4 ans, 32 equipes avant, 48 equipes en 2026 (USA / Canada / Mexique). 2022 = Argentine gagne contre France en finale (3-3, tirs au but). 2018 = France gagne. 2014 = Allemagne. Le Bresil a gagne 5 fois, record. La prochaine : 2026, 104 matchs, 16 villes.",
    " minecraft": """【entity-MINECRAFT¦canonical_name=Minecraft】 - EXPLICATION COMPLETE :

【entity-Minecraft¦canonical_name=Minecraft】, cree par Notch (Markus Persson) en 2011, rachete par 【entity-Microsoft¦canonical_name=Microsoft】 en 2014 pour 2,5 milliards $.

C'est le jeu le plus vendu au monde : 300M de copies ! Principe : monde infini en cubes, tu mines (tu casses des blocs), tu construis, tu survis.

Modes : Survie (tu as faim, tu as des coeurs, les monstres t'attaquent la nuit : creeper, zombie, squelette, enderman), Creatif (tu as tout illimite, tu voles), Aventure, Spectateur.

Mobs : Creeper (il explose, BOOM), Enderman (il se teleporte), Ender Dragon (boss final dans l'End), Wither.

Pourquoi c'est genial ? Tu peux tout construire : maison, chateau, ville, ordinateur, meme un autre jeu dedans ! C'est utilise a l'ecole pour apprendre a coder (【entity-Minecraft Education¦canonical_name=Minecraft】).""",
    " 【entity-fortnite¦canonical_name=Fortnite】": """【entity-FORTNITE¦canonical_name=Fortnite】 - EXPLICATION COMPLETE :

【entity-Fortnite¦canonical_name=Fortnite】, cree par 【entity-Epic Games¦canonical_name=Epic Games】 en 2017. Battle Royale : 100 joueurs sur une ile, le dernier vivant gagne.

Modes : Battle Royale (avec construction), Zero Construction (sans construction, plus facile), Sauver le monde, 【entity-Lego Fortnite¦canonical_name=Lego Fortnite】, Rocket Racing, Festival (musique).

Principe : Tu tombes en parachute, tu ramasses des armes (gris, vert, bleu, violet, orange = du moins fort au plus fort), tu construis des murs, tu te bats, la zone se retrecit.

Skins : 2000+ skins, dont des collabs : 【entity-Marvel¦canonical_name=Marvel】, 【entity-Star Wars¦canonical_name=Star Wars】, Dragon Ball, Naruto, 【entity-Messi¦canonical_name=Messi】, 【entity-Neymar¦canonical_name=Neymar】, 【entity-Ariana Grande¦canonical_name=Ariana Grande】...

Esport : 【entity-Fortnite¦canonical_name=Fortnite】 World Cup 2019, 【entity-Bugha¦canonical_name=Bugha】 a gagne 3M $ a 16 ans ! C'est le jeu le plus joue par les jeunes en France.""",
    " 【entity-roblox¦canonical_name=Roblox】": "【entity-ROBLOX¦canonical_name=Roblox】 - EXPLICATION : 【entity-Roblox¦canonical_name=Roblox】, c'est pas un jeu, c'est une plateforme avec des millions de jeux crees par les joueurs. Cree en 2006. Jeux cultes : Brookhaven (tu vis une vie), Blox Fruits (tu deviens pirate), Pet Simulator, Doors, Murder Mystery 2. Tu peux creer ton propre jeu avec 【entity-Roblox¦canonical_name=Roblox】 Studio et gagner des Robux (monnaie). 300M de joueurs par mois, surtout des jeunes.",
    "gta": "GTA V - EXPLICATION : 【entity-Grand Theft Auto V¦canonical_name=Grand Theft Auto V】, sorti en 2013, 190M de copies, 2eme jeu le plus vendu de l'histoire (apres 【entity-Minecraft¦canonical_name=Minecraft】). Monde ouvert : Los Santos (Los Angeles). 3 personnages : Michael, Franklin, Trevor. Tu conduis, tu fais des missions, tu peux tout faire. GTA VI sort en 2026, a Vice City (Miami), avec Lucia et Jason. C'est le jeu le plus attendu de tous les temps.",
    "tour eiffel": """TOUR EIFFEL - EXPLICATION COMPLETE :

A Paris, 330 metres (avec antenne), construite en 1889 par Gustave Eiffel pour l'Exposition Universelle. Au debut, les Parisiens la detestaient, ils voulaient la demolir ! Elle devait rester que 20 ans.

Elle a 3 etages : 1er a 57m (resto), 2eme a 115m (vue), 3eme a 276m (vue panoramique). 10 100 tonnes de fer, 2,5 millions de rivets.

Anecdotes : Elle grandit de 15 cm en ete (le fer se dilate avec la chaleur), elle est repeinte tous les 7 ans (60 tonnes de peinture), elle scintille la nuit avec 20 000 ampoules.

C'est le monument le plus visite au monde : 7M de visiteurs par an. Symbole de la France.""",
    "pyramide": "PYRAMIDES - EXPLICATION : En Egypte, construites il y a 4500 ans pour les Pharaons (rois). La plus grande = Kheops, 146m, 2,3 millions de blocs de pierre de 2,5 tonnes chacun ! Comment ils ont fait sans grues ? Avec des rampes, des cordes, 20 000 ouvriers pendant 20 ans. Dedans : chambres, couloirs, tresors. Les pyramides etaient blanches et brillantes au debut !",
    " 【entity-titanic¦canonical_name=Titanic】": """【entity-TITANIC¦canonical_name=Titanic】 - HISTOIRE COMPLETE :

Le 【entity-Titanic¦canonical_name=Titanic】, paquebot anglais, le plus grand du monde en 1912. 269m, 46 000 tonnes, 2200 passagers. Il devait etre insubmersible.

Le 14 avril 1912, il heurte un iceberg dans l'Atlantique Nord, a 23h40. Il coule en 2h40, a 2h20 le 15 avril. 1517 morts, 706 survivants. Pas assez de canots de sauvetage (20 pour 2200 personnes).

Film 【entity-Titanic¦canonical_name=Titanic】 en 1997 avec 【entity-Leonardo DiCaprio¦canonical_name=Leonardo DiCaprio】 et Kate Winslet, 11 【entity-Oscars¦canonical_name=Oscars】, 2 milliards $ de recettes. C'est le film d'amour le plus connu.

L'epave a ete retrouvee en 1985 a 3800m de profondeur. Elle est en train de disparaitre a cause des bacteries.""",
    " harry potter": "HARRY POTTER - EXPLICATION : Sorcier avec une cicatrice en eclair, ecrit par J.K. Rowling. 7 livres, 8 films, 500M de livres vendus. Histoire : Harry, orphelin, decouvre qu'il est sorcier a 11 ans, il va a Poudlard, il se bat contre Voldemort. Maisons : Gryffondor, Serpentard, Poufsouffle, Serdaigle. Personnages : Hermione, Ron, Dumbledore, Hagrid, Rogue.",
}

AVIONS = {
    "f-22": """F-22 RAPTOR - EXPLICATION COMPLETE :

Pays : USA. Premier vol : 1997. Prix : 150M $ par avion. Nombre : 195 exemplaires seulement, jamais vendu a d'autres pays, trop secret !

Vitesse : Mach 2.25 (2400 km/h). Plafond : 20 000m. Furtif : presque invisible au radar, grace a sa forme et sa peinture speciale.

Pourquoi c'est le plus performant en combat ? 1. Furtif : l'ennemi ne le voit pas. 2. Super maniable : il peut tourner a 60° par seconde, faire des cobra. 3. Super croisiere : il vole a Mach 1,5 sans postcombustion (il economise du carburant). 4. Capteurs : il voit l'ennemi a 200 km.

En dogfight (combat rapproche), il n'a jamais ete battu en exercice. Contre le F-35, il gagne 90% du temps en combat aerien pur.""",
    " f-35": """F-35 LIGHTNING II - EXPLICATION COMPLETE :

Pays : USA. Premier vol : 2006. Prix : 80M $. Nombre : 1000+ exemplaires, vendu a 20 pays, dont la Suisse (36 exemplaires pour 6 milliards CHF) !

Vitesse : Mach 1.6 (1900 km/h). Furtif, mais moins que le F-22. Son point fort : ses capteurs et son informatique. Il voit tout a 360°, il partage les infos avec les autres avions.

Il existe en 3 versions : F-35A (classique, pour l'armee de l'air), F-35B (il peut decoller verticalement, comme un helicoptere, pour les porte-avions), F-35C (pour les porte-avions, ailes plus grandes).

Role : Attaque au sol, reconnaissance, furtif, guerre electronique. C'est l'avion le plus moderne, le plus intelligent. C'est celui que la Suisse a choisi en 2021.""",
    "su-57": "SU-57 FELON - EXPLICATION : Chasseur furtif russe, premier vol 2010. Vitesse Mach 2.0. Tres maniable, il peut faire le cobra (nez en l'air a 120°). Mais peu produit : 30 exemplaires seulement, car trop cher pour la Russie. Il est moins furtif que le F-22 / F-35.",
    "j-20": "J-20 MIGHTY DRAGON - EXPLICATION : Chasseur furtif chinois, premier vol 2011. Vitesse Mach 2.0. Gros, furtif, pour attaquer de loin avec des missiles longue portee. La Chine en a 200+. Il est moins maniable que le F-22, mais il est bon pour attaquer les avions ravitailleurs et les AWACS.",
    "rafale": """RAFALE - EXPLICATION COMPLETE :

Pays : France, par 【entity-Dassault Aviation¦canonical_name=Dassault Aviation】. Premier vol : 1986, en service depuis 2001. Prix : 100M €.

Vitesse : Mach 1.8 (1900 km/h). Polyvalent : il peut tout faire : combat aerien, attaque au sol, attaque en mer, reconnaissance, dissuasion nucleaire (il peut larguer une bombe nucleaire).

Pays utilisateurs : France, Inde (36), Grece, Croatie, Egypte, Qatar, Emirats, Indonesie...

Pourquoi il est aime ? Parce qu'il est tres maniable, tres fiable, et il peut decoller d'un porte-avions (Charles de Gaulle). C'est le meilleur avion polyvalent europeen. En exercice contre le F-22, il a deja reussi a le verrouiller (a le viser) une fois, ce qui est un exploit.""",
    "eurofighter": "EUROFIGHTER TYPHOON - EXPLICATION : Construit par Allemagne, UK, Italie, Espagne. Vitesse Mach 2.0. Tres rapide en combat aerien, tres maniable. Il est moins furtif que le F-35, mais il est plus rapide. Utilise par 9 pays.",
    "f-16": "F-16 FIGHTING FALCON - EXPLICATION : Le chasseur le plus produit au monde : 4600 exemplaires ! Vitesse Mach 2.0. Petit, agile, pas cher (30M $). Utilise par 25 pays, dont la Belgique, les Pays-Bas, l'Ukraine. Il a 50 ans mais il est encore utilise car il est fiable et facile a entretenir.",
    "f-15": "F-15 EAGLE - EXPLICATION : Vitesse Mach 2.5 ! 104 victoires a 0 defaite en combat reel, legende ! C'est le seul avion avec un ratio parfait. Il a ete utilise par les USA, Israel, Japon, Arabie Saoudite. Il peut porter 10 tonnes de missiles.",
    "f-18": "F/A-18 HORNET - EXPLICATION : Avion embarque sur porte-avions. Vitesse Mach 1.8. La Suisse l'utilise aussi (30 F/A-18 Hornet suisses, achetes en 1996). Il va etre remplace par le F-35 en Suisse des 2028. Il peut atterrir sur un porte-avions avec un crochet.",
    "gripen": "GRIPEN - EXPLICATION : Suede. Vitesse Mach 2.0. Petit, pas cher (50M $), peut atterrir sur une autoroute ! La Suede l'a concu pour la guerre : si les aeroports sont detruits, il peut decoller d'une route. Il est utilise par la Suede, le Bresil, l'Afrique du Sud.",
    "su-35": "SU-35 - EXPLICATION : Russie. Vitesse Mach 2.25. Super maniable, il peut faire le cobra (nez en l'air a 120°) et le kulbit (looping complet). Il est tres impressionnant en meeting aerien. Mais il n'est pas furtif.",
    "mig-29": "MiG-29 - EXPLICATION : Russie. Vitesse Mach 2.25. Rival du F-16 pendant la Guerre Froide (USA vs URSS). Il est encore utilise par 20 pays, dont l'Inde, l'Ukraine.",
    "a-10": "A-10 WARTHOG - EXPLICATION : USA. Vitesse lente, 700 km/h, mais avec un canon geant de 30mm qui tire 3900 balles par minute et detruit les tanks ! Surnom : le sanglier, car il est moche mais tres efficace. Il vole bas, il est blinde, il peut rentrer avec une aile cassee.",
    "sr-71": "SR-71 BLACKBIRD - EXPLICATION : USA. Vitesse Mach 3.3 = 3500 km/h ! L'avion le plus rapide de tous les temps. Aucun missile ne l'a jamais touche. Il volait a 25 000m, tellement haut que les pilotes voyaient la courbure de la Terre. Il etait utilise pour espionner l'URSS. Retire en 1998.",
    "a380": "【entity-AIRBUS¦canonical_name=AIRBUS】 A380 - EXPLICATION : Le plus gros avion de passagers. 2 etages, 850 passagers max ! Longueur 73m, envergure 80m. 【entity-Emirates¦canonical_name=Emirates】 en a le plus (116). Il a 4 moteurs. Il a arrete d'etre produit en 2021 car trop gros, trop cher en carburant. Mais il est encore utilise pour les gros vols (Dubai - Londres).",
    "concorde": "CONCORDE - EXPLICATION : Avion supersonique ! Paris-New York en 3h30 au lieu de 8h. Mach 2 = 2x vitesse du son (2150 km/h). Il volait a 18 000m. Billet : 10 000 € aller-retour ! Arrete en 2003 apres le crash de Gonesse en 2000 et le 11 septembre. C'etait le seul avion de ligne supersonique avec le Tupolev Tu-144 russe.",
    "comment vole": "COMMENT VOLE UN AVION ? - EXPLICATION : L'aile est courbee en haut, plate en bas. L'air va plus vite au-dessus, donc pression plus faible au-dessus, pression plus forte en dessous. Ca cree une force vers le haut = portance. C'est le principe de Bernoulli. Pour decoller, il faut aller vite (250 km/h pour un A380). Pour atterrir, on sort les volets pour augmenter la portance a basse vitesse.",
    "pilote": "PILOTE - EXPLICATION : Pour devenir pilote, il faut 200h de vol, licence PPL puis CPL, beaucoup de maths / physique, anglais parfait, et etre en super forme. Formation : 2 ans, 100 000 CHF. Salaire : 8000-15000 CHF / mois en Suisse (SWISS), 5000 CHF au debut. Tu peux devenir pilote de ligne, pilote de chasse, pilote d'helicoptere, pilote prive.",
}

def toutes_tables():
    txt = "TOUTES LES TABLES DE MULTIPLICATION 1 a 12 :\n\n"
    for n in range(1, 13):
        txt += f"Table de {n} : " + ", ".join([f"{n}x{i}={n*i}" for i in range(1, 11)]) + "\n\n"
    return txt

def table_division(n):
    txt = f"TABLE DE DIVISION DE {n} :\n"
    for i in range(1, 11):
        txt += f"{n*i} / {n} = {i}  |  "
    return txt

def trouver(q_orig):
    q = q_orig.lower()
    for mot in ["c'est quoi", "c est quoi", "c'est", "comment", "pourquoi", "donne-moi", "donne moi", "c'est qui", "qui est", "quel est", "quelle est", "comment calculer", "?"]:
        q = q.replace(mot, " ")
    q = " ".join(q.split())
    if "toutes les tables" in q or "toutes tables" in q:
        return toutes_tables()
    if "division" in q:
        try:
            n = int(''.join(filter(str.isdigit, q)))
            return table_division(n)
        except:
            return "Essaie : Table de division de 8"
    if "table de" in q or "table du" in q:
        try:
            n = int(''.join(filter(str.isdigit, q)))
            res = ", ".join([str(n) + "x" + str(i) + "=" + str(n*i) for i in range(1, 11)])
            return "Table de " + str(n) + " : " + res
        except:
            pass
    if "performant" in q or "meilleur avion" in q:
        return "AVION LE PLUS PERFORMANT ? 1. Combat : F-22 Raptor - meilleur, furtif, jamais battu. 2. Moderne : F-35 - fait tout, Suisse a choisi. 3. Vitesse : SR-71 - 3500 km/h. Mon choix : F-22 = le roi."
    if "capitale" in q:
        for pays, cap in CAPITALES.items():
            if pays in q:
                return "Capitale de " + pays.capitalize() + " = " + cap
        return "J'ai 195 capitales ! Essaie : capitale du Japon..."
    for cle, rep in PC.items():
        if cle in q:
            return rep
    for cle, rep in CHANTEURS.items():
        if cle in q:
            return rep
    for cle, rep in AVIONS.items():
        if cle in q:
            return rep
    for mot, rep in TOUT.items():
        if mot in q:
            return rep
    for pays, cap in CAPITALES.items():
        if q == pays:
            return pays.capitalize() + " -> Capitale = " + cap
    return "Je ne connais pas encore : " + q_orig + ". Essaie : clique sur une matiere !"

if "auto_q" in st.session_state and st.session_state.auto_q:
    q_auto = st.session_state.auto_q
    st.session_state.auto_q = ""
    r_auto = trouver(q_auto)
    st.session_state.messages.append({"role": "assistant", "content": r_auto})
    with st.chat_message("assistant"):
        st.write(r_auto)

if question := st.chat_input("Pose ta question... ou clique sur une question en haut !"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        r = trouver(question)
        st.write(r)
    st.session_state.messages.append({"role": "assistant", "content": r})
