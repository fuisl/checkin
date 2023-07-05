import os
from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q

def gen(codes:list, folder_path='./qrcodes/'):
    folder_path = './'+folder_path+'/' if not(os.path.isdir(folder_path)) else folder_path
    try:
        os.mkdir(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    except:
        pass

    ren = QRCode(version=1,
                 error_correction=ERROR_CORRECT_M,
                 box_size=10,
                 border=4)
    
    for code in codes:
        file_path = folder_path+'/'+code+'.png'

        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass
        except PermissionError:
            print(f"Unable to delete {file_path}.")
        except Exception as e:
            print(f"An error occurred while deleting the file: {e}") 

        ren.add_data(code)  # Adding data for encoding
        ren.make(fit=True)

        img = ren.make_image()
        img.save(file_path)

        ren.clear()  # Reset attribute

    print(f'{len(codes)} QRCodes created successfully!')