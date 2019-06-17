from Window import *
import pygame
import sys
from tkinter import messagebox


def load_texture(file_name):
    """
    loads the texture and creates a surface with a texture blitted on top of it
    :param file_name: name of the file to load
    :return: surface if created properly, None otherwise
    """
    try:
        bit_map = pygame.image.load(file_name).convert_alpha()
        surface = pygame.Surface(bit_map.get_size(),
                                 pygame.HWSURFACE | pygame.SRCALPHA)
        surface.blit(bit_map, (0, 0))
        return surface
    except pygame.error:
        return None


class Textures:
    def __init__(self):
        self.tile_size = 16
        self.textures_dict = {}
        # checkerboard alike styled set of tiles is stored in this file.
        self.refill_tile_dictionary("images/sprite_sheets/default.png")
        # texture representing an idle (not clicked or focused) button
        self.button_idle = load_texture("images/icons/button_idle.png")
        # texture representing a button that is either pressed, or focused
        self.button_focused = load_texture("images/icons/button_focused.png")
        # texture of an icon that represents player's starting point in editor
        self.starting_position = load_texture("images/icons/start_position.png")
        # texture (supposedly) holding frames for player's movement animation, currently only 1 frame
        self.player_tiles = load_texture("images/sprite_sheets/temp_player.png")

        missing_files = []
        if self.button_idle is None:
            missing_files.append("images/icons/button_idle.png")
        if self.button_focused is None:
            missing_files.append("images/icons/button_focused.png")
        if self.starting_position is None:
            missing_files.append("images/icons/start_position.png")
        if not self.player_tiles:
            missing_files.append("images/sprite_sheets/player.png")
        if len(self.textures_dict) is 0:
            missing_files.append("images/sprite_sheets/default.png")
        if len(missing_files) > 0:
            tkinter.messagebox.showinfo("",
                                        "Important files could not be loaded")
            pygame.quit()
            sys.exit()

    def refill_tile_dictionary(self, file_name):
        """
        loads picture and splits it into several smaller pieces, which are then stored in texture_rep with
        their id's based on placement in original file
        :param file_name: name of a file to load
        :return: True if split were successful, False otherwise
        """
        try:
            bit_map = pygame.image.load(file_name).convert_alpha()
            if not bit_map:
                return False
            image_width, image_height = bit_map.get_size()
            if image_width < self.tile_size and image_height < self.tile_size:
                return False
            tile_table = []
            for tile_y in range(0, int(image_height / self.tile_size)):
                row = []
                for tile_x in range(0, int(image_width / self.tile_size)):
                    tile_rect = (tile_x * self.tile_size,
                                 tile_y * self.tile_size,
                                 self.tile_size,
                                 self.tile_size)
                    row.append(bit_map.subsurface(tile_rect))
                tile_table.append(row)
            self.textures_dict.clear()
            temp_id = 0
            for row in tile_table:
                for tile in row:
                    self.textures_dict[str(temp_id)] = tile
                    temp_id += 1
            return True
        except pygame.error:
            return False


textures_rep = Textures()
