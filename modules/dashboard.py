from uuid import uuid4
from abc import ABC, abstractmethod
from streamlit_elements import dashboard, mui
from contextlib import contextmanager


# The `Dashboard` class is a Python class that represents a draggable dashboard with items that can be added and
# customized.
class Dashboard:

    DRAGGABLE_CLASS = "draggable"

    def __init__(self):
        """
        The function initializes an empty list called "_layout".
        """
        self._layout = []

    def _register(self, item):
        """
        The function appends an item to a layout.

        :param item: The "item" parameter is the object that you want to register. It will be appended to the "_layout" list
        attribute of the object
        """
        self._layout.append(item)

    @contextmanager
    def __call__(self, **props):
        """
        The function sets a draggable handle for a grid layout in a dashboard.
        """
        # Draggable classname query selector.
        props["draggableHandle"] = f".{Dashboard.DRAGGABLE_CLASS}"

        def on_change(event):
            self._layout =  event

        with dashboard.Grid(self._layout,onLayoutChange=on_change, **props):
            yield

    def __repr__(self) -> list:
        """
        The function returns the string representation of the object.
        """
        return self._layout

    def __str__(self) -> str:
        """
        The function returns the string representation of the object.
        """
        return f"<Dashboard: {self._layout}>"

    def layout(self):
        return self._layout

    # The above class is an abstract base class for creating items in a dashboard, with methods for switching themes and
    # displaying a title bar.
    class Item(ABC):

        def __init__(self, board, x, y, w, h, **item_props):
            """
            The function initializes a draggable item on a dashboard board with specified properties.

            :param board: The `board` parameter is an instance of a class that represents a dashboard or a board where items
            can be placed. It is used to register the item created with the `Dashboard` class
            :param x: The x parameter represents the x-coordinate of the top-left corner of the item on the dashboard
            :param y: The parameter "y" represents the y-coordinate of the top-left corner of the item on the dashboard
            :param w: The parameter "w" represents the width of the item on the dashboard
            :param h: The parameter "h" represents the height of the item on the dashboard
            """
            self._key = str(uuid4())
            self._draggable_class = Dashboard.DRAGGABLE_CLASS
            self._dark_mode = True
            board._register(dashboard.Item(self._key, x, y, w, h, **item_props))

        def _switch_theme(self):
            """
            The function toggles the dark mode on and off.
            """
            self._dark_mode = not self._dark_mode

        @contextmanager
        def title_bar(self, padding="5px 15px 5px 15px", dark_switcher=True):
            """
            The `title_bar` function generates a title bar with optional dark mode switcher functionality.

            :param padding: The `padding` parameter specifies the padding around the title bar. It is set to "5px 15px 5px
            15px", which means there is 5 pixels of padding on the top and bottom, and 15 pixels of padding on the left and
            right, defaults to 5px 15px 5px 15px (optional)
            :param dark_switcher: The `dark_switcher` parameter is a boolean value that determines whether or not to display
            a switcher button for toggling between dark and light mode. If `dark_switcher` is set to `True`, the switcher
            button will be displayed. If it is set to `False`, the, defaults to True (optional)
            """
            with mui.Stack(
                className=self._draggable_class,
                alignItems="center",
                direction="row",
                spacing=1,
                sx={
                    "padding": padding,
                    "borderBottom": 1,
                    "borderColor": "divider",
                },
            ):
                yield

                if dark_switcher:
                    if self._dark_mode:
                        mui.IconButton(mui.icon.DarkMode, onClick=self._switch_theme)
                    else:
                        mui.IconButton(mui.icon.LightMode, sx={"color": "#ffc107"}, onClick=self._switch_theme)

        @abstractmethod
        def __call__(self):
            """
            The function is a placeholder that raises a NotImplementedError when called.
            """
            """Show elements."""
            raise NotImplementedError
