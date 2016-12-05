# Generic utilities for clustering

import numpy as np


def decode_centroids(encoded, mapping):
    """Takes encoded centroids and decodes them, taking the array back to the original data
    labels with a list of mappings.
    """
    decoded = []
    for ii in range(encoded.shape[1]):
        # Invert mapping to decode
        inv_mapping = {v: k for k, v in mapping[ii].items()}
        decoded.append(np.vectorize(inv_mapping.__getitem__)(encoded[:, ii]))
    return np.atleast_2d(np.array(decoded)).T

def encode_features(X, enc_map=None):
    """Converts the categorical values from every column of X to integers within the range
    [0, n_unique_values_in_column - 1], if X isn't dtype=int.

    If mapping is not provided, it is calculated based on the values in X.
    Any unknown values during the prediction get a value of -1 including np.NaNs.
    """
    if np.issubdtype(X.dtype, np.integer):
        # It is integer type, so for speed, reshape the data to mapping dictionaries and nothing with X.
        enc_map = [{val: val for val in np.unique(col)} for col in X.T]
        return X, enc_map
    if enc_map is None:
        fit = True
        # Calculate enc_map by initializing the list of column mappings.
        enc_map = []
    else:
        fit = False
    Xenc = np.zeros(X.shape).astype('int')
    for ii in range(X.shape[1]):
        if fit:
            col_enc = {val: jj for jj, val in enumerate(np.unique(X[:, ii]))
                       if not (isinstance(val, float) and np.isnan(val))}
            enc_map.append(col_enc)
        # All the unknown categories, including np.NaNs, get a value of -1.
        Xenc[:, ii] = np.array([enc_map[ii].get(x, -1) for x in X[:, ii]])

    return Xenc, enc_map

def get_max_value_key(dic):
    """Quick method to get key for maximum value in dict."""
    v = list(dic.values())
    k = list(dic.keys())
    return k[v.index(max(v))]

def get_unique_rows(a):
    """Gets unique rows in numpy array"""
    return np.vstack({tuple(row) for row in a})
