from ai.modelo import load_fichas, recommend_fichas


if __name__ == "__main__":
    csv_path = "final_csv.csv"  # Caminho para o CSV com as fichas
    fichas_df = load_fichas(csv_path)
    user_input = input("Digite sua necessidade: ")
    recommendations = recommend_fichas(user_input, fichas_df)

    print("\nAs 3 fichas mais recomendadas:")
    print(recommendations)