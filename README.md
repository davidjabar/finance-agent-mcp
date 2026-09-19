# Finance Agent MCP 🤖💰

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-1.4.0-darkgreen.svg)](https://www.langchain.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)](https://www.docker.com/)

**Finance Agent MCP** adalah asisten keuangan pribadi berbasis AI yang dikontrol langsung melalui Telegram. Bot ini memanfaatkan **Model Context Protocol (MCP)** via FastAPI untuk mengintegrasikan LLM dengan *database* keuangan secara modular, aman, dan responsif.

Cukup mengobrol secara natural via Telegram, agen AI akan otomatis mencatat, mengategorikan, dan memberikan ringkasan transaksi keuangan kamu.

---

## ✨ Fitur Utama

- **Pencatatan Natural via Chat**: Cukup ketik seperti obrolan biasa (contoh: *"Beli kopi susu 25rb"* atau *"Dapet gaji bulan ini 10jt"*).
- **Kategori Otomatis**: AI menganalisis deskripsi pesan dan menentukan kategori transaksi secara otomatis.
- **Ringkasan Keuangan**: Minta ringkasan pengeluaran atau pemasukan kapan saja melalui pesan teks.
- **Arsitektur MCP**: Menggunakan `fastapi-mcp` dan `langchain-mcp-adapters` sebagai "tangan dan otak" agen untuk mengakses *endpoint* database secara terstruktur.
- **Keamanan Khusus (Owner Protection)**: Bot dibatasi hanya untuk ID Telegram milikmu, mencegah intervensi dari pengguna tak dikenal.
- **Auto Database Migration**: Migrasi PostgreSQL ditangani otomatis oleh Alembic saat kontainer Docker dijalankan.

---

## 🛠️ Tech Stack

- **Language & API Framework**: Python, FastAPI, Uvicorn
- **AI Agent Framework**: LangChain, LangGraph, LangChain OpenAI, FastAPI MCP
- **Bot Interface**: `python-telegram-bot`
- **Database & ORM**: PostgreSQL, SQLAlchemy, Alembic (Auto Migration)
- **Containerization**: Docker & Docker Compose
- **Logging & Config**: Loguru, Pydantic Settings

---

## 🚀 Cara Menjalankan (Deployment)

Proyek ini sudah dibungkus rapi menggunakan Docker Compose, sehingga kamu hanya perlu menyiapkan variabel lingkungan (`.env`) dan menjalankan satu perintah.

### 1. Clone Repository

```bash
git clone [https://github.com/davidjabar/finance-agent-mcp.git](https://github.com/davidjabar/finance-agent-mcp.git)
cd finance-agent-mcp
```

### 2. Konfigurasi Environment Variable (.env)
Buat file .env di direktori utama proyek, lalu isi parameter berikut:

# Database Settings
```bash
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=db
DB_PORT=5432
DB_NAME=finance_db


# Telegram Settings
OWNER_TELEGRAM_ID=123456789  # ID Telegram kamu agar bot hanya merespons kamu
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyZ  # Token dari @BotFather

# LLM / AI Settings
LLM_API_KEY=sk-...  # API Key OpenAI / provider terkait
CHAT_MODEL=gpt-4o-mini  # Model yang ingin digunakan

# Catatan Keamanan: OWNER_TELEGRAM_ID memastikan orang lain tidak bisa menggunakan atau mengintervensi bot Telegram kamu.
```

### 3. Jalankan Docker Compose
Jalankan perintah berikut untuk mengompilasi dan menjalankan semua layanan (database PostgreSQL dan aplikasi Finance Agent):

```bash
docker compose up -d --build
```

Aplikasi akan otomatis menjalankan migrasi database via Alembic saat startup dan siap digunakan!

💬 Cara Penggunaan
Setelah kontainer berjalan, buka bot kamu di Telegram dan langsung kirimkan pesan tanpa perlu perintah khusus:

Mencatat Pengeluaran:

"Kemarin abis beli bensin 50rb sama makan siang 35rb"

Mencatat Pemasukan:

"Barusaja dapet transferan katering 500ribu"

Meminta Ringkasan:

"Tolong totalin dong pengeluaran gue minggu ini"

📄 Lisensi
Distributed under the MIT License. See LICENSE for more information.
