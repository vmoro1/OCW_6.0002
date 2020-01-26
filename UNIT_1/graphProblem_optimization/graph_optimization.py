import unittest
from graph import Digraph, Node, WeightedEdge


def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph.
    Each entry in the map file consists of the following four positive
    integers, separated by a blank space: From To TotalDistance DistanceOutdoors
    e.g. 32 76 54 23. This entry would become an edge from 32 to 76.

    map_filename : name of the map file

    Returns: a Digraph representing the map
    """
    digraph = Digraph()
    with open(map_filename, 'r') as file:
        read_data = file.read().split("\n")
        read_data = read_data[:-1]
        for edge in read_data:
            data = edge.split()
            for node in range(2):
                if not digraph.has_node(data[node]):
                    digraph.add_node(data[node])
            weighted_edge = WeightedEdge(data[0], data[1], data[2], data[3])
            digraph.add_edge(weighted_edge)
    return digraph

#print(load_map('mit_map.txt'))


def getDistance(digraph, path):
    total_dist = 0
    outdoor_dist = 0
    for i in range(len(path) - 1):
        for edge in digraph.edges[path[i]]:
            if edge.dest == path[i + 1]:
                total_dist += edge.get_total_distance()
                outdoor_dist += edge.get_outdoor_distance()
    return (total_dist, outdoor_dist)

## not finished
    
def get_best_path(digraph, start, end, path, max_dist_outdoors, best_dist,
                  best_path):
    """
    Finds the shortest path between buildings subject to constraints.

    digraph: Digraph instance
    start: Building number at which to start (string)
    end: Building number at which to end (string)
    path: list composed of [[list of strings], int, int]
    Represents the current path of nodes being traversed. Contains a list of 
    node names, total distance traveled, and total distance outdoors.
    max_dist_outdoors: Maximum distance spent outdoors on a path (int)
    best_dist: The smallest distance between the original start and end node
    for the initial problem that you are trying to solve (int)
    best_path: list of strings The shortest path found so far between the 
    original start and end node.

    Returns: A tuple with the shortest-path from start to end, represented by
    a list of building numbers (in strings), [n_1, n_2, ..., n_k],where there 
    exists an edge from n_i to n_(i+1) in digraph. If there exists no path that
    satisfies max_total_dist and max_dist_outdoors constraints, then return None.
    """
    path += [start]
    if start not in digraph.nodes:
        raise ValueError('Invalid Node')
    elif start == end:
        return path
    else:
        for node in digraph.get_edges_for_node(start):
            if node.dest not in path:
                if best_path == None or len(best_path) < len(path):
                    new_path = get_best_path(digraph, node.dest, end, 
                                path, max_dist_outdoors, best_dist, best_path)
                    if new_path != None:
                        total_dist, outdoor_dist = getDistance(digraph, new_path)
                        if outdoor_dist <= max_dist_outdoors and total_dist <= best_dist:
                            best_path = new_path
                            best_dist = total_dist
    return best_path


##not finished

def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not exceed 
    max_total_dist, and the distance spent outdoors on this path must not 
    exceed max_dist_outdoors.

    digraph: Digraph instance
    start: Building number at which to start (string)
    end: Building number at which to end (string)
    max_total_dist: Maximum total distance on a path (int)
    max_dist_outdoors: Maximum distance spent outdoors on a path (int)

    Returns: The shortest-path from start to end represented by a list of 
    building numbers (in strings), [n_1, n_2, ..., n_k], where there exists an 
    edge from n_i to n_(i+1) in digraph. If there exists no path that satisfies 
    max_total_dist and max_dist_outdoors constraints, then raises a ValueError.
    """
    start = Node(start)
    end = Node(end)
    best_path = get_best_path(digraph, start, end, [], max_dist_outdoors, max_total_dist, None)

    if best_path == None:
        raise ValueError
    return best_path 


##Test code

#class Ps2Test(unittest.TestCase):
#    LARGE_DIST = 99999
#
#    def setUp(self):
#        self.graph = load_map("mit_map.txt")
#
#    def test_load_map_basic(self):
#        self.assertTrue(isinstance(self.graph, Digraph))
#        self.assertEqual(len(self.graph.nodes), 37)
#        all_edges = []
#        for _, edges in self.graph.edges.items():
#            all_edges += edges  # edges must be dict of node -> list of edges
#        all_edges = set(all_edges)
#        self.assertEqual(len(all_edges), 129)
#
#    def _print_path_description(self, start, end, total_dist, outdoor_dist):
#        constraint = ""
#        if outdoor_dist != Ps2Test.LARGE_DIST:
#            constraint = "without walking more than {}m outdoors".format(
#                outdoor_dist)
#        if total_dist != Ps2Test.LARGE_DIST:
#            if constraint:
#                constraint += ' or {}m total'.format(total_dist)
#            else:
#                constraint = "without walking more than {}m total".format(
#                    total_dist)
#
#        print("------------------------")
#        print("Shortest path from Building {} to {} {}".format(
#            start, end, constraint))
#
#    def _test_path(self,
#                   expectedPath,
#                   total_dist=LARGE_DIST,
#                   outdoor_dist=LARGE_DIST):
#        start, end = expectedPath[0], expectedPath[-1]
#        self._print_path_description(start, end, total_dist, outdoor_dist)
#        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
#        print("Expected: ", expectedPath)
#        print("DFS: ", dfsPath)
#        self.assertEqual(expectedPath, dfsPath)
#
#    def _test_impossible_path(self,
#                              start,
#                              end,
#                              total_dist=LARGE_DIST,
#                              outdoor_dist=LARGE_DIST):
#        self._print_path_description(start, end, total_dist, outdoor_dist)
#        with self.assertRaises(ValueError):
#            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
#
#    def test_path_one_step(self):
#        self._test_path(expectedPath=['32', '56'])
#
#    def test_path_no_outdoors(self):
#        self._test_path(
#            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)
#
#    def test_path_multi_step(self):
#        self._test_path(expectedPath=['2', '3', '7', '9'])
#
#    def test_path_multi_step_no_outdoors(self):
#        self._test_path(
#            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)
#
#    def test_path_multi_step2(self):
#        self._test_path(expectedPath=['1', '4', '12', '32'])
#
#    def test_path_multi_step_no_outdoors2(self):
#        self._test_path(
#            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
#            outdoor_dist=0)
#
#    def test_impossible_path1(self):
#        self._test_impossible_path('8', '50', outdoor_dist=0)
#
#    def test_impossible_path2(self):
#        self._test_impossible_path('10', '32', total_dist=100)
#
#
#if __name__ == "__main__":
#    unittest.main()