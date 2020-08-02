<img src="quant.jpg">


# Quantitative Finance Project

Keyvan Tajbakhsh  
July 26th, 2020

This reasearch project is realized in Python language and edited in <i>Jupyter Notebook</i> environement. Before diving into it, please read carefully all requirements and instructions mentioned below. 

For decades financial institutions and alpha generation platforms focus solely on quantitative investment research rather than the rapid trading of investments. While some of these platforms do allow analysts to take their strategies to market, 
others focus solely on the research and development of these highly complex mathematical and statistical models. quantitative investing uses raw data to calculate potential stock values, earnings forecasts and other metrics that help investors make capital allocation decisions.<br>
The purpose of this project is to define a liquid universe of stocks where we would apply the alpha factors to see through our factor analysis if there is a potential or not to send these results to production. 
After selecting and combining factors using Machine Learning technics, the combined factor is analyzed and improved with an optimizer function and then integrated into the risk model.  


This project workflow is comprised of distinct stages including: 

1. Parameters
2. Universe definition
3. Sector definition
4. Alpha factors
5. Factor analysis
6. Factors combination
7. Risk analysis for equal weights
8. Integrating factor data to the optimizer
9. Optimized alpha vector analysis 
10. Predicted portfolio

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

#### Pypi Packages

* [NumPy](https://www.numpy.org/) - A fundamental package for scientific computing with Python.(<i>version == 1.19.1</i>)
* [Pandas](https://pandas.pydata.org/) - A library providing high-performance, easy-to-use data structures and data analysis tools.(<i>version == 0.22.0</i>)
* [ScikitLearn](https://scikit-learn.org/) - Simple and efficient tools for data mining and data analysis.(<i>version == 0.0</i>)
* [Matplotlib](https://matplotlib.org/) - Matplotlib is a Python 2D plotting library which produces publication quality figures in a variety of hardcopy formats and interactive environments across platforms.(<i>version == 3.3.0</i>)
* [Sea Born](https://seaborn.pydata.org/) - Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics.(<i>version == 0.10.1</i>)
* [Quandl](https://www.quandl.com/) - Quandl delivers market data from hundreds of sources via API, or directly into Python, R, Excel and many other tools.
* [Datetime](https://docs.python.org/3/library/datetime.html) - The datetime module supplies classes for manipulating dates and times.
* [Pytz](https://pypi.org/project/pytz/) - World timezone definitions, modern and historical.
* [Talib](https://mrjbq7.github.io/ta-lib/) - Talib is used by trading software developers requiring to perform technical analysis of financial market data.(<i>version == 0.4.17</i>)
* [Alphalens](https://quantopian.github.io/alphalens/index.html) - Alphalens is a library for performance analysis of predictive (alpha) stock factor.(<i>version == 0.3.6</i>)
* [Pyfolio](https://quantopian.github.io/pyfolio/) - Pyfolio is a library for performance and risk analysis of financial portfolios developed by Quantopian Inc.(<i>version == latest github</i>)  
* [Itertools](https://docs.python.org/3/library/itertools.html) - This module implements a number of iterator building blocks inspired by constructs from APL, Haskell, and SML. Each has been recast in a form suitable for Python.
* [Warnings](https://docs.python.org/3/library/warnings.html) - Warning messages are typically issued in situations where it is useful to alert the user of some condition in a program.
* [Os](https://docs.python.org/3/library/os.html) - This module provides a portable way of using operating system dependent functionality.
* [Zipfile](https://docs.python.org/3/library/zipfile.html) - The ZIP file format is a common archive and compression standard. This module provides tools to create, read, write, append, and list a ZIP file.
* [Time](https://docs.python.org/3/library/time.html) - This module provides various time-related functions. 
* [Yfinance](https://pypi.org/project/yfinance/) - Yahoo! Finance market data downloader (<i>version == 0.1.54</i>)
* [cvxpy](https://www.cvxpy.org/) - CVXPY is a Python-embedded modeling language for convex optimization problems. It allows you to express your problem in a natural way that follows the math, rather than in the restrictive standard form required by solvers.(<i>version == 1.0.11</i>)
* [ibapi](https://interactivebrokers.github.io/tws-api/index.html) - The TWS API is a simple yet powerful interface through which IB clients can automate their trading strategies, request market data and monitor your account balance and portfolio in real time.(<i>version == 9.76.1</i>)

#### Local Modules

* [risk_model](https://github.com/keyvantaj/Quantitative/blob/master/risk_model.py) - This module provides functions used in risk modeling and risk management.
* [factorize](https://github.com/keyvantaj/Quantitative/blob/master/factorize.py) - This module regroups some of useful functions for factorization of raw data.
* [account](https://github.com/keyvantaj/Quantitative/blob/master/account.py) - A package composed of functions with implemented IBKR api for portfolio management.
* [utils_s](https://github.com/keyvantaj/Quantitative/blob/master/utils_s.py) - This modlul delivers functions used in preprocessing and cleaning data.
* [feature_weights](https://github.com/keyvantaj/Quantitative/blob/master/feature_weights.py) - This Machine Learning module is implemented to calculate optimal weights distribution of factors for alpah factor combination

### Code

The project is divided into two parts. The code is provided in the `alpha_research.ipynb` and `portfoilo_management.ipynb` notebook file.
You will be required to have a <b>Quandl API access key</b> to download data and an <b>Interactive Brokers Account</b> for trading, to execute the code. 

### Run

In a terminal or command window, navigate to the top-level project directory `Quantitative/` (that contains this README) and run one of the following commands:

```bash
jupyter notebook alpha_research.ipynb
```

This will open the Jupyter Notebook software and project file in your browser.


### Data

For this porject multiple source of data has been used from 
[Sharadar](https://www.quandl.com/publishers/sharadar) and 
[IFT](https://www.quandl.com/publishers/ift) as described below:

- Sharadar Equity Prices ([SHARADAR/SEP](https://www.quandl.com/databases/SEP/data))
Updated daily,End-Of-Day (EOD) price (ohlcv) data for more than 14,000 US public companies.  
- Indicator Descriptions ([SHARADAR/INDICATORS](https://www.quandl.com/databases/SF1/data))
Description of indicators listed in SF1 table for more than 14,000 US public companies.
- Tickers and Metadata ([SHARADAR/TICKERS](https://www.quandl.com/databases/SF1/data))
Information and metadata for more than 14,000 US public companies.
- Core US Fundamentals ([SHARADAR/SF1](https://www.quandl.com/databases/SF1/data))
 150 essential fundamental indicators and financial ratios, for more than 14,000 US public companies.
- Daily Metrics ([SHARADAR/DAILY](https://www.quandl.com/databases/SF1/data))
 5 essential metrics indicators and financial ratios daily updated, for more than 14,000 US public companies.
- Sentiment Analysis and News Analytics ([IFT/NSA](https://www.quandl.com/databases/NS1/data)) 
News, blogs, social media and proprietary sources for thousands of stocks.

#### Features

##### Tickers and Metadata [SHARADAR/TICKERS] features

- <b>table</b> : Sharadar Table : The database table which the ticker is featured in. Examples are: "SF1" or "SEP. 
- <b>permaticker</b> : Permanent Ticker Symbol : The permaticker is a unique and unchanging identifier for an issuer in the dataset which is issued by Sharadar. 
- <b>name</b> : Issuer Name : The name of the security issuer. 
- <b>exchange</b> : Stock Exchange : The exchange on which the security trades. Examples are: "NASDAQ";"NYSE";"NYSEARCA";"BATS";"OTC" and "NYSEMKT" (previously the American Stock exchange). 
- <b>isdelisted</b> : Is Delisted? : Is the security delisted? [Y]es or [N]o. 
- <b>category</b> : Issuer Category : The category of the issuer: "Domestic"; "Canadian" or "ADR". 
- <b>cusips</b> : CUSIPs : A security identifier. Space delimited in the event of multiple identifiers. 
- <b>siccode</b> : Standard Industrial Classification (SIC) Code : The Standard Industrial Classification (SIC) is a system for classifying industries by a four-digit code; as sourced from SEC filings. More on the SIC system here: https://en.wikipedia.org/wiki/Standard_Industrial_Classification  
- <b>sicsector</b> : SIC Sector : The SIC sector is based on the SIC code and the division tabled here: https://en.wikipedia.org/wiki/Standard_Industrial_Classification  
- <b>sicindustry</b> : SIC Industry : The SIC industry is based on the SIC code and the industry tabled here: https://www.sec.gov/info/edgar/siccodes.htm 
- <b>famasector</b> : Fama Sector : Not currently active - coming in a future update. 
- <b>famaindustry</b> : Fama Industry : Industry classifications based on the SIC code and classifications by Fama and French here: http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_48_ind_port.html 
- <b>sector</b> : Sector : Sharadar's sector classification based on SIC codes in a format which approximates to GICS. 
- <b>industry</b> : Industry : Sharadar's industry classification based on SIC codes in a format which approximates to GICS. 
- <b>scalemarketcap</b> : Company Scale - Market Cap : This field is experimental and subject to change. It categorises the company according to it's maximum observed market cap as follows: 1 - Nano < 50m; 2 - Micro < 300m; 3 - Small < 2bn; 4 - Mid < 10bn; 5 - Large < 200bn; 6 - Mega >= 200bn 
- <b>scalerevenue</b> : Company Scale - Revenue : This field is experimental and subject to change. It categorises the company according to it's maximum observed annual revenue as follows: 1 - Nano < 50m; 2 - Micro < 300m; 3 - Small < 2bn; 4 - Mid < 10bn; 5 - Large < 200bn; 6 - Mega >= 200bn 
- <b>relatedtickers</b> : Related Tickers : Where related tickers have been identified this field is populated. Related tickers can include the prior ticker before a ticker change; and it tickers for alternative share classes. 
- <b>currency</b> : Currency : The company functional reporting currency for the SF1 Fundamentals table or the currency for EOD prices in SEP and SFP. 
- <b>location</b> : Location : The company location as registered with the Securities and Exchange Commission. 
- <b>lastupdated</b> : Last Updated Date : Last Updated represents the last date that this database entry was updated; which is useful to users when updating their local records. 
- <b>firstadded</b> : First Added Date : The date that the ticker was first added to coverage in the dataset. 
- <b>firstpricedate</b> : First Price Date : The date of the first price observation for a given ticker. Can be used as a proxy for IPO date. Minimum value of 1986-01-01 for IPO's that occurred prior to this date. Note: this does not necessarily represent the first price date available in our datasets since our end of day price history currently starts in December 1998. 
- <b>lastpricedate</b> : Last Price Date : The most recent price observation available. 
- <b>firstquarter</b> : First Quarter : The first financial quarter available in the dataset. 
- <b>lastquarter</b> : Last Quarter : The last financial quarter available in the dataset. 
- <b>secfilings</b> : SEC Filings URL : The URL pointing to the SEC filings which also contains the Central Index Key (CIK). 
- <b>companysite</b> : Company Website URL : The URL pointing to the company website. 

##### Core US Fundamentals [SHARADAR/SF1] features

- <b>accoci</b> : Accumulated Other Comprehensive Income : [Balance Sheet] A component of [Equity] representing the accumulated change in equity from transactions and other events and circumstances from non-owner sources; net of tax effect; at period end. Includes foreign currency translation items; certain pension adjustments; unrealized gains and losses on certain investments in debt and equity securities. 
- <b>assets</b> : Total Assets : [Balance Sheet] Sum of the carrying amounts as of the balance sheet date of all assets that are recognized. Major components are [CashnEq]; [Investments];[Intangibles]; [PPNENet];[TaxAssets] and [Receivables]. 
- <b>assetsc</b> : Current Assets : [Balance Sheet] The current portion of [Assets]; reported if a company operates a classified balance sheet that segments current and non-current assets. 
- <b>assetsnc</b> : Assets Non-Current : [Balance Sheet] Amount of non-current assets; for companies that operate a classified balance sheet. Calculated as the different between Total Assets [Assets] and Current Assets [AssetsC]. 
- <b>bvps</b> : Book Value per Share : [Metrics] Measures the ratio between [Equity] and [SharesWA] as adjusted by [ShareFactor]. 
- <b>capex</b> : Capital Expenditure : [Cash Flow Statement] A component of [NCFI] representing the net cash inflow (outflow) associated with the acquisition & disposal of long-lived; physical & intangible assets that are used in the normal conduct of business to produce goods and services and are not intended for resale. Includes cash inflows/outflows to pay for construction of self-constructed assets & software. 
- <b>cashneq</b> : Cash and Equivalents : [Balance Sheet] A component of [Assets] representing the amount of currency on hand as well as demand deposits with banks or financial institutions. 
- <b>cashnequsd</b> : Cash and Equivalents (USD) : [Balance Sheet] [CashnEq] in USD; converted by [FXUSD]. 
- <b>cor</b> : Cost of Revenue : [Income Statement] The aggregate cost of goods produced and sold and services rendered during the reporting period. 
- <b>consolinc</b> : Consolidated Income : [Income Statement] The portion of profit or loss for the period; net of income taxes; which is attributable to the consolidated entity; before the deduction of [NetIncNCI]. 
- <b>currentratio</b> : Current Ratio : [Metrics] The ratio between [AssetsC] and [LiabilitiesC]; for companies that operate a classified balance sheet. 
- <b>de</b> : Debt to Equity Ratio : [Metrics] Measures the ratio between [Liabilities] and [Equity]. 
- <b>debt</b> : Total Debt : [Balance Sheet] A component of [Liabilities] representing the total amount of current and non-current debt owed. Includes secured and unsecured bonds issued; commercial paper; notes payable; credit facilities; lines of credit; capital lease obligations; operating lease obligations; and convertible notes. 
- <b>debtc</b> : Debt Current : [Balance Sheet] The current portion of [Debt]; reported if the company operates a classified balance sheet that segments current and non-current liabilities. 
- <b>debtnc</b> : Debt Non-Current : [Balance Sheet] The non-current portion of [Debt] reported if the company operates a classified balance sheet that segments current and non-current liabilities. 
- <b>debtusd</b> : Total Debt (USD) : [Balance Sheet] [Debt] in USD; converted by [FXUSD]. 
- <b>deferredrev</b> : Deferred Revenue : [Balance Sheet] A component of [Liabilities] representing the carrying amount of consideration received or receivable on potential earnings that were not recognized as revenue; including sales; license fees; and royalties; but excluding interest income. 
- <b>depamor</b> : Depreciation Amortization & Accretion : [Cash Flow Statement] A component of operating cash flow representing the aggregate net amount of depreciation; amortization; and accretion recognized during an accounting period. As a non-cash item; the net amount is added back to net income when calculating cash provided by or used in operations using the indirect method. 
- <b>deposits</b> : Deposit Liabilities : [Balance Sheet] A component of [Liabilities] representing the total of all deposit liabilities held; including foreign and domestic; interest and noninterest bearing. May include demand deposits; saving deposits; Negotiable Order of Withdrawal and time deposits among others. 
- <b>divyield</b> : Dividend Yield : [Metrics] Dividend Yield measures the ratio between a company's [DPS] and its [Price]. 
- <b>dps</b> : Dividends per Basic Common Share : [Income Statement] Aggregate dividends declared during the period for each split-adjusted share of common stock outstanding. Includes spinoffs where identified. 
- <b>ebit</b> : Earning Before Interest & Taxes (EBIT) : [Income Statement] Earnings Before Interest and Tax is calculated by adding [TaxExp] and [IntExp] back to [NetInc]. 
- <b>ebitda</b> : Earnings Before Interest Taxes & Depreciation Amortization (EBITDA) : [Metrics] EBITDA is a non-GAAP accounting metric that is widely used when assessing the performance of companies; calculated by adding [DepAmor] back to [EBIT]. 
- <b>ebitdamargin</b> : EBITDA Margin : [Metrics] Measures the ratio between a company's [EBITDA] and [Revenue]. 
- <b>ebitdausd</b> : Earnings Before Interest Taxes & Depreciation Amortization (USD) : [Metrics] [EBITDA] in USD; converted by [FXUSD]. 
- <b>ebitusd</b> : Earning Before Interest & Taxes (USD) : [Income Statement] [EBIT] in USD; converted by [FXUSD]. 
- <b>ebt</b> : Earnings before Tax : [Metrics] Earnings Before Tax is calculated by adding [TaxExp] back to [NetInc]. 
- <b>eps</b> : Earnings per Basic Share : [Income Statement] Earnings per share as calculated and reported by the company. Approximates to the amount of [NetIncCmn] for the period per each [SharesWA] after adjusting for [ShareFactor]. 
- <b>epsdil</b> : Earnings per Diluted Share : [Income Statement] Earnings per diluted share as calculated and reported by the company. Approximates to the amount of [NetIncCmn] for the period per each [SharesWADil] after adjusting for [ShareFactor].. 
- <b>epsusd</b> : Earnings per Basic Share (USD) : [Income Statement] [EPS] in USD; converted by [FXUSD]. 
- <b>equity</b> : Shareholders Equity : [Balance Sheet] A principal component of the balance sheet; in addition to [Liabilities] and [Assets]; that represents the total of all stockholders' equity (deficit) items; net of receivables from officers; directors; owners; and affiliates of the entity which are attributable to the parent. 
- <b>equityusd</b> : Shareholders Equity (USD) : [Balance Sheet] [Equity] in USD; converted by [FXUSD]. 
- <b>ev</b> : Enterprise Value : [Metrics] Enterprise value is a measure of the value of a business as a whole; calculated as [MarketCap] plus [DebtUSD] minus [CashnEqUSD]. 
- <b>evebit</b> : Enterprise Value over EBIT : [Metrics] Measures the ratio between [EV] and [EBITUSD]. 
- <b>evebitda</b> : Enterprise Value over EBITDA : [Metrics] Measures the ratio between [EV] and [EBITDAUSD]. 
- <b>fcf</b> : Free Cash Flow : [Metrics] Free Cash Flow is a measure of financial performance calculated as [NCFO] minus [CapEx]. 
- <b>fcfps</b> : Free Cash Flow per Share : [Metrics] Free Cash Flow per Share is a valuation metric calculated by dividing [FCF] by [SharesWA] and [ShareFactor]. 
- <b>fxusd</b> : Foreign Currency to USD Exchange Rate : [Metrics] The exchange rate used for the conversion of foreign currency to USD for non-US companies that do not report in USD. 
- <b>gp</b> : Gross Profit : [Income Statement] Aggregate revenue [Revenue] less cost of revenue [CoR] directly attributable to the revenue generation activity. 
- <b>grossmargin</b> : Gross Margin : [Metrics] Gross Margin measures the ratio between a company's [GP] and [Revenue]. 
- <b>intangibles</b> : Goodwill and Intangible Assets : [Balance Sheet] A component of [Assets] representing the carrying amounts of all intangible assets and goodwill as of the balance sheet date; net of accumulated amortization and impairment charges. 
- <b>intexp</b> : Interest Expense : [Income Statement] Amount of the cost of borrowed funds accounted for as interest expense. 
- <b>invcap</b> : Invested Capital : [Metrics] Invested capital is an input into the calculation of [ROIC]; and is calculated as: [Debt] plus [Assets] minus [Intangibles] minus [CashnEq] minus [LiabilitiesC]. Please note this calculation method is subject to change. 
- <b>inventory</b> : Inventory : [Balance Sheet] A component of [Assets] representing the amount after valuation and reserves of inventory expected to be sold; or consumed within one year or operating cycle; if longer. 
- <b>investments</b> : Investments : [Balance Sheet] A component of [Assets] representing the total amount of marketable and non-marketable securties; loans receivable and other invested assets. 
- <b>investmentsc</b> : Investments Current : [Balance Sheet] The current portion of [Investments]; reported if the company operates a classified balance sheet that segments current and non-current assets. 
- <b>investmentsnc</b> : Investments Non-Current : [Balance Sheet] The non-current portion of [Investments]; reported if the company operates a classified balance sheet that segments current and non-current assets. 
- <b>liabilities</b> : Total Liabilities : [Balance Sheet] Sum of the carrying amounts as of the balance sheet date of all liabilities that are recognized. Principal components are [Debt]; [DeferredRev]; [Payables];[Deposits]; and [TaxLiabilities]. 
- <b>liabilitiesc</b> : Current Liabilities : [Balance Sheet] The current portion of [Liabilities]; reported if the company operates a classified balance sheet that segments current and non-current liabilities. 
- <b>liabilitiesnc</b> : Liabilities Non-Current : [Balance Sheet] The non-current portion of [Liabilities]; reported if the company operates a classified balance sheet that segments current and non-current liabilities. 
- <b>marketcap</b> : Market Capitalization : [Metrics] Represents the product of [SharesBas]; [Price] and [ShareFactor]. 
- <b>ncf</b> : Net Cash Flow / Change in Cash & Cash Equivalents : [Cash Flow Statement] Principal component of the cash flow statement representing the amount of increase (decrease) in cash and cash equivalents. Includes [NCFO]; investing [NCFI] and financing [NCFF] for continuing and discontinued operations; and the effect of exchange rate changes on cash [NCFX]. 
- <b>ncfbus</b> : Net Cash Flow - Business Acquisitions and Disposals : [Cash Flow Statement] A component of [NCFI] representing the net cash inflow (outflow) associated with the acquisition & disposal of businesses; joint-ventures; affiliates; and other named investments. 
- <b>ncfcommon</b> : Issuance (Purchase) of Equity Shares : [Cash Flow Statement] A component of [NCFF] representing the net cash inflow (outflow) from common equity changes. Includes additional capital contributions from share issuances and exercise of stock options; and outflow from share repurchases.  
- <b>ncfdebt</b> : Issuance (Repayment) of Debt Securities  : [Cash Flow Statement] A component of [NCFF] representing the net cash inflow (outflow) from issuance (repayment) of debt securities. 
- <b>ncfdiv</b> : Payment of Dividends & Other Cash Distributions    : [Cash Flow Statement] A component of [NCFF] representing dividends and dividend equivalents paid on common stock and restricted stock units. 
- <b>ncff</b> : Net Cash Flow from Financing : [Cash Flow Statement] A component of [NCF] representing the amount of cash inflow (outflow) from financing activities; from continuing and discontinued operations. Principal components of financing cash flow are: issuance (purchase) of equity shares; issuance (repayment) of debt securities; and payment of dividends & other cash distributions. 
- <b>ncfi</b> : Net Cash Flow from Investing : [Cash Flow Statement] A component of [NCF] representing the amount of cash inflow (outflow) from investing activities; from continuing and discontinued operations. Principal components of investing cash flow are: capital (expenditure) disposal of equipment [CapEx]; business (acquisitions) disposition [NCFBus] and investment (acquisition) disposal [NCFInv]. 
- <b>ncfinv</b> : Net Cash Flow - Investment Acquisitions and Disposals : [Cash Flow Statement] A component of [NCFI] representing the net cash inflow (outflow) associated with the acquisition & disposal of investments; including marketable securities and loan originations. 
- <b>ncfo</b> : Net Cash Flow from Operations : [Cash Flow Statement] A component of [NCF] representing the amount of cash inflow (outflow) from operating activities; from continuing and discontinued operations. 
- <b>ncfx</b> : Effect of Exchange Rate Changes on Cash  : [Cash Flow Statement] A component of Net Cash Flow [NCF] representing the amount of increase (decrease) from the effect of exchange rate changes on cash and cash equivalent balances held in foreign currencies. 
- <b>netinc</b> : Net Income : [Income Statement] The portion of profit or loss for the period; net of income taxes; which is attributable to the parent after the deduction of [NetIncNCI] from [ConsolInc]; and before the deduction of [PrefDivIS]. 
- <b>netinccmn</b> : Net Income Common Stock : [Income Statement] The amount of net income (loss) for the period due to common shareholders. Typically differs from [NetInc] to the parent entity due to the deduction of [PrefDivIS]. 
- <b>netinccmnusd</b> : Net Income Common Stock (USD) : [Income Statement] [NetIncCmn] in USD; converted by [FXUSD]. 
- <b>netincdis</b> : Net Loss Income from Discontinued Operations : [Income Statement] Amount of loss (income) from a disposal group; net of income tax; reported as a separate component of income. 
- <b>netincnci</b> : Net Income to Non-Controlling Interests : [Income Statement] The portion of income which is attributable to non-controlling interest shareholders; subtracted from [ConsolInc] in order to obtain [NetInc]. 
- <b>netmargin</b> : Profit Margin : [Metrics] Measures the ratio between a company's [NetIncCmn] and [Revenue]. 
- <b>opex</b> : Operating Expenses : [Income Statement] Operating expenses represents the total expenditure on [SGnA]; [RnD] and other operating expense items; it excludes [CoR]. 
- <b>opinc</b> : Operating Income : [Income Statement] Operating income is a measure of financial performance before the deduction of [IntExp]; [TaxExp] and other Non-Operating items. It is calculated as [GP] minus [OpEx]. 
- <b>payables</b> : Trade and Non-Trade Payables : [Balance Sheet] A component of [Liabilities] representing trade and non-trade payables. 
- <b>payoutratio</b> : Payout Ratio : [Metrics] The percentage of earnings paid as dividends to common stockholders. - Calculated by dividing [DPS] by [EPSUSD]. 
- <b>pb</b> : Price to Book Value : [Metrics] Measures the ratio between [MarketCap] and [EquityUSD]. 
- <b>pe</b> : Price Earnings (Damodaran Method) : [Metrics] Measures the ratio between [MarketCap] and [NetIncCmnUSD] 
- <b>pe1</b> : Price to Earnings Ratio : [Metrics] An alternative to [PE] representing the ratio between [Price] and [EPSUSD]. 
- <b>ppnenet</b> : Property Plant & Equipment Net : [Balance Sheet] A component of [Assets] representing the amount after accumulated depreciation; depletion and amortization of physical assets used in the normal conduct of business to produce goods and services and not intended for resale. Includes Operating Right of Use Assets. 
- <b>prefdivis</b> : Preferred Dividends Income Statement Impact : [Income Statement] Income statement item reflecting dividend payments to preferred stockholders. Subtracted from Net Income to Parent [NetInc] to obtain Net Income to Common Stockholders [NetIncCmn]. 
- <b>price</b> : Share Price (Adjusted Close) : [Entity] The price per common share adjusted for stock splits but not adjusted for dividends; used in the computation of [PE1]; [PS1]; [DivYield] and [SPS]. 
- <b>ps</b> : Price Sales (Damodaran Method) : [Metrics] Measures the ratio between [MarketCap] and [RevenueUSD]. 
- <b>ps1</b> : Price to Sales Ratio : [Metrics] An alternative calculation method to [PS]; that measures the ratio between a company's [Price] and it's [SPS]. 
- <b>receivables</b> : Trade and Non-Trade Receivables : [Balance Sheet] A component of [Assets] representing trade and non-trade receivables. 
- <b>retearn</b> : Accumulated Retained Earnings (Deficit) : [Balance Sheet] A component of [Equity] representing the cumulative amount of the entities undistributed earnings or deficit. May only be reported annually by certain companies; rather than quarterly. 
- <b>revenue</b> : Revenues : [Income Statement] Amount of Revenue recognized from goods sold; services rendered; insurance premiums; or other activities that constitute an earning process. Interest income for financial institutions is reported net of interest expense and provision for credit losses. 
- <b>revenueusd</b> : Revenues (USD) : [Income Statement] [Revenue] in USD; converted by [FXUSD]. 
- <b>rnd</b> : Research and Development Expense : [Income Statement] A component of [OpEx] representing the aggregate costs incurred in a planned search or critical investigation aimed at discovery of new knowledge with the hope that such knowledge will be useful in developing a new product or service. 
- <b>sbcomp</b> : Share Based Compensation : [Cash Flow Statement] A component of [NCFO] representing the total amount of noncash; equity-based employee remuneration. This may include the value of stock or unit options; amortization of restricted stock or units; and adjustment for officers' compensation. As noncash; this element is an add back when calculating net cash generated by operating activities using the indirect method. 
- <b>sgna</b> : Selling General and Administrative Expense : [Income Statement] A component of [OpEx] representing the aggregate total costs related to selling a firm's product and services; as well as all other general and administrative expenses. Direct selling expenses (for example; credit; warranty; and advertising) are expenses that can be directly linked to the sale of specific products. Indirect selling expenses are expenses that cannot be directly linked to the sale of specific products; for example telephone expenses; Internet; and postal charges. General and administrative expenses include salaries of non-sales personnel; rent; utilities; communication; etc. 
- <b>sharefactor</b> : Share Factor : [Entity] Share factor is a multiplicant in the calculation of [MarketCap] and is used to adjust for: American Depository Receipts (ADRs) that represent more or less than 1 underlying share; and; companies which have different earnings share for different share classes (eg Berkshire Hathaway - BRK.B). 
- <b>sharesbas</b> : Shares (Basic) : [Entity] The number of shares or other units outstanding of the entity's capital or common stock or other ownership interests; as stated on the cover of related periodic report (10-K/10-Q); after adjustment for stock splits. 
- <b>shareswa</b> : Weighted Average Shares : [Income Statement] The weighted average number of shares or units issued and outstanding that are used by the company to calculate [EPS]; determined based on the timing of issuance of shares or units in the period. 
- <b>shareswadil</b> : Weighted Average Shares Diluted : [Income Statement] The weighted average number of shares or units issued and outstanding that are used by the company to calculate [EPSDil]; determined based on the timing of issuance of shares or units in the period. 
- <b>sps</b> : Sales per Share : [Metrics] Sales per Share measures the ratio between [RevenueUSD] and [SharesWA] as adjusted by [ShareFactor]. 
- <b>tangibles</b> : Tangible Asset Value : [Metrics] The value of tangibles assets calculated as the difference between [Assets] and [Intangibles]. 
- <b>taxassets</b> : Tax Assets : [Balance Sheet] A component of [Assets] representing tax assets and receivables. 
- <b>taxexp</b> : Income Tax Expense : [Income Statement] Amount of current income tax expense (benefit) and deferred income tax expense (benefit) pertaining to continuing operations. 
- <b>taxliabilities</b> : Tax Liabilities : [Balance Sheet] A component of [Liabilities] representing outstanding tax liabilities. 
- <b>tbvps</b> : Tangible Assets Book Value per Share : [Metrics] Measures the ratio between [Tangibles] and [SharesWA] as adjusted by [ShareFactor]. 
- <b>workingcapital</b> : Working Capital : [Metrics] Working capital measures the difference between [AssetsC] and [LiabilitiesC]. 
- <b>roe</b>: Return on Average Equity : [Metrics] Return on equity measures a corporation's profitability by calculating the amount of [NetIncCmn] returned as a percentage of [EquityAvg]. 
- <b>roa</b> : Return on Average Assets : [Metrics] Return on assets measures how profitable a company is [NetIncCmn] relative to its total assets [AssetsAvg].

##### Sharadar Equity Prices [SHARADAR/SEP] features

- <b>open</b> : Open Price - Split Adjusted : The opening share price, adjusted for stock splits and stock dividends. 
- <b>high</b> : High Price - Split Adjusted : The high share price, adjusted for stock splits and stock dividends. 
- <b>low</b> : Low Price - Split Adjusted : The low share price, adjusted for stock splits and stock dividends. 
- <b>close</b> : Close Price - Split Adjusted : The open share closing, adjusted for stock splits and stock dividends. 
- <b>volume</b> : Volume - Split Adjusted : The traded volume, adjusted for stock splits and stock dividends.

##### Daily Metrics ([SHARADAR/DAILY] features

- <b>ev</b> : Enterprise Value - Daily : Enterprise value is a measure of the value of a business as a whole; calculated as [MarketCap] plus [DebtUSD] minus [CashnEqUSD]. [MarketCap] is calculated by us, and the remaining figures are sourced from the most recent SEC form 10 filings. 
- <b>evebit</b> : Enterprise Value over EBIT - Daily : Measures the ratio between [EV] and [EBITUSD]. EBITUSD is derived from the most recent SEC form 10 filings. 
- <b>evebitda</b> : Enterprise Value over EBITDA - Daily : Measures the ratio between [EV] and [EBITDAUSD]. EBITDAUSD is derived from the most recent SEC form 10 filings. 
- <b>marketcap</b> : Market Capitalization - Daily : Represents the product of [SharesBas]; [Price] and [ShareFactor]. [SharesBas] is sourced from the most recent SEC form 10 filing. 
- <b>pb</b> : Price to Book Value - Daily : Measures the ratio between [MarketCap] and [EquityUSD]. [EquityUSD] is sourced from the most recent SEC form 10 filing. 
- <b>pe</b> : Price Earnings (Damodaran Method) - Daily : Measures the ratio between [MarketCap] and [NetIncCmnUSD]. [NetIncCmnUSD] is sourced from the most recent SEC form 10 filings. 
- <b>ps</b> : Price Sales (Damodaran Method) - Daily : Measures the ratio between [MarketCap] and [RevenueUSD]. [RevenueUSD] is sourced from the most recent SEC form 10 filings. 

##### Sentiment Analysis and News Analytics ([IFT/NSA] features

- <b>sentiment</b>: a numeric measure of the bullishness / bearishness of news coverage of the stock.
- <b>sentiment_high</b>: highest intraday sentiment scores.
- <b>sentiment_low</b>: lowest intraday sentiment scores.
- <b>news_volume</b>: the absolute number of news articles covering the stock.
- <b>news_buzz</b>: a numeric measure of the change in coverage volume for the stock.


## Factor Analysis Target Variables

The factor analysis is performed using [alphalens](https://quantopian.github.io/alphalens/index.html) and [Pyfolio](https://quantopian.github.io/pyfolio/). These packages regrouped APIs useful for data processing and factor analysis over the pre-defined periods. These metrics are  mentioned here below:

- <b>Cleaning and preparing data</b> `alphalens.utils.get_clean_factor_and_forward_returns`: Formats the factor data, pricing data, and group mappings into a DataFrame that contains aligned MultiIndex indices of timestamp and asset. The returned data will be formatted to be suitable for Alphalens functions. 
- <b>Cumulated factor return</b> `alphalens.performance.factor_returns`: Builds cumulative returns from ‘period’ returns. This function simulate the cumulative effect that a series of gains or losses (the ‘returns’) have on an original amount of capital over a period of time.
-  <b>Mean quantile return</b> `alphalens.performance.mean_return_by_quantile`: Computes mean returns for factor quantiles across provided forward returns columns.
- <b>Factor Rank Autocorrelation</b> `alphalens.performance.factor_rank_autocorrelation`: Computes autocorrelation of mean factor ranks in specified time spans. We must compare period to period factor ranks rather than factor values to account for systematic shifts in the factor values of all names or names within a group. This metric is useful for measuring the turnover of a factor. If the value of a factor for each name changes randomly from period to period, we’d expect an autocorrelation of 0.
- <b>Sharpe ratio</b> `sharpe_ratio`: This function computes annualized sharpe ratio. This metric is used to understand the return of an investment compared to its risk. The ratio is the average return earned in excess per unit of volatility or total risk. Volatility is a measure of the factor return fluctuations of an asset.


## The Combined Alpha Vector

To get the single score for each stock we have to combine selected factors. This is an area where machine learning can be very helpful. In this context, the [feature_weights](https://github.com/keyvantaj/Quantitative/blob/master/feature_weights.py) module is implemented to gives us optimal weights to the selected alpha factors and result in the best combination.


## Risk Management

We measured the predicted risk cap using [risk_model](https://github.com/keyvantaj/Quantitative/blob/master/risk_model.py) module. For this purpose the portfolio risk formula is √𝑋𝑇(𝐵𝐹𝐵𝑇+𝑆)𝑋 where:

* 𝑋  is the portfolio weights
* 𝐵  is the factor betas
* 𝐹  is the factor covariance matrix
* 𝑆  is the idiosyncratic variance matrix


## Optimization

Once alpha model and a risk model are generated, we want to find a portfolio that trades as close as possible to the alpha model but limiting risk as measured by the [risk_model](https://github.com/keyvantaj/Quantitative/blob/master/risk_model.py). The [cxpy](https://www.cvxpy.org/) package is used to implement the [optimizer](https://github.com/keyvantaj/Quantitative/blob/master/optimizer.py)

The CVXPY objective function is to maximize 𝛼𝑇 ∗ 𝑥 , where x is the portfolio weights and alpha is the alpha vector.

In the other hand we have the following constraints:

* 𝑟 ≤ 𝑟𝑖𝑠𝑘2cap
* 𝐵𝑇 ∗ 𝑥 ⪯ 𝑓𝑎𝑐𝑡𝑜𝑟max
* 𝐵𝑇 ∗ 𝑥 ⪰ 𝑓𝑎𝑐𝑡𝑜𝑟min
* 𝑥𝑇𝟙 = 0
* ‖𝑥‖ ≤ 1
* 𝑥 ⪰ 𝑤𝑒𝑖𝑔ℎ𝑡𝑠min
* 𝑥 ⪯ 𝑤𝑒𝑖𝑔ℎ𝑡𝑠max

Where x is the portfolio weights, B is the factor betas, and r is the portfolio risk calculated in [risk model](https://github.com/keyvantaj/Quantitative/blob/master/risk_model.py) module.

The first constraint is that the predicted risk be less than some maximum limit. The second and third constraints are on the maximum and minimum portfolio factor exposures. The fourth constraint is the "market neutral constraint: the sum of the weights must be zero. The fifth constraint is the leverage constraint: the sum of the absolute value of the weights must be less than or equal to 1.0. The last are some minimum and maximum limits on individual holdings.






