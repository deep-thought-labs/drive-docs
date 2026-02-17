---
title: "Create-Validator Transaction"
---
A step-by-step guide to joining a live blockchain as a validator. Please make sure you understand the basic concepts of [Key](/en/concepts/key/) and [Keyring](/en/concepts/keyring/) before proceeding.

## Prerequisites

> [!important]
> - The validator key is restored when initialized your node. [See Initialization](/en/concepts/node-initialization/)
>
> - Node sync is completed
>
> - The same key is restored in your keyring

## 0️⃣ Keep your validator pub key

Keep the public key value of your validator for later use.
```bash
cd ~/drive/services/node0-infinite

# enter bash
./drive.sh exec infinite bash

# then, run
infinited comet show-validator --home ~/.infinited

# exit bash
exit
```

## 1️⃣ Create a `validator.json` file under the persistent-data directory

```bash
cd persistent-data

nano validator.json
```

The first time you open the file, it will be empty.  
Edit it as shown below:

```json
{
  "pubkey": {
    "@type": "/cosmos.crypto.ed25519.PubKey",
    "key": "<YOUR_PUBLIC_KEY_HERE>"
  },
  "amount": "1000000000000000000drop",
  "moniker": "<YOUR_MONIKER>",
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
- **key:** Enter the public key value of your validator.
- **moniker:** The name displayed on the block explorer.

The minimum amount for self-delegation is 1000000000000000000drop, below which the validator will not be able to start successfully. The commission and self-delegation parameters are set to typical defaults.  

---

### Verify before execution

#### 1. Confirm your key exists inside the container

```bash
infinited keys list \
  --keyring-backend file \
  --home ~/.infinited
```

If the `validator` (or whatever name you used) and its address appear, you’re good to go.  
If not, you need to restore the account into the keyring using `--recover`. Key is essential for signing blocks

#### 2. Check your wallet balance

```bash
infinited q bank balances <infinite1_your_address> \
  --home /home/ubuntu/.infinited
```

Since your address does not have any funds initially, we will send the seed funds for validators distributed by Genesis to your address. **2 [42]** will be distributed per validator. Please **stake 1 token and keep the rest for gas fees.**

>[!note]
> To receive seed tokens for validators, share your address with **Cypher Xenia (@XeniaCypher88)** on Telegram.

---

## 3️⃣ Execute `create-validator` inside the container bash

Run the following command inside your container:

```bash
infinited tx staking create-validator \
  /home/ubuntu/.infinited/validator.json \
  --from <YOUR KEY NAME> \
  --chain-id infinite_421018-1 \
  --keyring-backend file \
  --home ~/.infinited \
  --gas auto \
  --gas-adjustment 1.3 \
  --gas-prices 0.025drop \
  -y
```

---

## 4️⃣ Verify after transaction success

Once your transaction is confirmed, run the following to verify your validator:

```bash
infinited query staking validators \
  --home /home/ubuntu/.infinited 
```

✅ If your **moniker** appears in the list, your validator has been successfully registered.