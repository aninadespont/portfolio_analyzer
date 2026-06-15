# Portfolio analysis tool

# This program lets the user build a custom stock portfolio and analyze its returns, volatility, CAGR, beta, Sharpe ratio, correlation, diversification, CAPM, alpha vs a chosen benchmark, and a simple 1-year EMA-based forecast.
 
# Requirements: this program requires libraries that must be installed via pip if missing: 
    # pip install yfinance pandas numpy matplotlib seaborn

# Role of these libraries:
    # yfinance: historical market data using Yahoo's publicly available APIs
    # pandas: tabular data and time series
    # numpy: mathematical operations
    # matplotlib: charts and graphs
    # seaborn: correlation heatmap 

import yfinance as yf 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns

# Pandas display settings for cleaner console output
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)


# This program is divided into multiple functions, each responsible for one stage of the analysis
# Some of these functions compute and return several related values instead of being split into many smaller functions
# This was done intentionally to avoid having to pass a large number of separate arguments between many small functions
# All functions are defined first and called afterwards in the main execution block at the end of the program

#------------------------ PORTFOLIO CONSTRUCTION WITH THE USER ------------------------
      
# Asking the user the number of stocks they want to add to their portfolio 
# The program ensures that a positive number is entered and handles non-numeric inputs
def get_portfolio_size():
    while True:
        try:
            n = int(input("\nHow many stocks would you like to add to your portfolio?"))
            if n > 0:
                return n
            else:
                print("\nPlease enter a number greater than 0:")
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")

# Asking the user to enter the ticker symbol they want to add to their portfolio
# The program verifies that the ticker is not already in the portfolio
# It checks its existence by attempting to download it from yfinance
# If the ticker is not found in yfinance, this ticker either does not exist or it is misspelled
def get_valid_ticker(existing_tickers):
    while True:
        ticker = input("\nWhich stock would you like to add to your portfolio? Please enter the stock's ticker symbol.")

        if ticker in existing_tickers:
            print(f"Error: {ticker} has already been added to the portfolio.")
            continue
            
        stock_data = yf.download(ticker, period="5d", auto_adjust=True, progress=False)
        
        if not stock_data.empty:
            return ticker
        else:
            print(f"\n{ticker} was not found on Yahoo Finance. Either the ticker does not exist or you misspelled it. Please try again.")
            
# Asking the user to assign a weight to the stock in the portfolio, either as a percentage (e.g., 30) or as a decimal (e.g., 0.30)
# If the user enters a percentage, the value is converted to a decimal
# The program also ensures that the weight entered is between 0 and 100 and handles non-numeric inputs
def get_weight_ticker(ticker):
    while True:
        try:
            weight = float(input(f"\nWhat weight would you like to assign to {ticker}? Enter either a percentage or a decimal: "))

            if weight > 1:
                weight = weight / 100

            if 0 < weight <= 1:
                return weight
            else:
                print("\nThe weight must be greater than 0% and no more than 100%.")
        
        except ValueError:
            print("\nInvalid input. Please enter a numerical value for the weight.")

# Building the portfolio as a list of {"ticker": ..., "weight": ...} dictionaries
# The program loops until all the weights sum up to 1
# If the condition is not met, an error is raised and the user must restart the process
def create_portfolio():
    while True:
        portfolio = []
        existing_tickers = set()
        
        stocks_count = get_portfolio_size()
        
        for i in range(stocks_count):
            ticker = get_valid_ticker(existing_tickers)
            existing_tickers.add(ticker) 
            
            weight = get_weight_ticker(ticker)
            portfolio.append({"ticker": ticker, "weight": weight})

        total_weight = sum(item["weight"] for item in portfolio)
        
        if abs(total_weight - 1) < 1e-9:
            return portfolio
        else: 
            print(f"\nYour total weight is {total_weight}. It must add up to 1. Please enter valid weights.")

# Selection of the period by the user and handling of invalid input (non-numerical values and invalid choices outside the 4 options)
# If the user chooses a custom period, the program ensures that the input is positive and numerical.
# The program also asks for the unit of the number to build a string compatible with yfinance time units (e.g., 10y, 6mo, 90d)
def get_period_from_user():
    while True:
        try:
            period_choice = int(input("\nChoose a time period for the analysis:\n"
                "1. 1 year\n"
                "2. 5 years\n"
                "3. 10 years\n"
                "4. Other\n"
                "Please choose a number between 1 and 4: "))

            if period_choice == 1:
                return "1y"
            elif period_choice == 2:
                return "5y"
            elif period_choice == 3:
                return "10y"
            elif period_choice == 4:
                while True:
                    try:
                        custom = int(input("\nEnter a custom period length: "))
                        if custom <= 0:
                            print("Please enter a positive number.")
                            continue
                            
                        time_period = int(input("Is this in:\n"
                                                "1. Years\n"
                                                "2. Months\n"
                                                "3. Days\n"
                                                "Please choose a number between 1 and 3: "))
                        if time_period == 1:
                            return f"{custom}y"
                        elif time_period == 2:
                            return f"{custom}mo"
                        elif time_period == 3:
                            return f"{custom}d"
                        else:
                            print("Invalid input. Please enter a number between 1 and 3.")
                    except ValueError:
                        print("Invalid input. Please enter a number only.")
            else:
                print("Invalid input. Please choose a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number only.")

# Asking user which benchmark they want as a reference between Nasdaq, S&P 500, and Dow Jones
# The program ensures that the user enters a numerical value between 1 and 3
# It then retrieves the corresponding adjusted closing price from yfinance for the selected benchmark over the user-defined period to ensure that comparisons between portfolio and benchmark metrics are consistent
# The price and name of the benchmark are returned for later use in formulas and tables 
def get_benchmark_choice(period):
    while True:
        try:
            benchmark = int(input("\nWhich index would you like as a benchmark:\n"
                "1. S&P 500\n"
                "2. Nasdaq\n"
                "3. Dow Jones\n"
                "\nEnter 1, 2, or 3: "))
            
            if benchmark == 1:
                benchmark_name = "S&P 500"
                benchmark_price = yf.download("^GSPC", period = period, auto_adjust=True, progress=False)["Close"]
                
                return benchmark_name, benchmark_price
            
            elif benchmark == 2:
                benchmark_name = "Nasdaq"
                benchmark_price = yf.download("^IXIC", period = period, auto_adjust=True, progress=False)["Close"]
               
                return benchmark_name, benchmark_price
            
            elif benchmark == 3:
                benchmark_name = "Dow Jones"
                benchmark_price = yf.download("^DJI", period = period, auto_adjust=True, progress=False)["Close"]
                
                return benchmark_name, benchmark_price
            
            else:
                print("Invalid input. Please enter either the number 1, 2, or 3.")
        
        except ValueError:
            print("Invalid input. Please enter an integer between 1 and 3")

# ----------------------- METRICS CALCULATIONS AND TABLE GENERATION -----------------------

# Retrieving data from yfinance for each selected stock and computing multiple metrics for each stock
def get_stock_metrics(portfolio, period, benchmark_price):

    tickers = []
    for item in portfolio:
        tickers.append(item["ticker"])

    weights = []
    for item in portfolio:
        weights.append(item["weight"])

    # Downloading adjusted closing prices for all tickers
    prices = yf.download(tickers, period = period, auto_adjust=True, progress=False)["Close"]

    # Daily returns of stocks as percentage changes and removing NaN values (as the first row is always NaN because there is no previous price)
    daily_returns_stocks = prices.pct_change().dropna()

    # Annual volatility of each stock using 252 days (the number of trading days in a year)
    annual_stock_volatility = daily_returns_stocks.std() * np.sqrt(252)

    # Yearly stock returns by compounding daily to get the true yearly returns instead of summing daily returns
    # Calcuation of the average annual return over the chosen period to know how a typical year performs on average and identify the best and worst year
    yearly_stock_returns = daily_returns_stocks.resample("Y").apply(lambda x: (1 + x).prod() - 1) 
    avg_annual_stock_return  = yearly_stock_returns.mean()   
    best_year_stock_return   = yearly_stock_returns.max()
    worst_year_stock_return  = yearly_stock_returns.min()
 
    # Compound Annual Growth Rate (CAGR) per ticker to measure the total return over the entire period
    days_stocks = (prices.index[-1] - prices.index[0]).days
    cagr_stocks = (prices.iloc[-1] / prices.iloc [0]) ** (365 / days_stocks) -1

    # Betas of individual stocks to measure their sensitivity to the market
    # For this: calculation of the daily returns of the benchmark and its variance
    # Then a for loop is used to compute each stock's beta using: Beta = Cov(stock, benchmark) / Var(benchmark)
    # The dates of the stocks and benchmark are aligned to ensure they cover the same trading days
    daily_returns_benchmark = benchmark_price.squeeze().pct_change().dropna()
    benchmark_var = daily_returns_benchmark.var()

    common_dates = daily_returns_stocks.index.intersection(daily_returns_benchmark.index)
    daily_returns_stocks = daily_returns_stocks.loc[common_dates]
    daily_returns_benchmark = daily_returns_benchmark.loc[common_dates]

    beta_stocks = []
    for ticker in tickers:
        cov = daily_returns_stocks[ticker].cov(daily_returns_benchmark)
        beta = cov / benchmark_var
        beta_stocks.append(float(beta))

    # Table containing all the computed results
    df_stock_metrics = pd.DataFrame({
        "Ticker": tickers,
        "Weight (%)": np.array(weights) * 100,
        "Period": period,
        "Average annual return (%)": (avg_annual_stock_return.to_numpy() * 100),
        "Best year (%)": (best_year_stock_return.to_numpy() * 100),
        "Worst year (%)": (worst_year_stock_return.to_numpy() * 100),
        "Annual volatility (%)":(annual_stock_volatility.to_numpy() * 100), 
        "CAGR (%)": (cagr_stocks.to_numpy() * 100),
        "Beta": beta_stocks
            })
    
    # Setting the index to start the table at row 1 instead of 0
    df_stock_metrics.index = df_stock_metrics.index + 1

    return df_stock_metrics, daily_returns_stocks, yearly_stock_returns, avg_annual_stock_return, annual_stock_volatility, beta_stocks, prices, tickers, weights

# Correlation heatmap showing pairwise correlations between all stocks in the portfolio
# Values close to 1 indicate that two stocks move together, while values close to 0 or negative indicate that they move in different directions (higher diversification)
def get_corr_heatmap(daily_returns_stocks):
    
    corr_matrix = daily_returns_stocks.corr()
    
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", square=True, vmin=-1, vmax=1, center=0, xticklabels=True, yticklabels=True)
    plt.title("Portfolio Correlation Heatmap", fontsize=12)
    plt.tight_layout()
    plt.show()
    plt.close(fig)

# Function to select the most appropriate US Treasury yield ticker based on the chosen period
def get_rfr_ticker(period):

    # Extracting the numeric part of the period string (e.g.,"1y", "10y", "6mo", "90d") and turning months and days into yearly equivalents for comparison across time horizons
    period_lower = period.lower()
    if period_lower.endswith("y"):
        years = int(period_lower[:-1])
    elif period_lower.endswith("mo"):
        years = int(period_lower[:-2]) / 12
    elif period_lower.endswith("d"):
        years = int(period_lower[:-1]) / 365
    # Fallback option if the period is not recognized
    else:
        years = 5  

    # Assigning the corresponding yield to the period
    # Downloading the corresponding data
    # Converting the last available risk-free rate into decimal form for future computations as yfinance returns the data in %
    
    # 3-month T-bill for short-term horizons
    if years <= 1:
        raw_rfr = yf.download("^IRX", period=period, auto_adjust=True, progress=False)["Close"].squeeze()
        risk_free_rate = float((raw_rfr.iloc[-1] / 100))
        
        return raw_rfr, risk_free_rate
        
    # 5-year Treasury yield for medium-term horizons
    elif years <= 7:
        raw_rfr = yf.download("^FVX", period=period, auto_adjust=True, progress=False)["Close"].squeeze()
        risk_free_rate = float((raw_rfr.iloc[-1] / 100))

        return raw_rfr, risk_free_rate
    
    # 10-year Treasury note for long-term horizons
    else:
        raw_rfr = yf.download("^TNX", period=period, auto_adjust=True, progress=False)["Close"].squeeze()
        risk_free_rate = float((raw_rfr.iloc[-1] / 100))
                               
        return raw_rfr, risk_free_rate

# Calculation of different portfolio metrics
def get_portfolio_metrics(portfolio, daily_returns_stocks, yearly_stock_returns, avg_annual_stock_return, annual_stock_volatility, beta_stocks, prices, period, raw_rfr, risk_free_rate, tickers, weights):
 
    # Portfolio yearly returns as the weighted sum of individual stock returns per year 
    portfolio_yearly_returns = yearly_stock_returns @ weights
    avg_annual_return_portfolio = float(portfolio_yearly_returns.mean())
    best_year_portfolio = float(portfolio_yearly_returns.max())
    worst_year_portfolio = float(portfolio_yearly_returns.min())

    # Reconstructing the portfolio price series by summing weighted stock prices,
    # Portfolio CAGR computed using the same method as for individual stocks
    portfolio_prices = (prices * weights).sum(axis=1)  
    days_portfolio = (portfolio_prices.index[-1] - portfolio_prices.index[0]).days
    portfolio_cagr = float((portfolio_prices.iloc[-1] / portfolio_prices.iloc[0]) ** (365 / days_portfolio) - 1)
    
    # Portfolio volatility: accounts for the correlation between stocks using the covariance matrix to account for diversification
    covariance_matrix = daily_returns_stocks.cov() * 252
    portfolio_volatility = float(np.sqrt(weights @ covariance_matrix @ weights))

    # Portfolio beta calculated as the weighted average of individual stock betas
    portfolio_beta = np.dot(weights, beta_stocks)

    # Sharpe ratio (excess return per unit of risk)
    sharpe_ratio = float((avg_annual_return_portfolio - risk_free_rate) / portfolio_volatility)

    # Diversification score: 1 - weighted average pairwise correlation
    # A score close to 1 means stocks are uncorrelated (well diversified), while a score close to 0 means they are highly correlated (poorly diversified)
    
    # Converting the correlation matrix from pandas DataFrames to NumPy arrays to be able to properly loop below in the pairwise calculation
    correlation_matrix = daily_returns_stocks.corr().to_numpy()
    n = len(tickers)
    weighted_avg_corr = 0
    total_weight_pairs = 0

    for i in range(n):
        for j in range(n):
            # Excluding self-correlation (always 1)
            if i != j:
                pair_weight        = weights[i] * weights[j]
                weighted_avg_corr  += pair_weight * correlation_matrix[i, j]
                total_weight_pairs += pair_weight

    diversification_score = 1 - (weighted_avg_corr / total_weight_pairs)

    # Returning all computed metrics in a summary table
    df_portfolio_metrics = pd.DataFrame([{
        "Total weight (%)": (sum(weights) * 100),
        "Period": period,
        "Expected return (%)": (avg_annual_return_portfolio * 100),
        "Best year (%)": (best_year_portfolio * 100),
        "Worst year (%)": (worst_year_portfolio * 100),
        "Annual portfolio volatility (%)": (portfolio_volatility * 100),
        "CAGR (%)": (portfolio_cagr * 100),
        "Portfolio beta": portfolio_beta,
        "Sharpe ratio": sharpe_ratio, 
        "Diversification score": diversification_score
    }])

    return df_portfolio_metrics, risk_free_rate, avg_annual_return_portfolio, portfolio_beta, portfolio_prices

# Computing the same set of metrics for the benchmark as for the portfolio to compare them
def get_benchmark_metrics(risk_free_rate, period, benchmark_price, benchmark_name):

    # Convert the DataFrame into a series to compute daily returns
    benchmark_price_s = benchmark_price.squeeze()
    daily_returns_benchmark = benchmark_price_s.pct_change().dropna()

    # Annual benchmark volatility
    annual_benchmark_volatility = float(daily_returns_benchmark.std() * np.sqrt(252))

    # Benchmark CAGR
    days_benchmark = (benchmark_price_s.index[-1] - benchmark_price_s.index[0]).days 
    cagr_benchmark = float((benchmark_price_s.iloc[-1] / benchmark_price_s.iloc[0]) ** (365 / days_benchmark) -1)

    # Benchmark yearly returns on average over the period, including the best and worst year
    yearly_benchmark_returns = daily_returns_benchmark.resample("Y").apply(lambda x: (1 + x).prod() - 1)
    benchmark_avg   = float(yearly_benchmark_returns.mean())
    benchmark_best  = float(yearly_benchmark_returns.max())
    benchmark_worst = float(yearly_benchmark_returns.min())

    benchmark_sharpe = float((benchmark_avg - risk_free_rate) / annual_benchmark_volatility)

    # Displaying benchmark results in a table
    # By definition, the benchmark has no portfolio weight and a beta of 1 
    benchmark_row = pd.DataFrame([{
        "Ticker": benchmark_name,
        "Weight": None,                                        
        "Period": period,
        "Expected benchmark return (%)": (benchmark_avg * 100),
        "Best year (%)": (benchmark_best * 100),
        "Worst year (%)": (benchmark_worst * 100),
        "Annual volatility (%)": (annual_benchmark_volatility * 100),
        "CAGR (%)": (cagr_benchmark * 100),
        "Beta": 1.0,
        "Sharpe ratio": benchmark_sharpe, 
    }])

    return benchmark_row, yearly_benchmark_returns, benchmark_avg

# CAPM computation
def get_capm(portfolio, daily_returns_stocks, yearly_stock_returns, avg_annual_stock_return, annual_stock_volatility, beta_stocks, risk_free_rate, benchmark_name, yearly_benchmark_returns, benchmark_avg, avg_annual_return_portfolio, portfolio_beta, weights, tickers):
    
    #Stock CAPM calculation
    stock_capm_returns = []
    for beta in beta_stocks:
        capm = risk_free_rate + beta * (benchmark_avg - risk_free_rate)
        stock_capm_returns.append(capm)

    # Stock alpha calculation
    stock_alphas = []
    avg_returns = np.array(avg_annual_stock_return)
    for avg, capm in zip(avg_returns, stock_capm_returns):
        alpha = float(avg - capm)
        stock_alphas.append(alpha)

    # Portfolio CAPM and alpha calculation
    portfolio_capm_return = risk_free_rate + portfolio_beta * (benchmark_avg - risk_free_rate)
    portfolio_alpha = avg_annual_return_portfolio - portfolio_capm_return

    # Displaying CAPM results for each stock and the portfolio in separate tables
    capm_stock_df = pd.DataFrame({
        "Ticker": tickers,
        "Beta": beta_stocks,
        "CAPM return (%)": np.array(stock_capm_returns) * 100,
        "Actual return (%)": np.array(avg_annual_stock_return) * 100,
        "Alpha (%)": np.array(stock_alphas) * 100,
    })
    
    #Setting the index to start the table at row 1 instead of 0
    capm_stock_df.index = capm_stock_df.index + 1
    
    capm_portfolio_df = pd.DataFrame([{
        "Portfolio beta": portfolio_beta,
        "CAPM return (%)": (portfolio_capm_return * 100),
        "Actual return (%)": (avg_annual_return_portfolio * 100),
        "Alpha (%)": (portfolio_alpha * 100),
        }])

    return capm_stock_df, capm_portfolio_df, stock_capm_returns, stock_alphas, portfolio_capm_return, portfolio_alpha

# Secuirty Market Line calculation and graph creation 
def get_sml(benchmark_avg, beta_stocks, risk_free_rate, portfolio_beta, avg_annual_return_portfolio, portfolio_alpha, benchmark_name):

    # SML returns alongside a range of beta values
    beta_range   = np.linspace(-2, max(beta_stocks) + 0.5, 200)
    sml_returns  = risk_free_rate + beta_range * (benchmark_avg - risk_free_rate)

    # Graph creation
    fig, ax = plt.subplots(figsize=(12, 7)) 
    ax.plot(beta_range, sml_returns, color="black", linewidth=2, label="Security Market Line")

    # Portfolio dot: plotting the portfolio's actual return relative to the SML
    ax.scatter(portfolio_beta, avg_annual_return_portfolio, color="red", s=100, zorder=6, label="Portfolio", marker="o")
    ax.annotate(f"Portfolio\nα={portfolio_alpha * 100:.2f}%", (portfolio_beta, avg_annual_return_portfolio), textcoords="offset points", xytext=(10, -10), fontsize=8, color="red")

    # Plotting the risk-free rate point on the graph with a beta of 0
    ax.scatter(0, risk_free_rate, color="steelblue", s=100, zorder=6, label="Risk-free rate", marker="o")
    ax.annotate(f"Risk-free rate\nrf={risk_free_rate * 100:.2f}%", (0, risk_free_rate), textcoords="offset points", xytext=(-10, 10), fontsize=8, color="steelblue")

    ax.set_xlabel("Beta", fontsize=12)
    ax.set_ylabel("Expected Return", fontsize=12)
    ax.set_title(f"Security Market Line — {benchmark_name}", fontsize=14, fontweight="bold")
    ax.axhline(0, color="black", linewidth=0.5, linestyle="-")
    ax.legend(fontsize=8, loc="best")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.2%}"))
    plt.tight_layout()
    plt.show()
    plt.close(fig)

# ---------------------------- 1-YEAR FORECAST CALCULATIONS ----------------------------
# 1-year (252 trading days)
#U sing a weighted blend (50/50) of:
# - Exponential moving average: historical returns with exponentially decaying weights, placing more weight on the most recent 126 days (6 months) to capture recent market trends
# - Historical moving average: average daily returns over the historical period
# This combination captures recent market trends while filtering out short-term noise
# Additionally, an uncertainty range is computed using the standard deviation 

def get_ema_forecast(prices, portfolio, portfolio_prices, benchmark_price, benchmark_name, forecast_days=252):

    # Normalizing both portfolio and benchmark series to 100 for direct comparison on the same scale
    portfolio_normalized = portfolio_prices / portfolio_prices.iloc[0] * 100
    benchmark_normalized = benchmark_price.squeeze() / benchmark_price.squeeze().iloc[0] * 100

    # Daily returns of the normalized portfolio and benchmark
    portfolio_norm_daily_returns = portfolio_normalized.pct_change().dropna()
    benchmark_norm_daily_returns = benchmark_normalized.pct_change().dropna()

    # Historical daily mean and volatility computed over the full period for both portfolio and benchmark
    portfolio_longrun_drift = float(portfolio_norm_daily_returns.mean())
    benchmark_longrun_drift = float(benchmark_norm_daily_returns.mean())

    portfolio_longrun_volatility = float(portfolio_norm_daily_returns.std())
    benchmark_longrun_volatility = float(benchmark_norm_daily_returns.std())

    # EMA: smoothed average daily returns and volatility for both the portfolio and benchmark
    # Emphasis on the last 126 trading days, as it is long enough to smooth out recent noise but short enough to account for changing trends
    portfolio_ema_drift = float(portfolio_norm_daily_returns.ewm(span=126).mean().iloc[-1])
    portfolio_ema_volatility = float(portfolio_norm_daily_returns.ewm(span=126).std().iloc[-1])

    benchmark_ema_drift = float(benchmark_norm_daily_returns.ewm(span=126).mean().iloc[-1])
    benchmark_ema_volatility = float(benchmark_norm_daily_returns.ewm(span=126).std().iloc[-1])

    # Blended return and volatility combining historical and EMA-based estimates for the portfolio and benchmark
    # A 50/50 weight is used to balance short-term momentum captured by the EMA with long-term past returns, reducing sensitivity to recent noise
    portfolio_blend_drift = 0.5 * portfolio_ema_drift + 0.5 * portfolio_longrun_drift
    benchmark_blend_drift = 0.5 * benchmark_ema_drift + 0.5 * benchmark_longrun_drift

    portfolio_blend_volatility = 0.5 * portfolio_ema_volatility + 0.5 * portfolio_longrun_volatility
    benchmark_blend_volatility = 0.5 * benchmark_ema_volatility + 0.5 * benchmark_longrun_volatility

    # Extracting last known values before the forecast for the portfolio and benchmark
    last_portfolio_price = float(portfolio_normalized.iloc[-1])
    last_benchmark_price = float(benchmark_normalized.iloc[-1])

    # Generating future business dates using trading days only
    last_date = portfolio_normalized.index[-1]
    future_dates = pd.bdate_range(start=last_date, periods=forecast_days + 1)[1:]

    # Projecting future prices by compounding the blended daily drift forward over t days for the portfolio and the benchmark
    portfolio_forecast = []
    for t in range (1, forecast_days + 1):
        projected_portfolio = last_portfolio_price * (1 + portfolio_blend_drift) ** t 
        portfolio_forecast.append(projected_portfolio)

    benchmark_forecast = []
    for t in range (1, forecast_days + 1):
        projected_benchmark = last_benchmark_price * (1 + benchmark_blend_drift) ** t
        benchmark_forecast.append(projected_benchmark)

    # Standard deviation range scaled with √t (random-walk assumption) so that the uncertainty widens proportionally to the square root of time
    portfolio_upper = []
    for t in range (1, forecast_days + 1):
        p_up_std = last_portfolio_price * (1 + portfolio_blend_drift) ** t * np.exp(portfolio_blend_volatility * np.sqrt(t))
        portfolio_upper.append(p_up_std)

    portfolio_lower = []
    for t in range (1, forecast_days + 1):
        p_low_std = last_portfolio_price * (1 + portfolio_blend_drift) ** t * np.exp(-portfolio_blend_volatility * np.sqrt(t))
        portfolio_lower.append(p_low_std)

    benchmark_upper = []
    for t in range (1, forecast_days + 1):
        b_up_std = last_benchmark_price * (1 + benchmark_blend_drift) ** t * np.exp(benchmark_blend_volatility * np.sqrt(t))
        benchmark_upper.append(b_up_std)

    benchmark_lower = []
    for t in range (1, forecast_days + 1):
        b_low_std = last_benchmark_price * (1 + benchmark_blend_drift) ** t * np.exp(-benchmark_blend_volatility * np.sqrt(t))
        benchmark_lower.append(b_low_std)

    # Creating the graph
    fig, ax = plt.subplots(figsize=(14, 7))

    # Adding historical returns of the portfolio and benchmark
    ax.plot(portfolio_normalized.iloc[-252:], color="steelblue", linewidth=1.5, label="Portfolio past returns")
    ax.plot(benchmark_normalized.iloc[-252:], color= "dimgray", linewidth=1.5, label=f"{benchmark_name} past returns")

    # Adding forecasted blended returns of the protfolio and benchamrk
    ax.plot(future_dates, portfolio_forecast, color="steelblue", linewidth=1.5, label="Portfolio forecast")
    ax.plot(future_dates, benchmark_forecast, color="dimgray", linewidth=1.5, label=f"{benchmark_name} forecast")

    # Adding uncertainty bands
    ax.fill_between(future_dates, portfolio_lower,  portfolio_upper,  color="steelblue", alpha=0.12, label="Portfolio ±1σ range")
    ax.fill_between(future_dates, benchmark_lower, benchmark_upper, color="dimgray", alpha=0.12, label=f"{benchmark_name} ±1σ range")
    
    ax.axvline(last_date, color="black", linewidth=1)
    ax.set_title(f"1-Year EMA Forecast — Portfolio vs {benchmark_name}", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Normalised Price (base = 100)", fontsize=12)
    ax.legend(fontsize=10, loc="best")
    plt.tight_layout()
    plt.show()
    plt.close(fig)

    # Summary table showing the projected 1Y return in percentage, the projected end price, and the annualized forecasted volatility in percentage for the benchmark and the portfolio
    portfolio_end_base = float(portfolio_forecast[-1])
    benchmark_end_base =float(benchmark_forecast[-1])

    portfolio_forecasted_return = (portfolio_end_base / last_portfolio_price) -1 
    benchmark_forecasted_return = (benchmark_end_base / last_benchmark_price) -1 

    portfolio_end_price = float(portfolio_normalized.squeeze().iloc[-1]) * (1 + portfolio_forecasted_return)
    benchmark_end_price = float(benchmark_normalized.squeeze().iloc[-1]) * (1 + benchmark_forecasted_return)

    portfolio_annualized_volatility = portfolio_blend_volatility * np.sqrt(252)
    benchmark_annualized_volatility = benchmark_blend_volatility * np.sqrt(252)

    df_forecast_summary = pd.DataFrame([{
        "Series": "Portfolio",
        "Projected 1Y return (%)": (portfolio_forecasted_return * 100),
        "Projected end price": portfolio_end_price,
        "Annualized forecast volatility (%)": (portfolio_annualized_volatility * 100),
        },
        {
            "Series": benchmark_name,
            "Projected 1Y return (%)": (benchmark_forecasted_return * 100),
            "Projected end price": benchmark_end_price,
            "Annualized forecast volatility (%)": (benchmark_annualized_volatility * 100)
        }])

    return df_forecast_summary

#---------------------------- EXECUTION OF THE CODE ----------------------------

# Welcome message for the user and a brief description of what the program does
user_greeting = input("What is your name?")
print(f"""\nWelcome {user_greeting}!\nThis program lets you:
  - Build a custom stock portfolio with your chosen weights and time period
  - Analyse returns, volatility, CAGR, beta, and Sharpe ratio over any time period
  - Visualise portfolio diversification through a correlation heatmap
  - Benchmark your portfolio against the S&P 500, Nasdaq, or Dow Jones
  - Evaluate each stock's as well as the portfolio's alpha via CAPM and the Security Market Line
  - Forecast your portfolio's 1-year expected return using a mix of EMA and historical returns
""")

# Collecting user preferences regarding portfolio composition, time period, and benchmark
portfolio = create_portfolio()
period = get_period_from_user() 
benchmark_name, benchmark_price = get_benchmark_choice(period)

# Computing stock, portfolio, and benchmark metrics
df_stock_metrics, daily_returns_stocks, yearly_stock_returns, avg_annual_stock_return, annual_stock_volatility, beta_stocks, prices, tickers, weights = get_stock_metrics(portfolio, period, benchmark_price)

raw_rfr, risk_free_rate =get_rfr_ticker(period)
df_portfolio_metrics, risk_free_rate, avg_annual_return_portfolio, portfolio_beta, portfolio_prices = get_portfolio_metrics(portfolio, daily_returns_stocks, yearly_stock_returns, avg_annual_stock_return, annual_stock_volatility, beta_stocks, prices, period, raw_rfr, risk_free_rate, tickers, weights)

benchmark_row, yearly_benchmark_returns, benchmark_avg = get_benchmark_metrics(risk_free_rate, period, benchmark_price, benchmark_name)

# Printing stocks, portfolio, and benchmark overview, along with the correlation heatmap
print("\nPortfolio Stocks Metrics Overview:\n", df_stock_metrics.round(3).to_string(), "\n\n")

get_corr_heatmap(daily_returns_stocks)

print("\n\nPortfolio Metrics Overview:\n", df_portfolio_metrics.round(3).to_string(index=False))
print("\n\nBenchmark Metrics Overview:\n", benchmark_row.round(3).to_string(index = False))

# Displaying CAPM tables and SML graph
capm_stock_df, capm_portfolio_df, stock_capm_returns, stock_alphas, portfolio_capm_return, portfolio_alpha = get_capm(portfolio, daily_returns_stocks, yearly_stock_returns, avg_annual_stock_return, annual_stock_volatility, beta_stocks, risk_free_rate, benchmark_name, yearly_benchmark_returns, benchmark_avg, avg_annual_return_portfolio, portfolio_beta, weights, tickers)

print("\n\nIndividual Portfolio Stocks CAPM Results Overview:\n", capm_stock_df.round(3).to_string())
print("\n\nPortfolio CAPM Results Overview:\n", capm_portfolio_df.round(3).to_string(index=False),"\n\n")

get_sml(benchmark_avg, beta_stocks, risk_free_rate, portfolio_beta, avg_annual_return_portfolio, portfolio_alpha, benchmark_name)

# Generation and representation of the 1-year blended forecast graph and summary table 
df_forecast_summary = get_ema_forecast(prices, portfolio, portfolio_prices, benchmark_price, benchmark_name, forecast_days=252)

print("\n1-Year Forecast Summary Table:\n", df_forecast_summary.round(3).to_string(index=False))
