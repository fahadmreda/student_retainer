# K-modes clustering for categorical data

from collections import defaultdict
from sklearn.base import BaseEstimator, ClusterMixin
from sklearn.utils.validation import check_array
import sklearn.metrics

import numpy as np
from scipy import sparse

from utilities import get_max_value_key, encode_features, get_unique_rows, decode_centroids
from utilities.dissim import matching_dissim


def initialize_huang(X, n_clusters, dissim):
    """Initialize the centroids based on method by Huang [1997]"""
    nattrs = X.shape[1]
    centroids = np.empty((n_clusters, nattrs), dtype='object')
    # determine frequencies of attributes
    for iattr in range(nattrs):
        freq = defaultdict(int)
        for curattr in X[:, iattr]:
            freq[curattr] += 1
        choices = [chc for chc, wght in freq.items() for _ in range(wght)]
        centroids[:, iattr] = np.random.choice(choices, n_clusters)
    # Above chosen centroids could have empty clusters, so set centroid to the closest point in X
    for ik in range(n_clusters):
        ndx = np.argsort(dissim(X, centroids[ik]))
        while np.all(X[ndx[0]] == centroids, axis=1).any():  # ensure centroid is UNIQUE
            ndx = np.delete(ndx, 0)
        centroids[ik] = X[ndx[0]]
    return centroids


def initialize_cao(X, n_clusters, dissim):
    """Initialize the centroids according to method by Cao et al. [2009]"""
    npoints, nattrs = X.shape
    centroids = np.empty((n_clusters, nattrs), dtype='object')
    # This method based on finding density of points
    dens = np.zeros(npoints)
    for iattr in range(nattrs):
        freq = defaultdict(int)
        for val in X[:, iattr]:
            freq[val] += 1
        for ipoint in range(npoints):
            dens[ipoint] += freq[X[ipoint, iattr]] / float(nattrs)
    dens /= npoints
    # Choose the initial centroids based on the distance and density
    centroids[0] = X[np.argmax(dens)]
    if n_clusters > 1:
        # For all remaining centroids, choose maximum dens * dissim to the already assigned centroid 
        # with the lowest dens * dissim
        for ik in range(1, n_clusters):
            dd = np.empty((ik, npoints))
            for ikk in range(ik):
                dd[ikk] = dissim(X, centroids[ikk]) * dens
            centroids[ik] = X[np.argmax(np.min(dd, axis=0))]
    return centroids


def move_pt_categorical(point, ipoint, to_clust, from_clust, cl_attr_freq,
                   membership, centroids):
    """Move point between clusters (categorical attributes)"""
    membership[to_clust, ipoint] = 1
    membership[from_clust, ipoint] = 0
    for iattr, curattr in enumerate(point):  # Update the frequencies of attributes in the cluster
        to_attr_counts = cl_attr_freq[to_clust][iattr]
        from_attr_counts = cl_attr_freq[from_clust][iattr]
        # Increment attribute count for the new "to" cluster
        to_attr_counts[curattr] += 1
        current_attribute_value_freq = to_attr_counts[curattr]
        current_centroid_value = centroids[to_clust][iattr]
        current_centroid_freq = to_attr_counts[current_centroid_value]
        if current_centroid_freq < current_attribute_value_freq:
            # Then we've incremented this value to the new mode so update the centroid
            centroids[to_clust][iattr] = curattr
        # Decrement attribute count for the old "from" cluster
        from_attr_counts[curattr] -= 1
        old_centroid_value = centroids[from_clust][iattr]
        if old_centroid_value == curattr:
            # Then we've removed a count from the old centroid value, so we need to recalculate the centroid 
            # as it might not be the maximum anymore
            centroids[from_clust][iattr] = get_max_value_key(from_attr_counts)
    return cl_attr_freq, membership, centroids


def _labels_and_cost(X, centroids, dissim):
    """Calculate labels and cost function from a matrix of points and centroid list for the k-modes"""
    X = check_array(X)
    npoints = X.shape[0]
    cost = 0.
    labels = np.empty(npoints, dtype=np.uint8)
    for ipoint, curpoint in enumerate(X):  # ipoint - index of pt
        diss = dissim(centroids, curpoint)  # distance
        clust = np.argmin(diss)
        labels[ipoint] = clust
        cost += diss[clust]
    return labels, cost


def _k_modes_one_iter(X, centroids, cl_attr_freq, membership, dissim):
    """One iteration of k-modes clustering algorithm"""
    moves = 0
    for ipoint, curpoint in enumerate(X):
        clust = np.argmin(dissim(centroids, curpoint))
        if membership[clust, ipoint]:
            # Point is in the right place already
            continue

        # Move the point and update old and new cluster frequencies and centroids
        moves += 1
        old_clust = np.argwhere(membership[:, ipoint])[0][0]

        cl_attr_freq, membership, centroids = move_pt_categorical(
            curpoint, ipoint, clust, old_clust, cl_attr_freq, membership, centroids
        )

        # If cluster is empty, reinitialize with random point from the largest cluster
        if np.sum(membership[old_clust, :]) == 0:
            from_clust = membership.sum(axis=1).argmax()
            choices = [ii for ii, ch in enumerate(membership[from_clust, :]) if ch]
            rindx = np.random.choice(choices)
            cl_attr_freq, membership, centroids = move_pt_categorical(
                X[rindx], rindx, old_clust, from_clust, cl_attr_freq, membership, centroids
            )
    return centroids, moves


def k_modes(X, n_clusters, max_iterations, dissim, init, n_init, verbose):
    """The k-modes algorithm"""
    if sparse.issparse(X):
        raise TypeError("k-modes doesn't support sparse data.")
    
    X = check_array(X, dtype=None)
    
    # Convert categorical values in X array to integers for speed
    # Based on unique values in X, a mapping can be made to achieve this.
    X, enc_map = encode_features(X)
    npoints, nattrs = X.shape
    assert n_clusters <= npoints, "Do we have more clusters than data points?. Check please."

    # Does there exist more n_clusters than unique rows? Then set unique rows as initial values and skip iteration
    unique = get_unique_rows(X)
    n_unique = unique.shape[0]
    if n_unique <= n_clusters:
        max_iterations = 0
        n_init = 1
        n_clusters = n_unique
        init = unique
    all_centroids = []
    all_labels = []
    all_costs = []
    all_n_iters = []
    for init_no in range(n_init):
        # _____ INITIALIZE _____ #
        if verbose:
            print("Init: initializing the centroids")
        if isinstance(init, str) and init == 'Huang':
            centroids = initialize_huang(X, n_clusters, dissim)
        elif isinstance(init, str) and init == 'Cao':
            centroids = initialize_cao(X, n_clusters, dissim)
        elif isinstance(init, str) and init == 'random':
            seeds = np.random.choice(range(npoints), n_clusters)
            centroids = X[seeds]
        elif hasattr(init, '__array__'):
            # Make sure 'initialize' is a 2D array.
            if len(init.shape) == 1:
                init = np.atleast_2d(init).T
            assert init.shape[0] == n_clusters, \
                "We have the wrong number of initial centroids in init ({}, should be {})."\
                .format(init.shape[0], n_clusters)
            assert init.shape[1] == nattrs, \
                "We have the wrong number of attributes in init ({}, should be {})."\
                .format(init.shape[1], nattrs)
            centroids = np.asarray(init, dtype=np.uint8)
        else:
            raise NotImplementedError
        if verbose:
            print("Initialize: initializing clusters")
        membership = np.zeros((n_clusters, npoints), dtype=np.uint8)
        # cl_attr_freq is a list of lists of dictionaries that contain the frequencies of values
        # per cluster and attribute.
        cl_attr_freq = [[defaultdict(int) for _ in range(nattrs)]
                        for _ in range(n_clusters)]
        for ipoint, curpoint in enumerate(X):
            # The initial assignment to clusters
            clust = np.argmin(dissim(centroids, curpoint))
            membership[clust, ipoint] = 1
            # Count the attribute values per cluster
            for iattr, curattr in enumerate(curpoint):
                cl_attr_freq[clust][iattr][curattr] += 1
        # Perform initial centroid update
        for ik in range(n_clusters):
            for iattr in range(nattrs):
                if sum(membership[ik]) == 0:
                    # Empty centroid, choose it randomly
                    centroids[ik, iattr] = np.random.choice(X[:, iattr])
                else:
                    centroids[ik, iattr] = get_max_value_key(cl_attr_freq[ik][iattr])
        # _____ ITERATION _____ #
        if verbose:
            print("Starting all iterations...")
        itr = 0
        converged = False
        cost = np.Inf
        while itr <= max_iterations and not converged:
            itr += 1
            centroids, moves = _k_modes_one_iter(X, centroids, cl_attr_freq, membership, dissim)
            # All points seen in this iteration
            labels, ncost = _labels_and_cost(X, centroids, dissim)
            converged = (moves == 0) or (ncost >= cost)
            cost = ncost
            if verbose:
                print("Run {}, iteration: {}/{}, moves: {}, cost: {}"
                      .format(init_no + 1, itr, max_iterations, moves, cost))
        # Store current run results
        all_centroids.append(centroids)
        all_labels.append(labels)
        all_costs.append(cost)
        all_n_iters.append(itr)

    best = np.argmin(all_costs)
    if n_init > 1 and verbose:
        print("The best run was number {}".format(best + 1))

    return all_centroids[best], enc_map, all_labels[best], \
        all_costs[best], all_n_iters[best]


def calc_eval_metrics(X, centroids, labels, dissim):
    """Calculates SSE, Calinski-Harabasz index (VRC), Dunn index, Silhouette Width Criterion"""
    # VRC/SSE
    ssw = 0.0
    npoints, nattrs = X.shape
    N = npoints
    k = len(centroids)
    c = np.mean(centroids, axis=0)  # average of all clusters point
    split_X = [[] for x in range(k)]  # split X by clusters
    for ipoint, curpoint in enumerate(X):
        pt_cluster = labels[ipoint]
        pt_centroid = centroids[pt_cluster]
        split_X[pt_cluster].append(curpoint)  # store parsed X here
        diss = dissim(centroids, curpoint)  # distance from all centroids to point
        ssw += diss[pt_cluster]**2
    sse = ssw
    diss = dissim(centroids, c)
    ssb = np.sum(diss)
    if k > 0:
        vrc = (ssb/ssw) * (N-k)/(k-1.0)
    else:
        vrc = None
    print "VRC: %.4f" % vrc
    # Dunn index
    # get distances between all centroids
    centroid_dist = []
    #for i in range(len(centroids)):
    #    for j in range(len(centroids)):
    #        print centroids[i]
    #        temp = dissim(centroids[i], centroids[j])
    #        centroid_dist.append(temp)
    #dunn_numerator = np.min(centroid_dist)
    # calculate 3 different deltas for dunn index
    # https://en.wikipedia.org/wiki/Dunn_index
    int_cluster_dist = [[] for x in range(k)]
    delta_a = []
    # for i in range(len(split_X)):
    #     for j in range(len(split_X[i])):
    #         for k in range(len(split_X[i])):
    #             if j > k:
    #                 temp = dissim(split_X[i][j], split_X[i][k])
    #                 int_cluster_dist[i].append(temp)
    #     delta_a.append(np.max(int_cluster_dist[i]))
    # build distance matrix [n_samples_a, n_samples_a]
    # dist_matrix = np.zeros((npoints, npoints))
    # for i in range(len(X)):
    #     for j in range(len(X)):
    #         dist_matrix[i,j] = dissim(X[i], X[j])
    # scores = sklearn.metrics.silhouette_score(dist_matrix, metric='precomputed')
    return vrc, sse


class KModes(BaseEstimator, ClusterMixin):

    """k-modes clustering algorithm for categorical data.
    Parameters
    -----------
    n_clusters : int, optional, default: 8
        The number of clusters to form as well as the number of
        centroids to generate.
    max_iterations : int, default: 300
        Maximum number of iterations of the k-modes algorithm for a
        single run.
    cat_dissim : func, default: matching_dissim
        Dissimilarity function used by the algorithm for categorical variables.
        Defaults to the matching dissimilarity function.
    init : {'Huang', 'Cao', 'random' or an ndarray}, default: 'Cao'
        Method for initialization:
        'Huang': Method in Huang [1997, 1998]
        'Cao': Method in Cao et al. [2009]
        'random': choose 'n_clusters' observations (rows) at random from
        data for the initial centroids.
        If an ndarray is passed, it should be of shape (n_clusters, n_features)
        and gives the initial centroids.
    n_init : int, default: 10
        Number of time the k-modes algorithm will be run with different
        centroid seeds. The final results will be the best output of
        n_init consecutive runs in terms of cost.
    verbose : int, optional
        Verbosity mode.
        
    Attributes
    ----------
    cluster_centroids_ : array, [n_clusters, n_features]
        Categories of cluster centroids
    labels_ :
        Labels of each point
    cost_ : float
        Clustering cost, defined as the sum distance of all points to
        their respective cluster centroids.
    n_iter_ : int
        The number of iterations the algorithm ran for.

    Notes
    -----
    Reference:
    Huang, Z.: Extensions to the k-modes algorithm for clustering large
    data sets with categorical values, Data Mining and Knowledge
    Discovery 2(3), 1998.
    """

    def __init__(self, n_clusters=8, max_iterations=100, cat_dissim=matching_dissim,
                 init='Cao', n_init=1, verbose=0):

        self.n_clusters = n_clusters
        self.max_iterations = max_iterations
        self.cat_dissim = cat_dissim
        self.init = init
        self.n_init = n_init
        self.verbose = verbose
        self.vrc_ = None
        self.sse_ = None
        if ((isinstance(self.init, str) and self.init == 'Cao') or
                hasattr(self.init, '__array__')) and self.n_init > 1:
            if self.verbose:
                print("Initialization method and algorithm are deterministic. "
                      "Setting n_init to 1.")
            self.n_init = 1

    def fit(self, X, y=None, **kwargs):
        """Compute k-modes clustering algorithm.
        Parameters
        ----------
        X : array-like, shape=[n_samples, n_features]
        """
        self._enc_cluster_centroids, self._enc_map, self.labels_,\
            self.cost_, self.n_iter_ = k_modes(X,
                                               self.n_clusters,
                                               self.max_iterations,
                                               self.cat_dissim,
                                               self.init,
                                               self.n_init,
                                               self.verbose)
        self.vrc_, self.sse_ = calc_eval_metrics(X, self._enc_cluster_centroids, self.labels_, self.cat_dissim)


        return self

    def fit_predict(self, X, y=None, **kwargs):
        """Compute the cluster centroids and predict cluster index for each sample.
        A convenience method; equivalent to calling fit(X) followed by
        predict(X).
        """
        return self.fit(X, **kwargs).labels_

    def predict(self, X, **kwargs):
        """Prediction of the closest cluster each sample in X belongs to.
        Parameters
        ----------
        X : array-like, shape = [n_samples, n_features]
            New data to predict.
        Returns
        -------
        labels : array, shape [n_samples,]
            Index of the cluster each sample belongs to.
        """
        assert hasattr(self, '_enc_cluster_centroids'), "Model hasn't been fitted yet."
        X = check_array(X, dtype=None)
        X, _ = encode_features(X, enc_map=self._enc_map)
        return _labels_and_cost(X, self._enc_cluster_centroids, self.cat_dissim)[0]

    @property
    def cluster_centroids_(self):
        if hasattr(self, '_enc_cluster_centroids'):
            return decode_centroids(self._enc_cluster_centroids, self._enc_map)
        else:
            raise AttributeError("'{}' object has no attribute named 'cluster_centroids_' "
                                 "because the model is not yet fitted.")
