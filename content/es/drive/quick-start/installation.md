---
title: "Instalación"
---

Instala los requisitos técnicos antes de clonar el repositorio. Esta guía te ayudará a verificar si las herramientas requeridas ya están instaladas y proporcionará instrucciones de instalación si es necesario.

## Requisitos Previos

Drive requiere que las siguientes herramientas estén instaladas en tu sistema:

- **Git** - Para clonar el repositorio
- **Docker** (20.10+) - Para ejecutar contenedores
- **Docker Compose** (1.29+) - Para gestionar aplicaciones multi-contenedor

**Nota Importante sobre Permisos:**
- En Linux, es posible que necesites agregar tu usuario al grupo `docker` para ejecutar comandos de Docker sin `sudo`
- El script `drive.sh` funciona con o sin `sudo`, pero Docker en sí puede requerir `sudo` si no está configurado
- Consulta las instrucciones de instalación a continuación para saber cómo configurar esto

---

## Instalando Requisitos Previos

Selecciona tu sistema operativo para ver las instrucciones de instalación:

{{< tabs "installation-platform" >}}
{{< tab "Ubuntu/Linux" >}}

### Instalando Git

Git generalmente viene preinstalado en la mayoría de las distribuciones de Linux. Verifiquemos si ya está instalado:

**Paso 1: Verificar si Git está instalado**

```bash
git --version
```

**Si Git está instalado:** Verás una salida como `git version 2.34.1` o similar. Puedes saltar a la sección de instalación de Docker.

**Si Git no está instalado:** Verás un error como `command not found: git`. Sigue los pasos de instalación a continuación.

**Paso 2: Instalar Git (si es necesario)**

```bash
# Ubuntu/Debian:
sudo apt-get update
sudo apt-get install git

# CentOS/RHEL/Fedora:
sudo yum install git
# O en versiones más recientes:
sudo dnf install git
```

**Paso 3: Verificar la instalación de Git**

```bash
git --version
```

Ahora deberías ver el número de versión de Git, confirmando que la instalación fue exitosa.

---

### Instalando Docker y Docker Compose

Docker y Docker Compose generalmente no vienen preinstalados en sistemas Linux. Sigue estos pasos para instalarlos.

**Paso 1: Verificar si Docker está instalado**

```bash
docker --version
docker compose version
```

**Si Docker está instalado:** Verás números de versión para ambos comandos. Puedes saltar a la sección "Configurar Permisos de Docker" a continuación.

**Si Docker no está instalado:** Verás errores como `command not found: docker`. Sigue los pasos de instalación a continuación.

**Paso 2: Instalar Docker y Docker Compose**

Usa el script oficial de instalación de Docker para Ubuntu/Debian:

```bash
# Actualizar paquetes
sudo apt-get update

# Instalar dependencias
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# Agregar la clave GPG oficial de Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Configurar repositorio
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker Engine y Docker Compose
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

**Paso 3: Verificar la instalación de Docker**

```bash
docker --version
docker compose version
```

Deberías ver números de versión para ambos comandos, confirmando que la instalación fue exitosa.

---

### Configurar Permisos de Docker

**⚠️ IMPORTANTE:** Después de instalar Docker, necesitas agregar tu usuario al grupo `docker` para ejecutar comandos de Docker sin `sudo`. Este paso es **REQUERIDO** si deseas ejecutar comandos de Docker sin `sudo`.

**Paso 1: Agregar tu usuario al grupo docker**

```bash
sudo usermod -aG docker $USER
```

**Paso 2: Aplicar los cambios**

**⚠️ CRÍTICO:** Después de agregar tu usuario al grupo docker, **DEBES** cerrar sesión y volver a iniciar sesión (o reiniciar tu sesión de terminal) para que los cambios surtan efecto.

**Opción A: Cerrar sesión y volver a iniciar sesión** (recomendado)
- Cerrar todas las ventanas de terminal
- Cerrar sesión de tu usuario
- Volver a iniciar sesión

**Opción B: Reiniciar tu sesión de terminal**
- Cerrar todas las ventanas de terminal
- Abrir una nueva ventana de terminal

**Paso 3: Verificar que Docker funciona sin sudo**

Después de volver a iniciar sesión, prueba que Docker funciona sin `sudo`:

```bash
docker ps
```

Si este comando funciona sin errores, los permisos de Docker están configurados correctamente. Si ves un error de permisos, asegúrate de haber cerrado sesión y vuelto a iniciar sesión después de agregar tu usuario al grupo docker.

**Nota:** El script `drive.sh` admite tanto el uso con `sudo` como sin `sudo`, pero Docker en sí requiere `sudo` si tu usuario no está en el grupo docker. Se recomienda configurar los permisos correctamente para evitar necesitar `sudo` para todos los comandos de Docker.

---

### Lista de Verificación de Instalación Completa

Después de completar todos los pasos, verifica que todo funciona:

- [ ] Git está instalado: `git --version` muestra un número de versión
- [ ] Docker está instalado: `docker --version` muestra un número de versión
- [ ] Docker Compose está instalado: `docker compose version` muestra un número de versión
- [ ] Docker funciona sin sudo: `docker ps` se ejecuta sin errores de permisos
- [ ] El usuario está en el grupo docker: `groups` muestra `docker` en la lista

Si todas las verificaciones pasan, estás listo para proceder al siguiente paso: [Clonar el Repositorio]({{< relref "git-clone" >}}).

{{< /tab >}}
{{< tab "macOS" >}}

### Instalando Git

Git generalmente viene preinstalado en macOS. Verifiquemos si ya está instalado:

**Paso 1: Verificar si Git está instalado**

```bash
git --version
```

**Si Git está instalado:** Verás una salida como `git version 2.34.1` o similar. Puedes saltar a la sección de instalación de Docker.

**Si Git no está instalado:** Verás un error como `command not found: git`. Sigue los pasos de instalación a continuación.

**Paso 2: Instalar Git (si es necesario)**

**Opción 1: Usando Homebrew (Recomendado)**

Si tienes Homebrew instalado:

```bash
brew install git
```

Si no tienes Homebrew, instálalo primero:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Luego instala Git:

```bash
brew install git
```

**Opción 2: Usando Xcode Command Line Tools**

```bash
xcode-select --install
```

Esto instalará Git junto con otras herramientas de desarrollo.

**Paso 3: Verificar la instalación de Git**

```bash
git --version
```

Ahora deberías ver el número de versión de Git, confirmando que la instalación fue exitosa.

---

### Instalando Docker y Docker Compose

On macOS, Docker and Docker Compose are installed together as Docker Desktop.

**Paso 1: Verificar si Docker está instalado**

```bash
docker --version
docker compose version
```

**Si Docker está instalado:** Verás números de versión para ambos comandos. Puedes saltar a la sección "Verificar que Docker Desktop está Ejecutándose" a continuación.

**Si Docker no está instalado:** Verás errores como `command not found: docker`. Sigue los pasos de instalación a continuación.

**Paso 2: Instalar Docker Desktop**

1. Download Docker Desktop for Mac from [docker.com](https://www.docker.com/products/docker-desktop/)
2. Open the downloaded `.dmg` file
3. Drag Docker to the Applications folder
4. Open Docker from Applications
5. Complete the initial setup wizard
6. Docker Desktop will start automatically

**Step 3: Verify Docker Desktop is Running**

Docker Desktop debe estar ejecutándose para que los comandos de Docker funcionen. Verifica si está ejecutándose:

- Look for the Docker icon in your menu bar (whale icon)
- If the icon is not visible, open Docker Desktop from Applications

**Step 4: Verify Docker installation**

```bash
docker --version
docker compose version
```

Deberías ver números de versión para ambos comandos, confirmando que la instalación fue exitosa.

**Note:** On macOS, Docker Desktop handles permissions automatically, so you don't need to configure user groups like on Linux.

---

### Lista de Verificación de Instalación Completa

Después de completar todos los pasos, verifica que todo funciona:

- [ ] Git está instalado: `git --version` muestra un número de versión
- [ ] Docker Desktop is installed: `docker --version` shows a version number
- [ ] Docker Compose está instalado: `docker compose version` muestra un número de versión
- [ ] Docker Desktop is running: Docker icon is visible in menu bar
- [ ] Docker commands work: `docker ps` runs without errors

Si todas las verificaciones pasan, estás listo para proceder al siguiente paso: [Clonar el Repositorio]({{< relref "git-clone" >}}).

{{< /tab >}}
{{< tab "Windows" >}}

### Instalando Git

Git is not pre-installed on Windows. Follow these steps to install it.

**Paso 1: Verificar si Git está instalado**

Open PowerShell or Command Prompt and run:

```powershell
git --version
```

**Si Git está instalado:** Verás una salida como `git version 2.34.1` o similar. Puedes saltar a la sección de instalación de Docker.

**If Git is not installed:** You'll see an error like `'git' is not recognized as an internal or external command`. Follow the installation steps below.

**Step 2: Install Git**

**Option 1: Download Git for Windows (Recommended)**

1. Visit [git-scm.com/download/win](https://git-scm.com/download/win)
2. Download the installer (it will detect your system architecture automatically)
3. Run the downloaded `.exe` installer
4. Sigue el asistente de configuración:
   - Accept the default options (recommended for most users)
   - Choose your preferred editor
   - Select how Git should handle line endings (default is recommended)
5. Complete the installation

**Option 2: Install via Package Manager**

**Using Chocolatey (if installed):**

```powershell
choco install git
```

**Using winget (Windows 10/11):**

```powershell
winget install Git.Git
```

**Paso 3: Verificar la instalación de Git**

**Importante:** After installation, you may need to restart your terminal or PowerShell window for Git to be available.

Open a new PowerShell or Command Prompt window and run:

```powershell
git --version
```

Ahora deberías ver el número de versión de Git, confirmando que la instalación fue exitosa.

---

### Instalando Docker y Docker Compose

On Windows, Docker and Docker Compose are installed together as Docker Desktop.

**Paso 1: Verificar si Docker está instalado**

Open PowerShell and run:

```powershell
docker --version
docker compose version
```

**Si Docker está instalado:** Verás números de versión para ambos comandos. Puedes saltar a la sección "Verificar que Docker Desktop está Ejecutándose" a continuación.

**If Docker is not installed:** You'll see errors like `'docker' is not recognized as an internal or external command`. Follow the installation steps below.

**Step 2: Verify System Requirements**

Docker Desktop for Windows requires:

- **Windows 10 64-bit:** Pro, Enterprise, or Education (Build 19041 or higher)
- **Windows 11 64-bit:** Any edition
- **WSL 2 enabled:** Docker Desktop will configure this automatically if available

**Step 3: Install Docker Desktop**

1. Download Docker Desktop for Windows from [docker.com](https://www.docker.com/products/docker-desktop/)
2. Run the downloaded `.exe` installer
3. Accept the terms and conditions
4. Complete the installation (may require restart)
5. After installation, open Docker Desktop from the Start menu
6. Complete the initial setup wizard

**Step 4: Verify Docker Desktop is Running**

Docker Desktop debe estar ejecutándose para que los comandos de Docker funcionen. Verifica si está ejecutándose:

- Look for the Docker icon in your system tray (whale icon)
- If the icon is not visible, open Docker Desktop from the Start menu
- Wait for Docker Desktop to fully start (the icon will stop animating when ready)

**Step 5: Verify Docker installation**

Open PowerShell and run:

```powershell
docker --version
docker compose version
```

Deberías ver números de versión para ambos comandos, confirmando que la instalación fue exitosa.

**Note:** On Windows, Docker Desktop handles permissions automatically through WSL 2, so you don't need to configure user groups like on Linux.

---

### Lista de Verificación de Instalación Completa

Después de completar todos los pasos, verifica que todo funciona:

- [ ] Git está instalado: `git --version` muestra un número de versión
- [ ] Docker Desktop is installed: `docker --version` shows a version number
- [ ] Docker Compose está instalado: `docker compose version` muestra un número de versión
- [ ] Docker Desktop is running: Docker icon is visible in system tray
- [ ] Docker commands work: `docker ps` runs without errors

Si todas las verificaciones pasan, estás listo para proceder al siguiente paso: [Clonar el Repositorio]({{< relref "git-clone" >}}).

{{< /tab >}}
{{< /tabs >}}

---

## Próximos Pasos

Once you have all prerequisites installed and verified, proceed to:

- [Cloning the Repository]({{< relref "git-clone" >}}) - Clonar el repositorio de Drive to your local machine

---

## Solución de Problemas

### Docker Permission Errors (Linux)

If you see permission errors when running Docker commands on Linux:

1. **Verify you're in the docker group:**
   ```bash
   groups
   ```
   You should see `docker` in the list.

2. **If not in the group, add yourself:**
   ```bash
   sudo usermod -aG docker $USER
   ```

3. **Log out and log back in** (or restart your terminal session)

4. **Test again:**
   ```bash
   docker ps
   ```

### Docker Desktop Not Starting (macOS/Windows)

If Docker Desktop won't start:

1. **Check system requirements** - Ensure your system meets the minimum requirements
2. **Restart Docker Desktop** - Quit and reopen Docker Desktop
3. **Check for updates** - Update Docker Desktop to the latest version
4. **Check system resources** - Ensure you have enough RAM and disk space
5. **Review Docker Desktop logs** - Check the Docker Desktop logs for error messages

### Git Not Found After Instalación (Windows)

If Git commands don't work after installation:

1. **Restart your terminal** - Close and reopen PowerShell or Command Prompt
2. **Check PATH** - Verify Git is in your system PATH
3. **Reinstall Git** - If issues persist, try reinstalling Git

---

## Ver También

- [Arquitectura Overview]({{< relref "architecture" >}}) - Entender cómo funciona Drive
- [Cloning the Repository]({{< relref "git-clone" >}}) - Next step after installation
- [Managing Servicios]({{< relref "managing-services" >}}) - Aprender cómo usar servicios en Drive
