from flask import Blueprint, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()
        password = (request.form.get('password') or '').strip()
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            error = '用户名或密码错误'
        else:
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_role'] = user.role

            # Link anonymous session profile to this user (only if unowned)
            import uuid
            from app.models import UserProfile
            sid = session.get('session_id')
            if sid:
                profile = UserProfile.query.filter_by(session_id=sid, user_id=None).first()
                if profile:
                    profile.user_id = user.id
                    db.session.commit()
            # Generate fresh session_id to avoid cross-user contamination
            session['session_id'] = str(uuid.uuid4())[:8]

            return redirect(url_for('main.index'))

    return render_template('login.html', error=error)


@auth_bp.route('/register', methods=['POST'])
def register():
    username = (request.form.get('username') or '').strip()
    password = (request.form.get('password') or '').strip()
    confirm = (request.form.get('confirm') or '').strip()

    if not username or not password:
        return redirect(url_for('auth.login'))
    if password != confirm or len(password) < 4:
        return redirect(url_for('auth.login'))

    if not User.query.filter_by(username=username).first():
        db.session.add(User(username=username, password=generate_password_hash(password)))
        db.session.commit()

    return redirect(url_for('auth.login'))


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('user_role', None)
    return redirect(url_for('main.index'))
