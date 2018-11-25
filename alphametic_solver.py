from pyeasyga import pyeasyga

def parse_individual():
    input_data = "SEND+MORE=MONEY"
    raw_arguments, result = input_data.split("=")
    arguments = raw_arguments.split("+")

    st = ""
    chars = list(st.join(arguments))
    chars.extend(list(result))
    genetic_code = []
    
    for char in chars:
        if char not in genetic_code:
            genetic_code.append(char)

    #print(genetic_code)
    return genetic_code
