# Zero Knowledge Authentication System
## Demo Flow

`Register → Login → JWT Token → Protected Endpoint → Secure Access Granted`

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-REST_API-black)
![JWT](https://img.shields.io/badge/Auth-JWT-green)
![Swagger](https://img.shields.io/badge/API-Swagger-brightgreen)
![License](https://img.shields.io/badge/License-MIT-orange)

Flask tabanlı, JWT destekli, bcrypt ile güvenli hale getirilmiş, REST API ve Swagger dokümantasyonu içeren modern bir kimlik doğrulama sistemi.

Bu proje, kullanıcıların gizli bilgilerini doğrudan paylaşmadan kimlik doğrulama mantığını öğrenmek ve güvenli backend authentication akışını uygulamak amacıyla geliştirilmiştir.

---

## Özellikler

- JWT tabanlı kimlik doğrulama
- bcrypt + salt ile güvenli hashleme
- SQLite veritabanı entegrasyonu
- REST API mimarisi
- Swagger/OpenAPI dokümantasyonu
- Authorization Header ile korunan endpoint
- Challenge-response doğrulama mantığı
- Modern HTML/CSS arayüz
- Thunder Client ile API testleri

---

## Kullanılan Teknolojiler

- Python
- Flask
- SQLite
- bcrypt
- PyJWT
- Flasgger / Swagger
- HTML5
- CSS3
- Thunder Client

---

## Proje Yapısı

```bash
zero-knowledge-auth-system/
│
├── screenshots/
├── static/
│   └── style.css
├── templates/
│   ├── dashboard.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── result.html
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Kurulum ve Çalıştırma

```bash
git clone https://github.com/ikrabaser/zero-knowledge-auth-system.git
cd zero-knowledge-auth-system
pip install -r requirements.txt
python app.py
```

Uygulama:

```bash
http://127.0.0.1:5000
```

Swagger dokümantasyonu:

```bash
http://127.0.0.1:5000/apidocs
```

## Bu Projede Kazandıklarım

- REST API mimarisi geliştirme deneyimi
- JWT tabanlı authentication akışını uygulama
- bcrypt ile güvenli parola hashleme mantığını öğrenme
- Swagger ile API dokümantasyonu hazırlama
- Authorization header kullanımı
- Protected endpoint yapısı geliştirme
- API test süreçlerinde Thunder Client kullanımı
- Flask backend proje organizasyonu
- Güvenlik odaklı backend geliştirme yaklaşımı
- ---
## Sistem Mimarisi

```mermaid
flowchart LR

A[Kullanıcı / Client] --> B[Flask REST API]

B --> C[Register Endpoint]
B --> D[Login Endpoint]

D --> E[bcrypt Hash Kontrolü]

E --> F[JWT Token Üretimi]

F --> G[Protected API Endpoint]

G --> H[Authorization Header Kontrolü]

H --> I[SQLite Database]
```

## Authentication Flow

```mermaid
sequenceDiagram

participant User
participant API
participant Database
participant JWT

User->>API: Register / Login Request
API->>Database: Kullanıcı kontrolü
Database-->>API: Hashlenmiş veri
API->>JWT: Token oluştur
JWT-->>API: JWT Token
API-->>User: Authentication Success
User->>API: Protected Endpoint Request
API->>JWT: Token doğrula
JWT-->>API: Valid Token
API-->>User: Access Granted
```
```text
Kullanıcı kayıt olur
        ↓
Gizli bilgi bcrypt + salt ile hashlenir
        ↓
Hash veritabanında saklanır
        ↓
Kullanıcı giriş yapar
        ↓
Challenge-response mantığı çalışır
        ↓
JWT token üretilir
        ↓
Korunan API endpointlerine erişim sağlanır
```
---

## API Endpointleri

| Method | Endpoint | Açıklama |
|---|---|---|
| POST | `/api/register` | API üzerinden kullanıcı kaydı oluşturur |
| POST | `/api/login` | Kullanıcıyı doğrular ve JWT token üretir |
| GET | `/api/profile` | Authorization header ile JWT token doğrular |

---

## Ana Sayfa

![Ana Sayfa](screenshots/home.png)

---

## Kayıt Sonucu

![Kayıt Sonucu](screenshots/register-result.png)

---

## Dashboard ve JWT Token

![Dashboard](screenshots/dashboard.png)

---

## Swagger API Documentation

![Swagger](screenshots/swagger.png)

### Swagger Login Endpoint

![Swagger Login](screenshots/swagger-login.png)

### Swagger Register Endpoint

![Swagger Register](screenshots/swagger-register.png)

### Swagger Profile Endpoint

![Swagger Profile](screenshots/swagger-profile.png)

---

## Thunder Client API Testleri

### API Register Testi

![API Register](screenshots/api-register.png)

### API Login Testi

![API Login](screenshots/api-login.png)

### API Profile Testi

![API Profile](screenshots/api-profile.png)

---

## Güvenlik Özellikleri

Bu projede güvenli authentication akışını göstermek için aşağıdaki yapılar kullanılmıştır:

- Kullanıcı gizli bilgisi açık şekilde saklanmaz.
- bcrypt ile otomatik salt üretilir.
- JWT token ile kimlik doğrulama yapılır.
- `/api/profile` endpointi Authorization header olmadan erişime kapalıdır.
- Token süresi 1 saat olarak ayarlanmıştır.
- Challenge-response mantığı ile doğrulama süreci desteklenmiştir.

---

## Not

Bu proje eğitim ve portfolyo amacıyla geliştirilmiş bir demo authentication sistemidir. Production ortamında kullanılmadan önce secret key yönetimi, environment variable kullanımı, rate limiting, refresh token ve gelişmiş hata yönetimi gibi ek güvenlik önlemleri uygulanmalıdır.

---

## Geliştirici

**Leyla İkra Başer**  
Bilgisayar Mühendisliği Öğrencisi

GitHub: [ikrabaser](https://github.com/ikrabaser)
