# openai_helper.py

import os
from functools import lru_cache
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from openai import AzureOpenAI

# ❌ DO NOT use load_dotenv() in deployment

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
KEY_VAULT_URL = os.getenv("KEY_VAULT_URL")


def get_kv_secret_client():
    if not all([TENANT_ID, CLIENT_ID, CLIENT_SECRET, KEY_VAULT_URL]):
        raise RuntimeError("Missing Azure credentials in environment variables")

    credential = ClientSecretCredential(
        tenant_id=TENANT_ID,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )

    return SecretClient(
        vault_url=KEY_VAULT_URL,
        credential=credential
    )


@lru_cache(maxsize=1)
def fetch_openai_secrets():
    client = get_kv_secret_client()

    return {
        "deployment_name": client.get_secret("interview-openai-deployment-name").value,
        "model_name": client.get_secret("interview-openai-model-name").value,
        "api_key": client.get_secret("interview-openai-model-api-key").value,
        "endpoint": client.get_secret("interview-openai-model-endpoint").value,
    }


@lru_cache(maxsize=1)
def get_azure_openai_client():
    secrets = fetch_openai_secrets()

    client = AzureOpenAI(
        api_key=secrets["api_key"],
        azure_endpoint=secrets["endpoint"],
        api_version="2024-02-15-preview"
    )

    return client, secrets["deployment_name"]
