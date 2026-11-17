# PDF Word Converter Telegram bot

Bot PDF → DOCX va DOCX → PDF konvertatsiyasini bajaradi.

## Talablar
- Python 3.10+
- LibreOffice (DOCX → PDF uchun)
- Telegram bot tokeni

## O‘rnatish

### Ubuntu/Debian server
```bash
sudo apt update
sudo apt install -y libreoffice python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Tokenni sozlash
BotFather orqali bot ochib, token oling. Tokenni hech kimga yubormang.
```bash
export BOT_TOKEN="BU_YERGA_TOKEN"
python bot.py
```

Windows'da LibreOffice o‘rnatilgan bo‘lishi va `libreoffice` buyrug‘i PATH ichida bo‘lishi kerak.

## Ishlatish
1. Telegram'da botga `/start` yuboring.
2. `PDF → Word` yoki `Word → PDF` ni tanlang.
3. Mos faylni yuboring.
4. Bot tayyor faylni qaytaradi.

## Muhim eslatmalar
- Hozircha `.docx` formatidagi Word hujjatlari qabul qilinadi.
- Fayl hajmi 20 MB bilan cheklangan.
- PDF → Word aylantirishda murakkab jadvallar, ustunlar va rasmlar joylashuvi o‘zgarishi mumkin.
- Skaner qilingan PDF uchun OCR alohida qo‘shilishi kerak.
- Botni hamma ishlata olishi uchun uni doimiy ishlaydigan serverga joylashtirish kerak.
- Tokenni kod ichiga yozmang va ommaga ulashmang.
