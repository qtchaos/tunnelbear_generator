import asyncio
import random
import re
import sys
from math import sqrt

from pymailtm import pymailtm
from pymailtm.pymailtm import CouldNotGetAccountException

from utilities.data import Account
from utilities.etc import p_print, get_random_string, Colours


async def check_block(page, browser):
    try:
        await page.waitForSelector("#account-image > img", options={"timeout": 2500})
    except TimeoutError:
        p_print("You are getting blocked by TunnelBear, try a VPN connection.", Colours.FAIL)
        await browser.close()
        await sys.exit(1)


async def navigate_type(page):
    """Navigates to the website and types in the credentials."""
    first_selector = "#nav-items > div.nav-menu > div.nav-items-wrap > div:nth-child(5) > a"
    second_selector = "#app > div.app-content > div:nth-child(2) > div > section > div > div > div > div > div > div:nth-child(4) > p > button"
    await page.goto("https://www.tunnelbear.com/")
    await page.click("#mobile-menu")

    await wait_custom(first_selector, page)
    await page.click(first_selector)

    await wait_custom(second_selector, page)
    await page.click(second_selector)

    await wait_custom("#email", page)
    await page.type("#email", Account.email)
    await page.type("#password", Account.password)
    await page.click("#signup-form > button > span")


async def wait_custom(selector, page):
    """Wait for a random amount of time."""
    await page.waitForSelector(selector)
    await asyncio.sleep(sqrt(random.random()))


async def initial_setup(context, message):
    """Initial setup for the account."""
    confirm_link = (re.findall(r"(https?:[^ ]*)", str(message).replace(")\\n\\nThat's", "")))[0]

    confirm_page = await context.newPage()
    await confirm_page.goto(confirm_link)


async def generate_mail():
    """Generate mail.tm account and return account credentials."""
    mail = pymailtm.MailTm()
    while True:
        try:
            account = mail.get_account()
            break
        except CouldNotGetAccountException:
            p_print("Retrying mail.tm account generation...", Colours.WARNING)

    Account.id = account.id_
    Account.email = account.address
    Account.email_password = account.password
    Account.password = get_random_string(16)


async def mail_login():
    """Logs into the mail.tm account with the generated credentials"""
    while True:
        try:
            mail = pymailtm.Account(Account.id, Account.email,
                                    Account.email_password)
            p_print("Retrieved mail successfully!", Colours.OKGREEN)
            return mail
        except CouldNotGetAccountException:
            continue
