from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import login_required, current_user
from .models import Marble, TournamentResult
from . import db
from os import path
import json

views_tournaments = Blueprint('views_tournaments', __name__)

@views_tournaments.route('/tournaments/<int:tournament_ID>', methods=['GET', 'POST'])
def tournament_display(tournament_ID):

    all_marbles = Marble.query.all()

    if TournamentResult.query.count() < 1:
        return render_template("tournament_display.html", user=current_user, all_marbles = all_marbles, active_tab = 'tournaments');
    else:
        return render_template("tournament_display.html", user=current_user, all_marbles = all_marbles, active_tab = 'tournaments');