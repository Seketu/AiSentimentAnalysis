import pandas as pd
import matplotlib.pyplot as plt

# Veri setini yükleme
dataset = pd.read_csv(r"C:\Users\avina\OneDrive\Belgeler\python\new_dataset.csv")

# Sütunları seçme
columns = ["Gemini", "Gpt", "Llama", "Core"]

# Her sütun için Core ile eşleşen değerlerin hesaplanması
results = []
for column in columns[:-1]:  # 'Core' dışında kalan sütunları işler
    matched_values = dataset[column][dataset[column] == dataset["Core"]]
    value_counts = matched_values.value_counts()  # Eşleşen değerlerin frekansı
    results.append({
        "Column": column,
        "Matched Values": value_counts
    })

# Pie grafikleri çizme
fig, axes = plt.subplots(1, len(results), figsize=(15, 5))

for i, result in enumerate(results):
    ax = axes[i]
    values = result["Matched Values"]
    labels = values.index
    ax.pie(
        values,
        labels=[f"{label} ({value})" for label, value in zip(labels, values)],
        autopct='%1.1f%%',
        startangle=90
    )
    ax.set_title(result["Column"])

# Genel başlık ve düzenleme
plt.tight_layout()
plt.show()
