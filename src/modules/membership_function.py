"""
Definition gängiger Membership Functions für das Fuzzy-Logic-System.
Jede Funktion erzeugt ein MembershipFunction-Objekt mit einer passenden MF-Form.
"""

from modules.fuzzy_logic.membership_function import MembershipFunction

def trap_mf(a, b, c, d):
    """
    Trapezförmige Membership Function (Trapezoid MF).

    Args:
        a (float): Startpunkt der Steigung (links unten)
        b (float): Start des Plateaus (links oben)
        c (float): Ende des Plateaus (rechts oben)
        d (float): Endpunkt der Steigung (rechts unten)
    Returns:
        MembershipFunction: Trapezförmige MF
    """
    def mf(x):
        if x < a or x > d:
            return 0.0
        if x < b:
            return (x - a) / (b - a)
        if x <= c:
            return 1.0
        return (d - x) / (d - c)
    return MembershipFunction(mf)

def tri_mf(a, b, c):
    """
    Dreiecksförmige Membership Function (Triangular MF).

    Args:
        a (float): Linker Fuß (links)
        b (float): Spitze (Peak)
        c (float): Rechter Fuß (rechts)
    Returns:
        MembershipFunction: Dreiecksförmige MF
    """
    def mf(x):
        if x < a or x > c:
            return 0.0
        if x < b:
            return (x - a) / (b - a)
        return (c - x) / (c - b)
    return MembershipFunction(mf)

def bell_mf(a, b, c):
    """
    Glöckchenförmige Membership Function (Generalized Bell MF).

    Args:
        a (float): Breite der Glocke (>0)
        b (float): Steigung (Slope)
        c (float): Zentrum (Center)
    Returns:
        MembershipFunction: Bell-förmige MF
    """
    def mf(x):
        safe_a = max(abs(a), 1e-6)
        try:
            val = ((x - c) / safe_a) ** (2 * b)
        except Exception:
            val = float('inf')
        try:
            return 1.0 / (1.0 + val)
        except Exception:
            return 0.0
    return MembershipFunction(mf)
