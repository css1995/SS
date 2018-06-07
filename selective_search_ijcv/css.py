

a = [{"c": [1,2]}, {"d", 2}]
print(a[0])
'''
script_dirname = os.path.abspath(os.path.dirname(__file__))
file = '2007_trainval.txt'
train_data = 'groundtruth_train_data.txt'
train_data = open(train_data, 'w')
with open(file, 'r') as f:
        imaList = f.readlines()
for each in imaList:
        image_path = {script_dirname + "/" + each.strip()}
        image = Image.open(script_dirname + "/" + each.strip())
        print(image_path)
        label_path = os.path.join('data', 'label', each.split('/')[-1].split('.')[0] + '.txt')
        with open(label_path, 'r') as f:
            flabel = f.readlines()
        for eachline in flabel:
            if len(eachline) > 0:
                eachline = eachline.strip().split(' ')
                (xmin,ymin,xmax,ymax) = (float(eachline[3]), float(eachline[5]), float(eachline[4]), float(eachline[6]))
                cal = int(float(eachline[0]))
                train_data.write(each.strip() + " " + str(cal) + " " + str(xmin) + " " + str(ymin) + " " + str(xmax) + " " + str(ymax) + " " + '\n')
train_data.close()
'''

'''
file_name_list=os.listdir('./image')
script_dirname = os.path.abspath(os.path.dirname(__file__))
for i in range(len(file_name_list)):
    image_path=script_dirname + '/image/' + file_name_list[i]
    image=Image.open(image_path)
    img=image.convert('RGB')
    savename=script_dirname+"/result/"+file_name_list[i]
    img.save(savename)
 

'''
'''
script_dirname = os.path.abspath(os.path.dirname(__file__))
with open('./trainval.txt','r') as f:
    train_name_list = f.readlines()
sj=1
for each in train_name_list:
    sj=sj+1
    image_path = script_dirname + "/" + (each.split(' ')[0]).strip()
    y_label=(each.split(' ')[1]).strip()
    box=(float((each.split(' ')[2]).strip()),float((each.split(' ')[3]).strip()),float((each.split(' ')[4]).strip()),float((each.split(' ')[5]).strip()))
    image = Image.open(image_path)
    region = image.crop(box)
    draw = ImageDraw.Draw(region)
    savename = "tem_val/" + str(y_label)+"/"+str(sj)+ image_path.split('/')[-1]
    #savename = str(sj) + image_path.split('/')[-1]
    region.save(savename)
    '''
'''
image2=Image.open('000005.jpg')
image=image2
#draw = ImageDraw.Draw( image2)

with open('./00005.txt','r') as f:
    boxes=f.readlines()
for each in boxes:
    each=each.strip().split(' ')
    pr=int(float(each[1]))
    box=(int(float(each[2])),int(float(each[3])),int(float(each[4])),int(float(each[5])))
    x1 = box[0]
    y1 = box[1]
    x2 = box[2]
    y2 = box[3]
    line_width = 4
    flag=1
    if pr==5:
        #draw.line([(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)], width=line_width, fill='red')
        #draw.rectangle((box), outline='red')
        pass
    elif pr==4:
        #draw.line([(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)], width=line_width, fill='blue')
        #draw.rectangle((box), outline='blue')
        pass
    else:
        #draw.line([(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)], width=line_width, fill='green')
        if flag==1:
            box_save=box
            flag=0
        #draw.rectangle((box), outline='green')
#savename = "00005_new.jpg"
#image2.save(savename)
print(box_save)
xmin = box_save[0]
ymin = box_save[1]
xmax = box_save[2]
ymax = box_save[3]
w = xmax - xmin
h = ymax - ymin
image1 = image.convert('L')
reg = image1.crop(box_save)
if w < h:
        left_side = int((h - w) / 2)
        right_side = w + int((h - w) / 2)
        temp = np.ones((h, h)) * 255

        temp[0:h, left_side:(right_side)] = np.array(reg)
        region = Image.fromarray(temp).convert('L')
elif w > h:
        left_side = int((w - h) / 2)
        right_side = int((w - h) / 2) + h
        temp = np.ones((w, w)) * 255
        temp[left_side:right_side, 0:w] = np.asarray(reg)
        region = Image.fromarray(temp).convert('L')
else:
        region = reg
Draw = ImageDraw.Draw(region)
region.save('wrap.jpg')
'''
'''
script_dirname = os.path.abspath(os.path.dirname(__file__))
with open('./data/test_data.txt','r') as f:
    train_name_list = f.readlines()
sj=1
for i in range(len(train_name_list)):
    line = train_name_list[i * 2].strip().split(' ')
    box_num = int((len(line) - 1) / 4)
    image_path = script_dirname + "/" + (line[0]).strip()
    for j in range(box_num):
        ##box=[xmin,ymin,xmax,ymax]
        sj = sj + 1
        box = [float(line[j * 4 + 1]), float(line[j * 4 + 2]), float(line[j * 4 + 3]), float(line[j * 4 + 4])]
        image = Image.open(image_path)
        region = image.crop(box)
        draw = ImageDraw.Draw(region)
        savename = "temp/" + "test/" + str(sj) + image_path.split('/')[-1]
        region.save(savename)
     
'''
