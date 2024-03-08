from azure.storage.blob import BlobServiceClient, BlobClient
import os
 
# Initialize the Blob Service Client
connection_string = "DefaultEndpointsProtocol=https;AccountName=pistoragefrc1;AccountKey=0JfcY7Sg9tyRMLeaupyQBO3S3UUx8rAJl6jx2WAylYesrQPITUUzDRxKgtdI4b3Qtj68Hgf51oT/+AStb2zSPA==;EndpointSuffix=core.windows.net"
# connection_string = "your_connection_string"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Specify the container and the target folder
container_name = "containerfrc"
target_folder = "Users/simon/Desktop/Builds/Dashy/camels/"

# Access the container 
container_client = blob_service_client.get_container_client(container_name)

# List all blobs in the container and filter for Excel files
blobs_list = container_client.list_blobs()
for blob in blobs_list:
    if blob.name.endswith('.xlsx') or blob.name.endswith('.xls'):
        # Define the new blob name with the target folder prefix
        new_blob_name = f"{target_folder}{os.path.basename(blob.name)}"

        print("I am here")
        
        # Create a BlobClient for the source blob and the target blob
        source_blob = container_client.get_blob_client(blob)
        target_blob = container_client.get_blob_client(new_blob_name)
        
        # Copy the source blob to the target location
        target_blob.start_copy_from_url(source_blob.url)

