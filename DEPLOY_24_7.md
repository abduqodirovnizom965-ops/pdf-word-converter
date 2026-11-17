# 24/7 joylashtirish (Docker server)

1. ZIP arxivni oching va ichidagi fayllarni GitHub'dagi yangi, PRIVATE repository'ga yuklang.
2. Docker qo‘llaydigan VPS/server oling (Ubuntu 22.04/24.04 tavsiya qilinadi).
3. Serverga Docker o‘rnating.
4. Repository'ni serverga clone qiling.
5. Loyiha papkasida quyidagilarni bajaring:

```bash
docker build -t pdf-word-converter .
docker run -d --name pdf-word-converter --restart unless-stopped \
  -e BOT_TOKEN='BOTFATHER_TOKENINGIZ' \
  pdf-word-converter
```

6. Holatini tekshirish:
```bash
docker logs -f pdf-word-converter
```

Muhim:
- `BOT_TOKEN` maxfiy kalit. Uni GitHub'ga, chatga yoki ommaviy joyga joylamang.
- 24/7 ishlashi uchun VPS/server faol va internetga ulangan bo‘lishi kerak.
- VPS odatda pullik; bepul hostinglarning ayrimlari uxlab qolishi mumkin, shuning uchun haqiqiy 24/7 kafolat bermaydi.
- Botni yangilashda yangi image build qiling va konteynerni qayta ishga tushiring.
