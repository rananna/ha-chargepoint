# ChargePoint for Home Assistant (Custom Stealth)

A cloud-polling Home Assistant component to expose ChargePoint Home Charger and Account information. This version is a "bulletproofed" fork of the original integration, specifically modified to bypass modern cloud security blocks and prevent common math-related crashes.

![home assistant entities](https://github.com/rananna/ha-chargepoint/raw/main/.github/images/ha_chargepoint_sensor_card.png)

## Key Improvements in this Version

* **Stealth User-Agent:** Injects a modern browser identity to bypass `403 Forbidden` / DataDome bot-blocking screens.
* **Math Safety Nets:** Intercepts `None` or empty string values from the API for Power, Energy, and Time sensors to prevent `TypeError` crashes.
* **Binary Sensors:** Adds native `binary_sensor` entities for "Plugged In" status, enabling proper dashboard icons and simpler automations.
* **Fixed Session Persistence:** Corrects a bug where refreshed session tokens weren't saved to the config entry, leading to frequent logouts and 403 blocks.

## Installation

### Via HACS (Recommended)

1.  Ensure **HACS** is installed in your Home Assistant instance.
2.  Navigate to **HACS > Integrations**.
3.  Click the **three dots** in the top right corner and select **Custom repositories**.
4.  Paste the URL of this repository: `https://github.com/rananna/ha-chargepoint-custom`
5.  Select **Integration** as the category and click **Add**.
6.  Search for **ChargePoint Custom Stealth** and click **Download**.
7.  **Restart Home Assistant.**

## Usage

Once installed, go to `Settings > Devices & Services` and click `+ Add Integration`. Search for **ChargePoint** and enter your credentials.

> [!CAUTION]
> **Rate Limiting & Blocks:** If you see a `403 Forbidden` error in your logs, ChargePoint has flagged your IP. **Disable the integration for 12–24 hours** to allow the block to expire. Avoid polling intervals faster than 15 minutes to stay under the radar.

## Energy Tracking

This integration is fully compatible with the Home Assistant **Energy Dashboard**.
1.  Add the `Energy Output` sensor as a grid consumption source.
2.  Use the `Charge Cost` sensor as the "entity tracking the total costs."

## New Binary Sensors

This version includes a dedicated `binary_sensor` for your charger status. Unlike the standard text sensor, this allows for:
* **Device Classes:** Correctly identified as a `plug` class for better UI rendering.
* **Easy Automations:** Trigger alerts if the car isn't plugged in by a certain time (e.g., 9:00 PM).

## Development and Contributing

If you notice any issues, please create a GitHub issue describing the error and include any error messages or stack traces from your Home Assistant logs.

### Running the Integration (Docker)

A simple Docker Compose file is included to launch a test Home Assistant instance with the integration pre-installed:
```shell
docker-compose up -d
