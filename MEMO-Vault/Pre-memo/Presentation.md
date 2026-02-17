
# LLE challenges 

## This environment is particularly relevant because it introduces key coordination
challenges:
-  Perfect Coordination
	**Agents must follow a precise sequence of actions.** A single mistake, like moving too early or too late, can lead to failure. For example, if an agent does not block a laser at the right moment, a teammate may be eliminated.

-  Interdependence
	**Agents depend on one another to complete the task**. Some areas of the map are inaccessible to a single agent acting alone. Only by helping each other they can progress.

-  Zero-Incentive Dynamics
	**Essential cooperative actions**, like blocking a laser for another agent, **provide no direct reward**. This forces agents to learn helpful behaviours even in the absence of positive reward.

## VDN  (Value Decomposition Network): Deep Q-Based network. 

Non-stationary : Each agent influences the environment, so what one agent learns changes the experience of the others.

Deals with the non-stationarity problem, ather than learning a single joint Q-function for the entire team, the total team value is approximated as the sum of the individual Q-values of each agent.

VDN achieved the best results but failed to solve the task fully.
- None of the algorithms ever reaches the highest possible score of 9 and at most half of the agents ever reach the end exit tiles.

# LLM agents fot multi-agent collaboration 

## Chain of thoughts 

Method that encourages language models to **generate intermediate reasoning steps** before arriving at a final answer. Rather than immediately producing a solution, the model **is prompted to reason through the task step-by-step** in natural language.

## Belief state 

Due to input length constraints, the full interaction history cannot be included at every step. Instead, each agent maintains a structured, compressed summary of its understanding of the world, encoded as a belief state and injected into the prompt at each round.

This belief state includes:
• A summary of recent observations;
• Inferred knowledge or intentions of teammates


Text: 
The approach relies on **zero-shot or few-shot prompting**, where the model only receives a description of the mission context. We incorporate **Chain-of-Thought prompting** to guide reasoning and **belief state prompting** to maintain an updated view of the environment. In terms of performance, teams using **GPT-4** consistently achieve full scores, with belief states further improving efficiency. However, some limitations remain, including the generation of **invalid actions** and occasional **hallucinations** about the environment.


The setup uses **zero-shot or few-shot prompting**, where each agent receives only the **mission context**—no full map or hidden state information. Agents interact by **exchanging natural language messages** based on their own observations and belief states. This minimal input still leads to **emergent cooperative behaviors**, as agents share updates, coordinate actions, and adapt to each other’s moves. We apply **Chain-of-Thought prompting** for step-by-step reasoning and **belief state prompting** to help each agent track the environment over time. In performance tests, **GPT-4** teams reach full scores, with belief states improving efficiency. Limitations include occasional **invalid actions** and **hallucinations** about unseen parts of the environment.