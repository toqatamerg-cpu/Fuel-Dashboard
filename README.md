# Fuel Station Theft Detection & Dashboard

مشروع لتحليل بيانات محطات الوقود واكتشاف حالات السرقة (Fuel Theft Detection)، ويحتوي على جزئين:

## محتويات المشروع

- **`fuel_theft_analysis.ipynb`** — نوتبوك لتنظيف البيانات (Data Cleaning)، التحليل الاستكشافي (EDA)، اختبار Chi-Square، وبناء نموذج تعلم آلي (Random Forest / Logistic Regression) للتنبؤ بحالات السرقة.
- **`dashboard.py`** — لوحة تحكم تفاعلية (Interactive Dashboard) مبنية باستخدام Dash و Plotly لعرض بيانات المبيعات والسرقات بشكل مرئي.
- **`requirements.txt`** — قائمة المكتبات المطلوبة لتشغيل المشروع.

## متطلبات التشغيل

```bash
pip install -r requirements.txt
```

## تشغيل الداشبورد

الداشبورد يتوقع وجود ملف بيانات باسم `cleaned_fuel_data.csv` في نفس المجلد (ناتج من النوتبوك بعد التنظيف). تأكد من تصدير البيانات المنظفة من النوتبوك بهذا الاسم، ثم شغّل:

```bash
python dashboard.py
```

بعدها افتح الرابط الذي يظهر في الـ terminal (عادة `http://127.0.0.1:8050`).

## تشغيل النوتبوك

```bash
jupyter notebook fuel_theft_analysis.ipynb
```

النوتبوك يعتمد على ملف بيانات خام باسم `Fuel_station_theft_dataset.csv` — ضع الملف في نفس المجلد قبل التشغيل.

## بنية المشروع المقترحة

```
.
├── fuel_theft_analysis.ipynb
├── dashboard.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
    ├── Fuel_station_theft_dataset.csv   (البيانات الخام)
    └── cleaned_fuel_data.csv            (البيانات بعد التنظيف)
```
