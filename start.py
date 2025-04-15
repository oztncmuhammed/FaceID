############################################

####BU DOSYA 3.ADIMDA ÇALIŞTIRILMALDIR######

##########################
###Gerekli kütüphaneler######################

import cv2  # Bilgisayar kamerasını açmak ve görüntü işlemleri için kullandım.
import numpy as np  # Numarik işlemler ve matris manipülasyonu için kullandım.
import torch  # PyTorch kütüphanesi, tensor işlemleri ve model değerlendirmesi için kullandım.
from facenet_pytorch import InceptionResnetV1, MTCNN  # FaceNet ve MTCNN modellerini yüklemek için kullandım.
import json  # Yüz verilerini JSON dosyasına kaydetmek ve okumak için kullandım.
import os  # Dosya ve dizin işlemleri için kullandım.
import time  # Geri sayım ve zamanlama işlemleri için kullandım.
import sys  # Geri sayım çıktısı için kullanılır.
from cryptography.fernet import Fernet  # Veri şifreleme ve çözme işlemleri için kullandım.



def load_key():
    return open("key.key", "rb").read()  # Anahtar dosyasını okuma modunda aç ve içeriğini geri döndür



def decrypt_file(filename, key):
    fernet = Fernet(key)  # Fernet şifre çözme nesnesini anahtarla oluştur
    with open(filename, "rb") as file:  # Şifreli dosyayı okuma modunda aç
        encrypted_data = file.read()  # Şifreli dosyanın içeriğini oku

    decrypted_data = fernet.decrypt(encrypted_data)  # Dosya içeriğini çöz
    return decrypted_data  # Çözülmüş veriyi geri döndür



def load_admin_face():
    if os.path.exists('admin_face.json'):  # admin_face.json dosyası mevcut mu kontrol et
        with open('admin_face.json', 'r') as f:  # Dosyayı okuma modunda aç
            admin_face_encoding = np.array(json.load(f))  # JSON verisini numpy dizisine dönüştür
        return admin_face_encoding  # Yüz verisini geri döndür
    else:
        print("Hata: admin_face.json dosyası bulunamadı. Lütfen önce yönetici yüz verisi kaydedin.")  # Hata mesajı ver
        return None  # None döndür


def face_recognition_lock(admin_face_encoding):
    cap = cv2.VideoCapture(0)  # Bilgisayar kamerasını aç
    mtcnn = MTCNN(keep_all=True)  # MTCNN modelini yükle
    model = InceptionResnetV1(pretrained='vggface2').eval()  # FaceNet modelini yükle

    countdown = 8  # Geri sayım süresi
    while countdown > 0:
        sys.stdout.write("\rAdmin yüzü doğrulanıyor. Geri sayım: {:2}".format(countdown))  # Geri sayım çıktısı
        sys.stdout.flush()  # Çıktıyı temizle
        time.sleep(1)  # 1 saniye bekle
        countdown -= 1  # Geri sayımı azalt

        ret, frame = cap.read()  # Kameradan görüntü oku
        if not ret:
            print("\nKamera açılamadı.")  # Kamera açılamazsa hata mesajı ver
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR'den RGB'ye dönüştürür
        boxes, _ = mtcnn.detect(rgb_frame)  # MTCNN ile yüz algılaa

        if boxes is None:
            continue  # Yüz algılanamazsa döngüye devam eder

        x1, y1, x2, y2 = map(int, boxes[0])  # İlk yüzün koordinatlarını al ve tam sayı yapar
        face = rgb_frame[y1:y2, x1:x2]  # Yüz bölgesini kırpar
        face = cv2.resize(face, (160, 160))  # Yüzü 160x160 piksel boyutuna ölçeklendirir

        face = face.astype(np.float32)  # Yüzü float32 tipine çevirir
        mean, std = face.mean(), face.std()  # Ortalama ve standart sapmayı hesaplar
        face = (face - mean) / std  # Yüzü normalize eder

        face = np.transpose(face, (2, 0, 1))  # Yüz matrisinin boyutlarını (kanal, yükseklik, genişlik) olarak yeniden düzenler
        face = np.expand_dims(face, axis=0)  # 4 boyutlu tensör oluşturmak için boyut ekler
        face_tensor = torch.tensor(face)  # Numpy dizisini PyTorch tensörüne çevirir
        embedding = model(face_tensor).detach().numpy()  # Model ile yüzün gömülmesini hesapla ve numpy dizisine çevirir

        distance = np.linalg.norm(admin_face_encoding - embedding)  # Yönetici yüz verisi ile yeni yüz verisi arasındaki mesafeyi hesaplar
        if distance < 0.5:  # Mesafe belirli bir eşiğin altındaysa
            print("\nAdmin yüzü tanındı. Dosya açılıyor...")  # Başarılı doğrulama mesajı verir
            cap.release()  # Kamerayı kapat
            cv2.destroyAllWindows()  # Tüm OpenCV pencerelerini kapatır
            return True  # Kilidi açar

    print("\nAdmin yüzü doğrulanamadı. Program sonlandırılıyor.")  # Başarısız doğrulama mesajı verir
    cap.release()  # Kamerayı kapat
    cv2.destroyAllWindows()  # Tüm OpenCV pencerelerini kapatır
    return False  # Kilidi açar

admin_face_encoding = load_admin_face()  # Yönetici yüz verisini yükler
if admin_face_encoding is not None:  # Yüz verisi mevcutsa
    if face_recognition_lock(admin_face_encoding):  # Yüz doğrulama başarılıysa
        key = load_key()  # Şifreleme anahtarını yükler
        decrypted_data = decrypt_file("muhammed.txt.encrypted", key)  # Dosyayı çözer
        print("Dosya içeriği:")  # Dosya içeriğini yazdırır.
        print(decrypted_data.decode())  # Çözülen veriyi yazdırır
    else:
        print("Erişim reddedildi.")  # Erişim reddedildi mesajı verir
else:
    print("Admin yüz verisi bulunamadı. Lütfen önce yönetici yüz verisi kaydedin.")  # Yönetici yüz verisi bulunamadı mesajı verir

