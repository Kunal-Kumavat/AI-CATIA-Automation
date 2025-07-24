from flask import Blueprint, request, render_template

sign_in = Blueprint('sign_in', __name__, template_folder='../../templates')


@sign_in.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('sign_in.html')
    