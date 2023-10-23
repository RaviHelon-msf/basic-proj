def substrings (string = 'below how', dictionary= ['below', 'low', 'how'])
    result = {}
    words = string.split

    dictionary.each do |word|
        count = words.count {|str| str.include?(word)}
        result[word] = count if count > 0
    end

    result
end




puts substrings

dictionary = ["below","down","go","going","horn","how","howdy","it","i","low","own","part","partner","sit"]
puts substrings("below", dictionary)