from .test_menu_input import Main
from .frame_nodes import FrameNodes

if __name__ == "__main__":
    SUCCESS = 0
    ERROR = 1
    SCREEN = None
    LAST_SCENE = None
    MI = Main(
        success=SUCCESS,
        error=ERROR,
        screen=SCREEN,
        last_scene=LAST_SCENE
    )
    MI.run()
