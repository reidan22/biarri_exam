def checkCrossover(row):
    if row["SMAL"] > row["SMAH"]:
        return "Higher"
    else:
        return "Lower"

def timeFormatter(mins):
    time_hr = mins//60
    time_min = mins%60
    
    time_output = str(time_hr).zfill(2) + ':' + str(time_min).zfill(2) + ':00'
    return time_output

def reportMessage(report, _time, added_msg=""):
    buy_time = timeFormatter(report["buy"]["time"])
    buy_price = round(report["buy"]["price"],4)
    sell_time = timeFormatter(report["sell"]["time"])
    sell_price = round(report["sell"]["price"],4)
    diff_price = round(sell_price-buy_price,4)
    print(f'[{buy_time}] Open({buy_price:.4f}) | [{sell_time}] Close({sell_price:.4f}) | Profit ({diff_price:.4f}) <{_time}mins> | {added_msg}')