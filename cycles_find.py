"""Find elementary circuits of a directed graph."""

from collections import defaultdict # new in Python 2.5
import networkx as nx

def circuits(G):
    """Find elementary circuits of a directed graph.
    
    An elementary circuit is a closed path where no node appears twice, except 
    that the first and last node are the same. Two elementary circuits are 
    distinct if they are not cyclic permutations of each other.

    Parameters
    ----------
    G : NetworkX Graph
       A directed graph.

    Returns
    -------
    A list of circuits, where each circuit is a list of nodes, with the first 
    and last node being the same.
    
    Example:
    >>> G = nx.DiGraph([(0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2)])
    >>> circuits(G)
    [[0, 0], [0, 1, 2, 0], [0, 2, 0], [1, 2, 1], [2, 2]]
    
    See Also
    --------
    cycles (for undirected graphs)
    
    References
    ----------
    
    The implementation follows pp. 79-80 of:
    .. [1] Finding all the elementary circuits of a directed graph.
       D.B. Johnson
       SIAM Journal on Computing 4, no. 1: 77-84.
       http://dx.doi.org/10.1137/0204007
    
    Jon Olav Vik, 2010-08-09
    """
    path = [] # stack of nodes (vertices) in current path
    blocked = defaultdict(bool) # vertex: blocked from search?
    B = defaultdict(list) # graph portions that yield no elementary circuit
    result = [] # list to accumulate the circuits found
    
    def unblock(thisnode):
        """Recursively unblock and remove nodes from B[thisnode]."""
        if blocked[thisnode]:
            blocked[thisnode] = False
            while B[thisnode]:
                unblock(B[thisnode].pop())
    
    def circuit(thisnode, startnode, component):
        closed = False # set to True if elementary path is closed
        path.append(thisnode)
        blocked[thisnode] = True
        for nextnode in component[thisnode]: # direct successors of thisnode
            if nextnode == startnode:
                result.append(path + [startnode])
                closed = True
            elif not blocked[nextnode]:
                if circuit(nextnode, startnode, component):
                    closed = True
        if closed:
            unblock(thisnode)
        else:
            for nextnode in component[thisnode]:
                if thisnode not in B[nextnode]: # TODO: use set for speedup?
                    B[nextnode].append(thisnode)
        path.pop() # remove thisnode from path
        return closed
    
    # Johnson's algorithm requires some ordering of the vertices
    for s in sorted(G):
        # Find the strong component K with least vertex (i.e. node) 
        # in the subgraph induced by s and its following nodes.
        subgraph = G.subgraph(node for node in G if node >= s)
        strongcomp = nx.strongly_connected_components(subgraph)
        component = G.subgraph(min(strongcomp, key=min))
        if component:
            startnode = min(component.nodes())
            for node in component:
                blocked[node] = False
                B[node][:] = []
            circuit(startnode, startnode, component)
        else:
            break
    
    return result

if __name__ == "__main__":
    import doctest
    doctest.testmod()

