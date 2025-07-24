import os


from flask import Blueprint, request, render_template, flash

from backend.utils_scripts.check_catia_status import check_catia_status
# Create Blueprint
catia_automation = Blueprint('catia_automation', __name__, template_folder='..templates')



# @catia_automation.route('/catia_automation', methods=['GET', 'POST'])
# def index():
#     if request.method == "GET":
#         return render_template('index.html')
#     elif request.method == 'POST':
#         file = request.files.get('catpart_file')
#         # if file and file.filename.endswith('.CATPart'):
#         #     file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#         #     file.save(file_path)
#         #     success = open_catpart_in_catia(file_path)
#         # if success:
#         #     flash('File opened in CATIA successfully!', 'success')
#         # else:
#         #     flash('Failed to open file in CATIA.', 'error')
#     else:
#         flash('Please upload a valid .CATPart file.', 'warning')
#     return render_template('index.html')



@catia_automation.route('/catia_automation', methods=['GET', 'POST'])
def catiaautomation():
    if request.method == "GET":
        return render_template('catia_automation.html')
    elif request.method == 'POST':
        file = request.files.get('catpart_file')
        # if file and file.filename.endswith('.CATPart'):
        #     file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        #     file.save(file_path)
        #     success = open_catpart_in_catia(file_path)
        # if success:
        #     flash('File opened in CATIA successfully!', 'success')
        # else:
        #     flash('Failed to open file in CATIA.', 'error')
    else:
        flash('Please upload a valid .CATPart file.', 'warning')
    return render_template('catia_automation.html')

