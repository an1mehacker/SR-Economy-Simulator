import random
import secrets

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
    "Aikochak", "Aykhikka", "Alekhcha", "Aletskiish", "Allyasta", "Apacash", "Akhaicak", "Veremchushka", "Bushka", "Akoichukha",
    "Acikhak", "Ashkekhlak", "Ikhtishis", "Ikhtsichak", "Itsekhakka", "Yecheshka", "Ykushichan", "Ytsikash", "Ytsomakhak", "Kasatish",
    "Kakhitsak", "Kashikka", "Keshetskis", "Kintaksha", "Kushanak", "Lapashak", "Lakhatsan", "Lakhlyak", "Latsenkor", "Latsikakh",
    "Latsokka", "Lekeshkis", "Lelkash", "Leprakan", "Leptank", "Lesintsak", "Letokhcha", "Letsekka", "Letsishacha", "Letsetskish",
    "Lik Senats", "Li Peshka", "Lipshik", "Lishitsta", "Lok Khanka", "Lochechish", "Lyakshitish", "Lyasoshik", "Lyakhitsak", "Lya Chishkan",
    "Natsekkish", "Nachiksha", "Nashtochka", "Natschak", "Nelishek", "Nishakhak", "Nuitsachka", "Nukitsak", "Nuktiksha", "Nukhapash",
    "Nuceshka-Li", "Penechaska", "Pekhankash", "Rayecha", "Raykhan", "Ratlotska", "Rakhotsis", "Retsekchish", "Riohats", "Ritsashka",
    "Richetsis", "Roplatska", "Rulyakha", "Rukhalats", "Sainashi", "Savinka", "Seisoska", "Sipatska", "Sitsheplits", "Suitsanka",
    "Sukhatsan", "Sutsaykish", "Takasha", "Tashatak", "Tetsishkis", "Titsinchak", "Uikushka", "Ukayshak", "Ulyankishla", "Upatishakh",
    "Ukhaytsent", "Ukhehechish", "Ukhtaksha", "Ukshutak", "Utsaykhan", "Utsankha", "Utselaksha", "Utsetsashik", "Utseshli", "Utsukhek",
    "Uchatslis", "Uchulish", "Ushikka", "Ushipanka", "Ushkopek", "Ushotsis", "Khanachish", "Khekeshka", "Khetsetak", "Tsaikakh",
    "Tsaishiska", "Tsakla", "Tsalotsha", "Tsamartash", "Tsetsha-Pru", "Tsaachinshak", "Tseppish Tseppan", "Tsetsenash", "Tsetshutka",
    "Tsipaishi", "Tsipeksha", "Tsipishan", "Tsishiska", "Tslataksha", "Tsokakhak", "Tsopshik", "Tsotskekesh", "Tsubaksha", "Tsukali",
    "Tsukeshka", "Cheke Shan", "Chespeika", "Checekish", "Cheshuikis", "Chikkash", "Chappelli", "Chivchalka", "Shainakh", "Shatapan", "Shatsak",
    "Shekecha", "Shekitsak", "Shekhlak", "Shetsenka", "Shetsaplan", "Shukukkha", "Yakitseska", "Yatatchik", "Yakhatsish", "Yatsikka"
]


people_names = [
    "August", "Adam", "Admiral", "Aqua", "Albatross", "Albinos", "Altair", "Amber", "Anaconda",
    "Andromeda", "Anubis", "Apollon", "Arbiter", "Argo", "Artemis", "Archimede", "Astra", "Atoll",
    "Afina", "Aphrodite", "Blatosphera", "Venus", "Viktoriya",
    "Galileo", "Ganover", "Gauss", "Gera", "Hercules", "Germes", "Gerodot",
    "Gertsog", "Gibraltar", "Giant", "Gladiolus", "Hilly", "Delphin", "Dervish",  "Dionis", "Claus",
    "Druid", "Dune", "Cardinal", "Zvezda", "Emerald", "Illusion", "Immodium", "In i Yan",
    "Katana", "Kolibri", "Comet", "Crystal", "Legionnaire", "Liliya", "Lord", "Luna",
    "Luch", "May", "Malachite", "Mercury", "Merlin", "Minor",
    "Minotaur", "Mir", "Monarch", "Monarch", "Muse", "Hope", "Narcys", "Neptune", "Odyssey",
    "Ocean", "Octave", "Olimp", "Orel", "Orion", "Osiris", "Paradise", "Paris", "Patagonia", "Penelope",
    "Omicron Persei", "Perun", "Pluton", "Pathway", "Poseidon", "President", "Procurator",
    "Prometheus", "Prophet", "Put", "Rubin", "Mermaid", "Knight", "Senator",
    "Consensus", "Stranger", "Strela", "Destiny", "Sphinx", "Tacit", "Titan", "Topaz", "Tornado",
    "Troy", "Troubadour", "Work", "Pharaoh", "Phoenix", "Fialka", "Philosopher", "Peasant", "Khronos",
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
        "Specter Reload Solutions", "Infinity Power Systems", "Orion ChargeTech", "Blackhole Energy Co.", "Solaris Fuelworks"
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

gaalian_corporations_repeated = {'Organics': ['Verdant Muaayri', 'Varoola Exports', 'Kaara-il Bounty', 'Keentam Farms Inc.', 'Aadimra Corp.', 'Geoogra Farms Inc.'], 'Synthetics': ['Doolka Ltd.', 'Lao-oga Dynamics', 'Kra-abbor Dynamics', 'Exo Ltd.', 'NeoPolymer Keptaak', 'Kiinakle Luulia'], 'Common Minerals': ['Galactic Assela-an', 'Loo-hi Viamaat', 'Hyperion Lei-ima', 'Arne-em Agno-on', 'Universal Metals Ltd.', 'Kirkoya Excavations'], 'Rare Minerals': ['ExoRare Prisms', 'Istaan Corp.', 'Moolkar Naamika', 'Meengar Metals', 'Koo-ba Nekseer', 'Black Star Gaabebra'], 'Refined Minerals': ['Noorak Lenliiko', 'Dliipar Lo-osta', 'Lamaait Goostakli', 'Asooleun Kineela', 'XenoSteel Glassworks', 'Infinity Metallurgy'], 'Supplies': ['Dintaak Deerkia', 'Dleesna Inc.', 'Deekra Supply Chain', 'Liinka Braanakli', 'Kaasayar Keggeeba', 'Gaam-it Asaamrik'], 'Medicine': ['XenoMeds Medical Systems', 'Waitem Luikaast', 'Ilooni Pharmaceuticals', 'Galactic Solutions', 'Solaris Ariilka', 'Infinity Noola'], 'Alcohol': ['Stellar Brews', 'Nova Aleworks', 'Aasika Spirits Ltd.', 'Daankesa Spirits Ltd.', 'Zdaani Distillers Inc.', 'Astro Brewmasters'], 'Technology Goods': ['Gaal-la Devices', 'Zaamal Corp.', 'Gusarovka Gloobar', 'Zenith Digital Solutions', 'Celestial Electronics', 'Vinfaal Da-aroka'], 'Luxury Items': ['Deep Space Jewelworks', 'Hyperion Luxury Goods', 'Zeo-orin Masterworks', 'Kaalatka Jewelworks', 'Ga-aprog Luxury Goods', 'Celestial Prestige Ltd.'], 'Weapons': ['Blackstar No-omota', 'Dark Matter Defense Systems', 'Voidfire Arsenal', 'NovaCorp Akraak', 'Gneepi Aina-ant', 'Do-opra Strike Solutions'], 'Equipment Parts': ['Aarkis Gear Systems', 'Bunagraak Mechanics', 'Orion Ara-aga', 'Titan Mini-ir', 'Aegis Parts & Repair', 'Beelag Giraagma'], 'Fuel': ['Naavufra Fuels', 'Kliinna Miirka', 'HyperCharge Systems', 'Ara-at Fuelworks', 'Demeera Energy', 'VoidStream Fuels']}
faeyan_corporations_repeated = {'Organics': ['Matolli Bounty', 'Nebula Horizons', 'Teklinai Farms Inc.', 'Uania Star Agri', 'Solaris Iklutai', 'Lasigo Atilanni'], 'Synthetics': ['NanoWeave Illiaka', 'Exo Industries', 'OmniForm Ltd.', 'Ilanki-Ra Conglomerate', 'Quantum Synthetics', 'Plastech Materials'], 'Common Minerals': ['VoidMiner Conglomerate', 'Asteroid Oreworks', 'Olrai-Po Industries', 'Hyperion Aenteri', 'Laistan Ventures', 'Solaris Oreworks'], 'Rare Minerals': ['Quantum Ankaio', 'HyperCore Prisms', 'Nekki-Naki Elements', 'Celestial Corp.', 'Asaffi Anilkaya', 'Galactic Liami Ra'], 'Refined Minerals': ['Oakani Tillaya', 'Hyperion Foundries', 'Zenith Smelters', 'Lannati Aklikli', 'Lamikka Glassworks', 'Nova Igeida'], 'Supplies': ['Deep Space Goods', 'Universal Ofelaki', 'Oaronna Networks', 'Nannori Corp.', 'VoidSurvival Supply Chain', 'Hyperion Afaiyan'], 'Medicine': ['Zenith Ralanni', 'Alakai Solutions', 'Celestial Pharmaceuticals', 'Solaris Biotech', 'Hyperion Itilak', 'Lakemli Industries'], 'Alcohol': ['Solaris Distillers Inc.', 'Void Spirits Attolki', 'Celestial Distillers Inc.', 'Zenith Spirits Ltd.', 'Nikoria Reserve Wines', 'Ranimai Spirits Ltd.'], 'Technology Goods': ['Infinity Inc.', 'Celestial Industries', 'Nillaik Systems Ltd.', 'Voidware Devices', 'Inilai Electronics', 'Interstellar Circuits'], 'Luxury Items': ['Talaik Luxury Goods', 'Takiani Designs', 'Otialli Designs', 'Deep Space Designs', 'Minniati Prestige Ltd.', 'VoidFinery Couture'], 'Weapons': ['NovaCorp Industries', 'Eclipse Osnaris', 'Titan Arsenal', 'Dark Matter Arsenal', 'Matali-Va Arsenal', 'Ares Riania-Anro'], 'Equipment Parts': ['Talikia Nilami-Rak', 'Hyperion Forge', 'VoidWorks Engineering', 'Rokoyali Leinami', 'Neptune Parts & Repair', 'Ilifa Laoti-Ra'], 'Fuel': ['NovaCharge Uailai', 'Helios Allista', 'Memilki Energy', 'Ailtik Systems', 'HyperCharge Energy Systems', 'Liliam Propulsion Co.']}
human_corporations_repeated = {'Organics': ['Gaia Provisions', 'Bootes Bloom Inc.', 'Strela Corp.', 'BioFrontier Malachite', 'Eden Exports', 'Element May'], 'Synthetics': ['FusionMold Industries', 'Exo Corp.', 'Troy Dynamics', 'HyperPlast Corp.', 'NanoWeave Giant', 'OmniForm Materials'], 'Common Minerals': ['Titan Industries', 'Legionnaire Conglomerate', 'Heir Extractors', 'Solaris Ventures', 'Hyperion Extractors', 'Universal Ventures'], 'Rare Minerals': ['Singularity Minerals', 'Galactic Prisms', 'Quantum Prisms', 'HyperCore SunriseBrother Rabbit', 'Elixir Crystal', 'Black Star Claus'], 'Refined Minerals': ['Celestial Archimede', 'Gerodot Conglomerate', 'Prof Stranger', 'XenoSteel Astra', 'Solaris Industries', 'Cardinal Glassworks'], 'Supplies': ['Infinity Logistics', 'Hyperion Supply Chain', 'Elf Prophet', 'Admiral Provisions', 'Xeno Provisions', 'Universal Neptune'], 'Medicine': ['ElSent Medical Systems', 'Hyperion Biotech', 'VoidMed Solutions', 'Katana Medical Systems', 'XenoMeds Ltd.', 'NovaCure Medical'], 'Alcohol': ['Nova Immodium', 'Dionis Distillers Inc.', 'Altair Distillery', 'Zenith Reserve Wines', 'Infinity Galileo', 'Hyperion Brewmasters'], 'Technology Goods': ['Celestial Industries', 'Lord Technologies', 'Titan Industries', 'Hope Systems Ltd.', 'Hyperion Devices', 'Infinity Industries'], 'Luxury Items': ['Nova Mir', 'President Creations', 'XenoArtisan Designs', 'Albinos Prestige Ltd.', 'Hilly Spiker', 'Comet Couture'], 'Weapons': ['Ironclad Arms', 'Ares Arms', 'Titan Munitions', 'Blackstar Procurator', 'Adam Arsenal', 'Ellada Strike Solutions'], 'Equipment Parts': ['Put Delphin', 'Kolibri Mechanics', 'Zenith Mechanics', 'Titan Forgeworks', 'Assol Gear Systems', 'Hyperion Engineering'], 'Fuel': ['NovaCharge Power', 'VoidStream Energy', 'Justice Minor', 'Helios Fuels', 'Mercury Systems', 'Edip Power']}
peleng_corporations_repeated = {'Organics': ['Solaris Savinka', 'BioFrontier Chikkash', 'Verdant Exports', 'Celestial Bounty', 'Nova Naturals', 'Letsekka Tashatak'], 'Synthetics': ['Nachiksha Materials', 'GalaxiPlast Nuitsachka', 'Kakhitsak Synthetics', 'Exo Industries', 'Veremchushka Conglomerate', 'Quantum Materials'], 'Common Minerals': ['Tsaishiska Shekitsak', 'Utsukhek Suitsanka', 'Tseppish Tseppan Ventures', 'Tsaikakh Metals Ltd.', 'Bushka Mining Corp.', 'Tsishiska Itsekhakka'], 'Rare Minerals': ['Singularity Shukukkha', 'Shatapan Letsetskish', 'Roplatska Metals', 'Quantum Metals', 'Lapashak Metals', 'Rukhalats Elementals'], 'Refined Minerals': ['Cheshuikis Refining Corp.', 'Hyperion Tsamartash', 'Yakitseska Aykhikka', 'Ratlotska Refining Corp.', 'Quantum Tsakla', 'Lishitsta Glassworks'], 'Supplies': ['Lyakshitish Essentials', 'Shekhlak Logistics', 'Takasha Ltd.', 'Latsikakh Essentials', 'Ikhtsichak Kintaksha', 'Keshetskis Provisions'], 'Medicine': ['Lyakhitsak Pharmaceuticals', 'Khanachish Ashkekhlak', 'Galactic Allyasta', 'Akhaicak Solutions', 'XenoMeds Industries', 'Celestial Medical Systems'], 'Alcohol': ['Nukhapash Spirits Ltd.', 'Celestial Liquor Co.', 'Zenith Liquor Co.', 'Yatatchik Brews', 'Sutsaykish Letsishacha', 'Kushanak Spirits Ltd.'], 'Technology Goods': ['Yatsikka Digital Solutions', 'Utsetsashik Devices', 'Tsotskekesh Inc.', 'Interstellar Sukhatsan', 'Hyperion Devices', 'Titsinchak Inc.'], 'Luxury Items': ['VoidFinery Retsekchish', 'Rayecha Enterprises', 'Galactic Couture', 'Infinity Elegance', 'XenoArtisan Prestige Ltd.', 'Tsubaksha Designs'], 'Weapons': ['Titan Arms', 'Latsenkor Tactical', 'Ironclad Arms', 'Aletskiish Yakhatsish', 'Helios Tsaachinshak', 'Upatishakh Lipshik'], 'Equipment Parts': ['Lochechish Fabrication', 'Letokhcha Lelkash', 'Shainakh Forge', 'Cheke Shan Fabrication', 'Lakhatsan Industries', 'Zenith Mechanics'], 'Fuel': ['Nashtochka Power', 'Tsipishan Fuels', 'Nishakhak Propulsion Co.', 'Akoichukha Propulsion Co.', 'VoidStream Power', 'AetherCore Yecheshka']}
maloq_corporations_repeated = {'Organics': ['Andadru Harvest Ltd.', 'Aldakron Horizons', 'Nebula Corp.', 'BioFrontier Exports', 'Bakagor Corp.', 'Celestial Bloom Inc.'], 'Synthetics': ['FusionMold Dynamics', 'Gartan Kudatra', 'Zagnardu Ambakar', 'Dradat Industries', 'Plastech Industries', 'Dakadarr Dynamics'], 'Common Minerals': ['Asteroid Mining Corp.', 'Hyperion Oreworks', 'Deep Core Ventures', 'Derran Mining Corp.', 'VoidMiner Industries', 'Titan Balangak'], 'Rare Minerals': ['Meladza Bagarra', 'Darbo Corp.', 'Gongart Grantor', 'Langak Adegor', 'Bronakin Kmintura', 'Dark Matter Godoban'], 'Refined Minerals': ['Ardabon Refining Corp.', 'Kuragan Smelters', 'Aratog Smelters', 'Gondar Burdak', 'Hyperion Dangor', 'Agrank Ganaga'], 'Supplies': ['Solaris Solutions', 'Katanor Gundor', 'Universal Lotonga', 'Nova Goods', 'Kinzaza Kendilga', 'Albarga Gromag'], 'Medicine': ['Labaran BioSolutions', 'Galactic BioSolutions', 'NovaCure Badolka', 'Obbor Ltd.', 'Bedron Medical', 'Bolaner Medical'], 'Alcohol': ['Loddar Spirits Ltd.', 'Astro Reserve Wines', 'Void Spirits Brews', 'Lagarton Liquor Co.', 'Zenith Brewmasters', 'Infinity Distillers Inc.'], 'Technology Goods': ['Garond Electronics', 'Agedru Corp.', 'Zarran Corp.', 'XenoChip Devices', 'Aborag Systems Ltd.', 'Gragan Devices'], 'Luxury Items': ['XenoArtisan Masterworks', 'VoidFinery Opulence Corp.', 'Arkomaddan Buddar', 'Celestial Creations', 'Bodarken Jewelworks', 'Krakan Creations'], 'Weapons': ['Abragor Domkrak', 'Baldagr Armory', 'Gobarrak Armory', 'Blackstar Gloddar', 'Ironclad Industries', 'Krantor Arms'], 'Equipment Parts': ['NovaFrame Engineering', 'Barragar Gabanda', 'Adderak Drelak', 'Ogatak Forge', 'Gabarton Engineering', 'Zandar Kagerr'], 'Fuel': ['Kabadr Fuels', 'Gandok Kodag', 'Grobber Propulsion Co.', 'Argelar Fuels', 'Laksader Baksan', 'Branlandar Glatak']}

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
peleng_corporations = {'Organics': ['Solaris Savinka', 'BioFrontier Chikkash', 'Verdant Exports', 'Celestial Bounty', 'Nova Naturals', 'Letsekka Tashatak'], 'Synthetics': ['Nachiksha Materials', 'GalaxiPlast Nuitsachka', 'Kakhitsak Synthetics', 'Veremchushka Conglomerate', 'Quantum Materials'], 'Common Minerals': ['Tsaishiska Shekitsak', 'Utsukhek Suitsanka', 'Tseppish Tseppan Ventures', 'Tsaikakh Metals Ltd.', 'Bushka Mining Corp.', 'Tsishiska Itsekhakka'], 'Rare Minerals': ['Singularity Shukukkha', 'Shatapan Letsetskish', 'Roplatska Metals', 'Quantum Metals', 'Lapashak Metals', 'Rukhalats Elementals'], 'Refined Minerals': ['Cheshuikis Refining Corp.', 'Hyperion Tsamartash', 'Yakitseska Aykhikka', 'Ratlotska Refining Corp.', 'Quantum Tsakla', 'Lishitsta Glassworks'], 'Supplies': ['Lyakshitish Essentials', 'Shekhlak Logistics', 'Takasha Ltd.', 'Latsikakh Essentials', 'Ikhtsichak Kintaksha', 'Keshetskis Provisions'], 'Medicine': ['Lyakhitsak Pharmaceuticals', 'Khanachish Ashkekhlak', 'Galactic Allyasta', 'Akhaicak Solutions', 'XenoMeds Industries', 'Celestial Medical Systems'], 'Alcohol': ['Nukhapash Spirits Ltd.', 'Celestial Liquor Co.', 'Zenith Liquor Co.', 'Yatatchik Brews', 'Sutsaykish Letsishacha', 'Kushanak Spirits Ltd.'], 'Technology Goods': ['Yatsikka Digital Solutions', 'Utsetsashik Devices', 'Tsotskekesh Inc.', 'Interstellar Sukhatsan', 'Titsinchak Inc.'], 'Luxury Items': ['VoidFinery Retsekchish', 'Rayecha Enterprises', 'Galactic Couture', 'Infinity Elegance', 'XenoArtisan Prestige Ltd.', 'Tsubaksha Designs'], 'Weapons': ['Titan Arms', 'Latsenkor Tactical', 'Aletskiish Yakhatsish', 'Helios Tsaachinshak', 'Upatishakh Lipshik'], 'Equipment Parts': ['Lochechish Fabrication', 'Letokhcha Lelkash', 'Shainakh Forge', 'Cheke Shan Fabrication', 'Lakhatsan Industries'], 'Fuel': ['Nashtochka Power', 'Tsipishan Fuels', 'Nishakhak Propulsion Co.', 'Akoichukha Propulsion Co.', 'VoidStream Power', 'AetherCore Yecheshka']}
maloq_corporations = {'Organics': ['Andadru Harvest Ltd.', 'Aldakron Horizons', 'Nebula Corp.', 'BioFrontier Exports', 'Bakagor Corp.', 'Celestial Bloom Inc.'], 'Synthetics': ['FusionMold Dynamics', 'Gartan Kudatra', 'Zagnardu Ambakar', 'Dradat Industries', 'Plastech Industries', 'Dakadarr Dynamics'], 'Common Minerals': ['Asteroid Mining Corp.', 'Hyperion Oreworks', 'Deep Core Ventures', 'Derran Mining Corp.', 'VoidMiner Industries', 'Titan Balangak'], 'Rare Minerals': ['Meladza Bagarra', 'Darbo Corp.', 'Gongart Grantor', 'Langak Adegor', 'Bronakin Kmintura', 'Dark Matter Godoban'], 'Refined Minerals': ['Ardabon Refining Corp.', 'Kuragan Smelters', 'Aratog Smelters', 'Gondar Burdak', 'Hyperion Dangor', 'Agrank Ganaga'], 'Supplies': ['Solaris Solutions', 'Katanor Gundor', 'Universal Lotonga', 'Nova Goods', 'Kinzaza Kendilga', 'Albarga Gromag'], 'Medicine': ['Labaran BioSolutions', 'Galactic BioSolutions', 'NovaCure Badolka', 'Obbor Ltd.', 'Bedron Medical', 'Bolaner Medical'], 'Alcohol': ['Loddar Spirits Ltd.', 'Astro Reserve Wines', 'Void Spirits Brews', 'Lagarton Liquor Co.', 'Zenith Brewmasters', 'Infinity Distillers Inc.'], 'Technology Goods': ['Garond Electronics', 'Agedru Corp.', 'Zarran Corp.', 'XenoChip Devices', 'Aborag Systems Ltd.', 'Gragan Devices'], 'Luxury Items': ['XenoArtisan Masterworks', 'VoidFinery Opulence Corp.', 'Arkomaddan Buddar', 'Celestial Creations', 'Bodarken Jewelworks', 'Krakan Creations'], 'Weapons': ['Abragor Domkrak', 'Baldagr Armory', 'Gobarrak Armory', 'Blackstar Gloddar', 'Ironclad Industries', 'Krantor Arms'], 'Equipment Parts': ['NovaFrame Engineering', 'Barragar Gabanda', 'Adderak Drelak', 'Ogatak Forge', 'Gabarton Engineering', 'Zandar Kagerr'], 'Fuel': ['Kabadr Fuels', 'Gandok Kodag', 'Grobber Propulsion Co.', 'Argelar Fuels', 'Laksader Baksan', 'Branlandar Glatak']}
