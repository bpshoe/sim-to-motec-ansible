#!/bin/bash
# This script runs the Ansible playbook to provision the Raspberry Pi.

# --- CHANGE DIRECTORY TO SCRIPT LOCATION ---
# This ensures that all relative paths work correctly,
# regardless of where the script is called from.
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Define Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

# --- Pre-flight Checks and Config Creation ---
echo "Verifying project setup..."
CONFIG_CREATED=false

# Check for inventory.ini
if [ ! -f "inventory.ini" ]; then
    if [ -f "inventory.ini.example" ]; then
        echo "Creating 'inventory.ini' from template..."
        cp inventory.ini.example inventory.ini
        CONFIG_CREATED=true
    else
        echo -e "${RED}Error: 'inventory.ini.example' is missing. Cannot create config.${NC}" >&2
        exit 1
    fi
fi

# Check for config.yml
if [ ! -f "config.yml" ]; then
    if [ -f "config.yml.example" ]; then
        echo "Creating 'config.yml' from template..."
        cp config.yml.example config.yml
        CONFIG_CREATED=true
    else
        echo -e "${RED}Error: 'config.yml.example' is missing. Cannot create config.${NC}" >&2
        exit 1
    fi
fi

# If we just created the files, instruct the user and exit.
if [ "$CONFIG_CREATED" = true ]; then
    echo -e "\n${GREEN}Configuration files have been created.${NC}"
    echo -e "Please edit ${YELLOW}inventory.ini${NC} and ${YELLOW}config.yml${NC} with your details."
    echo -e "Then, place your Google Cloud key file in this directory."
    echo -e "\nAfter that, run this script again."
    exit 0
fi

echo -e "${GREEN}Configuration files found.${NC}"

# --- Dependency Checks ---
echo "Checking for local dependencies..."
if ! command -v ansible >/dev/null 2>&1; then
    echo -e "${RED}Error: Ansible is not installed.${NC}" >&2
    echo "Please install it to continue." >&2
    exit 1
fi
echo -e "${GREEN}Dependencies found.${NC}"

GCP_KEY_FILE=$(grep 'gcp_key_file:' config.yml | awk '{print $2}' | tr -d '"')
if [ ! -f "$GCP_KEY_FILE" ]; then
    echo -e "${RED}Error: Google Cloud key file '${GCP_KEY_FILE}' not found.${NC}" >&2
    echo "Please place your service account key in this directory and check the 'gcp_key_file' setting in config.yml." >&2
    exit 1
fi
echo -e "${GREEN}Google Cloud key found.${NC}"

# --- Run Ansible Playbook ---
echo ""
echo "Preparing to run Ansible playbook..."
echo "You will be prompted for an SSH password."
echo ""
ansible-playbook playbook.yml --ask-pass -v
ANSIBLE_EXIT_CODE=$?
if [ ${ANSIBLE_EXIT_CODE} -eq 0 ]; then
    echo -e "${GREEN}Setup script finished successfully!${NC}"
    echo "Your Raspberry Pi is now configured."
else
    echo -e "${RED}Setup script failed with exit code ${ANSIBLE_EXIT_CODE}.${NC}"
fi
exit ${ANSIBLE_EXIT_CODE}
