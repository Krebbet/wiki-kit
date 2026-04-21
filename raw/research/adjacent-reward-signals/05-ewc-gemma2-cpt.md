---
url: "https://arxiv.org/pdf/2505.05946"
title: "FULL-PARAMETER CONTINUAL PRETRAINING OF GEMMA2: INSIGHTS INTO FLUENCY AND DOMAIN KNOWLEDGE"
captured_on: "2026-04-20"
capture_method: "pdf"
engine: "marker"
assets_dir: "./assets/ewc-gemma2-cpt"
---

# FULL-PARAMETER CONTINUAL PRETRAINING OF GEMMA2: INSIGHTS INTO FLUENCY AND DOMAIN KNOWLEDGE

A PREPRINT

Vytenis Šliogeris [,](https://orcid.org/0000-0002-0943-9357) Povilas Daniušis [,](https://orcid.org/0000-0001-5977-827X) and Arturas Nakvosa[s](https://orcid.org/0009-0007-7391-5454) ¯

Neurotechnology, Laisves pr. 125A, LT-06118, Vilnius, Lithuania ˙ ∗

May 2025

## ABSTRACT

In this technical report, we empirically investigate the relationship between linguistic fluency and domain knowledge in the context of continual learning with large language models (LLMs). Specifically, we enhance the linguistic fluency of the Gemma2 LLM for the Lithuanian language by autoregressively pretraining its full parameter set on the first 10% of the Lithuanian language component of the CulturaX dataset. To prevent catastrophic forgetting of the model's existing domain knowledge, we apply Elastic Weight Consolidation (EWC), leveraging Fisher information estimated using data from the Massive Multitask Language Understanding (MMLU) benchmark. In the posttraining evaluations, we assess linguistic fluency through perplexity and evaluate domain knowledge using accuracy on a suite of language understanding benchmarks, including ARC-Easy, Belebele, GSM8K, HellaSwag, MMLU, TruthfulQA, and Winogrande, in both English and Lithuanian. The empirical results demonstrate that EWC not only mitigates catastrophic forgetting by preserving the model's performance in terms of both linguistic fluency and domain knowledge but also improves or maintains these capabilities for the newly added Lithuanian language. These findings highlight the potential for more efficient adaptation of general-purpose LLMs to under-represented languages without requiring access to the original training data. The accompanying codebase is openly accessible at: [https://github.com/Neurotechnology/LLM\\_EWC](https://github.com/Neurotechnology/LLM_EWC).

*Keywords* Continual learning · elastic weight consolidation · LLM · Lithuanian language · linguistic fluency · domain knowledge

## 1 Introduction

LLMs, based on Transformers [\[1\]](#page-5-0) and other neural architectures, are remarkably efficient knowledge models. However, as with most neural networks, learning a new task often reduces the performance of the model on the previously learned tasks. This undesirable effect is known as *catastrophic forgetting*. The field of mitigating catastrophic forgetting is called continual learning (CL). Specifically, it is a study of algorithms and models that can cope with a learning scenario in which new tasks should be learned, without losing performance on previously learned tasks. Formally, a model is usually represented by some parametrised function *f<sup>θ</sup>* (e.g., neural network), with parameters *θ*. Given a sequence of tasks T1*, ...,* T*<sup>n</sup>* represented with data sets D1*, ...,* D*n*, which arrive over time, this model should be able to learn a new task T*<sup>i</sup>* from D*<sup>i</sup>* , without access to previous D*<sup>j</sup>* (*j < i*), simultaneously maintaining performance on all previously learned tasks T*<sup>j</sup>* (where *j < i*).

The intersection of CL and LLMs is a nascent field, giving rise to questions regarding different types of knowledge. Several knowledge ontologies have been proposed. For example, a survey [\[2\]](#page-5-1) outlines factual knowledge, domain knowledge, language knowledge, and preference knowledge, and [\[3\]](#page-5-2) discusses different ontologies of knowledge, pairing them with different CL methods to improve the particular type of knowledge. In this work, we outline two

<sup>∗</sup>Neurotechnology <http://www.neurotechnology.com> is a Lithuanian company, specialising in artificial intelligence, biometrics, computer vision, and deep neural networks.

types of knowledge: the knowledge of language fluency and domain knowledge. Language fluency denotes the ability to produce grammatically correct sentences in a particular language. Computationally, it can be partially interpreted and measured via perplexity, which reflects how well the model can predict the next token, given the previous ones (lower perplexity indicates better performance). Domain knowledge, on the other hand, describes the ability of the model to know and reason about a specific domain. Having a set of language understanding benchmarks, we can also evaluate the model's domain knowledge by investigating the accuracy of the answers it selects. These two types of knowledge are partially related to linguistic competence and linguistic performance [\[4\]](#page-5-3).

We are interested in the research question of whether an enhancement of linguistic fluency of a given language in LLM can also improve its domain knowledge in that language, simultaneously preserving LLM's linguistic fluency and domain knowledge in previously learned languages. Since it is a very general question, we provide only a partial analysis, focusing on Lithuanian and English, respectively, and using CL (in the form of EWC regularisation [\[5\]](#page-5-4)) for the preservation of existing domain knowledge.

Our main contributions to the posed research question consist of the empirical findings that when we enhanced Gemma2's Lithuanian language fluency via autoregressive pretraining using the first 10% of the Lithuanian language component of the CulturaX dataset,

- EWC allowed us to mitigate the catastrophic forgetting effects in the English component both in linguistic fluency (measured via perplexity benchmark) and domain knowledge (measured via language understanding benchmarks; 7*/*7 cases);
- EWC allowed us to improve the performance of the Lithuanian component both in linguistic fluency (measured via perplexity benchmark) and domain knowledge in 5*/*7 language understanding benchmarks (ARC-Easy, GSM8K, HellaSwag, MMLU, and Winogrande).

We structure our article beginning with a short review of the related work in Section [2.](#page-1-0) In Section [3](#page-2-0) we discuss our experiment setup and present our empirical findings in Section [4.](#page-3-0) Finally, we conclude our research in Section [5.](#page-4-0)

## <span id="page-1-0"></span>2 Related work

#### 2.1 Continual learning in LLMs

CL methods used in LLMs are roughly classified into replay-based, regularisation-based, architecture-based [\[3\]](#page-5-2), or combined approaches. Since in this research, we assume a two-task CL scenario, let us denote them with A and B.

Replay-based methods rely on a fraction of the previous task datasets to be preserved for future training, [\[6,](#page-5-5) [7,](#page-5-6) [8\]](#page-5-7). However, previous training data are often not available, which limits the applicability of these methods for non-generative architectures. For generative architectures, the replay buffers can be sampled from the distribution, represented by the model, as in [\[9\]](#page-5-8).

Regularisation-based methods rely on additive regularisers, which encourage CL. Having a model, trained for task A, and new task B, regularisation-based models minimise the regularised loss *L*B(*θ*) + *λ*ΩA(*θ*), where *θ* are the model's parameters, *L*B(*θ*) is loss for task B, *λ >* 0 is a regularisation strength, and ΩA(*θ*) is regulariser, which encourages CL. These methods are usually computationally efficient and can be combined additively. For instance, in EWC, ΩA(*θ*) = P *<sup>i</sup> Fi*(*θ<sup>i</sup>* − *θ*<sup>A</sup>*,i*) 2 , where *F<sup>i</sup>* is Fisher information, *θ<sup>i</sup>* is the *i*-th model's parameter, and *θ*<sup>A</sup>*,i* is the corresponding parameter from the previous task (see Section [2.2](#page-2-1) for details). In synaptic intelli-

gence ΩA(*θ*) = P *<sup>i</sup> Si*(*θ<sup>i</sup>* − *θ*<sup>A</sup>*,i*) 2 , where *S<sup>i</sup>* = P *t*≤*T* (*θ*A*,i*(*t*+1)−*θ*A*,i*(*t*)) *<sup>∂</sup>*L(*t*) *∂θi* [*t*] (*θ*A*,i*−*θ*A*,i*(0))2+*ϵ* , *ϵ >* 0 is damping parameter, and *t* = 0*,* 1*, ..., T* are training steps. This approach requires recording loss gradients and weight changes. In Learning without Forgetting [\[10\]](#page-5-9), ΩA(*θ*) = KL (*f*A(*x*)∥*fθ*(*x*)), where *fA*(*x*) is the previously trained model's output distribution, *fθ*(*x*) is the current model's output distribution, and KL is the Kullback-Leibler divergence. This approach was used by [\[11\]](#page-5-10) to mitigate catastrophic forgetting for semantic processing tasks. In their work, the BERT-based model is incrementally trained with new languages, using unlabeled data from previous tasks.

Architecture-based approaches aim to have specific architectural components for individual tasks. For example, different tasks can be learned using performance-efficient fine-tuning (PEFT) adapters, such as LoRA [\[12\]](#page-5-11) and CUR-LoRA [\[13\]](#page-6-0).

Combined approaches integrate different CL methods to use the advantages and mitigate limitations of individual components (e.g., regularising PEFT adapters via EWC, as in [\[14\]](#page-6-1)). In addition, CL can be improved by incorporating various heuristics, such as learning rate schedulers [\[15\]](#page-6-2), where the learning rate is reduced after each task as such: *lr<sup>t</sup>* = max(*lrmin, lrt*−<sup>1</sup> · *γ*), where *γ >* 0 is a hyper-parameter.

#### <span id="page-2-1"></span>2.2 Elastic Weight Consolidation

In our experiments, we will use EWC, motivated by recent findings that regularisation-based CL methods, such as synaptic intelligence, are closely related to it [\[16\]](#page-6-3). The authors of [\[5\]](#page-5-4) describe an EWC regularisation framework in which the parameters that are important for the previous tasks have reduced plasticity. In this framework, model optimization is the finding of the most probable model parameters *θ* given data D. Taking logarithms of the Bayes' formula *p*(*θ*|D) = *<sup>p</sup>*(D|*θ*)*p*(*θ*) *<sup>p</sup>*(D) we have:

$$
\log p(\theta|\mathcal{D}) = \log p(\mathcal{D}|\theta) + \log p(\theta) - \log p(\mathcal{D}),\tag{1}
$$

where log *p*(D|*θ*) describes the log-probability of the model with parameters *θ* on the dataset D, which is the negative of the loss function. In the CL scenario, where task A with data D<sup>A</sup> is followed by task B with data DB, the probability of model parameters *p*(*θ*) following a pretraining on dataset D<sup>A</sup> has value *p*(*θ*|DA). Thus, the equation can be rewritten as follows:

$$
\log p(\theta | \mathcal{D}_{\mathcal{B}}) = \log p(\mathcal{D}_{\mathcal{B}} | \theta) + \log p(\theta | \mathcal{D}_{\mathcal{A}}) - \log p(\mathcal{D}_{\mathcal{B}}). \tag{2}
$$

We can notice that the right side of the equation depends on the loss of task B, and therefore all the information for task A is in the distribution *p*(*θ*|DA). Transforming this into a loss function, we get eq. [3:](#page-2-2)

<span id="page-2-2"></span>
$$
\mathcal{L}(\theta) = \mathcal{L}_{\mathcal{B}}(\theta) + \frac{\lambda}{2} \sum_{i} F_i (\theta_i - \theta_{A,i})^2,
$$
\n(3)

where *F<sup>i</sup>* = E *∂* log *p*(*y*|*x*;*θ*A) *∂θ<sup>i</sup>* 2 is Fisher information, and *p*(*y*|*x*; *θ*A) is the conditional density. Intuitively, this regulariser measures the importance of the parameter *θ<sup>i</sup>* , and during the training of task B it penalises its deviation according to this importance.

To protect the parameters of Gemma2, which are potentially responsible for domain knowledge, we use MMLU data (which consists of a set of academic language understanding benchmarks in multiple domains) for Fisher's information estimation, estimating it via the empirical Fisher estimator (see Section 5.4 from [\[17\]](#page-6-4)):

$$
F_i = \frac{1}{|D_{\text{MMLU}}|} \sum_{(x,y)\in D_{\text{MMLU}}} \left(\frac{\partial}{\partial \theta_i} \log p_{\theta}(y|x) \bigg|_{\theta_i = \theta_{\mathcal{A},i}}\right)^2,\tag{4}
$$

where *D*MMLU is the MMLU data set.

## <span id="page-2-0"></span>3 Experimental setup

Conceptually, our experiment is similar to that of [\[18\]](#page-6-5), where the authors use various architecture-based methods to continually pretrain the Llama2 model for the Chinese language. However, instead of architecture-based methods, we focus on adding EWC regularisation for achieving CL. In our experiments, we use Gemma2 LLM (gemma2-2bit) [\[19\]](#page-6-6), due to its sufficiently compact parametrisation and good performance on modern LLM benchmarks. The initial task A is the model's pretraining performed by the original authors, and task B is the next-token prediction on 10% of the Lithuanian portion of CulturaX [\[20\]](#page-6-7). We trained task B using EWC regularisation with a range of regularisation strengths *λ* ∈ {0*,* 10<sup>2</sup> *,* 10<sup>3</sup> *,* 10<sup>6</sup> *,* 10<sup>9</sup> *,* 10<sup>12</sup>}, and evaluated the linguistic fluency and domain knowledge of the resulting models in English and Lithuanian. In the training process, we used the AdamW optimizer with crossentropy loss and the following hyperparameters: a learning rate of 0*.*0002, a warm-up ratio of 0*.*05, weight decay of 0*.*01, a per-device batch size of 2, and 1 gradient accumulation step. The evaluation of each of the 6 values of *λ* described above required approximately 4 hours, totalling 24 hours of computation time. All experiments were carried out on a cluster of 8 H100 GPUs.

Linguistic fluency. For this, we performed two perplexity benchmarks. The first one was aimed at assessing the effectiveness of the CL in terms of perplexity. Specifically, we evaluated the average perplexity of TruthfulQA questionanswer pairs (in both English and Lithuanian). In the second one, we investigated the potential negative effects of EWC for the added Lithuanian language, when the regularisation strength *λ* is excessively high. To this end, we used the Lithuanian Q/A dataset [\[21,](#page-6-8) [22\]](#page-6-9) and measured the average perplexity of the model's responses to questions from this dataset using LT-Llama2-13B, which is noted for its grammatical accuracy [\[23\]](#page-6-10).

Domain knowledge. To measure the model's domain knowledge, we used popular language understanding benchmarks listed in Table [1](#page-3-1) (both in English and Lithuanian [\[21,](#page-6-8) [22\]](#page-6-9)). Note that although the English version of MMLU data was used in EWC to estimate Fisher information, we included this dataset in our benchmarks because, in our opinion, its empirical performance still may be interesting.

<span id="page-3-1"></span>

| Benchmark  | Description                                        | # Instances | Reference(s) |
|------------|----------------------------------------------------|-------------|--------------|
| MMLU       | Multi-task language understanding across 57 tasks. | 15,908      | [24, 25]     |
| Belebele   | Multilingual reading comprehension benchmark.      | 122,000     | [26]         |
| GSM8K      | School-level math word problems.                   | 8,500       | [27]         |
| HellaSwag  | Commonsense reasoning completion tasks.            | 70,000      | [28]         |
| ARC-Easy   | School-level science questions (easy subset).      | 2,251       | [29]         |
| TruthfulQA | Assessing truthfulness of model-generated answers. | 817         | [30]         |
| WinoGrande | Commonsense reasoning with pronoun resolution.     | 44,000      | [31]         |

Table 1: Summary of performed language understanding benchmarks.

## <span id="page-3-0"></span>4 Results

<span id="page-3-2"></span>![](./assets/ewc-gemma2-cpt/_page_3_Figure_5.jpeg)

![](./assets/ewc-gemma2-cpt/_page_3_Figure_7.jpeg)

(a) Perplexity vs. regularisation strength *λ* (TruthfulQA data). (b) The averaged accuracy on all language understanding benchmarks versus regularisation strength *λ*.

Figure 1: Comparison of perplexity and average accuracy in domain understanding tasks with varying regularisation strength *λ*. *λ* = 0 denotes a setting without EWC. "Fine-tuned" plot indicates autoregressive pretraining with EWC regularisation.

Linguistic fluency. Figure [1a](#page-3-2) shows the average perplexity evaluated using the TruthfulQA data in the same manner, while Figure [2](#page-4-1) displays the average perplexity evaluated via LT-Llama2-13B on the Lithuanian Q/A dataset. Figure [1a](#page-3-2) shows that the EWC enabled the preservation of English data perplexity when the Lithuanian language was integrated into the model. Although with *λ* = 0, we observed a similar effect as in domain knowledge benchmarks, as the value of *λ* increases, the perplexity of the English data approaches that of the initial Gemma2 model. On the other hand, Figure [2](#page-4-1) shows surprisingly low perplexities for *λ <* 10<sup>9</sup> . As *λ* increases, the perplexity of the answers tends to rise, indicating the negative effects of overly strong regularisation.

Domain knowledge. Figure [1b](#page-3-2) presents the average accuracy across all language understanding benchmarks listed in Table [1](#page-3-1) for different values of *λ*. The results of the individual language understanding benchmarks can be found in Figure [3.](#page-8-0) It can be seen that with *λ* = 0, analogous to not using EWC at all, the performance of the model drops significantly, often even not reaching the initial accuracy. This may be because our dataset (10% of the Lithuanian component of CulturaX, which mainly consists of web crawls of common websites) was insufficient for an improvement of LLMs trained with much larger and more diverse data. On the other hand, *λ >* 10<sup>11</sup> describes the case where the model is non-plastic. This can be seen in the accuracy, which is very similar to that of the initial model, suggesting that the model likely did not change much from its initial version, trained on task A. The range *λ* ∈ [10<sup>2</sup> *,* 10<sup>11</sup>] reveals two interesting effects. First, in Figure [3](#page-8-0) we see that in this range the accuracies for the Lithuanian version of the benchmarks are also higher, indicating that EWC may be helpful not only to not forget domain-level knowledge in English but also to attain it more efficiently in the newly added Lithuanian language. This may be partially explained by the mechanism of EWC in our setup, which inhibits updates of the parameters that are important for domain knowledge. In addition, Figure [3](#page-8-0) shows that for larger *λ*, EWC regularisation may even increase the accuracy for English domain knowledge benchmarks (e.g., GSM8K, TruthfulQA sets).

Figure [3](#page-8-0) includes the evaluation of the models on the GSM8K benchmark, which consists of grade-school mathematical problems (see Table [1\)](#page-3-1). It was previously observed [\[21,](#page-6-8) [22\]](#page-6-9) that the Llama2 model, fine-tuned on the Lithuanian part of the CulturaX dataset, loses its mathematical ability due to the absence of mathematics in CulturaX data. Although in our experiment we used a different LLM architecture, this effect is also visible in Figure [3.](#page-8-0) This figure also shows that for *λ >* 10<sup>6</sup> , the mathematical ability of Gemma2 LLM is retained with the help of EWC.

Figure [1](#page-3-2) suggests that the values of *λ* that resulted in lower perplexity also correspond to better performance in domain knowledge benchmarks, partially in agreement with the findings of [\[32\]](#page-7-0).

## <span id="page-4-0"></span>5 Conclusions

We empirically investigated the posed research question of whether an enhancement of the linguistic fluency of the Lithuanian language in LLM can also improve its domain knowledge in that language, simultaneously preserving LLM's linguistic fluency and domain knowledge in previously learned English language. We used perplexity as a measure of linguistic fluency and evaluated the model's domain knowledge via the accuracies of popular language understanding benchmarks (ARC-Easy, Belebele, GSM8K, HellaSwag, MMLU, TruthfulQA, and Winogrande). In order to preserve the existing knowledge, we used CL in the form of EWC.

Specifically, we autoregressively pretrained the Gemma2 LLM (2 billion parameter version) with 10% of the Lithuanian component of CulturaX, using EWC regularisation with different regularisation strengths *λ*. To foster reproducible research, we report the hyper-parameters we used in our experiments and include a link to the accompanying code repository.

The experiments performed reveal that our setup allowed us to enhance the Lithuanian component of Gemma2, simultaneously mitigating the catastrophic forgetting effects in its English component in both linguistic fluency and domain knowledge on all 7 benchmarks (ARC-Easy, Belebele, GSM8K, HellaSwag, MMLU, TruthfulQA, and Winogrande). Furthermore, the EWC regularisation also improved both linguistic fluency and domain knowledge for the Lithuanian language on the 5*/*7 benchmarks (ARC-Easy, GSM8K, HellaSwag, MMLU, and Winogrande).

<span id="page-4-1"></span>These findings support an affirmative response to the research question posed. Our results may have practical implications for utilising general-purpose LLMs for specialisation in low-resource languages: if it were possible to shift

![](./assets/ewc-gemma2-cpt/_page_4_Figure_8.jpeg)

Figure 2: Perplexity of the answer (evaluated with LT-Llama-13B) versus regularisation strength *λ* (Lithuanian Q/A [\[21,](#page-6-8) [22\]](#page-6-9) data).

linguistic fluency without disturbing the domain knowledge of an LLM, the creation of stronger regional LLMs would become far easier.

Limitations. Although we conducted a fairly large experiment, our findings are still based on limited data. For example, we used only 10% of the Lithuanian component of CulturaX for autoregressive pretraining, evaluated the Fisher information using MMLU only, and relied on just TruthfulQA and Lithuanian Q/A datasets for perplexity evaluations. Our approach to evaluating Fisher information via MMLU also asks for a theoretical justification. In addition, comparisons with other CL methods would better connect our work with the existing body of research and elucidate the extent to which our empirical findings hold. Although we roughly estimated intervals, the selection of optimal regularisation strength *λ* when applying EWC to full parameter continual pretraining of LLMs is still an open question.

Future work. We plan to investigate combined CL approaches for generative LLMs, leveraging their ability to generate samples from the initial task distribution and exploring mechanisms that allow for sparse updates while compensating for the limitations of individual components. In addition, since the linguistic fluency and domain knowledge of language models can be measured through perplexity and accuracy in benchmarks, a causal investigation of these two signals, in our opinion, would potentially provide interesting insights about LLMs.

## Acknowledgement

This research was funded and conducted by Neurotechnology. We are grateful to Neurotechnology for providing the necessary resources and support. We also thank Greta Tikužyte for editing the English language, and our colleagues ˙ for their helpful comments and discussions.

# References

- <span id="page-5-0"></span>[1] Ashish Vaswani, Noam Shazeer, Niki Parmar, and et al. Attention is all you need. In I. Guyon, U. Von Luxburg, S. Bengio, H. Wallach, R. Fergus, S. Vishwanathan, and R. Garnett, editors, *Advances in Neural Information Processing Systems*, volume 30. Curran Associates, Inc., 2017.
- <span id="page-5-1"></span>[2] Mingyang Wang, Alisa Stoll, Lukas Lange, Heike Adel, Hinrich Schütze, and Jannik Strötgen. Bring Your Own Knowledge: A Survey of Methods for LLM Knowledge Expansion, 2025.
- <span id="page-5-2"></span>[3] Haizhou Shi, Zihao Xu, Hengyi Wang, Weiyi Qin, Wenyuan Wang, Yibin Wang, Zifeng Wang, Sayna Ebrahimi, and Hao Wang. Continual learning of large language models: A comprehensive survey. *arXiv preprint arXiv:2404.16789*, 2024.
- <span id="page-5-3"></span>[4] Noam Chomsky. *Aspects of the Theory of Syntax*. The MIT Press, Cambridge, 1965.
- <span id="page-5-4"></span>[5] James Kirkpatrick, Razvan Pascanu, Neil Rabinowitz, Joel Veness, Guillaume Desjardins, Andrei A Rusu, Kieran Milan, John Quan, Tiago Ramalho, Agnieszka Grabska-Barwinska, et al. Overcoming Catastrophic Forgetting in Neural Networks. *Proceedings of the national academy of sciences*, 114(13):3521–3526, 2017.
- <span id="page-5-5"></span>[6] Wenzhen Zheng, Wenbo Pan, Xu Xu, Libo Qin, Li Yue, and Ming Zhou. Breaking Language Barriers: Cross-Lingual Continual Pre-Training at Scale. *arXiv preprint arXiv:2407.02118*, 2024.
- <span id="page-5-6"></span>[7] Thomas Scialom, Tuhin Chakrabarty, and Smaranda Muresan. Fine-tuned language models are continual learners. *arXiv preprint arXiv:2205.12393*, 2022.
- <span id="page-5-7"></span>[8] Adam Ibrahim, Benjamin Thérien, Kshitij Gupta, Mats L Richter, Quentin Anthony, Timothée Lesort, Eugene Belilovsky, and Irina Rish. Simple and scalable strategies to continually pre-train large language models. *arXiv preprint arXiv:2403.08763*, 2024.
- <span id="page-5-8"></span>[9] Fan-Keng Sun, Cheng-Hao Ho, and Hung-Yi Lee. LAMOL: LAnguage MOdeling for Lifelong Language Learning. *arXiv preprint arXiv:1909.03329*, 2019.
- <span id="page-5-9"></span>[10] Zhizhong Li and Derek Hoiem. Learning Without Forgetting. In Bastian Leibe, Jiri Matas, Nicu Sebe, and Max Welling, editors, *Computer Vision – ECCV 2016*, pages 614–629, Cham, 2016. Springer International Publishing.
- <span id="page-5-10"></span>[11] Giuseppe Castellucci, Simone Filice, Danilo Croce, and Roberto Basili. Learning to solve NLP tasks in an incremental number of languages. In *Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 2: Short Papers)*, pages 837–847, 2021.
- <span id="page-5-11"></span>[12] Edward J Hu, yelong shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. LoRA: Low-rank adaptation of large language models. In *International Conference on Learning Representations*, 2022.
- <span id="page-6-0"></span>[13] Muhammad Fawi. CURLoRA: Stable LLM Continual Fine-Tuning and Catastrophic Forgetting Mitigation, 2024.
- <span id="page-6-1"></span>[14] Jiannan Xiang, Tianhua Tao, Yi Gu, Tianmin Shu, Zirui Wang, Zichao Yang, and Zhiting Hu. Language models meet world models: Embodied experiences enhance language models. *Advances in Neural Information Processing Systems*, 36:75392–75412, 2023.
- <span id="page-6-2"></span>[15] Genta Indra Winata, Lingjue Xie, Karthik Radhakrishnan, Shijie Wu, Xisen Jin, Pengxiang Cheng, Mayank Kulkarni, and Daniel Preotiuc-Pietro. Overcoming catastrophic forgetting in massively multilingual continual learning. *arXiv preprint arXiv:2305.16252*, 2023.
- <span id="page-6-3"></span>[16] Frederik Benzing. Unifying Importance Based Regularisation Methods for Continual Learning. In Gustau Camps-Valls, Francisco J. R. Ruiz, and Isabel Valera, editors, *Proceedings of The 25th International Conference on Artificial Intelligence and Statistics*, volume 151 of *Proceedings of Machine Learning Research*, pages 2372– 2396. PMLR, 2022.
- <span id="page-6-4"></span>[17] Gido M. van de Ven. On the Computation of the Fisher Information in Continual Learning. In *ICLR Blogposts 2025*, 2025. https://d2jud02ci9yv69.cloudfront.net/2025-04-28-fisher-120/blog/fisher/.
- <span id="page-6-5"></span>[18] Chen-An Li and Hung-Yi Lee. Examining forgetting in continual pre-training of aligned large language models. *arXiv preprint arXiv:2401.03129*, 2024.
- <span id="page-6-6"></span>[19] Gemma Team, Morgane Riviere, Shreya Pathak, Pier Giuseppe Sessa, Cassidy Hardin, Surya Bhupatiraju, Léonard Hussenot, Thomas Mesnard, Bobak Shahriari, Alexandre Ramé, et al. Gemma 2: Improving open language models at a practical size. *arXiv preprint arXiv:2408.00118*, 2024.
- <span id="page-6-7"></span>[20] Thuat Nguyen, Chien Van Nguyen, Viet Dac Lai, Hieu Man, Nghia Trung Ngo, Franck Dernoncourt, Ryan A Rossi, and Thien Huu Nguyen. Culturax: A cleaned, enormous, and multilingual dataset for large language models in 167 languages. *arXiv preprint arXiv:2309.09400*, 2023.
- <span id="page-6-8"></span>[21] Arturas Nakvosas, Povilas Daniušis, and Vytas Mulevi ¯ cius. Open Llama2 Model for the Lithuanian Language. ˇ *arXiv preprint arXiv:2408.12963*, 2024.
- <span id="page-6-9"></span>[22] Arturas Nakvosas, Povilas Daniušis, and Vytas Mulevi ¯ cius. Open Llama2 Models for the Lithuanian Language. ˇ *Informatica*, pages 1–22, 2025.
- <span id="page-6-10"></span>[23] Jurgita Kapociˇ ut¯ e-Dzikien ˙ e, Toms Bergmanis, and M ˙ arcis Pinnis. Localizing AI: Evaluating Open-Weight Lan- ¯ guage Models for Languages of Baltic States. *arXiv preprint arXiv:2501.03952*, 2025.
- <span id="page-6-11"></span>[24] Dan Hendrycks, Collin Burns, Steven Basart, Andrew Critch, Jerry Li, Dawn Song, and Jacob Steinhardt. Aligning AI With Shared Human Values. *Proceedings of the International Conference on Learning Representations (ICLR)*, 2021.
- <span id="page-6-12"></span>[25] Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and Jacob Steinhardt. Measuring Massive Multitask Language Understanding. *Proceedings of the International Conference on Learning Representations (ICLR)*, 2021.
- <span id="page-6-13"></span>[26] Lucas Bandarkar, Davis Liang, Benjamin Muller, Mikel Artetxe, Satya Narayan Shukla, Donald Husa, Naman Goyal, Abhinandan Krishnan, Luke Zettlemoyer, and Madian Khabsa. The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants. In *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 749–775. Association for Computational Linguistics, 2024.
- <span id="page-6-14"></span>[27] Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman. Training Verifiers to Solve Math Word Problems. *arXiv preprint arXiv:2110.14168*, 2021.
- <span id="page-6-15"></span>[28] Rowan Zellers, Ari Holtzman, Yonatan Bisk, Ali Farhadi, and Yejin Choi. HellaSwag: Can a Machine Really Finish Your Sentence? In *Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics*, 2019.
- <span id="page-6-16"></span>[29] Peter Clark, Isaac Cowhey, Oren Etzioni, and Tushar Khot and. Think you have Solved Question Answering? Try ARC, the AI2 Reasoning Challenge. *arXiv:1803.05457v1*, 2018.
- <span id="page-6-17"></span>[30] Stephanie Lin, Jacob Hilton, and Owain Evans. TruthfulQA: Measuring How Models Mimic Human Falsehoods, 2021.
- <span id="page-6-18"></span>[31] Sakaguchi Keisuke, Le Bras Ronan, Bhagavatula Chandra, and Choi Yejin. WinoGrande: An Adversarial Winograd Schema Challenge at Scale. 2019.

<span id="page-7-0"></span>[32] Hila Gonen, Srini Iyer, Terra Blevins, Noah Smith, and Luke Zettlemoyer. Demystifying prompts in language models via perplexity estimation. In Houda Bouamor, Juan Pino, and Kalika Bali, editors, *Findings of the Association for Computational Linguistics: EMNLP 2023*, pages 10136–10148, Singapore, December 2023. Association for Computational Linguistics.

<span id="page-8-0"></span>![](./assets/ewc-gemma2-cpt/_page_8_Figure_0.jpeg)

Figure 3: Accuracy of the models versus EWC regularisation strength *λ* on the language understanding benchmarks. "Fine-tuned" plot indicates autoregressive pretraining with EWC regularisation.