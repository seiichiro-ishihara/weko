#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""initial"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d6b2ebed7eb'
down_revision = None
branch_labels = ('weko_indextree_journal',)
depends_on = None


def upgrade():
    """Upgrade database."""
    pass


def downgrade():
    """Downgrade database."""
    pass
