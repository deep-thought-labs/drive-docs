---
title: "Technical Initialization Flow"
weight: 407
---

The node initialization process is a complex flow involving multiple steps, validations, and configurations. This section documents the complete technical initialization flow.

## Overview

The initialization process (`node-init`) performs the following tasks:

1. Previous state verification
2. Moniker retrieval
3. Execution of `infinited init` command
4. Official genesis download and validation
5. Final configuration

## Detailed Flow

### 1. Previous State Verification

Before starting, the script verifies if the node is already initialized:

```bash
if [ -f "$NODE_GENESIS_FILE" ]; then
    print_warning "The node is already initialized."
    echo "   Genesis file found: ${CYAN}$NODE_GENESIS_FILE${RESET}"
    echo "   To reinitialize, delete the directory: ${CYAN}rm -rf ${NODE_HOME}/*${RESET}"
    exit 1
fi
```

**Verification:**
- Looks for the `genesis.json` file in `~/.infinited/config/`
- If it exists, assumes the node is already initialized
- Provides instructions to reinitialize if necessary

### 2. Argument Parsing

The script parses command line arguments:

```bash
RECOVERY_MODE=false
MONIKER=""

for arg in "$@"; do
    case $arg in
        --recover|-r)
            RECOVERY_MODE=true
            ;;
        *)
            # If not a flag and moniker is empty, treat as moniker
            if [ -z "$MONIKER" ] && [ "$arg" != "--recover" ] && [ "$arg" != "-r" ]; then
                MONIKER="$arg"
            fi
            ;;
    esac
done
```

**Supported arguments:**
- `--recover` or `-r`: Activates recovery mode
- First non-flag argument: Treated as moniker

**Examples:**
```bash
node-init my-node                    # Moniker: "my-node"
node-init --recover my-node         # Recovery mode, moniker: "my-node"
node-init my-node --recover         # Moniker: "my-node", recovery mode
```

### 3. Moniker Retrieval

The moniker is obtained in two ways:

#### From Argument

If provided as an argument, it's validated:

```bash
if [ -n "$provided_moniker" ]; then
    provided_moniker=$(echo "$provided_moniker" | xargs)  # Trim whitespace
    if [ -z "$provided_moniker" ] || [ -z "${provided_moniker// }" ]; then
        print_error "Moniker cannot be empty or whitespace only"
        provided_moniker=""
    else
        echo "$provided_moniker"
        return 0
    fi
fi
```

#### Interactively

If not provided and the terminal is interactive:

```bash
if is_interactive; then
    while true; do
        read -p "Moniker: " input_moniker < /dev/tty
        input_moniker=$(echo "$input_moniker" | xargs)  # Trim
        if [ -z "$input_moniker" ] || [ -z "${input_moniker// }" ]; then
            print_error "Moniker cannot be empty or whitespace only. Please try again."
            continue
        else
            echo "$input_moniker"
            return 0
        fi
    done
fi
```

**Validations:**
- Cannot be empty
- Cannot be only whitespace
- Automatically trimmed

### 4. Initialization Mode

The script supports two initialization modes:

#### Simple Mode (Without Seed Phrase)

```bash
if [ "$RECOVERY_MODE" != true ]; then
    # Show warnings about random keys
    print_warning "IMPORTANT: Random Keys Will Be Generated"
    
    # Interactive confirmation
    if is_interactive; then
        echo "Do you want to continue with random key generation? (yes/no)"
        read -p "Continue? " response
        case $response in
            [Yy][Ee][Ss]|y|Y)
                break
                ;;
            [Nn][Oo]|n|N)
                exit 0
                ;;
        esac
    fi
    
    # Execute init without --recover
    "${NODE_BINARY_PATH}" init "${MONIKER}" \
        --chain-id "${NODE_CHAIN_ID}" \
        --home "${NODE_HOME}" > /dev/null 2>&1
fi
```

**Characteristics:**
- Automatically generates random keys
- Doesn't show or save the seed phrase
- Not recoverable with seed phrase
- Suitable for full nodes (not validators)

#### Recovery Mode (With Seed Phrase)

```bash
if [ "$RECOVERY_MODE" = true ]; then
    print_step "Recovery Mode Activated"
    print_warning "IMPORTANT: You will be prompted to enter your seed phrase."
    
    # Execute init with --recover
    "${NODE_BINARY_PATH}" init "${MONIKER}" \
        --chain-id "${NODE_CHAIN_ID}" \
        --home "${NODE_HOME}" \
        --recover > /dev/null
fi
```

**Characteristics:**
- Requests seed phrase from user
- Validates seed phrase format
- Allows recovering existing keys
- Suitable for validators or nodes that need recovery

**Note:** The output of `infinited init --recover` is redirected only to `/dev/null` (stdout), keeping stderr for interactive seed phrase prompts.

### 5. Post-Initialization Verification

After executing `infinited init`, the script verifies it was successful:

```bash
if [ ! -f "$NODE_GENESIS_FILE" ]; then
    print_error "The genesis.json file was not generated correctly."
    exit 1
fi
```

**Verification:**
- Confirms that `genesis.json` was created
- If it doesn't exist, the process fails with error

### 6. Official Genesis Download

The script downloads the official genesis from the repository:

```bash
print_step "Downloading Official Genesis File"
echo "Source: ${CYAN}${NODE_GENESIS_URL}${RESET}"

# Download genesis
if wget --tries=3 --timeout=30 --quiet \
    --output-document="${NODE_GENESIS_FILE}.tmp" \
    "${NODE_GENESIS_URL}"; then
    
    # Validate JSON
    if jq empty "${NODE_GENESIS_FILE}.tmp" > /dev/null 2>&1; then
        mv "${NODE_GENESIS_FILE}.tmp" "$NODE_GENESIS_FILE"
        print_success "Official genesis file implemented correctly"
    else
        print_warning "The downloaded file is not valid JSON."
        rm -f "${NODE_GENESIS_FILE}.tmp"
    fi
else
    print_warning "Could not download the official genesis."
    rm -f "${NODE_GENESIS_FILE}.tmp" 2>/dev/null || true
fi
```

**Process:**

1. **Download:** Uses `wget` with 3 attempts and 30 second timeout
2. **JSON Validation:** Uses `jq` to validate that the file is valid JSON
3. **Replacement:** If valid, replaces the genesis generated by `init`
4. **Fallback:** If download or validation fails, keeps the genesis generated by `init`

**Characteristics:**
- Silent download (`--quiet`)
- JSON format validation
- Graceful error handling
- Temporary file to avoid corruption

### 7. Final Configuration

After initialization, the script shows summary information:

```bash
print_success "Node initialized successfully!"
echo "   Configuration location: ${CYAN}${NODE_HOME}${RESET}"

echo "${BOLD}To start the node:${RESET}"
print_code "Inside container: node-start"
print_code "From host: docker compose exec infinite-drive node-start"
```

## Complete Flow

```
User runs: node-init [--recover] [moniker]
    ↓
Already initialized?
    ├─ Yes → Show warning and exit
    └─ No → Continue
    ↓
Parse arguments (--recover, moniker)
    ↓
Moniker provided?
    ├─ No → Request interactively
    └─ Yes → Validate and use
    ↓
Recovery mode?
    ├─ Yes → Execute: infinited init --recover
    │       (requests seed phrase interactively)
    └─ No → Show warning about random keys
            Confirm?
            ├─ No → Exit
            └─ Yes → Execute: infinited init
    ↓
Genesis.json created?
    ├─ No → Error and exit
    └─ Yes → Continue
    ↓
Download official genesis
    ↓
Download successful?
    ├─ Yes → Valid JSON?
    │       ├─ Yes → Replace genesis
    │       └─ No → Keep generated genesis
    └─ No → Keep generated genesis
    ↓
Show summary and finish
```

## Files Created During Initialization

### Generated Structure

```
~/.infinited/
├── config/
│   ├── genesis.json          # Genesis (official or generated)
│   ├── config.toml           # Node configuration
│   ├── app.toml              # Application configuration
│   └── client.toml           # Client configuration
├── data/                     # Data directory (empty initially)
└── keyring-file/             # Keyring with generated keys
```

### Configuration Files

**`config.toml`:**
- P2P network configuration
- Ports (26656 for P2P, 26657 for RPC)
- Peer and seed configuration
- Timeout configuration

**`app.toml`:**
- Blockchain application configuration
- Gas limits
- API configuration
- gRPC configuration

**`client.toml`:**
- CLI client configuration
- Chain ID
- Keyring backend
- Output format

## Environment Variables Used

```bash
NODE_CHAIN_ID              # Chain ID for initialization
NODE_HOME                  # Node home directory
NODE_BINARY_PATH           # Path to infinited binary
NODE_GENESIS_FILE          # Path to genesis file
NODE_GENESIS_URL           # Official genesis URL
```

## Error Handling

### Common Errors

1. **Node already initialized:**
   - Clear message indicating it's already initialized
   - Instructions to reinitialize

2. **Invalid moniker:**
   - Real-time validation
   - Clear error messages
   - Retry in interactive mode

3. **Genesis download failure:**
   - Warning, not fatal error
   - Uses genesis generated by `init`
   - Process continues

4. **Invalid genesis JSON:**
   - Validation with `jq`
   - Keeps generated genesis if downloaded one is invalid

## Non-Interactive Mode

The script supports non-interactive mode for automation:

```bash
# Simple mode
node-init my-node-name

# Recovery mode
node-init --recover my-node-name
```

**Limitations:**
- Cannot request moniker interactively
- Cannot request confirmation for random keys
- Cannot request seed phrase (must be provided another way)

## See Also

- [Internal Configuration System]({{< relref "configuration-system" >}}) - Variables used in initialization
- [Internal Directory Structure]({{< relref "directory-structure" >}}) - Where files are created
- [Container Internal Scripts]({{< relref "internal-scripts" >}}) - node-init script implementation

