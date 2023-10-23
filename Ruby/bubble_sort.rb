def bubble_sort(array = [3,7,5,1])
    (array.length-1).times do |index|
        (array.length-1).times do |bubble|
            if array[bubble]>array[bubble+1]
                aux = array[bubble]
                array[bubble] = array[bubble+1]
                array[bubble+1] = aux
            end
        end
    end

    array
end

puts bubble_sort