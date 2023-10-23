"""
File in charge of containing binders for the Screen interraction
"""

from asciimatics.screen import Screen as SC


class MyScreen:
    """ The class in wharge of containing the binders for the Screen insterractions """

    def __init__(self, screen: SC = None) -> None:
        self.success = 0
        self.my_asciimatics_overlay_main_screen = screen

    def destroy_game_screen(self) -> int:
        """ Destroy the game screen """
        self.my_asciimatics_overlay_main_screen.close()
        return self.success

    def create_game_screen(self) -> int:
        """ Create the game screen """
        self.my_asciimatics_overlay_main_screen = SC.open()
        return self.success
