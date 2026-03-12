# ChargePoint for Home Assistant (Custom Stealth) 🔌⚡

[![Version](https://img.shields.io/badge/version-1.1.10-gold.svg?style=for-the-badge)](https://github.com/rananna/ha-chargepoint)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2026.3+-blue.svg?style=for-the-badge)
![Hardware](https://img.shields.io/badge/Hardware-Home%20Flex%20(CPH50)-green.svg?style=for-the-badge)

A high-performance, hardened fork of the ChargePoint integration. Optimized for the **Hyundai IONIQ 6** and engineered for high-frequency cloud polling without triggering security blocks.

---

## 🚀 Key Features

### 🛡️ Stealth & Stability
- **Anti-Fingerprinting:** Uses modern browser headers (Chrome 123) to bypass DataDome and cloud security barriers.
- **Async Hardening:** Fully asynchronous loading prevents "Blocking call in the event loop" warnings common in Home Assistant 2026.
- **Auto-Backoff:** Built-in intelligence to pause polling if 403 errors are detected, protecting your IP from potential bans.

### ⚡ Full Hardware Control
- **Dynamic Amperage:** Adjust your charging speed (16A to 48A) directly from the dashboard.
- **Remote Session Toggle:** Start or stop charging sessions with a single switch.
- **Model-Aware:** Automatically prefixes entities with your hardware model (e.g., `CPH50`) for easy identification.

### 📊 Precision Metrics
- **Currency Sync:** Automatically handles CAD formatting for Canadian users.
- **Range Tracking:** Real-time estimates for `Miles Added` and `Miles / Hour Added`.
- **Diagnostics:** Wi-Fi signal strength (RSSI) and precise Heartbeat monitoring.

---

## 🧩 Supported Entities

This integration provides a comprehensive set of entities to monitor and control your ChargePoint Home Flex.

### 🎮 Controls
| Entity Name | Type | Description |
| :--- | :--- | :--- |
| **Charging Amperage Limit** | `select` | Adjust the maximum current (16A - 50A) to match your circuit. |
| **Charge Control** | `switch` | Remotely start or stop a charging session. |

### 📊 Metrics
| Entity Name | Type | Description |
| :--- | :--- | :--- |
| **Charge Cost** | `sensor` | Real-time cost of the current/last session in **CAD**. |
| **Energy Output** | `sensor` | Total energy delivered in the current session (kWh). |
| **Power Output** | `sensor` | Real-time charging speed in kW. |
| **Miles Added** | `sensor` | Estimated range added during the current session. |
| **Miles / Hour Added** | `sensor` | Current charging efficiency (MPH). |
| **Charging Time** | `sensor` | Duration of the current session (HH:MM:SS). |
| **Account Balance** | `sensor` | Remaining credit on your ChargePoint account. |
| **Status** | `sensor` | High-level status (e.g., "Ready", "Charging"). |
| **Charger State** | `sensor` | Detailed internal state (e.g., "Not Charging", "In Use"). |

### 🛠️ Diagnostics & Connectivity
| Entity Name | Type | Description |
| :--- | :--- | :--- |
| **Plugged In** | `binary_sensor` | Returns `True` if the cable is physically connected to the vehicle. |
| **Wi-Fi Signal** | `sensor` | Real-time signal strength (dBm) of the charger. |
| **Last Heartbeat** | `sensor` | Timestamp of the last successful cloud synchronization. |

---

## 🛠️ Installation & Setup

1. Copy the `chargepoint` folder to your `custom_components/` directory.
2. **Restart Home Assistant.**
3. Go to **Settings > Devices & Services > Add Integration** and search for "ChargePoint (Custom Stealth)".
4. Enter your credentials.

> **Note:** For the **IONIQ 6**, it is recommended to set your Amperage Limit to **48A** for optimal Level 2 home charging on a 60A circuit.

---

## 📈 Dashboard Integration
This integration is 100% compatible with the **Energy Dashboard**. 
- **Energy Source:** Use `sensor.cph50_energy_output`.
- **Cost Tracking:** Use `sensor.cph50_charge_cost`.

---

## 📝 Credits
Maintained by **@rananna**. Based on the original architecture by @mbillow. 
*v1.1.10 is the stable production release.*
