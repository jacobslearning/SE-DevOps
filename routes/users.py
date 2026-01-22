from flask import Blueprint, render_template, request, flash, url_for, redirect
from werkzeug.security import generate_password_hash
from routes.utils import login_required, current_user, log_action
from database import db
from models import User, Asset

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/users')
@login_required
def users():
    user = current_user()

    if user.role == 'Admin':
        all_users = User.query.all()
    else:
        all_users = [user]
    log_action(user.id, f"Users viewed by {user.username} (ID: {user.id})")
    return render_template('users.html', users=all_users, user=user)


@users_blueprint.route('/user/edit/<int:user_id>', methods=['POST'])
@login_required
def edit_user(user_id):
    user = current_user()
    data = request.form
    username = data['username']
    password = data['password']
    role = data['role']

    # Access control
    if user.role != 'Admin' and user.id != user_id:
        log_action(
            user.id,
            f"User (ID: {user_id}) tried to be edited by "
            f"{user.username} (ID: {user.id})"
        )
        flash("Unauthorised Access", "danger")
        return redirect(url_for('users.users'))

    if user.role != 'Admin':
        role = "User"

    # admins cant demote themself back to user
    if user.role == 'Admin' and user.id == user_id and role == 'User':
        log_action(user.id, f"Admin (ID: {user.id}) tried to demote themself")
        flash("You cannot demote yourself to User", "info")
        return redirect(url_for('users.users'))

    target_user = User.query.get_or_404(user_id)
    target_user.username = username

    # only update password if its changed
    if password != '[HIDDEN]':
        target_user.password_hash = generate_password_hash(password)

    target_user.role = role
    db.session.commit()
    log_action(
        user.id,
        f"User (ID: {target_user.id}) updated by "
        f"{user.username} (ID: {user.id})"
    )

    flash(f"User {username} updated", "success")
    return redirect(url_for('users.users'))


@users_blueprint.route('/user/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = current_user()

    if user.role != 'Admin' and user.id != user_id:
        log_action(
            user.id,
            f"User (ID: {user_id}) tried to be deleted by "
            f"{user.username} (ID: {user.id})"
        )
        flash("Unauthorised Access", "danger")
        return redirect(url_for('users.users'))

    target_user = User.query.get_or_404(user_id)

    # delete all assets owned by user
    Asset.query.filter_by(owner_id=target_user.id).delete()

    # then delete user
    db.session.delete(target_user)
    db.session.commit()

    flash("User deleted", "info")

    # If a user deleted themself
    if user.id == user_id:
        log_action(user.id, f"User (ID: {user.id}) deleted themself")
        return redirect(url_for('auth.login'))
    log_action(
        user.id,
        f"User (ID: {target_user.id}) deleted by "
        f"{user.username} (ID: {user.id})"
    )
    return redirect(url_for('users.users'))


@users_blueprint.route('/user/promote/<int:user_id>', methods=['POST'])
@login_required
def promote_user(user_id):
    user = current_user()

    if user.role != 'Admin':
        log_action(
            user.id,
            f"User (ID: {user_id}) tried to be promoted by "
            f"{user.username} (ID: {user.id})"
        )
        flash("Unauthorised Access", "danger")
        return redirect(url_for('users.users'))

    target_user = User.query.get_or_404(user_id)
    target_user.role = "Admin"
    db.session.commit()
    log_action(
        user.id,
        f"User (ID: {target_user.id}) promoted to Admin by "
        f"{user.username} (ID: {user.id})"
    )

    flash("User promoted to Admin", "success")
    return redirect(url_for('users.users'))


@users_blueprint.route('/user/create', methods=['POST'])
@login_required
def create_user():
    user = current_user()

    if user.role != 'Admin':
        log_action(
            user.id,
            f"User creation attempt by {user.username} "
            f"(ID: {user.id})"
        )
        flash("Unauthorised Access", "danger")
        return redirect(url_for('users.users'))

    username = request.form['username']
    password = request.form['password']
    role = request.form['role']
    password_hash = generate_password_hash(password)

    if User.query.filter_by(username=username).first():
        flash("A user already exists with this name", "info")
        return redirect(url_for('users.users'))

    new_user = User(
        username=username,
        password_hash=password_hash,
        role=role
    )
    db.session.add(new_user)
    db.session.commit()
    log_action(
        user.id,
        f"User (ID: {new_user.id}) created by "
        f"{user.username} (ID: {user.id})"
    )

    flash(f"User {username} created", "success")
    return redirect(url_for('users.users'))
