# ChargePoint for Home Assistant (Custom Stealth) 🔌⚡

[![Version](https://img.shields.io/badge/version-1.1.12-gold.svg?style=for-the-badge)](https://github.com/rananna/ha-chargepoint)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2026.3+-blue.svg?style=for-the-badge)
![Hardware](https://img.shields.io/badge/Hardware-Home%20Flex%20(CPH50)-green.svg?style=for-the-badge)

A high-performance, hardened fork of the ChargePoint integration. Engineered for the **Hyundai IONIQ 6** and optimized for **Canadian (Metric)** households. This "Stealth" version bypasses modern cloud security barriers while providing reliable, precision data.

---

## 🚀 Key Features

### 🛡️ Stealth & Stability
- **Anti-Fingerprinting:** Injects modern browser headers (Chrome 123) to bypass DataDome and 403 Forbidden cloud blocks.
- **Async Hardening:** Optimized for Home Assistant 2026, preventing "blocking call" warnings and ensuring smooth UI performance.
- **Data Integrity:** Implements `_last_val` persistence to prevent energy and cost metrics from "dipping" to zero between API polls.

### ⚡ Full Hardware Control
- **Dynamic Amperage:** Adjust charging speed (16A to 48A) via the dashboard to manage home electrical load.
- **Remote Session Toggle:** Start or stop charging sessions with a native Home Assistant switch.
- **Model-Aware:** Automatically identifies hardware (e.g., `CPH50`) for clean entity naming.

### 🇨🇦 Metric Precision
- **Localized Metrics:** Native conversion for `Kilometers Added` and `Kilometers / Hour Added`.
- **Currency Support:** Hardened for **CAD** currency reporting and account balance tracking.

---

## 🧩 Supported Entities

### 🎮 Controls
| Entity Name | Type | Description |
| :--- | :--- | :--- |
| **Charging Amperage Limit** | `select` | Dynamic current adjustment (16A - 48A). |
| **Charge Control** | `switch` | Remote session start/stop toggle. |

### 📊 Charging Metrics
| Entity Name | Type | Description |
| :--- | :--- | :--- |
| **Charge Cost** | `sensor` | Real-time session cost in **CAD**. |
| **Energy Output** | `sensor` | Energy delivered in the current session (kWh). |
| **Power Output** | `sensor` | Real-time charging speed in kW. |
| **Kilometers Added** | `sensor` | Estimated range added (km). |
| **KM / Hour Added** | `sensor` | Charging efficiency speed (km/h). |
| **Charging Time** | `sensor` | Active session duration (HH:MM:SS). |
| **Account Balance** | `sensor` | Remaining ChargePoint account credit. |

### 🔌 Connectivity
| Entity Name | Type | Description |
| :--- | :--- | :--- |
| **Plugged In** | `binary_sensor` | Returns `True` when the J1772 cable is connected. |
| **Status** | `sensor` | High-level status (e.g., "Ready", "Charging"). |

---

## 🛠️ Installation

1. Copy the `chargepoint` folder to your `custom_components/` directory.
2. **Restart Home Assistant.**
3. Navigate to **Settings > Devices & Services > Add Integration** and search for "ChargePoint (Custom Stealth)".
4. Enter your credentials and set your preferred poll interval (15 min recommended).

> **Pro Tip:** For the **IONIQ 6**, set the Amperage Limit to **48A** to maximize your Level 2 home charging speed on a 60A circuit.

---

## 📝 Credits
Maintained by **@rananna**. Built on the foundations of the mbillow architecture.
*v1.1.12 is the final stable release removing legacy diagnostic noise.*
