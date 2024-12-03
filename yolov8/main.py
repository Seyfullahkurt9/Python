from ultralytics import YOLO
import torch
import cv2
import cvzone
import math
import time
import datetime
import os

# gözükecek sınıf isimlerini tanımlama (her model için o modelin içindeki objenin isimleriyle değiştirilmesi gerekiyor)
classNames = ["surat", "Sigara", "el"
              ]
# fps i ölçebilmek için frame time tanımlama
eski_frame_time = 0
yeni_frame_time = 0

# cap = cv2.VideoCapture(1)  # Webcam
# cap.set(3, 1280)
# cap.set(4, 720)

# webcamden kayıt alma ve boyut ayarlama
cap = cv2.VideoCapture(0)
cap.set(4, 720)

# video kayıt için fourcc(videonun türünü belirlemek için) ve VideoWriter tanımlama
cv2_fourcc = cv2.VideoWriter_fourcc(*'mp4v')
success, img = cap.read()
print(img.shape)

# şuanki zamanın bilgisi yıl, ay, gün, saat, dakika ve saniye
now = datetime.datetime.now()

# video ve örnek resim için kayıt klasörünün konumu
path = 'kayıt'

photoname = "ornek_resim_(" + now.strftime("%Y-%m-%d_%H-%M-%S") + ").jpg"
cv2.imwrite(os.path.join(path, photoname), img)
size = list(img.shape)
del size[2]
size.reverse()

videoname = "kaydedilen_video_(" + now.strftime("%Y-%m-%d_%H-%M-%S") + ").mp4"

video = cv2.VideoWriter(os.path.join(path, videoname), cv2_fourcc, 24, size)
# output video ismi, video türü, fps, size

# GPU
torch.cuda.set_device(0)
# cuda GPU varsa cuda'da yoksa CPU'da çalışacak
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# modelin yolunu tanıtma ve yolo fonksiyonuna modeli tanıtma
model_path = "modeller/el.pt"
model = YOLO(model_path, task='detect')
model.to(device=device)

while True:

    # fps hesaplama iççin yeni frame time tanımlama
    yeni_frame_time = time.time()
    # frame alma
    success, img = cap.read()
    # resmi aynalamak için
    img1 = cv2.flip(img, 1)
    # modeli kullanma
    results = model(img1, stream=True)

    for r in results:
        boxes = r.boxes
        for box in boxes:

            # kutu içine alma
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cv2.rectangle(img1,(x1,y1),(x2,y2),(255,0,255),3)
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img1, (x1, y1, w, h))

            # bulanıklastirma
            imgCrop = img1[y1:y1 + h, x1:x1 + w]
            imgBlur = cv2.blur(imgCrop, (80, 80))
            img1[y1:y1 + h, x1:x1 + w] = imgBlur

            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class isimlerini atama ve yazdırma
            cls = int(box.cls[0])
            cvzone.putTextRect(img1, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

    # video kayıt
    video.write(img1)

    # fps hesaplama ve yazdırma
    fps = 1 / (yeni_frame_time - eski_frame_time)
    eski_frame_time = yeni_frame_time
    print("fps: ", fps)

    # paneli gösterme
    cv2.imshow("Image", img1)

    # q tuşuna basıldığında çıkma
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

video.release()
