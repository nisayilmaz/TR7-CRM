# TR7 CRM Kullanım Dokümantasyonu

- ************************Dosya Dizini************************
    
    TR7 CRM iki ana dosya dizininden oluşur. Bunlardan biri backend (crm) diğeri ise frontend (frontend) içindir. 
    
    ![Untitled](TR7%20CRM%20Kullan%C4%B1m%20Doku%CC%88mantasyonu%20c4b017d97a8f48af8ad1f91d541a901c/Untitled.png)
    
    - **Arka Yüz**
        
        Django uygulamaları projenin belirli bir işlevselliğini veya bölümünü temsil eder ve bağımsız bir şekilde çalışabilir. CRM üç farklı uygulama içerir. Bunlardan “crm” isimli olan otomatik olarak oluşturulan ana uygulama, “relations” ve “accounts” ise fonksiyonaliteyi sağlamak için sonradan eklenen uygulamalardır. Bunun dışındaki dizinler ise “media”, “staticfiles” ve “templates” dizinleridir. “media” dizininde arayüz aracılığıyla eklenen resim, dosya v.b bulunur. “templates” dizininde ise html dosyaları bulunur. CRM uygulamasının ön yüzü vue.js ile yapıldığı için “templates” dizininde sadece “index.html” bulunur. “staticfiles” dizini ise collectstatic komutu ile bir araya getirilen tüm statik dosyaları içerir. Bunun dışında arka yüz dizininde bulunan diğer dosyalar veritabanı dosyası (sqlite dosyası), çevre değişkenleri dosyası, gereksinimler dosyası ve Django komut satırı aracıdır.
        
        ![Untitled](TR7%20CRM%20Kullan%C4%B1m%20Doku%CC%88mantasyonu%20c4b017d97a8f48af8ad1f91d541a901c/Untitled%201.png)
        
    - **Ön Yüz**
        
        TR7 CRM’in ön yüzü vue.js ile geliştirilmiştir ve hazır bir şablon kullanılmıştır ([https://www.creative-tim.com/product/vue-soft-ui-dashboard](https://www.creative-tim.com/product/vue-soft-ui-dashboard)). Ön yüz dizinin içinde kaynak kod “src” dizininin içinde bulunur.
        
        ![Untitled](TR7%20CRM%20Kullan%C4%B1m%20Doku%CC%88mantasyonu%20c4b017d97a8f48af8ad1f91d541a901c/Untitled%202.png)
        
- **********Kurulum**********
    - Debian 10 Python 3.9 Kurulumu
        
        [https://linuxize.com/post/how-to-install-python-3-9-on-debian-10/](https://linuxize.com/post/how-to-install-python-3-9-on-debian-10/)
        
        ```bash
        su
        apt update
        apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev
        wget https://www.python.org/ftp/python/3.9.1/Python-3.9.1.tgz
        tar -xf Python-3.9.1.tgz
        cd Python-3.9.1
        ./configure --enable-optimizations
        make -j 2
        make altinstall
        ```
        
        Bu adımları tamamladıktan sonra 
        
        ```bash
        python3.9 --version
        ```
        
        komutu ile başarılı olup olmadığı kontrol edilebilir.
        
    - Debian 10 Node.js 18.14.2 Kurulumu
        
        ```bash
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
        source ~/.bashrc
        nvm install v18.14.2
        ```
        
    
    Proje https://github.com/nisayilmaz/TR7-CRM.git adresinden
    
    ```jsx
    git clone https://github.com/nisayilmaz/TR7-CRM.git
    ```
    
    komutu ile indirilebilir.
    
    Projenin kurulumu için gerekli olan ilk adım gereksinimlerin indirilmesidir. Arka yüz geneksinimleri “requirements.txt” dosyasının olduğu dizinde
    
    ```jsx
    pip install -r requirements.txt
    ```
    
    komutu ile indirilebilir. Ön yüz gerenksinimleri ise “frontend” dizininde 
    
    ```jsx
    npm install
    npm i
    ```
    
    komutlarından biri ile indirilebilir. Veritabanı dosyasını oluşturmak için ise
    
    ```jsx
    python manage.py makemigrations
    python manage.py migrate
    ```
    
    komutları çalıştırılmalıdır. Bunun ardından ürünleri veritabanına eklemek için 
    
    ```bash
    python manage.py register_product
    ```
    
    komutu çalıştırılmalı. Eğer veritabanı yeni oluşturuluduğunda hardcoded şekilde eklenmesi gereken objeler varsa “crm/relations/management/command” dizinindeki “register_product.py” dosyası gibi bir komut dosyası oluşturularak bu komut çalıştırılabilir.
    
    - **********************Development**********************
        
        Eğer proje geliştirme için kuruluyorsa “crm” dizininin içindeki “.env” dosyadındaki ayarlar 
        
        ```jsx
        DEBUG = True
        DEVELOPMENT_MODE = True
        ```
        
        şeklinde olmalıdır. Django’nun geliştirme sunucusu yine “crm” dizininin içinde (manage.py dosyası ile aynı dizinin içinde iken)
        
        ```jsx
        python manage.py runserver
        ```
        
        şeklinde çalıştırılabilir. Bu sunucu eğer bir port verilmezse 8000 portunda çalışmaya başlar.
        
        ```jsx
        python manage.py runserver 5000 
        ```
        
        komutu ile istenilen portta çalıştırılabilir. Arka yüz bu şekilde çalıştırıldıktan sonra ön yüzde “frontend/src/utils/utils.js” dosyasında
        
        ```jsx
        let isDev = import.meta.env.DEV
        const serverUrl = isDev ? "http://localhost:5000" : ""
        ```
        
        "http://localhost:5000" kısmı değiştirilerek istenen port belirlenmelidir. Bunun ardından 
        
        ```jsx
        npm run dev
        ```
        
        komutu ile vue.js uygulaması çalıştırılır.
        
    - ****************Deployment****************
        
        Eğer proje deployment için kuruluyorsa  veya değişiklikler yapıldıysa “crm” dizininin içindeki “.env” dosyadındaki ayarlar 
        
        ```jsx
        DEBUG = False
        DEVELOPMENT_MODE = False
        ```
        
        şeklinde değiştirilmelidir. Bunun ardından vue.js projesi 
        
        ```jsx
        npm run build
        ```
        
        komutu ile derlenmelidir. Derleme işlemi bittiği zaman dosyalar “frontend/dist” dizinine kaydedilecektir.
        
        ![Untitled](TR7%20CRM%20Kullan%C4%B1m%20Doku%CC%88mantasyonu%20c4b017d97a8f48af8ad1f91d541a901c/Untitled%203.png)
        
        Derleme işlemi bittikten sonra “dist” dizini içerisindeki “index.html” dosyası “crm/templates” dizinine kopyalanmalı. Bunun ardından 
        
        ```jsx
        <link rel="icon" href="/favicon.ico" />
        <script type="module" crossorigin src="/assets/index.657ba752.js"></script>
        <link rel="stylesheet" href="/assets/index.984f8f88.css">
        ```
        
        satırlarına sırasıyla 
        
        ```jsx
        **{% load static %}**
        <link rel="icon" href=**"{% static '**/favicon.ico**' %}**" />
        <script type="module" crossorigin src="**{% static '**/assets/index.657ba752.js**' %}**"></script>
        <link rel="stylesheet" href="**{% static '**/assets/index.984f8f88.css**' %}**">
        ```
        
        altı çizili eklemeler yapılmalı.
        
        Ardından “crm” dizini içinde
        
        ```bash
        gunicorn crm.wsgi [ip]:[port]
        ```
        
        komutu kullanılarak uygulama deploy edilebilir.
        
- ****************Düzenleme****************
    
    TR7 CRM’in arka yüzünde değişiklikler için “crm/crm” dizinindeki dosyalardan yapılır. Burada daha önceden de bahsedilen Django uygulamaları bulunur. Kurumları, kişileri ve fırsatları yönetmek için olan apiler “relations” uygulamasının içinde yer alırken kullanıcı hesaplarını yönetmek için olanlar “accounts” uygulamasında yer alır. Değişikliler genelde bir uygulamanın “models”, “views”, “urls” ve “serializers” dosyalarını değiştirmeyi gerektirir. 
    
    1. **Modeller**
        
        “models” dosyasında veritabanındaki tablolar oluşturulur. Bu dosyadaki her bir sınıf tanımı veritabanında bir tabloya denk gelir. Örnek olarak “company” tablosu aşağıdaki gibidir.
        
        ```bash
        ROLES = (
            ('client', 'Son Kullanıcı'),
            ('partner', 'İş Ortağı'),
        )
        
        class Company(models.Model):
            name = models.CharField(max_length=255)
            role = models.CharField(max_length=7, choices=ROLES)
            email = models.EmailField(null=True, blank=True)
            phone = models.CharField(max_length=25, null=True, blank=True)
            address = models.CharField(max_length=255, null=True, blank=True)
            registered_by = models.ForeignKey(to=CustomUser, blank=True, null=True, on_delete=models.PROTECT)
        ```
        
        Modellerle ilgili detaylı bilgi için [https://docs.djangoproject.com/en/4.2/topics/db/models/](https://docs.djangoproject.com/en/4.2/topics/db/models/) sayfasına bakılabilir. Modellerle ilgili bir değişiklik yapıldığında bu değişikliklerin veritabanına yansıması için 
        
        ```jsx
        python manage.py makemigrations
        python manage.py migrate
        ```
        
        komutları çalıştırılmalı.
        
    2. **Görünümler**
        
        “views” dosyası ise gönderilen taleplere yanıt vermek için kullanılır. Bir Django görünümü (view), bir Python fonksiyonu veya sınıfı olarak tanımlanabilir. TR7 CRM’de genellikle görünümler sınıf olarak tanımlanmıştır. Görünümlerle ilgili daha fazla bilgiye [https://www.django-rest-framework.org/api-guide/views/](https://www.django-rest-framework.org/api-guide/views/) adresinden ulaşılabilir. Görünüm yazmak için aşağıdakine benzer bir yapı kullanılabilir 
        
        ```python
        class MyApiView(APIView):
        		# Kimlik doğrulama gerektiren görünümler için bu iki satır kullanılmalı.
        		# Eğer istekte token gelmediyse cevap olarak 401 (Unauthorized) döner.
            authentication_classes = [KnoxTokenAuthentication]
            permission_classes = (permissions.IsAuthenticated,)
        
        		# Sınıf görünmlerin içerisine gerekli olan tüm HTTP metotları 
        		# (get,post, put, delete) yazılabilir.
            def get(self, request, *args, **kwargs):
                # Gerekli olan işlemler
                return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
        
           
        ```
        
    3. **URLler**
        
        Hangi görünümlere hangi URL üzerinden ulaşılacağını belirlemek için ise “urls.py” dosyası kullanılır. Burada bir url ile bir görğnğm eşleştirilir. Bir Django projesinde, genellikle her uygulamanın kendi "urls.py" dosyası bulunur. Bu, projenizi modüler ve yönetilebilir hale getirir. Bir uygulamanın "urls.py" dosyası, yalnızca bu uygulamanın URL yapılandırmasını tanımlar ve daha sonra projenin ana "urls.py” dosyasına dahil edilir. Bu dosya için aşağıdaki gibi bir yapı kullanılarbilir. 
        
        ```python
        urlpatterns = [
            path('my_endpoint/', MyApiView.as_view()),
        ]
        ```
        
    4. **Serializerlar**
        
        Django, web tabanlı API'lar oluştururken veri dönüşümü (serialization) işlemlerini yönetmek için "serializers" adında bir modül sağlar. Bu modül, Django model nesnelerini, JSON gibi veri formatlarına veya diğer veri türlerine dönüştürmeyi ve aynı şekilde geri dönüştürmeyi sağlar. Serileştirme işlemi, veritabanı modelinizden alınan verileri, API taleplerine uygun bir formatta sunmak için kullanılırken, ters serileştirme işlemi ise gelen verileri model nesnelerine çevirerek veritabanına kaydetmeyi kolaylaştırır. Serializer oluşturmak için aşağıdaki gibi bir yapı kullanılabilir.
        
        ```python
        class CompanySerializer(serializers.ModelSerializer):
            class Meta:
                model = Company
        				# Modelin tüm alanları kullanılacaksa 
        				# fields = '__all__'
        				# kullanılabilir
                fields = ['id', 'name']
        ```