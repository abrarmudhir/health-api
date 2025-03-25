"""Seed initial data for patient, clinician, and medication

Revision ID: 079f31fe42d8
Revises: 5cb52f69e1f2
Create Date: 2025-03-25 02:15:11.773829

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "079f31fe42d8"
down_revision: Union[str, None] = "5cb52f69e1f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Insert an example patient
    stmt = sa.text(
        """
        INSERT INTO patients (first_name, last_name, date_of_birth, sex)
        VALUES (:first_name, :last_name, :date_of_birth, :sex)
        """
    ).bindparams(
        first_name="John", last_name="Doe", date_of_birth="1990-01-01", sex="male"
    )
    op.execute(stmt)

    # Insert an example clinician
    stmt = sa.text(
        """
        INSERT INTO clinicians (first_name, last_name, registration_id)
        VALUES (:first_name, :last_name, :registration_id)
        """
    ).bindparams(first_name="Alice", last_name="Smith", registration_id="REG123")
    op.execute(stmt)

    # Insert an example medication
    stmt = sa.text(
        """
        INSERT INTO medications (code, code_name, code_system, strength_value, strength_unit, form)
        VALUES (:code, :code_name, :code_system, :strength_value, :strength_unit, :form)
        """
    ).bindparams(
        code="12345",
        code_name="Aspirin",
        code_system="SNOMED",
        strength_value=500.0,
        strength_unit="mg",
        form="tablet",
    )
    op.execute(stmt)


def downgrade():
    op.execute("DELETE FROM medications")
    op.execute("DELETE FROM clinicians")
    op.execute("DELETE FROM patients")
