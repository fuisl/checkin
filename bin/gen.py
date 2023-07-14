import pandas as pd
from ticket.codegen import generate_ticket_code
from ticket import qrgen, bargen


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