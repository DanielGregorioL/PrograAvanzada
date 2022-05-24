"""This module provides regular expression matching operations"""
import re


def date_in_spanish(date):
    """
    Translates a string date to spanish. That is, all references to months
    abbreviations like 'Jan', 'Feb', 'Mar' and so on are changed to 'Ene',
    'Feb', 'Mar', respectively.

    Parameters
    ----------
    date : str
        Date to be translated.

    Returns
    ------
        str
        The translated base_date.

    Examples
    --------
    >>> date_in_spanish("23-Apr-2021")
    23-Abr-2021
    >>> date_in_spanish("Dec-24-2020")
    Dic-24-2020
    """
    change_date = {"Jan": "Ene", "Apr": "Abr", "Aug": "Ago", "Dec": "Dic"}
    for key in change_date.items():
        if re.search(key[0], date) is not None:
            return re.sub(key[0], key[1], date)
    return date


def from_standard_equity_option_convention(code: str) -> dict:
    """
    Transform characters standard equity option convention code to record representation.

    Parameters
    ----------
    code : str
        Standard equity option convention code (see
        https://en.wikipedia.org/w. Programar el método siguiente.


    Returns
    -------
        dict
        A dictionary containing:
        'symbol': Symbol name
        'expire': Option expiration base_date
        'right': Put (P) or Call (C).
        'strike': Option strike

    Examples:
    >>> from_standard_equity_option_convention('YHOO150416C00030000')
    {'symbol': 'YHOO', 'expire': '20150416', 'right': 'C', 'strike': 30.0}
    """
    characters = re.findall("[A-Z]+", code)
    numbers = re.findall(r"\d+", code)
    symbol = characters[0]
    right = characters[1]
    expire = "20"+numbers[0]
    strike = int(numbers[1]) / 1000

    return {"symbol": symbol, "expire": expire, "right": right, "strike": strike}


def collect_commission_adjustment(data):
    """
    Retrieve a commision adjustment record from the section "Commission
    Adjustments" in one Interactive Brokers activity report.

    PARAMETERS
    ----------
    data : list[]
        Line from the activity report in the "Commission Adjustment" section
        in list format. That is, each element in the list is a comma
        separated item from the line.

    RETURNS
    -------
        dict
        Containing the open position information in dictionary format.

    Examples
    --------
    >>> collect_commission_adjustment(['Commission Adjustments', 'Data', 'USD',
    ... '2021-04-23',
    ... 'Commission Computed After Trade Reported (C210430C00069000)',
    ... '-1.0906123', '\\n'])
    {'end_date': '20210423', 'symbol': 'C', 'expire': '20210430', \
    'right': 'C', 'strike': 69.0, 'sectype': 'OPT', 'amount': -1.0906123}
    >>> collect_commission_adjustment(
    ... ['Commission Adjustments', 'Data', 'USD', '2021-02-19',
    ... 'Commission Computed After Trade Reported (ALB)', '-0.4097', '\\n'])
    {'end_date': '20210219', 'symbol': 'ALB', 'sectype': 'STK', \
    'amount': -0.4097}
    """
    reg_exp = "[A-Z]+[0-9]{6}[CP][0-9]{8}"
    opt_stk = re.search(reg_exp, str(data))

    date = re.search("[0-9]{4}-[0-9]{2}-[0-9]{2}", str(data)).group(0)
    end_date = re.sub("-", "", date)
    reg_amount = r"[-][0-9]+\.[0-9]+"
    amount = float(re.search(reg_amount, str(data)).group(0))

    if opt_stk is not None:
        opt_conv_letters = re.findall("[A-Z]+", opt_stk.group(0))
        opt_conv_numbers = re.findall("[0-9]+", opt_stk.group(0))
        symbol = opt_conv_letters[0]
        expire = end_date[0]+end_date[1] + opt_conv_numbers[0]
        right = opt_conv_letters[1]
        strike = int(opt_conv_numbers[1])/1000
        return {"end_date": end_date, "symbol": symbol, "expire": expire, "right": right,
                "strike": strike, "sectype": "OPT", "amount": amount}

    reg_stk = "[(][A-Z]+[)]"
    sym = re.search(reg_stk, str(data)).group(0)
    symbol = re.sub("[()]", "", sym)
    return {"end_date": end_date, "symbol": symbol, "sectype": "STK", "amount": amount}


