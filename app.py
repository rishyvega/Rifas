import streamlit as st
from supabase import create_client
from datetime import datetime, timedelta

# 1. Configuración de conexión
# Asegúrate de que los nombres de los Secrets sean exactamente iguales en Streamlit Cloud
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("Rifa JR - Selección de Boletos")

# 2. Intentamos la limpieza de boletos de forma segura
try:
    limit_time = datetime.now() - timedelta(hours=1)
    # Actualizamos boletos expirados
    supabase.table("tickets").update({"status": "disponible", "apartado_at": None})\
        .eq("status", "apartado")\
        .lt("apartado_at", limit_time.isoformat())\
        .execute()
except Exception:
    # Si hay error en la base de datos, simplemente continuamos para que la app cargue
    pass

# 3. Obtener boletos
try:
    response = supabase.table("tickets").select("*").order("id").execute()
    tickets = response.data
    
    # 4. Mostrar boletos
    cols = st.columns(10)
    for i, ticket in enumerate(tickets):
        status = ticket.get('status', 'disponible')
        if status == 'disponible':
            if cols[i % 10].button(f"{ticket['id']}", key=f"btn_{ticket['id']}"):
                supabase.table("tickets").update({
                    "status": "apartado", 
                    "apartado_at": datetime.now().isoformat()
                }).eq("id", ticket['id']).execute()
                st.rerun()
        else:
            cols[i % 10].button(f"{ticket['id']}", key=f"btn_{ticket['id']}", disabled=True)

except Exception as e:
    st.error(f"No se pudieron cargar los boletos: {e}")
