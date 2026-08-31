import requests

from config import Config


class AIServiceError(Exception):
    pass


class AIService:
    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.1-8b-instant"
        self.fallback_model = "openai/gpt-oss-20b"
        
    def _sistem_talimati(self):
        return Config.BUSINESS_CONTEXT.strip()

    def yanit_uret(self, mesaj, gecmis=None):
        if not mesaj or not mesaj.strip():
            raise AIServiceError("Mesaj boş olamaz.")
        if not self.api_key:
            return "Demo modu: Yapay zekâ servisi şu anda bağlı değil."

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
            if response.status_code == 404:
                response = requests.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.fallback_model,
                        "messages": messages,
                    },
                    timeout=30,
    )

            response.raise_for_status()

            data = response.json()

            ham_cevap = data["choices"][0]["message"]["content"]
            return ham_cevap.strip()
        
        except requests.RequestException as error:
            raise AIServiceError(
                "Yapay zeka servisine şu anda ulaşılamıyor."
            ) from error
        except (KeyError, IndexError, TypeError, ValueError) as error:
            raise AIServiceError(
                "Yapay zeka servisinden beklenmeyen bir yanıt geldi."
            ) from error

ai_service = AIService()