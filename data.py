# data.py
"""
NemaIQ - Data Module
Contains research data for 5 EPN species based on the research document.
"""

# ============================================================================
# SPECIES DATA - 5 Nematode Species
# ============================================================================

SPECIES_DATA = {
    "Heterorhabditis indica": {
        "name": "Heterorhabditis indica",
        "common_name": "H. indica",
        "soil_moisture": {"min": 8, "max": 18, "unit": "%"},
        "soil_temperature": {"min": 25, "max": 30, "unit": "°C"},
        "atmospheric_temperature": {"min": 15, "max": 35, "unit": "°C"},
        "ph": {"min": 5.5, "max": 7.0, "up_to": 9.2},
        "relative_humidity": {"min": 90, "unit": "%"},
        "preferred_soils": ["Sandy Loam", "Sand", "Light Clay-Sand"],
        "porosity": {"min": 40, "max": 60, "unit": "%"},
        "bulk_density": {"min": 1.15, "max": 1.30, "unit": "g/cm³"},
        "ec": {"min": 0.0, "max": 2.0, "unit": "dS/m", "decline_at": 4.0, "blocked_at": 30.0},
        "saline_tolerance": {"max": 50.0, "unit": "dS/m"},
        "sodic_tolerance": {"max": 12, "unit": "ESP%", "reduced_at": 15},
        "penetration_depth": {
            "typical": {"min": 10, "max": 20, "unit": "cm"},
            "sandy_optimum": 30,
            "clay": 5,
        },
        "pests": [
            "White Grubs",
            "Small Hive Beetle",
            "Fall Armyworm",
            "Tobacco Caterpillar",
            "Sweet Potato Weevil",
            "Cotton Bollworm",
            "Fungus Gnats",
            "Oriental Fruit Fly",
            "Root Weevils",
            "Banana Weevil Borer",
            "Diamondback Moth",
            "Termites",
        ],
        "description": "Heterorhabditis indica is a highly effective entomopathogenic nematode for controlling a wide range of soil-dwelling pests. It is known for its excellent host-finding ability and tolerance to various soil conditions. Effective against Coleoptera, Lepidoptera, Diptera and Orthoptera.",
        "icon": "🐛",
        "color": "#2E7D32",
    },
    "Steinernema siamkayai": {
        "name": "Steinernema siamkayai",
        "common_name": "S. siamkayai",
        "soil_moisture": {"min": 15, "max": 20, "unit": "%"},
        "soil_temperature": {"min": 25, "max": 35, "unit": "°C"},
        "atmospheric_temperature": {"min": 20, "max": 35, "unit": "°C"},
        "ph": {"min": 3.0, "max": 7.0, "up_to": 8.5},
        "relative_humidity": {"min": 90, "unit": "%"},
        "preferred_soils": ["Sand", "Sandy Loam", "Sandy Clay Loam"],
        "porosity": {"min": 45, "max": 52, "unit": "%"},
        "bulk_density": {"min": 1.25, "max": 1.45, "unit": "g/cm³"},
        "ec": {"min": 0.5, "max": 1.5, "unit": "dS/m", "decline_at": 3.0},
        "saline_tolerance": {"min": 15.0, "max": 20.0, "unit": "dS/m"},
        "sodic_tolerance": {"max": 8, "unit": "ESP%"},
        "penetration_depth": {
            "typical": {"min": 5, "max": 15, "unit": "cm"},
            "clay": 10,
        },
        "pests": [
            "Guava Fruit Fly",
            "Solanum Fruit Fly",
            "Oriental Fruit Fly",
            "Fall Armyworm",
            "Tobacco Caterpillar",
            "Corn Earworm",
            "Greater Wax Moth",
            "Fungus Gnats",
            "Diamondback Moth",
            "Common Cutworm",
        ],
        "description": "Steinernema siamkayai is a versatile entomopathogenic nematode species effective against a broad spectrum of pests. It performs well across a wide pH range and is particularly effective in sandy soils. Effective against Coleoptera, Lepidoptera, Diptera and Thysanoptera.",
        "icon": "🪱",
        "color": "#1565C0",
    },
    "Steinernema glaseri": {
        "name": "Steinernema glaseri",
        "common_name": "S. glaseri",
        "soil_moisture": {"min": 19, "max": 25, "unit": "%"},
        "soil_temperature": {"min": 20, "max": 28, "unit": "°C"},
        "atmospheric_temperature": {"min": 15, "max": 25, "unit": "°C"},
        "ph": {"min": 5.5, "max": 7.5, "up_to": 7.5},
        "relative_humidity": {"min": 90, "unit": "%"},
        "preferred_soils": ["Sand", "Fine Sand", "Loamy Sand"],
        "porosity": {"min": 46, "max": 54, "unit": "%"},
        "bulk_density": {"min": 1.15, "max": 1.35, "unit": "g/cm³"},
        "ec": {"min": 0.0, "max": 2.0, "unit": "dS/m", "decline_at": 4.0},
        "saline_tolerance": {"min": 30.0, "max": 50.0, "unit": "dS/m"},
        "sodic_tolerance": {"max": 10, "unit": "ESP%"},
        "penetration_depth": {
            "typical": {"min": 15, "max": 30, "unit": "cm"},
        },
        "pests": [
            "Black Cutworm",
            "Fall Armyworm",
            "Beet Armyworm",
            "Sod Webworms",
            "Codling Moth",
            "Peachtree Borer",
            "Lesser Peachtree Borer",
            "Squash Vine Borer",
            "Tawny Mole Cricket",
            "Southern Mole Cricket",
            "Short-winged Mole Cricket",
            "Cat Flea",
            "Dog Flea",
        ],
        "description": "Steinernema glaseri is a highly effective EPN species known for its deep penetration ability (15-30 cm). It performs well in coarse sandy soils and has excellent tolerance to saline conditions. Effective against a wide range of pests including mole crickets, cutworms, and fleas.",
        "icon": "🐛",
        "color": "#E65100",
    },
    "Steinernema carpocapsae": {
        "name": "Steinernema carpocapsae",
        "common_name": "S. carpocapsae",
        "soil_moisture": {"min": 10, "max": 20, "unit": "%"},
        "soil_temperature": {"min": 22, "max": 28, "unit": "°C"},
        "atmospheric_temperature": {"min": 15, "max": 28, "unit": "°C"},
        "ph": {"min": 5.0, "max": 8.0, "up_to": 8.0},
        "relative_humidity": {"min": 90, "unit": "%"},
        "preferred_soils": ["Sandy Loam", "Loam", "Silt Loam"],
        "porosity": {"min": 40, "max": 50, "unit": "%"},
        "bulk_density": {"min": 1.20, "max": 1.50, "unit": "g/cm³"},
        "ec": {"min": 0.0, "max": 2.5, "unit": "dS/m"},
        "saline_tolerance": {"max": 25.0, "unit": "dS/m"},
        "sodic_tolerance": {"max": 8, "unit": "ESP%"},
        "penetration_depth": {
            "typical": {"min": 3, "max": 5, "unit": "cm"},
        },
        "pests": [
            "Japanese Beetle",
            "European Chafer",
            "Northern Masked Chafer",
            "Southern Masked Chafer",
            "Black Vine Weevil",
            "Strawberry Root Weevil",
            "Diaprepes Root Weevil",
            "Western Corn Rootworm",
            "Northern Corn Rootworm",
            "Southern Corn Rootworm",
            "Fungus Gnats",
        ],
        "description": "Steinernema carpocapsae is one of the most widely used EPN species. It is highly effective against a variety of pests and is known for its ambush foraging strategy, making it particularly effective against surface-dwelling pests. Penetration depth is up to 5 cm.",
        "icon": "🪱",
        "color": "#7B1FA2",
    },
    "Heterorhabditis bacteriophora": {
        "name": "Heterorhabditis bacteriophora",
        "common_name": "H. bacteriophora",
        "soil_moisture": {"min": 15, "max": 25, "unit": "%"},
        "soil_temperature": {"min": 25, "max": 30, "unit": "°C"},
        "atmospheric_temperature": {"min": 18, "max": 32, "unit": "°C"},
        "ph": {"min": 6.0, "max": 7.5, "up_to": 7.5},
        "relative_humidity": {"min": 95, "unit": "%"},
        "preferred_soils": ["Sand", "Sandy Loam", "Loamy Sand"],
        "porosity": {"min": 43, "max": 55, "unit": "%"},
        "bulk_density": {"min": 1.15, "max": 1.35, "unit": "g/cm³"},
        "ec": {"min": 0.0, "max": 2.0, "unit": "dS/m"},
        "saline_tolerance": {"max": 35.0, "unit": "dS/m"},
        "sodic_tolerance": {"max": 12, "unit": "ESP%"},
        "penetration_depth": {
            "typical": {"min": 10, "max": 35, "unit": "cm"},
        },
        "pests": [
            "Japanese Beetle (Late 3rd Instar)",
            "May Beetles",
            "June Beetles",
            "Oriental Beetle",
            "Green June Beetle",
            "Banana Weevil Borer",
            "Greater Wax Moth",
        ],
        "description": "Heterorhabditis bacteriophora is a powerful EPN species known for its excellent host-finding ability and deep penetration (10-35 cm). It is particularly effective against white grubs, June beetles, and banana weevil borers. Requires relative humidity >95%.",
        "icon": "🐛",
        "color": "#00838F",
    },
}

# ============================================================================
# PEST MAPPING
# ============================================================================

# Build pest to species mapping
PEST_MAPPING = {}
for species, data in SPECIES_DATA.items():
    for pest in data["pests"]:
        if pest not in PEST_MAPPING:
            PEST_MAPPING[pest] = []
        PEST_MAPPING[pest].append(species)

# All unique pests
ALL_PESTS = sorted(PEST_MAPPING.keys())

# Species names list
SPECIES_NAMES = list(SPECIES_DATA.keys())

# Soil types (combined from all species)
SOIL_TYPES = sorted(
    set(
        soil
        for species in SPECIES_DATA.values()
        for soil in species["preferred_soils"]
    )
)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_species_for_pest(pest_name):
    """Get all species that can control a given pest."""
    return PEST_MAPPING.get(pest_name, [])


def get_pests_for_species(species_name):
    """Get all pests that a species can control."""
    if species_name in SPECIES_DATA:
        return SPECIES_DATA[species_name]["pests"]
    return []


def get_species_data(species_name):
    """Get full data for a species."""
    return SPECIES_DATA.get(species_name, None)


def get_all_parameter_names():
    """Get list of all parameter names."""
    return [
        "Soil Type",
        "pH",
        "Soil Moisture",
        "Soil Temperature",
        "EC",
    ]


def get_parameter_display_name(param):
    """Get display name for a parameter."""
    mapping = {
        "soil_type": "Soil Type",
        "ph": "pH",
        "soil_moisture": "Soil Moisture",
        "soil_temperature": "Soil Temperature",
        "ec": "EC",
    }
    return mapping.get(param, param)


def get_parameter_key(param):
    """Get the internal key for a parameter."""
    mapping = {
        "Soil Type": "soil_type",
        "pH": "ph",
        "Soil Moisture": "soil_moisture",
        "Soil Temperature": "soil_temperature",
        "EC": "ec",
    }
    return mapping.get(param, param.lower().replace(" ", "_"))


def validate_parameter(param_name, value):
    """Validate a parameter value."""
    param_key = get_parameter_key(param_name)

    if param_key == "soil_type":
        return value in SOIL_TYPES, f"Must be one of: {', '.join(SOIL_TYPES)}"
    elif param_key == "ph":
        try:
            v = float(value)
            return 0 <= v <= 14, "pH must be between 0 and 14"
        except:
            return False, "Please enter a valid number"
    elif param_key == "soil_moisture":
        try:
            v = float(value)
            return 0 <= v <= 100, "Soil moisture must be between 0% and 100%"
        except:
            return False, "Please enter a valid number"
    elif param_key == "soil_temperature":
        try:
            v = float(value)
            return -10 <= v <= 60, "Temperature must be between -10°C and 60°C"
        except:
            return False, "Please enter a valid number"
    elif param_key == "ec":
        try:
            v = float(value)
            return 0 <= v <= 100, "EC must be between 0 and 100 dS/m"
        except:
            return False, "Please enter a valid number"
    return True, ""
