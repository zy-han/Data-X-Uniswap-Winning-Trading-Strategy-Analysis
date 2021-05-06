import requests
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def auto_query_uniswap(token_id_0, token_id_1, time_left, time_right, skip=5, first=100):
    pair_prefix = """{
        pairs(where: {token0: """
    pair_midfix = """, token1: """
    pair_tailfix =  """}) {
        id
        token0 {
        id
        name
        symbol
        totalSupply
        totalLiquidity
        }
        token1 {
        id
        name
        symbol
        totalSupply
        totalLiquidity
        }
        token0Price
        volumeToken0
        token1Price
        volumeToken1
        volumeUSD
        txCount
        }
        }"""
    pair_query = pair_prefix + "\"" +token_id_0 + "\"" + pair_midfix + "\"" + token_id_1 + "\"" + pair_tailfix
    url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'
    r = requests.post(url, json={'query':pair_query})
    if r:
        print('Success_pair')
    else:
        print('Fail_pair.')
    raw_data = r.json()
    pair_id = raw_data['data']['pairs'][0]['id']
    volume_token_0 = raw_data['data']['pairs'][0]['volumeToken0']
    volume_token_1 = raw_data['data']['pairs'][0]['volumeToken1']
    volume_USD = raw_data['data']['pairs'][0]['volumeUSD']
    volume_all = {'volume_token_0': volume_token_0, 'volume_token_1': volume_token_1, 'volume_USD': volume_USD}

    #find the actual transaction records
    tran_prefix = "{ swaps (where: {pair: "
    tran_midfix_0 = ", timestamp_gte: "
    tran_midfix_1 = ", timestamp_lt: "
    tran_skip = "}, skip: "
    tran_first = ", first: "
    tran_tail = """) {
    id
    timestamp
    pair {
    token0 {
    symbol
    }
    token1 {
    symbol
    }
    }
    sender
    to
    amount0In
    amount0Out
    amount1In
    amount1Out
    amountUSD
    }
    }"""
    tran_query = tran_prefix + "\"" +  pair_id + "\"" + tran_midfix_0 + str(time_left) + tran_midfix_1 + str(time_right) \
                 + tran_skip + str(skip) + tran_first + str(first) + tran_tail
    tran_r = requests.post(url, json={'query': tran_query})
    if tran_r:
        print('Success_transaction')
    else:
        print('Fail_transaction')
    return volume_all, tran_r.json()



if __name__ == "__main__":
    # sample code to request transaction records from uniswap
    token_id_0 = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"  #USDC
    token_id_1 = "0xdac17f958d2ee523a2206206994597c13d831ec7"  #USDT
    time_left = 1613523600 #2021.2.17 - 1am
    time_right = 1614387600 #2021.2.27 - 1am
    skip = 1
    first = 200
    volume, raw_data = auto_query_uniswap(token_id_0, token_id_1, time_left, time_right, skip, first)
    if len(raw_data['data']['swaps']) >= 1:
        df_data = pd.DataFrame(raw_data['data']['swaps'])
        df_data.to_csv('sample_uniswap_record.csv', index = False)
    else:
        print('No record')
