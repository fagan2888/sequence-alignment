import copy

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
        # print(self.table)
        # self.print_table()
    
    def align(self):
        row_index = 0
        col_index = 0
        for row in self.table:
            for el in row:
                # get parent values in list
                # print("\nCurrent Cell:", row_index, col_index)
                el['coord'] = (row_index, col_index)
                if (row_index == 0 and col_index == 0):   # Case: top left cell, start cell
                    el['type'] = 'start'
                    # print("Cell in upper left")
                else:
                    if(row_index == 0 and col_index != 0):    # Case: top row disabled. Only move is accross.
                        # print(self.table[row_index][col_index-1]['total_score'] - 2)
                        el['total_score'] = self.table[row_index][col_index-1]['total_score'] - 2
                        el['type'] = 's2gap'
                        el['score'] = (-2)
                        el['parents'].append((row_index, col_index-1))
                        # print('row_index == 0')
                    elif(col_index == 0 and row_index != 0):   # Case: side column disabled. Only move is down.
                        el['total_score'] = self.table[row_index-1][col_index]['total_score'] - 2
                        # print(self.table[row_index][col_index-1]['total_score'] - 2)
                        el['type'] = 's1gap'
                        el['score'] = (-2)
                        el['parents'].append((row_index-1, col_index))
                        # print('col_index == 0')
                    else:
                        # print("cell inside")
                        # A - Diagonal
                        if (self.s1[row_index] == self.s2[col_index]):
                            # print(self.s1[row_index], " == ", self.s2[col_index])
                            # print('Cell ', (row_index-1,col_index-1) , self.table[row_index-1][col_index-1]['total_score'])
                            a_totalscore = self.table[row_index-1][col_index-1]['total_score'] + 1
                            el['score'] = 1
                        else:
                            # print(self.s1[row_index], " != ", self.s2[col_index])
                            # print('Cell ', (row_index-1,col_index-1) , self.table[row_index-1][col_index-1]['total_score'])
                            a_totalscore = self.table[row_index-1][col_index-1]['total_score'] - 1
                            # print(self.table[row_index-1][col_index-1]['total_score'], ' -1 = ', a_totalscore)
                            el['score'] = (-1)
                        # B/C - Gaps
                        # print(self.table[row_index-1][col_index]['total_score'], self.table[row_index][col_index-1]['total_score'])
                        b_totalscore = self.table[row_index-1][col_index]['total_score'] - 2  # B
                        c_totalscore = self.table[row_index][col_index-1]['total_score'] - 2  # C

                        values = [a_totalscore, b_totalscore, c_totalscore]    # represented in order, A -> B -> C

                        # print(b_totalscore, c_totalscore)
                        # print("Scores:", values)
                        
                        # Find max - we find the max score possible in this cell and add those parents to the element dictionary object
                        max_score = max(values)
                        val_index = [i for i, j in enumerate(values) if j == max_score]
                        # print("Value List: ",val_index)
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
                # print(el)
                el = None
            col_index = 0
            row_index += 1
        # self.print_table()

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
                "prior_coord" : copy.deepcopy(bottom_left)
            },
            True
        )

    def traverse_tree(self, node, state, first_iteration):
        print("\ninteration coord: ", node.coord)
        print('Parent coord', state["prior_coord"])
        if (first_iteration):
            print("psych")
            print_str = 'First_Iter: '
            for child in node.children:
                print_str += str(child.coord)
            print (print_str)
            for child in node.children:
                self.traverse_tree(child, copy.deepcopy(state), False)
        else:
            if (state["prior_coord"][0] - 1 == node.coord[0] and state["prior_coord"][1] - 1 == node.coord[1]):
                print("diagonal state")
                if (self.s1[node.coord[0] + 1] == self.s2[node.coord[1] + 1]):
                    state['score'].insert(0, "+")
                else:
                    state['score'].insert(0, "-")
                state['s1'].insert(0, self.s1[node.coord[0] + 1])
                state['s2'].insert(0, self.s2[node.coord[1] + 1])
            elif (state["prior_coord"][0] - 1 == node.coord[0] and state["prior_coord"][1] == node.coord[1]):
                print("s2gap state")
                # S2 Gap
                state['s1'].insert(0, self.s1[node.coord[1] + 1])
                state['s2'].insert(0, '-')
                state['score'].insert(0, "*")
            elif (state["prior_coord"][0] == node.coord[0] and state["prior_coord"][1] - 1 == node.coord[1]):
                # S1 Gap
                print("s1gap state")
                state['s2'].insert(0, self.s2[node.coord[1] + 1])
                state['s1'].insert(0, '-')
                state['score'].insert(0, "*")
        
        # Modify state        
        state['prior_coord'] = copy.deepcopy(node.coord)
        if (len(node.children) > 0):
            print_str = 'Print before rec:'
            for child in node.children:
                print_str += str(child.coord)
            print (print_str)

            # Recurse - for loop causing issues with rec? amount of children might be issue
            for child in node.children:
                self.traverse_tree(child, copy.deepcopy(state), False)
        else:
            print('coord is 0,0', len(node.children))
            node.children = []
            self.results.append(state)
            return

    def print_sequences(self):
        for seq in self.results:
            print(' '.join(seq['s1']))
            print(' '.join(seq['s2']))
            print(' '.join(seq['score']))
            print('\n')
    
    def print_table(self):
        # print(self.table)
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

seq1 = "ACT"
seq2 = "GTAA"
dna = SequenceAlign(seq1, seq2)
dna.align()
dna.print_table()
bottom_left = (len(dna.table)-1,len(dna.table[0])-1)
dna.tree = Node({"coord":(-1,-1)})
dna.create_tree(bottom_left, dna.tree)
dna.init_traverse_tree(dna.tree, bottom_left)
print(str(len(dna.results)))
dna.print_sequences()
dna.tree.print_tree()