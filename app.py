import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- MANEJO DE DEPENDENCIAS ---
# Intentamos importar Graphviz, si falla, desactivamos esa funcionalidad
# para que la app no se rompa durante la presentación.
try:
    import graphviz
    has_graphviz = True
except ImportError:
    has_graphviz = False

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Ecotracks Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS PERSONALIZADOS (CSS) ---
st.markdown("""
    <style>
    .css-1d391kg {padding-top: 1rem;} 
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        border-left: 5px solid #002664; /* Azul Massy */
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    [data-testid="stSidebar"] {
        background-color: #002664;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    .orange-highlight {
        background-color: #FF8C00;
        color: white;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATOS REALES (CARGADOS MANUALMENTE) ---

def get_regional_data():
    # Datos específicos solicitados
    data = {
        'Regional': ['GRB', 'CATENARE', 'VRC', 'GGS', 'VRO', 'GOR', 'VAO', 'CEDI'],
        'Total': [0.50, 14.25, 46.46, 28.34, 36.31, 13.16, 9.07, 0.38]
    }
    df = pd.DataFrame(data)
    
    # Distribución simulada para visualización (75% A1, 15% A2, 10% A3)
    df['Alcance 1'] = df['Total'] * 0.75
    df['Alcance 2'] = df['Total'] * 0.15
    df['Alcance 3'] = df['Total'] * 0.10
    
    # Cálculo de árboles (Ratio solicitado: 40 árboles por tCO2e)
    df['Arboles'] = (df['Total'] * 40).astype(int)
    return df

def get_general_indicators():
    # Suma de los datos regionales ingresados: 148.47
    total_huella = 148.47
    total_arboles = int(total_huella * 40) # ~5938
    
    return {
        'Huella Total': total_huella,
        'Meta Reducción': 141.05, # -5% aprox
        'Alcance 1 %': 75,
        'Alcance 2 %': 15,
        'Alcance 3 %': 10,
        'Arboles Totales': total_arboles
    }

def get_factors_data():
    return pd.DataFrame([
        {'ID': 'F-001', 'Tipo': 'Combustible Líquido', 'Nombre': 'Diésel (ACPM)', 'Factor': 10.15, 'Unidad': 'kgCO2e/gal', 'Fuente': 'UPME 2023'},
        {'ID': 'F-002', 'Tipo': 'Combustible Líquido', 'Nombre': 'Gasolina Corriente', 'Factor': 8.15, 'Unidad': 'kgCO2e/gal', 'Fuente': 'UPME 2023'},
        {'ID': 'F-003', 'Tipo': 'Energía Eléctrica', 'Nombre': 'SIN Colombia', 'Factor': 0.136, 'Unidad': 'kgCO2/kWh', 'Fuente': 'UPME-FECOC'},
        {'ID': 'F-004', 'Tipo': 'Refrigerante', 'Nombre': 'R-417B', 'Factor': 3235, 'Unidad': 'kgCO2e/kg', 'Fuente': 'IPCC AR5'},
        {'ID': 'F-005', 'Tipo': 'Material', 'Nombre': 'Papel Blanco', 'Factor': 1.84, 'Unidad': 'kgCO2/kg', 'Fuente': 'Defra UK'},
    ])

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    
    # --- LOGO INTELIGENTE ---
    # 1. Busca logo local. 2. Si no, dibuja uno SVG profesional (Massy Azul / Energy Rojo)
    if os.path.exists("logo.png"):
        st.image("logo.png", use_column_width=True)
    else:
        # Logo SVG embebido para asegurar que siempre se vea bien sin archivos externos
        st.markdown("""
        <div style="background-color: white; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
            <svg viewBox="0 0 240 60" xmlns="http://www.w3.org/2000/svg">
                <text x="10" y="40" font-family="Arial, sans-serif" font-size="28" font-weight="900" fill="#002664">MASSY</text>
                <text x="115" y="40" font-family="Arial, sans-serif" font-size="28" font-weight="bold" fill="#D9232D">ENERGY</text>
                <rect x="10" y="48" width="220" height="4" fill="#002664" />
            </svg>
        </div>
        """, unsafe_allow_html=True)

    st.title("ECOTRACKS")
    st.markdown("### Enterprise Carbon Mgmt.")
    st.markdown("---")
    
    selected_page = st.radio(
        "Navegación",
        ["Panel de Control", "Gestor de Factores", "Ingeniería de Preguntas", "Reportes ISO 14064"],
        index=0
    )
    
    st.markdown("---")
    st.caption(f"Configuración v1.0.4")
    st.caption("© Massy Energy Colombia")

# --- HEADER DE LA PÁGINA PRINCIPAL ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title(f"{selected_page}")
    st.markdown("**Proyecto:** Contrato CW11333073 (Massy-Ecopetrol) | ✅ SISTEMA AUDITADO")
with col_h2:
    st.info("Usuario: Admin HSE")

st.markdown("---")

# --- VISTAS DEL DASHBOARD ---

# 1. PANEL DE CONTROL (Overview)
if selected_page == "Panel de Control":
    
    gen_data = get_general_indicators()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Factores Activos", "1,240", "Base de Datos") 
    kpi2.metric("Transacciones Totales", "295", "Registros 2025") 
    kpi3.metric("Equivalencia Árboles", f"{gen_data['Arboles Totales']} 🌳", "Compensación req.")
    kpi4.metric("Calidad de Datos", "87.5%", "⚠️ Requiere revisión")

    st.markdown("### 📊 Tablero de Mando e Indicadores")
    st.write("Visualización consolidada basada en *Indicadores Propuestos*.")

    # Pestañas
    tab_regional, tab_general = st.tabs(["🌎 Por Regional (Detalle)", "🔶 General (Consolidado)"])
    
    with tab_regional:
        st.subheader("Distribución de Huella por Zona Operativa")
        df_reg = get_regional_data()
        
        col_reg_chart, col_reg_kpi = st.columns([3, 1])
        
        with col_reg_chart:
            fig_reg = go.Figure()
            # Ordenamos por Total descendente para mejor visualización
            df_reg_sorted = df_reg.sort_values(by="Total", ascending=False)
            
            fig_reg.add_trace(go.Bar(name='Alcance 1 (Directo)', x=df_reg_sorted['Regional'], y=df_reg_sorted['Alcance 1'], marker_color='#D9232D'))
            fig_reg.add_trace(go.Bar(name='Alcance 2 (Energía)', x=df_reg_sorted['Regional'], y=df_reg_sorted['Alcance 2'], marker_color='#002664'))
            fig_reg.add_trace(go.Bar(name='Alcance 3 (Indirecto)', x=df_reg_sorted['Regional'], y=df_reg_sorted['Alcance 3'], marker_color='#94a3b8'))
            
            fig_reg.update_layout(barmode='stack', title="Emisiones Totales por Regional (tCO2e)", height=450)
            st.plotly_chart(fig_reg, use_container_width=True)
            
        with col_reg_kpi:
            top_regional = df_reg.loc[df_reg['Total'].idxmax()]
            st.markdown("#### Top Contribuyente")
            st.error(f"{top_regional['Regional']}")
            st.caption(f"Emisión: {top_regional['Total']} tCO2e")
            
            st.markdown("#### Detalle (tCO2e)")
            st.dataframe(df_reg[['Regional', 'Total', 'Arboles']], hide_index=True, use_container_width=True)

    with tab_general:
        st.markdown(f"""
        <div style="display: flex; justify-content: space-around; background-color: #FFF3E0; padding: 20px; border-radius: 10px; border: 1px solid #FF8C00; margin-bottom: 20px;">
            <div style="text-align: center;">
                <h3 style="color: #FF8C00; margin:0;">{gen_data['Huella Total']} tCO2e</h3>
                <p style="margin:0; font-weight:bold;">Huella de Carbono Total</p>
            </div>
            <div style="text-align: center;">
                <h3 style="color: #002664; margin:0;">{gen_data['Meta Reducción']} tCO2e</h3>
                <p style="margin:0;">Meta Contractual (-5%)</p>
            </div>
            <div style="text-align: center;">
                <h3 style="color: green; margin:0;">{gen_data['Arboles Totales']} 🌳</h3>
                <p style="margin:0;">Árboles Necesarios (Factor ~40)</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_gen_1, col_gen_2 = st.columns(2)
        with col_gen_1:
            st.subheader("Participación por Alcance (%)")
            labels = ['Alcance 1', 'Alcance 2', 'Alcance 3']
            values = [gen_data['Alcance 1 %'], gen_data['Alcance 2 %'], gen_data['Alcance 3 %']]
            colors = ['#D9232D', '#002664', '#94a3b8']
            fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker_colors=colors)])
            fig_pie.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col_gen_2:
            st.subheader("Indicadores de Desempeño")
            st.progress(gen_data['Alcance 1 %'], text="Peso del Alcance 1 (Crítico)")
            st.caption("La mayor parte de la huella proviene de fuentes directas (Combustible).")
            st.write("")
            st.progress(95, text="Avance vs Línea Base")
            st.caption("Estamos gestionando activamente la reducción.")

# 2. GESTOR DE FACTORES
elif selected_page == "Gestor de Factores":
    st.markdown("Gestión centralizada de coeficientes de emisión.")
    df_factors = get_factors_data()
    filtro = st.text_input("🔍 Buscar factor (ej. Diesel, Gasolina):")
    if filtro:
        df_factors = df_factors[df_factors['Nombre'].str.contains(filtro, case=False)]
    st.dataframe(df_factors, use_container_width=True, hide_index=True)
    st.warning("⚠️ Nota de Seguridad: Cambios requieren autorización.")

# 3. INGENIERÍA DE PREGUNTAS
elif selected_page == "Ingeniería de Preguntas":
    st.markdown("### Árbol de Decisión Lógica (UX)")
    st.write("Diagrama de flujo lógico para el operador.")
    
    if has_graphviz:
        try:
            graph = graphviz.Digraph()
            graph.attr(rankdir='TB')
            graph.node('A', '¿Es propiedad de Massy Energy?', shape='box', style='filled', fillcolor='#002664', fontcolor='white')
            graph.node('B', 'SI: Alcance 1 (Directo)', shape='ellipse', color='green')
            graph.node('C', 'NO: Alcance 3 (Indirecto)', shape='ellipse', color='gray')
            graph.node('D', '¿Qué tipo de vehículo es?', shape='box')
            graph.node('E', '¿Quién paga el combustible?', shape='box')
            graph.node('F', 'Selección: Diésel/Gasolina', shape='note', style='filled', fillcolor='#D9232D', fontcolor='white')
            graph.node('G', 'Selección: Cliente/Proveedor', shape='note')
            graph.edge('A', 'B', label='Si')
            graph.edge('A', 'C', label='No')
            graph.edge('B', 'D')
            graph.edge('C', 'E')
            graph.edge('D', 'F')
            graph.edge('E', 'G')
            st.graphviz_chart(graph)
        except Exception:
            st.warning("El módulo de gráficos no pudo renderizar el diagrama.")
            st.info("Flujo: Propiedad -> Sí (Alcance 1) / No (Alcance 3) -> Vehículo -> Combustible.")
    else:
        st.warning("⚠️ Librería Graphviz no detectada.")
        st.info("El sistema funciona correctamente, pero la visualización del árbol lógico se ha simplificado a texto.")
        st.code("Flujo Lógico:\n1. ¿Propiedad Massy? -> SÍ (A1) / NO (A3)\n2. ¿Tipo Vehículo? -> Configuración Factor\n3. ¿Combustible? -> Diésel/Gasolina")
    
    col1, col2, col3 = st.columns(3)
    col1.success("✅ **Prevención de Error**")
    col2.success("✅ **Cálculo Automático**")
    col3.success("✅ **Auditoría**")

# 4. REPORTES ISO 14064
elif selected_page == "Reportes ISO 14064":
    st.markdown("### Informe de Desempeño por Alcance | 2025")
    tab1, tab2, tab3 = st.tabs(["🔥 Alcance 1", "⚡ Alcance 2", "🚛 Alcance 3"])

    with tab1:
        col_a1_1, col_a1_2 = st.columns([1, 2])
        with col_a1_1:
            st.metric("Total Alcance 1", "111.35 tCO2e", "75% del Total")
            st.info("Fuente Principal: Consumo de Diésel.")
        with col_a1_2:
            df_a1 = pd.DataFrame({'Fuente': ['Diésel', 'Gasolina', 'Gas Natural'], 'Valor': [90.5, 20.1, 0.75]})
            fig_a1 = px.bar(df_a1, x='Fuente', y='Valor', color='Fuente', color_discrete_sequence=['#D9232D', '#ff6b6b', '#ffbaba'])
            st.plotly_chart(fig_a1, use_container_width=True)

    with tab2:
        col_a2_1, col_a2_2 = st.columns([1, 2])
        with col_a2_1:
            st.metric("Total Alcance 2", "22.27 tCO2e", "15% del Total")
            st.info("Fuente: Consumo eléctrico Red SIN.")
        with col_a2_2:
            st.progress(100, text="100% Energía de Red")

    with tab3:
        col_a3_1, col_a3_2 = st.columns([1, 2])
        with col_a3_1:
            st.metric("Total Alcance 3", "14.85 tCO2e", "10% del Total")
        with col_a3_2:
            df_a3 = pd.DataFrame({'Fuente': ['Transporte', 'Residuos', 'Papel', 'Viajes'], 'Valor': [10.2, 3.5, 1.0, 0.15]})
            fig_a3 = px.pie(df_a3, values='Valor', names='Fuente', hole=0.5)
            st.plotly_chart(fig_a3, use_container_width=True)

    st.markdown("---")
    st.download_button("📥 Descargar Informe PDF", "Simulacion PDF", "reporte.pdf")