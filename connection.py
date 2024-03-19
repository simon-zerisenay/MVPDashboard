from azure.storage.blob import BlobServiceClient
import os

connection_string = "DefaultEndpointsProtocol=https;AccountName=pistoragefrc1;AccountKey=0JfcY7Sg9tyRMLeaupyQBO3S3UUx8rAJl6jx2WAylYesrQPITUUzDRxKgtdI4b3Qtj68Hgf51oT/+AStb2zSPA==;EndpointSuffix=core.windows.net"

 
 
container_name = "containerfrc" 

try:
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    print("Listing Excel files in the container:")
    for blob in container_client.list_blobs():
        if blob.name.endswith('.xlsx') or blob.name.endswith('.xls'):
            print(blob.name)
            
except Exception as e:
    print(f"An error occurred: {e}")

