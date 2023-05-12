from dash import register_page

from CommTrading.GeospatialAnalysis.layout import geospatial_analysis_layout

register_page(__name__, path="/GeospatialAnalysis", layout=geospatial_analysis_layout)