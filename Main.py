# created with Python 3.6 in Pycharm Community Edition 2017 2.4
# author Jakub Grzeszczak
# sources required to run this program:
# every .png file was created from scratch as a basic template for this project
# application requires pygame library to run. Version used in production (1.9.3-cp36-win_amd64) can be downloaded
# here: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame
from MapEditor import *
from TestLevel import *


if __name__ == "__main__":
    map_editor = MapEditor()
    map_editor.run()
    pygame.quit()
    sys.exit()
