# Cool Agent - Project Report

## Problem statement

Design a simple agentic block explorer that can detect and flag malicious on-chain behavior by analyzing transactions and contract activity. The system should demonstrate how autonomous agents can reason over blockchain data and identify exploit-like patterns.

---

## Understanding the problem statement

The problem statement leaves many things unclear. These are questions I needed to answer before starting:

- **`identify exploit-like patterns`** → Agent decides, not hardcoded rules
- **`reason over blockchain data`** → Iterative investigation loop

---

## Constraints

Requirements identified from the prompt:

1. **Agentic block explorer**
2. **Must analyze transactions and contract activity** 
3. **Reason over blockchain data**

---

## Interpretation

### What does `identify exploit-like patterns` mean?

- Let the agent decide what "exploit-like" means
- Compile exploit patterns as context, not rules
- No manual if/else decisions
- Agent reasons over data and draws conclusions

### What does it mean to `reason over blockchain data`?

Here is the reasoning loop that I came up with:

```
Agent reads data
    ↓
Interprets what it read
    ↓
Decides what additional data to fetch
    ↓
Iterates until satisfied
    ↓
Makes a reasoned decision
```

---

## Design

### MCP

Creating an MCP seemed like the right approach.

**Initial endpoint list (too short):**

- `block_to_transactions` 
- `address_to_transactions`
- `transaction_to_trace`
- `contract_to_source` 

> **What happened**: The list grew significantly. Every time the agent struggled for data, I added an MCP tool instead of fixing prompts.

Putting the full list won't add much to the report, but you can read the code to get it

### Block explorer

This app is a block explorer before its an agent. Initial approach: fully agent-driven, no traditional UI.

This was not a good idea, because of the following reasons:

- Slow, frustrating for simple queries
- Agent loses track of intent
- "Shitty user interface"
- Changed approach

**Final approach**: Browser integration for context, with a chat on the side. "Its cursor but for the blockchain!"

### Agent

Simple concept: ask question, agent thinks, gets data, returns answer.

**Required capabilities:**

- Pre-defined exploit patterns as context
- Address reputation lookup
- Contract code analysis

#### System Prompt

Iterated extensively. The loop that worked:

1. Use the agent as if testing the product
2. Identify where it messes up
3. Diagnose: missing data? unclear instructions?
4. **Add MCP tool** if data access is the issue
5. **Refine prompt** if behavioral issues
6. Repeat

> **Finding**: Adding tools was faster than perfecting prompts.

---

## Implementation

### MCP stack

```
FastMCP          → MCP server framework
Panoramix        → Decompiler (etherscan uses this)
Web3.py          → Blockchain interaction
Kaggle dataset   → Labeled addresses (local)
Eth-labels API   → Reputation data (remote)
4byte.directory  → Function signature lookup
Flashbots RPC    → Free Ethereum endpoint
```

### Context system

Context is VERY important, I did a lot of things to inject more information that what the RPC gives.

**Dual-layer approach:**

```
Layer 1: Local (Kaggle dataset)
    → Fast, free, labeled addresses
    
Layer 2: Remote (Eth-labels API)  
    → Fresh data, reputation flags
```

**Agent queries return:**

- Is this address labeled?
- What is it labeled as?
- Any reputation flags?
- Previous incidents?

**ERC-20 context:**

- Anytime there is a ERC-20 transfer, I get its contract address
- I can fetch the token name and symbol and decimals using the RPC
- Inject it into the JSON returned by web3.py

### Decompiler

Most contracts lack verified source. Panoramix integration lets agent read the code without relying on an API

**Agent capabilities now:**

- Fetch bytecode for any contract
- Decompile to readable pseudocode
- Find hidden functions

> This is essential. The agent can verify what the contract *actually* does.

### Transaction trace issue

**Problem:** Transaction traces are the most useful data for exploit detection.

**Options:**

- **Paid API** → Cost, complexity
- **Geth debug_trace** → Requires archive node
- **caste** → Very slow

**Current state:** Placeholder API. Need to figure this out properly.

### Browser integration

I wanted context awareness, so it feels like me and the Agent are on the same page. If user says "is this suspicious" while looking at etherscan, agent should know what "this" is.

**BroTab integration enables:**

1. Get active browser tab
2. Check if etherscan URL
3. Extract address/tx from URL
4. Analyze that entity

> Natural language queries work because agent sees what user sees.

### Agent architecture

**Multi-agent orchestration:**

```
Main Orchestrator (blockchain-analyst)
         │
    ┌────┼────┐
    ↓    ↓    ↓
  Data  Context  Security
 Collector Enricher Analyzer
              ↓
         Reality
          Check
```

**Workflow:**

1. User asks question
2. Main agent spawns subagents
3. Data collector fetches blockchain data
4. Context enricher adds labels/flags
5. Security analyzer looks for patterns
6. **Reality check challenges findings**
7. Main agent synthesizes output

**Why reality check matters:** Security analyzers flag things aggressively. Reality check actively seeks benign explanations. Prevents false positives.

---

## What worked and what didnt

### What worked

- MCP approach. The agent has access to all the data it needs through clean tool interfaces.
- Adding MCP tools when the agent struggled. Instead of fixing the prompt, I just added more tools.
- The reality check agent. It catches a lot of false positives.
- Browser integration. Natural language queries work way better when the agent knows what youre looking at.
- Panoramix decompilation. Being able to read contract code is essential for security analysis.

### What didnt work

- Fully agentic UI. Asking the agent to navigate blocks and transactions is slow and frustrating.
- Transaction traces. Still dont have a good solution for this.
- Prompt iteration. It took forever to get the agent to behave consistently. Adding MCP tools was faster than fixing prompts.

## Resources used

- FastMCP for the MCP server
- Panoramix decompiler
- Web3.py for blockchain interaction
- Flashbots RPC (free, no API key)
- Kaggle labeled addresses dataset
- Eth-labels API
- 4byte.directory for function signatures
- BroTab for browser integration

## Thoughts

The agent is surprisingly good at finding patterns. When I watched it analyze a suspicious transaction, it correctly identified that a large transfer to a new wallet looked like money laundering. But then the reality check agent found that the destination wallet was a public project sacrifice wallet, and the transfer was actually legitimate project participation.

The key insight is that pattern matching alone is not enough. You need context, and you need to challenge your conclusions. The multi-agent architecture with reality checking is what makes this useful.

## Interesting findings

Heres some stuff the agent did that surprised me:

### The ProveX sacrifice wallet

The user asked about a transaction transferring 200 ETH to a fresh wallet. The security analyzer flagged it as CRITICAL risk. Heres why:

- 200 ETH to a wallet with zero history
- Sender wallet nearly emptied, left with 0.000093 ETH
- Recipient now holds 121,233 ETH from a single incoming transaction
- Pattern matched money laundering consolidation

The reality check agent searched for the recipient address and found it was publicly listed as the official Richard Heart ProveX project sacrifice wallet. The "suspicious" pattern was actually expected behavior for a project fundraising mechanism.

Final verdict: 95% legitimate, 5% suspicious. The agent changed its mind when given context. This is what I wanted the system to do.

### The honeypot contract

User asked about a token contract that looked legit on etherscan.

The agent:
1. Decompiled the bytecode using Panoramix
2. Found a hidden function that only the owner could call
3. That function could set any address balance to zero
4. The "transfer" function had a fake require statement that only passed for the owner

### The context switch

User was browsing etherscan, looking at an address. They said "what is this" without pasting anything.

The agent:
1. Detected the active etherscan tab
2. Extracted the address from the URL
3. Querried the address details
4. Cross-referenced with Kaggle dataset
5. Found the address was labeled as "Bybit Hot Wallet"

The agent knew what "this" meant because it saw what the user was looking at. No copy pasting required.

### The reentrancy guard that was actually a trap

User asked about a yield farm contract. On the surface it had a reentrancy guard, which is good practice.

The agent decompiled it and found:
- The guard was present but checked the wrong variable
- The actual state change happened after the external call
- The guard could be bypassed by calling through a specific function

The "guard" was there to make auditors feel good while the actual vulnerability remained. The agent caught this by reading the bytecode.

## What I would add next

- Address transaction history. Right now I can get balance and nonce, but not the full transaction history for an address.
- Transaction traces. Still need to figure this out.
- Multi-chain support. The agent is Ethereum-only right now.

## Files

```
/home/truegav/Projects/Cool-Agent/
├── MCP/
│   ├── main.py              # FastMCP server with all tools
│   ├── Context.py           # Dual-layer context system
│   ├── Decompiler.py        # Panoramix integration
│   ├── browser_connect.py   # BroTab integration
│   └── eth_addresses.csv    # Kaggle dataset
├── .opencode/agent/         # Agent prompts
│   ├── blockchain-analyst.md
│   ├── @blockchain-data-collector.md
│   ├── @blockchain-security-analyzer.md
│   ├── @blockchain-context-enricher.md
│   ├── @blockchain-reality-check.md
│   └── @blockchain-fast-mode.md
└── opencode.jsonc           # OpenCode configuration
```

## End

The project works. Its not perfect, but it demonstrates that autonomous agents can reason over blockchain data and identify potentially malicious patterns. The key is giving the agent good data access, letting it spawn specialized subagents, and requiring it to challenge its own conclusions.
