# Portfolio Analyzer
# **Portfolio Analyzer**

Python command-line tool for constructing and analyzing a user-defined stock portfolio. The program retrieves historical financial data from yfinance, which fetches publicly available data from Yahoo Finance. Based on this data, the program computes a comprehensive set of financial metrics for individual stocks, the portfolio as a whole, and a major index used as a benchmark for comparison. It also analyzes stocks’ and the portfolio’s CAPM to estimate expected returns and alpha. Finally, it projects 1-year future returns for both the benchmark and the portfolio using a blended forecasting model combining exponential moving averages and historical averages. 

## Features

- Custom portfolio construction: the user defines the number of stocks, selects the tickers, attributes custom weights to each stock, and chooses a custom period. It also selects a benchmark index among the S&P 500, Nasdaq, and Dow Jones. 
-	Stock-level metrics: average annual return, best year, worst year, annual volatility, CAGR, and beta for each ticket.
-	Correlation heatmap: visual representation of pairwise correlations between stocks to assess diversification.
-	Portfolio-level metrics: expected return, best year, worst year, annual volatility, CAGR, beta, Sharpe ratio, and diversification score.
-	Benchmark-level metrics: expected return, best year, worst year, annual volatility, CAGR, and Sharpe ratio.
-	CAPM analysis: portfolio beta, CAPM return, actual return, and alpha for both individual stocks and the portfolio.
-	Security Market Line: visual representation of the security market line, the risk-free rate, portfolio expected return according to the CAPM, and portfolio alpha. 
-	1-year EMA forecast: projected future returns, prices, and volatility for the portfolio and the benchmark, using the combination of 50% historical average returns and 50% exponential moving averages with an emphasis on the last 63 trading days and a standard deviation range scaled with √t under a random-walk assumption. Outputs include a graph representing forecasted prices and uncertainty bands, as well as a summary table of projected returns and volatility. 

## Project Structure:
- Main script: main.py
- Readme file: README.md  

## Requirements

Environment:
-	Command Line Interface interactive script
-	Developed in Jupyter Notebook (version 7.0.8) 
-	Python 3.11.7 (ipykernel)

Libraries:
-	Pandas (version 2.1.4): 
-	Numpy (version 1.26.4):
-	Matplotlib (version 3.8.0):
-	Seaborn (version 0.12.2):
-	yfinance (version 1.4.1): financial and market data 
o	Source: https://github.com/ranaroussi/yfinance 

Installation:
Install dependencies using: 
pip install yfinance pandas numpy matplotlib seaborn
You can run this in a terminal or directly inside a Jupyter notebook cell.

Notes: 
-	Different library versions may affect function behaviors or parameters.
-	The program depends on the retrieval of up-to-date market data via yfinance library.

## Usage

Install Python3
Open Jupyter Notebook (recommended)
Download main.ipynb inside Jupyter Notebook

Run the script from the command line:

%run main.ipynb
Or 
Open the file, click on the cell with the code, and do Shift + Enter to run the code.

The program is interactive and will guide you through the following steps:

1.	User setup
What is your name?
-> The program returns a personalized welcome message.

2.	Portfolio construction: 
-	Number of stocks:
How many stocks would you like to add to your portfolio?

-	Stock selection:
Which stock would you like to add to your portfolio? Please enter the stock's ticker symbol.

-	Weight allocation:
What weight do you wish to put on {ticker}? Enter either a percentage or a decimal:

3.	Analysis settings:
-	Choose a time period: 
1 year, 5 years, 10 years, or a custom period length in years, months, or days
-	Choose benchmark:
Which benchmark would you like as a reference? 1. S&P 500, 2. Nasdaq, 3. Dow Jones. Enter 1, 2, or 3:

4.	Output: 
Once the inputs are provided, the program automatically generates the following:
o	Stocks performance summary tables 
o	Stocks correlation heatmap
o	Portfolio and benchmark performance summary tables
o	Stock and portfolio CAPM analysis table
o	Security market line chart
o	1-year projected price and volatility band chart
o	Forecast summary table (returns, price, volatility) 

## Example
![alt text](image.png)
![alt text](image-1.png)
![alt text](image-2.png)
![alt text](image-3.png)
![alt text](image-4.png)
![alt text](image-5.png)
![alt text](image-6.png)
![alt text](image-7.png)
![alt text](image-8.png)
![alt text](image-9.png)
![alt text](image-10.png)
![alt text](image-11.png)


## Project Context

Python-based portfolio analysis tool developed as part of the course “Skills: Programming – Introduction Level” at the University of St. Gallen (Spring 2026). The project combines Python programming (functions, input validation, error handling, and loops) with applied financial analysis (risk, return, covariance, diversification, and time series forecasting).
Anina Despont

