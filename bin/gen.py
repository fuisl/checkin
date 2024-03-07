from typing import Any
from ticket.codegen import generate_ticket_code
from ticket import qrgen, bargen

class Gen:
    def __init__(self, event_code=None) -> None:
        """
        Initialize Generator object.

        Parameters:
        :event_code: code for the event. This serves as seed for the code generator.
        """
        if event_code == None:  # set event_code if None
            self.event_code = 'default'
        else:
            self.event_code = event_code

        self.codes = []  # empty list of codes

    def gen(self, quantity=10, length=6) -> list:
        """
        Initialize and return a list of n number of code.

        Parameters:
        :quantity: number of codes to generate.
        :length: length of each code.
        """
        self.codes = generate_ticket_code(quantity, length=length, seed=self.event_code)
        
        return self.codes
    
    def encode(self, codes=None, type='qr', transparent=False, custom_path=None):
        """
        Encode codes into QRCode/Barcode.

        Parameters:
        :codes: list of codes to encode.
        :type: qr or bar.
        :transparent: settings for transparent background. Default is False, should be use for designing works for the ticket.
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