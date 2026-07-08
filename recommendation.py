# recommendation.py
"""
Neptune 1.0 - Recommendation Engine
Implements weighted scoring for EPN species selection.
"""

from data import SPECIES_DATA, PEST_MAPPING, SOIL_TYPES, get_species_data
import math

# ============================================================================
# WEIGHT CONFIGURATION
# ============================================================================

WEIGHTS = {
    "pest_match": 50,
    "soil_type_match": 20,
    "ph_match": 10,
    "moisture_match": 10,
    "temperature_match": 5,
    "ec_match": 5,
}

TOTAL_WEIGHT = sum(WEIGHTS.values())

# Confidence levels based on information availability
CONFIDENCE_LEVELS = {
    0: 40,  # Only pest
    1: 55,  # Pest + 1 parameter
    2: 70,  # Pest + 2 parameters
    3: 82,  # Pest + 3 parameters
    4: 92,  # Pest + 4 parameters
    5: 100,  # All parameters
}


# ============================================================================
# SCORING FUNCTIONS
# ============================================================================

def score_pest_match(pest_name, species_name):
    """Score pest match: 100 if species controls the pest, 0 otherwise."""
    species_data = get_species_data(species_name)
    if not species_data:
        return 0
    if pest_name in species_data["pests"]:
        return 100
    return 0


def score_soil_type_match(soil_type, species_name):
    """Score soil type match based on preferred soils."""
    species_data = get_species_data(species_name)
    if not species_data or not soil_type:
        return 50  # Neutral if not provided

    preferred = species_data["preferred_soils"]
    if soil_type in preferred:
        return 100
    return 0


def score_ph_match(ph_value, species_name):
    """Score pH match based on species pH range."""
    species_data = get_species_data(species_name)
    if not species_data or ph_value is None:
        return 50  # Neutral if not provided

    ph_range = species_data["ph"]
    min_ph = ph_range["min"]
    max_ph = ph_range["max"]
    up_to = ph_range.get("up_to", max_ph)

    try:
        ph = float(ph_value)
    except:
        return 50

    # Within ideal range: 100%
    if min_ph <= ph <= max_ph:
        return 100

    # Within extended range (up_to): partial score
    if max_ph < ph <= up_to:
        # Linear decay from 100% at max_ph to 0% at up_to
        score = 100 * (1 - (ph - max_ph) / (up_to - max_ph))
        return max(0, min(100, score))

    if ph < min_ph:
        # Linear decay from 100% at min_ph to 0% at (min_ph - 2)
        lower_limit = max(0, min_ph - 2)
        if ph >= lower_limit:
            score = 100 * (1 - (min_ph - ph) / 2)
            return max(0, min(100, score))
        return 0

    return 0


def score_moisture_match(moisture_value, species_name):
    """Score soil moisture match based on species moisture range."""
    species_data = get_species_data(species_name)
    if not species_data or moisture_value is None:
        return 50  # Neutral if not provided

    moisture_range = species_data["soil_moisture"]
    min_m = moisture_range["min"]
    max_m = moisture_range["max"]

    try:
        m = float(moisture_value)
    except:
        return 50

    # Within range: 100%
    if min_m <= m <= max_m:
        return 100

    # Outside range: partial score with decay
    if m < min_m:
        # Decay from 100% at min_m to 0% at (min_m - 5)
        lower_limit = max(0, min_m - 5)
        if m >= lower_limit:
            score = 100 * (1 - (min_m - m) / 5)
            return max(0, min(100, score))
        return 0
    else:  # m > max_m
        # Decay from 100% at max_m to 0% at (max_m + 5)
        upper_limit = max_m + 5
        if m <= upper_limit:
            score = 100 * (1 - (m - max_m) / 5)
            return max(0, min(100, score))
        return 0


def score_temperature_match(temp_value, species_name):
    """Score soil temperature match based on species temperature range."""
    species_data = get_species_data(species_name)
    if not species_data or temp_value is None:
        return 50  # Neutral if not provided

    temp_range = species_data["soil_temperature"]
    min_t = temp_range["min"]
    max_t = temp_range["max"]

    try:
        t = float(temp_value)
    except:
        return 50

    # Within range: 100%
    if min_t <= t <= max_t:
        return 100

    # Outside range: partial score with decay
    if t < min_t:
        lower_limit = max(0, min_t - 10)
        if t >= lower_limit:
            score = 100 * (1 - (min_t - t) / 10)
            return max(0, min(100, score))
        return 0
    else:  # t > max_t
        upper_limit = max_t + 10
        if t <= upper_limit:
            score = 100 * (1 - (t - max_t) / 10)
            return max(0, min(100, score))
        return 0


def score_ec_match(ec_value, species_name):
    """Score EC match based on species EC range."""
    species_data = get_species_data(species_name)
    if not species_data or ec_value is None:
        return 50  # Neutral if not provided

    ec_range = species_data["ec"]
    min_ec = ec_range["min"]
    max_ec = ec_range["max"]
    decline_at = ec_range.get("decline_at", max_ec + 1)

    try:
        ec = float(ec_value)
    except:
        return 50

    # Within ideal range: 100%
    if min_ec <= ec <= max_ec:
        return 100

    # Between max_ec and decline_at: gradual decline
    if max_ec < ec <= decline_at:
        score = 100 * (1 - (ec - max_ec) / (decline_at - max_ec))
        return max(0, min(100, score))

    # Beyond decline_at: 0
    if ec > decline_at:
        return 0

    if ec < min_ec:
        # Decay from 100% at min_ec to 0% at (min_ec - 2)
        lower_limit = max(0, min_ec - 2)
        if ec >= lower_limit:
            score = 100 * (1 - (min_ec - ec) / 2)
            return max(0, min(100, score))
        return 0

    return 0


# ============================================================================
# MAIN RECOMMENDATION ENGINE
# ============================================================================

def calculate_suitability(pest_name, params):
    """
    Calculate suitability score for each species.

    Args:
        pest_name: Name of the pest
        params: Dictionary of parameter values
            Keys: 'soil_type', 'ph', 'soil_moisture', 'soil_temperature', 'ec'

    Returns:
        Dictionary with scores for each species
    """
    scores = {}

    for species in SPECIES_DATA.keys():
        total_score = 0

        # Pest match (weight: 50)
        pest_score = score_pest_match(pest_name, species)
        total_score += pest_score * (WEIGHTS["pest_match"] / 100)

        # Soil type match (weight: 20)
        soil_type = params.get("soil_type")
        if soil_type:
            soil_score = score_soil_type_match(soil_type, species)
            total_score += soil_score * (WEIGHTS["soil_type_match"] / 100)

        # pH match (weight: 10)
        ph = params.get("ph")
        if ph is not None:
            ph_score = score_ph_match(ph, species)
            total_score += ph_score * (WEIGHTS["ph_match"] / 100)

        # Moisture match (weight: 10)
        moisture = params.get("soil_moisture")
        if moisture is not None:
            moisture_score = score_moisture_match(moisture, species)
            total_score += moisture_score * (WEIGHTS["moisture_match"] / 100)

        # Temperature match (weight: 5)
        temp = params.get("soil_temperature")
        if temp is not None:
            temp_score = score_temperature_match(temp, species)
            total_score += temp_score * (WEIGHTS["temperature_match"] / 100)

        # EC match (weight: 5)
        ec = params.get("ec")
        if ec is not None:
            ec_score = score_ec_match(ec, species)
            total_score += ec_score * (WEIGHTS["ec_match"] / 100)

        scores[species] = round(total_score, 1)

    return scores


def get_confidence(params):
    """
    Calculate confidence score based on available information.

    Args:
        params: Dictionary of parameter values

    Returns:
        Confidence percentage (0-100)
    """
    # Count how many parameters are provided (excluding None/empty)
    provided = 0
    param_keys = ["soil_type", "ph", "soil_moisture", "soil_temperature", "ec"]

    for key in param_keys:
        val = params.get(key)
        if val is not None and val != "" and val != "unknown":
            provided += 1

    # Base confidence: pest is always provided (from the selection)
    # So total info = 1 (pest) + provided parameters
    total_info = 1 + provided

    # Map to confidence level
    if total_info >= 6:  # All parameters + pest
        return 100
    elif total_info >= 5:
        return 92
    elif total_info >= 4:
        return 82
    elif total_info >= 3:
        return 70
    elif total_info >= 2:
        return 55
    else:
        return 40


def get_recommendation_details(pest_name, params):
    """
    Get detailed recommendation including reasons.

    Args:
        pest_name: Name of the pest
        params: Dictionary of parameter values

    Returns:
        Dictionary with recommendation details
    """
    scores = calculate_suitability(pest_name, params)
    confidence = get_confidence(params)

    # Sort species by score
    sorted_species = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    if not sorted_species:
        return None

    best_species, best_score = sorted_species[0]

    # Build reasons
    reasons = []
    species_data = get_species_data(best_species)

    if species_data:
        # Pest match
        if pest_name in species_data["pests"]:
            reasons.append(f"✓ Effective against {pest_name}")

        # Soil type
        soil_type = params.get("soil_type")
        if soil_type and soil_type in species_data["preferred_soils"]:
            reasons.append(f"✓ Soil type ({soil_type}) is compatible")

        # pH
        ph = params.get("ph")
        if ph is not None:
            ph_range = species_data["ph"]
            if ph_range["min"] <= float(ph) <= ph_range["max"]:
                reasons.append(f"✓ pH ({ph}) is within preferred range")
            elif float(ph) <= ph_range.get("up_to", ph_range["max"]):
                reasons.append(f"✓ pH ({ph}) is within tolerant range")

        # Moisture
        moisture = params.get("soil_moisture")
        if moisture is not None:
            m_range = species_data["soil_moisture"]
            if m_range["min"] <= float(moisture) <= m_range["max"]:
                reasons.append(f"✓ Soil moisture ({moisture}%) is optimal")

        # Temperature
        temp = params.get("soil_temperature")
        if temp is not None:
            t_range = species_data["soil_temperature"]
            if t_range["min"] <= float(temp) <= t_range["max"]:
                reasons.append(f"✓ Soil temperature ({temp}°C) is suitable")

        # EC
        ec = params.get("ec")
        if ec is not None:
            ec_range = species_data["ec"]
            if ec_range["min"] <= float(ec) <= ec_range["max"]:
                reasons.append(f"✓ EC ({ec} dS/m) is within ideal range")

    # If no reasons, add a generic one
    if not reasons:
        reasons.append(f"✓ {best_species} is the best match based on available data")

    return {
        "recommended_species": best_species,
        "suitability_score": best_score,
        "confidence": confidence,
        "scores": scores,
        "reasons": reasons,
        "all_scores": sorted_species,
    }


def get_all_parameter_names():
    """Get list of all parameter names for display."""
    return ["Soil Type", "pH", "Soil Moisture", "Soil Temperature", "EC"]
