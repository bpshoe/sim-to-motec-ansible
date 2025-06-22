# Sim-to-MoTeC Automator

This Ansible project fully automates the setup and configuration of a Raspberry Pi as a dedicated telemetry logger for `sim-to-motec`. It installs the application in a secure virtual environment and sets up **event-driven, on-demand** log uploads to a Google Drive folder that you control.

Log files are automatically categorized into sub-folders based on the track name.

## Features

-   **Automated Setup:** Configures a standard Raspberry Pi into a dedicated telemetry appliance.
-   **Multi-Sim Support:** Easily switch between `gt7` (Gran Turismo 7) and `ams2` (Automobilista 2) via a simple configuration change.
-   **On-Demand Uploads:** Automatically detects when a new log file is created and uploads it to your Google Drive.
-   **Organized Storage:** Creates sub-folders in your Google Drive for each track, keeping your logs neatly organized.
-   **Flexible Configuration:** Control replay mode, driver names, upload behavior, and more from a central config file.
-   **Easy Monitoring:** Includes a simple `status.sh` script that is installed on the Pi for easy real-time monitoring.

---

## Quick Start Guide

### Step 1: Google Drive & Service Account Setup

This is a one-time setup to create a secure "robot" account that the script will use to upload files without needing your personal Google password.

1.  **Create a Google Drive Folder:** Go to your regular Google Drive and create a new, empty folder. Name it whatever you like (e.g., `Sim_MoTeC_Logs`).
2.  **Get the Folder ID:** Open the folder. The ID is the long string of letters and numbers in the URL, after `.../folders/`. For example, if the URL is `https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h9i0j`, your folder ID is `1a2b3c4d5e6f7g8h9i0j`. Copy this ID. You will need it for `config.yml`.
3.  **Create a Cloud Project:** Go to the [Google Cloud Console](https://console.cloud.google.com/projectcreate) and create a new project (e.g., `pi-motec-uploader`).
4.  **Enable the API:** In the project dashboard, use the search bar to find and **Enable** the "Google Drive API".
5.  **Create Service Account:**
    * In the left menu, go to `APIs & Services > Credentials`.
    * Click `+ CREATE CREDENTIALS` and select `Service account`.
    * Give it a name (e.g., `motec-pi-robot`) and click through the optional steps (`Grant access` sections can be skipped).
6.  **Get the Service Account Email:** On the Credentials screen, find the service account you just created. Copy its long email address (e.g., `motec-pi-robot@pi-motec-uploader.iam.gserviceaccount.com`).
7.  **Share Your Folder:** Go back to your Google Drive, right-click on the folder you created in Step 1, and select **Share**. Paste the service account's email address into the sharing dialog and grant it **Editor** permissions.
8.  **Generate JSON Key:** In the Google Cloud Console, click on the service account's email address, go to the **KEYS** tab, click **ADD KEY**, and create a new **JSON** key. A file will be downloaded.
9.  **Place Key File:** Move the downloaded JSON key file into this `motec/` project directory.

### Step 2: Create and Edit Local Configuration

The `setup.sh` script is designed to be run twice initially.

```bash
chmod +x setup.sh
./setup.sh
```

The first time you run it, it will create your local configuration files (`inventory.ini`, `config.yml`) from templates.

-   Open `inventory.ini` and set your Raspberry Pi's IP address and the `ansible_user`.
-   Open `config.yml` and adjust the variables to your needs.
-   Ensure the `gcp_key_file` in `config.yml` matches the filename of the key you downloaded.

### Step 3: Run the Setup

Run the script again to provision the Raspberry Pi. The script will prompt for the SSH password of the user you defined in `inventory.ini`.

```bash
./setup.sh
```

---

## Post-Installation Monitoring & Troubleshooting

A simple script is installed on your Raspberry Pi to check the status of all services.

1.  Log into your Pi: `ssh <user>@<pi_ip>`
2.  Run the status command: `status.sh`

This dashboard provides a quick overview. For more detailed logs, you can use these commands on the Pi:

| Command | Purpose |
| :--- | :--- |
| `sudo systemctl status sim-to-motec.service` | **Check Logger Status:** Use this first to see if the service is `active (running)` or if it has failed. |
| `journalctl -u sim-to-motec.service -f` | **Watch Live Logger Logs:** Streams the application's log in real-time. |
| `ls -l /opt/sim-to-motec/logs/{gt7,ams2}/` | **Check for Log Files:** See if the application is successfully creating `.ld` files. |
| `tail -f /var/log/rclone-upload.log` | **Watch Live Upload Logs:** The best way to see what `rclone` is doing. |
| `sudo tcpdump -i any -n udp port <port_number>` | **Monitor Network Traffic:** Use this to see if telemetry data is arriving from your console/PC. |
