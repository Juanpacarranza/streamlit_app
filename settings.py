from dotenv import load_dotenv
import os

load_dotenv()

print(os.getenv('PROD_AZURE_CLIENT_ID'))

environment = os.getenv('ENVIRONMENT', 'dev').lower()

if environment == 'prod':
    CLIENT_ID = os.getenv('PROD_AZURE_CLIENT_ID')
    TENANT_ID = os.getenv('PROD_AZURE_TENANT_ID')
    CLIENT_SECRET = os.getenv('PROD_AZURE_CLIENT_SECRET')
else:
    CLIENT_ID = os.getenv('DEV_AZURE_CLIENT_ID')
    TENANT_ID = os.getenv('DEV_AZURE_TENANT_ID')
    CLIENT_SECRET = os.getenv('DEV_AZURE_CLIENT_SECRET')

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
# REDIRECT_PATH = "/getAToken" 
# SCOPES = ["https://graph.microsoft.com/.default"] 
SCOPES = ["User.Read"]

if not all([CLIENT_ID, TENANT_ID, CLIENT_SECRET]):
    if CLIENT_ID is None:
        'No hay CLIENT_ID'
    else:
        print(CLIENT_ID)
        
    if TENANT_ID is None:
        'No hay TENANT_ID'
    else:
        print(TENANT_ID)
        
    if CLIENT_SECRET is None:
        'No hay CLIENT_SECRET'
    else:
        print(CLIENT_SECRET)
        
    raise ValueError("One or more environment variables have not been configured correctly.")
