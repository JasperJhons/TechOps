from urllib import parse

import requests

from variables.variables import *


class SberbankAppiUtils(object):
    _common_url = "http://www.sberbank.ru/portalserver/proxy"
    _internal_api_url = "http://localhost/rates-web/rateService/rate/current"

    def get_current_currency_data_from_api(self, currency_code, region=region_code['Moscow'],
                                           rate_category=rate_category['beznal']):
        internal_url_with_params = self.__prepare_internal_url(region, rate_category, currency_code)
        query_params = {'pipe': 'shortCachePipe', 'url': internal_url_with_params}
        response = requests.get(self._common_url, query_params)
        return response.json()[rate_category][currency_code]['0']

    def __prepare_internal_url(self, region, rate_category, currency_code):
        query_params = parse.urlencode({'regionId': region,
                                        'rateCategory': rate_category,
                                        'currencyCode': currency_code})
        return self._internal_api_url + '?' + query_params
