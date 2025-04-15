############################################

####BU DOSYA 2.ADIMDA ÇALIŞTIRILMALDIR######

##########################
###Gerekli kütüphaneler######################

###Gerekli kütüphaneler######
from cryptography.fernet import Fernet  # Veri şifreleme ve çözme işlemleri için kullanılan bir kütüphane
import os  # Dosya ve dosya yolu ile ilgili işlemler için kullanılır

def generate_key():
    key = Fernet.generate_key()  # Yeni bir şifreleme anahtarı oluştur
    with open("key.key", "wb") as key_file:  # Anahtar dosyasını yazma modunda açar
        key_file.write(key)  # Anahtarı dosyaya yazar

def load_key():
    return open("key.key", "rb").read()  # Anahtar dosyasını okuma modunda aç ve içeriğini geri döndürür

def encrypt_file(filename, key):
    if os.path.exists(f"{filename}.encrypted"):  # Şifreli dosya eğer zaten varsa
        print("Dosya zaten şifrelenmiş.")  # Uyarı mesajı verir
        return

    fernet = Fernet(key)  # Fernet şifreleme nesnesini anahtarla oluşturur
    with open(filename, "rb") as file:  # Şifrelenecek dosyayı okuma modunda açar
        file_data = file.read()  # Dosyanın içeriğini okur

    encrypted_data = fernet.encrypt(file_data)  # Dosya içeriğini şifreler
    with open(f"{filename}.encrypted", "wb") as file:  # Şifreli dosyayı yazma modunda açar
        file.write(encrypted_data)  # Şifreli veriyi dosyaya yazar
    print(f"{filename} dosyası şifrelendi.")  # Başarılı şifreleme mesajı verir

def decrypt_file(filename, key):
    fernet = Fernet(key)  # Fernet şifre çözme nesnesini anahtarla oluşturur
    with open(filename, "rb") as file:  # Şifreli dosyayı okuma modunda açar
        encrypted_data = file.read()  # Şifreli dosyanın içeriğini okur

    decrypted_data = fernet.decrypt(encrypted_data)  # Dosya içeriğini çözer
    return decrypted_data  # Çözülmüş veriyi geri döndürür

# Anahtar üretme ve dosyayı şifreleme işlemleri
generate_key()  # Yeni bir anahtar üret ve dosyaya kaydeder
key = load_key()  # Anahtarı dosyadan yükler
encrypt_file("muhammed.txt", key)  # Belirtilen dosyayı şifreler
