from flask import Blueprint, render_template, url_for, redirect
from routes.utils import login_required, current_user
from models import Asset, User, Department
from database import db

dashboard_blueprint = Blueprint('dashboard', __name__)

@dashboard_blueprint.route('/')
def index():
    if current_user():
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.login'))

@dashboard_blueprint.route('/dashboard')
@login_required
def dashboard():
    user = current_user()

    if user.role == 'Admin':
        assets = (
            Asset.query
            .filter_by(approved=False)
            .join(User, Asset.owner_id == User.id)
            .join(Department, Asset.department_id == Department.id)
            .add_columns(
                Asset.id, Asset.name, Asset.description, Asset.type, Asset.serial_number,
                Asset.date_created, Asset.in_use, Asset.approved,
                User.username.label("owner_username"),
                Department.name.label("department_name")
            )
            .all()
        )
    else:
        assets = (
            Asset.query
            .filter_by(approved=False, owner_id=user.id)
            .join(User, Asset.owner_id == User.id)
            .join(Department, Asset.department_id == Department.id)
            .add_columns(
                Asset.id, Asset.name, Asset.description, Asset.type, Asset.serial_number,
                Asset.date_created, Asset.in_use, Asset.approved,
                User.username.label("owner_username"),
                Department.name.label("department_name")
            )
            .all()
        )

    assets_list = [
        {
            "id": asset.id,
            "name": asset.name,
            "description": asset.description,
            "type": asset.type,
            "serial_number": asset.serial_number,
            "date_created": asset.date_created.strftime("%Y-%m-%d %H:%M") if asset.date_created else None,
            "in_use": asset.in_use,
            "approved": asset.approved,
            "owner_username": asset.owner_username,
            "department_name": asset.department_name
        }
        for asset in assets
    ]

    metrics = {
        "total_assets": Asset.query.count(),
        "pending_assets": Asset.query.filter_by(approved=False).count(),
        "total_users": User.query.count(),
        "total_departments": Department.query.count()
    }

    return render_template('dashboard.html', user=user, assets=assets_list, metrics=metrics)