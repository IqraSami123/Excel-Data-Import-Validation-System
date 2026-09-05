from datetime import datetime

from sqlalchemy import select

from app.celery_app import celery_app
from app.database import SessionLocal
from app.models.customer import Customer
from app.models.import_job import ImportError, ImportJob
from app.services.excel_service import read_excel_rows
from app.services.validation_service import validate_row


@celery_app.task
def test_celery_task():
    ### just to test if celery is working or not"""
    return "Celery is working!"


@celery_app.task
def process_import_job(import_job_id: int, file_path: str):
    ### this function will process the import job and update the import job status and records in the database ###
    db = SessionLocal()

    try:
        import_job = db.get(ImportJob, import_job_id)

        if import_job is None:
            return

        import_job.status = "PROCESSING"
        import_job.started_at = datetime.utcnow()
        db.commit()

        for row_number, row in enumerate(
            read_excel_rows(file_path),
            start=2,
        ):
            import_job.total_records += 1

            errors = validate_row(row)

            if errors:
                import_job.invalid_records += 1

                import_error = ImportError(
                    import_job_id=import_job.id,
                    row_number=row_number,
                    errors={"errors": errors},
                )

                db.add(import_error)

            else:
                email = str(row["email"]).strip().lower()

                existing_customer = db.scalar(
                    select(Customer).where(Customer.email == email)
                )

                if existing_customer:
                    import_job.invalid_records += 1

                    import_error = ImportError(
                        import_job_id=import_job.id,
                        row_number=row_number,
                        errors={
                            "errors": [
                                "email already exists"
                            ]
                        },
                    )

                    db.add(import_error)

                else:
                    customer = Customer(
                        name=str(row["name"]).strip(),
                        email=email,
                        phone=str(row["phone"]).strip(),
                        age=int(row["age"]),
                        city=str(row["city"]).strip(),
                        status=str(row["status"]).strip().lower(),
                    )

                    db.add(customer)

                    import_job.valid_records += 1
                    import_job.imported_records += 1

            import_job.processed_records += 1

            # this is batch processing, we commit the changes to the database after every 500 records to avoid memory issues and to improve performance
            if import_job.processed_records % 500 == 0:
                db.commit()

        db.commit()

        import_job.status = "COMPLETED"
        import_job.completed_at = datetime.utcnow()
        db.commit()

    except Exception as exc:
        db.rollback()

        import_job = db.get(ImportJob, import_job_id)

        if import_job:
            import_job.status = "FAILED"
            import_job.error_message = str(exc)
            db.commit()

        raise

    finally:
        db.close()