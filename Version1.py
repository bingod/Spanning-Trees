from graph import *

class node:
	#optional parameter keeps track of ancestor
	def __init__(self, G = Graph(), ancestor = []):
		self.tree = []
		self.G = G
		for edge in ancestor:
			self.tree.append(edge)
	
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
				new_path = []
				for edge in path:
					new_path.append(edge)
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
def gen_trees(tree_node, orig_tree_node, FE = [], args = []):
	Trees = []
	Trees.append(tree_node.tree)
	
	if len(args) == 0:
		i = 0
		while i < len(FE):
			f = tree_node.G.edges[FE[i]]
			#find the cycle closed by f
			v, w = f.v1, f.v2
			cycle = tree_node.find_min_path(v, w)

			#create a new node corresponding to each edge exchange
			e = 0
			while e < len(cycle):
				new = node(tree_node.G, tree_node.tree)
				new.new_node(new.G.edges.index(f), cycle[e])
				#for each new node, run gen_trees(node, F, i)
				#this will insure that descendants don't exchange 
				#...for a repeated fundamental edge
				more_Trees = gen_trees(new, orig_tree_node, FE, [i])
				for t in more_Trees:
					Trees.append(t)
				e += 1
			i += 1
	else:
		i = args[len(args) - 1] + 1
		while i < len(FE):
			f = tree_node.G.edges[FE[i]]
			#find the cycle closed by f
			v, w = f.v1, f.v2
			cycle = tree_node.find_min_path(v, w)
			for e in cycle:
				if e not in orig_tree_node.tree:
					cycle.remove(e)
			
			#create a new node corresponding to each edge exchange
			e = 0
			while e < len(cycle):
				new = node(tree_node.G, tree_node.tree)
				new.new_node(new.G.edges.index(f), cycle[e])
				#for each new node, run gen_trees(node, F, args, i)
				#this will insure that descendants don't exchange 
				#...for a fundamental edge that's already been seen
				args.append(i)
				more_Trees = gen_trees(new, orig_tree_node, FE, args)
				for t in more_Trees:
					Trees.append(t)
				e += 1
			i += 1

	n = 0
	while n < len(Trees):
		if Trees.index(Trees[n]) != n:
			Trees.pop(n)
		else: n += 1
	
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

	Spanning_Trees = gen_trees(T_node, T_node, F, [])
		
	for tree in Spanning_Trees:
		print "Tree " + str(Spanning_Trees.index(tree) + 1) + ": ",
		for edge_num in tree:
			edge = G.edges[edge_num]
			print "[" + str(edge.v1.i) + "," + str(edge.v2.i) + "]",
		print "\n"











