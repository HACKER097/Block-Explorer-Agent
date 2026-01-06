# Project Planning

- [x] Define project scope and constraints
- [x] Research agentic block explorer patterns
- [x] Design MCP architecture
- [x] Choose tech stack (FastMCP, Web3.py, Panoramix)
- [x] Plan agent reasoning loop
- [x] Create initial task list

# MCP Server

## Setup & Infrastructure
- [x] Initialize FastMCP server
- [x] Configure Web3 RPC connection (eth.llamarpc.com)
- [x] Set up project structure
- [x] Implement ERC-20 ABI for token interactions

## Core Endpoints
- [x] Block to transactions
- [ ] Address to transactions (needs API integration)
- [x] Transaction to execution trace (using debug_traceTransaction)
- [x] Contract to source code/decompilation
- [x] Details about a transaction
- [x] Details about a contract
- [x] Details about an address

## Context & Security
- [x] Suspicious addresses database integration
  - [x] Kaggle dataset integration
  - [x] eth-labels API integration
- [x] Address context enrichment
- [ ] Address to transactions endpoint (blocked by API requirement)

## Additional Features
- [x] Get latest block number
- [x] Get ERC-20 token details (name, symbol, decimals, total supply)
- [x] Browser integration for Etherscan tab detection
  - [x] BroTab integration
  - [x] Active tab detection
  - [ ] Handle multiple Etherscan tabs
- [x] Contract code decompilation with Panoramix
- [ ] Improve transaction trace performance
- [ ] Add caching layer for frequently accessed data
- [ ] Implement rate limiting for API calls

# Block Explorer

- [x] Initial UI design - TUI vs chat
- [x] Decide on hybrid approach (traditional UI + agent chat)
- [ ] Implement basic web interface
- [ ] Integrate agent chat with Etherscan tab context

# Agent

## System Prompt Development
- [x] Define agent personality and role
- [x] Implement context awareness for Etherscan tabs
- [x] Add intent recognition logic
- [x] Define security analysis protocol
- [x] Add token handling rules
- [ ] Implement memory for context retention

## Capabilities
- [x] Security analysis and threat detection
- [x] Pattern recognition (flash loans, reentrancy, etc.)
- [x] Contract vulnerability detection
- [x] Malicious actor identification
- [x] Transaction flow analysis
- [ ] Exploit database lookup
- [-] Generate detailed security reports

## Integration
- [x] Connect to MCP server
- [x] Implement reasoning loop
- [x] Add web search for security resources validation

