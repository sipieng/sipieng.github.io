import re

def process_subtitle_file(filepath):
    """
    Processes a subtitle file by removing numbering and timestamps,
    and concatenating the remaining text into a single string.

    Args:
        filepath (str): The path to the subtitle file.

    Returns:
        str: A single string containing all the text from the subtitle file,
             with numbering and timestamps removed.
    """

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"Error: An error occurred while reading the file: {e}"

    text_lines = []
    for line in lines:
        # Remove numbering
        if re.match(r'^\d+$', line.strip()):
            continue
        # Remove timestamps
        if re.match(r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$', line.strip()):
            continue
        # Append the line to the list of text lines after removing leading/trailing whitespace
        text_lines.append(line.strip())

    # Concatenate the text lines into a single string, separated by a single space
    full_text = ' '.join(filter(None, text_lines))  # Use filter(None, ...) to remove empty strings

    return full_text

# Example usage:
filepath = 'transcr/beowulf.txt'  # Replace with your actual file path
processed_text = process_subtitle_file(filepath)

if processed_text.startswith("Error:"):
    print(processed_text)  # Print the error message
else:
    print(processed_text)

# OPTIONAL: Save the processed text to a new file.
    output_filepath = 'beowulf_merged.txt'
    with open(output_filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(processed_text)
    print(f"Processed text saved to: {output_filepath}")