import os
from typing import Any, Dict, Optional
import httpx
from dotenv import load_dotenv

load_dotenv()


class ApiExtractor:
    def __init__(self):
        """
        Inicializa el extractor de API.
        Carga la configuración desde variables de entorno.
        """
        # Construir URL base desde componentes o usar la variable compuesta
        self.api_url = os.getenv("API_URL")
        if not self.api_url:
            scheme = os.getenv("API_SCHEME", "http")
            host = os.getenv("API_HOST", "35.190.132.15")
            port = os.getenv("API_PORT", "8087")
            base = os.getenv("API_BASE", "/WS_AB/api")
            self.api_url = f"{scheme}://{host}:{port}{base}"
        
        self.authorization = os.getenv("AUTHORIZATION", "")
        
        # Parámetros fijos
        self.ruc_empresa = os.getenv("API_PARAM_RUC_EMPRESA", "20170040938")
        self.cultivo_id = os.getenv("API_PARAM_CULTIVO_ID", "2")

    def _get_headers(self) -> Dict[str, str]:
        """Construye los headers para las peticiones a la API."""
        return {
            "Authorization": self.authorization,
            "Content-Type": "application/json",
        }

    def _build_params(self, custom_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Construye los parámetros con los prefijos correctos de la API.
        
        Args:
            custom_params: Parámetros personalizados con nombres simplificados:
                - fundo: int
                - cartilla: int
                - fecha_inicio: str (YYYY-MM-DD)
                - fecha_fin: str (YYYY-MM-DD)
        
        Returns:
            Dict con parámetros en formato de la API
        """
        # Mapeo de nombres simplificados a nombres de la API
        param_mapping = {
            "fundo": "prmstrFundo",
            "cartilla": "prmintCartilla",
            "cultivo": "prmintCultivo",
            "fecha_inicio": "prmdatFechaInicio",
            "fecha_fin": "prmdatFechaFin",
            "ruc_empresa": "prmstrRUCEmpresa",
        }
        
        # Parámetros base
        params = {
            "prmintCultivo": self.cultivo_id,
            "prmstrRUCEmpresa": self.ruc_empresa,
        }
        
        # Agregar parámetros personalizados con mapeo
        if custom_params:
            for key, value in custom_params.items():
                api_key = param_mapping.get(key, key)
                params[api_key] = value
        
        return params

    async def get_evaluaciones(
        self,
        fundo: int,
        cartilla: int,
        fecha_inicio: str,
        fecha_fin: str,
    ) -> Dict[str, Any] | list[Dict[str, Any]]:
        """
        Obtiene datos de evaluaciones por variable.
        
        Args:
            fundo: ID del fundo
            cartilla: ID de la cartilla
            fecha_inicio: Fecha de inicio (YYYY-MM-DD)
            fecha_fin: Fecha de fin (YYYY-MM-DD)
        
        Returns:
            Respuesta de la API
        
        Example:
            data = await api.get_evaluaciones(
                fundo=290,
                cartilla=493,
                fecha_inicio="2025-10-27",
                fecha_fin="2025-10-27"
            )
        """
        endpoint = "/Fitosanidad/ZABG_ExcelRptEvaluacionesXVariable"
        
        params = self._build_params({
            "fundo": fundo,
            "cartilla": cartilla,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        })
        
        return await self._request(endpoint, params)

    async def get(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any] | list[Dict[str, Any]]:
        """
        Método genérico para cualquier endpoint.
        
        Args:
            endpoint: Ruta del endpoint (ej: "/Fitosanidad/ZABG_ExcelRptEvaluacionesXVariable")
            params: Parámetros con nombres simplificados (fundo, cartilla, fecha_inicio, etc.)
        
        Returns:
            Respuesta de la API
        """
        all_params = self._build_params(params)
        return await self._request(endpoint, all_params)

    async def _request(
        self, 
        endpoint: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any] | list[Dict[str, Any]]:
        """
        Realiza la petición HTTP.
        
        Args:
            endpoint: Ruta del endpoint
            params: Parámetros ya formateados
        
        Returns:
            Respuesta de la API
        
        Raises:
            httpx.HTTPError: Si hay un error en la petición HTTP
        """
        url = f"{self.api_url}{endpoint}"
        headers = self._get_headers()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers=headers,
                params=params,
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()