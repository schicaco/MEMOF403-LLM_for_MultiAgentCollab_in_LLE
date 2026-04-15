 
-  Link papers used to get to results (an anchor for the jury)
- Shapey value ( optimize prompts) library : SHAP 
- Is CoT really pertinent, is it really reasoning 
- Have insgihts about the research 
- Do comparison with rl approach (what happens if I change that or this? ) How is it different from a tradi RL? 
- How much the prompt should be specific 
- Synchro: test both (we can explore)
- For thesis : goal give some questions that i want to answer 
- BE an expert about the subjec 

---

Notes yannick 

- More or less 45 pages long thesis (without references, foreword, etc). At least 20 pages must be your contributions
	- Methodology
	- Results
	- This defines your research questions and the answers that you provide

- You should really "compare" your approach with what exists in the rest of the scientific community: you have designed a prompt, but how does it compare to the SOTA?
- For every single experiment + result that you provide, you have to explain your methodology (justified according to the SOTA).
- Look for newer papers than the one of 2023 that Tom send you
- (Tom:) investigate the robustness of the agents by moving the start positions, the exit positions, etc.
- You have to show what the differences are between your approach and the "standard" RL approach (use reward signal, etc.). This has to be extremely clear in your problem statement. (Yannick:) The agents have two biases:
	- the prompt that you give the the agents where you explain the rules of the game
	- the pre-trained model has been trained on text where it has extracted information.
- In your experiments, are you only using text or are you using a multi-modal LLM and provide images as input ?
- (Tom:) investigate what are the pieces of text in the prompt that give some information with Shapley values:
	- If I remove this sentence, how do the agents perform ?
	- Beware that you have to repeat the experiment multiple times to make conclusions about this.
	- Check the "SHAP" library for that [https://shap.readthedocs.io/en/latest/](https://eur01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fshap.readthedocs.io%2Fen%2Flatest%2F&data=05%7C02%7CSofia.Chica.Cobo%40ulb.be%7Cc2677b1967e343877df808de9acdc8b5%7C30a5145e75bd4212bb028ff9c0ea4ae9%7C0%7C0%7C639118405778430205%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C0%7C%7C%7C&sdata=s%2BXLhDZuF%2FDewPZK91OXFn0VxIDLlGNw1QT13lQvNRY%3D&reserved=0 "URL d'origine: https://shap.readthedocs.io/en/latest/. Cliquez ou appuyez si vous faites confiance à ce lien.")
- What about chain of thought model ?
	- Assess whether reasoning provides any improvement in comparison to "non-reasoning" ones. Make a critical assessment.
- (Derar:)
	- Be extremely careful with what you put in the prompt.
	- Are you taking actions simultaneously or not