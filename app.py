import streamlit as st
from streamlit_folium import folium_static
import folium
import geopandas as gpd
from folium.plugins import Fullscreen 


st.set_page_config(layout="wide")
# Caminho para o arquivo GeoJSON
mun_path = "data/mun_adesao2.geojson"
mun_out_path = "data/mun_out.geojson"
mun_sabesp_path = "data/mun_sabesp.geojson"

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
    gdf_out = load_geojson(mun_out_path)
    gdf_sabesp = load_geojson(mun_sabesp_path)

    # Criar o mapa com folium
    m = folium.Map(location=[-22.245, -48.669], zoom_start=6.5, tiles='CartoDB positron')


    Fullscreen(position='topright').add_to(m)

    # Criar camadas para cada GeoJSON
    adesao_layer = folium.FeatureGroup(name="Municípios Universaliza SP", show=True)
    out_layer = folium.FeatureGroup(name="Municípios Fora", show=True)
    sabesp_layer = folium.FeatureGroup(name="Municípios SABESP", show=True)


    # Adicionar os dados GeoJSON ao mapa com hover e popup
    folium.GeoJson(
        gdf,
        style_function=lambda feature: {
            'fillColor': 'green',  
            'color': 'green',      
            'weight': 2,     
            'fillOpacity': 0.5    
        },
            highlight_function=lambda feature: {
            'fillColor': 'red',             
            'color': 'red',                
            'weight': 3,                     
            'fillOpacity': 0.7           
            },

        tooltip=folium.GeoJsonTooltip(
            fields=['NOME'],  
            aliases=['Nome:'],  
            localize=True
        ),
        popup=folium.GeoJsonPopup(
            fields=['NOME', 'mun_adesao_UGRHI', 'mun_adesao_Data Adesão', 'mun_adesao_Populacao  Estimada', 'csvjson_Classificação Manancial', 'csvjson_Classificação Sistema Produtor', 'csvjson_Eficiência da Produção de Água', 'csvjson_Perdas', 'csvjson_Cobertura','csvjson_Eficiência da Distribuição de Água', 'csvjson_ISH-U', 'csvjson_População Urbana 2020', 'csvjson_População Urbana 2035', 'csvjson_Demanda Urbana 2020 (litros/s)', 'csvjson_Demanda Urbana 2035 (litros/s)', 'csvjson_Operador Oficial', 'csvjson_Tipo Operador', 'csvjson_Sistema(s) Produtor(es)', 'csvjson_Tipo Sistema(s)', 'csvjson_Manancial(is) de Abastecimento', 'csvjson_Tipo Manancial(is)', 'csvjson_URAE', 'csvjson_reg_administrativa', 'csvjson_reg_metropolitanas'],  # Campos no popup
            aliases=['Nome: ', 'UGRHI: ', 'Data Adesão: ', 'População Estimada: ', 'Classificação Manancial: ', 'Classificação Sistema Produtor: ', 'Eficiência da Produção de Água: ', 'Perdas: ', 'Cobertura: ', 'Eficiência da Distribuição de Água:', 'ISH-U: ', 'População Urbana 2020: ', 'População Urbana 2035: ', 'Demanda Urbana 2020 (litros/s): ', 'Demanda Urbana 2035 (litros/s): ', 'Operador Oficial: ', 'Tipo Operador: ', 'Sistema(s) Produtor(es): ', 'Tipo Sistema(s): ', 'Manancial(is) de Abastecimento: ', 'Tipo Manancial(is): ', 'URAE: ', 'Região Administrativa: ', 'Região Metropolitana: '],  # Aliases para o popup
            localize=True
        )
    ).add_to(adesao_layer)

    folium.GeoJson(
            gdf_out,
            style_function=lambda feature: {
            'fillColor': 'red',
            'color': 'red',
            'weight': 2,
            'fillOpacity': 0.5
            },
            tooltip=folium.GeoJsonTooltip(fields=['NOME'], aliases=['Nome:'],localize=True),
            popup=folium.GeoJsonPopup(
            fields=['NOME', 'csvjson_Classificação Manancial', 'csvjson_Classificação Sistema Produtor', 'csvjson_Eficiência da Produção de Água', 'csvjson_Perdas', 'csvjson_Cobertura','csvjson_Eficiência da Distribuição de Água', 'csvjson_ISH-U', 'csvjson_População Urbana 2020', 'csvjson_População Urbana 2035', 'csvjson_Demanda Urbana 2020 (litros/s)', 'csvjson_Demanda Urbana 2035 (litros/s)', 'csvjson_Operador Oficial', 'csvjson_Tipo Operador', 'csvjson_Sistema(s) Produtor(es)', 'csvjson_Tipo Sistema(s)', 'csvjson_Manancial(is) de Abastecimento', 'csvjson_Tipo Manancial(is)', 'csvjson_URAE', 'csvjson_reg_administrativa', 'csvjson_reg_metropolitanas'],  # Campos no popup
            aliases=['Nome: ', 'Classificação Manancial: ', 'Classificação Sistema Produtor: ', 'Eficiência da Produção de Água: ', 'Perdas: ', 'Cobertura: ', 'Eficiência da Distribuição de Água:', 'ISH-U: ', 'População Urbana 2020: ', 'População Urbana 2035: ', 'Demanda Urbana 2020 (litros/s): ', 'Demanda Urbana 2035 (litros/s): ', 'Operador Oficial: ', 'Tipo Operador: ', 'Sistema(s) Produtor(es): ', 'Tipo Sistema(s): ', 'Manancial(is) de Abastecimento: ', 'Tipo Manancial(is): ', 'URAE: ', 'Região Administrativa: ', 'Região Metropolitana: '],  # Aliases para o popup
            localize=True
        )).add_to(out_layer)

    folium.GeoJson(
        gdf_sabesp,
        style_function=lambda feature: {
            'fillColor': 'blue',
            'color': 'blue',
            'weight': 2,
            'fillOpacity': 0.5
        },
                    tooltip=folium.GeoJsonTooltip(fields=['NOME'], aliases=['Nome:'],localize=True),
            popup=folium.GeoJsonPopup(
            fields=['NOME', 'csvjson_Classificação Manancial', 'csvjson_Classificação Sistema Produtor', 'csvjson_Eficiência da Produção de Água', 'csvjson_Perdas', 'csvjson_Cobertura','csvjson_Eficiência da Distribuição de Água', 'csvjson_ISH-U', 'csvjson_População Urbana 2020', 'csvjson_População Urbana 2035', 'csvjson_Demanda Urbana 2020 (litros/s)', 'csvjson_Demanda Urbana 2035 (litros/s)', 'csvjson_Operador Oficial', 'csvjson_Tipo Operador', 'csvjson_Sistema(s) Produtor(es)', 'csvjson_Tipo Sistema(s)', 'csvjson_Manancial(is) de Abastecimento', 'csvjson_Tipo Manancial(is)', 'csvjson_URAE', 'csvjson_reg_administrativa', 'csvjson_reg_metropolitanas'],  # Campos no popup
            aliases=['Nome: ', 'Classificação Manancial: ', 'Classificação Sistema Produtor: ', 'Eficiência da Produção de Água: ', 'Perdas: ', 'Cobertura: ', 'Eficiência da Distribuição de Água:', 'ISH-U: ', 'População Urbana 2020: ', 'População Urbana 2035: ', 'Demanda Urbana 2020 (litros/s): ', 'Demanda Urbana 2035 (litros/s): ', 'Operador Oficial: ', 'Tipo Operador: ', 'Sistema(s) Produtor(es): ', 'Tipo Sistema(s): ', 'Manancial(is) de Abastecimento: ', 'Tipo Manancial(is): ', 'URAE: ', 'Região Administrativa: ', 'Região Metropolitana: '],  # Aliases para o popup
            localize=True)
    ).add_to(sabesp_layer)

    adesao_layer.add_to(m)
    sabesp_layer.add_to(m)
    out_layer.add_to(m)

    folium.LayerControl().add_to(m)

    # Exibir o mapa como estático
    folium_static(m, width=800, height=700)

except FileNotFoundError:
    st.error(f"Arquivo GeoJSON não encontrado no caminho: {mun_path}")
except ValueError as ve:
    st.error(f"Erro nos dados GeoJSON: {ve}")
except Exception as e:
    st.error(f"Erro ao carregar o GeoJSON: {e}")
