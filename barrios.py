# Datos estáticos por barrio de CABA
# alquiler_m2: precio promedio mensual en ARS por m² (comercial, actualizado ~2024)
# nse: nivel socioeconómico predominante (alto / medio_alto / medio / bajo)
# densidad: densidad peatonal/comercial estimada (alta / media / baja)
# categoria: para clasificación de alquiler (premium / medio / economico)

BARRIOS_DATA = {
    # ── Zona Norte / Premium ─────────────────────────────────────
    "Palermo": {
        "alquiler_m2": 38000,
        "nse": "medio_alto",
        "densidad": "alta",
        "categoria": "premium"
    },
    "Recoleta": {
        "alquiler_m2": 45000,
        "nse": "alto",
        "densidad": "alta",
        "categoria": "premium"
    },
    "Belgrano": {
        "alquiler_m2": 36000,
        "nse": "alto",
        "densidad": "alta",
        "categoria": "premium"
    },
    "Nuñez": {
        "alquiler_m2": 32000,
        "nse": "medio_alto",
        "densidad": "media",
        "categoria": "premium"
    },
    "Colegiales": {
        "alquiler_m2": 30000,
        "nse": "medio_alto",
        "densidad": "media",
        "categoria": "medio"
    },
    "Villa Urquiza": {
        "alquiler_m2": 27000,
        "nse": "medio_alto",
        "densidad": "media",
        "categoria": "medio"
    },
    "Saavedra": {
        "alquiler_m2": 24000,
        "nse": "medio_alto",
        "densidad": "media",
        "categoria": "medio"
    },

    # ── Centro / Microcentro ──────────────────────────────────────
    "San Nicolás": {
        "alquiler_m2": 42000,
        "nse": "medio",
        "densidad": "alta",
        "categoria": "premium"
    },
    "Monserrat": {
        "alquiler_m2": 35000,
        "nse": "medio",
        "densidad": "alta",
        "categoria": "medio"
    },
    "San Telmo": {
        "alquiler_m2": 28000,
        "nse": "medio",
        "densidad": "alta",
        "categoria": "medio"
    },
    "Puerto Madero": {
        "alquiler_m2": 60000,
        "nse": "alto",
        "densidad": "media",
        "categoria": "premium"
    },
    "Retiro": {
        "alquiler_m2": 38000,
        "nse": "medio",
        "densidad": "alta",
        "categoria": "premium"
    },

    # ── Zona Oeste / Centro ───────────────────────────────────────
    "Caballito": {
        "alquiler_m2": 25000,
        "nse": "medio",
        "densidad": "alta",
        "categoria": "medio"
    },
    "Flores": {
        "alquiler_m2": 20000,
        "nse": "medio",
        "densidad": "alta",
        "categoria": "economico"
    },
    "Almagro": {
        "alquiler_m2": 24000,
        "nse": "medio",
        "densidad": "alta",
        "categoria": "medio"
    },
    "Boedo": {
        "alquiler_m2": 20000,
        "nse": "medio",
        "densidad": "media",
        "categoria": "economico"
    },
    "Villa Crespo": {
        "alquiler_m2": 26000,
        "nse": "medio_alto",
        "densidad": "alta",
        "categoria": "medio"
    },
    "Chacarita": {
        "alquiler_m2": 22000,
        "nse": "medio",
        "densidad": "media",
        "categoria": "medio"
    },
    "Paternal": {
        "alquiler_m2": 18000,
        "nse": "medio",
        "densidad": "media",
        "categoria": "economico"
    },
    "Villa del Parque": {
        "alquiler_m2": 18000,
        "nse": "medio",
        "densidad": "media",
        "categoria": "economico"
    },
    "Villa Devoto": {
        "alquiler_m2": 20000,
        "nse": "medio_alto",
        "densidad": "media",
        "categoria": "medio"
    },
    "Monte Castro": {
        "alquiler_m2": 15000,
        "nse": "medio",
        "densidad": "baja",
        "categoria": "economico"
    },

    # ── Zona Sur ──────────────────────────────────────────────────
    "La Boca": {
        "alquiler_m2": 18000,
        "nse": "bajo",
        "densidad": "media",
        "categoria": "economico"
    },
    "Barracas": {
        "alquiler_m2": 16000,
        "nse": "bajo",
        "densidad": "media",
        "categoria": "economico"
    },
    "Parque Patricios": {
        "alquiler_m2": 17000,
        "nse": "medio",
        "densidad": "media",
        "categoria": "economico"
    },
    "Nueva Pompeya": {
        "alquiler_m2": 14000,
        "nse": "bajo",
        "densidad": "baja",
        "categoria": "economico"
    },
    "Villa Lugano": {
        "alquiler_m2": 12000,
        "nse": "bajo",
        "densidad": "media",
        "categoria": "economico"
    },
    "Villa Riachuelo": {
        "alquiler_m2": 11000,
        "nse": "bajo",
        "densidad": "baja",
        "categoria": "economico"
    },
    "Mataderos": {
        "alquiler_m2": 13000,
        "nse": "bajo",
        "densidad": "media",
        "categoria": "economico"
    },

    # ── Default (si no se identifica el barrio) ───────────────────
    "_default": {
        "alquiler_m2": 22000,
        "nse": "medio",
        "densidad": "media",
        "categoria": "medio"
    }
}
