import zlib
import base64
import sys

LOCALIZATION = {
    'en': {
        'title': "--- Text Compressor/Decompressor ---",
        'menu_header': "\nPlease select an action:",
        'opt_1': "1. Compress text",
        'opt_2': "2. Decompress text",
        'opt_3': "3. Exit",
        'choice_prompt': "Your choice (1-3): ",
        'input_compress': "\nEnter text to compress: ",
        'input_decompress': "\nEnter string to decompress: ",
        'res_compress': "\n--- Compressed Result ---",
        'res_decompress': "\n--- Original Text ---",
        'err_empty': "Input cannot be empty.",
        'err_invalid_choice': "Invalid choice. Please try again.",
        'err_decode': "Error: Invalid compressed data or corrupted string. Details: {}",
        'exit_msg': "Exiting...",
        'interrupt': "\n\nOperation cancelled by user. Exiting...",
        'separator': "-------------------------"
    },
    'ru': {
        'title': "--- Компрессор/Декомпрессор текста ---",
        'menu_header': "\nПожалуйста, выберите действие:",
        'opt_1': "1. Сжать текст",
        'opt_2': "2. Распаковать текст",
        'opt_3': "3. Выход",
        'choice_prompt': "Ваш выбор (1-3): ",
        'input_compress': "\nВведите текст для сжатия: ",
        'input_decompress': "\nВведите строку для распаковки: ",
        'res_compress': "\n--- Сжатый результат ---",
        'res_decompress': "\n--- Исходный текст ---",
        'err_empty': "Ввод не может быть пустым.",
        'err_invalid_choice': "Неверный выбор. Пожалуйста, попробуйте снова.",
        'err_decode': "Ошибка: Неверные сжатые данные или поврежденная строка. Подробности: {}",
        'exit_msg': "Выход...",
        'interrupt': "\n\nОперация отменена пользователем. Выход...",
        'separator': "-------------------------"
    }
}

CURRENT_LANG = {}

def select_language():
    print("\nSelect Language / Выберите язык:")
    print("1. English")
    print("2. Русский")
    
    while True:
        choice = input(">>> ").strip()
        if choice == '1':
            return 'en'
        elif choice == '2':
            return 'ru'
        else:
            print("Invalid choice / Неверный выбор (1-2)")

def compress_text(input_string):
    if not input_string:
        return ""
    try:
        input_bytes = input_string.encode('utf-8')
        compressed_data = zlib.compress(input_bytes, level=9)
        b64_encoded = base64.urlsafe_b64encode(compressed_data)
        return b64_encoded.decode('utf-8')
    except Exception as e:
        return f"Compression Error: {e}"

def decompress_text(compressed_string):
    if not compressed_string:
        return ""

    try:
        compressed_string = compressed_string.strip()
        b64_bytes = compressed_string.encode('utf-8')
        compressed_data = base64.urlsafe_b64decode(b64_bytes)
        decompressed_bytes = zlib.decompress(compressed_data)
        return decompressed_bytes.decode('utf-8')
        
    except (zlib.error, base64.binascii.Error, UnicodeDecodeError) as e:
        return CURRENT_LANG['err_decode'].format(e)

def main():
    global CURRENT_LANG
    
    lang_code = select_language()
    CURRENT_LANG = LOCALIZATION[lang_code]
    
    print(f"\n{CURRENT_LANG['title']}")
    
    while True:
        print(CURRENT_LANG['menu_header'])
        print(CURRENT_LANG['opt_1'])
        print(CURRENT_LANG['opt_2'])
        print(CURRENT_LANG['opt_3'])
        
        choice = input(CURRENT_LANG['choice_prompt']).strip()
        
        if choice == '1':
            original_text = input(CURRENT_LANG['input_compress'])
            if original_text:
                result = compress_text(original_text)
                print(f"{CURRENT_LANG['res_compress']}\n{result}")
                print(CURRENT_LANG['separator'])
            else:
                print(CURRENT_LANG['err_empty'])
                
        elif choice == '2':
            cipher_text = input(CURRENT_LANG['input_decompress']).strip()
            if cipher_text:
                result = decompress_text(cipher_text)
                print(f"{CURRENT_LANG['res_decompress']}\n{result}")
                print(CURRENT_LANG['separator'])
            else:
                print(CURRENT_LANG['err_empty'])
                
        elif choice == '3':
            print(CURRENT_LANG['exit_msg'])
            sys.exit()
            
        else:
            print(CURRENT_LANG['err_invalid_choice'])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        msg = LOCALIZATION['en']['interrupt'] if not CURRENT_LANG else CURRENT_LANG['interrupt']
        print(msg)
        sys.exit()

