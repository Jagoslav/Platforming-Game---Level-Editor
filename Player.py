from Textures import *


class Player:
    def __init__(self, position):
        self.x_pos = position[0]  # x position of a player
        self.y_pos = position[1]  # y position of a player
        self.move_left = False  # flags the desire of a player to move left
        self.move_right = False  # flags the desire of a player to move right
        self.jump = False  # flags the desire of a player to jump
        self.jump_possible = True  # defines if a player is able to make a jump (stays on a ground
        self.velocity_x = 0  # defines the velocity of a player along the x axis
        self.velocity_y = 0  # defines the velocity of a player along the y axis
        self.top_jump_speed = 3  # terminal initial velocity of a jump
        self.top_move_speed = 3  # terminal velocity of players movement
        self.bounds = (0 - textures_rep.player_tiles.get_size()[0] / 2,
                       0 - textures_rep.player_tiles.get_size()[1] / 2,
                       textures_rep.player_tiles.get_size()[0],
                       textures_rep.player_tiles.get_size()[1])  # bounds of a player's position with shifted center
        self.is_alive = True  # life status (player dies if he fells out of a map

    def move(self, bounds_list, map_bounds):
        """
        Controls the movement of a player based on his velocity and collision checking
        :param bounds_list: collision boxes of map's solid surfaces
        :param map_bounds: collision of the whole map area
        :return:
        """
        # player dependent and desired movement
        if self.move_left and self.move_right:
            self.velocity_x = 0
        elif self.move_right:
            self.velocity_x = self.top_move_speed
        elif self.move_left:
            self.velocity_x = -self.top_move_speed
        else:
            self.velocity_x = 0
        if self.jump and self.jump_possible:
            self.velocity_y = -self.top_jump_speed
            self.jump_possible = False
        else:
            self.velocity_y += 0.1 * window_frame.delta_time

        # collision checking
        temp_move_x = pygame.Rect(self.x_pos + self.velocity_x * window_frame.delta_time,
                                  self.y_pos,
                                  textures_rep.player_tiles.get_size()[0],
                                  textures_rep.player_tiles.get_size()[1])  # bounds of a movement on x axis
        temp_move_y = pygame.Rect(self.x_pos,
                                  self.y_pos + self.velocity_y * window_frame.delta_time,
                                  textures_rep.player_tiles.get_size()[0],
                                  textures_rep.player_tiles.get_size()[1])  # bounds of a movement on y axis
        if temp_move_x.collidelist(bounds_list) == -1 and map_bounds.contains(temp_move_x):
            self.x_pos += self.velocity_x * window_frame.delta_time
        if temp_move_y.collidelist(bounds_list) == -1 and map_bounds.contains(temp_move_y):
            self.y_pos += self.velocity_y * window_frame.delta_time
            self.jump_possible = False
        else:
            self.velocity_y = 0
            self.jump_possible = True
        if self.y_pos + textures_rep.player_tiles.get_size()[1] + 0.01 > map_bounds[1] + map_bounds[3]:
            self.is_alive = False

    def get_animation_frame(self):
        """
        Supposed to return the right animation frame, returns the whole player image instead
        :return: player's texture
        """
        # if statement to trick compiler to thinking it can't be static function instead of method.
        if self.is_alive:
            return textures_rep.player_tiles
        else:
            return textures_rep.player_tiles
