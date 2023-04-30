def categorize(value):
    if 35 <= value <= 69:
        return "A"
    elif 70 <= value <= 140:
        return "B"
    elif 141 <= value <= 180:
        return "C"
    elif 181 <= value <= 200:
        return "D"
    else:
        return None


with open("input_glucose_target_label.txt", "r") as f_in, open("output_categorized_target_label.txt", "w") as f_out:
    for line in f_in:
        try:
            value = int(line.strip())
            category = categorize(value)
            if category is not None:
                f_out.write(category + "\n")
        except ValueError:
            pass
