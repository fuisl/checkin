import os
from qrcode import QRCode

def gen(codes:list, folder_path='./qrcodes/'):
    folder_path = './'+folder_path+'/' if not(os.path.isdir(folder_path)) else folder_path
    try:
        os.mkdir(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    except:
        pass

    

gen()