import unittest
import requests
import base64
import os
import time
from config import Config
from io import BytesIO
from PIL import Image

class TestParkingAPI(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:8085"
    TEST_IMAGE_PATH = os.path.join(Config.BASE_PATH, "matricula_test.jpg")
    
    @classmethod
    def setUpClass(cls):
        """Prepara los datos de prueba"""
        # Crear imagen de prueba si no existe
        if not os.path.exists(cls.TEST_IMAGE_PATH):
            img = Image.new('RGB', (640, 480), color='red')
            img.save(cls.TEST_IMAGE_PATH)
        
        # Codificar imagen de prueba
        with open(cls.TEST_IMAGE_PATH, "rb") as f:
            cls.test_image_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        # Matrícula de prueba (simulamos una reconocida)
        cls.test_plate = "TEST123"
    
    def test_01_model_v2_success(self):
        """Prueba el endpoint /model_v2 con datos válidos"""
        print("\n🔍 Probando /model_v2 (POST) - Caso exitoso")
        response = requests.post(
            f"{self.BASE_URL}/model_v2",
            json={"photo": self.test_image_base64, "status": 2}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("matricula", data)
        self.assertIn("timestamp", data)
        print(f"✅ Matrícula reconocida: {data['matricula']}")
        
        # Guardamos la matrícula para pruebas posteriores
        self.__class__.test_plate = data['matricula']
    
    def test_02_get_matricula_info(self):
        """Prueba el endpoint /matricula con datos válidos"""
        print("\n🔍 Probando /matricula (GET) - Caso exitoso")
        response = requests.get(
            f"{self.BASE_URL}/matricula",
            params={"matricula": self.test_plate}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("_id", data)
        print(f"✅ Datos obtenidos para matrícula: {data['_id']}")
        print(data)
    
    def test_03_invalid_status(self):
        """Prueba estado inválido en /model_v2"""
        print("\n🔍 Probando /model_v2 (POST) - Estado inválido")
        response = requests.post(
            f"{self.BASE_URL}/model_v2",
            json={"photo": self.test_image_base64, "status": 99}
        )
        
        self.assertEqual(response.status_code, 400)
        error = response.json()
        self.assertIn("error", error)
        print(f"✅ Error manejado correctamente: {error['error']}")
    
    def test_04_missing_photo(self):
        """Prueba falta de foto en /model_v2"""
        print("\n🔍 Probando /model_v2 (POST) - Falta foto")
        response = requests.post(
            f"{self.BASE_URL}/model_v2",
            json={"status": 0}
        )
        
        self.assertEqual(response.status_code, 400)
        error = response.json()
        self.assertIn("error", error)
        print(f"✅ Error manejado correctamente: {error['error']}")
    
    def test_05_missing_plate_param(self):
        """Prueba falta de parámetro matrícula en /matricula"""
        print("\n🔍 Probando /matricula (GET) - Falta parámetro")
        response = requests.get(f"{self.BASE_URL}/matricula")
        
        self.assertEqual(response.status_code, 400)
        error = response.json()
        self.assertIn("error", error)
        print(f"✅ Error manejado correctamente: {error['error']}")
    
    def test_06_unknown_plate(self):
        """Prueba matrícula no existente en /matricula"""
        print("\n🔍 Probando /matricula (GET) - Matrícula desconocida")
        response = requests.get(
            f"{self.BASE_URL}/matricula",
            params={"matricula": "PLATE999"}
        )
        
        self.assertEqual(response.status_code, 404)
        error = response.json()
        self.assertIn("error", error)
        print(f"✅ Error manejado correctamente: {error['error']}")
    
    def test_07_performance(self):
        """Prueba de rendimiento con múltiples peticiones"""
        print("\n⏱️ Probando rendimiento con 5 peticiones rápidas")
        start_time = time.time()
        
        for i in range(5):
            status = i % 3  # Rotar entre 0, 1, 2
            response = requests.post(
                f"{self.BASE_URL}/model_v2",
                json={"photo": self.test_image_base64, "status": status}
            )
            self.assertIn(response.status_code, [200, 400])
        
        elapsed = time.time() - start_time
        print(f"✅ 5 peticiones completadas en {elapsed:.2f} segundos")

if __name__ == "__main__":
    # Configurar y ejecutar pruebas
    print("\n" + "="*60)
    print("  INICIANDO PRUEBAS DE LA API DE MATRÍCULAS")
    print("="*60 + "\n")
    
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestParkingAPI)
    result = runner.run(suite)
    
    # Mostrar resumen
    print("\n" + "="*60)
    print(f"  RESUMEN: {result.testsRun} pruebas ejecutadas")
    print(f"  Fallos: {len(result.failures)}, Errores: {len(result.errors)}")
    print("="*60)
    
    if not result.wasSuccessful():
        exit(1)