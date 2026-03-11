# ChargePoint for Home Assistant (Custom Stealth) 🔌⚡

<p align="center">
  <img src="https://brands.home-assistant.io/_/chargepoint/logo.png" width="200" alt="ChargePoint Logo">
</p>

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
![Version](https://img.shields.io/badge/version-1.1.6-orange.svg?style=for-the-badge)
![Stability](https://img.shields.io/badge/Stability-Stealth--Hardened-green?style=for-the-badge)

A high-performance, "bulletproofed" fork of the ChargePoint integration. Engineered to bypass 2026-era cloud security (DataDome) and optimized for the Hyundai IONIQ 6 and Home Flex hardware.

---

## 🔄 Changes from Original Fork (@mbillow)

This fork was created to resolve frequent `403 Forbidden` disconnections and transform the integration from "Read-Only" to "Full Control."

### 🛡️ Security & Stealth (The "Stealth" Layer)
- **Chrome 123 Headers:** Mimics a modern desktop browser to bypass DataDome CAPTCHA blocks.
- **Smart Back-off Logic:** Automatically enters a **60-minute cool-down** if a block is detected, preventing permanent IP bans.
- **Critical Bugfix (v1.1.6):** Resolved `ImportError` and `NameError` in `switch.py` and `select.py` by standardizing internal constants.

### 🕹️ Active Control (Write Access)
Unlike the original, this version adds native **Switch**, **Select**, and **Button** platforms:
- **Charge Control Switch:** Start or stop charging sessions with a single toggle.
- **Amperage Selector:** Dynamically adjust charging speed (e.g., 6A to 48A) for load shedding.
- **Restart Button:** Soft-reboot the Home Flex hardware via the Cloud API.

### 📊 Data Integrity & Diagnostics
- **Math Safety:** Prevents `TypeError` crashes on null/empty API responses during vehicle handshakes.
- **Energy Dashboard Persistence:** Uses `TOTAL_INCREASING` logic to eliminate negative spikes in the Home Assistant Energy tab.
- **Wi-Fi Signal (RSSI):** Monitor your charger's connection quality in real-time to troubleshoot garage dropouts.

---

## 🛠️ Installation

1. Open **HACS** in Home Assistant.
2. Go to **Integrations** > **Three Dots (Top Right)** > **Custom Repositories**.
3. Add `https://github.com/rananna/ha-chargepoint` as an **Integration**.
4. Download **v1.1.6** and **Restart Home Assistant**.
5. **Pro-Tip:** If upgrading from an older version, delete the integration from "Devices & Services" and re-add it to ensure the new entities (Select/Switch) are registered correctly.

## ⚠️ Dealing with 403 Forbidden
If you see a 403 error in your logs:
- **Wait:** The integration will auto-retry in 1 hour.
- **Cool Down:** If persistent, disable for 24 hours to reset your IP reputation.
- **Modem Reset:** Power cycling your home router often grabs a fresh IP, bypassing the block immediately.

---

## 📝 Credits
Based on the original work by **@mbillow**. Enhanced and maintained by **@rananna** for superior reliability and control.
