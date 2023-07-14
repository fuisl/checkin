import pandas as pd
import numpy as np

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from gen import Gen

class CheckIn:
    def __init__(self, file:str, url=None, sheet=None, event_code='presto') -> None:
        """
        Check for code in database

        (1) Open database (GSheet or .csv)
            - If using GSheet as database, you need to provide url and sheet.
        (2) Use `check()` method to check if a code is in database
        """
        
        if file.lower().endswith('.json'):
            # Connect to Google Sheet API
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                file, ['https://www.googleapis.com/auth/spreadsheets'])
            self.client = gspread.authorize(credentials)
            
            self.spreadsheet_o = self.client.open_by_url(url)
            ws = self.spreadsheet_o.worksheet(sheet)
            
            # Set df_input
            list_of_dict = ws.get_all_records()
            self.df_input = pd.DataFrame(list_of_dict)


        elif file.lower().endswith('.csv'):
            self.df_input = pd.read_csv(file)

        # Dataframe use for checking
        self.df = self._add_code(self.df_input, event_code)
    
    def check(self, code: str) -> bool:
        if code in self.df['codes'].values:
            return True
        
        return False
    
    def _add_code(self, df_input, event_code) -> pd.DataFrame:
        generator = Gen(df_input, event_code)

        return generator._exploded()
    
    def _export(self):
        raise NotImplementedError
    
    def _is_used() -> bool:
        raise NotImplementedError

    def get_info(self, code) -> pd.DataFrame:
        """
        Print info
        """
        if self.check(code):
            temp = self.df[self.df['codes'].apply(lambda x: code in x)]['id'].to_list()
            info = self.df_input[self.df_input['id'] == temp[0]]
            return info