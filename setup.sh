mkdir -p ~/.streamlit/
cp /cancer.keras ~/.streamlit/

echo "\
[general]\n\
email = \"i.jonathan.cosme@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
