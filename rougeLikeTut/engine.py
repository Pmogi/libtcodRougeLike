import tcod as libtcod

from input_handler import handle_keys
from entity import Entity
from rendering_functions import clear_all, render_all

from map_objects.game_map import GameMap
from fov_functions import initialize_fov, compute_fov



def main():
    screen_height = 50
    screen_width = 80

    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    colors = {
        'dark_wall'   : libtcod.Color(0, 0, 100),
        'dark_ground' : libtcod.Color(50, 50, 150),
        'light_wall'  : libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    # initial position for player
    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', libtcod.white)

    # test NPC
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), '@', libtcod.yellow)

    # creates list of current entities
    entities = [npc, player]

    # set font for game
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # makes root console
    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)

    # console for drawing the game
    con = libtcod.console.Console(screen_width, screen_height)

    # instance the game's map
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)

    # init field-of-view for player character
    fov_recompute = True
    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        # gets new events, and updates key and mouse
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            compute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)
            # recomputed, until player moves, don't recomputer fov map
            


        libtcod.console_set_default_foreground(con, libtcod.white)


        # render all entities to desired console
        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)
        fov_recompute = False

        # output to console
        libtcod.console_flush()

        # clear last position
        clear_all(con, entities)

        # obtain event
        action = handle_keys(key)

        # check and handle event
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            # from the move dictionary obtain the x and y and update player pos
            dx, dy = move

            # check if direction of movement is towards blocked tile
            if not game_map.is_blocked(player.x + dx, player.y + dy):

                # if not blocked, move player there
                player.move(dx, dy)

                fov_recompute = True

        if exit:
            return True

        # toggles full screen based on ALT+ENTER user event
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())




if __name__ == '__main__':
  main()
