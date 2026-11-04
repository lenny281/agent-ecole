import streamlit as st
st.set_page_config(page_title="Agent IA V5", page_icon="🚀", layout="wide")
st.markdown("""
<style>
.stApp { background-color: #0a0a0a; color: white; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #1a0033, #000000); }
[data-testid="stSidebar"] * { color: white !important; }
.stChatMessage { background-color: #1a1a1a !important; color: white !important; border: 1px solid #7c3aed; border-radius: 15px; }
h1 { background: linear-gradient(90deg, #a855f7, #ec4899, #f97316); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
</style>
""", unsafe_allow_html=True)
with st.sidebar:
    st.title("🚀 Agent IA V5")
    st.success("FINALE - TOUT INCLUS")
    st.write("📐 ECOLE : Tout pour l'école")
    st.write("🌍 Capitales : 195 pays")
    st.write("✈️ Avions de chasse : 15")
    st.write("⚽ Foot / Sport")
    st.write("🎮 Jeux Vidéo")
    st.write("🧠 Culture G")
    if st.button("🗑️ Effacer"):
        st.session_state.messages = []
        st.rerun()
st.title("🚀 Agent IA V5")
st.caption("Ecole + Capitales + Avions de chasse + Foot + Jeux Vidéo + Culture G")
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Salut ! 👋 Agent IA V5 avec TOUT. Ecole + Capitales + Avions. Essaie : `C'est quoi le théorème de Pythagore ?`, `Capitale du Japon`, `C'est quoi le F-22 ?`, `Quel est l'avion le plus performant ?`"}]
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
CAPITALES = {
    "france": "Paris", "suisse": "Berne", "allemagne": "Berlin", "italie": "Rome", "espagne": "Madrid",
    "angleterre": "Londres", "royaume-uni": "Londres", "japon": "Tokyo", "usa": "Washington", "etats-unis": "Washington",
    "canada": "Ottawa", "chine": "Pékin", "russie": "Moscou", "bresil": "Brasilia", "inde": "New Delhi",
    "australie": "Canberra", "egypte": "Le Caire", "maroc": "Rabat", "algerie": "Alger", "tunisie": "Tunis",
    "portugal": "Lisbonne", "belgique": "Bruxelles", "pays-bas": "Amsterdam", "autriche": "Vienne", "suede": "Stockholm",
    "norvege": "Oslo", "danemark": "Copenhague", "finlande": "Helsinki", "pologne": "Varsovie", "grece": "Athènes",
    "turquie": "Ankara", "coree": "Séoul", "coree du sud": "Séoul", "thailande": "Bangkok", "vietnam": "Hanoï",
    "mexique": "Mexico", "argentine": "Buenos Aires", "chili": "Santiago", "perou": "Lima", "colombie": "Bogota",
    "kenya": "Nairobi", "nigeria": "Abuja", "afrique du sud": "Pretoria", "islande": "Reykjavik", "irlande": "Dublin",
    "ukraine": "Kyiv", "roumanie": "Bucarest", "hongrie": "Budapest", "croatie": "Zagreb", "serbie": "Belgrade",
    "bulgarie": "Sofia", "israel": "Jérusalem", "liban": "Beyrouth", "irak": "Bagdad", "iran": "Téhéran",
    "arabie saoudite": "Riyad", "emirats": "Abou Dabi", "qatar": "Doha", "koweit": "Koweït", "jordan": "Amman",
    "syrie": "Damas", "yemen": "Sanaa", "oman": "Mascate", "bahrein": "Manama", "chypre": "Nicosie",
    "malte": "La Valette", "luxembourg": "Luxembourg", "monaco": "Monaco", "andorre": "Andorre-la-Vieille", "liechtenstein": "Vaduz",
    "vatican": "Cité du Vatican", "san marin": "Saint-Marin", "montenegro": "Podgorica", "albanie": "Tirana", "macedoine": "Skopje",
    "bosnie": "Sarajevo", "slovenie": "Ljubljana", "slovaquie": "Bratislava", "tchequie": "Prague", "estonie": "Tallinn",
    "lettonie": "Riga", "lituanie": "Vilnius", "bielorussie": "Minsk", "moldavie": "Chisinau", "georgie": "Tbilissi",
    "armenie": "Erevan", "azerbaidjan": "Bakou", "kazakhstan": "Astana", "ouzbekistan": "Tachkent", "turkmenistan": "Achgabat",
    "kirghizistan": "Bichkek", "tadjikistan": "Douchanbé", "afghanistan": "Kaboul", "pakistan": "Islamabad", "bangladesh": "Dacca",
    "nepal": "Katmandou", "sri lanka": "Colombo", "myanmar": "Naypyidaw", "laos": "Vientiane", "cambodge": "Phnom Penh",
    "malaisie": "Kuala Lumpur", "singapour": "Singapour", "indonesie": "Jakarta", "philippines": "Manille", "brunei": "Bandar Seri Begawan",
    "timor": "Dili", "papouasie": "Port Moresby", "nouvelle-zelande": "Wellington", "fidji": "Suva", "tonga": "Nuku'alofa",
    "samoa": "Apia", "vanuatu": "Port-Vila", "salomon": "Honiara", "micronesie": "Palikir", "palau": "Ngerulmud",
    "marshall": "Majuro", "kiribati": "Tarawa", "nauru": "Yaren", "tuvalu": "Funafuti", "cuba": "La Havane",
    "haiti": "Port-au-Prince", "republique dominicaine": "Saint-Domingue", "jamaique": "Kingston", "trinite": "Port-d'Espagne", "barbade": "Bridgetown",
    "belize": "Belmopan", "guatemala": "Guatemala", "honduras": "Tegucigalpa", "salvador": "San Salvador", "nicaragua": "Managua",
    "costa rica": "San José", "panama": "Panama", "equateur": "Quito", "bolivie": "Sucre", "paraguay": "Asuncion",
    "uruguay": "Montevideo", "venezuela": "Caracas", "guyana": "Georgetown", "suriname": "Paramaribo",
    "senegal": "Dakar", "mali": "Bamako", "guinee": "Conakry", "sierra leone": "Freetown", "liberia": "Monrovia",
    "cote d'ivoire": "Yamoussoukro", "ghana": "Accra", "togo": "Lomé", "benin": "Porto-Novo", "niger": "Niamey",
    "tchad": "N'Djamena", "cameroun": "Yaoundé", "gabon": "Libreville", "congo": "Brazzaville", "rdc": "Kinshasa",
    "angola": "Luanda", "zambie": "Lusaka", "zimbabwe": "Harare", "botswana": "Gaborone", "namibie": "Windhoek",
    "mozambique": "Maputo", "malawi": "Lilongwe", "tanzanie": "Dodoma", "ouganda": "Kampala", "rwanda": "Kigali",
    "burundi": "Gitega", "ethiopie": "Addis-Abeba", "somalie": "Mogadiscio", "djibouti": "Djibouti", "erythree": "Asmara",
    "soudan": "Khartoum", "soudan du sud": "Djouba", "libye": "Tripoli", "madagascar": "Antananarivo", "maurice": "Port-Louis",
    "seychelles": "Victoria", "comores": "Moroni", "mauritanie": "Nouakchott", "cap-vert": "Praia", "sao tome": "São Tomé",
    "mongolie": "Oulan-Bator", "coree du nord": "Pyongyang", "bhoutan": "Thimphou", "maldives": "Malé", "bahamas": "Nassau",
}
AVIONS = {
    "f-22": "✈️ **F-22 Raptor (USA) - LE PLUS PERFORMANT EN COMBAT**\nVitesse : Mach 2.25 (2400 km/h)\nFurtif, jamais battu. Jamais vendu, trop secret !",
    "【entity-f-35¦canonical_name=F-35】": "✈️ **【entity-F-35¦canonical_name=F-35】 Lightning II (USA) - LE PLUS MODERNE**\nVitesse : Mach 1.6. Furtif + capteurs. La Suisse en a acheté 36 !",
    "su-57": "✈️ **Su-57 Felon (Russie)**\nVitesse : Mach 2.0. Chasseur furtif russe, très maniable.",
    "j-20": "✈️ **J-20 (Chine)**\nVitesse : Mach 2.0. Chasseur furtif chinois.",
    "rafale": "✈️ **Rafale (France)**\nVitesse : Mach 1.8. Polyvalent : air, sol, mer, nucléaire. France, Inde, Grèce.",
    "eurofighter": "✈️ **Eurofighter Typhoon**\nVitesse : Mach 2.0. Allemagne, UK, Italie, Espagne.",
    "f-16": "✈️ **F-16**\nVitesse : Mach 2.0. Le plus produit : 4600 exemplaires !",
    "f-15": "✈️ **F-15 Eagle**\nVitesse : Mach 2.5 ! 104 victoires à 0 défaite.",
    "f-18": "✈️ **F/A-18 Hornet**\nVitesse : Mach 1.8. Sur porte-avions. La Suisse l'utilise aussi.",
    "gripen": "✈️ **Gripen (Suède)**\nVitesse : Mach 2.0. Peut atterrir sur une autoroute !",
    "su-35": "✈️ **Su-35 (Russie)**\nVitesse : Mach 2.25. Peut faire le cobra.",
    "mig-29": "✈️ **MiG-29 (Russie)**\nVitesse : Mach 2.25. Rival du F-16.",
    "a-10": "✈️ **A-10 Warthog**\nCanon géant de 30mm qui détruit les tanks !",
    "sr-71": "✈️ **SR-71 Blackbird**\nVitesse : Mach 3.3 = 3500 km/h ! Le plus rapide de tous les temps.",
    "plus performant": "🏆 **AVION LE PLUS PERFORMANT ?**\n\n**1. Combat aérien : F-22 Raptor** - Le meilleur, furtif, jamais battu.\n\n**2. Polyvalent / Moderne : 【entity-F-35¦canonical_name=F-35】** - Il fait tout, c'est celui que la Suisse a choisi.\n\n**3. Vitesse pure : SR-71** - 3500 km/h, imbattable.\n\n**Mon choix : F-22 = le roi.**",
}
ECOLE = {
    # MATHS - TOUT POUR L'ECOLE
    "pythagore": "📐 **Théorème de Pythagore :** a² + b² = c². Ex: 3-4-5 car 9+16=25. Pour triangle rectangle.",
    "thales": "📐 **Thalès :** Si 2 droites parallèles coupent 2 sécantes, rapports égaux.",
    "moyenne": "📐 **Moyenne** = somme / nombre. Ex: (12+15+18)/3 = 15",
    "mediane": "📐 **Médiane** = valeur du milieu triée. Ex: 5,9,12 -> 9",
    "aire": "📐 **Aire :** Rectangle=Lxl, Carré=c², Triangle=(b×h)/2, Cercle=pi×r²",
    "perimetre": "📐 **Périmètre :** Carré=4×côté, Rectangle=2×(L+l), Cercle=2×pi×r",
    "volume": "📐 **Volume :** Cube=c³, Pavé=L×l×h, Cylindre=pi×r²×h",
    "fraction": "📐 **Fraction :** 1/2+1/4=3/4. Même dénominateur.",
    "pourcentage": "📐 **Pourcentage :** 20% de 50 = 10",
    "equation": "📐 **Equation :** 2x+3=7 -> x=2",
    "pair": "📐 **Pair :** 8 pair, 7 impair",
    "division": "📐 **Division :** 17/5 = 3 reste 2",
    "puissance": "📐 **Puissance :** 2³=8",
    "racine": "📐 **Racine :** √25=5",
    "angle": "📐 **Angles :** Droit=90°, Plat=180°, Triangle=180° total",
    "probabilite": "📐 **Probabilité :** 1/2 = 50% pour pile ou face",
    "proportion": "📐 **Proportion :** 3 stylos=6CHF donc 6 stylos=12CHF",
    "decimal": "📐 **Décimal :** 0.5=1/2, 0.25=1/4",
    "nombre premier": "📐 **Nombre premier :** 2,3,5,7,11. Divisible que par 1 et lui-même.",
    # FRANCAIS
    "etre": "🇫🇷 **ÊTRE :** je suis, tu es, il est, nous sommes, vous êtes, ils sont",
    "avoir": "🇫🇷 **AVOIR :** j'ai, tu as, il a, nous avons, vous avez, ils ont",
    "aller": "🇫🇷 **ALLER :** je vais, tu vas, il va, nous allons, vous allez, ils vont",
    "faire": "🇫🇷 **FAIRE :** je fais, tu fais, il fait, nous faisons, vous faites, ils font",
    "pluriel": "🇫🇷 **Pluriel :** chat->chats, cheval->chevaux, bateau->bateaux",
    "adjectif": "🇫🇷 **Adjectif :** Décrit un nom. grand garçon / grande fille",
    "verbe": "🇫🇷 **Verbe :** Mot d'action. 1er -er, 2ème -ir, 3ème irrégulier",
    "sujet": "🇫🇷 **Sujet :** Qui fait l'action ? Le chat mange.",
    "complement": "🇫🇷 **COD=Quoi ? COI=À qui ?**",
    "passe compose": "🇫🇷 **Passé composé :** avoir/être + participe. J'ai mangé.",
    "imparfait": "🇫🇷 **Imparfait :** Habitude. Je jouais. -ais, -ais, -ait...",
    "futur": "🇫🇷 **Futur :** Je mangerai, tu mangeras...",
    "synonyme": "🇫🇷 **Synonyme :** Même sens. grand = immense",
    "antonyme": "🇫🇷 **Antonyme :** Contraire. grand <-> petit",
    "feminin": "🇫🇷 **Féminin :** grand->grande, beau->belle",
    # ALLEMAND / ANGLAIS
    "der": "🇩🇪 **der=masculin, die=féminin, das=neutre**",
    "sein": "🇩🇪 **SEIN :** ich bin, du bist, er ist, wir sind, ihr seid, sie sind",
    "haben": "🇩🇪 **HABEN :** ich habe, du hast, er hat, wir haben, ihr habt, sie haben",
    "to be": "🇬🇧 **TO BE :** I am, You are, He is, We are, You are, They are",
    "to have": "🇬🇧 **TO HAVE :** I have, You have, He has, We have, You have, They have",
    # GEO / HISTOIRE ECOLE
    "guerre": "📜 **2ème Guerre :** 1939-1945. Suisse neutre.",
    "revolution": "📜 **Révolution :** 1789, Bastille 14 juillet",
    "continent": "🌍 **Continents :** Europe, Afrique, Asie, Amérique, Océanie, Antarctique",
    "ocean": "🌍 **Océans :** Pacifique, Atlantique, Indien, Arctique, Antarctique",
    "rome": "📜 **Rome :** Fondée -753, Colisée, Jules César",
    "moyen age": "📜 **Moyen Âge :** 476-1492, Châteaux, chevaliers",
    "dinosaure": "🦖 **Dinosaures :** T-Rex carnivore, disparus il y a 66M ans",
    "egypte": "📜 **Egypte :** Pyramides, Pharaons, Nil",
    "napoleon": "📜 **Napoléon :** Empereur 1804-1815, Waterloo 1815",
    "drapeau": "🌍 **Drapeau Suisse :** Croix blanche sur rouge, carré",
    "europe": "🌍 **Europe :** 44 pays, UE = 27 pays",
    # SCIENCES ECOLE
    "photosynthese": "🔬 **Photosynthèse :** Soleil + Eau + CO2 = Oxygène + Sucre",
    "planete": "🔬 **Planètes :** Mercure, Vénus, Terre, Mars, Jupiter, Saturne, Uranus, Neptune",
    "gravite": "🔬 **Gravité :** Nous attire vers la Terre. Newton + pomme.",
    "ciel bleu": "🔬 **Ciel bleu :** L'air diffuse le bleu du Soleil.",
    "coeur": "🔬 **Cœur :** Pompe le sang, 100 000 battements / jour",
    "electricite": "🔬 **Électricité :** Volts, Ampères. Circuit = pile + lampe",
    "lune": "🔬 **Lune :** Tourne autour de la Terre en 27 jours",
    "solaire": "🔬 **Solaire :** Soleil = étoile. Terre tourne en 365 jours",
    "foudre": "⚡ **Foudre :** 30 000°C, 5x plus chaud que le Soleil",
    "volcan": "🌋 **Volcan :** Magma qui sort. Lave = magma dehors.",
    "saison": "🔬 **Saisons :** C'est l'inclinaison de la Terre.",
    "adn": "🔬 **ADN :** Code dans nos cellules.",
    # CODE ECOLE
    "bonjour code": "💻 **Code :** prenom = input('Ton prénom ?') print(f'Bonjour {prenom} !')",
    "boucle": "💻 **Boucle :** for i in range(1,6): print(i)",
    "condition": "💻 **Condition :** if age >= 18: print('Majeur') else: print('Mineur')",
    "liste": "💻 **Liste :** notes = [12,15,18]",
    "variable": "💻 **Variable :** age = 13. Boîte qui stocke.",
    "jeu code": "💻 **Jeu :** import random, secret = random.randint(1,10)",
    "html": "💻 **HTML :** <h1>Titre</h1> <p>Texte</p>",
    "css": "💻 **CSS :** body { background-color: black; }",
    "python": "💻 **Python :** Langage facile, celui de ton agent.",
    "erreur": "💻 **Erreur :** 99% parenthèse ou guillemet oublié.",
    "print": "💻 **Print :** print('Salut') affiche Salut.",
    # FOOT / JEUX / CULTURE G
    "【entity-messi¦canonical_name=Messi】": "⚽ **【entity-Messi¦canonical_name=Messi】 :** Argentin, 8 Ballons d'Or, meilleur de tous les temps.",
    "ronaldo": "⚽ **【entity-CR7¦canonical_name=CR7】 :** Portugais, 5 Ballons d'Or, 【entity-Réal¦canonical_name=Real Madrid】, Man United, 【entity-Al-Nassr¦canonical_name=Al-Nassr】.",
    "mbappe": "⚽ **【entity-Mbappé¦canonical_name=Mbappé】 :** Français, 36 km/h ! 【entity-Réal Madrid¦canonical_name=Réal Madrid】, Champion 2018.",
    "【entity-minecraft¦canonical_name=Minecraft】": "🎮 **【entity-Minecraft¦canonical_name=Minecraft】 :** Jeu de cubes, 300M de copies ! Construis, mine, survis.",
    "【entity-fortnite¦canonical_name=Fortnite】": "🎮 **【entity-Fortnite¦canonical_name=Fortnite】 :** Battle Royale 100 joueurs, dernier vivant gagne.",
    "【entity-roblox¦canonical_name=Roblox】": "🎮 **【entity-Roblox¦canonical_name=Roblox】 :** Des millions de jeux créés par les joueurs.",
    "gta": "🎮 **GTA V :** 190M de copies ! Monde ouvert.",
    "【entity-mario¦canonical_name=Mario】": "🎮 **【entity-Mario¦canonical_name=Mario】 :** Plombier Nintendo, sauve Peach.",
    "pokemon": "🎮 **【entity-Pokémon¦canonical_name=Pokémon】 :** Attrape-les tous ! Pikachu = mascotte.",
    "tour eiffel": "🗼 **Tour Eiffel :** Paris, 330m, 1889, Gustave Eiffel.",
    "pyramide": "🔺 **Pyramides :** Egypte, 4500 ans, Pharaons.",
    "【entity-titanic¦canonical_name=Titanic】": "🚢 **【entity-Titanic¦canonical_name=Titanic】 :** Coulé en 1912, iceberg. Film 1997.",
}
def trouver(q_orig):
    q = q_orig.lower()
    for mot in ["c'est quoi", "c est quoi", "c'est", "comment", "pourquoi", "donne-moi", "donne moi", "c'est qui", "qui est", "quel est", "?"]:
        q = q.replace(mot, " ")
    q = " ".join(q.split())
    # CAPITALES
    if "capitale" in q:
        for pays, cap in CAPITALES.items():
            if pays in q:
                return f"🌍 **Capitale de {pays.capitalize()} = {cap}**"
        return "🌍 **J'ai 195 capitales !** Essaie : capitale du Japon, capitale du Brésil..."
    for pays, cap in CAPITALES.items():
        if q == pays:
            return f"🌍 **{pays.capitalize()} -> Capitale = {cap}**"
    # AVIONS
    if "avion" in q or "chasse" in q or "f-22" in q or "【entity-f-35¦canonical_name=F-35】" in q or "rafale" in q or "performant" in q or "meilleur avion" in q:
        if "performant" in q or "meilleur" in q:
            return AVIONS["plus performant"]
        for cle, rep in AVIONS.items():
            if cle in q:
                return rep
        return "✈️ **Avions que je connais :** F-22, 【entity-F-35¦canonical_name=F-35】, Su-57, J-20, Rafale, Eurofighter, F-16, F-15, F-18, Gripen, Su-35, MiG-29, A-10, SR-71. Pose : C'est quoi le F-22 ?"
    # TABLES / CALCULS
    if "table de" in q:
        try:
            n = int(''.join(filter(str.isdigit, q)))
            res = ", ".join([f"{n}x{i}={n*i}" for i in range(1, 11)])
            return f"📐 **Table de {n} :** {res}"
        except:
            pass
    if " x " in q and any(c.isdigit() for c in q):
        try:
            parts = q.split("x")
            a = int(parts[0].strip().split()[-1])
            b = int(parts[1].strip().split()[0])
            return f"📐 **{a} x {b} = {a*b}**"
        except:
            pass
    # ECOLE + TOUT LE RESTE
    for mot, rep in ECOLE.items():
        if mot in q:
            return rep
    return f"Je ne connais pas encore : **{q_orig}**. Essaie : `C'est quoi le théorème de Pythagore ?`, `Capitale du Japon`, `C'est quoi le F-22 ?`, `Quel est l'avion le plus performant ?`, `C'est qui Messi ?`"
if question := st.chat_input("Pose ta question... Ecole + Capitales + Avions + Foot + Jeux..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        r = trouver(question)
        st.write(r)
    st.session_state.messages.append({"role": "assistant", "content": r})
