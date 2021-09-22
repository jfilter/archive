"""
Multidimensional Scaling

Computes the multidimensional scaling using eigendecomposition ``numpy.linalg.eigh``. 

The implementation is based on a snippet published on a mailing list:
http://mail.scipy.org/pipermail/scipy-user/2011-January/028064.html
"""

from numpy.linalg import eigh
import numpy as np


def mds_eigh(D, p=2):
    """Computes the p-dimensional scaling using pairwise distance matrix D of size n.
    
    Returns matrix of n p-dimensional vectors such that distances between vectors match target 
    distances from distance matrix D as close as possible. 
    """
    D2 = D ** 2
    av = D2.mean(axis=0)
    B = -.5 * ((D2 - av).T - av + D2.mean())
    evals, evecs = eigh(B)  # few biggest evals / evecs ?
    pvals = evals[-p:] ** .5
    pvecs = evecs[:, -p:]
    M = pvecs * pvals
    return M - M.mean(axis=0)


def do_mds(distances, instances_original_order):
    # copy instances and sort them
    instances = np.copy(instances_original_order)
    instances.sort()
    # distances between instances
    instance_distances = distances[np.ix_(instances, instances)]
    if not instance_distances.any():
        np.random.seed(1)
        instance_distances += np.random.rand(*instance_distances.shape)
        
    # do mds
    mds =  mds_eigh(instance_distances, p=2)

    # get vectors by original order
    return np.array([mds[instances.tolist().index(n)] for n in instances_original_order])


def k_mds(distances, instance, k):
    print('s nearest')
    nearest = k_nearest_neighbors(distances, instance, k)
    print('f nearest')
     
    # make sure nearest list is sorted by distance to instance 
    sort_idx = np.argsort(distances[instance, nearest])

    # make sure instance is first element in list even if distances are all equal
    nearest = list(nearest[sort_idx])
    if instance in nearest:
        nearest.remove(instance)
    nearest.insert(0, instance)
    nearest = np.array(nearest)
        
    # do mds on instances
    print('s domds')
    mds_sorted = do_mds(distances, nearest)
    print('f domds')

    # select first k
    instance_idx = np.arange(k, dtype=np.int)

    # return mds 
    return nearest[instance_idx], mds_sorted[instance_idx]


def k_nearest_neighbors(distances, instance, k):
    """Returns the k nearest neighbors including the instance itself."""
    return np.array(k_argmin(distances[instance,:], k+1))

import heapq

def k_argmin(values, k):
    vk = [(v,i) for i, v in enumerate(values)]
    vk_min = heapq.nsmallest(k, vk)
    return [i for v, i in vk_min]

