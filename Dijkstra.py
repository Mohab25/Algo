import sys
import heapq
# making the vertices
class Vertex:
    """
    a class for making the vertex data structure that will be used to compose the graph and added to the shortest path.
    """
    def __init__(self,node_id):
        self.id = node_id
        self.distance = sys.maxsize
        self.visited = False
        # adding the adjacent
        self.neighbors = {}
        #empty object holding previous vertices
        self.previous = {} 
        
    def add_neighbors(self,neighbor,cost=0):
        # adding neighbors to the node when it is traversed
        self.neighbors[neighbor] = cost
    
    def get_neighbors(self):
        return self.neighbors
    
    def get_cost(self,neighbor):
        # get the weigh previously set on add_neighbors.
        return self.neighbors[neighbor]

    def set_visited(self):
        self.visited=True
    
    def set_distance(self,distance):
        self.distance = distance
    
    def get_distance(self):
        return self.distance

    def add_previous(self,previous):
        self.previous.append(previous)
    
    def get_previous(self):
        return self.previous

    def get_id(self):
        return self.id

    # def __getitem__(self, item):
    #     return self.neighbors[item]

    def __lt__(self,other_vertex):
        # this is used by python class for making comparsions -> required by the heapq
        return self.distance < other_vertex.distance

class Graph:
    def __init__(self):
        self.vertices_dict = {}
        self.num_vertices = 0

    def __iter__(self): # this will cause this class to be iterable
        return iter(self.vertices_dict.values())

    def get_dict_values(self):
        return self.vertices_dict.value()
    
    def add_vertex(self,node):
        new_vertex = Vertex(node)
        self.vertices_dict[node] = new_vertex
        self.num_vertices+=1
        return new_vertex
    
    def get_vertex(self,node):
        if node in self.vertices_dict:
            return self.vertices_dict[node]
        else:
            return None

        
    def construct_edge(self,From,to,cost=0):
        """
            take from and to (Vertices) to make the edge, check if these Vertices already exists on the vertices_dict 
            if not add them, and then call Vertex add_neighbors() method. 
        """
        if From not in self.vertices_dict:
            self.add_vertex(From)
        elif to not in self.vertices_dict:
            self.add_vertex(to)
        self.vertices_dict[From].add_neighbors(self.vertices_dict[to],cost)
        self.vertices_dict[to].add_neighbors(self.vertices_dict[From],cost)


    def construct_shortest_path(self,v,path):
        """
            recursively construct the shortest path from the vertex previous.
        """
        if v.previous:
            path.append(v.previous.get_id())
            # recursion
            construct_shortest_path(v.previous,path)
    

def dijkstra(graph,start,end):
    """
        1. adjust the distance of the start and add it to a list of unvisited_vertices "also known as openSet"
        2. get vertices and their indexes from the graph.
        3. loop until the len of unvisited_vertices equals 0.
        4. pop the first item of the unvisited_vertices and adjust it's visited value, name the item current.
        5. loop the neighbors of current, and check if it is already visited
             5.1 if not make a new distance equals to current vertex distance+ the cost from current ot next
             if this distance is less the distance of the neighbor, assign it to the neighbor instead and
             assign previous in the neighbors properties to current so you can keep track of previous vertices.
             if it is not less the distance of the nighbor don't do anything.
             
        6. the shortest path is stored in the previous of the nodes, another function has to handle extracting the 
            path (construct_shortest_path).
        note that the dijkstra function steps is slightly more complicated as heaps are used to organize data.  

    """
    start.set_distance(0)
    unvisited_nodes = [[vertex.get_distance(),vertex] for vertex in graph]
    #unvisited_nodes.append(start) # the start is assumed to be outer to the graph (not added to it already)
    # heapify the list so the the least distance is at the begining
    print('Before being heapified:',unvisited_nodes)
    heapq.heapify(unvisited_nodes)
    print(unvisited_nodes)
    while(len(unvisited_nodes)):
        heap_tuple = heapq.heappop(unvisited_nodes) # using heappop instead of pop.
        print("Heap tuple:",heap_tuple)
        print("Heap vertex:",heap_tuple[1])
        print("the problem is in the line above  ... ")
        current = heap_tuple[1]
        print('Current:',current)
        current.set_visited()
        if current==end:
            break
        for next in current.neighbors:
            if next.visited:
                continue
            tentative_distance = current.get_distance()+current.get_cost(next)
            if tentative_distance < next.get_distance():
                next.set_distance = tentative_distance
                next.previous = current
            else:
                continue
        
        # heap rebuild (i don't believe this is a good practice, there should be another way to refresh the heapq)
        # empty  the heap 
        while(len(unvisited_nodes)):
            heapq.heappop(unvisited_nodes)
        # again add vertices unvisited to it
        unvisited_nodes.append([v.get_distance(),v] for v in graph)
        heapq.heapify(unvisited_nodes)
        print('Reached the end')


if __name__ == '__main__':

    g = Graph()

    g.add_vertex('a')
    g.add_vertex('b')
    g.add_vertex('c')
    g.add_vertex('d')
    g.add_vertex('e')
    g.add_vertex('f')

    g.construct_edge('a', 'b', 7)  
    g.construct_edge('a', 'c', 9)
    g.construct_edge('a', 'f', 14)
    g.construct_edge('b', 'c', 10)
    g.construct_edge('b', 'd', 15)
    g.construct_edge('c', 'd', 11)
    g.construct_edge('c', 'f', 2)
    g.construct_edge('d', 'e', 6)
    g.construct_edge('e', 'f', 9)

    print ('Graph data:',g)
    for v in g.vertices_dict.values():
        for w in v.get_neighbors():
            vid = v.get_id()
            wid = w.get_id()
            txt = '{}, {}, {}'.format(vid,wid,v.get_cost(w))
            print(txt)

    dijkstra(g, g.get_vertex('a'), g.get_vertex('e')) 

    target = g.get_vertex('e')
    path = [target.get_id()]
    shortest(target, path)
    tx = 'The shortest path:{}'.format(path[::-1])
    print(tx)