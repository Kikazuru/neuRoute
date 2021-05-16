import networkx as nx
import matplotlib.pyplot as plt

from utm import from_latlon

class TSP:
    def __init__(self):
        self.daftar_lokasi = [None]
        self.graf = None
        self.n = None

    def show_graf(self):
        G = nx.Graph()
        
        for lokasi in self.daftar_lokasi:
            nama = lokasi["nama"]
            koordinat = lokasi["koordinat"]
            G.add_node(nama, pos=(koordinat[0],koordinat[1]))

        for i in range(self.n):
            nama1 = self.daftar_lokasi[i]["nama"]
            for j in range(i + 1, self.n):
                nama2 = self.daftar_lokasi[j]["nama"]
                G.add_edge(nama1, nama2, weight = self.graf[i][j])

        pos=nx.get_node_attributes(G,'pos')
        nx.draw(G,pos)
        nx.draw_networkx_labels(G, pos, font_size=12, font_family="sans-serif")
        labels = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
        plt.savefig("figure/hasil.png")

    def conversion(self, location):
        res = from_latlon(location[0], location[1])[:2]
        return res

    def add_node(self, name, location):
        self.daftar_lokasi.append({"nama":name, "koordinat":self.conversion(location)})
    
    def add_curr(self, location):
        self.daftar_lokasi[0] = {
            "nama":"your location",
            "koordinat":self.conversion(location)
        }

    def generate_graf(self):
        if self.daftar_lokasi[0] != None:
            self.n = n = len(self.daftar_lokasi)
            self.graf = [[0] * n for _ in range(n)]
            for i in range(n):
                x1, y1 = self.daftar_lokasi[i]["koordinat"]
                for j in range(i + 1, n):
                    x2, y2 = self.daftar_lokasi[j]["koordinat"]
                    jarak = (abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2) ** (0.5)
                    self.graf[i][j] = round(jarak, 4)
                    self.graf[j][i] = round(jarak, 4)
    
    def getCombination(self, arr, combination):
        comb = []
        for x, y in combination:
            temp = arr.copy()
            temp[x], temp[y] = temp[y], temp[x]
            comb.append(temp)
        return comb

    def evaluate(self, arr):
        cost = 0
        frm = 0
        for to in arr:
            cost += self.graf[frm][to]
            frm = to

        cost += self.graf[frm][0]
        return cost

    # SAHC
    def solve(self):
        # mencari kombinasi untuk operator switch
        operator = []
        n = self.n

        if n != None:
            for i in range(0,n):
                for j in range(i + 1, n):
                    operator.append((i,j))

            initial_path = [i for i in range(n)]
            min_cost = (initial_path, self.evaluate(initial_path))

            tabu_list = [initial_path]

            while True:
                list_combination = self.getCombination(min_cost[0], operator)
                cek = False
                for comb in list_combination:
                    if comb not in tabu_list:
                        cost = self.evaluate(comb)
                        if cost < min_cost[1]:
                            cek = True
                            min_cost = (comb, cost)
                            tabu_list.append(comb)
                
                if not cek:
                    break
            
            path = min_cost[0]
            idx = path.index(0)

            path = path[idx:] + path[:idx]

            min_cost = ([self.daftar_lokasi[i]["nama"] for i in path], min_cost[1])

            return min_cost