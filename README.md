
# 🚗 Juice Booster 3 Air – Home Assistant Integration

This custom Home Assistant integration adds full support for monitoring and controlling a **Juice Booster 3 Air** EV charging controller using Juice Pilot cloud APIs.

> Includes sensors, select controls, and automation-ready entities for PV-optimized charging.

---

## ✅ Features

- 🔐 OAuth2 login with Juice credentials
- 📊 Real-time charging view with state, power, cost, energy, duration
- 🔌 Control charging current: 0, 6, 8, 10, 13, 16 A
- 📈 Sensor entities for measured per-phase voltage, current, power
- 🧠 Supports battery-aware and PV-aware automation
- 📱 Lovelace dashboard compatible
- 🎉 HACS-compatible structure

---

## 📦 Installation via HACS

1. Open Home Assistant → HACS → Integrations
2. Click menu → **Custom Repositories**
3. Add this repo URL:
   ```
   https://github.com/class142/hacs-juice-plus-pilot
   ```
   Type: **Integration**
4. Find "Juice Booster" in HACS and install
5. Reboot Home Assistant

### 🧰 Manual Install (optional)

1. Copy this repository to:
   ```
   config/custom_components/juice_booster/
   ```
2. Restart Home Assistant

---

## 🔧 Setup Instructions

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **Juice Booster**
3. Enter your Juice Pilot **email and password**
4. Done! Entities will be created after first sync.

---

## 🧩 Entities Created

### ⚙️ Select Entity

| Entity ID | Description |
|-----------|-------------|
| `select.juice_booster_charging_current` | Set charging current (0, 6, 8, 10, 13, 16 A) |

---

### 📊 Sensor Entities

| Entity ID | Description |
|-----------|-------------|
| `sensor.juice_booster_charge_state` | Current charge state (e.g. Charging, Idle) |
| `sensor.juice_booster_charge_control` | Whether charging can be stopped |
| `sensor.juice_booster_charge_authentication_type` | Type of charging authentication |
| `sensor.juice_booster_charge_duration_total` | Charging duration (seconds) |
| `sensor.juice_booster_charge_cost_total` | Charging cost (EUR) |
| `sensor.juice_booster_energy_total` | Total energy this session (kWh) |
| `sensor.juice_booster_power` | Instantaneous charging power (kW) |
| `sensor.juice_booster_voltage_l1` | Voltage on L1 (V) |
| `sensor.juice_booster_voltage_l2` | Voltage on L2 (V) |
| `sensor.juice_booster_voltage_l3` | Voltage on L3 (V) |
| `sensor.juice_booster_current_l1` | Current on L1 (A) |
| `sensor.juice_booster_current_l2` | Current on L2 (A) |
| `sensor.juice_booster_current_l3` | Current on L3 (A) |
| `sensor.juice_booster_power_l1` | Power on L1 (kW) |
| `sensor.juice_booster_power_l2` | Power on L2 (kW) |
| `sensor.juice_booster_power_l3` | Power on L3 (kW) |
| `sensor.juice_booster_energy_level` | Current EV battery energy level (kWh) |
| `sensor.juice_booster_energy_level_start` | Start energy level of EV battery (kWh) |
| `sensor.juice_booster_max_device_current` | Max current supported by device (A) |
| `sensor.juice_booster_max_supply_current` | Max current currently supplied (A) |
| `sensor.juice_booster_smart_juice_enabled` | Smart Juice control active (bool) |

---

## 🧠 Automation Ideas

- 🔆 Charge EV when PV surplus is available
- 🔋 Limit charging if home battery is low
- 🌙 Nighttime charging if forecast is cloudy
- ⏱️ Use dynamic SoC and sunrise/sunset to optimize battery reserve

A sample automation and Lovelace dashboard is included in the [dashboards](dashboards) folder.

---

## 🔐 Security

This integration uses **OAuth2 (password grant)** to securely access the Juice Pilot cloud API.

Your credentials and refresh tokens are stored securely by Home Assistant.

---

## 📘 Requirements

- Juice Booster 3 Air device with Juice Pilot cloud access
- Home Assistant 2024.1.0 or newer
- Internet access for cloud polling

---

## 👨‍💻 Author

- Maintainer: [@class142](https://github.com/class142)
- License: MIT

Not affiliated with Juice Technology AG. This is a community integration.
