from master_file_cayley import Letter
from master_file_cayley import Word
from master_file_cayley import WordTrie
from master_file_cayley import NewGroup
from graphviz import Digraph

import time
import os
import psutil
import networkx as nx
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pickle

process = psutil.Process(os.getpid())


print(process.memory_info().rss / 10 ** 6)

class Cayley:
    # the purpose of this class is to store the data from previously
    # generated Groups and produce Cayley graphs from that data. In fact,
    # if I can, I can also create a program that will output a bunch of
    # text that can be fed into different
    def __init__(self):
        self._paranoid = True
        self._graph = nx.Graph()

    def read_newgraph(self, a_group):
        # this is the same code i've been using to output all of the group graphics so far (so any and
        # all networkx/matplotlib graphics). i allowed for the user to input the numerator and denominator
        # as that would be simpler. the purpose of this class is in part to limit the computational effort
        # for each yielding of edges, etc. However, if this is just being called and the graph hasn't been
        # constructed yet then we might as well give the user some choice.
        if self._paranoid:
            if not isinstance(a_group, NewGroup):
                raise Exception("only groups with this method")

        num1 = int(input("numerator? "))
        num2 = int(input("denominator? "))

        color_list = ['b', 'r', 'c', 'm', 'y', 'k']

        identity = Word([])
        elements = [identity]
        non_e_elements = a_group.yield_elems_of_quotient(num1, num2)
        for entry in non_e_elements:
            elements.append(entry)

        i = 0

        generators = a_group.list_non_inv_generators()

        for member in elements:
            # print(member)
            for j in range(len(generators)):
                gen_letter = generators[j]
                elem_with_letter = Word([])
                elem_with_letter.add_word(member)
                elem_with_letter.add_letter(gen_letter)
                # print(elem_with_letter)
                for member_2 in elements:
                    if a_group.test_equals(elem_with_letter, member_2, num2):
                        # print(elem_with_letter.return_word_str() + " == " + member_2.return_word_str())
                        # print(member.return_word_str() + " is connected to " + member_2.return_word_str() +
                              # " by " + gen_letter.get_str())
                        self._graph.add_edges_from([(member, member_2)], color=color_list[j])
                        break

            i = i + 1
            print(str(i) + " out of " + str(len(elements)) + " completed \n")

        # print(str(self._graph.number_of_nodes()) + " is the number of nodes")
        # print(str(self._graph.number_of_edges()) + " is the number of edges")

        pickel = input("Do you want me to pickle this graph? Y/N ")
        if pickel.lower() == 'y':
            self.pickle_me()

        group_p = input("Do you want me to pickle this group? Y/N ")
        if group_p.lower() == "y":
            self.pickle_my_group(a_group)

    def read_pickle(self, a_str):
        # this allows the user to input a pickle file for the graph rather
        # than having to generate the graph every time.
        self._graph = pickle.load(open(a_str, 'rb'))

        if not self._graph.nodes():
            raise Exception("there might be a problem, no nodes")

        self.draw()

    def read_pickle_group(self, a_str):
        # this allows for a cayley object to read in a group from a pickle
        # rather than having to generate the group every time. This massively
        # increases the efficiency for larger groups.

        a_group = pickle.load(open(a_str, 'rb'))
        if self._paranoid:
            if not isinstance(a_group, NewGroup):
                raise Exception("This didn't read in a group")

        self.read_newgraph(a_group)

    def feed_pickle(self):
        # this takes a string input for the file name and feeds it to read pickle
        file_name = input("Please type the exact document name into this input: ")

        self.read_pickle(file_name)

    def draw(self):
        # this draws the graph that has been stored in the cayley object.
        if self._paranoid:
            if not self._graph.nodes():
                raise Exception("There's nothing to print, you haven't populated me with a graph yet")

        # word labels
        word_labels = {}
        for i in self._graph.nodes():
            word_labels[i] = i.return_word_str()

        # edge colors
        edges = self._graph.edges()
        colors = [self._graph[u][v]['color'] for u, v in edges]

        options = {
            'node_color': 'yellow',
            'node_size': 400,
        }
        pos = nx.spring_layout(self._graph)

        save_file = input("Do you want me to save this file? Y/N ")
        if save_file.lower() == 'y':
            denom = int(input("denominator? numbers only please "))
            group = str(input("what group is this? i.e. g2, g3, etc. "))
            version_num = str(input("what version i.e. 1, 2, etc. "))
            imagename = "ngroup.cayley." + group + ".(4," + str(denom) + ") - " + version_num + ".png"
            plt.savefig(imagename)

        print(str(self._graph.number_of_nodes()) + " is the number of nodes")
        print(str(self._graph.number_of_edges()) + " is the number of edges")

        plt.subplot()
        nx.draw(self._graph, pos, **options, labels=word_labels, edge_color=colors)
        plt.show()

    def pickle_me(self):
        input_name = str(input("What do you want me to name the pickle file "))
        filename = 'pickles/' + input_name + ".txt"
        print('hello')
        pickle.dump(self._graph, open(filename, 'wb'))
        print("saved to: "+filename)

    def pickle_my_group(self, a_group):
        if self._paranoid:
            if not isinstance(a_group, NewGroup):
                raise Exception("This is only for pickling groups")

        group_name = str(input("What should I name this group pickle? "))
        filename = 'pickles/' + group_name + ".txt"
        pickle.dump(self._graph, open(filename, 'wb'))
        print("saved to: " + filename)

    def export_gv(self):
        if self._paranoid:
            if not self._graph.nodes():
                raise Exception("I need a graph first")

        graphviz_output = Digraph()

        nodes = self._graph.nodes()
        for node in nodes:
            graphviz_output.node(node.return_word_str())

        edges = self._graph.edges()
        colors = [self._graph[u][v]['color'] for u,v in edges]
        i = 0
        for (u, v) in edges:
            graphviz_output.edge(u, v, colors[i])
            i = i+1


num = int(input("Max num? "))

a = Letter("a")
b = Letter("b")
A = Letter("A")
B = Letter("B")

identity = Word([])

a_word = Word([a])
b_word = Word([b])

aa = Word([a, a])
aA = Word([a, A])
bB = Word([b, B])
bb = Word([b, b])
ababab = Word([a, b, a, b, a, b])
bbb = Word([b, b, b])
bbbbbb = Word([b, b, b, b, b, b])
abab = Word([a, b, a, b])
abAB = Word([a, b, A, B])

group_selection = input("Which group? G2/G3/G4 exclusively ")
if group_selection.lower() == "g2":
    G = NewGroup([a, b], [aa, bbbbbb, aA, bB, abAB], num)
elif group_selection.lower() == "g3":
    G = NewGroup([a, b], [aa, bbbbbb, aA, bB, abab], num)
elif group_selection.lower() == "g4":
    G = NewGroup([a, b], [aa, bbb, aA, bB, ababab], num)
else:
    raise Exception("for the code to proceed, I need to make some G so I had to stop")


newCayley = Cayley()

newCayley.read_newgraph(G)
newCayley.draw()


# secondCayley = Cayley()
# secondCayley.feed_pickle()
# secondCayley.export_gv()
