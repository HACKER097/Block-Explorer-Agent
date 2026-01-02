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

## Design

### MCP

Creating an MCP seems seems like a good way to give the agent blokchain data to reason over. Its modular, so I can keep the MCP seperate from the agent.

List of endpoints that might be useful:

- **Block to transactions**: Given a block hash, return a list of transaction hashes
- **Address to transactions**: Given an address, return a list of transaction hashes
- **Transaction to execution trace**: Given a transaction hash, return the execution trace
- **Contract to source code**: Given a contract address, return the source code, decompile if needed

Update: This list ended up being too short, and the final MCP server has a lot more endpoints.

### Block explorer

This app is a block explorer, before its an agent, I am not sure how much time I want to commit to the block explorer part. At this point I am going to fully commit to the Agentic part, so you ask the agent for everything, instead of clicking things. Will have to plan something else if its not usable.

I think a simple TUI explorer would be good, with a prompt to ask the agent and suggestions. Kinda like if Claude Code was a block explorer.

I will assume I am not allowed to use ethscan API or something similar, otherwise I am using someone elses block explorer instead of writing my own.

#### User interface

After trying to keep the block exploration part fully agenting, it have realized that its a shitty user interface, and very slow to work with for any practical use. It involves asking the agent to do things you could to in a few clicks on etherscan by yourself. The agent is also terrible at keeping track of what you want.

I am opting for a different approach, one many popular 'Agentic' apps use, that is, having the same old interface people are used to, but with a chat at the side. The agent will be the same, but have access the the user's browser

### Agent

Pretty simple, ask question, agent thinks, gets data, and returns a response.

The agent will need a bunch of pre defined exploit patterns, also the ability to lookup suspicious addresses.

#### System Prompt

This required a lot of playing around with, I iterated on the prompt in this loop:

1. Use the agent as if I am using the final product
2. Agent messes up, does not understand, or is not helpful
3. Try to understand why the agent is messing up
4. Add additional MCP tools if issue is caused by missing context
5. Clearly or add to the promot if issue is caused by the agent not doing what I would expect from the finished product
6. Repeat

## Implementation

### MCP

- FastMCP for the MCP server
- Panoramix for decompiling (used by etherscan.io) [Github](https://github.com/palkeo/panoramix)
- Web3 for interacting with the blockchain
- Kaggle dataset to get more context: https://www.kaggle.com/datasets/hamishhall/labelled-ethereum-addresses
- Using ethscan api for context: https://eth-labels-production.up.railway.app/labels/{addr}

In the end, I added a lot more mcp tools that I initially thought would be needed. Everytime I thought the agent was doing too much work to get some data, or didn't even try to get data that would have been very helpful, I added an mcp

#### Transaction trace issue:

- I can't find a good way to get the transaction trace
- Either I use a paid API, or I use caste, which is VERY slow
- This is not good, because the transaction is likelt the most helpful in finding potential exploits
- Fow now I have put in a placeholder which uses an API, I'll figure something out later
