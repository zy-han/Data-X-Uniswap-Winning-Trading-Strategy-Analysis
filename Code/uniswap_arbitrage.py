import random
import json
from decimal import Decimal

def randSelect(allp, num=200):
    maxNum = len(allp)
    start = random.randint(0, maxNum-num)
    return allp[start:start+num]

def removeBlackList(pairs):
    blacklist = json.load(open('files/blacklist.json'))
    r = []
    for i in range(len(pairs)):
        if pairs[i]['token0']['address'].lower() in blacklist or pairs[i]['token1']['address'].lower() in blacklist:
            r.append(i)
    r.reverse()
    for t in r:
        del pairs[t]
    return pairs

def toDict(pairs):
    p = {}
    i = 0
    for pair in pairs:
        p[pair['address']] = pair
        p[pair['address']]['arrIndex'] = i
        i += 1
    return p

def selectPairs(all_pairs):
    if config['pairs'] == 'random':
        pairs = randSelect(all_pairs, config['pair_num'])
    elif config['pairs'] == 'main_pairs':
        pairs = json.load(open('files/main_pairs.json'))
    pairs = removeBlackList(pairs)
    # pairs = removeLowLiq(pairs)
    pairsDict = toDict(pairs)
    return pairs, pairsDict

d997 = Decimal(997)
d1000 = Decimal(1000)
def getOptimalAmount(Ea, Eb):
    if Ea > Eb:
        return None
    if not isinstance(Ea, Decimal):
        Ea = Decimal(Ea)
    if not isinstance(Eb, Decimal):
        Eb = Decimal(Eb)
    return Decimal(int((Decimal.sqrt(Ea*Eb*d997*d1000)-Ea*d1000)/d997))

def adjustReserve(token, amount):
    # res = Decimal(amount)*Decimal(pow(10, 18-token['decimal']))
    # return Decimal(int(res))
    return amount

def toInt(n):
    return Decimal(int(n))

def getEaEb(tokenIn, pairs):
    Ea = None
    Eb = None
    idx = 0
    tokenOut = tokenIn.copy()
    for pair in pairs:
        if idx == 0:
            if tokenIn['address'] == pair['token0']['address']:
                tokenOut = pair['token1']
            else:
                tokenOut = pair['token0']
        if idx == 1:
            Ra = adjustReserve(pairs[0]['token0'], pairs[0]['reserve0'])
            Rb = adjustReserve(pairs[0]['token1'], pairs[0]['reserve1'])
            if tokenIn['address'] == pairs[0]['token1']['address']:
                temp = Ra
                Ra = Rb
                Rb = temp
            Rb1 = adjustReserve(pair['token0'], pair['reserve0'])
            Rc = adjustReserve(pair['token1'], pair['reserve1'])
            if tokenOut['address'] == pair['token1']['address']:
                temp = Rb1
                Rb1 = Rc
                Rc = temp
                tokenOut = pair['token0']
            else:
                tokenOut = pair['token1']
            Ea = toInt(d1000*Ra*Rb1/(d1000*Rb1+d997*Rb))
            Eb = toInt(d997*Rb*Rc/(d1000*Rb1+d997*Rb))
        if idx > 1:
            Ra = Ea
            Rb = Eb
            Rb1 = adjustReserve(pair['token0'], pair['reserve0'])
            Rc = adjustReserve(pair['token1'], pair['reserve1'])
            if tokenOut['address'] == pair['token1']['address']:
                temp = Rb1
                Rb1 = Rc
                Rc = temp
                tokenOut = pair['token0']
            else:
                tokenOut = pair['token1']
            Ea = toInt(d1000*Ra*Rb1/(d1000*Rb1+d997*Rb))
            Eb = toInt(d997*Rb*Rc/(d1000*Rb1+d997*Rb))
        idx += 1
    return Ea, Eb

def getAmountOut(amountIn, reserveIn, reserveOut):
    assert amountIn > 0
    assert reserveIn > 0 and reserveOut > 0
    if not isinstance(amountIn, Decimal):
        amountIn = Decimal(amountIn)
    if not isinstance(reserveIn, Decimal):
        reserveIn = Decimal(reserveIn)
    if not isinstance(reserveOut, Decimal):
        reserveOut = Decimal(reserveOut)
    return d997*amountIn*reserveOut/(d1000*reserveIn+d997*amountIn)

def sortTrades(trades, newTrade):
    trades.append(newTrade)
    return sorted(trades, key = lambda x: x['profit'])

def findArb(pairs, tokenIn, tokenOut, maxHops, currentPairs, path, bestTrades, count=5):
    # The core method to find arbitrage routes by DFS (depth first search)
    for i in range(len(pairs)):
        newPath = path.copy()
        pair = pairs[i]
        if not pair['token0']['address'] == tokenIn['address'] and not pair['token1']['address'] == tokenIn['address']:
            continue
        if pair['reserve0']/pow(10, pair['token0']['decimal']) < 1 or pair['reserve1']/pow(10, pair['token1']['decimal']) < 1:
            continue
        if tokenIn['address'] == pair['token0']['address']:
            tempOut = pair['token1']
        else:
            tempOut = pair['token0']
        newPath.append(tempOut)
        if tempOut['address'] == tokenOut['address'] and len(path) > 2:
            Ea, Eb = getEaEb(tokenOut, currentPairs + [pair])
            newTrade = { 'route': currentPairs + [pair], 'path': newPath, 'Ea': Ea, 'Eb': Eb }
            if Ea and Eb and Ea < Eb:
                newTrade['optimalAmount'] = getOptimalAmount(Ea, Eb)
                if newTrade['optimalAmount'] > 0:
                    newTrade['outputAmount'] = getAmountOut(newTrade['optimalAmount'], Ea, Eb)
                    newTrade['profit'] = newTrade['outputAmount']-newTrade['optimalAmount']
                    newTrade['p'] = int(newTrade['profit'])/pow(10, tokenOut['decimal'])
                else:
                    continue
                bestTrades = sortTrades(bestTrades, newTrade)
                bestTrades.reverse()
                bestTrades = bestTrades[:count]
        elif maxHops > 1 and len(pairs) > 1:
            pairsExcludingThisPair = pairs[:i] + pairs[i+1:]
            bestTrades = findArb(pairsExcludingThisPair, tempOut, tokenOut, maxHops-1, currentPairs + [pair], newPath, bestTrades, count)
    return bestTrades

if __name__ == "__main__":
    # Sample output for finding arbitrage opportunity of USDT
    usdt = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
    tokenIn = {
        'address': usdt,
        'symbol': 'USDT',
        'decimal': 6,
    }
    tokenOut = {
        'address': usdt,
        'symbol': 'USDT',
        'decimal': 6,
    }
    currentPairs = []
    path = [tokenIn]
    Ea = None
    Eb = None
    bestTrade = []
    pairs = json.load(open('files/pairs.json'))[:200]

    #The max transaction depth is predefined
    maxHops = 4
    trade = findArb(pairs, tokenIn, tokenOut, maxHops, currentPairs, path, bestTrade)
    print(trade)