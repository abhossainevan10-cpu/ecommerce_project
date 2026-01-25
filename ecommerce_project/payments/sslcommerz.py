import requests
from django.conf import settings

class SSLCommerz:
    """
    SSLCommerz পেমেন্ট গেটওয়ের সাথে যোগাযোগ করার ক্লাস।
    এটি স্যান্ডবক্স (টেস্টিং) মোডে সেট করা আছে।
    """
    # টেস্টিং এর জন্য স্যান্ডবক্স এন্ডপয়েন্ট
    endpoint = 'https://sandbox.sslcommerz.com/gwprocess/v4/api.php'

    def initiate(self, **kwargs):
        """
        পেমেন্ট শুরু করার জন্য এই মেথডটি ব্যবহার করা হয়।
        """
        # ডিফল্ট ডাটা যা প্রত্যেকটি পেমেন্টের জন্য প্রয়োজন
        data = {
            'store_id': settings.SSL_STORE_ID,
            'store_passwd': settings.SSL_STORE_PASS,
            'currency': 'BDT',
            'shipping_method': 'NO',
            'product_category': 'Electronics',
            'product_name': 'Mobile Phone',
            'product_profile': 'general',
            'cus_country': 'Bangladesh',
            'total_amount': kwargs.get('total_amount'),
        }
        
        # views.py থেকে আসা dynamic ডাটা (amount, tran_id, success_url ইত্যাদি) এখানে যুক্ত হবে
        data.update(kwargs)
        
        try:
            # SSLCommerz সার্ভারে ডাটা পাঠানো
            resp = requests.post(self.endpoint, data=data)
            
            # সার্ভার থেকে আসা রেসপন্স চেক করা
            resp.raise_for_status() 
            
            # JSON ফরম্যাটে ডাটা রিটার্ন করা
            return resp.json()
            
        except requests.exceptions.HTTPError as http_err:
            return {'status': 'FAILED', 'failedreason': f'HTTP error occurred: {http_err}'}
        except Exception as err:
            return {'status': 'FAILED', 'failedreason': f'Other error occurred: {err}'}
        
        
