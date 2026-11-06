#figure(
  image("images/LLE_VDN_baseline.svg", width: 40%),
  caption: [Training score and exit rate over time for IQL, VDN and QMIX on Level 6 (@fig:level-6). @Molinghen2024LLE],
) <fig:lle-vdn-baseline>

=== Using Neural Networks

To address cooperative multi-agent environment challenges like the Laser Learning Environment (LLE), researchers have explored various reinforcement learning (RL) algorithms. Similar cooperative problems have been studied in environments such as Hanabi @bard2019Hanabi and Overcooked @sarah2020Overcook.

In these contexts, Q-learning-based methods have been used extensively to train agents. In this setup, agents learn action policies by maximizing expected rewards over time.

However, when multiple agents are involved, things get more complicated. Each agent influences the environment, so what one agent learns changes the experience of the others. This problem is known as *non-stationarity*, and it makes learning stable strategies much harder.

==== Value Decomposition Networks (VDN)

One way to deal with the non-stationarity problem in cooperative multi-agent environments is the Value Decomposition Network (VDN) @sunehag2017VDN. VDN introduces a simple yet effective idea: rather than learning a single joint Q-function for the entire team, the total team value is approximated as the sum of the individual Q-values of each agent.

Formally:

$
Q_"total"(s, a_1, dots, a_n) approx sum_(i=1)^n Q_i(s_i, a_i)
$


According to the results in @fig:lle-vdn-baseline from the original LLE paper @Molinghen2024LLE, VDN was the most successful among the tested baseline algorithms. While more advanced methods like QMIX @rashid2020QMIX were also evaluated, VDN performed better in terms of both score and exit rate, especially on Level 6, which has the highest level of interdependence among all the levels.

For this reason, VDN serves as a solid baseline to see if LLM-based agents can come close to or match the kind of performance learning-based methods achieve.


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