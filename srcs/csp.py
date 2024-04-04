import numpy as np
from scipy import linalg
from sklearn.base import BaseEstimator, TransformerMixin


class CommonSpacialPattern(BaseEstimator, TransformerMixin):
    """Common Spacial Pattern (CSP) transformer.

    This transformer is used to extract features from EEG signals.

    Attributes:
        n_components (int): Number of components to keep.
    """

    n_components: int
    classes: np.ndarray

    def __init__(self, n_components: int = 4):
        self.n_components = n_components
        self.filter_components = None

    def __compute_cov(self, X, y):
        covs = []
        for c in self.classes:
            x_class = X[y == c]
            _, n_channels, _ = x_class.shape

            x_class = np.transpose(x_class, [1, 0, 2])
            x_class = x_class.reshape(n_channels, -1)
            cov = np.cov(x_class)

            covs.append(cov)

        return covs

    def fit(self, X, y) -> "CommonSpacialPattern":
        if not isinstance(X, np.ndarray):
            raise ValueError(f"X should be of type ndarray (got {type(X)}).")
        if y is not None:
            if len(X) != len(y) or len(y) < 1:
                raise ValueError("X and y must have the same length.")
        if X.ndim < 3:
            raise ValueError("X must have at least 3 dimensions.")

        self.classes = np.unique(y)
        if len(self.classes) < 2:
            raise ValueError("n_classes must be >= 2.")

        covs = self.__compute_cov(X, y)
        eigvals, eigvecs = linalg.eigh(covs[0], covs[0] + covs[1])
        ix = np.argsort(np.abs(eigvals - 0.5))[::-1]

        eigvecs = eigvecs[:, ix]

        if self.n_components is not None:
            eigvecs = eigvecs[:, : self.n_components]

        self.filter_components = eigvecs
        return self

    def transform(self, X):
        if self.filter_components is None:
            raise ValueError("The model has not been trained.")

        X = np.array([np.dot(self.filter_components.T, epoch) for epoch in X])
        X = (X**2).mean(axis=2)
        return X
