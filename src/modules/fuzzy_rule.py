class FuzzyRule:
    """
    Eine Regel: IF Antezedenzien THEN Konsequenz.
    antecedents: List of (var_name, term_label)
    consequent:  (var_name, term_label)
    """
    def __init__(self, antecedents: list, consequent: tuple):
        self.antecedents = antecedents
        self.consequent = consequent

    def evaluate(self, fuzzified_inputs: dict) -> float:
        """
        fuzzified_inputs: { var_name: {term_label: degree, ...}, ... }
        AND-Verknüpfung via Minimum.
        """
        degrees = []
        for var, term in self.antecedents:
            deg = fuzzified_inputs[var].get(term, 0.0)
            degrees.append(deg)
        return min(degrees) if degrees else 0.0