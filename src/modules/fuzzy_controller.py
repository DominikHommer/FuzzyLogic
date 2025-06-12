import numpy as np

from .defuzzifier import Defuzzifier

class FuzzyController:
    def __init__(self, input_vars, output_var, rules):
        self.input_vars = input_vars  # dict name : FuzzyVariable
        self.output_var = output_var  # FuzzyVariable
        self.rules = rules
        self.xs = np.linspace(0, 100, 1001)

    def infer(self, crisp_inputs):
        fuzzified = {name: var.fuzzify(value)
                     for name, value in crisp_inputs.items() for var in [self.input_vars[name]]}
        agg = {term: 0.0 for term in self.output_var.terms}
        for rule in self.rules:
            degree = rule.evaluate(fuzzified)
            _, out_term = rule.consequent
            agg[out_term] = max(agg[out_term], degree)
        ys = np.zeros_like(self.xs)
        for term, degree in agg.items():
            mf = self.output_var.terms[term]
            ys = np.maximum(ys, np.minimum(degree, np.array([mf(x) for x in self.xs])))
        return agg, ys

    def defuzzify(self, ys, method='centroid'):
        f = getattr(Defuzzifier, method)
        return f(self.xs, ys)
