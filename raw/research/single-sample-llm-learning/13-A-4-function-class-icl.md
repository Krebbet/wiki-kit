---
url: "file:///home/david/code/wiki-kit/raw/research/single-sample-llm-learning/pdfs/A-4-function-class-icl.pdf"
title: "What Can Transformers Learn In-Context? A Case Study of Simple Function Classes"
captured_on: "2026-04-20"
capture_method: "pdf"
engine: "marker"
assets_dir: "./assets/A-4-function-class-icl"
---

# What Can Transformers Learn In-Context? A Case Study of Simple Function Classes

Shivam Garg\* Stanford University shivamg@cs.stanford.edu

Percy Liang Stanford University pliang@cs.stanford.edu

Dimitris Tsipras\* Stanford University tsipras@stanford.edu

Gregory Valiant Stanford University valiant@stanford.edu

#### **Abstract**

In-context learning refers to the ability of a model to condition on a prompt sequence consisting of in-context examples (input-output pairs corresponding to some task) along with a new query input, and generate the corresponding output. Crucially, in-context learning happens only at inference time without any parameter updates to the model. While large language models such as GPT-3 exhibit some ability to perform in-context learning, it is unclear what the relationship is between tasks on which this succeeds and what is present in the training data. To make progress towards understanding in-context learning, we consider the well-defined problem of training a model to in-context learn a function class (e.g., linear functions): that is, given data derived from some functions in the class, can we train a model to in-context learn "most" functions from this class? We show empirically that standard Transformers can be trained from scratch to perform in-context learning of linear functions—that is, the trained model is able to learn unseen linear functions from in-context examples with performance comparable to the optimal least squares estimator. In fact, in-context learning is possible even under two forms of distribution shift: (i) between the training data of the model and inference-time prompts, and (ii) between the in-context examples and the query input during inference. We also show that we can train Transformers to in-context learn more complex function classes—namely sparse linear functions, two-layer neural networks, and decision trees—with performance that matches or exceeds task-specific learning algorithms. [1](#page-0-0)

# **1 Introduction**

Large language models such as GPT-3 [\[Brown et al., 2020\]](#page-13-0) are able to perform *in-context learning*: given a prompt containing examples from a task (input-output pairs) and a new query input, the language model can generate the corresponding output. For example, these models are able to produce English translations of French words after being prompted on a few such translations, e.g.:

$$
\underbrace{\text{maison} \to \text{house, chat} \to \text{cat, chien} \to \text{dog}}_{\text{prompt}}.
$$

This capability is quite intriguing as it allows models to adapt to a wide range of downstream tasks on-thefly—i.e., without the need to perform any parameter updates after the model is trained [\[Brown et al., 2020,](#page-13-0)

\*Equal contribution.

<span id="page-0-0"></span><sup>1</sup>Our code and models are available at <https://github.com/dtsip/in-context-learning>.

[Lieber et al., 2021,](#page-15-0) [Rae et al., 2021,](#page-16-0) [Black et al., 2022\]](#page-13-1). However, it is unclear to what extent these models have developed the ability to learn *new tasks* from in-context examples alone as opposed to simply indexing into a vast set of known tasks from the training data (e.g., see [Min et al.](#page-15-1) [\[2022\]](#page-15-1)). [2](#page-1-0)

To make progress towards understanding in-context learning, we consider the well-defined problem of learning a *function class* from in-context examples. That is, we say that a model can in-context learn a function class F if, for "most" functions *f* ∈ F, the model can approximate *f*(*x*query) for a new query input *x*query by conditioning on a prompt sequence (*x*1, *f*(*x*1), . . . , *x<sup>k</sup>* , *f*(*x<sup>k</sup>* ), *x*query) containing in-context examples and the query input.

Formally, let *D*<sup>X</sup> be a distribution over inputs and *D*<sup>F</sup> be a distribution over functions in F. A prompt *P* is a sequence (*x*1, *f*(*x*1), . . . , *x<sup>k</sup>* , *f*(*x<sup>k</sup>* ), *x*query) where inputs (i.e., *x<sup>i</sup>* and *x*query) are drawn i.i.d. from *D*<sup>X</sup> and *f* is drawn from *D*<sup>F</sup> . We say that a model *M* can in-context learn the function class F up to *ϵ*, with respect to (*D*<sup>F</sup> , *D*<sup>X</sup> ), if it can predict *f*(*x*query) with an average error

<span id="page-1-2"></span>
$$
\mathbb{E}_P\left[\ell\left(M\left(P\right),f\left(x_{\text{query}}\right)\right)\right] \leq \epsilon,\tag{1}
$$

where ℓ(·, ·) is some appropriate loss function, such as the squared error.

Within this framework, we can now concretely ask:

*Can we train a model to in-context learn a certain function class?*

Note that, here, being able to in-context learn a function class is a property of model *M* alone, independent of how it was trained. *Training* such a model can be viewed as an instance of *meta-learning* [\[Schmidhuber,](#page-16-1) [1987,](#page-16-1) [Naik and Mammone, 1992,](#page-15-2) [Thrun and Pratt, 2012\]](#page-17-0), a general paradigm for learning a model or method that can learn from data.

We empirically study this question, focusing on Transformer models [\[Vaswani et al., 2017,](#page-17-1) [Radford](#page-16-2) [et al., 2018\]](#page-16-2)—the architecture behind recent large language models—trained from scratch to in-context learn a range of simple, well-defined function classes (e.g. linear functions). Specifically, we sample prompts containing in-context examples (input-output pairs) generated using functions in a given class and train models to predict the function value at the corresponding query inputs. (see illustration in Figure [1\)](#page-1-1). Our findings are as follows.

<span id="page-1-1"></span>![](./assets/A-4-function-class-icl/_page_1_Figure_9.jpeg)

Figure 1: *Can we train a model that in-context learns a function class (here linear functions)?* We train Transformers by repeatedly sampling a random function *f* from that class, as well as random inputs *x*1, . . . , *x<sup>k</sup>* and training the model to predict each *f*(*xi*) given the prompt *x*1, *f*(*x*1), . . . , *xi*−<sup>1</sup> , *f*(*xi*−1), *x<sup>i</sup>* (wrt squared loss). Then, during inference, we evaluate the model's ability to predict accurately on new, *unseen* functions.

<span id="page-1-0"></span><sup>2</sup>The term "in-context learning" has also been used to refer to a more general notion of learning from a prompt [\[Olsson et al., 2022\]](#page-15-3). In this work, we focus on the standard notion which refers to learning a task/function given in-context examples [\[Brown et al., 2020\]](#page-13-0).

**Transformers can in-context learn linear functions.** We show empirically that we can train a standard Transformer from scratch to in-context learn the class of linear functions, with respect to the input distribution *D*X being an isotropic Gaussian in 20 dimensions, and *D*F being the distribution over linear functions with weight vectors drawn from an isotropic Gaussian (the model was trained on prompts generated from the same distributions *D*X and *D*F ). Specifically, the trained model achieves error comparable to the optimal least squares estimator, suggesting that it encodes an effective learning algorithm, at least for the distribution used to generate the training prompts.

**Generalization to out-of-distribution prompts.** To understand the extent to which the trained model encodes an algorithm that works beyond the training distribution, we consider in-context learning under two types of distribution shifts: (a) a shift between the prompts encountered during training and inference (e.g., training on prompts without any noise in the in-context example outputs but testing with noisy outputs), (b) a shift between the in-context examples and the query input during inference (e.g., in-context examples lie in one orthant and the query input lies in another). We find that the performance of our model is quite robust to such shifts, indicating that it has learned to perform linear regression with some generality.

**More complex function classes.** We also consider the function classes of 3-sparse linear functions, two-layer ReLU neural networks with 100 hidden units, and decision trees of depth 4, all with 20 dimensional inputs. We show that we can again train Transformer models that can in-context learn these classes (with respect to isotropic Gaussian inputs and appropriately defined distributions over functions). For sparse linear functions, the trained model is able to exploit sparsity, obtaining performance better than least squares and comparable to Lasso. For neural networks, the corresponding model is able to obtain performance comparable to neural networks of the same architecture trained using gradient descent on in-context examples. Moreover, it is also able to in-context learn linear functions. For decision trees, the trained model can learn unseen trees with as few as 100 in-context examples, whereas greedy learning and tree boosting algorithms are unable to achieve competitive performance (for the distribution of prompts studies here). Note that learning these function classes requires involved algorithms (e.g., gradient descent with the Lasso objective), and our results show that Transformers can encode algorithms with similar performance in a single forward pass.

**Role of model capacity and problem dimension.** Finally, we explore how the ability of Transformers to in-context learn linear functions scales with model capacity and problem dimensionality. We find that increasing the capacity of the model improves performance significantly, and also allows the model to incontext learn higher-dimensional functions. Moreover, increasing the capacity often significantly improves performance with distribution shifts, even when the absolute improvement in the standard error is small.

# <span id="page-2-0"></span>**2 Training models for in-context learning**

We now describe a general methodology for training a model that can in-context learn a function class F with respect to a distribution *D*F over functions, and *D*X over inputs. To do so, we start by constructing random training prompts as follows. For each prompt, we first sample a random function *f* from the class according to *D*<sup>F</sup> , then create a set of random inputs *x*1, . . . , *xk*+<sup>1</sup> drawn independently from *D*<sup>X</sup> , and finally evaluate *f* on these inputs to produce the prompt *P* = (*x*1, *f*(*x*1), . . . , *xk*+<sup>1</sup> , *f*(*xk*+<sup>1</sup> )). For example, in the case of linear functions, inputs could be drawn from the isotropic Gaussian distribution *N*(0, *I<sup>d</sup>* ), and a random function chosen by sampling weight vector *w* from *N*(0, *I<sup>d</sup>* ) and setting *f*(*x*) = *w* <sup>⊤</sup>*x*.

Now, given such prompts, we train a model to predict *f*(*xi*) for a given *x<sup>i</sup>* based on a set of preceding in-context examples. Concretely, let *P <sup>i</sup>* denote the prompt prefix containing *i* in-context examples (the first *i* input-output pairs) and the (*i* + 1) th input: *P <sup>i</sup>* = (*x*1, *f*(*x*1), *x*2, *f*(*x*2), . . . , *x<sup>i</sup>* , *f*(*xi*), *xi*+1). Then, we train a model *M<sup>θ</sup>* parameterized by *θ* aiming to minimize the expected loss over all the prompt prefixes:

<span id="page-3-0"></span>
$$
\min_{\theta} \mathbb{E}_{P} \left[ \frac{1}{k+1} \sum_{i=0}^{k} \ell \left( M_{\theta} \left( P^{i} \right) , f \left( x_{i+1} \right) \right) \right], \tag{2}
$$

where ℓ(·, ·) is an appropriately chosen loss function. Below, we describe how this general methodology can be implemented for a concrete model family (see Appendix [A](#page-18-0) for additional details).

**Model structure.** We use a decoder-only Transformer architecture [\[Vaswani et al., 2017\]](#page-17-1) from the GPT-2 family [\[Radford et al., 2019\]](#page-16-3). Our model consists of 12 layers, 8 attention heads, and a 256-dimensional embedding space (9.5M parameters). This architecture takes as input a sequence of vectors in its embedding space and predicts the next vector in the sequence within the same space (in language modeling, these vectors correspond to input tokens). We apply this architecture to our prompt format of (*x*1, *f*(*x*1), . . . , *xk*+<sup>1</sup> , *f*(*xk*+<sup>1</sup> )) as follows. We map each prompt output *f*(*xi*) to the same dimension as prompt inputs *x<sup>i</sup>* by appending zeros, and map the prompt inputs and outputs into the latent embedding space of the Transformer through a (learnable) linear transformation. We then use another (learnable) linear transformation to map the vector predicted by the model to a scalar. Note that the Transformer architecture allows us to compute the prediction (*M<sup>θ</sup>* (*P i* )) for all prompt prefixes in a single forward pass.

**Training.** We train the model according to the training objective in [\(2\)](#page-3-0) using squared error as the loss function. We do so by sampling a batch of random prompts at each training step and then updating the model through a gradient update (we use a batch size of 64 and train for 500k total steps). This training is done from scratch, that is, we do *not* fine-tune a pre-trained language model, nor do we train on actual text.

**Curriculum learning.** Many natural function classes contain functions of varying complexity. We exploit this by training our model using a curriculum [\[Bengio et al., 2009,](#page-13-2) [Elman, 1993,](#page-14-0) [Sanger, 1994,](#page-16-4) [Wu et al., 2020\]](#page-17-2), where we train on a simpler distribution of functions in the beginning (e.g., linear functions with weight vectors restricted to a low-dimensional subspace) and gradually increase the function complexity. This speeds up training drastically, often allowing us to train models that would be significantly more expensive to train without a curriculum (see Section [6](#page-9-0) for details).

## <span id="page-3-1"></span>**3 In-context learning of linear functions**

In the previous section, we describe a general methodology for training Transformer models to in-context learn a class of functions. Here, we focus on a simple function class—namely linear functions—and study how well models trained using our methodology can in-context learn this class.

**Prompt distribution.** We consider the class of linear functions F = n *f* | *f*(*x*) = *w* <sup>⊤</sup>*x*, *w* ∈ **R***<sup>d</sup>* o , in *d* dimensions where *d* = 20. We sample *x*1, . . . , *x<sup>k</sup>* , *x*query, and *w* independently from the isotropic Gaussian distribution *N*(0, *I<sup>d</sup>* ). We then compute each *y<sup>i</sup>* = *w* <sup>⊤</sup>*x<sup>i</sup>* and construct the prompt as *P* = (*x*1, *y*1, *x*2, *y*2, . . . , *x<sup>k</sup>* , *y<sup>k</sup>* , *x*query).

**Baselines.** To contextualize the performance of our trained model, we compare it to other learning algorithms: (a) the least squares estimator, computing the minimum-norm linear fit to the in-context examples (*xi* , *yi*), (b) *n*-Nearest Neighbors, averaging the *y<sup>i</sup>* values for the *n* nearest neighbors of *x*query, (c) averaging the values *yix<sup>i</sup>* to estimate *w* and compute the inner product of this estimate with *x*query. Least squares is the optimal estimator for this problem and thus serves as a lower bound to the best error one can achieve. The other two baselines are consistent (but sub-optimal) estimators that are easier to compute and thus provide an estimate of the performance achieved by simple approaches. See Appendix [A.3](#page-19-0) for more details.

### <span id="page-4-1"></span>**3.1 Transformers can in-context learn linear functions**

<span id="page-4-0"></span>We show the in-context learning ability of the resulting model along with the relevant baselines in Figure [2.](#page-4-0) The trained Transformer is able to in-context learn the class of linear functions with respect to the prompt distribution specified above, performing comparably to the optimal least squares estimator for any number of in-context examples considered. While the simpler baselines achieve non-trivial error, they are far worse, indicating that the trained model encodes a more complex algorithm.

![](./assets/A-4-function-class-icl/_page_4_Figure_2.jpeg)

Figure 2: *Evaluating the trained Transformer on in-context learning linear functions.* We plot the normalized squared error of the Transformer ((*M*(*P*) − *w* <sup>⊤</sup>*x*query) <sup>2</sup>/*d*), along with the relevant baselines, as a function of the number of in-context examples. Transformer's error decreases at a rate comparable to least squares. When the number of in-context examples reaches the problem dimension *d* (here 20), least squares achieves 0 error while the Transformer achieves an error of 0.02, improving to 0.0006 at 2*d* in-context examples. While the simple baselines obtain better-than-trivial error (zero estimator, dashed line), their performance is relatively poor. (Error averaged over 1280 prompts. 90% confidence intervals over 1000 bootstrap trials.)

**Can memorization of training prompts explain model performance?** Note that the probability of the model encountering a training prompt similar to the one used for testing is astronomically low—the prompt inputs alone lie in a 800-dimensional space when predicting with 2*d* in-context examples (*d* = 20). Moreover, even considering the possibility that the model encountered a similar *weight vector* during training cannot explain its performance. That is, the model encounters 32 million random weight vectors during training and even using the best of these vectors would lead to an expected error of around 0.2 (computed empirically, see Appendix [B.7](#page-30-0) for details). However, the model is able to achieve an error of less than 0.001 for a prompt with 2*d* in-context examples. Further, in Section [6,](#page-9-0) we show that the model is able to obtain a similar error even when trained on prompts generated using only 10, 000 distinct weight vectors, in which case the best weight vector seen during training would yield an even worse error of around 0.5. Thus, the model cannot be relying on memorization of training prompts or weight vectors, and instead encodes an algorithm capable of in-context learning linear functions that are very different from those seen during training.

### **3.2 What functions is the model learning in-context?**

Recall that the goal of our model is: given the prompt *P* = (*x*1, *w* <sup>⊤</sup>*x*1, . . . , *x<sup>k</sup>* , *w* <sup>⊤</sup>*x<sup>k</sup>* , *x*query), output *w* <sup>⊤</sup>*x*query. Thus, if we fix the prefix given by the *k* in-context examples, we can view the output of the model as a function ˆ *fw*,*x*1:*<sup>k</sup>* (*x*query), that approximates *w* <sup>⊤</sup>*x*query. When *k* < *d* (fewer in-context examples than dimensions), the ground truth cannot be recovered perfectly and the ideal model should approximate (proj*x*1:*<sup>k</sup>* (*w*))⊤*x*query, where proj*x*1:*<sup>k</sup>* (*w*) is the projection of *w* onto the subspace spanned by *x*1, . . . , *x<sup>k</sup>* . Here, we will evaluate how accurately the model approximates this.

<span id="page-5-0"></span>![](./assets/A-4-function-class-icl/_page_5_Figure_0.jpeg)

Figure 3: *Understanding the prefix-conditioned function*. (a) We plot the model prediction as we fix the in-context examples and vary the query input along a random direction (for three random prompts). The shaded regions denote the intervals in which the norm of a randomly training input lies with probability 0.99. When the scale of the query input is close to this range, the model prediction is close to the ground truth linear function (or its projection to the space of in-context inputs when *k* < *d*). (b) We compute the gradient of the model prediction with respect to the query input, and plot its (normalized) inner product with the true *w* and projected *w*, averaged over 1280 random prompts. The gradient aligns almost perfectly with *w* when *k* ≥ *d*, and with projected *w* for all *k*, indicating that the model locally aligns with the ground truth.

**Visualizing along a random direction.** For a randomly sampled fixed prefix, we visualize ˆ *fw*,*x*1:*<sup>k</sup>* (*x*query) as we vary the query input along a random direction *x* (Figure [3a\)](#page-5-0). That is, we pick a random unit vector *x*, and evaluate ˆ *fw*,*x*1:*<sup>k</sup>* (*λx*) as we vary *λ*, the distance of the query input from origin. We observe that ˆ *fw*,*x*1:*<sup>d</sup>* (*λx*) and ˆ *fw*,*x*1:2*<sup>d</sup>* (*λx*) closely match the ground truth and ˆ *fw*,*x*1:*d*/2 (*λx*) matches the projected ground truth, when the distance from origin is not too large compared to the norm of a typical randomly sampled input. In fact, in Appendix [B.1,](#page-21-0) we show that the model is quite robust to scaling the query input: the error doesn't increase much as we scale up the query input by a factor of up to 2, or scale down by a factor of up to 16, and degrades slowly after that.

**Local correctness.** So far, we have seen that the model is able to make predictions close to the ground truth for randomly drawn query inputs and in-context examples. We will now turn our attention to the local change of ˆ *f* around *x*query by considering the gradient of the function ˆ *fw*,*x*1:*<sup>k</sup>* (*x*query) with respect to *x*query (our model is fully differentiable so we can compute the gradient directly). Since ˆ *f* computed by the model should ideally approximate proj*x*1:*<sup>k</sup>* (*w*) <sup>⊤</sup>*x*, this gradient should lie in the direction of the projected ground truth proj*x*1:*<sup>k</sup>* (*w*). In Figure [3b,](#page-5-0) we show the inner product between the gradient and proj*x*1:*<sup>k</sup>* (*w*) (both normalized), averaged over 1280 random prompts, and observe that they align almost perfectly. Since proj*x*1:*<sup>k</sup>* (*w*) = *w* almost surely when *k* ≥ *d*, we observe that the gradient also aligns with *w* perfectly in this regime. Thus the model is locally correct with respect to changes in the query input.

# <span id="page-5-1"></span>**4 Extrapolating beyond the training distribution**

In the previous section, we demonstrated that we can train a model to in-context learn linear functions with respect to the distribution of prompts encountered during training. That is, we evaluate the in-context learning ability of the model with respect to distributions *D*X and *D*F that were also used to train the model.

Here, we evaluate the in-context learning performance of our model on prompt distributions different from the one used for training. Our overarching goal here is to better understand the learning algorithm encoded by our model by analysing how it responds to different prompt distributions.

Formally, we will refer to the distribution of functions used during training as *D*train F and the corresponding distribution of prompt inputs as *D*train X . Then, during inference, functions are sampled from a (potentially different) distribution *D*test F , while prompt inputs from a distribution *D*test X . Moreover, deviating again from our analysis so far, we also consider a separate distribution *D*test query, from which the query input is sampled, potentially dependent on the rest of the in-context inputs *x*1, . . . , *x<sup>k</sup>* (which are still sampled from *D*test X ).

Within this framework, we consider the same model as last section, and evaluate its performance on prompts that deviate from those encountered during training, either by

- 1. sampling prompt inputs or functions from a different distribution, that is *D*train X /F ̸= *D*test X /F or
- 2. introducing a mismatch between in-context examples and the query input, that is *D*test query ̸= *D*test X

.

We describe each such prompt structure below and present a subset of the results in Figure [4](#page-6-0) (see Appendix [B.2](#page-22-0) for additional details and full results). Overall, the model performs reasonably accurate in-context learning with respect to these prompt distributions, indicating that it has indeed learnt to perform linear regression to some generality.

Recall that we generate a training prompt *P* = (*x*1, *w <sup>T</sup>x*1, . . . , *x<sup>k</sup>* , *w <sup>T</sup>x<sup>k</sup>* , *x*query) by drawing the prompt inputs (*x<sup>i</sup>* and *x*query), and the weight vector (*w*) i.i.d. from *N*(0, *I<sup>d</sup>* ), with *d* = 20. For all the settings below, except prompt scaling, we normalize the inputs so that their expected squared norm is equal to that of inputs encountered during training.

<span id="page-6-0"></span>![](./assets/A-4-function-class-icl/_page_6_Figure_6.jpeg)

Figure 4: *In-context learning on out-of-distribution prompts.* We evaluate the trained model on prompts that deviate from those seen during training by: (a) sampling prompt inputs from a non-isotropic Gaussian, (b) adding label noise to in-context examples, (c) restricting in-context examples to a single (random) orthant. In all cases, the model error degrades gracefully and remains close to that of the least squares estimator, indicating that its in-context learning ability extrapolates beyond the training distribution.

**Skewed covariance.** We sample prompt inputs from *N*(0, Σ) where Σ is a skewed covariance matrix with eigenbasis chosen uniformly at random and *i* th eigenvalue proportional to <sup>1</sup>/*<sup>i</sup>* 2 . The model matches the performance of least squares until *k* = 10, mimicking the sharp drop in the error in this regime, but its error plateaus afterwards (see Figure [4a\)](#page-6-0). Thus, it is not perfectly robust to this distribution mismatch but still does relatively well, achieving less than half the error of the nearest neighbor baseline in most cases.

**Low-dimensional subspace.** We sample prompt inputs from a random 10 dimensional subspace. In this case, the model achieves low error after 10 in-context examples, closely matching the behavior of the optimal least squares estimator (the model achieves an error of 0.036, 0.0014, and 0.00057 at 10, 20, and 40 in-context examples respectively)—see Appendix Figure [8b.](#page-23-0) Crucially, unlike the training prompts, when *k* is between 10 and 20, the prompt inputs are linearly dependent, and a model achieving low error in this regime indicates that it encodes a valid orthogonalization procedure for these inputs.

**Noisy linear regression.** We add noise to each prompt output, that is, the *i* th output is equal to *w <sup>T</sup>x<sup>i</sup>* + *ϵ<sup>i</sup>* where *ϵ<sup>i</sup>* ∼ *N*(0, 1). The trained model closely tracks the performance of least squares when the number of in-context examples is not close to the input dimension 20 (see Figure [4b\)](#page-6-0). Interestingly, the model also exhibits the double descent error curve [\[Belkin et al., 2019\]](#page-13-3) that is known to manifest for the least squares estimator [\[Nakkiran, 2019\]](#page-15-4). Note that in this noisy setting, the optimal estimator corresponds to solving least squares with appropriate ℓ2-regularization. However, since the model was trained on noiseless data, we cannot expect it to learn this.

**Prompt scale.** We consider the setting where the prompt scale between training and inference is different. We either scale the prompt inputs or the weight vectors, by a factor {1/3, <sup>1</sup>/2, 2, 3}. The model is relatively robust when scaling the weight vector, but not as robust when scaling the prompt inputs, especially for the more extreme scales 1/3 and 3. Specifically, for 40 in-context examples, the model achieves errors 0.0012, 0.0008, 0.0016, 0.0278 when scaling the weights, and errors 0.30, 0.013, 0.043, 0.58 while scaling the inputs, by factors 1/3, 1/2, 2 and 3 respectively (Appendix Figure [9\)](#page-23-1). For context, recall that with 40 in-context examples, the least squares estimator achieves an error of 0 whereas the model achieves an error of 0.0006 at the original scale.

**Different orthants for in-context and query inputs.** We fix the sign of each coordinate to be positive or negative for all in-context inputs *x<sup>i</sup>* (at random). As a result, all in-context inputs lie in the same orthant, while the query input lies in another orthant with high probability. The model is not affected by the mismatch between in-context and query inputs and closely match the performance of least squares. In this case, the model achieves errors 0.062 and 0.004 for 20 and 40 in-context examples respectively (see Figure [4c\)](#page-6-0), whereas recall that it achieves errors 0.02 and 0.0006 on standard prompts. This indicates that the model is not relying on some variant of nearest neighbor search as in that case, its error would have been significantly larger (see the 3-nearest neighbor baseline).

**Query input orthogonal to in-context inputs.** We sample the query input from the subspace orthogonal to the subspace spanned by in-context example inputs. Here, there is no information relevant to the query input in the in-context examples and thus the model would ideally predict something close to 0 to minimize the error. Indeed, the model outputs such a prediction, achieving an error close to 1 (Appendix Figure [8d\)](#page-23-0).

**Query input matches an in-context example.** We choose the query input to match one of the in-context examples inputs chosen uniformly at random. In this case, the model achieves errors 0.001, 0.001, 0.0005 for 10, 20, 40 examples respectively thus making close to the correct prediction, without being affected by the additional in-context examples present (Appendix Figure [8e\)](#page-23-0).

# <span id="page-7-0"></span>**5 More complex function classes**

We now turn our attention to in-context learning for more complex function classes, namely sparse linear functions, decision trees, and two-layer ReLU neural networks. Here, we are back in the setting where the distribution of prompts during inference is same as that during training (except the setting of neural networks where we evaluate on linear functions as well). The overall methodology remains the same: we sample random functions from these families and train a Transformer from scratch to approximate these functions given in-context examples. (See Appendix [A.3](#page-19-0) for more details and baselines.)

**Sparse linear functions.** First, we consider functions of the form *f*(*x*) = *w* <sup>⊤</sup>*x* where *w* ∈ **R***<sup>d</sup>* and has exactly *s* non-zero coordinates. To sample a prompt *P* = (*x*1, *f*(*x*1), . . . , *x<sup>k</sup>* , *f*(*x<sup>k</sup>* ), *x*query), we draw prompt inputs *x<sup>i</sup>* and *x*query, and a weight vector *w* from *N*(0, *I<sup>d</sup>* ), and then zero out all but *s* coordinates of *w* uniformly at random. We choose *d* = 20 and *s* = 3. In this setting, the least squares estimator is no longer optimal—one can perform better by leveraging the weight vector sparsity. One estimator that leverages sparsity is Lasso [\[Tibshirani, 1996\]](#page-17-3), which involves solving the least squares objective with an ℓ1-norm regularizer for the weight vector. We plot the performance of our model in Figure [5a,](#page-8-0) and observe that it is also able to leverage sparsity, nearly matching the performance of Lasso. Our model achieves errors 0.58 and 0.09 while Lasso achieves errors 0.62 and 0.08 for *k* = 5 and 10 respectively. Note that, unlike least squares, Lasso does not have a closed form expression and involves iterative minimization of the regularized objective, yet the Transformer is able to achieve comparable performance in a single forward pass.

<span id="page-8-0"></span>![](./assets/A-4-function-class-icl/_page_8_Figure_1.jpeg)

Figure 5: *Training a Transformer to in-context learn more complex function classes.* (a) A Transformer trained on prompts generated using sparse linear functions can in-context learn this class, with error decreasing at a rate similar to Lasso, and significantly better than minimum norm least squares. (b) A Transformer trained on prompts generated using random decision trees can in-context learn this class, with much better performance than greedy tree learning or tree boosting. (c) A Transformer trained on prompts generated using random 2-layer ReLU neural networks can in-context learn this class. The error decreases at a rate similar to the baseline which involves training a neural network using a variant of gradient descent with in-context examples as the training data. (d) The same model (from (c)) can in-context learn the class of linear functions. The error decreases at a rate slower than least squares, but comparable to a neural network trained using a variant of gradient descent. In all cases, the errors are normalized so that the trivial zero estimator achieves an error of 1 (dashed line).

**Decision trees.** Next, we consider the class of depth 4 decision trees with 20 dimensional inputs. A function *f* in this class is represented by a full binary tree (with 16 leaf nodes) where each non-leaf node is associated with a coordinate, and each leaf node is associated with a target value. To evaluate *f* on an input *x*, we traverse the tree starting from the root node, and go to the right child if the coordinate associated with the current node is positive and go to the left child otherwise (that is, the threshold at each node is 0). *f*(*x*) is given by the value associated with the leaf node reached at the end. To sample a random prompt *P* = (*x*1, *f*(*x*1), . . . , *x<sup>k</sup>* , *f*(*x<sup>k</sup>* ), *x*query), we draw prompt inputs *xi*s and *x*query from *N*(0, *I<sup>d</sup>* ), and *f* corresponds to a tree where the coordinates associated with the non-leaf nodes are drawn uniformly at random from

{1, 2, . . . , *d*} and the values associated with the leaf nodes are drawn from *N*(0, 1). In Figure [5b,](#page-8-0) we show that Transformers can be trained to in-context learn this class, with performance much better than greedy tree learning and boosting (via XGBoost [\[Chen and Guestrin, 2016\]](#page-13-4)). With *k* = 100 in-context examples, the Transformer achieves an error of 0.12 whereas greedy learning achieves an error of 0.80 and XGBoost achieves an error of 0.62.

Since the decision trees in our function class predict solely based on the sign of each coordinate of *x<sup>i</sup>* , we also consider a baseline where we provide the greedy learning and XGBoost algorithms with the signs of each *xi* instead. This significantly improves their performance—at 100 in-context examples, greedy achieves an error of 0.50 and XGBoost an error if 0.31—but they still perform much worse than the trained Transformer.

Note that, in general, we do not have a good understanding of the space of efficient algorithms for learning decision trees, and the conditions under which known heuristics work [\[Blanc et al., 2021,](#page-13-5) [Brutzkus](#page-13-6) [et al., 2020\]](#page-13-6). At the same time, we found that Transformers can be trained to directly discover such an algorithm for the prompt distribution we considered. This suggests an intriguing possibility where we might be able to reverse engineer the algorithm encoded by a Transformer to obtain new sample efficient algorithms for existing learning problems.

**Two-layer ReLU neural networks.** Finally, we consider the class of two layer ReLU neural networks containing functions of the form *f*(*x*) = ∑ *r i*=1 *α<sup>i</sup> σ*(*w* ⊤ *i x*), where *α<sup>i</sup>* ∈ **R**, *w<sup>i</sup>* ∈ **R***<sup>d</sup>* and *σ*(·) = max(0, ·) is the ReLU activation function. To draw a random prompt *P* = (*x*1, *f*(*x*1), . . . , *x<sup>k</sup>* , *f*(*x<sup>k</sup>* ), *x*query), we sample prompt inputs *xi*s and *x*query from *N*(0, *I<sup>d</sup>* ), along with network parameters *ai*s and *wi*s from *N*(0, 2/*r*) and *N*(0, *I<sup>d</sup>* ) respectively. We set the input dimension *d* to 20 and the number of the hidden nodes *r* to 100. In Figure [5c,](#page-8-0) we show that Transformers can be trained to in-context learn this class of functions. In fact, the Transformer performs comparably to the baseline which involves training a two-layer neural network of the same architecture on in-context examples using Adam [\[Kingma and Ba, 2014\]](#page-15-5), a variant of gradient descent (see Appendix [A.3](#page-19-0) for details). Specifically, for *k* = 100 in-context examples, both the Transformer and the neural network trained on in-context examples achieve an error of 0.17.

Moreover, the model trained to in-context learn two-layer neural networks is also able to in-context learn linear functions (for which it is not explicitly trained), albeit with a rate slower than least squares, but comparable to a neural network trained on in-context examples generated using a linear function (Figure [5d\)](#page-8-0). For *k* = 20, 50, and 100 in-context examples respectively, the Transformer achieves error 0.34, 0.05, and 0.01, and the two-layer network achieves error 0.37, 0.04, and 0.003 (the least squares estimator achieves error 0 for *k* ≥ 20).

# <span id="page-9-0"></span>**6 Investigating what matters for in-context learning**

We now return to the setting of training models to in-context learn linear functions and explore different factors that lead to successful in-context learning.

**Problem Dimension and Capacity.** In Section [3](#page-3-1) and [4,](#page-5-1) we saw that Transformer models can be trained to in-context learn 20-dimensional linear functions accurately and relatively robustly. To explore the interplay between problem dimensionality and capacity, we also consider models with fewer parameters (see Appendix [A.1\)](#page-18-1) and train each architecture on {10, 30, 40, 50}-dimensional problems. In Figure [6,](#page-10-0) we plot the model error with 2*d* in-context examples as we vary the problem dimension *d* and the model capacity. In the standard setting, i.e., when the training and inference time prompt distributions are the same, we observe that the error decreases as we increase the capacity or reduce the problem dimensionality (see Figure [6a\)](#page-10-0). Thus, model capacity helps perform accurate in-context learning. For out-of-distribution prompts, we observe that the settings where the input covariance is skewed or where in-context example inputs and query inputs lie in different orthants are particularly challenging, especially for higher dimensional problems. However, the error decreases considerably (in most cases) as we increase the model capacity, even when absolute decrease in the standard error is small (see Figure [6b](#page-10-0) and [6c\)](#page-10-0). See Appendix [B.3](#page-24-0) for additional plots.

<span id="page-10-0"></span>![](./assets/A-4-function-class-icl/_page_10_Figure_0.jpeg)

Figure 6: *Understanding the effect of model capacity and problem dimension on in-context learning performance for in-distribution (a) and out-of-distribution (b,c) prompts.* We train Transformers to in-context learn linear functions and plot the error with 2*d* in-context examples as we vary problem dimension *d* and model capacity. Capacity helps with in-context learning in most cases, especially on out-of-distribution prompts (even when the absolute gains in the in-distribution setting are small). We train 3 models in each case with different random seeds, and show the median error (solid lines), and the minimum and maximum errors (shaded region). (See Appendix [B.4](#page-25-0) for training variance analysis.)

**Curriculum.** We train our models using curriculum learning. That is, we initially draw the prompt inputs from a fixed 5 dimensional subspace (by setting some of the coordinates to 0) with prompt length 11 (number of input-output pairs), and increase the subspace dimension by 1 and prompt length by 2 every 2, 000 training steps, until the subspace dimension reaches the ambient dimension *d* and prompt length reaches 2*d* + 1 (see Appendix [A.2](#page-18-2) for details). This process can also be viewed as gradually increasing the complexity of the function class. This speeds up training drastically, especially for higher dimensional problems: for dimension 50, the loss barely decreases through the 500k training steps without curriculum but reaches close to the optimum with curriculum. For the 20 dimensional problem where we were able to train the model without curriculum within the training (step count) budget, we did not observe any qualitative difference in accuracy or robustness compared to the model trained with curriculum. We include plots comparing the speed and accuracy of training with and without curriculum in Appendix [B.5.](#page-27-0)

Notably, when training Transformers without curriculum, there is an initial—relatively long—period in training where the loss does not decrease, followed by a period of sharp decrease. The length of this period varies with training randomness and seems to increase on average with problem dimension. Understanding the model just before and after this transition moment is a promising future direction, which can give insights into the emergence of in-context learning. Interestingly, [Olsson et al.](#page-15-3) [\[2022\]](#page-15-3) observe a similar jump in the in-context learning ability of a language model which they attribute to the formation of "induction heads".

**Number of distinct prompts or functions seen during training.** To estimate the amount of training data required for in-context learning, we perform two ablation studies. In the first study, we limit the number of distinct prompts seen during training. That is, we create a set of *n<sup>p</sup>* randomly generated prompts (as described in Section [2\)](#page-2-0), and sample prompts from this set during training (here, we train without curriculum, as it would introduce additional prompts during the warmup phase). In the second study, we only limit the number of distinct functions used for training. That is we create a set of *n<sup>w</sup>* randomly chosen vectors (corresponding to *n<sup>w</sup>* linear functions) and sample weight vectors uniformly from that set to generate the training prompts (the inputs are still sampled from *N*(0, *I<sup>d</sup>* ) for each training prompt). We find that the amount of training data required is relatively small: non-trivial in-context learning is possible with *n<sup>p</sup>* = 100k or *n<sup>w</sup>* = 1k, and the error drops close to that of the unrestricted model (discussed in Section [3\)](#page-3-1) with *n<sup>p</sup>* = 1M or *n<sup>w</sup>* = 10k (details in Appendix [B.6\)](#page-29-0). For context, in Section [3,](#page-3-1) the model is trained on fresh prompts each step, thus encountering 32M distinct functions and prompts (500k training steps with 64 prompts/batch).

# **7 Related work**

**In-context learning.** Since [Brown et al.](#page-13-0) [\[2020\]](#page-13-0) demonstrated the in-context learning ability of GPT-3, there has been a significant interest in improving and understanding this capability [\[Liu et al., 2021,](#page-15-6) [Min et al.,](#page-15-7) [2021a,](#page-15-7) [Zhao et al., 2021,](#page-17-4) [Lu et al., 2021b,](#page-15-8) [Rubin et al., 2021,](#page-16-5) [Min et al., 2021b,](#page-15-9) [Chen et al., 2021,](#page-14-1) [Mishra et al.,](#page-15-10) [2021,](#page-15-10) [Lampinen et al., 2022\]](#page-15-11). The works most relevant to ours are as follows. [Xie et al.](#page-17-5) [\[2022\]](#page-17-5) propose a Bayesian inference framework explaining how in-context learning works despite formatting differences between training and inference distributions. [Razeghi et al.](#page-16-6) [\[2022\]](#page-16-6) show that in-context learning for numerical reasoning tasks is better for instances whose terms are more prevalent in training data. [Min et al.](#page-15-7) [\[2021a\]](#page-15-7) demonstrate tasks where in-context learning works even when the prompt outputs are chosen randomly, questioning to what extent these models are truly learning new tasks on-the-fly, while [Rong](#page-16-7) [\[2021\]](#page-16-7) gives examples of novel tasks on which these models demonstrate on-the-fly learning ability. [Chan et al.](#page-13-7) [\[2022\]](#page-13-7) demonstrate that distributional properties such as long-tailedness are crucial for in-context learning on an image-based few-shot dataset. [Olsson et al.](#page-15-3) [\[2022\]](#page-15-3) and [Elhage et al.](#page-14-2) [\[2021\]](#page-14-2) consider a different framing of in-context learning, referring to any model behavior that utilizes information in a prompt to make predictions that improve with prompt size. They hypothesize the existence of special circuits inside Transformer models responsible for in-context learning, that can complete prompts by copying previous similar patterns in the prompt sequence. [Pesut](#page-16-8) [\[2022\]](#page-16-8) and [Dinh et al.](#page-14-3) [\[2022,](#page-14-3) Table 16] consider in-context learning for small tabular datasets and learning problems in one and two dimensions, and show that GPT-3 can obtain non-trivial accuracy. Our work contributes to and complements this line of work, by posing in-context learning as a well-defined problem of learning function classes at inference time, and empirically investigating training models that in-context learn simple function classes.

**Transformers.** There is a long line of work investigating the capabilities [\[Vaswani et al., 2017,](#page-17-1) [Dehghani](#page-14-4) [et al., 2018,](#page-14-4) [Yun et al., 2019,](#page-17-6) [Pérez et al., 2019,](#page-16-9) [Yao et al., 2021,](#page-17-7) [Bhattamishra et al., 2020b,](#page-13-8) [Zhang et al., 2022\]](#page-17-8), limitations [\[Hahn, 2020,](#page-14-5) [Bhattamishra et al., 2020a\]](#page-13-9), applications [\[Lu et al., 2021a,](#page-15-12) [Dosovitskiy et al., 2020,](#page-14-6) [Parmar et al., 2018\]](#page-16-10), and internal workings [\[Elhage et al., 2021,](#page-14-2) [Snell et al., 2021,](#page-16-11) [Weiss et al., 2021,](#page-17-9) [Edelman](#page-14-7) [et al., 2022,](#page-14-7) [Olsson et al., 2022\]](#page-15-3) of Transformer models. Most similar to our work, [Müller et al.](#page-15-13) [\[2021\]](#page-15-13) and [Nguyen and Grover](#page-15-14) [\[2022\]](#page-15-14) demonstrate the ability of Transformer models to solve prediction tasks using the input context, albeit in different settings. [Müller et al.](#page-15-13) [\[2021\]](#page-15-13) introduce a "Prior-data fitted transformer network" that is trained to approximate Bayesian inference with priors such as Gaussian processes and Bayesian neural networks, and use it to perform downstream tasks such as tabular dataset classification and few-shot image classification. [Nguyen and Grover](#page-15-14) [\[2022\]](#page-15-14) introduce Transformer neural processes, building on prior work on neural processes [\[Garnelo et al., 2018b](#page-14-8)[,a,](#page-14-9) [Kim et al., 2019\]](#page-14-10), and show that they achieve state-of-the art performance on tasks such as image completion and contextual multi-armed bandits. Our work complements these works, focusing on understanding the in-context learning ability of Transformers for various simple function classes and the extent to which this ability extrapolates beyond the training distribution.

**Meta learning.** Training a model to perform in-context learning can be viewed as an instance of the more general learning-to-learn or meta-learning paradigm [\[Schmidhuber, 1987,](#page-16-1) [Naik and Mammone, 1992,](#page-15-2) [Thrun](#page-17-0) [and Pratt, 2012\]](#page-17-0). Typical approaches from this extensive line of work (see [\[Hospedales et al., 2020\]](#page-14-11) for a survey) include: training a meta-learner on how to update the parameters of a downstream learner [\[Bengio](#page-13-10) [et al., 1995,](#page-13-10) [Li and Malik, 2016\]](#page-15-15), learning parameter initializations from which one can quickly train for many downstream tasks [\[Finn et al., 2017,](#page-14-12) [Ravi and Larochelle, 2017\]](#page-16-12), learning latent embeddings that allow for effective similarity search [\[Snell et al., 2017\]](#page-16-13). Most relevant to our setting are approaches that directly take as input examples from a downstream task and a query input and produce the corresponding output [\[Hochreiter et al., 2001,](#page-14-13) [Mishra et al., 2018,](#page-15-16) [Santoro et al., 2016,](#page-16-14) [Garnelo et al., 2018b](#page-14-8)[,a,](#page-14-9) [Kirsch and](#page-15-17) [Schmidhuber, 2021\]](#page-15-17). Our work contributes to this line of work, by investigating the learning-to-learn abilities of Transformer models in a well-defined setting.

**Data-driven algorithm design.** Another line of work aims to discover algorithms that perform well on a distribution of inputs [\[Horvitz et al., 2001,](#page-14-14) [Xu et al., 2008,](#page-17-10) [Vinyals et al., 2015,](#page-17-11) [Bello et al., 2016,](#page-13-11) [Khalil et al.,](#page-14-15) [2017,](#page-14-15) [Selsam et al., 2018,](#page-16-15) [Schwarzschild et al., 2021\]](#page-16-16) (as opposed to algorithms with guarantees on their worst-case performance). See [Balcan](#page-13-12) [\[2020\]](#page-13-12) for a survey on advancements on the theoretical foundations of such algorithms. Our work can be viewed as part of this line of work, as we train Transformer models to discover algorithms for different learning problems.

## **8 Discussion**

In this work, we formalize and study the question: can we train models that learn different classes of functions in-context? We show that Transformer models trained from scratch can in-context learn the class of linear functions, with performance comparable to the optimal least squares estimator, even under distribution shifts. Moreover, we show that in-context learning is also possible for sparse linear functions, decision trees, and two-layer neural networks; learning problems which are solved in practice with involved iterative algorithms such as gradient descent.

At the same time, understanding the implications of our results for language models requires further investigation. A pertinent question regarding the in-context learning capabilities of language models is how they leverage in-context examples [\[Min et al., 2022\]](#page-15-1). Our results demonstrate that Transformers can encode complex learning algorithms that utilize in-context examples in a far-from-trivial manner. In fact, this is the case for standard Transformer architectures trained with standard optimization procedures. The extent to which such non-trivial in-context learning behavior exists in large language models is still open, but we believe that our work takes a step towards formalizing and investigating this question.

Our work lays the groundwork for several future directions.

**Complexity of in-context learning.** We empirically show that model capacity helps in performing incontext learning accurately and robustly. This raises the question: How does the in-context learning loss [\(1\)](#page-1-2) depend on the complexity of the function class F, the capacity of model *M*, and the number of prompts used to train *M*. Even the right notion of complexity of F is unclear and may depend on the model family. Understanding this question for models explicitly trained to perform in-context learning may suggest an upper bound for the in-context learning performance of models such as GPT-3 that have not been explicitly trained for this purpose.

**Curriculum learning.** Within our framework, there is natural notion of curriculum learning where during training, we gradually increase the complexity of the function class learned in-context. This leads to drastic speed-ups in training. What is the reason behind such a speedup? Are similar speedups also possible for training large language models? Understanding these questions can have implications for training of models on large real-world datasets, potentially reducing the time and energy used for training.

**Inductive bias of model families.** Our framework presents an opportunity to understand and compare the inductive biases of different model families (e.g., Transformers vs. LSTMs) in a well-defined setting. For instance, a concrete question is: Are there function classes that are easier to in-context learn using Transformers but harder for LSTMs and vice-versa?

**Understanding the learning algorithms encoded in Transformers.** The models we train are able to perform in-context learning, and are thus themselves encoding learning algorithms. A worthwhile research direction would be to investigate the internal workings of these models and better understand the exact learning algorithms that they encode. Moreover, for settings such as decision trees, we do not have a good understanding of what the optimal learning algorithms are. Nevertheless, in Section [5](#page-7-0) we found that Transformers are able to discover sample efficient algorithms when being trained to perform in-context

learning. This suggests an intriguing possibility where we might be able to reverse engineer the Transformer to obtain better learning algorithms for such problems.

## **Acknowledgements**

We thank Niladri Chatterji, Micah Goldblum, Rohith Kuditipudi, Shibani Santurkar, Carmen Strassle, Mirac Sugzun, and Li-Yang Tan for helpful conversations, and anonymous reviewers for helpful comments.

SG was funded by a Stanford Interdisciplinary Graduate Fellowship. DT was funded by Open Philanthropy, and partially supported by NSF Award CCF-1813049. GV was supported by NSF Awards CCF-1704417, CCF-1813049, Frontier Award 1804222 and DOE award DE-SC0019205. We performed our experiments on the Stanford NLP cluster.

## **References**

- <span id="page-13-12"></span>Maria-Florina Balcan. Data-driven algorithm design. In Tim Roughgarden, editor, *Beyond Worst Case Analysis of Algorithms*. Cambridge University Press, 2020.
- <span id="page-13-3"></span>Mikhail Belkin, Daniel Hsu, Siyuan Ma, and Soumik Mandal. Reconciling modern machine-learning practice and the classical bias–variance trade-off. *Proceedings of the National Academy of Sciences*, 2019.
- <span id="page-13-11"></span>Irwan Bello, Hieu Pham, Quoc V Le, Mohammad Norouzi, and Samy Bengio. Neural combinatorial optimization with reinforcement learning. *arXiv preprint arXiv:1611.09940*, 2016.
- <span id="page-13-10"></span>Samy Bengio, Yoshua Bengio, Jocelyn Cloutier, and Jan Gecsei. On the optimization of a synaptic learning rule. In *Preprints Conf. Optimality in Artificial and Biological Neural Networks*, 1995.
- <span id="page-13-2"></span>Yoshua Bengio, Jérôme Louradour, Ronan Collobert, and Jason Weston. Curriculum learning. In *International Conference on Machine Learning (ICML)*, pages 41–48, 2009.
- <span id="page-13-9"></span>Satwik Bhattamishra, Kabir Ahuja, and Navin Goyal. On the ability and limitations of transformers to recognize formal languages. *arXiv preprint arXiv:2009.11264*, 2020a.
- <span id="page-13-8"></span>Satwik Bhattamishra, Arkil Patel, and Navin Goyal. On the computational power of transformers and its implications in sequence modeling. *arXiv preprint arXiv:2006.09286*, 2020b.
- <span id="page-13-1"></span>Sid Black, Stella Biderman, Eric Hallahan, Quentin Anthony, Leo Gao, Laurence Golding, Horace He, Connor Leahy, Kyle McDonell, Jason Phang, et al. Gpt-neox-20b: An open-source autoregressive language model. *arXiv preprint arXiv:2204.06745*, 2022.
- <span id="page-13-5"></span>Guy Blanc, Jane Lange, Mingda Qiao, and Li-Yang Tan. Decision tree heuristics can fail, even in the smoothed setting. *arXiv preprint arXiv:2107.00819*, 2021.
- <span id="page-13-0"></span>Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language models are few-shot learners. *Neural Information Processing Systems (NeurIPS)*, 2020.
- <span id="page-13-6"></span>Alon Brutzkus, Amit Daniely, and Eran Malach. Id3 learns juntas for smoothed product distributions. In *Conference on Learning Theory*, pages 902–915. PMLR, 2020.
- <span id="page-13-7"></span>Stephanie CY Chan, Adam Santoro, Andrew K Lampinen, Jane X Wang, Aaditya Singh, Pierre H Richemond, Jay McClelland, and Felix Hill. Data distributional properties drive emergent few-shot learning in transformers. *arXiv preprint arXiv:2205.05055*, 2022.
- <span id="page-13-4"></span>Tianqi Chen and Carlos Guestrin. Xgboost: A scalable tree boosting system. In *conference on knowledge discovery and data mining (KDD)*, 2016.
- <span id="page-14-1"></span>Yanda Chen, Ruiqi Zhong, Sheng Zha, George Karypis, and He He. Meta-learning via language model in-context tuning. *arXiv preprint arXiv:2110.07814*, 2021.
- <span id="page-14-4"></span>Mostafa Dehghani, Stephan Gouws, Oriol Vinyals, Jakob Uszkoreit, and Łukasz Kaiser. Universal transformers. *arXiv preprint arXiv:1807.03819*, 2018.
- <span id="page-14-3"></span>Tuan Dinh, Yuchen Zeng, Ruisu Zhang, Ziqian Lin, Shashank Rajput, Michael Gira, Jy-yong Sohn, Dimitris Papailiopoulos, and Kangwook Lee. Lift: Language-interfaced fine-tuning for non-language machine learning tasks. *arXiv preprint arXiv:2206.06565*, 2022.
- <span id="page-14-6"></span>Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, et al. An image is worth 16x16 words: Transformers for image recognition at scale. *arXiv preprint arXiv:2010.11929*, 2020.
- <span id="page-14-7"></span>Benjamin L Edelman, Surbhi Goel, Sham Kakade, and Cyril Zhang. Inductive biases and variable creation in self-attention mechanisms. In *International Conference on Machine Learning (ICML)*, 2022.
- <span id="page-14-2"></span>Nelson Elhage, Neel Nanda, Catherine Olsson, Tom Henighan, Nicholas Joseph, Ben Mann, Amanda Askell, Yuntao Bai, Anna Chen, Tom Conerly, Nova DasSarma, Dawn Drain, Deep Ganguli, Zac Hatfield-Dodds, Danny Hernandez, Andy Jones, Jackson Kernion, Liane Lovitt, Kamal Ndousse, Dario Amodei, Tom Brown, Jack Clark, Jared Kaplan, Sam McCandlish, and Chris Olah. A mathematical framework for transformer circuits. *Transformer Circuits Thread*, 2021. https://transformercircuits.pub/2021/framework/index.html.
- <span id="page-14-0"></span>Jeffrey L Elman. Learning and development in neural networks: The importance of starting small. *Cognition*, 1993.
- <span id="page-14-12"></span>Chelsea Finn, Pieter Abbeel, and Sergey Levine. Model-agnostic meta-learning for fast adaptation of deep networks. In *International conference on machine learning (ICML)*, 2017.
- <span id="page-14-16"></span>Jerome H Friedman. Greedy function approximation: a gradient boosting machine. *Annals of statistics*, 2001.
- <span id="page-14-9"></span>Marta Garnelo, Dan Rosenbaum, Christopher Maddison, Tiago Ramalho, David Saxton, Murray Shanahan, Yee Whye Teh, Danilo Rezende, and SM Ali Eslami. Conditional neural processes. In *International Conference on Machine Learning*, pages 1704–1713. PMLR, 2018a.
- <span id="page-14-8"></span>Marta Garnelo, Jonathan Schwarz, Dan Rosenbaum, Fabio Viola, Danilo J Rezende, SM Eslami, and Yee Whye Teh. Neural processes. *arXiv preprint arXiv:1807.01622*, 2018b.
- <span id="page-14-5"></span>Michael Hahn. Theoretical limitations of self-attention in neural sequence models. *Transactions of the Association for Computational Linguistics*, 2020.
- <span id="page-14-13"></span>Sepp Hochreiter, A Steven Younger, and Peter R Conwell. Learning to learn using gradient descent. In *International conference on artificial neural networks (ICANN)*, 2001.
- <span id="page-14-14"></span>Eric Horvitz, Yongshao Ruan, Carla Gomes, Henry Kautz, Bart Selman, and Max Chickering. A bayesian approach to tackling hard computational problems (preliminary report). *Electronic Notes in Discrete Mathematics*, 2001.
- <span id="page-14-11"></span>Timothy Hospedales, Antreas Antoniou, Paul Micaelli, and Amos Storkey. Meta-learning in neural networks: A survey. *arXiv preprint arXiv:2004.05439*, 2020.
- <span id="page-14-15"></span>Elias Khalil, Hanjun Dai, Yuyu Zhang, Bistra Dilkina, and Le Song. Learning combinatorial optimization algorithms over graphs. *Neural Information Processing Systems (NeurIPS)*, 2017.
- <span id="page-14-10"></span>Hyunjik Kim, Andriy Mnih, Jonathan Schwarz, Marta Garnelo, Ali Eslami, Dan Rosenbaum, Oriol Vinyals, and Yee Whye Teh. Attentive neural processes. *arXiv preprint arXiv:1901.05761*, 2019.
- <span id="page-15-5"></span>Diederik P Kingma and Jimmy Ba. Adam: A method for stochastic optimization. *arXiv preprint arXiv:1412.6980*, 2014.
- <span id="page-15-17"></span>Louis Kirsch and Jürgen Schmidhuber. Meta learning backpropagation and improving it. *Neural Information Processing Systems (NeurIPS)*, 2021.
- <span id="page-15-11"></span>Andrew K Lampinen, Ishita Dasgupta, Stephanie CY Chan, Kory Matthewson, Michael Henry Tessler, Antonia Creswell, James L McClelland, Jane X Wang, and Felix Hill. Can language models learn from explanations in context? *arXiv preprint arXiv:2204.02329*, 2022.
- <span id="page-15-15"></span>Ke Li and Jitendra Malik. Learning to optimize. *arXiv preprint arXiv:1606.01885*, 2016.
- <span id="page-15-0"></span>Opher Lieber, Or Sharir, Barak Lenz, and Yoav Shoham. Jurassic-1: Technical details and evaluation. *White Paper. AI21 Labs*, 2021.
- <span id="page-15-6"></span>Jiachang Liu, Dinghan Shen, Yizhe Zhang, Bill Dolan, Lawrence Carin, and Weizhu Chen. What makes good in-context examples for gpt-3? *arXiv preprint arXiv:2101.06804*, 2021.
- <span id="page-15-12"></span>Kevin Lu, Aditya Grover, Pieter Abbeel, and Igor Mordatch. Pretrained transformers as universal computation engines. *arXiv preprint arXiv:2103.05247*, 2021a.
- <span id="page-15-8"></span>Yao Lu, Max Bartolo, Alastair Moore, Sebastian Riedel, and Pontus Stenetorp. Fantastically ordered prompts and where to find them: Overcoming few-shot prompt order sensitivity. *arXiv preprint arXiv:2104.08786*, 2021b.
- <span id="page-15-7"></span>Sewon Min, Mike Lewis, Hannaneh Hajishirzi, and Luke Zettlemoyer. Noisy channel language model prompting for few-shot text classification. *arXiv preprint arXiv:2108.04106*, 2021a.
- <span id="page-15-9"></span>Sewon Min, Mike Lewis, Luke Zettlemoyer, and Hannaneh Hajishirzi. Metaicl: Learning to learn in context. *arXiv preprint arXiv:2110.15943*, 2021b.
- <span id="page-15-1"></span>Sewon Min, Xinxi Lyu, Ari Holtzman, Mikel Artetxe, Mike Lewis, Hannaneh Hajishirzi, and Luke Zettlemoyer. Rethinking the role of demonstrations: What makes in-context learning work? *arXiv preprint arXiv:2202.12837*, 2022.
- <span id="page-15-16"></span>Nikhil Mishra, Mostafa Rohaninejad, Xi Chen, and Pieter Abbeel. A simple neural attentive meta-learner. In *International Conference on Learning Representations (ICLR)*, 2018.
- <span id="page-15-10"></span>Swaroop Mishra, Daniel Khashabi, Chitta Baral, Yejin Choi, and Hannaneh Hajishirzi. Reframing instructional prompts to gptk's language. *arXiv preprint arXiv:2109.07830*, 2021.
- <span id="page-15-13"></span>Samuel Müller, Noah Hollmann, Sebastian Pineda Arango, Josif Grabocka, and Frank Hutter. Transformers can do bayesian inference. *arXiv preprint arXiv:2112.10510*, 2021.
- <span id="page-15-2"></span>Devang K Naik and Richard J Mammone. Meta-neural networks that learn by learning. In *International Joint Conference on Neural Networks (IJCNN)*, 1992.
- <span id="page-15-4"></span>Preetum Nakkiran. More data can hurt for linear regression: Sample-wise double descent. *arXiv preprint arXiv:1912.07242*, 2019.
- <span id="page-15-14"></span>Tung Nguyen and Aditya Grover. Transformer neural processes: Uncertainty-aware meta learning via sequence modeling. *arXiv preprint arXiv:2207.04179*, 2022.
- <span id="page-15-3"></span>Catherine Olsson, Nelson Elhage, Neel Nanda, Nicholas Joseph, Nova DasSarma, Tom Henighan, Ben Mann, Amanda Askell, Yuntao Bai, Anna Chen, Tom Conerly, Dawn Drain, Deep Ganguli, Zac Hatfield-Dodds, Danny Hernandez, Scott Johnston, Andy Jones, Jackson Kernion, Liane Lovitt, Kamal Ndousse, Dario Amodei, Tom Brown, Jack Clark, Jared Kaplan, Sam McCandlish, and Chris Olah. In-context learning and induction heads. *Transformer Circuits Thread*, 2022. https://transformer-circuits.pub/2022/in-contextlearning-and-induction-heads/index.html.
- <span id="page-16-10"></span>Niki Parmar, Ashish Vaswani, Jakob Uszkoreit, Lukasz Kaiser, Noam Shazeer, Alexander Ku, and Dustin Tran. Image transformer. In *International Conference on Machine Learning (ICML)*, 2018.
- <span id="page-16-17"></span>F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, P. Prettenhofer, R. Weiss, V. Dubourg, J. Vanderplas, A. Passos, D. Cournapeau, M. Brucher, M. Perrot, and E. Duchesnay. Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 2011.
- <span id="page-16-9"></span>Jorge Pérez, Javier Marinkovi´c, and Pablo Barceló. On the turing completeness of modern neural network architectures. *arXiv preprint arXiv:1901.03429*, 2019.
- <span id="page-16-8"></span>Lovre Pesut. Who models the models that model models? an exploration of gpt-3's in-context model fitting ability, 2022. URL [https://www.alignmentforum.org/posts/c2RzFadrxkzyRAFXa/](https://www.alignmentforum.org/posts/c2RzFadrxkzyRAFXa/who-models-the-models-that-model-models-an-exploration-of) [who-models-the-models-that-model-models-an-exploration-of](https://www.alignmentforum.org/posts/c2RzFadrxkzyRAFXa/who-models-the-models-that-model-models-an-exploration-of).
- <span id="page-16-2"></span>Alec Radford, Karthik Narasimhan, Tim Salimans, and Ilya Sutskever. Improving language understanding by generative pre-training. *OpenAI blog*, 2018.
- <span id="page-16-3"></span>Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever, et al. Language models are unsupervised multitask learners. *OpenAI blog*, 2019.
- <span id="page-16-0"></span>Jack W Rae, Sebastian Borgeaud, Trevor Cai, Katie Millican, Jordan Hoffmann, Francis Song, John Aslanides, Sarah Henderson, Roman Ring, Susannah Young, et al. Scaling language models: Methods, analysis & insights from training gopher. *arXiv preprint arXiv:2112.11446*, 2021.
- <span id="page-16-12"></span>Sachin Ravi and Hugo Larochelle. Optimization as a model for few-shot learning. *International Conference for Learning Representations (ICLR)*, 2017.
- <span id="page-16-6"></span>Yasaman Razeghi, Robert L Logan IV, Matt Gardner, and Sameer Singh. Impact of pretraining term frequencies on few-shot reasoning. *arXiv preprint arXiv:2202.07206*, 2022.
- <span id="page-16-7"></span>Frieda Rong. Extrapolating to unnatural language processing with gpt-3's in-context learning: The good, the bad, and the mysterious), 2021. URL <http://ai.stanford.edu/blog/in-context-learning/>.
- <span id="page-16-5"></span>Ohad Rubin, Jonathan Herzig, and Jonathan Berant. Learning to retrieve prompts for in-context learning. *arXiv preprint arXiv:2112.08633*, 2021.
- <span id="page-16-4"></span>Terence D Sanger. Neural network learning control of robot manipulators using gradually increasing task difficulty. *IEEE transactions on Robotics and Automation*, 1994.
- <span id="page-16-14"></span>Adam Santoro, Sergey Bartunov, Matthew Botvinick, Daan Wierstra, and Timothy Lillicrap. Meta-learning with memory-augmented neural networks. In *International conference on machine learning (ICML)*, 2016.
- <span id="page-16-1"></span>Jürgen Schmidhuber. *Evolutionary principles in self-referential learning, or on learning how to learn: the meta-meta-... hook*. PhD thesis, Technische Universität München, 1987.
- <span id="page-16-16"></span>Avi Schwarzschild, Eitan Borgnia, Arjun Gupta, Furong Huang, Uzi Vishkin, Micah Goldblum, and Tom Goldstein. Can you learn an algorithm? generalizing from easy to hard problems with recurrent networks. *Neural Information Processing Systems (NeurIPS)*, 2021.
- <span id="page-16-15"></span>Daniel Selsam, Matthew Lamm, B Benedikt, Percy Liang, Leonardo de Moura, David L Dill, et al. Learning a sat solver from single-bit supervision. In *International Conference on Learning Representations (ICLR)*, 2018.
- <span id="page-16-11"></span>Charlie Snell, Ruiqi Zhong, Dan Klein, and Jacob Steinhardt. Approximating how single head attention learns. *arXiv preprint arXiv:2103.07601*, 2021.
- <span id="page-16-13"></span>Jake Snell, Kevin Swersky, and Richard Zemel. Prototypical networks for few-shot learning. *Neural Information Processing Systems (NeurIPS)*, 2017.

<span id="page-17-0"></span>Sebastian Thrun and Lorien Pratt. *Learning to learn*. Springer Science & Business Media, 2012.

- <span id="page-17-3"></span>Robert Tibshirani. Regression shrinkage and selection via the lasso. *Journal of the Royal Statistical Society: Series B (Methodological)*, 1996.
- <span id="page-17-1"></span>Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. *Neural Information Processing Systems (NeurIPS)*, 2017.
- <span id="page-17-11"></span>Oriol Vinyals, Meire Fortunato, and Navdeep Jaitly. Pointer networks. In C. Cortes, N. Lawrence, D. Lee, M. Sugiyama, and R. Garnett, editors, *Neural Information Processing Systems (NeurIPS)*, 2015.
- <span id="page-17-9"></span>Gail Weiss, Yoav Goldberg, and Eran Yahav. Thinking like transformers. In *International Conference on Machine Learning*, 2021.
- <span id="page-17-12"></span>Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement Delangue, Anthony Moi, Pierric Cistac, Tim Rault, Rémi Louf, Morgan Funtowicz, Joe Davison, Sam Shleifer, Patrick von Platen, Clara Ma, Yacine Jernite, Julien Plu, Canwen Xu, Teven Le Scao, Sylvain Gugger, Mariama Drame, Quentin Lhoest, and Alexander M. Rush. Transformers: State-of-the-art natural language processing. In *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations*. Association for Computational Linguistics (ACL), 2020.
- <span id="page-17-2"></span>Xiaoxia Wu, Ethan Dyer, and Behnam Neyshabur. When do curricula work? *arXiv preprint arXiv:2012.03107*, 2020.
- <span id="page-17-5"></span>Sang Michael Xie, Aditi Raghunathan, Percy Liang, and Tengyu Ma. An explanation of in-context learning as implicit bayesian inference. In *International Conference on Learning Representations (ICLR)*, 2022.
- <span id="page-17-10"></span>Lin Xu, Frank Hutter, Holger H Hoos, and Kevin Leyton-Brown. Satzilla: portfolio-based algorithm selection for sat. *Journal of artificial intelligence research*, 2008.
- <span id="page-17-7"></span>Shunyu Yao, Binghui Peng, Christos Papadimitriou, and Karthik Narasimhan. Self-attention networks can process bounded hierarchical languages. *arXiv preprint arXiv:2105.11115*, 2021.
- <span id="page-17-6"></span>Chulhee Yun, Srinadh Bhojanapalli, Ankit Singh Rawat, Sashank J Reddi, and Sanjiv Kumar. Are transformers universal approximators of sequence-to-sequence functions? *arXiv preprint arXiv:1912.10077*, 2019.
- <span id="page-17-8"></span>Yi Zhang, Arturs Backurs, Sébastien Bubeck, Ronen Eldan, Suriya Gunasekar, and Tal Wagner. Unveiling transformers with lego: a synthetic reasoning task. *arXiv preprint arXiv:2206.04301*, 2022.
- <span id="page-17-4"></span>Zihao Zhao, Eric Wallace, Shi Feng, Dan Klein, and Sameer Singh. Calibrate before use: Improving few-shot performance of language models. In *International Conference on Machine Learning (ICML)*, 2021.

# <span id="page-18-0"></span>**A Experimental setup**

Here, we provide additional details on our experimental setup.

### <span id="page-18-1"></span>**A.1 Model architecture**

We use architectures from the GPT-2 family [\[Radford et al., 2018\]](#page-16-2) as implemented by HuggingFace [\[Wolf](#page-17-12) [et al., 2020\]](#page-17-12) [3](#page-18-3) . Specifically, we consider the following set of configurations.

| Model    | Embedding size | #Layers | #Heads | (Total parameters) |
|----------|----------------|---------|--------|--------------------|
| Tiny     | 64             | 3       | 2      | 0.2M               |
| Small    | 128            | 6       | 4      | 1.2M               |
| Standard | 256            | 12      | 8      | 9.5M               |

We use the Standard model for the bulk of our experiments and only consider the smaller models for the capacity explorations in Section [6](#page-9-0) and Appendix [B.3.](#page-24-0) Since we train on each input once (we sample new inputs at each training step), overfitting to the training data is not an issue. Therefore, we set the Dropout probability to 0.

Out of the box, these models take as input a sequence of vectors in embedding space and output a sequence of vectors in the same space. However, the tasks we study are functions from a lower dimensional vector space (e.g., 10-50 dimensions) to a scalar value. Thus, in order to use a prompt such as *x*1, *f*(*x*1), *x*2, *f*(*x*2). . ., we need to map *xi*s and *f*(*xi*)s to vectors in embedding space. We do so by first turning the scalars *f*(*xi*) into vectors of the same dimension as *x<sup>i</sup>* by appending 0s and then applying a learnable linear transformation to map all these vectors into the embedding space. Finally, we map the model output into a scalar value through a dot product with a learnable vector.

We treat the prediction of the model at the position corresponding to *x<sup>i</sup>* (that is absolute position 2*i* − 1) as the prediction of *f*(*xi*). Due to the structure of these models, this prediction only depends on (*x<sup>j</sup>* , *f*(*xj*)) for *j* < *i* and *x<sup>i</sup>* . We ignore the model predictions at positions corresponding to *f*(*xi*).

### <span id="page-18-2"></span>**A.2 Training**

Each training prompt is produced by sampling a random function *f* from the function class we are training on, then sampling inputs *x<sup>i</sup>* from the isotropic Gaussian distribution *N*(0, *I<sup>d</sup>* ) and constructing a prompt as (*x*1, *f*(*x*1), . . . , *x<sup>k</sup>* , *f*(*x<sup>k</sup>* )). Given a prompt, we obtain model predictions *y*ˆ*<sup>i</sup>* (meant to approximate *f*(*xi*)) for each input, and compute the loss

$$
\frac{1}{k}\sum_{i=1}^k\left(\hat{y}_i-f(x_i)\right)^2.
$$

At each training step, we average the loss over a batch of randomly generated prompts (with different functions and prompt inputs), and perform an update step. We use the Adam optimizer [\[Kingma and Ba,](#page-15-5) [2014\]](#page-15-5), and train for 500,000 total steps with a batch size of 64. We use a learning rate of 10−<sup>4</sup> for all function classes and models.

**Curriculum learning.** To accelerate training, we start by training on prompt inputs *x<sup>i</sup>* lying in a smaller dimensional subspace, and with fewer inputs per prompt, and gradually increase the subspace dimension and number of prompt inputs. Specifically, we zero out all but the first *d*cur coordinates of *x<sup>i</sup>* , sample prompts of size *k*cur and leave the rest of the training process the same. We use the same schedule for all training runs for the function classes of linear functions and sparse linear functions, starting with *d*cur = 5, *k*cur = 11, and increasing *d*cur and *k*cur by 1 and 2 respectively, every 2000 steps, until *d*cur = *d*, *k*cur = 2*d* + 1. We use a slightly different schedule for 2 layer neural networks and decision trees as we want prompts with more

<span id="page-18-3"></span><sup>3</sup>[https://huggingface.co/docs/transformers/model\\_doc/gpt2](https://huggingface.co/docs/transformers/model_doc/gpt2)

inputs for these function classes. For these classes, we start with *d*cur = 5, *k*cur = 26, and increase *d*cur and *k*cur by 1 and 5 respectively, every 2000 steps, until *d*cur = *d*, *k*cur = 5*d* + 1.

Overall, with curriculum, a training prompt (*x*1, *f*(*x*1), . . . , *xk*cur , *f*(*xk*cur ) is generated by sampling a random function *f* from the function class, drawing inputs *x<sup>i</sup>* by sampling i.i.d. from *N*(0, *I<sup>d</sup>* ) and zeroing out all but the first *d*cur coordinates. Given model predictions *y*ˆ*<sup>i</sup>* , the loss is given by

$$
\frac{1}{k_{\text{cur}}} \sum_{i=1}^{k_{\text{cur}}} \left( \hat{y}_i - f(x_i) \right)^2.
$$

**Sampling random functions.** For the class of linear functions, we sample random function *f*(*x*) = *w* <sup>⊤</sup>*x* by drawing *w* ∼ *N*(0, *I<sup>d</sup>* ). For our main setting (Section [3](#page-3-1) and [4\)](#page-5-1), we set *d* = 20.

For the class of two-layer neural networks, we sample *f*(*x*) = ∑ *r i*=1 *αiσ*(*w* ⊤ *i x*), where *αi*s and *wi*s are drawn i.i.d. from *N*(0, 2/*r*) and *N*(0, *I<sup>d</sup>* ) respectively. We set *d* = 20 and *r* = 100.

For the class of *k*-sparse linear functions, we sample *f*(*x*) = *w* <sup>⊤</sup>*x* by drawing *w* ∼ *N*(0, *I<sup>d</sup>* ) and zeroing out all but *k* coordinates of *w* chosen uniformly at random from the first *d*cur coordinates (as defined in the curriculum learning description above). We set *d* = 20 and *k* = 3.

For the class of decision trees, the random function *f* is represented by a decision tree of depth 4 (with 16 leaf nodes), with 20 dimensional inputs. Each non-leaf node of the tree is associated with a coordinate selected uniformly at random from {1, 2, . . . , *d*}, and each leaf node is associated with a value drawn randomly from *N*(0, 1). To evaluate *f* on an input *x*, we traverse the tree starting from the root node, and go to the right child if the coordinate associated with the current node is positive and go to the left child otherwise. *f*(*x*) is given by the value associated with the leaf node reached at the end.

**Computational resources.** We train using a single NVIDIA GeForce RTX 3090 GPU and most training runs take 5-20 hours depending on model size and context length. For instance, for the class of linear functions, training the standard model takes 17 hours for *d* = 50, 7 hours for *d* = 20 and 5.5 hours for *d* = 10. For decision trees, training the standard model takes 17 hours. The time it takes for decision trees and 50 dimensional linear functions is higher due to larger context lengths (we train for *d* dimensional linear functions with 2*d* + 1 input-output pairs per prompt).

### <span id="page-19-0"></span>**A.3 Baselines**

**Least squares.** Minimum norm least squares is the optimal estimator for the linear regression problem. Given a prompt *P* = (*x*1, *y*1, . . . , *x<sup>k</sup>* , *y<sup>k</sup>* , *x*query), let *X* be a *k* × *d* matrix with row *i* given by *x<sup>i</sup>* , and let *y* be a *k* dimensional vector with the *i* th entry *y<sup>i</sup>* . Set *w*ˆ *<sup>T</sup>* = *X* <sup>+</sup>*y*, where *X* <sup>+</sup> denotes the Moore-Penrose pseudoinverse of *X*. The estimator predicts *M*(*P*) = *w*ˆ *<sup>T</sup>x*query.

**Averaging estimator.** This corresponds to *M*(*P*) = *w*ˆ *<sup>T</sup>x*query where *w*ˆ = <sup>1</sup> *<sup>k</sup>* ∑ *k i*=1 *xiy<sup>i</sup>* . This estimator is consistent (yet sub-optimal) when *xi*s are drawn from *N*(0, *I<sup>d</sup>* ). Unlike least squares, this estimator does not involve an inverse computation, and might be easier for a model to encode.

**Nearest neighbors.** This corresponds to setting *M*(*P*) = <sup>1</sup> *<sup>n</sup>* ∑*i*∈*<sup>S</sup> y<sup>i</sup>* . Here, *S* is the set of indices of the *n* nearest neighbors of *x*query among *x*<sup>1</sup> to *x<sup>k</sup>* . For *k* < *n*, we average over all the *yi*s from 1 to *k*, and for *k* = 0, we set *M*(*P*) = 0. We consider the nearest neighbors baselines as it might be easier for a Transformer model to encode using self-attention compared to least squares.

**Lasso.** We use this baseline for sparse linear functions (Section [5\)](#page-7-0). This corresponds to *M*(*P*) = *w*ˆ *<sup>T</sup>x*query, where *w*ˆ minimizes the ℓ1-norm regularized least squares objective:

$$
\min_{\hat{w}} \frac{1}{2k} ||y - X\hat{w}||_2^2 + \alpha ||\hat{w}||_1.
$$

We try different values of *α* ∈ {1, 10−<sup>1</sup> , 10−<sup>2</sup> , 10−<sup>3</sup> , 10−4}, and report the best solution (achieving the smallest error with 10 in-context examples) corresponding to *α* = 10−<sup>2</sup> . To solve the optimization problem, we use the Lasso implementation from Scikit-learn [\[Pedregosa et al., 2011\]](#page-16-17) [4](#page-20-0) .

**Greedy Tree Learning.** We use this baseline for the class of decision trees. This corresponds to greedily learning a decision tree using the in-context examples, and using it to classify the query input. To construct the tree, at each node (starting from a root node), we choose a coordinate for partitioning the examples into two sets, so as to minimize the variance of *yi*s in each set, averaged across the two sets. The value associated with a leaf node is the average *y<sup>i</sup>* value of the examples belonging to it. We use Scikit-learn's decision tree regressor [\[Pedregosa et al., 2011\]](#page-16-17) [5](#page-20-1) implementation for this, with all the arguments set to their default value except the max\_depth argument which is set to 2. We considered values {1, 2, 3, 4, 5, 6, unbounded} for the maximum depth and chose the value that performs best at 100 in-context examples which was 2 (which differs from the decision trees sampled from the function class which have depth 4). We also considered a baseline where we learn this tree using only the signs of each *x<sup>i</sup>* coordinate—after all, the decision tree we are trying to learn depends only on the signs of *x<sup>i</sup>* . In this case, we found the optimal depth to be 4.

**Tree boosting.** For the class of decision trees, we also consider a tree boosting baseline that corresponds to learning an ensemble of decision trees (see [Friedman](#page-14-16) [\[2001\]](#page-14-16) for a description of the general framework). Specifically, we use the XGBoost library [\[Chen and Guestrin, 2016\]](#page-13-4) [6](#page-20-2) , an implementation commonly used for a wide range of real-world machine learning tasks.

We performed a hyperpameter search by considering {1, 2, 5, 10, 50, 100, 200, 400} estimators in the ensemble (equivalent to number of boosting rounds), a learning rate of {0.001, 0.01, 0.1, 0.3, 0.6, 1, 3}, and a maximum depth of {1, 2, 3, 4, 6, 10, 16}. In general, we found the performance of the learning algorithm to be quite robust. We chose the hyperparameters obtaining the best performance with 100 training examples, corresponding to 50 estimators, a maximum depth of 4, and a learning rate f 0.1. We found these hyperparameters to also be optimal when learning based on the signs of each *x<sup>i</sup>* .

**Learning neural networks with gradient descent.** We use this baseline for the class of two-layer neural networks (Section [5\)](#page-7-0). This corresponds to training a two-layer neural network on the in-context examples, and outputting its prediction on the query point. That is, *M*(*P*) = ˆ *f*(*x*query), where

$$
\hat{f}(x_{\text{query}}) = \sum_{i=1}^{r} \hat{\alpha}_i \sigma(\hat{\omega}_i^{\top} x_{\text{query}}).
$$

Here, *σ*(·) is the ReLU activation. We find parameters *α*ˆ*<sup>i</sup>* , *w*ˆ*<sup>i</sup>* by minimizing the squared error of the prediction for the in-context examples

$$
\sum_{i=1}^k \left(\hat{f}(x_i) - f(x_i)\right)^2,
$$

using the Adam optimizer. We use a batch size of 10 (we use full batch when the number of in-context examples is less than 10) with 5000 optimization steps, and set *r* = 100. We use a learning rate of 5 · 10−<sup>3</sup> in the case when the data is generated using a neural network, and a learning rate of 5 · 10−<sup>2</sup> when the data is generated using a linear function. We consider the setting with 100 in-context examples, and do a hyperparameter grid search over learning rate ∈ {5 · 10−<sup>4</sup> , 5 · 10−<sup>3</sup> , 5 · 10−<sup>2</sup> , 5 · 10−<sup>1</sup> , 5}, *r* ∈ {100, 400}, batch size ∈ {10, 100}, optimization algorithm ∈ {adam, sgd}. All the hyperparameter settings in this grid led to a similar or worse performance compared to the hyperparameter setting we choose.

<span id="page-20-0"></span><sup>4</sup> [https://scikit-learn.org/stable/modules/generated/sklearn.linear\\_model.Lasso.html](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html)

<span id="page-20-1"></span><sup>5</sup> <https://scikit-learn.org/stable/modules/tree.html#regression>

<span id="page-20-2"></span><sup>6</sup> <https://github.com/dmlc/xgboost>

# **B Additional experimental results**

### <span id="page-21-0"></span>**B.1 Robustness to query scale**

<span id="page-21-1"></span>In Figure [7,](#page-21-1) we show that the trained model is quite robust to scaling the query input (while keeping the in-context examples fixed): the error does not increase much as we scale up the query input by a factor of up to 2, or scale down by a factor of up to 16, and degrades slowly after that.

![](./assets/A-4-function-class-icl/_page_21_Figure_3.jpeg)

Figure 7: *Robustness to the scale of query input.* For a fixed set of in-context examples, we measure the model's error as we scale the query input by a scalar.

### <span id="page-22-0"></span>**B.2 Out-of-distribution prompts**

Here, we describe the structure of our out-of-distribution prompts (cf. Section [4\)](#page-5-1), and show the corresponding plots (Figure [8\)](#page-23-0). To avoid conflating factors, we normalize the prompt inputs such that their expected norm is equal to the expected norm of inputs during training and investigate the role of scaling these inputs separately. We summarize how these prompts deviate from those seen during training in the table below.

| Prompting strategy                                              | Dtrain<br>Dtest<br≯=<br>X<br>X | Dtrain<br>Dtest<br≯=<br>F<br>F | Dtest<br>Dtest<br>query ̸=<br>X |
|-----------------------------------------------------------------|---------------------------------|---------------------------------|---------------------------------|
| Skewed covariance<br>d/2-dimensional subspace<br>Scale inputs   | ✓<br>✓<br>✓                     |                                 |                                 |
| Noisy output<br>Scale weights                                   |                                 | ✓<br>✓                          |                                 |
| Different Orthants<br>Orthogonal query<br>Query matches example | ✓                               |                                 | ✓<br>✓<br>✓                     |

**Skewed covariance.** (Figure [8a\)](#page-23-0) We sample inputs from *N*(0, Σ) where Σ is a skewed covariance matrix with eigenbasis chosen uniformly at random and *i* th eigenvalue proportional to <sup>1</sup>/*<sup>i</sup>* 2 .

**Low-dimensional subspace.** (Figure [8b\)](#page-23-0) We sample prompt inputs from a random *d*/2 dimensional subspace. That is, we pick a random *d*/2 dimensional subspace, and draw the prompt inputs from an isotropic Gaussian distribution restricted to this subspace. As a result, it is possible to achieve zero error after *d*/2 in-context examples.

**Prompt scale.** (Figure [9\)](#page-23-1) We consider the setting where the prompt scale between training and inference is different. We either scale the prompt inputs or the weight vectors, by a factor {1/3, 1/2, 2, 3}.

**Noisy linear regression.** (Figure [8c\)](#page-23-0) We add noise to each prompt output, that is, the *i* th output is equal to *w <sup>T</sup>x<sup>i</sup>* + *ϵ<sup>i</sup>* where *ϵ<sup>i</sup>* ∼ *N*(0, *d*/20).

**Different orthants for in-context and query inputs.** (Figure [8f\)](#page-23-0) We fix the sign of each coordinate to be positive or negative for all in-context inputs *x<sup>i</sup>* (at random), and draw *x*query (as before) i.i.d. from *N*(0, *I<sup>d</sup>* ). As a result, all in-context inputs lie in the same orthant, while the query input lies in another orthant with high probability.

**Query input orthogonal to in-context inputs.** (Figure [8d\)](#page-23-0) We choose the query input randomly in the space orthogonal to the space spanned by in-context example inputs. That is, we draw the query input from an isotropic Gaussian distribution restricted to the subspace orthogonal to the space spanned by the in-context examples. Thus, the optimal normalized error is 1 for any number of in-context examples (there can be at most *d* − 1 in-context examples for an orthogonal query to exist).

**Query input matches an in-context example.** (Figure [8e\)](#page-23-0) We set the query input equal to one of the in-context examples chosen uniformly at random. Thus it's possible to achieve zero error since the in-context examples include the correct prediction for the query input already.

<span id="page-23-0"></span>![](./assets/A-4-function-class-icl/_page_23_Figure_0.jpeg)

Figure 8: *In-context learning on out-of-distribution prompts.* We evaluate the model trained to in-context learn linear functions on prompt distribution that deviates from the training prompt distribution. In general, the model error degrades gracefully and closely tracks that of the least squares estimator.

<span id="page-23-1"></span>![](./assets/A-4-function-class-icl/_page_23_Figure_2.jpeg)

Figure 9: *In-context learning robustness to prompt scaling.* We evaluate the model trained to in-context learn linear functions when we scaled the prompt inputs *x* or the weight of the function class *w*. The model appear to be quite robust to scaling *w* but their performance degrades when scaling the inputs up or down by a factor of 3.

### <span id="page-24-0"></span>**B.3 Effect of problem dimension and model capacity**

We plot the model error for additional out-of-distribution prompts in Figure [10](#page-24-1) for 2*d* in-context examples (with the exception of orthogonal queries where we use *d* − 1 in-context examples).

Similar to the settings in Section [6](#page-9-0) (skewed covariance and different orthants), accuracy improves with capacity in most cases. One exception is scaling *x* (Figure [10e\)](#page-24-1), in which case we do not see any clear trend. In the case of noisy output (Figure [10b\)](#page-24-1), the accuracy almost saturates at 1.2M parameters, close to the error of the least squares estimator. In the case of orthogonal query input (Figure [10c\)](#page-24-1), the model achieves the optimum error of 1 even with the tiny model with 0.2M parameters.

<span id="page-24-1"></span>![](./assets/A-4-function-class-icl/_page_24_Figure_3.jpeg)

Figure 10: *The effect of model capacity and problem dimension for in-context learning performance on out-ofdistribution prompts.* We train Transformer models of varying capacity to in-context learn linear function in varying dimensions *d*. We plot the error with 2*d* in-context examples (or *d* − 1 for orthogonal queries). We find that capacity helps in most cases, with the exception of scaling *x* where we find no clear trend. For each setting, we train 3 models with different random seeds, and show the median error (solid lines), and the minimum and maximum errors (shaded region). (See Figures [6b, 6c](#page-10-0) in the main text for the corresponding plots on different-orthants and skewed-covariance.)

### <span id="page-25-0"></span>**B.4 Training variance**

In Figure [11,](#page-26-0) we show the variance in error across training runs for the standard Transformer model (9.5M parameters). We plot the squared error for 3 models (with different random seeds) each for *d* ∈ {10, 20, 30, 40, 50}, trained to in-context learn linear functions. The error is quite concentrated in the standard setting as well as for most out-of-distribution prompts. In the different-orthants and skewed-covariance settings, we observe a high variance for higher dimensional problems (*d* ≥ 30). However, in Section [6,](#page-9-0) we saw that the error in these settings usually decreases as we increase the model size. In the setting where we scale *x*, there is high variance even when *d* = 10.

![](./assets/A-4-function-class-icl/_page_25_Figure_2.jpeg)

(d) *d*/2-dimensional subspace

Figure 11: *Errors for models trained with different random seeds.* For each dimension, we train three models with different random seeds and show the corresponding error curves.

<span id="page-26-0"></span>![](./assets/A-4-function-class-icl/_page_26_Figure_0.jpeg)

(i) scaled *w* by a factor of 2

Figure 11: (continued) *Errors for models trained with different random seeds.* For each dimension, we train three models with different random seeds and show the corresponding error curves.

### <span id="page-27-0"></span>**B.5 Curriculum**

In Figure [12,](#page-28-0) we show the training loss of the Transformer model trained to in-context learn linear functions, with and without a curriculum. Specifically, given a random training prompt sequence (*x*1, *f*(*x*1), *x*2, *f*(*x*2), . . ., *xk*cur , *f*(*xk*cur )), let *y*ˆ*<sup>i</sup>* be the model's prediction for the *i* th input (meant to approximate *f*(*xi*)). For each such prompt, we consider the loss given by the normalized squared error averaged over all prompt prefixes

$$
\frac{1}{k_{\text{cur}}} \sum_{i=1}^{k_{\text{cur}}} \frac{(\hat{y}_i - f(x_i))^2}{d}.
$$

At each training step, we plot the loss averaged over a batch of 64 random prompts. For training with curriculum, *k*cur is gradually increased to 2*d* + 1 as described in Section [A.2.](#page-18-2) For training without curriculum *k*cur = 2*d* + 1 at all times.

Note that the loss often increases in the beginning as we train the model with curriculum. This is due to a sharp increase in the loss at steps where we increase the effective dimensionality (*d*cur) of prompt inputs (*x<sup>i</sup>* ). There are two reasons for this increase: (i) variance of the target output (*f*(*xi*) = *w* <sup>⊤</sup>*x<sup>i</sup>* ) increases, so even the optimum loss is larger, (ii) the model performance is worse for the prompt inputs with increased effective dimension. After each such step where we increment *d*cur, the loss starts to decrease again until the next increment. The overall trend in the loss looks upward when the sharp increase dominates the decrease that follows. Some observations worth highlighting are as follows.

**Curriculum drastically speed-ups training.** For functions in 20 or more dimensions, curriculum allows us to train a low-error model often 4 times faster. Moreover, training without curriculum does not always succeed within our training budget (500k steps), e.g., for one run with *d* = 30 and *all* runs with *d* = 50, the loss does not decrease at all without curriculum.

**Initial lull without curriculum.** For training without curriculum, we observe that the loss does not decrease for relatively a long period in the beginning, and starts to decrease sharply thereafter. There is a large variance in the length of this period for any fixed dimension, and the average length seems to increase with dimension. This period is almost non-existent for smaller dimensions (e.g., see the plot for *d* = 10), and therefore we do not observe such a period while training with curriculum where we start training with inputs lying in a 5 dimensional subspace.

**Curriculum does not affect final performance significantly.** For our core setting (*d* = 20), where we are able to train the model to low error even without curriculum, we do not observe any qualitative differences in the error in most cases (both with and without distribution shifts). One exception is the case with skewed covariance, where the model trained without curriculum seems to do slightly better. We plot the error curves for the standard, different orthants and skewed covariance cases in Figure [13.](#page-28-1)

<span id="page-28-0"></span>![](./assets/A-4-function-class-icl/_page_28_Figure_0.jpeg)

Figure 12: *Loss progression during training with and without curriculum.* For each dimension, we show the loss progression with 3 random seeds each for training with and without curriculum. The vertical dashed line shows the point at which the effective dimension of prompt inputs *d*cur reaches the actual dimension *d*, after which training with and without curriculum have the same prompt distribution. The horizontal dashed line shows the optimum expected loss. There is a drastic speedup in training with curriculum. Without curriculum, there is an initial relatively long period where the loss does not decrease. For each dimension, there is a large variance in the length of this period, and the average length seems to increase with dimension.

<span id="page-28-1"></span>![](./assets/A-4-function-class-icl/_page_28_Figure_2.jpeg)

Figure 13: *In-context learning performance for models trained with and without curriculum*. We show the performance for models trained with and without curriculum for in-context learning linear functions (*d* = 20). We did not observe any major qualitative difference in performance between the two settings in most cases. One exception is the case with skewed covariance where the model trained without curriculum does better.

### <span id="page-29-0"></span>**B.6 Effect of number of distinct prompts/functions seen during training**

Here, we investigate the effect of amount of training data required for in-context learning linear functions.

First, we consider the effect of number of distinct prompts encountered during training. For this, we create a set *S<sup>p</sup>* of *n<sup>p</sup>* randomly generated prompts, where each prompt in *S<sup>p</sup>* is generated by sampling a weight vector and prompt inputs from *N*(0, *I<sup>d</sup>* ). We generate random prompts during training by sampling uniformly from this set. As before, we train the model for 500*k* steps with a batch size of 64. We observe (see Figure [14\)](#page-29-1) that a model trained with *n<sup>p</sup>* = 100*k* is able to achieve non-trivial error and a model trained with *n<sup>p</sup>* = 1*M* achieves error close to that of the unrestricted model (trained with 32*M* distinct prompts). Recall that with curriculum learning, we zero out some of the coordinates of prompt inputs in the beginning of training, which will increase the total number of prompts the model sees during training. Therefore we do not use curriculum learning for this study to avoid inflating the number of distinct prompts seen during training.

Second, we consider the effect of number of distinct weight vectors (equivalently, distinct functions) encountered during training. For this, we create a set *S<sup>w</sup>* of *n<sup>w</sup>* weight vectors where each weight *w* is drawn i.i.d. from *N*(0, *I<sup>d</sup>* ). To generate a training prompt, (*x*1, *w* <sup>⊤</sup>*x*1, . . . , *x<sup>k</sup>* , *w* <sup>⊤</sup>*x<sup>k</sup>* ), we draw prompt inputs (*xi*s) i.i.d. from *N*(0, *I<sup>d</sup>* ) as in the unrestricted setting, and sample *w* uniformly at random from *Sw*. Thus while we sample from a finite set of weight vectors, we sample fresh inputs at each step. As before, we train the model for 500*k* steps with a batch size of 64. Here, we observe (see Figure [14\)](#page-29-1) that the model trained with as few as 10*k* distinct weight vectors achieves error close to the unrestricted model (trained with 32*M* distinct functions). We use curriculum learning for this study as in our standard setting. Recall that with curriculum learning, we only zero out some coordinates of prompt inputs in the beginning, so this does not change the number of distinct weight vectors seen by the model during training.

<span id="page-29-1"></span>![](./assets/A-4-function-class-icl/_page_29_Figure_4.jpeg)

Figure 14: *Effect of number of distinct prompts/functions seen during training.* We plot the squared error for models trained to in-context linear functions, as we increase the number of distinct prompts and distinct weight vectors (equivalently, distinct functions) seen during training. (Note that 32M corresponds to the unrestricted model where we sample fresh prompts at each training step.) The models are able to achieve error close to that of the unrestricted model with 1*M* distinct prompts or 10*k* distinct weight vectors.

### <span id="page-30-0"></span>**B.7 Can memorization explain model performance?**

In Section [3.1,](#page-4-1) we discussed that memorization of prompts seen during training cannot explain model performance. This is because the probability of the model encountering a training prompt similar to the one used for testing is astronomically low—the prompt inputs alone lie in a 800-dimensional space when predicting with 2*d* in-context examples (*d* = 20).

Moreover, even considering the possibility that the model encountered a similar *weight vector* during training cannot explain its performance. Let *S<sup>w</sup>* be the set of weight vectors used to generate training prompts. At inference time, given a prompt with in-context examples generated using a weight vector *w*⋆, suppose the model is somehow able to find the best weight vector *w*ˆ in *S<sup>w</sup>* minimizing the normalized squared error on query inputs:

$$
\hat{w} = \underset{w \in S_w}{\arg \min} \mathbb{E}_{x_{\text{query}} \sim N(0, I_d)} \left[ \frac{(w^\top x_{\text{query}} - w_\star^\top x_{\text{query}})^2}{d} \right]
$$
\n
$$
= \underset{w \in S_w}{\arg \min} \frac{\|w - w_\star\|_2^2}{d}
$$

Taking expectation over the weight vector *w*⋆, we get the expected normalized squared error of the model (with respect to randomly drawn in-context examples and query inputs):

$$
\mathbb{E}_{w_{\star} \sim N(0,I_d)} \left[ \min_{w \in S_w} \frac{\|w - w_{\star}\|_2^2}{d} \right].
$$

To empirically estimate this quantity, we sample *n<sup>w</sup>* weight vectors from *N*(0, *I<sup>d</sup>* ) (with *d* = 20) that form the set *Sw*, and 500 weight vectors from *N*(0, *I<sup>d</sup>* ) to estimate the outer expectation. We do this 20 times, freshly sampling the 500 weight vectors and the vectors comprising *S<sup>w</sup>* each time, and compute the mean of the 20 estimates obtained. When *n<sup>w</sup>* = 32*M* (number of weight vectors encountered in our standard training setup), we get a mean of 0.216 (standard deviation 0.004). However, our model is able to achieve an expected error of less than 0.001 for prompts with 2*d* in-context examples. Similarly, when *n<sup>w</sup>* = 10, 000, we get a mean of 0.505 (standard deviation 0.006), while a model trained on prompts generated using 10, 000 distinct weight vectors is able to achieve a much smaller error (see Figure [14\)](#page-29-1).

Thus we can conclude that the model cannot be relying on memorization of the training prompts or weight vectors, and is encoding a more sophisticated algorithm capable of in-context learning linear functions that are very different from those seen during training.