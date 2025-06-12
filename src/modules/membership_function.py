class MembershipFunction:
    """
    Wrappt eine Python-Funktion, die einen numerischen Wert x auf einen 
    Zugehörigkeitsgrad [0..1] abbildet.
    """
    def __init__(self, func):
        self.func = func

    def __call__(self, x):
        return float(self.func(x))