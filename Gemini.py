import asyncio
import requests
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Certificar de colocar a API do GEMINI no .env
API_KEY = os.getenv("GEMINI_API_KEY")

async def analyze_files_with_gemini(contents_dict, titles_dict):
    output = {}

    try:
        # Iterar sobre os IDs das notícias
        for id_key in contents_dict:
            content = contents_dict[id_key]
            title = titles_dict.get(id_key, "Sem título")

            # Verificar se o conteúdo não está vazio
            if not content.strip():
                output[id_key] = {
                    "title": title,
                    "response": "Conteúdo vazio ou não fornecido."
                }
                continue

            print(f"Analisando conteúdo para {title}...")

            # Configuração da requisição
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {"text": "Quero que me traga um resumo do que é mais importante na notícia abaixo:"},
                            {"text": content}
                        ]
                    }
                ]
            }
            headers = {
                "Content-Type": "application/json"
            }

            # Fazer a requisição POST
            response = requests.post(url, json=payload, headers=headers)

            # Verificar a resposta
            if response.status_code == 200:
                insights = response.json()

                # Extrair apenas o texto da resposta do modelo
                candidates = insights.get("candidates", [])
                if candidates and "content" in candidates[0]:
                    parts = candidates[0]["content"].get("parts", [])
                    if parts:
                        text_response = parts[0].get("text", "Sem resposta.")
                    else:
                        text_response = "Sem resposta."
                else:
                    text_response = "Sem resposta."

                output[id_key] = {
                    "title": title,
                    "response": text_response
                }
            else:
                output[id_key] = {
                    "title": title,
                    "response": f"Erro {response.status_code}: {response.text}"
                }

    except Exception as e:
        print(f"Erro geral: {e}")

    return output

def gemini_analysis(titles,contents):
    results = asyncio.run(analyze_files_with_gemini(contents, titles)) # Executar a função da IA

    # # Teste da IA
    # if __name__ == "__main__":
    #     # Dicionários de exemplo
    #     contents = {
    #         "news1": "Este é o conteúdo da primeira notícia.",
    #         "news2": "Este é o conteúdo da primeira notícia.",
    #         "news3": "Este é o conteúdo da primeira notícia.",
    #     }
    #     titles = {
    #         "news1": "Título da Notícia 1",
    #         "news2": "Título da Notícia 2",
    #         "news3": "Título da Notícia 3"
    #     }

    #     # Exibir os resultados
    #     for key, value in results.items():
    #         print(f"\nID: {key}")
    #         print(f"Título: {value['title']}")
    #         if "response" in value:
    #             print(f"Resposta: {value['response']}")
    #         else:
    #             print(f"Erro: {value['error']}")
    return results