#import skimage.data
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import selectivesearch
from utils import *

import os


import numpy as np
from PIL import Image, ImageDraw, ImageFont

def bbox_iou(box1, box2, x1y1x2y2=True):
    if x1y1x2y2:
        mx = min(box1[0], box2[0])
        Mx = max(box1[2], box2[2])
        my = min(box1[1], box2[1])
        My = max(box1[3], box2[3])
        w1 = box1[2] - box1[0]
        h1 = box1[3] - box1[1]
        w2 = box2[2] - box2[0]
        h2 = box2[3] - box2[1]
    else:
        mx = min(box1[0]-box1[2]/2.0, box2[0]-box2[2]/2.0)
        Mx = max(box1[0]+box1[2]/2.0, box2[0]+box2[2]/2.0)
        my = min(box1[1]-box1[3]/2.0, box2[1]-box2[3]/2.0)
        My = max(box1[1]+box1[3]/2.0, box2[1]+box2[3]/2.0)
        w1 = box1[2]
        h1 = box1[3]
        w2 = box2[2]
        h2 = box2[3]
    uw = Mx - mx
    uh = My - my
    cw = w1 + w2 - uw
    ch = h1 + h2 - uh
    carea = 0
    if cw <= 0 or ch <= 0:
        return 0.0

    area1 = w1 * h1
    area2 = w2 * h2
    carea = cw * ch
    uarea = area1 + area2 - carea
    return carea/uarea


def loaddata(file,train_data,train_tag):
    print(file)
    print(train_data)
    print(train_tag)
    train_data = open(train_data, 'w')
    with open(file,'r') as f:
        imaList=f.readlines()
    if train_tag:
        for each in imaList:
            print(each.strip())
        #   each = 'test.jpg'
            image = Image.open(each.strip())
            image = image.convert('RGB')
            img = np.array(image)
            label_path=os.path.join('data','label',each.split('/')[-1].split('.')[0]+'.txt')
            print(label_path)
            with open(label_path,'r') as f:
                flabel=f.readlines()
            # img = Image.fromarray(img_convert_ndarray)
            g_boxes = []
            for eachline in flabel:
                if len(eachline) > 0:
                    eachline = eachline.strip().split(' ')
                    train_data.write(each.strip() + " " + str(eachline[0]) + " " + str(eachline[3]) + " " + str(
                        eachline[5]) + " " + str(eachline[4]) + " " + str(eachline[6]) + '\n')
                    print(each.strip() + " " + str(eachline[0]) + " " + str(eachline[3]) + " " + str(
                        eachline[5]) + " " + str(eachline[4]) + " " + str(eachline[6]))
                    g_box = (float(eachline[3]), float(eachline[5]), float(eachline[4]), float(eachline[6]))
                    g_boxes.append(g_box)

            # perform selective search

            img_lbl, regions = selectivesearch.selective_search(img, scale=1000, sigma=0.8, min_size=90)
            #print(label_path)
            # print(regions[:10])
            candidates = set()
            for r in regions:
                # excluding same rectangle (with different segments)
                if r['rect'] in candidates:
                    continue
                # excluding regions smaller than 2000 pixels
                if r['size'] < 2000:
                    continue
                # distorted rects
                x, y, w, h = r['rect']
                if w<=50 or h<=50 or w / h > 1.2 or h / w > 1.2:
                    continue
                candidates.add(r['rect'])
            for x, y, w, h in candidates:
                xmin = x
                xmax = x + w
                ymin = y
                ymax = y + h
                box = (xmin, ymin, xmax, ymax)
                for j in range(len(g_boxes)):
                    if bbox_iou(box,g_boxes[j])>0.1:
                        #print(box,bbox_iou(box,g_boxes[j]))
                        break
                    if j==len(g_boxes)-1:
                        print(each.strip() + " " + "4 " + " ".join([str(s) for s in box]) )
                        train_data.write(each.strip() + " " + "4 " + " ".join([str(s) for s in box]) + '\n')
        train_data.close()

    else:
        train_data = open('tiaocan', 'w')
        total=0
        pos=0
        dex=0
        eps=0.000001
        for sca in range(20):
            scale = (sca + 1) *100
            for each in imaList:
                dex=dex+1
                image = Image.open(each.strip())
                print(each.strip())
                image = image.convert('RGB')
                img = np.array(image)
                ave=np.sum(np.sum(img))
                img[np.where(img>ave)]=255
                label_path = os.path.join('data', 'label', each.split('/')[-1].split('.')[0] + '.txt')
                #print(label_path)
                with open(label_path, 'r') as f:
                    flabel = f.readlines()
                g_boxes = []
                for eachline in flabel:
                    if len(eachline) > 0:
                        eachline = eachline.strip().split(' ')
                        #train_data.write(each.strip() + " " + str(eachline[0]) + " " + str(eachline[3]) + " " + str(eachline[5]) + " " + str(eachline[4]) + " " + str(eachline[6]) + '\n')
                        #print(each.strip() + " " + str(eachline[0]) + " " + str(eachline[3]) + " " + str(eachline[5]) + " " + str(eachline[4]) + " " + str(eachline[6]))
                        g_box = (float(eachline[3]), float(eachline[5]), float(eachline[4]), float(eachline[6]))
                        g_boxes.append(g_box)
                        total=total+1
                img_lbl, regions = selectivesearch.selective_search(img, scale=scale, sigma=0.8, min_size=30)
                candidates = set()
                for r in regions:
                    # excluding same rectangle (with different segments)
                    # print(r['rect'])
                    if r['rect'] in candidates:
                        continue
                    # excluding regions smaller than 1000 pixels
                    if r['size'] < 2000:
                        continue
                    # distorted rects
                    x, y, w, h = r['rect']
                    # if w / h > 1.2 or h / w > 1.2:
                    # if w==0 or h==0 or  w / h > 5 or h / w > 5:
                    if w <= 64 or h <=64 or w / h >5 or h / w >= 5:
                        continue
                    candidates.add(r['rect'])
                train_data.write(each.strip())
                savename = "results/"+str(scale)+str(each.split('/')[-1].split('.')[0])+'output.jpg'
                draw = ImageDraw.Draw(image)
                for x, y, w, h in candidates:
                    xmin = x
                    xmax = x + w
                    ymin = y
                    ymax = y + h
                    draw.rectangle((xmin, ymin, xmax, ymax), outline='red')
                print("save plot results to %s" % savename)
                image.save(savename)
                for j in range(len(g_boxes)):
                    for x, y, w, h in candidates:
                        xmin = x
                        xmax = x + w
                        ymin = y
                        ymax = y + h
                        box = (xmin, ymin, xmax, ymax)
                        if bbox_iou(box, g_boxes[j]) > 0.8 :
                            pos = pos + 1
                            break
                for x, y, w, h in candidates:
                    # print(x, y, w, h)
                    xmin = x
                    xmax = x + w
                    ymin = y
                    ymax = y + h
                    box = (xmin, ymin, xmax, ymax)
                    # print(box,w,h)
                    train_data.write(str(" " + " ".join([str(s) for s in box])))
                train_data.write('\n')

                train_data.write('label:')
                for eachline in flabel:
                   if len(eachline) > 0:
                        eachline = eachline.strip().split(' ')
                        # print(eachline)
                        g_box = (eachline[0], float(eachline[3]), float(eachline[5]), float(eachline[4]), float(eachline[6]))
                        #print(g_box)
                        train_data.write(str(" " + " ".join([str(s) for s in g_box])))
                train_data.write('\n')

                print(pos, total)
            if sca ==0:
                print(scale, pos, total, pos / (total + eps))
                break


        train_data.close()




if __name__ == "__main__":
    #print(forwhich)
    train_tag =0
    if train_tag:
        # for train or valid set
        file = '2007_train.txt'
        train_data = 'train_data.txt'
        loaddata(file, train_data, train_tag)
        file = '2007_val.txt'
        train_data = 'val_data.txt'
        loaddata(file, train_data, train_tag)
    else:
        file = '2007_test.txt'
        train_data = 'test_data.txt'
        loaddata(file,train_data,train_tag)





