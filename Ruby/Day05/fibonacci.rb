# frozen_string_literal: true

# Classe de Fibonacci
class Fibonacci
  attr_reader :result

  def initialize(number)
    @result = [0]
    @result.push(1) unless number == 1
    generate(number) unless number < 2
  end

  def generate(number)
    length = @result.length
    soma = @result[length - 1] + @result[length - 2]
    @result.push(soma)
    generate(number) unless number <= length + 1
  end
end

fib = Fibonacci.new(8)

puts(fib.result)
