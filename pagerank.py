"""
Code you are given for using PageRank:
    - the power method for finding stationary distributions (given P^T)
    - the power method, modified to add the (1-alpha)/n term inside
           (still takes in the un-modified P^T as an input)
    - A function that reads graph data from a file, creating the adj. list
"""
import numpy as np


def ranking_sparse(mat, alpha, steps=100):
    """ Power method for pagerank, sparse-matrix friendly.
        Arguments:
            mat - the transpose of the transition matrix (P^T), either
                    an np.array (2d) or a sparse matrix.
            steps - the number of steps to take
            alpha - the teleport parameter (<1, but close to 1)
        Returns:
            x - the stationary distribution (the page rank)
    """
    n = mat.shape[0]
    x = np.random.rand(n)
    x /= sum(x)
    for it in range(steps):
        x = alpha*mat.dot(x)
        x += (1-alpha)/n  # add in the teleport part manually
        x /= sum(x)     # note: x + scalar adds scalar to each component of x
    return x


def ranking(mat, steps=100):
    """ Power method for pagerank (calculates stationary distribution)
        Arguments:
            mat - the transpose of the transition matrix (P^T) used
                    for the power method [or the pagerank matrix]
            steps - the number of steps to take
        Returns:
            x - the stationary distribution (the page rank)
    """
    n = mat.shape[0]
    x = np.random.rand(n)
    x /= sum(x)
    for it in range(steps):
        x = mat.dot(x)
        x /= sum(x)
    return x


def read_graph_file(fname, node_pre='n', adj_pre='a', edge_pre='e'):
    """ First, it reads lines with prefix n (for node) of the form
        n k name    and stores a dict. of names for the nodes.
        Reads adj. matrix data from a file, returning the adj. list.
        Format: A line starting with...
            - 'a' is read as  a k a b c   where a b c ... are the links from k
            - 'n' is instead read as  n k name  (the node's name)
            - 'e' is read as e k m (an edge k->m)

        Returns:
            adj - the adj. dictionary, with adj[k] -> list of neighbors of k
            n - the number of nodes in the graph
            names - the dictionary of node names, if they exist

        NOTE: the adj. list does not store dead nodes (with no links)
    """
    adj = {}
    names = {}
    n = 0  # track index of max node

    with open(fname, 'r') as fp:
        for line in fp:
            parts = line.split(' ')
            if len(parts) < 2:
                continue
            node = int(parts[1])
            n = max(n, node)
            if parts and parts[0][0] == 'n':
                names[node] = parts[2].strip('\n')
            elif parts and parts[0][0] == 'a':
                adj[node] = [int(p) for p in parts[2:]]
                largest = max(adj[node])
                n = max(n, largest)
            elif parts and parts[0][0] == 'e':
                v = int(parts[2])
                if node not in adj:
                    adj[node] = [v]
                else:
                    adj[node].append(v)
                n = max(n, v)

    return adj, n + 1, names
