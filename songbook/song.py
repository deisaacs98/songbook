from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from songbook.composer import login_required
from songbook.db import get_db

bp = Blueprint('song', __name__)


@bp.route('/')
def index():
    db = get_db()
    songs = db.execute(
        'SELECT p.id, title, subtitle, author, description, email, created, composer_id, username'
        ' FROM song p JOIN user u ON p.composer_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('song/index.html', songs=songs)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        author = request.form['author']
        email = request.form['email']
        description = request.form['description']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO song (title, author, email, subtitle, description, composer_id)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (title, author, email, subtitle, description, g.user['id'])
            )
            db.commit()
            return redirect(url_for('song.index'))

    return render_template('song/create.html')


def get_song(id, check_composer=True):
    song = get_db().execute(
        'SELECT p.id, title, subtitle, author, description, email, created, composer_id, username'
        ' FROM song p JOIN user u ON p.composer_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if song is None:
        abort(404, f"Song id {id} doesn't exist.")

    if check_composer and song['composer_id'] != g.user['id']:
        abort(403)

    return song


def get_tracks(song_id):
    db = get_db()
    tracks = db.execute(
        'SELECT p.id, composer_id, song_id, instrument, created, username'
        ' FROM track p JOIN user u ON p.composer_id = u.id'
        ' WHERE p.song_id = ?'
        ' ORDER BY created ASC',
        (song_id,)
    ).fetchall()

    return tracks


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    song = get_song(id)
    tracks = get_tracks(id)
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        email = request.form['email']
        subtitle = request.form['subtitle']
        error = None
        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE song SET title = ?, author = ?, description = ?, email = ?, subtitle = ?'
                ' WHERE id = ?',
                (title, author, description, email, subtitle, id)
            )
            db.commit()
            return redirect(url_for('song.index'))

    return render_template('song/update.html', id=id, tracks=tracks, song=song)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_song(id)
    db = get_db()
    db.execute('DELETE FROM song WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('song.index'))


