import os
import ftfy

def fix_encoding(text):
    return ftfy.fix_text(text)

# Function to remove trailing spaces from HTML content
def trim_trailing_spaces_html(content):
    # Split the content into lines, strip trailing spaces from each line, and rejoin them
    return "\n".join([line.rstrip() for line in content.splitlines()])

def fix_html_encoding(input_file, filename):
    try:
        # Read the HTML file content
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Fix encoding in the HTML content
        fixed_content = fix_encoding(content)

        # Remove trailing spaces from each line in the HTML content
        fixed_content = trim_trailing_spaces_html(fixed_content)

        # Write the corrected HTML to a new file
        with open(fr"C:\Scripts\hondurus\UPDATED_HTML\{filename}", 'w', encoding='utf-8') as file:
            file.write(fixed_content)

        print(f"Fixed HTML has been written to {filename}")
    except Exception as e:
        print(f"Error processing {filename}: {e}")

def process_html_files(directory_path):
    # Loop through all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith(".html"):
            file_path = os.path.join(directory_path, filename)
            print(f"Processing {file_path}...")
            fix_html_encoding(file_path, filename)

# Example usage: specify the directory containing your HTML files
directory = "C:\\Scripts\\hondurus\\html\\"
process_html_files(directory)
