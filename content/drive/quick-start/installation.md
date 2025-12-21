---
title: "Installation"
---

# Installation

Install the technical requirements before cloning the repository. This guide will help you verify if the required tools are already installed and provide installation instructions if needed.

## Prerequisites

Drive requires the following tools to be installed on your system:

- **Git** - For cloning the repository
- **Docker** (20.10+) - For running containers
- **Docker Compose** (1.29+) - For managing multi-container applications

**Important Note on Permissions:**
- On Linux, you may need to add your user to the `docker` group to run Docker commands without `sudo`
- The `drive.sh` script works with or without `sudo`, but Docker itself may require `sudo` if not configured
- See the installation instructions below for how to configure this

---

## Installing Prerequisites

Select your operating system to see installation instructions:

{{< tabs "installation-platform" >}}
{{< tab "Ubuntu/Linux" >}}

### Installing Git

Git is usually pre-installed on most Linux distributions. Let's verify if it's already installed:

**Step 1: Check if Git is installed**

```bash
git --version
```

**If Git is installed:** You'll see output like `git version 2.34.1` or similar. You can skip to the Docker installation section.

**If Git is not installed:** You'll see an error like `command not found: git`. Follow the installation steps below.

**Step 2: Install Git (if needed)**

```bash
# Ubuntu/Debian:
sudo apt-get update
sudo apt-get install git

# CentOS/RHEL/Fedora:
sudo yum install git
# Or on newer versions:
sudo dnf install git
```

**Step 3: Verify Git installation**

```bash
git --version
```

You should now see the Git version number, confirming the installation was successful.

---

### Installing Docker and Docker Compose

Docker and Docker Compose are typically not pre-installed on Linux systems. Follow these steps to install them.

**Step 1: Check if Docker is installed**

```bash
docker --version
docker compose version
```

**If Docker is installed:** You'll see version numbers for both commands. You can skip to the "Configure Docker Permissions" section below.

**If Docker is not installed:** You'll see errors like `command not found: docker`. Follow the installation steps below.

**Step 2: Install Docker and Docker Compose**

Use the official Docker installation script for Ubuntu/Debian:

```bash
# Update packages
sudo apt-get update

# Install dependencies
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine and Docker Compose
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

**Step 3: Verify Docker installation**

```bash
docker --version
docker compose version
```

You should see version numbers for both commands, confirming the installation was successful.

---

### Configure Docker Permissions

**⚠️ IMPORTANT:** After installing Docker, you need to add your user to the `docker` group to run Docker commands without `sudo`. This step is **REQUIRED** if you want to run Docker commands without `sudo`.

**Step 1: Add your user to the docker group**

```bash
sudo usermod -aG docker $USER
```

**Step 2: Apply the changes**

**⚠️ CRITICAL:** After adding your user to the docker group, you **MUST** log out and log back in (or restart your terminal session) for the changes to take effect.

**Option A: Log out and log back in** (recommended)
- Close all terminal windows
- Log out of your user session
- Log back in

**Option B: Restart your terminal session**
- Close all terminal windows
- Open a new terminal window

**Step 3: Verify Docker works without sudo**

After logging back in, test that Docker works without `sudo`:

```bash
docker ps
```

If this command works without errors, Docker permissions are configured correctly. If you see a permission error, make sure you logged out and back in after adding your user to the docker group.

**Note:** The `drive.sh` script supports both `sudo` and non-sudo usage, but Docker itself requires `sudo` if your user is not in the docker group. It's recommended to configure permissions properly to avoid needing `sudo` for all Docker commands.

---

### Complete Installation Checklist

After completing all steps, verify everything is working:

- [ ] Git is installed: `git --version` shows a version number
- [ ] Docker is installed: `docker --version` shows a version number
- [ ] Docker Compose is installed: `docker compose version` shows a version number
- [ ] Docker works without sudo: `docker ps` runs without permission errors
- [ ] User is in docker group: `groups` shows `docker` in the list

If all checks pass, you're ready to proceed to the next step: [Cloning the Repository]({{< relref "git-clone" >}}).

{{< /tab >}}
{{< tab "macOS" >}}

### Installing Git

Git is usually pre-installed on macOS. Let's verify if it's already installed:

**Step 1: Check if Git is installed**

```bash
git --version
```

**If Git is installed:** You'll see output like `git version 2.34.1` or similar. You can skip to the Docker installation section.

**If Git is not installed:** You'll see an error like `command not found: git`. Follow the installation steps below.

**Step 2: Install Git (if needed)**

**Option 1: Using Homebrew (Recommended)**

If you have Homebrew installed:

```bash
brew install git
```

If you don't have Homebrew, install it first:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then install Git:

```bash
brew install git
```

**Option 2: Using Xcode Command Line Tools**

```bash
xcode-select --install
```

This will install Git along with other development tools.

**Step 3: Verify Git installation**

```bash
git --version
```

You should now see the Git version number, confirming the installation was successful.

---

### Installing Docker and Docker Compose

On macOS, Docker and Docker Compose are installed together as Docker Desktop.

**Step 1: Check if Docker is installed**

```bash
docker --version
docker compose version
```

**If Docker is installed:** You'll see version numbers for both commands. You can skip to the "Verify Docker Desktop is Running" section below.

**If Docker is not installed:** You'll see errors like `command not found: docker`. Follow the installation steps below.

**Step 2: Install Docker Desktop**

1. Download Docker Desktop for Mac from [docker.com](https://www.docker.com/products/docker-desktop/)
2. Open the downloaded `.dmg` file
3. Drag Docker to the Applications folder
4. Open Docker from Applications
5. Complete the initial setup wizard
6. Docker Desktop will start automatically

**Step 3: Verify Docker Desktop is Running**

Docker Desktop must be running for Docker commands to work. Check if it's running:

- Look for the Docker icon in your menu bar (whale icon)
- If the icon is not visible, open Docker Desktop from Applications

**Step 4: Verify Docker installation**

```bash
docker --version
docker compose version
```

You should see version numbers for both commands, confirming the installation was successful.

**Note:** On macOS, Docker Desktop handles permissions automatically, so you don't need to configure user groups like on Linux.

---

### Complete Installation Checklist

After completing all steps, verify everything is working:

- [ ] Git is installed: `git --version` shows a version number
- [ ] Docker Desktop is installed: `docker --version` shows a version number
- [ ] Docker Compose is installed: `docker compose version` shows a version number
- [ ] Docker Desktop is running: Docker icon is visible in menu bar
- [ ] Docker commands work: `docker ps` runs without errors

If all checks pass, you're ready to proceed to the next step: [Cloning the Repository]({{< relref "git-clone" >}}).

{{< /tab >}}
{{< tab "Windows" >}}

### Installing Git

Git is not pre-installed on Windows. Follow these steps to install it.

**Step 1: Check if Git is installed**

Open PowerShell or Command Prompt and run:

```powershell
git --version
```

**If Git is installed:** You'll see output like `git version 2.34.1` or similar. You can skip to the Docker installation section.

**If Git is not installed:** You'll see an error like `'git' is not recognized as an internal or external command`. Follow the installation steps below.

**Step 2: Install Git**

**Option 1: Download Git for Windows (Recommended)**

1. Visit [git-scm.com/download/win](https://git-scm.com/download/win)
2. Download the installer (it will detect your system architecture automatically)
3. Run the downloaded `.exe` installer
4. Follow the setup wizard:
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

**Step 3: Verify Git installation**

**Important:** After installation, you may need to restart your terminal or PowerShell window for Git to be available.

Open a new PowerShell or Command Prompt window and run:

```powershell
git --version
```

You should now see the Git version number, confirming the installation was successful.

---

### Installing Docker and Docker Compose

On Windows, Docker and Docker Compose are installed together as Docker Desktop.

**Step 1: Check if Docker is installed**

Open PowerShell and run:

```powershell
docker --version
docker compose version
```

**If Docker is installed:** You'll see version numbers for both commands. You can skip to the "Verify Docker Desktop is Running" section below.

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

Docker Desktop must be running for Docker commands to work. Check if it's running:

- Look for the Docker icon in your system tray (whale icon)
- If the icon is not visible, open Docker Desktop from the Start menu
- Wait for Docker Desktop to fully start (the icon will stop animating when ready)

**Step 5: Verify Docker installation**

Open PowerShell and run:

```powershell
docker --version
docker compose version
```

You should see version numbers for both commands, confirming the installation was successful.

**Note:** On Windows, Docker Desktop handles permissions automatically through WSL 2, so you don't need to configure user groups like on Linux.

---

### Complete Installation Checklist

After completing all steps, verify everything is working:

- [ ] Git is installed: `git --version` shows a version number
- [ ] Docker Desktop is installed: `docker --version` shows a version number
- [ ] Docker Compose is installed: `docker compose version` shows a version number
- [ ] Docker Desktop is running: Docker icon is visible in system tray
- [ ] Docker commands work: `docker ps` runs without errors

If all checks pass, you're ready to proceed to the next step: [Cloning the Repository]({{< relref "git-clone" >}}).

{{< /tab >}}
{{< /tabs >}}

---

## Next Steps

Once you have all prerequisites installed and verified, proceed to:

- [Cloning the Repository]({{< relref "git-clone" >}}) - Clone the Drive repository to your local machine

---

## Troubleshooting

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

### Git Not Found After Installation (Windows)

If Git commands don't work after installation:

1. **Restart your terminal** - Close and reopen PowerShell or Command Prompt
2. **Check PATH** - Verify Git is in your system PATH
3. **Reinstall Git** - If issues persist, try reinstalling Git

---

## See Also

- [Architecture Overview]({{< relref "architecture" >}}) - Understand how Drive works
- [Cloning the Repository]({{< relref "git-clone" >}}) - Next step after installation
- [Managing Services]({{< relref "managing-services" >}}) - Learn how to use services in Drive
