---
url: "https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback"
title: "Constitutional AI: Harmlessness from AI Feedback \\ Anthropic"
captured_on: "2026-04-21"
capture_method: "url"
---

AlignmentResearch# Constitutional AI: Harmlessness from AI Feedback

15 Dec 2022[Read Paper](https://arxiv.org/abs/2212.08073)## Abstract

As AI systems become more capable, we would like to enlist their help to supervise other AIs. We experiment with methods for training a harmless AI assistant through self\-improvement, without any human labels identifying harmful outputs. The only human oversight is provided through a list of rules or principles, and so we refer to the method as 'Constitutional AI'. The process involves both a supervised learning and a reinforcement learning phase. In the supervised phase we sample from an initial model, then generate self\-critiques and revisions, and then finetune the original model on revised responses. In the RL phase, we sample from the finetuned model, use a model to evaluate which of the two samples is better, and then train a preference model from this dataset of AI preferences. We then train with RL using the preference model as the reward signal, i.e. we use 'RL from AI Feedback' (RLAIF). As a result we are able to train a harmless but non\-evasive AI assistant that engages with harmful queries by explaining its objections to them. Both the SL and RL methods can leverage chain\-of\-thought style reasoning to improve the human\-judged performance and transparency of AI decision making. These methods make it possible to control AI behavior more precisely and with far fewer human labels.

## Policy Memo

[Constitutional AI Policy Memo](https://www-cdn.anthropic.com/7512771452629584566b6303311496c262da1006/Anthropic_ConstitutionalAI_v2.pdf)

## Related content

### Automated Alignment Researchers: Using large language models to scale scalable oversight

Can Claude develop, test, and analyze alignment ideas of its own? We ran an experiment to find out.

[Read more](/research/automated-alignment-researchers)### Trustworthy agents in practice

AI “agents” represent the latest major shift in how people and organizations are using AI. Here, we explain how they work and how we ensure they're trustworthy.

[Read more](/research/trustworthy-agents)### Emotion concepts and their function in a large language model

All modern language models sometimes act like they have emotions. What’s behind these behaviors? Our interpretability team investigates.

[Read more](/research/emotion-concepts-function)