
# 🎮 Ejecución del juego desde `main.py`

Este proyecto está desarrollado en **Python** y utiliza dependencias externas listadas en `requirements.txt`.  
A continuación encontrarás los pasos para instalar todo lo necesario y ejecutar el juego en **Windows** y **Linux**.

---

## 📦 1. Instalar Python y pip

### 🔹 Windows
1. Descarga e instala **Python** desde la página oficial:  
   👉 [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)

2. **Durante la instalación**, asegúrate de marcar la opción:  
   `Add Python to PATH`

3. Verifica que Python y pip estén instalados correctamente:
   ```powershell
   python --version
   pip --version
   ```
   

### 🔹 Linux (Debian/Ubuntu y derivados)

En la mayoría de distribuciones Linux, Python ya viene instalado.
Si no es así, instálalo con:

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip -y
   ```

Verifica que estén instalados:
   ```bash
   python3 --version
   pip3 --version
   ```

### 📂 2. Instalar dependencias del proyecto
🔹 Windows o Linux
   ```bash
   pip install -r requirements.txt
   ```
O también si es el caso:
   ```bash
   pip3 install -r requirements.txt
   ```

### ▶️ 3. Ejecutar el juego
🔹 Windows
```bash
python main.py
```
🔹 Linux
```bash
python3 main.py
```

> 💡 **Nota**: Dependiendo de tu sistema operativo, el comando para ejecutar Python puede variar:
> - En Windows: `py` o `python`
> - En Linux/macOS: `python3` o `python`


