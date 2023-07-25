from typing import Any
import pandas as pd
from ticket.codegen import generate_ticket_code
from ticket import qrgen, bargen

class Gen:
    def __init__(self, event_code=None) -> None:
        """
        Initialize Generator object.
        """
        if event_code == None:  # set event_code if None
            self.event_code = 'default'

        # self.df = df_input
        self.codes = []

    def gen(self, ticket_info: dict, n:int=1) -> list:
        """
        Initialize and return a list of n number of code.
        """
        # Generate codes and assign code to self.codes
        self.codes = generate_ticket_code(ticket_info, n, seed=self.event_code)

        return self.codes

    def cut(self, n=1):
        """
        Slice n code(s) and return new list
        """
        raise NotImplementedError
    
    def encode(self, codes=None, type='qr', transparent=False, custom_path=None):
        """
        Encode codes into QRCode/Barcode.

        Parameters:
        :type: qr or bar.
        :transparent: settings for transparent background.
        :custom_path: path folder to export encoded files.
        """
        # Set path if not provided
        if custom_path == None:
            custom_path = './qrcodes' if type=='qr' else './barcodes'
        
        if codes == None:
            codes = self.codes
        # Call generator
        if type == 'qr':
            qrgen.gen(codes, custom_path, transparent)
        elif type == 'bar':
            bargen.gen(codes, custom_path, transparent)