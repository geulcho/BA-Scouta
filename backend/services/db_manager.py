import os
import json
import requests
import asyncio
import aiohttp
from typing import Dict, Any

DATA_URL = "https://raw.githubusercontent.com/lonqie/SchaleDB/main/data/kr/students.min.json"
ICON_URL_BASE = "https://raw.githubusercontent.com/lonqie/SchaleDB/main/images/student/icon/{}.webp"
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
ICONS_DIR = os.path.join(DATA_DIR, "icons")

class DBManager:
    def __init__(self):
        self.students = {}
        self.student_list = []
        
    def load_data(self):
        print("Fetching SchaleDB data...")
        response = requests.get(DATA_URL)
        response.raise_for_status()
        raw_data = response.json()
        
        for st in raw_data:
            # We only need playable students, but let's just parse what we have.
            # ID, Name, BulletType, ArmorType, StreetBattle, MaxHP, HealPower, DodgePoint
            sid = st.get("Id")
            name = st.get("Name")
            bullet_type = st.get("BulletType")
            armor_type = st.get("ArmorType")
            squad_type = st.get("SquadType") # "Main" (Striker) or "Support" (Special)
            tactic_role = st.get("TacticRole")
            
            # Adaptation types are typically in 'StreetBattle', 'OutdoorBattle', 'IndoorBattle'
            street_battle = st.get("StreetBattle", "C")
            
            # MaxHP is usually calculated, but we might just take base stats at max level or level 90
            # From the sample, it seems MaxHP100, HealPower100 etc might be in some arrays or standard fields.
            # Let's extract MaxHP100, HealPower100 if present.
            max_hp = st.get("MaxHP100", 10000)
            heal_power = st.get("HealPower100", 0)
            dodge_point = st.get("DodgePoint100", 0) # Fallback to 0 if not present
            
            # We must apply HP * 3
            pvp_hp = max_hp * 3
            
            self.students[sid] = {
                "Id": sid,
                "Name": name,
                "BulletType": bullet_type,
                "ArmorType": armor_type,
                "SquadType": squad_type,
                "TacticRole": tactic_role,
                "StreetBattle": street_battle,
                "BaseMaxHP": max_hp,
                "PvPMaxHP": pvp_hp,
                "HealPower": heal_power,
                "DodgePoint": dodge_point
            }
            self.student_list.append(self.students[sid])
            
        print(f"Loaded {len(self.students)} students.")

db = DBManager()
