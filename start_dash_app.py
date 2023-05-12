from CommTrading.init import init_app
from flask import Flask
import dash
import dash_bootstrap_components as dbc

server = Flask(__name__)

app = dash.Dash(
    name=__name__,
    suppress_callback_exceptions=True,
    assets_folder=f'CommTrading/assets',
    server=server,
    use_pages=True,
    pages_folder=f"CommTrading/pages",
    title='Commodity Trading Stats',
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

init_app(app)

if __name__ == "__main__":
    app.run_server(debug=False, port=8570)
