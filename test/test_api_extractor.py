import httpx
import pytest

from src.shared.api_extractor import ApiExtractor


class TestApiExtractorIntegracion:
    """Tests de integración que prueban contra la API real."""

    @pytest.mark.asyncio
    async def test_get_cartillas_retorna_ok(self):
        """
        Test de integración que valida la petición GET a la API.
        Envía una lista de cartillas y verifica que la respuesta es OK.
        """
        # Datos de prueba
        cartillas = [492, 493, 669, 624]

        # Crear instancia del extractor con datos reales del .env
        extractor = ApiExtractor(
            prmstr_fundo=290,
            prmint_cartilla=492,
            prmint_cultivo=2,
            prmdat_fecha_inicio="2025-10-10",
            prmdat_fecha_fin="2025-10-27",
            prmstrRUCEmpresa="20170040938",
        )

        try:
            # Realizar petición GET a un endpoint de la API
            # Ajusta el endpoint según lo que necesites consultar
            params = {
                "cartillas": ",".join(map(str, cartillas)),
                "ruc": extractor.ruc_empresa,
                "cultivo_id": extractor.cultivo,
                "fecha_inicio": extractor.fecha_inicio,
                "fecha_fin": extractor.fecha_fin,
            }

            resultado = await extractor.get("/cartillas", params=params)

            # Validaciones del test
            assert resultado is not None, "La respuesta no debe ser nula"
            assert isinstance(resultado, (dict, list)), (
                "La respuesta debe ser un diccionario o lista"
            )
            assert len(resultado) > 0, "La respuesta debe contener datos"

            print(f"✅ Test exitoso. Respuesta recibida: {len(resultado)} elementos")
            print(f"Tipo de respuesta: {type(resultado).__name__}")
            print(f"Contenido: {resultado}")

        except httpx.HTTPStatusError as e:
            pytest.fail(
                f"❌ Error HTTP {e.response.status_code}: {e.response.text}. "
                f"Verifica que la API está disponible en {extractor.api_url}"
            )
        except httpx.ConnectError:
            pytest.fail(
                f"❌ Error de conexión: No se pudo conectar a {extractor.api_url}. "
                f"Verifica que la API está disponible y accesible."
            )
        except Exception as e:
            pytest.fail(f"❌ Error inesperado: {str(e)}")
