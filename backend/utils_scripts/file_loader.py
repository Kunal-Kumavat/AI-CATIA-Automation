import os
import logging
import win32com.client
import pythoncom

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../../uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



def open_catpart_in_catia(file_path):
    """
    Enhanced version with comprehensive error handling and COM initialization.
    """
    com_initialized = False

    print('printing catia file path', file_path)
    
    try:
        # Initialize COM
        pythoncom.CoInitialize()
        com_initialized = True
        logger.info("COM initialized successfully")
        
        # Validate file
        if not os.path.isfile(file_path):
            logger.error(f"File does not exist: {file_path}")
            return False
        
        if not file_path.lower().endswith('.catpart'):
            logger.error("The file is not a .CATPart file.")
            return False
        
        logger.info("Attempting to connect to CATIA...")
        
        # Try to connect to existing CATIA instance first
        try:
            catia = win32com.client.GetActiveObject("CATIA.Application")
            logger.info("Connected to existing CATIA instance")
        except:
            # If no existing instance, create new one
            logger.info("No existing CATIA instance found, launching new one...")
            catia = win32com.client.Dispatch("CATIA.Application")
        
        catia.Visible = True
        
        logger.info(f"Opening file: {file_path}")
        documents = catia.Documents
        
        # Check if file is already open
        for i in range(1, documents.Count + 1):
            doc = documents.Item(i)
            if os.path.normpath(doc.FullName) == os.path.normpath(file_path):
                logger.info("File is already open in CATIA")
                doc.Activate()
                return True
        
        # Open the file
        document = documents.Open(file_path)
        logger.info("File opened successfully in CATIA.")
        return True
        
    except Exception as e:
        logger.exception(f"Failed to open .CATPart file: {e}")
        return False
        
    finally:
        # Clean up COM if we initialized it
        if com_initialized:
            try:
                pythoncom.CoUninitialize()
                logger.info("COM uninitialized")
            except:
                logger.warning("Error during COM cleanup")











# def open_catpart_in_catia(file_path):
#     try:
#         catia = win32com.client.Dispatch("CATIA.Application")
#         catia.Visible = True
#         documents = catia.Documents
#         documents.Open(file_path)
#         return True
#     except Exception as e:
#         print(f"Error opening file in CATIA: {e}")
#         return False





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
#         return False




# def open_catpart_in_catia(file_path):
#     try:
#         pythoncom.CoInitialize()  # Initialize COM for this thread
#         catia = win32com.client.Dispatch("CATIA.Application")
#         catia.Visible = True
#         documents = catia.Documents
#         documents.Open(file_path)
#         return True
#     except Exception as e:
#         print(f"Error opening file in CATIA: {e}")
#         return False


