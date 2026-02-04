---
title: "Scripts de validación de endpoints"
weight: 5231
---

Drive incluye tres scripts de validación para comprobar que los endpoints de un nodo (Cosmos gRPC, Tendermint RPC y EVM RPC) son alcanzables y responden correctamente. Son útiles antes de conectar un cliente, tras desplegar un nodo o al diagnosticar conectividad. Los tres están en `drive/tools/` y comparten lógica común en `tools/common/endpoint-validation-common.sh`.

## Resumen

| Script | Tipo de endpoint | Puerto típico | Propósito |
|--------|------------------|---------------|-----------|
| `validate-cosmos-grpc-endpoint.sh` | Cosmos gRPC | 9090 | Consultas de aplicación y módulos (balances, staking, estado de cuentas). Forma estándar de consultar el estado de la cadena en el ecosistema Cosmos. |
| `validate-cosmos-rpc-endpoint.sh` | Tendermint RPC | 26657 | Datos de bajo nivel del nodo/cadena: estado de sincronización, chain ID, último bloque, consenso. Usado por relayers, exploradores y clientes a nivel Tendermint. |
| `validate-evm-rpc-endpoint.sh` | EVM JSON-RPC | 8545 | Interfaz compatible con Ethereum: balances, estado, bloques, envío de transacciones. Usado por wallets, dApps y herramientas EVM. |

**Sobre los puertos:** El "puerto típico" indicado en la tabla es el predeterminado para ese tipo de servicio. El puerto realmente configurado y expuesto en tu endpoint puede ser distinto. En nuestro ecosistema, al usar Drive, es habitual tener varios nodos o servicios en el mismo servidor; gracias a nuestra [estrategia de asignación de puertos]({{< relref "../../services/ports" >}}), el puerto expuesto en el host puede diferir del que el servicio usa internamente. Usa el puerto que el administrador haya configurado o expuesto (p. ej. en el catálogo de servicios o en el proxy inverso).

**Resultado esperado:** Cada script termina con código `0` si todas las comprobaciones pasan, y `1` si alguna falla. La salida usa colores (✓ correcto, ✗ fallo, ⚠ advertencias) y un resumen final; cuando el endpoint responde, el resumen muestra chain ID, último bloque y datos relacionados cuando aplique.

---

## 1. Cosmos gRPC (`validate-cosmos-grpc-endpoint.sh`)

**Qué hace:** Comprueba que el endpoint gRPC sea alcanzable y, cuando es posible, que exponga los servicios gRPC esperados. Opcionalmente lista servicios y llama a `GetNodeInfo` y `GetLatestBlock` para mostrar chain ID, versión del nodo, nombre de la app y último bloque.

**Comprobaciones:** Normalización de URL/host:puerto, resolución DNS, conectividad del puerto gRPC (preferiblemente con `grpcurl`; si no, prueba TCP), certificado SSL para HTTPS, lista opcional de servicios gRPC e información de cadena, y opcionalmente cabeceras CORS y de seguridad si el endpoint responde por HTTP.

**Antes de ejecutar:** Entra en la carpeta que contiene el script (desde la raíz del repositorio Drive):

```bash
cd drive/tools/validate-cosmos-grpc-endpoint
```

**Uso:**

```bash
./validate-cosmos-grpc-endpoint.sh <URL_o_host:puerto>
```

**Ejemplos:**

```bash
# Con protocolo y puerto
# (típico;
# el puerto real puede ser otro según tu configuración)
./validate-cosmos-grpc-endpoint.sh https://grpc.ejemplo.com:9090
./validate-cosmos-grpc-endpoint.sh localhost:9090
./validate-cosmos-grpc-endpoint.sh grpc.ejemplo.com:9090

# Dominio o subdominio sin puerto
# (el servidor/proxy enruta;
# común cuando el administrador apunta un subdominio al puerto del servicio)
./validate-cosmos-grpc-endpoint.sh https://grpc.ejemplo.com
```

**Requisitos:** Se recomienda `grpcurl` para una validación completa; sin él solo se usa un fallback de conectividad TCP. Opcionales: `openssl` (HTTPS), `curl`, `nc` o `/dev/tcp`, y herramientas DNS (`host`, `dig`, `nslookup`).

---

## 2. Cosmos (Tendermint) RPC (`validate-cosmos-rpc-endpoint.sh`)

**Qué hace:** Comprueba que el endpoint Tendermint RPC sea alcanzable y devuelva datos válidos. Llama a GET `/status` y valida el JSON con `result.node_info` y `result.sync_info`; muestra chain ID y altura del último bloque.

**Comprobaciones:** Normalización de URL (protocolo añadido si falta), resolución DNS, conectividad del puerto (o vía `/status` si no se indica puerto) y respuesta Tendermint `/status`.

**Antes de ejecutar:** Entra en la carpeta que contiene el script (desde la raíz del repositorio Drive):

```bash
cd drive/tools/validate-cosmos-rpc-endpoint
```

**Uso:**

```bash
./validate-cosmos-rpc-endpoint.sh <URL>
```

**Ejemplos:**

```bash
# Con protocolo y puerto
# (típico;
# el puerto real puede ser otro según tu configuración)
./validate-cosmos-rpc-endpoint.sh https://rpc.ejemplo.com:26657
./validate-cosmos-rpc-endpoint.sh http://localhost:26657
./validate-cosmos-rpc-endpoint.sh rpc.ejemplo.com:26657

# Dominio o subdominio sin puerto
# (el servidor/proxy enruta;
# común cuando el administrador apunta un subdominio al puerto del servicio)
./validate-cosmos-rpc-endpoint.sh https://rpc.ejemplo.com
```

**Requisitos:** `curl` (necesario); opcionales `nc` o `/dev/tcp` y herramientas DNS.

---

## 3. EVM RPC (`validate-evm-rpc-endpoint.sh`)

**Qué hace:** Comprueba que el endpoint EVM JSON-RPC sea alcanzable y esté bien configurado. Ejecuta varias comprobaciones, entre ellas cuatro métodos RPC (`web3_clientVersion`, `eth_blockNumber`, `net_version`, `eth_chainId`), además de cabeceras CORS y de seguridad para uso en navegador/wallet.

**Comprobaciones:** Normalización de URL, resolución DNS, conectividad, certificado SSL (HTTPS), respuesta HTTP/HTTPS, métodos RPC EVM, cabeceras CORS y cabeceras de seguridad. El resumen final indica el número total de comprobaciones (p. ej. 12+) y cuántas pasaron o fallaron.

**Antes de ejecutar:** Entra en la carpeta que contiene el script (desde la raíz del repositorio Drive):

```bash
cd drive/tools/validate-evm-rpc-endpoint
```

**Uso:**

```bash
./validate-evm-rpc-endpoint.sh <URL>
```

**Ejemplos:**

```bash
# Con protocolo y puerto
# (típico;
# el puerto real puede ser otro según tu configuración)
./validate-evm-rpc-endpoint.sh https://rpc.ejemplo.com:8545
./validate-evm-rpc-endpoint.sh http://localhost:8545
./validate-evm-rpc-endpoint.sh rpc.ejemplo.com:8545

# Dominio o subdominio sin puerto
# (el servidor/proxy enruta;
# común cuando el administrador apunta un subdominio al puerto del servicio)
./validate-evm-rpc-endpoint.sh https://evmrpc.ejemplo.com
```

**Requisitos:** `curl` (necesario); opcionales `openssl`, `nc` o `/dev/tcp` y herramientas DNS.

---

## Comportamiento común

- **Sin puertos por defecto:** Si no se indica puerto, la URL se deja tal cual; el servidor o balanceador gestiona el enrutado. Los scripts no asumen un puerto.
- **Timeouts:** El timeout de conexión por defecto es 10 segundos (algunos pasos usan timeouts más cortos para fallbacks rápidos).
- **Códigos de salida:** `0` = todas las validaciones pasaron; `1` = una o más fallaron o hubo error.
- **Compatibilidad:** Linux, macOS, BSD y sistemas Unix-like con bash 4.0+.

Los scripts cargan `common/endpoint-validation-common.sh` para compartir comportamiento: colores, ayudas de impresión, resolución DNS, tiempos y un pie de página uniforme.
