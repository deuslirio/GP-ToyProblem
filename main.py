import json
import random
import math
import copy

with open('data.json') as json_file:
    data = json.load(json_file)



examples=[]
terminals=['x','y','z','w','int']
functions=['+','-','*','/']

# FUNCTIONS =========================================================================================
def grow_or_full(k):
    if random.random() <0.1:
        return full_individual(k)
    else:
        return grow_individual(k)

def full_individual(k):
    if k ==0:
        return Node(random.choice(terminals),[])
    else:
        return Node(random.choice(functions),[full_individual(k-1),full_individual(k-1)])

def grow_individual(k):
    a=random.random()
    if k ==0:
        return Node(random.choice(terminals),[])
    elif a>0.5:
        return Node(random.choice(functions),[grow_individual(k-1),grow_individual(k-1)])
    elif a<=0.5:
        return Node(random.choice(terminals),[])


def generate_examples(n_examples):

    for i in range(0,n_examples):
        input= [random.randint(-300,300),random.randint(-300,300),random.randint(-300,300),random.randint(-300,300)]
        examples.append([input, param_function(input[0],input[1],input[2],input[3])])

def param_function(x,y,z,w):
    return eval(data["function"])

def generate_population(generation):
    pop=[]
    for i in range(0, data['pop_size']):
        pop.append(Individual(grow_or_full(random.randint(0,data["max_depth"]-1)),generation))
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
    result=0
    try:
        result= eval(func)
    except ZeroDivisionError:
        result=0
    return abs(result-output)

def tournament(pop, n):
    winners=[]

    for i in range(0, n):
        tourn_pop=[]
        k=random.randint(2,data["pop_size"]//2)
        for i in range(0,k):
            random_number =random.randint(0, len(pop)-1)
            tourn_pop.append(pop[random_number])
        winner=best(tourn_pop)
        winners.append(winner)

    return winners

def best(pop):
    best=pop[0]
    for i in pop:
        if i._fitness< best._fitness:
            best=i

    return best

def calculate_depth(tree):
        if len(tree._list) == 0:
            return 1
        return max(calculate_depth(tree._list[0]), calculate_depth(tree._list[1])) + 1

def crossover_sub_tree(parents):
    parent=copy.deepcopy(parents);

    path_p1=[]
    path_p2=[]
    max_depth_p1= random.randint(1,parent[0]._depth)
    max_depth_p2=random.randint(1, parent[1]._depth)

    if max_depth_p2<=0:
        max_depth_p2=1

    for i in range(0,max_depth_p1):
        path_p1.append(random.randint(0,1))


    for i in range(0,max_depth_p2):
        path_p2.append(random.randint(0,1))

    sub_tree_p2= get_sub_tree(parent[1]._tree, path_p2)
    new_tree= join_sub_trees(parent[0]._tree, sub_tree_p2, path_p1)

    return new_tree



def get_sub_tree(tree, path_p2):
    sub_tree=tree

    for i in range(0, len(path_p2)-1):
        if len(sub_tree._list)>0:
            sub_tree=sub_tree._list[path_p2[i]]

    # print("subtree_function",sub_tree)
    return sub_tree

def join_sub_trees(subtree1, subtree2, path_p1):
    # print(print_tree(subtree1), print_tree(subtree2))
    subtree2=copy.deepcopy(subtree2)
    if len(path_p1)==0 or len(subtree1._list)==0:
        subtree1 = subtree2
    else:
        # print(subtree1._list[path_p1[0]], subtree2, path_p1[0:])
         subtree1._list[path_p1[0]] = join_sub_trees(subtree1._list[path_p1[0]], subtree2, path_p1[0:])
    return subtree1

def change_note_char(tree, path_p1):
    tree=copy.deepcopy(tree)
    if len(tree._list)==0:
        tree._char=random.choice(terminals)
        if(tree._char=='int'):
            tree._char=random.randint(0,10)
    elif len(path_p1)==0:
        tree._char=random.choice(functions)
    else:
        tree._list[path_p1[0]] = change_note_char(tree._list[path_p1[0]], path_p1[0:])
    return tree


def mutation_sub_tree(mutant):
    mutant=copy.deepcopy(mutant);
    path_p1=[]
    max_depth_p1= random.randint(0,mutant._depth)
    sub_tree=None

    for i in range(0,max_depth_p1):
        path_p1.append(random.randint(0,1))

    if(data["max_depth"]-(max_depth_p1)>0):
        random_number=random.randint(0,data["max_depth"]-(max_depth_p1))
        sub_tree=grow_or_full(random_number)
    else:
        sub_tree=grow_or_full(0)

    new_tree=join_sub_trees(mutant._tree,sub_tree,path_p1)
    return new_tree

def mutation_point(mutant):
    mutant=copy.deepcopy(mutant);
    path_p1=[]
    max_depth_p1= random.randint(0,mutant._depth)

    for i in range(0,max_depth_p1):
        path_p1.append(random.randint(0,1))

    new_tree = change_note_char(mutant._tree, path_p1)

    return new_tree

def create_new_population(pop,gen):

    new_pop=[]
    while len(new_pop)< data["pop_size"]:
        random_number=random.random()
        if random_number<= data["cross_rate"]:
            parents=tournament(pop,2)
            new_pop.append(crossover_sub_tree(parents))
            # print("cross ",random_number)

        elif random_number<= data["cross_rate"]+data["mut1_rate"]:
            mutant=tournament(pop,1)
            new_pop.append(mutation_sub_tree(mutant[0]))
            # print("mutation1 ",random_number)


        elif random_number<= data["cross_rate"]+data["mut1_rate"]+data["mut2_rate"]:
            # print("mutation2 ",random_number)
            mutant=tournament(pop,1)
            new_pop.append(mutation_point(mutant[0]))
        else:
            reproduction=tournament(pop,1)
            new_pop.append(reproduction[0]._tree)
            # print("reproduction ",random_number)


    population=[]


    for i in range(0, len(new_pop)):
        if (calculate_depth(new_pop[i])>data["max_depth"]):
            new_pop[i]=grow_or_full(random.randint(0,data["max_depth"]))

        population.append(Individual(new_pop[i],gen))

    return population


# OBJECTS=========================================================================================
class Node(object):
    _char=''
    _list=[]

    def __init__(self, char, list):
        if(char=='int'):
            self._char=random.randint(0,10)
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
    _depth=0
    def __init__(self, root, generation):
        self._tree=root
        self._generation=generation
        self._fitness= self.evaluate()
        self._depth= calculate_depth(self._tree)

    def evaluate(self):
        error=0
        for i in examples:
            error += calculate_error_function_param(i[0], print_tree(self._tree), i[1] )
        return error/len(examples)



    def __repr__(self):
        # return "\n Generation: %s, vector: %s, string: %s, fitness: %s, price: %s, weight: %s" %(self._generation, self._vector, self._string, self._fitness, self._price, self._weight)
        return " Generation:%s Function:%s Fitness:%s Altura:%s"%(self._generation, print_tree(self._tree), self._fitness, self._depth)



# MAIN =========================================================================================


def main():
    generate_examples(data["n_examples"])
    population = generate_population(0)
    # print(best(population))
    # print(population[0])
    # print(population[1])
    # crossover_sub_tree(population)


    bes = population[0]
    best_of_all = bes

    j = 0
    while (j < data["stop_generation"] ):
        population=create_new_population(population,j)
        print(j)
        bes = best(population)
        if best_of_all._fitness > bes._fitness:
            best_of_all = bes
            print("best_of_all has changed: %s %s"%(best_of_all._generation, best_of_all))
            print('')
        j+=1

    print("####################################################################")
    print("best of last generation: %s"%(bes))
    print('')
    print("best_of_all: %s"%(best_of_all))

main()
