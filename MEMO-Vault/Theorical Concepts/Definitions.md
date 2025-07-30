## Zero-shot prompting 

>Refers to using a **pretrained language model** (like GPT-4) to perform a new task **without any additional training or task-specific examples**.

## Few-shot prompting

>Few-shot prompting involves giving the LLM **a few examples** of the task in the prompt—usually as text demonstrations—before asking it to act.

## Centralised Training with Decentralised Execution (CTDE)

>CTDE is a common approach used in multi-agent reinforcement learning to deal with the challenges of coordination and partial observability. The idea is simple: during training, agents can use **extra information** (like the global state or other agents’ observations), but during execution, each agent must act **independently**, based only on its own local observation.
>
  So in practice:
> -  **Centralised training** means the algorithm can access the full environment state and even other agents' actions to help learn better policies.
> - **Decentralised execution** means that once training is done, each agent has to make decisions using only what it can see on its own.
>
>This setup helps solve the problem of **non-stationarity**, where the environment changes from each agent's point of view as others are learning. It also allows agents to learn **cooperative behaviour** using shared information, while still being able to act independently at test time.
>
>CTDE is used in many MARL algorithms like **VDN**, **QMIX**, and **MAPPO**.

## Large context window
>In a large language model (LLM) refers to the maximum amount of text—measured in tokens—that the model can "see" and process at one time within a single input prompt.
