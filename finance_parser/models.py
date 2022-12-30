from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

from finance_parser.db.base_class import Base

class RawData(Base):
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    interval = Column(Integer)
    date_time = Column(String)
    data_open = Column(String)
    data_high = Column(String)
    data_low = Column(String)
    data_close = Column(String)
    data_volume = Column(String)

class Symbol(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    items = relationship("Item", back_populates="symbol") 
    day_stats = relationship("DayStats", back_populates="symbol")     

class Date(Base):
    id = Column(Integer, primary_key=True, index=True)
    date_as_text = Column(String)
    items = relationship("Item", back_populates="date_unique")
    day_stats = relationship("DayStats", back_populates="date_unique") 

class Item(Base):
    id = Column(Integer, primary_key=True, index=True)
    symbol_id = Column(Integer, ForeignKey("symbol.id"))
    symbol = relationship("Symbol", back_populates="items")
    date_unique_id = Column(Integer, ForeignKey("date.id"))
    date_unique = relationship("Date", back_populates="items")
    interval = Column(Integer)
    date_time = Column(DateTime)
    data_open = Column(Float)
    data_high = Column(Float)
    data_low = Column(Float)
    data_close = Column(Float)
    data_volume = Column(Integer)

class DayStats(Base):
    id = Column(Integer, primary_key=True, index=True)
    symbol_id = Column(Integer, ForeignKey("symbol.id"))
    symbol = relationship("Symbol", back_populates="day_stats")
    date_unique_id = Column(Integer, ForeignKey("date.id"))
    date_unique = relationship("Date", back_populates="day_stats")
    day_open = Column(Float)
    day_close = Column(Float)
    day_volume = Column(Integer)
    day_diff_percent = Column(Float)
    time_high_cost = Column(DateTime)
    time_low_cost = Column(DateTime)
    time_high_volume = Column(DateTime)