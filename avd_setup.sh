#!/usr/bin/env bash

main() {
    EXIT_SUCCESS=0

    echo "Setting up AVD environment..."

    echo "Installing FreeRDP..."
    sudo apt-get update && sudo apt-get install -y freerdp2-x11 || sudo apt-get install -y freerdp3-x11

    echo "Installing flatseal..."
    sudo apt-get install -y flatpak
    flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
    flatpak install -y flathub com.github.tchx84.Flatseal
    flatpak override --user --socket=pcsc

    echo "Installing avd (as current user)..."
    pipx install --force --pip-args="--no-cache-dir" git+https://github.com/davissondeoliveira/avd.git@main

    echo "Ensuring pipx path is configured..."
    pipx ensurepath

    echo "Done!"
}

main