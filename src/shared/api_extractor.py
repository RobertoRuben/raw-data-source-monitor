import httpx
import os
from dotenv import load_dotenv
from typing import Any, Dict

load_dotenv()


class ApiExtractor:
    def __init__(
        self,
        prmstr_fundo: int,
        prmint_cartilla: int,
        prmint_cultivo: int,
        prmdat_fecha_inicio: str,
        prmdat_fecha_fin: str,
        prmstrRUCEmpresa: str,
    ):
        """
        Inicializa el extractor de API.
        
        Args:
            prmstr_fundo: Identificador del fundo
            prmint_cartilla: ID de la cartilla
            prmint_cultivo: ID del cultivo
            prmdat_fecha_inicio: Fecha de inicio (formato: YYYY-MM-DD)
            prmdat_fecha_fin: Fecha de fin (formato: YYYY-MM-DD)
            prmstrRUCEmpresa: RUC de la empresa
        """
        self.fundo = prmstr_fundo
        self.cartilla = prmint_cartilla
        self.cultivo = prmint_cultivo
        self.fecha_inicio = prmdat_fecha_inicio
        self.fecha_fin = prmdat_fecha_fin
        self.ruc_empresa = prmstrRUCEmpresa
        
        # Configuración de la API desde variables de entorno
        self.api_url = os.getenv("API_URL", "http://35.190.132.15:8087/WS_AB/api")
        self.authorization = os.getenv("AUTHORIZATION", "")
        
    def _get_headers(self) -> Dict[str, str]:
        """
        Construye los headers para las peticiones a la API.
        
        Returns:
            Dict con los headers incluyendo autenticación
        """
        return {
            "Authorization": self.authorization,
            "Content-Type": "application/json",
        }
    
    async def get(self, endpoint: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        Realiza una petición GET asincrónica a la API.
        
        Args:
            endpoint: Endpoint de la API (ej: "/data" o "/consultas")
            params: Parámetros de query opcionales
            
        Returns:
            Dict con la respuesta de la API
            
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