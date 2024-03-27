# F0: not taken
# F1: taken
# Eval: Score max
# P: weight

import copy

# Read the file and return the values
def getValueInTxt(file_name):    
    with open(file_name, 'r') as file:
        lines = file.readlines()  # Read all lines from the file
        # Process the lines as needed
        
        init = lines[0].strip().split()
        n = int(init[0])
        Wmax = int(init[1])
        aliment_list = []
        
        
        for line in lines[1:]:
            # Example: Split the line by a delimiter and convert values to integers
            values = line.strip().split()
            aliment_list.append(Aliment(int(values[0]), int(values[1]), int(values[2])))
    
    return n, Wmax, aliment_list

# Class Aliment
class Aliment:
    def __init__(self, id, p, score):
        self.id = id
        self.weight = p
        self.score = score
   
# Class Decision     
class Decision:
    def __init__(self, f1: list, f0: list, L: list):
        self.f1 = f1
        self.f0 = f0
        self.L = L
        
    def __copy__(self):
        return Decision(self.f1.copy(), self.f0.copy(), self.L.copy())
    
    def __str__(self):
        return "F1:", self.f1, " \nF0:", self.f0, "\nL:", self.L
        
    def weightF1Total(self):
        weight = 0
        for i in range (0, len(self.f1)):
            id = self.f1[i]
            aliment = next(aliment for aliment in aliment_list if aliment.id == id)
            weight += aliment.weight
        return weight
    
    def scoreEval(self):
        score = 0
        # F1
        for i in range (0, len(self.f1)):
            id = self.f1[i]
            aliment = next(aliment for aliment in aliment_list if aliment.id == id)
            score += aliment.score
            
        # L
        for i in range (0, len(self.L)):
            id = self.L[i]
            aliment = next(aliment for aliment in aliment_list if aliment.id == id)
            score += aliment.score
        return score

# Branch and Bound
def Branch_Bound(decision: Decision, best):
    global countEval
    global countContraint
    global node
    global weightFinal
    node += 1
    if decision.weightF1Total() <= Wmax:
        score = decision.scoreEval()
        if len(decision.L) == 0:
            if score > best:
                best = score
        else:
            if score > best:
                x = decision.L[0]
                decision.L.pop(0)
                
                # Taken
                decision1 = copy.copy(decision)
                decision1.f1.append(x)
                # Not taken
                decision2 = copy.copy(decision)
                decision2.f0.append(x)
                
                best1 = Branch_Bound(decision1, best)
                best2 = Branch_Bound(decision2, best)
                # get the best best
                best = best1 if best1 > best2 else best2
            else:
                countEval += 1
    else: 
        countContraint += 1
        
    return best   

n, Wmax, aliment_list = getValueInTxt("Instances/inst4obj.txt")

countContraint = 0
countEval = 0
node = 0
weightFinal = 0

# globalWeight = 0
# Eval = 0
# for i in range (0, n):
#     Eval += aliment_list[i].score
    
decision = Decision([], [], [aliment.id for aliment in aliment_list])

aliment_list.sort(key=lambda x: x.score, reverse=True)
print("Fin:",Branch_Bound(decision, 180))
print("node:", node)
print("countContraint:", countContraint)
print("countEval:", countEval)

print("\n")
aliment_list.sort(key=lambda x: x.weight)
print("Fin:",Branch_Bound(decision, 180))
print("node:", node)
print("countContraint:", countContraint)
print("countEval:", countEval)