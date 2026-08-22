from flask import Blueprint, jsonify, render_template, request

from app.database import lead_ekle, tum_leadler, lead_durum_guncelle, lead_sil as lead_sil_db
from app.services.ai_service import AIServiceError, ai_service


pages_bp = Blueprint("pages", __name__)
api_bp = Blueprint("api", __name__)


@pages_bp.route("/")
def ana_sayfa():
    return render_template("index.html")


@pages_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@api_bp.route("/sohbet", methods=["POST"])
def sohbet():
    data = request.get_json(silent=True) or {}

    mesaj = data.get("mesaj", "").strip()
    gecmis = data.get("gecmis", [])

    if not mesaj:
        return jsonify({
            "basari": False,
            "hata": "Mesaj alanı zorunludur."
        }), 400

    try:
        cevap = ai_service.yanit_uret(mesaj, gecmis)

        return jsonify({
            "basari": True,
            "cevap": cevap
        }), 200

    except AIServiceError as error:
        return jsonify({
            "basari": False,
            "hata": str(error)
        }), 503


@api_bp.route("/leads", methods=["POST"])
def yeni_lead():
    data = request.get_json(silent=True) or {}

    isim = data.get("isim", "").strip()
    telefon = data.get("telefon", "").strip()
    email = data.get("email", "").strip()
    mesaj = data.get("mesaj", "").strip()

    if not isim or not telefon or not email:
        return jsonify({
            "basari": False,
            "hata": "İsim, telefon ve e-mail alanları zorunludur."
        }), 400

    lead_id = lead_ekle(
        isim=isim,
        telefon=telefon,
        email=email,
        mesaj=mesaj
    )

    return jsonify({
        "basari": True,
        "id": lead_id
    }), 201


@api_bp.route("/leads", methods=["GET"])
def lead_listesi():
    leadler = tum_leadler()

    return jsonify({
        "basari": True,
        "leadler": leadler
    }), 200

@api_bp.route("/leads/<int:lead_id>/durum", methods=["PUT"])
def lead_durum_degistir(lead_id):
    data = request.get_json(silent=True) or {}

    durum = data.get("durum", "").strip()

    izinli_durumlar = ["Yeni", "İletişime Geçildi", "Tamamlandı"]

    if durum not in izinli_durumlar:
        return jsonify({
            "basari": False,
            "hata": "Geçersiz durum."
        }), 400

    lead_durum_guncelle(lead_id, durum)

    return jsonify({
        "basari": True,
        "durum": durum
    }), 200


@api_bp.route("/leads/<int:lead_id>", methods=["DELETE"])
def lead_sil(lead_id):
    silindi_mi = lead_sil_db(lead_id)

    if not silindi_mi:
        return jsonify({
            "basari": False,
            "hata": "Lead bulunamadı."
        }), 404

    return jsonify({
        "basari": True,
        "mesaj": "Lead başarıyla silindi."
    }), 200