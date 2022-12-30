# Import all the models, so that Base has them before being
# imported by Alembic
from finance_parser.db.base_class import Base  # noqa
from finance_parser.models import RawData, Symbol, Item, Date, DayStats  # noqa

