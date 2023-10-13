import re 
files = ['Banner.tsx']

var1 = 'w-\[?\d*p?x?r?e?m?\]?'
var2 = 'w-[]'

pattern = fr"(class=\".*)({var1})"
replacement_text = fr"\1{var2} md:\2"
# Open a file in read mode


for file_path in files:
    with open(file_path, "r+") as file:
            full_file = file.readlines()
        # Read the entire contents of the file into a string
            for id, line in enumerate(full_file):
                res = re.findall(pattern,line)
                if len(res) > 0:
                    modified_line = re.sub(pattern, replacement_text, line)
                    line = modified_line
                full_file[id] = line
    with open(file_path, "w") as file:
            file.writelines(full_file)
                