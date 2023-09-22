import asyncio

import pyppeteer as pyppeteer
import argparse
from faker import Faker
from pymailtm.pymailtm import Account

from utilities.data import AccountEncoder, Account
from utilities.etc import p_print, Colours, clear_console, clear_tmp, save_credentials
from utilities.web import navigate_type, generate_mail, check_block, mail_login, initial_setup

args = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-infobars",
    "--window-position=0,0",
    "--ignore-certificate-errors",
    "--ignore-certificate-errors-spki-list",
    'referer: "https://www.google.com/"'
    "sec-ch-ua-mobile: ?0",
    'sec-ch-ua-platform: "Windows"',
    'sec-fetch-dest: document',
    'sec-fetch-mode: navigate',
    'sec-fetch-site: same-origin',
    'sec-fetch-user: ?1',
    'upgrade-insecure-requests: 1',
    'user-agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"',
]

faker = Faker()
loops = 0

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--loop', required=False, action='store_true',
                    help='Automatically create new accounts in an infinite loop.')

console_args = parser.parse_args()


async def register():
    browser = await pyppeteer.launch({
        "headless": True,
        "ignoreHTTPSErrors": True,
        "userDataDir": "./tmp",
        "args": args,
        "autoClose": False,
        "ignoreDefaultArgs": ["--enable-automation", "--disable-extensions"],
    })

    await generate_mail()

    context = await browser.createIncognitoBrowserContext()
    page = await context.newPage()

    p_print("Registering account...", Colours.OKCYAN)
    await navigate_type(page)
    await check_block(page, browser)

    mail_account = await mail_login()
    while len(mail_account.get_messages()) == 0:
        await asyncio.sleep(1)

    messages = mail_account.get_messages()

    await initial_setup(context, messages)
    await browser.close()
    await save_credentials(Account, AccountEncoder)
    p_print("Verified account successfully!", Colours.OKGREEN)
    p_print(
        f"Email: {Account.email}\nPassword: {Account.password}", Colours.OKCYAN)

    if console_args.loop:
        p_print(f"Looping... {'' if loops == 0 else loops}")
        loops += 1
        await register()

if __name__ == "__main__":
    clear_console()

    clear_tmp()
    asyncio.run(register())
