from typing import Any
from ticket.codegen import generate_ticket_code
from ticket import qrgen, bargen

class Gen:
    def __init__(self, event_code=None) -> None:
        """
        Initialize Generator object.
        """
        if event_code == None:  # set event_code if None
            self.event_code = 'default'
        else:
            self.event_code = event_code

        self.codes = []  # list of codes

    def gen(self, quantity=10, length=6) -> list:
        """
        Initialize and return a list of n number of code.
        """
        self.codes = generate_ticket_code(quantity, length=length, seed=self.event_code)
        
        return self.codes
    
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
            qrgen.render(codes, custom_path, transparent)
        elif type == 'bar':
            bargen.render(codes, custom_path, transparent)