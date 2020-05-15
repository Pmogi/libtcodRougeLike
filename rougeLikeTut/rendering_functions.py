# Rendering functions
import tcod as libtcod

def render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
    # Draw all the tiles in the game map
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):

                # the visible tiles calculated by libtcod fov alogrithm
                visible = libtcod.map_is_in_fov(fov_map, x, y)

                wall = game_map.tiles[x][y].block_sight


                # if visible draw a light_ground/light_wall
                if visible:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_wall'), libtcod.BKGND_SET)

                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)
                    game_map.tiles[x][y].explored = True



                # if the tiles has been explored before, leave an outline of the room with the dark_wall/dark_ground
                elif game_map.tiles[x][y].explored == True:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)
                # otherwise the room is not visi
                #else:
                #    pass

    # draw all entities in the list
    for entity in entities:
        draw_entity(con, entity, fov_map)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity, fov_map):
    '''
    Draw entity on desired console based on their x and y position
    '''

    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

def clear_entity(con, entity):
    '''
    Clear's entity positon
    '''
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
