#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 15:50:01 2022

@author: jp
"""

# Crop
import cv2
from PIL import Image
import pytesseract
import os

def img_proc(savepath):
    
    # Opens a image in RGB mode
    im = Image.open(savepath)
    os.remove(savepath)
     
    # Size of the image in pixels (size of original image)
    # (This is not mandatory)
    width, height = im.size
     
    # Setting the points for cropped image
    left = 480
    top = 275
    right = 580
    bottom = 300
     
    # Cropped image of above dimension
    # (It will not change original image)
    im1 = im.crop((left, top, right, bottom))
    
    cropped_savepath = savepath.split('.png')[0] + '_cropped.png'
    
    im1.save(cropped_savepath)
    
    im2 = cv2.imread(cropped_savepath, 1)
    
    os.remove(cropped_savepath)
     
    # Increase contrast:
    # converting to LAB color space
    lab= cv2.cvtColor(im2, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)
    
    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv2.createCLAHE(clipLimit=10.0, tileGridSize=(8,8))
    cl = clahe.apply(l_channel)
    
    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl,a,b))
    
    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    
    contrast_savepath = savepath.split('.png')[0] + '_cropped.png'
    
    cv2.imwrite(contrast_savepath, enhanced_img)
    
    imc = Image.open(contrast_savepath)
    
    os.remove(contrast_savepath)
    
    
    # Read value
    raw_res = pytesseract.image_to_string(imc, lang='eng',config='--psm 6')

    raw_res = raw_res.split('\n')[0]
    
    # Catch '0' being interpreted as '8':
    if raw_res[-1] in ('6', '8'):
        raw_res = raw_res[:-1] + '0'
        
    if '€' in raw_res:
        
        raw_res = raw_res.replace('€', 'e')
        
    elif '&' in raw_res:
        
        raw_res = raw_res.replace('&', 'e')
        
    if '-e' in raw_res:
        
        raw_res = raw_res.replace('—-', 'e-')
    
    val = None
    try:
        val = float(raw_res)
    except ValueError:
        if '—-' in raw_res:
            raw_res = raw_res.replace('—-', 'e-')
            try:
                val = float(raw_res)
            except ValueError:
                pass

    return val
     
