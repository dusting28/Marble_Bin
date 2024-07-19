from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json

views_home = Blueprint('views_home', __name__)


@views_home.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user, active_tab = 'home')

