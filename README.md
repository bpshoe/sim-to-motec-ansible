# MoTeC Automator

This Ansible project automates the setup and configuration of a Raspberry Pi as a dedicated telemetry logger for `sim-to-motec`. It installs the application in a secure virtual environment and makes logs available via a simple network share. A web-based control panel allows for easy management of the service without needing to use the command line.

## Features

-   **Automated Setup:** Configures a Raspberry Pi into a dedicated telemetry appliance.
-   **Web Control Panel:** Start, stop, and restart the logger from a simple web page.
-   **Samba File Share:** Access your log files easily over the network at `\\race-pi\logs`. **No complex Google Drive setup required.**
-   **Multi-Sim Support:** Easily switch between `gt7` (Gran Turismo 7) and `ams2` (Automobilista 2) via a simple configuration change.
-   **On-Pi Status Script:** Includes a `status.sh` command for convenient terminal-based debugging.

---

## Quick Start Guide

### 1. Create and Edit Local Configuration

The `setup.sh` script is designed to be run twice initially.

```bash
chmod +x setup.sh
./setup.sh
```

The first time, it will create your local configuration files (`inventory.ini`, `config.yml`).

-   **Edit `inventory.ini`:** Set your Raspberry Pi's IP address and the `ansible_user` (e.g., `pi`).
-   **Edit `config.yml`:** Review the settings and adjust as needed, especially the `sim_type` and `playstation_ip` (if using GT7).

### 2. Run the Setup

Run the script again to provision the Raspberry Pi. The script will prompt for the SSH password of the user you defined in `inventory.ini`.

```bash
./setup.sh
```

---

## Post-Installation Usage

### Accessing the Web Control Panel
Once the setup is complete, open a web browser on your PC or Mac and navigate to:
`http://<your_pi_ip_address>:8080` (e.g., `http://10.0.0.5:8080`)

### Accessing Your Log Files
1.  Open **File Explorer** on Windows or **Finder** on Mac.
2.  Go to `\\race-pi` (Windows) or `smb://race-pi.local` (Mac).
3.  Open the `motec_logs` folder to find your `.ld` files.

---

## Troubleshooting

A simple script is installed on your Raspberry Pi to check the status of all services.
1.  Log into your Pi: `ssh <user>@<pi_ip>`
2.  Run the status command: `status.sh`
