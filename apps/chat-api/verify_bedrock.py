import boto3
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def verify_bedrock_access():
    try:
        # Crear cliente Bedrock
        client = boto3.client(
            'bedrock',
            region_name=os.getenv('AWS_REGION'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        
        # Listar modelos disponibles
        response = client.list_foundation_models()
        print("✅ Conexión a Bedrock exitosa!")
        print(f"✅ Modelos disponibles: {len(response['modelSummaries'])}")
        
        # Verificar Claude específicamente
        claude_models = [
            model for model in response['modelSummaries'] 
            if 'claude' in model['modelId'].lower()
        ]
        
        if claude_models:
            print("✅ Modelos Claude disponibles:")
            for model in claude_models:
                print(f"   - {model['modelId']}")
        else:
            print("❌ No se encontraron modelos Claude disponibles")
            print("   Verifica que tengas acceso aprobado a los modelos Anthropic")
            
    except Exception as e:
        print(f"❌ Error conectando a Bedrock: {e}")
        print("   Verifica tus credenciales AWS y permisos")

if __name__ == "__main__":
    verify_bedrock_access()