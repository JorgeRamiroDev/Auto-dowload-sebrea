import os
import PyPDF2
import pandas as pd



"""ETL FEITO NOS DADOS DE TEXTOS"""
def processar_pasta_pdfs(caminho_pasta, caminho_csv):
    # Verifica se o diretório existe
    if not os.path.isdir(caminho_pasta):
        print("Erro: O caminho da pasta especificado não existe ou não é um diretório.")
        return

    # Lista todos os arquivos PDF na pasta
    arquivos_pdf = [f for f in os.listdir(caminho_pasta) if f.lower().endswith('.pdf')]

    if not arquivos_pdf:
        print("Nenhum arquivo PDF encontrado na pasta especificada.")
        return

    dados = []
    id_atual = 1  # Inicia o ID em 1

    for arquivo in arquivos_pdf:
        caminho_completo = os.path.join(caminho_pasta, arquivo)
        print(f"Processando: {arquivo}")

        try:
            # Extrai o nome do documento conforme especificado
            nome_sem_extensao = os.path.splitext(arquivo)[0]  # Remove a extensão ".pdf"
            nome_documento = nome_sem_extensao.replace('-', ' ').lower()  # Substitui '-' por ' ' e converte para minúsculas

            # Abre o arquivo PDF no modo de leitura binária
            with open(caminho_completo, 'rb') as arquivo_pdf:
                leitor_pdf = PyPDF2.PdfReader(arquivo_pdf)
                texto_total = ""

                for num_pagina, pagina in enumerate(leitor_pdf.pages, start=1):
                    texto = pagina.extract_text()
                    if texto:
                        texto_total += texto + "\n"
                    else:
                        texto_total += f"[Sem texto extraível na página {num_pagina}]\n"

            # Adiciona o nome do documento no início do texto
            texto_total = f"nome do documento: {nome_documento}\n{texto_total.strip()}"

            # Adiciona os dados ao conjunto
            dados.append({
                'id': id_atual,
                'nome_documento': nome_documento,
                'txt': texto_total
            })
            print(f"Arquivo '{arquivo}' processado com sucesso.\n")
            id_atual += 1

        except Exception as e:
            print(f"Erro ao processar o arquivo '{arquivo}': {e}\n")
            continue  # Continua com o próximo arquivo

    # Cria o DataFrame
    df = pd.DataFrame(dados, columns=['id', 'nome_documento', 'txt'])

    # Salva o DataFrame no arquivo CSV
    try:
        df.to_csv(caminho_csv, index=False, encoding='utf-8')
        print(f"Todos os PDFs foram processados. O arquivo CSV foi salvo em: {caminho_csv}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo CSV: {e}")

if __name__ == "__main__":
    print("=== Conversor de PDFs para CSV ===\n")

    # Solicita ao usuário o caminho da pasta contendo os PDFs
    caminho_pasta = f"downloads_pdfs"

    # Solicita ao usuário o caminho onde o CSV será salvo
    caminho_csv = f'final_csv.csv'

    # Verifica se o caminho do CSV possui a extensão .csv
    if not caminho_csv.lower().endswith('.csv'):
        print("O caminho do arquivo CSV deve terminar com a extensão '.csv'. Adicionando automaticamente.")
        caminho_csv += '.csv'

    # Processa a pasta de PDFs e gera o CSV
    processar_pasta_pdfs(caminho_pasta, caminho_csv)
