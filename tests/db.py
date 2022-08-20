from faker import Faker

from factory import PatientBuilder
from app.models import db, session, Patient

fake = Faker(["pt_BR"])

NUMBERS_PATIENTS = 5


def _fk_pragma_on_connect(dbapi_con, _):
    """
    Enable FK constraint in sqllite
    """
    dbapi_con.execute("PRAGMA foreign_keys = ON")


def set_up_db():
    """
    Create test database and populate
    """
    from sqlalchemy import event
    event.listen(db.engine, 'connect', _fk_pragma_on_connect)
    db.create_all()


def populate_patients(num_rows=NUMBERS_PATIENTS, created_patients=None):
    """
    Populate table patients
    """
    patients = []
    with db.session():
        for i in range(num_rows):
            patient = PatientBuilder().complete().build_object(
            ) if i % 2 == 0 else PatientBuilder().build_object()
            db.session.add(patient)
            session.flush()
            patients.append(patient.as_json())

        if created_patients:
            for patient in created_patients:
                db.session.add(patient)
                session.flush()
                patients.append(patient.as_json())

        session.commit()
    return patients
