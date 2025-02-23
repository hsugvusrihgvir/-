from moviepy.editor import *
from PIL import Image
from random import randint


def cut_images():
    for i in range(5):
        img = Image.open("data\\" + str(i) + ".jpg")
        w, h = img.size
        img = img.crop(((w - h // 16 * 9) // 2, 0, h // 16 * 9 + (w - h // 16 * 9) // 2, h))
        img = img.resize((1080, 1920))
        img.save('data\\' + str(i) + '.jpg')


def create_video():
    ic_1 = ImageClip('data\\0.jpg').set_duration(2)
    ic_2 = ImageClip('data\\1.jpg').set_duration(2)
    ic_3 = ImageClip('data\\2.jpg').set_duration(2)
    ic_4 = ImageClip('data\\3.jpg').set_duration(2)
    ic_5 = ImageClip('data\\4.jpg').set_duration(2)
    video = concatenate([ic_1, ic_2, ic_3, ic_4, ic_5], method="compose")
    a_cl = AudioFileClip("data\\sound\\" + str(randint(1, 9)) + ".mp3")

    video = video.set_audio(a_cl)
    video.write_videofile('res.mp4', fps=1)

cut_images()
create_video()


