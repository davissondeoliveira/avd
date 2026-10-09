# AVD Python Package

A Python utility for establishing connections to Azure Virtual Desktop (AVD) environments on Linux.

## Overview

This package provides a wrapper for `xfreerdp` to seamlessly handle authentication, smart card routing, and session management when connecting to AVD, specifically optimized for Department of Defense (DoD) and Army environments.

## Prerequisites

Before using this tool, ensure your system has the following configured:

* **FreeRDP:** Properly installed `freerdp3-x11`. (use: `xfreerdp3 /version` to check if you have or not)

* **CAC** and proper drivers installed.

* **Connection File:** A valid AVD `.rdpw` configuration file.

## Installation

Install the package directly using the provided wheel file:

For Ubuntu/Debian-based systems:
```bash
sudo apt update
sudo apt install freerdp3-x11
```
For Fedora-based systems:
```bash
sudo dnf install freerdp3-x11
```

> **Note:** You will need to install (Flatseal)[https://flathub.org/en/apps/com.github.tchx84.Flatseal] or (option 2)[https://flathub.org/en/setup/Ubuntu]. Then enable `Smart Card` permissions for the AVD application.


Then:

```bash
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install your package / dependencies
pip install --upgrade pip
pip install avd-x.x.x.zip
playwright install
```

## Getting the RDP Configuration File

To use this utility, you first need to download your specific connection file from the [AVD web portal](https://rdweb.wvd.azure.us/arm/webclient/index.html).

1. **Configure Launch Settings:** Open your AVD portal **Settings** (usually a gear icon in the top right). Look for the "Resources Launch Method" section and select the **Download the rdp file** radio button.
   <br>![Download RDP Setting](images/step1.png)

2. **Select Your Desktop:** Return to the main workspace screen. Click on the **Army Desktop** icon under your preferred region (e.g., Army 365 AVD - Arizona or Virginia).
   <br>![Select Location](images/step2.png)

3. **Save the File:** A file typically named `Army Desktop.rdpw` will download to your local machine. Take note of where this file is saved (e.g., your `Downloads` folder), as you will need to provide this path to the CLI tool.
   <br>![Downloaded RDP File](images/step3.png)

## Usage

Start an AVD connection using the `start` command.

```bash
avd start -u <username> -l <path_to_rdp_file>
```

### Options

* `-u, --username`: Your AVD connection username (required). This should be your official `Army.mil` email address.

* `-l, --location`: Absolute or relative path to the AVD connection file you downloaded (default: `Army Desktop.rdpw`).

### Example

```bash
avd start -u john.doe@army.mil -l "/home/user/Downloads/Army Desktop.rdpw"
```

## Authentication Flow

Once the command is executed, the tool will guide you through the standard DoD authentication sequence. Here is what to expect:

1. **Microsoft Sign-in:** You will first be prompted by Microsoft to enter your email.
   <br>![Microsoft Sign in](images/step4.png)

2. **Certificate Selection:** A dialog will appear asking you to select a certificate to authenticate yourself; choose your active DOD ID certificate.

3. **Security Device Unlock:** You must enter your Smart Card PIN to unlock the security device.

4. **Connection Consent:** Microsoft will ask you to confirm and allow the remote desktop connection to the specific AVD host.

5. **DoD Warning Statement:** Finally, the FreeRDP window will launch, presenting the standard US Department of Defense Warning Statement, which you must acknowledge by clicking "OK" to access your desktop.
   <br>![DoD Warning Statement](images/dod_page.png)

## Support

For technical questions, bug reports, or feature requests, please contact the repository maintainer or open an issue in the project tracker.


EXTRA:

Install flatseal:
sudo apt install flatpak
sudo apt install gnome-software-plugin-flatpak
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install flathub com.github.tchx84.Flatseal


if cac doesnt show:
1.Ensure you have Native Chrome:Requirement.Do not use the Ubuntu App Center to install Chromium or Firefox. Download and install the official Google Chrome .deb package directly from Google's website so it runs natively on the host.
2.Install Smartcard and NSS Tools:Terminal.You need the OpenSC smartcard driver and the NSS database management tools. Run this in your terminal:Bashsudo apt-get update
sudo apt-get install pcscd opensc libnss3-tools
3.Register the CAC Driver:Terminal.Register the OpenSC driver to your local NSS database so Chrome knows how to read the smartcard. Run these commands:Bashmkdir -p $HOME/.pki/nssdb
modutil -dbdir sql:$HOME/.pki/nssdb/ -add "OpenSC" -libfile /usr/lib/x86_64-linux-gnu/opensc-pkcs11.so
To verify it worked, run modutil -dbdir sql:$HOME/.pki/nssdb/ -list and ensure "OpenSC" appears in the output.
1.Create a Dedicated Profile Folder:Terminal.Create a permanent directory on your host machine to store the Playwright Firefox database and session data.Bashmkdir -p ~/.playwright-firefox-profile
2.Inject the OpenSC Driver:Terminal.Use the NSS tools you installed earlier to register the OpenSC driver into this new folder. Playwright's bundled Firefox will read this database upon launch.Bashmodutil -dbdir sql:$HOME/.playwright-firefox-profile -add "OpenSC" -libfile /usr/lib/x86_64-linux-gnu/opensc-pkcs11.so
Note: If it prompts you to create a new database password, simply press Enter to leave it blank.