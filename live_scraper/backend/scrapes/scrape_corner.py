import requests
import httpx


class C_t3:
    @staticmethod
    def scraper_t3():  # self
        products_list = []
        ids_list_whole = [1170046, 1191407, 1265903, 1191384]  # 1265903, 1191384, 1203972, 1170046, 1454790, 2065015]
        ids_list = [1988649]
        # req_prod_id = requests.get('https://cornershopapp.com/api/v2/branches/6558/products/1170046')
        for x in ids_list_whole:
            r = requests.get(f'https://cornershopapp.com/api/v2/branches/6558/products/{x}').json()
            try:
                id = r[0]['id']
            except (TypeError, IndexError):
                id = None

            try:
                availability_status = r[0]['availability_status']
            except (TypeError, IndexError):
                availability_status = None

            try:
                price = r[0]['original_price'].replace('NaN', '')
            except (AttributeError, TypeError, IndexError):
                price = None

            try:
                brand = r[0]['brand']['name']
            except (TypeError, IndexError):
                brand = None
            # print(r)
            if isinstance(id, (int, float)):
                prod_dict = {
                    'id': id,
                    'availability_status': availability_status,
                    'price': price,
                    'brand': brand,
                }

                products_list.append(prod_dict)

        return products_list


data_t3 = C_t3()
data_t3.scraper_t3()

# data1 = data_t3.scraper_t3()

# data1 = dict('{' + 'request' + ':'f'{data_t3.scraper_t3()}' + '}')
# print(data1)

# dictss = {'request': [{'id': 1191407, 'availability_status': 'AVAILABLE', 'price': None, 'brand': 'Intimus'}, {'id': 1265903, 'availability_status': 'AVAILABLE', 'price': None, 'brand': 'Intimus'}]}
#
# for x in dictss['request']:
#     print(x)

# dicts = {'abc': 123, 'axl': 'pi'}
#
# print(dicts['axl'])

# <!--<p style='margin-bottom:2px;'>campo: <b>{{ items }} {{ items }}</b></p>-->
