from urllib.request import urlopen

# 計測対象の目印として「@profile」をつける
@profile
def get_images():
    images = []
    for index in range(500, 510):
        with urlopen("http://www.yoheim.net/image/{}.jpg".format(index)) as res:
            images.append(res.read())
    return images

images = get_images()