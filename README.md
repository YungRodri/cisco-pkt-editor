# packetWinner

**packetWinner** es una herramienta de interfaz gráfica ultrarrápida diseñada para decodificar, editar y recodificar archivos de Cisco Packet Tracer (`.pkt`).
Es compatible con las versiones más recientes de Packet Tracer (8.x y 9.x) y no requiere que el usuario final tenga Python instalado.

El core criptográfico está basado en una implementación nativa en C del algoritmo Twofish para garantizar que la ejecución de la herramienta sea instantánea y que el archivo XML en texto plano se despliegue en la interfaz gráfica en menos de 2 segundos.

## ⚠️ Advertencia Legal

> [!WARNING]
> Esta herramienta ha sido desarrollada estrictamente con **fines educativos y de auditoría personal**.
> Solamente debes utilizarla en archivos `.pkt` que sean de tu propiedad o sobre los cuales tengas permiso explícito para modificar.

## Cómo compilar desde cero (Entorno de Desarrollador)

Si deseas auditar el código y generar tu propio archivo `.exe`, sigue estos pasos:

### 1. Requisitos
- Python 3.8 o superior.
- Compilador GCC instalado y disponible en la variable `PATH` (en Windows puedes instalarlo vía MinGW o MSYS2).

### 2. Pasos de Compilación
Abre una terminal en la raíz del proyecto y ejecuta:

```bash
python build.py
```

El script `build.py` realizará automáticamente los siguientes pasos:
1. Comprobará si la librería criptográfica nativa ya existe. Si no, invocará a `gcc` para compilar `native/twofish.c` y generará la librería compartida correspondiente a tu sistema (`libtwofish.dll` en Windows).
2. Verificará e instalará `pyinstaller` si es necesario.
3. Empaquetará la interfaz (`main.py`) y la librería nativa (`libtwofish.dll`) en un único archivo ejecutable (Standalone).
4. El ejecutable final se guardará en la carpeta `dist/`.

## Cómo distribuir el ejecutable
El `.exe` generado en la carpeta `dist/` es **100% independiente (standalone)**. Puedes copiarlo y llevarlo a cualquier máquina con Windows 10 u 11, limpia, y funcionará inmediatamente sin requerir instalación de Python, dependencias adicionales, o extracción manual de DLLs.

## Troubleshooting: Falsos Positivos del Antivirus

> [!TIP]
> Los ejecutables generados por PyInstaller (que empaquetan todo dentro de sí mismos) a menudo activan alertas **falsas positivas** en Windows Defender o VirusTotal. Esto ocurre debido a la firma heurística del *bootloader* de PyInstaller y no porque el código sea malicioso.

### Soluciones
1. **Firma Digital (Para entornos de producción):** Si distribuyes esta herramienta, la mejor forma de evitar que Defender la bloquee es firmar el `.exe` con un certificado Authenticode válido (`signtool`).
2. **Exclusión en Windows Defender (Para uso propio):**
   - Abre **Seguridad de Windows** > Protección contra virus y amenazas > Administrar la configuración.
   - Desplázate hacia abajo hasta **Exclusiones** y haz clic en *Agregar o quitar exclusiones*.
   - Añade el archivo `packetWinner.exe` o la carpeta que lo contiene.
