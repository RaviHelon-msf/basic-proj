# frozen_string_literal: true

require './app/connect_four'
# Assuming the ConnectFour class is defined in the 'connect_four.rb' file

describe ConnectFour do
  let(:game) { ConnectFour.new }

  describe '#play' do
    it 'checks board height' do
      expect(game.board.length).to eql(7)
      expect(game.board[0].length).to eql(6)

      game.input(1)
      expect(game.board[0][0]).to eql("\u{1F534}")

      game.input(1)
      expect(game.board[0][1]).to eql("\u{26AB}")

      4.times do
        game.input(0)
      end

      expect(game.input(0)).to eql('error')

      2.times do
        game.input(2)
        game.input(3)
      end

      expect(game.input(4)).to eql('Victory')
    end
  end
end
