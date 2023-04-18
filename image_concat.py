import os
from tkinter import *
from tkinter import filedialog
from PIL import Image
import natsort as nt

SUBFIXS = ["png","jpg","jpeg","bmp","webp"]

IMAGE_TOTAL = 0
SUB_FOLDER_TOTAL = 0

IMAGE_COUNT = 0
SUB_FOLDER_COUNT = 0

def select_director():
    global TARGET_FOLDER
    folder_path = filedialog.askdirectory(initialdir = "/", title = "Select a Folder")
    TARGET_FOLDER.set(folder_path)

def caculate_width(width_list:list) -> int:
    if not width_list:
        return
    if len(width_list) <= 0:
        return

    width_list = nt.natsorted(width_list)

    if len(width_list) >= 3:
        width_list.pop(0)
        width_list.pop(-1)

    width_mean = 0
    for width_item in width_list:
        width_mean = width_mean + width_item
    width_mean = int(width_mean / len(width_list))

    return width_mean

def caculate_height(image_list:list, target_width:int, image_format:str) -> list:
    size_limit = 65500
    if image_format == 'png':
        # due to limited memory on the user's computer, the limit is set to within 1 million
        size_limit = 1000000
    heights = []
    height_temp = 0
    index = 0
    pre_index = 0
    for index in range(len(image_list)):
        image_item = image_list[index]
        if height_temp + int(image_item.height * (target_width / image_item.width)) > size_limit:
            heights.append((height_temp, image_list[pre_index: index]))
            height_temp = 0
            pre_index = index
        height_temp = height_temp + int(image_item.height * (target_width / image_item.width))
    heights.append((height_temp, image_list[pre_index: index + 1]))
    return heights


def generate_long_image(image_path_list:list, target_file:str, gap_size:int, image_format:str):
    global SUB_FOLDER_TOTAL, SUB_FOLDER_COUNT, IMAGE_TOTAL, IMAGE_COUNT
    if len(image_path_list) <= 0:
        return
    image_path_list = nt.os_sorted(image_path_list)
    image_width_list = []
    image_list = []
    for image_path_item in image_path_list:
        #print(image_path_item)
        try:
            image_item = Image.open(image_path_item)
            image_list.append(image_item)
            image_width_list.append(image_item.width)
        except Exception as e:
            print(str(e))
            label_process.config(text="Huston, We have a problem: " + str(e))

    target_image_width = caculate_width(width_list=image_width_list.copy())
    target_image_heights = caculate_height(image_list=image_list, target_width=target_image_width, image_format=image_format) 
 
    split_count = 0
    for height, image_list_temp in target_image_heights:
        target_image = Image.new('RGB', (target_image_width, height + gap_size * len(image_list_temp)))
        image_item_top = 0
        for image_item in image_list_temp:
            app.update()
            label_process.config(text="Sub-Folders:" + str(SUB_FOLDER_COUNT) + "/" + str(SUB_FOLDER_TOTAL) + "  Images:" + str(IMAGE_COUNT) + "/" + str(IMAGE_TOTAL))
            image_item_height = int(image_item.height * target_image_width / image_item.width)
            image_item.resize((target_image_width, image_item_height), resample=Image.Resampling.BICUBIC)
            target_image.paste(image_item, (0, image_item_top))
            image_item_top = image_item_top + image_item_height
            IMAGE_COUNT = IMAGE_COUNT + 1
        split_count = split_count + 1
        try:
            if image_format == 'jpeg':
                target_image.save(target_file + '_' + str(split_count).zfill(3) + '.jpeg', quality=95)
            elif image_format == 'png':
                target_image.save(target_file + '.png', format='png', optimize=True)
        except Exception as e:
            print(str(e))
            label_process.config(text="Huston, We have a problem: " + str(e))
    
def walk_and_generate():
    global TARGET_FOLDER, GAP_SIZE, SUBFIXS, IMAGE_TOTAL, IMAGE_COUNT, SUB_FOLDER_TOTAL, SUB_FOLDER_COUNT, IMAGE_FORMAT

    gap_size = 0

    if not os.path.isdir(TARGET_FOLDER.get()):
        label_process.config(text="It seem like you may not select a valid folder.")

    if GAP_SIZE.get().strip() == '':
        GAP_SIZE.set('0')
    if GAP_SIZE.get().strip().isnumeric():
        gap_size = int(GAP_SIZE.get())

    IMAGE_TOTAL = 0
    SUB_FOLDER_TOTAL = 0
    # first of all, we collect information of the target folder
    for fpathe, dirs, fs in os.walk(TARGET_FOLDER.get(), topdown=True):
        SUB_FOLDER_TOTAL = SUB_FOLDER_TOTAL + 1
        for f in fs:
            fArray = f.split(".")
            end = fArray[-1].lower()
            if(end in SUBFIXS):
                IMAGE_TOTAL = IMAGE_TOTAL + 1

    SUB_FOLDER_COUNT = 0
    IMAGE_COUNT = 0
    # do the real job
    for fpathe, dirs, fs in os.walk(TARGET_FOLDER.get(), topdown=True):
        image_files = []
        SUB_FOLDER_COUNT = SUB_FOLDER_COUNT + 1
        for f in fs:
            fArray = f.split(".")
            end = fArray[-1].lower()
            if(end in SUBFIXS):
                image_files.append(os.path.join(fpathe,f))
        target_file_name = fpathe + '/' + fpathe.split("\\")[-1].split('/')[-1]
        label_process.config(text="Sub-Folders:" + str(SUB_FOLDER_COUNT) + "/" + str(SUB_FOLDER_TOTAL) + "  Images:" + "0/" + str(IMAGE_TOTAL))
        generate_long_image(image_files, target_file_name, gap_size, image_format=IMAGE_FORMAT.get())
        
    label_process.config(text="Done! Check the target folder.")

app = Tk()
app.title("A Simple Image Stitching Program, larryflynt@github")

TARGET_FOLDER = StringVar()
GAP_SIZE = StringVar()
IMAGE_FORMAT = StringVar()

sw = app.winfo_screenwidth()
sh = app.winfo_screenheight()

center_x = (sw - 600) / 2
center_y = (sh - 400) / 2
app.geometry("%dx%d+%d+%d" % (750, 500, center_x, center_y))

label_step_first = Label(app, font= ('Helvetica 22'), text="Step 1, Choose your target folder")
label_step_first.grid(column = 0, row=0, columnspan=3, padx=(10,5), sticky=W)

label_folder_selector = Label(app, text = "Target Folder: ")
label_folder_selector.grid(column=0, row=1, sticky=E)

entry_folder = Entry(app, textvariable=TARGET_FOLDER, width=55, fg="gray")
entry_folder.grid(column=1, row=1, sticky=W)

button_folder = Button(app, text = "Select a Folder", command = select_director)
button_folder.grid(column=2, row=1, pady=(5,20), sticky=W)

label_step_second = Label(app, font= ('Helvetica 22'), text="Step 2, Set size of gaps, and Select a image format")
label_step_second.grid(column = 0, row=2, columnspan=3, pady=(5,10), padx=(10,5), sticky=W)

label_gap_size = Label(app, text = "Size of Gap ( 0 for NO gap ): ")
label_gap_size.grid(column=0, row=3, sticky=E)

entry_gap_size = Entry(app, textvariable = GAP_SIZE, width=6, fg="gray")
entry_gap_size.grid(column=1, row=3, padx=(0,0), sticky=W)
GAP_SIZE.set('0')

label_gap_size_suffix = Label(app, text = "pixels")
label_gap_size_suffix.grid(column=1, row=3, padx=(50,0), pady=(5,10), sticky=W)

label_image_format = Label(app, text = "Select the image format you prefer: ")
label_image_format.grid(column=0, row=4, sticky=E)

radio_jpeg = Radiobutton(app, text="jpeg", variable=IMAGE_FORMAT, value='jpeg')
radio_png = Radiobutton(app, text="png", variable=IMAGE_FORMAT, value='png')
IMAGE_FORMAT.set('jpeg')

radio_jpeg.grid(column=1, row=4, sticky=W)
radio_png.grid(column=1, row=5, sticky=W)

label_image_format_note = Label(app, 
    text = " Note: 'jpeg' format is more efficient, but the target image size can not exceed 65500 pixels, \
    \n If the target image exceeds 65500 pixels, it will be automatically divided into servral smaller jpeg images, \
    \n 'png' format has no size limit, but it will take up more space.", 
    anchor='w', justify='left')
label_image_format_note.grid(column=0, row=6, columnspan=3, pady=(5,20), padx=(10,5), sticky=W)

label_step_third = Label(app, font= ('Helvetica 22'), text="Step 3, Click 'Generate' to Start!")
label_step_third.grid(column = 0, row=7, columnspan=3, pady=(5,10), padx=(10,5), sticky=W)

button_generate = Button(app, font= ('Helvetica 18'), text = "Generate", command = walk_and_generate)
button_generate.grid(column = 1,row=8, pady=(5,10))

label_process = Label(app, text="0/0 sub-folders, 0/0 images")
label_process.grid(column = 0, row=9, columnspan=3, padx=(10,5), sticky=W)

app.mainloop()