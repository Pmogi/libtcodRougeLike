from random import randint

from map_objects.tile import Tile
from map_objects.rectangle import Rect


class GameMap:
    def __init__(self, width, height):

        # width and height of map
        self.width = width
        self.height = height

        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        # create a map of blocked tiles
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles


    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player):
        # Create two rooms for demonstration
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # random width and range of room_max_size
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random position
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # "Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            # run through the other rooms to check if they intsersect
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break

            # otherwise this a viable place for a room
            else:
                # 'paint' the room to the map's tiles
                self.create_room(new_room)

                #center the coordinates of the room
                (new_x, new_y) = new_room.center()

                # if it's the first room, the player starts in the center
                if num_rooms == 0:
                    player.x = new_x
                    player.y = new_y
                else:
                    # after first room:
                    # Connect this room to the previous room with a tunnel
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # randomly decided to go horizontal then verticle or vice versa

                    if randint(0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                # finally, add the new room to the list
                rooms.append(new_room)
                num_rooms += 1



    def create_room(self, room):
        # go through the tiles in the rectangle, and make them passable
        # the x+1/y+1 accounts for the walls of the room
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False


    def create_h_tunnel(self, x1, x2, y):
        '''
        Create a tunnel between rooms in x-axis
        '''
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False


    def create_v_tunnel(self, y1, y2, x):
        '''
        Create a tunnet between rooms in y-axis
        '''
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        # if tile is blocked,
        if self.tiles[x][y].blocked == True:
            return True

        return False
