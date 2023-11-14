"""
File in charge of containing the chess board screen
"""

from time import sleep
from functools import partial
import asciimatics.widgets as WIG
from asciimatics.event import Event
from asciimatics.exceptions import NextScene
from asciimatics_overlay_ov import AsciiMaticsOverlayMain
from asciimatics_overlay_ov.widgets import FrameNodes


class ChessTest(WIG.Frame, AsciiMaticsOverlayMain, FrameNodes):
    """ A simple Chess board window """

    def __init__(self, screen):
        super(ChessTest, self).__init__(
            screen,
            screen.height,
            screen.width,
            has_border=True,
            title="Chess Test"
        )
        self.frame_node = FrameNodes()
        self.event = Event()
        self.asciimatics_overlay = AsciiMaticsOverlayMain(self.event, screen)
        self.asciimatics_overlay.update_initial_pointers(self.event, screen)
        # Define a layout with three columns
        self.layout = WIG.Layout([100], fill_frame=True)
        self.add_layout(self.layout)
        self.place_content_on_screen()
        self.fix()

    def place_content_on_screen(self) -> None:
        """ Create the welcome screen """
        self.layout.add_widget(
            self.add_label(
                "Hello World !",
                align=self.frame_node.label_center,
                name=None
            ),
            0
        )
        self.layout.add_widget(
            self.add_button(
                text="Draw chess",
                on_click=self._draw_chess,
                box=True,
                name=None
            ),
            0
        )
        self.layout.add_widget(
            self.add_button(
                text="Exit",
                on_click=self._exit,
                name=None
            ),
            0
        )

    def _draw_chess(self) -> None:
        """ Draw a chess board """
        self.asciimatics_overlay.mvprintw_colour(
            text="jfdjioqdsjqosjdioqsdiqsjdiqsjdqdqsjdqsodjqjsoidqsdqsd",
            posx=5,
            posy=5,
            colour=7,
            attr=0,
            bg=0,
            transparent=False,
            parent_screen=None
        )
        sleep(4)
        self.asciimatics_overlay.print_checker_board(
            data_array=[],
            width=64,
            height=64,
            iposx=1,
            iposy=1,
            seperator_character_vertical="|",
            seperator_character_horizontal="-",
            even_bg_colour=self.asciimatics_overlay.colour_cyan,
            even_fg_colour=self.asciimatics_overlay.colour_black,
            uneven_bg_colour=self.asciimatics_overlay.colour_green,
            uneven_fg_colour=self.asciimatics_overlay.colour_black,
            border_fg=self.asciimatics_overlay.colour_yellow,
            border_bg=self.asciimatics_overlay.colour_black,
            transparent_even=False,
            transparent_uneven=False,
            border_transparent=False,
            attr_even=0,
            attr_uneven=0,
            parent_screen=None
        )

    def _exit(self):
        raise NextScene("Main")
