from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv, find_dotenv
import os

# See https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python

# Read and write YAML config file for authentication
account_url = os.getenv("BLOB_ACCOUNT_URL", "https://rbrandswebstorage.blob.core.windows.net/")
container_name = "streamlit-example"
config_blob_name = "config.yaml"
default_credential = DefaultAzureCredential()

def read_authentication_config():
    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)
    container_client = blob_service_client.get_container_client(container=container_name)
    config = container_client.download_blob(config_blob_name).readall()
    return config

def write_authentication_config(config):
    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)
    container_client = blob_service_client.get_container_client(container=container_name)
    config = container_client.upload_blob(config_blob_name, config, overwrite=True)

# Read and write a blob from/to configured storage container

def read_blob(blob_name):
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)
    container_client = blob_service_client.get_container_client(container=container_name)
    content = container_client.download_blob(blob_name).readall()
    return content

def write_blob(blob_name, content):    
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)
    container_client = blob_service_client.get_container_client(container=container_name)
    content = container_client.upload_blob(blob_name, content, overwrite=True)
