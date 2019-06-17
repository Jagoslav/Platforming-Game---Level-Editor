from Player import *
import tkinter
from tkinter import messagebox


class TestLevel:
    def __init__(self, width, height, map_data, start_position):
        """
        initiate the object
        :param width: width of a map
        :param height: height of a map
        :param map_data: solid objects placed on a map
        :param start_position: starting position of a player
        """
        self.width = width * textures_rep.tile_size  # width of the map
        self.height = height * textures_rep.tile_size  # height of the map
        self.bounds = pygame.Rect(0,
                                  0,
                                  self.width,
                                  self.height)  # rectangular bounds of the map
        self.display_bounds = pygame.Rect(0,
                                          0,
                                          window_frame.width,
                                          window_frame.height)  # area of a map to display on screen
        self.map_surface = pygame.Surface((self.width,
                                           self.height),
                                          pygame.HWSURFACE | pygame.SRCALPHA)  # surface of the displayed building area
        pygame.draw.rect(self.map_surface,
                         color.white,
                         self.bounds,
                         4)
        self.solid_blocks = []  # solid objects present on a level
        for tile in map_data:
            bounds_rect = (tile[0][0] * textures_rep.tile_size,
                           tile[0][1] * textures_rep.tile_size,
                           textures_rep.tile_size,
                           textures_rep.tile_size)
            self.map_surface.blit(textures_rep.textures_dict[tile[1]],
                                  (bounds_rect[0],
                                   bounds_rect[1]))
            self.solid_blocks.append(bounds_rect)
        self.player = Player((start_position[0] * textures_rep.tile_size,
                              start_position[1] * textures_rep.tile_size))
        self.view_shift = ((start_position[0] * textures_rep.tile_size)
                           - window_frame.width / 2 + textures_rep.player_tiles.get_width() / 2,
                           (start_position[1] * textures_rep.tile_size)
                           - window_frame.height / 2 + textures_rep.player_tiles.get_height() / 2)
        self.is_running = False  # loop flag

    def run(self):
        self.is_running = True
        while self.is_running:
            if self.player is None:
                self.is_running = False
                continue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                    elif event.key == pygame.K_a:
                        self.player.move_left = True
                    elif event.key == pygame.K_d:
                        self.player.move_right = True
                    elif event.key == pygame.K_w:
                        self.player.jump = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.player.move_left = False
                    elif event.key == pygame.K_d:
                        self.player.move_right = False
                    elif event.key == pygame.K_w:
                        self.player.jump = False

            # LOGIC
            self.view_shift = (self.player.x_pos - window_frame.width / 2 + textures_rep.player_tiles.get_width() / 2,
                               self.player.y_pos - window_frame.height / 2 + textures_rep.player_tiles.get_height() / 2)
            # RENDER
            window_frame.display.fill(Color.black)
            window_frame.display.blit(self.map_surface,
                                      (0, 0),
                                      (0 + self.view_shift[0],
                                       0 + self.view_shift[1],
                                       window_frame.width,
                                       window_frame.height))  # draw building zone
            window_frame.display.blit(self.player.get_animation_frame(),
                                      (window_frame.width / 2 - textures_rep.player_tiles.get_width() / 2,
                                       window_frame.height / 2 - textures_rep.player_tiles.get_height() / 2))
            self.player.move(self.solid_blocks, self.bounds)
            if not self.player.is_alive:
                self.is_running = False
                tkinter.messagebox.showinfo("",
                                            "You died")
            pygame.display.update()
            window_frame.get_fps()
