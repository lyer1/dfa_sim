import networkx as nx
import matplotlib.pyplot as plt

class DFA:
  def __init__(self, states, alphabet, transition_function, start_state, accept_states):
    self.states = states
    self.alphabet = alphabet
    self.transition_function = transition_function
    self.start_state = start_state
    self.accept_states = accept_states
    self.current_state = start_state

  def transition(self, string):
    for char in string:
      self.current_state = self.transition_function[(self.current_state, char)]
    return self.current_state

  def accepts(self, string):
    return self.transition(string) in self.accept_states

  def visualize(self):
    graph = nx.DiGraph()
    for state in self.states:
      graph.add_node(state)
    for transition in self.transition_function:
      graph.add_edge(transition[0], self.transition_function[transition], label=transition[1])
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos, nodelist=self.states, node_color='lightblue', node_size=600)
    nx.draw_networkx_nodes(graph, pos, nodelist=self.accept_states, node_color='pink', node_size=600)
    nx.draw_networkx_nodes(graph, pos, nodelist=[self.start_state], node_color='yellow', node_size=600)
    nx.draw_networkx_labels(graph, pos, font_color='black')
    nx.draw_networkx_edges(graph, pos, edgelist=self.transition_function.keys(), arrowsize=20)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels={(k[0], v): k[1] for k, v in self.transition_function.items()})
    plt.axis('off')
    plt.show()

states = {0, 1, 2}
alphabet = {'0', '1'}
transition_function = {
  (0, '0'): 0,
  (0, '1'): 1,
  (1, '0'): 2,
  (1, '1'): 1,
  (2, '0'): 1,
  (2, '1'): 2
}
start_state = 0
accept_states = {1}

dfa = DFA(states, alphabet, transition_function, start_state, accept_states)
dfa.visualize()
