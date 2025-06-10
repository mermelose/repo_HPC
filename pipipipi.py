import streamlit as st
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Consulta de Teatros en MongoDB",
    page_icon="🎭",
    layout="centered"
)

# Título principal
st.title("Consulta de Teatros en MongoDB Atlas")

# Texto explicativo
st.markdown("""
Esta aplicación se conecta a una base de datos MongoDB Atlas y consulta información 
sobre teatros según la ciudad que especifiques.
""")

# Función para conectar a MongoDB (del archivo pipipi.py)
def connect_to_mongodb():
    """Connect to MongoDB Atlas using connection string"""
    load_dotenv()
    connection_string = os.environ.get("MONGODB_CONNECTION_STRING")

    if not connection_string:
        st.warning("Usando cadena de conexión hardcodeada (no seguro para producción)")
        username = "mermelose"
        password = "z03L0QimUfTTG7RE"
        cluster = "clus.vabbzew.mongodb.net"
        connection_string = f"mongodb+srv://{username}:{password}@{cluster}/"

    try:
        client = MongoClient(connection_string)
        return client
    except Exception as e:
        st.error(f"Error conectando a MongoDB Atlas: {e}")
        return None

# Función para consultar teatros (adaptada para Streamlit)
def query_theaters_by_city(city_name):
    """Query theaters in sample_mflix database by city name"""
    try:
        client = connect_to_mongodb()
        if not client:
            return None, 0

        db = client.sample_mflix
        theaters_collection = db.theaters

        query = {"location.address.city": city_name}
        theaters = list(theaters_collection.find(query).limit(10))
        total_count = theaters_collection.count_documents(query)

        client.close()
        return theaters, total_count

    except Exception as e:
        st.error(f"Error en la consulta: {e}")
        return None, 0

# Widget de entrada para la ciudad
city_name = st.text_input("Introduce el nombre de una ciudad para buscar teatros:", "Bismarck")

# Botón para ejecutar la consulta
if st.button("Buscar Teatros"):
    with st.spinner("Consultando la base de datos..."):
        theaters, total_count = query_theaters_by_city(city_name)
        
        if theaters is not None:
            st.success(f"Encontrados {total_count} teatros en {city_name}")
            st.subheader(f"Primeros {len(theaters)} resultados:")
            
            for i, theater in enumerate(theaters, 1):
                with st.expander(f"Theater #{i}: ID {theater.get('theaterId')}"):
                    st.write(f"**Dirección:** {theater.get('location', {}).get('address', {}).get('street1')}")
                    st.write(f"**Ciudad:** {theater.get('location', {}).get('address', {}).get('city')}")
                    st.write(f"**Estado:** {theater.get('location', {}).get('address', {}).get('state')}")
                    st.write(f"**Código postal:** {theater.get('location', {}).get('address', {}).get('zipcode')}")
                    st.json(theater)  # Mostrar todos los datos en formato JSON

# Información adicional
st.markdown("---")
st.info("""
**Nota:** Esta aplicación usa la colección 'theaters' de la base de datos 
'sample_mflix' proporcionada por MongoDB Atlas.
""")