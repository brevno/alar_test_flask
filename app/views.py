from flask import render_template, request, redirect, url_for, g, jsonify
from flask.ext.login import login_required, login_user, logout_user, current_user
from app import app, db, lm
from .forms import LoginForm, EditUserForm, NewUserForm, NewPasswordForm
from .models import User
from .utils import compose_json_error, admin_priveleges_required

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
@login_required
def index():
    form_edit = EditUserForm()
    form_password = NewPasswordForm()
    form_new_user = NewUserForm()
    return render_template('index.html',
                           users=User.query.order_by('name'),
                           username=current_user.name,
                           form_edit=form_edit,
                           form_new_user=form_new_user,
                           form_password=form_password)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.found_user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/edit_user', methods=['POST'])
@login_required
@admin_priveleges_required
def edit_user():
    form = EditUserForm()
    if form.validate_on_submit():
        try:
            user = User.query.get(form.user_id.data)
            user.name = form.name.data
            user.is_admin = form.is_admin.data
            db.session.add(user)
            db.session.commit()
        except:
            return compose_json_error({'Backend error': 'DB error'})

        return jsonify({
            'status': 'OK'
        })
    else:
        return compose_json_error(form.errors)


@app.route('/new_user', methods=['POST'])
@login_required
@admin_priveleges_required
def new_user():
    form = NewUserForm()
    if form.validate_on_submit():
        try:
            user = User(
                name = form.name.data,
                is_admin = form.is_admin.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
        except:
            return compose_json_error({'Backend error': 'DB error'})

        return jsonify({
            'status': 'OK'
        })
    else:
        return compose_json_error(form.errors)


@app.route('/new_password', methods=['POST'])
@login_required
@admin_priveleges_required
def new_password():
    form = NewPasswordForm()
    if form.validate_on_submit():
        try:
            user = User.query.get(form.user_id.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
        except:
            return compose_json_error({'Backend error': 'DB error'})

        return jsonify({
            'status': 'OK'
        })
    else:
        return compose_json_error(form.errors)


@app.route('/delete_user', methods=['POST'])
@login_required
@admin_priveleges_required
def delete_user():
    try:
        user = User.query.get(request.form.get('user_id'))
        db.session.delete(user)
        db.session.commit()
    except:
        return compose_json_error({'Backend error': 'DB error'})

    return jsonify({
        'status': 'OK'
    })
