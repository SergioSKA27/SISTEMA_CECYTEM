from functools import partial
from streamlit_elements import mui, editor, sync, lazy
from .dashboard import Dashboard


# The `Editor` class is a subclass of `Dashboard.Item` that represents an editor component with multiple tabs and the
# ability to switch between them, update their content, and apply changes.
class Editor(Dashboard.Item):

    def __init__(self, *args, **kwargs):
        """
        The function initializes various attributes for a coding assistant with a default theme and styling.
        """
        super().__init__(*args, **kwargs)

        self._dark_theme = False
        self._index = 0
        self._tabs = {}
        self._editor_box_style = {
            "flex": 1,
            "minHeight": 0,
            "borderBottom": 1,
            "borderTop": 1,
            "borderColor": "divider"
        }

    def _change_tab(self, _, index):
        """
        The function changes the value of the index attribute in the class.

        :param _: The underscore (_) is a convention in Python to indicate that a parameter is not going to be used in the
        function. It is often used as a placeholder when the parameter is required by the function signature but not
        actually needed within the function body
        :param index: The `index` parameter represents the new index value that you want to set for the `_index` attribute
        """
        self._index = index

    def update_content(self, label, content):
        """
        The function updates the content of a specific tab in a GUI.

        :param label: The label parameter is a string that represents the label of the tab whose content you want to update
        :param content: The "content" parameter is the new content that you want to update for a specific label in the tabs
        """
        self._tabs[label]["content"] = content

    def add_tab(self, label, default_content, language):
        """
        The function `add_tab` adds a new tab to a dictionary with a given label, default content, and language.

        :param label: The label parameter is a string that represents the label or name of the tab
        :param default_content: The default content parameter is the initial content that will be displayed in the tab
        :param language: The "language" parameter is used to specify the programming language of the content in the tab. It
        can be any string that represents a programming language, such as "Python", "JavaScript", "Java", etc
        """
        self._tabs[label] = {
            "content": default_content,
            "language": language
        }

    def get_content(self, label):
        """
        The function `get_content` returns the content associated with a given label in a dictionary.

        :param label: The `label` parameter is a string that represents the label of a tab
        :return: The content associated with the given label in the `_tabs` dictionary.
        """
        return self._tabs[label]["content"]

    def __call__(self):
        """
        The function creates a graphical editor with multiple tabs and a button to apply changes or a keyboard shortcut to
        save.
        """
        with mui.Paper(key=self._key, sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=1):

            with self.title_bar("0px 15px 0px 15px"):
                mui.icon.Terminal()
                mui.Typography("Editor")

                with mui.Tabs(value=self._index, onChange=self._change_tab, scrollButtons=True, variant="scrollable", sx={"flex": 1}):
                    for label in self._tabs.keys():
                        mui.Tab(label=label)

            for index, (label, tab) in enumerate(self._tabs.items()):
                with mui.Box(sx=self._editor_box_style, hidden=(index != self._index)):
                    editor.Monaco(
                        css={"padding": "0 2px 0 2px"},
                        defaultValue=tab["content"],
                        language=tab["language"],
                        onChange=lazy(partial(self.update_content, label)),
                        theme="vs-dark" if self._dark_mode else "light",
                        path=label,
                        options={
                            "wordWrap": True
                        }
                    )

            with mui.Stack(direction="row", spacing=2, alignItems="center", sx={"padding": "10px"}):
                mui.Button("Apply", variant="contained", onClick=sync())
                mui.Typography("Or press ctrl+s", sx={"flex": 1})
