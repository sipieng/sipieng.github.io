import re

def merge_subtitle_file(filepath):
    """
    移除srt字幕中的时间轴，并把内容合并为一整段
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



def remove_timestamps(filepath):
    """
    移除srt字幕中的时间轴，但不合并内容
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

    full_text = '\n'.join(filter(None, text_lines))  # Use filter(None, ...) to remove empty strings

    return full_text




if __name__ == "__main__":

    filepath = 'transcripts/brave_new_world_2.txt'
    processed_text = remove_timestamps(filepath)

    if processed_text.startswith("Error:"):
        print(processed_text)  # Print the error message
    else:
        print(processed_text)

    # OPTIONAL: Save the processed text to a new file.
        output_filepath = 'transcripts/brave2.md'
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            outfile.write(processed_text)
        print(f"Processed text saved to: {output_filepath}")