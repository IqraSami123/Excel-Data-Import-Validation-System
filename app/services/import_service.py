from sqlalchemy.orm import Session

from app.models.import_job import ImportJob


def create_import_job(     #this function will create a new import job in the database with the given filename and status "PENDING"
    db: Session,
    filename: str,
) -> ImportJob:
    import_job = ImportJob(
        filename=filename,
        status="PENDING",
    )

    db.add(import_job)
    db.commit()
    db.refresh(import_job)

    return import_job