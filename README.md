# 🔍 LocalScope — Análisis de viabilidad de locales comerciales en CABA

App web en Python/Streamlit que analiza la viabilidad de abrir un local comercial en CABA dada una dirección y un rubro.

---

## ¿Qué analiza?

| Capa | Fuente |
|------|--------|
| 🏪 Competencia del rubro | Google Places API |
| 🚌 Transporte público cercano | Google Places API |
| 💰 Precio de alquiler estimado | Tabla estática por barrio |
| 👥 Demografía del barrio | Tabla estática + API datos abiertos CABA |
| 💡 Puntos clave | Análisis basado en reglas (sin costo adicional) |

---

## Cómo deployar en Streamlit Cloud (paso a paso)

### 1. Obtené la API Key de Google Places (gratis hasta $200/mes)

1. Ir a https://console.cloud.google.com
2. Crear un proyecto nuevo
3. Activar "Places API" en "APIs & Services"
4. Ir a "Credenciales" → "Crear credencial" → "Clave de API"
5. Guardar la clave

---

### 2. Subí el código a GitHub

1. Crear cuenta en https://github.com si no tenés
2. Crear un repositorio nuevo (ej: `localscope`)
3. Subir todos los archivos de esta carpeta:
   - `app.py`
   - `requirements.txt`
   - `data/__init__.py`
   - `data/barrios.py`

Si no sabés usar git, podés usar la interfaz web de GitHub:
- Abrí tu repo → "Add file" → "Upload files" → arrastrá los archivos

---

### 3. Deployá en Streamlit Cloud (100% gratis)

1. Ir a https://share.streamlit.io
2. Conectar tu cuenta de GitHub
3. "New app" → seleccionar el repo `localscope`
4. Main file: `app.py`
5. Click en "Deploy"

En 2-3 minutos tenés tu app en una URL pública.

---

### 4. Usarla

1. Abrí la URL de tu app
2. En el panel lateral (←) ingresá tus API keys
3. Completá dirección, rubro y radio
4. Click en "Analizar ubicación"

---

## Estructura del proyecto

```
localscope/
├── app.py              # App principal
├── requirements.txt    # Dependencias Python
└── data/
    ├── __init__.py
    └── barrios.py      # Tabla de precios y perfil por barrio
```

---

## Próximas mejoras posibles

- [ ] Agregar scraping en tiempo real de ZonaProp para precios de alquiler
- [ ] Integrar datos de flujo peatonal
- [ ] Exportar el análisis como PDF
- [ ] Comparar múltiples direcciones en simultáneo
- [ ] Historial de análisis guardados
