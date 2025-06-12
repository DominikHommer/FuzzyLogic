class FuzzyVariable:
    """
    Repräsentiert eine Fuzzy-Variable mit mehreren linguistischen Termen.
    name: String-Name
    terms: Dict[label, MembershipFunction]
    domain: Tuple[min, max] für Plot und Sampling
    """
    def __init__(self, name: str, terms: dict, domain: tuple):
        self.name = name
        self.terms = terms
        self.domain = domain

    def fuzzify(self, x: float) -> dict:
        """Gibt Dict[label, degree] für einen crisp-Wert x zurück."""
        return {label: mf(x) for label, mf in self.terms.items()}