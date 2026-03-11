# ChargePoint for Home Assistant (Custom Stealth)

A cloud-polling Home Assistant component to expose ChargePoint Home Charger and Account information. This version is modified to include stealth masking and data safety nets to prevent cloud-blocking and integration crashes.

![home assistant entities](https://github.com/mbillow/ha-chargepoint/raw/main/.github/images/ha_chargepoint_sensor_card.png)

## Key Improvements in this Version

* **Stealth User-Agent:** Injects a modern browser identity to bypass `403 Forbidden` / DataDome bot-blocking screens.
* **Math Safety Nets:** Intercepts `None` or empty string values from the API for Power, Energy, and Time sensors to prevent `TypeError` crashes.
* **Binary Sensors:** Adds native `binary_sensor` entities for "Plugged In" status, enabling proper dashboard icons and simpler automations.
* **Fixed Session Persistence:** Corrects a bug where refreshed session tokens weren't saved, leading to frequent logouts.

## Installation

### Via HACS (Recommended)

1. Ensure **HACS** is installed.
2. Navigate to **HACS > Integrations**.
3. Click the **three dots** in the top right and select **Custom repositories**.
4. Paste the URL of your repository: `https://github.com/YOUR_USERNAME/ha-chargepoint-custom`
5. Select **Integration** as the category and click **Add**.
6. Find **ChargePoint Custom Stealth** and click **Download**.
7. **Restart Home Assistant.**

## Usage

Once installed, go to `Settings > Devices & Services` and click `+ Add Integration`. Search for **ChargePoint** and enter your credentials.

> [!CAUTION]
> **Rate Limiting & Blocks:** If you see a `403 Forbidden` error in your logs, ChargePoint has flagged your IP. **Disable the integration for 12–24 hours** to allow the block to expire. Avoid polling intervals faster than 15 minutes.

## Energy Tracking

This integration is fully compatible with the Home Assistant **Energy Dashboard**. 
1. Add the `Energy Output` sensor as a grid consumption source.
2. Use the `Charge Cost` sensor as the "entity tracking the total costs."



## New Binary Sensors

This version includes a `binary_sensor` for your charger. Unlike the standard text sensor, this allows for:
* **Device Classes:** Correctly identified as a `plug` class.
* **Easy Automations:** Trigger alerts if the car isn't plugged in by a certain time.

## Development and Contributing

If you notice issues, please create an issue with your logs. 

### Local Testing
To test logic without hitting the cloud too hard, you can use the included `docker-compose` setup:
```shell
docker-compose up -d
