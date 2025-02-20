from datasets import load_dataset
import pandas as pd
import matplotlib.pyplot as plt

# Veri setini yükle
dataset = load_dataset("winvoker/turkish-sentiment-analysis-dataset")

# Tüm bölümleri birleştir
df_train = pd.DataFrame(dataset['train'])
df_test = pd.DataFrame(dataset['test'])
df_combined = pd.concat([df_train, df_test], ignore_index=True)

# Rastgele 10 satır seç
sampled_df = df_combined.sample(10)

# Tabloyu Matplotlib ile görselleştir
fig, ax = plt.subplots(figsize=(12, 6))  # Grafik boyutu
ax.axis('tight')
ax.axis('off')

# Tabloyu oluştur
table = ax.table(
    cellText=sampled_df.values, 
    colLabels=sampled_df.columns, 
    loc='center'
)

# Font boyutunu ayarla
table.auto_set_font_size(False)
table.set_fontsize(12)  # Font boyutunu artır

# Hücre boyutlarını ayarla (isteğe bağlı)
table.scale(1.2, 1.5)  # x, y oranlarını büyüt

# Göster
plt.show()
