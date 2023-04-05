import numpy as np
import pandas as pd
import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
# import leafmap

st.set_page_config(page_title="Marine Spatial Planning Tool", layout="wide")
st.warning(":warning: This webapp is a dummy. It is not fully functional.")
st.title("Offshore wind Philippines")


@st.cache_data
def load_powerplants():
    return pd.read_csv("Data/global_power_plant_database.csv")

ppl = load_powerplants()
gdf = gpd.GeoDataFrame(ppl, geometry=gpd.points_from_xy(ppl.longitude, ppl.latitude))
gdf.set_crs("epsg:4326", inplace=True)

st.header("Map View")
st.markdown("In this web application you can view different map layers relevant to offshore wind. The button at the top right of the map allows for the selection of the map layers. For now, 3 layers are present.")

logoUrl = "https://www.betoniek.nl/library/article/WB%20png-1598871074.4599.png"


gebcoWMSurl = "https://www.gebco.net/data_and_products/gebco_web_services/web_map_service/mapserv?"
gebcoWMSLayer = "GEBCO_LATEST_2_sub_ice_topo"
gebcoWMSName = "GEBCO elevation"
phWmsUrl = "https://geoserver.geoportal.gov.ph/geoserver/ows?"
phWmsLayer = "geoportal:keybiodiversityareas_202005"
phWmsName = "Key Biodiversity Areas"
m = leafmap.Map(center=[14.597, 120.98], zoom=6, height=1200, widescreen=False)
m.add_wms_layer(phWmsUrl, layers=phWmsLayer, name=phWmsName, opacity = 0.5)
m.add_wms_layer(gebcoWMSurl, layers=gebcoWMSLayer, name=gebcoWMSName, opacity=0.5)
# m.add_raster("Data/PHL_wind-speed_100m.tif", colormap="terrain", layer_name="Wind Speed")

col1, col2 = st.columns(2)

with st.sidebar:
    st.image(logoUrl)
    st.title("Marine spatial planning tool for the Philippines")
    st.warning(":warning: This webapp is a dummy. It is not fully functional.")
    st.markdown("This webapp serves as an example to the UNOPS proposal on marine spatial planning for offshore energy in the Philippines. \n\r ToR reference: RFP/2023/45800 \r \r For more information in the proposed contents and functionalities of the MSP-tool, please refer the relevant section in the proposal. ")

with col1:

    st.subheader("Options")
    st.markdown(f"Add addtional map layers by WMS endpoint. For example the biodiversity areas from the geoportal:")
    inputUrl = st.text_input("Enter WMS url to add to the list", value=phWmsUrl)
    inputLayer = st.text_input("Enter WMS layer to add to the list", value=phWmsLayer)
    st.markdown("This functionality allows users to add relevant map layers themselves. Adding for GeoJSON or shapefiles by the user is also a possibility.")

    st.subheader("Power plant database")
    st.markdown("A database containing powerplants for every country is present. The user can select for which countries the data should be shown.")
    country = st.multiselect("Select countries to show",gdf.country_long.unique(), default="Philippines")
    gdf_show = gdf.query("country_long == @country")
    gdf_show.drop(gdf_show.columns[16:-1],axis=1, inplace=True) # drop irrelevant data, otherwise it shows on hover
    gdf_show.drop(gdf_show.columns[[0,3,8,9,10]],axis=1, inplace=True) # drop irrelevant data, otherwise it shows on hover
    m.add_gdf(gdf_show, layer_name="Power plants")

    st.subheader("Turbine specifications")
    st.markdown("This section reads user input and performs a calculation. This can also be coupled with user inputs on the map. For example performing a LCOE calculation for a selected area")
    power = st.selectbox("Turbine power", ["10 MW", "12 MW", "15 MW"])
    diameter = st.selectbox("Turbine rotor diameter", ["100 m", "150 m", "200 m"])
    number = st.number_input("Number of turbines", min_value=1, max_value=100)
    farmPower = float(power.split(" ")[0])*number
    

with col2:
    # m.add_wms_layer(inputUrl, layers=inputLayer, control=True)

    st.subheader("Interactive map of Philippines")
    m.to_streamlit()
    st.markdown(f"you selected a **{power}** turbine with a rotor diameter of **{diameter}** \r \r The windfarm has a total installed capacity of **{farmPower}** MW and has an AEP of **{0.5*365*24*farmPower/1000}** GWh")

