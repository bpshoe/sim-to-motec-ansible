#!/bin/bash
# scripts/diagnose.sh
# Full verbose diagnostics, then quick-triage summary

# Color codes
BOLD_BLUE='\033[1;34m'
BOLD_RED='\033[1;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Determine script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

print_section() {
  echo -e "\n${BOLD_BLUE}🔹 $1${NC}"
}

# --- Verbose Diagnostics ---

print_section "SYSTEMD SERVICE STATUS"
systemctl --no-pager --no-legend status motec-webapp nginx || true

print_section "RECENT LOGS (motec-webapp)"
journalctl -u motec-webapp -n 100 --no-pager --output=short-iso \
  || echo -e "${BOLD_RED}No logs found${NC}"

print_section "PORT LISTENERS (5000 & 8080)"
ss -tulnp | grep -E ":5000|:8080" \
  || echo -e "${BOLD_RED}No listeners found${NC}"

print_section "FASTAPI HEALTH CHECK"
curl -s -o /dev/null -w "Status: %{http_code}\n" http://localhost:5000/api/status \
  || echo -e "${BOLD_RED}Request failed${NC}"

print_section "NGINX PROXY CHECK"
curl -s -o /dev/null -w "Status: %{http_code}\n" http://localhost:8080/api/status \
  || echo -e "${BOLD_RED}Request failed${NC}"

print_section "SERVICE FILE EXISTENCE"
[ -f /etc/systemd/system/motec-webapp.service ] \
  && echo -e "${GREEN}motec-webapp.service exists${NC}" \
  || echo -e "${BOLD_RED}Service file missing${NC}"

print_section "SYSTEMD ENVIRONMENT VARIABLES"
systemctl show motec-webapp --property=Environment \
  || echo -e "${BOLD_RED}No environment variables found${NC}"

print_section "DISK & MEMORY SNAPSHOT"
df -h / | grep -v tmpfs; echo; free -m

print_section "PYTHON TRACEBACKS (last 5)"
journalctl -u motec-webapp | grep -i traceback | tail -n 5 \
  || echo -e "${GREEN}No tracebacks found${NC}"

print_section "PYTHON VERSION"
python3 --version \
  || echo -e "${BOLD_RED}Python3 not found${NC}"

print_section "SYSTEM UPTIME"
uptime -p \
  || echo -e "${BOLD_RED}Could not retrieve uptime${NC}"

# --- Quick-Triage Summary ---

print_section "QUICK TRIAGE SUMMARY"
bash "${SCRIPT_DIR}/diagnose_quick.sh"