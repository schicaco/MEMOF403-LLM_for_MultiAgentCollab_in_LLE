
# Introduction 

---

# Problem Statement and Objectives 

See if it change something if it is decentrelised or centrelised observation for each agent

---

# State of the Art 

### 3.1 Cooperative Multi-Agent Reinforcement Learning

### 3.2 The Laser Learning Environment (LLE)

The Laser Learning Environment is a multi-agent grid world populated by agents of different colours. It includes various types of tiles: floor, start, wall, laser, laser source, and exit tiles.

The main objective in this environment is for all agents to reach the exit tile.

However, to do so, the agents must overcome several constraints. Since laser beams are deadly to agents of a different colour, an agent cannot cross a laser unless it matches their colour. To get around this, agents must cooperate—one can block a laser beam, allowing another to pass safely. This makes the game fully cooperative, as success depends on helping teammates advance through the level.

The points distribution is as follows: 
- +1 point per agent that reaches the exit tile
- +1 point if all agents reach the exit tile 
- +1 point per gem collected
- 0 points for intermediate cooperative actions
- Negative outcome: agent death

Additionally, hidden gems scattered throughout the map provide bonus points when collected by agents.

This environment is particularly relevant because it introduces key coordination challenges:

- **a. Perfect Coordination**  
    Agents must follow a precise sequence of actions. A single mistake, like moving too early or too late, can lead to failure. For example, if an agent does not block a laser at the right moment, a teammate may be eliminated.
    
- **b. Interdependence**  
    Agents depend on one another to complete the task. Some areas of the map are inaccessible to a single agent acting alone. Only by helping each other can they progress.
    
- **c. Zero-Incentive Dynamics**  
    Crucial cooperative actions, like blocking a laser for another agent, provide no direct reward. This forces agents to learn helpful behaviours even in the absence of positive feedback.

In this project, we will focus on level 6 of the LLE, which features 4 agents, 3 lasers, and 4 hidden gems.

![[LLE.png|400]]

### 3.3 Large Language Models for Multi-Agent Collaboration

Large Languade Model, specially GPT-4, have been used recently to explored the multi-agent collaboration task. 

Unlike traditional reinforcement learning approaches, LLMs are not trained through a system of reward. Instead, they rely on [[Definitions#Zero prompting|zero-shot]] or [[Definitions#Few-shot prompting|few-shot]] prompting, basing themself only on the LLM logic and the mission context. 

Recent work done by [[ToM_for_multi-agentCollab_via_LLMs.pdf|Li et al.]] demonstrate in the collaborative learning environment - where 3 agents which communicate through GPT-4 need to defuse color-coded bombs (where a sequence order needs to be respect to defuse it) scattered in an unexplored environment - display emergent cooperative behaviors. 

Despite the absence of explicit multi-agent training, GPT-4 agents training exhibit: coordinated tasl allocation, synchronized movement and strategy negotiation and delegation. 

One key limitation of LLMs is the lack of persistent memory and internal state tracking. To address this, [[ToM_for_multi-agentCollab_via_LLMs.pdf|Li et al.]] introduce **belief state prompting**, in which each agent is given a text-based summary of what it has observed and what it believes about the environment and teammates. This technique enables the model to perform **Theory of Mind (ToM)** reasoning—that is, to make inferences about what other agents know or believe.

The use of belief states allows agents to: 
- Maintain reliable knowledge about the situation
- keep tracks of the tools or intentions of the other agents 
- Reason about both **first-order beliefs** (what others know) and **second-order beliefs** (what others think you know)

In the bomb defusal task, GPT-4 agents equipped with belief states consistently achieve **perfect or near-perfect scores**, completing all three bomb phases with high success rates.

Some vulnabiities remains such as proposing invalid actions or the agents having hallucinations. 
#### Comparison with MARL 

The same environment of [[ToM_for_multi-agentCollab_via_LLMs.pdf| Li et al.]] was tested with **MAPPO**, a multi-agent reinforcement learning algorithm. MAPPO required environment interaction and shaped rewards (e.g., small bonuses for correct tool usage) to learn effective policies. While MAPPO eventually outperformed GPT-4 in terms of action efficiency, it required extensive training and hyperparameter tuning.

In contrast, **LLMs required no gradient-based training**, instead leveraging pretraining and structured prompts to plan and coordinate. Planning-based agents (like CBS) performed optimally under full observability but lacked generality across tasks or environments.




--- 

# Proposed Approach




