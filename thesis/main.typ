#set document(title: "Using LLMs for Multi-Agent Collaboration in the Laser Learning Environment")
#set page(paper: "a4", margin: (top: 25mm, bottom: 25mm, left: 32mm, right: 25mm))
// #set text(font: "Times New Roman", size: 11pt)
#set par(justify: true, leading: 0.65em)
#set heading(numbering: "1.1")
#let todo(body) = text(fill: rgb("#6666FF"), weight: "bold")[TODO: #body]


#align(center)[
  #v(10mm)
  #text(size: 16pt)[Faculty of Sciences]
  #h(1fr)
  #text(size: 16pt)[Department of Computer Science]

  #v(10mm)
  #image("images/sceau-ulb.jpg", width: 25%)

  #v(10mm)
  #text(size: 16pt, weight: "regular")[Master thesis]

  #v(10mm)
  #line(length: 100%, stroke: 1mm)
  #v(3mm)
  #text(size: 22pt, weight: "bold")[
    Using LLMs for Multi-Agent Collaboration in the Laser Learning Environment
  ]
  #v(3mm)
  #line(length: 100%, stroke: 1mm)

  #v(10mm)
  #text(size: 18pt)[
    *Author:* Sofia Chica Cobo \
    *Supervisor:* Derar Alnakeb \
    *Director:* Tom Lenaerts
  ]

  #v(1fr)
  #text(size: 16pt)[Academic year 2026–2027]
]

#pagebreak()

#outline(title: "Contents", depth: 3)

#pagebreak()
#set page(numbering: "1")
#counter(page).update(1)

= Introduction


This thesis investigates whether independently LLM-controlled agents can coordinate in the Laser Learning Environment (LLE), and how well they perform on the environment’s coordination-critical tasks. In particular, it examines whether the agents can reach the exit and collect all available gems, thereby achieving the maximum map score n+g+1 , where n  is the number of agents and g  is the number of gems. The study analyzes not only task completion and score, but also the agents’ coordination behavior and the conditions under which they succeed or fail.

#todo[it's to give an idea]


//======================================================================================================

#pagebreak()
= Background & related work

== Laser Learning Problem

The Laser Learning Environment is a multi-agent grid world populated by agents of different colours. It includes various types of elements: floor, wall, laser, laser source, gems, start and exit tiles. The main objective in this environment is for all agents to reach the exit tile.

However, to do so, the agents must overcome several constraints. Since laser beams are deadly to agents of a different colour, an agent cannot cross a laser unless it matches their colour. To get around this, agents must cooperate: one can block a laser beam, allowing another to pass safely. This makes the game fully cooperative, as success depends on helping teammates advance through the level.

The points distribution is as follows:

- +1 point per agent that reaches the exit tile;
- +1 point if all agents reach the exit tile;
- -1 point per agent death 
- 0 points for intermediate cooperative actions;
- Negative outcome: agent death.

Additionally, hidden gems scattered throughout the map provide bonus points when collected by agents.

This environment is particularly relevant because it introduces key coordination challenges:

- *Perfect coordination.* Agents must follow a precise sequence of actions. A single mistake, like moving too early or too late, can lead to failure. For example, if an agent does not block a laser at the right moment, a teammate may be eliminated.
- *Interdependence.* Agents depend on one another to complete the task. Some areas are inaccessible to a single agent acting alone. Only by helping each other can they progress.
- *Zero-incentive dynamics.* Essential cooperative actions, like blocking a laser for another agent, provide no direct reward. This forces agents to learn helpful behaviours even in the absence of positive reward.

The most interesting level in LLE is Level 6, shown in @fig:level-6, which has the highest level of interdependence. It features 4 agents, 3 lasers, and 4 hidden gems.

#figure(
  image("images/LLE.png", width: 50%),
  caption: [Level 6 of the Laser Learning Environment.],
) <fig:level-6>

== LLM-based agents 

A LLM-based agent is an agent whose decisions are made by a Large Language Model. At each step, the agent receives a description of what it observes in the environment (in our case, the LLE) in the form of a text prompt. The LLM then reasons over this information and returns an answer that is converted into an action the agent performs in the environment. Unlike RL agents, which learn a policy through training, an LLM-based agent relies on the knowledge already contained in the model and on the instructions given in its prompt.

== Cooperative MARL

This section introduces the formal framework and the learning methods used as references in related work of LLE.

=== Multi-agent Markov Decision Process 

In an MMDP @boutilier1996, a team of $n$ agents acts in a shared environment, and every agent sees the full state. It is a tuple $ (n, S, A, T, R, s_0, s_f, gamma) $. Here, $S$ is the set of states and $A = A_1 times dots.c times A_n$ is the set of joint actions, where $A_i$ is the set of actions available to agent $i$. The transition function $T(s, a)$ gives the probability distribution over next states $s'$ when the team plays joint action $a$ in state $s$. The reward
function $R(s, a, s')$ gives the team reward for that transition. The episode starts in $s_0$ and ends in $s_f$, and $gamma in [0, 1)$ discounts future rewards.

Each agent $i$ follows a policy $pi_i: S -> Delta(A_i)$. Together, they form the joint policy $pi = (pi_1, dots.c, pi_n)$, and the team seeks the policy that maximises

$ E[ sum_(t=0)^infinity gamma^t R_t | s = s_0, pi ]. $

The joint action-value function $Q^pi(s, a)$ is the expected return when the team plays $a$ in state $s$ and then follows $pi$.

#todo[to be checked]

=== Independent Q-Learning


The simplest approach is independent Q-learning (IQL): each agent learns its own Q-function and treats the others as part of the environment.

When multiple agents collaborate, we face the problem of non-stationarity. As the other agents also learn and change the environment, they must not only learn from their own strategies but also adapt to those of the other agents, which makes learning more challenging. 


=== QMIX

QMIX @rashid2020QMIX is a value-based method for cooperative multi-agent reinforcement learning. Each agent learns an action-value function, $Q_i$​ , from its local observation and action history. A mixing network combines these individual values into a joint value, $Q_"tot"$​ , conditioned on the global state available during training.

The key constraint is monotonicity: increasing any agent’s $Q_i$​  cannot decrease $Q_"tot"$​ . This allows each agent to choose its locally highest-valued action independently at execution time, while those choices also maximize the joint value.

Its limitation is that the monotonic constraint cannot represent every possible interaction among agents’ actions.

More formally QMIX combines each agent’s action-value function into a team value:

$ Q_"tot" = f_"mix"(Q_1, Q_2, dots, Q_n | s) $

The mixing function is constrained to be monotonic:

$ (partial Q_"tot") / (partial Q_i) >= 0 quad "for every agent" i. $

Here, $Q_i$ is agent $i$'s action-value, and $s$ is the global state used during training. This constraint lets each agent choose its locally best action, $arg max_(a_i) Q_i$, while ensuring those choices maximize the joint value $Q_"tot"$.


#todo[To be checked]

=== Value Decomposition Networks (VDN)

The Value Decomposition Network (VDN) @sunehag2017VDN introduces a simple yet effective idea: rather than learning a single joint Q-function for the entire team, the total team value is approximated as the sum of the individual Q-values of each agent.

Formally:

$
Q_"total"(s, a_1, dots, a_n) approx sum_(i=1)^n Q_i(s_i, a_i)
$

This is one way to deal with the non-stationarity problem in cooperative multi-agent environments

=== Centralised Training with Decentralised Execution (CTDE)

CTDE @oliehoek_concise_2016 is a common approach used in multi-agent reinforcement learning to deal with the challenges of coordination and partial observability. The idea is simple: during training, agents can use *extra information* (like the global state or other agents’ observations), but during execution, each agent must act *independently*, based only on its own local observation.

So in practice:
- *Centralised training* means the algorithm can access the full environment state and even other agents' actions to help learn better policies.
- *Decentralised execution* means that once training is done, each agent has to make decisions using only what it can see on its own.

This setup helps solve the problem of *non-stationarity*, where the environment changes from each agent's point of view as others are learning. It also allows agents to learn *cooperative behaviour* using shared information, while still being able to act independently at test time.

CTDE is used in many MARL algorithms like *VDN* and *QMIX*.


== Last collaboration over the LLE problem

#figure(
  image("images/LLE_VDN_baseline.svg", width: 40%),
  caption: [Training score and exit rate over time for IQL, VDN and QMIX on Level 6 (@fig:level-6). @Molinghen2024LLE],
) <fig:lle-vdn-baseline>


To address cooperative multi-agent environment challenges like the Laser Learning Environment (LLE), researchers have explored various reinforcement learning (RL) algorithms. Similar cooperative problems have been studied in environments such as Hanabi @bard2019Hanabi and Overcooked @sarah2020Overcook.

In these contexts, Q-learning-based methods have been used extensively to train agents. In this setup, agents learn action policies by maximizing expected rewards over time.

However, when multiple agents are involved, things get more complicated. Each agent influences the environment, so what one agent learns changes the experience of the others. This problem is known as *non-stationarity*, and it makes learning stable strategies much harder.


According to the results in @fig:lle-vdn-baseline from the original LLE paper @Molinghen2024LLE, VDN was the most successful among the tested baseline algorithms. While more advanced methods like QMIX @rashid2020QMIX were also evaluated, VDN performed better in terms of both score and exit rate, especially on Level 6, which has the highest level of interdependence among all the levels.

=== Challenges 

- There's is a combination of *perfect coordination, interdependence, and zero-incentive dynamics*. Indeed, an agent’s unilateral mistake can cause a penalty or end the episode; agents sometimes need one another to progress; and some necessary cooperative actions receive no immediate reward, this creates *state-space bottlenecks* that are difficult for learning agents to discover and pass through. 

- In their *Level 6 experiments* with IQL, VDN, and QMIX, the agents learned some local coordination—for example, blocking lasers for teammates—but did not learn to reliably complete the overall task. None reached the maximum score, and at most half the agents reached the exits, the policies did not wait for all agents to finish. 

#todo[to be checked]


=== Experimental setup

- *Observation:* The experimental setup is fully observable. All agents have a knowledge knowledge of the map' state.  
- *Maps: * Six standard maps increase in coordination difficulty; Level 6 is the main experiment map and has four agents and three lasers
- *Episode Limit:* $"width" times frac("height", 2)$ (ex. Level 6 is $12 × 13$ and which gives its limit as 12 × 13 / 2 = 78 steps.)
- *Metrics used: * the score and exit rate. The maximum score is $n + g + 1$, where $n$ is the number of agents and $g$ is the number of gems.
- *Repeated runs: * The paper’s main training plots average 20 seeds and show 95% confidence intervals 
- *Agents actions:* simultanuous each round 


//=====================================================================================================

#pagebreak()
= Problem formulation 

// objectives 

The Laser Learning Environment (LLE) is a cooperative multi-agent task in which agents must coordinate their actions to collect gems and reach exit tiles while avoiding lethal hazards. The LLE paper characterizes the task as requiring perfect coordination and interdependence, and discusses zero-incentive dynamics. For a map with n agents and g  gems, the maximum score is n+g+1 : one point for each collected gem, one for each agent reaching an exit, and one additional point for completing the task 

This thesis investigates how LLM-based agents perform in selected LLE settings, focusing on their ability to coordinate, collect gems, and complete the task. Rather than assuming that LLM agents outperform reinforcement-learning methods or solve every map, the study examines their performance and the coordination difficulties observed under the chosen agent, information, and communication settings. The work also considers how results vary across the selected maps and experimental conditions.

#todo[rephrase]

== Settings 

=== Maps 

=== LLM-based agents 

- Full observability 
- Actions each round : 
  - Synchronous
  - Asynchronous 
- Get same system prompt 
- Different prompt to specify who they are and what they can do 
- Information given : 
  - The fact that we tell them that they can communicate between each other is variable 
  - The fact that they can communicate between each other is variable 
  - ... 

#todo[scratch]

=== Models used 


== Evaluations

- The score 
- Their comportment given different situation, different models 


== LLM-based agents

// ==========================================================================================

#pagebreak()
= Method

== Architecture: agent loop, belief state, message passing

== Prompt design and its iteration 

== Action parsing, failure handling

#todo[ Do we add a section "Observation regimes (full vs. partial)"]? 

= Experimental setup 

== The maps

=== The LLM models

== Prompt techniques


= Results


= Discussion
#todo[ex: why LLMs succeed or fail, failure taxonomy]

= Limitations

= Conclusion


#pagebreak()
#bibliography("bibtex.bib", style: "ieee")



#pagebreak()
= Annexes 




// =====================================================================================================================


// === Multi-agent Markov Decision Process 

// A Multi-agent Markov Decision Process (MMDP) [Boutilier, 1996] is described as a tuple
// $⟨n, S, A, T, R, s_0, s_f, gamma⟩$, where $n$ is the number of agents, $S$ is the set of states, and $A = A_1 times dots times A_n$ is the set of joint actions, with $A_i$ the set of actions available to agent $i$. The transition function $T: S times A arrow.r Delta(S)$ gives the probability of transitioning from state $s$ to state $s'$ by taking action $a$. The reward function $R: S times A times S arrow.r RR$ gives the reward obtained by transitioning from $s$ to $s'$ after performing joint action $a$. The initial state is $s_0 in S$, $s_f$ is the final state, and $gamma in [0, 1)$ is a discount factor.

// A transition is defined as $tau = ⟨s, a, r, s'⟩$, where $s, s' in S$, $a in A$, and $r in RR$. An episode of length $l$ is a sequence of transitions $tau_1, dots, tau_l$ such that $tau_1 = ⟨s_0, a, r, s'⟩$ and $tau_l = ⟨s_(l - 1), a, r, s_f⟩$.

// Each agent $i$ acts according to a policy $pi_i: S arrow.r Delta(A_i)$. Their objective is to find the joint policy $pi = ⟨pi_1, dots, pi_n⟩$ that maximises their expected discounted reward:
// $ E[sum_(t = 0)^infinity gamma^t R_t | s = s_0, pi] $.

// The action-value function of a policy measures the expected return obtained by taking action $a$ in state $s$ and then following policy $pi$. In particular, we define the joint action-value function as $Q^pi: S times A arrow.r RR$. Scenarios in which agents receive individual observations of the state instead of the full state are referred to as Decentralised Partially Observable Markov Decision Processes @oliehoek_concise_2016.

// #todo[This is a copy/paste of Yannick's paper, write your own explanation]


// === Challenges
// - The authors identify a difficult combination of *perfect coordination, interdependence, and zero-incentive dynamics*. In practical terms, an agent’s unilateral mistake can cause a penalty or end the episode; agents sometimes need one another to progress; and some necessary cooperative actions receive no immediate reward. The authors argue that this creates *state-space bottlenecks* that are difficult for learning agents to discover and pass through. *(Molinghen et al., §3.1, PDF pp. 5–6; also abstract, PDF p. 1.)*

// - In their *Level 6 experiments* with IQL, VDN, and QMIX, the agents learned some local coordination—for example, blocking lasers for teammates—but did not learn to reliably complete the overall task. None reached the maximum score, and at most half the agents reached the exits. The authors note that the policies did not wait for all agents to finish. *(§4.1, Figure 3, PDF p. 9; §5.1, Figure 5 and Table 1, PDF pp. 11–12; §6, PDF p. 14.)*

// - They also tested prioritized experience replay (PER), n-step returns, and random network distillation (RND); these additions did not resolve the Level 6 difficulty in their experiments. The authors’ explanations—that PER may overemphasize penalties, and n-step returns may spread sparse penalties backward—are presented as hypotheses, not established mechanisms. *(§4.2, Figure 4, PDF pp. 10–11; §§5.2–5.3, PDF pp. 13–14.)*

// - *Scope:* These results concern the algorithms and setup tested in the paper, especially Level 6. They do not prove that RL in general cannot solve LLE, or establish failure on every level.