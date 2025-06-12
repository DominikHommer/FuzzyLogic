import numpy as np

class Defuzzifier:
    @staticmethod
    def min_of_max(xs, ys):
        max_y = ys.max()
        idx = np.where(ys == max_y)[0]
        return xs[idx].min()

    @staticmethod
    def max_of_max(xs, ys):
        max_y = ys.max()
        idx = np.where(ys == max_y)[0]
        return xs[idx].max()

    @staticmethod
    def mean_of_max(xs, ys):
        max_y = ys.max()
        idx = np.where(ys == max_y)[0]
        return xs[idx].mean()

    @staticmethod
    def bisector(xs, ys):
        area = np.trapezoid(ys, xs)
        half = area / 2
        cum = np.cumsum((ys[:-1] + ys[1:]) / 2 * np.diff(xs))
        idx = np.searchsorted(cum, half)
        return xs[idx]

    @staticmethod
    def blend(xs, ys):
        return (xs * ys).sum() / ys.sum() if ys.sum() != 0 else 0

    @staticmethod
    def centroid(xs, ys):
        return Defuzzifier.blend(xs, ys)