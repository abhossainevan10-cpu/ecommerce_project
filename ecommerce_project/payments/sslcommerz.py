import requests
from django.conf import settings

class SSLCommerz:
    endpoint = 'https://sandbox.sslcommerz.com/gwprocess/v4/api.php'

    def initiate(self, amount, tran_id, success_url, fail_url, cancel_url):
        data = {
            'store_id': settings.SSL_STORE_ID,
            'store_passwd': settings.SSL_STORE_PASS,
            'total_amount': amount,
            'currency': 'BDT',
            'tran_id': tran_id,
            'success_url': success_url,
            'fail_url': fail_url,
            'cancel_url': cancel_url,
        }
        resp = requests.post(self.endpoint, data=data)
        return resp.json()
