from graph import *

class node:
	#optional parameter keeps track of ancestor
	def __init__(self, G = Graph(), ancestor = []):
		self.tree = ancestor[:]
		self.G = G
	
	#make tree node unique by exchanging an edge for a fundamental edge
	def new_node(self, new_edge, stale_edge):
		self.tree.append(new_edge)
		#NOTE: this only works for simple graphs
		#do we need to check that this edge is actually in the tree?
		self.tree.remove(stale_edge)
	
	#adjacent vertices to a vertex v in a node's tree
	def adj_verts(self, v):
		neighbors = []
		for edge_num in self.tree:
			edge = self.G.edges[edge_num]
			if edge.v1.i == v.i:
				neighbors.append(edge.v2)
			elif edge.v2.i == v.i:
				neighbors.append(edge.v1)
		return neighbors
		
    #find all paths between two vertices in a node's tree
    #return a list of paths (which are in turn lists of vertices in the path)
	def find_all_paths(self, start_vertex, end_vertex, path=[]):

		#list of all paths
		paths = []
    	#keep track of all vertices in the tree
		verts = []
		for edge_num in self.tree:
			edge = self.G.edges[edge_num]
			if(edge.v1 not in verts):
				verts.append(edge.v1)
			if(edge.v2 not in verts):
				verts.append(edge.v2)

		#error if start and end aren't in tree
		if start_vertex not in verts or end_vertex not in verts:
			print "You can't make a path here!"
			return []
        
        #return if you've gotten to the end point
		if start_vertex == end_vertex:
			paths.append(path)
			return paths
        #move starting point to all adjacent vertices and call function again
		for vertex in self.adj_verts(start_vertex):
			k = 0
			for edge_num in path:
				edge = self.G.edges[edge_num]
				if edge.has(vertex):
					k += 1
					break
			if k == 0:
				new_path = path[:]
				for edge_num in self.tree:
					if self.G.edges[edge_num].has(start_vertex) and self.G.edges[edge_num].has(vertex):
						new_path.append(edge_num)
						break
				extended_paths = self.find_all_paths(vertex, end_vertex, new_path)
				for p in extended_paths:
					paths.append(p)
		return paths

    #find path of smallest length
	def find_min_path(self, start_vertex, end_vertex):
		paths = self.find_all_paths(start_vertex, end_vertex, path=[])
		min_path = paths[0]
		i = 0
		j = 1
		while j < len(paths):
			if len(paths[j]) < len(paths[i]):
				min_path = paths[j]
				i = j
			j += 1
		return min_path  

#generate trees from a node
#optional parameter keeps track of which fundamental edges to not consider
#note to self: only change trees by fundamental edges > final parameter
#note to self: will need to keep track of how many fundamental edges changed
def gen_trees(tree_node, FE, INx, OUTx):
	Trees = []
	Trees.append(tree_node.tree)
	
	while len(FE) > 0:

		if FE[0] not in OUTx:

			f = tree_node.G.edges[FE[0]]
			v, w = f.v1, f.v2
			b_cycle = tree_node.find_min_path(v, w)
			cycle = []
			for edge in b_cycle:
				if edge not in INx:
					cycle.append(edge)
			
			if len(cycle) > 0:
				e_i = 0
				while e_i < len(cycle):
					new = node(tree_node.G, tree_node.tree)
					new.new_node(FE[0], cycle[e_i])
					
					new_IN = INx[:] + [FE[0]] + cycle[0:e_i]

					new_OUT = OUTx[:] + [cycle[e_i]]

					FE_copy = FE[:]

					more_Trees = gen_trees(new, FE_copy, new_IN, new_OUT)
					for t in more_Trees:
						Trees.append(t)
					e_i += 1

		FE.pop(0)

	#n = 0
	#while n < len(Trees):
	#	if Trees.index(Trees[n]) != n:
	#		Trees.pop(n)
	#	else: n += 1

	return Trees

def Main(G):
	#find the first tree
	T = G.find_tree()
	#initialize list of fundamental edges
	F = []

	#fill list of fundamental edges
	edge_num = 0
	while edge_num < len(G.edges):
		if edge_num not in T:
			F.append(edge_num)
		edge_num += 1

	#print "\n Here are the fundamental edges:"
	#for edge_num in F:
		#edge = G.edges[edge_num]
		#print "[" + str(edge.v1.i) + "," + str(edge.v2.i) + "]",
	#print "\n"

	#create node from T
	T_node = node(G, T)

	print "\n Here are all trees:"

	Spanning_Trees = gen_trees(T_node, F, [], [])

	n = 0
	r = 0
	while n < len(Spanning_Trees):
		if Spanning_Trees.index(Spanning_Trees[n]) != n:
			Spanning_Trees.pop(n)
			r += 1
		else: n += 1
		
	for tree in Spanning_Trees:
		print "Tree " + str(Spanning_Trees.index(tree) + 1) + ": ",
		for edge_num in tree:
			edge = G.edges[edge_num]
			print "[" + str(edge.v1.i) + "," + str(edge.v2.i) + "]",
		print "\n"

	print "#repeats: " + str(r)






