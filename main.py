import json
import random
import math

with open('data.json') as json_file:
    data = json.load(json_file)



examples=[]
terminals=['x', 'y', 'z','w', 'int']
functions=['+','-','*','/']

# FUNCTIONS =========================================================================================
def full_individual(k):
    if k ==0:
        return Node(random.choice(terminals),[])
    else:
        return Node(random.choice(functions),[full_individual(k-1),full_individual(k-1)])

def generate_examples(n_examples):

    for i in range(0,n_examples):
        input= [random.randint(0,1000),random.randint(0,1000),random.randint(0,1000),random.randint(0,1000)]
        examples.append([input, param_function(input[0],input[1],input[2],input[3])])

def param_function(x,y,z,w):
    return eval(data["function"])

def generate_population(generation):
    pop=[]
    for i in range(0, data['pop_size']):
        pop.append(Individual(full_individual(data["max_depth"]),generation))
    return pop;

def print_tree(tree):
    if len(tree._list)==0:
        return str(tree._char)
    else:
        return "("+print_tree(tree._list[0])+")"+ tree._char + "("+print_tree(tree._list[1])+")"

def calculate_error_function_param(input, func, output ):
    x=input[0]
    y=input[1]
    z=input[2]
    w=input[3]
    try:
        result= eval(func)
    except ZeroDivisionError:
        result= 10000000000000000
    return abs(result-output)

def tournament(pop):
    parents=[]

    for i in range(0, len(pop)):
        tourn_pop=[]
        k=random.randint(2,data["pop_size"]//2)
        for i in range(0,k):
            random_number =random.randint(0, len(pop)-1)
            tourn_pop.append(pop[random_number])
        winner=best(tourn_pop)
        parents.append(winner)

    return parents

def best(pop):
    best=pop[0]
    for i in pop:
        if i._fitness< best._fitness:
            best=i

    return best

def create_new_population(pop,gen):
    random_number=random.random()
    new_pop=pop
    if random_number<= data["cross_rate"]:
        # parents=tournament(pop)
        # new_pop=crossover(parents)
        print("crossover")
    elif random_number<= data["cross_rate"]+data["mut1_rate"]:
        # new_pop=mutation(new_pop)
        print("mutation")
    elif random_number<= data["cross_rate"]+data["mut1_rate"]+data["mut2_rate"]:
        print("mutation2")
    else:
        print("reproduction")
    population=[]
    for i in new_pop:
        population.append(Individual(i._tree,gen))

    return population


# OBJECT=========================================================================================
class Node(object):
    _char=''
    _list=[]

    def __init__(self, char, list):
        if(char=='int'):
            self._char=random.randint(-500,500)
        else:
            self._char=char
        self._list=list
        # print("node init")

    def __repr__(self):
        # return "\n Generation: %s, vector: %s, string: %s, fitness: %s, price: %s, weight: %s" %(self._generation, self._vector, self._string, self._fitness, self._price, self._weight)
        return "( %s %s )"%(self._char, self._list)


class Individual(object):
    _tree=[]
    _fitness=0
    _h=0
    def __init__(self, root, generation):
        self._tree=root
        self._generation=generation
        self._fitness=self.evaluate()
        self._h=self.calculate_h()

    def evaluate(self):
        error=0
        for i in examples:
            error+=calculate_error_function_param(i[0], print_tree(self._tree), i[1] )
        return error

    def calculate_h(self):
        return 1

    def __repr__(self):
        # return "\n Generation: %s, vector: %s, string: %s, fitness: %s, price: %s, weight: %s" %(self._generation, self._vector, self._string, self._fitness, self._price, self._weight)
        return " %s #### %s #### %s "%(self._generation, print_tree(self._tree), self._fitness)



# MAIN =========================================================================================


def main():
    generate_examples(data["n_examples"])
    # print(examples)
    # node=Node('+',[2,3])
    # node2=Node('-',[node,5])
    population = generate_population(0)
    # print(best(population))
    # print(print_tree(population[0]._tree))

    bes= best(population)
    best_of_all=bes

    j=0
    while (j < data["stop_generation"]):

        print(j)
        bes=best(population)
        if best_of_all._fitness<bes._fitness:
            best_of_all=bes
            print("best_of_all has changed: %s %s"%(best_of_all._generation, best_of_all))
            print('')
        population=create_new_population(population,j)
        j+=1

    print("####################################################################")
    print("best of last generation: %s"%(bes))
    print('')
    print("best_of_all: %s"%(best_of_all))

main()
