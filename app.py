import streamlit as st
import requests
import math
import folium
from streamlit_folium import st_folium
from data.barrios import BARRIOS_DATA

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LocalScope · Análisis de Locales CABA",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── STYLES ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

* { box-sizing: border-box; }

html, body, .stApp {
    background-color: #0f0f0f;
    color: #e8e4dc;
    font-family: 'DM Sans', sans-serif;
}

.stApp > header { background: transparent !important; }

h1, h2, h3 { font-family: 'DM Serif Display', serif; }

/* Hero */
.hero {
    padding: 3rem 0 2rem 0;
    border-bottom: 1px solid #2a2a2a;
    margin-bottom: 2.5rem;
}
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 3.2rem;
    line-height: 1.1;
    color: #e8e4dc;
    margin: 0 0 0.5rem 0;
}
.hero-title span { color: #c8f065; }
.hero-sub {
    font-size: 1rem;
    color: #888;
    font-weight: 300;
    letter-spacing: 0.02em;
}

/* Cards */
.score-card {
    background: #181818;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.score-card h4 {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #666;
    margin: 0 0 0.5rem 0;
}
.score-card .value {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem;
    line-height: 1;
    color: #e8e4dc;
    margin: 0 0 0.3rem 0;
}
.score-card .label { font-size: 0.85rem; color: #888; }

/* Semáforo */
.semaforo {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    margin: 0.4rem 0;
}
.dot {
    width: 12px; height: 12px;
    border-radius: 50%;
    background: #2a2a2a;
}
.dot.green { background: #c8f065; box-shadow: 0 0 8px #c8f065aa; }
.dot.yellow { background: #f0c040; box-shadow: 0 0 8px #f0c040aa; }
.dot.red { background: #f06060; box-shadow: 0 0 8px #f06060aa; }

/* Layer card */
.layer-card {
    background: #181818;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.8rem;
}
.layer-title {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #888;
    margin-bottom: 0.3rem;
}
.layer-value {
    font-size: 1.1rem;
    color: #e8e4dc;
    font-weight: 500;
}
.layer-detail { font-size: 0.85rem; color: #666; margin-top: 0.2rem; }

/* Analysis box */
.analysis-box {
    background: #141414;
    border: 1px solid #2a2a2a;
    border-left: 3px solid #c8f065;
    border-radius: 0 12px 12px 0;
    padding: 1.5rem;
    font-size: 0.95rem;
    line-height: 1.7;
    color: #ccc;
}

/* Input overrides */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stSlider {
    background: #181818 !important;
    border-color: #2a2a2a !important;
    color: #e8e4dc !important;
}

.stButton > button {
    background: #c8f065;
    color: #0f0f0f;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
    letter-spacing: 0.05em;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 2rem;
    width: 100%;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: #d8ff70;
    transform: translateY(-1px);
}

.stSpinner > div { border-top-color: #c8f065 !important; }

hr { border-color: #2a2a2a; }
</style>
""", unsafe_allow_html=True)

# ─── HELPERS ────────────────────────────────────────────────────────────────────

def geocode_address(address: str, api_key: str) -> dict | None:
    """Geocodifica una dirección en CABA."""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": f"{address}, Buenos Aires, Argentina", "key": api_key}
    r = requests.get(url, params=params, timeout=10)
    data = r.json()
    if data["status"] == "OK":
        loc = data["results"][0]["geometry"]["location"]
        return {"lat": loc["lat"], "lng": loc["lng"], "formatted": data["results"][0]["formatted_address"]}
    return None


def search_places(lat: float, lng: float, radius: int, keyword: str, place_type: str, api_key: str) -> list:
    """Busca lugares cercanos con Places API."""
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "keyword": keyword,
        "type": place_type,
        "key": api_key,
        "language": "es"
    }
    r = requests.get(url, params=params, timeout=10)
    data = r.json()
    return data.get("results", [])


def get_transit_stops(lat: float, lng: float, radius: int, api_key: str) -> list:
    """Busca paradas de transporte público cercanas."""
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "type": "transit_station",
        "key": api_key,
        "language": "es"
    }
    r = requests.get(url, params=params, timeout=10)
    data = r.json()
    stops = data.get("results", [])

    # También buscar paradas de colectivo (bus_station)
    params["type"] = "bus_station"
    r2 = requests.get(url, params=params, timeout=10)
    data2 = r2.json()
    stops += data2.get("results", [])
    return stops


def get_barrio_from_coords(lat: float, lng: float) -> str | None:
    """Intenta identificar el barrio usando la API de datos abiertos CABA."""
    try:
        url = f"https://datosabiertos-apis.buenosaires.gob.ar/datasets/barrios/consultar_punto?x={lng}&y={lat}"
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            data = r.json()
            return data.get("nombre") or data.get("NOMBRE")
    except Exception:
        pass
    return None


def haversine(lat1, lng1, lat2, lng2) -> float:
    """Distancia en metros entre dos coordenadas."""
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


def score_competencia(competitors: list, radius: int) -> tuple[int, str, str]:
    """Calcula score de competencia. Devuelve (score 0-100, semáforo, descripción)."""
    n = len(competitors)
    ratings = [p.get("rating", 0) for p in competitors if p.get("rating")]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0

    density = n / (math.pi * (radius/1000)**2)  # locales por km²

    if density < 2:
        color = "green"; desc = f"{n} competidores en el radio — zona con baja saturación"
        score = 85
    elif density < 5:
        if avg_rating < 3.8:
            color = "yellow"; desc = f"{n} competidores, rating promedio bajo ({avg_rating:.1f}⭐) — oportunidad de diferenciación"
            score = 70
        else:
            color = "yellow"; desc = f"{n} competidores bien posicionados ({avg_rating:.1f}⭐) — mercado activo"
            score = 55
    else:
        if avg_rating < 3.5:
            color = "yellow"; desc = f"Alta densidad ({n} locales) pero calidad mediocre ({avg_rating:.1f}⭐) — oportunidad para un operador de calidad"
            score = 60
        else:
            color = "red"; desc = f"Zona saturada: {n} competidores con buen rating ({avg_rating:.1f}⭐)"
            score = 25

    return score, color, desc


def score_transporte(stops: list, radius: int) -> tuple[int, str, str]:
    n = len(stops)
    if n >= 4:
        return 90, "green", f"{n} paradas de transporte en el radio — excelente accesibilidad"
    elif n >= 2:
        return 65, "yellow", f"{n} paradas de transporte — accesibilidad media"
    elif n == 1:
        return 40, "yellow", "Solo 1 parada cercana — accesibilidad limitada"
    else:
        return 15, "red", "Sin transporte público identificado en el radio"


def score_alquiler(barrio: str, rubro: str) -> tuple[int, str, str, int]:
    """Score basado en tabla estática. Devuelve (score, color, desc, precio_m2)."""
    data = BARRIOS_DATA.get(barrio, BARRIOS_DATA.get("_default"))
    precio = data["alquiler_m2"]
    categoria = data["categoria"]  # premium / medio / economico

    if categoria == "premium":
        color = "red"; score = 35
        desc = f"Zona premium · ~${precio:,}/m² — alquiler alto, evaluar bien el volumen esperado"
    elif categoria == "medio":
        color = "yellow"; score = 65
        desc = f"Zona de valor medio · ~${precio:,}/m² — relación riesgo/costo razonable"
    else:
        color = "green"; score = 85
        desc = f"Zona accesible · ~${precio:,}/m² — bajo costo de entrada"

    return score, color, desc, precio


def score_demografia(barrio: str, rubro: str) -> tuple[int, str, str]:
    data = BARRIOS_DATA.get(barrio, BARRIOS_DATA.get("_default"))
    nse = data["nse"]  # alto / medio_alto / medio / bajo
    densidad = data["densidad"]  # alta / media / baja

    # Rubros que prefieren NSE alto
    rubros_premium = ["restaurant", "cafeteria", "cafe", "joyeria", "ropa", "indumentaria", "gym", "fitness"]
    rubros_popular = ["almacen", "ferreteria", "verduleria", "carniceria", "lavanderia", "farmacia"]

    rubro_lower = rubro.lower()
    es_premium = any(r in rubro_lower for r in rubros_premium)
    es_popular = any(r in rubro_lower for r in rubros_popular)

    if densidad == "alta":
        base_score = 80
    elif densidad == "media":
        base_score = 60
    else:
        base_score = 40

    if (es_premium and nse in ["alto", "medio_alto"]) or (es_popular and nse in ["medio", "bajo"]):
        score = min(base_score + 15, 95)
        color = "green"
        desc = f"Perfil del barrio compatible con el rubro · NSE {nse.replace('_', ' ')}, densidad {densidad}"
    elif (es_premium and nse == "bajo") or (es_popular and nse == "alto"):
        score = max(base_score - 20, 20)
        color = "red"
        desc = f"Posible desajuste entre rubro y perfil socioeconómico del barrio ({nse.replace('_', ' ')})"
    else:
        score = base_score
        color = "yellow" if base_score < 70 else "green"
        desc = f"Barrio de perfil {nse.replace('_', ' ')}, densidad {densidad}"

    return score, color, desc


def global_score(scores: list[int], weights: list[float]) -> int:
    return round(sum(s * w for s, w in zip(scores, weights)))


def get_key_insights(c_comp, c_trans, c_alq, c_demo, score_total) -> list[dict]:
    """Genera insights basados en reglas según los colores de cada capa."""
    insights = []

    # Insight principal según score global
    if score_total >= 70:
        insights.append({"icon": "✅", "text": "La ubicación presenta condiciones favorables para abrir el local."})
    elif score_total >= 45:
        insights.append({"icon": "⚠️", "text": "La ubicación tiene potencial pero requiere análisis más profundo antes de decidir."})
    else:
        insights.append({"icon": "❌", "text": "La ubicación presenta factores de riesgo importantes. Considerá otras opciones."})

    # Competencia
    if c_comp == "green":
        insights.append({"icon": "🏪", "text": "Baja competencia directa en el radio — ventana de oportunidad para posicionarse."})
    elif c_comp == "yellow":
        insights.append({"icon": "🏪", "text": "Competencia moderada — la diferenciación en calidad o propuesta será clave."})
    else:
        insights.append({"icon": "🏪", "text": "Zona saturada del rubro — necesitás una propuesta muy diferenciada para competir."})

    # Transporte
    if c_trans == "green":
        insights.append({"icon": "🚌", "text": "Excelente acceso en transporte público — favorece el flujo de clientes."})
    elif c_trans == "red":
        insights.append({"icon": "🚌", "text": "Poca accesibilidad en transporte — el negocio dependerá más de clientes del barrio."})

    # Alquiler
    if c_alq == "red":
        insights.append({"icon": "💰", "text": "Alquiler alto para la zona — asegurate de proyectar bien el volumen de ventas necesario."})
    elif c_alq == "green":
        insights.append({"icon": "💰", "text": "Costo de entrada bajo — margen favorable para cubrir el punto de equilibrio."})

    # Demografía
    if c_demo == "red":
        insights.append({"icon": "👥", "text": "El perfil del barrio no matchea bien con el rubro — revisá si el público objetivo está en la zona."})
    elif c_demo == "green":
        insights.append({"icon": "👥", "text": "El perfil socioeconómico del barrio es compatible con el rubro."})

    # Combinaciones especiales
    if c_comp == "red" and c_alq == "red":
        insights.append({"icon": "🔴", "text": "Zona de alta competencia Y alquiler caro: combinación de mayor riesgo."})
    if c_comp == "green" and c_alq == "green":
        insights.append({"icon": "🟢", "text": "Baja competencia con alquiler accesible: combinación ideal para entrada al mercado."})

    return insights


def build_map(lat, lng, radius, competitors, transit_stops):
    """Construye el mapa Folium."""
    m = folium.Map(
        location=[lat, lng],
        zoom_start=15,
        tiles="CartoDB dark_matter"
    )

    # Radio
    folium.Circle(
        location=[lat, lng],
        radius=radius,
        color="#c8f065",
        fill=True,
        fill_opacity=0.08,
        weight=1.5
    ).add_to(m)

    # Punto central
    folium.CircleMarker(
        location=[lat, lng],
        radius=10,
        color="#c8f065",
        fill=True,
        fill_color="#c8f065",
        fill_opacity=0.9,
        popup="📍 Dirección analizada"
    ).add_to(m)

    # Competidores
    for p in competitors[:20]:
        ploc = p.get("geometry", {}).get("location", {})
        if ploc:
            rating = p.get("rating", "N/D")
            folium.CircleMarker(
                location=[ploc["lat"], ploc["lng"]],
                radius=6,
                color="#f06060",
                fill=True,
                fill_color="#f06060",
                fill_opacity=0.7,
                popup=f"🏪 {p.get('name', '')}<br>⭐ {rating}"
            ).add_to(m)

    # Transporte
    seen = set()
    for s in transit_stops[:15]:
        sloc = s.get("geometry", {}).get("location", {})
        key = (round(sloc.get("lat", 0), 5), round(sloc.get("lng", 0), 5))
        if sloc and key not in seen:
            seen.add(key)
            folium.CircleMarker(
                location=[sloc["lat"], sloc["lng"]],
                radius=5,
                color="#60b4f0",
                fill=True,
                fill_color="#60b4f0",
                fill_opacity=0.8,
                popup=f"🚌 {s.get('name', 'Parada')}"
            ).add_to(m)

    return m


# ─── UI ─────────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero">
    <p class="hero-title">Local<span>Scope</span></p>
    <p class="hero-sub">Análisis de viabilidad comercial · Ciudad Autónoma de Buenos Aires</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar: API Keys ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuración")
    st.markdown("---")
    google_key = st.text_input("Google Places API Key", type="password", help="Obtenés tu clave en console.cloud.google.com")
    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.8rem; color:#666; line-height:1.6'>
    <b style='color:#888'>Leyenda del mapa</b><br>
    🟢 Dirección analizada<br>
    🔴 Competidores del rubro<br>
    🔵 Transporte público
    </div>
    """, unsafe_allow_html=True)

# ── Input Form ─────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([3, 2, 1])

with col1:
    direccion = st.text_input("📍 Dirección", placeholder="Ej: Av. Corrientes 1500, CABA")

with col2:
    rubro = st.text_input("🏪 Rubro del negocio", placeholder="Ej: cafetería, ferretería, ropa")

with col3:
    radio = st.slider("Radio (m)", min_value=200, max_value=1500, value=500, step=100)

st.markdown("<br>", unsafe_allow_html=True)
analizar = st.button("🔍 Analizar ubicación")

# ── Analysis ──────────────────────────────────────────────────────────────────
if analizar:
    if not google_key:
        st.error("⚠️ Ingresá tu Google Places API key en el panel lateral para continuar.")
        st.stop()
    if not direccion or not rubro:
        st.error("⚠️ Completá la dirección y el rubro.")
        st.stop()

    with st.spinner("Analizando ubicación..."):

        # 1. Geocodificar
        coords = geocode_address(direccion, google_key)
        if not coords:
            st.error("No se pudo geocodificar la dirección. Verificá que sea una dirección válida de CABA.")
            st.stop()

        lat, lng = coords["lat"], coords["lng"]

        # 2. Buscar datos en paralelo
        competitors = search_places(lat, lng, radio, rubro, "establishment", google_key)
        transit = get_transit_stops(lat, lng, radio, google_key)
        barrio = get_barrio_from_coords(lat, lng) or "Palermo"  # fallback

        # 3. Calcular scores
        s_comp, c_comp, d_comp = score_competencia(competitors, radio)
        s_trans, c_trans, d_trans = score_transporte(transit, radio)
        s_alq, c_alq, d_alq, precio_m2 = score_alquiler(barrio, rubro)
        s_demo, c_demo, d_demo = score_demografia(barrio, rubro)

        score_total = global_score(
            [s_comp, s_trans, s_alq, s_demo],
            [0.35, 0.20, 0.25, 0.20]
        )

        # 4. Insights basados en reglas
        insights = get_key_insights(c_comp, c_trans, c_alq, c_demo, score_total)

    # ── Layout de resultados ──────────────────────────────────────────────────
    st.markdown(f"<div style='color:#666; font-size:0.85rem; margin-bottom:1.5rem'>📌 {coords['formatted']} · Barrio: <b style='color:#aaa'>{barrio}</b></div>", unsafe_allow_html=True)

    left, right = st.columns([2, 3])

    with left:
        # Score global
        if score_total >= 70:
            emoji = "✅"; label = "Viable"
        elif score_total >= 45:
            emoji = "⚠️"; label = "Análisis requerido"
        else:
            emoji = "❌"; label = "Alto riesgo"

        st.markdown(f"""
        <div class="score-card">
            <h4>Score de viabilidad</h4>
            <div class="value">{score_total}</div>
            <div class="label">{emoji} {label}</div>
        </div>
        """, unsafe_allow_html=True)

        # Capas
        def dot_html(color):
            return f'<span class="dot {color}"></span>'

        def layer_card(title, dot_color, value, detail):
            return f"""
            <div class="layer-card">
                <div class="layer-title">{dot_html(dot_color)} {title}</div>
                <div class="layer-value">{value}</div>
                <div class="layer-detail">{detail}</div>
            </div>
            """

        st.markdown(layer_card(
            "Competencia",
            c_comp,
            f"{len(competitors)} locales en {radio}m",
            d_comp
        ), unsafe_allow_html=True)

        st.markdown(layer_card(
            "Transporte público",
            c_trans,
            f"{len(set(s.get('place_id') for s in transit))} paradas",
            d_trans
        ), unsafe_allow_html=True)

        st.markdown(layer_card(
            "Alquiler estimado",
            c_alq,
            f"~${precio_m2:,} / m²",
            d_alq
        ), unsafe_allow_html=True)

        st.markdown(layer_card(
            "Demografía del barrio",
            c_demo,
            barrio,
            d_demo
        ), unsafe_allow_html=True)

    with right:
        # Mapa
        mapa = build_map(lat, lng, radio, competitors, transit)
        st_folium(mapa, width=None, height=420)

        # Insights
        st.markdown("<br>", unsafe_allow_html=True)
        insights_html = "".join([
            f'<div style="display:flex;gap:0.8rem;align-items:flex-start;margin-bottom:0.8rem">'
            f'<span style="font-size:1.1rem;flex-shrink:0">{i["icon"]}</span>'
            f'<span style="font-size:0.9rem;color:#bbb;line-height:1.5">{i["text"]}</span>'
            f'</div>'
            for i in insights
        ])
        st.markdown(f"""
        <div class="analysis-box">
            <div style="font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; color:#c8f065; margin-bottom:1rem; font-weight:600">✦ Puntos clave</div>
            {insights_html}
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style='text-align:center; padding:4rem 2rem; color:#444'>
        <div style='font-size:3rem; margin-bottom:1rem'>🗺️</div>
        <div style='font-family:"DM Serif Display",serif; font-size:1.4rem; color:#666'>Ingresá una dirección y un rubro para comenzar</div>
        <div style='font-size:0.85rem; margin-top:0.5rem'>Colocá tus API keys en el panel lateral ←</div>
    </div>
    """, unsafe_allow_html=True)
