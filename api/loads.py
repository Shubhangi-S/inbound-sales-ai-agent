import pandas as pd
from typing import List, Optional
from .models import Load
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "loads.csv"

df = pd.read_csv(DATA_PATH)

def search_loads(origin: Optional[str]=None, destination: Optional[str]=None, equipment_type: Optional[str]=None, limit:int=3) -> List[Load]:
    res = df.copy()
    if origin:
        res = res[res['origin'].str.lower().str.contains(origin.lower())]
    if destination:
        res = res[res['destination'].str.lower().str.contains(destination.lower())]
    if equipment_type:
        res = res[res['equipment_type'].str.lower().str.contains(equipment_type.lower())]
    res = res.sort_values('pickup_datetime').head(limit)
    return [Load(**row.to_dict()) for _, row in res.iterrows()]
