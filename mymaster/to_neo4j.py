
from neo4j import GraphDatabase
import pandas as pd
from datetime import datetime
# 1. إعدادات الاتصال
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "Asdfqwer@1234#") 

# 2. تحميل البيانات
file_name = 'X-IIoTID dataset.csv'
df = pd.read_csv(file_name, nrows=10000)

# تنظيف أسماء الأعمدة من أي مسافات زائدة
df.columns = df.columns.str.strip()

# تصحيح المسميات بناءً على قائمة الأعمدة التي ظهرت عندك:
# المصدر: Scr_IP، الهدف: Des_IP، البروتوكول: Protocol
# معدل الحزم موجود أصلاً باسم: paket_rate

# ... (جزء الاتصال بالقاعدة كما هو)

def upload_to_neo4j(df):
    driver = GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as session:
        print(f"--- بدء رفع {len(df)} سجل مع بيانات الزمن ---")
        
        