import pandas as pd
import numpy as np

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from ticket.codegen import generate_ticket_code
from ticket import qrgen, bargen

class Check:
    def __init__(self, file_json) -> None:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            file_json, ['https://www.googleapis.com/auth/spreadsheets'])
        
        self.client = gspread.authorize(credentials)

    def open(self, url) -> None:
        self.spreadsheet_o = self.client.open_by_url(url)

    def read_to_df(self, sheet: str) -> pd.DataFrame:
        ws = self.spreadsheet_o.worksheet(sheet)
        list_of_dict = ws.get_all_records()

        return pd.DataFrame(list_of_dict)
    
    def check(self, code) -> bool:
        raise NotImplementedError
        
    def _clean(self, df) -> pd.DataFrame:
        raise NotImplementedError
    
    def _export(self):
        raise NotImplementedError
    
class Gen:
    def __init__(self, event_code: str, input_df: pd.DataFrame) -> None:
        """
        DataFrame must includes:
            - id: id of individuals
            - quantity: number of tickets each individual bought
        """
        
        self.df = input_df
        
        # Generate codes and assign code to data
        codes = generate_ticket_code(self.df['quantity'].sum(), seed=event_code)

        # Slicing codes for individuals
        index = self.df['quantity'].cumsum()

        code_list = list()
        start = 0  # Initializing start index

        for stop in index:
            code_cut = codes[start:stop]  # List slicing and append to new list.
            start = stop  # Update new start
            code_list.append(code_cut)

        self.df['codes'] = code_list

    def exploded(self) -> pd.DataFrame:
        exploded_df = self.df[['id', 'codes']].explode('codes', ignore_index=1)
        return exploded_df