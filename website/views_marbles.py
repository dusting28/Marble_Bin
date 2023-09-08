from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import login_required, current_user
from .models import Marble
from . import db
from os import path

views_marbles = Blueprint('views_marbles', __name__)

@views_marbles.route('/receive_selected_value', methods=['POST'])
def receive_selected_value():
    marble_name = request.form['selected_value']
    marble_name = marble_name.split(">", 1)
    marble_name = marble_name[1][1:]
    selected_marble = Marble.query.filter_by(Name = marble_name).first()
    
    if selected_marble:
        response_data = {'redirect_url': url_for('views_marbles.marble_display', marble_ID = selected_marble.ID)}
        return jsonify(response_data)

    

@views_marbles.route('/marbles/<int:marble_ID>', methods=['GET', 'POST'])
def marble_display(marble_ID):

    if Marble.query.count() < 1:
        default_marble = Marble(Name = "--EMPTY--", Weight = 0, Diameter1 = 0, Diameter2 = 0)
        db.session.add(default_marble)
        db.session.commit()

    existing_new_marble = Marble.query.filter_by(Name = "New Marble").first()
    if existing_new_marble:
        db.session.delete(existing_new_marble)
        db.session.commit()

    all_marbles = Marble.query.all()
    selected_marble = Marble.query.filter_by(ID = marble_ID).first()

    action = request.form.get('action')
    # Edit Marble Button
    if action == 'edit':
        if selected_marble and selected_marble.ID > 1:
            return redirect(url_for('views_marbles.marble_edit',selected_ID = selected_marble.ID))
        else:
            flash('Select a Marble', category='error')
    
    # New Marble Button
    if action == 'newMarble':
        existing_new_marble = Marble.query.filter_by(Name = "New Marble").first()
        if existing_new_marble:
            return redirect(url_for('views_marbles.marble_edit',selected_ID = existing_new_marble.ID))
        else:
            new_marble = Marble()
            db.session.add(new_marble)
            db.session.commit()
            return redirect(url_for('views_marbles.marble_edit',selected_ID = new_marble.ID))

    return render_template("marble_display.html", user=current_user, all_marbles = all_marbles, marble_ID = marble_ID, selected_marble = selected_marble, template_ID = "marbles_select", active_tab = 'marbles')


@views_marbles.route('/edit_marble/<int:selected_ID>', methods=['GET', 'POST'])
@login_required
def marble_edit(selected_ID):
    
    selected_marble = Marble.query.filter_by(ID=selected_ID).first()

    action = request.form.get('action')
    if action == 'save':
        name = request.form.get('name')
        team = request.form.get('team')
        cheat = request.form.get('cheat')
        weight = request.form.get('weight')
        diameter1 = request.form.get('diameter1')
        diameter2 = request.form.get('diameter2')
        image = request.files['image']
        timeTrial = request.files['timeTrial']

        cheat = (cheat == "on")
        weight = int(weight)
        diameter1 = int(diameter1)
        diameter2 = int(diameter2)

        duplicate_flag = False
        duplicates = Marble.query.filter_by(Name=name).all()
        if duplicates:
            for duplicate in duplicates:
                if duplicate.ID != selected_ID:
                    duplicate_flag = True

        if duplicate_flag:
            flash('Marble name already exists.', category='error')
        elif name == "New Marble":
            flash('Give the marble a different name.', category='error')
        elif len(name) > 30:
            flash('Name must be 30 characters or less.', category='error')
        elif diameter2 < diameter1:
            flash('Minor diameter cannot be less than major diameter.', category='error')
        elif not(('.' in image.filename) and (image.filename.rsplit('.', 1)[1].lower() == "png")) and not(image.filename==""):
            flash('Image must be a PNG file.', category='error')
        elif not(('.' in timeTrial.filename) and (timeTrial.filename.rsplit('.', 1)[1].lower() == "csv")) and not(timeTrial.filename==""):
            flash('Time trial data must be a CSV file.', category='error')
        elif selected_marble:
            selected_marble.Name = name
            selected_marble.Team = team
            selected_marble.Cheat = cheat
            selected_marble.Weight = weight
            selected_marble.Diameter1 = diameter1
            selected_marble.Diameter2 = diameter2
            if (('.' in image.filename) and (image.filename.rsplit('.', 1)[1].lower() == "png")):
                new_filename = "Marble"+str(selected_marble.ID)+"_Image.png"
                image.save(path.join(current_app.config['UPLOAD_FOLDER'], new_filename))
                selected_marble.Image = new_filename

            if (('.' in timeTrial.filename) and (timeTrial.filename.rsplit('.', 1)[1].lower() == "csv")):
                new_filename = "Marble"+str(selected_marble.ID)+"_TimeTrials.csv"
                timeTrial.save(path.join(current_app.config['UPLOAD_FOLDER'], new_filename))
                selected_marble.Time_Trials = new_filename

            db.session.commit()
            flash('Saved.', category='success')
            return redirect(url_for('views_marbles.marble_display', marble_ID = selected_marble.ID))
        else:
            flash('Unknown Error', category='error')
    
    if action == 'cancel':
        if selected_marble:
            if (selected_marble.Name == "New Marble"):
                db.session.delete(selected_marble)
                db.session.commit()
                return redirect(url_for('views_marbles.marble_display', marble_ID = 1))
            else:
                return redirect(url_for('views_marbles.marble_display', marble_ID = selected_marble.ID))
        else:
            flash('Invalid ID Error', category='error')
            
    
    if action == 'delete':
        db.session.delete(selected_marble)
        db.session.commit()
        return redirect(url_for('views_marbles.marble_display', marble_ID = 1))

    return render_template("marble_edit.html", user=current_user, marble=selected_marble, active_tab = 'marbles')
