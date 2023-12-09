import json

from streamlit_elements import mui
from .dashboard import Dashboard


# The `DataGrid` class is a component that displays a grid of data with editable cells and pagination.
class DataGrid(Dashboard.Item):

    DEFAULT_COLUMNS = [
        { "field": 'id', "headerName": 'ID', "width": 90 },
        { "field": 'firstName', "headerName": 'First name', "width": 150, "editable": True, },
        { "field": 'lastName', "headerName": 'Last name', "width": 150, "editable": True, },
        { "field": 'age', "headerName": 'Age', "type": 'number', "width": 110, "editable": True, },
    ]
    DEFAULT_ROWS = [
        { "id": 1, "lastName": 'Snow', "firstName": 'Jon', "age": 35 },
        { "id": 2, "lastName": 'Lannister', "firstName": 'Cersei', "age": 42 },
        { "id": 3, "lastName": 'Lannister', "firstName": 'Jaime', "age": 45 },
        { "id": 4, "lastName": 'Stark', "firstName": 'Arya', "age": 16 },
        { "id": 5, "lastName": 'Targaryen', "firstName": 'Daenerys', "age": None },
        { "id": 6, "lastName": 'Melisandre', "firstName": None, "age": 150 },
        { "id": 7, "lastName": 'Clifford', "firstName": 'Ferrara', "age": 44 },
        { "id": 8, "lastName": 'Frances', "firstName": 'Rossini', "age": 36 },
        { "id": 9, "lastName": 'Roxie', "firstName": 'Harvey', "age": 65 },
    ]

    def _handle_edit(self, params):
        """
        The function _handle_edit takes in a parameter called params and prints its value.

        :param params: The `params` parameter is a dictionary that contains key-value pairs of parameters
        """
        print(params)

    def __call__(self, json_data,colums,title='Data grid'):
        """
        The function takes in JSON data, parses it, and displays it in a data grid with specific settings and options.

        :param json_data: The `json_data` parameter is a string containing JSON data. It is used to populate the rows of the
        `DataGrid` component
        """
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            data = self.DEFAULT_ROWS

        with mui.Paper(key=self._key, sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=1):
            with self.title_bar(padding="10px 15px 10px 15px", dark_switcher=False):
                mui.icon.ViewCompact()
                mui.Typography(title)

            with mui.Box(sx={"flex": 1, "minHeight": 0}):
                mui.DataGrid(
                    columns=colums,
                    rows=data,
                    pageSize=5,
                    rowsPerPageOptions=[5],
                    checkboxSelection=True,
                    disableSelectionOnClick=True,
                    onCellEditCommit=self._handle_edit,
                )
