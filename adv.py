from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


reverse_directions = {'n':'s', 's':'n','e':'w','w':'e'}

reverse_path = []

visited = {}


#Let's start with current room and get the exits from that room 
visited[player.current_room.id] = player.current_room.get_exits()

# Let us traverse the room while the number of rooms we have visited < total num of rooms
while len(visited) < len(room_graph) -1:
	#if the current room is not in the dictionary set of visited rooms
	if player.current_room.id not in visited:
		 # Let's add the room to the visited dictionary, and keep track of what exits are there, value is lists
		visited[player.current_room.id] = player.current_room.get_exits()

        # Remove the exit one at a time so we do not traverse the way we came immediately
		visited[player.current_room.id].remove(reverse_path[-1]) 
	
	
    # While the room has no more exits  and we hit a deadend 
	while len(visited[player.current_room.id]) == 0:
		# Get the last direction (the way we came in)
		reverse = reverse_path.pop()
		# update traversal Path (travel back that way)
		traversal_path.append(reverse)
		#update player movement in the opposite direction as we need to back track to a room where above condition is not met
		player.travel(reverse)
	
	# Go to the first available exit (last added to the list for that room entry in the dictionary) 
	movement = visited[player.current_room.id].pop()

	# Update the path 
	traversal_path.append(movement)

	# Update the reverse path (for back tracking)
	reverse_path.append(reverse_directions[movement])

	# Update player movement to go in that direction
	player.travel(movement)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")