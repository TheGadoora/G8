class Transaction:
    fees = {
        "Bahrain": 0.0275,
        "UAE": 0.0250,
        "Qatar": 0.0375,
        "Oman": 0.0300,
        "Kuwait": 0.0175,
        "KSA": 0.0200
    }

    @staticmethod
    def apply_fee(country, trade_value):
        """
        Apply the transaction fee according to the country of the stock

        :param country: the country where the stock is from
        :param trade_value: the value of the trade
        :return: the trade value after the fee is deducted
        """
        fee_rate = Transaction.fees[country]
        return trade_value - trade_value * fee_rate
