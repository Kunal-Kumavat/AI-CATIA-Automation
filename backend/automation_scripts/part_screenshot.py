import os
import sys

# Add pycatia to path
sys.path.insert(0, os.path.abspath("..\\pycatia"))

from pathlib import Path
import time
from PIL import Image
from flask import session

import pythoncom
from pycatia import catia
from pycatia.cat_logger import create_logger
from pycatia.enumeration.enumeration_types import cat_capture_format
from pycatia.enumeration.enumeration_types import cat_specs_and_geom_window_layout
from pycatia.in_interfaces.camera_3d import Camera3D
from pycatia.in_interfaces.specs_and_geom_window import SpecsAndGeomWindow
from pycatia.in_interfaces.viewer_3d import Viewer3D
from pycatia.product_structure_interfaces.product import Product

def setup_save_path():
    """Setup and create the image save directory"""
    image_save_path = Path.cwd() / 'static' / 'catia_screenshots'
    
    if not image_save_path.exists():
        image_save_path.mkdir(parents=True, exist_ok=True)
        print(f"Created image save directory: {image_save_path}")
    
    return image_save_path

def capture_cad_model_screenshot():
    pythoncom.CoInitialize()
    """Capture screenshot of the currently active document in CATIA"""
    logger = create_logger()
    
    try:
        # Connect to running CATIA instance
        logger.info("Connecting to CATIA...")
        caa = catia()
        
        # Check if CATIA has any documents open
        if caa.documents.count == 0:
            logger.error("No documents are currently open in CATIA!")
            print("Error: Please open a CATPart file in CATIA first.")
            return False
        
        # Get the active document
        active_document = caa.active_document
        logger.info(f"Active document: {active_document.name}")
        
        # Check if it's a part document
        if not (active_document.name.lower().endswith('.catpart') or 
                hasattr(active_document, 'product')):
            logger.warning(f"Active document '{active_document.name}' may not be a CATPart file")
        
        # Setup save path
        image_save_path = setup_save_path()
        
        # Get product information for naming
        try:
            product = Product(active_document.product.com_object)
            part_number = product.part_number or active_document.name.split('.')[0]
            revision = product.revision or 'NA'
        except:
            # If product interface fails, use document name
            part_number = active_document.name.split('.')[0]
            revision = 'NA'
        
        # Generate filename
        img_name = f'{part_number} - {revision}.bmp'
        img_save_name = Path(image_save_path, img_name)
        
        # Check if file already exists
        if img_save_name.exists():
            logger.warning(f'File will be overwritten: {img_name}')
        
        # Get the active window and viewer
        active_window = caa.active_window
        if not active_window:
            logger.error("No active window found in CATIA!")
            return False
        
        viewer_3d = Viewer3D(active_window.active_viewer.com_object)
        specs_window = SpecsAndGeomWindow(active_window.com_object)
        
        # Store original settings
        logger.info("Configuring view for screenshot...")
        default_background_colour = viewer_3d.get_background_color()
        original_layout = specs_window.layout
        
        # Configure view for screenshot
        # Hide specification tree
        specs_window.layout = cat_specs_and_geom_window_layout.index('catWindowGeomOnly')
        
        # Toggle compass off (if it's on)
        caa.start_command('Compass')
        
        # Set white background
        white = (1, 1, 1)
        viewer_3d.put_background_color(white)
        
        # Set to isometric view and reframe
        try:
            camera_3d = Camera3D(active_document.cameras.item(1).com_object)
            viewpoint_3d = viewer_3d.viewpoint_3d
            sight = (-1, -1, -1)
            viewpoint_3d.put_sight_direction(sight)
        except:
            logger.warning("Could not set camera view, using current view")
        
        viewer_3d.reframe()
        viewer_3d.zoom_in()
        
        # Make fullscreen for better quality
        viewer_3d.full_screen = True
        
        # Small delay to ensure view is updated
        time.sleep(1.0)
        
        # Capture the screenshot
        logger.info(f'Capturing screenshot: {img_save_name}')
        viewer_3d.capture_to_file(cat_capture_format.index('catCaptureFormatBMP'), str(img_save_name))
        
        # Reset view settings
        logger.info("Restoring original view settings...")
        viewer_3d.full_screen = False
        viewer_3d.put_background_color(default_background_colour)
        specs_window.layout = original_layout
        caa.start_command('Compass')  # Toggle compass back
        
        # Convert BMP to PNG
        if img_save_name.exists():
            logger.info("Converting to PNG format...")
            with Image.open(img_save_name) as img:
                png_name = img_save_name.with_suffix('.png')
                img.save(png_name, 'PNG', optimize=True)
                logger.info(f'PNG saved: {png_name}')
            
            # Delete original BMP
            img_save_name.unlink()
            
            print(f"\n✅ Screenshot captured successfully!")
            print(f"📁 File saved at : {png_name} {png_name.name}")
            print(f"📂 Location: {image_save_path}")

            saved_screenshot_name = f"catia_screenshots/{png_name.name}"
            
            return saved_screenshot_name
        else:
            logger.error("Screenshot file was not created!")
            return False
            
    except Exception as e:
        logger.error(f"Error capturing screenshot: {str(e)}")
        print(f"❌ Error: {str(e)}")
        return False

# def main():
#     """Main function"""
#     print("🔧 CATIA Screenshot Tool - Active Document Mode")
#     print("=" * 50)
    
#     # Check if CATIA is running
#     try:
#         caa = catia()
#         print(f"✅ Connected to CATIA (Version: {caa.system_service.environ('CATInstallPath')})")
#     except:
#         print("❌ Error: CATIA is not running or not accessible!")
#         print("Please start CATIA and open a CATPart file first.")
#         return
    
#     # Capture screenshot
#     success = capture_cad_model_screenshot()
    
#     if success:
#         print("\n🎉 Process completed successfully!")
#     else:
#         print("\n⚠️  Process failed. Check the logs for details.")

# if __name__ == "__main__":
#     main()
