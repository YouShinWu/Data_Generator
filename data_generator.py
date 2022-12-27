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
# result_path = '/home/woody/dataset/DIV2k_train_origin_'
result_path = '/home/woody/dataset/training_data/Class_'
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
        print(f'Get dataset path {self.dataset_path}')
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
    
    def extract_yuv_component(self):
        class_table = {'A':'3840x2160','B':'1920x1080','C':'832x480', 'D':'416x240', 'E':'1280x720'}
        yuv_files = [f for f in os.listdir(self.result_path) if f.endswith('.yuv')]
        # print(png)
        yuv_files.sort()
        for yuv in yuv_files:
            image_path = os.path.join(self.result_path,yuv)
            print(image_path)
            file_name = yuv.split('.')[0]
            y_path = os.path.join(self.result_path,f"{file_name}_y_.png")
            u_path = os.path.join(self.result_path,f"{file_name}_u_.png")
            v_path = os.path.join(self.result_path,f"{file_name}_v_.png")
            size = class_table[self.class_name]
            command = f"{ffmpeg} -y -f rawvideo -s {size} -i {image_path} -filter_complex 'extractplanes=y+u+v[y][u][v]' -map '[y]' {y_path} -map '[u]' {u_path} -map '[v]' {v_path}"
            print(command)
            os.system(command)
        
    def extract_yuv420p10le_component(self):
        class_table = {'A':'3840x2160','B':'1920x1080','C':'832x480', 'D':'416x240', 'E':'1280x720'}
        yuv_files = [f for f in os.listdir(self.result_path) if f.endswith('.yuv')]
        # print(png)
        yuv_files.sort()
        for yuv in yuv_files:
            image_path = os.path.join(self.result_path,yuv)
            print(image_path)
            file_name = yuv.split('.')[0]
            y_path = os.path.join(self.result_path,f"{file_name}_extract_y_.png")
            u_path = os.path.join(self.result_path,f"{file_name}_extract_u_.png")
            v_path = os.path.join(self.result_path,f"{file_name}_extract_v_.png")
            size = class_table[self.class_name]
            command = f"{ffmpeg} -y -f rawvideo -s {size} -pix_fmt yuv420p10le -i {image_path} -filter_complex 'extractplanes=y+u+v[y][u][v]' -map '[y]' {y_path} -map '[u]' {u_path} -map '[v]' {v_path}"
            # print(command)
            os.system(command)
    

def main() -> None:
    generator = Data_Generator(dataset_path, result_path, 'D', 0)
    # generator.resize_and_write_img()
    generator.extract_yuv_component()

if __name__ == '__main__':
    main()
   




  
