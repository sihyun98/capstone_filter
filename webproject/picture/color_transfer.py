import numpy as np
import cv2
import os
from PIL import Image
from PIL import ImageEnhance


# def read_file(sn, tn):
#   s = cv2.imread('source/' + sn + '.bmp')
#   s = cv2.cvtColor(s, cv2.COLOR_BGR2LAB)
#   t = cv2.imread('target/' + tn + '.bmp')
#   t = cv2.cvtColor(t, cv2.COLOR_BGR2LAB)
#   return s, t


def get_mean_and_std(x):
  x_mean, x_std = cv2.meanStdDev(x)
  x_mean = np.hstack(np.around(x_mean, 2))
  x_std = np.hstack(np.around(x_std, 2))
  return x_mean, x_std


def color_transfer(sources, target):
    res = {}
    MaxLength=550
    t_image = target.convert('RGB') 
    t_image = np.array(t_image) 
    # Convert RGB to BGR 
    t = t_image[:,:,::-1].copy()
    theight, twidth, channel = t.shape
    if max(theight,twidth)>MaxLength:
        tratio = MaxLength / max(theight, twidth)
        t = cv2.resize(t, dsize=(0, 0), fx=tratio, fy=tratio,  interpolation=cv2.INTER_AREA)

    t = cv2.cvtColor(t, cv2.COLOR_BGR2LAB)
    

    for n in range(len(sources)):
        s_image = sources[n].convert('RGB') 
        s_image = np.array(s_image) 
        # Convert RGB to BGR 
        s = s_image[:,:,::-1].copy()
        sheight, swidth, channel = s.shape
        if max(sheight,swidth)>MaxLength:
            sratio = MaxLength / max(sheight, swidth)
            s= cv2.resize(s, dsize=(0, 0), fx=sratio, fy=sratio, interpolation=cv2.INTER_AREA)

        s = cv2.cvtColor(s, cv2.COLOR_BGR2LAB)

        s_mean, s_std = get_mean_and_std(s)
        t_mean, t_std = get_mean_and_std(t)

        height, width, channel = s.shape
       
        for i in range(0, height):
            for j in range(0, width):
                for k in range(0, channel):
                    x = s[i, j, k]
                    x = ((x - s_mean[k]) * (t_std[k] / s_std[k])) + 1.01*t_mean[k]
                    # round or +0.5
                    x = round(x)
                    # boundary check
                    x = 0 if x < 0 else x
                    x = 255 if x > 255 else x
                    s[i, j, k] = x
        
        s = cv2.cvtColor(s, cv2.COLOR_LAB2RGB)
        
        s = Image.fromarray(s)
        res[n+1] = s
    # cv2.imwrite('result/r' + str(n + 1) + '.bmp', s)
    return res




