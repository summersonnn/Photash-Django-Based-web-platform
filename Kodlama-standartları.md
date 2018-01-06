# Kodlama Standartları

Kaynak kodlarının okunulabilirliği ve diğer geliştiriciler tarafından sorunsuz bir şekilde anlaşılması için birkaç kodlama standartlarına uymak gerekmektedir. 


## Genel Kurallar

- Tab indentation
- Öncelikli olarak tek tırnak, nested durumunda içte tek dışta tek tırnak. 
- Tırnak standardına istisna olarak, html tag attribute'ları için çift tırnak.
- Satır sonlarında gereksiz whitespace yok. (En son koddan sonra alt satıra geçiş)
- Bir değişkenin tanımı, onun kullanıldığı en geniş scope'un en başında yapılır.
- Aynı satırda birden fazla değişken tanımlanması.
- Keyword'lerden sonra ve operator ile argümanlar arasında boşluk.
- Return için fonksiyon sonunu beklemek yok, return edilebilecek en kısa zamanda return.
- İstikrar ve tutarlılık.
- Bir satırda birden fazla import (mümkünse)
- Değişken tipi bool ise ismi "is" ile başlar. İkinci kelime büyük harf ile başlar. Aşağıdaki adlandırma standartları kısmındaki değişken isimleri kuralına istisnadır. (Örnek: isPremium) 
- Virgül-boşluk-kodun devamı. (Örnek için alttaki fonksiyonun aldığı parametrelere bakın)
- if bloğu başlamadan önce bir boşluk, else bloğu bittikten sonra bir boşluk bırakılır.
- Template dosyalarında template taglarından sonra indentation yapılır. Yani template taglarına ve içindekilere(for, if veya custom tag) python kodu muamelesi yapılır.


Örnek:

```python
def silly_function(number1, number2, number3, isOkay) 
  sum = number3
  
  if isOkay: 
    return 0
	
  for x in range(0, 3):
    sum = sum + x * (number1 + number2 + number3)

  return sum

```


## Yorum satırları

- Kod ile yorumu aynı satırda yapmak yerine yorum satırını farklı bir satırda tek başına, açıkladığı kod satırından önce yapın.
- İstisna olarak, art arda durması göze daha hoş gelen bazı kısımlarda (örneğin model tanımlamaları, import vs.) kod ile aynı satırda yapın.
- İstisna durumlarda yorum, koddan bir boşluk sonra başlar.
- Çok uzun yorum satırı ikiye bölünüp, kalan kısım aşağı satıra yazılır. (Yukarıda belirtilen istisnai durum varsa bölünmez)

Örnek:

```python
#Koddan önce yorum.
def mymodel_delete(sender, instance, **kwargs):
        # Pass false so FileField doesn't save the model.
        instance.photoItself.delete(False)
        
#İstisna durumlar.
class Photo(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='Photo id') #Aynı fotoğraf farklı contestlerde farklı id'ye sahip olacağından tek primary key photoid (belki bunu değiştirebilirim)
    uploading_date = models.DateTimeField(default=datetime.now, verbose_name="Yüklenme Tarihi") #auto_now_add=True, koymaya çalıştım fakat default istedi. default ile ikisini aynı anda koymama da izin vermedi. sadece default koyabildim.
    ratings = GenericRelation(Rating, related_query_name='photos')
       
```
## Adlandırma standartları

* Dosya İsimleri: photopool

* Klasör İsimleri: Photopool

* Class İsimleri (tek kelime): Photo

* Class İsimleri (uzun): PhotoPool

* Değişken isimleri: photopool

* Değişken isimleri (uzun): photopool_size

* Fonksiyonlar (tek kelime): photo

* Fonksiyonlar (uzun): photo_pool

* Constants: PHOTO_POOL

## Class stili

- Class fonksiyonları arasında 1 boş satır. İlk fonksiyondan önce de 1 boş satır.

- Class'ın bitişinde, class'a ait son koddan sonra 1 boş satır.

- Class memberlar'ının yorum satırları aynı satıra eklenir.

## Fonksiyon stili

- Class fonksiyonları arasında 1 boş satır

- Fonksiyon genel bilindik bir şey return ediyorsa get_ ile başlar.

- Fonksiyonun amacı yorum satırı olarak eklenecekse fonksiyondan bir üst satıra eklenir.

Örnek:

```python
    
    #Fotoğrafın detail url'sini döndürür.
    def get_absolute_url(self):
        return reverse('contest:detail', kwargs={'slug': self.slug})
       
```





