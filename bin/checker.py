import pandas as pd
import numpy as np

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from ticket.codegen import generate_ticket_code
from ticket import qrgen, bargen

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

    def get_info(self, code) -> pd.DataFrame:
        """
        Print 
        """
        if self.check(code):
            temp = self.df_input[self.df[self.df['codes'] == code]['id']]
            print(temp)
            return temp

class Gen:
    def __init__(self, df_input: pd.DataFrame, event_code) -> None:
        """
        DataFrame must includes:
            - id: id of individuals
            - quantity: number of tickets each individual bought
        """
        
        self.df = df_input
        
        # Generate codes and assign code to data
        self.codes = generate_ticket_code(self.df['quantity'].sum(), seed=event_code)

        # Slicing codes for individuals
        index = self.df['quantity'].cumsum()

        code_list = list()
        start = 0  # Initializing start index

        for stop in index:
            code_cut = self.codes[start:stop]  # List slicing and append to new list.
            start = stop  # Update new start
            code_list.append(code_cut)

        self.df['codes'] = code_list

    def _exploded(self) -> pd.DataFrame:
        exploded_df = self.df[['id', 'codes']].explode('codes', ignore_index=1)
        return exploded_df
    
    def set(self, **kwargs):
        """
        set methods to change some settings
        """
        pass

    def encode(self, type='qr', transparent=False, custom_path=None):
        """
        Encode codes into QRCode/Barcode.

        Parameters:
        :type -> qr or bar.
        :transparent -> settings for transparent background.
        :custom_path -> path folder to export encoded files.
        """
        # Set path if not provided
        if custom_path == None:
            custom_path = './qrcodes/' if type=='qr' else './barcodes/'
        
        # Call generator
        if type == 'qr':
            qrgen.gen(self.codes, custom_path, transparent)  # TODO: restructure qrgen for transparent option
        elif type == 'bar':
            bargen.gen(self.codes, custom_path, transparent)  # TODO: restructure bargen for transparent option