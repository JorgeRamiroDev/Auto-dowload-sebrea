from ai.modelo import load_fichas, recommend_fichas
from etl_att.clear_text import limpar_texto
import os
from groq import Groq

def main():
    # Inicializa o cliente Groq com a chave de API
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    
    csv_path = "final_csv.csv"  # Caminho para o CSV com as fichas
    
    # Carrega as fichas do CSV
    fichas_df = load_fichas(csv_path)
    
    # Obtém a entrada do usuário
    user_input = input("Digite sua necessidade: ")
    
    # Recomenda fichas com base na entrada do usuário
    result = recommend_fichas(user_input, fichas_df)
    print(result)
    # Seleciona as colunas relevantes e limpa o texto
    recommendations = result[["nome_documento", "txt"]].copy()
    recommendations['txt'] = recommendations['txt'].apply(limpar_texto)
    
    # Concatena os textos das fichas recomendadas em uma única string
    texto_doc = ' '.join(recommendations["txt"].tolist())
    nome_cod = " ".join(recommendations["nome_documento"].tolist())
    

    
    # Cria a mensagem para a API de completions
    mensagem = f"Faça um resumo de no máximo 200 palavras sobre o conteudo do texto a seguir: {texto_doc}, obrigatoriamente junto a isso traga {nome_cod}."
    
    try:
        # Solicita a conclusão do chat à API
        chat_completion = client.chat.completions.create(
            messages=[
                {
            "role": "system",
            "content": "Você é um consultor de negócios"
                 },
                {
                    "role": "user",
                    "content": mensagem,
                }
            ],
            model="llama3-8b-8192",  # Verifique se o nome do modelo está correto
            temperature=0.8,
            max_completion_tokens=1024,
            top_p=1,

        )
        
        # Imprime a resposta da API
        print("Descrição da ficha:")
        print(chat_completion.choices[0].message.content)
        
    except Exception as e:
        print("Ocorreu um erro ao se comunicar com a API:", e)

if __name__ == "__main__":
    main()
