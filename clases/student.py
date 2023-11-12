import numpy as np
import pandas as pd
from xata.client import XataClient
class Students:
    def __init__(self,**kwargs) -> None:
        self.__dict__.update(kwargs)

    def __repr__(self) -> dict:
        pass

    def add_info(self,**kwargs):
        self.__dict__.update(kwargs)


    def send_to_db(self):
        pass

    def get_from_db(self,qry,**kwargs):
        pass
