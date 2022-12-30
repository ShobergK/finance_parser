from datetime import date, datetime
from finance_parser.schemas import RawDataCreate, SymbolCreate, ItemCreate, DateCreate, DateStatsCreate
from finance_parser.crud.crud_item import raw_item_crud, symbol_crud, item_crud, date_crud, date_stats_crud
from tqdm import tqdm
from finance_parser.utils import get_data_from_alphavintage_full, get_db
from finance_parser.config import settings

symbols_list = ["IBM", "AA", "AAC", "UZE", "BB"] 
unique_dates_list = []

# get_db
db = next(iter(get_db()))

for symbol in symbols_list:

    unique_dates_dict = {}

    #create symbol db object
    symbol_db_obj = symbol_crud.create(db = db, obj_in=SymbolCreate(**{"name": symbol}))

    data = get_data_from_alphavintage_full(symbol, settings.interval, settings.api_key)

    print(f"saving {symbol} data to database")
    
    for key in tqdm(data[f'Time Series ({settings.interval}min)'].keys()):

            cur_data = data[f'Time Series ({settings.interval}min)'][key]
            date = datetime.strptime(key, '%Y-%m-%d %X')

            raw_dict = {
                "symbol": symbol,
                "interval": settings.interval,

                "date_time": key,
                "data_open": cur_data['1. open'],
                "data_high": cur_data['2. high'],
                "data_low": cur_data['3. low'],
                "data_close": cur_data['4. close'],
                "data_volume": cur_data['5. volume'],
            }

            raw_item_crud.create(db = db, obj_in=RawDataCreate(**raw_dict))

            date_as_text = date.strftime("%Y-%m-%d")

            if date_as_text not in unique_dates_list and date_crud.exists(db = db, date_as_text=date_as_text):
                date_db_obj = date_crud.create(db = db, obj_in=DateCreate(**{"date_as_text": date_as_text}))
                unique_dates_list.append(date_as_text)

            else: 
                date_db_obj = date_crud.get_one(db = db, date_as_text=date_as_text)

            if date_as_text not in unique_dates_dict.keys():
                unique_dates_dict[date_as_text] = {
                    "open": float(cur_data['1. open']),
                    "open_time": date,
                    "close": float(cur_data['4. close']),
                    "close_time": date,
                    "volume_total": int(cur_data['5. volume']),
                    "volume_high": int(cur_data['5. volume']),
                    "time_high_volume": date,
                    "high": float(cur_data['2. high']),
                    "time_high_cost": date,
                    "low": float(cur_data['3. low']),
                    "time_low_cost": date,
                }
            else:
                if date < unique_dates_dict[date_as_text]["open_time"]:
                    unique_dates_dict[date_as_text]["open_time"] = date
                    unique_dates_dict[date_as_text]["open"] = float(cur_data['1. open'])

                if date > unique_dates_dict[date_as_text]["open_time"]:
                    unique_dates_dict[date_as_text]["close_time"] = date
                    unique_dates_dict[date_as_text]["close"] = float(cur_data['4. close'])                

                unique_dates_dict[date_as_text]["volume_total"] += int(cur_data['5. volume'])

                if int(cur_data['5. volume']) > unique_dates_dict[date_as_text]["volume_high"]:
                    unique_dates_dict[date_as_text]["time_high_volume"] = date
                    unique_dates_dict[date_as_text]["volume_high"] = int(cur_data['5. volume'])  

                if float(cur_data['2. high']) > unique_dates_dict[date_as_text]["high"]:
                    unique_dates_dict[date_as_text]["time_high_cost"] = date
                    unique_dates_dict[date_as_text]["high"] = float(cur_data['2. high'])  

                if float(cur_data['3. low']) < unique_dates_dict[date_as_text]["low"]:
                    unique_dates_dict[date_as_text]["time_low_cost"] = date
                    unique_dates_dict[date_as_text]["low"] = float(cur_data['3. low'])  
            

            normalized_dict = {
                "symbol_id": symbol_db_obj.id,
                "date_unique_id": date_db_obj.id,
                "interval": settings.interval,
                "date_time": date,

                "data_open": float(cur_data['1. open']),
                "data_high": float(cur_data['2. high']),
                "data_low": float(cur_data['3. low']),
                "data_close": float(cur_data['4. close']),
                "data_volume": int(cur_data['5. volume']),

            }

            item_crud.create(db = db, obj_in=ItemCreate(**normalized_dict))

    for unique_date in unique_dates_dict.keys():

        date_db_obj = date_crud.get_one(db = db, date_as_text=unique_date)

        day_open = unique_dates_dict[unique_date]["open"]
        day_close = unique_dates_dict[unique_date]["close"]
        day_diff_percent = min(day_open, day_close) / max(day_open, day_close) * 100

        stats_dict = {
            "symbol_id": symbol_db_obj.id,    
            "date_unique_id": date_db_obj.id,
            "day_open": day_open,
            "day_close": day_close,
            "day_volume": unique_dates_dict[unique_date]["volume_total"],
            "day_diff_percent": day_diff_percent,
            "time_high_cost": unique_dates_dict[unique_date]["time_high_cost"],
            "time_low_cost": unique_dates_dict[unique_date]["time_low_cost"],
            "time_high_volume": unique_dates_dict[unique_date]["time_high_volume"],
        }
        date_stats_crud.create(db = db, obj_in=DateStatsCreate(**stats_dict))

