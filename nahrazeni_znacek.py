import re
import os

input_file_path = r"D:\Downloads\GenModified.txt"
output_file_path = r"D:\Downloads\GenModifiedFormatted.txt"

try:
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Nahrazení tagů
    content = re.sub(r'<italic>', r'\\it', content)
    content = re.sub(r'</italic>', r'\\it*', content)
    content = re.sub(r'<p/>', r'\\p', content)
    content = re.sub(r'<kap/>', r'\\cl_', content)

    # Nahrazení tagu verše
    content = re.sub(r'<vers n="(\d+)"/>', r'\\v_\1_', content)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"Úpravy byly úspěšně provedeny. Výstup byl uložen do: {output_file_path}")

except Exception as ex:
    print(f"Došlo k chybě: {str(ex)}")