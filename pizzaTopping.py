# Uncomment import statements if libraries are installed and you want to see graph visualization of small examples
#import networkx as nx
#import matplotlib.pyplot as plt

# uncomment this class if you want Graph visualization
'''class GraphVisualization:
    def __init__(self):
        self.visual = []
        self.nodes = []
    
    def addNode(self, p):
        self.nodes.append(p)
    
    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)
    
    def visualize(self):
        G = nx.Graph()
        for n in self.nodes:
            G.add_node(n)
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()'''

class Customer:
    def __init__(self, likes = [], dislikes = [], name = ''):
        self.likes = likes
        self.dislikes = dislikes
        self.name = name

class Pizza:
    def __init__(self, toppings = [], cServe = 0):
        self.toppings = toppings
        self.cServe = cServe

def parseFile():
    file = open('c_coarse.in.txt', mode='r') # replace with file you want to read

    lines = file.readlines()
    people = []
    likesDict = {}
    disDict  = {}
    linNum = 0
    # Parse file and create list of customers with likes/dislikes
    for lin in lines:
        lin = lin.split(' ')
        first = 1
        if linNum % 2 == 1:
            likeList = []
            for i in lin:
                if not first:
                    likeList.append(i.strip())
                    if i.strip() in likesDict:
                        likesDict[i.strip()] +=1
                        
                    else:
                        likesDict[i.strip()] = 1
                else:
                    first = 0
        elif linNum != 0:
            disList = []

            for i in lin:
                
                if not first:
                    disList.append(i.strip())
                    if i.strip() in disDict:
                        disDict[i.strip()] +=1
                        
                    else:
                        disDict[i.strip()] = 1
                else:
                    first = 0

            p = Customer(likeList, disList, 'p' + str(int(linNum/2)-1))
            people.append(p)
            
        linNum+=1

    return people

    # netfavorite dict, currently not necessary but could potentially be useful for optimization?
    '''netFavor = {}
    for like in likesDict:
        if like in disDict:
            netFavor[like] = likesDict[like] - disDict[like]
        else:
            netFavor[like] = likesDict[like]
    
    highTop = ''
    highTopNum = 0
    for k in netFavor:
        if netFavor[k] > highTopNum:
            highTop = k
            highTopNum = netFavor[k]'''


def makeGraph(dictGraph):
    dictGraph = {}

    # Create a dictionary of all the customers as keys and all the incompatible customers
    # as values (this is our graph)
    for p in people:
        antiPeople = []

        for disP in people:

            for d in disP.dislikes:

                if d in p.likes:
                    antiPeople.append(disP.name)

            for l in disP.likes:

                if l in p.dislikes and p.name not in antiPeople and disP.name not in antiPeople:
                    antiPeople.append(disP.name)
        
        print(p.name)
        dictGraph[p.name] = antiPeople

    
    # Graph visualization, useful for small examples and debugging
    # visualizeGraph(dictGraph)
    maxEdges = 1 # placeholder value

    # remove nodes from graph until all nodes are isolated and have no edges with other nodes
    # i.e., all nodes are compatible with all other nodes
    while( maxEdges > 0):
        
        dictGraph, pL = removePickyCustomer(dictGraph)
        # more Graph visualization
        # visualizeGraph(dictGraph)

        # find max edges
        # only need to go through this loop if only nodes with single edges are left,
        # saves a little computation time
        if pL <= 1:
            maxEdges = -1
            for v in dictGraph.values():
                if len(v) > maxEdges:
                    maxEdges = len(v)
    

    piz = Pizza([],len(dictGraph))

    for p in people:
        if p.name in dictGraph:
            for l in p.likes:
                if l not in piz.toppings:
                    piz.toppings.append(l)
    
    print(str(len(piz.toppings)) + " " + str(piz.toppings))
    print(str(piz.cServe) + " Customers served")
    

def removePickyCustomer(people):

    # finds 'pickiest' customer and removes from graph
    pickEdges = 0
    pickiest = None
    for k in people:
        if len(people[k]) > pickEdges:
            pickEdges = len(people[k])
            pickiest = k

    people.pop(pickiest,None)
    

    # removes connections that other customer nodes have with pickiest customer
    for k in people:
        if pickiest in people[k]:
            people[k].remove(pickiest)
    print(pickiest)
    print(str(pickEdges)+'\n')
    # print(people)
    
    return people, pickEdges


# Uncomment for graph visualization
'''def visualizeGraph(dictGraph):
    G = GraphVisualization()
    for p in dictGraph:
        if not dictGraph[p]:
            G.addNode(p)
        for v in dictGraph[p]:
            G.addEdge(p,v)
        
    G.visualize()'''


if __name__ == '__main__':
    people = parseFile()
    makeGraph(people)