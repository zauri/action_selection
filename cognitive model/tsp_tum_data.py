V = 4
answer = [] 

# Function to find the minimum weight 
# Hamiltonian Cycle 

# n = number of nodes
# visited = list of Boolean values for each node (visited/not visited)
# answer = list of costs for different paths

def tsp(graph, visited, currPos, n, count, cost): 
	# check if end is reached, if yes return current cost
	if (count == n and graph[currPos][0]): 
		answer.append(cost + graph[currPos][0]) 
		return

	# loop trough nodes
	for i in range(n): 
		if (visited[i] == False and graph[currPos][i]): 
			
			# mark as visited 
			visited[i] = True
			tsp(graph, visited, i, n, count + 1, 
				cost + graph[currPos][i]) 
			
			# mark ith node as unvisited 
			visited[i] = False

# Driver code 


if __name__ == '__main__': 
	n = 4
	graph= [[ 0, 4, 4, 5 ], 
			[ 4, 0, 3, 4 ], 
			[ 4, 3, 0, 2 ], 
			[ 5, 4, 2, 0 ]] 

	# boolean array to check if a node has been visited or not 
	visited = [False for i in range(n)] 
	
	# mark 0th node as visited 
	visited[0] = True

	# find the minimum weight Hamiltonian Cycle 
	tsp(graph, visited, 0, n, 1, 0) 

	# ans is the minimum weight Hamiltonian Cycle 
	print(min(answer)) 
