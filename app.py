import streamlit as st
from supabase import create_client
from datetime import datetime, timedelta

# 1. Configuración de conexión (usando los Secrets de Streamlit)
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# 2. Función para liberar boletos expirados
def liberar_boletos_expirados():
    limit_time = datetime.now() - timedelta(hours=1)
    supabase.table("tickets").update({"status": "disponible", "apartado_at": None})\
        .eq("status", "apartado")\
        .lt("apartado_at", limit_time.isoformat())\
        .execute()

# 3. Lógica principal de la interfaz
st.title("Rifa JR - Selección de Boletos")

# Ejecutar limpieza antes de mostrar los datos
liberar_boletos_expirados()

# Obtener boletos de la base de datos
response = supabase.table("tickets").select("*").order("id").execute()
tickets = response.data

# Mostrar boletos en una cuadrícula
cols = st.columns(10)
for i, ticket in enumerate(tickets):
    # Definir color del botón
    if ticket['status'] == 'disponible':
        color = "green"
        if cols[i % 10].button(f"{ticket['id']}", key=f"btn_{ticket['id']}"):
            # Lógica de apartado
            supabase.table("tickets").update({
                "status": "apartado", 
                "apartado_at": datetime.now().isoformat()
            }).eq("id", ticket['id']).execute()
            st.rerun() # Reemplaza a experimental_rerun en versiones recientes
    else:
        cols[i % 10].button(f"{ticket['id']}", key=f"btn_{ticket['id']}", disabled=True)
