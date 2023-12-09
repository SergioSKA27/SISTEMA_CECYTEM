from streamlit_elements import mui
from .dashboard import Dashboard


# The `Card` class represents a card component with a title, subheader, image, content, and action buttons.
class Card(Dashboard.Item):

    DEFAULT_CONTENT = (
        "This impressive paella is a perfect party dish and a fun meal to cook "
        "together with your guests. Add 1 cup of frozen peas along with the mussels, "
        "if you like."
    )

    def __call__(self, content,img,title='Card',subheader='September 14, 2016',avatar='R'):
        """
        The function creates a card component with a title, subheader, image, content, and action buttons.

        :param content: The `content` parameter is the text or content that will be displayed in the `CardContent` component
        of the card
        """
        with mui.Card(key=self._key, sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=1):
            mui.CardHeader(
                title=title,
                subheader=subheader,
                avatar=mui.Avatar(avatar, sx={"bgcolor": "red"}),
                action=mui.IconButton(mui.icon.MoreVert),
                className=self._draggable_class,
            )
            mui.CardMedia(
                component="img",
                height=194,
                image=img,
                alt="Paella dish",
            )

            with mui.CardContent(sx={"flex": 1}):
                mui.Typography(content)

            with mui.CardActions(disableSpacing=True):
                mui.IconButton(mui.icon.Favorite)
                mui.IconButton(mui.icon.Share)
