import pandas as pd
import matplotlib.pyplot as plt

# Veri setini yükleme
dataset = pd.read_csv(r"C:\Users\avina\OneDrive\Belgeler\python\new_dataset.csv")

# Sütunlar
columns = ["Gemini", "Gpt", "Llama", "Core"]

# Pie grafikleri çizme
fig, axes = plt.subplots(2, 2, figsize=(16, 12))  # 2x2 düzeninde grafik

for i, column in enumerate(columns):
    ax = axes[i // 2, i % 2]  # 2x2 grid'de grafiği seç
    
    # Sütundaki değerlerin frekanslarını hesaplama
    value_counts = dataset[column].value_counts()
    
    # Pie grafiği için veriler
    values = value_counts.values
    labels = value_counts.index
    colors = plt.cm.Paired(range(len(values)))  # Renk paleti

    # Pie grafiğini çizme
    wedges, texts, autotexts = ax.pie(
        values,
        labels=[f"{label} ({value})" for label, value in zip(labels, values)],
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        textprops={'fontsize': 14}  # Etiket font boyutu
    )
    
    # Otomatik yazı (yüzdeler) font boyutunu ayarlama
    for autotext in autotexts:
        autotext.set_fontsize(16)
    
    # Başlık font boyutunu ayarlama
    ax.set_title(column, fontsize=20)

# Genel başlık ve düzenleme
plt.suptitle("Distribution of Values in Each Column", fontsize=24, y=1.05)
plt.tight_layout()
plt.show()
