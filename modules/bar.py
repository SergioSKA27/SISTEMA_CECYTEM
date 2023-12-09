from streamlit_elements import mui, nivo
from .dashboard import Dashboard
import json


class Bar(Dashboard.Item):

    DEFAULT_DATA = [
        {
            "country": "AD",
            "hot dog": 113,
            "hot dogColor": "hsl(297, 70%, 50%)",
            "burger": 47,
            "burgerColor": "hsl(253, 70%, 50%)",
            "sandwich": 127,
            "sandwichColor": "hsl(345, 70%, 50%)",
            "kebab": 153,
            "kebabColor": "hsl(164, 70%, 50%)",
            "fries": 79,
            "friesColor": "hsl(342, 70%, 50%)",
            "donut": 7,
            "donutColor": "hsl(314, 70%, 50%)"
          },
          {
            "country": "AE",
            "hot dog": 32,
            "hot dogColor": "hsl(148, 70%, 50%)",
            "burger": 147,
            "burgerColor": "hsl(94, 70%, 50%)",
            "sandwich": 28,
            "sandwichColor": "hsl(100, 70%, 50%)",
            "kebab": 106,
            "kebabColor": "hsl(1, 70%, 50%)",
            "fries": 68,
            "friesColor": "hsl(331, 70%, 50%)",
            "donut": 13,
            "donutColor": "hsl(354, 70%, 50%)"
          },
          {
            "country": "AF",
            "hot dog": 110,
            "hot dogColor": "hsl(157, 70%, 50%)",
            "burger": 91,
            "burgerColor": "hsl(259, 70%, 50%)",
            "sandwich": 23,
            "sandwichColor": "hsl(299, 70%, 50%)",
            "kebab": 40,
            "kebabColor": "hsl(156, 70%, 50%)",
            "fries": 150,
            "friesColor": "hsl(173, 70%, 50%)",
            "donut": 74,
            "donutColor": "hsl(178, 70%, 50%)"
          },
          {
            "country": "AG",
            "hot dog": 142,
            "hot dogColor": "hsl(94, 70%, 50%)",
            "burger": 16,
            "burgerColor": "hsl(360, 70%, 50%)",
            "sandwich": 95,
            "sandwichColor": "hsl(236, 70%, 50%)",
            "kebab": 91,
            "kebabColor": "hsl(157, 70%, 50%)",
            "fries": 152,
            "friesColor": "hsl(219, 70%, 50%)",
            "donut": 97,
            "donutColor": "hsl(62, 70%, 50%)"
          },
          {
            "country": "AI",
            "hot dog": 58,
            "hot dogColor": "hsl(98, 70%, 50%)",
            "burger": 90,
            "burgerColor": "hsl(205, 70%, 50%)",
            "sandwich": 15,
            "sandwichColor": "hsl(50, 70%, 50%)",
            "kebab": 102,
            "kebabColor": "hsl(263, 70%, 50%)",
            "fries": 11,
            "friesColor": "hsl(249, 70%, 50%)",
            "donut": 3,
            "donutColor": "hsl(150, 70%, 50%)"
          },
          {
            "country": "AL",
            "hot dog": 114,
            "hot dogColor": "hsl(168, 70%, 50%)",
            "burger": 11,
            "burgerColor": "hsl(92, 70%, 50%)",
            "sandwich": 49,
            "sandwichColor": "hsl(146, 70%, 50%)",
            "kebab": 48,
            "kebabColor": "hsl(82, 70%, 50%)",
            "fries": 2,
            "friesColor": "hsl(274, 70%, 50%)",
            "donut": 143,
            "donutColor": "hsl(137, 70%, 50%)"
          },
          {
            "country": "AM",
            "hot dog": 191,
            "hot dogColor": "hsl(10, 70%, 50%)",
            "burger": 64,
            "burgerColor": "hsl(3, 70%, 50%)",
            "sandwich": 78,
            "sandwichColor": "hsl(17, 70%, 50%)",
            "kebab": 87,
            "kebabColor": "hsl(297, 70%, 50%)",
            "fries": 14,
            "friesColor": "hsl(123, 70%, 50%)",
            "donut": 67,
            "donutColor": "hsl(81, 70%, 50%)"
          }
            ]


    def __init__(self, *args, **kwargs):
        """
        The function initializes a dictionary containing two themes, "dark" and "light", with corresponding color values for
        background, text, and tooltip.
        """
        super().__init__(*args, **kwargs)
        self._theme = {
            "dark": {
                "background": "#252526",
                "textColor": "#FAFAFA",
                "tooltip": {
                    "container": {
                        "background": "#3F3F3F",
                        "color": "FAFAFA",
                    }
                }
            },
            "light": {
                "background": "#FFFFFF",
                "textColor": "#31333F",
                "tooltip": {
                    "container": {
                        "background": "#FFFFFF",
                        "color": "#31333F",
                    }
                }
            }
        }

    def __call__(self, json_data):
        """
        The function takes in JSON data, parses it, and then generates a radar chart using the Nivo library.

        :param json_data: The `json_data` parameter is a string containing JSON data. It is used to load the data for the
        radar chart
        """
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            data = self.DEFAULT_DATA

        with mui.Paper(key=self._key, sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=1):
            with self.title_bar():
                mui.icon.Radar()
                mui.Typography("Radar chart", sx={"flex": 1})

            with mui.Box(sx={"flex": 1, "minHeight": 0}):
                nivo.Bar(
                data=data,
                theme=self._theme["dark" if self._dark_mode else "light"],
                indexBy="country",
                keys=["hot dog", "burger", "sandwich", "kebab", "fries", "donut"],



                )







