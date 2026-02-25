from backtesting import Backtesting

if __name__ == '__main__':
    backtester = Backtesting()
    backtester.run()

    end_val = backtester.portfolio.value
    print(end_val)
    print((end_val/10000 - 1)*100)
    print(backtester.portfolio.cash)