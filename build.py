import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def build_dll():
    system = platform.system().lower()
    
    # Determine extension and compiler options
    if system == "windows":
        out_name = "libtwofish.dll"
        compile_cmd = ["gcc", "-shared", "-O2", "-o", f"native/{out_name}", "native/twofish.c"]
    elif system == "darwin":
        out_name = "libtwofish.dylib"
        compile_cmd = ["gcc", "-shared", "-fPIC", "-O2", "-o", f"native/{out_name}", "native/twofish.c"]
    else:
        out_name = "libtwofish.so"
        compile_cmd = ["gcc", "-shared", "-fPIC", "-O2", "-o", f"native/{out_name}", "native/twofish.c"]
        
    out_path = Path("native") / out_name
    
    if not out_path.exists():
        print(f"[*] {out_name} no existe. Compilando desde C usando gcc...")
        try:
            subprocess.run(compile_cmd, check=True)
            print(f"[+] {out_name} compilado correctamente.")
        except FileNotFoundError:
            print("[-] Error: No se encontró 'gcc'. Asegúrate de que esté instalado y en tu PATH.")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"[-] Error durante la compilación de {out_name}: {e}")
            sys.exit(1)
    else:
        print(f"[*] {out_name} ya existe. Saltando compilación.")
        
    return out_name

def build_exe(dll_name):
    print("[*] Verificando e instalando dependencias (pyinstaller)...")
    try:
        import PyInstaller
    except ImportError:
        print("[*] PyInstaller no encontrado. Instalando...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        except subprocess.CalledProcessError:
            print("[*] Falló la instalación normal. Intentando con --break-system-packages...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller", "--break-system-packages"], check=True)
        
    print("[*] Ejecutando PyInstaller...")
    sep = ";" if platform.system().lower() == "windows" else ":"
    
    # --noconsole para no mostrar ventana de CMD en Windows
    # --onefile para un solo ejecutable
    # --add-binary para incluir la DLL nativa en _MEIPASS/native/
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        "--name", "packetWinner",
        f"--add-binary=native/{dll_name}{sep}native",
        "main.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("[+] Empaquetado exitoso.")
        
        exe_ext = ".exe" if platform.system().lower() == "windows" else ""
        exe_path = Path("dist") / f"packetWinner{exe_ext}"
        if exe_path.exists():
            print(f"[+] El ejecutable final se encuentra en: {exe_path.absolute()}")
    except subprocess.CalledProcessError as e:
        print(f"[-] Error durante el empaquetado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("====================================")
    print(" packetWinner - Build Script")
    print("====================================")
    dll_name = build_dll()
    build_exe(dll_name)
    print("====================================")
    print(" Compilación terminada.")
