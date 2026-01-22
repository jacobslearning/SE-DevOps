from flask import Blueprint, render_template, request, flash, url_for, redirect
from routes.utils import login_required, current_user, log_action
from database import db
from models import Department, Asset

departments_blueprint = Blueprint('departments', __name__)

@departments_blueprint.route('/departments')
@login_required
def departments():
    user = current_user()
    all_departments = Department.query.all()
    log_action(user.id, f"Departments viewed by {user.username} (ID: {user.id})")
    return render_template('departments.html', user=user, departments=all_departments)

@departments_blueprint.route('/department/create', methods=['POST'])
@login_required
def create_department():
    user = current_user()
    if user.role != 'Admin':
        log_action(user.id, f"Unauthorised department creation attempt by {user.username} (ID: {user.id})")
        flash("Unauthorised Access", "danger")
        return redirect(url_for('departments.departments'))

    name = request.form['name']

    # does department exist already
    if Department.query.filter_by(name=name).first():
        flash("A department already exists with this name", "info")
        return redirect(url_for('departments.departments'))

    new_department = Department(name=name)
    db.session.add(new_department)
    db.session.commit()
    log_action(user.id, f"Department {name} created by {user.username} (ID: {user.id})")
    flash(f"Department {name} created", "success")
    return redirect(url_for('departments.departments'))

@departments_blueprint.route('/department/edit/<int:dept_id>', methods=['POST'])
@login_required
def edit_department(dept_id):
    user = current_user()
    if user.role != 'Admin':
        log_action(user.id, f"Department (ID: {dept_id}) tried to be edited by {user.username} (ID: {user.id})")
        flash("Unauthorised Access", "danger")
        return redirect(url_for('departments.departments'))

    new_name = request.form['name']
    department = Department.query.get_or_404(dept_id)
    department.name = new_name
    db.session.commit()
    log_action(user.id, f"Department (ID: {dept_id}) updated to {new_name} by {user.username} (ID: {user.id})")
    flash(f"Department {new_name} updated", "success")
    return redirect(url_for('departments.departments'))

@departments_blueprint.route('/department/delete/<int:dept_id>', methods=['POST'])
@login_required
def delete_department(dept_id):
    user = current_user()
    if user.role != 'Admin':
        log_action(user.id, f"Department (ID: {dept_id}) tried to be deleted by {user.username} (ID: {user.id})")
        flash("Unauthorised Access", "danger")
        return redirect(url_for('departments.departments'))

    department = Department.query.get_or_404(dept_id)

    # delete all assets assigned to department
    Asset.query.filter_by(department_id=department.id).delete()

    db.session.delete(department)
    db.session.commit()
    log_action(user.id, f"Department (ID: {dept_id}, Name: {department.name}) deleted by {user.username} (ID: {user.id})")
    flash("Department deleted", "info")
    return redirect(url_for('departments.departments'))