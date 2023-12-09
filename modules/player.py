from streamlit_elements import media, mui, sync, lazy
from .dashboard import Dashboard

# The Player class is a media player that allows users to input a URL and play the corresponding media.
class Player(Dashboard.Item):

    def __init__(self, *args, **kwargs):
        """
        The function initializes an object with a URL attribute set to "https://www.youtube.com/watch?v=CmSKVW1v0xM".
        """
        super().__init__(*args, **kwargs)
        self._url = "https://www.youtube.com/watch?v=CmSKVW1v0xM"

    def _set_url(self, event):
        """
        The function sets the value of the `_url` attribute to the value of the `event.target.value`.

        :param event: The event parameter is an object that represents the event that triggered the function. It contains
        information about the event, such as the target element that triggered the event and the value of the target
        element. In this case, the event object is expected to have a target property, which is an object representing the
        """
        self._url = event.target.value

    def __call__(self, urlset=None,desc=None,title='Media player'):
        with mui.Paper(key=self._key, sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=1):
            with self.title_bar(padding="10px 15px 10px 15px", dark_switcher=False):
                mui.icon.OndemandVideo()
                mui.Typography(title)
            if urlset:
                self._url = urlset
                if desc and  desc != '':
                    mui.Typography(desc)
            else:
                with mui.Stack(direction="row", spacing=2, justifyContent="space-evenly", alignItems="center", sx={"padding": "10px"}):
                    mui.TextField(defaultValue=self._url, label="URL", variant="standard", sx={"flex": 0.97}, onChange=lazy(self._set_url))
                    mui.IconButton(mui.icon.PlayCircleFilled, onClick=sync(), sx={"color": "primary.main"})

            if self._url == 'patrick':
                self._url = 'https://www.youtube.com/watch?v=DtL_giO-EB8&pp=ygUaZmx5IG1lIHRvIHRoZSBtb29uIHBhdHJpY2s%3D'



            media.Player(self._url, controls=True, width="100%", height="100%")
