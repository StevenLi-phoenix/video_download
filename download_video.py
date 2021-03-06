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


def download():
    global FPS, RES, path_to_video
    yt = YouTube('https://www.youtube.com/watch?v=h3fUgOKFMNU')
    dl = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    print(dl)
    path_to_video = dl.download(output_path="video", filename="1.mp4")
    FPS = dl.fps
    RES = dl.resolution
    print(path_to_video, FPS, RES)


def slice():
    global FPS, RES, path_to_video

    section = 0  # [0,1,2,...

    cap = cv2.VideoCapture(path_to_video)
    image_size = RESCONVERT[RES]

    frame_step = 1
    # frame_step = FPS
    destination_dir = 'output/'
    os.makedirs(destination_dir, exist_ok=True)
    destination_format = 'png'

    image_counter = 0
    read_counter = 0

    threshold_start = section * 150
    threshold_end = (section + 1) * 150

    while (cap.isOpened()):
        read_counter += 1
        if read_counter < threshold_start:
            continue
        ret, cv2_im = cap.read()
        if ret and read_counter % frame_step == 0:
            if image_size:
                cv2.resize(cv2_im, image_size)
            cv2.imwrite(os.path.join(destination_dir, str(read_counter // frame_step) + "." + destination_format),
                        cv2_im)
            print(f"\r{read_counter // frame_step}.{destination_format}", end="")
            image_counter += 1
        elif not ret:
            print("END FRAME AT:", read_counter)
            break
        if read_counter > threshold_end:
            break
    cap.release()


if __name__ == "__main__":
    download()
    slice()
