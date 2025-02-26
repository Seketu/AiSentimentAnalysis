import pandas as pd
import matplotlib.pyplot as plt

# Veri setini okuma
dataset = pd.read_csv(r"C:\Users\avina\OneDrive\Belgeler\python\new_dataset.csv")

# Tüm verileri küçük harfe çevirerek normalize etme
dataset = dataset.apply(lambda x: x.str.lower() if x.dtype == "object" else x)

# Sütunları seçme
geminiColumn = dataset["Gemini"]
gptColumn = dataset["Gpt"]
llamaColumn = dataset["Llama"]
coreColumn = dataset["Core"]

# Core'daki "negative" değerlerle eşleşen diğer sütunların "negative" değerlerini seçme
gemini_negative_match = ((geminiColumn == "negative") & (coreColumn == "negative")).sum()
gpt_negative_match = ((gptColumn == "negative") & (coreColumn == "negative")).sum()
llama_negative_match = ((llamaColumn == "negative") & (coreColumn == "negative")).sum()

# Her sütun için toplam "negative" değerler
gemini_total_negative = (geminiColumn == "negative").sum()
gpt_total_negative = (gptColumn == "negative").sum()
llama_total_negative = (llamaColumn == "negative").sum()

# Her sütun için kalan (eşleşmeyen) "negative" değerler
gemini_non_match = gemini_total_negative - gemini_negative_match
gpt_non_match = gpt_total_negative - gpt_negative_match
llama_non_match = llama_total_negative - llama_negative_match

# Çapraz kontrol
print("Kontrol: Toplamlar doğru mu?")
print(f"Gemini toplam: {gemini_total_negative}, Match: {gemini_negative_match}, Non-Match: {gemini_non_match}")
print(f"GPT toplam: {gpt_total_negative}, Match: {gpt_negative_match}, Non-Match: {gpt_non_match}")
print(f"Llama toplam: {llama_total_negative}, Match: {llama_negative_match}, Non-Match: {llama_non_match}")

# Pie grafikleri için veri
data = [
    [gemini_negative_match, gemini_non_match],
    [gpt_negative_match, gpt_non_match],
    [llama_negative_match, llama_non_match]
]
labels = ["match", "non-match"]
colors = ["red", "lightgray"]
titles = ["Gemini", "GPT", "Llama"]

# Özelleştirilmiş autopct fonksiyonu
def autopct_with_counts(pct, all_values):
    total = sum(all_values)
    absolute = int(round(pct * total / 100.0))
    return f'{pct:.1f}%\n({absolute})'

# Grafik oluşturma
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for i, ax in enumerate(axes):
    wedges, texts, autotexts = ax.pie(
        data[i],
        labels=None,  # Sadece sayılar göstermek için labels'i kaldırıyoruz
        colors=colors,
        autopct=lambda pct: autopct_with_counts(pct, data[i]),
        textprops={'fontsize': 14}
    )
    ax.set_title(titles[i], fontsize=20)

# Genel legend ekleme
fig.legend(
    handles=[
        plt.Line2D([0], [0], color=color, linewidth=10) for color in colors
    ],
    labels=labels,
    loc="upper right",
    fontsize=14
)

plt.tight_layout()
plt.show()
