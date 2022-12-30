from pydantic import BaseModel
from datetime import datetime

#########################################
# RawData schemas

# Shared properties
class RawDataBase(BaseModel):
    symbol: str
    interval: int
    date_time: str
    data_open: str
    data_high: str
    data_low: str
    data_close: str
    data_volume: str

# Properties to receive on item creation
class RawDataCreate(RawDataBase):
    pass

# Properties to receive on item update
class RawDataUpdate(RawDataBase):
    pass

# Properties shared by models stored in DB
class RawDataInDBBase(RawDataBase):
    id: int    

    class Config:
        orm_mode = True

# Properties to return to client
class RawData(RawDataInDBBase):
    pass

# Properties properties stored in DB
class RawDataInDB(RawDataInDBBase):
    pass


#########################################
# Symbol schemas

# Shared properties
class SymbolBase(BaseModel):
    name: str

# Properties to receive on item creation
class SymbolCreate(SymbolBase):
    pass

# Properties to receive on item update
class SymbolUpdate(SymbolBase):
    pass

# Properties shared by models stored in DB
class SymbolInDBBase(SymbolBase):
    id: int    

    class Config:
        orm_mode = True

# Properties to return to client
class Symbol(SymbolInDBBase):
    pass

# Properties properties stored in DB
class SymbolInDB(SymbolInDBBase):
    pass


#########################################
# Item schemas

# Shared properties
class ItemBase(BaseModel):
    symbol_id: int
    date_unique_id: int
    interval: int
    date_time: datetime
    data_open: float
    data_high: float
    data_low: float
    data_close: float
    data_volume: int

# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass

# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass

# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int    

    class Config:
        orm_mode = True

# Properties to return to client
class Item(ItemInDBBase):
    pass

# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass

#########################################
# Date schemas

# Shared properties
class DateBase(BaseModel):
    date_as_text: str

# Properties to receive on item creation
class DateCreate(DateBase):
    pass

# Properties to receive on item update
class DateUpdate(DateBase):
    pass

# Properties shared by models stored in DB
class DateInDBBase(DateBase):
    id: int    

    class Config:
        orm_mode = True

# Properties to return to client
class Date(DateInDBBase):
    pass

# Properties properties stored in DB
class DateInDB(DateInDBBase):
    pass

#########################################
# Date schemas

# Shared properties
class DateStatsBase(BaseModel):
    symbol_id: int
    date_unique_id: int
    day_open: float
    day_close: float
    day_volume: int
    day_diff_percent: float
    time_high_cost: datetime
    time_low_cost: datetime
    time_high_volume: datetime

# Properties to receive on item creation
class DateStatsCreate(DateStatsBase):
    pass

# Properties to receive on item update
class DateStatsUpdate(DateStatsBase):
    pass

# Properties shared by models stored in DB
class DateStatsInDBBase(DateStatsBase):
    id: int    

    class Config:
        orm_mode = True

# Properties to return to client
class DateStats(DateStatsInDBBase):
    pass

# Properties properties stored in DB
class DateStatsInDB(DateStatsInDBBase):
    pass
