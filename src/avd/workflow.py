"""AVD workflow using xfreerdp and Playwright."""

import sys
from re import Match
from typing import cast

import pexpect
from playwright.sync_api import sync_playwright


def avd_workflow(location: str, username: str):
    """AVD workflow using xfreerdp and Playwright."""

    command = "xfreerdp"
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
    ]

    print("Starting xfreerdp... waiting for output...")
    child = pexpect.spawn(command, args, encoding="utf-8")

    child.logfile = sys.stdout

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)

            context = browser.new_context(ignore_https_errors=True)

            for _ in range(2):

                child.expect(r"Browse to:\s*(https?://[^\s]+)", timeout=600)
                login_link = cast(Match[str], child.match).group(1)

                child.expect(r"Paste redirect URL here:\s*")

                page = context.new_page()
                page.goto(login_link)

                page.wait_for_url("**/nativeclient**", timeout=60000)

                redirect_url = page.url
                child.sendline(redirect_url)

                page.close()

            browser.close()

        child.expect(pexpect.EOF, timeout=None)

    except pexpect.EOF:
        print("xfreerdp closed successfully.")
    except pexpect.TIMEOUT:
        print("ERROR: Timed out waiting for URL or Browser action.")
    except (RuntimeError, OSError, KeyboardInterrupt) as e:
        print(f"ERROR during browser automation: {e}")
