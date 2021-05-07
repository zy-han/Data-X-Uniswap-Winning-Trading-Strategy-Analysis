# Data-X Applied Data Science with Venture Applications

# Uniswap Arbitraging Platform: Winning Trading Strategies for Cryptocurrencies

Team 1 - INDENG 290 - 21 Spring at Cal

## Motivation
Cryptocurrency is one of the hottest fields in investment, promising immense opportunity for those willing to take risks. While the price of Bitcoin skyrocketed from $5,000 to $60,000 and the daily trading volume reached a billion-dollar level in the past year, people’s interest in trading and swapping crypto assets has grown exponentially. However, the process is not as easy as it sounds - investors are likely to lose money due to a lack of knowledge of the market and the fast-changing exchange rates. Under the guidance of AnChain.ai, six students from the University of California, Berkeley gathered to create a platform that could recommend arbitraging strategies based on users’ preferences and boost people’s portfolios, making it less risky for cryptocurrency investors.

## File Introduction
The project consists of three parts - Datasets, API, and Models.

### Datasets 
Our data came from two sources. We fetched USDC Token's daily transaction data of the recent year using the GraphQL language on [TheGraph Uniswap-V2](https://thegraph.com/explorer/subgraph/uniswap/uniswap-v2). The other part was downloaded from [Yahoo Finance](https://finance.yahoo.com/quote/USDC-USD/). The file [USDC-USD.csv](https://github.com/zy-han/Data-X-Uniswap-Winning-Trading-Strategy-Analysis/blob/main/Datasets/USDC-USD.csv) (Oct 18 to April 21) was solely from Yahoo and was used for anomaly detection and outlier identification, whereas the file [USDC Price.csv](https://github.com/zy-han/Data-X-Uniswap-Winning-Trading-Strategy-Analysis/blob/main/Datasets/USDC%20Price.csv) was two-source concatenated (Uniswap (May 20 to April 21) and [USDC 3year.csv](https://github.com/zy-han/Data-X-Uniswap-Winning-Trading-Strategy-Analysis/blob/main/Datasets/USDC%203year.csv) (Oct 18 to May 20) from Yahoo) and was used for time series predictive models. [sample_uniswap_record.csv](https://github.com/zy-han/Data-X-Uniswap-Winning-Trading-Strategy-Analysis/blob/main/Datasets/sample_uniswap_record.csv) was pulled by our API, which would be introduced later, from the Uniswap platform. In addition, in the folder exist jupyter notebooks of our data pre-processing and EDA codes.

### API
We programmed an [API](https://github.com/zy-han/Data-X-Uniswap-Winning-Trading-Strategy-Analysis/blob/main/API/Request_Uniswap_try.py) that could automatically request and download within-a-day transaction data between a pair of tokens on Uniswap, given the token ID and Unix timestamp. It would output transaction IDs, volumes, and equivalent USD price. It was referenced when we located the specific dates with abnormal prices and performed intra-day outlier detections.

### Models
The Models folder includes all four time series predictive models (ARIMA, SARIMA, Prophet, and LSTM) that we used to predict future USDC token price using the past 3 years' data. The files for the [Depth-First-Search (DFS) algorithm](https://github.com/zy-han/Data-X-Uniswap-Winning-Trading-Strategy-Analysis/blob/main/Models/uniswap_arbitrage.py) could also be found here.

## Reproduction Guide
Here is a step-by-step introduction on how to reproduce our work:

1. Download all files in the three folders to your local environment.
2. Open [Raw Data Preparation.ipynb](https://github.com/zy-han/Data-X-Uniswap-Winning-Trading-Strategy-Analysis/blob/main/Datasets/Raw%20Data%20Preparation.ipynb) and use the GraphQL query in the first box to fetch the USDC Token's daily transaction data of the recent year, as shown in the second box. Load the Yahoo Finance data [USDC 3years.csv](https://github.com/zy-han/Data-X-Uniswap-Winning-Trading-Strategy-Analysis/blob/main/Datasets/USDC%203year.csv) and contatenate two datasets into [USDC Price.csv](https://github.com/zy-han/Data-X-Uniswap-Winning-Trading-Strategy-Analysis/blob/main/Datasets/USDC%20Price.csv).
3. Run [Exploratory Data Analysis.ipynb](https://github.com/zy-han/Data-X-Uniswap-Winning-Trading-Strategy-Analysis/blob/main/Datasets/Exploratory%20Data%20Analysis.ipynb) to perform EDA and identify real-life arbitraging transactions on your dates of prederence that are classified as outlier dates. After that, feel free to go to [Etherscan](https://etherscan.io) to see transaction details using the transaction IDs given in the end. For intra-day analysis, please use the [API](https://github.com/zy-han/Data-X-Uniswap-Winning-Trading-Strategy-Analysis/blob/main/API/Request_Uniswap_try.py) we prepared to get transactions within a specific day.
4. With the [DFS algorithm](https://github.com/zy-han/Data-X-Uniswap-Winning-Trading-Strategy-Analysis/blob/main/Models/uniswap_arbitrage.py) and the supportive [document](https://github.com/zy-han/Data-X-Uniswap-Winning-Trading-Strategy-Analysis/blob/main/Models/pairs.json) that records exchange rates between pairs, one can imput a token name to get arbitraging recommendations with arbitrage routes and optimal volumes. There is also a choice to limit the number of tokens involved and therefore limit the length of routes suggested.
5. Run the USDC ARIMA/SARIMA/Prophet/LSTM files in the Models folder to compare the performances of the models' ability to predict future token price through error measures and graphs.

## API Reference
The data collection stage of our project involves the usage of Uniswap API. Details could be found [here](https://uniswap.org/docs/v2/API/overview/).

## Credits
We would like to thank [Dr. Victor Fang](https://www.linkedin.com/in/drvictorfang/) from AnChain.AI for his guidance and support.

## Contacts
* Kexin Fang    |  kexin_fang@berkeley.edu
* Lei Liang     |  lei_liang@berkeley.edu
* Shuyang Yu    |  shuyang_yu@berkeley.edu
* Yuying Chen   |  yuyingc18@berkeleu.edu
* Zhiyang Han   |  z-han@berkeley.edu
* Zihao Zhou    |  zhouzh20@berkeley.edu


## Liscense
© Apache 2.0
