from datetime import datetime, timedelta

# Liberar boletos apartados hace más de 1 hora
limit_time = datetime.now() - timedelta(hours=1)
supabase.table("tickets").update({"status": "disponible", "apartado_at": None})\
    .eq("status", "apartado").lt("apartado_at", limit_time.isoformat()).execute()

import os
import streamlit as st
from supabase import create_client

# Configuración segura: Streamlit buscará esto en sus "Secrets"
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("Rifa JR - Selección de Boletos")

# Obtener boletos de la base de datos
response = supabase.table("tickets").select("*").order("id").execute()
tickets = response.data

# Mostrar boletos en una cuadrícula
cols = st.columns(10) # 10 columnas para ver los números
for i, ticket in enumerate(tickets):
    color = "green" if ticket['status'] == 'disponible' else "red"
    if cols[i % 10].button(f"{ticket['id']}", key=ticket['id'], disabled=(ticket['status'] != 'disponible')):
        # Lógica de apartado
        supabase.table("tickets").update({"status": "apartado"}).eq("id", ticket['id']).execute()
        st.experimental_rerun()
