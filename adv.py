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

# We need a way to go backwards
reverse = {
        'n': 's',
        's': 'n',
        'e': 'w',
        'w': 'e'
}

def traverse(starting_room, visited=set()):
    # begin with path empty to fill in and append
    path = []

    # make basic loop to traverse
    for i in player.current_room.get_exits():
        player.travel(i)

        # visit the room and reverse out
        if player.current_room in visited:
            player.travel(reverse[i])
        # otherwise keep moving and add rooms
        else:
            visited.add(player.current_room)
            path.append(i)
            path = path + traverse(player.current_room, visited)
            player.travel(reverse[i])
            path.append(reverse[i])

    return path

# begin empty and traverse through using graph
traversal_path = []
traversal_path = traverse(player.current_room)



# TRAVERSAL TEST - DO NOT MODIFY
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
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
