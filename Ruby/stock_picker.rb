def stock_picker(market = [1, 2, 313, 13, 1515, 1])
    max_profit = 0
    buy_day, sell_day = 0, 0
  
    market.each_with_index do |buy_price, buy_index|
      market[buy_index + 1..-1].each_with_index do |sell_price, sell_index|
        profit = sell_price - buy_price
        if profit > max_profit
          max_profit = profit
          buy_day = buy_index
          sell_day = buy_index + sell_index + 1
        end
      end
    end
  
    [buy_day, sell_day]
  end
  
  # Example usage:
  market = [1, 2, 313, 13, 1515, 1]
  result = stock_picker(market)
  puts "Buy on day #{result[0]}, sell on day #{result[1]} for maximum profit."
  