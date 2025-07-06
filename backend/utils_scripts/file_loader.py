import os
import logging
import win32com.client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# def open_catpart_in_catia(file_path):
#     """
#     Opens a .CATPart file in CATIA using COM automation.

#     Parameters:
#         file_path (str): The full path to the .CATPart file.

#     Returns:
#         bool: True if the file was opened successfully, False otherwise.
#     """
#     try:
#         if not os.path.isfile(file_path):
#             logger.error(f"File does not exist: {file_path}")
#             return False

#         if not file_path.lower().endswith('.catpart'):
#             logger.error("The file is not a .CATPart file.")
#             return False

#         logger.info("Launching CATIA application...")
#         catia = win32com.client.Dispatch("CATIA.Application")
#         catia.Visible = True

#         logger.info(f"Opening file: {file_path}")
#         documents = catia.Documents
#         documents.Open(file_path)

#         logger.info("File opened successfully in CATIA.")
#         return True

#     except Exception as e:
#         logger.exception(f"Failed to open .CATPart file: {e}")
#         return Fal se



UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def open_catpart_in_catia(file_path):
    try:
        catia = win32com.client.Dispatch("CATIA.Application")
        catia.Visible = True
        documents = catia.Documents
        documents.Open(file_path)
        return True
    except Exception as e:
        print(f"Error opening file in CATIA: {e}")
        return False
