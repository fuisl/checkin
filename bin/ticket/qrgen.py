import os
from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q
from PIL import Image

def gen(codes:list, folder_path='./qrcodes/', transparent=False):
    """
    Generate barcode using QRCode from a list of codes and
    export to a destinated folder, if not exist, automatically
    create one.

    If files exist, replace the duplicate files.

    (optional) Transparent QRCode
    """
    folder_path = './'+folder_path+'/qrcodes/' if not(os.path.isdir(folder_path)) else folder_path
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

        img = ren.make_image(fill_color="black", back_color="white")
        
        if transparent:
            # Converting to transparent background
            img = img.convert("RGBA")
            
            datas = img.getdata()
            new_data = []
            
            for item in datas:
                # Set the white pixels as transparent
                if item[:3] == (255, 255, 255):
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            
            img.putdata(new_data)

        img.save(file_path, "PNG")

        ren.clear()  # Reset attribute

    print(f'{len(codes)} QRCodes created successfully!')