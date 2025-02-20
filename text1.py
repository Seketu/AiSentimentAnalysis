import pandas as pd
import matplotlib.pyplot as plt

# CSV dosyasını oku
df = pd.read_csv(r"C:\Users\avina\OneDrive\Belgeler\python\new_dataset.csv")

# Eşleşme durumunu kontrol et
def check_agreement(row):
    if row['Gpt'] == row['Gemini'] == row['Llama'] == row['Core']:
        return 'Eşleşenler'
    else:
        return 'Eşleşmeyenler'

df['Eşleşme'] = df.apply(check_agreement, axis=1)
results = df['Eşleşme'].value_counts()

# Grafik ayarları
fig, ax = plt.subplots(figsize=(10, 5))
colors = ['#2ecc71', '#e74c3c']

# Yatay bar grafiği oluştur
bars = results.plot(kind='barh', color=colors, ax=ax)

# Çerçeveyi kaldır
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# Grid çizgilerini kaldır
ax.grid(False)

# X ekseni sayılarını kaldır
ax.set_xticks([])

# Bar üzerine değerleri ve yüzdeleri yaz
for i, v in enumerate(results):
    percentage = (v / results.sum()) * 100
    ax.text(v, i, f'{v} (%{percentage:.1f})', va='center', fontsize=12)

plt.title('AI Modellerinin Eşleşme Durumu', pad=20, fontsize=16)
plt.ylabel('')  # Y ekseni etiketini kaldır

# Y ekseni etiketlerinin fontunu büyüt
plt.yticks(fontsize=12)

plt.tight_layout()
plt.show()