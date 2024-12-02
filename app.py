import streamlit as st
import folium
from streamlit_folium import folium_static
import geopandas as gpd

# Caminho para o arquivo GeoJSON
mun_path = "data/mun_adesao.geojson"
logo_path = "data/logo.png"
logo_univer_path = "data/logo_univers.png"

# Adicionar a imagem ao sidebar
st.sidebar.image(logo_path)
st.sidebar.image(logo_univer_path)

# Função para carregar o GeoJSON com cache
@st.cache_data
def load_geojson(path):
    """
    Carrega um GeoJSON e retorna um GeoDataFrame.
    Os dados são armazenados em cache para melhorar o desempenho.
    """
    gdf = gpd.read_file(path)
    
    # Garantir que o GeoDataFrame tenha uma coluna de geometria válida
    if 'geometry' not in gdf.columns:
        raise ValueError("O GeoJSON não possui uma coluna 'geometry'.")
    
    return gdf

# Aplicação principal
try:
    # Carregar os dados do GeoJSON
    gdf = load_geojson(mun_path)

    # Criar o mapa com folium
    m = folium.Map(location=[-22.245, -48.669], zoom_start=6.5, tiles='CartoDB positron')

    # Adicionar os dados GeoJSON ao mapa com hover e popup
    folium.GeoJson(
        gdf,
        style_function=lambda feature: {
            'fillColor': 'blue',  # Cor do preenchimento padrão
            'color': 'blue',      # Cor da borda padrão
            'weight': 2,          # Espessura da borda
            'fillOpacity': 0.5    # Opacidade do preenchimento
        },
        highlight_function=lambda feature: {
            'fillColor': 'red',  # Cor do preenchimento no hover
            'color': 'red',      # Cor da borda no hover
            'weight': 3,         # Espessura da borda no hover
            'fillOpacity': 0.7   # Opacidade do preenchimento no hover
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['NOME'],  # Campos selecionados
            aliases=['Nome:'],  # Aliases para hover
            localize=True
        ),
        popup=folium.GeoJsonPopup(
            fields=['NOME', 'mun_adesao_UGRHI'],  # Campos no popup
            aliases=['Nome:', 'UGRHI:'],  # Aliases para o popup
            localize=True
        )
    ).add_to(m)

    # Exibir o mapa como estático
    folium_static(m, width=800, height=700)

except FileNotFoundError:
    st.error(f"Arquivo GeoJSON não encontrado no caminho: {mun_path}")
except ValueError as ve:
    st.error(f"Erro nos dados GeoJSON: {ve}")
except Exception as e:
    st.error(f"Erro ao carregar o GeoJSON: {e}")
