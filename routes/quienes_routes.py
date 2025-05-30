from flask import Blueprint, render_template

quienes_bp = Blueprint('quienes', __name__)

@quienes_bp.route('/quienes')
def quienes():
    return render_template('quienes.html')