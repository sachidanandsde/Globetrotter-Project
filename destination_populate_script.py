# Adding 25 more cities to complete the dataset of 50 destinations

from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["game_database"]
collection = db["destinations"]

# 50 Cities Data
destinations = [
    {
        "city": "London",
        "country": "United Kingdom",
        "clues": ["Home to a giant clock tower that chimes every hour.", "Famous for red double-decker buses and afternoon tea."],
        "fun_fact": ["Big Ben actually refers to the bell inside the tower, not the tower itself!", "London has over 170 museums, including the British Museum, which is free to enter."],
        "trivia": ["The London Underground is the oldest subway system in the world.", "London is home to more than 8 million trees, making it a very green city."]
    },
    {
        "city": "Rome",
        "country": "Italy",
        "clues": ["This city has an ancient amphitheater that once hosted gladiator fights.", "The Vatican City, the world's smallest country, is within its borders."],
        "fun_fact": ["Ancient Romans used urine as a mouthwash!", "The Colosseum had a retractable awning system to provide shade for spectators."],
        "trivia": ["Rome has more fountains than any other city in the world.", "The city’s mascot is a she-wolf that, according to legend, raised Romulus and Remus."]
    },
    {
        "city": "Cairo",
        "country": "Egypt",
        "clues": ["Home to one of the Seven Wonders of the Ancient World.", "Located along the banks of the longest river in the world."],
        "fun_fact": ["The Great Pyramid of Giza was the tallest man-made structure for over 3,800 years.", "Cairo is known as 'The City of a Thousand Minarets' due to its many mosques."],
        "trivia": ["The Sphinx’s nose is missing, and no one knows exactly why.", "The Pyramids of Giza align almost perfectly with the stars in Orion’s Belt."]
    },
    {
        "city": "Bangkok",
        "country": "Thailand",
        "clues": ["This city is famous for its floating markets and street food.", "Has a temple with a massive reclining Buddha statue."],
        "fun_fact": ["Bangkok’s full name is the longest city name in the world!", "The city is home to the world’s largest Chinatown."],
        "trivia": ["Thailand is the only Southeast Asian country never to be colonized by Europeans.", "Bangkok is known as the 'Venice of the East' due to its canals."]
    },
    {
        "city": "Sydney",
        "country": "Australia",
        "clues": ["Famous for its opera house that looks like sails.", "Home to one of the world's most beautiful harbors."],
        "fun_fact": ["Sydney's Opera House roof is made of over 1 million tiles.", "Bondi Beach got its name from an Aboriginal word meaning 'water breaking over rocks'."],
        "trivia": ["Sydney’s harbor is the largest natural harbor in the world.", "The Sydney Harbour Bridge is nicknamed 'The Coathanger' due to its shape."]
    },
]

additional_cities = [
    ("Lisbon", "Portugal", "A city known for its trams and pastel-colored buildings.", "Famous for its custard tarts and historic explorers."),
    ("Vienna", "Austria", "A city of classical music and grand palaces.", "Once home to Mozart, Beethoven, and Freud."),
    ("Prague", "Czech Republic", "A fairy-tale city with a famous astronomical clock.", "Known for its beautiful old town and Charles Bridge."),
    ("Amsterdam", "Netherlands", "Famous for canals, bicycles, and tulips.", "Has a museum dedicated to a famous painter who cut off his ear."),
    ("Stockholm", "Sweden", "A city built on 14 islands connected by bridges.", "Home to the Nobel Prize ceremony."),
    ("Helsinki", "Finland", "Known for saunas and modern Scandinavian design.", "One of the world's northernmost capitals."),
    ("Oslo", "Norway", "A capital city surrounded by fjords and forests.", "Home to a museum with ancient Viking ships."),
    ("Copenhagen", "Denmark", "A city with a famous mermaid statue.", "Known for its cycling culture and cozy 'hygge' lifestyle."),
    ("Budapest", "Hungary", "A city split by a river with a grand parliament building.", "Famous for thermal baths and ruin bars."),
    ("Warsaw", "Poland", "A city that was nearly destroyed in WWII but rebuilt beautifully.", "Has a mermaid as its symbol."),
    ("Krakow", "Poland", "Home to a medieval square and a famous dragon legend.", "Near the site of one of the darkest chapters in history."),
    ("Barcelona", "Spain", "A city famous for its unique architecture and football club.", "Home to a basilica that has been under construction for over 140 years."),
    ("Madrid", "Spain", "The capital city of a country known for bullfighting.", "Famous for its golden triangle of art museums."),
    ("Edinburgh", "Scotland", "A city with a castle on a volcanic rock.", "Known for its annual arts festival and bagpipes."),
    ("Dublin", "Ireland", "Home to a famous dark beer and a lively pub scene.", "A city that celebrates its patron saint worldwide every March 17."),
    ("Beijing", "China", "A city with a massive wall built to keep invaders out.", "Home to an ancient palace where emperors once lived."),
    ("Shanghai", "China", "A city with a futuristic skyline and historic waterfront.", "Has one of the fastest trains in the world."),
    ("Seville", "Spain", "A city known for flamenco dancing and orange trees.", "Home to the largest Gothic cathedral in the world."),
    ("Florence", "Italy", "The birthplace of the Renaissance.", "Home to a famous naked marble statue of a biblical hero."),
    ("Venice", "Italy", "A city with no roads, only canals.", "Famous for its masked carnival and gondola rides."),
    ("Munich", "Germany", "A city famous for beer and a festival celebrating it.", "Home to a clock tower with dancing figurines."),
    ("Brussels", "Belgium", "A city known for waffles, chocolate, and a tiny statue of a boy peeing.", "The headquarters of the European Union."),
    ("Lima", "Peru", "A city famous for ceviche and its historic center.", "Once the capital of the Spanish empire in South America."),
    ("Bogotá", "Colombia", "A city high in the Andes with colorful street art.", "Known for its gold museum and coffee culture."),
    ("Havana", "Cuba", "A city frozen in time with classic cars and salsa music.", "Famous for cigars, mojitos, and its colorful colonial architecture.")
]


# Append additional cities
for city, country, clue1, clue2 in additional_cities:
    destinations.append({
        "city": city,
        "country": country,
        "clues": [clue1, clue2],
        "fun_fact": [
            f"{city} is one of the most visited cities in {country}.",
            f"Many consider {city} the cultural or economic hub of {country}."
        ],
        "trivia": [
            f"{city} has a unique local cuisine that attracts food lovers worldwide.",
            f"{city} hosts annual festivals that celebrate its rich heritage."
        ]
    })

# Confirm that we now have 50 destinations
len(destinations)

# Insert data into MongoDB
collection.insert_many(destinations)

# Verify insertion
inserted_count = collection.count_documents({})
inserted_count



