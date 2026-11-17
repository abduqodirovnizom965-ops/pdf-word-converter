import os
import logging
import tempfile
import subprocess
from pathlib import Path

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ContextTypes, filters
)
from pdf2docx import Converter

BOT_TOKEN = os.getenv("BOT_TOKEN")
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

MENU = ReplyKeyboardMarkup(
    [["📄 PDF → Word", "📝 Word → PDF"], ["ℹ️ Yordam"]],
    resize_keyboard=True,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "Assalomu alaykum! PDF Word Converter botiga xush kelibsiz.\n\n"
        "Kerakli xizmatni tanlang:",
        reply_markup=MENU,
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📄 PDF → Word: avval shu tugmani bosing, keyin PDF yuboring.\n"
        "📝 Word → PDF: avval shu tugmani bosing, keyin DOCX yuboring.\n\n"
        "Qo‘llab-quvvatlanadigan formatlar: PDF va DOCX.\n"
        "Maksimal fayl hajmi: 20 MB.\n"
        "Eslatma: skaner qilingan PDF fayllarda matnni tanish (OCR) talab qilinishi mumkin."
    )

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📄 PDF → Word":
        context.user_data["mode"] = "pdf_to_word"
        await update.message.reply_text("PDF faylni yuboring.")
    elif text == "📝 Word → PDF":
        context.user_data["mode"] = "word_to_pdf"
        await update.message.reply_text("Word (.docx) faylni yuboring.")
    elif text == "ℹ️ Yordam":
        await help_command(update, context)
    else:
        await update.message.reply_text("Menyudan xizmat turini tanlang.", reply_markup=MENU)

def convert_pdf_to_docx(source: Path, target: Path):
    converter = Converter(str(source))
    try:
        converter.convert(str(target))
    finally:
        converter.close()

def convert_docx_to_pdf(source: Path, output_dir: Path):
    # Requires LibreOffice to be installed on the server.
    result = subprocess.run(
        [
            "libreoffice", "--headless", "--convert-to", "pdf",
            "--outdir", str(output_dir), str(source)
        ],
        capture_output=True, text=True, timeout=120
    )
    generated = output_dir / (source.stem + ".pdf")
    if result.returncode != 0 or not generated.exists():
        raise RuntimeError(result.stderr or result.stdout or "LibreOffice konvertatsiya qila olmadi.")
    return generated

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    doc = message.document
    mode = context.user_data.get("mode")

    if not mode:
        await message.reply_text(
            "Avval menyudan konvertatsiya turini tanlang.",
            reply_markup=MENU,
        )
        return

    if doc.file_size and doc.file_size > MAX_FILE_SIZE:
        await message.reply_text("Fayl hajmi 20 MB dan oshmasligi kerak.")
        return

    filename = doc.file_name or "document"
    suffix = Path(filename).suffix.lower()

    if mode == "pdf_to_word" and suffix != ".pdf":
        await message.reply_text("Bu xizmat uchun PDF fayl yuboring.")
        return
    if mode == "word_to_pdf" and suffix not in (".docx",):
        await message.reply_text("Bu xizmat uchun Word (.docx) fayl yuboring.")
        return

    status = await message.reply_text("⏳ Fayl konvertatsiya qilinmoqda...")
    try:
        with tempfile.TemporaryDirectory() as tmp:
            workdir = Path(tmp)
            source = workdir / ("input" + suffix)
            target = workdir / ("output.docx" if mode == "pdf_to_word" else "output.pdf")

            tg_file = await doc.get_file()
            await tg_file.download_to_drive(custom_path=str(source))

            if mode == "pdf_to_word":
                convert_pdf_to_docx(source, target)
            else:
                target = convert_docx_to_pdf(source, workdir)

            if not target.exists() or target.stat().st_size == 0:
                raise RuntimeError("Natijaviy fayl yaratilmadi.")

            with target.open("rb") as file_obj:
                await message.reply_document(
                    document=file_obj,
                    filename=("converted.docx" if mode == "pdf_to_word" else "converted.pdf"),
                    caption="✅ Tayyor! Faylingiz konvertatsiya qilindi.",
                )

        await status.delete()
        context.user_data.pop("mode", None)
    except subprocess.TimeoutExpired:
        await status.edit_text("Konvertatsiya vaqti tugadi. Kichikroq fayl bilan urinib ko‘ring.")
    except Exception as exc:
        logger.exception("Conversion failed")
        await status.edit_text(
            "❌ Faylni aylantirib bo‘lmadi. PDF himoyalangan, buzilgan yoki "
            "format mos kelmasligi mumkin. Boshqa fayl bilan urinib ko‘ring."
        )

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN muhit o‘zgaruvchisiga Telegram bot tokenini kiriting.")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.run_polling()

if __name__ == "__main__":
    main()
