
import os
from dotenv import load_dotenv
from pinecone import Pinecone

class PineconeService:
    def __init__(self, namespace="default"):
        load_dotenv()
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "financial-docs")
        self.environment = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
        self.namespace = namespace
        self.pc = Pinecone(api_key=self.api_key, environment=self.environment)
        self.dense_index = self.pc.Index(self.index_name)

    def search(self, query, top_k=2):
        results = self.dense_index.search(
            namespace=self.namespace,
            query={
                "top_k": top_k,
                "inputs": {
                    'text': query
                }
            }
        )
        import pprint; 
        #pprint.pprint(results)
        # for hit in results['result']['hits']:
            #print(f"id: {hit['_id']:<5} | score: {round(hit['_score'], 2):<5} | text: {hit['fields']['text']}")
            #print(f"score: {round(hit['_score'], 2):<5} | text: {hit['fields']['text']}")
            #print(f"id: {hit['_id']:<5} | score: {round(hit['_score'], 2):<5} | category: {hit['fields']['category']:<10} | text: {hit['fields']['chunk_text']:<50}")
            
            
            # print(".."*15)
            # print(f" text: {hit['fields']['text']}")
            # print(".."*15)
            
        return " ".join([hit['fields']['text'] for hit in results['result']['hits']])
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
