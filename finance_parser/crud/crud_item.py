from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from finance_parser.crud.base import CRUDBase
from finance_parser.models import RawData, Symbol, Item, Date, DayStats
from finance_parser.schemas import ItemCreate, ItemUpdate, RawDataCreate, RawDataUpdate, SymbolCreate, SymbolUpdate, \
    ItemCreate, ItemUpdate, DateCreate, DateUpdate, DateStatsCreate, DateStatsUpdate


class CRUDRawData(CRUDBase[RawData, RawDataCreate, RawDataUpdate]):
    def create(
        self, db: Session, *, obj_in: RawDataCreate,
    ) -> RawData:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session, 
    ) -> List[RawData]:
        return (
            db.query(self.model)
            .all()
        )


raw_item_crud = CRUDRawData(RawData)

class CRUDSymbol(CRUDBase[Symbol, SymbolCreate, SymbolUpdate]):
    def create(
        self, db: Session, *, obj_in: SymbolCreate,
    ) -> Symbol:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session, 
    ) -> List[Symbol]:
        return (
            db.query(self.model)
            .all()
        )


symbol_crud = CRUDSymbol(Symbol)

class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def create(
        self, db: Session, *, obj_in: ItemCreate,
    ) -> Item:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session, 
    ) -> List[Item]:
        return (
            db.query(self.model)
            .all()
        )


item_crud = CRUDItem(Item)

class CRUDDate(CRUDBase[Date, DateCreate, DateUpdate]):
    def create(
        self, db: Session, *, obj_in: DateCreate,
    ) -> Date:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session, 
    ) -> List[Date]:
        return (
            db.query(self.model)
            .all()
        )

    def get_one(
        self, db: Session, date_as_text
    ) -> List[Date]:
        return (
            db.query(self.model)
            .filter(Date.date_as_text == date_as_text)
            .one()
        )

    def exists(
        self, db: Session, date_as_text
    ):
        return (
            db.query(self.model)
            .filter(Date.date_as_text == date_as_text)
            .all() is not None
        )


date_crud = CRUDDate(Date)

class CRUDDateStats(CRUDBase[DayStats, DateStatsCreate, DateStatsUpdate]):
    def create(
        self, db: Session, *, obj_in: DateStatsCreate,
    ) -> DayStats:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi(
        self, db: Session, 
    ) -> List[DayStats]:
        return (
            db.query(self.model)
            .all()
        )

date_stats_crud = CRUDDateStats(DayStats)