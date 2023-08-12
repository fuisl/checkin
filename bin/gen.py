from typing import Any
from ticket.codegen import generate_ticket_code
from ticket import qrgen, bargen

from updater import TicketCode

class Gen:
    def __init__(self, event_code=None) -> None:
        """
        Initialize Generator object.
        """
        if event_code == None:  # set event_code if None
            self.event_code = 'default'

        self.codes = []  # list of codes

    def gen(self, ticket_info: dict) -> list:
        """
        Initialize and return a list of n number of code.
        """
        # Get number of tickets
        n = sum(ticket_info.values())

        # Generate codes and assign code to self.codes
        codes = generate_ticket_code(ticket_info, seed=self.event_code)

        self.codes = codes

        TicketCode().create_tickets(codes) # Create tickets in database
    
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