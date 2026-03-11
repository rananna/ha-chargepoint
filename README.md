# ChargePoint for Home Assistant (Custom Stealth) 🔌⚡

<p align="center">
  <img src="https://brands.home-assistant.io/_/chargepoint/logo.png" width="200" alt="ChargePoint Logo">
</p>

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
![Version](https://img.shields.io/badge/version-1.1.5-orange.svg?style=for-the-badge)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2026.3+-blue.svg?style=for-the-badge&logo=home-assistant)

A high-performance, "bulletproofed" fork of the ChargePoint integration. Engineered to bypass 2026-era cloud security (DataDome) and optimized for the Hyundai IONIQ 6 and Home Flex hardware.

---

## 🔄 Changes from Original Fork (@mbillow)

This fork was created to resolve frequent disconnections and add essential control features:

### 🛡️ Security & Stealth
- **Chrome 123 Headers:** Mimics a modern desktop browser to bypass `403 Forbidden` CAPTCHA blocks.
- **Smart Back-off Logic:** Automatically enters a **60-minute cool-down** if a block is detected, protecting your IP reputation.


### 🕹️ Active Control (Write Access)
Adds a new **Button Platform** for direct hardware management:
- **Start / Stop Charge:** Control sessions directly from your HA dashboard.
- **Restart Charger:** Soft-reboot the hardware via the cloud API.

### 📊 Data Integrity
- **Math Safety:** Prevents `TypeError` crashes on null/empty API responses.
- **Energy Dashboard Persistence:** Uses `TOTAL_INCREASING` logic to eliminate negative spikes when a session ends.


### 📡 Advanced Diagnostics
- **Wi-Fi Signal (RSSI):** Monitor your charger's connection quality in real-time.
- **Last Heartbeat:** Track precisely when the charger last checked in with the cloud.

---

## 🛠️ Installation

1. Open **HACS** in Home Assistant.
2. Go to **Integrations** > **Three Dots (Top Right)** > **Custom Repositories**.
3. Add `https://github.com/rananna/ha-chargepoint` as an **Integration**.
4. Download **v1.1.5** and **Restart Home Assistant**.

## ⚠️ Dealing with 403 Forbidden
If you see a 403 error in your logs:
- **Wait:** The integration will auto-retry in 1 hour.
- **Cool Down:** If persistent, disable for 24 hours.
- **Reset:** Power cycle your home modem to obtain a fresh IP address.

---

## 📝 Credits
Based on the original work by **@mbillow**. Enhanced and maintained by **@rananna**.
