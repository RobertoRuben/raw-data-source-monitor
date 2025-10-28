import os

import httpx
from dotenv import load_dotenv

load_dotenv()


class ApiExtractor:
    def __init__(self):
        """Inicializa el extractor de API con configuración del .env"""
        scheme = os.getenv("API_SCHEME", "http")
        host = os.getenv("API_HOST", "35.190.132.15")
        port = os.getenv("API_PORT", "8087")
        base = os.getenv("API_BASE", "/WS_AB/api")
        
        self.base_url = f"{scheme}://{host}:{port}{base}"
        self.authorization = os.getenv("AUTHORIZATION", "")
        self.ruc_empresa = os.getenv("API_PARAM_RUC_EMPRESA", "20170040938")
        self.cultivo_id = os.getenv("API_PARAM_CULTIVO_ID", "2")

    async def get_evaluaciones(
        self,
        fundo: int,
        cartilla: int,
        fecha_inicio: str,
        fecha_fin: str,
    ) -> str:
        """
        Obtiene el Excel en base64 de evaluaciones por variable.
        
        Args:
            fundo: ID del fundo
            cartilla: ID de la cartilla
            fecha_inicio: Fecha inicio (YYYY-MM-DD)
            fecha_fin: Fecha fin (YYYY-MM-DD)
            
        Returns:
            String base64 del archivo Excel
        """
        url = f"{self.base_url}/Fitosanidad/ZABG_ExcelRptEvaluacionesXVariable"
        
        params = {
            "prmstrFundo": fundo,
            "prmintCartilla": cartilla,
            "prmintCultivo": self.cultivo_id,
            "prmdatFechaInicio": fecha_inicio,
            "prmdatFechaFin": fecha_fin,
            "prmstrRUCEmpresa": self.ruc_empresa,
        }
        
        headers = {
            "Authorization": self.authorization,
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()