"""
FuzzyRule-Modul:
Definiert eine Fuzzy-Regel ("IF ... THEN ...") für Fuzzy-Logic-Systeme.
"""

class FuzzyRule:
    """
    Eine Fuzzy-Regel nach dem Schema:
        IF <Antezedenz1> AND <Antezedenz2> ... THEN <Konsequenz>
    
    Attributes:
        antecedents (list): Liste von (var_name, term_label)-Tupeln für die Bedingungen.
        consequent (tuple): (var_name, term_label) für die Konsequenz.
    """
    def __init__(self, antecedents: list, consequent: tuple):
        """
        Initialisiert eine neue Fuzzy-Regel.

        Args:
            antecedents (list): Liste der Bedingungen [(var_name, term_label), ...]
            consequent (tuple): Konsequenz als (var_name, term_label)
        """
        self.antecedents = antecedents
        self.consequent = consequent

    def evaluate(self, fuzzified_inputs: dict) -> float:
        """
        Bewertet die Regel für gegebene fuzzifizierte Eingaben.
        Die AND-Verknüpfung erfolgt als Minimum der Grade der Antezedenzien.

        Args:
            fuzzified_inputs (dict): { var_name: {term_label: degree, ...}, ... }
        
        Returns:
            float: Stärke (alpha) der Regelaktivierung (zwischen 0 und 1).
        """
        degrees = []
        for var, term in self.antecedents:
            deg = fuzzified_inputs[var].get(term, 0.0)
            degrees.append(deg)
        return min(degrees) if degrees else 0.0
