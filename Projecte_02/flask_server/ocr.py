from paddleocr import PaddleOCR
import numpy as np
from PIL import Image

ocr_engine = PaddleOCR(use_angle_cls=True, lang='es')

def paddleocr_get_text_pil(pil_image):
    """
    Procesa una imagen PIL/Pillow para extraer texto con PaddleOCR.
    
    Args:
        pil_image: Objeto Image de PIL
    
    Returns:
        str: Texto detectado o None si falla
    """
    try:
        img_array = np.array(pil_image)
        
        if img_array.ndim == 3:  
            img_array = img_array[:, :, ::-1]  
        
        result = ocr_engine.ocr(img_array, cls=True)
        
        if result and result[0]:
            return result[0][0][1][0]  
            
        return None
        
    except Exception as e:
        print(f"❌ Error en OCR: {str(e)}")
        return None
    

# -- EJEMPLO DE USO --

# Cargar imagen con PIL
img = Image.open("matricula.jpg")

# Opcional: Preprocesamiento básico con PIL
img = img.convert('L')  # Escala de grises
img = img.point(lambda x: 0 if x < 128 else 255)  # Binarización

# Ejecutar OCR
texto = paddleocr_get_text_pil(img)
print(f"Texto detectado: {texto}" if texto else "No se detectó texto")