# ChargePoint for Home Assistant (Custom Stealth) 🔌⚡

[![Version](https://img.shields.io/badge/version-1.1.12-gold.svg?style=for-the-badge)](https://github.com/rananna/ha-chargepoint)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2026.3+-blue.svg?style=for-the-badge)
![Hardware](https://img.shields.io/badge/Hardware-Home%20Flex%20(CPH50)-green.svg?style=for-the-badge)
![Localization](https://img.shields.io/badge/Region-Canada%20(Metric)-red.svg?style=for-the-badge)

A high-performance, hardened fork of the ChargePoint integration. Engineered specifically for the **Hyundai IONIQ 6** and optimized for **Canadian** households. This "Stealth" version is built to bypass modern cloud security barriers while providing high-precision, localized data.

---

## 🚀 Key Improvements in v1.1.12

### 🛡️ Resilience & Stealth
* **Self-Healing Connection:** Implements a sophisticated `urllib3` retry strategy with exponential backoff to handle 429 (Rate Limit) and 5xx (Server Error) responses gracefully.
* **Anti-Fingerprinting:** Injects modern Chrome 123 browser headers to bypass DataDome and 403 Forbidden cloud blocks.
* **Async Hardening:** Fully asynchronous initialization compliant with the latest Home Assistant core standards.

### 🇨🇦 Metric & UI Excellence
* **Native Kilometers:** Range and speed estimates are natively converted using a high-precision 1.60934 multiplier.
* **Clean Diagnostics:** Legacy diagnostic "noise" (RSSI, Heartbeat, and non-functional Restart buttons) has been stripped to ensure a 100% stable, "Unknown"-free dashboard.
* **Persistence Logic:** State-aware code ensures cumulative sensors (Energy/Cost) maintain their values during API polling gaps.

---

## 🧩 Supported Entities

### 🎮 Controls
| Entity Name | Type | Description |
| :--- | :--- | :--- |
| **Amperage Limit** | `select` | Adjust charging speed dynamically (16A - 48A). |
| **Charge Control** | `switch` | Remote start/stop toggle for charging sessions. |

### 📊 Charging Metrics (Metric/CAD)
| Entity Name | Type | Description |
| :--- | :--- | :--- |
| **Charge Cost** | `sensor` | Real-time session cost in **CAD**. |
| **Energy Output** | `sensor` | Energy delivered in the current session (kWh). |
| **Power Output** | `sensor` | Real-time charging speed in kW. |
| **Kilometers Added** | `sensor` | Estimated range added during the session (km). |
| **KM / Hour Added** | `sensor` | Current charging efficiency speed (km/h). |
| **Charging Time** | **sensor** | Active session duration (HH:MM:SS). |
| **Account Balance** | `sensor` | Remaining ChargePoint account credit in **CAD**. |

### 🔌 Connectivity & Status
| Entity Name | Type | Description |
| :--- | :--- | :--- |
| **Plugged In** | `binary_sensor` | Returns `True` when the J1772 cable is connected. |
| **Status** | `sensor` | High-level state (e.g., "Ready", "Charging"). |
| **Charger State** | `sensor` | Detailed internal state (e.g., "In Use", "Not Charging"). |

---

## 🛠️ Installation & Setup

1. Copy the `chargepoint` folder to your `custom_components/` directory.
2. **Restart Home Assistant.**
3. Navigate to **Settings > Devices & Services > Add Integration** and search for "ChargePoint (Custom Stealth)".
4. Enter your credentials.

> **Pro Tip:** For the **IONIQ 6**, set the Amperage Limit to **48A** to maximize Level 2 home charging on a standard 60A circuit.

---

## 📝 Credits
Maintained by **@rananna**. Based on the architecture by @mbillow. 
*v1.1.12 represents the final stable "Gold" release for residential Home Flex hardware.*
