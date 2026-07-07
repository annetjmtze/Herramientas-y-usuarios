# 🤖 Dr. Ahorro Bot

> Bot conversacional multicanal para consultar información de medicamentos en México utilizando **Claude (Anthropic)** como motor de inteligencia artificial. Disponible en **Telegram** y **WhatsApp**.

---

# 📌 Tabla de Contenidos

- [🚀 Características](#-características)
- [🛠️ Tecnologías](#️-tecnologías)
- [🧠 Arquitectura](#-arquitectura)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [📋 Requisitos Previos](#-requisitos-previos)
- [⚙️ Instalación y Configuración](#️-instalación-y-configuración)
- [🚀 Uso](#-uso)
- [🔧 Variables de Entorno](#-variables-de-entorno)
- [🧪 Posibles Errores y Soluciones](#-posibles-errores-y-soluciones)
- [🚧 Mejoras Futuras](#-mejoras-futuras)
- [🙏 Créditos](#-créditos)
- [📜 Licencia](#-licencia)

---

# 🚀 Características

- ✅ Funciona tanto en **Telegram** como en **WhatsApp**.
- ✅ Utiliza **Claude (Anthropic)** para normalizar y estructurar la información de medicamentos.
- ✅ Respuestas adaptadas al formato de cada plataforma.
- ✅ Arquitectura modular y fácil de mantener.
- ✅ Fácil de extender a nuevos canales como Discord o Messenger.
- ✅ Registro automático del webhook de WhatsApp.

---

# 🛠️ Tecnologías

| Tecnología | Uso |
|------------|-----|
| Python 3.14+ | Lenguaje principal |
| Flask | Webhook para WhatsApp |
| Twilio API | Integración con WhatsApp |
| python-telegram-bot | Bot de Telegram |
| Anthropic Claude | Procesamiento mediante IA |
| python-dotenv | Variables de entorno |
| ngrok | Exposición del servidor local |

---

# 🧠 Arquitectura

```text
                     ┌────────────────┐
                     │    Telegram    │
                     └───────┬────────┘
                             │
                     ┌───────▼────────┐
                     │ TelegramHandler │
                     └───────┬────────┘
                             │
                             │
                     ┌───────▼────────┐
                     │                │
                     │  Normalizador  │
                     │ Claude (LLM)   │
                     │                │
                     └───────▲────────┘
                             │
                     ┌───────┴────────┐
                     │ WhatsAppHandler│
                     └───────▲────────┘
                             │
                    ┌────────┴────────┐
                    │ Flask + Webhook │
                    └────────▲────────┘
                             │
                        WhatsApp
```

### Principio de diseño

El **normalizador** únicamente recibe texto y devuelve un JSON estructurado. No conoce si la solicitud proviene de Telegram o WhatsApp.

Cada handler se encarga únicamente del formato de salida correspondiente a su plataforma.

---

# 📁 Estructura del Proyecto

```text
dr-ahorro-bot/
│
├── bot/
│   ├── __init__.py
│   ├── telegram_handler.py
│   └── whatsapp_handler.py
│
├── llm/
│   ├── __init__.py
│   └── normalizer.py
│
├── config/
│   └── __init__.py
│
├── data/
│   └── __init__.py
│
├── venv/
├── .env
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

---

# 📋 Requisitos Previos

Antes de ejecutar el proyecto necesitas:

- Python 3.14 o superior
- Cuenta de Anthropic
- Cuenta de Twilio
- Bot creado mediante BotFather en Telegram
- ngrok instalado

---

# ⚙️ Instalación y Configuración

## 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/dr-ahorro-bot.git
cd dr-ahorro-bot
```

---

## 2. Crear un entorno virtual

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```cmd
python -m venv venv
venv\Scripts\activate
```

---

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 4. Configurar variables de entorno

Copia el archivo de ejemplo:

```bash
cp .env.example .env
```

Después completa las credenciales.

```env
# Telegram
TELEGRAM_BOT_TOKEN=tu_token

# Anthropic
ANTHROPIC_API_KEY=tu_api_key

# Twilio
TWILIO_ACCOUNT_SID=tu_sid
TWILIO_AUTH_TOKEN=tu_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

WEBHOOK_URL=https://xxxxxxxx.ngrok-free.app/webhook

PORT=5000
```

---

## 5. Ejecutar ngrok

En otra terminal:

```bash
ngrok http 5000
```

Copia la URL pública y actualiza la variable:

```env
WEBHOOK_URL=https://tu-url.ngrok-free.app/webhook
```

---

# 🚀 Uso

## Solo Telegram

```bash
python main.py --channel telegram
```

---

## Solo WhatsApp

```bash
python main.py --channel whatsapp --port 5000
```

---

## Ambos canales

```bash
python main.py --channel all
```

> **Nota:** Para WhatsApp es necesario que **ngrok esté ejecutándose** antes de iniciar el bot.

---

# 🔧 Variables de Entorno

| Variable | Descripción | Obligatoria |
|-----------|-------------|-------------|
| TELEGRAM_BOT_TOKEN | Token del bot de Telegram | ✅ |
| ANTHROPIC_API_KEY | API Key de Claude | ✅ |
| TWILIO_ACCOUNT_SID | SID de Twilio | Solo WhatsApp |
| TWILIO_AUTH_TOKEN | Token de Twilio | Solo WhatsApp |
| TWILIO_WHATSAPP_NUMBER | Número Sandbox | Solo WhatsApp |
| WEBHOOK_URL | URL pública de ngrok | Solo WhatsApp |
| PORT | Puerto de Flask | No |

---

# 🧪 Posibles Errores y Soluciones

| Error | Solución |
|--------|----------|
| ModuleNotFoundError | Ejecuta `pip install -r requirements.txt` |
| ERROR 404 en getMe | Verifica el token del bot de Telegram |
| Webhook no registrado | Configura manualmente la URL en Twilio |
| Error de modelo Claude | Actualiza el modelo en `normalizer.py` |
| WhatsApp no responde | Revisa ngrok, el puerto y la URL configurada |

---

# 🙏 Créditos

Proyecto desarrollado con fines educativos para practicar:

- Arquitectura de proyectos en Python.
- Desarrollo de bots conversacionales.
- Integración con Telegram.
- Integración con WhatsApp mediante Twilio.
- Webhooks con Flask.
- Uso de modelos LLM mediante Anthropic Claude.
---

⭐ Si este proyecto te resulta útil, considera darle una estrella en GitHub.
