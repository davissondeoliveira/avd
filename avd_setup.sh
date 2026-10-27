#!/usr/bin/env bash

main() {
    EXIT_SUCCESS=0

    echo -e "Setting up AVD environment \n\n"

    echo -e "Installing FreeRDP \n\n"
    sudo apt-get update && sudo apt-get install -y freerdp2-x11 || sudo apt-get install -y freerdp3-x11

    echo -e "Installing flatseal \n\n"
    sudo apt-get install -y flatpak
    flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
    flatpak install -y flathub com.github.tchx84.Flatseal
    flatpak override --user --socket=pcsc

    echo -e "Installing pipx (if not already installed) \n\n"
    sudo apt-get install -y pipx
    pipx ensurepath

    echo -e "Installing avd (as current user) \n\n"
    pipx install --force --pip-args="--no-cache-dir" git+https://github.com/davissondeoliveira/avd.git@main

    if xdg-settings get default-web-browser 2>/dev/null | grep -qi chrome; then
        echo -e "Installing Playwright's bundled Google Chrome \n\n"
        "$(pipx environment --value PIPX_LOCAL_VENVS)/avd/bin/playwright" install chrome
    else
        echo -e "Installing Playwright's bundled Firefox \n\n"
        "$(pipx environment --value PIPX_LOCAL_VENVS)/avd/bin/playwright" install firefox
    fi

    echo -e "Ensuring pipx path is configured \n\n"
    pipx ensurepath

    echo -e "Done! \n\n"
}

main