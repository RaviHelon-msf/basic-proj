# frozen_string_literal: true

# Classe ConnectFour
class ConnectFour
  attr_reader :board

  def initialize
    @player_one_token = 'W'
    @player_two_token = 'S'
    @turn_player_one = false
    @board = Array.new(7) { Array.new(6, ' ') }
    @gamestate = ''
  end

  def start
    until gameover?
      @turn_player_one = !@turn_player_one
      display
      make_play
    end

    puts @turn_player_one ? 'Player One' : 'Player Two'
  end

  def gameover?
    true unless @gamestate != 'Victory'
  end

  def display
    puts '  1   2   3   4   5   6   7'
    puts '+---+---+---+---+---+---+---+'
    5.downto(0) do |row|
      print '|'
      7.times do |col|
        print " #{@board[col][row]} |"
      end
      puts ' '
      puts '+---+---+---+---+---+---+---+'
    end
  end

  def make_play
    valid = false
    until valid
      puts 'Where do you want to place your tile?'
      user_input = gets.chomp.to_i
      next unless user_input.between?(1, 7)

      @gamestate = input(user_input)
      valid = true unless @gamestate == 'error'
      puts @gamestate
    end
  end

  def input(column)
    return 'error' unless board[column - 1][5] == ' '

    row = @board[column - 1].index(' ') # Find the first empty slot in the column
    @board[column - 1][row] = @turn_player_one ? @player_one_token : @player_two_token
    check_win?(column - 1, row) ? 'Victory' : 'Nice Play'
  end

  def check_win?(column, row)
    current_token = @board[column][row]
    return true if check_consecutive_tokens(@board[column], current_token)

    return true if check_consecutive_tokens(@board.transpose[row], current_token)

    return true if check_diagonal_win?(column, row, current_token)

    false
  end

  private

  def check_consecutive_tokens(tokens, target_token)
    consecutive_tokens = 0

    tokens.each do |token|
      if token == target_token
        consecutive_tokens += 1
        return true if consecutive_tokens == 4
      else
        consecutive_tokens = 0
      end
    end
    false
  end

  def check_diagonal_win?(column, row, target_token)
    return true if check_consecutive_tokens(tokens_from_bottom_left(column, row), target_token)

    return true if check_consecutive_tokens(tokens_from_top_left(column, row), target_token)

    false
  end

  def tokens_from_bottom_left(column, row)
    tokens = []
    while column < @board.length && row >= 0
      tokens << @board[column][row]
      column += 1
      row -= 1
    end
    tokens
  end

  def tokens_from_top_left(column, row)
    tokens = []
    while column < @board.length && row < @board[column].length
      tokens << @board[column][row]
      column += 1
      row += 1
    end
    tokens
  end
end

if __FILE__ == $PROGRAM_NAME
  game = ConnectFour.new

  game.start
end
