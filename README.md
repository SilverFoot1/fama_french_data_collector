<h2>Fama & French 3-Factor Model Script</h2>
https://www.youtube.com/watch?v=pYTraS5WR3s (5 min video to explain FF 3-Factor Model)
<h3>Introduction</h3>
<p>This is a script that collects stock data and does the calculations to get the risk factors used for a three-factor regression. These factors are market risk, the 'High minus Low' (HML) and 'Small minus Big' (SMB) factors. HML refers to the difference in returns between high market cap and low market cap stocks. SMB refers to the difference in returns between high book-to-market ratio stocks, and low book-to-market stocks</p>
<p><b>Disclaimer:</b> This script only works for stocks on the New Zealand stock exchange. I have implemented the financial concepts to the best of my knowledge (Im no financial expert), but there may be some imperfections im unaware of. If someone actually uses this, invest at your own risk. Note that the CRON job would need to be scheduled some time after the market closes, and before it opens, and not over the weekend when the exchange is closed.</p>
<p>The idea is that this script can be run daily inorder to calculate these values, and then can be used in a simple linear regression to explain the returns of an equity or portfolio. This does NOT help PREDICT returns, rather retro-actively EXPLAINS returns statistically, in regard to these three factors. This is particuarly useful for helping choose a manged fund for something like Kiwisaver.</p> 
<p>This could be run via CRON tab or Task Scheduler</p>
<p>The final row produced has: Date, Excess Market Return(MKT_RF), SMB, HML, Risk-Free-Rate(RFR) and then a JSON object with all the daily returns of equities as percentages. An example row is found in the 'Images' folder.</p>

<h3>Code Overview</h3>
The basic flow is:
- NZX stock tickers are web scraped
- Data is collected for each of the stocks
- Data is cleaned & features created
- Stocks are split into 6 portfolios
- The factors are calculated from these portfolios
- Data is assembled into a single row
- Data is written to the DB/Excel
Data is also stored along the way and at the end in Excel files. 

<h3>Conceptual Explanation</h3>
All the code is documented but conceptually this is what it is doing. 
<p>For every stock in the NZX it gets specific values, notably, book value, market cap, current price, and previous close price. From the book price and actual price we calculate the book to market ratio</p>
<p>The stocks are then split into 6 portfolios based on their market cap and book values. First stocks are split into big and small, where the median market cap acts as the dividing line. Next, these two sets are split into high, neutral and low</p>
<p>High B/M indicates a value stock, where it is undervalued. Low indicates a growth stock, where the book value of the stock is lower than its actual price e.g. your Tesla or Apple stocks. Neutral consist of the middle 40% of stocks in terms of B/M. In 'Images' there is a picture that shows this</p>
<p>The third factor is the traditional market risk. This is the return of the market, minus the risk free rate. The NZX50 is used to represent the market return, and the 90-day bank bill rate for the risk free rate</p>
<p>Once enough data is gathered you can do a linear regression where MKT-RF, SMB and HML are your independent variables, and a stocks return minus the RFR over the same period is the dependent variable. We can then interpret the statistical ouputs to try explain why the equity has performed the way it did, based on its market risk, SMB risk and HML risk exposure.</p>
