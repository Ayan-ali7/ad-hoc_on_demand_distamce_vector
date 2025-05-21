import networkx as nx 
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import time

class AODVNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.routing_table = {}
        self.graph = None

    def initialize_distances(self, neighbors):
        for node_id in self.graph.nodes:
            if node_id in neighbors:
                self.routing_table[node_id] = {'distance': 1, 'next_hop': node_id}
            elif node_id == self.node_id:
                self.routing_table[node_id] = {'distance': 0, 'next_hop': self.node_id}
            else:
                self.routing_table[node_id] = {'distance': float('inf'), 'next_hop': None}

    def update_distance(self, destination, new_distance, next_hop):
        if new_distance < self.routing_table[destination]['distance']:
            self.routing_table[destination] = {'distance': new_distance, 'next_hop': next_hop}

    def route_discovery(self, destination_node_id):
        print(f"Node {self.node_id} initiates route discovery for {destination_node_id}")
        # Simulate RREQ broadcast to neighbors
        for neighbor_id in self.graph.neighbors(self.node_id):
            self.send_rreq(destination_node_id, neighbor_id)

    def send_rreq(self, destination, neighbor):
        print(f"Node {self.node_id} broadcasting RREQ for {destination} via {neighbor}")
        time.sleep(0.1)  # Simulate transmission delay
        self.graph.nodes[neighbor]['obj'].handle_rreq(self.node_id, destination)

    def handle_rreq(self, source, destination):
        print(f"Node {self.node_id} handling RREQ from {source} to {destination}")
        self.update_distance(destination, self.routing_table[source]['distance'] + 1, source)
        time.sleep(0.1)  # Simulate processing delay
        self.send_rrep(source, destination)

    def send_rrep(self, source, destination):
        print(f"Node {self.node_id} sending RREP for {destination} to {source}")
        time.sleep(0.1)  # Simulate transmission delay
        self.graph.nodes[source]['obj'].handle_rrep(self.node_id, destination)

    def handle_rrep(self, source, destination):
        print(f"Node {self.node_id} handling RREP from {source} to {destination}")
        self.update_distance(destination, self.routing_table[source]['distance'] + 1, source)

    def display_routing_table(self):
        table = PrettyTable(['Destination', 'Distance', 'Next Hop'])
        table.align = 'l'
        for dest, values in self.routing_table.items():
            table.add_row([dest, values['distance'], values['next_hop']])
        print(f"Routing table for Node {self.node_id}:\n{table}")

def generate_connected_graph(num_nodes):
    G = nx.connected_watts_strogatz_graph(num_nodes, 4, 0.1)
    return G

def visualize_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, font_weight='bold')
    plt.show()

def simulate_aodv(graph, source_node_id,destination_node_id):
    nodes = {node_id: AODVNode(node_id) for node_id in graph.nodes}

    for node_id in graph.nodes:
        nodes[node_id].graph = graph  # Set the graph attribute for each node
        graph.nodes[node_id]['obj'] = nodes[node_id]  # Store node object in the graph

    for node_id in graph.nodes:
        neighbors = list(graph.neighbors(node_id))
        nodes[node_id].initialize_distances(neighbors)

    graph.time_instance = 0

    for node_id in graph.nodes:
        nodes[node_id].display_routing_table()

    source_node = nodes[source_node_id]
    destination_node = nodes[destination_node_id]

    source_node.route_discovery(destination_node_id)

    for node_id in graph.nodes:
        nodes[node_id].display_routing_table()

# Example usage:
num_nodes = 10
G = generate_connected_graph(num_nodes)
visualize_graph(G)
simulate_aodv(G, 0, 7)