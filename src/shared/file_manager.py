import base64
from datetime import datetime
from pathlib import Path

import polars as pl


class FileManager:
    def __init__(self, base_dir: str = "temp"):
        self.base_dir = Path(base_dir)
        self.excel_dir = self.base_dir / "excel"
        self.excel_dir.mkdir(parents=True, exist_ok=True)

    def save_excel(self, cartilla_id: int, base64_data: str) -> Path | None:
        """
        Decodifica y guarda un archivo Excel desde base64.
        Retorna el Path del archivo guardado o None si falla o está vacío.
        """
        try:
            # Decodificar base64
            decoded = base64.b64decode(base64_data)
            
            # Generar nombre de archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = self.excel_dir / f"cartilla_{cartilla_id}_{timestamp}.xlsx"
            
            # Guardar archivo
            filepath.write_bytes(decoded)
            
            # Validar que tiene datos
            df = pl.read_excel(filepath)
            if len(df) == 0:
                filepath.unlink()  # Eliminar si está vacío
                return None
            
            return filepath
            
        except Exception as e:
            print(f"❌ Error guardando cartilla {cartilla_id}: {e}")
            if filepath.exists():
                filepath.unlink()
            return None