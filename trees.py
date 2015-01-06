class node:
	#optional parameter keeps track of ancestor
	def _init_(self, ancestor = []):
		self.tree = ancestor
	
	#make tree node unique by exchanging an edge for a fundamental edge
	def new_node(self, new_edge, stale_edge):
		self.tree.append(new_edge)
		self.tree.remove(stale_edge)
	
	#adjacent vertices to a vertex v in a node's tree
	def adj_verts(self, v):
		neighbors = []
		for edge in self.tree:
			if edge.has(v):
				neighbors.append(edge.v1, edge.v2)
				neighbors.remove(v)
		return neighbors
		
    #find all paths between two vertices in a node's tree
    #return a list of paths (which are in turn lists of vertices in the path)
	def find_all_paths(self, start_vertex, end_vertex, path=[]):
    	#keep track of all vertices in the tree
		verts = []
    	for edge in self.tree:
			if(edge.v1 not in verts):
				verts.append(edge.v1)
			if(edge.v2 not in verts):
				verts.append(edge.v2)
        #add the starting point to a path
		path = path + [start_vertex]
        #return if you've gotten to the end point
		if start_vertex == end_vertex:
			return [path]
        #error if start and end aren't in tree
		if start_vertex not in verts or end_vertex not in verts:
			print "You can't make a path here!"
			return []
        #list of all paths
		paths = []
        #move starting point to all adjacent vertices and call function again
		for vertex in self.adj_verts(start_vertex):
			if vertex not in path:
				extended_paths = self.find_all_paths(vertex, end_vertex, path)
				for p in extended_paths: 
					paths.append(p)
		return paths
    
    #find path of smallest length
    def find_min_path(self, start_vertex, end_vertex):
    	paths = self.find_all_paths(start_vertex, end_vertex, path=[])
    	min_path = paths[0]
    	i = 0
    	j = 1
    	while j < paths.len():
    		if paths[j].len() < paths[i].len():
    			min_path = paths[j]
    			i = j
    		j += 1
    	return min_path  				   			

#generate trees from a node
#optional parameter keeps track of which fundamental edges to not consider
#note to self: only change trees by fundamental edges > final parameter
#note to self: will need to keep track of how many fundamental edges changed
def gen_trees(tree_node, F, args = []):
	Trees = []
	Trees.append(tree_node.tree)
	
	if args.len() == 0:
		i = 0
		while i < F.len():
			f = F[i]
			#find the cycle closed by f
			v, w = f.v1, f.v2
			cycle_verts = tree_node.find_min_path(v, w)
			#list of cycle edges - ordered
			cycle = []
			k = 0
			while k < cycle_verts.len() - 1:
				cycle.append(Edge(cycle_verts[k],cycle_verts[k+1]))
				k += 1
			#create a new node corresponding to each edge exchange
			e = 0
			while e < cycle.len():
				new = node(tree_node.tree)
				new.new_node(f, cycle[e])
				#for each new node, run gen_trees(node, F, i)
				#this will insure that descendants don't exchange 
				#...for a repeated fundamental edge
				gen_trees(new, F, i)
				e += 1
			i += 1
	else:
		i = args[args.len() - 1] + 1
		while i < F.len():
			f = F[i]
			#find the cycle closed by f
			v, w = f.v1, f.v2
			cycle_verts = tree_node.find_min_path(v, w)
			#make a list of the cycle edges
			cycle = []
			k = 0
			while k < cycle_verts.len() - 1:
				cycle.append(Edge(cycle_verts[k],cycle_verts[k+1]))
				k += 1
			#create a new node corresponding to each edge exchange
			e = 0
			while e < cycle.len():
				new = node(tree_node.tree)
				new.new_node(f, cycle[e])
				#for each new node, run gen_trees(node, F, args, i)
				#this will insure that descendants don't exchange 
				#...for a fundamental edge that's already been seen
				#??will it pass the same args again?
				gen_trees(new, F, args, i)
			i += 1

def Main(G):
	#find the first tree
	T = G.find_tree()
	#initialize list of fundamental edges
	F = []
	i = 0
	#fill list of fundamental edges
	while i < G.edges.len():
		j = 0
		while j < T.len():
			if G.edges[i] == T[j]:
				break
			else j+= 1
		if j == T.len() - 1:
			F.append(G.edges[i])
		i += 1					
	
	#create node from T
	T_node = node()
	for edge in T:
		T_node.tree.append(edge)
		
	return gen_trees(T_node, F)
		
	
