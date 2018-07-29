from utils.api_utils import SberbankAppiUtils

from variables import variables


class ApiHelper(SberbankAppiUtils):
    def get_current_buy_and_sell_values_from_api(self, from_currency, to_currency):
        data = self.get_exchange_rate_from_api(from_currency, to_currency)
        return [data['buyValue'], data['sellValue']]

    def get_exchange_rate_from_api(self, from_currency, to_currency):
        api = SberbankAppiUtils()
        currency_code = ""
        if from_currency != "RUB":
            currency_code = from_currency
        else:
            currency_code = to_currency
        data_from_api = api.get_current_currency_data_from_api(currency_code=variables.currency_code[currency_code])
        return data_from_api
