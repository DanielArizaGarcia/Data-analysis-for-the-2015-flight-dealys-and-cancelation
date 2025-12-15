#!/bin/bash

# Script para ejecutar app.py con entorno virtual usando uv

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # Sin color

echo -e "${BLUE}🚀 Iniciando app.py con uv...${NC}"

# Verificar si uv está instalado
if ! command -v uv &> /dev/null; then
    echo -e "${RED}❌ Error: uv no está instalado${NC}"
    echo -e "${BLUE}Instálalo con: curl -LsSf https://astral.sh/uv/install.sh | sh${NC}"
    exit 1
fi

# Directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${GREEN}✓ Directorio de trabajo: $SCRIPT_DIR${NC}"

# Verificar si existe app.py
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ Error: app.py no encontrado en $SCRIPT_DIR${NC}"
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo -e "${BLUE}📦 Creando entorno virtual con uv...${NC}"
    uv venv
fi

# Activar el entorno virtual
echo -e "${BLUE}🔄 Activando entorno virtual...${NC}"
source .venv/bin/activate

# Instalar/actualizar dependencias necesarias para app.py
echo -e "${BLUE}📥 Instalando dependencias...${NC}"
uv pip install streamlit pandas numpy plotly matplotlib

# Ejecutar la aplicación Streamlit
echo -e "${GREEN}✓ Lanzando aplicación Streamlit...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
streamlit run app.py

# Desactivar entorno virtual al terminar
deactivate
