#!/bin/bash

# Обновление пакетов и установка зависимостей
echo "Updating packages..."
sudo apt-get update -y
sudo apt-get install -y ca-certificates curl

# Установка Docker GPG ключа
echo "Adding Docker's GPG key..."
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Добавление репозитория Docker в список источников APT
echo "Adding Docker repository..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Обновление списка пакетов
echo "Updating package list..."
sudo apt-get update -y

# Установка Docker
echo "Installing Docker..."
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose

# Проверка версии Docker
echo "Docker installation completed. Verifying installation..."
docker --version
docker-compose --version

echo "Docker has been installed and is ready to use!"
