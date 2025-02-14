from PIL import Image

def grayscale():
    image = Image.open('input.jpg')
    data = image.load()

    for i in range(image.size[0]):
        for j in range(image.size[1]):
            rgb = data[i, j]

            media = (rgb[0] + rgb[1] + rgb[2]) // 3

            data[i, j] = (media, media, media)

    image.show()

def binary():
    image = Image.open('input.jpg')
    data = image.load()

    for i in range(image.size[0]):
        for j in range(image.size[1]):
            rgb = data[i, j]

            media = (rgb[0] + rgb[1] + rgb[2]) // 3
            
            color = 255 if media > 120 else 0

            data[i, j] = (color ,color, color)

    image.show()

grayscale()
binary()