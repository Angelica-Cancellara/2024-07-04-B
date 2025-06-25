from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._nodes = []
        self._edges = []
        self._idMap = {}
        self._graph = nx.Graph()
        self._architot = []

    def getAnni(self):
        return DAO.getYears()

    def getState(self, anno):
        return DAO.getState(anno)

    def buildGraph(self, anno, stato):
        self._graph.clear()
        self._nodes = DAO.getNodi(anno, stato)
        self._graph.add_nodes_from(self._nodes)

        self._idMap = {}
        for n in self._nodes:
            self._idMap[n.id] = n

        self._architot = DAO.getArchi(anno, stato, self._idMap)
        for e in self._architot:
            if e[0].distance_HV(e[1]) < 100:
                self._edges.append((e[0], e[1]))
                self._graph.add_edge(e[0], e[1])

    def getNumNodi(self):
        return self._graph.number_of_nodes()

    def getNumEdges(self):
        return self._graph.number_of_edges()

    def getNumCompConessa(self):
        return nx.number_connected_components(self._graph)

    def getLargestConnessa(self):
        conn = list(nx.connected_components(self._graph))
        conn.sort(key=lambda x: len(x), reverse=True)
        return conn[0]

