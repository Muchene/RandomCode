import argparse

class Room(object):
    def __init__(self, num):
        self.connected_rooms = []
        self.num = num
    
    def add_corridor(self, room):
        room.connected_rooms.append(self)
        self.connected_rooms.append(room)
        

def read_graph(fname):
    visited = {}
    with open(fname) as f:
        i = 0
        for line in f.readlines():
            if i == 0:
                parts = line.strip().split(",")
                num_rooms = int(parts[0])
                num_corridors = int(parts[1])
                num_steps = int(parts[2])
            else:
                parts = line.strip().split(",")
                
                visited[rkey(int(parts[0]), int(parts[1]))] = 0 
            i += 1
    if len(visited.keys()) != num_corridors:
        raise Exception("Error invalid input format: wrong number of corridors")
    rooms = {}
    for corridor in visited.keys():
        if corridor[0] not in rooms:
            rooms[corridor[0]] = Room(corridor[0])
        if corridor[1] not in rooms:
            rooms[corridor[1]] = Room(corridor[1])
        rooms[corridor[0]].add_corridor(rooms[corridor[1]])

    if len(rooms.keys()) != num_rooms:
        raise Exception("Error invalid input format : wrong number of rooms")
    return rooms,visited, num_steps


def rkey(r1, r2):
    return tuple(sorted((r1,r2)))

def explore(start_room, visited, num_steps, verbose=False):
    q = [start_room]
    current_room = start_room
    steps = 0
    while len(q) > 0 and steps < num_steps:
        current_room = q.pop()
        if verbose:
            print("Visiting room: {}".format(current_room.num))
        next_room = current_room.connected_rooms[0]
        for r in current_room.connected_rooms:
            if visited[rkey(current_room.num, r.num)] < visited[rkey(current_room.num, next_room.num)]:
                next_room = r
            elif visited[rkey(current_room.num, r.num)] == visited[rkey(current_room.num, next_room.num)]:
                if r.num < next_room.num:
                    next_room = r
        visited[rkey(current_room.num, next_room.num)] += 1
        q.append(next_room)
        steps += 1
    return current_room

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help= "input file")
    parser.add_argument("--verbose", default="store_false")
    args = parser.parse_args()
    rooms, visited, num_steps = read_graph(args.input)
    print("Stopping Room: {} ".format(explore(rooms[0], visited, num_steps, verbose=args.verbose).num))

if __name__ == "__main__":
    main()