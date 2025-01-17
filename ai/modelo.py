import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Carregar as fichas do CSV
def load_fichas(csv_path):
    return pd.read_csv(csv_path)

# 2. Pré-processar os textos
def preprocess_text(text):
    # Para simplificar, apenas convertemos para minúsculas. Pode-se adicionar mais etapas aqui.
    return text.lower()

# 3. Calcular similaridade e recomendar fichas
def recommend_fichas(user_input, fichas_df, top_n=3):
    # Pré-processar os textos
    fichas_df['txt_processed'] = fichas_df['txt'].apply(preprocess_text)
    user_input_processed = preprocess_text(user_input)

    # Vetorização TF-IDF
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_df=0.80)

    tfidf_matrix = vectorizer.fit_transform(fichas_df['txt_processed'])
    user_vector = vectorizer.transform([user_input_processed])

    # Similaridade Coseno
    similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()

    # Ordenar as fichas por similaridade
    fichas_df['similarity'] = similarities
    recommended_fichas = fichas_df.sort_values(by='similarity', ascending=False).head(top_n)

    return recommended_fichas[['id', 'nome_documento', 'similarity']]