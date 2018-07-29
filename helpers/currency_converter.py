from helpers.api_helper import ApiHelper


class CurrencyConverter(object):
    def convert_currency_by_api_rates(self, ammount, from_currency, to_currency):
        rates = ApiHelper().get_exchange_rate_from_api(from_currency, to_currency)
        buy_rates = float(rates['buyValue'])
        sell_rates = float(rates['sellValue'])
        scale = int(rates['scale'])

        if from_currency == "RUB":
            return round(float(ammount) * scale / sell_rates, 2)
        else:
            return round(float(ammount) * scale * buy_rates, 2)
