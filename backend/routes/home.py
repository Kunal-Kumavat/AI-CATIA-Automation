import os


from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from werkzeug.utils import secure_filename



from backend.utils_scripts.check_catia_status import check_catia_status
from backend.utils_scripts.file_loader import open_catpart_in_catia, UPLOAD_FOLDER
from ..automation_scripts.part_screenshot import capture_cad_model_screenshot

# Create Blueprint
home = Blueprint('home', __name__, template_folder='..templates')



# @home.route('/home', methods=['GET', 'POST'])
# def homepage():
#     catia_status = check_catia_status()

#     if request.method == "GET":      
#         return render_template('home.html', catia_status=catia_status)
    
#     elif request.method == 'POST':
#         if 'catpart_file' in request.files:
#             file = request.files['catpart_file']

#             if file and file.filename and file.filename.endswith('.CATPart'):
#                 try:
#                     # save the uploaded file
#                     filename = secure_filename(file.filename)
#                     filepath = os.path.join(UPLOAD_FOLDER, filename)
#                     file.save(filepath)

#                     # store file info into session 
#                     session['uploaded_file'] = {'filename': filename, 'filepath': filepath, 'original_name': file.filename}

#                     # open file into catia
#                     if open_catpart_in_catia(filepath):
#                         flash('.CATPart file loaded successfully in CATIA!', 'success')
#                         return redirect(url_for('catia_automation.catiaautomation'))
#                     else :
#                         flash('Failed to open file in CATIA. Please try again.', 'error')
#                         return render_template('home.html')
                
#                 except Exception as e:
#                     flash(f'Error processing file: {str(e)}', 'error')
                
#             else:
#                 flash('Please select a valid .CATPart file.', 'warning')
        
#         elif 'user_query' in request.files:
#             print('request.files', request.files)


#         # return render_template('home.html', catia_status=catia_status)
#     else:
#         flash('Please upload a valid .CATPart file.', 'warning')
#     return render_template('home.html')






@home.route('/home', methods=['GET', 'POST'])
def homepage():
    catia_status = check_catia_status()

    if request.method == "GET":
        return render_template('home.html', catia_status=catia_status)

    elif request.method == "POST":
        user_query = request.form.get('user_query', '').strip()

        if 'catpart_file' in request.files:
            # existing CATPart upload logic
            file = request.files['catpart_file']
            if file and file.filename and file.filename.endswith('.CATPart'):
                try:
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(filepath)
                    session['uploaded_file'] = {
                        'filename': filename,
                        'filepath': filepath,
                        'original_name': file.filename
                    }
                    if open_catpart_in_catia(filepath):
                        flash('.CATPart file loaded successfully in CATIA!', 'success')
                        saved_screenshot_name  = capture_cad_model_screenshot()
                        print("from home py file ", saved_screenshot_name)
                        if saved_screenshot_name:
                            session['cad_screenshot'] = f"{saved_screenshot_name}"
                        return redirect(url_for('catia_automation.catiaautomation'))
                    else:
                        flash('Failed to open file in CATIA. Please try again.', 'error')
                        return render_template('home.html', catia_status=catia_status)
                except Exception as e:
                    flash(f'Error processing file: {e}', 'error')
                    return render_template('home.html', catia_status=catia_status)
            else:
                flash('Please select a valid .CATPart file.', 'warning')
                return render_template('home.html', catia_status=catia_status)
            


        # NEW: redirect based on text input only
        elif user_query != "":
            return redirect(url_for('catia_automation.catiaautomation', text=user_query))

    else:
        # neither file nor non-empty text
        flash('Please upload a valid .CATPart file or enter your requirement.', 'warning')
        return render_template('home.html', catia_status=catia_status)
