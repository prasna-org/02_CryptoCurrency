## Nanopool API Req
#Rate limited to 30calls/minute
import urllib
import json
import pandas as pd

try:
	from urllib.request import urlopen
	from urllib.parse import urlencode
except ImportError:
	print ('Version error. This Lib can be used from python 3 or greater..')

## Service URL and currency symbols
pool_url = "https://api.nanopool.org/v1/"
Ethereum_sym = "eth"
Zcash_sym = "zec"
Monero_sym = "xmr"

#Currency of interest
curr = "eth"

if curr == Ethereum_sym: baseurl = pool_url+Ethereum_sym+"/"
if curr == Zcash_sym: baseurl = pool_url+Zcash_sym+"/"
if curr == Monero_sym: baseurl = pool_url+Monero_sym+"/"

def readjsondata(add_url):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        response = opener.open(add_url)
        UrlData = response.read()
        idData = json.loads(UrlData)
        return idData

def Miner(account):
    id_url = baseurl + "user/" + account
    Miner_data = readjsondata(id_url)

    MinerAccount = Miner_data['data']['account']
    if Miner_data['status'] == True: MinerStatus = 'Online'
    else: MinerStatus = 'Offline'
    MinerBalance = Miner_data['data']['balance']
    MinerNumWorkers = len(Miner_data['data']['workers'])
    MinerHashrate = Miner_data['data']['hashrate']
    MinerWorkers = Miner_data['data']['workers']

    print('Miner address: ', Miner_data['data']['account'])
    print('Miner status: ', MinerStatus)
    print('Account Balance: ', MinerBalance)
    print('Hashrate: ', MinerHashrate)
    print('Number of workers: ', MinerNumWorkers)
    for w in MinerWorkers:
        print('\tWorker ID: ', w['id'], '\tHashrate: ', w['hashrate'])
    return Miner_data

def Payments(account):
    id_url = baseurl + "payments/" + account
    Payment_data = readjsondata(id_url)

    Payments = Payment_data['data']

    print('Payment Date', '\tTransaction Hash', '\tAmount', '\tConfirmation')
    print('------------', '\t----------------', '\t------', '\t------------')
    if len(Payments) > 0 and Payment_data['status'] == True:
        for pay in Payments:
            print(Payment_data['data']['date'], '\t', Payment_data['data']['txHash'], '\t', Payment_data['data']['amount'], '\t', Payment_data['data']['confirmed'])

    return Payment_data

def Earnings(hashrate):
    id_url = baseurl + "approximated_earnings/" + hashrate
    Earnings_data = readjsondata(id_url)

    cols = ["Currency", "Minute", "Hour", "Day", "Week", "Month"]
    Earning_df = pd.DataFrame(columns=cols)
    Earning_df['Currency'] = [curr, "Dollars", "Bitcoin"]
    Earning_df['Minute'] = [Earnings_data['data']['minute']['coins'], Earnings_data['data']['minute']['dollars'], Earnings_data['data']['minute']['bitcoins']]
    Earning_df['Hour'] = [Earnings_data['data']['hour']['coins'], Earnings_data['data']['hour']['dollars'], Earnings_data['data']['hour']['bitcoins']]
    Earning_df['Day'] = [Earnings_data['data']['day']['coins'], Earnings_data['data']['day']['dollars'], Earnings_data['data']['day']['bitcoins']]
    Earning_df['Week'] = [Earnings_data['data']['week']['coins'], Earnings_data['data']['week']['dollars'], Earnings_data['data']['week']['bitcoins']]
    Earning_df['Month'] = [Earnings_data['data']['month']['coins'], Earnings_data['data']['month']['dollars'], Earnings_data['data']['month']['bitcoins']]

    print(Earning_df)

    return Earnings_data

def Prices():
    id_url = baseurl + "prices/"
    Price_data = readjsondata(id_url)

    print(curr, " pricing:","\nUSD: ", Price_data['data']['price_usd'], "\tBitcoin: ", Price_data['data']['price_btc'])

    return Price_data

def Network():
    print("nanopool network stats for ", curr, " block chain:")
    id_url = baseurl + "network/avgblocktime/"
    BlockTime_data = readjsondata(id_url)
    print('Average block time(',curr, '.nanopool.org): ', BlockTime_data['data'])

    id_url_1 = baseurl + "network/timetonextepoch/"
    TTNE_data = readjsondata(id_url_1)
    print('Time to next Epoch: ', TTNE_data['data'])

    return (BlockTime_data['data'], TTNE_data['data'])

def Pool():
    print("nanopool pool stats for ", curr, " block chain:")
    id_url = baseurl + "pool/activeminers/"
    Pool_numMiners_data = readjsondata(id_url)
    print('Number of Miners: ', Pool_numMiners_data['data'])
    id_url = baseurl + "pool/activeworkers/"
    Pool_numWorkers_data = readjsondata(id_url)
    print('Number of Workers: ', Pool_numWorkers_data['data'])
    id_url = baseurl + "pool/hashrate/"
    Pool_hashrate_data = readjsondata(id_url)
    print('Pool Hashrate: ', Pool_hashrate_data['data'])

    return (Pool_numMiners_data['data'], Pool_numWorkers_data['data'], Pool_hashrate_data['data'])

def Worker():

    return #xyz
