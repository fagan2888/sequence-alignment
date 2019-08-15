import copy
import random
import csv
import os

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
    # s1 : list = []
    # s2 : list = []
    # table : list = []
    # tree : Node
    # results : list = []

    def __init__(self, s1, s2):
        # Takes input as 2 strings, convert them into instance variables x and y
        self.s1 = []
        self.s2 = []
        self.table = []
        self.results = []
        self.tree = None
        self.s1.append('-')
        self.s2.append('-')
        for el in s1:
            self.s1.append(el)
        for el in s2:
            self.s2.append(el)
            
        # Init table
        for i in range(0, len(self.s1)-1):
            row = [{} for j in range(0, len(self.s2))]
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
            for col_index, el in enumerate(row):
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
            
                state['s1'].insert(0, self.s1[node.coord[0] + 1])
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
    
    def return_results(self):
        results_list = [self.results[0]['total_score'], len(self.results)]
        return results_list
    
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
    dec_val = int(n * 0.1)
    print("dec_val",dec_val)
    s2_length = random.randint(n-dec_val, n)

    options = ['A', 'C', 'T', 'G']
    s1 = ''.join(random.choice(options) for i in range(0,n))
    s2 = ''.join(random.choice(options) for i in range(0,n))

    return (s1, s2)

def run_timed_test(n : int):
    import time
    import gc
    with open('/home/wilbanbric/Desktop/COMP/sequence-alignment/results.csv', 'w') as results:
        writer = csv.writer(results)
        writer.writerow(["Results"])
        writer.writerow(["length", "Time (Seconds)", "Number of Trees", "Score"])

        sequences = []
        for i in range(1, n+1):
            seq = generate_sequence(i*5)
            inst = SequenceAlign(seq[0], seq[1])
            sequences.append(inst)
        
        # loading bar
        loading_bar = ['-'] * int(n+1)
        loading_bar[0] = '@'

        for index, dna in enumerate(sequences):
            iteration_n = index+1 * 5

            # Loading Bar
            print(n)
            loading_bar[index+1] = '@'
            os.system('clear')
            print (''.join(map(str, loading_bar)))

            #Time and generate seq
            start_time = time.time()

            # Align in Table
            dna.align()
            
            # Find Sequences
            dna.tree = Node({"coord":(-1,-1)})
            bottom_left = (len(dna.table)-1,len(dna.table[0])-1)
            dna.create_tree(bottom_left, dna.tree)
            dna.init_traverse_tree(dna.tree, bottom_left)
            
            #End
            end_time = time.time()
            total_time = end_time - start_time
            print(total_time)
            res = dna.return_results()

            res.insert(0, iteration_n)
            res.insert(1, total_time)
            writer.writerow(res)
            # dna.print_sequences()
            
max_len = input("Max length to test. Will count up in intervals of 5.")
run_timed_test(int(max_len))
