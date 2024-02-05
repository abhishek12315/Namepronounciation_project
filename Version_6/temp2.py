def insert_newline(sentence, max_length=21):
    words = sentence.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_length:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    # Add the last line
    lines.append(current_line.strip())

    return lines

# Example usage
input_sentence = "This is a sample sentence that needs to be formatted with new lines if it exceeds a certain length."
formatted_lines = insert_newline(input_sentence)
print(formatted_lines)
