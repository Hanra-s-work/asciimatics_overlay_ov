# -*- coding: utf-8 -*-
"""This module defines a datepicker widget"""
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from asciimatics.event import KeyboardEvent, MouseEvent
from asciimatics.exceptions import StopApplication
from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics import widgets as WIG
from asciimatics import effects as EFF
from asciimatics import event as EVE
from asciimatics.widgets.temppopup import _TempPopup
from asciimatics_overlay_ov import AsciimaticsOverlay


class PopupConstants:
    """
    A class containing constants for the Popup class
    """

    def __init__(self) -> None:
        self.unknown_code = -1
        self.regular_item = 0
        self.widget_item = 1
        self.effects_item = 2
        self.success = 0
        self.error = 1
        self.error_item = 84
        self.error_item_arg1_not_an_object = 85
        self.error_item_arg2_not_a_boolean = 86
        self.error_item_arg3_not_a_number = 87
        self.error_item_arg4_not_a_number = 88
        self.error_item_arg5_not_a_string = 89
        self.error_item_arg6_not_a_string = 90
        self.error_item_arg4_number_option_non_existant = 91
        self.error_item_arg5_name_already_taken = 92
        self.error_item_arg6_parent_widget_not_found = 93
        self.error_item_arg6_parent_widget_not_a_layout = 94
        self.human_readable_dict = {
            self.unknown_code: "Error: The code you have provided is not referenced in this error code database",
            self.success: "success",
            self.error: "error",
            self.error_item: "An unknown error has occurred while processing your item",
            self.error_item_arg1_not_an_object: "Error: the provided item in position 1 is not an object",
            self.error_item_arg2_not_a_boolean: "Error: the provided item in position 2 is not a boolean",
            self.error_item_arg3_not_a_number: "Error: the provided item in position 3 is not a number",
            self.error_item_arg4_not_a_number: "Error: the provided item in position 4 is not a whole unsigned number",
            self.error_item_arg5_not_a_string: "Error: the provided item in position 5 is not a string",
            self.error_item_arg6_not_a_string: "Error: the provided item in position 6 is not a string",
            self.error_item_arg4_number_option_non_existant: "Error: the provided item in position 4 is not a valid number option (see description for more information)",
            self.error_item_arg5_name_already_taken: "Error: the provided name in position 5 is already taken",
            self.error_item_arg6_parent_widget_not_found: "Error: the provided parent layout/effect in position 6 was not found",
            self.error_item_arg6_parent_widget_not_a_layout: "Error: the provided parent layout/effect in position 6 is not a layout nor an effect"
        }


class MyPopup(_TempPopup, PopupConstants, AsciimaticsOverlay):
    """
    A class in charge of helping you to create more powerfull pop-up windows
        :param parent: This is the self variable from the class that is calling it
        :param content: The list containing the list of items to place
        :return: None

        How content works:
            * Content is a double array.
            * Each line of the array represents an object of the window
            * The order in which the lines are declared represent the order in which they will be added to the screen

            * This is how a line is defined:
                * :param 1: This is the item you wish to add to your screen
                * :param 2: This is a boolean indicating if the parameter is to be added as a widget (True) or as an effect (False)
                * :param 3: This is an integer indicating where to add the element within the widget grid (if param2 is False, this parameter will need to be specified but won't be used)
                * :param 4: This is an integer indicating if the provided parameter is an item, a widget or an effect
                * :param 5: This is a place where you can provide a name for the item you provide (it is recommended to use it when adding widget/effect instances so that they can be called later on when adding other items)
                * :param 6: This is the place where you can specify the name of the widget/effect you wish to use for the current item ("" or <nothing>: the latest widget/effect used will be used for the item)

            * PS: 
                * For param 4 it is important to specify it when a widget or an effect container is being added
                * Pre-set variables are available for param 4 (call the PopupConstants class for access)
                * The default values are None, True, False, 0:
                    * None: it will act as a comment (the line will not be processed)
                    * True: The current item will be added as a widget
                    * 0: The current item will be added at position 0 of the widget
                    * 0: The current item is a regular item (not a widget, nor an effect)
                    * "": There will be no name assigned to the item, this makes any referencing to this item by this class later on impossible (you will not be able to retreive data from the istance by that method)
                    * "": The latest widget/effect used will be used when adding this item
        Usage example:
            self._place_content(
                [
                    [self.add_label(text="This is a pop-up",height=2,align=self.label_center),True,0,self.regular_item,""],
                    [self.add_button(text="Close",on_click=None),True,0,self.regular_item,"my_close_button"],
                    [self.add_layout(columns=[33, 33, 33],fill_frame=False),True,0,self.widget_item,"my_widget"],
                    [self.add_label(text="Sample Text",height=1,align=self.label_center,name="dummy_test"),True,1,self.regular_item,"my_label_in_my_widget","my_widget"]
                ]
            )
    """

    def __init__(self, parent, data: list[tuple[object | bool | bool | int | str | str]] = None) -> None:
        """
        :param parent: The widget that spawned this pop-up.
        :param year_range: Optional range to limit the year selection to.
        """
        # Construct the Frame
        location = parent.get_location()
        frame_height = 3
        frame_width = 12
        frame_dim = 2
        offset_x = 1  # This move the box of frame_dim + offset_x lines from the original location
        offset_y = -3  # This move the box of frame_dim + offset_y lines from the original location

        posx = location[0] - (frame_dim + offset_x)
        posy = location[1] + (frame_dim + offset_y)
        location = parent.get_location()
        super(PopupConstants, self).__init__()
        super(MyPopup, self).__init__(
            screen=parent.frame.screen,
            parent=parent,
            x=posx,
            y=posy,
            w=frame_width,
            h=frame_height
        )

        # node_tracking
        self.input_node = dict()
        self.layout_node = dict()
        self.effect_node = dict()
        self.latest_input = None
        self.latest_parent_type_is_layout = True

        # item tracking (before being added to the window)
        self.node_function_id = "function"
        self.node_is_widget_id = "is_widget"
        self.node_item_position_id = "item_position"
        self.node_item_type_id = "item_type"
        self.node_name_id = "name"
        self.node_parent_widget_id = "parent_widget"

        # Build the widget to display the time selection.
        self.layouts = dict()
        self.default_main_layout = WIG.Layout([100], fill_frame=True)
        self.input_node["hl_my_popup_container"] = self.default_main_layout
        self.layout_node["hl_my_popup_container"] = self.default_main_layout
        self.latest_parent_type_is_layout = True
        self.latest_input = self.default_main_layout
        self.add_layout(self.default_main_layout)
        if data != None:
            self._place_content(data)
        self.fix()

    def _code_to_human_readable(self, code: int) -> str:
        """ Returns the human readable version of the provided code """
        if code == self.human_readable_dict:
            return self.human_readable_dict[code]
        return self.human_readable_dict[self.unknown_code]

    def _compile_item(self, item: tuple[object | bool | bool | int | str | str]) -> int | dict[str]:
        """ The function in charge of checking the user input and putting it in a structure """
        item_data = {
            self.node_function_id: None,
            self.node_is_widget_id: True,
            self.node_item_position_id: False,
            self.node_item_type_id: 0,
            self.node_name_id: "",
            self.node_parent_widget_id: ""
        }
        if isinstance(item, (tuple, list)) is False:
            return self.error_item
        item_length = len(item)
        if item_length == 0:
            return self.error_item
        if item_length >= 1:
            if callable(item[0]) is True:
                item_data[self.node_function_id] = item[0]
            else:
                return self.error_item_arg1_not_an_object
        if item_length >= 2:
            if isinstance(item_data[1], bool) is True:
                item_data[self.node_is_widget_id] = item_data[1]
            else:
                return self.error_item_arg2_not_a_boolean
        if item_length >= 3:
            if isinstance(item_data[2], int) is True:
                if item_data[2] >= 0:
                    item_data[self.node_item_position_id] = item_data[2]
                else:
                    return self.error_item_arg4_not_a_number
            else:
                return self.error_item_arg3_not_a_number
        if item_length >= 4:
            if isinstance(item_data[3], int) is True:
                item_data[self.node_item_type_id] = item[3]
            else:
                return self.error_item_arg4_not_a_number
        if item_length >= 5:
            if isinstance(item_data[4], str) is True:
                item_data[self.node_name_id] = item[4]
            else:
                return self.error_item_arg5_not_a_string
        if item_length >= 6:
            if isinstance(item_data[5], str) is True:
                item_data[self.node_parent_widget_id] = item[5]
            else:
                return self.error_item_arg6_not_a_string
        return item_data

    def _place_item(self, item: dict[str, object | bool | bool | int | str | str]) -> int:
        """ Same way of functioning as _place_content but working the the line and not the array """
        item_data = {
            self.node_function_id: None,
            self.node_is_widget_id: True,
            self.node_item_position_id: False,
            self.node_item_type_id: 0,
            self.node_name_id: "",
            self.node_parent_widget_id: ""
        }
        parent_type_is_layout = self.latest_parent_type_is_layout
        latest_parent_layout = self.latest_input
        if len(item[self.node_parent_widget_id]) > 0:
            if item[self.node_parent_widget_id] in self.input_node:
                if isinstance(self.input_node[item[self.node_parent_widget_id]], WIG.Layout) is True:
                    latest_parent_layout = self.input_node[item[self.node_parent_widget_id]]
                    parent_type_is_layout = True
                elif isinstance(self.input_node[item[self.node_parent_widget_id]], EFF.Effect) is True:
                    latest_parent_layout = self.input_node[item[self.node_parent_widget_id]]
                    parent_type_is_layout = False
                else:
                    return self.error_item_arg6_parent_widget_not_a_layout
        if item[self.node_name_id] == self.regular_item:
            if parent_type_is_layout is True:
                latest_parent_layout.add_widget()
            else:
                latest_parent_layout.add_effect()
        elif item[self.node_name_id] == self.widget_item:
            if parent_type_is_layout is True:
                latest_parent_layout.add_widget()
            else:
                latest_parent_layout.add_effect()
        elif item[self.node_name_id] == self.effects_item:
            if parent_type_is_layout is True:
                latest_parent_layout.add_widget()
            else:
                latest_parent_layout.add_effect()
        else:
            return self.error_item_arg4_number_option_non_existant
        if len(item[self.node_name_id]) > 0:
            if item[self.node_name_id] not in self.input_node:
                self.input_node[item[self.node_name_id]] = item_data
                if item[self.node_item_type_id] == self.widget_item:
                    self.layout_node[item[self.node_name_id]] = item_data
                    self.latest_parent_type_is_layout = True
                if item[self.node_item_type_id] == self.effects_item:
                    self.effect_node[item[self.node_name_id]] = item_data
                    self.latest_parent_type_is_layout = False
            else:
                return self.error_item_arg5_name_already_taken

    def _place_content(self, content: list[tuple[object | bool | bool | int | str | str]]) -> None:
        """
        Place the content on the screen based on the the provided list of items
        :param content: The list containing the list of items to place
        :return: None

        How content works:
            * Content is a double array.
            * Each line of the array represents an object of the window
            * The order in which the lines are declared represent the order in which they will be added to the screen

            * This is how a line is defined:
                * :param 1: This is the item you wish to add to your screen
                * :param 2: This is a boolean indicating if the parameter is to be added as a widget (True) or as an effect (False)
                * :param 3: This is an integer indicating where to add the element within the widget grid (if param2 is False, this parameter will need to be specified but won't be used)
                * :param 4: This is an integer indicating if the provided parameter is an item, a widget or an effect
                * :param 5: This is a place where you can provide a name for the item you provide (it is recommended to use it when adding widget/effect instances so that they can be called later on when adding other items)
                * :param 6: This is the place where you can specify the name of the widget/effect you wish to use for the current item ("" or <nothing>: the latest widget/effect used will be used for the item)

            * PS: 
                * For param 4 it is important to specify it when a widget or an effect container is being added
                * Pre-set variables are available for param 4 (call the PopupConstants class for access)
                * The default values are None, True, False, 0:
                    * None: it will act as a comment (the line will not be processed)
                    * True: The current item will be added as a widget
                    * 0: The current item will be added at position 0 of the widget
                    * 0: The current item is a regular item (not a widget, nor an effect)
                    * "": There will be no name assigned to the item, this makes any referencing to this item by this class later on impossible (you will not be able to retreive data from the istance by that method)
                    * "": The latest widget/effect used will be used when adding this item
        Usage example:
            self._place_content(
                [
                    [self.add_label(text="This is a pop-up",height=2,align=self.label_center),True,0,self.regular_item,""],
                    [self.add_button(text="Close",on_click=None),True,0,self.regular_item,"my_close_button"],
                    [self.add_layout(columns=[33, 33, 33],fill_frame=False),True,0,self.widget_item,"my_widget"],
                    [self.add_label(text="Sample Text",height=1,align=self.label_center,name="dummy_test"),True,1,self.regular_item,"my_label_in_my_widget","my_widget"]
                ]
            )
        """
        for index, line in enumerate(content):
            response = self._compile_item(line)
            if isinstance(response, int) is True:
                current_code = self._code_to_human_readable(response)
                print(
                    f"Error: line n°{index}, '{current_code}' for {str(line)}"
                )
                continue
            status = self._place_item(response)
            if status != self.success:
                current_code = self._code_to_human_readable(status)
                print(
                    f"Error: line n°{index}, '{current_code}' for {str(line)}"
                )
                continue

    def _on_close(self, cancelled: bool):
        print(f"cancelled = {cancelled}")


class DatePicker(WIG.Widget, AsciimaticsOverlay, PopupConstants):
    """
    A DatePicker widget allows you to pick a date from a compact, temporary, pop-up Frame.
    """

    def __init__(self, screen: Screen, my_name: str = "Test class capsule", my_disabled: bool = False):
        """
        :param label: An optional label for the widget.
        :param name: The name for the widget.
        :param on_change: Optional function to call when the selected time changes.

        Also see the common keyword arguments in :py:obj:`.Widget`.
        """
        super(DatePicker, self).__init__(
            name=my_name,
            tab_stop=True,
            disabled=my_disabled,
            on_focus=None,
            on_blur=None
        )
        self.screen = screen
        self._value = "ee"
        self._child = None
        self.event = EVE.Event()
        self.ao = AsciimaticsOverlay(self.event, self.screen)

    def update(self, frame_no):
        self._draw_label()

        # This widget only ever needs display the current selection - the separate Frame does all
        # the clever stuff when it has the focus.
        (colour, attr, background) = self._pick_colours("edit_text")
        self._frame.canvas.print_at(
            self._value,
            self._x + self._offset,
            self._y,
            colour, attr, background)

    def reset(self): pass

    def process_event(self, event):
        if event is not None:
            if isinstance(event, KeyboardEvent):
                if event.key_code in [Screen.ctrl("M"), Screen.ctrl("J"), ord(" ")]:
                    event = None
            elif isinstance(event, MouseEvent):
                if event.buttons != 0:
                    if self.is_mouse_over(event, include_label=False):
                        event = None
            if event is None:
                input_data = [
                    [
                        self.add_label(
                            text="This is a pop-up",
                            height=2,
                            align=self.label_center
                        ),
                        True,
                        0,
                        self.regular_item,
                        ""
                    ],
                    [
                        self.add_button(
                            text="Close",
                            on_click=None
                        ),
                        True,
                        0,
                        self.regular_item,
                        "my_close_button"
                    ],
                    [
                        self.add_layout(
                            columns=[33, 33, 33],
                            fill_frame=False
                        ),
                        True,
                        0,
                        self.widget_item,
                        "my_widget"
                    ],
                    [
                        self.add_label(
                            text="Sample Text",
                            height=1,
                            align=self.label_center,
                            name="dummy_test"
                        ),
                        True,
                        1,
                        self.regular_item,
                        "my_label_in_my_widget",
                        "my_widget"
                    ]
                ]
                self._child = MyPopup(self, input_data)
                self.frame.scene.add_effect(self._child)

        return event

    def required_height(self, offset, width):
        return 1

    @property
    def value(self):
        """
        The current selected date.
        """
        return self._value

    @value.setter
    def value(self, new_value):
        # Only trigger the notification after we've changed the value.
        old_value = self._value
        self._value = new_value
        if old_value != self._value and self._on_change:
            self._on_change()


class dummy(WIG.Frame):
    def __init__(self, screen: Screen):
        super(dummy, self).__init__(
            screen,
            height=screen.height,
            width=screen.width,
            has_border=True,
            name="Main Scene",
            hover_focus=True,
            has_shadow=True,
            x=0,
            y=0,
            is_modal=False,
            can_scroll=True
        )
        self.layout = WIG.Layout([100], fill_frame=False)
        self.add_layout(self.layout)
        self.layout.add_widget(
            WIG.Label(label="This is a pop-up")
        )
        self.layout.add_widget(DatePicker(
            label="data"
        ))
        self.layout.add_widget(
            WIG.Button("Close", on_click=self._exit)
        )
        self.fix()

    def _exit(self):
        raise StopApplication("User pressed close")


def demo(screen: Screen):
    """ The function in charge of booting up the display """
    scenes = [
        Scene([dummy(screen)], -1, name="Main")
    ]
    screen.play(
        scenes,
        stop_on_resize=True,
        start_scene=None,
        allow_int=True
    )


Screen.wrapper(demo)
