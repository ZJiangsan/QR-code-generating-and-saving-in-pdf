# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 16:29:22 2019

@author: jizh
"""


import barcode
from barcode import generate
import treepoem
import numpy as np
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import os
from fpdf import FPDF


##############

## generate a series of data
innoled_x_no = np.array([i for i in range(1,73)]).tolist()
innoled_x_no = [str(i) for i in innoled_x_no]
x = np.array(["9:0:1", "8:0:2", "7:0:3", "9:1:0", "8:1:1", "7:1:2"])
x_list = np.repeat(x, [6, 6,6,6,6,6], axis=0).tolist()*2
len(x_list)
rep = [i for i in range(1,7)]*12

innoled_x = ["{}, {}, {}".format(i,j,k) for i, j, k in zip(innoled_x_no, x_list, rep)] 


## first save all targeted ar code to a folder, then these qr code will be read and rendered in pdf
path_qr_1st = "qr_1st"
if not os.path.exists(path_qr_1st):
    os.makedirs(path_qr_1st)

for txt_i in innoled_x:
    print(txt_i)
    x = int(txt_i.split(",")[0])
    y = int(txt_i.split(",")[2])
    img = treepoem.generate_barcode(
    barcode_type='qrcode',
    data=txt_i,
    options={"eclevel": "Q"})
    
    fig, ax = plt.subplots()
    plt.axis('off')
    plt.title(txt_i, fontsize=30)
    arr_lena =img
    imagebox = OffsetImage(arr_lena, zoom=2)
    ab = AnnotationBbox(imagebox, (0.5, 0.6))
    ax.add_artist(ab)
    plt.draw()
    plt.savefig(os.path.join(path_qr_1st, '{}_{}.png'.format(x,y)),bbox_inches='tight')
    plt.close()


## check the file list and re-order them
path_qr_1st = "qr_1st"
train_ids = next(os.walk(path_qr_1st))[2]
train_ids
train_id_x=[i.split('.', 1)[0] for i in train_ids]
train_id_x.sort(key=int)
train_id_x=["{}{}".format(a_, b_) for a_, b_ in zip(train_id_x, [".png"]*len(train_id_x))]
train_id_x


## read the QR codes and save them in pdf, 6 in a row, 54 in one page
pdf = FPDF()
pdf.set_auto_page_break(0)
# imagelist is the list with all image filenames
pdf.add_page()
m = 0
n = 0
for id_ in train_id_x:
#    pdf.add_page()
    print(id_)
    id_x = id_.split(".")[0]
    x = int(id_x.split("_")[0])
    y = int(id_x.split("_")[1])
    if x ==55: ## the number of qr code that can be put in one page, can be specified
        print((x,y))
        pdf.add_page()
        n =0
        m = 0
    img_i_x = os.path.join(path_qr_1st, id_)
#    pdf.add_page()
    print(x)
    if (y-1)%6==0: # change line every six barcodes
        m = 0
        n +=1
    print(("n", n))
    pdf.image(img_i_x,m,(n-1)*30,30,30)
    m +=30
pdf.output("barcode_trial.pdf", "F")
















