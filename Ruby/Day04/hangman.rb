# frozen_string_literal: false

# Hangman Game Class
class Hangman
  def initialize
    @misses = ''
    game_start

    until game_over?
      display_hangman
      player_guess
    end

    puts "The word was #{@word}"
  end

  def game_start
    filename = 'dictionary.txt'
    file = File.readlines(filename) if File.exist? filename
    valid = false
    until valid
      @word = file[rand(file.length)][0..-2]
      valid = @word.length > 5 && @word.length < 12
    end
    @state = '_' * @word.length
  end

  def game_over?
    @misses.length >= 7 or !@state.include?('_')
  end

  def player_guess
    puts 'Guess a letter'
    valid = false
    until valid
      guess = gets.chomp
      valid = guess.length == 1 && guess.is_a?(String)
    end
    letter_check(guess)
  end

  def letter_check(guess)
    hits = 0
    @word.each_char.each_with_index do |letter, index|
      if guess == letter
        @state[index] = letter
        hits += 1
      end
    end
    puts "There is #{hits} #{guess} in the word"
    @misses << guess if hits.zero?
  end

  def display_hangman
    stages = [
      ['   +---+', '   |   |', '       |', '       |', '       |', '       |', '========='],
      ['   +---+', '   |   |', '   O   |', '       |', '       |', '       |', '========='],
      ['   +---+', '   |   |', '   O   |', '   |   |', '       |', '       |', '========='],
      ['   +---+', '   |   |', '   O   |', '  /|   |', '       |', '       |', '========='],
      ['   +---+', '   |   |', '   O   |', '  /|\\  |', '       |', '       |', '========='],
      ['   +---+', '   |   |', '   O   |', '  /|\\  |', '  /    |', '       |', '========='],
      ['   +---+', '   |   |', '   O   |', '  /|\\  |', '  / \\  |', '       |', '=========']
    ]
    puts stages[@misses.length]
    puts "Word: #{@state}"
    puts "Letters not present:#{@misses}"
  end
end

Hangman.new
