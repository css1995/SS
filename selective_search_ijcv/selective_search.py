import tempfile
import subprocess
import shlex
import os
import numpy as np
import scipy.io
from util import *

from PIL  import Image, ImageDraw, ImageFont


script_dirname = os.path.abspath(os.path.dirname(__file__))


def get_windows(image_fnames, cmd='selective_search_rcnn'):
    """
    Run MATLAB Selective Search code on the given image filenames to
    generate window proposals.

    Parameters
    ----------
    image_filenames: strings
        Paths to images to run on.
    cmd: string
        selective search function to call:
            - 'selective_search' for a few quick proposals
            - 'selective_seach_rcnn' for R-CNN configuration for more coverage.
    """
    # Form the MATLAB script command that processes images and write to
    # temporary results file.
    f, output_filename = tempfile.mkstemp(suffix='.mat')
    os.close(f)
    fnames_cell = '{' + ','.join("'{}'".format(x) for x in image_fnames) + '}'
    command = "{}({}, '{}')".format(cmd, fnames_cell, output_filename)
    print(command)

    # Execute command in MATLAB.
    mc = "matlab -nojvm -r \"try; {}; catch; exit; end; exit\"".format(command)
    pid = subprocess.Popen(
        #shlex.split(mc), stdout=open('/dev/null', 'w'), cwd=script_dirname)
        shlex.split(mc), stdout=open('null', 'w'), cwd=script_dirname)
    time.sleep(30)
    retcode = pid.wait()
    if retcode != 0:
        raise Exception("Matlab script did not exit successfully!")

    # Read the results and undo Matlab's 1-based indexing.
    all_boxes = list(scipy.io.loadmat(output_filename)['all_boxes'][0])
    subtractor = np.array((1, 1, 0, 0))[np.newaxis, :]
    all_boxes = [boxes - subtractor for boxes in all_boxes]

    # Remove temporary file, and return.
    os.remove(output_filename)
    if len(all_boxes) != len(image_fnames):
        raise Exception("Something went wrong computing the windows!")
    return all_boxes


if __name__ == '__main__':
    """
    Run a demo.
    """
    import time
    '''
    image_filenames = [
        #script_dirname + '/image/cat.jpg',
        script_dirname + '/image/000003.jpg'
    ]
    t = time.time()
    print(image_filenames[0])
    print(len(image_filenames))
    boxes = get_windows(image_filenames)

    for i in range(len(image_filenames)):
        print(image_filenames[i])
        image = Image.open(image_filenames[i])
        draw = ImageDraw.Draw( image)
        for (x,y,w,h) in boxes[i]:
            xmin = x
            xmax = x + w
            ymin = y
            ymax = y + h
            draw.rectangle((xmin, ymin, xmax, ymax), outline='red')
        savename="result/"+str(i)+".jpg"
        image.save(savename)

    print("Processed {} images in {:.3f} s".format(
        len(image_filenames), time.time() - t))

    '''
    flag=1
    if flag:
        file = '2007_trainval.txt'
        train_data = 'trainval_data.txt'
        train_data = open(train_data, 'w')
        with open(file, 'r') as f:
            imaList = f.readlines()
        '''
        pos=0
        pos_0=0
        pos_1=0
        pos_2=0
        pos_3=0
        total=0
        total_0 = 0
        total_1 = 0
        total_2 = 0
        total_3 = 0
        '''
        for each in imaList:
            image_path = {script_dirname + "/" + each.strip()}
            image = Image.open(script_dirname + "/" + each.strip())
            print(image_path)
            label_path = os.path.join('data', 'label', each.split('/')[-1].split('.')[0] + '.txt')
            with open(label_path, 'r') as f:
                flabel = f.readlines()

            # img = Image.fromarray(img_convert_ndarray)
            g_boxes = []
            b_boxes=[]
            num=0
            #boxes = get_windows(image_path)[0][0:1000]
            boxes = get_windows(image_path)[0]
            for eachline in flabel:
                if len(eachline) > 0:
                    eachline = eachline.strip().split(' ')
                    g_box = (float(eachline[3]), float(eachline[5]), float(eachline[4]), float(eachline[6]))
                    cal = int(float(eachline[0]))
                    g_boxes.append(g_box)
                    for (ymin, xmin, ymax, xmax) in boxes:
                        box = (xmin, ymin, xmax, ymax)
                        if bbox_iou(box, g_box) > 0.7:
                             num+=1
                             train_data.write(each.strip() + " " +str(cal)+" "+ str(xmin) + " " + str(ymin) + " " + str(xmax) + " " + str(ymax) + " " + '\n')
                             print(each.strip() + " " +str(cal)+" "+ str(xmin) + " " + str(ymin) + " " + str(xmax) + " " + str(ymax))
                    '''
                    total = total+1
                    g_box = (float(eachline[3]), float(eachline[5]), float(eachline[4]), float(eachline[6]))
                    cal=int(float(eachline[0]))
                    if cal==0:
                        total_0 += 1
                    elif cal == 1:
                        total_1 += 1
                    elif cal == 2:
                        total_2 += 1
                    elif cal == 3:
                        total_3 += 1
                    for (ymin,xmin, ymax,xmax) in boxes:
                        box = (xmin, ymin, xmax, ymax)
                        if bbox_iou(box,g_box)>0.7:
                            pos += 1
                            if cal==0:
                                pos_0+=1
                            elif cal == 1:
                                pos_1 += 1
                            elif cal == 2:
                                pos_2 += 1
                            elif cal == 3:
                                pos_3 += 1
                            break
                print(pos,total)

                    #print(tmp)
                    #g_boxes.append(g_box)
            '''
            for (ymin,xmin, ymax,xmax) in boxes:
                box = (xmin, ymin, xmax, ymax)
                
                for j in range(len(g_boxes)):
                    iou=bbox_iou(box,g_boxes[j])
                    if iou>0.1:
                        #print(box,bbox_iou(box,g_boxes[j]))
                        break
                    if j==len(g_boxes)-1:
                        b_boxes.append([xmin, ymin, xmax, ymax])
             
            for k in range(num):
                num=int(np.random.random()*len(b_boxes))
                print(each.strip() + " " + "4 " + " ".join([str(s) for s in b_boxes[num]]))
                train_data.write(each.strip() + " " + "4 " + " ".join([str(s) for s in b_boxes[num]]) + '\n')
                region = image.crop(b_boxes[num])
                draw = ImageDraw.Draw(region)
                #savename1 = "temp/" + "4/" + str(k) + "_" + each.strip().split('/')[-1]
                #region.save(savename1)
            #break
            '''
        print(pos,total,pos*1.0/total)
        print("0:  ",pos_0, total_0,pos_0*1.0/total_0)
        print("1:  ", pos_1, total_1,pos_1*1.0/total_1)
        print("2:  ", pos_2, total_2,pos_2*1.0/total_2)
        print("3:  ", pos_3, total_3,pos_3*1.0/total_3)
        #train_data.close()
        '''
        train_data.close()
    flag=0
    if not flag :
        file = '2007_test.txt'
        train_data = 'test_data.txt'
        train_data = open(train_data, 'w')
        with open(file, 'r') as f:
            imaList = f.readlines()
        for each in imaList:
            image_path={script_dirname+"/"+each.strip()}
            print(image_path)
            label_path = os.path.join('data', 'label', each.split('/')[-1].split('.')[0] + '.txt')
            t = time.time()
            boxes = get_windows(image_path)
            img  = Image.open(script_dirname+"/"+each.strip())
            #img = img1.convert('rgb')
            draw = ImageDraw.Draw(img)
            train_data.write(each.strip())
            for  (xmin,ymin,xmax,ymax) in boxes[0][:]:
                train_data.write(" "+str(ymin)+" "+str(xmin)+" "+str(ymax)+" "+str(xmax))
            train_data.write("\n")
            with open(label_path, 'r') as f:
                flabel = f.readlines()
            train_data.write("label:")
            for eachline in flabel:
                if len(eachline) > 0:
                    eachline = eachline.strip().split(' ')
                    train_data.write(" " +str(eachline[0]) + " " + str(eachline[3]) + " " + str(eachline[5]) + " " + str(eachline[4]) + " " + str(eachline[6]))
                    #g_box = (float(eachline[3]), float(eachline[5]), float(eachline[4]), float(eachline[6]))
            train_data.write("\n")
        train_data.close()
    '''

    file_name_list=os.listdir('./image')
    image_filenames=[]
    for i in range(len(file_name_list[:3])):
        image_filenames.append(script_dirname + '/image/'+file_name_list[i])
    t = time.time()
    print(image_filenames)
    print(len(image_filenames))
    boxes = get_windows(image_filenames[:3])

    for i in range(len(image_filenames)):
        print(image_filenames[i])
        image = Image.open(image_filenames[i])
        draw = ImageDraw.Draw( image)


        for (xmin,ymin,xmax,ymax) in boxes[i][:50]:



            #draw.rectangle((xmin, ymin, xmax, ymax), outline='red')
            #draw.rectangle((xmin, ymin, w, h), outline='red')
            draw.rectangle(( ymin,xmin,ymax,xmax), outline='yellow')

        savename="result/"+file_name_list[i]
        image.save(savename)
       
       
              draw.rectangle(g_box, outline='yellow')
        savename = "result/" + each.split('/')[-1].split('.')[0]+".jpg"
        img.save(savename)
        break
    print("Processed {} images in {:.3f} s".format(len(image_filenames), time.time() - t))
    '''