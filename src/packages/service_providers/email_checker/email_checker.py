import asyncio
from src.packages.http_requests.req_http_aio import http_post

class EmailChecker:

    async def call_product(self, product: dict):
        resp_data, resp_status = await http_post(product["email_verification_url"])
        product['is_found'] = True if resp_status == 200 else False
        return product

    async def call_products(self, products:list):
        response_products_data = await asyncio.gather(*[self.call_product(product) for product in products['__root__'] if product["name"] != 'ez-login'])
        return response_products_data
