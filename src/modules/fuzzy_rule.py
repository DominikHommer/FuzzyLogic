class FuzzyRule:
    """A rule linking input terms to an output term."""
    def __init__(self, antecedents, consequent):
        self.antecedents = antecedents
        self.consequent = consequent

    def evaluate(self, fuzzified_inputs):
        # AND = min
        degrees = [fuzzified_inputs[var][term] for var, term in self.antecedents]
        return min(degrees) if degrees else 0