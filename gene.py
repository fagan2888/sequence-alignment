import copy
import random

class Node:
    coord : tuple
    children : list

    def __init__(self, data):
        self.coord = data['coord']
        self.children = []

    def add_child(self, data):
        self.children.append(data)
    
    def print_tree(self):
        level = ''
        for child in self.children:
            level += str(child.coord)
        print(level)
        for child in self.children:
            child.print_tree()

class SequenceAlign:
    s1 : list = []
    s2 : list = []
    table : list = []
    tree : Node
    results : list = []

    def __init__(self, s1, s2):
        # Takes input as 2 strings, convert them into instance variables x and y
        self.s1.append('-')
        self.s2.append('-')
        for el in s1:
            self.s1.append(el)
        for el in s2:
            self.s2.append(el)

        # Init table
        for i in range(0, len(self.s1)):
            row = [{} for j in range((len(self.s2)))]
            for el in row:
                el['coord'] = (0,0)
                el["total_score"] = 0
                el["score"] = 0
                el["parents"] = []
                el["type"] = None
            self.table.append(row)
    
    def align(self):
        row_index = 0
        col_index = 0
        for row in self.table:
            for el in row:
                # Get parent values in list
                el['coord'] = (row_index, col_index)
                if (row_index == 0 and col_index == 0):   # Case: top left cell, start cell
                    el['type'] = 'start'
                else:
                    if(row_index == 0 and col_index != 0):    # Case: top row disabled. Only move is accross.
                        el['total_score'] = self.table[row_index][col_index-1]['total_score'] - 2
                        el['type'] = 's2gap'
                        el['score'] = (-2)
                        el['parents'].append((row_index, col_index-1))
                    elif(col_index == 0 and row_index != 0):   # Case: side column disabled. Only move is down.
                        el['total_score'] = self.table[row_index-1][col_index]['total_score'] - 2
                        el['type'] = 's1gap'
                        el['score'] = (-2)
                        el['parents'].append((row_index-1, col_index))
                    else:
                        # A - Diagonal
                        if (self.s1[row_index] == self.s2[col_index]):
                            a_totalscore = self.table[row_index-1][col_index-1]['total_score'] + 1
                            el['score'] = 1
                        else:
                            a_totalscore = self.table[row_index-1][col_index-1]['total_score'] - 1
                            el['score'] = (-1)
                        # B/C - Gaps
                        b_totalscore = self.table[row_index-1][col_index]['total_score'] - 2  # B
                        c_totalscore = self.table[row_index][col_index-1]['total_score'] - 2  # C

                        values = [a_totalscore, b_totalscore, c_totalscore]    # represented in order, A -> B -> C
                        
                        # Find max - we find the max score possible in this cell and add those parents to the element dictionary object
                        max_score = max(values)
                        val_index = [i for i, j in enumerate(values) if j == max_score]
                        for i in val_index:
                            if (i == 0):  # A
                                el['type'] = 'match/mismatch'
                                el['total_score'] = values[i]
                                el['parents'].append((row_index-1, col_index-1))
                            if (i == 1):  # B
                                el['type'] = 's1Gap'
                                el['total_score'] = values[i]
                                el['score'] = (-2)
                                el['parents'].append((row_index-1, col_index))
                            if (i == 2):  # C
                                el['type'] = 's2Gap'
                                el['total_score'] = values[i]
                                el['score'] = (-2)
                                el['parents'].append((row_index, col_index-1))
                col_index += 1
                el = None
            col_index = 0
            row_index += 1

    def create_tree(self, coord : tuple, parent_node : Node):
        data = self.table[coord[0]][coord[1]]
        node = Node(data)
        parent_node.add_child(node)
        for coord in data['parents']:
            self.create_tree(coord, node)

    def init_traverse_tree(self, node : Node, bottom_left : tuple):
        return self.traverse_tree(
            node.children[0], 
            {
                "s1" : [],
                "s2" : [],
                "score" : [],
                "prior_coord" : copy.deepcopy(bottom_left),
                "total_score" : 0
            },
            True
        )

    def traverse_tree(self, node, state, first_iteration):
        if (not first_iteration):
            if (state["prior_coord"][0] - 1 == node.coord[0] and state["prior_coord"][1] - 1 == node.coord[1]):
                if (self.s1[node.coord[0] + 1] == self.s2[node.coord[1] + 1]):
                    state['score'].insert(0, "+")
                    state['total_score'] += 1
                else:
                    state['score'].insert(0, "-")
                    state['total_score'] -= 1
                state['s1'].insert(0, self.s1[node.coord[0] + 1])
                state['s2'].insert(0, self.s2[node.coord[1] + 1])
            elif (state["prior_coord"][0] - 1 == node.coord[0] and state["prior_coord"][1] == node.coord[1]):
                # S2 Gap
                state['s1'].insert(0, self.s1[node.coord[1] + 1])
                state['s2'].insert(0, '-')
                state['score'].insert(0, "*")
                state['total_score'] -= 2
            elif (state["prior_coord"][0] == node.coord[0] and state["prior_coord"][1] - 1 == node.coord[1]):
                # S1 Gap
                state['s2'].insert(0, self.s2[node.coord[1] + 1])
                state['s1'].insert(0, '-')
                state['score'].insert(0, "*")
                state['total_score'] -= 2
        
            # Modify state        
            state['prior_coord'] = copy.deepcopy(node.coord)
            if (len(node.children) == 0):
                node.children = []
                self.results.append(state)
                return

            # Recurse - for loop causing issues with rec? amount of children might be issue
        for child in node.children:
            self.traverse_tree(child, copy.deepcopy(state), False)

    def print_sequences(self):
        for seq in self.results:
            print(' '.join(seq['s1']))
            print(' '.join(seq['s2']))
            print(' '.join(seq['score']), "\t", seq['total_score'])
            print('\n')
    
    def print_table(self):
        first_line = self.s2.copy()
        first_line.insert(0, ' ')
        print(' '.join(first_line))
        i = 0
        for row in self.table:
            line = ''
            line += self.s1[i]
            for el in row:
                line += str(el['total_score'])
            print(' '.join(line))
            i += 1

def generate_sequence(n : int):
    s2_length = random.randint(1, n)

    options = ['A', 'C', 'T', 'G']
    s1 = ''.join(random.choice(options) for i in range(n))
    s2 = ''.join(random.choice(options) for i in range(n))

    return (s1, s2)



seq = generate_sequence(100)
seq1 = seq[0]
seq2 = seq[1]
dna = SequenceAlign(seq1, seq2)
dna.align()
bottom_left = (len(dna.table)-1,len(dna.table[0])-1)
dna.tree = Node({"coord":(-1,-1)})
dna.create_tree(bottom_left, dna.tree)
dna.init_traverse_tree(dna.tree, bottom_left)
dna.print_sequences()
