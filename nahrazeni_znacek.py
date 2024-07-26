import codecs
import re
import os

def get_file_path(prompt):
    return input(prompt).strip()

def main():
    input_file_path = get_file_path("Zadejte cestu k vstupnímu souboru: ")
    output_file_path = get_file_path("Zadejte cestu k výslednému souboru: ")

    try:
        # Zkusíme různá kódování
        encodings_to_try = ['windows-1250', 'iso-8859-2', 'cp852', 'utf-8', 'windows-1252']

        content = None
        detected_encoding = None

        for encoding in encodings_to_try:
            try:
                with codecs.open(input_file_path, 'r', encoding=encoding) as file:
                    content = file.read()
                if "Výčet Jákobových synů" in content:
                    detected_encoding = encoding
                    break
            except UnicodeDecodeError:
                continue

        if detected_encoding is None:
            print("Nepodařilo se detekovat správné kódování. Zkontrolujte vstupní soubor.")
            return

        print(f"Detekované kódování: {detected_encoding}")

        # Úpravy obsahu
        content = re.sub(r'<italic>', r'\\it', content)
        content = re.sub(r'</italic>', r'\\it*', content)
        content = re.sub(r'<p/>', r'\\p', content)
        content = re.sub(r'<kap/>', r'\\cl_', content)
        content = re.sub(r'<vers n="(\d+)"/>', r'\\v_\1_', content)
        content = re.sub(r'<kap n="(\d+)"/>', r'\\cl_\1', content)

        # Zápis souboru v UTF-8 bez BOM
        with codecs.open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Úpravy byly úspěšně provedeny. Výstup byl uložen do: {output_file_path} v kódování UTF-8")

        # Pro kontrolu vypíšeme část obsahu
        print("Prvních 100 znaků výstupního souboru:")
        print(content[:100])

    except Exception as ex:
        print(f"Došlo k chybě: {str(ex)}")

if __name__ == "__main__":
    main()