import os
import time
import sys
import datetime
import requests
import pandas as pd
from configurations import INTERVAL_OF_SECONDS, DATA_PROVIDER_LINK, DATA_FILE_NAME


def from_webpage_to_data(CONTENT):
    """
    get EUR USD data from the data provider
    """
    n1 = str(CONTENT)[2:].replace("<table>", "").replace("<tr>", "").replace(
        "<td>", "").split("</td></tr>USD/JPY</td>")[0].split("</td>")  # <table><tr><td>
    n2 = n1[:2]+[str(n1[2])+str(n1[3])]+[str(n1[4])+str(n1[5])]+n1[6:]
    return n2


if __name__ == '__main__':

    """
    get EUR USD data and save it into csv file each 60 seconds
    """

    if not os.path.isfile(DATA_FILE_NAME):
        os.system(f"touch {sys.path[0]+'/'+DATA_FILE_NAME}")

    while True:

        try:
            r = requests.get(DATA_PROVIDER_LINK)

            # check status code for response received
            # 200 is the status code for success
            if str(r) == "<Response [200]>":

                df = pd.DataFrame(from_webpage_to_data(r.content)[1:])

                price = {}

                price['open'] = float(df.values[-1])
                price['high'] = float(df.values[-2])
                price['low'] = float(df.values[-3])
                price['close'] = float(df.values[-4])
                price['volume'] = int(df.values[0])

                current_time = datetime.datetime.now()

                row = str(current_time)[
                    :-7]+', ' + str(list(price.values())).replace('[', '').replace(']', '')+'\n'

                os.system('clear')

                print('\n\tData provider: ', DATA_PROVIDER_LINK)
                print('\n\tEURUSD price: ', price['close'])
                print('\n\tDatetime: ', str(current_time)[:-7])

                print('\n\tContent: '+row)

                with open(DATA_FILE_NAME, "+a") as f:
                    f.write(row)
                    f.close()

                # - 1 for process time and async request
                time.sleep(INTERVAL_OF_SECONDS - 1)

        except:
            print('data not recived')
            time.sleep(2)
