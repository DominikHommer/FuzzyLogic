"""
FuzzyController-Modul:
Kapselt die gesamte Fuzzy-Inferenz inklusive Fuzzifizierung, Regelanwendung, Aggregation und Defuzzifizierung.
"""

import numpy as np
from modules.fuzzy_logic.defuzzifier import Defuzzifier

class FuzzyController:
    """
    FuzzyController führt die Kernlogik eines Fuzzy-Systems aus:
    - Fuzzifizierung der Eingaben
    - Auswertung der Fuzzy-Regeln
    - Aggregation der Output-Fuzzy-Sets
    - Defuzzifizierung des Gesamtergebnisses

    Attributes:
        input_vars (dict): Name -> FuzzyVariable für alle Eingabegrößen.
        output_var (FuzzyVariable): Output-Fuzzy-Variable.
        rules (list): Liste von FuzzyRule-Objekten (Regelbasis).
        xs (np.ndarray): X-Achse für die Output-MF (Diskretisierung).
    """
    def __init__(self, input_vars: dict, output_var, rules: list):
        """
        Initialisiert den Controller mit Input-Variablen, Output-Variable und Regelsatz.

        Args:
            input_vars (dict): Name -> FuzzyVariable für Input-Variablen.
            output_var (FuzzyVariable): Die Output-Variable.
            rules (list): Liste der FuzzyRule-Objekte.
        """
        self.input_vars = input_vars
        self.output_var = output_var
        self.rules = rules
        self.xs = np.linspace(output_var.domain[0], output_var.domain[1], 500)

    def infer(self, crisp_inputs: dict):
        """
        Fuzzy-Inferenzpipeline: Fuzzifizierung -> Regelbewertung -> Aggregation -> Aggregiertes Output-Set.

        Args:
            crisp_inputs (dict): Zuordnung: Variablenname -> Wert.

        Returns:
            fuzzified (dict): Für jede Inputvariable die Fuzzy-Zugehörigkeitswerte zum Input.
            agg (dict): Aggregierte Stärke für jeden Outputterm.
            ys (np.ndarray): Aggregierte Output-Membership-Function über self.xs.
        """
        # 1. Fuzzifizierung der Eingabewerte
        fuzzified = {name: var.fuzzify(crisp_inputs[name])
                     for name, var in self.input_vars.items()}

        # 2. Regelbewertung und Aggregation (pro Outputterm das Maximum aller Regeln)
        agg = {term: 0.0 for term in self.output_var.terms}
        for rule in self.rules:
            alpha = rule.evaluate(fuzzified)
            _, out_term = rule.consequent
            agg[out_term] = max(agg[out_term], alpha)

        # 3. Aggregiertes Output-MF (pro x: max über alle terms der min(term-mf, degree))
        ys = np.zeros_like(self.xs)
        for term, degree in agg.items():
            mf = self.output_var.terms[term]
            ys = np.maximum(ys, np.minimum(degree, np.array([mf(x) for x in self.xs])))
        return fuzzified, agg, ys

    def defuzzify(self, ys: np.ndarray, method: str = 'centroid') -> float:
        """
        Führt Defuzzifizierung durch, um aus dem Output-MF einen Crisp-Wert zu berechnen.

        Args:
            ys (np.ndarray): Das aggregierte Output-MF über self.xs.
            method (str): Name der Defuzzifizierungsstrategie
                ('min_of_max', 'max_of_max', 'mean_of_max', 'centroid', ...)

        Returns:
            float: Crisp-Ausgabewert nach Defuzzifizierung.
        """
        f = getattr(Defuzzifier, method)
        return float(f(self.xs, ys))


