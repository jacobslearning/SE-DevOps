from flask import Blueprint, render_template, request, flash, url_for, redirect
from datetime import datetime
from routes.utils import login_required, current_user, log_action
from database import db
from models import Asset, User, Department

assets_blueprint = Blueprint('assets', __name__)


@assets_blueprint.route('/assets')
@login_required
def assets():
    user = current_user()

    if user.role == 'Admin':
        assets_query = (
            Asset.query
            .join(User, Asset.owner_id == User.id)
            .join(Department, Asset.department_id == Department.id)
            .add_columns(
                Asset.id, Asset.name, Asset.description,
                Asset.type, Asset.serial_number,
                Asset.date_created, Asset.in_use, Asset.approved,
                Asset.owner_id, Asset.department_id,
                User.username.label("owner_username"),
                Department.name.label("department_name")
            )
        )
    else:
        assets_query = (
            Asset.query
            .filter_by(owner_id=user.id)
            .join(User, Asset.owner_id == User.id)
            .join(Department, Asset.department_id == Department.id)
            .add_columns(
                Asset.id, Asset.name, Asset.description,
                Asset.type, Asset.serial_number,
                Asset.date_created, Asset.in_use, Asset.approved,
                Asset.owner_id, Asset.department_id,
                User.username.label("owner_username"),
                Department.name.label("department_name")
            )
        )

    assets_list = [
        {
            "id": asset.id,
            "name": asset.name,
            "description": asset.description,
            "type": asset.type,
            "serial_number": asset.serial_number,
            "date_created": (
                asset.date_created.strftime("%Y-%m-%d %H:%M")
                if asset.date_created else None
            ),
            "in_use": "1" if asset.in_use else "0",
            "approved": "1" if asset.approved else "0",
            "owner_id": str(asset.owner_id),
            "department_id": (
                str(asset.department_id)
                if asset.department_id else ""
            ),
            "owner_username": asset.owner_username,
            "department_name": asset.department_name
        }
        for asset in assets_query.all()
    ]

    departments = Department.query.all()
    users = User.query.order_by(User.username.asc()).all()
    log_action(user.id, f"Assets viewed by {user.username} (ID: {user.id})")
    return render_template(
        'assets.html',
        assets=assets_list,
        user=user,
        departments=departments,
        users=users
    )


@assets_blueprint.route('/asset/create', methods=['POST'])
@login_required
def create_asset():
    user = current_user()
    data = request.form
    date_created = datetime.now()

    new_asset = Asset(
        name=data['name'],
        description=data['description'],
        type=data['type'],
        serial_number=data['serial_number'],
        date_created=date_created,
        in_use=bool(int(data.get('in_use', 1))),
        approved=bool(int(data.get('approved', 0))),
        owner_id=data['assigned_user_id'],
        department_id=data['department_id']
    )

    db.session.add(new_asset)
    db.session.commit()
    log_action(
        user.id,
        f"Asset (ID: {new_asset.id}, Name: {new_asset.name}) "
        f"created by {user.username} (ID: {user.id})"
    )
    flash("Asset created and awaiting approval", "success")
    return redirect(url_for('assets.assets'))


@assets_blueprint.route('/asset/edit/<int:asset_id>', methods=['POST'])
@login_required
def edit_asset(asset_id):
    data = request.form
    user = current_user()

    asset = db.session.get(Asset, asset_id)
    if not asset:
        flash("Asset not found", "danger")
        return redirect(url_for('assets.assets'))

    if user.role != 'Admin' and asset.owner_id != user.id:
        log_action(
            user.id,
            f"Asset (ID: {asset.id}, Name: {asset.name}) tried to "
            f"be updated by {user.username} (ID: {user.id})"
        )
        flash("Unauthorised Access", "danger")
        return redirect(url_for('assets.assets'))

    asset.name = data['name']
    asset.description = data['description']
    asset.type = data['type']
    asset.serial_number = data['serial_number']
    asset.in_use = True if data.get('in_use') == "1" else False
    asset.department_id = int(data['department_id'])
    asset.owner_id = int(data['assigned_user_id'])

    if user.role == 'Admin':
        asset.approved = True if data.get('approved') == "1" else False
    db.session.commit()
    log_action(
        user.id,
        f"Asset (ID: {asset.id}, Name: {asset.name}) updated by "
        f"{user.username} (ID: {user.id})"
    )
    flash("Asset updated", "success")
    return redirect(url_for('assets.assets'))


@assets_blueprint.route('/asset/delete/<int:asset_id>', methods=['POST'])
@login_required
def delete_asset(asset_id):
    user = current_user()
    asset = db.session.get(Asset, asset_id)
    if not asset:
        flash("Asset not found", "danger")
        return redirect(url_for('assets.assets'))

    if user.role != 'Admin' and asset.owner_id != user.id:
        log_action(
            user.id,
            f"Asset (ID: {asset.id}, Name: {asset.name}) tried to "
            f"be deleted by {user.username} (ID: {user.id})"
        )
        flash("Unauthorised Access", "danger")
        return redirect(url_for('assets.assets'))

    db.session.delete(asset)
    db.session.commit()
    log_action(
        user.id,
        f"Asset (ID: {asset.id}, Name: {asset.name}) "
        f"deleted by {user.username} (ID: {user.id})"
    )
    flash("Asset deleted", "info")
    return redirect(url_for('assets.assets'))


@assets_blueprint.route('/asset/approve/<int:asset_id>', methods=['POST'])
@login_required
def approve_asset(asset_id):
    user = current_user()
    if user.role != 'Admin':
        log_action(
            user.id,
            f"Asset (ID: {asset_id}) tried to be approved by "
            f"{user.username} (ID: {user.id})"
        )
        flash("Unauthorised Access", "danger")
        return redirect(url_for('assets.assets'))

    asset = db.session.get(Asset, asset_id)
    if not asset:
        flash("Asset not found", "danger")
        return redirect(url_for('assets.assets'))
    asset.approved = True
    db.session.commit()
    log_action(
        user.id,
        f"Asset (ID: {asset.id}, Name: {asset.name}) "
        f"approved by {user.username} (ID: {user.id})"
    )
    flash("Asset approved", "success")
    return redirect(url_for('assets.assets'))
