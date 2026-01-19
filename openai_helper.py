# openai_helper.py

import os
from functools import lru_cache
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from openai import AzureOpenAI


# ✅ Load variables from .env
load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
KEY_VAULT_URL = os.getenv("KEY_VAULT_URL")


def get_kv_secret_client():
    """Authenticate and create Key Vault Secret client."""
    if not all([TENANT_ID, CLIENT_ID, CLIENT_SECRET, KEY_VAULT_URL]):
        raise ValueError("Missing one or more env variables. Check your .env file.")

    credential = ClientSecretCredential(
        tenant_id=TENANT_ID,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET
    )
    return SecretClient(vault_url=KEY_VAULT_URL, credential=credential)


@lru_cache(maxsize=1)
def fetch_openai_secrets():
    """
    Fetch Azure OpenAI / AI Foundry secrets from Key Vault.
    Secret names are provided in assignment.
    """
    client = get_kv_secret_client()

    deployment_name = client.get_secret("interview-openai-deployment-name").value
    model_name = client.get_secret("interview-openai-model-name").value
    api_key = client.get_secret("interview-openai-model-api-key").value
    endpoint = client.get_secret("interview-openai-model-endpoint").value

    return {
        "deployment_name": deployment_name,
        "model_name": model_name,
        "api_key": api_key,
        "endpoint": endpoint
    }


@lru_cache(maxsize=1)
def get_azure_openai_client():
    """Create AzureOpenAI client using secrets fetched from key vault."""
    secrets = fetch_openai_secrets()

    client = AzureOpenAI(
        api_key=secrets["api_key"],
        azure_endpoint=secrets["endpoint"],
        api_version="2024-02-15-preview"
    )

    return client, secrets["deployment_name"]
