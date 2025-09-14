import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.data.clean_data import load_and_clean_data
import uv  # استخدام UV حسب الحاجة (مثال)

# === تحميل البيانات ===
@st.cache_data
def load_data():
    df = load_and_clean_data("data/vehicles.csv")
    return df

df = load_data()

# === عنوان التطبيق ===
st.title("🚗 مشروع معلومات السيارات (AI Car Info + UV)")

# === شريط الفلاتر ===
brands = df["make"].dropna().unique()
brand = st.sidebar.selectbox("اختر العلامة التجارية:", sorted(brands))

models = df[df["make"] == brand]["model"].dropna().unique()
model = st.sidebar.selectbox("اختر الموديل:", sorted(models))

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ فلاتر متقدمة")

# سنة الصنع
if "year" in df.columns:
    min_year, max_year = int(df["year"].min()), int(df["year"].max())
    year_range = st.sidebar.slider("اختر نطاق السنة:", min_year, max_year, (min_year, max_year))
    df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

# قوة المحرك
if "horsepower" in df.columns:
    min_hp, max_hp = int(df["horsepower"].min()), int(df["horsepower"].max())
    hp_range = st.sidebar.slider("اختر قوة المحرك (HP):", min_hp, max_hp, (min_hp, max_hp))
    df = df[(df["horsepower"] >= hp_range[0]) & (df["horsepower"] <= hp_range[1])]

# نوع الوقود
if "fuel_type" in df.columns:
    fuels = df["fuel_type"].dropna().unique()
    fuel_filter = st.sidebar.multiselect("اختر نوع الوقود:", fuels, default=fuels)
    df = df[df["fuel_type"].isin(fuel_filter)]

# === عرض معلومات السيارة ===
car_info = df[(df["make"] == brand) & (df["model"] == model)]

st.subheader(f"📊 تفاصيل السيارة: {brand} {model}")
if not car_info.empty:
    st.dataframe(car_info)

    # عرض الصورة
    img_col = None
    for possible_col in ["image_url", "img_link", "photo", "picture"]:
        if possible_col in car_info.columns:
            img_col = possible_col
            break

    if img_col:
        image_url = car_info.iloc[0][img_col]
        if pd.notna(image_url) and str(image_url).startswith("http"):
            st.image(image_url, caption=f"{brand} {model}", use_column_width=True)
        else:
            st.info("📷 لا توجد صورة متوفرة.")
    else:
        st.info("📷 ملف البيانات لا يحتوي على روابط صور.")
else:
    st.warning("❌ لا توجد بيانات مطابقة للفلاتر المحددة.")

# === إحصائيات عامة ===
st.subheader("📈 إحصائيات عامة")
st.write("عدد السيارات:", len(df))
st.write("عدد العلامات التجارية:", df["make"].nunique())
st.write("عدد الموديلات:", df["model"].nunique())

# === Bar Chart: قوة المحرك ===
if "horsepower" in df.columns and not df["horsepower"].dropna().empty:
    st.subheader("⚡ توزيع قوة المحرك (Horsepower)")
    st.bar_chart(df["horsepower"].dropna())

# === Pie Chart: نوع الوقود ===
if "fuel_type" in df.columns:
    st.subheader("⛽ توزيع السيارات حسب نوع الوقود")
    fuel_counts = df["fuel_type"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(fuel_counts, labels=fuel_counts.index, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

# === Bar Chart: عدد السيارات لكل شركة ===
if "make" in df.columns:
    st.subheader("🏢 عدد السيارات لكل شركة")
    make_counts = df["make"].value_counts()
    st.bar_chart(make_counts)

# === Scatter Plot: السنة × قوة المحرك ===
if "year" in df.columns and "horsepower" in df.columns:
    st.subheader("📊 العلاقة بين سنة الصنع وقوة المحرك")
    fig, ax = plt.subplots()
    scatter = ax.scatter(df["year"], df["horsepower"],
                         c=pd.factorize(df.get("fuel_type", "Unknown"))[0],
                         cmap="viridis", alpha=0.7)
    ax.set_xlabel("سنة الصنع")
    ax.set_ylabel("قوة المحرك (HP)")
    ax.set_title("Year vs Horsepower (حسب نوع الوقود)")

    if "fuel_type" in df.columns:
        legend_labels = df["fuel_type"].dropna().unique()
        legend_handles = [plt.Line2D([0], [0], marker='o', color='w',
                                     markerfacecolor=plt.cm.viridis(i/len(legend_labels)), markersize=8)
                          for i in range(len(legend_labels))]
        ax.legend(legend_handles, legend_labels, title="نوع الوقود", loc="best")

    st.pyplot(fig)

# === مثال استخدام UV ===
st.subheader("🔹 مثال استخدام UV")
st.write("يمكنك هنا دمج أي ميزة أو نموذج من مكتبة UV حسب مشروعك.")
# مثال: uv.some_function(df)