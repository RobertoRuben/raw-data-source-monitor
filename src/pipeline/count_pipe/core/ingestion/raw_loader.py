import asyncio

from src.shared import ApiExtractor, FileManager


class RawLoader:
    def __init__(self, api_extractor: ApiExtractor, file_manager: FileManager):
        self.api = api_extractor
        self.file_manager = file_manager
        self.cartillas = [492, 493, 669, 624]
        self.fundo = 290

    async def extract(self, fecha_inicio: str, fecha_fin: str) -> dict:
        """
        Extrae datos de cartillas y guarda archivos Excel con datos válidos.
        """
        print(f"\n🔄 Extrayendo cartillas: {self.cartillas}")
        
        # Descargar en paralelo
        tasks = [
            self.api.get_evaluaciones(self.fundo, cartilla, fecha_inicio, fecha_fin)
            for cartilla in self.cartillas
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Guardar archivos
        saved_files = []
        for cartilla, response in zip(self.cartillas, responses):
            if isinstance(response, Exception):
                print(f"❌ Cartilla {cartilla}: Error")
                continue
                
            if not isinstance(response, str) or len(response) < 100:
                print(f"⏭️  Cartilla {cartilla}: Sin datos")
                continue
            
            filepath = self.file_manager.save_excel(cartilla, response)
            if filepath:
                print(f"✅ Cartilla {cartilla}: {filepath.name}")
                saved_files.append(filepath)
            else:
                print(f"⏭️  Cartilla {cartilla}: Excel vacío")
        
        print(f"\n✅ Guardados: {len(saved_files)}/{len(self.cartillas)} archivos")
        
        return {
            "total": len(self.cartillas),
            "saved": len(saved_files),
            "files": [str(f) for f in saved_files]
        }