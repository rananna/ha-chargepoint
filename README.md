# ChargePoint for Home Assistant (Custom Stealth)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
![Version](https://img.shields.io/badge/version-1.1.3-orange.svg)

A "bulletproofed" fork of the original ChargePoint integration. This version is specifically optimized for **2026 security standards**, adding stealth layers to bypass DataDome bot-blocking and robust safety nets for the Home Assistant Energy Dashboard.

## 🚀 Key Enhancements (v1.1.3)

- **DataDome Bypass:** Injects a verified **Chrome 123** User-Agent to prevent the common `403 Forbidden` CAPTCHA lockout.
- **Fail-Safe Math:** Custom helpers intercept `None` or `NaN` API responses during vehicle handshakes, preventing `TypeError` from crashing the integration.
- **Energy Dashboard Stability:** Implemented `TOTAL_INCREASING` persistence. Sensors will hold their last known value if the API temporarily reports zero, preventing massive energy spikes.
- **Binary "Plug" Logic:** Replaces the text-based status for cable connection with a native `binary_sensor` for immediate dashboard feedback and cleaner automations.

## 📊 Available Entities

### 👤 Account Level
* **Account Balance:** Your current wallet balance and currency.
* **User Profile:** (Attribute) Displays your ChargePoint User ID and Username.

### 🔌 Home Charger (Per Device)
* **Charging Status:** Real-time state (Available, Charging, Finishing, etc.).
* **Plugged In (Binary):** Native plug icon that reflects the physical connection.
* **Power Output:** Current draw in **kW**.
* **Energy Output:** Cumulative energy for the current session in **kWh**.
* **Charging Time:** Duration of current session in seconds (auto-formatted by HA).
* **Miles Added:** Estimated range added based on your vehicle's efficiency.
* **Charge Cost:** Real-time cost calculation based on your utility rate.
* **Technical Info:** (Attributes) Software version, Serial Number, and Model ID (e.g., CPH50).

## 🛠️ Installation

### Via HACS (Recommended)
1. Navigate to **HACS > Integrations**.
2. Click the **three dots** (top right) > **Custom repositories**.
3. Repository: `https://github.com/rananna/ha-chargepoint`
4. Category: **Integration**.
5. Click **Download**, then **Restart Home Assistant**.

## ⚠️ Troubleshooting the "403" Lockout
If ChargePoint detects too many rapid requests, it may serve a CAPTCHA.
* **v1.1.3 Automatic Back-off:** The code will detect a 403 and automatically **wait 1 hour** before retrying to prevent a permanent IP ban.
* **Manual Cool-down:** If the issue persists, **Disable** the integration for 24 hours. This is the only way to reset your IP reputation with DataDome.

## 📝 Credits
Based on the original work by **@mbillow**. Updated and maintained by **@rananna** for improved stability and security compatibility.
