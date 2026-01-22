from datetime import datetime
from database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(
        db.String(10),
        nullable=False
    )

    assets = db.relationship("Asset", back_populates="owner", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100), nullable=False)

    assets = db.relationship("Asset", back_populates="department", lazy="dynamic")

    def __repr__(self):
        return f"<Department {self.name}>"


class Asset(db.Model):
    __tablename__ = "assets"

    id = db.Column(db.Integer, primary_key=True, index = True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(50))
    serial_number = db.Column(db.String(150), unique=True)

    date_created = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    in_use = db.Column(db.Boolean, nullable=False, default=True)
    approved = db.Column(db.Boolean, nullable=False, default=False)

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id", ondelete="SET NULL"),
        nullable=True
    )

    # relationships
    owner = db.relationship("User", back_populates="assets")
    department = db.relationship("Department", back_populates="assets")

    def __repr__(self):
        return f"<Asset {self.name} ({self.type})>"

class Log(db.Model):
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="logs")

    def __repr__(self):
        return f"<Log {self.action} by User {self.user_id}>"