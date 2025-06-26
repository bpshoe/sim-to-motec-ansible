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

if [ ! -f "inventory.ini" ]; then
    cp inventory.ini.example inventory.ini
    CONFIG_CREATED=true
fi
if [ ! -f "config.yml" ]; then
    cp config.yml.example config.yml
    CONFIG_CREATED=true
fi

if [ "$CONFIG_CREATED" = true ]; then
    echo -e "\n${GREEN}Configuration files have been created.${NC}"
    echo -e "Please edit ${YELLOW}inventory.ini${NC} and ${YELLOW}config.yml${NC} with your details."
    echo -e "\nAfter that, run this script again."
    exit 0
fi

echo -e "${GREEN}Configuration files found.${NC}"

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
