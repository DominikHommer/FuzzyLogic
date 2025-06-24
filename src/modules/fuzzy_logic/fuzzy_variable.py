"""
FuzzyVariable-Modul:
Repräsentiert eine linguistische Variable mit mehreren Fuzzy-Terms (Labels).
"""

class FuzzyVariable:
    """
    Eine Fuzzy-Variable besteht aus mehreren linguistischen Termen (z.B. 'low', 'medium', 'high'),
    die jeweils durch eine Membership Function (MF) beschrieben werden.

    Attributes:
        name (str): Name der Variable (z.B. 'Health')
        terms (dict): Mapping von Label (str) auf MembershipFunction
        domain (tuple): Wertebereich (min, max) der Variable, z.B. für Plotting/Sampling
    """

    def __init__(self, name: str, terms: dict, domain: tuple):
        """
        Initialisiert eine Fuzzy-Variable.

        Args:
            name (str): Name der Variable
            terms (dict): Dict[label, MembershipFunction]
            domain (tuple): (min, max) Wertebereich für die Variable
        """
        self.name = name
        self.terms = terms
        self.domain = domain

    def fuzzify(self, x: float) -> dict:
        """
        Fuzzifiziert einen Crisp-Wert x.
        Berechnet für jeden Term/Label die Zugehörigkeit (Degree of Membership).

        Args:
            x (float): Crisp-Inputwert

        Returns:
            dict: Dict[label, degree] mit Grad der Zugehörigkeit für jeden Term
        """
        return {label: mf(x) for label, mf in self.terms.items()}
