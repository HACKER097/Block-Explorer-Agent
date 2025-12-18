## Understanding the prompt

The prompt leaves many things unclear, I am guessing this is intentional. These are some questions I need to answer for myself before I begin the project.

1. What does `identify exploit-like patterns` mean?
2. What does it mean to `reason over blockchain data`?

## Constraints

Here are the required constraints/features I found in the prompt:

1. Agentic block explorer
2. Must analyze transactions and contract activity
3. Reason over blockchain data

## Interpretation

### What does `identify exploit-like patterns` mean?

- I will let the agent decide what exploit-like is 
- I will compile a list of exploit-like patterns, and feed it to the agent as context
- There will be no manual if/else to make decisions, The agent should be able to reason over the data and make decisions

### What does it mean to `reason over blockchain data`?

- The agent should be able to read blokchain data, and make it's next decisions based on it
- I imagine a reasoning loop, where agent reads data, interprits it, decides what data to read next, until its satisfied and can make a decision

## Implementation

### MCP

Creating an MCP seems seems like a good way to give the agent blokchain data to reason over. Its modular, so I can keep the MCP seperate from the agent.

List of endpoints that might be useful:

- **Block to transactions**: Given a block hash, return a list of transaction hashes
- **Address to transactions**: Given an address, return a list of transaction hashes
- **Transaction to execution trace**: Given a transaction hash, return the execution trace
- **Contract to source code**: Given a contract address, return the source code, decompile if needed

### Agent

I want the agent 
