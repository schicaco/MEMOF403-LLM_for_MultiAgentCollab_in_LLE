

---

## Introduction

Briefly introduce the importance of coordination in cooperative Multi-Agent Reinforcement Learning (MARL), the recent capabilities of Large Language Models (LLMs), and the motivation to combine the two in the Laser Learning Environment (LLE).

---

## Problem Statement and Objectives

This project investigates whether LLMs can support coordination in multi-agent systems by acting as decentralized communicators or planners. The objectives are:

- Integrate LLMs with value-based MARL methods in LLE
    
- Enable LLM agents to communicate and reason
    
- Study how belief states and Theory of Mind (ToM) can improve collaboration
    
- Evaluate the impact on score, exit rate, and qualitative coordination behavior
    

---

## State of the Art

### 3.1 Cooperative Multi-Agent Reinforcement Learning

- MARL formalized as Multi-Agent MDPs and Dec-POMDPs
    
- Review of IQL, VDN, and QMIX
    
- Discussion of non-stationarity and the need for value decomposition (VDN)
    

### 3.2 The Laser Learning Environment (LLE)

- Grid-world environment with multiple agents and interactive tiles (lasers, gems, exits)
    
- Coordination is required due to:
    
    - **Perfect coordination** (simultaneous actions)
        
    - **Interdependence** (agents block lasers for others)
        
    - **Zero-incentive dynamics** (key actions unrewarded)
        
- Evaluation: Score and Exit Rate
    

### 3.3 Large Language Models for Multi-Agent Collaboration

- LLMs show emergent collaboration and planning abilities
    
- Belief state prompting enhances Theory of Mind reasoning
    
- Prior work demonstrates strong zero-shot performance with GPT-4
    

---

## Proposed Approach

- Use VDN as the base RL algorithm for decentralized execution
    
- Add LLMs to generate messages and reason about teammate intent
    
- Maintain belief states as prompt context for the LLM
    
- Develop a text interface to LLE for LLM-agent interaction
    
- Evaluate performance, communication quality, and ToM reasoning
    

---

