from os import listdir
from os.path import isfile, join
import cv2

'''
Class D: 416 x 240
Class E: 
'''

dataset_path = '/home/woody/dataset/DIV2K_train_HR'

class Data_Generator:
    def __init__(self,dataset_path, result_path, class_name):
        self.dataset_path = dataset_path
        self.result_path = result_path
        self.class_name = class_name 

def get_all_files(path):
    only_files = [join(path,f) for f in listdir(path) if isfile(join(path, f))]
    only_files.sort()
    return only_files

def resize_img(image_path, width, hight):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (width,hight),interpolation=cv2.INTER_AREA)
    cv2.imshow('Result', image)
    cv2.waitKey(0)

if __name__ == '__main__':
    files = get_all_files(dataset_path)
    print(files[0])
    resize_img(files[0], 416, 240)

