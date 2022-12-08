from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Line, Color
from collections import defaultdict


class Node(Button):
    def __init__(self, text, pos, ** kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.pos = pos
        self.size_hint = (None, None)
        self.size = ("40dp", "40dp")
        self.first_click_ever = True


class Edge(Line):
    def __init__(self, pt1, pt2, ** kw):
        super().__init__(**kw)
        self.points = (pt1[0], pt1[1], pt2[0], pt2[1])


class GraphCanvas(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nb = 0
        self.nodes = []
        self.selected_node = None
        self.graph = defaultdict(list)

    def creation_possible(self, pos):
        possible = True
        i = 0
        while i < len(self.nodes) and possible:
            node = self.nodes[i]["pos"]
            if pos[0] >= node[0] - dp(50) and pos[0] <= node[0] + dp(50):
                if pos[1] >= node[1] - dp(50) and pos[1] <= node[1] + dp(50):
                    possible = False
            i += 1
        return possible

    def create_node(self, args):
        pos = args[1].pos
        if self.creation_possible(pos):
            n = Node(text=str(self.nb), pos=pos)
            self.add_widget(n)
            self.nodes.append({"name": self.nb, "pos": pos, "button": n})
            self.nb += 1

    def create_edge(self, pt1, pt2):
        with self.canvas:
            Color(58/255, 134/255, 255/255)
            Edge(pt1, pt2, width=2)

    def select_node(self, btn):
        if btn.first_click_ever:
            btn.first_click_ever = False
        else:
            if self.selected_node == None:
                self.selected_node = btn
            elif self.selected_node == btn:
                self.selected_node = None
            else:
                self.create_edge(btn.pos, self.selected_node.pos)
                self.graph[int(btn.text)].append(int(self.selected_node.text))
                self.graph[int(self.selected_node.text)].append(int(btn.text))
                self.selected_node = None


class RootContainer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Time = 0
        self.graph = None
        self.V = 0
        self.nodes = None

    def APUtil(self, u, visited, ap, parent, low, disc):
        children = 0
        visited[u] = True
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1
        for v in self.graph[u]:
            if visited[v] == False:
                parent[v] = u
                children += 1
                self.APUtil(v, visited, ap, parent, low, disc)
                low[u] = min(low[u], low[v])
                if parent[u] == -1 and children > 1:
                    ap[u] = True
                if parent[u] != -1 and low[v] >= disc[u]:
                    ap[u] = True
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])

    def AP(self):
        visited = [False] * (self.V)
        disc = [float("Inf")] * (self.V)
        low = [float("Inf")] * (self.V)
        parent = [-1] * (self.V)
        ap = [False] * (self.V)
        for i in range(self.V):
            if visited[i] == False:
                self.APUtil(i, visited, ap, parent, low, disc)

        for index, value in enumerate(ap):
            if value == True:
                for node in self.nodes:
                    if node["name"] == index:
                        button = node["button"]
                        with button.canvas:
                            Color(0, 1, 0, 1)
                            Line(
                                circle=(button.pos[0]+20, button.pos[1]+20, 20), width=2)

    def find_joint_nodes(self, nodes, graph):
        self.graph = graph
        self.nodes = nodes
        self.V = len(nodes)
        self.AP()

    def clear(self, graph):
        graph.clear_widgets()
        graph.canvas.clear()
        graph.nb = 0
        self.graph = None
        self.nodes = None
        self.V = 0


class GrapheApp(App):
    pass


if __name__ == "__main__":
    GrapheApp().run()
