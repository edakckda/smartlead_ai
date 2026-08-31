# Vela — Akıllı Aksesuar Danışmanı

Vela, vintage ve lüks aksesuar markası için geliştirilmiş yapay zekâ destekli bir müşteri danışmanı ve lead yönetim sistemidir.

Kullanıcılar yapay zekâ asistanına ürünler hakkında soru sorabilir ve iletişim bilgilerini bırakabilir. Kaydedilen müşteri talepleri yönetim panelinde görüntülenebilir.

## Özellikler

- Yapay zekâ destekli Türkçe müşteri danışmanı
- Kullanıcı mesajlarının Groq API üzerinden yanıtlanması
- İsim, telefon ve e-posta ile müşteri talebi oluşturma
- Lead kayıtlarının veritabanında saklanması
- Yönetim panelinde müşteri taleplerinin listelenmesi
- Lead durumlarının görüntülenmesi
- Wix Studio ile hazırlanmış canlı kullanıcı arayüzü
- Render üzerinde yayınlanan Flask backend

## Kullanılan Teknolojiler

- Python
- Flask
- PostgreSQL / SQLite
- Groq API
- Gunicorn
- Wix Studio + Velo
- Git / GitHub
- Render

## Proje Yapısı

```text
smartlead_ai/
│
├── app/
│   ├── services/
│   │   └── ai_service.py
│   ├── templates/
│   ├── __init__.py
│   ├── database.py
│   └── routes.py
│
├── config.py
├── run.py
├── requirements.txt
├── .gitignore
└── README.md
```

Projede sorumluluklar ayrı katmanlara bölünmüştür:

- `config.py`: yapılandırma ve ortam değişkenleri
- `database.py`: veritabanı ve SQL işlemleri
- `ai_service.py`: yapay zekâ servisi
- `routes.py`: HTTP endpointleri
- `__init__.py`: Flask uygulama fabrikası
- `run.py`: uygulamanın giriş noktası

## Ortam Değişkenleri

Uygulamanın çalışması için aşağıdaki ortam değişkenleri kullanılmaktadır:

```text
SECRET_KEY
DATABASE_URL
GROQ_API_KEY
```

Gizli anahtarlar `.env` dosyasında tutulur ve `.gitignore` sayesinde GitHub'a yüklenmez.

## Yerelde Çalıştırma

Sanal ortamı etkinleştirin:

```powershell
.\venv\Scripts\Activate.ps1
```

Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

Uygulamayı başlatın:

```bash
python run.py
```

Yerel adres:

```text
http://127.0.0.1:5000
```

## Canlı Proje

Backend:

```text
https://smartlead-ai-p8pq.onrender.com
```

Sağlık kontrolü:

```text
https://smartlead-ai-p8pq.onrender.com/health
```

Wix arayüzü:

```text
https://edakucuk573.wixstudio.com/vela
```

Yönetim paneli:

```text
https://edakucuk573.wixstudio.com/vela/yonetim-paneli
```

## Proje Amacı

Projenin amacı; yapay zekâ, backend, veritabanı ve Wix arayüzünü birbirinden ayrılmış katmanlarla bir araya getirerek gerçek bir işletme için çalışan müşteri danışmanı ve lead yönetim sistemi oluşturmaktır.