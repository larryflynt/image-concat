# image-concat

This is a small program with a UI interface used for batch image stitching. It can stitch a series of small images into a single long strip image, making it suitable for creating long comic strips that can be conveniently read on mobile devices.

Its operation is very simple：

1, select the folder containing the images. 

2, set the image interval and format. 

Finally, click "Generate"! 

All images within the subfolders will be sorted by name and stitched together into a long strip image, which will be stored in the respective subfolders.

For example:

```
Target_Folder--SubfolderA--A01.jpg
            |           |--A02.jpg
            |           |--A03.jpg
            |           
            |--SubfolderB--B01.jpg
                        |--B02.jpg
                        |--B03.jpg
```

Images 'A01', 'A02', 'A03' will be stitched together to form a long strip image named 'SubfolderA.jpg'. It will be stored in 'SubfolderA'. 

Similarly, images 'B01', 'B02', 'B03' will also be stitched together to form a long strip image named 'SubfolderB.jpg', which will be stored in 'SubfolderB'.

#### How are the images sorted before concatenation?

Before concatenating the images, Image-concat will sort them according to the 'os_sort' rules in the https://github.com/SethMMorton/natsort library, which means that they will be sorted based on your computer's default sorting rule. "natsort" is an efficient and beautiful sorting library, and we thank @SethMMorton for his contribution!


## 中文

这是一个带UI界面的小程序，用来批量的拼接图片，它可以把一系列小图片拼接成一整张长条图片，适合用来把单页漫画做成手机上方便阅读的长条漫画。

它的操作非常简单：

第一步，选择包含图片的文件夹。

第二步，设置图片间隔和图片格式。

第三步，点击“Generate”！所有子文件夹内的图片，都会按名字排序后，分别拼接成一整张长条图片，存储在子文件夹内。

比如：

```
Target_Folder--SubfolderA--A01.jpg
            |           |--A02.jpg
            |           |--A03.jpg
            |           
            |--SubfolderB--B01.jpg
                        |--B02.jpg
                        |--B03.jpg
```

'A01'、'A02'、'A03' 图片将被拼接成一张名为 'SubfolderA.jpg' 的长条图片，保存在 'SubfolderA' 中。

同样，'B01'、'B02'、'B03' 图片也将被拼接成一张名为 'SubfolderB.jpg' 的长条图片，保存在 'SubfolderB' 中。

#### 图片按什么顺序排序？

Image-concat在拼接图片前，会先按照https://github.com/SethMMorton/natsort 库的os_sort规则排序图片，即按照您的电脑系统默认排序规则排序，natsort是一个高效且优美的排序库，感谢@SethMMorton 的贡献！
