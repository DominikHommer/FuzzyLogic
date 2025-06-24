"""
Defuzzifizierungsmethoden für Fuzzy-Logic-Systeme.
Stellt gängige Techniken bereit, um aus einer Fuzzy-Ausgabemenge einen Crisp-Wert zu berechnen.
"""

import numpy as np

class Defuzzifier:
    """
    Sammlung statischer Methoden zur Defuzzifizierung von Fuzzy-Ausgaben.
    Alle Methoden erwarten:
        xs (np.ndarray): x-Werte (Domäne der Output-MF)
        ys (np.ndarray): Zugehörige μ-Werte (Mitgliedschaft)
    Rückgabe jeweils: float (crisper Output-Wert)
    """

    @staticmethod
    def min_of_max(xs, ys):
        """
        Gibt das Minimum aller x zurück, für die die MF ihr Maximum erreicht (first-max).

        Args:
            xs (np.ndarray): X-Achse der Output-MF
            ys (np.ndarray): Zugehörige MF-Werte
        Returns:
            float: Linker Wert bei Maximum
        """
        max_y = ys.max()
        idx = np.where(ys == max_y)[0]
        return xs[idx].min()

    @staticmethod
    def max_of_max(xs, ys):
        """
        Gibt das Maximum aller x zurück, für die die MF ihr Maximum erreicht (last-max).

        Args:
            xs (np.ndarray): X-Achse der Output-MF
            ys (np.ndarray): Zugehörige MF-Werte
        Returns:
            float: Rechter Wert bei Maximum
        """
        max_y = ys.max()
        idx = np.where(ys == max_y)[0]
        return xs[idx].max()

    @staticmethod
    def mean_of_max(xs, ys):
        """
        Gibt das arithmetische Mittel aller x zurück, für die die MF ihr Maximum erreicht (center-of-maxima).

        Args:
            xs (np.ndarray): X-Achse der Output-MF
            ys (np.ndarray): Zugehörige MF-Werte
        Returns:
            float: Mittelwert der Maxima
        """
        max_y = ys.max()
        idx = np.where(ys == max_y)[0]
        return xs[idx].mean()

    @staticmethod
    def centroid(xs, ys):
        """
        Berechnet das Flächenschwerpunkt-Verfahren (center-of-gravity/centroid).

        Args:
            xs (np.ndarray): X-Achse der Output-MF
            ys (np.ndarray): Zugehörige MF-Werte
        Returns:
            float: Schwerpunkt der Fläche unter der MF
        """
        return (xs * ys).sum() / ys.sum() if ys.sum() != 0 else 0
