from dash import register_page

from CommTrading.HistoricalAnalysis.layout import historical_analysis_layout

register_page(__name__, path="/HistoricalAnalysis", layout=historical_analysis_layout())