---
title: "Transacción Create-Validator"
---
Guía paso a paso para unirse a una blockchain en vivo como validador. Asegúrate de entender los conceptos básicos de [Clave](/es/concepts/key/) y [Keyring](/es/concepts/keyring/) antes de continuar.

## Requisitos previos

> [!important]
> - La clave del validador se restaura al inicializar tu nodo. [Ver Inicialización](/es/concepts/node-initialization/)
>
> - La sincronización del nodo está completada
>
> - La misma clave está restaurada en tu keyring

## 0️⃣ Conserva tu clave pública del validador

Guarda el valor de la clave pública de tu validador para uso posterior.
```bash
cd ~/drive/services/node0-infinite

# entrar en bash
./drive.sh exec infinite bash

# luego, ejecutar
infinited comet show-validator --home ~/.infinited

# salir de bash
exit
```

## 1️⃣ Crear un archivo `validator.json` en el directorio persistent-data

```bash
cd persistent-data

nano validator.json
```

La primera vez que abras el archivo estará vacío.  
Edítalo como se muestra a continuación:

```json
{
  "pubkey": {
    "@type": "/cosmos.crypto.ed25519.PubKey",
    "key": "<TU_CLAVE_PUBLICA_AQUI>"
  },
  "amount": "1000000000000000000drop",
  "moniker": "<TU_MONIKER>",
  "identity": "",
  "website": "",
  "security": "",
  "details": "",
  "commission-rate": "0.10",
  "commission-max-rate": "0.20",
  "commission-max-change-rate": "0.01",
  "min-self-delegation": "1000000000000000000"
}
```

- **amount:** 1 [42] = `1000000000000000000drop` 
- **key:** Introduce el valor de la clave pública de tu validador.
- **moniker:** El nombre mostrado en el explorador de bloques.

La cantidad mínima de auto-delegación es 1000000000000000000drop; por debajo de esto el validador no podrá arrancar correctamente. Los parámetros de comisión y auto-delegación están configurados con valores por defecto típicos.  

---

### Verificar antes de ejecutar

#### 1. Confirmar que tu clave existe dentro del contenedor

```bash
infinited keys list \
  --keyring-backend file \
  --home ~/.infinited
```

Si aparecen el `validator` (o el nombre que hayas usado) y su dirección, puedes continuar.  
Si no, debes restaurar la cuenta en el keyring con `--recover`. La clave es esencial para firmar bloques.

#### 2. Comprobar el balance de tu wallet

```bash
infinited q bank balances <infinite1_tu_direccion> \
  --home /home/ubuntu/.infinited
```

Como tu dirección no tiene fondos inicialmente, se enviarán los fondos semilla para validadores distribuidos por Genesis a tu dirección. Se distribuirán **2 [42]** por validador. **Haz stake de 1 token y conserva el resto para las comisiones de gas.**

>[!note]
> Para recibir tokens semilla para validadores, comparte tu dirección con **Cypher Xenia (@XeniaCypher88)** en Telegram.

---

## 3️⃣ Ejecutar `create-validator` dentro del bash del contenedor

Ejecuta el siguiente comando dentro de tu contenedor:

```bash
infinited tx staking create-validator \
  /home/ubuntu/.infinited/validator.json \
  --from <NOMBRE_DE_TU_CLAVE> \
  --chain-id infinite_421018-1 \
  --keyring-backend file \
  --home ~/.infinited \
  --gas auto \
  --gas-adjustment 1.3 \
  --gas-prices 0.025drop \
  -y
```

---

## 4️⃣ Verificar tras el éxito de la transacción

Una vez confirmada la transacción, ejecuta lo siguiente para verificar tu validador:

```bash
infinited query staking validators \
  --home /home/ubuntu/.infinited 
```

✅ Si tu **moniker** aparece en la lista, tu validador se ha registrado correctamente.
