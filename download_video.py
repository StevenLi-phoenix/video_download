from pytube import YouTube
import cv2
import os

RESCONVERT = {
    "4320p": (7680, 4320),
    "2160p": (3840, 2160),
    "1440p": (2560, 1440),
    "1080p": (1920, 1080),
    "720p": (1280, 720),
    "480p": (640, 480),
    "360p": (480, 360),
    "240p": (426, 240),
    "144p": (256, 144),
}
yt = YouTube('https://www.youtube.com/watch?v=h3fUgOKFMNU')
dl = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
print(dl)

path_to_video = dl.download(output_path="video", filename="1.mp4")
FPS = dl.fps
RES = dl.resolution
# YouTube('https://www.youtube.com/watch?v=h3fUgOKFMNU').streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path="video", filename="1.mp4")
print(path_to_video, FPS, RES)

cap = cv2.VideoCapture(path_to_video)  # says we capture an image from a webcam
image_size = RESCONVERT[RES]

# frame_step = 1
frame_step = FPS
destination_dir = 'video/'
os.makedirs(destination_dir, exist_ok=True)
destination_format = 'png'

image_counter = 0
read_counter = 0

while (cap.isOpened()):
    ret, cv2_im = cap.read()
    if ret and read_counter % frame_step == 0:
        if image_size:
            cv2.resize(cv2_im, image_size)
        cv2.imwrite(os.path.join(destination_dir, str(image_counter) + "." + destination_format), cv2_im)
        print(f"\r{image_counter}/{read_counter}", end="")
        image_counter += 1
    elif not ret:
        break
    read_counter += 1
cap.release()
