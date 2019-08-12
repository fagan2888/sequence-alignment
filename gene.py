class SequenceAlign:
    s1 : list = []
    s2 : list = []
    table : list = []
    blank_cell : dict = {
        "total_score" : 0,
        "score" : 0,
        "parents" : []
    }

    def __init__(self, s1, s2):
        # Takes input as 2 strings, convert them into instance variables x and y
        for el in s1:
            self.s1.append(el)
        for el in s2:
            self.s2.append(el)

        # Init table
        for i in range(0, len(self.s1) + 1):
            row = [self.blank_cell] * (len(self.s2) + 1)
            self.table.append(row)
        
        self.print_table()
        # print(self.table)

    
    def print_table(self):
        first_line = self.s2.copy()
        first_line.insert(0, ' ')
        first_line.insert(1, '-')
        print(' '.join(first_line))
        i = 0
        for row in self.table:
            line = ''
            if i == 0:
                line += '-'
            else:
                line += self.s1[i-1]
            for el in row:
                line += str(el['total_score'])
            print(' '.join(line))
            i += 1

seq1 = "AGCTA"
seq2 = "CCGTA"
dna = SequenceAlign(seq1, seq2)