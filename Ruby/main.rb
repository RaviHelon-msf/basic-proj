require 'pry-byebug'

def caesar_cypher(plain_text='aAZz', shift=1)
    plain_text.chars.map do |char|
      char == char.downcase ? ((char.ord - 97 + shift)%26+97).chr : ((char.ord - 65 + shift)%26+65).chr
    end.join
end

puts caesar_cypher('baBuinoz',10)