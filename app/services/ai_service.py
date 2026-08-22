import requests

from config import Config


class AIServiceError(Exception):
    pass


class AIService:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "openai/gpt-oss-20b"
        
    def _sistem_talimati(self):
        return Config.BUSINESS_CONTEXT.strip()

    def yanit_uret(self, mesaj, gecmis=None):
        if not mesaj or not mesaj.strip():
            raise AIServiceError("Mesaj boş olamaz.")

        messages = [
            {
                "role": "system",
                "content": self._sistem_talimati(),
            }
        ]

        if gecmis:
            messages.extend(gecmis)

        messages.append(
            {
                "role": "user",
                "content": mesaj.strip(),
            }
        )

        try:
            response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": messages,
                },
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()

            ham_cevap = data["choices"][0]["message"]["content"]

            kontrol_response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": """
Sen yalnızca Türkçe yazım denetimi yapan bir editörsün.

Sana verilen metnin anlamını değiştirme.
Yeni bilgi ekleme veya bilgi çıkarma.
Soruların içeriğini değiştirme.
Satır düzenini mümkün olduğunca koru.
Markdown, yıldız, tablo veya yeni biçimlendirme ekleme.

Yalnızca:
- Türkçe yazım hatalarını,
- yanlış yazılmış kelimeleri,
- büyük ve küçük harf hatalarını,
- noktalama işaretlerini,
- noktalama sonrası cümle başlangıçlarını,
- ürün ve aksesuar isimlerindeki yazım hatalarını

düzelt.

Örneğin "kolya" yazıyorsa "kolye" yap.
Sadece düzeltilmiş metni döndür.
""".strip(),
                        },
                        {
                            "role": "user",
                            "content": ham_cevap,
                        },
                    ],
                    "temperature": 0,
                },
                timeout=30,
            )

            kontrol_response.raise_for_status()

            kontrol_data = kontrol_response.json()

            return kontrol_data["choices"][0]["message"]["content"].strip()
        except requests.RequestException as error:
            raise AIServiceError(
                "Yapay zeka servisine şu anda ulaşılamıyor."
            ) from error

        except (KeyError, IndexError, TypeError, ValueError) as error:
            raise AIServiceError(
                "Yapay zeka servisinden beklenmeyen bir yanıt geldi."
            ) from error


ai_service = AIService()