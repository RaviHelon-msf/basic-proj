# frozen_string_literal: true

require './app/connect_four'

RSpec.describe ConnectFour do
  let(:game) { ConnectFour.new }

  describe '#board' do
    it 'has the correct dimensions' do
      expect(game.board.length).to eql(7)
      expect(game.board[0].length).to eql(6)
    end
  end

  describe '#input' do
    it 'places tokens on the board' do
      game.input(1)
      expect(game.board[0][0]).to eql('W').or eql('S')
    end

    it 'handles column overflow' do
      6.times { game.input(1) }
      expect(game.input(1)).to eql('error')
    end

    it 'handles multiple plays and declares victory' do
      [1, 2, 3].each { |column| game.input(column) }

      expect(game.input(4)).to eql('Victory')
    end
  end
end
