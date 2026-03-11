# ChargePoint for Home Assistant (Custom Stealth) ⚡

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
![Version](https://img.shields.io/badge/version-1.1.4-orange.svg)

A professional-grade fork of the ChargePoint integration, hardened for 2026 security standards and optimized for Home Flex hardware (tested with Hyundai IONIQ 6).

---

## 🔄 Changes from Original Fork (@mbillow)

This fork was created to address critical stability issues and functional gaps in the original integration. Below are the key improvements:

### 🛡️ Security & Anti-Bot Bypassing
- **Chrome 123 Stealth Headers:** Replaces generic Python headers with a modern browser identity to bypass **DataDome/Cloudflare 403 Forbidden** blocks.
- **Smart Back-off Logic:** If the API returns a 403 error, the integration automatically enters a "cool-down" period for **60 minutes** rather than spamming requests and risking a permanent IP ban.

### 🕹️ New Active Controls (Write Access)
The original integration was "Read-Only." This version adds a new **Button Platform**:
- **Start Charge:** Manually trigger a charging session from your dashboard.
- **Stop Charge:** Cease an active session remotely.
- **Restart Charger:** Soft-reboot the Home Flex hardware via the Cloud API.

### 📊 Data Integrity & Math Safety
- **Zero-Value Protection:** Added safety helpers to prevent `TypeError` crashes when the API returns `None` or `NaN` (common during vehicle handshake).
- **Energy Dashboard Persistence:** Implemented `TOTAL_INCREASING` logic with "Last Known Value" memory. This prevents massive negative spikes in the Energy Dashboard when a session ends and data temporarily resets to zero.

### 📡 Advanced Diagnostics
- **Wi-Fi Signal Strength (RSSI):** Real-time monitoring of your charger's connection quality to help troubleshoot dropouts.
- **Last Cloud Heartbeat:** A timestamped sensor showing exactly when the charger last successfully communicated with ChargePoint.

---

## 🛠️ Installation

1. Open **HACS** in Home Assistant.
2. Go to **Integrations** > **Three Dots (Top Right)** > **Custom Repositories**.
3. Add: `https://github.com/rananna/ha-chargepoint` as an **Integration**.
4. Download **v1.1.4** and **Restart Home Assistant**.

## ⚠️ Troubleshooting 403 Errors
If your integration shows "Needs Attention" or a 403 in the logs:
- **Do not restart it repeatedly.** The new code will automatically wait 1 hour.
- If persistent, **Disable** for 24 hours to reset your IP reputation with DataDome.
- Cycling your home modem to get a fresh IP address is often an instant fix.

---

## 📝 Credits
Based on the original work by **@mbillow**. Maintained and enhanced by **@rananna** for superior reliability and control.
