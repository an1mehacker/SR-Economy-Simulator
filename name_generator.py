import random
import secrets
import re
from collections import Counter

# Define target consonants
consonant_mids = ['sht', 'shk', 'ly', 'pl', 'sh', 'ts', 'ch', 'k', 't', 'n', 'h', 'l', 's', 'v', 'm', 'p']  # Longer substrings first!

def analyze_consonant_frequencies(names, consonants):
    freq = Counter()

    # Pre-sort consonants by descending length to match digraphs (e.g. 'sh') before single letters
    consonants = sorted(consonants, key=len, reverse=True)

    for name in names:
        name = name.lower()
        i = 0
        while i < len(name):
            matched = False
            for cons in consonants:
                if name[i:i+len(cons)] == cons:
                    freq[cons] += 1
                    i += len(cons)
                    matched = True
                    break
            if not matched:
                # Count each unmatched character as 'other'
                #freq['other'] += 1
                i += 1

    total = sum([count[1] for count in freq.items()])

    freq = {k: round(v / total, 3) for k, v in freq.items()}
    return dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

# Split names into syllables using a regex that tries to identify common syllable boundaries
def split_into_syllables(name):
    # This isn't nowhere near perfect for complicated names with lots of consonants like Polish names
    parts = re.split(r"[-\s]", name)
    syllables = []
    for part in parts:
        syllables.extend(re.findall(r'[^aeiouy]*[aeiouy]+(?:[^aeiouy]*)', part, flags=re.IGNORECASE))
    return syllables

def split_syllables_into_sets(list_names_syllables):
    starts = set()
    mids = set()
    ends = set()

    for syllables in list_names_syllables:
        if not syllables:
            continue
        starts.add(syllables[0])
        if len(syllables) > 2:
            mids.update(syllables[1:-1])
        if len(syllables) > 1:
            ends.add(syllables[-1])
        else:
            # For 1-syllable names, the start is also the end
            ends.add(syllables[0])

    return starts, mids, ends

def join_syllables(syllables):
    result = syllables[0]
    for i in range(1, len(syllables)):
        prev_last = result[-1]
        next_first = syllables[i][0]
        if prev_last == next_first:
            result = result[:-1] + syllables[i]  # Drop last of previous syllable
        else:
            result += syllables[i]
    return result

fei_names = [
    "Aenai", "Aenteri", "Ailtik", "Aitali", "Alakai", "Alameya", "Aklikli", "Aliota", "Allista", "Anainni",
    "Anilkaya", "Ankaio", "Ankilti", "Asaffi", "Atilanni", "Attolki", "Afaiyan", "Igeida", "Ikatar", "Iklutai",
    "Ilanki-Ra", "Iliela", "Ilifa", "Illanfi", "Illiaka", "Inilai", "Iplinir", "Isiata-Ra", "Itilak", "Laistan",
    "Lakemli", "Lalami-Ra", "Lamikka", "Lannati", "Lanoya", "Laoti-Ra", "Lasigo", "Latiar", "Layafena", "Leinami",
    "Lekian", "Lenenta", "Liami Ra", "Liemanni", "Likaina", "Liliam", "Linanki", "Liolasta", "Litaina", "Lotolai",
    "Matali-Va", "Matolli", "Memilki", "Miani", "Minilai", "Minniati", "Naima", "Naliak", "Naloya", "Namlak",
    "Nannori", "Nekki-Naki", "Nikoria", "Nilami-Rak", "Nillaik", "Nuinna", "Oakani", "Oaronna", "Olaniya",
    "Olian", "Oloaki", "Olrai-Po", "Onirana", "Onnamli", "Onolisk", "Oriali", "Osnaris", "Otialli", "Ofelaki",
    "Rakaya", "Ralanni", "Ramilta", "Ranimai", "Riania-Anro", "Rilofi", "Rioali", "Ritonkai", "Rokoyali",
    "Ruaitni", "Takiani", "Talaik", "Talikia", "Teklinai", "Tillaya", "Tolika", "Uailai", "Uainak", "Uaiya",
    "Uania"
]

gaal_names = [
    "Aadimra", "Aarkis", "Aasika", "Aga-akra", "Agligaan", "Agno-on", "Aili-irk", "Aina-ant", "Akraak",
    "Alseeki", "Ara-aga", "Ara-at", "Ariilka", "Arne-em", "Asaamrik", "Asooleun", "Assela-an", "Astiilga",
    "Beelag", "Braanakli", "Bunagraak", "Waitem", "Varoola", "Veepakar", "Vekuulga", "Viamaat", "Vinfaal",
    "Gaabebra", "Gaal-la", "Gaam-it", "Gaange", "Ga-aprog", "Geoogra", "Giraagma", "Glau-uta", "Gloobar",
    "Gusarovka", "Gneepi", "Goostakli", "Greemian", "Daaena", "Daankesa", "Da-aroka", "Deekra", "Deerkia",
    "Demeera", "Demiraak", "Dintaak", "Dleenk", "Dleesna", "Dliipar", "Doolka", "Do-opra", "Zaamal", "Zdaani",
    "Zeo-orin", "Ilooni", "Istaan", "Kaalatka", "Kaara-il", "Kaasayar", "Kageenka", "Keentam", "Keggeeba",
    "Keptaak", "Kiinakle", "Kineela", "Kirkoya", "Kliinna", "Koo-ba", "Koolat", "Kra-abbor", "Laanta",
    "Lamaait", "Lao-oga", "Leemark", "Lei-ima", "Lenliiko", "Liinka", "Liisik", "Loonen", "Lo-osta", "Loo-hi",
    "Luikaast", "Luulia", "Meengar", "Miirka", "Mini-ir", "Mooynak", "Moolkar", "Muaayri", "Naavufra",
    "Naamika", "Naklaaya", "Neekanpi", "Nekseer", "Noola", "No-omota", "Noorak"
]

maloc_names = [
    "Aborag", "Abragor", "Agedru", "Aglamagar", "Agrank", "Adderak", "Adegor", "Albarga", "Aldakron",
    "Ambakar", "Andadru", "Aratog", "Argelar", "Argontu", "Ardabon", "Areddan", "Arkelga", "Arkomaddan",
    "Atalon", "Bagarra", "Badolka", "Bakagor", "Baksan", "Balangak", "Baldagr", "Bantog", "Barragar",
    "Bebondu", "Bedron", "Bodarken", "Bolaner", "Bonaga", "Branlandar", "Brojdan", "Bronakin", "Buddar",
    "Burdak", "Gabanda", "Gabarton", "Ganaga", "Gandok", "Garond", "Gartan", "Glatak", "Gloddar", "Gnaber",
    "Gobarrak", "Godoban", "Gongart", "Gondar", "Gragan", "Grantor", "Grobber", "Gromag", "Gundor",
    "Dakadarr", "Dangor", "Darbo", "Debargon", "Derigla", "Derran", "Domkrak", "Dradat", "Drelak",
    "Zagnardu", "Zandar", "Zarran", "Kabadr", "Kagerr", "Katanor", "Kendilga", "Kinzaza", "Klabborr",
    "Kmintura", "Kodag", "Krakan", "Krantor", "Kudatra", "Kuragan", "Labaran", "Lagarton", "Ladrakru",
    "Laksader", "Langak", "Latakan", "Lebran", "Legebar", "Lekar", "Lobardu", "Loddar", "Lotonga",
    "Matagon", "Meladza", "Nabadan", "Naglabar", "Nezartu", "Obbor", "Ogatak", "Odarbag"
]

peleng_names = [
    "Aikochak", "Ayhikka", "Alehcha", "Aletskiish", "Allyasta", "Apatsash", "Ahaicak", "Veremchushka", "Bushka", "Akoichuha",
    "Acihak", "Ashkehlak", "Ihtishis", "Ihtsichak", "Itsehakka", "Yecheshka", "Ykushichan", "Ytsikash", "Ytsomahak", "Kasatish",
    "Kahitsak", "Kashikka", "Keshetskis", "Kintaksha", "Kushanak", "Lapashak", "Lahatsan", "Lahlyak", "Latsenkor", "Latsikah",
    "Latsokka", "Lekeshkis", "Lelkash", "Leprakan", "Leptank", "Lesintsak", "Letohcha", "Letsekka", "Letsishacha", "Letsetskish",
    "Lik Senats", "Li Peshka", "Lipshik", "Lishitsta", "Lok hanka", "Lochechish", "Lyakshitish", "Lyasoshik", "Lyahitsak", "Lya Chishkan",
    "Natsekkish", "Nachiksha", "Nashtochka", "Natschak", "Nelishek", "Nishahak", "Nuitsachka", "Nukitsak", "Nuktiksha", "Nuhapash",
    "Nuceshka-Li", "Penechaska", "Pehankash", "Rayecha", "Rayhan", "Ratlotska", "Rahotsis", "Retsekchish", "Riohats", "Ritsashka",
    "Richetsis", "Roplatska", "Rulyaha", "Ruhalats", "Sainashi", "Savinka", "Seisoska", "Sipatska", "Sitsheplits", "Suitsanka",
    "Suhatsan", "Sutsaykish", "Takasha", "Tashatak", "Tetsishkis", "Titsinchak", "Uikushka", "Ukayshak", "Ulyankishla", "Upatishah",
    "Uhaytsent", "Uhehechish", "Uhtaksha", "Ukshutak", "Utsayhan", "Utsanha", "Utselaksha", "Utsetsashik", "Utseshli", "Utsuhek",
    "Uchatslis", "Uchulish", "Ushikka", "Ushipanka", "Ushkopek", "Ushotsis", "hanachish", "hekeshka", "hetsetak", "Tsaikah",
    "Tsaishiska", "Tsakla", "Tsalotsha", "Tsamartash", "Tsetsha-Pru", "Tsaachinshak", "Tseppish Tseppan", "Tsetsenash", "Tsetshutka",
    "Tsipaishi", "Tsipeksha", "Tsipishan", "Tsishiska", "Tslataksha", "Tsokahak", "Tsopshik", "Tsotskekesh", "Tsubaksha", "Tsukali",
    "Tsukeshka", "Cheke Shan", "Chespeika", "Checekish", "Cheshuikis", "Chikkash", "Chappelli", "Chivchalka", "Shainah", "Shatapan", "Shatsak",
    "Shekecha", "Shekitsak", "Shehlak", "Shetsenka", "Shetsaplan", "Shukukha", "Yakitseska", "Yatatchik", "Yahatsish", "Yatsikka"
]


people_names = [
    "August", "Adam", "Admiral", "Aqua", "Albatross", "Albinos", "Altair", "Amber", "Anaconda",
    "Andromeda", "Anubis", "Apollon", "Arbiter", "Argo", "Artemis", "Archimede", "Astra", "Atoll",
    "Afina", "Aphrodite", "Blatosphera", "Venus", "Viktoriya",
    "Galileo", "Ganover", "Gauss", "Gera", "Hercules", "Germes", "Gerodot",
    "Gertsog", "Gibraltar", "Giant", "Gladiolus", "Hilly", "Delphin", "Dervish",  "Dionis", "Claus",
    "Druid", "Dune", "Cardinal", "Star", "Emerald", "Illusion", "Immodium", "In i Yan",
    "Katana", "Kolibri", "Comet", "Crystal", "Legionnaire", "Liliya", "Lord", "Luna",
    "Luch", "May", "Malachite", "Mercury", "Merlin", "Minor",
    "Minotaur", "Mir", "Monarch", "Monarch", "Muse", "Hope", "Narcys", "Neptune", "Odyssey",
    "Ocean", "Octave", "Olimp", "Orel", "Orion", "Osiris", "Paradise", "Paris", "Patagonia", "Penelope",
    "Omicron Persei", "Perun", "Pluton", "Pathway", "Poseidon", "President", "Procurator",
    "Prometheus", "Prophet", "Put", "Rubin", "Mermaid", "Knight", "Senator",
    "Consensus", "Stranger", "Strela", "Destiny", "Sphinx", "Tacit", "Titan", "Topaz", "Tornado",
    "Troy", "Troubadour", "Work", "Pharaoh", "Phoenix", "Fialka", "Philosopher", "Peasant", "hronos",
    "Caesar", "Shuttle", "Shiva", "Evolution", "Edip", "Euler", "Elixir", "Ellada", "Elf", "Emissary",
    "Spiker", "ElSent", "Bulldozer", "Partisan", "Prof", "Artemis", "Heir", "Sunrise" "Brother Rabbit",
    "Vesuvius", "Assol", "Marquis", "Matthew", "Moment", "Mendeleev", "Firewood", "Wenzel", "Bootes",
    "Ajax", "Begonia", "Cassiopeia", "Ark", "Pericles", "Pythagoras", "Beacon", "Flute", "Priest", "Justice",
    "Element", "Brave", "Helionaut",
]

corporation_names = {
    "Organics": [
        "Gaia Harvest Ltd.", "Verdant Star Agri", "OrbiGrow Corp.", "Celestial Farms Inc.", "BioFrontier Exports",
        "Nebula Naturals", "Organic Horizons", "Eden's Bounty", "Solaris Provisions", "Nova Bloom Inc.",
        "Primeval Earth Co.", "Terra Vita Organics", "CosmoHarvest Collective", "Aurora Botanicals",
        "Interstellar Organics", "Starborne Harvesters", "Deep Green Ventures", "Galactic Grain Exchange",
        "Xenoflora Enterprises", "Hyperflora Trading"
    ],
    "Synthetics": [
        "Plastech Dynamics", "SynthCore Industries", "NeoPolymer Corp.", "GalaxiPlast Ltd.", "OmniForm Materials",
        "NanoWeave Systems", "HyperPlast Conglomerate", "Quantum Composites", "ExoSynthetics", "FusionMold Industries",
        "MechaPoly Corp.", "BioSynthetic Ventures", "VoidResin Technologies", "Starbond Polymers",
        "AstroPlastics Ltd.", "NextGen Materials", "CryoForm Synthetics", "DuraTech Polymers", "Orion SynthTech",
        "Infinity Composites"
    ],
    "Common Minerals": [
        "Galactic Oreworks", "Universal Mining Corp.", "Asteroid Alloy Co.", "Stellar Metals Ltd.", "Deep Core Extractors",
        "Hyperion Mining Conglomerate", "Solaris Excavations", "Titan Metallurgy", "VoidMiner Industries", "Helios Ore Ventures",
        "Interstellar Miners Guild", "Quantum Oreworks", "AstroCore Extractions", "Zenith Mining Inc.", "Dreadnought Metallurgy",
        "XenoMetal Industries", "Lunar Alloy Syndicate", "Outer Rim Miners", "Asteroid Strip Co.", "Celestial Extraction Group"
    ],
    "Rare Minerals": [
        "ExoRare Metals Ltd.", "Singularity Extractors", "Celestial Prisms", "Void Treasure Corp.", "HyperCore Elements",
        "Dark Matter Refinery", "Quantum Rares Syndicate", "Galactic Precious Metals", "Zenith Elementals", "Black Star Minerals",
        "NovaGem Enterprises", "Infinity Core Mining", "Stellar Rares Consortium", "XenoOre Industries", "Cosmic Alloy Traders",
        "Dawnlight Metallurgy", "Solaris Rares Corp.", "Titanium Prime Resources", "Deep Void Extracts", "ExoTech Materials"
    ],
    "Refined Minerals": [
        "Quantum Forge Ltd.", "VoidSteel Refinery", "Celestial Smelters", "Hyperion Metallurgy", "Infinity Alloy Works",
        "Zenith Refining Corp.", "Solaris Foundries", "XenoSteel Industries", "Nova Glassworks", "Titanium Prime Refinery",
        "AstroMetals Conglomerate", "Deep Core Smelting", "Lunar Glassworks", "Stellar Alloy Consortium",
        "Singularity Metalworks", "HyperForge Systems", "OmniRefine Enterprises", "VoidMeld Inc.", "Black Star Smelting",
        "GalaxiRefine Industries"
    ],
    "Supplies": [
        "Galactic Essentials", "Nova Provisions", "Solaris Logistics", "Hyperion Supply Chain", "VoidSurvival Inc.",
        "XenoGoods Ltd.", "Deep Space Essentials", "Universal Trade Solutions", "CosmoSupply Corp.", "Infinity Necessities",
        "Frontier Provisions", "AstroBasics Ltd.", "Nebula Living Co.", "Interstellar Aid Logistics", "Zenith Supply Networks",
        "OmniLife Goods", "ExoSupply Chain", "Nova Comfort Goods", "Starborne Essentials", "Orion Logistics"
    ],
    "Medicine": [
        "Celestial Pharma", "VoidMed Solutions", "Stellar Biotech", "Hyperion Medical", "Galactic Lifeline Corp.",
        "NovaCure Pharmaceuticals", "Infinity BioSolutions", "Solaris Medical Systems", "Zenith Health Industries", "XenoMeds Ltd.",
        "Frontier Pharmaceuticals", "Deep Space Biotech", "OmniHealth Corp.", "Cosmic Cure Ventures", "VoidAid Industries",
        "Singularity BioTech", "Interstellar Medical Consortium", "Nebula Pharma Corp.", "AstroHealth Solutions", "ExoMed Technologies"
    ],
    "Alcohol": [
        "Void Spirits Distillery", "Celestial Brews", "Hyperion Liquor Co.", "Nova Reserve Wines", "Galactic Aleworks",
        "Stellar Spirits Ltd.", "Infinity Brewmasters", "Solaris Fermentation Co.", "AstroDistillers Inc.", "Zenith Cellars",
        "Black Star Brewing", "Nebula Rum Co.", "XenoWhiskey Ltd.", "Deep Space Vintners", "Singularity Brewing Syndicate",
        "Interstellar Spirits Consortium", "Frontier Fermentation", "Dreadnought Distillers", "Quantum Liquors Ltd.", "Orion Craft Beverages"
    ],
    "Technology Goods": [
        "NovaTek Industries", "Voidware Technologies", "Hyperion Electronics", "Celestial Systems Ltd.", "XenoChip Inc.",
        "Infinity Digital Solutions", "Solaris Quantum Devices", "AstroLogic Corp.", "Zenith AI Technologies", "Interstellar Circuits",
        "Singularity Robotics", "Galactic Softworks", "Deep Core Tech Systems", "Quantum Computronics", "Dreadnought Techworks",
        "Frontier Digital Labs", "OmniCyber Industries", "Black Star Innovations", "VoidNet Technologies", "ExoTech Solutions"
    ],
    "Luxury Items": [
        "Celestial Couture", "Nova Elegance", "Solaris Jewelworks", "Hyperion Luxury Goods", "XenoArtisan Creations",
        "Infinity Opulence Corp.", "Stellar Prestige Ltd.", "VoidFinery Designs", "Galactic Glamour Enterprises", "Deep Space Masterworks",
        "Singularity Design House", "Zenith Elite Goods", "Nebula Rarities", "OmniLuxury Ltd.", "AstroRiches Co.",
        "Quantum Jewels & Finery", "Dreadnought Elite Creations", "Black Star Prestige", "Frontier Luxe", "Orion Craftsmanship"
    ],
    "Weapons": [
            "Titan Arms", "Blackstar Munitions", "NovaCorp Warfare", "Helios Defense Systems", "Ironclad Arsenal",
            "Ares Tactical", "Voidfire Industries", "Omega Strike Solutions", "Dark Matter Ordnance", "Eclipse Armory",
            "Crimson Legion Tech", "Orion Warworks", "Zenith Ballistics", "Prometheus Defense", "Stormfront Armaments",
            "Havoc Industries", "Cerberus Munitions", "Thunderforge Weapons", "Quantum Killzone", "Specter Arms"
        ],
    "Equipment Parts": [
        "Hyperion Components", "Neptune Forge", "OmniTech Fabrication", "AstroCore Mechanics", "VoidWorks Engineering",
        "Aegis Parts & Repair", "NovaFrame Industries", "Titan Gear Systems", "Zenith Mechanics", "Orion Forgeworks",
        "Helios Machine Works", "Quantum Alloy Systems", "StarForge Parts", "Celestial Components", "Inferno Assembly",
        "Vanguard Systems", "Omega Forge", "Blackstar Engineering", "Nebula Tech Solutions", "WarpDrive Components"
    ],
    "Fuel": [
        "Quantum Fuel Dynamics", "HyperCharge Energy", "AetherCore Power", "PlasmaFlow Fuels", "NovaCharge Systems",
        "Helios Energy Solutions", "Titan Propulsion Co.", "VoidStream Fuelworks", "Eclipse Energy Systems", "DarkStar Fuels",
        "Stellar Pulse Dynamics", "Zenith Power Core", "WarpCell Technologies", "Celestial Charge Industries", "Ares Fuel & Ammo",
        "Specter Reload Solutions", "Infinity Power Systems", "Orion ChargeTech", "Blachole Energy Co.", "Solaris Fuelworks"
    ]
}

prefixes = {
    "Organics": ["Gaia", "Verdant", "Orbi", "Celestial", "BioFrontier", "Nebula", "Organic", "Eden", "Solaris", "Nova"],
    "Synthetics": ["Plastech", "SynthCore", "NeoPolymer", "GalaxiPlast", "OmniForm", "NanoWeave", "HyperPlast", "Quantum", "Exo", "FusionMold"],
    "Common Minerals": ["Galactic", "Universal", "Asteroid", "Stellar", "Deep Core", "Hyperion", "Solaris", "Titan", "VoidMiner", "Helios"],
    "Rare Minerals": ["ExoRare", "Singularity", "Celestial", "Void", "HyperCore", "Dark Matter", "Quantum", "Galactic", "Zenith", "Black Star"],
    "Refined Minerals": ["Quantum", "VoidSteel", "Celestial", "Hyperion", "Infinity", "Zenith", "Solaris", "XenoSteel", "Nova", "Titanium Prime"],
    "Supplies": ["Galactic", "Nova", "Solaris", "Hyperion", "VoidSurvival", "Xeno", "Deep Space", "Universal", "CosmoSupply", "Infinity"],
    "Medicine": ["Celestial", "VoidMed", "Stellar", "Hyperion", "Galactic", "NovaCure", "Infinity", "Solaris", "Zenith", "XenoMeds"],
    "Alcohol": ["Void Spirits", "Celestial", "Hyperion", "Nova", "Galactic", "Stellar", "Infinity", "Solaris", "Astro", "Zenith"],
    "Technology Goods": ["NovaTek", "Voidware", "Hyperion", "Celestial", "XenoChip", "Infinity", "Solaris", "AstroLogic", "Zenith", "Interstellar"],
    "Luxury Items": ["Celestial", "Nova", "Solaris", "Hyperion", "XenoArtisan", "Infinity", "Stellar", "VoidFinery", "Galactic", "Deep Space"],
    "Weapons": ["Titan", "Blackstar", "NovaCorp", "Helios", "Ironclad", "Ares", "Voidfire", "Omega", "Dark Matter", "Eclipse"],
    "Equipment Parts": ["Hyperion", "Neptune", "OmniTech", "AstroCore", "VoidWorks", "Aegis", "NovaFrame", "Titan", "Zenith", "Orion"],
    "Fuel": ["Quantum", "HyperCharge", "AetherCore", "PlasmaFlow", "NovaCharge", "Helios", "Titan", "VoidStream", "Eclipse", "DarkStar"]
}

suffixes = {
    "Organics": ["Harvest Ltd.", "Star Agri", "Corp.", "Farms Inc.", "Exports", "Naturals", "Horizons", "Bounty", "Provisions", "Bloom Inc."],
    "Synthetics": ["Dynamics", "Industries", "Corp.", "Ltd.", "Materials", "Systems", "Conglomerate", "Composites", "Synthetics", "Industries"],
    "Common Minerals": ["Oreworks", "Mining Corp.", "Alloy Co.", "Metals Ltd.", "Extractors", "Conglomerate", "Excavations", "Metallurgy", "Industries", "Ventures"],
    "Rare Minerals": ["Metals Ltd.", "Extractors", "Prisms", "Corp.", "Elements", "Refinery", "Syndicate", "Metals", "Elementals", "Minerals"],
    "Refined Minerals": ["Forge Ltd.", "Refinery", "Smelters", "Metallurgy", "Works", "Refining Corp.", "Foundries", "Industries", "Glassworks", "Conglomerate"],
    "Supplies": ["Essentials", "Provisions", "Logistics", "Supply Chain", "Inc.", "Ltd.", "Solutions", "Corp.", "Networks", "Goods"],
    "Medicine": ["Pharma", "Solutions", "Biotech", "Medical", "Lifeline Corp.", "Pharmaceuticals", "BioSolutions", "Medical Systems", "Industries", "Ltd."],
    "Alcohol": ["Distillery", "Brews", "Liquor Co.", "Reserve Wines", "Aleworks", "Spirits Ltd.", "Brewmasters", "Fermentation Co.", "Distillers Inc.", "Cellars"],
    "Technology Goods": ["Industries", "Technologies", "Electronics", "Systems Ltd.", "Inc.", "Digital Solutions", "Devices", "Corp.", "Circuits"],
    "Luxury Items": ["Couture", "Elegance", "Jewelworks", "Luxury Goods", "Creations", "Opulence Corp.", "Prestige Ltd.", "Designs", "Enterprises", "Masterworks"],
    "Weapons": ["Arms", "Munitions", "Warfare", "Defense Systems", "Arsenal", "Tactical", "Industries", "Strike Solutions", "Ordnance", "Armory"],
    "Equipment Parts": ["Components", "Forge", "Fabrication", "Mechanics", "Engineering", "Parts & Repair", "Industries", "Gear Systems", "Mechanics", "Forgeworks"],
    "Fuel": ["Fuel Dynamics", "Energy", "Power", "Fuels", "Systems", "Solutions", "Propulsion Co.", "Fuelworks", "Energy Systems", "Fuels"]
}

company_names = ["Aibo-3001", "Malocosoft"]

race_names = {
    "Gaalians": gaal_names,
    "Faeyans": fei_names,
    "Humans": people_names,
    "Pelengs": peleng_names,
    "Maloqs": maloc_names
}

trade_good_types = [
    "Organics",
    "Synthetics",
    "Common Minerals",
    "Rare Minerals",
    "Refined Minerals",
    "Supplies",
    "Medicine",
    "Alcohol",
    "Technology Goods",
    "Luxury Items",
    "Weapons",
    "Equipment Parts",
    "Fuel"
]

def pop_random_item(uncasted_list, remove=True):
    new_list = list(uncasted_list)
    item = secrets.choice(new_list)
    if remove is True:
        new_list.remove(item)

    return item, new_list

def generate_names(amount_of_companies, race):
    names = {}
    for t in trade_good_types:
        names[t] = []
        for i in range(amount_of_companies):
            random_prefix = random.random()
            random_suffix  = random.random()

            if random_prefix <= 0.6 and len(race_names[race]) > 0:
                prefix, race_names[race] = pop_random_item(race_names[race])  #
            else:
                prefix, prefixes[t] = pop_random_item(prefixes[t])

            if random_suffix <= 0.3 and len(race_names[race]) > 0:
                suffix, race_names[race] = pop_random_item(race_names[race])
            else:
                suffix, _ = pop_random_item(suffixes[t], False)

            names[t].append(prefix + " " + suffix)

    return names

#generated_names = generate_names(6, list(race_names.keys())[4])
#print(generated_names)
maloq_corporations_repeated = {'Organics': ['Andadru Harvest Ltd.', 'Aldakron Horizons', 'Nebula Corp.', 'BioFrontier Exports', 'Bakagor Corp.', 'Celestial Bloom Inc.'], 'Synthetics': ['FusionMold Dynamics', 'Gartan Kudatra', 'Zagnardu Ambakar', 'Dradat Industries', 'Plastech Industries', 'Dakadarr Dynamics'], 'Common Minerals': ['Asteroid Mining Corp.', 'Hyperion Oreworks', 'Deep Core Ventures', 'Derran Mining Corp.', 'VoidMiner Industries', 'Titan Balangak'], 'Rare Minerals': ['Meladza Bagarra', 'Darbo Corp.', 'Gongart Grantor', 'Langak Adegor', 'Bronakin Kmintura', 'Dark Matter Godoban'], 'Refined Minerals': ['Ardabon Refining Corp.', 'Kuragan Smelters', 'Aratog Smelters', 'Gondar Burdak', 'Hyperion Dangor', 'Agrank Ganaga'], 'Supplies': ['Solaris Solutions', 'Katanor Gundor', 'Universal Lotonga', 'Nova Goods', 'Kinzaza Kendilga', 'Albarga Gromag'], 'Medicine': ['Labaran BioSolutions', 'Galactic BioSolutions', 'NovaCure Badolka', 'Obbor Ltd.', 'Bedron Medical', 'Bolaner Medical'], 'Alcohol': ['Loddar Spirits Ltd.', 'Astro Reserve Wines', 'Void Spirits Brews', 'Lagarton Liquor Co.', 'Zenith Brewmasters', 'Infinity Distillers Inc.'], 'Technology Goods': ['Garond Electronics', 'Agedru Corp.', 'Zarran Corp.', 'XenoChip Devices', 'Aborag Systems Ltd.', 'Gragan Devices'], 'Luxury Items': ['XenoArtisan Masterworks', 'VoidFinery Opulence Corp.', 'Arkomaddan Buddar', 'Celestial Creations', 'Bodarken Jewelworks', 'Krakan Creations'], 'Weapons': ['Abragor Domkrak', 'Baldagr Armory', 'Gobarrak Armory', 'Blackstar Gloddar', 'Ironclad Industries', 'Krantor Arms'], 'Equipment Parts': ['NovaFrame Engineering', 'Barragar Gabanda', 'Adderak Drelak', 'Ogatak Forge', 'Gabarton Engineering', 'Zandar Kagerr'], 'Fuel': ['Kabadr Fuels', 'Gandok Kodag', 'Grobber Propulsion Co.', 'Argelar Fuels', 'Laksader Baksan', 'Branlandar Glatak']}

gaalian_interstellar_corpos = {
    'Organics': 'Kaara-il Exports',
    'Synthetics': 'Kiinakle NeoPolymers',
    'Common Minerals': 'Meengar Metals',
    'Rare Minerals': 'Meengar Metals',
    'Refined Minerals': 'Solaris Muaayris',
    'Essential Goods': 'Liinka & Braankli',
    'Medicine': 'Ilooni Pharmaceuticals',
    'Narcotics': 'Ilooni Pharmaceuticals',
    'Vice Goods': 'Aasika Spirits Ltd.',
    'Microchips': 'Gaal-da',
    'Technology Goods': 'Gaal-da',
    'Luxury Goods': 'Ga-aprog Jewelworks',
    'Weapons': 'Blackstar No-omota',
    'Equipment Parts': 'Mini-ir Forgeworks',
    'Fuel': 'Demeera Energy',
    'Ammunition': 'Blackstar No-omota'
}

faeyan_interstellar_corpos = {
    'Organics': 'Teklinai Farms Inc.',
    'Synthetics': 'Ilanki-Ra Conglomerate',
    'Common Minerals': 'Nekki-Naki Hyperion',
    'Rare Minerals': 'Nekki-Naki Hyperion',
    'Refined Minerals': 'Eypentak Industries',
    'Essential Goods': 'OFLK', #Ofelaki
    'Medicine': 'Ralanni Biotech',
    'Narcotics': 'Ralanni Biotech',
    'Vice Goods': 'Attolki & Nikoria',
    'Microchips': 'Aibo-3001',
    'Technology Goods': 'Aibo-3001',
    'Luxury Goods': 'Talaik Luxuries',
    'Weapons': 'Riania-Anro',
    'Equipment Parts': 'Eypentak Industries',
    'Fuel': 'Eypentak Industries',
    'Ammunition': 'Riania-Anro'
}

human_interstellar_corpos = {
    'Organics': 'Eden Exports',
    'Synthetics': 'Exo Corp.',
    'Common Minerals': 'Titan Extractors',
    'Rare Minerals': 'Titan Extractors',
    'Refined Minerals': 'Astro Metals',
    'Essential Goods': 'GalaMart',
    'Medicine': 'Kessler-Cortek Union',
    'Narcotics': 'Kessler-Cortek Union',
    'Vice Goods': 'Blaire Syndicate',
    'Microchips': 'Zenith',
    'Technology Goods': 'Zenith',
    'Luxury Goods': 'Nova Mir',
    'Weapons': 'Mars Armaments',
    'Equipment Parts': 'Sakiji Mechanics',
    'Fuel': 'VoidStream',
    'Ammunition': 'Mars Armaments'
}

peleng_interstellar_corpos = {
    'Organics': 'BioFrontier Chikkash',
    'Synthetics': 'Kahitsak Synthetics',
    'Common Minerals': 'Lapashak Metals',
    'Rare Minerals': 'Lapashak Metals',
    'Refined Minerals': 'Lapashak Metals',
    'Essential Goods': 'RealMart',
    'Medicine': 'Honest Meds',
    'Narcotics': 'Nuhapash',
    'Vice Goods': 'Nuhapash',
    'Microchips': 'Interstellar Suhatsan',
    'Technology Goods': 'Interstellar Suhatsan',
    'Luxury Goods': 'Nuhapash',
    'Weapons': 'Latsenkor Tactical',
    'Equipment Parts': 'Phedok Industries',
    'Fuel': 'Nuhapash',
    'Ammunition': 'Latsenkor Tactical'
}

maloq_interstellar_corpos = {
    'Organics': 'BagaCorp',
    'Synthetics': 'RGT Workshop 2-SU',
    'Common Minerals': 'PPR Sector 7-K',
    'Rare Minerals': 'PPR Sector 7-K',
    'Refined Minerals': 'AGD Factory 4-VN',
    'Essential Goods': 'BagaCorp',
    'Medicine': 'RGT Workshop 2-SU',
    'Narcotics': 'GPT Processing Unit 6-X',
    'Vice Goods': 'GPT Processing Unit 6-X',
    'Microchips': 'Malocosoft',
    'Technology Goods': 'Malocosoft',
    'Luxury Goods': 'PPR Factory #9',
    'Weapons': 'RGT Armament Plant 1-A',
    'Equipment Parts': 'RGT SpacePort Complex #5',
    'Fuel': 'RGT SpacePort Complex #5',
    'Ammunition': 'RGT Armament Plant 1-A'
}

def remove_duplicates(*dicts):
    seen = set()  # Track seen names
    cleaned_dicts = []

    for d in dicts:
        cleaned_dict = {}
        for category, names in d.items():
            unique_names = []
            for name in names:
                if name not in seen:
                    unique_names.append(name)
                    seen.add(name)
                else:
                    print("Duplicate Found: " + name)
            cleaned_dict[category] = unique_names
        cleaned_dicts.append(cleaned_dict)

    return cleaned_dicts

# Example usage with 5 dictionaries
'''
gaalian_corporations_repeated, faeyan_corporations_repeated, human_corporations_repeated, peleng_corporations_repeated, maloq_corporations_repeated = remove_duplicates(
    gaalian_corporations_repeated, faeyan_corporations_repeated, human_corporations_repeated, peleng_corporations_repeated, maloq_corporations_repeated
)'''

#print(gaalian_corporations_repeated)
#print(faeyan_corporations_repeated)
#print(human_corporations_repeated)
#print(peleng_corporations_repeated)
#print(maloq_corporations_repeated)


# corporations without duplicates
gaalian_corporations = {'Organics': ['Verdant Muaayri', 'Varoola Exports', 'Kaara-il Bounty', 'Keentam Farms Inc.', 'Aadimra Corp.', 'Geoogra Farms Inc.'], 'Synthetics': ['Doolka Ltd.', 'Lao-oga Dynamics', 'Kra-abbor Dynamics', 'Exo Ltd.', 'NeoPolymer Keptaak', 'Kiinakle Luulia'], 'Common Minerals': ['Galactic Assela-an', 'Loo-hi Viamaat', 'Hyperion Lei-ima', 'Arne-em Agno-on', 'Universal Metals Ltd.', 'Kirkoya Excavations'], 'Rare Minerals': ['ExoRare Prisms', 'Istaan Corp.', 'Moolkar Naamika', 'Meengar Metals', 'Koo-ba Nekseer', 'Black Star Gaabebra'], 'Refined Minerals': ['Noorak Lenliiko', 'Dliipar Lo-osta', 'Lamaait Goostakli', 'Asooleun Kineela', 'XenoSteel Glassworks', 'Infinity Metallurgy'], 'Supplies': ['Dintaak Deerkia', 'Dleesna Inc.', 'Deekra Supply Chain', 'Liinka Braanakli', 'Kaasayar Keggeeba', 'Gaam-it Asaamrik'], 'Medicine': ['XenoMeds Medical Systems', 'Waitem Luikaast', 'Ilooni Pharmaceuticals', 'Galactic Solutions', 'Solaris Ariilka', 'Infinity Noola'], 'Alcohol': ['Stellar Brews', 'Nova Aleworks', 'Aasika Spirits Ltd.', 'Daankesa Spirits Ltd.', 'Zdaani Distillers Inc.', 'Astro Brewmasters'], 'Technology Goods': ['Gaal-la Devices', 'Zaamal Corp.', 'Gusarovka Gloobar', 'Zenith Digital Solutions', 'Celestial Electronics', 'Vinfaal Da-aroka'], 'Luxury Items': ['Deep Space Jewelworks', 'Hyperion Luxury Goods', 'Zeo-orin Masterworks', 'Kaalatka Jewelworks', 'Ga-aprog Luxury Goods', 'Celestial Prestige Ltd.'], 'Weapons': ['Blackstar No-omota', 'Dark Matter Defense Systems', 'Voidfire Arsenal', 'NovaCorp Akraak', 'Gneepi Aina-ant', 'Do-opra Strike Solutions'], 'Equipment Parts': ['Aarkis Gear Systems', 'Bunagraak Mechanics', 'Orion Ara-aga', 'Titan Mini-ir', 'Aegis Parts & Repair', 'Beelag Giraagma'], 'Fuel': ['Naavufra Fuels', 'Kliinna Miirka', 'HyperCharge Systems', 'Ara-at Fuelworks', 'Demeera Energy', 'VoidStream Fuels']}
faeyan_corporations = {'Organics': ['Matolli Bounty', 'Nebula Horizons', 'Teklinai Farms Inc.', 'Uania Star Agri', 'Solaris Iklutai', 'Lasigo Atilanni'], 'Synthetics': ['NanoWeave Illiaka', 'Exo Industries', 'OmniForm Ltd.', 'Ilanki-Ra Conglomerate', 'Quantum Synthetics', 'Plastech Materials'], 'Common Minerals': ['VoidMiner Conglomerate', 'Asteroid Oreworks', 'Olrai-Po Industries', 'Hyperion Aenteri', 'Laistan Ventures', 'Solaris Oreworks'], 'Rare Minerals': ['Quantum Ankaio', 'HyperCore Prisms', 'Nekki-Naki Elements', 'Celestial Corp.', 'Asaffi Anilkaya', 'Galactic Liami Ra'], 'Refined Minerals': ['Oakani Tillaya', 'Hyperion Foundries', 'Zenith Smelters', 'Lannati Aklikli', 'Lamikka Glassworks', 'Nova Igeida'], 'Supplies': ['Deep Space Goods', 'Universal Ofelaki', 'Oaronna Networks', 'Nannori Corp.', 'VoidSurvival Supply Chain', 'Hyperion Afaiyan'], 'Medicine': ['Zenith Ralanni', 'Alakai Solutions', 'Celestial Pharmaceuticals', 'Solaris Biotech', 'Hyperion Itilak', 'Lakemli Industries'], 'Alcohol': ['Solaris Distillers Inc.', 'Void Spirits Attolki', 'Celestial Distillers Inc.', 'Zenith Spirits Ltd.', 'Nikoria Reserve Wines', 'Ranimai Spirits Ltd.'], 'Technology Goods': ['Infinity Inc.', 'Celestial Industries', 'Nillaik Systems Ltd.', 'Voidware Devices', 'Inilai Electronics', 'Interstellar Circuits'], 'Luxury Items': ['Talaik Luxury Goods', 'Takiani Designs', 'Otialli Designs', 'Deep Space Designs', 'Minniati Prestige Ltd.', 'VoidFinery Couture'], 'Weapons': ['NovaCorp Industries', 'Eclipse Osnaris', 'Titan Arsenal', 'Dark Matter Arsenal', 'Matali-Va Arsenal', 'Ares Riania-Anro'], 'Equipment Parts': ['Talikia Nilami-Rak', 'Hyperion Forge', 'VoidWorks Engineering', 'Rokoyali Leinami', 'Neptune Parts & Repair', 'Ilifa Laoti-Ra'], 'Fuel': ['NovaCharge Uailai', 'Helios Allista', 'Memilki Energy', 'Ailtik Systems', 'HyperCharge Energy Systems', 'Liliam Propulsion Co.']}
human_corporations = {'Organics': ['Gaia Provisions', 'Bootes Bloom Inc.', 'Strela Corp.', 'BioFrontier Malachite', 'Eden Exports', 'Element May'], 'Synthetics': ['FusionMold Industries', 'Exo Corp.', 'Troy Dynamics', 'HyperPlast Corp.', 'NanoWeave Giant', 'OmniForm Materials'], 'Common Minerals': ['Titan Industries', 'Legionnaire Conglomerate', 'Heir Extractors', 'Solaris Ventures', 'Hyperion Extractors', 'Universal Ventures'], 'Rare Minerals': ['Singularity Minerals', 'Galactic Prisms', 'Quantum Prisms', 'HyperCore SunriseBrother Rabbit', 'Elixir Crystal', 'Black Star Claus'], 'Refined Minerals': ['Celestial Archimede', 'Gerodot Conglomerate', 'Prof Stranger', 'XenoSteel Astra', 'Solaris Industries', 'Cardinal Glassworks'], 'Supplies': ['Infinity Logistics', 'Hyperion Supply Chain', 'Elf Prophet', 'Admiral Provisions', 'Xeno Provisions', 'Universal Neptune'], 'Medicine': ['ElSent Medical Systems', 'Hyperion Biotech', 'VoidMed Solutions', 'Katana Medical Systems', 'XenoMeds Ltd.', 'NovaCure Medical'], 'Alcohol': ['Nova Immodium', 'Dionis Distillers Inc.', 'Altair Distillery', 'Zenith Reserve Wines', 'Infinity Galileo', 'Hyperion Brewmasters'], 'Technology Goods': ['Lord Technologies', 'Hope Systems Ltd.', 'Hyperion Devices', 'Infinity Industries'], 'Luxury Items': ['Nova Mir', 'President Creations', 'XenoArtisan Designs', 'Albinos Prestige Ltd.', 'Hilly Spiker', 'Comet Couture'], 'Weapons': ['Ironclad Arms', 'Ares Arms', 'Titan Munitions', 'Blackstar Procurator', 'Adam Arsenal', 'Ellada Strike Solutions'], 'Equipment Parts': ['Put Delphin', 'Kolibri Mechanics', 'Zenith Mechanics', 'Titan Forgeworks', 'Assol Gear Systems', 'Hyperion Engineering'], 'Fuel': ['NovaCharge Power', 'VoidStream Energy', 'Justice Minor', 'Helios Fuels', 'Mercury Systems', 'Edip Power']}
peleng_corporations = {'Organics': ['Solaris Savinka', 'BioFrontier Chikkash', 'Verdant Exports', 'Celestial Bounty', 'Nova Naturals', 'Letsekka Tashatak'], 'Synthetics': ['Nachiksha Materials', 'GalaxiPlast Nuitsachka', 'Kahitsak Synthetics', 'Veremchushka Conglomerate', 'Quantum Materials'], 'Common Minerals': ['Tsaishiska Shekitsak', 'Utsuhek Suitsanka', 'Tseppish Tseppan Ventures', 'Tsaikah Metals Ltd.', 'Bushka Mining Corp.', 'Tsishiska Itsehakka'], 'Rare Minerals': ['Singularity Shukukha', 'Shatapan Letsetskish', 'Roplatska Metals', 'Quantum Metals', 'Lapashak Metals', 'Ruhalats Elementals'], 'Refined Minerals': ['Cheshuikis Refining Corp.', 'Hyperion Tsamartash', 'Yakitseska Ayhikka', 'Ratlotska Refining Corp.', 'Quantum Tsakla', 'Lishitsta Glassworks'], 'Supplies': ['Lyakshitish Essentials', 'Shehlak Logistics', 'Takasha Ltd.', 'Latsikah Essentials', 'Ihtsichak Kintaksha', 'Keshetskis Provisions'], 'Medicine': ['Lyahitsak Pharmaceuticals', 'hanachish Ashkehlak', 'Galactic Allyasta', 'Ahaicak Solutions', 'XenoMeds Industries', 'Celestial Medical Systems'], 'Alcohol': ['Nuhapash Spirits Ltd.', 'Celestial Liquor Co.', 'Zenith Liquor Co.', 'Yatatchik Brews', 'Sutsaykish Letsishacha', 'Kushanak Spirits Ltd.'], 'Technology Goods': ['Yatsikka Digital Solutions', 'Utsetsashik Devices', 'Tsotskekesh Inc.', 'Interstellar Suhatsan', 'Titsinchak Inc.'], 'Luxury Items': ['VoidFinery Retsekchish', 'Rayecha Enterprises', 'Galactic Couture', 'Infinity Elegance', 'XenoArtisan Prestige Ltd.', 'Tsubaksha Designs'], 'Weapons': ['Titan Arms', 'Latsenkor Tactical', 'Aletskiish Yahatsish', 'Helios Tsaachinshak', 'Upatishah Lipshik'], 'Equipment Parts': ['Lochechish Fabrication', 'Letohcha Lelkash', 'Shainah Forge', 'Cheke Shan Fabrication', 'Lahatsan Industries'], 'Fuel': ['Nashtochka Power', 'Tsipishan Fuels', 'Nishahak Propulsion Co.', 'Akoichuha Propulsion Co.', 'VoidStream Power', 'AetherCore Yecheshka']}
maloq_corporations = {'Organics': ['Andadru Harvest Ltd.', 'Aldakron Horizons', 'Nebula Corp.', 'BioFrontier Exports', 'Bakagor Corp.', 'Celestial Bloom Inc.'], 'Synthetics': ['FusionMold Dynamics', 'Gartan Kudatra', 'Zagnardu Ambakar', 'Dradat Industries', 'Plastech Industries', 'Dakadarr Dynamics'], 'Common Minerals': ['Asteroid Mining Corp.', 'Hyperion Oreworks', 'Deep Core Ventures', 'Derran Mining Corp.', 'VoidMiner Industries', 'Titan Balangak'], 'Rare Minerals': ['Meladza Bagarra', 'Darbo Corp.', 'Gongart Grantor', 'Langak Adegor', 'Bronakin Kmintura', 'Dark Matter Godoban'], 'Refined Minerals': ['Ardabon Refining Corp.', 'Kuragan Smelters', 'Aratog Smelters', 'Gondar Burdak', 'Hyperion Dangor', 'Agrank Ganaga'], 'Supplies': ['Solaris Solutions', 'Katanor Gundor', 'Universal Lotonga', 'Nova Goods', 'Kinzaza Kendilga', 'Albarga Gromag'], 'Medicine': ['Labaran BioSolutions', 'Galactic BioSolutions', 'NovaCure Badolka', 'Obbor Ltd.', 'Bedron Medical', 'Bolaner Medical'], 'Alcohol': ['Loddar Spirits Ltd.', 'Astro Reserve Wines', 'Void Spirits Brews', 'Lagarton Liquor Co.', 'Zenith Brewmasters', 'Infinity Distillers Inc.'], 'Technology Goods': ['Garond Electronics', 'Agedru Corp.', 'Zarran Corp.', 'XenoChip Devices', 'Aborag Systems Ltd.', 'Gragan Devices'], 'Luxury Items': ['XenoArtisan Masterworks', 'VoidFinery Opulence Corp.', 'Arkomaddan Buddar', 'Celestial Creations', 'Bodarken Jewelworks', 'Krakan Creations'], 'Weapons': ['Abragor Domkrak', 'Baldagr Armory', 'Gobarrak Armory', 'Blackstar Gloddar', 'Ironclad Industries', 'Krantor Arms'], 'Equipment Parts': ['NovaFrame Engineering', 'Barragar Gabanda', 'Adderak Drelak', 'Ogatak Forge', 'Gabarton Engineering', 'Zandar Kagerr'], 'Fuel': ['Kabadr Fuels', 'Gandok Kodag', 'Grobber Propulsion Co.', 'Argelar Fuels', 'Laksader Baksan', 'Branlandar Glatak']}


def generate_fei_name():
    starts = ["Aen", "Ail", "Al", "An", "Asa", "Ige", "Ila", "Il", "In", "Is", "La", "Li", "Ma", "Na", "Ola", "On",
              "Ra", "Ri", "Ta", "Uai"]
    mids = ["na", "ti", "la", "mi", "kai", "lli", "lo", "ro", "ni", "ya", "an", "to", "si", "li", "ri"]
    ends = ["ai", "li", "ra", "ya", "na", "ka", "ta", "po", "ro", "la"]

    first = random.choice(starts) + random.choice(mids) + random.choice(ends)
    if random.random() < 0.25:  # 25% chance for compound
        first += "-" + random.choice(starts) + random.choice(ends)

    last = random.choice(starts) + random.choice(mids) + random.choice(ends)
    if random.random() < 0.25:  # 25% chance for compound
        last += "-" + random.choice(starts) + random.choice(ends)
    return f"{first} {last}"


def generate_gaal_name():
    syllables = ["Aar", "Ka", "Be", "Dle", "No", "Lu", "Zaa", "Mo", "Ko", "Ve", "Nee", "Daa", "Ra", "Gaa", "Gaab",
                 "Lee", "Vin", "Mii", "Saa", "Bru", "Na", "Gre"]
    syllables2 = ["Ka", "Be", "Dle", "No", "Lu", "Zaa", "Mo", "Ko", "Ve", "Nee", "Daa", "Ra", "Gaa", "Gaab",
                 "Lee", "Vin", "Mii", "Saa", "Bru", "Na", "Gre"]
    suffixes = ["kra", "tag", "ro", "aka", "rla", "gra", "kli", "tan", "taak", "liik", "sta", "oon", "sha", "nek",
                "oor", "aat"]

    first = random.choice(syllables) + random.choice(syllables2).lower() + random.choice(suffixes)
    if random.random() < 0.3:
        first = first[:4] + "-" + first[4:]

    last = random.choice(syllables) + random.choice(syllables2).lower() + random.choice(suffixes)
    if random.random() < 0.3:
        last = last[:4] + "-" + last[4:]
    return f"{first} {last}"

def generate_maloq_name():
    starts = ["Ab", "Ag", "Bak", "Bal", "Bor", "Dar", "Gon", "Gra", "Kud", "Lag", "Zar"]
    mids = ["ra", "do", "ka", "ta", "lan", "gar", "don", "nak", "lek", "barg", "tro"]
    ends = ["gor", "dan", "br", "gr", "rak", "dru", "ban", "gak", "tor", "kar", "dron", "grom"]
    ends_2 = ["gor", "dan", "bar", "gar", "rak", "dru", "ban", "gak", "tor", "kar", "dron", "grom"]

    first = random.choice(starts) + (random.choice(mids) + random.choice(ends) if random.random() < 0.7 else random.choice(ends_2))
    last = random.choice(starts) + (random.choice(mids) + random.choice(ends) if random.random() < 0.7 else random.choice(ends_2))
    return f"{first} {last}"

def generate_peleng_name2():
    starts = {
        "sibilant": ["Uh", "Shu", "Sha", "Shai", "Ches", "Che", "Chush", "Tsa", "Tush", "Bush"],
        "plosive": ["Ayk", "Aha", "Apac", "Iht", "Nat", "Uh"],
        "soft": ["Ai", "Ally", "Lek", "Lya"]
    }

    mids = {
        "sibilant": ["sha", "shka", "sish", "tsak"],
        "plosive": ["tak", "pash", "pek", "lak"],
        "soft": ["ka", "chi", "kish"]
    }

    ends = {
        "sibilant": ["sha", "chan", "ish", "tsis", "shak", "shik", "shok", "ska"],
        "plosive": ["tka", "ak", "kach"],
        "soft": ["an", "ash", "osh"]
    }

    def choose_syllable(category, last_type=None):
        # Avoid repeating the same phoneme type twice
        available = [k for k in category.keys() if k != last_type]
        chosen_type = random.choice(available) if available else random.choice(list(category.keys()))
        syllable = random.choice(category[chosen_type])
        return syllable, chosen_type

    def create_name():
        first_start, type1 = choose_syllable(starts)
        mid, type2 = choose_syllable(mids, last_type=type1) if random.random() < 0.7 else ("", type1)
        end, _ = choose_syllable(ends, last_type=type2)
        return first_start + mid + end

    first = create_name()
    last = create_name()
    return f"{first} {last}"

def generate_peleng_name(syllable_count):
    starts_only = ['Che', 'Tsats', 'Lyak', 'Tsai', 'Lya', 'Chesh', 'Tsop', 'Lek', 'Tsok', 'Chiv', 'Lok', 'Suh', 'Shu',
                   'Nel', 'Peh', 'Ches', 'Sui', 'Shek', 'Cha', 'Nuk', 'Sei', 'Tsot', 'Sheh','Rah', 'Pehi' 'Pasha',
                   'Sisha', 'Shak', 'Uka', 'Po', 'Pru', 'Li', 'Han', 'Shup']

    starts = ['Ash', 'Che', 'Ti', 'Tsa', 'Sip', 'Lyak', 'Sut', 'Kas', 'Tsla', 'Bush', 'Ya', 'Ri', 'Ra', 'Pen', 'Ro', 'Tsai',
     'Lya', 'Rat', 'Sai', 'Tsaa', 'Rul', 'Tset', 'Ay', 'Nuh', 'Shet', 'Ve', 'Chesh', 'Ui', 'Tsop', 'Lek', 'Tsok', 'Rio',
     'Tsu', 'Let', 'A', 'Nats', 'Ret', 'Lo', 'Ih', 'Ye', 'Les', 'Ni', 'Uh', 'Its', 'Lip', 'Lel', 'Shai', 'La', 'Sit',
     'Chiv', 'Na', 'Te', 'Nu', 'Lok', 'Ha', 'Ray', 'Kin', 'Ta', 'Lik', 'Al', 'Ke', 'Uk', 'Chi', 'Nui', 'Suh', 'Shat',
     'Le', 'Ai', 'Ku', 'He', 'Lep', 'Shu', 'Nel', 'Sa', 'Peh', 'Ches', 'Sui', 'Ruh', 'Shek', 'Cha', 'Nuk', 'Sei', 'Tsot',
     'Ka', 'U', 'Sheh', 'Shup', 'Tsi', 'Tse', 'Sha', 'Rah', 'Pehi' 'Pasha', 'Sisha', 'Shak', 'Uka', 'Po', 'Pru', 'Li', 'Han']

    mids = ['pak', 'pek', 'kay', 'ses', 'sosh', 'si', 'pei', 'its', 'sih', 'sek', 'lot', 'akk', 'kuk', 'shu', 'sos',
            'tsay', 'tsen', 'chut', 'pa', 'ish', 'shtoch', 'llyas', 'int', 'han', 'tsom', 'chin', 'ra', 'pra', 'ats', 'tsi',
            'kesh', 'keh', 'pesh', 'sen', 'lyan', 'as', 'ui', 'ich', 'kish', 'che', 'hayt', 'shik', 'set', 'ah', 'at',
            'chush', 'sha', 'hai', 'ap', 'mar', 'koi', 'shis', 'tak', 'rem', 'ke', 'eshk', 'pel', 'hal', 'pash', 'lak',
            'shko', 'ech', 'an', 'tsash', 'bak', 'shit', 'chat', 'chish', 'tish', 'tsan', 'she', 'ske', 'chal', 'sesh',
            'chu', 'tsa', 'tsuh', 'kush', 'plat', 'eh', 'tsesh', 'tsok', 'tat', 'tsach', 'kit', 'say', 'shet', 'pai',
            'hat', 'toh', 'ka', 'sho', 'hot', 'tse', 'na', 'sap', 'yah', 'al', 'lets', 'pish', 'ek', 'chesh', 'tsish',
            'tik', 'hi', 'vin', 'chet', 'tsin', 'ship', 'ko', 'hit', 'shikk', 'chik', 'tsik', 'ha']


    ends = ['li', 'sta', 'cha', 'pek', 'kah', 'is', 'la', 'lak', 'yecha', 'kla', 'kesh', 'ska', 'hats', 'ha', 'an', 'shi',
            'sak', 'ka', 'chak', 'hak', 'skis', 'shak', 'a', 'slis', 'yak', 'sish', 'chish', 'ash', 'kor', 'kis', 'tsis',
            'lish', 'ak', 'kish', 'ek', 'shik', 'sis', 'plits', 'kiish', 'kan', 'ah', 'sent', 'lan', 'tsak', 'ish', 'lya'
            'chik', 'pan', 'tank', 'shan', 'san', 'han', 'tash', 'ta', 'sha', 'nak', 'ik', 'nash', 'pru', 'skish', 'ya',
            'kash', 'nah', 'tak', 'ats', 'shpak', 'nets', 'tsa', 'tlan', 'tsak', 'kach']

    # too many S letters but not Sh

    consonant_mids = {'k': 0.22, 'ts': 0.15, 'sh': 0.129, 'h': 0.083, 'n': 0.079, 'l': 0.076, 'ch': 0.063, 's': 0.051,
                      't': 0.046, 'p': 0.046, 'shk': 0.025, 'ly': 0.014, 'v': 0.005, 'm': 0.005, 'pl': 0.005, 'sht': 0.002}

    if syllable_count == 1:
        return random.choice(list(starts_only))
    elif syllable_count == 2:
        return join_syllables([random.choice(list(starts)), random.choice(list(ends))])
    elif syllable_count == 3:
        return join_syllables([random.choice(list(starts)), random.choice(list(mids)), random.choice(list(ends))])
    else:  # syllable_count == 4
        return join_syllables([random.choice(list(starts)), random.choice(list(mids)), random.choice(list(mids)), random.choice(list(ends))])

def generate_human_name():
    ethnicity = random.choice(["American-European", "Slavic", "Asian", "African", "Latino"])

    if ethnicity == "American-European":
        first = random.choice(
            ["John", "Emily", "Michael", "Sarah", "James", "Jessica", "David", "Ashley", "Daniel", "Lauren"])
        last = random.choice(
            ["Smith", "Johnson", "Brown", "Taylor", "Anderson", "Walker", "White", "Robinson", "Clark", "Lewis"])

    elif ethnicity == "Slavic":
        first = random.choice(
            ["Ivan", "Anya", "Mihail", "Katerina", "Boris", "Nina", "Dmitri", "Tatiana", "Alexei", "Irina"])
        last = random.choice(
            ["Petrov", "Ivanov", "Kuznetsov", "Smirnov", "Vasiliev", "Volkov", "Sokolov", "Romanov", "Morozov",
             "Kovalenko"])

    elif ethnicity == "Asian":
        first = random.choice(["Wei", "Hana", "Kenji", "Mei", "Satoshi", "Yuna", "Jin", "Aiko", "Takeshi", "Ling"])
        last = random.choice(
            ["Kim", "Yamamoto", "Zhang", "Park", "Chen", "Kobayashi", "Nguyen", "Tanaka", "Li", "Wong"])

    elif ethnicity == "African":
        first = random.choice(["Kwame", "Amina", "Jabari", "Zola", "Oba", "Imani", "Tariq", "Nia", "Chinedu", "Fatou"])
        last = random.choice(
            ["Okoye", "Adebayo", "Mensah", "Mbatha", "Ndlovu", "Diop", "Aminu", "Kamanzi", "Obasanjo", "Nyong'o"])

    elif ethnicity == "Latino":
        first = random.choice(
            ["Carlos", "Lucia", "Mateo", "Isabela", "Javier", "Camila", "Santiago", "Mariana", "Diego", "Valentina"])
        last = random.choice(
            ["Garcia", "Martinez", "Rodriguez", "Lopez", "Hernandez", "Torres", "Ramirez", "Sanchez", "Cruz",
             "Morales"])

    return f"{first} {last}"

# Create a list of syllable lists
#split_names = [split_into_syllables(name) for name in peleng_names]
#print(split_names) # Show the first 10 as a sample

names = []
for _ in range(1000):
    #print(generate_fei_name())
    #print(generate_gaal_name())
    #print(generate_maloq_name())

    choices = [1, 2, 3, 4]
    one = random.choice(choices)
    choices.remove(one)
    two = random.choice(choices)

    name1 = generate_peleng_name(one)
    name2 = generate_peleng_name(two)

    names.append(name1)
    names.append(name2)

    #print(name1 + " " + name2)
    #print(generate_human_name())
    #print()

print(analyze_consonant_frequencies(peleng_names, consonant_mids))

print(analyze_consonant_frequencies(names, consonant_mids))