import os

# Exercice 1
class Aliment:
    def __init__(self, id, p, score):
        self.id = id
        self.weight = p
        self.score = score
        
def algo_glouton(n, Wmax, aliment_list):
    x = [0 for i in range (0, n)]
    p_total = 0
    score_total = 0
    for i in range (0, n):
        if aliment_list[i].weight + p_total <= Wmax:
            x[i] = [1, aliment_list[i].id]
            p_total += aliment_list[i].weight 
            score_total += aliment_list[i].score
        else:
            x[i] = [0, aliment_list[i].id]
    return x, p_total, score_total
            
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

def resultOrder(file_name):
    n, Wmax, aliment_list = getValueInTxt(file_name)
    print(file_name)
    print("Wmax: ", Wmax)
    # Poid croisant
    aliment_list.sort(key=lambda x: x.weight)
    printGloutonRes(n, Wmax, aliment_list)
    
    # Poid decroisant
    aliment_list.sort(key=lambda x: x.weight, reverse=True)
    printGloutonRes(n, Wmax, aliment_list)
    
    # Score croisant
    aliment_list.sort(key=lambda x: x.score)
    printGloutonRes(n, Wmax, aliment_list)
    
    # Score decroisant
    aliment_list.sort(key=lambda x: x.score, reverse=True)
    printGloutonRes(n, Wmax, aliment_list)
    print("\n")
    
def printGloutonRes(n, Wmax, aliment_list):
    x, p_total, score_total = algo_glouton(n, Wmax, aliment_list)
    print("x:",x, "p_total",p_total, "score_total",score_total)
    
def get_file_names(directory):
    file_names = []
    for file_name in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file_name)):
            file_names.append(file_name)
    return file_names
    
n = 0
Wmax = 0
x = []
p = []
score = [] 

directory = "Instances"
file_names = get_file_names(directory)


# resultOrder("Instances/inst4obj.txt")

# Exercice 3

def generer_variantes(ensemble):
    if not ensemble:
        return [()]
    else:
        variante = set()
        for i, e in enumerate(ensemble):
            for variante_valeur in generer_variantes(ensemble[:i] + ensemble[i+1:]):
                variante.add((e.id,) + variante_valeur)
        return variante

# Exemple d'utilisation :
ensemble = [Aliment(1, 1, 1), Aliment(2, 2, 2), Aliment(3, 3, 3)]
variantes = generer_variantes(ensemble)
print("variantes", variantes)
for variante in variantes:
    print(variante)
        
