CUT_PARAMS = {

    "steel": {
        0.5: {"speed": 5.0, "gas": "O2", "pressure": 0.7, "nozzle": "1.0", "power": 60, "focus": 0.0},
        1:   {"speed": 3.5, "gas": "O2", "pressure": 0.8, "nozzle": "1.0", "power": 70, "focus": 0.0},
        2:   {"speed": 2.8, "gas": "O2", "pressure": 0.9, "nozzle": "1.2", "power": 75, "focus": 0.0},
        3:   {"speed": 2.0, "gas": "O2", "pressure": 1.0, "nozzle": "1.4", "power": 80, "focus": 0.0},
        4:   {"speed": 1.5, "gas": "O2", "pressure": 1.1, "nozzle": "1.6", "power": 85, "focus": 0.0},
        5:   {"speed": 1.2, "gas": "O2", "pressure": 1.2, "nozzle": "1.8", "power": 90, "focus": 0.0},
        6:   {"speed": 1.0, "gas": "O2", "pressure": 1.3, "nozzle": "2.0", "power": 95, "focus": 0.0},
        8:   {"speed": 0.7, "gas": "O2", "pressure": 1.4, "nozzle": "2.2", "power": 100, "focus": 0.0},
        10:  {"speed": 0.5, "gas": "O2", "pressure": 1.5, "nozzle": "2.5", "power": 100, "focus": 0.0},
        12:  {"speed": 0.38, "gas": "O2", "pressure": 1.6, "nozzle": "2.5", "power": 100, "focus": +0.2},
        15:  {"speed": 0.28, "gas": "O2", "pressure": 1.7, "nozzle": "2.5", "power": 100, "focus": +0.3},
        20:  {"speed": 0.18, "gas": "O2", "pressure": 1.8, "nozzle": "2.5", "power": 100, "focus": +0.5},
        25:  {"speed": 0.12, "gas": "O2", "pressure": 1.9, "nozzle": "2.5", "power": 100, "focus": +0.7},
    },

    "stainless": {
        0.5: {"speed": 4.5, "gas": "N2", "pressure": 1.1, "nozzle": "1.0", "power": 70, "focus": -0.8},
        1:   {"speed": 3.0, "gas": "N2", "pressure": 1.2, "nozzle": "1.0", "power": 85, "focus": -1.0},
        2:   {"speed": 2.2, "gas": "N2", "pressure": 1.3, "nozzle": "1.2", "power": 90, "focus": -1.2},
        3:   {"speed": 1.5, "gas": "N2", "pressure": 1.4, "nozzle": "1.4", "power": 95, "focus": -1.5},
        4:   {"speed": 1.1, "gas": "N2", "pressure": 1.5, "nozzle": "1.6", "power": 100, "focus": -2.0},
        5:   {"speed": 0.8, "gas": "N2", "pressure": 1.6, "nozzle": "1.8", "power": 100, "focus": -2.5},
        6:   {"speed": 0.6, "gas": "N2", "pressure": 1.7, "nozzle": "2.0", "power": 100, "focus": -3.0},
        8:   {"speed": 0.35, "gas": "N2", "pressure": 1.8, "nozzle": "2.0", "power": 100, "focus": -3.5},
        10:  {"speed": 0.22, "gas": "N2", "pressure": 1.9, "nozzle": "2.0", "power": 100, "focus": -4.0},
        12:  {"speed": 0.15, "gas": "N2", "pressure": 2.0, "nozzle": "2.0", "power": 100, "focus": -4.5},
        15:  {"speed": 0.10, "gas": "N2", "pressure": 2.1, "nozzle": "2.0", "power": 100, "focus": -5.0},
        20:  {"speed": 0.06, "gas": "N2", "pressure": 2.2, "nozzle": "2.0", "power": 100, "focus": -5.5},
    },

    "aluminum": {
        0.5: {"speed": 4.0, "gas": "N2", "pressure": 1.1, "nozzle": "1.0", "power": 70, "focus": -0.8},
        1:   {"speed": 3.0, "gas": "N2", "pressure": 1.2, "nozzle": "1.0", "power": 90, "focus": -1.0},
        2:   {"speed": 2.0, "gas": "N2", "pressure": 1.3, "nozzle": "1.2", "power": 95, "focus": -1.5},
        3:   {"speed": 1.2, "gas": "N2", "pressure": 1.4, "nozzle": "1.4", "power": 100, "focus": -2.0},
        4:   {"speed": 0.8, "gas": "N2", "pressure": 1.5, "nozzle": "1.6", "power": 100, "focus": -2.5},
        6:   {"speed": 0.45, "gas": "N2", "pressure": 1.6, "nozzle": "1.8", "power": 100, "focus": -3.0},
        8:   {"speed": 0.28, "gas": "N2", "pressure": 1.7, "nozzle": "2.0", "power": 100, "focus": -3.5},
        10:  {"speed": 0.18, "gas": "N2", "pressure": 1.8, "nozzle": "2.0", "power": 100, "focus": -4.0},
        12:  {"speed": 0.12, "gas": "N2", "pressure": 1.9, "nozzle": "2.0", "power": 100, "focus": -4.5},
    },
}


def get_params(material: str, thickness):
    try:
        thickness = float(thickness)
    except:
        return None

    material = material.lower()

    if material not in CUT_PARAMS:
        return None

    return CUT_PARAMS[material].get(thickness)