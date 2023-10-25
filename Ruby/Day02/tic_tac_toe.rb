# frozen_string_literal:true

# Classe que define o jogo de Tic Tac Toe
class TicTacToe
  def initialize
    @state = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    @player_mark = ['X', 'O']
    @current_player = 0
    @winner = 'No one'
    @player_name = ['', '']
    name_players
    puts 'Write a play as the row number followed by the column number (e.g., 1 2 for the second row, third column).'
    until game_over?
      @current_player = @current_player == 1 ? 0 : 1
      make_move
      display
    end
    puts "Aaand the winner is #{@winner}"
  end

  def name_players
    puts 'Enter Player 1\'s name:'
    @player_name[0] = gets.chomp
    puts 'Enter Player 2\'s name:'
    @player_name[1] = gets.chomp
  end

  def display
    puts "#{@player_name[0]} (X) vs #{@player_name[1]} (O)"
    puts ' '
    puts '  1   2   3'
    puts "1 #{@state[0].join(' | ')}"
    puts '  ---+---+---'
    puts "2 #{@state[1].join(' | ')}"
    puts '  ---+---+---'
    puts "3 #{@state[2].join(' | ')}"
  end

  def make_move
    valid_move = false
    until valid_move
      print "#{@player_name[@current_player]}'s turn: "
      move = gets.chomp
      row, col = move.split.map(&:to_i)
      if valid?(row, col)
        @state[row - 1][col - 1] = @player_mark[@current_player]
        valid_move = true
      else
        puts 'Invalid move. Try again.'
      end
    end
  end

  def valid?(row, col)
    row.between?(1, 3) && col.between?(1, 3) && @state[row - 1][col - 1] == ' '
  end

  def game_over?
    check_row
    check_column
    check_diag_princ
    check_diag_sec
    (!@state.flatten.include?(' ') or @winner != 'No one')
  end

  def check_diag_princ
    if [@state[0][0], @state[1][1], @state[2][2]].uniq.length == 1 && @state[0][0] == @player_mark[@current_player]
      @winner = @player_name[@current_player]
    end
  end

  def check_diag_sec
    if [@state[0][2], @state[1][1], @state[2][1]].uniq.length == 1 && @state[0][2] == @player_mark[@current_player]
      @winner = @player_name[@current_player]
    end
  end

  def check_column
    @state.transpose.each do |row|
      @winner = @player_name[@current_player] if row.uniq.length == 1 && row[0] == @player_mark[@current_player]
    end
  end

  def check_row
    @state.each do |row|
      @winner = @player_name[@current_player] if row.uniq.length == 1 && row[0] == @player_mark[@current_player]
    end
  end
end

TicTacToe.new
