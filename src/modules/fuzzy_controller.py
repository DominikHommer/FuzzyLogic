import numpy as np

from modules.defuzzifier import Defuzzifier

class FuzzyController:
    """
    Führt Inferenz und Defuzzifizierung durch.
    input_vars:  Dict[name, FuzzyVariable]
    output_var:  FuzzyVariable
    rules:       List[FuzzyRule]
    """
    def __init__(self, input_vars: dict, output_var, rules: list):
        self.input_vars = input_vars
        self.output_var = output_var
        self.rules = rules
        # x-Achse für Output-MF
        self.xs = np.linspace(output_var.domain[0], output_var.domain[1], 500)

    def infer(self, crisp_inputs: dict):
        # 1) Fuzzification
        fuzzified = {name: var.fuzzify(crisp_inputs[name])
                     for name, var in self.input_vars.items()}
        # 2) Rule Evaluation & Aggregation
        agg = {term: 0.0 for term in self.output_var.terms}
        for rule in self.rules:
            alpha = rule.evaluate(fuzzified)
            _, out_term = rule.consequent
            agg[out_term] = max(agg[out_term], alpha)
        # 3) Build aggregated output fuzzy set
        ys = np.zeros_like(self.xs)
        for term, degree in agg.items():
            mf = self.output_var.terms[term]
            ys = np.maximum(ys, np.minimum(degree, np.array([mf(x) for x in self.xs])))
        return fuzzified, agg, ys

    def defuzzify(self, ys: np.ndarray, method: str = 'centroid') -> float:
        """
        Wahl der Defuzzifizierung:
        'min_of_max', 'max_of_max', 'mean_of_max',
        'bisector', 'blend', 'centroid'
        """
        f = getattr(Defuzzifier, method)
        return float(f(self.xs, ys))

