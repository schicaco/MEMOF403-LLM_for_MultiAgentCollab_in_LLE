
code : https://github.com/romanlee6/multi_LLM_comm


# Problem Addressed

Modern Large Language Models (LLMs) like GPT-4 show impressive reasoning and planning abilities in single-agent settings, but their capacity for _multi-agent collaboration_ remains poorly understood.

Key problem:

- Can LLM-based agents _collaborate_ effectively in dynamic, decentralized, partially observable environments?
- Can they exhibit _Theory of Mind_ (ToM): reasoning about others' beliefs, intentions, and knowledge?

The paper explores whether LLM-based agents can plan, communicate, and coordinate in a team task—comparing them to reinforcement learning (MARL) and planning-based baselines.

---

# Task and Environment Design

## Collaborative Search-and-Rescue Task

A **text-based multi-agent environment** simulating search-and-rescue teamwork:

- **Agents**: Three specialists (Alpha, Bravo, Charlie).
- **Objective**: Locate and defuse color-coded bombs with multi-phase sequences.
- **Key constraints**:
    - Partial observability: agents only see their current room.
    - Communication: only through text messages each round.
    - Coordination: agents have different colored wire cutters, must synchronize tools and movement.

**Environment structure**:

- Modeled as a graph with rooms (nodes) and hallways (edges).
- Agents act sequentially, choosing:
    - Move to adjacent room
    - Inspect bomb
    - Apply wire cutter
    - Send communication message

**Rewards**:

- 10 points per correctly defused bomb phase.
- Encourages efficiency (fewer rounds) and precise cooperation.

---

# Unique Challenges Introduced

## 1. **Partial Observability and Decentralized Information**

Each agent has a **limited view** of the environment:

- Agents can only see the **room they are in**.
- They do not initially know:
    - Where the bomb is located.
    - The layout of the rooms and their connectivity.
    - The defusal sequence.
    - The positions and tools of other agents.

**Implication:**  
Agents must build and maintain **internal belief states** based on their own observations and what others have communicated. All knowledge is either **locally perceived** or **inferred** from messages. There is no centralized controller or shared memory.

**Related MARL concept:**  
This reflects the decentralized execution setting commonly assumed in MARL, where agents must act independently based on partial local information, even if trained centrally (see CTDE in previous section).

---

## 2. **Dynamic and Evolving Belief States**

The environment is not static from the agent’s point of view. Key information becomes available gradually:

- The **defusal sequence** is only known after someone finds and inspects the bomb.
- Teammates’ **positions and plans** evolve round by round.
- The state of the bomb (e.g., which phases are already defused) changes during the game.

**Implication:**  
Agents must update their **beliefs over time**, reasoning not only about the current state of the world but also about its **evolution** based on prior knowledge and communication. This requires **temporal reasoning** and **belief revision**.

---

## 3. **Theory of Mind (ToM) Reasoning**

To collaborate efficiently, agents must reason about the **mental states of others**:

- **What do they know?** (First-order ToM)
- **What do they think I know?** (Second-order ToM)
- **What will they likely do based on that belief?**

**Examples:**

- If Alpha finds the bomb but does not communicate its location, Bravo and Charlie remain unaware.
- If Bravo sends a vague message like "I’m on my way", Alpha must infer whether Bravo:
    - Has the correct tool.
    - Knows the bomb’s location.
    - Understands the correct sequence.

**Implication:**  
Agents must **model the beliefs, goals, and intentions** of their teammates to plan effective collaborative actions. This goes beyond standard coordination in MARL and mirrors social reasoning in humans.

---

## 4. **Communication as the Only Means of Coordination**

Agents can only coordinate through **free-form textual communication**.

- There is **no direct access to global state or teammate policies**.
- Messages are broadcast once per round and must be interpreted by LLMs.
- Communication may be **ambiguous**, **incomplete**, or even **inaccurate** (due to hallucination).

**Implication:**  
Agents must decide:

- What to communicate.
- When to communicate.
- How to interpret teammates' messages, potentially in light of what they believe the sender knows or assumes.

This introduces **pragmatic reasoning** challenges, similar to those studied in computational linguistics and human-agent interaction.

**Failure modes:**

- Omission: agents forget to communicate critical information (e.g., the bomb's location).
- Misinterpretation: agents misunderstand teammate intentions.
- Hallucination: false messages lead others into incorrect beliefs or actions.

---

## 5. **Sequential and Ordered Multi-Agent Planning**

The bomb must be defused in a strict **three-phase sequence**, where each phase:
- Requires a specific **agent’s tool color**.
- Must be completed **in order**, by different agents.
- Requires all agents to **converge** at the same room at different times.

**Implication:**  
Agents must **synchronize** their plans across time and space:
- Someone needs to **discover and share** the bomb’s location and sequence.
- Each agent must **navigate the environment** to reach the bomb room at the right moment.
- Agents must **not act too early or too late**, which would break the sequence and fail the task.


This introduces **multi-step temporal dependencies** and **task interleaving**, typical of hierarchical planning.

---

## 6. **High-Stakes, Low-Feedback Coordination**

- There is **no reward shaping**: only the final defusal steps are rewarded.
- Invalid defusal attempts **fail silently** or fail the task.
- Poor communication or miscoordination leads to **wasted rounds** or **irreversible errors**.

**Implication:**  
Agents must coordinate with **limited feedback**, relying heavily on reasoning and communication. Reinforcement learning agents, in contrast, typically need shaped rewards or extensive training to discover such behaviors.

This design makes the task an excellent challenge for LLMs to demonstrate **emergent collaboration** without explicit reward engineering.

---

# Experimental Setup and Interface


![[ToM_embodied_agent.png|600]]

- Text-game interface mediates between LLM outputs and environment:
    - Translates environment observations to text.
    - Encodes LLM's text outputs as structured actions.
    - Provides error feedback for invalid moves.
- Agents alternate turns.
- Includes a **communication channel**: messages broadcast to teammates each round.

---

# Key Theoretical Concepts

## Theory of Mind (ToM)

> Ability to reason about others' hidden mental states (beliefs, intentions, knowledge).

- **Introspection**: understanding own beliefs.
- **First-order ToM**: inferring others’ beliefs.
- **Second-order ToM**: reasoning about what others believe about you.

Essential for cooperative AI to coordinate under partial observability.

---

## Belief State Representation

> Text-based prompt structure encoding an agent’s internal model of the environment.

- Maintains updated descriptions of:
    - Bomb locations and sequences
    - Room connectivity
    - Teammate locations and tools
- Inspired by Chain-of-Thought prompting.
- Explicitly included in prompts to mitigate LLM memory limits.

---

## Multi-Agent Reinforcement Learning (MARL)

> Agents learn policies in a shared environment to maximize collective reward.

- **MAPPO (Multi-Agent Proximal Policy Optimization)**
    - Actor-critic algorithm for MARL with centralized training and decentralized execution.
    - Uses shared critic for better credit assignment.
    - Reward shaping (small rewards for correct tool use) improves sample efficiency.

---

## Planning-based Baseline

> Conflict-Based Search (CBS):

- Solves multi-agent pathfinding with temporal and precedence constraints.
- Generates optimal joint plans with perfect information.
- Serves as a strong planning benchmark.

---

# Experimental Results

## Performance Comparison

- **ChatGPT**: consistently fails to complete the task (score ~43/90).
- **GPT-4**: reaches full score but less efficient (28.3 rounds).
- **GPT-4 + Belief State**:
    - Matches optimal score (90/90).
    - Improves efficiency significantly (12.3 rounds).
    - Reduces invalid actions by ~50%.
- **MAPPO**: strong MARL baseline (11 rounds on average after extensive training).
- **CBS Planner**: solves optimally in 6 rounds.

---

## Theory of Mind Evaluation

Agents answered ToM questions across three levels:

- **Introspection**: ~97% accuracy with GPT-4+Belief.
- **First-order ToM**: ~80% accuracy.
- **Second-order ToM**: ~69% accuracy.

GPT-4 consistently outperformed ChatGPT, and explicit belief states further improved ToM inference quality.

---

## Emergent Collaborative Behaviors

Qualitative analysis revealed:

- Role assignment and leadership (e.g., Alpha delegating).
- Coordinated task allocation and planning.
- Communication resembling human teamwork (instructions, status updates).

---

## Systematic Failures Observed

1. **Long-horizon context management**:
    - Agents sometimes ignored room connectivity or tool constraints far from prompt start.
2. **Hallucination**:
    - Invented bomb states or impossible moves.
    - Spread false beliefs via communication.

Explicit belief states mitigated these issues by reinforcing relevant context.

---

# Authors’ Conclusions

- LLMs can achieve _emergent collaborative behaviors_ without task-specific training.
- Explicit belief representations improve planning, communication, and Theory of Mind inferences.
- LLMs remain less efficient than optimal planners due to context length limits and hallucinations.
- Suggests LLMs have latent social reasoning skills from language training, but need structured memory and context management to scale.

---

# Suggested Future Directions

- Scaling environments with more agents, bombs, or rooms.
- Heterogeneous agent roles (including human-agent teams).
- Improving belief tracking with first- and second-order beliefs about others.
- Studying trust, transparency, and human-centered design for collaborative AI.
- Using structured memory or external knowledge graphs to mitigate hallucination.

---

# Suggested Related Research Directions

- **Curriculum Learning**:
    - Training agents with gradually harder collaboration tasks.
    - E.g., environment design frameworks to scale complexity.
- **Exploration in Sparse-Reward RL**:
    - Go-Explore strategies for discovering rare coordinated solutions.
    - Intrinsic motivation with structured belief tracking.
- **Communication in MARL**:
    - Differentiable channels (CommNet, DIAL).
    - Emergent protocols for decentralized planning.
- **Planning with LLMs**:
    - Integrating symbolic planners with LLM-generated goals.
    - Hierarchical decision-making in multi-agent systems.
- **Human-AI Collaboration**:
    - Trust calibration, explainable communication, role assignment.

---

# Takeaways for Your Thesis

- This paper is a useful example of testing _LLM-based embodied agents_ in dynamic, multi-agent teamwork tasks.
    
- Demonstrates the importance of **belief modeling** for coordination under partial observability.
    
- Shows that Theory of Mind can be probed and enhanced in LLMs via structured prompts.
    
- Suggests that even large pre-trained models benefit from explicit representations and communication frameworks when deployed in multi-agent settings.
    

---