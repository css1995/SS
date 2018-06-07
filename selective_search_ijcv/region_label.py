import os
import xml.etree.ElementTree as ET
classes=['kinef','razor','shuriken','gun']
def get_image(dir,image_path):
    path_trainval=os.path.join(dir,'trainval.txt')
    path_test=os.path.join(dir,'test.txt')
    path_train = os.path.join(dir, 'train.txt')
    path_val = os.path.join(dir, 'val.txt')
    with open(path_trainval) as trainval_file:
        trainval_name=trainval_file.readlines()
    with open(path_test) as test_file:
        test_name = test_file.readlines()
    with open(path_train ) as train_file:
        train_name = train_file.readlines()
    with open(path_val) as val_file:
        val_name = val_file.readlines()


    f1= open('2007_trainval.txt','w')
    for each in trainval_name:
        convert_annotation(each.strip())
        image_path1 = os.path.join(image_path,each.strip()+".jpg")
        f1.write(image_path1+'\n')
    f1.close()
    f2 = open('2007_test.txt', 'w')
    for each in test_name:
        convert_annotation(each.strip())
        image_path1 = os.path.join(image_path, each.strip() + ".jpg")
        f2.write(image_path1+'\n')
    f2.close()

    f3 = open('2007_train.txt', 'w')
    for each in train_name:
        convert_annotation(each.strip())
        image_path1 = os.path.join(image_path, each.strip() + ".jpg")
        f3.write(image_path1 + '\n')
    f3.close()

    f4 = open('2007_val.txt', 'w')
    for each in val_name:
        convert_annotation(each.strip())
        image_path1 = os.path.join(image_path, each.strip() + ".jpg")
        f4.write(image_path1 + '\n')
    f4.close()

def convert_annotation(image_id):
    in_file = open('data/annotation/%s.xml'%(image_id))
    out_file = open('data/label/%s.txt'%(image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        print(str(cls_id) + " " +str(w)+" "+str(h)+" ".join([str(a) for a in b]))
        out_file.write(str(cls_id) + " " +str(w)+" "+str(h)+ " "+ " ".join([str(a) for a in b])+ '\n')
        #out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')



if __name__ == "__main__":
    dir='data/imageSets'
    image_path='data/image'
    get_image(dir,image_path)