"""
File in charge of displaying content on the screen
"""

from asciimatics.screen import Screen as SC


class Display:
    """ Class in charge of displaying content on the screen """

    def __init__(self, screen: SC) -> None:
        self.my_asciimatics_overlay_main_screen = screen

    def mvprintw(self, text: str, posx: int, posy: int, width: int = 0) -> None:
        """ Display a string at a specific location """
        self.my_asciimatics_overlay_main_screen.print_at(
            text,
            posx,
            posy,
            width
        )

    def mvprintw_colour(self, text: str, posx: int, posy: int, colour: int = 7, attr: int = 0, bg: int = 0, transparent: bool = False) -> None:
        """ Display a string at a specific location with a specific colour """
        self.my_asciimatics_overlay_main_screen.print_at(
            text,
            posx,
            posy,
            colour,
            attr,
            bg,
            transparent
        )

    def print_array(self, array: list, seperator: str, posx: int, posy: int, colour: int = 7, attr: int = 0, bg: int = 0, transparent: bool = False) -> None:
        """ Display an array at a specific location with a specific colour """
        self.my_asciimatics_overlay_main_screen.print_at(
            seperator.join(array),
            posx,
            posy,
            colour,
            attr,
            bg,
            transparent
        )

    def print_array_colour(self, array: list[dict], seperator: str, posx: int, posy: int, colour: int = 7, attr: int = 0, bg: int = 0, transparent: bool = False) -> None:
        """ Display an array at a specific location with a specific colour """
        default_list = {
            "seperator": seperator,
            "posx": posx,
            "posy": posy,
            "colour": colour,
            "attr": attr,
            "bg": bg,
            "transparent": transparent
        }
        for index, item in enumerate(array):
            for key, value in default_list.items():
                if hasattr(item, key) is False and key == "posx":
                    item[key] = posx + index
                if hasattr(item, key) is False:
                    item[key] = value
            self.my_asciimatics_overlay_main_screen.print_at(
                item["text"],
                item["posx"],
                item["posy"],
                item["colour"],
                item["attr"],
                item["bg"],
                item["transparent"]
            )

    def print_double_array(self, array: list[list], seperator: str, posx: int, posy: int, colour: int = 7, attr: int = 0, bg: int = 0, transparent: bool = False) -> None:
        """ Display a double array at a specific location with a specific colour """
        result = ""
        for i in array:
            result += seperator.join(i)
            result += "\n"
        self.my_asciimatics_overlay_main_screen.print_at(
            result,
            posx,
            posy,
            colour,
            attr,
            bg,
            transparent
        )

    def print_double_array_colour(self, array: list[list[dict]], seperator: str, posx: int, posy: int, colour: int = 7, attr: int = 0, bg: int = 0, transparent: bool = False) -> None:
        """ Display a double array at a specific location with a specific colour """
        for index, item in enumerate(array):
            self.print_array_colour(
                item,
                seperator,
                posx,
                posy+index,
                colour,
                attr,
                bg,
                transparent
            )

    def print_array_cloud_points(self, array: list[dict], iposx: int = 0, iposy: int = 0, colour: int = 7, attr: int = 0, bg: int = 0, transparent: bool = False) -> None:
        """ Display a double array at a specific location with a specific colour """
        new_posx = 0
        new_posy = 0
        new_character = ""
        new_colour = colour
        new_attr = attr
        new_bg = bg
        new_transparent = transparent
        prev_y = 0
        for line, character in enumerate(array):
            if "posx" in character:
                new_posx = character["posx"]+iposx
            else:
                new_posx = line + iposx
            if "posy" in character:
                new_posy = character["posy"] + iposy
                prev_y = character["posy"]
            else:
                new_posy = prev_y + iposy
            if "character" in character:
                new_character = character["character"]
            else:
                new_character = " "
            if "colour" in character:
                new_colour = character["colour"]
            else:
                new_colour = colour
            if "attr" in character:
                new_attr = character["attr"]
            else:
                new_attr = attr
            if "bg" in character:
                new_bg = character["bg"]
            else:
                new_bg = bg
            if "transparent" in character:
                new_transparent = character["transparent"]
            else:
                new_transparent = transparent
            self.my_asciimatics_overlay_main_screen.print_at(
                new_character,
                new_posx,
                new_posy,
                new_colour,
                new_attr,
                new_bg,
                new_transparent
            )

    def print_double_array_cloud_points(self, array: list[list[dict]], iposx: int = 0, iposy: int = 0, colour: int = 7, attr: int = 0, bg: int = 0, transparent: bool = False) -> None:
        """ Display a double array at a specific location with a specific colour """
        new_posx = 0
        new_posy = 0
        new_character = ""
        new_colour = colour
        new_attr = attr
        new_bg = bg
        new_transparent = transparent
        for index, item in enumerate(array):
            for line, character in enumerate(item):
                if "posx" in character:
                    new_posx = character["posx"]+iposx
                else:
                    new_posx = line + iposx
                if "posy" in character:
                    new_posy = character["posy"] + iposy
                else:
                    new_posy = index + iposy
                if "character" in character:
                    new_character = character["character"]
                else:
                    new_character = " "
                if "colour" in character:
                    new_colour = character["colour"]
                else:
                    new_colour = colour
                if "attr" in character:
                    new_attr = character["attr"]
                else:
                    new_attr = attr
                if "bg" in character:
                    new_bg = character["bg"]
                else:
                    new_bg = bg
                if "transparent" in character:
                    new_transparent = character["transparent"]
                else:
                    new_transparent = transparent
                self.my_asciimatics_overlay_main_screen.print_at(
                    new_character,
                    new_posx,
                    new_posy,
                    new_colour,
                    new_attr,
                    new_bg,
                    new_transparent
                )
