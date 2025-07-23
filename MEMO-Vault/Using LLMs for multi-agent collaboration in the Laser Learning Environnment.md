

# 1. Introduction 

Multi-agent reinforcement learning (MARL) focuses on training multiple agents to work together in shared environments. While some environments allow agents to learn good strategies independently ( #source), others require a high level of coordination and planning ( #source). The Laser Learning Environment (LLE) is one such example, where agents must cooperate to overcome obstacles like laser beams, unreachable zones, and shared bottlenecks.   

Traditional MARL methods, such as value-based deep Q-networks ( #source), have achieved promising results on LLE’s simpler levels. However, they still struggle on the most difficult tasks, especially when long-term planning and unrewarded cooperation are required.

This project explores whether large language models (LLMs) can support agent coordination in LLE. Rather than learning from scratch, LLM agents rely on structured prompts, memory representations, and theory of mind (ToM) reasoning to plan and collaborate in zero-shot or few-shot settings.

#TODO *Still see if those are the corrects objectives*
The main objectives are:
- Combine LLMs with value-based MARL algorithms to solve tasks in LLE
- Enable agents to communicate and make cooperative decisions using LLM reasoning
- Explore how belief state prompting and ToM can support coordination
- Measure the impact on score, exit rate, and qualitative teamwork behaviors

---

# 2. State of the Art 


### 2.1 The Laser Learning Environment (LLE)

The Laser Learning Environment is a multi-agent grid world populated by agents of different colours. It includes various types of tiles: floor, start, wall, laser, laser source, and exit tiles.

The main objective in this environment is for all agents to reach the exit tile.

However, to do so, the agents must overcome several constraints. Since laser beams are deadly to agents of a different colour, an agent cannot cross a laser unless it matches their colour. To get around this, agents must cooperate, one can block a laser beam, allowing another to pass safely. This makes the game fully cooperative, as success depends on helping teammates advance through the level.

The points distribution is as follows: 
- +1 point per agent that reaches the exit tile
- +1 point if all agents reach the exit tile 
- 0 points for intermediate cooperative actions
- Negative outcome: agent death

Additionally, hidden gems scattered throughout the map provide bonus points when collected by agents.

This environment is particularly relevant because it introduces key coordination challenges:

- **a. Perfect Coordination**  
    Agents must follow a precise sequence of actions. A single mistake, like moving too early or too late, can lead to failure. For example, if an agent does not block a laser at the right moment, a teammate may be eliminated.
- **b. Interdependence**  
    Agents depend on one another to complete the task. Some areas of the map are inaccessible to a single agent acting alone. Only by helping each other can they progress.
- **c. Zero-Incentive Dynamics**  
    Essential cooperative actions, like blocking a laser for another agent, provide no direct reward. This forces agents to learn helpful behaviours even in the absence of positive feedback.

In this project, we will focus on level 6 of the LLE, which features 4 agents, 3 lasers, and 4 hidden gems.

![[LLE.png|400]]

#TODO   Present the algorithms use for this level, the results (maybe explain why the level 6 is pertinent? )

### 2.2 Cooperative Multi-Agent Reinforcement Learning

There are several cooperative multi-agent environments that have been proposed , such as **Overcooked**, **Hanabi**,the one that we presented,  the **Laser Learning Environment (LLE)**.

These environments are typically designed to test agents on tasks that require **tight coordination**, and **team-level rewards**. Most of the time, the algorithms used to address these problems are **deep Q-network (DQN)** based ( #source), extended to handle multiple agents acting simultaneously.

#### Background 

##### Deep Q-Network 

The Deep Q-Network (DQN) is one of the basic algorithms in reinforcement learning. It allows an agent to learn how to act by estimating the expected reward it can get by taking a certain action in a given state. The idea is to use a neural network to approximate the Q-function, and update it over time as the agent interacts with the environment.

In the case of multi-agent setting, there could be some difficulties especially due to **non-stationarity**: as each agent learns and updates its policy, the environment becomes unstable from the perspective of any one agent.

##### Value decomposition network 

Value Decomposition Networks (VDN) introduce a simple but effective idea: instead of learning a single joint Q-function for the entire team, the total team value is approximated as the sum of individual agents’ Q-values.

Formally:  
    Q_total(s, a₁, ..., aₙ) ≈ Σ Qᵢ(sᵢ, aᵢ)

This decomposition allows for:
#TODO *Check this* 
- **Centralized training**, where the full state and joint actions are used to compute gradients.
- **Decentralized execution**, where each agent selects its action based only on its own local observation.

VDN addresses the non-stationarity issue and enables scalable learning in cooperative tasks.

In our case, since we are focusing on the Laser Learning Environment (LLE), we highlight the fact that VDN was the algorithm that performed best among the baseline methods tested.

While VDN is relatively simple compared to more advanced algorithms like [[QMIX.pdf|QMIX]], it was found to be more robust in the LLE setting, achieving higher scores and exit rates across different levels.

### 2.3 Large Language Models for Multi-Agent Collaboration

#TODO *change GTP-4 by other thing (since chatgpt, gpt-4 and gpt4-belief were used)*

Large Language Models, especially GPT-4, have been used recently to explored the multi-agent collaboration task. 

Unlike traditional reinforcement learning approaches, LLMs are not trained through a system of reward. Instead, they rely on [[Definitions#Zero prompting|zero-shot]] or [[Definitions#Few-shot prompting|few-shot]] prompting, basing themself only on the LLM logic and the mission context. 

Recent work done by [[ToM_for_multi-agentCollab_via_LLMs.pdf|Li et al.]] demonstrate in the collaborative learning environment - where 3 agents which communicate through GPT-4 need to defuse color-coded bombs (where a sequence order needs to be respect to defuse it) scattered in an unexplored environment - that agents display emergent cooperative behaviors. 
Despite the absence of explicit multi-agent training, GPT-4 agents training exhibit: coordinated task allocation, synchronized movement and strategy negotiation and delegation. 

One key limitation of LLMs is the lack of persistent memory and internal state tracking. To address this, [[ToM_for_multi-agentCollab_via_LLMs.pdf|Li et al.]] introduce **belief state prompting**, in which each agent is given a text-based summary of what it has observed and what it believes about the environment and teammates. This technique enables the model to perform **Theory of Mind (ToM)** reasoning, that is, to make inferences about what other agents know or believe. #TODO Check 
if correct 

#TODO  *check if correct*
The use of belief states allows agents to: 
- Maintain reliable knowledge about the situation
- Keep tracks of the tools or intentions of the other agents 
- Reason about both **first-order beliefs** (what others know) and **second-order beliefs** (what others think you know)

In the bomb defusal task, GPT-4 agents equipped with belief states consistently achieve **perfect or near-perfect scores**, completing all three bomb phases with high success rates.

Some vulnerabilities remains such as proposing invalid actions or the agents having 
hallucinations.

#TODO  Find other kind of example where they use LLMs to make 2 agents cooperate? 



--- 

# 3. Proposed Approach

#### 3.1 Which LLM use (which one would be the better fit)

- Review to know which LLM would be used (which one would be the better fit)

#### 3.2 Using LLM in the LLE 

##### 3.2.1 Exploring multi-agent collaboration only with LLM

As in shown in the paper "Theory of Mind for Multi-Agent Collaboration via Large Language Models" when using the LLMs in the environment, there is not a training through system reward. Instead, they rely on zero-shot or few-shot prompting. 

That would be one of the approaches taken to implement LLMs to the Laser Learning Environment. 
Instead of using an algorithm such as VDN we would  

##### 3.2.2 Exploring multi-agent collabation with LLM and VDN 

#### 3.3 Test on different type of observation

- Try with centralized view 
- Try with decentralized view 





