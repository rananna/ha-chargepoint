# ChargePoint for Home Assistant (Custom Stealth) 🔌⚡

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
![Version](https://img.shields.io/badge/version-1.1.4-orange.svg)

A high-performance, "bulletproofed" fork of the ChargePoint integration. This version is specifically engineered to bypass modern cloud security blocks (DataDome) and provide robust data for the Home Assistant Energy Dashboard.

## 🚀 Why this fork? (v1.1.4)

Unlike the standard integration, this version includes specific fixes for 2026-era cloud requirements:

- **Stealth Networking:** Uses a verified **Chrome 123** User-Agent to prevent the `403 Forbidden` CAPTCHA lockout.
- **Active Control (New!):** Added native **Start**, **Stop**, and **Restart** button entities for direct charger control.
- **Math Safety Nets:** Custom helpers prevent `TypeError` crashes when the API returns null or empty values during vehicle handshakes.
- **Energy Stability:** Uses `TOTAL_INCREASING` persistence to prevent erratic energy spikes when charging sessions end.
- **Auto-Backoff:** If a security block is detected, the integration automatically pauses for **1 hour** to protect your IP reputation.

## 📊 Available Entities

### 👤 Account & Profile
* **Account Balance:** Current wallet credit and currency.
* **User Info:** (Attributes) Username and User ID.

### 🔌 Home Flex Charger
* **Status:** Real-time state (Available, Charging, Finishing).
* **Power:** Current draw in **kW**.
* **Energy:** Cumulative session energy in **kWh** (Energy Dashboard ready).
* **Plugged In:** Native binary sensor for physical connection status.
* **Buttons:** Start Charge, Stop Charge, and Restart Charger.
* **Diagnostics:** Last Connected time, Signal Strength, and Firmware Version.

## 🛠️ Installation

### Via HACS (Recommended)
1. Navigate to **HACS > Integrations**.
2. Click the **three dots** (top right) > **Custom repositories**.
3. Repository: `https://github.com/rananna/ha-chargepoint`
4. Category: **Integration**.
5. Click **Download**, then **Restart Home Assistant**.

## ⚠️ Dealing with 403 Forbidden / CAPTCHA
If your logs show a `403` error, ChargePoint's security layer (DataDome) has flagged your IP. 
1. **Don't Panic:** v1.1.4 will automatically stop retrying for 60 minutes.
2. **The Fix:** If the block persists, **Disable** the integration for 12–24 hours. 
3. **Pro-Tip:** Power cycling your home internet modem can often grab a fresh IP address and bypass the block immediately.

## 📝 Credits
Based on the original work by **@mbillow**. Maintained and enhanced by **@rananna** for superior stability and security.
