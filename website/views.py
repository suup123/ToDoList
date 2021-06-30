from flask import Blueprint, render_template, url_for, request, flash, jsonify, redirect
from flask.json import jsonify
from flask_login import login_required, current_user
from .models import Note
from .models import User
from . import db
import json


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify ({})

@views.route("/new")
@login_required
def new_note():
    return render_template('create_note.html')


@views.route("/new", methods=['POST'])
@login_required
def new_note_post():
    data = request.form.get('note')
    end_date = request.form.get('end_date')
    status = request.form.get('status')
    if len(data) < 1:
        flash('Note is too short!', category='error')
        return redirect(url_for('views.new_note'))
    else:
        print(data, end_date, status)
        note2 = Note(data=data, end_date=end_date, status=status, user_id=current_user.id)
        db.session.add(note2)
        db.session.commit()
        flash('Your note has been added!')
        return redirect(url_for('views.home'))

@views.route("/note/<int:note_id>/update", methods=['GET', 'POST'])
@login_required
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    if request.method == "POST":
        note.data = request.form['note']
        note.end_date = request.form['end_date']
        note.status = request.form['status']
        db.session.commit()
        flash('Your post has been updated!')
        return redirect(url_for('views.home'))

    return render_template('update_note.html', note=note)