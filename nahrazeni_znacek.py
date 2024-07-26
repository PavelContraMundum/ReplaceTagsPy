import codecs
import re
import os
from collections import Counter

def get_file_path(prompt):
    return input(prompt).strip()

def detect_encoding(file_path):
    encodings_to_try = ['utf-8', 'windows-1250', 'iso-8859-2', 'cp852', 'windows-1252']
    
    for encoding in encodings_to_try:
        try:
            with codecs.open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
                
            # Kontrola platnosti českých znaků
            czech_chars = set('ěščřžýáíéůúňťďóĚŠČŘŽÝÁÍÉŮÚŇŤĎÓ')
            char_count = Counter(content)
            czech_char_ratio = sum(char_count[c] for c in czech_chars) / len(content)
            
            # Pokud je dostatek českých znaků, považujeme kódování za správné
            if czech_char_ratio > 0.01:  # 1% českých znaků
                return encoding
        except UnicodeDecodeError:
            continue
    
    return None

def main():
    input_file_path = get_file_path("Zadejte cestu k vstupnímu souboru: ")
    output_file_path = get_file_path("Zadejte cestu k výslednému souboru: ")

    try:
        detected_encoding = detect_encoding(input_file_path)

        if detected_encoding is None:
            print("Nepodařilo se detekovat správné kódování. Zkontrolujte vstupní soubor.")
            return

        print(f"Detekované kódování: {detected_encoding}")

        with codecs.open(input_file_path, 'r', encoding=detected_encoding) as file:
            content = file.read()

        # Úpravy obsahu
        content = re.sub(r'<italic>', r'\\it', content)
        content = re.sub(r'</italic>', r'\\it*', content)
        content = re.sub(r'<p/>', r'\\p', content)
        content = re.sub(r'<kap/>', r'\\cl_', content)
        content = re.sub(r'<vers n="(\d+)"/>', r'\\v_\1_', content)
        content = re.sub(r'<kap n="(\d+)"/>', r'\\cl_\1', content)

        # Zápis souboru v UTF-8
        with codecs.open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Úpravy byly úspěšně provedeny. Výstup byl uložen do: {output_file_path} v kódování UTF-8")

        # Kontrolní vypís části obsahu
        print("Prvních 100 znaků výstupního souboru:")
        print(content[:100])

    except Exception as ex:
        print(f"Došlo k chybě: {str(ex)}")

if __name__ == "__main__":
    main()