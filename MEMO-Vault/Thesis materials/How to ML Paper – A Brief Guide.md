_Feel free to comment / share and happy paper writing! Also, please see caveats below._  
If you like this, why not follow **How to ML** on Twitter and share the advice/love?

---

## Canonical ML Paper Structure

### Abstract (TL;DR of paper):

- **X**: What are we trying to do and why is it relevant?
- **Y**: Why is this hard?
- **Z**: How do we solve it (i.e. our contribution!)
- **1**: How do we verify that we solved it:
    - **1a)** Experiments and results
    - **1b)** Theory

---

### Introduction (Longer version of the Abstract, i.e. of the entire paper):

- **X**: What are we trying to do and why is it relevant?
- **Y**: Why is this hard?
- **Z**: How do we solve it (i.e. our contribution!)
- **1**: How do we verify that we solved it:
    - **1a)** Experiments and results, including comparison to prior SOTA if applicable
    - **1b)** Theory

**New trend**: specifically list your contributions as bullet points (credits to Brendan)  
Extra space? Add **Future work**!  
Extra points for having **Figure 1 on the first page**

---

### Related Work

**Academic siblings** of our work — alternative attempts in literature at trying to solve the same problem.  
Goal is to **compare and contrast** — how does their approach differ in either assumptions or method?  
If their method is applicable to our **Problem Setting**, include it in experiments. If not, **explain why**.

> **Note**: Just describing what another paper is doing is not enough. We need to compare and contrast.

---

### Background

**Academic ancestors** of our work — prior concepts and work needed to understand our method.  
Usually includes a **Problem Setting** subsection with formalism, assumptions, and notation.

> **Note**: If our paper introduces a novel problem setting as part of its contributions, make a **separate section**.

---

### Problem Setting (optional)

Use this **only if** the problem setting is **novel** and part of the contribution.

---

### Method

What we do. Why we do it.  
All described using the general formalism and building on the concepts from **Background**.

---

### Experimental Setup

How do we test our stuff?  
Details about the problem instance and implementation for this experiment.

---

### Results and Discussion

- Results from running our method
- Compare to baselines
- Include confidence intervals, hyperparameters
- **Ablation studies** to show each part of method matters
- Discuss limitations

---

### Conclusion

We did it. This paper rocks.  
Brief recap of the paper + what we want to explore next.  
Future work = **academic offspring** (credits to James).

---

## Other Advice

- Start with an **outline** (each line = 1 paragraph later). Much easier to revise and get feedback.
- Then expand the outline, but **keep the TL;DR as comments** (e.g., in LaTeX) at the start of each paragraph
- This will:
    - a) keep you focused
    - b) help others give feedback quickly on structure
- Write the **abstract early**. It helps sharpen your focus and reveal gaps. You can always update it later.

---

## Author Ordering & Inclusion

- **Who is an author?** Anyone who contributed significantly (time or ideas).
- **Err on the side of generosity.**
- **Discuss expectations early!**
### Author order:

- **First author**: main contributor
- **Second author**: significant contributions (may be co-* with *)
- **Middle authors**: range from minor results to valuable feedback
- **Second senior**: day-to-day supervisor
- **Senior author**: PI/professor (whose name is “on the line” 😅)

---

## ✅ Extremely Common Writing Pitfalls and Other Advice (Print this out and tick off!)

- [ ] Avoid passive voice unless truly justified  
- [ ] Be clear on your contributions vs prior work  
- [ ] Use consistent tense (avoid switching and future tense if possible)  
- [ ] Avoid filler words (“can”, “in order to”, “shall”, etc.)  
- [ ] After writing, try to cut 1/3 of the words  
- [ ] Guide the reader – always show why something is relevant  
- [ ] Use correct quotation marks: ``like this’’  
- [ ] Punctuate equations correctly (✔ `A = r^2 \pi.` ❌ `A = r^2 \pi:`)  
- [ ] Use `\citet` and `\citep` properly in LaTeX  
- [ ] Use `\usepackage[backref=page]{hyperref}` to make refs clickable  
- [ ] Acronym + citation: `proximal policy optimisation \citep[PPO]{schulman2017ppo}`  
- [ ] Cite any unsupported claim  
- [ ] Use correct citation versions (not just arXiv)  
- [ ] Check for broken refs (`??`) in the final PDF  
- [ ] Don’t leave writing to the last minute – aim for a full draft 1 week before deadline  
- [ ] Enable track changes in Overleaf and invite co-authors directly  
- [ ] Introduce specific terms clearly and contrast if confusing  
- [ ] Never synonymize technical terms  
- [ ] Define acronyms before use (`\usepackage[acronym]{glossaries}` helps)  
- [ ] No Random Capitalisation (RC) except for proper nouns  
- [ ] Only introduce symbols and acronyms you actually use  
- [ ] Be consistent with bold/italics (e.g. bold = main idea, italics = key term)  
- [ ] Avoid anthropomorphizing AI (no “the model understands…”)  
- [ ] Watch out for subjective adjectives and broad claims  
- [ ] Don’t use “on the other hand” without a “one the one hand”  
- [ ] Avoid word repetition  
- [ ] Use simple language (no fancy vocabulary)  
- [ ] Footnotes come after punctuation  
- [ ] Break up overly long sentences  
- [ ] Avoid lines with only 1–2 words (formatting looks lazy)  
- [ ] Use full page limit, don’t leave whitespace  
- [ ] Stick to either British or American English, not both  
- [ ] Do not copy-paste from other papers (unless quoting)  
- [ ] Use the `cleveref` package for smart cross-references  
- [ ] Communicate daily with co-authors during last week  
- [ ] Have fun!

## Final Notes

Nothing here is mandatory, but these conventions help everyone read and write better.

Think of it as a **broad template** that improves clarity and consistency across ML papers.

---

## Caveats

There are stylistic exceptions — but **only break the rule if you can justify it clearly**.  
Example:

> “Passive voice is normally avoided because it obscures who did what.  
> But here, the object is the topic and has already been introduced — so putting it first reduces cognitive load.”