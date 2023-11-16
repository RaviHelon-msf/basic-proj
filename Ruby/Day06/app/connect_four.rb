# frozen_string_literal: true

# Classa Calculadora
class ConnectFour
  attr_reader :board

  def initialize
    @player_one_token = '\u{1F534}'
    @player_two_token = '\u{1F534}'
    @turn_player_one = true
    @board = array(7, array(6))
  end

  def input(column)
    @board[column].puts(@turn_player_one ? @player_one_token : @player_two_token) unless board[column][6].zero?
  end
end
