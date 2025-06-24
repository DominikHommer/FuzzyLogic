"""
Konfiguration für das Fuzzy-Logic-System:
- Definitionen der Membership-Function-Typen und deren Parameter
- Hilfetexte für UI-Tooltips
- Variable-Konfigurationen für Health, Enemies, Distance, Outlook
"""

from modules.membership_function import trap_mf, tri_mf, bell_mf

#: Definition der verfügbaren Membership-Function-Typen
MF_TYPES = {
    "Trapezoid": {
        "func": trap_mf,
        "params": ["a", "b", "c", "d"],
        "default": [0, 0, 25, 50]
    },
    "Triangle": {
        "func": tri_mf,
        "params": ["a", "b", "c"],
        "default": [25, 50, 75]
    },
    "Bell": {
        "func": bell_mf,
        "params": ["a", "b", "c"],
        "default": [15, 4, 50]
    }
}

#: Hilfetexte für Membership-Function-Parameter (wird im UI als Tooltip angezeigt)
MF_PARAM_HELP = {
    "Trapezoid": {
        "a": "Start of slope (links unten)",
        "b": "Start of plateau (links oben)",
        "c": "End of plateau (rechts oben)",
        "d": "End of slope (rechts unten)"
    },
    "Triangle": {
        "a": "Left foot (links)",
        "b": "Peak (Spitze)",
        "c": "Right foot (rechts)"
    },
    "Bell": {
        "a": "Width (Breite, muss >0 sein)",
        "b": "Slope (Steigung)",
        "c": "Center (Zentrum)"
    }
}

#: Definition aller Fuzzy-Variablen inkl. Domänen, Labelnamen und Default-MFs
VAR_CONFIG = {
    "Health": {
        "domain": (0, 100),
        "labels": ["weak", "medium", "strong"],
        "defaults": {
            "weak":   ("Trapezoid", [0, 0, 25, 50]),
            "medium": ("Triangle",  [25, 50, 75]),
            "strong": ("Trapezoid", [50, 75, 100, 100])
        }
    },
    "Enemies": {
        "domain": (0, 100),
        "labels": ["low", "mod", "high"],
        "defaults": {
            "low":   ("Trapezoid", [0, 0, 25, 50]),
            "mod":   ("Triangle",  [25, 50, 75]),
            "high":  ("Trapezoid", [50, 75, 100, 100])
        }
    },
    "Distance": {
        "domain": (0, 10),
        "labels": ["near", "medium", "far"],
        "defaults": {
            "near":   ("Trapezoid", [0, 0, 2.5, 5]),
            "medium": ("Triangle",  [2.5, 5, 7.5]),
            "far":    ("Trapezoid", [5, 7.5, 10, 10])
        }
    },
    "Outlook": {
        "domain": (0, 100),
        "labels": ["poor", "medium", "good"],
        "defaults": {
            "poor":   ("Trapezoid", [0, 0, 25, 50]),
            "medium": ("Triangle",  [25, 50, 75]),
            "good":   ("Trapezoid", [50, 75, 100, 100])
        }
    }
}