# frozen_string_literal: true

# Class for the mastermind game
class Mastermind
  def initialize
    @code = 4.times.map { rand(1...6) }
    @player_guess = ' '
    @turn_number = 0
    @win = false

    puts 'Hello, Player. Can you decode my super duper secret?'

    until game_over?
      player_guess
      verify_guess
      @turn_number += 1
    end

    show_code
  end

  def verify_guess
    correct_guess = @code.each_with_index.count { |num, index| 1 if num == @player_guess[index] }
    @win = correct_guess == 4
    puts "You got #{correct_guess} right"

    semi_correct_guess = scg - correct_guess
    puts "You got #{semi_correct_guess} almost right (right number, but wrong position)"
  end

  def scg
    counter = 0
    @code.each do |num| 
      if @player_guess.include?(num)
        @player_guess.delete_at(@player_guess.index(num))
        counter += 1
      end
    end
    counter
  end

  def game_over?
    if @turn_number >= 10
      puts 'This was the last try. Sorry =('
      true
    end
    puts 'You WIN' if @win
    @win
  end

  def player_guess
    valid_move = false
    until valid_move
      puts 'Try 4 numbers between 1 and 6 separated by a space'
      @player_guess = gets.chomp.split.map(&:to_i)
      valid_move = @player_guess.all? { |num| num.between?(1, 6) }
      puts 'Invalid Move. Try again' unless valid_move
    end
  end

  def show_code
    puts "The code was #{@code}"
  end
end

Mastermind.new
