import smtplib
import ssl
from email.message import EmailMessage
from getpass import getpass

from requests_html import HTMLSession

URL = 'https://www.lululemon.de/en-de/p/lululemon-align%E2%84%A2-pant-25inch/prod2020012.html'

class Crawler:
    prices = []
    desired_price = 100

    def __init__(self, desired_price):
        self.desired_price = desired_price


    def scan_prices(self):
        session = HTMLSession()
        page = session.get(URL)
        content = page.html.find('.product-detail-content', first=True)
        for price in content.find('.markdown-prices'):
            self.prices.append(price.text)

    def alert(self):
        for price in self.prices:
            if int(price[1:3]) <= self.desired_price:
                print(f'discount alert!! price: {price} is lower than desired price {self.desired_price}')
                Emailer().send_email()


class Emailer:
    subject: str = 'You favorite lulu leggings are on discount!'
    content: str = f'Don\'t miss it here: {URL}'
    from_address: str = 'yourdevaccount@gmail.com'
    to_address: str = 'yourprivateaccount@gmail.com'

    SMTP_SERVER = 'smtp.gmail.com'
    PORT = 465

    def _create_email(self):
        msg = EmailMessage()
        msg['Subject'] = self.subject
        msg['From'] = self.from_address
        msg['To'] = self.to_address
        msg.set_content(self.content)

        return msg

    def send_email(self):
        msg = self._create_email()

        context = ssl.create_default_context()

        password = getpass()

        with smtplib.SMTP_SSL(self.SMTP_SERVER, self.PORT, context=context) as server:
            server.login(self.from_address, password=password)
            server.send_message(msg)
            server.quit()


if __name__ == '__main__':
    crawler = Crawler(90)
    prices = crawler.scan_prices()
    crawler.alert()
