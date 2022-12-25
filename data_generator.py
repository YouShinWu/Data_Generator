import os
from os import listdir
from os.path import isfile, join, exists
import cv2

'''
This Data Generator will resize input image to different size image based on jem test image
Class A: 3840 x 2160
Class B: 1920 x 1080
Class C: 832 x 480
Class D: 416 x 240
Class E: 1280 x 720
'''

dataset_path = '/home/woody/dataset/DIV2K_train_HR'
result_path = '/home/woody/dataset/DIV2k_train_origin_'
ffmpeg = '/usr/local/bin/ffmpeg-5.1.1/ffmpeg'

class Data_Generator:
    def __init__(self,dataset_path, result_path, class_name, to_yuv420_flag):
        self.dataset_path = dataset_path
        self.result_path = result_path +class_name
        self.class_name = class_name 
        self.file_names = []
        self.to_yuv420 = to_yuv420_flag
        self.get_all_files()
        self.create_dir()
        print('Create Data Generator:')
        print(f'Dataset path: {self.dataset_path}')
        print(f'Result path: {self.result_path}')

    def get_all_files(self):
        print('Get dataset path {}'.format(self.dataset_path))
        only_files = [f for f in listdir(self.dataset_path) if isfile(join(self.dataset_path, f))]
        only_files.sort()
        self.file_names = only_files
        # return only_files

    def resize_and_write_img(self):
        class_table = {'A':(3840,2160),'B':(1920,1080),'C':(832,480), 'D':(416,240), 'E':(1280, 720)}
        size = class_table[self.class_name]
        for file in self.file_names:
            image_path = join(self.dataset_path,file)
            print(f'Resize {image_path}')
            image = cv2.imread(image_path)
            image = cv2.resize(image, size,interpolation=cv2.INTER_AREA)
            write_path = join(self.result_path,file)
            print(f'Write image to {write_path}')
            cv2.imwrite(write_path,image)
            if self.to_yuv420:
                name = file.split('.')[0]
                yuv = join(self.result_path,name+'.yuv')
                print(f'Convert to yuv {yuv}')
                os.system(f'{ffmpeg} -i {write_path} -pix_fmt yuv420p {yuv}')
    
    def create_dir(self):    
        if exists(self.result_path):
            print(f"{self.result_path} exist")
            return True
        else:
            print(f"mkdir {self.result_path}")
            os.mkdir(self.result_path)
            return True
    

def main() -> None:
    generator = Data_Generator(dataset_path, result_path, 'C', 1)
    generator.resize_and_write_img()

if __name__ == '__main__':
    main()
   




  
