
# First output


## Using the ChatGPT API (e.g., GPT-4)

This approach has the advantage of leveraging a powerful, state-of-the-art model that has already shown promising results in multi-agent collaboration tasks (see Li et al.). It supports zero-shot and few-shot reasoning, has strong language understanding, and has already been tested in belief-state and Theory of Mind (ToM) scenarios.

However, the downside is the cost. Since each agent interaction requires an API call and the prompt can grow over time, this could quickly become expensive — especially when running multiple simulations for evaluation or ablation studies.

## Using an open-source LLM locally (e.g., LLaMA, Mistral, Orca, etc.)

Running the model locally would remove the cost constraint and give more flexibility over customization (e.g., modifying prompts, injecting memory, adjusting temperature).

On the other hand, most open-source models are less capable than GPT-4 when it comes to complex multi-step reasoning and ToM-like inference. Some models may also have limited context windows, which is a critical factor when agents need to process history or belief states.

Additional setup time is also required to host the model efficiently (possibly with quantization or GPU optimization).

Beyond the technical trade-offs, it could also be interesting to compare how different types of LLMs perform on this kind of task. Testing a variety of models may reveal differences in how they reason, coordinate, or handle uncertainty — even under the same prompting structure. This could lead to insights on what capabilities matter most for multi-agent collaboration and where current models fall short.

Current plan:
Start with ChatGPT or GPT-4 for proof-of-concept and initial testing, since it guarantees high-quality reasoning. If results are promising and cost becomes a constraint, consider migrating to a local open-source LLM and benchmarking performance differences.

# Second Output 

### 3.1.1 Using GPT-4 API model

As shown in the paper Theory of Mind for Multi-Agent Collaboration via Large Language Models, GPT-4 has demonstrated strong reasoning capabilities in multi-agent collaboration tasks. In particular, when combined with belief state prompting, it achieves high scores, clear communication patterns, and emergent Theory of Mind behaviors.

Using the GPT-4 API would allow the agents in LLE to benefit from a powerful model that requires no additional training. It supports zero-shot and few-shot prompting, making it directly compatible with the approach considered here.

The main limitation of this option is cost. Every prompt sent to the model (for each agent, at each round) consumes tokens and could lead to significant API usage fees. This could become a constraint, especially when running many trials, performing ablation studies, or testing with long interaction histories.

Still, GPT-4 remains a strong candidate for the initial proof of concept, as it provides robust performance and allows us to test whether structured prompting alone is enough to solve coordination challenges in LLE.

### 3.1.2 Using an open-source LLM locally

Another approach would be to use an open-source LLM, such as LLaMA, Mistral, or Orca, and run it locally. This would remove the cost constraint and provide more flexibility in experimentation — especially when designing custom memory components or modifying the way prompts are handled.

However, open-source models are generally less powerful than GPT-4 in tasks that require multi-step reasoning, long-term planning, or Theory of Mind-like inference. They often come with shorter context windows, which can limit the amount of belief state or history that can be passed to the agent at each step. Some models also produce less stable or consistent outputs, which may lead to hallucinations or coordination failures.

Still, it could be interesting to explore how different types of LLMs perform when given the same task structure. Comparing them to GPT-4 could help identify which reasoning abilities are essential for success in this kind of environment.

For now, the plan is to start with GPT-4 and, depending on the results and resource limits, explore alternatives based on open-source models later in the project.
