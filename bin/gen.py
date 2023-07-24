import pandas as pd
from ticket.codegen import generate_ticket_code
from ticket import bargen, qrgen

class GenDecorator:
    def encode(self, type='qr', transparent=False, custom_path=None):
        """
        Encode codes into QRCode/Barcode.

        Parameters:
        :type: qr or bar.
        :transparent: settings for transparent background.
        :custom_path: path folder to export encoded files.
        """
        # Set path if not provided
        if custom_path == None:
            custom_path = './qrcodes/' if type=='qr' else './barcodes/'
        
        # Call generator
        if type == 'qr':
            qrgen.gen(self.codes, custom_path, transparent)
        elif type == 'bar':
            bargen.gen(self.codes, custom_path, transparent)

@GenDecorator
class Gen:
    def __init__(self, df_input: pd.DataFrame, event_code=None) -> None:
        """
        Initialize Generator object.
        """
        if event_code == None:  # set event_code if None
            self.event_code = 'default'

        self.df = df_input
        self.codes = []

    def gen(self, n:int) -> list:
        """
        Initialize and return a list of n number of code.
        """
        # Generate codes and assign code to self.codes
        self.codes = generate_ticket_code(n, seed=self.event_code)

        return self.codes

    def cut(self, n):
        """
        Slice n code(s) and return new list
        """
        raise NotImplementedError