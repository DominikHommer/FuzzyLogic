"""
MembershipFunction-Modul:
Wrappt eine Funktion, die einen Wert auf einen Zugehörigkeitsgrad [0..1] abbildet.
Erlaubt, beliebige Python-Funktionen als Fuzzy-Membership Functions zu verwenden.
"""

class MembershipFunction:
    """
    Eine MembershipFunction kapselt eine numerische Funktion,
    die einen Inputwert x ∈ ℝ auf einen Zugehörigkeitsgrad μ ∈ [0, 1] abbildet.
    Damit kann jede MF (Trapez, Dreieck, Bell etc.) einfach als Python-Callable genutzt werden.

    Attributes:
        func (callable): Eine Funktion x -> μ(x), die den Zugehörigkeitsgrad zurückgibt.
    """

    def __init__(self, func):
        """
        Initialisiert eine MembershipFunction mit einer gegebenen Funktion.

        Args:
            func (callable): Funktion, die für x den Zugehörigkeitsgrad μ(x) berechnet.
        """
        self.func = func

    def __call__(self, x):
        """
        Erlaubt das direkte Aufrufen des Objekts wie eine Funktion: mf(x)

        Args:
            x (float): Eingabewert

        Returns:
            float: Zugehörigkeitsgrad im Bereich [0, 1]
        """
        return float(self.func(x))
