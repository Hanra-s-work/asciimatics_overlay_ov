"""
File in charge of acting as the main script of the library when it is called as a standalone
"""
from asciimatics_overlay_ov import AsciimaticsOverlay
from asciimatics.event import Event
from asciimatics.screen import Screen
from random import randint
from time import sleep


print("Hello world")


SUCCESS = 0
ERROR = 1
QUOTES = [
    "Carpe Diem",
    "Think big",
    "Dream big",
    "Love wins",
    "Be yourself",
    "Stay curious",
    "Never give up",
    "Less is more",
    "Do it now",
    "Live fully",
    "Stay positive",
    "Learn, adapt, overcome",
    "Embrace the journey",
    "Create, not consume",
    "Seek inner peace",
    "Follow your heart",
    "Chase your dreams",
    "Keep it simple",
    "Stay humble",
    "Work hard, play hard",
    "Find your passion",
    "Love unconditionally",
    "Hope never dies",
    "Time heals all",
    "Believe in yourself",
    "Spread love, not hate",
    "Make it happen",
    "Smile, be happy"
]


def _get_colour_data(amom: AsciimaticsOverlay) -> list:
    """ Get a set of available colours for automating"""
    colour_options = list(amom.human_bind)
    colour_options_length = len(colour_options) - 1
    return colour_options, colour_options_length


def _get_random_colour(colour_data: list[list, int]) -> str:
    """ Get a random colour from the available ones """
    colour_options, colour_options_length = colour_data
    choice = randint(0, colour_options_length)
    return colour_options[choice]


def _make_transparent() -> bool:
    """ Check if the colour is transparent """
    choice = randint(0, 10) % 2
    return bool(choice)


def _is_quit_key_pressed(amom: AsciimaticsOverlay) -> bool:
    """ Check if the key to stop the animation was pressed """
    pressed_key = amom.get_event_key_code()
    if amom.is_it_this_key(pressed_key, "q") is True or amom.is_it_this_key(pressed_key, "Q") is True:
        return True
    return False


def _goodbye_message(amom: AsciimaticsOverlay, colour_data: list[list, int]) -> int:
    line_top = "                                "
    line_center = "  Goodbye, see you next time !  "
    line_bottom = "                                "
    center_screen_x = amom.get_screen_center_x()
    center_screen_y = amom.get_screen_center_y()
    center_colour_fg = amom.pick_colour(_get_random_colour(colour_data))
    center_colour_bg = amom.pick_colour(_get_random_colour(colour_data))
    if center_colour_fg == center_colour_bg:
        if center_colour_fg == 0:
            center_colour_bg = 1
        else:
            center_colour_bg -= 1
    padding_top = 4
    padding_bottom = 4
    for i in range(1, padding_top+1):
        amom.mvprintw_colour(
            line_top,
            center_screen_x,
            center_screen_y-i,
            center_colour_fg,
            0,
            center_colour_bg,
            False
        )
    amom.mvprintw_colour(
        line_center,
        center_screen_x,
        center_screen_y,
        center_colour_fg,
        0,
        center_colour_bg,
        False
    )
    for i in range(1, padding_bottom+1):
        amom.mvprintw_colour(
            line_bottom,
            center_screen_x,
            center_screen_y+i,
            center_colour_fg,
            0,
            center_colour_bg,
            False
        )
    amom.my_asciimatics_overlay_main_screen.refresh()
    sleep(4)


def _funk_up_the_display(amom: AsciimaticsOverlay, colour_data: list[list, int], main_loop: bool = True) -> int:
    """ Update the display with funny text """
    screen_width = amom.get_screen_width()
    screen_height = amom.get_screen_height()-1
    quotes_length = len(QUOTES)-1
    while main_loop is True:
        x = randint(0, screen_width)
        y = randint(0, screen_height)
        random_foreground = amom.pick_colour(_get_random_colour(colour_data))
        random_background = amom.pick_colour(_get_random_colour(colour_data))
        random_content = QUOTES[randint(0, quotes_length)]
        random_transparent = _make_transparent()
        amom.mvprintw_colour(
            random_content,
            x,
            y,
            random_foreground,
            0,
            random_background,
            random_transparent
        )
        if _is_quit_key_pressed(amom) is True:
            _goodbye_message(amom, colour_data)
            break
        amom.my_asciimatics_overlay_main_screen.refresh()
    return SUCCESS


def main(screen: Screen) -> int:
    """ The main function """
    event = Event()
    main_loop = True
    amom = AsciimaticsOverlay(event, screen)
    amom.update_initial_pointers(event, screen)
    colour_data = _get_colour_data(amom)
    _funk_up_the_display(amom, colour_data, main_loop)
    amom.screen_.destroy_game_screen()
    return SUCCESS


if __name__ == "__main__":
    error = 1
    try:
        status = Screen.wrapper(main)
        exit(status)
    except Exception as err:
        print(f"Error: {err}")
        exit(error)
