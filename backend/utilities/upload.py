import os
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.storage.blob import ContentSettings, ContainerClient
import random
import string
MY_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=viaegnatia20;AccountKey=5q2myTqtPWSaS9OUwta5Woc0opbWgaaOluLHAOa7tiqjiXsDq2sFCqAmoFaJc5tPk/Z+8SaYmgyulgKB6Vk3ng==;EndpointSuffix=core.windows.net"
MY_IMAGE_CONTAINER = "egnatia20"

# Replace with the local folder which contains the image files for upload
LOCAL_IMAGE_PATH = "REPLACE_THIS"


class AzureBlobFileUploader:
    def __init__(self):
        print("Intializing AzureBlobFileUploader")

        # Initialize the connection to Azure storage account
        self.blob_service_client = BlobServiceClient.from_connection_string(MY_CONNECTION_STRING)

    def upload_all_images_in_folder(self):
        # Get all files with jpg extension and exclude directories
        all_file_names = [f for f in os.listdir(LOCAL_IMAGE_PATH)
                          if os.path.isfile(os.path.join(LOCAL_IMAGE_PATH, f)) and ".jpg" in f]

        # Upload each file
        for file_name in all_file_names:
            self.upload_image(file_name)

    def get_random_string(length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str + '.jpg'
    def upload_image(self, file_name):
        # Create blob with same name as local file name
        blob_client = self.blob_service_client.get_blob_client(container=MY_IMAGE_CONTAINER,
                                                               blob=file_name)
        # Get full current path and substitute utilities with buffer used to temporary store image data
        path = os.getcwd()
        path = path.replace('utilities', 'buffer')
        print(path)
        upload_file_path = path +'/rottie.jpg'

        # Create blob on storage
        # Overwrite if it already exists!
        image_content_setting = ContentSettings(content_type='image/jpeg')
        print(f"uploading file - {file_name}")
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True, content_settings=image_content_setting)
        return file_name


# Initialize class and upload files
azure_blob_file_uploader = AzureBlobFileUploader()
#azure_blob_file_uploader.upload_all_images_in_folder()
name = azure_blob_file_uploader.upload_image(AzureBlobFileUploader.get_random_string(11))
base_url = 'https://viaegnatia20.blob.core.windows.net/egnatia20/'
print(base_url+name)