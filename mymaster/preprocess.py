import pandas as pd

# قراءة أول 5 أسطر من ملف X-IIoTID بعد تحميله
file_path = 'X-IIoTID dataset.csv' 
df = pd.read_csv(file_path, low_memory=False)

print("أعمدة البيانات المتاحة:")
print(df.columns.tolist())

# توزيع أنواع الهجمات حسب المستويات المختلفة
print("\nتوزيع التصنيفات العامة (Normal vs Attack):")
print(df['class1'].value_counts())

print("\nتوزيع أنواع الهجمات التفصيلية (Class 2):")
print(df['class2'].value_counts())
# 1. اختيار الأعمدة الأساسية للـ Graph
graph_df = df[['Scr_IP', 'Des_IP', 'Protocol', 'class1', 'class2']].copy()

# 2. تنظيف البيانات من أي قيم فارغة في الـ IPs
graph_df.dropna(subset=['Scr_IP', 'Des_IP'], inplace=True)

# 3. عرض عينة من العلاقات التي سنبنيها
print("\nعينة من العلاقات الجاهزة للـ Graph:")
print(graph_df.head())