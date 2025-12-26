---
title: "Configuración de Firewall"
---

Esta guía explica cómo configurar el firewall de tu sistema para permitir conexiones entrantes a los servicios de Drive. Estas instrucciones son para tu sistema host local donde Drive está ejecutándose.

## Important Notes

**Before You Begin:**
- These commands configure the firewall on your **local host system** only
- Network-level firewalls (routers, ISPs, cloud providers) may also need configuration
- For remote servers in datacenters, firewall rules are typically pre-configured by the hosting provider
- If you still cannot connect after configuring your local firewall, check for additional network-level firewalls

**⚠️ Critical: SSH Access**
Before configuring any firewall rules, **always ensure SSH (port 22) is allowed**. Si te estás conectando a un servidor remoto vía SSH and you enable the firewall without allowing SSH, perderás el acceso a tu servidor. Make sure to add SSH to your firewall rules first.

---

## Understanding Configuración de Firewall

Cuando ejecutas servicios de Drive, necesitan aceptar conexiones entrantes en puertos específicos. El firewall de tu sistema puede bloquear estas conexiones por defecto. Esta guía te muestra cómo configurar tu firewall para permitir estas conexiones.

**What ports need to be opened?**
- Cada servicio tiene specific ports that need to be accessible
- See the [Catálogo de Servicios]({{< relref "../catalog" >}}) for port configurations for each service
- Required ports must be opened for the service to function
- Optional ports can be opened if you need specific features (APIs, monitoring, etc.)

---

## Platform-Specific Instructions

Select your operating system to see detailed firewall configuration instructions:

{{< tabs "firewall-platform" >}}
{{< tab "Ubuntu/Linux" >}}
UFW (Uncomplicated Firewall) is the default firewall management tool on Ubuntu and many Linux distributions.

### ⚠️ Critical: Allow SSH Before Enabling UFW

**Before enabling UFW, you MUST allow SSH (port 22).** If you enable UFW without allowing SSH first, you will lose access to your server if you're connecting remotely.

### Checking Current Status

**Step 1: Check UFW Status**

First, check if UFW is installed and its current status:

```bash
sudo ufw status
```

This will show:
- `Status: inactive` - UFW is installed but not enabled
- `Status: active` - UFW is enabled and running
- If UFW is not installed, you'll need to install it first: `sudo apt install ufw`

**Step 2: Check if SSH (Port 22) is Allowed**

Check if port 22 is already allowed in UFW:

```bash
sudo ufw status | grep 22
# Or check for SSH service name:
sudo ufw status | grep ssh
```

If you see a rule allowing port 22 or SSH, it's already configured. If you see nothing, port 22 is not allowed.

**Step 3: Allow SSH (If Not Already Allowed)**

If port 22 is not in the status output, you need to allow it **before enabling UFW**:

```bash
# Allow SSH before enabling firewall
sudo ufw allow 22/tcp
# Or use the service name:
sudo ufw allow ssh
```

**Step 4: Enable UFW (Only After SSH is Allowed)**

**Only after confirming that SSH (port 22) is allowed**, you can enable UFW:

```bash
sudo ufw enable
```

**Importante:** If UFW is already active, you don't need to enable it again. Just make sure SSH is allowed.

### Allowing Specific Puertos

To allow a specific port:

```bash
sudo ufw allow <PORT>/tcp
```

**Example:**
```bash
# Allow P2P port for blockchain node
sudo ufw allow 26656/tcp

# Allow RPC port
sudo ufw allow 26657/tcp
```

**Note:** The `/tcp` protocol specification is optional. You can use either `sudo ufw allow 26656/tcp` or `sudo ufw allow 26656` - both work the same way.

### Allowing Multiple Puertos

You can allow multiple ports in a single command:

```bash
sudo ufw allow 26656,26657,9090/tcp
```

### Checking Firewall Status

View all active firewall rules:

```bash
sudo ufw status
```

View detailed status with port numbers:

```bash
sudo ufw status numbered
```

### Removing Rules

To remove a firewall rule:

```bash
# First, list rules with numbers
sudo ufw status numbered

# Then delete by number
sudo ufw delete <RULE_NUMBER>
```

Or delete by rule:

```bash
sudo ufw delete allow 26656/tcp
```

### Disabling UFW

If you need to temporarily disable UFW:

```bash
sudo ufw disable
```
{{< /tab >}}
{{< tab "macOS" >}}
macOS has a built-in firewall that can be managed through System Preferences or command line.

### Important Note

**macOS typically allows incoming connections by default**, so you may not need to configure anything. However, we recommend verifying your firewall settings.

### Method 1: System Preferences (Recommended)

This is the easiest and most user-friendly method:

1. Open **System Preferences** (or **System Settings** on macOS Ventura and later)
2. Go to **Security & Privacy** (or **Network** > **Firewall** in newer versions)
3. Click the lock icon 🔒 and enter your password to make changes
4. Click **Firewall Options...** (or **Options...**)
5. Click the **+** button to add an application or port
6. For each port you want to allow:
   - Select "Add Port..."
   - Enter the port number
   - Select TCP protocol
   - Click OK

**Note:** On newer macOS versions, the firewall primarily manages applications rather than individual ports. If you're running Docker, you may need to allow Docker Desktop in the firewall settings.

### Method 2: Command Line (Advanced)

For advanced users who prefer command-line configuration:

#### Using pfctl

macOS uses `pfctl` (packet filter control) to manage the firewall. The configuration file is `/etc/pf.conf`.

**Warning:** Editing `/etc/pf.conf` requires root access and can affect system security. Only proceed if you're comfortable with command-line administration.

1. Create a backup of the current configuration:
```bash
sudo cp /etc/pf.conf /etc/pf.conf.backup
```

2. Edit the configuration file:
```bash
sudo nano /etc/pf.conf
```

3. Add rules for each port you want to allow:
```
pass in proto tcp from any to any port 26656  # P2P port
pass in proto tcp from any to any port 26657  # RPC port
```

4. Reload the firewall:
```bash
sudo pfctl -f /etc/pf.conf
```

5. Enable the firewall if not already enabled:
```bash
sudo pfctl -e
```

**Note:** Changes to `/etc/pf.conf` may be overwritten by system updates. Consider using a custom configuration file that's included in the main config.
{{< /tab >}}
{{< tab "Windows" >}}
Windows Firewall can be managed through the graphical interface or PowerShell.

### Method 1: Windows Defender Firewall (Interfaz Gráfica)

1. Open **Windows Defender Firewall**:
   - Press `Win + R`, type `wf.msc`, and press Enter
   - Or search for "Windows Defender Firewall" in the Start menu

2. Click **Advanced settings** in the left panel

3. Click **Inbound Rules** in the left panel

4. Click **New Rule...** in the right panel

5. Select **Port** and click **Next**

6. Select **TCP** and enter the specific port number (e.g., `26656`), then click **Next**

7. Select **Allow the connection** and click **Next**

8. Check all profiles (Domain, Private, Public) and click **Next**

9. Enter a name for the rule (e.g., "Drive P2P Port") and click **Finish**

Repeat these steps for each port you need to allow.

### Method 2: PowerShell (Command Line)

Open PowerShell as Administrator and use the `New-NetFirewallRule` cmdlet:

**Allow SSH (Critical - Do This First!):**
```powershell
New-NetFirewallRule -DisplayName "SSH" -Direction Inbound -LocalPort 22 -Protocol TCP -Action Allow
```

**Allow a single port:**
```powershell
New-NetFirewallRule -DisplayName "Drive P2P" -Direction Inbound -LocalPort 26656 -Protocol TCP -Action Allow
```

**Allow multiple ports:**
```powershell
New-NetFirewallRule -DisplayName "Drive Service Puertos" -Direction Inbound -LocalPort 26656,26657,9090 -Protocol TCP -Action Allow
```

### Viewing Firewall Rules

To view all firewall rules:

```powershell
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*Drive*"}
```

### Removing Firewall Rules

To remove a firewall rule:

```powershell
Remove-NetFirewallRule -DisplayName "Drive P2P"
```
{{< /tab >}}
{{< /tabs >}}

---

## Verifying Configuración de Firewall

After configuring your firewall, verify that the ports are accessible:

### From the Same Machine

```bash
# Check if port is listening
netstat -tuln | grep <PORT>

# Or using ss (modern alternative)
ss -tuln | grep <PORT>
```

### From Another Machine

```bash
# Test connection (replace with your server IP)
telnet <SERVER_IP> <PORT>

# Or using nc (netcat)
nc -zv <SERVER_IP> <PORT>
```

### Using Online Tools

You can use online port checking tools to verify if your ports are accessible from the internet (if that's your goal).

---

## Solución de Problemas

### Port Still Blocked After Configuración

1. **Verify the rule was added correctly:**
   - Check firewall status and rules
   - Ensure the rule is enabled

2. **Check for multiple firewalls:**
   - Some systems have multiple firewall layers
   - Cloud providers often have their own firewall rules

3. **Verify the service is running:**
   - Ensure the Docker container is running
   - Check that the service is listening on the correct port

4. **Check network-level firewalls:**
   - Router firewall settings
   - ISP restrictions
   - Cloud provider security groups

### Lost SSH Access

If you've lost SSH access after configuring the firewall:

1. **Physical access:** If you have physical access to the server, you can fix it directly
2. **Console access:** Many cloud providers offer console access through their web interface
3. **Recovery mode:** Boot into recovery mode to reset firewall rules

**Prevention:** Always allow SSH (port 22) before configuring other firewall rules.

---

## Service-Specific Examples

For service-specific firewall configurations with actual port numbers, see the individual service documentation in the [Catálogo de Servicios]({{< relref "../catalog" >}}).

Each service's documentation includes:
- Exact port numbers for that service
- Required vs optional ports
- Platform-specific commands with the correct port values

---

## Ver También

- [Estrategia de Puertos]({{< relref "." >}}) - Estrategia de asignación de puertos e información general
- [Referencia de Puertos: Nodos Blockchain]({{< relref "blockchain-nodes" >}}) - Descripciones detalladas de puertos
- [Catálogo de Servicios]({{< relref "../catalog" >}}) - Service-specific port configurations
