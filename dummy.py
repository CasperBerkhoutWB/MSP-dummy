import numpy as np
import pandas as pd
import streamlit as st
import leafmap.foliumap as leafmap
# import leafmap

st.set_page_config(page_title="Marine Spatial Planning Tool", layout="wide")

st.title("Offshore wind Philippines")

@st.cache_data
def load_powerplants():
    url = "https://raw.githubusercontent.com/PyPSA/powerplantmatching/master/powerplants.csv"
    return pd.read_csv(url, index_col=0)

ppl = load_powerplants()

st.header("Map View")
st.markdown("In this web application you can view different map layers relevant to offshore wind. For example the water depth, the wind resource and nature reserves have map layers. These can be selected with the dropdown menu \r \r You can also view LCOE maps for offshore wind to identify possible locations for wind farms \r \r Lastly you can draw a polygon on the map and input turbine paramters to get an estimate of the CAPEX and LCOE for that area")

gebcoWMSurl = "https://www.gebco.net/data_and_products/gebco_web_services/web_map_service/mapserv?"
gebcoWMSName = "GEBCO_LATEST_2_sub_ice_topo"
phWmsUrl = "https://geoserver.geoportal.gov.ph/geoserver/ows?"
phWmsLayer = "geoportal:keybiodiversityareas_202005"
phWmsName = "Key Biodiversity Areas"

col1, col2 = st.columns(2)

with col1:
    st.subheader("Interactive map of Philippines")
    m = leafmap.Map(center=[14.597, 120.98], zoom=6, height=800, widescreen=False)
    m.add_wms_layer(phWmsUrl, layers=phWmsLayer, name=phWmsName, opacity = 0.5)
    m.add_wms_layer(gebcoWMSurl, layers=gebcoWMSName, name=gebcoWMSName, opacity=0.5)
    # m.add_raster("Data/PHL_wind-speed_100m.tif", colormap="terrain", layer_name="Wind Speed")
    m.to_streamlit()

with col2:
    st.subheader("Options")
    st.multiselect("Map layers to show",["Wind resource", "Water depth", "Nature reserves"])
    inputText = st.text_input("Enter WMS url to add to the list", value="https://services.terrascope.be/wms/v2")
    st.markdown(f"This is the URL you put in: {inputText}")
    st.subheader("Turbine specifications")
    power = st.selectbox("Turbine power", ["10 MW", "12 MW", "15 MW"])
    diameter = st.selectbox("Turbine rotor diameter", ["100 m", "150 m", "200 m"])
    number = st.number_input("Number of turbines", min_value=1, max_value=100)
    farmPower = float(power.split(" ")[0])*number
    st.markdown(f"you selected a **{power}** turbine with a rotor diameter of **{diameter}** \r \r The windfarm has a total installed capacity of **{farmPower}** MW and has an AEP of **{0.5*365*24*farmPower/1000}** GWh")

