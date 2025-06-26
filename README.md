# MoTeC Automator

This Ansible project automates the setup and configuration of a Raspberry Pi as a dedicated telemetry logger for `sim-to-motec`. It installs the application in a secure virtual environment and makes logs available via a simple network share. A web-based control panel allows for easy management of the service without needing to use the command line.

## Features

-   **Automated Setup:** Configures a Raspberry Pi into a dedicated telemetry appliance.
-   **Web Control Panel:** Start, stop, restart, and configure the logger from a simple web page hosted on the Pi. Includes a live log viewer for easy troubleshooting.
-   **Samba File Share:** Access your log files easily over the network at `\\race-pi\logs`.
-   **Multi-Sim Support:** Easily switch between `gt7` (Gran Turismo 7) and `ams2` (Automobilista 2) via a simple configuration change.
-   **On-Pi Status Script:** Includes a `status.sh` command for convenient terminal-based debugging.
-   **Automated Verification:** The playbook finishes with a self-test to confirm all services are running correctly.

---

## Quick Start Guide

### Step 1: Create and Edit Local Configuration

The `setup.sh` script is designed to be run twice initially.

```bash
chmod +x setup.sh
./setup.sh
```

The first time, it will create your local configuration files (`inventory.ini`, `config.yml`).

1.  **Edit `inventory.ini`:** Open this file and set your Raspberry Pi's IP address. You can also change the `ansible_user` if it's different from the default `pi`.
2.  **Edit `config.yml`:** Open this file and review the settings. You can set initial/default values for the logger here. These can be changed later via the web interface.

### Step 2: Run the Setup

Run the script again to provision the Raspberry Pi. The script will prompt for the SSH password of the user you defined in `inventory.ini`.

```bash
./setup.sh
```

---

## Post-Installation Usage

### Accessing the Web Control Panel
Once the setup is complete, open a web browser on your PC or Mac and navigate to:
`http://<your_pi_ip_address>:8080` (e.g., `http://10.0.0.5:8080`)

Use the web panel to change the Driver, Session, and Replay mode, then click "Save & Restart" to apply them.

### Accessing Your Log Files
1.  Open **File Explorer** on Windows or **Finder** on Mac.
2.  In the address bar, go to `\\race-pi` (Windows) or `smb://race-pi.local` (Mac).
3.  Open the `motec_logs` folder to find your `.ld` files.
