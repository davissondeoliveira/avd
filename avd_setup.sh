#!/usr/bin/env bash

detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo "$ID"
    elif [ -f /etc/redhat-release ]; then
        echo "fedora"
    else
        echo "unknown"
    fi
}

main() {
    EXIT_SUCCESS=0
    DISTRO=$(detect_distro)

    echo -e "Setting up AVD environment for $DISTRO \n\n"

    if [ "$DISTRO" = "ubuntu" ] || [ "$DISTRO" = "debian" ]; then
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

    elif [ "$DISTRO" = "fedora" ]; then
        echo -e "Installing FreeRDP \n\n"
        sudo dnf install -y freerdp

        echo -e "Installing flatseal \n\n"
        sudo dnf install -y flatpak
        flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
        flatpak install -y flathub com.github.tchx84.Flatseal
        flatpak override --user --socket=pcsc

        echo -e "Installing avd with pip \n\n"
        pip install --user --force-reinstall --no-cache-dir git+https://github.com/davissondeoliveira/avd.git@main

        if xdg-settings get default-web-browser 2>/dev/null | grep -qi chrome; then
            echo -e "Installing Playwright's bundled Google Chrome \n\n"
            python -m playwright install chrome
        else
            echo -e "Installing Playwright's bundled Firefox \n\n"
            python -m playwright install firefox
        fi

    else
        echo "The following: $DISTRO is unsupported on this setup script. Please use Ubuntu, Debian, or Fedora."
        exit 1
    fi

    echo -e "Done! \n\n"
}

main