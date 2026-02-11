#!/bin/bash
set -euo pipefail

# --- CONFIG ---
MQTT_USERNAME="${MQTT_USERNAME:-user1}"
MQTT_PASSWORD="${MQTT_PASSWORD:-password1}"
MOSQUITTO_PASSWD_FILE="./mosquitto/config/passwd_file"
MOSQUITTO_LOG_FILE="./mosquitto/log/mosquitto.log"
MOSQUITTO_DATA_DIR="./mosquitto/data"

# --- 1. Install Docker if missing ---
if ! command -v docker >/dev/null 2>&1; then
    echo "Docker not found. Installing..."
    sudo apt update
    sudo apt install -y ca-certificates curl gnupg lsb-release
    sudo mkdir -p /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
        $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
fi

# --- 2. Ensure mosquitto config directory exists ---
mkdir -p "./mosquitto/config"
echo "mosquitto_passwd_file: $MOSQUITTO_PASSWD_FILE"
mkdir  -p "$(dirname "$MOSQUITTO_PASSWD_FILE")" "$(dirname "$MOSQUITTO_LOG_FILE")" "$MOSQUITTO_DATA_DIR"
touch "$MOSQUITTO_PASSWD_FILE" "$MOSQUITTO_LOG_FILE"

# --- 3. Start Docker Compose ---
docker compose up -d

# --- 4. Create MQTT user ---
sudo docker exec -i mosquitto sh -c "mosquitto_passwd -b /mosquitto/config/passwd_file '$MQTT_USERNAME' '$MQTT_PASSWORD'"

echo "Project setup complete."
