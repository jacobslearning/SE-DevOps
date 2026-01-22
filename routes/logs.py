from flask import Blueprint, render_template, flash, url_for, redirect
from routes.utils import login_required, current_user, log_action
from models import Log

logs_blueprint = Blueprint('logs', __name__)


@logs_blueprint.route('/logs')
@login_required
def logs():
    user = current_user()
    if user.role != 'Admin':
        log_action(
            user.id,
            f"Unauthorised logs access attempt by {user.username} "
            f"(ID: {user.id})"
        )
        flash("Unauthorised Access", "danger")
        return redirect(url_for('dashboard.dashboard'))

    all_logs = Log.query.order_by(Log.timestamp.desc()).all()
    log_action(user.id, f"Logs viewed by {user.username} (ID: {user.id})")
    return render_template(
        "logs.html",
        logs=[
            {
                "user_id": log.user_id,
                "action": log.action,
                "timestamp": log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for log in all_logs
        ],
        user=user
    )
