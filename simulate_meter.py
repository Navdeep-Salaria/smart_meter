import json
import time
import random
import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meterr.settings")
django.setup()

from reading.models import Meter

# Initialize meters from database
meters = {}
for meter in Meter.objects.all():
    meters[meter.meter_id] = {
        "current_power": 0,
        "daily_total": 0,
        "peak_power": 0
    }

def simulate_meter_step(meter_data):
    max_power = 650
    increase = random.uniform(0, max_power / 60)
    meter_data["current_power"] = increase
    meter_data["daily_total"] += increase / 1000  # kWh
    meter_data["peak_power"] = max(meter_data["peak_power"], increase)
    return meter_data

def save_meter_json(meter_id, meter_data):
    with open(f"{meter_id}.json", "w") as f:
        json.dump(meter_data, f, indent=2)

# Main loop
try:
    while True:
        for meter_id, data in meters.items():
            meters[meter_id] = simulate_meter_step(data)
            save_meter_json(meter_id, meters[meter_id])
        time.sleep(1)  # update every second
except KeyboardInterrupt:
    print("Simulation stopped.")
