
# ⚡ Smart EV Charging Automation for Home Assistant

This automation intelligently controls EV charging current for a **Juice Booster 3 Air**, using:
- Solar production forecast (Solcast)
- Real-time battery SoC from a SolMan-integrated Deye inverter
- Home power consumption
- Dynamic night length (sunset → sunrise)
- User-defined SoC limits for the EV

✅ Optimized to use **excess solar** and preserve **battery reserve** for overnight needs.

---

## 🚘 What It Does

- ⛽️ Only charges EV when:
  - It's plugged in
  - SoC is below your desired limit
  - There’s solar surplus **beyond what the home battery can handle**
- 🌇 Avoids discharging the home battery below a calculated **reserve** based on:
  - Night duration
  - Average night load
- 🔁 Adjusts charging current (0, 6, 10, 16 A) depending on available solar power

---

## 📋 Required Integrations & Entities

| Requirement | Type | Example Entity | Purpose |
|------------|------|----------------|---------|
| ✅ [Juice Booster Integration](https://github.com/class142/hacs-juice-plus-pilot) | Custom integration | `select.juice_booster_charging_current` | Control charging amperage |
| ✅ Solcast Forecast (via HACS) | Sensor | `sensor.solcast_pv_forecast_leistung_in_30_minuten` | Solar power forecast |
| ✅ Skoda / EV Integration | Sensors | `sensor.skoda_elroq_batteriestand`, `sensor.skoda_elroq_ladegrenze_in_prozent`, `binary_sensor.skoda_elroq_ladekabel` | EV SoC, charging limit, plugged status |
| ✅ SolMan (Deye Inverter) Integration | Sensors | `sensor.inverter_pv_power`, `sensor.inverter_power`, `sensor.inverter_battery`, `sensor.inverter_battery_capacity` | PV production, home load, battery SoC and capacity |
| ✅ Sun integration (built-in) | Sensor | `sensor.sun_next_rising`, `sensor.sun_next_setting` | For night detection |

---

## 🧠 Logic Overview

| Condition | Action |
|----------|--------|
| Battery > 85% + Surplus > 11.5 kW | Charge at 16 A |
| Battery > 60% + Surplus > 7 kW | Charge at 10 A |
| Battery < reserve (night need) | Stop charging |
| At night (sunset → sunrise) + SoC < 70% + reserve OK | Charge slowly at 6 A |

---

## ⚙️ Variables Used in Automation

- `pv_power`, `forecast_kw`, `surplus_kw`
- `battery_soc`, `battery_kwh_available`, `battery_reserve`
- `ev_soc`, `ev_capacity_kwh`, `avg_night_load_kw`
- `next_sunrise`, `next_sunset`, `night_hours`, `reserve_kwh`

These are dynamically calculated in the automation to ensure safe, smart, energy-aware EV charging.

---

## 📲 Usage Instructions

1. Install required integrations
2. Make sure all sensors mentioned above exist and update properly
3. Import or copy this automation YAML into **Configuration → Automations**
4. Customize thresholds if needed (e.g. surplus limits or SoC %)
5. Monitor and tweak using a Lovelace dashboard if desired

---

## 🧪 Tips

- Ensure Solcast forecast sensors are up to date
- Match entity IDs to your own inverter, EV, and charger setup
- Consider visualizing `surplus_kw`, `battery_kwh_available`, etc. with template sensors

---

## 📘 License

MIT License – provided as-is, community-supported  
Not affiliated with Juice Technology, Skoda, Solcast, or Deye.
