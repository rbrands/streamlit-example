from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Read YAML config file for authentication
def read_authentication_config():
    account_url = "https://rbrandswebstorage.blob.core.windows.net/"
    container_name = "streamlit-example"
    config_blob_name = "config.yaml"
    default_credential = DefaultAzureCredential()

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)
    container_client = blob_service_client.get_container_client(container=container_name)
    config = container_client.download_blob(config_blob_name).readall()
    return config
