import pandas as pd

def load_and_clean_data(path: str) -> pd.DataFrame:
    # تحميل البيانات
    df = pd.read_csv(path)

    # تصحيح أسماء الأعمدة (اختياري)
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # حذف القيم المفقودة الحرجة
    if "make" in df.columns and "model" in df.columns:
        df = df.dropna(subset=["make", "model"])

    # محاولة تحويل الأعمدة الرقمية
    numeric_cols = ["year", "horsepower", "torque", "top_speed", "acceleration"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df