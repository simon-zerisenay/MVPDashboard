from azure.storage.blob import BlobServiceClient
import os
 
# Replace YOUR_CONNECTION_STRING with your actual Azure Blob Storage connection string
connection_string = "DefaultEndpointsProtocol=https;AccountName=pistoragefrc1;AccountKey=0JfcY7Sg9tyRMLeaupyQBO3S3UUx8rAJl6jx2WAylYesrQPITUUzDRxKgtdI4b3Qtj68Hgf51oT/+AStb2zSPA==;EndpointSuffix=core.windows.net"


# Name of the container  
container_name = "containerfrc" 

try:
    # Create a blob service client using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    # Access the specified container within the Blob service
    container_client = blob_service_client.get_container_client(container_name)
    
    # List all blobs (files) within the container
    print("Listing Excel files in the container:")
    for blob in container_client.list_blobs():
        # Check if the file is an Excel file by its extension
        if blob.name.endswith('.xlsx') or blob.name.endswith('.xls'):
            print(blob.name)
            
except Exception as e:
    print(f"An error occurred: {e}")


# import ssl
# print(ssl.OPENSSL_VERSION)

