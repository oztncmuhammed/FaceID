############################################

####BU DOSYA 1.ADIMDA ÇALIŞTIRILMALDIR######

##########################
###Gerekli kütüphaneler######################

###Gerekli kütüphaneler######

import cv2  # Bilgisayar kamerasını açmak ve görüntü işlemleri için kullandım.
import numpy as np  # Numarik işlemler ve matris manipülasyonu için kullandım.
import torch  # PyTorch kütüphanesi, tensor işlemleri ve model değerlendirmesi için kullandım.
from facenet_pytorch import InceptionResnetV1, MTCNN  # FaceNet modelini kullanmak amacı ile kullandığım kütüphane.
import json  # Admin yüz verilerini JSON dosyasına kaydetmek için kullandım.

def register_admin_face():
    cap = cv2.VideoCapture(0)  # Bilgisayar kamerasını açar
    mtcnn = MTCNN(keep_all=True)  # MTCNN modelini yükler
    model = InceptionResnetV1(pretrained='vggface2').eval()  # FaceNet modelini yükler

    while True: ##r
        ret, frame = cap.read()  # Kameradan görüntü oku
        if not ret:
            print("Kamera açılamadı.") #uygulama için hata mesajımız
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #renkleri bgrden RGB dönüştürür
        boxes, _ = mtcnn.detect(rgb_frame) #yüz algılama

        if boxes is None:
            print("Yüz algılanamadı. Lütfen tekrar deneyin.") #uygulama için hata mesajımız
            continue

        # İlk yüzü al
        x1, y1, x2, y2 = map(int, boxes[0])  #yüzün koordinatlarını alır ve tam sayı yapar
        face = rgb_frame[y1:y2, x1:x2] #sadece yüz bölgesini kırpar
        face = cv2.resize(face, (160, 160)) #Yüzü 160x160 piksel boyutuna ölçeklendirir

        face = face.astype(np.float32) # Yüzü float32 tipine çevirir
        mean, std = face.mean(), face.std()  ## Ortalama ve standart sapmayı hesapla
        face = (face - mean) / std  ## Yüzü normalize eder

        face = np.transpose(face, (2, 0, 1))  # Yüz matrisinin boyutlarını (kanal, yükseklik, genişlik) olarak yeniden düzenle
        face = np.expand_dims(face, axis=0)  # 4 boyutlu tensör oluşturmak için boyut ekle
        face_tensor = torch.tensor(face)  # Numpy dizisini PyTorch tensörüne çevir
        embedding = model(face_tensor).detach().numpy()  # Model ile yüzün gömülmesini hesapla ve numpy dizisine çevir

        with open('admin_face.json', 'w') as f:  # JSON dosyasını yazma modunda aç
            json.dump(embedding.tolist(), f)  # Gömülmüş yüz verisini JSON dosyasına kaydet
        print("Admin yüz verisi kaydedildi.")  # Başarılı kaydetme mesajı ver
        break  # Döngüyü sonlandır


    cap.release()  # Kamerayı kapat
    cv2.destroyAllWindows()  # Tüm OpenCV pencerelerini kapat


register_admin_face()  # Fonksiyonu çağır



