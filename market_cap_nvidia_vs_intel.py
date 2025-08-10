import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Update tickers and time period for NVIDIA and Intel
new_tickers = ["NVDA", "INTC"]
new_start_date = "2010-01-01"
new_end_date = "2024-01-01"

# Redefine tickers and time period
tickers = new_tickers
start_date = new_start_date
end_date = new_end_date

# Clear previous data
data = {}
shares_outstanding = {}

# Download historical data
for ticker in tickers:
    ticker_obj = yf.Ticker(ticker)
    hist = ticker_obj.history(start=start_date, end=end_date)
    so = ticker_obj.info.get("sharesOutstanding")
    if hist.empty or so is None:
        print(f"Missing data for {ticker}, check availability.")
        continue
    hist["Market Cap"] = hist["Close"] * so
    data[ticker] = hist["Market Cap"].resample("M").mean()

# Plotting
# Adjust figure size for half an A4 page
plt.figure(
    figsize=(8.27, 5.85)
)  # A4 dimensions in inches: 8.27 x 11.69, half page height

for ticker in data:
    plt.plot(data[ticker].index, data[ticker] / 1e9, label=ticker, linewidth=2)

# Update font sizes for better readability
# plt.title("Market Capitalization (2010–2015): NVIDIA vs Intel", fontsize=16)
plt.xlabel("Date", fontsize=14)
plt.ylabel("Market Capitalization (Billion USD)", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize=12, loc="upper left")

# Improve grid visibility
plt.grid(True, linestyle="--", alpha=0.8)

# Tighten layout for better fit
plt.tight_layout(pad=2.0)

# Save figure
plt.savefig("nvidia_intel_market_cap_2010_2015.png", dpi=300)
plt.show()
