# tile object container

class Tile:
    '''
    A tile on a map. It may or may not be block movement and may or may not block sight.
    '''
    def __init__(self, blocked, block_sight=None):
        # if a tile is blocked, it cannot be moved through
        self.blocked = blocked

        # tile is initially not known to the player
        self.explored = False

        # By default, if a tile is blocks movement, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
