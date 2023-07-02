import os
from barcode import Code128
from barcode.writer import ImageWriter

def gen(codes:list, folder_path='./barcodes/'):
    folder_path = './'+folder_path+'/' if os.path.isdir(folder_path) else folder_path

    # (optional) font_path: path to font file to be used
    # Use PIL to set transparent (1) Switch mode to RGBA, (2) set alpha = 0 - 255, (3) 
    ren = ImageWriter(format='PNG', mode='RGBA')

    barcode_options = {'font_size':5,
                       'module_width':0.2,
                       'module_height':7,
                       'text_distance':3,
                       }
 
    for code in codes:
        with open(folder_path+code+'.png', 'wb') as f:
            Code128(code, writer=ren).write(f, options=barcode_options)