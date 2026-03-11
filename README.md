# ChargePoint for Home Assistant (Custom Stealth) ⚡

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
![Version](https://img.shields.io/badge/version-1.1.5-orange.svg)

A professional-grade fork of the ChargePoint integration, hardened for 2026 security standards and optimized for Home Flex hardware (tested with Hyundai IONIQ 6).

---

## 🔄 Changes from Original Fork (@mbillow)

This fork addresses critical stability issues and adds full "write" capability for charger control:

### 🛡️ Security & Stability
- **Stealth User-Agent:** Mimics Chrome 123 to bypass DataDome 403 blocks.
- **Auto-Backoff:** Detects 403 errors and automatically pauses updates for **60 minutes** to protect your IP address.
- **Math Safety:** Helpers to prevent crashes on null/empty API responses.

### 🕹️ Active Control (Write Access)
Adds a new **Button Platform** for direct hardware control:
- **Start / Stop Charge:** Control your session directly from the UI.
- **Restart Charger:** Soft-reboot the hardware via the cloud API.

### 📊 Advanced Diagnostics
- **Wi-Fi Signal (RSSI):** Monitor connection quality in the garage.
- **Last Heartbeat:** Tracks precisely when the charger last checked in.
- **Energy Stability:** Fixed Energy Dashboard spikes using `TOTAL_INCREASING` persistence.

---

## 🛠️ Installation

1. Add `https://github.com/rananna/ha-chargepoint` as a Custom Repository in **HACS**.
2. Download **v1.1.5** and **Restart Home Assistant**.
3. **Important:** If you have an old version installed, delete the integration entry from "Devices & Services" and add it fresh to clear database errors.

## 📝 Credits
Based on the original work by **@mbillow**. Enhanced by **@rananna**.
