import pandas as pd

df = pd.read_csv(r"C:\Users\avina\OneDrive\Belgeler\python\dataset.csv")

# Sütun renklerini ayarlamak için bir fonksiyon tanımlayın
def highlight_columns(s):
    color_map = {
        'Gemini': 'background-color: lightblue;',  # Açık mavi
        'Gpt': 'background-color: lightyellow;',    # Açık sarı
        'Llama': 'background-color: lightcoral;',   # Açık kırmızı
        'Train': 'background-color: lightpurple;',   # Açık mor
        'GeminiContent': 'background-color: lightblue;',  # Açık mavi
        'GptContent': 'background-color: lightyellow;',    # Açık sarı
        'LlamaContent': 'background-color: lightcoral;',   # Açık kırmızı
        'Core': 'background-color: lightpurple;'            # Açık mor
    }
    return [color_map.get(col, '') for col in s.index]

# DataFrame'e stil uygulayın
styled_df = df.style.apply(highlight_columns, axis=1)

# HTML dosyasını oluştur
html_file_path = html_file_path = r"C:\Users\avina\OneDrive\Belgeler\python\dataset_output2.html"

styled_df.to_html(html_file_path, index=False, escape=False)