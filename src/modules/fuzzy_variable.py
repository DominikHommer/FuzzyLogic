class FuzzyVariable:
    """Holds linguistic terms and their membership functions."""
    def __init__(self, name, terms):
        self.name = name
        self.terms = terms  # dict label : MembershipFunction

    def fuzzify(self, x):
        return {label: mf(x) for label, mf in self.terms.items()}