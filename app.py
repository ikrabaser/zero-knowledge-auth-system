from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flasgger import Swagger
import sqlite3
import random
import jwt
import datetime
import bcrypt
import hashlib

app = Flask(__name__)
app.secret_key = "zk_auth_secret_key_for_jwt_demo_2026"

swagger = Swagger(app)

DATABASE = "users.db"


def bcrypt_hash_uret(gizli_bilgi):
    return bcrypt.hashpw(
        gizli_bilgi.encode(),
        bcrypt.gensalt()
    ).decode()


def bcrypt_dogrula(gizli_bilgi, kayitli_hash):
    return bcrypt.checkpw(
        gizli_bilgi.encode(),
        kayitli_hash.encode()
    )


def sha256_uret(veri):
    return hashlib.sha256(veri.encode()).hexdigest()


def veritabani_olustur():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            public_hash TEXT
        )
    """)

    conn.commit()
    conn.close()


def token_uret(kullanici_adi):
    return jwt.encode(
        {
            "username": kullanici_adi,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        app.secret_key,
        algorithm="HS256"
    )


def kullanici_hash_getir(kullanici_adi):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT public_hash
        FROM users
        WHERE username = ?
    """, (kullanici_adi,))

    sonuc = cursor.fetchone()
    conn.close()

    return sonuc


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        kullanici_adi = request.form["username"]
        gizli_bilgi = request.form["secret"]

        public_hash = bcrypt_hash_uret(gizli_bilgi)

        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO users (username, public_hash)
                VALUES (?, ?)
            """, (kullanici_adi, public_hash))

            conn.commit()
            conn.close()

            mesaj = "Kayıt başarılı. Gizli bilgi bcrypt + salt ile veritabanına kaydedildi."

        except sqlite3.IntegrityError:
            mesaj = "Bu kullanıcı zaten kayıtlı."

        return render_template("result.html", mesaj=mesaj)

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        kullanici_adi = request.form["username"]
        gizli_bilgi = request.form["secret"]

        sonuc = kullanici_hash_getir(kullanici_adi)

        if sonuc is None:
            return render_template(
                "result.html",
                mesaj="Kullanıcı bulunamadı."
            )

        kayitli_public_hash = sonuc[0]

        if bcrypt_dogrula(gizli_bilgi, kayitli_public_hash):
            challenge = str(random.randint(100000, 999999))
            kanit = sha256_uret(kayitli_public_hash + challenge)
            token = token_uret(kullanici_adi)

            session["username"] = kullanici_adi
            session["token"] = token
            session["challenge"] = challenge
            session["proof"] = kanit

            return redirect(url_for("dashboard"))

        return render_template(
            "result.html",
            mesaj="Kimlik doğrulama başarısız."
        )

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session["username"],
        token=session["token"]
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/api/register", methods=["POST"])
def api_register():
    """
    API ile kullanıcı kaydı
    ---
    tags:
      - Authentication API
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - secret
          properties:
            username:
              type: string
              example: api_user
            secret:
              type: string
              example: "12345"
    responses:
      201:
        description: Kullanıcı başarıyla oluşturuldu
      400:
        description: Eksik veya hatalı JSON veri
      409:
        description: Kullanıcı zaten kayıtlı
    """
    veri = request.get_json()

    if not veri:
        return jsonify({"error": "JSON veri gönderilmedi."}), 400

    kullanici_adi = veri.get("username")
    gizli_bilgi = veri.get("secret")

    if not kullanici_adi or not gizli_bilgi:
        return jsonify({
            "error": "username ve secret alanları zorunludur."
        }), 400

    public_hash = bcrypt_hash_uret(gizli_bilgi)

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (username, public_hash)
            VALUES (?, ?)
        """, (kullanici_adi, public_hash))

        conn.commit()
        conn.close()

        return jsonify({
            "message": "API kaydı başarılı.",
            "username": kullanici_adi
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "Bu kullanıcı zaten kayıtlı."
        }), 409


@app.route("/api/login", methods=["POST"])
def api_login():
    """
    API ile kullanıcı girişi
    ---
    tags:
      - Authentication API
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - secret
          properties:
            username:
              type: string
              example: api_user
            secret:
              type: string
              example: "12345"
    responses:
      200:
        description: Login başarılı, JWT token döner
      400:
        description: Eksik veya hatalı JSON veri
      401:
        description: Kimlik doğrulama başarısız
      404:
        description: Kullanıcı bulunamadı
    """
    veri = request.get_json()

    if not veri:
        return jsonify({"error": "JSON veri gönderilmedi."}), 400

    kullanici_adi = veri.get("username")
    gizli_bilgi = veri.get("secret")

    if not kullanici_adi or not gizli_bilgi:
        return jsonify({
            "error": "username ve secret alanları zorunludur."
        }), 400

    sonuc = kullanici_hash_getir(kullanici_adi)

    if sonuc is None:
        return jsonify({"error": "Kullanıcı bulunamadı."}), 404

    kayitli_public_hash = sonuc[0]

    if not bcrypt_dogrula(gizli_bilgi, kayitli_public_hash):
        return jsonify({"error": "Kimlik doğrulama başarısız."}), 401

    challenge = str(random.randint(100000, 999999))
    proof = sha256_uret(kayitli_public_hash + challenge)
    token = token_uret(kullanici_adi)

    return jsonify({
        "message": "API login başarılı.",
        "username": kullanici_adi,
        "challenge": challenge,
        "proof": proof,
        "token": token
    }), 200


@app.route("/api/profile")
def api_profile():
    """
    JWT token ile kullanıcı profili doğrulama
    ---
    tags:
      - Authentication API
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer JWT_TOKEN formatında token gönderilmelidir.
        example: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    responses:
      200:
        description: Token başarıyla doğrulandı
      401:
        description: Token yok, süresi dolmuş veya geçersiz
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({
            "error": "Authorization header bulunamadı."
        }), 401

    try:
        token = auth_header.split(" ")[1]

        veri = jwt.decode(
            token,
            app.secret_key,
            algorithms=["HS256"]
        )

        return jsonify({
            "message": "Token doğrulandı.",
            "username": veri["username"]
        })

    except jwt.ExpiredSignatureError:
        return jsonify({
            "error": "Token süresi dolmuş."
        }), 401

    except:
        return jsonify({
            "error": "Geçersiz token."
        }), 401


if __name__ == "__main__":
    veritabani_olustur()
    app.run(debug=True)