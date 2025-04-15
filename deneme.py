# public abstract class Ogrenci
# {
#     public string Isim { get; set; } // Her öğrencinin bir adı olacak        //Property
#     public int Numara { get; set; } // Her öğrencinin bir numarası olacak
#
#     public abstract void DersCalis(); // Her öğrenci ders çalışacak, ama nasıl çalışacağını kendisi belirleyecek
#
#     public void BilgiYazdir()
#     {
#         Console.WriteLine($"Öğrenci: {Isim}, Numara: {Numara}"); // Her öğrenci bilgilerini yazdıracak
#     }
# }
#
# public class BilgisayarMuhendisligiOgrencisi : Ogrenci
# {
#     public override void DersCalis()
#     {
#         Console.WriteLine("Kod yazıyor!"); // Bilgisayar Mühendisliği öğrencisinin ders çalışma şekli
#     }
# }
#
#
# public class TipFakultesiOgrencisi : Ogrenci
# {
#     public override void DersCalis()
#     {
#         Console.WriteLine("Kitap okuyor!"); // Tıp Fakültesi öğrencisinin ders çalışma şekli
#     }
# }
#
#
# public class Program
# {
#     public static void Main()
#     {
#         BilgisayarMuhendisligiOgrencisi bmOgrencisi = new BilgisayarMuhendisligiOgrencisi { Isim = "Ali", Numara = 123 };
#         TipFakultesiOgrencisi tipOgrencisi = new TipFakultesiOgrencisi { Isim = "Ayşe", Numara = 456 };
#
#         bmOgrencisi.BilgiYazdir(); // Çıktı: Öğrenci: Ali, Numara: 123
#         bmOgrencisi.DersCalis(); // Çıktı: Kod yazıyor!
#
#         tipOgrencisi.BilgiYazdir(); // Çıktı: Öğrenci: Ayşe, Numara: 456
#         tipOgrencisi.DersCalis(); // Çıktı: Kitap okuyor!
#     }
# }
