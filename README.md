# Lamport Distributed Mutual Exclusion Simulation

## Introduction
This project simulates Lamport's Distributed Mutual Exclusion algorithm using SimPy and Streamlit.

## Algorithm Phases

### 1. REQUEST
Each process sends a timestamped request to all other processes.

### 2. WAIT
The process waits until:
- It receives replies from all processes
- Its request has the smallest timestamp

### 3. RELEASE
After exiting the Critical Section, the process sends a RELEASE message.

## Lamport Clock Rule
- On send → increment clock  
- On receive → max(local, received) + 1  

## Safety Property
No two processes enter the Critical Section simultaneously.

## Message Complexity
For N processes:
- REQUEST: N-1  
- REPLY: N-1  
- RELEASE: N-1  

Total = 3(N-1)

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py