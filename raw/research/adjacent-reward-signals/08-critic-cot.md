---
url: "https://arxiv.org/pdf/2408.16326"
title: "Critic-CoT: Boosting the Reasoning Abilities of Large Language Model via Chain-of-Thought Critic"
captured_on: "2026-04-20"
capture_method: "pdf"
engine: "marker"
assets_dir: "./assets/critic-cot"
---

# Critic-CoT: Boosting the Reasoning Abilities of Large Language Model via Chain-of-Thought Critic

Xin Zheng 1 , 2 \* Jie Lou 3 Boxi Cao 1 , <sup>2</sup> Xueru Wen 1 , <sup>2</sup> Yuqiu Ji 3

Hongyu Lin 1 Yaojie Lu <sup>1</sup> Xianpei Han <sup>1</sup> Debing Zhang <sup>3</sup> Le Sun 1

<sup>1</sup> Chinese Information Processing Laboratory, Institute of Software,

Chinese Academy of Sciences <sup>2</sup> University of Chinese Academy of Sciences

<sup>3</sup> Xiaohongshu Inc

{zhengxin2020,boxi2020,wenxueru2022}@iscas.ac.cn

{hongyu,luyaojie,xianpei,sunle}@iscas.ac.cn

{yinyue2,dengyang}@xiaohongshu.com

### Abstract

Self-critic has become a crucial mechanism for enhancing the reasoning performance of LLMs. However, current approaches mainly involve basic prompts for intuitive instance-level feedback, which resembles System-1 processes and limits the reasoning capabilities. Moreover, there is a lack of in-depth investigations into the relationship between LLM's ability to criticize and its task-solving performance. To address these issues, we propose Critic-CoT, a novel framework that pushes LLMs toward System-2-like critic capability. Through a step-wise CoT reasoning paradigm and the automatic construction of weak-supervision data without human annotation, Critic-CoT enables LLMs to engage in slow, analytic self-critique and refinement, thereby improving their reasoning abilities. Experiments on GSM8K and MATH and out-of-domain evaluation demonstrate that our enhanced model significantly boosts tasksolving performance by filtering out invalid solutions or iterative refinement. Furthermore, we investigate the intrinsic correlation between critique and task-solving abilities within LLMs, discovering that these abilities can mutually reinforce each other rather than conflict. [1](#page-0-0)

### 1 Introduction

Enhancing the reasoning abilities of large language models is essential for creating more intelligent and reliable AI systems, which has drawn extensive attention from researchers [\(Chollet,](#page-8-0) [2019;](#page-8-0) [Bubeck](#page-8-1) [et al.](#page-8-1) , [2023](#page-8-1) ; [Morris et al.](#page-10-0) , [2024\)](#page-10-0). From a cognitive perspective, the procedure of human reasoning involves constant reflection and revision [\(Hegel](#page-9-0) [et al.](#page-9-0) , [1991](#page-9-0) ; [Kierkegaard](#page-9-1) , [1989](#page-9-1) ; [Popper](#page-10-1) , [1934\)](#page-10-1), which has inspired increasing focus on integrating self-critic mechanisms in the reasoning process of

large-scale models [\(Kim et al.](#page-9-2) , [2023](#page-9-2) ; [Shinn et al.](#page-10-2) , [2023](#page-10-2) ; [Madaan et al.](#page-10-3) , [2023\)](#page-10-3). This involves iteratively allowing the model to generate feedback on its own responses and then refining its reasoning based on the feedback. Compared with traditional critic methods that depend on feedback from external sources [\(Saunders et al.,](#page-10-4) [2022;](#page-10-4) [McAleese et al.,](#page-10-5) [2024\)](#page-10-5), self-critic relies solely on the model's internal capabilities, thus reducing the high cost of additional human annotation, and serving as a promising potential solution to scalable oversight [\(Leike](#page-9-3) [et al.](#page-9-3) , [2018](#page-9-3) ; [Burns et al.](#page-8-2) , [2023](#page-8-2) ; [Cao et al.](#page-8-3) , [2024\)](#page-8-3).

However, current studies primarily focus on utilizing LLMs' critique abilities to enhance their performance. Yet, relatively little attention has been given to the investigation and development of the critique ability itself. Firstly, existing critique methods are often overly simplistic, typically relying on a basic prompt to directly point out the error, without stepwise Chain-of-Thought examination or training procedure, which leads to relatively poor self-critic accuracy [\(Luo et al.](#page-10-6) , [2023](#page-10-6) ; [West et al.](#page-10-7) , [2024\)](#page-10-7). Specifically, proposing a valid critique is a complicated task that requires a thorough understanding of statements and precise negativity. However, current LLMs are normally not explicitly trained for critic capability. Therefore, these simple approaches usually tend to "criticize" like System-1 (fast thinking mode), which is more intuitive and likely to make mistakes, rather than more rigorous and deliberate System-2 (slow thinking mode) [\(Kahneman,](#page-9-4) [2011;](#page-9-4) [Yu et al.,](#page-11-0) [2024\)](#page-11-0), while shifting LLMs from System-1 toward System-2, which is to perform systematical analysis that fully utilizes the advantage of Chain-of-Thought reasoning, emerges as a promising approach for improving the reasoning capability [\(OpenAI](#page-10-8) , [2024\)](#page-10-8). This limitation diminishes the effectiveness of self-critic and, further, self-correct [\(Huang et al.](#page-9-5) , [2024\)](#page-9-5). Secondly, the capabilities of task-solving and self-critic are both dependent on the model's inherent knowledge,

1

<sup>\*</sup> This work was done when Xin Zheng interned at Xiaohongshu.

<span id="page-0-0"></span><sup>1</sup>Our code and data are available at [https://github.](https://github.com/AlignRM/Critic-CoT) [com/AlignRM/Critic-CoT](https://github.com/AlignRM/Critic-CoT)

<span id="page-1-0"></span>![](./assets/critic-cot/_page_1_Picture_0.jpeg)

Figure 1: Illustration of Critic-CoT: Previous instance-level critic methods attempt to identify errors directly without any prior analysis, and restart from the beginning during refinement. In contrast, our proposed Critic-CoT framework performs a step-wise examination using the Chain-of-Thought approach. When refining, rather than starting from scratch, our method makes the correction from the specific error step with the help of the corresponding critique.

while there is currently a lack of in-depth exploration regarding the correlation between these two capabilities within LLMs. In that case, it's challenging to balance the task-solving and the selfcritic capabilities of the model within the self-critic framework, which poses a significant obstacle to the subsequent development.

To this end, this paper is devoted to diving into the following critical research questions:

- How can we enhance a model's critique ability, pushing it toward System 2 reasoning?
- What is the relationship between a model's critique ability and its task-solving capability?

To answer the above questions, as shown in Figure [1,](#page-1-0) we propose Critic-CoT, a novel framework designed to enhance LLMs' reasoning abilities. Through step-wise Chain-of-Thought critique format and automated data construction through weak supervision, our method is able to strengthen System-2-like critic ability, without the intensive cost of human annotation. Specifically, during training, we let LLMs criticize and refine their solutions in a complete CoT way, and collect successful pairs that convert wrong solutions into correct ones, or affirm the validity of original right solutions. After supervised fine-tuning on the obtained step-wise critic-refine data, we enable the target LLM to analyze and criticize each step of its generated reasoning procedure, so that it can filter out wrong attempts and preserve the correct ones with greater precision. During inference, to leverage the model's abilities of CoT-critique and refinement, we employ two strategies: 1) majority vote filtering involves using the critic model to evaluate multiple

generated solutions and filter out those incorrect; and 2) iterative refinement, on the other hand, involves repeatedly critiquing and refining a solution until no further error is detected.

Through a series of experiments on the indomain dataset of GSM8K and MATH, together with out-of-domain evaluation on StrategyQA, AGIEval and HumanEval, we find that our trained critic model can fairly distinguish incorrect solutions from correct ones, and improve the reasoning accuracy via iterative refinement or critic filtering. These results demonstrate the helpfulness and effectiveness of our proposed method. Additionally, we observed that our critic model already exhibits noticeable performance improvements in task-solving, even in the absence of additional critique steps during the decoding phase. Such findings reveal that strengthening the ability to critique and refinement would not compromise the tasksolving performance, but improve it. This also suggests the presence of an intrinsic mechanism by which critique ability and task-solving capability mutually reinforce one another.

Our main contributions are as follows:

- We propose Critic-CoT, which pushes the critic paradigm of LLMs from System-1-like incentive "thinking" toward System-2-like deliberate "reasoning".
- Through experiments, we find that Critic-CoT can effectively teach the model to criticize and refine its own output step by step, thus noticeably improving the reasoning performance.
- Moreover, we find that for LLMs, the ability of critique and refinement could mutually re-

inforce, which may shed light on designing more advanced self-critic framework designs in future work.

## 2 Related Works

With the development of LLMs, self-critic has emerged as a widely-adopted mechanism for reasoning, code generation, computer control, hallucination mitigation, retrieval-augmented generation and other tasks [\(Kim et al.,](#page-9-2) [2023;](#page-9-2) [Shinn et al.,](#page-10-2) [2023;](#page-10-2) [Madaan et al.,](#page-10-3) [2023;](#page-10-3) [Ji et al.,](#page-9-6) [2023;](#page-9-6) [Asai et al.,](#page-8-4) [2024\)](#page-8-4). However, typical self-critic approaches like Reflexion [\(Shinn et al.,](#page-10-2) [2023\)](#page-10-2), only utilize the LLMs' existing critique ability without further enhancement, and require the gold environment signal to iteratively generate critiques and make refinements. As long as external feedback is not available, off-the-shelf LLMs cannot perform intrinsic self-correct effectively due to limited critique and refinement abilities [\(Huang et al.,](#page-9-5) [2024;](#page-9-5) [Luo et al.,](#page-10-6) [2023;](#page-10-6) [Zeng et al.,](#page-11-1) [2023\)](#page-11-1). Later, several works are proposed to improve self-reflection via a carefully designed prompting pipeline on frozen LLMs, and no active training process is involved [\(Zhang et al.,](#page-11-2) [2024b;](#page-11-2) [Yan et al.,](#page-11-3) [2024;](#page-11-3) [Wu et al.,](#page-11-4) [2024\)](#page-11-4). Concurrently, [Zhang et al.](#page-11-5) [\(2024a\)](#page-11-5) trained a generative reward model on the outcome level rather than the process level, and did not incorporate refinement into the schema. Therefore, given the limited critic ability of current LLMs, how to train a robust and applicable critic model, which conducts detailed Chain-of-Thougt analysis in a step-wise systematic manner, and thus shifts from System-1 reasoning toward more deliberate System-2 reasoning [\(Kah](#page-9-4)[neman,](#page-9-4) [2011\)](#page-9-4), is worth investigating.

From the perspective of recursive reward modeling [\(Leike et al.,](#page-9-3) [2018;](#page-9-3) [Saunders et al.,](#page-10-4) [2022\)](#page-10-4) and scalable oversight [\(Burns et al.,](#page-8-2) [2023\)](#page-8-2), [McAleese](#page-10-5) [et al.](#page-10-5) [\(2024\)](#page-10-5) recently trained "CriticGPT" to assist human labelers, which aims to improve the ability of human rather than the base model, i.e., improve the overall recall of error detection, rather than precision. While in this paper, we try to improve the reasoning ability of LLM without costly human annotation.

## 3 Method

Critic CoT is to equip LLMs with the ability to criticize and refine themselves step-by-step. As shown in Figure [2,](#page-3-0) it consists of two modules, including automated data construction via weak-

supervision and self-check at inference-time. The weak-supervision principles are in Section [3.1,](#page-2-0) followed by the training process in Section [3.1,](#page-2-0) and the inference strategies in [3.3.](#page-3-1)

### <span id="page-2-0"></span>3.1 Chain-of-Thought Critique

In this work, we utilize a step-wise chain-ofthought critique, which makes the critique-refine process both controllable and formalizable, thereby facilitating the collection of weak supervision data. Formally, given the question Q and the corresponding gold answer Ans, we have the n-step attempt Att = [s1, ..., sn] with predicted answer P red sampled by generator G. The corresponding critique Cri then can be represented as L = [l1, ..., ln], where the step label l<sup>i</sup> = +1 indicates that step i is predicted to be correct, and l<sup>i</sup> = −1 to be incorrect. Then the refinement Att′ = [s ′ i , ..., s′ <sup>n</sup>′] is start from the first incorrect step i with new answer P red′ . We automatically annotate the process labels as follows:

- P red ̸= Ans, −1 ∈/ L: The attempt is wrong, yet the critique did not discover any error step. Thus the critique itself is problematic, and we need to sample another critique.
- P red ̸= Ans, −1 ∈ L, P red′ ̸= Ans: The attempt is wrong, and the critique found an error, but still, the refinement is not correct. There could be two cases for this situation: (1) the refinement is unsuccessful; (2) the critique did not detect an earlier mistake. We simply sample another critique and corresponding refinement for this situation.
- P red ̸= Ans, −1 ∈ L, P red′ = Ans: Not only did the critique point out the error, but also the refinement reached the correct answer. We then believe the critique is valid, and collect the critique data instance C = (Q, Att, Cri) and the refinement data R = (Q, Att, Cri−1, Att′ ), where Cri−<sup>1</sup> is the critique of last step, since explaining why previous steps are correct may not be helpful.
- P red = Ans, −1 ∈/ L: The attempt is correct, and the critique believes it is correct. So we can collect the positive critique data instance C = (Q, Att, Cri).
- P red = Ans, −1 ∈ L: The attempt reached the correct answer, yet the critique found an

<span id="page-3-0"></span>![](./assets/critic-cot/_page_3_Figure_0.jpeg)

and Critic As Filter

Figure 2: The Process of Critic-CoT during training (a) and inference (b). For training, we collect the critic-refine data on the generator's samples via weak supervision (Section [3.1\)](#page-2-0). Through fine-tuning, we enable the target model to criticize and refine its own reasoning process. Then, during inference, we can leverage the capabilities via Iterative Refine or Critic As Filter (Section [3.3\)](#page-3-1).

error. Then, the critique could be wrong, and we need to sample another critique.

### <span id="page-3-4"></span>3.2 Auto Train: Two-Stage Training

To enable the model to acquire self-critiquing and refining capabilities, we first need to provide it with basic critiquing abilities, followed by self-critique for further enhancement. The overall training procedure is divided into two stages.

Stage 1 In the first step, we collect high-quality critique data to provide the model's basic critiquing ability. Specifically, we first sample both positive and negative solutions from a representative instruction-following model M<sup>G</sup> on the dataset D. Then, we utilize LLMs like GPT4- Turbo to serve as critic model MC. For each generated attempt Att, the critic model will retry at most k times to produce a valid critique until it reaches one of the weak supervision constraints. This will form the critic-refine dataset D<sup>1</sup> = {(Q, Att, Cri)} S {(Q, Att, Cri−1, Att′ )} for fine-tuning the initial model M<sup>0</sup> into the critic model M1. Note that in this process, we actually distill Pass1@N of the teacher model M<sup>C</sup> into Top1@N of the student model. So, the theoretical upper bound of the student model is not necessarily limited by the teacher model's performance.

Stage 2 In the second step, we leverage the model's self-critique to enhance its critiquing and refining capabilities further. Namely, we let the learned critic model M<sup>1</sup> criticize and refine its own output. We first sample M correct-answer solutions and M incorrect-answer solutions for each

question Q in the original dataset D. Then, for each attempt Att, we employ M<sup>1</sup> to repeatedly criticize and refine at most k times. If the model fails to critique even after k times, we fall back on the critique from a stronger yet frozen model M<sup>C</sup> as the final choice. Finally, we collect dataset D<sup>2</sup> = {(Q, Att, Cri)} S {(Q, Att, Cri−1, Att′ )} and use D<sup>1</sup> S D<sup>2</sup> to train the initial model M<sup>0</sup> into the final critic model M2, which is similar to [Wang et al.](#page-10-9) [\(2024\)](#page-10-9). This procedure helps the model to learn to criticize and refine its own reasoning outputs better.

## <span id="page-3-1"></span>3.3 Inference: Self-Check

<span id="page-3-2"></span>Iterative Refine One single-turn refinement, which consists of multiple steps, may still contain errors. Therefore, we could iteratively inspect the refined solution, and re-refine once the critique found a mistake, and only output the final solution if it's convincing for the critic, or if it reached the maximum retry. To avoid de-generation after too many refinements, we set the maximum refine depth d = 8, and restart from the initial solution after d unsuccessful refinement at most n = 8 times. Figure [A4](#page-20-0) presents a single successful round of critique and refinement.

<span id="page-3-3"></span>Critic As Filter Self-consistency is an effective way to reduce variance. With the ability to critique, we can filter out predict-to-be-wrong answers to further boost the performance. Specifically, for the m attempts S = {(Att, P red)}, we first let our model M check each attempt and obtain the stepwise label, which is S<sup>c</sup> = {(Att, P red, L)}.

<span id="page-4-1"></span>

| Model                                            | Sampling Method   | GSM8K      | MATH500    |
|--------------------------------------------------|-------------------|------------|------------|
| Base Model                                       |                   |            |            |
| Llama-3-70B-Instruct (Dubey et al., 2024)        | -                 | 89.6       | 50.4       |
|                                                  | Maj1@96           | 94.1       | 62.2       |
|                                                  | Maj1@512          | -          | 63.4       |
| Llama-3.1-70B-Instruct (Dubey et al., 2024)      | -                 | 94.5       | 65.7       |
| GPT4-0314 (OpenAI, 2023)                         | -                 | 92.0       | 52.6       |
| DeepSeek-V2 Chat-236B (DeepSeek-AI et al., 2024) | -                 | 92.2       | 56.3       |
| Reasoning-Enhanced Model                         |                   |            |            |
| MATH-Minos, Mistral-7B (Gao et al., 2024)        | PRM+Maj1@256      | 87.8       | 38.6       |
| InternLM-MATH-20B (Ying et al., 2024)            | PRM Best-of-100   | 89.3       | 50.0       |
| DART, Llama3-70B (Tong et al., 2024)             | -                 | 89.6       | 56.1       |
| Math-Shepherd, DeepSeek-67B (Wang et al., 2023a) | PRM+Maj1@256      | 92.5       | 48.1       |
| Ours                                             |                   |            |            |
| Critic-CoT, Llama-3-70B-Instruct                 | -                 | 91.7       | 57.6       |
|                                                  | Iterative Refine  | 93.3 ↑ 1.6 | 57.8 ↑ 0.2 |
|                                                  | Maj1@96           | 94.8       | 64.6       |
|                                                  | Critic + Maj1@96  | 95.4 ↑ 0.6 | 66.6 ↑ 2.0 |
|                                                  | Maj1@512          | -          | 65.4       |
|                                                  | Critic + Maj1@512 | -          | 68.4 ↑ 3.0 |

Table 1: Solution Accuracy of GSM8K and MATH500. Compared with the base model, iterative refinement with our trained model improves from 89.6% to 93.3%% for GSM8K and from 50.4% to 57.8% for MATH500, while the critic filter increases the accuracy to 95.4% for GSM8K and 68.4% for MATH500.

Then those which detect the error at some step are filtered out and reach S ′ <sup>c</sup> = {(Att, P red, L)|−1 ∈/ L}. Finally, we perform the majority vote to get the answer.

### 4 Experiment

We apply the Critic-CoT training process on the training dataset of GSM8K and MATH (Section [4.1\)](#page-4-0), and observe a noticeable performance improvement (Section [4.2\)](#page-5-0), and out-of-domain evaluations on AGIEval, StrategyQA, and HumanEval further exhibits the generalization of our trained critic ability (Section [4.3\)](#page-5-1) For more analysis, discussion, see Appendix [A.3](#page-13-0) and Appendix [A.4,](#page-13-1) and the prompt is presented in Appendix [A.6.](#page-17-0)

### <span id="page-4-0"></span>4.1 Setup

## 4.1.1 Model

We fine-tune the critic-refine model on Llama-3-70B-Instruct [\(Dubey et al.,](#page-9-7) [2024\)](#page-9-7), which was pre-trained on more than 15 Trillion tokens and has a context length of 8,192. For critique / refinement sampling, we use GPT4-Turbo [\(OpenAI,](#page-10-10) [2023\)](#page-10-10) of the version gpt-4-0125-preview. We use the Huggingface Transformers [\(Wolf et al.,](#page-10-13) [2020\)](#page-10-13), DeepSpeed [\(Rajbhandari et al.,](#page-10-14) [2021\)](#page-10-14) and FastChat [\(Zheng et al.,](#page-11-7) [2023\)](#page-11-7) libraries for training. We use vLLM library [\(Kwon et al.,](#page-9-9) [2023\)](#page-9-9) for model inference, adapting top-p sampling of p = 0.95, with temperature 0.7 for solution sampling, which follows [Cobbe et al.](#page-8-6) [\(2021a\)](#page-8-6), and 0.5 for critique and refinement. All inferences are zero-shot.

### 4.1.2 Dataset

Train & In-Domain Eval Separately, we train our model on the problem of GSM8K [\(Cobbe](#page-8-6) [et al.,](#page-8-6) [2021a\)](#page-8-6) and MATH [\(Hendrycks et al.,](#page-9-10) [2021\)](#page-9-10). GSM8K is a grade-school-level math word problem dataset, with 7,473 training instances and 1,319 test instances. MATH is a challenging high school math competition dataset, which consists of 7,500 training problems and 5,000 test problems. For the MATH dataset, we also follow the data split of [Lightman et al.](#page-9-11) [\(2024\)](#page-9-11), which adds 4,500 test problems into a training set and, therefore, contains 12,000 training instances and 500 representative test instances. More details are in Appendix [A.1.](#page-12-0)

Out-of-Domain Eval To further evaluate our critic model's generalization capabilities beyond math, we assess its performance on reasoning tasks using the StrategyQA, AGIEval, and HumanEval datasets, which cover different domains. StrategyQA [\(Geva et al.,](#page-9-12) [2021\)](#page-9-12) is a multi-step reasoning task constructed from Wikipedia, with binary answers indicating either true or false. AGIEval [\(Zhong et al.,](#page-11-8) [2023\)](#page-11-8) comprises standardized exam questions from various fields, including college entrance exams, law school admission tests, math competitions, and lawyer qualification tests. Given the overlap with the MATH test set, we evaluated

<span id="page-5-2"></span>

| Model                  | Acc.       |  |  |  |
|------------------------|------------|--|--|--|
| Llama-3-70B-Instruct   | 56.6       |  |  |  |
| Llama-3.1-70B-Instruct | 61.8       |  |  |  |
| DeepSeek-V2 Chat-236B  | 61.4       |  |  |  |
| GPT4o                  | 65.2       |  |  |  |
| Critic-CoT, GSM8K      | 54.7       |  |  |  |
| - Iterative Refine     | 55.6 ↑ 0.8 |  |  |  |
| - Maj1@96              | 60.7       |  |  |  |
| - Critic + Maj1@96     | 60.3 ↓ 0.4 |  |  |  |
| Critic-CoT, MATH       | 59.8       |  |  |  |
| - Iterative Refine     | 63.7 ↑ 3.9 |  |  |  |
| - Maj1@96              | 61.0       |  |  |  |
| - Critic + Maj1@96     | 61.2 ↑ 0.2 |  |  |  |
| (a) AGIEval            |            |  |  |  |
| Model                  | Acc.       |  |  |  |
| Llama-3-70B-Instruct   | 76.2       |  |  |  |
| Llama-3.1-70B-Instruct | 84.3       |  |  |  |
| DeepSeek-V2 Chat-236B  | 75.6       |  |  |  |
| GPT4-0314              | 83.6       |  |  |  |
| Critic-CoT, GSM8K      | 77.5       |  |  |  |
| - Iterative Refine     | 78.8 ↑ 1.3 |  |  |  |
| - Maj1@96              | 78.7       |  |  |  |
| - Critic + Maj1@96     | 80.5 ↑ 1.8 |  |  |  |
| Critic-CoT, MATH       | 78.0       |  |  |  |
| - Iterative Refine     | 80.1 ↑ 2.1 |  |  |  |
| - Maj1@96              | 78.3       |  |  |  |
| - Critic + Maj1@96     | 79.7 ↑ 1.4 |  |  |  |
| (b) StrategyQA         |            |  |  |  |
| Model                  | Pass@1     |  |  |  |
| Llama-3-70B-Instruct   | 76.2       |  |  |  |
| Llama-3.1-70B-Instruct | 80.5       |  |  |  |
| DeepSeek-V2 Chat-236B  | 81.1       |  |  |  |
| GPT4-0314              | 86.6       |  |  |  |
| Critic-CoT, GSM8K      | 77.4       |  |  |  |
| - Iterative Refine     | 78.1 ↑ 0.7 |  |  |  |
| Critic-CoT, MATH       | 84.1       |  |  |  |
| - Iterative Refine     | 84.8 ↑ 0.7 |  |  |  |
| (c) HumanEval          |            |  |  |  |

Table 2: Solution Accuracy of standardize exam dataset AGIEval [\(2a\)](#page-5-2), multi-hop reasoning dataset StrategyQA [\(2b\)](#page-5-2) and code generation dataset HumanEval [\(2c\)](#page-5-2). Our models generally show robust generalization.

our model using the original 7,500/5,000 split from MATH, rather than the extended 12,000/500 split. HumanEval [\(Chen et al.,](#page-8-7) [2021\)](#page-8-7) contains 164 handwritten Python program problems, which evaluate the code generation capability.

## <span id="page-5-0"></span>4.2 Critic-CoT Improves Mathematical Reasoning

The results of in-domain evaluation are shown in Table [1,](#page-4-1) which demonstrate the effectiveness of Critic-CoT in improving the model's mathematical reasoning performance. First, strengthening the ability to critique and refinement would not

compromise the task-solving performance, but improve it. After Critic-CoT training, our model's top-1 accuracy increases from 89.6% to 91.7% on GSM8K, and from 50.4% to 57.6% on MATH500. Second, the step-wise self-critique ability of the models can further enhance the reasoning performance during inference, via Iterative Refinement and Critic As Filter. With Iterative Refinement, our model achieves 93.3% accuracy on GSM8K and 57.8% on MATH500. Applying Critic As Filter, the performance improves further on the basis of majority vote. On GSM8K it rises from 94.8% with Maj1@96 to 95.4% and on MATH500 it rises from 65.4% with Maj1@512 to 68.4%. Thus, our model's accuracy surpasses strong baselines of Process Reward Model assisted model MATH-Minos, InternLM-MATH-20B, Math-Shepherd, and rejection sampling finetuning model DART. Overall, the results indicate the model's enhanced abilities to identify mistakes and recover from them, thereby boosting the reasoning performance.

## <span id="page-5-1"></span>4.3 Critic-CoT Strengthens Out-of-Domain Reasoning

The results of out-domain evaluation are shown in Table [2.](#page-5-2) In general, our model, especially trained on MATH dataset, achieves positive performance gain with Iteartive Refinement and Critic As Filter, which demonstrates the generalized critique and refinement abilities beyond the math training domains. For StrategyQA, our critic models trained on two datasets show a positive performance increase when applying iterative refine and majority vote with the critic filter. On the more challenging dataset AGIEval, the Critic-CoT model trained on MATH performs much better than the model trained on grade-school level GSM8K dataset, and shows significant improvements in iterative refinement, rising to 63.7% compared with 56.6% prior the Critic-CoT training. On the code generation task HumanEval, the majority vote method is not applicable, but we can still observe the positive improvement with iterative refinement: while the base model's pass rate is 76.2%, our model trained on GSM8K and MATH achieved 78.1% and 84.8% respectively. These results highlight the robustness of our Critic-CoT models.

## 5 Ablation Analysis

To demonstrate the effectiveness of our Critic-CoT designs, we conduct a series of manual examination

<span id="page-6-2"></span>

| Data  | Critique of   | Refinement of | Critique of            |
|-------|---------------|---------------|------------------------|
|       | Wrong Attempt | Wrong Attempt | Correct Answer Attempt |
| GSM8K | 86%           | 97%           | 100%                   |
| MATH  | 85%           | 96%           | 92%                    |

Table 3: Human Evaluation on the critique and refinement of Critic-CoT Training Data. The automatically constructed data maintain high quality, which can well support the critique training process.

<span id="page-6-3"></span>

| Model         |      | Critic |      |      | Refine    |           | Majority Vote |               |         |  |
|---------------|------|--------|------|------|-----------|-----------|---------------|---------------|---------|--|
|               | P    | R      | F1   | Acc. | Init. Acc | Ref. Acc. | Pass1@N       | Maj1@N        | +Critic |  |
| Outcome Label | 95.5 | 28.9   | 44.4 | 88.0 | 87.7      | 89.7      | 99.0          | 93.6          | 93.7    |  |
| Process Label | 67.9 | 22.8   | 34.1 | 89.5 | 88.0      | 89.2      | 99.0          | 93.0          | 93.0    |  |
| Only Refine   | 30.0 | 11.4   | 16.6 | 90.8 | 92.0      | 88.2      | 98.9          | 95.2          | 95.2    |  |
| Only Critic   | 57.1 | 31.0   | 40.2 | 91.9 | 91.2      | 91.4      | 98.9          | 94.4          | 94.5    |  |
| Stage 1       | 42.5 | 41.5   | 42.0 | 89.3 | 90.7      | 91.1      | 98.9          | 93.6          | 94.2    |  |
| Stage 2       | 50.0 | 25.0   | 33.3 | 85.5 | 90.5      | 91.3      | 99.0          | 94.4          | 94.4    |  |
| Critic-CoT    | 53.3 | 58.2   | 55.7 | 92.3 | 91.7      | 93.3      | 99.1          | 94.8          | 95.4    |  |
|               |      |        |      |      | (a) GSM8K |           |               |               |         |  |
| Model         |      | Critic |      |      | Refine    |           |               | Majority Vote |         |  |
|               | P    | R      | F1   | Acc. | Init. Acc | Ref. Acc. | Pass1@N       | Maj1@N        | +Critic |  |
| Outcome Label | 84.4 | 39.0   | 53.3 | 63.0 | 51.8      | 53.6      | 84.0          | 56.2          | 56.2    |  |
| Process Label | 80.2 | 35.9   | 49.6 | 63.8 | 50.4      | 52.6      | 78.6          | 49.4          | 50.8    |  |
| Only Refine   | 62.3 | 60.1   | 61.2 | 66.0 | 55.4      | 49.8      | 90.4          | 63.0          | 62.8    |  |
| Only Critic   | 67.9 | 75.4   | 71.5 | 71.6 | 52.8      | 55.8      | 89.0          | 60.6          | 60.6    |  |
| Stage 1       | 64.6 | 93.7   | 76.5 | 69.0 | 53.2      | 41.2      | 90.4          | 63.4          | 63.0    |  |
| Stage 2       | 79.7 | 45.8   | 58.2 | 71.8 | 57.2      | 57.4      | 90.4          | 64.6          | 65.0    |  |
| Critic-CoT    | 66.1 | 73.7   | 69.7 | 72.2 | 57.6      | 57.8      | 89.2          | 64.6          | 66.6    |  |

(b) MATH500

Table 4: Ablation Study on GSM8K and MATH500. We use the metrics from three aspects: critic, including precision, recall, f1-score and accuracy; Iterative Refine, including accuracy before and after the refinement; and Critic As Filter, including Pass1@96, Maj1@96, and Critic+Maj1@96. The ablation study demonstrates the effectiveness of our Critic-CoT design.

and ablation studies, which confirm that our training data is still in high quality (Section [5.1\)](#page-6-0), our proposed stepwise CoT critique is advantageous (Section [5.2\)](#page-6-1), the composition of training data is beneficial (Section [5.3\)](#page-7-0), and the source of improvement shall be attributed to our Critic-CoT framework rather than distillation (Section [5.4\)](#page-7-1).

## <span id="page-6-0"></span>5.1 The Quality of Constructed Data

To examine the correctness of constructed Critic-CoT training data, we perform the manual evaluation. We sample 300 entries (100 with the critique of correct answer and 100 with the critique and refinemnt of wrong answer) each from the critic-cot data on GSM8K and MATH, and conduct a manual verification to verify the accuracy of the step-wise critiques. For the critique of the correct answer attempt, it is valid if there is indeed no error in all

the intermediate steps; for the critique of the wrong attempt, it is valid if the first error step and the reason for the error are both identified. A refinement is correct, if the continuation steps are flawless.

The results of manual verification are demonstrated in Table [3,](#page-6-2) with about 85% accuracy on wrong-answer critique, and more than 90% on refinement and correct-answer critique. Therefore, the data we automatically constructed maintain a high level of accuracy at the step level, which can well support the critique training process.

## <span id="page-6-1"></span>5.2 The Necessity of CoT Critique

To assess the necessity of the stepwise CoT critic, we remove CoT and train two baselines, namely "Process Label" and "Outcome Label". Specifically, for Process Label, the model is trained to directly predict the correctness of each step, e.g., "Step

1 is correct. Step 2 is incorrect.". Further, for Outcome Label, we remove the stepwise labels, which is to predict whether the entire solution is correct without providing step-wise details, e.g., "Each step from Step 1 to Step 8 is correct" or "Some step from Step 1 to Step 8 is incorrect". These two baselines can be viewed as the natural language versions of the Process Reward Model and Outcome Reward Model.

The results are shown in Table [4.](#page-6-3) We find that removing the Chain-of-Thought intermediate analysis and further stepwise labels, negatively impacts the critic accuracy, which indicates the effectiveness of stepwise CoT critique in improving the discrimination performance. From the original Critic-CoT model to the Process Label Model and the Outcome Label Model, the critique accuracy drops from 92.3% to 89.5% and further to 88.0% on GSM8K, and from 72.2% to 63.8% and further to 63.0% on MATH500. They fail to detect more errors and the recall metric is lower, despite its tendency to more easily pass correct solutions. Compared with System-1 like reasoning without explicit analysis, System-2 like reasoning with CoT critique can more precisely identify the errors.

### <span id="page-7-0"></span>5.3 The Impact of Training Data

To evaluate the impact of different data types during training, we perform a vertical ablation by removing either the critic data or the refinement data across both stages. In addition, we perform a horizontal ablation by training only with either stage 1 data or stage 2 data.

As the result shown in Table [4,](#page-6-3) we find that training only on the single-type data is less optimal. If only training to refine, the base model's critic ability remains weak, and still *cannot effectively self-correct*, as on GSM8K the accuracy drops from 92.0% to 88.2% after iterative refinement, and on MATH500 it drops from 55.4% to 49.8%. If only training to critic, the model obtains positive improvement from iterative refinement, with increases from 91.2% to 91.4% on GSM8K and 52.8% to 55.8% on MATH500, but still lags behind to Critic-CoT model that jointly trains the two capabilities. And finally, in terms of critic and reasoning performance, combining the data from two stages is better than training the data only from one stage.

### <span id="page-7-1"></span>5.4 Comparison with Solution Distilation

Since our data construction process leverages GPT-4 Turbo, one potential concern is whether the per-

<span id="page-7-2"></span>

| Model                                       | GSM8K        | MATH500      |  |
|---------------------------------------------|--------------|--------------|--|
| Llama-3-70B-Instruct<br>GPT4-Turbo Solution | 89.6<br>90.7 | 50.4<br>48.0 |  |
| Critic-CoT                                  | 93.3         | 57.8         |  |

Table 5: Comparision between solution distillation and our Critic-CoT model with Iterative Refine, with the metric of Top-1 Accuracy. Directly training on the trajectories of advanced LLMs did not necessarily improve the performance.

formance increase comes from distilling GPT-4, or our proposed Critic-CoT framework. To address this concern and better understand the source of improvement, we also train the traditional rejection sampling fine-tuning (RFT) baseline, using GPT4-Turbo to generate a correct-answer solution for each problem on the dataset of GSM8K and MATH respectively.

As the result shown in Table [5,](#page-7-2) unlike Critic-CoT, directly distilling from frontier LLMs may not significantly improve the reasoning performance, with only 90.7% on GSM8K and 48.0% on MAT500, which is less superior. On the one hand, the Llama-3-70B model has already experienced heavy post-training for downstream reasoning tasks [\(AI@Meta,](#page-8-8) [2024\)](#page-8-8). On the other hand, as shown in Section [4.2,](#page-5-0) the improvements can be attributed to two key factors. First, strengthening the ability to critique and refinement, which is under-trained, directly improves the Top-1 accuracy. Moreover, at the inference phase, we can actively leverage the model's ability to reflect on its reasoning and correct mistakes, thus obtaining additional improvements that are not applicable without critic-refine training. Therefore, our proposed Critic-CoT framework plays a crucial role in driving the observed performance improvements.

## 6 Conclusion

In this paper, we introduced the Critic-CoT paradigm to enhance the reasoning abilities of Large Language Models, through a more System-2 like, step-by-step Chain-of-Thought critique. Our approach leverages weak supervision to construct training data for critiques and refinements, thereby reducing the reliance on extensive human annotation. We demonstrated the effectiveness of our method through substantial improvements across the dataset of GSM8K and MATH. Additionally, our results present that training on the capabilities of critique and refinement alone improves tasksolving performance, which indicates a mutualreinforce mechanism within the LLMs. We hope our work may inspire further investigations into the advancement of the self-critic framework and the transition toward System-2 reasoning.

## Limitations

In this paper, we propose Critic-CoT, a framework to automatically construct critic-refine training data in the reasoning domain, where the correctness of a solution is verifiable by checking the final answer. For more general tasks, how to filter valid critiques and train robust critic models is worth investigating in future works.

## Ethics Statement

All the data and models are acquired from public datasets and pre-trained models, and no human annotators are involved during the data construction procedure.

## Acknowledgment

We sincerely thank the reviewers for their insightful comments and valuable suggestions. This work was supported by Beijing Natural Science Foundation (L243006), Beijing Municipal Science and Technology Project (Nos. Z231100010323002), and the Natural Science Foundation of China (No. 62476265, 62306303).

# References

<span id="page-8-8"></span>AI@Meta. 2024. [Llama 3.1 model card.](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md)

- <span id="page-8-4"></span>Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, and Hannaneh Hajishirzi. 2024. [Self-RAG: Learning to](https://openreview.net/forum?id=hSyW5go0v8) [retrieve, generate, and critique through self-reflection.](https://openreview.net/forum?id=hSyW5go0v8) In *The Twelfth International Conference on Learning Representations*.
- <span id="page-8-1"></span>Sébastien Bubeck, Varun Chandrasekaran, Ronen Eldan, Johannes Gehrke, Eric Horvitz, Ece Kamar, Peter Lee, Yin Tat Lee, Yuanzhi Li, Scott Lundberg, Harsha Nori, Hamid Palangi, Marco Tulio Ribeiro, and Yi Zhang. 2023. [Sparks of artificial general in](https://arxiv.org/abs/2303.12712)[telligence: Early experiments with gpt-4.](https://arxiv.org/abs/2303.12712) *Preprint*, arXiv:2303.12712.
- <span id="page-8-2"></span>Collin Burns, Pavel Izmailov, Jan Hendrik Kirchner, Bowen Baker, Leo Gao, Leopold Aschenbrenner, Yining Chen, Adrien Ecoffet, Manas Joglekar, Jan Leike, Ilya Sutskever, and Jeff Wu. 2023. [Weak-to](https://arxiv.org/abs/2312.09390)[strong generalization: Eliciting strong capabilities](https://arxiv.org/abs/2312.09390) [with weak supervision.](https://arxiv.org/abs/2312.09390) *Preprint*, arXiv:2312.09390.
- <span id="page-8-3"></span>Boxi Cao, Keming Lu, Xinyu Lu, Jiawei Chen, Mengjie Ren, Hao Xiang, Peilin Liu, Yaojie Lu, Ben He, Xianpei Han, Le Sun, Hongyu Lin, and Bowen Yu. 2024. [Towards scalable automated alignment of llms: A](https://arxiv.org/abs/2406.01252) [survey.](https://arxiv.org/abs/2406.01252) *Preprint*, arXiv:2406.01252.
- <span id="page-8-12"></span>Chi-Min Chan, Weize Chen, Yusheng Su, Jianxuan Yu, Wei Xue, Shanghang Zhang, Jie Fu, and Zhiyuan Liu. 2024. [Chateval: Towards better LLM-based eval](https://openreview.net/forum?id=FQepisCUWu)[uators through multi-agent debate.](https://openreview.net/forum?id=FQepisCUWu) In *The Twelfth International Conference on Learning Representations*.
- <span id="page-8-10"></span>Guoxin Chen, Minpeng Liao, Chengxi Li, and Kai Fan. 2024a. [Alphamath almost zero: process supervision](https://doi.org/10.48550/ARXIV.2405.03553) [without process.](https://doi.org/10.48550/ARXIV.2405.03553) *CoRR*, abs/2405.03553.
- <span id="page-8-7"></span>Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba. 2021. [Evaluat](https://arxiv.org/abs/2107.03374)[ing large language models trained on code.](https://arxiv.org/abs/2107.03374) *Preprint*, arXiv:2107.03374.
- <span id="page-8-11"></span>Xingyu Chen, Jiahao Xu, Tian Liang, Zhiwei He, Jianhui Pang, Dian Yu, Linfeng Song, Qiuzhi Liu, Mengfei Zhou, Zhuosheng Zhang, et al. 2024b. Do not think that much for 2+ 3=? on the overthinking of o1-like llms. *arXiv preprint arXiv:2412.21187*.
- <span id="page-8-0"></span>François Chollet. 2019. [On the measure of intelligence.](https://arxiv.org/abs/1911.01547) *Preprint*, arXiv:1911.01547.
- <span id="page-8-6"></span>Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman. 2021a. [Training verifiers to solve math word prob](https://arxiv.org/abs/2110.14168)[lems.](https://arxiv.org/abs/2110.14168) *CoRR*, abs/2110.14168.
- <span id="page-8-9"></span>Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman. 2021b. [Training verifiers to solve math word prob](https://arxiv.org/abs/2110.14168)[lems.](https://arxiv.org/abs/2110.14168) *Preprint*, arXiv:2110.14168.
- <span id="page-8-5"></span>DeepSeek-AI, Aixin Liu, Bei Feng, Bin Wang, Bingxuan Wang, Bo Liu, and et al. 2024. [Deepseek-v2: A](https://doi.org/10.48550/ARXIV.2405.04434) [strong, economical, and efficient mixture-of-experts](https://doi.org/10.48550/ARXIV.2405.04434) [language model.](https://doi.org/10.48550/ARXIV.2405.04434) *CoRR*, abs/2405.04434.
- <span id="page-9-7"></span>Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, Anirudh Goyal, Anthony Hartshorn, Aobo Yang, Archi Mitra, and et al. 2024. [The llama 3 herd of](https://arxiv.org/abs/2407.21783) [models.](https://arxiv.org/abs/2407.21783) *Preprint*, arXiv:2407.21783.
- <span id="page-9-14"></span>Guhao Feng, Bohang Zhang, Yuntian Gu, Haotian Ye, Di He, and Liwei Wang. 2023. [Towards revealing](https://openreview.net/forum?id=qHrADgAdYu) [the mystery behind chain of thought: A theoretical](https://openreview.net/forum?id=qHrADgAdYu) [perspective.](https://openreview.net/forum?id=qHrADgAdYu) In *Thirty-seventh Conference on Neural Information Processing Systems*.
- <span id="page-9-17"></span>Kanishk Gandhi, Ayush Chakravarthy, Anikait Singh, Nathan Lile, and Noah D Goodman. 2025. Cognitive behaviors that enable self-improving reasoners, or, four habits of highly effective stars. *arXiv preprint arXiv:2503.01307*.
- <span id="page-9-8"></span>Bofei Gao, Zefan Cai, Runxin Xu, Peiyi Wang, Ce Zheng, Runji Lin, Keming Lu, Junyang Lin, Chang Zhou, Wen Xiao, Junjie Hu, Tianyu Liu, and Baobao Chang. 2024. [LLM critics help catch](https://doi.org/10.48550/ARXIV.2406.14024) [bugs in mathematics: Towards a better mathemati](https://doi.org/10.48550/ARXIV.2406.14024)[cal verifier with natural language feedback.](https://doi.org/10.48550/ARXIV.2406.14024) *CoRR*, abs/2406.14024.
- <span id="page-9-12"></span>Mor Geva, Daniel Khashabi, Elad Segal, Tushar Khot, Dan Roth, and Jonathan Berant. 2021. [Did aristotle](https://doi.org/10.1162/tacl_a_00370) [use a laptop? a question answering benchmark with](https://doi.org/10.1162/tacl_a_00370) [implicit reasoning strategies.](https://doi.org/10.1162/tacl_a_00370) *Transactions of the Association for Computational Linguistics*, 9:346– 361.
- <span id="page-9-16"></span>Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. 2025. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. *arXiv preprint arXiv:2501.12948*.
- <span id="page-9-13"></span>Alexander Havrilla, Yuqing Du, Sharath Chandra Raparthy, Christoforos Nalmpantis, Jane Dwivedi-Yu, Eric Hambro, Sainbayar Sukhbaatar, and Roberta Raileanu. 2024. [Teaching large language models to](https://openreview.net/forum?id=mjqoceuMnI) [reason with reinforcement learning.](https://openreview.net/forum?id=mjqoceuMnI) In *AI for Math Workshop @ ICML 2024*.
- <span id="page-9-18"></span>Yancheng He, Shilong Li, Jiaheng Liu, Weixun Wang, Xingyuan Bu, Ge Zhang, Zhongyuan Peng, Zhaoxiang Zhang, Wenbo Su, and Bo Zheng. 2025. Can large language models detect errors in long chain-of-thought reasoning? *arXiv preprint arXiv:2502.19361*.
- <span id="page-9-0"></span>G.W.F. Hegel, T.F. Geraets, W.A. Suchting, and H.S. Harris. 1991. *[The Encyclopaedia Logic, with the](https://books.google.ca/books?id=4BNUFZ_hQ1wC) [Zustze: Part I of the Encyclopaedia of Philosophical](https://books.google.ca/books?id=4BNUFZ_hQ1wC) [Sciences with the Zusatze](https://books.google.ca/books?id=4BNUFZ_hQ1wC)*. Hackett Classics Series. Hackett.
- <span id="page-9-10"></span>Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob Steinhardt. 2021. [Measuring mathematical](https://openreview.net/forum?id=7Bywt2mQsCe) [problem solving with the MATH dataset.](https://openreview.net/forum?id=7Bywt2mQsCe) In *Thirtyfifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2)*.
- <span id="page-9-5"></span>Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, and Denny Zhou. 2024. [Large language](https://openreview.net/forum?id=IkmD3fKBPQ) [models cannot self-correct reasoning yet.](https://openreview.net/forum?id=IkmD3fKBPQ) In *The Twelfth International Conference on Learning Representations*.
- <span id="page-9-6"></span>Ziwei Ji, Tiezheng Yu, Yan Xu, Nayeon Lee, Etsuko Ishii, and Pascale Fung. 2023. [Towards mitigating](https://doi.org/10.18653/v1/2023.findings-emnlp.123) [LLM hallucination via self reflection.](https://doi.org/10.18653/v1/2023.findings-emnlp.123) In *Findings of the Association for Computational Linguistics: EMNLP 2023*, pages 1827–1843, Singapore. Association for Computational Linguistics.
- <span id="page-9-4"></span>Daniel Kahneman. 2011. *Thinking Fast and Slow*. Farrar, Straus and Giroux.
- <span id="page-9-1"></span>Søren Kierkegaard. 1989. *[Kierkegaard's Writings, II,](http://www.jstor.org/stable/j.ctt24hr3n) [Volume 2: The Concept of Irony, with Continual Ref](http://www.jstor.org/stable/j.ctt24hr3n)[erence to Socrates/Notes of Schelling's Berlin Lec](http://www.jstor.org/stable/j.ctt24hr3n)[tures](http://www.jstor.org/stable/j.ctt24hr3n)*. Princeton University Press.
- <span id="page-9-2"></span>Geunwoo Kim, Pierre Baldi, and Stephen Marcus McAleer. 2023. [Language models can solve com](https://openreview.net/forum?id=M6OmjAZ4CX)[puter tasks.](https://openreview.net/forum?id=M6OmjAZ4CX) In *Thirty-seventh Conference on Neural Information Processing Systems*.
- <span id="page-9-9"></span>Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gonzalez, Hao Zhang, and Ion Stoica. 2023. [Efficient](https://doi.org/10.1145/3600006.3613165) [memory management for large language model serv](https://doi.org/10.1145/3600006.3613165)[ing with pagedattention.](https://doi.org/10.1145/3600006.3613165) In *Proceedings of the 29th Symposium on Operating Systems Principles*, SOSP '23, page 611–626, New York, NY, USA. Association for Computing Machinery.
- <span id="page-9-3"></span>Jan Leike, David Krueger, Tom Everitt, Miljan Martic, Vishal Maini, and Shane Legg. 2018. [Scalable agent](https://arxiv.org/abs/1811.07871) [alignment via reward modeling: a research direction.](https://arxiv.org/abs/1811.07871) *Preprint*, arXiv:1811.07871.
- <span id="page-9-15"></span>Zhiyuan Li, Hong Liu, Denny Zhou, and Tengyu Ma. 2024. [Chain of thought empowers transformers to](https://openreview.net/forum?id=3EWTEy9MTM) [solve inherently serial problems.](https://openreview.net/forum?id=3EWTEy9MTM) In *The Twelfth International Conference on Learning Representations*.
- <span id="page-9-20"></span>Tian Liang, Zhiwei He, Wenxiang Jiao, Xing Wang, Yan Wang, Rui Wang, Yujiu Yang, Shuming Shi, and Zhaopeng Tu. 2024. [Encouraging divergent thinking](https://doi.org/10.18653/v1/2024.emnlp-main.992) [in large language models through multi-agent debate.](https://doi.org/10.18653/v1/2024.emnlp-main.992) In *Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing*, pages 17889–17904, Miami, Florida, USA. Association for Computational Linguistics.
- <span id="page-9-11"></span>Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. 2024. [Let's verify step by step.](https://openreview.net/forum?id=v8L0pN6EOi) In *The Twelfth International Conference on Learning Representations*.
- <span id="page-9-19"></span>Zicheng Lin, Zhibin Gou, Tian Liang, Ruilin Luo, Haowei Liu, and Yujiu Yang. 2024. [CriticBench:](https://doi.org/10.18653/v1/2024.findings-acl.91) [Benchmarking LLMs for critique-correct reasoning.](https://doi.org/10.18653/v1/2024.findings-acl.91) In *Findings of the Association for Computational Linguistics: ACL 2024*, pages 1552–1587, Bangkok, Thailand. Association for Computational Linguistics.
- <span id="page-10-16"></span>Yixin Liu, Avi Singh, C. Daniel Freeman, John D. Co-Reyes, and Peter J. Liu. 2023. [Improving large lan](https://doi.org/10.48550/ARXIV.2310.10047)[guage model fine-tuning for solving math problems.](https://doi.org/10.48550/ARXIV.2310.10047) *CoRR*, abs/2310.10047.
- <span id="page-10-6"></span>Liangchen Luo, Zi Lin, Yinxiao Liu, Lei Shu, Yun Zhu, Jingbo Shang, and Lei Meng. 2023. [Cri](https://arxiv.org/abs/2310.04815)[tique ability of large language models.](https://arxiv.org/abs/2310.04815) *Preprint*, arXiv:2310.04815.
- <span id="page-10-18"></span>Liangchen Luo, Yinxiao Liu, Rosanne Liu, Samrat Phatale, Harsh Lara, Yunxuan Li, Lei Shu, Yun Zhu, Lei Meng, Jiao Sun, and Abhinav Rastogi. 2024. [Improve mathematical reasoning in language](https://arxiv.org/abs/2406.06592) [models by automated process supervision.](https://arxiv.org/abs/2406.06592) *Preprint*, arXiv:2406.06592.
- <span id="page-10-3"></span>Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann, Sean Welleck, Amir Yazdanbakhsh, and Peter Clark. 2023. [Self-refine: Itera](https://openreview.net/forum?id=S37hOerQLB)[tive refinement with self-feedback.](https://openreview.net/forum?id=S37hOerQLB) In *Thirty-seventh Conference on Neural Information Processing Systems*.
- <span id="page-10-5"></span>Nat McAleese, Rai Michael Pokorny, Juan Felipe Ceron Uribe, Evgenia Nitishinskaya, Maja Trebacz, and Jan Leike. 2024. [Llm critics help catch llm bugs.](https://arxiv.org/abs/2407.00215) *Preprint*, arXiv:2407.00215.
- <span id="page-10-0"></span>Meredith Ringel Morris, Jascha Sohl-Dickstein, Noah Fiedel, Tris Warkentin, Allan Dafoe, Aleksandra Faust, Clement Farabet, and Shane Legg. 2024. [Posi](https://openreview.net/forum?id=0ofzEysK2D)[tion: Levels of AGI for operationalizing progress on](https://openreview.net/forum?id=0ofzEysK2D) [the path to AGI.](https://openreview.net/forum?id=0ofzEysK2D) In *Forty-first International Conference on Machine Learning*.
- <span id="page-10-10"></span>OpenAI. 2023. [GPT-4 technical report.](https://doi.org/10.48550/ARXIV.2303.08774) *CoRR*, abs/2303.08774.
- <span id="page-10-8"></span>OpenAI. 2024. [Openai o1 system card.](https://assets.ctfassets.net/kftzwdyauwt9/67qJD51Aur3eIc96iOfeOP/71551c3d223cd97e591aa89567306912/o1_system_card.pdf)
- <span id="page-10-17"></span>Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul F Christiano, Jan Leike, and Ryan Lowe. 2022. [Training language models to follow instructions with](https://proceedings.neurips.cc/paper_files/paper/2022/file/b1efde53be364a73914f58805a001731-Paper-Conference.pdf) [human feedback.](https://proceedings.neurips.cc/paper_files/paper/2022/file/b1efde53be364a73914f58805a001731-Paper-Conference.pdf) In *Advances in Neural Information Processing Systems*, volume 35, pages 27730–27744. Curran Associates, Inc.
- <span id="page-10-20"></span>Long Phan, Alice Gatti, Ziwen Han, Nathaniel Li, Josephina Hu, Hugh Zhang, Chen Bo Calvin Zhang, Mohamed Shaaban, John Ling, Sean Shi, et al. 2025. Humanity's last exam. *arXiv preprint arXiv:2501.14249*.
- <span id="page-10-1"></span>Karl Raimund Popper. 1934. *The Logic of Scientific Discovery*. Routledge, New York.
- <span id="page-10-14"></span>Samyam Rajbhandari, Olatunji Ruwase, Jeff Rasley, Shaden Smith, and Yuxiong He. 2021. [Zero-infinity:](https://doi.org/10.1145/3458817.3476205) [breaking the gpu memory wall for extreme scale deep](https://doi.org/10.1145/3458817.3476205) [learning.](https://doi.org/10.1145/3458817.3476205) In *Proceedings of the International Conference for High Performance Computing, Networking, Storage and Analysis*, SC '21, New York, NY, USA. Association for Computing Machinery.
- <span id="page-10-4"></span>William Saunders, Catherine Yeh, Jeff Wu, Steven Bills, Long Ouyang, Jonathan Ward, and Jan Leike. 2022. [Self-critiquing models for assisting human evaluators.](https://arxiv.org/abs/2206.05802) *Preprint*, arXiv:2206.05802.
- <span id="page-10-21"></span>Tom Schaul. 2024. Boundless socratic learning with language games. *arXiv preprint arXiv:2411.16905*.
- <span id="page-10-2"></span>Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik R Narasimhan, and Shunyu Yao. 2023. [Re](https://openreview.net/forum?id=vAElhFcKW6)[flexion: language agents with verbal reinforcement](https://openreview.net/forum?id=vAElhFcKW6) [learning.](https://openreview.net/forum?id=vAElhFcKW6) In *Thirty-seventh Conference on Neural Information Processing Systems*.
- <span id="page-10-19"></span>Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar. 2024. [Scaling llm test-time compute optimally](https://arxiv.org/abs/2408.03314) [can be more effective than scaling model parameters.](https://arxiv.org/abs/2408.03314) *Preprint*, arXiv:2408.03314.
- <span id="page-10-11"></span>Yuxuan Tong, Xiwen Zhang, Rui Wang, Ruidong Wu, and Junxian He. 2024. [Dart-math: Difficulty-aware](https://arxiv.org/abs/2407.13690) [rejection tuning for mathematical problem-solving.](https://arxiv.org/abs/2407.13690) *Preprint*, arXiv:2407.13690.
- <span id="page-10-12"></span>Peiyi Wang, Lei Li, Zhihong Shao, R. X. Xu, Damai Dai, Yifei Li, Deli Chen, Y. Wu, and Zhifang Sui. 2023a. [Math-shepherd: Verify and reinforce llms](https://doi.org/10.48550/ARXIV.2312.08935) [step-by-step without human annotations.](https://doi.org/10.48550/ARXIV.2312.08935) *CoRR*, abs/2312.08935.
- <span id="page-10-9"></span>Tianlu Wang, Ilia Kulikov, Olga Golovneva, Ping Yu, Weizhe Yuan, Jane Dwivedi-Yu, Richard Yuanzhe Pang, Maryam Fazel-Zarandi, Jason Weston, and Xian Li. 2024. [Self-taught evaluators.](https://arxiv.org/abs/2408.02666) *Preprint*, arXiv:2408.02666.
- <span id="page-10-15"></span>Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le, Ed H. Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou. 2023b. [Self-consistency improves](https://openreview.net/forum?id=1PL1NIMMrw) [chain of thought reasoning in language models.](https://openreview.net/forum?id=1PL1NIMMrw) In *The Eleventh International Conference on Learning Representations*.
- <span id="page-10-7"></span>Peter West, Ximing Lu, Nouha Dziri, Faeze Brahman, Linjie Li, Jena D. Hwang, Liwei Jiang, Jillian Fisher, Abhilasha Ravichander, Khyathi Chandu, Benjamin Newman, Pang Wei Koh, Allyson Ettinger, and Yejin Choi. 2024. [The generative AI paradox: "what it can](https://openreview.net/forum?id=CF8H8MS5P8) [create, it may not understand".](https://openreview.net/forum?id=CF8H8MS5P8) In *The Twelfth International Conference on Learning Representations*.
- <span id="page-10-13"></span>Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement Delangue, Anthony Moi, Pierric Cistac, Tim Rault, Rémi Louf, Morgan Funtowicz, Joe Davison, Sam Shleifer, Patrick von Platen, Clara Ma, Yacine Jernite, Julien Plu, Canwen Xu, Teven Le Scao, Sylvain Gugger, Mariama Drame, Quentin

Lhoest, and Alexander M. Rush. 2020. [Transform](https://www.aclweb.org/anthology/2020.emnlp-demos.6)[ers: State-of-the-art natural language processing.](https://www.aclweb.org/anthology/2020.emnlp-demos.6) In *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations*, pages 38–45, Online. Association for Computational Linguistics.

- <span id="page-11-4"></span>Zhenyu Wu, Qingkai Zeng, Zhihan Zhang, Zhaoxuan Tan, Chao Shen, and Meng Jiang. 2024. [Large lan](https://aclanthology.org/2024.emnlp-main.714)[guage models can self-correct with key condition ver](https://aclanthology.org/2024.emnlp-main.714)[ification.](https://aclanthology.org/2024.emnlp-main.714) In *Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing*, pages 12846–12867, Miami, Florida, USA. Association for Computational Linguistics.
- <span id="page-11-3"></span>Hanqi Yan, Qinglin Zhu, Xinyu Wang, Lin Gui, and Yulan He. 2024. [Mirror: Multiple-perspective self](https://doi.org/10.18653/v1/2024.acl-long.382)[reflection method for knowledge-rich reasoning.](https://doi.org/10.18653/v1/2024.acl-long.382) In *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 7086–7103, Bangkok, Thailand. Association for Computational Linguistics.
- <span id="page-11-11"></span>An Yang, Baosong Yang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Zhou, and et al. 2024. [Qwen2](https://arxiv.org/abs/2407.10671) [technical report.](https://arxiv.org/abs/2407.10671) *Preprint*, arXiv:2407.10671.
- <span id="page-11-6"></span>Huaiyuan Ying, Shuo Zhang, Linyang Li, Zhejian Zhou, Yunfan Shao, Zhaoye Fei, Yichuan Ma, Jiawei Hong, Kuikun Liu, Ziyi Wang, Yudong Wang, Zijian Wu, Shuaibin Li, Fengzhe Zhou, Hongwei Liu, Songyang Zhang, Wenwei Zhang, Hang Yan, Xipeng Qiu, Jiayu Wang, Kai Chen, and Dahua Lin. 2024. [Internlm](https://doi.org/10.48550/ARXIV.2402.06332)[math: Open math large language models toward veri](https://doi.org/10.48550/ARXIV.2402.06332)[fiable reasoning.](https://doi.org/10.48550/ARXIV.2402.06332) *CoRR*, abs/2402.06332.
- <span id="page-11-0"></span>Ping Yu, Jing Xu, Jason Weston, and Ilia Kulikov. 2024. [Distilling system 2 into system 1.](https://arxiv.org/abs/2407.06023) *Preprint*, arXiv:2407.06023.
- <span id="page-11-10"></span>Weizhe Yuan, Richard Yuanzhe Pang, Kyunghyun Cho, Xian Li, Sainbayar Sukhbaatar, Jing Xu, and Jason E Weston. 2024. [Self-rewarding language mod](https://openreview.net/forum?id=0NphYCmgua)[els.](https://openreview.net/forum?id=0NphYCmgua) In *Forty-first International Conference on Machine Learning*.
- <span id="page-11-9"></span>Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah Goodman. 2022. [STar: Bootstrapping reasoning with rea](https://openreview.net/forum?id=_3ELRdg2sgI)[soning.](https://openreview.net/forum?id=_3ELRdg2sgI) In *Advances in Neural Information Processing Systems*.
- <span id="page-11-1"></span>Zhongshen Zeng, Pengguang Chen, Shu Liu, Haiyun Jiang, and Jiaya Jia. 2023. [Mr-gsm8k: A meta](https://doi.org/10.48550/ARXIV.2312.17080)[reasoning benchmark for large language model eval](https://doi.org/10.48550/ARXIV.2312.17080)[uation.](https://doi.org/10.48550/ARXIV.2312.17080) *CoRR*, abs/2312.17080.
- <span id="page-11-5"></span>Lunjun Zhang, Arian Hosseini, Hritik Bansal, Mehran Kazemi, Aviral Kumar, and Rishabh Agarwal. 2024a. [Generative verifiers: Reward modeling as next-token](https://arxiv.org/abs/2408.15240) [prediction.](https://arxiv.org/abs/2408.15240) *Preprint*, arXiv:2408.15240.
- <span id="page-11-2"></span>Wenqi Zhang, Yongliang Shen, Linjuan Wu, Qiuying Peng, Jun Wang, Yueting Zhuang, and Weiming Lu. 2024b. [Self-contrast: Better reflection through](https://doi.org/10.18653/v1/2024.acl-long.197) [inconsistent solving perspectives.](https://doi.org/10.18653/v1/2024.acl-long.197) In *Proceedings of the 62nd Annual Meeting of the Association for*

*Computational Linguistics (Volume 1: Long Papers)*, pages 3602–3622, Bangkok, Thailand. Association for Computational Linguistics.

- <span id="page-11-7"></span>Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric Xing, Hao Zhang, Joseph E Gonzalez, and Ion Stoica. 2023. [Judging](https://proceedings.neurips.cc/paper_files/paper/2023/file/91f18a1287b398d378ef22505bf41832-Paper-Datasets_and_Benchmarks.pdf) [llm-as-a-judge with mt-bench and chatbot arena.](https://proceedings.neurips.cc/paper_files/paper/2023/file/91f18a1287b398d378ef22505bf41832-Paper-Datasets_and_Benchmarks.pdf) In *Advances in Neural Information Processing Systems*, volume 36, pages 46595–46623. Curran Associates, Inc.
- <span id="page-11-8"></span>Wanjun Zhong, Ruixiang Cui, Yiduo Guo, Yaobo Liang, Shuai Lu, Yanlin Wang, Amin Saied, Weizhu Chen, and Nan Duan. 2023. [Agieval: A human](https://arxiv.org/abs/2304.06364)[centric benchmark for evaluating foundation models.](https://arxiv.org/abs/2304.06364) *Preprint*, arXiv:2304.06364.

## A Appendix

### <span id="page-12-0"></span>A.1 Training & Evaluation Details

### A.1.1 Critic Data Construction

GSM8K On GSM8K, since GPT-4 already got 92.0% accuracy on the test set [\(OpenAI,](#page-10-10) [2023\)](#page-10-10), which makes it hard to obtain negative data, we use GPT-3.5-Turbo-0125 instead to sample 10 solutions for each question in the training set. Then, we use GPT-4-Turbo as the critic-refine model to criticize the solutions (Table [A7\)](#page-21-0), with K = 16 retry. We obtain 63,485 cases, with 49,832 positive examples and 13,653 negative examples.

In the second stage of GSM8K critique construction, we use the learned critic model to repeatedly sample until we obtain at most 5 positive and 5 negative solutions. For strong LLMs like LLaMA-3, it's challenging to get enough negative solutions even among 512 samples, so the size of negative data would be slightly smaller. Then, we use the learned critic model to criticize itself, also with K = 16 retry. In stage two, we obtain 62,877 instances, with 39,654 positive and 26,001 negative. Among the two stages, we got 126,362 instances, with 86,708 positive and 39,654 negative.

MATH On MATH, in the first stage, we directly use the 90,074 GPT-4 generated solutions of PRM800K Dataset [\(Lightman et al.,](#page-9-11) [2024\)](#page-9-11), with 11,665 positive instances which all the step labels are correct, and 78,409 negative instances which one step label is incorrect. Since the MATH dataset is challenging, in order to reduce retry of GPT-4-Turbo and avoid not getting valid critique, for the critique of the negative solution, we additionally append reference solution in the input prompt, and hint it might contain mistakes, as suggested in prior work [\(Zelikman et al.,](#page-11-9) [2022\)](#page-11-9); for the positive solution, we simply hint it's correct. After obtaining the initial critique, we use GPT-4-Turbo again to remove hint phrases like "According to the reference" or "Given the hint" since we do not have any hint or reference during the test time. In stage one, we obtain 1,606 positive cases and 69,775 negative cases.

Similarly, in the second stage of MATH, we use the learned critic model to sample at most 5 positive and negative solutions. Then, we first use the critic model itself to critic its solutions, and without any hints, under K = 16 retry, and use GPT-4-Turbo to retry another K = 16 times with hint if failed. We construct 51,618 positive cases and 65,456 negative

cases. Among the two stages, we got 188,455 cases, with 53,224 positive and 135,231 negative.

### <span id="page-12-1"></span>A.1.2 Answer Extraction

We let the model print the answer in the format \boxed{answer}. The model generates the answer following this pattern. We then extract the regular expression \boxed{.\*} from the model output, and obtain the valid answer expression with matched parenthesis. The Python code for answer extraction is shown in Table [A5.](#page-18-0)

### A.1.3 Evaluation Metric

Solution For the evaluation of the solution, we extract the final answer (Appendix [A.1.2\)](#page-12-1) and compute the metrics of Top-1 Accuracy Acc and Refine Accuracy Refine-Acc, in which the original Top-1 predict-answer is replaced with a refined one if the critic model found an error and made iterative refinement (Section [3.3\)](#page-3-2). We also compute Majority Vote Accuracy Maj1@N [\(Wang et al.,](#page-10-15) [2023b\)](#page-10-15) and Majority Vote Accuracy After Critique Critic + Maj1@N (Section [3.3\)](#page-3-3), which is to select the most frequent answer among N samples, i.e. arg max<sup>a</sup> P<sup>N</sup> <sup>i</sup>=1 <sup>1</sup> (a<sup>i</sup> <sup>=</sup> <sup>a</sup>). Following [Liu et al.](#page-10-16) [\(2023\)](#page-10-16); [Havrilla et al.](#page-9-13) [\(2024\)](#page-9-13), we compute Pass@N, which select the gold answer g among the N predictions if present, i.e. arg max<sup>a</sup> 1 (g = a).

Critique For the "evaluation of evaluation", we compute Precision, Recall, and F1 for error detection; also, we compute Critic Accuracy, where the critique should find the error in wrong answer solutions and pass the correct answer solution:

$$
P = \frac{\{|Pred_i \neq Ans_i \land -1 \in L_i|\}}{| \{-1 \in L_i\}|} \qquad (1)
$$

$$
R = \frac{\{|Pred_i \neq Ans_i \land -1 \in L_i|\}}{|\{Pred_i \neq Ans_i\}|} \qquad (2)
$$

$$
F1 = \frac{2 \times P \times R}{P + R} \tag{3}
$$

$$
CriticAcc =
$$
  
\n
$$
\frac{1}{N} \sum_{i=1}^{N} (Pred_i = Ans_i \land -1 \notin L_i)
$$
 (4)  
\n
$$
\lor (Pred_i \neq Ans_i \land -1 \in L_i)
$$

Here, for the i-th instance, P red<sup>i</sup> is the prediction answer, Ans<sup>i</sup> is the ground truth answer, and L<sup>i</sup> is the predicted step label list.

### A.1.4 Implementation Details

The training on GSM8K dataset takes 23 hours, while on MATH dataset it takes 37 hours. The two datasets are under MIT license. For software, Huggingface Transformers, DeepSpeed, vLLM, and FastChat libraries we used are under Apache-2.0 license.

### A.2 Additional Result on MATH

Table [A1](#page-14-0) presents the results of Critic-CoT training on MATH dataset, with the original 7,500/5,000 split setting.

### <span id="page-13-0"></span>A.3 Analysis

### A.3.1 Critic Performance

For both datasets, the critic model's accuracy continues to grow as the sample size N increases, ultimately surpassing the performance of the majority vote, which gradually converges. Specifically, in the MATH dataset, the critic model achieves substantially higher accuracy than the solution accuracy, consistently outperforming the naive majority vote due to the critic filter's superior performance. This stark contrast highlights the critic model's effectiveness in identifying and promoting correct answers. In the GSM8K dataset, despite having a critic accuracy of only 92.3%, the critic model still manages to deliver higher accuracy gains. This outcome suggests that the critic model successfully filters answers to increase the density of correct answers and decrease the density of wrong answers, compared to the normal answer distribution. The overall results demonstrate the critic model's robust capability to enhance accuracy across different datasets, validating its practical utility in improving prediction outcomes.

### A.3.2 Inspect on Iterative Refine

The iterative refinement process for the GSM8K and MATH datasets demonstrates different levels of effectiveness due to their complexity, as shown in Table [A2.](#page-15-0) GSM8K, being simpler, shows a higher success rate in refinement. For effective refinement, the number of false answers corrected (False → True) must exceed the number of true answers incorrectly changed (True → False). Despite occasional mistakes by the critic, correct answers are not always altered incorrectly.

For GSM8K (Table [A2a\)](#page-15-0), accuracy improves from 91.7% initially to 93.3% by the seventh round, with significant gains in both true-to-true and falseto-true transformations. In contrast, MATH (Table

[A2b\)](#page-15-0) starts at 57.6% accuracy, reaching 57.8% by the seventh round. The iterative refinement process tends to converge, which is expected.

### A.3.3 Group By Difficulty Level

For the MATH dataset, the difficulty level is given from 1 to 5. For the GSM8K dataset, we set the difficulty level according to the number of expressions n that appeared in the reference solution, i.e., max(1, min(5, n)). As illustrated in Figure [A2,](#page-15-1) the performance on the GSM8K dataset shows a gradual decline as the difficulty level increases. This trend is accompanied by the emerging effects of the critic and refine stages, which become more prominent at higher difficulty levels. In contrast, the accuracy on the MATH dataset declines sharply as the problems become more challenging. Generally, the refine stage proves effective across all levels, while the critic stage is beneficial at most levels, with some minor exceptions. These observations suggest potential areas for further improvements in the critic mechanism.

### <span id="page-13-1"></span>A.4 Discussion

### A.4.1 Discriminative Verifier for Mathematics

To further improve the reasoning ability of large language models, one applicable approach is through the use of reward models, which can either be used in reinforcement learning during training [\(Ouyang et al.,](#page-10-17) [2022\)](#page-10-17) or rejection sampling at test time [\(Cobbe et al.,](#page-8-9) [2021b\)](#page-8-9). While outcomesupervised reward models (ORMs) allow for the automatic collection of training data based on the signal of the gold answer, process-supervised reward models (PRMs) would be more advantageous for more precise feedback, better interpretability and stronger alignment [\(Lightman et al.,](#page-9-11) [2024\)](#page-9-11).

To reduce the considerable human labeling cost and difficulty for dense annotation, a series of works based on automatic approaches have been proposed [\(Wang et al.,](#page-10-12) [2023a;](#page-10-12) [Chen et al.,](#page-8-10) [2024a;](#page-8-10) [Luo et al.,](#page-10-18) [2024;](#page-10-18) [Snell et al.,](#page-10-19) [2024\)](#page-10-19), all under the heuristic that for an incorrect solution, the first error step is where the continuation of previous step would lead to a correct answer. This may bring noise into training data due to false positives and negatives [\(Luo et al.,](#page-10-18) [2024\)](#page-10-18). Moreover, annotation based on the implicit solution continuation alone does not leverage LLM's emerging ability of critic, which is in a more explicit and analytic way and brings better explainability [\(Saun](#page-10-4)[ders et al.,](#page-10-4) [2022;](#page-10-4) [Yuan et al.,](#page-11-10) [2024;](#page-11-10) [Luo et al.,](#page-10-6) [2023;](#page-10-6)

<span id="page-14-0"></span>

| Model                                            | Sampling Method   | Acc.       |
|--------------------------------------------------|-------------------|------------|
| Llama-3-70B-Instruct (Dubey et al., 2024)        | -                 | 51.0       |
|                                                  | Maj1@96           | 63.5       |
|                                                  | Maj1@512          | 64.3       |
| Llama-3.1-70B-Instruct (Dubey et al., 2024)      | -                 | 68.0       |
| DeepSeek-V2 Chat-236B (DeepSeek-AI et al., 2024) | -                 | 53.9       |
| Qwen2-72B (Yang et al., 2024)                    | -                 | 69.0       |
| GPT4-0314 (OpenAI, 2023)                         | -                 | 42.5       |
| Critic-CoT, Llama-3-70B-Instruct (Ours)          | -                 | 56.2       |
|                                                  | Iterative Refine  | 56.6 ↑ 0.4 |
|                                                  | Maj1@96           | 64.2       |
|                                                  | Critic + Maj1@96  | 65.0 ↑ 0.8 |
|                                                  | Maj1@512          | 64.4       |
|                                                  | Critic + Maj1@512 | 66.4 ↑ 2.0 |

Table A1: Solution Accuracy of MATH. The top-1 accuracy of our method increases from 51.0% to 56.2%, and the effect of iterative refinement is moderate but positive improvement of 0.4%, while the performance gain of the critic filter is larger.

![](./assets/critic-cot/_page_14_Figure_2.jpeg)

Figure A1: Performance of majority vote on GSM8K and MATH500 Datasets

[McAleese et al.,](#page-10-5) [2024\)](#page-10-5). Additionally, binary 0/1 discrimination alone, whether outcome-based or process-based, remains more similar to System-1 reasoning rather than the desirable System-2, thus may not fully leverage the computation power support by empirically successful Chain-of-Thought prompting [\(Feng et al.,](#page-9-14) [2023;](#page-9-14) [Li et al.,](#page-9-15) [2024\)](#page-9-15).

## A.4.2 Differences Between Critic-CoT and Reflexion

We adopt a similar approach to Relexion [\(Shinn](#page-10-2) [et al.,](#page-10-2) [2023\)](#page-10-2), which leverages natural language critique to facilitate refinement, but our method diverges in the following ways:

Step-wise CoT Critique Reflexion translates and augments the binary reward signal from the

environment to natural language, but on an instance level. Instead, fine-grained Chain-of-Thought analysis at the step level, which is more systematic, and enables us to locate the error and start refinement from a specific step, rather than refine the whole attempt.

Enhanced Critic ability While Relexion proposed an in-context learning pipeline for policy optimization under the oracle success/fail binary feedback signal, [Huang et al.](#page-9-5) [\(2024\)](#page-9-5) showed that without external feedback, vanilla LLMs cannot self-correct effectively due to limited critique ability. Therefore, to teach the LLMs the ability of intrinsic self-critique, our approach tries to learn the critique ability itself, through Critic-CoT train-

<span id="page-15-1"></span>![](./assets/critic-cot/_page_15_Figure_0.jpeg)

Figure A2: Performance group by difficulty level, on GSM8K and MATH500 Datasets

<span id="page-15-0"></span>

| Round  | Refine Acc.  | True →<br>True | False →<br>True |  |
|--------|--------------|----------------|-----------------|--|
| 0      | 91.7         | -              | -               |  |
| 1      | 91.7         | 48.2           | 45.3            |  |
| 2      | 92.6         | 78.6           | 37.5            |  |
| 3      | 92.7         | 64.3           | 53.1            |  |
| 4      | 93.0         | 73.2           | 50.0            |  |
| 5      | 93.2         | 75.0           | 53.1            |  |
| 6      | 93.2         | 76.8           | 53.1            |  |
| 7      | 93.3         | 80.4           | 50.0            |  |
| 8      | 93.3         | 80.4           | 50.0            |  |
|        | (a) GSM8K    |                |                 |  |
|        |              |                | False →<br>True |  |
| Round  | Refine Acc.  | True →<br>True |                 |  |
|        |              |                |                 |  |
| 0      | 57.6         | -              | -               |  |
| 1      | 53.4         | 29.0           | 17.7            |  |
| 2      | 57.2         | 65.7           | 13.9            |  |
| 3      | 55.2         | 48.6           | 15.2            |  |
| 4      | 57.2         | 60.9           | 15.9            |  |
| 5      | 57.4         | 60.0           | 17.1            |  |
| 6      | 57.6         | 61.4           | 17.1            |  |
| 7<br>8 | 57.8<br>57.8 | 60.0<br>62.9   | 18.4<br>16.5    |  |

Table A2: Iterative Refine on GSM8K [\(A2a\)](#page-15-0) and MATH500 [\(A2b\)](#page-15-0).

ing, and can apply it to test-time situations where the oracle feedback signal is not available.

## A.4.3 Differences between Critic-CoT and Long Reasoning Model

Compared with these reasoning models, our method differs in terms of training mechanism and inference method. While reasoning models attempt to improve the accuracy with longer CoT output, our Critic-CoT method introduces explicit, stepwise critique, which helps identify the error more precisely and facilitates refinement. The key distinctions are as follows:

Controllability and Efficiency It could be nontrivial to control the long reasoning models to critic and refine during inference. When to critic, critic at which step, and when to restart depends on the model itself, and they often exhibit "overthinking," performing unnecessary reflections or exploring multiple solutions even for simple problems, leading to increased computational costs without proportionate gains [\(Chen et al.,](#page-8-11) [2024b\)](#page-8-11). On the contrary, our method can achieve controllable testtime scaling, by specifying the number of reflection rounds for Iterative Refine, and the number of samples for Critic As Filter.

Adaptability While models like R1 [\(Guo et al.,](#page-9-16) [2025\)](#page-9-16) are trained with reinforcement learning with outcome reward and implicitly learn the critic and refine patterns, this self-reflection behavior is not guaranteed to emerge reliably across all models [\(Gandhi et al.,](#page-9-17) [2025\)](#page-9-17). Instead, our proposed framework explicitly teaches the model step-level critique and refinement, and can be easily adapted to different LLMs of various sizes.

Moreover, we believe our approach is complementary to long reasoning models. Given the limited self-critic ability of current R1-like models [\(He et al.,](#page-9-18) [2025\)](#page-9-18), our method could strengthen these models to precisely detect errors while maintaining confidence in correct steps. Reasoning models with enhanced self-critic ability could potentially reduce overthinking, boost performance for more complex tasks [\(Phan et al.,](#page-10-20) [2025\)](#page-10-20), and move toward self-improvement and scalable oversight [\(Schaul,](#page-10-21) [2024\)](#page-10-21).

## A.4.4 Comparison Between Inference Methods

The statistics of average tokens and latency per instance are shown in Table [A3](#page-16-0) and [A3.](#page-16-0) For Iterative

<span id="page-16-0"></span>

| GSM8K |      |            | MATH             |       |      |            |                  |
|-------|------|------------|------------------|-------|------|------------|------------------|
| Round | Acc. | Avg. Token | Avg. Latency (s) | Round | Acc. | Avg. Token | Avg. Latency (s) |
| 0     | 91.7 | 176.7      | 1.156            | 0     | 57.6 | 296.7      | 1.941            |
| 1     | 91.7 | 377.6      | 2.470            | 1     | 53.4 | 694.5      | 4.544            |
| 2     | 92.6 | 395.1      | 2.585            | 2     | 57.2 | 872.8      | 5.710            |
| 3     | 92.7 | 408.2      | 2.671            | 3     | 55.2 | 1003.0     | 6.562            |
| 4     | 93.0 | 418.5      | 2.738            | 4     | 57.2 | 1114.4     | 7.291            |
| 5     | 93.2 | 426.3      | 2.789            | 5     | 57.4 | 1202.0     | 7.864            |
| 6     | 93.2 | 432.6      | 2.830            | 6     | 57.6 | 1282.7     | 8.392            |
| 7     | 93.3 | 436.8      | 2.858            | 7     | 57.8 | 1343.1     | 8.787            |
| 8     | 93.3 | 440.4      | 2.881            | 8     | 57.8 | 1390.6     | 9.098            |

Table A3: Inference cost of Iterative Refine on GSM8K and MATH500.

| GSM8K  |      |            | MATH             |        |      |            |                  |
|--------|------|------------|------------------|--------|------|------------|------------------|
| Sample | Acc. | Avg. Token | Avg. Latency (s) | Sample | Acc. | Avg. Token | Avg. Latency (s) |
| 1      | 91.7 | 176.7      | 1.156            | 1      | 57.6 | 296.7      | 1.941            |
| 8      | 93.7 | 2974.6     | 2.433            | 8      | 61.0 | 4446.33    | 3.636            |
| 16     | 94.2 | 6261.6     | 5.121            | 16     | 63.4 | 9198.43    | 7.523            |
| 32     | 94.5 | 12524.1    | 10.242           | 32     | 64.8 | 19228.69   | 15.726           |
| 64     | 95.0 | 25057.9    | 20.493           | 64     | 66.2 | 41709.00   | 34.110           |
| 96     | 95.4 | 37574.6    | 30.729           | 96     | 66.6 | 60907.41   | 49.811           |

Table A4: Inference cost of Critic As Filter on GSM8K and MATH500.

Refinement, as the number of rounds increases, the computation cost and latency slowly increase, but the performance gain gradually becomes saturated. The reason for non-linear computation increase is that, refinement only occurs if the critique detects that the attempt is wrong and stops if the critique validates it. Yet, the pipeline of iterative refinement could be more sensitive to error accumulation, which could limit performance.

For Critic As Filter, the computation cost and latency increase linearly as the number of samples increases, and the performance also improves steadily. The linear cost increase is because we need to sample the attempt first, then perform CoT critic for each step. To reduce latency, we can parallelize the inference, and in our setting, we use 32 GPUs for inference, which deploys 8 models in total.

As the results in Table [1](#page-4-1) shows, the performance of majority vote and Critic As Filter surpass Iterative Refinement. We believe it's due to the intrinsic challenges of refinement and the relatively limited search space.

On the one hand, for Iterative Refinement to work properly, it requires the model to 1) Detect er-

rors on an attempt; 2) Refine the mistakes; 3) Exit if no further errors are detected. This pipeline could be more sensitive to error accumulation. Moreover, it only edits on a single example and has a limited retry, which is sample-efficient, but may not explore the solution space more actively, as majority vote does. Specifically on the dataset of GSM8K, the invocation statistics are as follows:

- Majority vote: 1319 \* 96 = 126,624
- Iterative Refinement: among 1319 test cases, our Critic-CoT model predicts 274 problematic instances and iterates 1627 times (on average 5.94 rounds for each wrong case), which makes in total 1319 \* 2 + 1627 \* 2 = 5892 invocations, which is 21.5 times fewer than Majority Vote calls.

On the other hand, majority vote is a strong baseline, as it requires massive sampling. It leverages diverse reasoning paths and tries to mitigate the stochastic of a single sample. But under the method of Critic As Filter, we actively filter out problematic attempts and perform the majority vote on the more reasonable candidates, rather than equally account for all the predicted answers as the vanilla

majority vote does, which further increases performance. This in turn demonstrates our model's strong ability to critique.

## A.4.5 Self-Reflection

Besides the main results, through out-of-domain evaluation in Table [2,](#page-5-2) we find our model demonstrates generalized ability to critique and refine. While the ability of LLMs to self-reflect still remains an open question, and we hope our work as a valuable exploration could shed light on future studies in this area.

Moreover, as long as we adequately improve the models' ability to critique, we could achieve test-time performance increase in the form of "selfreflection". As the experiment results present, after Critic-CoT training, the ability to critique and generate both improves, though they are not exactly identical. Notably, the critique ability can surpass the task-solving ability, allowing the model to detect errors even when it has a low probability of generating a valid solution, as prior works [\(Saun](#page-10-4)[ders et al.,](#page-10-4) [2022;](#page-10-4) [Lin et al.,](#page-9-19) [2024\)](#page-9-19) also suggest. This indicates that by strengthening the model's CoT critique ability beyond its generation capability, we can leverage this discriminative power to reject imperfect responses and achieve positive performance gains.

## A.4.6 Process Correctness of Correct Answer Attempt

We each sample 100 correct answer solutions, on GSM8K by GPT-3.5-Turbo and GPT-4-Turbo, and MATH by GPT-4-Turbo, and manually check if all intermediate steps are correct. The results are demonstrated in Table [A6.](#page-18-1) We find that in general, the correct final answer is a good indicator of correct intermediate steps. Also, from GSM8K to MATH, as the reasoning traces become longer and more complicated, the percentage of correct answer but with wrong intermediate steps increases.

## A.4.7 Alternatives of Leveraging Proprietary Models for Data Construction

To mitigate the data bias from GPT-4, we can introduce other open-source LLMs like DeepSeek-V3 or Qwen2.5-Max to perform multi-agent debates [\(Chan et al.,](#page-8-12) [2024;](#page-8-12) [Liang et al.,](#page-9-20) [2024\)](#page-9-20). This could encourage diverse thinking trajectories and overcome the inherited bias from a single model.

To reduce computation costs, we may substitute with smaller models. While our weak supervision method can effectively filter out problematic critic, to maintain a high success rate of generating valid data for smaller models, we can apply iterative refinement with more rounds, Monte Carlo Tree Search that more efficiently explores the search space, and other techniques. This can facilitate smaller models to produce desirable critic-refine data that is comparable with larger models.

## A.5 Examples of Refinement

As presented in Figure [A3,](#page-19-0) in an example of GSM8K, the model forgot to add one year at Step 3; then, through CoT critique, the model found that while Step 1 and Step 2 are correct, Step 3 contains this ignorance error. Finally, guided by the critique of Step 3, the model made a correction and reached the gold answer of 13. Similarly, in an example of MATH [\(A4\)](#page-20-0), the model identified and successfully fixed the error.

## <span id="page-17-0"></span>A.6 Prompts

Table [A7,](#page-21-0) Table [A10,](#page-23-0) and Table [A8](#page-22-0) presents the prompt for critic-refine data collection using GPT4- Turbo, with Table [A9](#page-22-1) for removing the hint phrases (Section [3.2\)](#page-3-4). Table [A11,](#page-23-1) Table [A12,](#page-24-0) and Table [A13](#page-24-1) shows the prompt of trained model for solving, critique, and refinement during stage-2-training (Section [3.2\)](#page-3-4) and inference (Section [3.3\)](#page-3-1). Table [A14,](#page-31-0) Table [A15](#page-32-0) and Table [A16](#page-34-0) present the prompts and responses of a single-turn critique-refinement, under Critic-CoT, Step-wise Label Critic and Final Label Critic respectively. Table [A17](#page-38-0) presents a single-turn critique-refinement on HumanEval.

```
import re
def extract_boxed_expressions_custom(text):
  stack = []
  current_expr = ""
  i = 0
  while i < len(text):
    if text[i:i+7] == r"\boxed{":
        if stack:
            current_expr += text[i]
        stack.append("{")
        i += 7
    elif text[i] == "{" and stack:
        stack.append("{")
        current_expr += text[i]
        i += 1
    elif text[i] == "}" and stack:
        stack.pop()
        if stack:
            current_expr += text[i]
        else:
            current_expr = re.split('=', current_expr)[-1]
            return current_expr
        i += 1
    elif stack:
        current_expr += text[i]
        i += 1
    else:
        i += 1
  return "
def extract_answer(text):
  predict_answer_span = re.findall(r'(\boxed{.*})', text, re.DOTALL)[-1]
  predict_answer = extract_boxed_expressions_custom(predict_answer_span)
  return predict_answer
```
Table A5: Python code for extracting the boxed answer.

<span id="page-18-1"></span>

| Data  | Model         | Intermediate Accuracy of Correct Answer Attempt |
|-------|---------------|-------------------------------------------------|
| GSM8K | GPT-3.5-Turbo | 97%                                             |
| GSM8K | GPT-4-Turbo   | 99%                                             |
| MATH  | GPT-4-Turbo   | 93%                                             |

Table A6: Human Evaluation on the Intermediate Steps of Attempts with Correct Answer

<span id="page-19-0"></span>

| Question:<br>Carlos is planting a lemon tree. The tree will cost \$90 to plant. Each year it will grow 7 lemons, which he can sell for<br>\$1.5 each. It costs \$3 a year to water and feed the tree. How many years will it take before he starts earning money on<br>the lemon tree?                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Model Attempt:<br>Step 1: Calculate the annual income from selling lemons. This is done by multiplying the number of lemons grown per<br>year (7) by the price per lemon (\$1.5). So, 7 * \$1.5 = \$10.50.<br>Step 2: Subtract the annual cost of watering and feeding the tree (\$3) from the annual income from selling lemons<br>(\$10.50). So, \$10.50 - \$3 = \$7.50. This is the net income per year after expenses.<br>Step 3: Determine when Carlos will start earning money back. This is done by dividing the initial cost of planting the<br>tree (\$90) by the net income per year (\$7.50). So, \$90 / \$7.50 = 12 years.<br>Therefore, it will take Carlos 12 years before he starts earning money on the lemon tree. |
| Model Critique:<br>Step 1: The attempt calculates the annual income from selling lemons by multiplying the number of lemons grown per<br>year (7) by the price per lemon (\$1.5), resulting in \$10.50.<br>Conclusion: Step 1 is correct.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Step 2:<br>The attempt subtracts the annual cost of watering and feeding the tree (\$3) from the annual income<br>from selling lemons (\$10.50), resulting in a net income per year of \$7.50.<br>Conclusion: Step 2 is correct.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| Step 3:<br>The attempt divides the initial cost of planting the tree (\$90) by the net income per year (\$7.50),<br>resulting in 12 years. However, this calculation does not account for the fact that Carlos will start earning money back<br>in the first year, even though he won't break even until the 13th year.<br>Conclusion: Step 3 is incorrect.                                                                                                                                                                                                                                                                                                                                                                         |
| Model Refinement:<br>Step 3 (Corrected): Determine when Carlos will start earning money back. This is done by dividing the initial cost of<br>planting the tree (\$90) by the net income per year (\$7.50). So, \$90 / \$7.50 = 12 years.<br>However, since Carlos will start earning money back in the first year, we need to add one more year to this calculation.<br>Therefore, it will take Carlos 13 years before he starts earning money on the lemon tree.                                                                                                                                                                                                                                                                  |

Figure A3: Criticize and refine a problem in the GSM8K test set.

<span id="page-20-0"></span>

| Question:<br>What is the smallest positive perfect cube that can be written as the sum of three consecutive integers?                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Model Attempt:<br>Step 1: Let the three consecutive integers be x − 1, x, and x + 1. The sum of these three integers is 3x.<br>3 = 3x.<br>Step 2: Since we are looking for a perfect cube, let's express 3x as a cube of some integer n, where n<br>3 must be divisible by 3, and<br>Step 3: To find the smallest such n, we need to minimize x.<br>However, since n<br>x is an<br>integer, n itself must also be divisible by 3.<br>3 = 216.<br>Step 4: The smallest integer n that is divisible by 3 and gives us a perfect cube when cubed is n = 6, because 6<br>3 = 3x, we get<br>Step 5: Substituting n = 6 into n<br>216 = 3x, which simplifies to x = 72.<br>Step 6: Therefore, the smallest positive perfect cube that can be written as the sum of three consecutive integers is<br>216 . |
| Model Critique:<br>Step 1: Let the three consecutive integers be x − 1, x, and x + 1. The sum of these three integers is indeed 3x.<br>Conclusion: Step 1 is correct.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 3<br>Step 2:<br>Expressing 3x as a cube of some integer n, where n<br>= 3x, correctly sets up the equation needed<br>to solve the problem. This step accurately translates the problem statement into a mathematical expression.<br>Conclusion: Step 2 is correct.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| 3 must be divisible by 3 is a misunderstanding.<br>Step 3:<br>The claim that n must be divisible by 3 because n<br>3<br>3 will<br>In reality, n<br>being divisible by 3 does not imply that n itself must be divisible by 3; rather, it simply means that n<br>always be divisible by 3 regardless of whether n is divisible by 3. This step introduces an unnecessary restriction on n.<br>Conclusion: Step 3 is incorrect.                                                                                                                                                                                                                                                                                                                                                                        |
| Model Refinement:<br>Step 3 (Corrected): Since we are looking for the smallest positive perfect cube that can be expressed as 3x, we should<br>start by identifying the smallest perfect cubes and checking if any of them can be represented in this form.<br>3 = 1,<br>3 = 8,<br>3 = 27,<br>3 = 64,<br>3 = 125,<br>3 = 216, and so on. Among<br>Step 4: The smallest perfect cubes are 1<br>2<br>3<br>4<br>5<br>6<br>these, 27 is the first number that can be expressed as 3x, where x is an integer (x = 9).<br>Step 5: Therefore, the smallest positive perfect cube that can be written as the sum of three consecutive integers is 27 .                                                                                                                                                      |

Figure A4: Criticize and refine a problem in the MATH test set. In the attempt, the model made a hallucination in Step 3, then through stepwise CoT critique, the model detected this error, and accordingly refined the solution starting from Step 3 successfully.

<span id="page-21-0"></span>How do you evaluate the following attempt with respect to the problem?

<problem> {problem} </problem>

<attempt> {attempt} </attempt>

—–

\*\*Notes\*\*:

- Please think step by step.

- Your reasoning should precede any claims or conclusions you make to avoid unwarranted assertions.

- At the end of the evaluation for each step, YOU MUST articulate the conclusion using the format "Conclusion: Step [i] is correct" or "Conclusion: Step [i] is incorrect". Words like "partially correct" are prohibited.

- You shall not evaluate multiple steps at a time, so words like "Step 7 to Step 24:" or "Step 4 through 6" are forbidden.

- Once a mistake is identified and stated, stop the evaluation, and enumerate the corrected steps starting from the step where the mistake was detected, and label this part of your response with <correction> at the start and </correction> at the end. Also, the final answer should be a single number, in the form \boxed{}, at the final step.

Table A7: The prompt for the collection of critique and refinement on GSM8K, using GPT4-Turbo.

<span id="page-22-0"></span>How do you evaluate the following attempt with respect to the problem, with the help of reference solution?

Hint: There could be a mistake.

<problem> {problem} </problem>

<reference\_solution> {reference\_solution} </reference\_solution>

<attempt> {attempt} </attempt>

—–

\*\*Notes\*\*:

- Please think step by step.

- Your reasoning should precede any claims or conclusions you make to avoid unwarranted assertions.

- Please ensure that the output text does not include phrases implying the use of a reference solution or hint, even though these resources are being utilized.

- At the end of the evaluation for each step, YOU MUST articulate the conclusion using the format "Conclusion: Step [i] is correct" or "Conclusion: Step [i] is incorrect". Words like "partially correct" are prohibited.

- You shall not evaluate multiple steps at a time, so words like "Step 7 to Step 24:" or "Step 4 through 6" are forbidden.

- Once a mistake is identified and stated, stop the evaluation, and enumerate the corrected steps starting from the step where the mistake was detected, and label this part of your response with <correction> at the start and </correction> at the end. Also, the final answer should be in the form \boxed{}, at the final step.

Table A8: The prompt for the collection of critique and refinement on MATH incorrect attempt, using GPT4-Turbo.

### <span id="page-22-1"></span>Prompt

For the following text, remove any phrases like "reference solution" or "hint", and keep all the other content. Do not miss the "<correction>" and "</correction>" labels that exist in the text. Do not respond to anything else.

—–

{critique\_refinement}

Table A9: The prompt for removing the hint of critique and refinement on MATH, using GPT4-Turbo.

<span id="page-23-0"></span>How do you evaluate the following attempt with respect to the problem? Hint: All the steps are correct, and the attempt reached a correct answer.

<problem> {problem} </problem>

<attempt> {attempt} </attempt>

—–

\*\*Notes\*\*:

- Please think step by step.

- Your reasoning should precede any claims or conclusions you make to avoid unwarranted assertions.

- Please ensure that the output text does not include phrases implying the use of a reference solution or hint, even though these resources are being utilized.

- At the end of the evaluation for each step, YOU MUST articulate the conclusion using the format "Conclusion: Step [i] is correct" or "Conclusion: Step [i] is incorrect". Words like "partially correct" are prohibited.

- You shall not evaluate multiple steps at a time, so words like "Step 7 to Step 24:" or "Step 4 through 6" are forbidden.

- Once a mistake is identified and stated, stop the evaluation, and enumerate the corrected steps starting from the step where the mistake was detected, and label this part of your response with <correction> at the start and </correction> at the end. Also, the final answer should be in the form \boxed{}, at the final step.

Table A10: The prompt for the collection of critique on MATH correct attempt, using GPT4-Turbo.

## <span id="page-23-1"></span>Prompt

## Problem {problem}

—–

Solve the problem step by step, marking each step as "Step [i]:". Your final answer should be in the form \boxed{answer}, at the end of your response.

Table A11: The prompt for solution sampling.

<span id="page-24-0"></span>How do you evaluate the following attempt with respect to the problem?

<problem> {problem} </problem>

<attempt> {attempt} </attempt>

—–

\*\*Notes\*\*:

- Please think step by step.

- Your reasoning should precede any claims or conclusions you make to avoid unwarranted assertions. - At the end of the evaluation for each step, YOU MUST articulate the conclusion using the format "Conclusion: Step [i] is correct" or "Conclusion: Step [i] is incorrect". Words like "partially correct" are prohibited.

Table A12: The prompt for critique.

## <span id="page-24-1"></span>Prompt

How do you refine the following attempt with respect to the problem, given the criticism?

<problem> {problem} </problem>

<attempt> {attempt} </attempt>

<criticism> {wrong\_step\_criticism} </criticism>

![](./assets/critic-cot/_page_24_Figure_14.jpeg)

### Prompt of Critique under Critic-CoT

How do you evaluate the following attempt with respect to the problem?

<problem>

Consider the geometric sequence <sup>125</sup> 9 , 25 3 , 5, 3, . . .. What is the eighth term of the sequence? Express your answer as a common fraction.

</problem>

<attempt> Step 1: Identify the first term of the sequence. The first term a<sup>1</sup> is:

$$
a_1 = \frac{125}{9}
$$

Step 2: Calculate the common ratio r.

The common ratio r can be found by dividing the second term a<sup>2</sup> by the first term a1:

$$
r = \frac{a_2}{a_1} = \frac{\frac{25}{3}}{\frac{125}{9}} = \frac{25}{3} \times \frac{9}{125}
$$

Calculating the right-hand side:

$$
=\frac{25\cdot 9}{3\cdot 125}=\frac{225}{375}
$$

Now simplify <sup>225</sup> <sup>375</sup> :

$$
=\frac{225 \div 75}{375 \div 75}=\frac{3}{5}
$$

Thus, the common ratio is:

$$
r = \frac{3}{5}
$$

Step 3: Use the formula for the n-th term of a geometric sequence. The n-th term of a geometric sequence can be calculated using the formula:

$$
a_n = a_1 \cdot r^{n-1}
$$

Step 4: Calculate the eighth term a8. Substituting n = 8 into the formula:

$$
a_8 = a_1 \cdot r^{8-1} = \frac{125}{9} \cdot \left(\frac{3}{5}\right)^7
$$

Step 5: Calculate 3 5 7 . Calculating 3 5 7 :

$$
\left(\frac{3}{5}\right)^7 = \frac{3^7}{5^7} = \frac{2187}{78125}
$$

Step 6: Substitute back into the expression for a8. Now we compute:

$$
a_8 = \frac{125}{9} \cdot \frac{2187}{78125}
$$

Step 7: Multiply the fractions.

Prompt of Critique under Critic-CoT

To multiply:

|                              | 125<br>·<br>2187<br>a8<br>=<br>9<br>·<br>78125 |
|------------------------------|------------------------------------------------|
| Calculating the denominator: | ·<br>9<br>78125 = 703125                       |
| Calculating the numerator:   | 125<br>·<br>2187 = 273375                      |
| Thus:                        | 273375<br>a8<br>=<br>703125                    |

Step 8: Simplify the fraction <sup>273375</sup> <sup>703125</sup> .

To simplify: First, calculate the GCD of the numerator and denominator. We can find that both 273375 and 703125 are divisible by 135.

Calculating:

| 273375<br>÷<br>135 |   | 2025 |
|--------------------|---|------|
| ÷<br>703125<br>135 | = | 5205 |

Continuing to simplify, both 2025 and 5205 are divisible by 15:

$$
\frac{2025 \div 15}{5205 \div 15} = \frac{135}{347}
$$

This is now fully simplified because 135 and 347 have no common factors. Final Answer:

Thus, the eighth term of the sequence is:

| 135 |
|-----|
| 347 |

</attempt>

—–

\*\*Notes\*\*:

- Please think step by step.

- Your reasoning should precede any claims or conclusions you make to avoid unwarranted assertions.

- At the end of the evaluation for each step, YOU MUST articulate the conclusion using the format "Conclusion: Step [i] is correct" or "Conclusion: Step [i] is incorrect". Words like "partially correct" are prohibited.

### Response of Critique under Critic-CoT

Step 1: The first term a<sup>1</sup> = 125 9 is identified correctly. Conclusion: Step 1 is correct.

Step 2: The common ratio r is calculated as:

$$
r = \frac{a_2}{a_1} = \frac{\frac{25}{3}}{\frac{125}{9}} = \frac{25}{3} \times \frac{9}{125} = \frac{225}{375} = \frac{3}{5}
$$

This calculation is correct.

Conclusion: Step 2 is correct.

### Response of Critique under Critic-CoT

Step 3: The formula for the n-th term is correctly stated as:

a<sup>n</sup> = a<sup>1</sup> · r n−1

Conclusion: Step 3 is correct. Step 4: The eighth term is computed as:

$$
a_8 = \frac{125}{9} \cdot \left(\frac{3}{5}\right)^7
$$

This is correct. Conclusion: Step 4 is correct. Step 5: Calculating 3 5 7 :

$$
\left(\frac{3}{5}\right)^7 = \frac{2187}{78125}
$$

This calculation is correct. Conclusion: Step 5 is correct. Step 6: Substituting back:

$$
a_8 = \frac{125}{9} \cdot \frac{2187}{78125}
$$

This is correct. Conclusion: Step 6 is correct. Step 7: Multiplying the fractions:

$$
a_8 = \frac{125 \cdot 2187}{9 \cdot 78125}
$$

The denominator calculation is correct:

$$
9 \cdot 78125 = 703125
$$

However, for the numerator:

$$
125 \cdot 2187 = 273375
$$

This is also correct.

Conclusion: Step 7 is correct.

Step 8: The goal is to simplify the fraction <sup>273375</sup> <sup>703125</sup> . The attempt made to find the GCD and simplify. To simplify the fraction, we need to find the greatest common divisor (GCD) of 273375 and 703125. The standard approach involves either prime factorization or using the Euclidean algorithm. Prime Factorization:

- 273375:

- Dividing by 5: 273375 ÷ 5 = 54675
- Dividing by 5 again: 54675 ÷ 5 = 10935
- Dividing by 5 again: 10935 ÷ 5 = 2187
- The number 2187 is 3 7 .
- Therefore, 273375 = 5<sup>3</sup> · 3 7 .
- 703125:
- Dividing by 5: 703125 ÷ 5 = 140625
- Dividing by 5 again: 140625 ÷ 5 = 28125
- Dividing by 5 again: 28125 ÷ 5 = 5625

### Response of Critique under Critic-CoT

- Dividing by 5 again: 5625 ÷ 5 = 1125
- Dividing by 5 again: 1125 ÷ 5 = 225
- Dividing by 5 again: 225 ÷ 5 = 45
- Finally, 45 = 3<sup>2</sup> · 5 1 .
- Therefore, 703125 = 5<sup>6</sup> · 3 2 .

The GCD can now be derived from the lowest powers of the common factors:

- For 5: 5 3
- For 3: 3 2

Thus, the GCD is:

5 3 · 3 2

Therefore, 273375 and 703125 are not divisible by 135. Conclusion: Step 8 is incorrect.

### Prompt of Refinement under Critic-CoT

How do you refine the following attempt with respect to the problem, given the criticism?

<problem>

Consider the geometric sequence <sup>125</sup> 9 , 25 3 , 5, 3, . . .. What is the eighth term of the sequence? Express your answer as a common fraction.

</problem>

<attempt> Step 1: Identify the first term of the sequence. The first term a<sup>1</sup> is:

$$
a_1 = \frac{125}{9}
$$

Step 2: Calculate the common ratio r.

The common ratio r can be found by dividing the second term a<sup>2</sup> by the first term a1:

$$
r = \frac{a_2}{a_1} = \frac{\frac{25}{3}}{\frac{125}{9}} = \frac{25}{3} \times \frac{9}{125}
$$

Calculating the right-hand side:

$$
=\frac{25\cdot 9}{3\cdot 125}=\frac{225}{375}
$$

Now simplify <sup>225</sup> <sup>375</sup> :

$$
=\frac{225 \div 75}{375 \div 75}=\frac{3}{5}
$$

r = 3 5

Thus, the common ratio is:

Step 3: Use the formula for the n-th term of a geometric sequence. The n-th term of a geometric sequence can be calculated using the formula:

$$
a_n = a_1 \cdot r^{n-1}
$$

### Prompt of Refinement under Critic-CoT

Step 4: Calculate the eighth term a8. Substituting n = 8 into the formula:

$$
a_8 = a_1 \cdot r^{8-1} = \frac{125}{9} \cdot \left(\frac{3}{5}\right)^7
$$

Step 5: Calculate 3 5 7 . Calculating 3 5 7 :

$$
\left(\frac{3}{5}\right)^7 = \frac{3^7}{5^7} = \frac{2187}{78125}
$$

Step 6: Substitute back into the expression for a8. Now we compute:

$$
a_8 = \frac{125}{9} \cdot \frac{2187}{78125}
$$

Step 7: Multiply the fractions. To multiply:

$$
a_8 = \frac{125 \cdot 2187}{9 \cdot 78125}
$$

Calculating the denominator:

9 · 78125 = 703125

Calculating the numerator:

$$
125 \cdot 2187 = 273375
$$

Thus:

$$
a_8 = \frac{273375}{703125}
$$

Step 8: Simplify the fraction <sup>273375</sup> <sup>703125</sup> .

To simplify: First, calculate the GCD of the numerator and denominator. We can find that both 273375 and 703125 are divisible by 135.

Calculating:

$$
\frac{273375 \div 135}{703125 \div 135} = \frac{2025}{5205}
$$

Continuing to simplify, both 2025 and 5205 are divisible by 15:

$$
\frac{2025 \div 15}{5205 \div 15} = \frac{135}{347}
$$

This is now fully simplified because 135 and 347 have no common factors. Final Answer:

Thus, the eighth term of the sequence is:

| 135 |  |
|-----|--|
| 347 |  |

</attempt>

### Prompt of Refinement under Critic-CoT

## <criticism>

Step 8: The goal is to simplify the fraction <sup>273375</sup> <sup>703125</sup> . The attempt made to find the GCD and simplify. To simplify the fraction, we need to find the greatest common divisor (GCD) of 273375 and 703125. The standard approach involves either prime factorization or using the Euclidean algorithm. Prime Factorization:

- 273375:
- Dividing by 5: 273375 ÷ 5 = 54675
- Dividing by 5 again: 54675 ÷ 5 = 10935

.

- Dividing by 5 again: 10935 ÷ 5 = 2187
- The number 2187 is 3 7
- Therefore, 273375 = 5<sup>3</sup> · 3 7 .
- 703125:
- Dividing by 5: 703125 ÷ 5 = 140625
- Dividing by 5 again: 140625 ÷ 5 = 28125
- Dividing by 5 again: 28125 ÷ 5 = 5625
- Dividing by 5 again: 5625 ÷ 5 = 1125
- Dividing by 5 again: 1125 ÷ 5 = 225

1

- Dividing by 5 again: 225 ÷ 5 = 45
- Finally, 45 = 3<sup>2</sup> · 5
- . - Therefore, 703125 = 5<sup>6</sup> · 3 2 .

The GCD can now be derived from the lowest powers of the common factors:

- For 5: 5 3

- For 3: 3 2

Thus, the GCD is:

5 3 · 3 2

Therefore, 273375 and 703125 are not divisible by 135. Conclusion: Step 8 is incorrect. </criticism>

### <span id="page-31-0"></span>Prompt of Refinement under Critic-CoT

<correction>

Step 8: Simplify <sup>273375</sup> <sup>703125</sup> . First, we divide it by 375. Calculating:

273375 ÷ 375 703125 ÷ 375 = 729 1875

Step 9: Further simplify <sup>729</sup> <sup>1875</sup> . The numerator 729 is 3 6 and the denominator 1875 is 3 · 625. The GCD is 3.

Calculating:

| 729<br>÷<br>3<br>= | 243 |
|--------------------|-----|
| 1875<br>÷<br>3     | 625 |

243 625

This fraction is fully simplified.

Final Answer: Thus, the eighth term of the sequence is:

|--|--|--|--|

Table A14: Full example of Critic-CoT. The model got the wrong common factor in Step 8, and through CoT critique, identified this mistake, then took the refinement and reached the correct answer.

### Prompt of Critique under Step-wise Label Critic

How do you evaluate the following attempt with respect to the problem?

<problem> [...] </problem> <attempt> [...]

</attempt>

—–

```
**Notes**:
```
- For each step, you only need to output "Step [i] is correct" if right, or "Step [i] is incorrect" if wrong. Do not provide anything else in your output.

## Response of Critique under Step-wise Label Critic

Step 1 is correct. Step 2 is correct. Step 3 is correct. Step 4 is correct. Step 5 is incorrect.

### <span id="page-32-0"></span>Prompt of Refinement under Step-wise Label Critic

How do you refine the following attempt with respect to the problem, given the criticism?

<problem> [...] </problem> <attempt> [...] </attempt> <criticism>

Step 5 is incorrect. </criticism>

### Response of Refinement under Step-wise Label Critic

<correction>

Step 5: Calculate 3 5 7 .

$$
\left(\frac{3}{5}\right)^7 = \frac{3^7}{5^7} = \frac{2187}{78125}
$$
 (correct)

Step 6: Substitute back into the expression for a8.

$$
a_8=\frac{125}{9}\cdot\frac{2187}{78125}
$$

Step 7: Multiply the fractions. Calculating the numerator:

$$
125 \cdot 2187 = 273375 \text{ (correct)}
$$

Calculating the denominator:

$$
9 \cdot 78125 = 703125 \text{ (correct)}
$$

Step 8: Simplify the fraction <sup>273375</sup> <sup>703125</sup> . To simplify: Calculating the GCD shows that both 273375 and 703125 are divisible by 675, so:

$$
\frac{273375 \div 675}{703125 \div 675} = \frac{405}{1045}
$$

Continuing to simplify, both 405 and 1045 are divisible by 5:

$$
\frac{405 \div 5}{1045 \div 5} = \frac{81}{209}
$$

Thus, the final answer is:

| 81  |
|-----|
| 209 |

</correction>

Table A15: Full example of Step-wise Label Critic. The problem and the attempt are the same in Table [A14,](#page-31-0) so we skip them. Without CoT critique, the model incorrectly believed that Step 5 is wrong, then made the refinement starting from Step 5, which is unsuccessful.

### Prompt of Critique under Outcome Label Critic

How do you evaluate the following attempt with respect to the problem?

```
<problem>
[...]
</problem>
<attempt>
[...]
</attempt>
```
—–

\*\*Notes\*\*:

- For the whole attempt, you only need to output "Each step from Step 1 to Step 8 is correct." if right, or "Some step from Step 1 to Step 8 is incorrect" if wrong. Do not provide anything else in your output.

Response of Critique under Outcome Label Critic

Some step from Step 1 to Step 8 is incorrect.

### Prompt of Refinement under Outcome Label Critic

How do you refine the following attempt with respect to the problem, given the criticism?

<problem> [...] </problem> <attempt> [...] </attempt>

<criticism> Some step from Step 1 to Step 8 is incorrect. </criticism>

### Response of Refinement under Outcome Label Critic

<correction> Step 1: Identify the first term of the sequence. The first term a<sup>1</sup> is:

$$
a_1=\frac{125}{9}
$$

Step 2: Calculate the common ratio r.

The common ratio r can be found by dividing the second term a<sup>2</sup> by the first term a1:

$$
r = \frac{a_2}{a_1} = \frac{\frac{25}{3}}{\frac{125}{9}} = \frac{25}{3} \times \frac{9}{125} = \frac{225}{375}
$$

Now simplify <sup>225</sup> <sup>375</sup> :

$$
=\frac{225 \div 75}{375 \div 75}=\frac{3}{5}
$$

### <span id="page-34-0"></span>Response of Refinement under Outcome Label Critic

Thus, the common ratio is:

$$
r = \frac{3}{5}
$$

Step 3: Use the formula for the n-th term of a geometric sequence. The n-th term of a geometric sequence can be calculated using the formula:

$$
a_n = a_1 \cdot r^{n-1}
$$

Step 4: Calculate the eighth term a8. Substituting n = 8 into the formula:

$$
a_8 = a_1 \cdot r^{8-1} = \frac{125}{9} \cdot \left(\frac{3}{5}\right)^7
$$

Step 5: Calculate 3 5 7 . Calculating 3 5 7 :

$$
\left(\frac{3}{5}\right)^7 = \frac{3^7}{5^7} = \frac{2187}{78125}
$$

Step 6: Substitute back into the expression for a8. Now we compute:

$$
a_8 = \frac{125}{9} \cdot \frac{2187}{78125}
$$

Step 7: Multiply the fractions. To multiply:

$$
a_8 = \frac{125 \cdot 2187}{9 \cdot 78125}
$$
  
Calculating the denominator:  

$$
9 \cdot 78125 = 703125
$$
  
Calculating the numerator:  

$$
125 \cdot 2187 = 273375
$$

Thus:

$$
a_8 = \frac{273375}{703125}
$$

Step 8: Simplify the fraction <sup>273375</sup> <sup>703125</sup> . To simplify: Finding the GCD, both 273375 and 703125 are divisible by 675:

$$
\frac{273375 \div 675}{703125 \div 675} = \frac{405}{1042}
$$

Now we check if <sup>405</sup> <sup>1042</sup> can be simplified further. Both numbers do not have common factors. Final Answer:

Thus, the eighth term of the sequence is:

| 405  |
|------|
| 1042 |

### </correction>

Table A16: Full example of Final Label Critic. The problem and the attempt are also the same in Table [A14.](#page-31-0) With only the outcome label, the model managed to detect the attempt was incorrect, then made the refinement starting from the first step, which was unsuccessful.

### Prompt of Code Generation on HumanEval

## Python code problem

```
def s p l i t _ w o r d s ( t x t ) :
      ' ' '
      Given a s t r i n g o f words , r e t u r n a l i s t o f words s p l i t on
      w h i t e s p a c e , i f no w h i t e s p a c e s e x i s t s i n t h e t e x t you
      s h o u l d s p l i t on commas ' , ' i f no commas e x i s t s you s h o u l d
      r e t u r n t h e number o f lower −ca se l e t t e r s w i t h odd o r d e r i n t h e
      a l p h a b e t , ord ( ' a ' ) = 0 , ord ( ' b ' ) = 1 , . . . ord ( ' z ' ) = 25
      Examples
      s p l i t _ w o r d s ( " H e l l o world ! " ) −> [ " H e l l o " , " world ! " ]
      s p l i t _ w o r d s ( " Hello , world ! " ) −> [ " H e l l o " , " world ! " ]
      s p l i t _ w o r d s ( " a b c d e f " ) == 3
      ' ' '
```
Before writing the code, think step by step, marking each step as "Step [i]:" Your final function split\_words should be in the form ```python\n[code]\n```, at the end of your response.

### Response of Code Generation on HumanEval

Step 1: Create a function named `split\_words` that takes a string `txt` as an input.

Step 2: Check if there are any whitespace characters in the string. If there are, split the string into words using the 'split()' function with the default separator (whitespace).

Step 3: If there are no whitespace characters, check if there are any commas in the string. If there are, split the string into words using the 'split()' function with the comma as the separator.

Step 4: If there are neither whitespace characters nor commas in the string, iterate over the characters in the string, keeping track of the count of lowercase letters with odd alphabetical order (based on their ASCII value modulo 2).

Step 5: Return the result based on the conditions met in steps 2, 3, or 4.

Here is the Python code for the function:

```python

—–

```
def s p l i t _ w o r d s ( t x t ) :
      i f ' ' in t x t :
            return t x t . s p l i t ( )
      e l i f ' , ' in t x t :
            return t x t . s p l i t ( ' , ' )
      e l s e :
            c o u n t = sum(1 f o r c h a r in t x t i f c h a r . i s l o w e r ( ) and
            ord ( c h a r ) % 2 != 0)
            return c o u n t
```
```

This function first checks for whitespace characters, then for commas, and finally counts the lowercase letters with odd alphabetical order if neither of the first two conditions is met.

### Prompt of Critique on HumanEval

How do you evaluate the following attempt with respect to the problem? <problem>

```
def s p l i t _ w o r d s ( t x t ) :
      ' ' '
      Given a s t r i n g o f words , r e t u r n a l i s t o f words s p l i t on
      w h i t e s p a c e , i f no w h i t e s p a c e s e x i s t s i n t h e t e x t you
      s h o u l d s p l i t on commas ' , ' i f no commas e x i s t s you s h o u l d
      r e t u r n t h e number o f lower −ca se l e t t e r s w i t h odd o r d e r i n t h e
      a l p h a b e t , ord ( ' a ' ) = 0 , ord ( ' b ' ) = 1 , . . . ord ( ' z ' ) = 25
      Examples
      s p l i t _ w o r d s ( " H e l l o world ! " ) −> [ " H e l l o " , " world ! " ]
      s p l i t _ w o r d s ( " Hello , world ! " ) −> [ " H e l l o " , " world ! " ]
      s p l i t _ w o r d s ( " a b c d e f " ) == 3
      ' ' '
```
</problem>

<attempt>

Step 1: Create a function named `split\_words` that takes a string `txt` as an input.

Step 2: Check if there are any whitespace characters in the string. If there are, split the string into words using the 'split()' function with the default separator (whitespace).

Step 3: If there are no whitespace characters, check if there are any commas in the string. If there are, split the string into words using the 'split()' function with the comma as the separator.

Step 4: If there are neither whitespace characters nor commas in the string, iterate over the characters in the string, keeping track of the count of lowercase letters with odd alphabetical order (based on their ASCII value modulo 2).

Step 5: Return the result based on the conditions met in steps 2, 3, or 4.

Here is the Python code for the function:

```python

```
def s p l i t _ w o r d s ( t x t ) :
Line 1 : i f ' ' in t x t :
Line 2 : return t x t . s p l i t ( )
Line 3 : e l i f ' , ' in t x t :
Line 4 : return t x t . s p l i t ( ' , ' )
Line 5 : e l s e :
Line 6 : c o u n t = sum(1 f o r c h a r in t x t i f c h a r . i s l o w e r ( ) and
                   ord ( c h a r ) % 2 != 0)
Line 7 : return c o u n t
```

```
```
```
This function first checks for whitespace characters, then for commas, and finally counts the lowercase letters with odd alphabetical order if neither of the first two conditions is met. </attempt>

## Response of Critique on HumanEval

Step 1: Define a function called `split\_words` that takes a string `txt` as its parameter. Conclusion: Step 1 is correct.

Step 2: Verify if there are any whitespace characters in the string. If they exist, divide the string into words using the `split()` function with the default separator (whitespace).

Conclusion: Step 2 is correct.

Step 3: If no whitespace characters are found, check for commas in the string. If commas are present, split the string into words using the `split()` function with the comma as the separator. Conclusion: Step 3 is correct.

Step 4: Otherwise, loop through the characters in the string, counting the number of lowercase letters that have an odd alphabetical order (based on their ASCII value modulo 2). The mistake in Step 4 lies in the interpretation of "odd alphabetical order." The problem statement refers to the alphabetical order of lowercase letters in the alphabet, not their ASCII values. The correct approach is to count the lowercase letters whose alphabetical order (where 'a' is 0, 'b' is 1, ..., 'z' is 25) is odd. Conclusion: Step 4 is incorrect.

## Prompt of Refinement on HumanEval

How do you refine the following attempt with respect to the problem, given the criticism? You shall write another complete Python function, in the format ```python\n[code]\n```. <problem>

[...] </problem>

<attempt> [...] </attempt>

# <criticism>

Step 4: Otherwise, loop through the characters in the string, counting the number of lowercase letters that have an odd alphabetical order (based on their ASCII value modulo 2). The mistake in Step 4 lies in the interpretation of "odd alphabetical order." The problem statement refers to the alphabetical order of lowercase letters in the alphabet, not their ASCII values. The correct approach is to count the lowercase letters whose alphabetical order (where 'a' is 0, 'b' is 1, ..., 'z' is 25) is odd. Conclusion: Step 4 is incorrect.

</criticism>

### <span id="page-38-0"></span>Response of Refinement on HumanEval

```
<correction>
Here is the corrected Python function:
```python
def s p l i t _ w o r d s ( t x t ) :
      i f ' ' in t x t :
             return t x t . s p l i t ( )
      e l i f ' , ' in t x t :
             return t x t . s p l i t ( ' , ' )
      e l s e :
             c o u n t = sum(1 f o r c h a r in t x t i f c h a r . i s l o w e r ( )
            and ( ord ( c h a r ) − ord ( ' a ' ) ) % 2 != 0)
             return c o u n t
```
```
This function correctly counts the lowercase letters with odd alphabetical order by subtracting the ASCII value of 'a' from the ASCII value of each lowercase letter to get its alphabetical order, and then checking if this order is odd. If the order is odd, it increments the count. </correction>

Table A17: Full example of a single-turn refinement on HumanEval. The attempt made mistakes in Step 4 and Line 6, which use the ASCII value directly rather than subtract the value of 'a'. The critique detect this error, and made a successul refinement.