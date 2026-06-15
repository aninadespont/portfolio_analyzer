# **Portfolio Analyzer**

Python command-line tool for constructing and analyzing a user-defined stock portfolio. The program retrieves historical financial data from yfinance, which fetches publicly available data from Yahoo Finance. Based on this data, the program computes a comprehensive set of financial metrics for individual stocks, the portfolio as a whole, and a major index used as a benchmark for comparison. It also analyzes stocks’ and the portfolio’s CAPM to estimate expected returns and alpha and plots the latter against the security market line. Finally, it projects 1-year future prices, returns, and volatility for both the benchmark and the portfolio using a blended forecasting model combining exponential moving averages and historical averages 50/50. 

## Features

- **Custom Portfolio Construction:** the user defines the number of stocks, selects the tickers, attributes custom weights to each stock, and chooses a custom period. It also selects a benchmark index among the S&P 500, Nasdaq, and Dow Jones

-	**Stock-Level Metrics:** average annual return, best year, worst year, annual volatility, CAGR, and beta for each ticket

-	**Correlation Heatmap:** visual representation of pairwise correlations between stocks to assess diversification

-	**Portfolio-Level Metrics:** expected return, best year, worst year, annual volatility, CAGR, beta, Sharpe ratio, and diversification score
  
-	**Benchmark-Level Metrics:** expected return, best year, worst year, annual volatility, CAGR, and Sharpe ratio

-	**CAPM Analysis:** portfolio beta, CAPM return, actual return, and alpha for both individual stocks and the portfolio

-	**Security Market Line:** visual representation of the security market line, the risk-free rate, portfolio expected return according to the CAPM, and portfolio alpha

-	**1-Year Exponential Moving Average Forecast:** projected future returns and prices for the portfolio and the benchmark, using the combination of 50% historical average returns and 50% exponential moving averages with an emphasis on the last 126 trading days. The same approach is used to forecast volatility with standard deviation range scaled with √t under a random-walk assumption. Outputs include a graph representing forecasted prices and uncertainty bands, as well as a summary table of projected returns and volatility over the period, as well as the forecasted end price. 

## Project Structure
- Main script: main.py
- Readme file: README.md  

## Requirements

**Environment**:
-	Command-line interface interactive script
-	Developed in Jupyter Notebook (version 7.0.8) 
-	Python 3.11.7 (ipykernel)

**Libraries**:
-	Pandas (version 2.1.4): tabular data and time series
-	Numpy (version 1.26.4): mathematical operations
-	Matplotlib (version 3.8.0): charts and graphs
-	Seaborn (version 0.12.2): correlation heatmap
-	yfinance (version 1.4.1): financial data from https://github.com/ranaroussi/yfinance 

**Installation**:

Install libraries using: 
- pip install yfinance pandas numpy matplotlib seaborn

You can run this in a terminal or directly inside a Jupyter notebook cell.

**Notes**: 
-	Different library versions may affect function behaviors or supported parameters
-	The program depends on the retrieval of up-to-date market data via yfinance library

## Usage

- Install Python3
- Open Jupyter Notebook (recommended)
- Download the file main.py in your computer and then upload it to Jupyter Notebook
- Run the following script in an empty cell in Jupyter Notebook:
  - %run main.py


**The program is interactive and will guide you through the following steps:**

**1.	User Setup:**
- What is your name?
   - The program returns a personalized welcome message.

**2.	Portfolio Construction:** 
-	Number of stocks:
    - How many stocks would you like to add to your portfolio?

-	Stock selection:
    - Which stock would you like to add to your portfolio? Please enter the stock's ticker symbol.

-	Weight allocation:
    - What weight do you wish to put on {ticker}? Enter either a percentage or a decimal:


**3.	Analysis Settings:**
-	Choose a time period: 
    - 1 year, 5 years, 10 years, or a custom period length in years, months, or days
 	
-	Choose benchmark:
    - Which benchmark would you like as a reference? 1. S&P 500, 2. Nasdaq, 3. Dow Jones. Enter 1, 2, or 3:


**4.	Output:**
   
  Once the inputs are provided, the program automatically generates the following:
- Stock performance summary tables 
- Stocks correlation heatmap
- Portfolio and benchmark performance summary tables
-	Stock and portfolio CAPM analysis table
-	Security market line chart plotted against the risk-free rate and the portfolio expected return
-	1-year projected price and volatility band chart for the index and the portfolio
-	Forecast summary table (returns, price, volatility) for both the benchmark and portfolio

## Example
<img width="940" height="241" alt="image" src="https://github.com/user-attachments/assets/f1cb467d-73ce-4e06-82ac-ea4080c7c6d3" />
<img width="940" height="225" alt="image" src="https://github.com/user-attachments/assets/2ccd5980-0669-412e-b13f-0499214e9ba0" />
<img width="940" height="350" alt="image" src="https://github.com/user-attachments/assets/9c388899-1b6d-448b-8d58-24b359700246" />
<img width="940" height="92" alt="image" src="https://github.com/user-attachments/assets/8d348ab9-9ed1-45e3-a0ff-57eb066e0aa7" />
<img width="940" height="729" alt="image" src="https://github.com/user-attachments/assets/7560f234-4676-411f-891f-35ace7e8cf9c" />
<img width="940" height="89" alt="image" src="https://github.com/user-attachments/assets/9e7609bf-5e0c-4570-98e0-8f9fb3977871" />
<img width="940" height="73" alt="image" src="https://github.com/user-attachments/assets/4cd17253-46de-445c-94d9-9b88d27bf15d" />
<img width="700" height="124" alt="image" src="https://github.com/user-attachments/assets/441671e9-e59a-4e92-9db8-4e2f144e51f0" />
<img width="682" height="95" alt="image" src="https://github.com/user-attachments/assets/2ef44b12-bb91-4d71-873b-08c11c78cb3f" />
<img width="940" height="546" alt="image" src="https://github.com/user-attachments/assets/5e1cc2fe-ca54-4caf-9c9c-f6f1ea17f93f" />
<img width="940" height="456" alt="image" src="https://github.com/user-attachments/assets/a59c5064-4270-4baa-8507-fe9ce81bc9e9" />
<img width="940" height="128" alt="image" src="https://github.com/user-attachments/assets/5c940978-fd3c-47be-b1ae-7f8ddf790698" />


## Project Context

Python-based portfolio analysis tool developed as part of the course “Skills: Programming – Introduction Level” at the University of St. Gallen (Spring 2026). The project combines Python programming (functions, input validation, error handling, and loops) with applied financial analysis (risk, return, covariance, diversification, and time series forecasting).



