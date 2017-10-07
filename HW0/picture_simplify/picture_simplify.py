# divide the pixel value of picture by 2
# By Junhong Yang

from PIL import Image

# open image
im = Image.open('westbrook.jpg')
pixelMap = im.load()

# create a new image

new_img = Image.new(im.mode, im.size)
pixelNew = new_img.load()

# read image data by column and row

for i in range(new_img.size[0]):  #  size return 2-tuple (width, height)
    for j in range(new_img.size[1]):
        x, y, z = pixelMap[i,j][0], pixelMap[i,j][1], pixelMap[i,j][2]
        pixelNew[i,j] = (x/2, y/2, z/2) # change the pixel value by 2

#im.close()
new_img.show()
new_img.save("output.jpg")
#new_img.close()


