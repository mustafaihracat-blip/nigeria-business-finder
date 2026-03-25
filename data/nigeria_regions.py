"""
Nigeria - Bölgeler ve Büyük Şehirler
"""

NIGERIA_REGIONS = {
    "North West": {
        "states": ["Kano", "Kaduna", "Katsina", "Sokoto", "Zamfara", "Kebbi", "Jigawa"],
        "major_cities": ["Kano", "Kaduna", "Katsina", "Sokoto", "Birnin Kebbi", "Gusau", "Dutse"]
    },
    "North East": {
        "states": ["Borno", "Adamawa", "Bauchi", "Gombe", "Taraba", "Yobe"],
        "major_cities": ["Maiduguri", "Yola", "Bauchi", "Gombe", "Jalingo", "Damaturu"]
    },
    "North Central": {
        "states": ["Abuja (FCT)", "Niger", "Benue", "Kogi", "Kwara", "Nassarawa", "Plateau"],
        "major_cities": ["Abuja", "Minna", "Makurdi", "Lokoja", "Ilorin", "Lafia", "Jos"]
    },
    "South West": {
        "states": ["Lagos", "Ogun", "Oyo", "Osun", "Ondo", "Ekiti"],
        "major_cities": ["Lagos", "Abeokuta", "Ibadan", "Osogbo", "Akure", "Ado-Ekiti"]
    },
    "South East": {
        "states": ["Anambra", "Imo", "Enugu", "Ebonyi", "Abia"],
        "major_cities": ["Onitsha", "Owerri", "Enugu", "Abakaliki", "Umuahia"]
    },
    "South South": {
        "states": ["Rivers", "Delta", "Cross River", "Akwa Ibom", "Edo", "Bayelsa"],
        "major_cities": ["Port Harcourt", "Warri", "Calabar", "Uyo", "Benin City", "Yenagoa"]
    }
}

# Tüm şehirleri düz liste olarak al
ALL_CITIES = []
for region, data in NIGERIA_REGIONS.items():
    for city in data["major_cities"]:
        ALL_CITIES.append({
            "city": city,
            "region": region,
            "states": data["states"]
        })
