"""AVD workflow using xfreerdp and Playwright."""

import sys
from re import Match
from typing import cast
import shutil
import os
import subprocess

import pexpect
from playwright.sync_api import sync_playwright


def get_xfreerdp_path():
    """Finds the available xfreerdp binary on the system."""
    for binary in ["xfreerdp3", "xfreerdp"]:
        path = shutil.which(binary)
        if path:
            return path
    raise RuntimeError(
        "Neither xfreerdp3 nor xfreerdp is installed. Please install FreeRDP."
    )


def launch_default_browser(p):
    """Detects the Linux default browser and maps it to a Playwright persistent context."""
    try:
        # Detect default browser
        default_app = subprocess.check_output(
            ["xdg-settings", "get", "default-web-browser"], text=True
        ).lower()

        if "chrome" in default_app:
            user_data_dir = os.path.expanduser("~/.config/google-chrome")
            return p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                channel="chrome",
                headless=False,
                ignore_https_errors=True,
            )
        user_data_dir = os.path.expanduser("~/.playwright-firefox-profile")
        return p.firefox.launch_persistent_context(
            user_data_dir=user_data_dir, headless=False, ignore_https_errors=True
        )

    except (subprocess.CalledProcessError, FileNotFoundError):
        user_data_dir = os.path.expanduser("~/.playwright-firefox-profile")
        return p.firefox.launch_persistent_context(
            user_data_dir=user_data_dir, headless=False, ignore_https_errors=True
        )


def avd_workflow(location: str, username: str):
    """AVD workflow using xfreerdp and Playwright."""

    command = get_xfreerdp_path()
    azure_url = (
        "https%3A%2F%2Fwww.wvd.azure.us%2F.default%20openid%20profile"
        "%20offline_access"
    )
    azure_access = (
        "https%%3A%%2F%%2Flogin.microsoftonline.com%%2Fcommon%%2Foauth2%%2Fnativeclient"
    )
    args = [
        location,
        f"/u:{username}",
        "/gateway:type:arm",
        "/sec:aad",
        f"/azure:ad:login.microsoftonline.us,avd-scope:{azure_url},avd-access:{azure_access}",
        "/smartcard",
        "/clipboard",
        "/sound:sys:pulse",
        "/cert:ignore",
    ]

    print("Starting xfreerdp... waiting for output...")
    child = pexpect.spawn(command, args, encoding="utf-8")

    child.logfile = sys.stdout

    try:
        with sync_playwright() as p:

            context = launch_default_browser(p)
            page = context.pages[0]

            for _ in range(2):

                child.expect(r"Browse to:\s*(https?://[^\s]+)", timeout=600)
                login_link = cast(Match[str], child.match).group(1)

                child.expect(r"Paste redirect URL here:\s*")

                page.goto(login_link)

                page.wait_for_url("**/nativeclient**", timeout=60000)

                redirect_url = page.url
                child.sendline(redirect_url)

            context.close()

        child.expect(pexpect.EOF, timeout=None)

    except pexpect.EOF:
        print("xfreerdp closed successfully.")
    except pexpect.TIMEOUT:
        print("ERROR: Timed out waiting for URL or Browser action.")
    except (RuntimeError, OSError, KeyboardInterrupt) as e:
        print(f"ERROR during browser automation: {e}")
