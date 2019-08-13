class SequenceAlign:
    s1 : list = []
    s2 : list = []
    table : list = []
    blank_cell : dict = {
        "total_score" : 0,
        "score" : 0,
        "parents" : [],
        "type" : None  # start, s1Gap, s2Gap, match, mismatch
    }

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
                el["total_score"] = 0
                el["score"] = 0
                el["parents"] = []
                el["type"] = None
            self.table.append(row)
        print(self.table)
        self.print_table()
    
    def align(self):
        row_index = 0
        col_index = 0
        for row in self.table:
            for el in row:
                # get parent values in list
                print("\nCurrent Cell:", row_index, col_index)
                if (row_index == 0 and col_index == 0):   # Case: top left cell, start cell
                    el['type'] = 'start'
                    print("Cell in upper left")
                else:
                    if(row_index == 0 and col_index != 0):    # Case: top row disabled. Only move is accross.
                        print(self.table[row_index][col_index-1]['total_score'] - 2)
                        el['total_score'] = self.table[row_index][col_index-1]['total_score'] - 2
                        el['type'] = 's2gap'
                        el['score'] = (-2)
                        el['parents'].append((row_index, col_index-1))
                        print('row_index == 0')
                    elif(col_index == 0 and row_index != 0):   # Case: side column disabled. Only move is down.
                        el['total_score'] = self.table[row_index-1][col_index]['total_score'] - 2
                        print(self.table[row_index][col_index-1]['total_score'] - 2)
                        el['type'] = 's1gap'
                        el['score'] = (-2)
                        el['parents'].append((row_index-1, col_index))
                        print('col_index == 0')
                    else:
                        print("cell inside")
                        # A - Diagonal
                        if (self.s1[row_index] == self.s2[row_index]):
                            print(self.s1[row_index], " == ", self.s2[row_index])
                            print('Cell ', (row_index-1,col_index-1) , self.table[row_index-1][col_index-1]['total_score'])
                            a_totalscore = self.table[row_index-1][col_index-1]['total_score'] + 1
                            el['score'] = 1
                        else:
                            print(self.s1[row_index], " != ", self.s2[row_index])
                            print('Cell ', (row_index-1,col_index-1) , self.table[row_index-1][col_index-1]['total_score'])
                            a_totalscore = self.table[row_index-1][col_index-1]['total_score'] - 1
                            print(self.table[row_index-1][col_index-1]['total_score'], ' -1 = ', a_totalscore)
                            el['score'] = (-1)
                        # B/C - Gaps
                        print(self.table[row_index-1][col_index]['total_score'], self.table[row_index][col_index-1]['total_score'])
                        b_totalscore = self.table[row_index-1][col_index]['total_score'] - 2  # B
                        c_totalscore = self.table[row_index][col_index-1]['total_score'] - 2  # C

                        values = [a_totalscore, b_totalscore, c_totalscore]    # represented in order, A -> B -> C

                        print(b_totalscore, c_totalscore)
                        print("Scores:", values)
                        
                        # Find max - we find the max score possible in this cell and add those parents to the element dictionary object
                        max_score = max(values)
                        val_index = [i for i, j in enumerate(values) if j == max_score]
                        print("Value List: ",val_index)
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
                print(el)
                el = None
            col_index = 0
            row_index += 1
        self.print_table()

    def print_table(self):
        # print(self.table)
        first_line = self.s2.copy()
        first_line.insert(0, ' ')
        # first_line.insert(1, '-')
        print(' '.join(first_line))
        i = 0
        for row in self.table:
            line = ''
            line += self.s1[i]
            for el in row:
                line += str(el['total_score'])
            print(' '.join(line))
            i += 1


seq1 = "AGCTAG"
seq2 = "TAGCTAG"
dna = SequenceAlign(seq1, seq2)
dna.align()
