from werkzeug.security import generate_password_hash
from datetime import datetime
from app import app
from database import db
from models import User, Department, Asset
from tests.utils import ADMIN_DB_URL


def init_db():
    app.config.update(
        TESTING=False,
        SQLALCHEMY_DATABASE_URI=ADMIN_DB_URL,
    )
    with app.app_context():
        # create all tables
        db.drop_all()
        db.create_all()
        print(ADMIN_DB_URL)

        # departments
        dept_names = [
            'HR', 'Customer Service', 'IT', 'Store Operations',
            'Security', 'Marketing'
        ]
        for name in dept_names:
            if not Department.query.filter_by(name=name).first():
                db.session.add(Department(name=name))
        db.session.commit()

        # users
        password_hash = generate_password_hash("password")
        user_data = [
            ('harry', 'User'), ('jacob', 'User'), ('josh', 'User'),
            ('tHisIsCool12', 'User'), ('Harry_Truman', 'User'),
            ('Doris_Day', 'Admin'),
            ('Joe_DiMaggio', 'User'), ('Joe_McCarthy', 'User'),
            ('Richard_Nixon', 'User'),
            ('Marilyn_Monroe', 'User'), ('Rosenbergs', 'User'),
            ('Roy_Cohn', 'User'),
            ('Juan_Perón', 'User'), ('Einstein', 'User'),
            ('James_Dean', 'User'),
            ('Elvis_Presley', 'User'), ('Brigitte_Bardot', 'User'),
            ('Nikita_Khrushchev', 'User'),
            ('Princess_Grace', 'User'), ('Peyton_Place', 'User'),
            ('Mickey_Mantle', 'User'),
            ('Jack_Kerouac', 'User'), ('Charles_de_Gaulle', 'User'),
            ('Buddy_Holly', 'User'),
            ('Hemingway', 'User'), ('Bob_Dylan', 'User'),
            ('John_Glenn', 'User'),
            ('Pope_Paul', 'User'), ('Malcolm_X', 'User'), ('JFK', 'User'),
            ('Ho_Chi_Minh', 'User'), ('Ronald_Reagan', 'Admin'),
            ('Sally_Ride', 'User'),
            ('Bernhard_Goetz', 'User'), ('admin', 'Admin'),
        ]

        for username, role in user_data:
            if not User.query.filter_by(username=username).first():
                db.session.add(User(
                    username=username,
                    password_hash=password_hash,
                    role=role
                ))
        db.session.commit()

        # users and departments
        user_map = {u.username: u.id for u in User.query.all()}
        dept_map = {d.name: d.id for d in Department.query.all()}

        # assets
        date_now = datetime.now()

        assets = [
            ('Lenova XP5 15', 'Work laptop', 'Laptop',
             'SN12345AL32323', date_now, True, True, 'jacob', 'IT'),
            ('Iphone 15 Pro Max', 'Company phone', 'Phone',
             'SN12346AL', date_now, True, True, 'jacob', 'IT'),
            ('Windows 10 PC', 'Office desktop', 'Desktop',
             'SN22345BO', date_now, True, False, 'harry',
             'Customer Service'),
            ('Ipad Pro', 'Tablet for presentations', 'Tablet',
             'SN22346BO', date_now, True, True, 'harry',
             'Customer Service'),
            ('Lenova XP5 15', 'Development laptop', 'Laptop',
             'SN32345CA', date_now, True, False, 'harry', 'IT'),
            ('Iphone 14 Pro Max', 'Company phone', 'Phone',
             'SN32346CA', date_now, False, True, 'harry', 'HR'),
            ('Windows 10 PC', 'Windows PC for testing', 'Windows',
             'SN32347CA', date_now, True, True, 'harry', 'IT'),
            ('DELL 313183XP3', 'Main office workstation', 'Desktop',
             'SN42345AD3232323', date_now, True, True, 'jacob',
             'IT'),
            ('DELL 48248248XN2', 'Backup laptop', 'Laptop',
             'SN42346AD11134', date_now, False, True, 'jacob', 'IT'),
            ('Iphone 16', 'Company phone', 'Phone',
             'SN42347ADDDDDDF', date_now, True, True, 'jacob', 'HR'),
            ('HP EliteBook 840', 'Work laptop', 'Laptop',
             'HPEL-2485KWS-001', date_now, True, False, 'Bob_Dylan',
             'IT'),
            ('iPhone 14', 'Company phone', 'Phone',
             'IPHN-7453MNS-119', date_now, True, True, 'JFK', 'HR'),
            ('Dell OptiPlex 7090', 'Office desktop', 'Desktop',
             'DELL-OPT7090-663', date_now, True, False,
             'Elvis_Presley', 'Customer Service'),
            ('iPad Air', 'Tablet for presentations', 'Tablet',
             'IPAD-2023AIR-384', date_now, True, False, 'Sally_Ride',
             'Marketing'),
            ('MacBook Pro 16"', 'Development laptop', 'Laptop',
             'MBPRO16-MKT-881FF', date_now, True, False, 'James_Dean',
             'IT'),
            ('Zebra TC52', 'Inventory scanner', 'Device',
             'ZEBRA-TC52-455KFF', date_now, False, True, 'Juan_Perón',
             'Store Operations'),
            ('Samsung Galaxy Tab S8', 'Tablet for stock check',
             'Tablet', 'SMSNG-TABS8-922FFFF', date_now, True, True,
             'Joe_DiMaggio', 'Store Operations'),
            ('DELL 313183XP3', 'Main office workstation', 'Desktop',
             'SN42345ADEEEEA', date_now, True, False, 'Richard_Nixon',
             'IT'),
            ('HP EliteBook 840', 'Backup laptop', 'Laptop',
             'SN42346AD33113D', date_now, False, True,
             'Princess_Grace', 'Marketing'),
            ('iPhone 16', 'Company phone', 'Phone',
             'SN42347ADDDDAAAA', date_now, True, True, 'Malcolm_X',
             'Security'),
        ]

        for name, desc, typ, serial, date_created, in_use, approved, \
                owner_name, dept_name in assets:
            if not Asset.query.filter_by(serial_number=serial).first():
                db.session.add(
                    Asset(
                        name=name,
                        description=desc,
                        type=typ,
                        serial_number=serial,
                        date_created=date_created,
                        in_use=in_use,
                        approved=approved,
                        owner_id=user_map[owner_name],
                        department_id=dept_map[dept_name]
                    )
                )
        db.session.commit()

        print("Database ingest succesful")


if __name__ == '__main__':
    init_db()
