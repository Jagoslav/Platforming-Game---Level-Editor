from Textures import *
import math
import json
from tkinter import messagebox
from tkinter import filedialog
import TestLevel


class MapEditor:
    def __init__(self):
        messagebox.showinfo("help",
                            "Use W,A,S,D keys to move around building area \n" +
                            "Place selected tiles using LPM and erase them with PPM \n" +
                            "To place player starting point press the scroll wheel \n" +
                            "Tile selection list can also be moved by using scroll wheel")
        # save button, located at 1/5th of a window width at the bottom of a screen
        self.button_save = Button("save",
                                  1 * window_frame.width / 8 - textures_rep.button_idle.get_size()[0] / 2,
                                  window_frame.height - 4 * textures_rep.tile_size)
        # load button, located at 2/5th of a window width at the bottom of a screen
        self.button_load = Button("load",
                                  3 * window_frame.width / 8 - textures_rep.button_idle.get_size()[0] / 2,
                                  window_frame.height - 4 * textures_rep.tile_size)
        # clear button, located at 3/5th of a window width at the bottom of a screen
        self.button_clear = Button("clear",
                                   5 * window_frame.width / 8 - textures_rep.button_idle.get_size()[0] / 2,
                                   window_frame.height - 4 * textures_rep.tile_size)
        # test button, located at 4/5th of a window width at the bottom of a screen
        self.button_test = Button("test",
                                  7 * window_frame.width / 8 - textures_rep.button_idle.get_size()[0] / 2,
                                  window_frame.height - 4 * textures_rep.tile_size)
        self.start_position = None  # point on a map where player will start
        self.build_area_pivot_x = 0  # pivot point to shift build area based on user's movement
        self.build_area_pivot_y = 0  # pivot point to shift build area based on user's movement
        # key type flags
        self.build_area_move_left = False
        self.build_area_move_right = False
        self.build_area_move_up = False
        self.build_area_move_down = False

        self.build_area_move_x = 0  # defines the x axis movement of a pivot point
        self.build_area_move_y = 0  # defines the y axis movement of a pivot point
        self.build_area_width = 100  # number of tiles in a row
        self.build_area_height = 40  # number of tiles in a column
        # surface of the displayed building area
        self.build_area_surface = pygame.Surface((self.build_area_width * textures_rep.tile_size,
                                                  self.build_area_height * textures_rep.tile_size),
                                                 pygame.HWSURFACE | pygame.SRCALPHA)
        # surface of the displayed building area
        self.event_area_surface = pygame.Surface((self.build_area_width * textures_rep.tile_size,
                                                  self.build_area_height * textures_rep.tile_size),
                                                 pygame.HWSURFACE | pygame.SRCALPHA)
        self.build_area_display = (
            0, 0, 44 * textures_rep.tile_size, 33 * textures_rep.tile_size)  # building area position on screen
        self.build_area_data = []  # list of placed tiles
        self.selector = pygame.Surface((textures_rep.tile_size,
                                        textures_rep.tile_size),
                                       pygame.HWSURFACE | pygame.SRCALPHA)  # highlighted tile surface
        self.selector.fill(with_alpha(100, color.red))  # color of the highlighting effect
        self.highlighted_tile = None  # position of a tile under the cursor
        # list of possible to place tiles, right side of a screen
        self.tile_selection_area = TileSelectionArea(44 * textures_rep.tile_size,
                                                     0,
                                                     window_frame.width - 44 * textures_rep.tile_size,
                                                     33 * textures_rep.tile_size)
        self.is_running = False  # loop flag

    def save_map(self):
        """
        saves map data to a specified location
        :return: State of the load. True if successfull, False otherwise
        """
        if self.start_position is None:
            messagebox.showerror("Error",
                                 "Can't save a file if player starting position is not specified")
            return False
        try:
            window_frame.tk_root.filename = filedialog.asksaveasfilename(initialdir="/",
                                                                         title="Select file",
                                                                         filetypes=(("save files", "*.save"),
                                                                                    ("all files", "*.*")))

            if window_frame.tk_root.filename == "":
                messagebox.showerror("Error",
                                     "File name not specified")
                return False
            if window_frame.tk_root.filename[-5:] == ".save":
                file = open(window_frame.tk_root.filename, 'w')
            else:
                file = open(window_frame.tk_root.filename + ".save", 'w')
            file.write(json.dumps({"map_width": self.build_area_width,
                                   "map_height": self.build_area_height,
                                   "map_data": self.build_area_data,
                                   "starting_position": self.start_position
                                   }))
            messagebox.showinfo("",
                                "File Saved")
            return True
        except IOError:
            messagebox.showerror("Error",
                                 "Save not possible")
            return False

    def load_map(self,):
        """
        loads map data from specified file
        :return: State of the load. True if successful, False otherwise
        """
        try:
            window_frame.tk_root.filename = filedialog.askopenfilename(initialdir="/",
                                                                       title="Select file",
                                                                       filetypes=(("save files", "*.save"),
                                                                                  ("all files", "*.*")))

            if window_frame.tk_root.filename == "":
                messagebox.showerror("Error",
                                     "File name not specified")
                return False
            print(window_frame.tk_root.filename)
            file = open(window_frame.tk_root.filename, 'r')
            info = json.loads(file.read())
            if info is None:
                return False
            build_area_width = info["map_width"]
            build_area_height = info["map_height"]
            temp_starting_position = info["starting_position"]
            starting_position = (temp_starting_position[0],
                                 temp_starting_position[1])
            temp_build_area_data = info["map_data"]
            build_area_data = []
            # change json's list back into a tuple...
            for temp in temp_build_area_data:
                temp_pos = (temp[0][0],
                            temp[0][1])
                temp_id = temp[1]
                build_area_data.append((temp_pos,
                                        temp_id))
            if temp_build_area_data is None \
                    or build_area_width is None \
                    or build_area_height is None \
                    or starting_position is None:
                return False
            build_area_surface = pygame.Surface((build_area_width * textures_rep.tile_size,
                                                 build_area_height * textures_rep.tile_size),
                                                pygame.HWSURFACE | pygame.SRCALPHA)
            event_area_surface = pygame.Surface((build_area_width * textures_rep.tile_size,
                                                 build_area_height * textures_rep.tile_size),
                                                pygame.HWSURFACE | pygame.SRCALPHA)
            event_area_surface.blit(textures_rep.starting_position,
                                    (starting_position[0] * textures_rep.tile_size,
                                     starting_position[1] * textures_rep.tile_size))
            for tile in build_area_data:
                build_area_surface.blit(textures_rep.textures_dict[tile[1]],
                                        (tile[0][0] * textures_rep.tile_size,
                                         tile[0][1] * textures_rep.tile_size))
            self.build_area_data = build_area_data
            self.build_area_width = build_area_width
            self.build_area_height = build_area_height
            self.build_area_surface = build_area_surface
            self.event_area_surface = event_area_surface
            self.start_position = starting_position
            messagebox.showinfo("",
                                "File successfully loaded")
            return True
        except IOError:
            messagebox.showerror("Error",
                                 "Corrupted save file")
            return False

    def test_map(self):
        """
        Allows user to test play his creation without a need of saving a file and running it in game
        :return:
        """
        if self.start_position is None:
            messagebox.showerror("Error",
                                 "Can't test a level if starting area is not specified")
            return

        level = TestLevel.TestLevel(self.build_area_width,
                                    self.build_area_height,
                                    self.build_area_data,
                                    self.start_position)
        level.run()

    def run(self):
        """
        main map_editor loop
        :return:
        """
        self.is_running = True
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.build_area_move_up = True
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.build_area_move_down = True
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.build_area_move_left = True
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.build_area_move_right = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.build_area_move_up = False
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.build_area_move_down = False
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.build_area_move_left = False
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.build_area_move_right = False
                elif event.type == pygame.MOUSEMOTION:
                    self.update_selector()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.tile_selection_area.x_pos < pos[0] \
                            <= self.tile_selection_area.x_pos + self.tile_selection_area.width \
                            and self.tile_selection_area.y_pos < pos[1] \
                            <= self.tile_selection_area.y_pos + self.tile_selection_area.height:
                        if event.button == 4:
                            self.tile_selection_area.shift_view(-textures_rep.tile_size)
                        elif event.button == 5:
                            self.tile_selection_area.shift_view(textures_rep.tile_size)
                        if event.button == 1:
                            self.tile_selection_area.select_tile(
                                (pos[0] - self.tile_selection_area.x_pos,
                                 pos[1] - self.tile_selection_area.y_pos))
            if pygame.mouse.get_pressed() != (0, 0, 0):
                if self.highlighted_tile:
                    # clicked position
                    tile_pos = (int((self.highlighted_tile[0] + self.build_area_pivot_x) / textures_rep.tile_size),
                                int((self.highlighted_tile[1] + self.build_area_pivot_y) / textures_rep.tile_size))
                    # is it inside drawing board?
                    click_allowed = True
                    if tile_pos[0] < self.build_area_display[0] or tile_pos[0] >= self.build_area_display[2] \
                            or tile_pos[1] < self.build_area_display[1] or tile_pos[1] >= self.build_area_display[3]:
                        click_allowed = False

                    # editing building area
                    if click_allowed:
                        found = False
                        for temp_tile in self.build_area_data:
                            if temp_tile[0] == tile_pos:
                                found = temp_tile[1]
                                break
                        # adding tiles
                        if pygame.mouse.get_pressed()[0] == 1:  # placing a tile
                            if tile_pos != self.start_position:
                                if found is not None:  # placing in already occupied area
                                    if self.tile_selection_area.selected_tile_id is not None:
                                        tile_to_add = (tile_pos, self.tile_selection_area.selected_tile_id)
                                        for temp_tile in self.build_area_data:
                                            if temp_tile[0] == tile_to_add[0]:
                                                self.build_area_data.remove(temp_tile)
                                        self.build_area_data.append(tile_to_add)
                                        pos_to_blit = (tile_pos[0] * textures_rep.tile_size,
                                                       tile_pos[1] * textures_rep.tile_size)
                                        pygame.draw.rect(self.build_area_surface,
                                                         color.transparent,
                                                         (pos_to_blit[0], pos_to_blit[1], textures_rep.tile_size,
                                                          textures_rep.tile_size))
                                        self.build_area_surface.blit(
                                            textures_rep.textures_dict[self.tile_selection_area.selected_tile_id],
                                            pos_to_blit)
                                else:  # placing a tile in a new spot
                                    if self.tile_selection_area.selected_tile_id is not None:
                                        tile_to_add = (tile_pos, self.tile_selection_area.selected_tile_id)
                                        self.build_area_data.append(tile_to_add)
                                        pos_to_blit = (tile_pos[0] * textures_rep.tile_size,
                                                       tile_pos[1] * textures_rep.tile_size)
                                        self.build_area_surface.blit(
                                            textures_rep.textures_dict[self.tile_selection_area.selected_tile_id],
                                            pos_to_blit)
                        # removing tiles
                        elif pygame.mouse.get_pressed()[2] == 1:
                            if tile_pos == self.start_position:
                                pos_to_clear = (self.start_position[0] * textures_rep.tile_size,
                                                self.start_position[1] * textures_rep.tile_size)
                                pygame.draw.rect(self.event_area_surface,
                                                 color.transparent,
                                                 (pos_to_clear[0],
                                                  pos_to_clear[1],
                                                  textures_rep.tile_size,
                                                  textures_rep.tile_size))
                                self.start_position = None
                            if found:
                                tile_to_add = (tile_pos, self.tile_selection_area.selected_tile_id)
                                for temp_tile in self.build_area_data:
                                    if temp_tile[0] == tile_to_add[0]:
                                        self.build_area_data.remove(temp_tile)
                                        clear_rect = (tile_pos[0] * textures_rep.tile_size,
                                                      tile_pos[1] * textures_rep.tile_size,
                                                      textures_rep.tile_size,
                                                      textures_rep.tile_size)
                                        self.build_area_surface.fill(color.transparent,
                                                                     clear_rect)
                        # placing player starting position
                        elif pygame.mouse.get_pressed()[1] == 1:
                            # can't place a player on an active surface
                            if not found:
                                if self.start_position is not None:
                                    pos_to_clear = (self.start_position[0] * textures_rep.tile_size,
                                                    self.start_position[1] * textures_rep.tile_size)
                                    pygame.draw.rect(self.event_area_surface,
                                                     color.transparent,
                                                     (pos_to_clear[0],
                                                      pos_to_clear[1],
                                                      textures_rep.tile_size,
                                                      textures_rep.tile_size))
                                self.start_position = tile_pos
                                pos_to_blit = (tile_pos[0] * textures_rep.tile_size,
                                               tile_pos[1] * textures_rep.tile_size)
                                self.event_area_surface.blit(textures_rep.starting_position,
                                                             pos_to_blit)

                if self.button_load.is_focused():
                    self.load_map()
                if self.button_save.is_focused():
                    self.save_map()
                if self.button_clear.is_focused():
                    self.build_area_data = []
                    # surface of the displayed building area
                    self.build_area_surface = pygame.Surface((self.build_area_width * textures_rep.tile_size,
                                                              self.build_area_height * textures_rep.tile_size),
                                                             pygame.HWSURFACE | pygame.SRCALPHA)
                    self.start_position = None
                    # surface of the displayed building area
                    self.event_area_surface = pygame.Surface((self.build_area_width * textures_rep.tile_size,
                                                              self.build_area_height * textures_rep.tile_size),
                                                             pygame.HWSURFACE | pygame.SRCALPHA)
                if self.button_test.is_focused():
                    self.test_map()

            # LOGIC
            if self.build_area_move_left and self.build_area_move_right:
                self.build_area_move_x = 0
            elif self.build_area_move_left:
                self.build_area_move_x = -1
            elif self.build_area_move_right:
                self.build_area_move_x = 1
            else:
                self.build_area_move_x = 0
            if self.build_area_move_up and self.build_area_move_down:
                self.build_area_move_y = 0
            elif self.build_area_move_up:
                self.build_area_move_y = -1
            elif self.build_area_move_down:
                self.build_area_move_y = 1
            else:
                self.build_area_move_y = 0
            move_rect_x = tuple(sum(i) for i in zip(self.build_area_display,
                                                    (self.build_area_pivot_x + self.build_area_move_x,
                                                     self.build_area_pivot_y,
                                                     0,
                                                     0)))
            move_rect_y = tuple(sum(i) for i in zip(self.build_area_display,
                                                    (self.build_area_pivot_x,
                                                     self.build_area_pivot_y + self.build_area_move_y,
                                                     0,
                                                     0)))
            if self.build_area_surface.get_rect().contains(move_rect_x):
                self.build_area_pivot_x += self.build_area_move_x
                self.update_selector()
            if self.build_area_surface.get_rect().contains(move_rect_y):
                self.build_area_pivot_y += self.build_area_move_y
                self.update_selector()
            self.button_save.update()
            self.button_load.update()
            self.button_clear.update()
            self.button_test.update()
            # GRAPHICS
            window_frame.display.fill(color.white)  # background
            window_frame.display.blit(self.build_area_surface,
                                      (0, 0),
                                      (0 + self.build_area_pivot_x,
                                       0 + self.build_area_pivot_y,
                                       self.build_area_display[2],
                                       self.build_area_display[3]))  # draw building zone
            window_frame.display.blit(self.event_area_surface,
                                      (0, 0),
                                      (0 + self.build_area_pivot_x,
                                       0 + self.build_area_pivot_y,
                                       self.build_area_display[2],
                                       self.build_area_display[3]))  # draw event zone
            if self.highlighted_tile:
                window_frame.display.blit(self.selector,
                                          (self.highlighted_tile[0],
                                           self.highlighted_tile[1]))  # highlights the tile under cursor
            # clear part of a screen where selected tile could be drawn outside of bounds
            pygame.draw.rect(window_frame.display,
                             color.white,
                             (self.tile_selection_area.x_pos,
                              self.tile_selection_area.y_pos,
                              textures_rep.tile_size,
                              window_frame.height))
            # clear part of a screen where selected tile could be drawn outside of bounds
            pygame.draw.rect(window_frame.display,
                             color.white,
                             (0,
                              self.build_area_display[3],
                              self.build_area_display[2],
                              textures_rep.tile_size))
            window_frame.display.blit(self.tile_selection_area.tile_selection_surface,
                                      (self.tile_selection_area.x_pos,
                                       self.tile_selection_area.y_pos),
                                      (0,
                                       self.tile_selection_area.shift,
                                       self.tile_selection_area.width,
                                       self.tile_selection_area.height))  # draw tile's selection list
            pygame.draw.rect(window_frame.display,
                             color.black,
                             self.build_area_display,
                             2)  # draw building area's bounds
            pygame.draw.rect(window_frame.display, color.black,
                             (self.tile_selection_area.x_pos,
                              self.tile_selection_area.y_pos,
                              self.tile_selection_area.width,
                              self.tile_selection_area.height),
                             2)  # draw tile's selection list's bounds
            self.button_save.draw()
            self.button_load.draw()
            self.button_clear.draw()
            self.button_test.draw()
            pygame.display.update()
            window_frame.get_fps()

    def update_selector(self):
        """
        updates the position of a tile highlighter under user's mouse
        :return:
        """
        pos = pygame.mouse.get_pos()
        if pos[0] < self.build_area_display[0] or pos[0] >= self.build_area_display[2] \
                or pos[1] < self.build_area_display[1] or pos[1] >= self.build_area_display[3]:
            self.highlighted_tile = None
        else:
            self.highlighted_tile = (math.floor((pos[0] + self.build_area_pivot_x) / textures_rep.tile_size)
                                     * textures_rep.tile_size - self.build_area_pivot_x,
                                     math.floor((pos[1] + self.build_area_pivot_y) / textures_rep.tile_size)
                                     * textures_rep.tile_size - self.build_area_pivot_y)


class Button:
    def __init__(self, msg, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width, self.height = textures_rep.button_idle.get_size()
        font = pygame.font.SysFont(None, 16)
        self.text_surface = font.render(msg, True, Color.black)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (self.x_pos + self.width / 2, self.y_pos + self.height / 2)
        self.focused = False
        self.pressed = False

    def draw(self):
        if self.focused:
            window_frame.display.blit(textures_rep.button_focused, (self.x_pos, self.y_pos))
        else:
            window_frame.display.blit(textures_rep.button_idle, (self.x_pos, self.y_pos))
        window_frame.display.blit(self.text_surface, self.text_rect)

    def update(self):
        if pygame.mouse.get_pressed() != (0, 0, 0):
            return
        pos = pygame.mouse.get_pos()
        if self.x_pos < pos[0] < self.x_pos + self.width \
                and self.y_pos < pos[1] < self.y_pos + self.height:
            self.focused = True
        else:
            self.focused = False

    def is_focused(self):
        return self.focused


class TileSelectionArea:
    def __init__(self, x_pos, y_pos, width, height):
        self.tiles_id = []  # list of tiles id's in a surface.
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.shift = 0  # defines which part of a surface should be displayed in its area
        self.spacing = 0  # distance between two tiles on a display surface
        self.tiles_per_row = 0  # number of tiles displayed in a single row
        self.tile_selection_surface = None  # surface to display all tiles to choose from
        self.tiles_id_list = []  # tiles in a list
        self.load_tiles()
        self.selected_tile_id = None  # id of a tile to select

    def select_tile(self, mouse_pos):
        """
        selects tile from the list based on mouse position
        :param mouse_pos: position of a mouse in relation to object's area
        :return:
        """
        mouse_pos = (mouse_pos[0], mouse_pos[1] + self.shift)
        selected_tile_pos = (math.floor((mouse_pos[0] - self.spacing / 2) / (textures_rep.tile_size + self.spacing)),
                             math.floor((mouse_pos[1] - self.spacing / 2) / (textures_rep.tile_size + self.spacing)))
        if self.selected_tile_id:
            old_selection_rect = (
                (int(self.selected_tile_id) % self.tiles_per_row) * (textures_rep.tile_size + self.spacing),
                math.floor((int(self.selected_tile_id) / self.tiles_per_row)) * (textures_rep.tile_size + self.spacing),
                textures_rep.tile_size + self.spacing,
                textures_rep.tile_size + self.spacing)
            pygame.draw.rect(self.tile_selection_surface,
                             color.transparent,
                             old_selection_rect,
                             2)
        new_selection_rect = (selected_tile_pos[0] * (textures_rep.tile_size + self.spacing),
                              selected_tile_pos[1] * (textures_rep.tile_size + self.spacing),
                              textures_rep.tile_size + self.spacing,
                              textures_rep.tile_size + self.spacing)
        pygame.draw.rect(self.tile_selection_surface,
                         color.red,
                         new_selection_rect,
                         2)
        self.selected_tile_id = str(selected_tile_pos[0] + self.tiles_per_row * selected_tile_pos[1])

    def shift_view(self, distance):
        """
        slides through tile selection surface allowing to choose tiles normally outside of a screen
        :param distance: distance o shift
        :return:
        """
        if distance > 0:
            self.shift = min(self.shift + distance, self.tile_selection_surface.get_rect()[3] - self.height)
        else:
            self.shift = max(self.shift + distance, 0)

    def load_tiles(self):
        """
        fills the list with tiles from a sprite sheet
        :return:
        """
        self.tiles_id_list = textures_rep.textures_dict.keys()
        self.tiles_per_row = math.floor(self.width / (3 * textures_rep.tile_size / 2 - 1))
        self.spacing = self.width / self.tiles_per_row - textures_rep.tile_size
        minimal_required_height = max(self.height,
                                      (textures_rep.tile_size + self.spacing)
                                      * (math.ceil(len(self.tiles_id_list) / self.tiles_per_row)))
        self.tile_selection_surface = pygame.Surface((self.width,
                                                      minimal_required_height),
                                                     pygame.HWSURFACE | pygame.SRCALPHA)
        pygame.draw.rect(self.tile_selection_surface, color.transparent, self.tile_selection_surface.get_rect())
        for tile_id in self.tiles_id_list:
            blit_x = self.spacing / 2 + \
                (int(tile_id) % self.tiles_per_row) * (self.spacing + textures_rep.tile_size)
            blit_y = self.spacing / 2 \
                + math.floor((int(tile_id) / self.tiles_per_row)) \
                * (self.spacing + textures_rep.tile_size)
            self.tile_selection_surface.blit(textures_rep.textures_dict[tile_id],
                                             (blit_x, blit_y))
