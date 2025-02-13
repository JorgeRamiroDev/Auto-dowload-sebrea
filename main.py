from ai.modelo import load_fichas, recommend_fichas
from crewai import Crew
from crew_agents.agents import consultor_sebrae
from crew_agents.tasks import task


if __name__ == "__main__":
    csv_path = "final_csv.csv"  # Caminho para o CSV com as fichas
    fichas_df = load_fichas(csv_path)
    user_input = input("Digite sua necessidade:")
    recommendations = recommend_fichas(user_input, fichas_df)
    
    nome_doc =  str(recommendations.nome_documento)
    print (type(nome_doc))
   
    inputs = {"nome_ficha" : "criar website"}
    resultado = rag_crew.kickoff(inputs=inputs)
    
    print(resultado)