from PIL import Image
import random
from tweet import update_image


def new_pixel(old, new, ratio):
    ret = [0,0,0]
    i_ratio = 1.0 - ratio
    for i in range(0,3):
        ret[i] = int((old[i] * new[i]) / 256)
    for i in range(0, 3):
        ret[i] = int((old[i] * i_ratio) + (ret[i] * ratio))
    return ret[0], ret[1], ret[2]


def calculate_opacity_ratio(i,j,source):
    sum = 0
    count = 0
    for x in range(-2,2):
        for y in range(-2,2):
            count += 1
            if 0 <= x+i < 631 and 0 <= y+j < 631:
                sum += source[x+i,y+j][3]
    return  sum/count/256


def generate_and_update_pfp(x,y):
    with Image.open("boys.png") as boys:
        with Image.open("shirt.png") as shirt:
            with Image.open("sky.png") as sky:
                with Image.open("hat.png") as hat:
                    boy_pixels = boys.load()  # create the pixel map
                    shirt_pixels = shirt.load()  # create the pixel map
                    sky_pixels = sky.load()  # create the pixel map
                    hat_pixels = hat.load()  # create the pixel map

                    shirt_color = (random.randint(0,256),random.randint(0,256),random.randint(0,256))
                    sky_color = (random.randint(0,256),random.randint(0,256),random.randint(0,256))
                    hat_color = (random.randint(0,256),random.randint(0,256),random.randint(0,256))
                    for i in range(boys.size[0]):    # for every col:
                        for j in range(boys.size[1]):    # For every row
                            if shirt_pixels[i,j][3] > 1:
                                boy_pixels[i, j] = new_pixel(boy_pixels[i,j],shirt_color, calculate_opacity_ratio(i,j,shirt_pixels))
                            elif sky_pixels[i,j][3] > 1:
                                boy_pixels[i, j] = new_pixel(boy_pixels[i,j],sky_color,calculate_opacity_ratio(i,j,sky_pixels))
                            elif hat_pixels[i,j][3] > 1:
                                boy_pixels[i, j] = new_pixel(boy_pixels[i,j],hat_color, calculate_opacity_ratio(i,j,hat_pixels))
                    # boys.show()
                    boys.save("/tmp/generated.png")
                    return update_image("/tmp/generated.png")


if __name__ == '__main__':
    generate_and_update_pfp(None, None)