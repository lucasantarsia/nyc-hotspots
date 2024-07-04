import copy
import random

import networkx as nx

from database.DAO import DAO

from geopy.distance import distance


class Model:
    def __init__(self):
        self._providers = DAO.getAllProviders()
        self._graph = nx.Graph()

    def buildGraph(self, provider, soglia):
        # locations = DAO.getLocationsOfProvider(provider)
        locations = DAO.getLocationsOfProviderV2(provider)
        self._graph.add_nodes_from(locations)

        # Aggiungere archi
        # Modo 1: faccio una query e mi restituisce gli archi
        # allEdges = DAO.getAllEdges(provider)
        # for edge in allEdges:
        #     l1 = edge[0]
        #     l2 = edge[1]
        #     dist = distance((l1.Latitude, l1.Longitude), (l2.Latitude, l2.Longitude)).km
        #     if dist < soglia:
        #         self._graph.add_edge(l1.Location, l2.Location, weight=dist)
        # print(f"Modo 1: {self._graph.nodes} nodi e {self._graph.edges} archi")

        self._graph.clear_edges()

        # Modo 2: modifico il metodo del dao che legge i nodi, e ci aggiungo le coordinate di ogni location
        # Dopo, doppio ciclo sui nodi e mi calcolo la distanza in python
        for u in self._graph.nodes:
            for v in self._graph.nodes:
                if u != v:
                    dist = distance((u.Latitude, u.Longitude), (v.Latitude, v.Longitude)).km
                    if dist < soglia:
                        self._graph.add_edge(u, v, weight=dist)
        print(f"Modo 1: {self._graph.nodes} nodi e {self._graph.edges} archi")

        # Modo 3: doppio ciclo sui nodi, e per ogni "possibile" arco faccio una query

    def getNodesMostVicini(self):
        listTuples = []
        for v in self._graph.nodes:
            listTuples.append((v, len(list(self._graph.neighbors(v)))))
        listTuples.sort(key=lambda x: x[1], reverse=True)

        result = list(filter(lambda x: x[1] == listTuples[0][1], listTuples))

        # Oppure:
        # result = [x for x in listTuples if x[1] == listTuples[0][1]]
        return result

    def getCammino(self, target, subString):
        sources = self.getNodesMostVicini()
        source = sources[random.randint(0, len(sources)-1)][0]

        if not nx.has_path(self._graph, source, target):
            print(f"{source} e {target} non sono connessi")
            return [], source

        self._bestPath = []
        self._bestLen = 0
        parziale = [source]

        self._ricorsione(parziale, target, subString)

        return self._bestPath, source

    def _ricorsione(self, parziale, target, subString):
        if parziale[-1] == target:
            # devo uscire, ma prima controllo che sia una soluzione ottima
            if len(parziale) > self._bestLen:
                self._bestLen = len(parziale)
                self._bestPath = copy.deepcopy(parziale)
            return

        for v in self._graph.neighbors(parziale[-1]):
            if v not in parziale and subString not in v.Location:
                parziale.append(v)
                self._ricorsione(parziale, target, subString)
                parziale.pop()

    def getAllProviders(self):
        return self._providers

    def getAllLocations(self):
        return list(self._graph.nodes)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)


    def getBestPath(self, source, target, stringa):
        self._bestPath = []
        self._bestLen = 0

        parziale = [source]
        self.ricorsione(parziale, target, stringa)

        return self._bestPath

    def ricorsione(self, parziale, target, stringa):
        if parziale[-1] == target:
            if len(parziale) > self._bestLen:
                self._bestPath = copy.deepcopy(parziale)
                self._bestLen = len(parziale)
            return

        for n in nx.neighbors(self._graph, parziale[-1]):
            if n not in parziale and stringa not in n.Location:
                parziale.append(n)
                self.ricorsione(parziale, target, stringa)
                parziale.pop()
