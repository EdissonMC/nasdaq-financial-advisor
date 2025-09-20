
import os
from dotenv import load_dotenv
from pinecone import Pinecone

class PineconeService:
    def __init__(self, namespace="default"):
        load_dotenv()
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "financial-docs")
        self.namespace = namespace
        # Nueva API de Pinecone 7.3.0 - sin environment parameter
        self.pc = Pinecone(api_key=self.api_key)
        self.dense_index = self.pc.Index(self.index_name)

    def search(self, query, top_k=2):
        try:
            # Búsqueda con la nueva API de Pinecone
            results = self.dense_index.search(
                namespace=self.namespace,
                query={
                    "top_k": top_k,
                    "inputs": {'text': query}
                }
            )
            
            # Extraer contextos de los resultados
            if results and 'result' in results and 'hits' in results['result']:
                contexts = [hit['fields']['text'] for hit in results['result']['hits'] 
                           if 'fields' in hit and 'text' in hit['fields']]
                return " ".join(contexts) if contexts else "No relevant financial context found."
            else:
                return "No relevant financial context found."
                
        except Exception as e:
            print(f"Error in Pinecone search: {e}")
            return "Financial context not available due to search service error."
if __name__ == "__main__":
    print("==="*30)
    print("Iniciando búsqueda...")
    searcher = PineconeService()
    #query = "how held the shares of american airlines?"
    #query ="How many passengers boarded American Airlines flights in 2020?"
    # query ="What was American Airlines' total available liquidity as of December 31, 2020?"
    # query ="What cost-cutting measures did American Airlines implement in response to the COVID-19 pandemic?"
    # query ="How many team members at American Airlines took early retirement or long-term leave in 2020?"
   
    # APPLE
    #query ="What factors affect the Company's stock price volatility?"
    #query ="How does the Company handle stock repurchases during volatile periods?"
    # query ="What are the Company's expectations regarding dividends and share repurchases?"
    # query ="What factors influence technology company stock performance?"
    # query="How do share repurchase programs work during market fluctuations?"
    # query="Are there any guarantees about future dividend payments?"
    
    # ¿Qué factores afectan la volatilidad del precio de las acciones de la Compañía?
    query ="¿Qué factores afectan la volatilidad del precio de las acciones de la Compañía apple?"
    # ¿Cómo maneja la Compañía las recompras de acciones durante períodos de volatilidad?

    # ¿Cuáles son las expectativas de la Compañía con respecto a los dividendos y la recompra de acciones?

    # ¿Qué factores influyen en el desempeño de las acciones de las empresas tecnológicas?

    # ¿Cómo funcionan los programas de recompra de acciones durante las fluctuaciones del mercado?

    # ¿Existen garantías sobre los pagos futuros de dividendos?
    
    searcher.search(query, top_k=2)
    print("Búsqueda finalizada.")
