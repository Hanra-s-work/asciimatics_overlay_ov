from time import sleep
import asciimatics.widgets as WIG
from asciimatics.event import Event
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.effects import Print
from asciimatics.renderers import FigletText
# from asciimatics.widgets.temppopup import _TempPopup
from asciimatics.exceptions import StopApplication
# from asciimatics_overlay_ov import AsciimaticsOverlay


class MyOverlayScene(WIG.Frame):  # _TempPopup):
    """ The class in charge of simulating a pop-up """

    def __init__(self, screen: Screen, parent):
        super(MyOverlayScene, self).__init__(
            # on_load: Any | None = None,
            screen=screen,
            x=screen.width//4,
            y=screen.height//4,
            title="A Popup",
            has_border=True,
            has_shadow=True,
            can_scroll=True,
            hover_focus=True,
            width=screen.width//2,
            height=screen.height//2
        )
        self.parent = parent
        # self.ao = AsciimaticsOverlay(parent.event, screen)
        # self.ao.update_initial_pointers(
        #     parent.event,
        #     screen,
        #     success=0,
        #     error=1
        # )
        self.layout = WIG.Layout([100], fill_frame=False)
        self.add_layout(self.layout)
        self.layout.add_widget(
            # self.ao.add_label(
            #     text="This is a pop-up",
            #     height=2,
            #     align=self.ao.label_center,
            #     name=None
            # )
            WIG.Label(label="This is a pop-up")
        )
        self.layout.add_widget(
            # self.ao.add_button(
            #     text="Close",
            #     on_click=self.screen.close
            # )
            WIG.Button("Close", on_click=self.screen.close)
        )
        print("Fixing screen")
        self.fix()
        print("Screen fixed")
        # sleep(2)

    def _on_close(self, cancelled):
        print(f"closing, cancelled = {cancelled}")


class MainScene(WIG.Frame):  # , AsciimaticsOverlay):
    """ The class in charge of simulating the main window that will have a child one displayed over it """

    def __init__(self, screen: Screen):
        super(MainScene, self).__init__(
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
        self.event = Event()
        # self.ao = AsciimaticsOverlay(
        #     self.event,
        #     self.screen,
        #     success=0,
        #     error=1
        # )
        self.layout = WIG.Layout([1, 1, 1], fill_frame=True)
        self.add_layout(self.layout)
        self.add_effect(
            Print(
                screen,
                FigletText(
                    "Main Scene",
                    font='big'
                ),
                y=10,
                x=0,
                speed=1,
                transparent=False
            )
        )

        self.layout.add_widget(
            # self.add_button(
            #     text="Open Pop-UP",
            #     on_click=self._run_popup,
            #     label=None,
            #     box=True,
            #     name=None
            # )
            WIG.Button("Open Pop-UP", on_click=self._run_popup)
        )
        self.layout.add_widget(
            # self.add_button(
            #     text="Exit",
            #     on_click=self._exit,
            #     label=None,
            #     box=True,
            #     name=None
            # )
            WIG.Button("Exit", on_click=self._exit)
        )
        self.fix()

    def _run_popup(self) -> None:
        pop_up_scene = MyOverlayScene(self.screen, self)
        self.add_effect(pop_up_scene)
        sleep(2)
        print(f"pop_up_scene = {pop_up_scene}")

    def _exit(self) -> None:
        raise StopApplication("User pressed quit")


def demo(screen: Screen):
    """ The function in charge of booting up the display """
    scenes = [
        Scene([MainScene(screen)], -1, name="Main")
    ]
    screen.play(
        scenes,
        stop_on_resize=True,
        start_scene=None,
        allow_int=True
    )


Screen.wrapper(demo)
