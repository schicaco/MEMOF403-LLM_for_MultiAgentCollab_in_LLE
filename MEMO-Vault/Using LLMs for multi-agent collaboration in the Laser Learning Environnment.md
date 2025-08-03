

# 1. Introduction 

Multi-agent reinforcement learning (MARL) focuses on training multiple agents to work together in shared environments. While some environments allow agents to learn good strategies independently, others require a high level of coordination and planning. The Laser Learning Environment (LLE) is one such example, where agents must cooperate to overcome obstacles like laser beams, unreachable zones, and shared bottlenecks.   

Traditional MARL methods, such as value-based deep Q-networks, have achieved promising results on LLE’s simpler levels. However, they still struggle on the most difficult tasks, especially when long-term planning and unrewarded cooperation are required.

This project explores whether large language models (LLMs) can support agent coordination in LLE. Rather than learning from scratch, LLM agents rely on structured prompts, memory representations, and theory of mind (ToM) reasoning to plan and collaborate in zero-shot or few-shot settings.

The main objectives are:
- Introduce LLM-based agents in the Laser Learning Environment;  
- Enable agents to communicate and make cooperative decisions using LLM reasoning; 
- Explore how belief state prompting and ToM can support coordination; 
- Measure the impact on score, exit rate, and qualitative teamwork behaviors.


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

### 2.1.1 Reinforcement Learning Approaches for Solving Coordination in LLE

To tackle the coordination challenges in environments like the Laser Learning Environment (LLE), several reinforcement learning (RL) algorithms have been tested , especially those designed for cooperative multi-agent settings.

A common approach is to use deep Q-learning techniques, where agents learn action policies by maximizing expected rewards over time. However, when multiple agents are involved, things get more complicated. Each agent influences the environment, so what one agent learns changes the experience of the others. This problem is known as **non-stationarity**, and it makes learning stable strategies much harder.

One way to deal with this is through **Value Decomposition Networks (VDN)**: 

Value Decomposition Networks (VDN) introduces a simple but effective idea: instead of learning a single joint Q-function for the entire team, the total team value is approximated as the sum of individual agents’ Q-values.

Formally:  
    Q_total(s, a₁, ..., aₙ) ≈ Σ Qᵢ(sᵢ, aᵢ)

This decomposition allows for Centralised Training with Decntralised Execution (CTDE):
- **Centralized training**, where the full state and joint actions are used to compute gradients.
- **Decentralized execution**, where each agent selects its action based only on its own local observation.

VDN addresses the non-stationarity issue and enables scalable learning in cooperative tasks.

According to the results from the original LLE paper, VDN was the most successful among the tested baseline algorithms. While more advanced methods like QMIX ( #source) were also evaluated, VDN performed better in terms of both score and exit rate, especially on **Level 6**, which has the highest level of interdependence among all the levels.

For this reason, VDN serves as a solid baseline to see if LLM-based agents can come close to or match the kind of performance learning-based methods achieve.

--- 

### 2.2 Large Language Models for Multi-Agent Collaboration

Large Language Models, especially GPT-4, have been used recently to explored the multi-agent collaboration task. 

Unlike traditional reinforcement learning approaches, LLMs are not trained through a system of reward. Instead, they rely on [[Definitions#Zero prompting|zero-shot]] or [[Definitions#Few-shot prompting|few-shot]] prompting, basing themself only on the LLM logic and the mission context. 

Recent work done by [[ToM_for_multi-agentCollab_via_LLMs.pdf|Li et al.]] demonstrate in the collaborative learning environment, where 3 agents which communicate through GPT-4 need to defuse color-coded bombs (where a sequence order needs to be respect to defuse it) scattered in an unexplored environment - that agents display emergent cooperative behaviors. 
Despite the absence of explicit multi-agent training, LLM-based agents training exhibit: coordinated task allocation, synchronized movement and strategy negotiation and delegation. 

One key limitation of LLMs is the lack of persistent memory and internal state tracking. To address this, [[ToM_for_multi-agentCollab_via_LLMs.pdf|Li et al.]] introduce **belief state prompting**, in which each agent is given a text-based summary of what it has observed and what it believes about the environment and teammates. This technique enables the model to perform **Theory of Mind (ToM)** reasoning.

The use of belief states allows agents to: 
- Maintain reliable knowledge about the situation
- Reason about both **first-order beliefs** (what others know) and **second-order beliefs** (what others think you know)

Implementing this belief states helps agents to collaborate in better ways. For example **first order belief** lets an agent reason: *Agent B doestn't know the laser is blocked, I should tell them*, while **second order belief** allows thoughts like: *Agent A knows that I know about the gem, so  they won't go for it*. 

In the bomb defusal task, LLM-based agents equipped with belief states consistently achieve **perfect or near-perfect scores**, completing all three bomb phases with high success rates.

Some vulnerabilities may be encountered such as proposing invalid actions or the agents having 
hallucinations.

#TODO Explain what is Theory of Mind ? 
#TODO  Find other kind of example where they use LLMs to make 2 agents cooperate? (Related work)

--- 

# 3. Proposed Approach

#### 3.2 Using LLM in the LLE 

##### 3.2.1 Exploring multi-agent collaboration only with LLM

As shown in the paper _Theory of Mind for Multi-Agent Collaboration via Large Language Models_, when using LLMs in multi-agent environments, the models are not trained through a reward-based system. Instead, they rely on **zero-shot** or **few-shot prompting**. 

This would be one of the approaches explored in this project to implements LLMs in the Laser Learning Environment. In contrast to methods used like VDN, this method  bypass training entirely. 
Agents will operate as LLM-driven entities capable of reasoning, planning, and communicating based on structured textual prompts. 

To implement this approach within LLE:
-   Agents will take turns to interact with the environmentand when communicating with each other and taking the actions

- For prompting framework, each agent will have their dedicated LLM session where 
	- Intial prompt: A zero-shot prompt will be provided containing 
		- The agent identity and role
		- The game description and rules
		- Initial observation 
		- Belief state format
	- Step-by-step prompting (each round), fter the initial setup, **at each round**, the agent receives:
		- An update of its current observation  
		- Its updated belief state, which summarizes what the agent has previously seen or inferred
		- A record of the last round’s communication
		- A request to generate an action and a message 

The hypothesis is that, by using structured communication and reasoning (rather than reinforcement signals), LLM agents may be able to exhibit **emergent collaborative behavior**.

###### Types of observations:

Another interesting aspect to explore is the type of observation each agent receives.

- In the **centralized view** case, each agent has access to the full map from the beginning — they know where all the elements (lasers, gems, walls, exits, etc.) are located. The challenge here lies mainly in **planning and coordination**, as no communication is needed to discover the environment.

- In the **decentralized view** case, each agent starts with only a **limited local observation**, for example seeing only the tiles within a 2-square radius. In this setting, agents must not only coordinate but also **communicate effectively** to share what they see, what they need, and what others may be missing.

In the centralized setting, the main focus is on sequencing and cooperation.

In the decentralized setting, **information sharing becomes critical**, as agents need to build a shared understanding of the environment before they can even begin to plan joint actions.

###### Belief states to allow Theory of Mind reasoning:

One of the key components that enables LLM agents to go beyond simple rule-following is the use of **belief states**. These are structured textual summaries that represent what an agent knows — not just about its own observations, but also what it believes about the environment and its teammates.

Inspired by the prompting technique used in the paper _Theory of Mind for Multi-Agent Collaboration via Large Language Models_, each agent will maintain and update a belief state at every step. This belief state is explicitly included in the prompt and acts as a form of memory. It allows the agent to track:

- What it has observed directly in the environment
- What it infers based on communication from others
- What others likely know or do not know

By incorporating this belief tracking, agents can begin to perform **Theory of Mind (ToM)** reasoning — inferring not only the state of the world, but also the mental state of other agents. This includes:

- **First-order beliefs**: “Agent B doesn’t know the yellow laser is blocked”
- **Second-order beliefs**: “Agent C thinks that I don’t know the gem is behind the wall”

These capabilities are especially important in the **decentralized view**, where agents do not see the full environment and must rely on reasoning about what others perceive and communicate.

In this setup, belief states will evolve dynamically: after each round, the agent updates its belief based on new observations and messages. This updated belief is then passed as part of the next prompt, supporting continuity in reasoning across steps.

The expectation is that belief-aware agents will show more coordinated and adaptive behaviors, even without being explicitly trained — especially in tasks that involve helping others, waiting, or anticipating actions based on partial information.

#### 3.4 Technical aspect of the implementation 

##### 3.4.1 Which LLM use (which one would be the better fit)

###### Using GPT-4 API model 
This approach has the advantage that it has demonstrated  a powerful, state-of-the-art model that has already shown promising results in multi-agent collaboration tasks (see [[ToM_for_multi-agentCollab_via_LLMs.pdf| Li et al.]]). 

It has been prove that it supports zero-shot and few-shot reasoning, has strong language understanding, and has already been tested in belief-state and Theory of Mind (ToM) scenarios.

The main limitation of this option is cost. Every prompt sent to the model (for each agent, at each round) consumes tokens and could lead to significant API usage fees. This could become a constraint, especially when running many trials, or testing with long interactionu histories.

However, given the nature of this project, which relies on **zero-shot** or **few-shot prompting**, and the fact that it does not require shaped rewards or long training phases to discover collaborative behaviors, the overall cost is likely to remain lower than traditional AI training approaches. Unlike reinforcement learning, which often large number of interaction steps and extensive compute resources,this method builds on pre-trained knowledge, making it a more lightweight and scalable option. 

###### Using an open-source LLM locally

Another approach would be to use an open-source LLM, such as LLamA, DeepSeek or Mistral, and run it locally. This would remove the cost constraint and provide more flexibility in experimentation, especially when designing custom memory components or modifying the way prompts are handled.

On the other hand, most open-source models are less capable than GPT-4 when it comes to complex multi-step reasoning and ToM-like inference. Some models may also have limited context windows, which is a critical factor when agents need to process history or belief states.

Additional setup time is also required to host the model efficiently (possibly with quantization or GPU optimization).

Beyond the technical trade-offs, it could also be interesting to compare how different types of LLMs perform on this kind of task. Testing a variety of models may reveal differences in how they reason, coordinate, or handle uncertainty — even under the same prompting structure. This could lead to insights on what capabilities matter most for multi-agent collaboration and where current models fall short.
In addition, Comparing them to GPT-4 could help identify which reasoning abilities are essential for success in this kind of environment.


*Which LLM to use among all the open source LLM that exist:*

When checking the existing **LLM leaderboards** where we get public rankings, such as the LLM arena ( #source :  https://lmarena.ai/leaderboard/text) which is  a crowdsourced battle platform or llm-stat ( #source :https://llm-stats.com/  ) which based its leaderboard on standarized benchmarks. 

Among the **open-source** models, **four stand out consistently** for their high performance, accessibility, and reasoning ability:

- DeepSeek R1 
- Mistral 
- LLaMA 4
- Qwen 3

In our case, **DeepSeek emerges as the most suitable choice**, as it consistently outperforms the others across multiple evaluation platforms, making it the strongest candidate for our needs in multi-agent collaboration.

###### Selected Implementation Strategy

For the purposes of this project, the selected approach is to go whith an open-source language model and run the model locally. Since the number of interactions or episodes needed to evaluate and compare strategies is still unknown, this approach avoids API cost limitations and gives more freedom during experimentation. It also makes it easier to scale up if needed.

Another reason is that it would be interesting to test with a different LLM than the one used in the paper by Li et al. Using another model allows us to see whether the same prompting framework and belief-state setup can work beyond GPT-4. This could help assess how transferable and general the method is.

Running locally also gives us more control and flexibility. This makes it easier to adapt the setup to the needs of the task, and to explore variations without being limited by a fixed API.

In terms of model choice, we will begin with DeepSeek, as it consistently ranks among the top open-source models on several public benchmarks. Its strong reasoning performance makes it a good candidate for handling multi-agent communication and coordination tasks.

If time allows, it could also be interesting to test how different **model sizes or architectures** affect collaboration quality, for example, whether smaller LLMs can still perform well  with the right belief state prompts. It could also be interesting to compare other open-source models like Mistral, Qwen, or LLaMA under the same setup.
##### 3.4.1 What kind of results will be evaluated

To evaluate the performance of the LLM-based agents in the Laser Laser Environment several metrics will be used.  Among them, we will use the same metrics proposed in the orignal  LLE paper ( #source): 

- **Score** refers to the total number of points collected during an episode, without applying any discount.  The maximum possible score in LLE depends on the map: if there are _n_ agents and _g_ gems, the best possible score is **n + g + 1** (with the extra +1 coming from the team bonus when all agents reach the exit).
- **Exit rate** measures how many agents make it to the exit by the end of the episode. It gives a good idea of how close the team gets to completing the task. An exit rate of **1** means that all agents successfully reached the goal.

These results will then be compared to the baseline performance of VDN on Level 6 of LLE ( #source), as described in Molinghen et al. (2024). Since VDN is considered the best-performing MARL baseline in that paper, it gives us a good reference to see if LLM-based agents can reach similar or better results.

In addition, we'll add a new metric that we'll want to evaluated: 

- **Belief state reasoning**: whether agents show signs of Theory of Mind (e.g., adapting their behavior based on what others know or don’t know).

To evaluate this metric, we will rely on **manual analysis** of selected episodes, focusing on situations where agents are expected to reason about the mental states of others. This includes identifying moments where an agent acts (or chooses not to act) based on what it believes another agent knows, has seen, or has been told.

The evaluation will follow a few simple criteria inspired by the setup in the ToM paper ( #source ):

1. Did the agent demonstrate awareness of what another agent has or has not observed (e.g., based on location or visibility)?
2. Did the agent respond appropriately to information received through communication?
3. Did the agent act in a way that suggests second-order reasoning (e.g., “they don’t know that I know X”)?

By reviewing the full interaction history — including the belief states and messages exchanged — we will be able to assess whether agents are applying some form of **Theory of Mind** reasoning in practice.

