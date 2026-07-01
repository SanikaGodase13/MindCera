from app.services.gemini_service import GeminiService

gemini = GeminiService()

response = gemini.generate_response(
    "I feel anxious about my future."
)

print(response)