---
url: "https://arxiv.org/pdf/2511.08544"
title: "<span id=\"page-0-1\"></span>**LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics**"
captured_on: "2026-04-22"
capture_method: "pdf"
engine: "marker"
assets_dir: "./assets/07-lejepa"
---

# <span id="page-0-1"></span>**LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics**

Randall Balestriero1,2,\* Yann LeCun3,2,\* <sup>1</sup> Brown University <sup>3</sup> New York University (NYU) <sup>2</sup> Meta-FAIR \* Equal contribution

Learning manipulable representations of the world and its dynamics is central to AI. Joint-Embedding Predictive Architectures (JEPAs) offer a promising blueprint, but lack of practical guidance and theory has led to ad-hoc R&D. We present a comprehensive theory of JEPAs and instantiate it in **LeJEPA**, a lean, scalable, and theoretically grounded training objective. First, we identify the isotropic Gaussian as the optimal distribution that JEPAs' embeddings should follow to minimize downstream prediction risk. Second, we introduce a novel objective–**Sketched Isotropic Gaussian Regularization** (SIGReg)–to constrain embeddings to reach that ideal distribution. Combining the JEPA predictive loss with SIGReg yields LeJEPA with numerous theoretical and practical benefits: (i) single trade-off hyperparameter, (ii) linear time and memory complexity, (iii) stability across hyper-parameters, architectures (ResNets, ViTs, ConvNets) and domains, (iv) heuristics-free, e.g., no stop-gradient, no teacher–student, no hyper-parameter schedulers, and (v) distributed training-friendly implementation requiring only ≈50 lines of code. Our empirical validation covers 10+ datasets, 60+ architectures, all with varying scales and domains. As an example, using imagenet-1k for pretraining and linear evaluation with frozen backbone, LeJEPA reaches 79% with a ViT-H/14. We hope that the simplicity and theory-friendly ecosystem offered by LeJEPA will reestablish self-supervised pre-training as a core pillar of AI research [\(GitHub repo\)](https://github.com/rbalestr-lab/lejepa).

![](./assets/07-lejepa/_page_0_Figure_3.jpeg)

<span id="page-0-0"></span>**Figure 1. LeJEPA overview. Top-left:** Training loss exhibits strong correlation with downstream linear probe performance on ImageNet-1k (ViT-base), providing the first practical loss for model selection without supervised probing. **Top-right:** Training stability without heuristics even on 1.8B ViT-g models, stable training loss. **Bottom-left:** PCA features from ImageNet-1k pretrained LeJEPA ViT-Large demonstrate clear semantic relationships. **Bottom-right:** Galaxy10 in-domain results showcasing LeJEPA's in-domain pretraining consistently outperforms state-of-the-art frontier foundation models transfer learning (DINOv2/v3 trained on natural images) across data regimes from 1-shot to full supervision. This demonstrates that *domain-specific SSL beats generic transfer learning*, even against massive-scale frontier models, when the framework scales effortlessly to any domain, model, and data scale.

# <span id="page-1-0"></span>**1 Introduction**

Learning manipulable representations of the world and its dynamics is a long-standing question in AI, with roots dating back centuries ago [\[Von Helmholtz, 1867,](#page-21-0) [Tolman,](#page-21-1) [1948,](#page-21-1) [Gregory, 1980,](#page-19-0) [Sutton, 1991,](#page-21-2) [Friston, 2010\]](#page-19-1). Across domains, e.g., image recognition, robotics, physics, space exploration, the unifying question is *how to learn an organized and actionable high-dimensional embedding space from observations?* Using Deep Networks–parameterized nonlinear operators –to map observations to embeddings is a standard first piece of that puzzle [\[LeCun et al., 2015,](#page-20-0) [Goodfellow et al., 2016\]](#page-19-2). The second, less standardized, piece of that puzzle is *how to train* . Joint-Embedding Predictive Architectures (JEPAs) suggest training by maximizing predictive agreement between the embeddings of semantically related *views* [\[Bromley et al., 1993,](#page-18-0) [LeCun, 2022,](#page-20-1) [Balestriero et al., 2023\]](#page-17-0). Views can come in two forms: transformations or corruptions. They can involve masking, cropping, blurring, temporal or spatial translations, geometric or photometric transformations, viewpoint changes, views from different sensor modalities, etc. The supervised forms involve human-produced components such as image-caption pairs, text-code pairs, etc [\[Tian et al., 2020\]](#page-21-3). In any case, views are expected to share some degree of semantic relationship to allow the prediction task to align 's embeddings towards the underlying knowledge present in the data.

Alas, JEPA's prediction task admits failure modes, such as representation collapse, where maps all inputs to nearly identical embeddings (*complete collapse*) or to a lowdimensional subspace (*dimensional collapse*) [\[Jing et al.,](#page-19-3) [2021\]\[Jing et al., 2021,](#page-19-3) [Cosentino et al., 2022,](#page-18-1) [Balestriero](#page-17-1) [and LeCun, 2022\]](#page-17-1). To mitigate such shortcut solutions, state-of-the-art recipes rely on heuristics–stop-gradient [\[Chen et al., 2020a\]](#page-18-2), asymmetric view generation [\[Wang](#page-22-0) [et al., 2022\]](#page-22-0), teacher–student networks with carefully tuned EMA schedules [\[Caron et al., 2021,](#page-18-3) [Tian et al., 2021\]](#page-21-4), explicit normalization and whitening layers [\[Ermolov et al.,](#page-18-4) [2021,](#page-18-4) [Chen et al., 2021\]](#page-18-5)–and a delicate balance of hyperparameters. As a result, today's JEPA training is brittle and most research has shifted toward scaling data [\[Vo et al.,](#page-21-5) [2024\]](#page-21-5), models [\[Fan et al., 2025\]](#page-18-6) and even post-training [Ro](#page-20-2)[das et al.](#page-20-2) [\[2025\]](#page-20-2) while leaving the theoretical foundations of JEPAs largely unexplored.

Our study proposes to break that cycle by questioning some of the fundamental design principles underpinning JEPAs. That introspection will start by asking *what are the necessary conditions that JEPAs should abide by?* Those minimal conditions will then act as *axioms* for us to design a novel and lean JEPA. We identify two axioms: (i) solving the prediction task while (ii) enforcing an isotropic Gaussian distribution of the embeddings

(Section [3\)](#page-4-0). While (i) follows standard practice [\[Balestriero](#page-17-1) [and LeCun, 2022\]](#page-17-1), we introduce in Section [4](#page-5-0) a novel distribution matching objective–Sketched Isotropic Gaussian Regularization (SIGReg)–to enforce (ii). The use of SIGReg not only removes the need for the numerous heuristics previously employed to prevent representation collapse, but SIGReg also exhibits favorable scaling properties as its *memory and computational complexity is linear in dimension and sample size*. Crucially, SIGReg's isotropic Gaussian enforcement solves the collapsed shortcut solution and provably minimizes the model's expected risk over the space of downstream tasks to be encountered post-training. The resulting JEPA solution–coined Latent-Euclidean JEPA (LeJEPA)–is introduced in Section [5.](#page-10-0) Beyond theoretical optimality, LeJEPA offers numerous benefits such as (i) provable statistical guarantees, (ii) removal of heuristics such as teacher-student networks, (iii) linear memory and computational complexity, and most importantly (iv) a unified design with a single trade-off parameter that works out of the box across datasets, architectures and scales (see Section [6\)](#page-11-0). We summarize our contributions below.

**Contribution 1: We prove the optimal embedding distribution for foundation models.** We establish that the isotropic Gaussian uniquely minimizes downstream prediction risk across broad task families. In Section [3,](#page-4-0) we derive this result rigorously for both linear (Section [3.1\)](#page-4-1) and nonlinear probes (Section [3.2\)](#page-4-2), providing the first principled answer to what distribution 's embeddings should follow. This theoretical result transforms JEPA design from heuristic exploration to targeted optimization. **Contribution 2: We introduce SIGReg, a distribution matching objective that uniquely combines provable correctness with computational efficiency at scale.** We present *Sketched Isotropic Gaussian Regularization* (SIGReg), a novel objective that enforces distributional alignment via random projections and characteristic-function matching (Section [4](#page-5-0) and Figure [2\)](#page-2-1). SIGReg provides statistical guarantees (Sections [4.1](#page-5-1) and [4.2\)](#page-6-0) while achieving linear complexity and bounded gradients—a combination that existing distribution matching methods do not offer. Critically, its projection-based construction defeats the curse of dimensionality (Section [4.3\)](#page-9-0), making it both theoretically sound and practically efficient for high-dimensional embeddings.

**Contribution 3: We design LeJEPA, a statistically optimal JEPA that eliminates collapse by construction.** By combining JEPA's predictive objective with SIGReg targeting the isotropic Gaussian, we introduce *LeJEPA*—Latent-Euclidean JEPA (Section [5\)](#page-10-0). LeJEPA requires only a single hyperparameter, eliminates representational collapse without stop-gradients or teacher-student architectures, and transfers across architectures and datasets without hyperparameter tuning. This demonstrates that principled

**LeJEPA:** [Sec 1: Intro](#page-1-0) | **[Sec 2: Background](#page-2-0)** | [Sec 3: Why Gaussian?](#page-4-0) | [Sec 4: SIGReg](#page-5-0) | [Sec 5: LeJEPA](#page-10-0) | [Sec 6: Experiments](#page-11-0)

<span id="page-2-1"></span>![](./assets/07-lejepa/_page_2_Figure_1.jpeg)

**Figure 2. Sketched Isotropic Gaussian Regularization (SIGReg):** Given some arbitrary input data with density with support that may or may not lie on a manifold (**left**), a Deep network (DN) encoder ( ) produces embeddings <sup>=</sup> () with some distribution <sup>∼</sup> (**middle**). Our proposed Backward Cramér-Wold Statistics (Section [4\)](#page-5-0) objective pushes to match a target distribution by projecting the embeddings along <sup>1</sup> directions (**middle, arrows**) and enforcing that the univariate densities (**right, colored lines**) match the distribution of , projected along the same directions. Any popular statistical test (provided in Section [4.2\)](#page-6-0) can assess the goodness-of-fit–in practice we argue for characteristic function tests (Section [4.2\)](#page-6-0). By using SIGReg with isotropic Gaussian (**right, black lines**), we introduce a lean and provably optimal (Section [3\)](#page-4-0) JEPA, coined LeJEPA, free of numerous heuristics and able to produce competitive performances (Sections [5](#page-10-0) and [6\)](#page-11-0).

theory directly yields practical simplicity.

**Contribution 4: We validate LeJEPA at scale across diverse architectures and establish in-domain pretraining as viable.** Our experiments (Section [6\)](#page-11-0) span ViTs, ConvNeXts, ResNets, MaxViTs, and Swin Transformers at scales approaching 1 billion parameters, where LeJEPA matches or exceeds state-of-the-art methods while maintaining training simplicity and robustness. Critically, on domain-specific datasets (Galaxy10, Food101), LeJEPA outperforms DINOv2-based transfer learning when pretrained directly on target data. This challenges the transfer learning paradigm and demonstrates that principled SSL can unlock effective in-domain pretraining—previously considered impractical for small datasets.

## <span id="page-2-0"></span>**2 Background and Notations**

We start by introducing some of the notations we will be using throughout our manuscript (Section [2.1\)](#page-2-2), followed by a review of JEPAs (Section [2.2\)](#page-3-0), and existing literature studying their design (Section [2.3\)](#page-3-1).

## <span id="page-2-2"></span>**2.1 Notations and Definitions**

**Data.** We are in possession of a dataset of shape (, , ) ∈ <sup>N</sup><sup>∗</sup><sup>3</sup> where is the number of samples, is the number of views, and is the dimension. One entry of this dataset is accessed via ,,. Those dimensions are often interpreted as follows: (**N**) is the number of independent samples, e.g., different images or different videos, (**V**) is the number of *views*, e.g., data-augmentations for images, frames for videos, and (**D**) is the dimension of each ,, e.g., number of RGB pixels for images. In many cases the ordering over is given by *time*–but in some cases, e.g., data-augmentation of an image, ordering becomes

irrelevant. Our study does not require any particular choice to organize one's dataset into a (, , ) tensor– *and none of our theory and implementation assumes a particular design decision for that tensor*. However, we will rely on the following two properties, (*independence*) the samples , ′ have been obtained independently from each other <sup>∀</sup> <sup>≠</sup> ′ , and (*identically distributed*) the sampling process was identical among , <sup>∀</sup>.

**Deep Networks.** Today's AI solutions rely on *Deep (Neural) Networks* (DNs), which are compositions of a large number of parameterized linear and nonlinear operators. We denote the DN's mapping as : <sup>R</sup> → R with the dimension of the embedding space. The internals of are designed by the researcher to incorporate as much prior knowledge about the data as possible. The details of are irrelevant to our study–as we will see the proposed LeJEPA works out-of-the-box on any . In any case, all the *learnable parameters* are gathered in the vector ∈ R , with counting the total number of parameters. A central challenge in AI research is to design the right architecture and training objective so that can be learned from gradient descent to ultimately produce a useful system, or foundation model, .

**JEPAs.** A foundation model is any system, e.g., a DN, able to solve numerous downstream tasks without requiring any change in its internal parameters . This is in sharp contrast with a supervised model that only considers its training task. JEPAs have formally been introduced by [LeCun](#page-20-1) [\[2022\]](#page-20-1) as a vehicle to produce foundation models. The core building blocks of JEPAs rely on numerous wellestablished techniques such as siamese networks [\[Bromley](#page-18-0) [et al., 1993\]](#page-18-0) and predictive coding [\[Helmholtz et al., 1867,](#page-19-4) [Bruner and Postman, 1949\]](#page-18-7). While the exact blueprint of

#### <span id="page-3-2"></span>**LeJEPA:**

![](./assets/07-lejepa/_page_3_Figure_2.jpeg)

JEPAs varies greatly between use-cases, they all rely on two core principles: (i) being able to predict the embedding of a view , from the embedding of another view ,′ , ′ <sup>≠</sup> , all while (ii) ensuring that the embeddings do not become degenerate. Concretely, once a JEPA is designed and trained, it should be able to solve numerous downstream tasks in zero or few shots. The JEPA objective function, along with some examples for , is provided in Equation [\(1\)](#page-3-2). The *predictability* criterion can be done by directly comparing the embeddings of the partial views (,,.) and (,′ ,.) with a metric, e.g., <sup>ℓ</sup>. In some cases, an additional DN coined *Pred*, is employed to compare ((,,.)) against (,′ ,.)–which is only justified when there exists an asymmetry between the information content of the different views, e.g., by conditioning the predictions on observed actions from robotics data [\[Khazatsky et al., 2024\]](#page-19-5).

## <span id="page-3-0"></span>**2.2 The Need for Reliable Pretraining**

The JEPA's prediction task is designed based on a priori knowledge of the data. Its design is often quite natural since it is relatively intuitive to form so that its views share the relevant information content one hope to capture. On the other hand, the design of the "anti-collapse" criterion is much closer to a game of Whac-A-Mole. Today's designs rely on many different under-specified safeguards which are carefully combined in the hope that degenerate shortcut solutions are avoided during training. Such mechanisms include (i) feature whitening [\[Ermolov et al.,](#page-18-4) [2021,](#page-18-4) [Bardes et al., 2021\]](#page-17-2), (ii) negative samples [\[Chen](#page-18-2) [et al., 2020a,](#page-18-2) [He et al., 2020\]](#page-19-6), and (iii) asymmetric views and teacher-student networks with stop-gradient [\[Caron](#page-18-3) [et al., 2021,](#page-18-3) [Assran et al., 2023\]](#page-17-3). Those mechanisms all suffer from at least two of the following limitations: (i) under-specification, i.e., the criteria can be minimized while embeddings are in a degenerate configuration, (ii) quadratic time and memory complexity with mini-batch size and/or embedding dimension, (iii) sensitivity to data distribution, hyperparameters, architecture, and (iv) lack of theoretical understanding and guarantees.

## <span id="page-3-1"></span>**2.3 The Need for Actionable Theory**

For decades, the two major solutions for AI were supervised learning [\[LeCun et al., 2015\]](#page-20-0) and learning by reconstruction [\[Rumelhart et al., 1986\]](#page-21-6)–sometimes combined together, e.g., for semi-supervised learning [\[Kingma et al.,](#page-20-3) [2014\]](#page-20-3). In supervised learning, the labels both ensure that semantically similar samples are close to each other in embedding space while preventing complete representation collapse. In particular, it is possible to measure the amount of collapse in supervised learning as a function of the number of classes [\[Papyan et al., 2020\]](#page-20-4). The reconstruction objective is similarly well suited to prevent representation collapse as the original input must be recovered from the embeddings, i.e., the embeddings must be as informative about the input as possible–up to some optional denoising tasks that users can setup as part of the training [\[Vincent](#page-21-7) [et al., 2010\]](#page-21-7).

Because supervised and reconstruction-based learning have been widely studied for decades, there exists a large body of work to explain and inform practical designs–as well as studying their limitations in producing foundation models [\[Balestriero and LeCun, 2024,](#page-17-4) [Van Assel et al.,](#page-21-8) [2025\]](#page-21-8). This is not the case for the more recent JEPAs where empirical advances quickly outpace anyone hoping to delve into their inner workings. This dynamic led the community to focus on post-hoc theoretical justification of already found solutions [\[Liu et al., 2021,](#page-20-5) [Shwartz Ziv](#page-21-9)

[and LeCun, 2024,](#page-21-9) [Shwartz-Ziv et al., 2022,](#page-21-10) [Zhang et al.,](#page-22-1) [2023\]](#page-22-1). In most cases, those studies involve the *Mutual Information (MI)* [\[Shannon, 1948,](#page-21-11) [Cover, 1999\]](#page-18-8) whose different bounds recover established methods [\[Gutmann and](#page-19-7) [Hyvärinen, 2010,](#page-19-7) [Ma and Collins, 2018,](#page-20-6) [Oord et al., 2018,](#page-20-7) [Poole et al., 2019,](#page-20-8) [Hjelm et al., 2018,](#page-19-8) [McAllester and Stratos,](#page-20-9) [2020\]](#page-20-9). Because existing studies focus on explaining and interpreting already developed JEPAs, too little principled guidance and innovation has been brought forward. Instead, most of the recent empirical advances take the form of collecting larger dataset, scaling up pre-existing training recipes [\[Goyal et al., 2019,](#page-19-9) [Chen et al., 2020b,](#page-18-9) [Oquab et al.,](#page-20-10) [2023,](#page-20-10) [Fan et al., 2025\]](#page-18-6), and deriving novel data curation processes [\[Vo et al., 2024,](#page-21-5) [Kerdreux et al., 2025\]](#page-19-10).

In contrast, our goal in the following Sections [3](#page-4-0) to [5](#page-10-0) will be to derive a novel JEPA solution from first principles, i.e., whose design relies on proved necessary conditions for optimality, and with a pretraining recipe that can finally reconcile exploratory research, scalability, and state-of-theart performances.

# <span id="page-4-0"></span>**3 Latent Euclidean: Embeddings Should be Isotropic Gaussian**

We address a fundamental question: *which distribution should* Enc() *follow to minimize empirical risk on any downstream task?* We prove that the isotropic Gaussian is the unique optimal distribution for both linear (Section [3.1\)](#page-4-1) and nonlinear probing (Section [3.2\)](#page-4-2), with geometric intuition provided in Section [3.3.](#page-5-2) This theoretical result establishes the necessary design principle for our JEPA; Section [4](#page-5-0) then provides the practical implementation to achieve it.

## <span id="page-4-1"></span>**3.1 Linear Probing**

We begin by identifying the optimal distribution for 's embeddings by analyzing linear probes–one of the most popular methods for frozen encoder evaluation. Specifically, we ask: *which distribution for* () *would be most favorable for solving arbitrary downstream tasks, i.e., for any realization of targets ?*

Denote as ∈ R × the matrix of embeddings, each -dimensional, from (). The *unknown* corresponding labels are denoted as ∈ R . Without loss of generality, we consider univariate targets; the following analysis extends to multivariate targets. The linear probe minimizes the following least square problem [\[Bishop and Nasrabadi,](#page-18-10) [2006\]](#page-18-10)

<span id="page-4-6"></span>
$$
\hat{\beta} = \underset{\beta \in \mathbb{R}^K}{\arg \min} ||y - Z\beta||_2^2 + \lambda ||\beta||_2^2, \quad (OLS)
$$

where <sup>ˆ</sup> is the optimal probe parameters, and <sup>≥</sup> <sup>0</sup> is an hyperparameter controlling the Tikhonov regularizer strength [\[Bishop, 1995,](#page-18-11) [Golub et al., 1999\]](#page-19-11). Despite

not knowing , it is possible to describe the bias and variance of the estimator <sup>ˆ</sup> as a function of the distribution of . Consider two embeddings with identical column spans aniso, iso. aniso's covariance matrix eigenvalues are given by { } =<sup>1</sup> with at least two distinct values, while iso's covariance matrix eigenvalues are all equal to <sup>1</sup> Í =1 . Hence, the two candidate embeddings aniso, iso capture the same intrinsic features and have same energy, but different geometries.

### <span id="page-4-4"></span>**Lemma 1: Anisotropy amplifies bias**

Whenever > 1, there always exists a downstream task () for which aniso produces a higher bias estimator than iso for > 0. (Proof in Section [B.1.](#page-25-0))

### <span id="page-4-5"></span>**Lemma 2: Anisotropy amplifies variance**

With <sup>=</sup> 0, the total variance of <sup>ˆ</sup> [\(OLS\)](#page-4-3) is minimized for iso with tr(Var(<sup>ˆ</sup> aniso)) <sup>&</sup>gt; tr(Var(<sup>ˆ</sup> iso)). (Proof in Section [B.2.](#page-25-1))

From the above lemmas. [1](#page-4-4) and [2](#page-4-5) we obtain that the distribution of features must be isotropic. We now move to nonlinear probing where the standard Gaussian will emerge as the unique optimum.

## <span id="page-4-2"></span>**3.2 Nonlinear Probing**

To allow for more flexible evaluation of the pretrained encoder , it has become increasingly common to work with a nonlinear probe. We analyze two widely-used nonlinear methods: radius-based k-NN [\[Taunk et al., 2019,](#page-21-12) [Sun and Huang, 2010,](#page-21-13) [Zhang et al., 2017,](#page-22-2) [Abu Alfeilat et al.,](#page-17-5) [2019\]](#page-17-5) for its simplicity and kernel methods [\[Nadaraya,](#page-20-11) [1964,](#page-20-11) [Watson, 1964\]](#page-22-3) for their theoretical tractability.

As in Section [3.1,](#page-4-1) we ask ourselves which distribution of embeddings would be preferable for a foundation model. We first define our prediction function. The training data consists of the embeddings along with their training labels {( , )} =1 . The prediction, using radius-based k-NN for a query vector is formed as

$$
\widehat{y}(q) := \frac{1}{|N_{r_0}(q)|} \sum_{n \in N_{r_0}(q)} y_n, \qquad \text{(kNN)}
$$

where <sup>0</sup> () <sup>=</sup> { : <sup>∥</sup> <sup>−</sup> ∥ ≤ 0}. The specific choice of radius <sup>0</sup> controls how many neighbors predictions are averaged to form the query's prediction. The kernel's prediction at a query ∈ R is given by

$$
\widehat{y}(q) \triangleq \frac{\sum_{n=1}^{N} K_h(q - z_n) y_n}{\sum_{n=1}^{N} K_h(q - z_n)}.
$$
 (Kernel)

<span id="page-4-3"></span>We search over all distributions of Z subject to a fixed total variance constraint, e.g., Tr(Cov()) <sup>=</sup> <sup>1</sup> or <sup>∥</sup>Cov()∥ <sup>=</sup> 2. The specific value of does not affect the optimal dis-

<span id="page-5-3"></span>![](./assets/07-lejepa/_page_5_Figure_1.jpeg)

**Figure 3.** Illustration of lemma. [2](#page-4-5) showcasing how anisotropic (**right**) embeddings lead to higher variance estimator compared to isotropic embeddings (**left**). We sample 100 training points for the 2-class classification task and fit a logistic regression–repeating the process over numerous training set sample. Each sampling results in a decision boundary (**purple**).

tribution shape. Following the same type of derivations as done in the linear regime–with the exception of some additional regularity conditions–we are able to precisely identify the isotropic Gaussian as the unique optimum to minimize bias as formalized below.

### **Theorem 1: isotropic Gaussian Optimality**

The integrated square bias (ISB) over query points is given by

$$
ISB_{k-NN} = \frac{r_0^4}{(K+2)^2} \tau_g^2 J(p) + O(r_0^4), \quad \text{(k-NN)}
$$

$$
\text{ISB}_{\text{kernel}} \le \Big(\frac{h^2\mu_2(K)}{2}\Big)^2 \Big(2B^2 + 8L^2J(p)\Big) + o(h^4), \quad \text{(kernel)}
$$

and among distributions with a scalar-based covariance constraint, the isotropic Gaussian is the unique minimizer of the integrated square bias. (Proof in Sections [B.4](#page-27-0) and [B.7.](#page-33-0))

Numerous additional details and discussions on the regularity assumptions we employed are provided in Section [A.](#page-23-0) Together, these results establish the isotropic Gaussian distribution as the optimal design to minimize the worst-case risk of a foundation model across downstream tasks.

### <span id="page-5-2"></span>**3.3 Geometric and Practical Insights**

We now empirically validate that the isotropic Gaussian is optimal when no information about downstream tasks is available. We focus on linear probing (Section [3.1\)](#page-4-1), where all considered distributions have the same total variance.

When employing a linear probe, an anisotropic distribution increases both bias (with Tikhonov regularization) and variance. Examining bias first (lemma. [1\)](#page-4-4), we present in Figure [18](#page-48-0) visualizations for both continuous regression and discrete classification tasks. We observe that the cosine similarity between estimated and ground-truth

parameters equals 1 only for isotropic distributions, degrading for anisotropic cases regardless of sample size or regularization strength. Regarding variance (lemma. [2\)](#page-4-5), we show in Figure [3](#page-5-3) that learned parameters vary significantly more across training sets when the covariance is anisotropic (right) compared to isotropic (left)—even when using logistic regression instead of OLS. Figure [17](#page-47-0) further illustrates this effect, showing the distribution of learned parameters across different training samples for both cases. The anisotropic distribution clearly produces higher-variance estimators.

These theoretical and empirical results establish our design principle for LeJEPA: *embeddings* () *should follow an isotropic Gaussian distribution to minimize worst-case risk across downstream tasks encountered post-training*. Section [4](#page-5-0) introduces a novel regularizer to achieve this distribution.

# <span id="page-5-0"></span>**4 SIGReg: Reliable Isotropic Gaussian Regularization in High-Dimension**

Having established the isotropic Gaussian as the optimal embedding distribution (Section [3\)](#page-4-0), we now introduce *Sketched Isotropic Gaussian Regularization* (SIGReg)–a distribution matching objective that is simultaneously (i) *differentiable*, (ii) *scalable*, (iii) *provable*, and (iv) *interpretable*. SIGReg builds on three key innovations. First, we formulate distribution matching as a statistical test under the null hypothesis <sup>=</sup> (Section [4.1\)](#page-5-1). Second, we identify a test that guarantees bounded gradients and curvature while maintaining linear complexity and efficient multi-GPU scaling (Section [4.2\)](#page-6-0). Third, SIGReg bypasses the curse of dimensionality, eliminating collapsed shortcut solutions entirely (Section [4.3\)](#page-9-0).

### <span id="page-5-1"></span>**4.1 Hypothesis Testing as a Judge**

Asking for ()'s distribution to match a target distribution is typically done by creating various measures of distance or divergence, and estimating them in highdimension. We propose a different starting point grounded in statistics. Consider the hypothesis testing framework [\[Fisher, 1928,](#page-19-12) [Neyman and Pearson, 1933\]](#page-20-12) given by

$$
H_0: P_{\theta} = Q \quad \text{vs.} \quad H_1: P_{\theta} \neq Q,
$$
 (2)

with <sup>0</sup> being referred to as the *null hypothesis*. That is, we are asking in Equation [\(2\)](#page-4-6) if there is enough empirical evidence to reject the null. To answer that question, one (i) employs a *test-statistic*, i.e., a single scalar value summarizing the evidence from the empirical samples, (ii) determines a critical value for the test-statistic based on the probability of Type I error, i.e., of mistakenly rejecting a true null hypothesis, (iii) compares the test-statistic to

the critical value ; if the test-statistic exceeds , reject the null hypothesis. If the null is not rejected, we can only claim that *there is not sufficient empirical evidence against* <sup>=</sup> .

As it stands, Equation [\(2\)](#page-4-6) remains impractical in large dimension as existing tests have at least quadratic complexity with the number of samples considered (more details in Section [F\)](#page-43-0). We thus propose to derive a sketching strategy by decomposing Equation [\(2\)](#page-4-6) into simpler univariate tests. Denoting the push-forward distributions () ≜ ( <sup>⊤</sup>)# and () <sup>≜</sup> ( <sup>⊤</sup>)#, we can define the following *directional* univariate test

$$
H_0(a): P_{\theta}^{(a)} = Q^{(a)}
$$
 vs.  $H_1(a): P_{\theta}^{(a)} \neq Q^{(a)}$ , (3)

for a given directional unit-norm vector ∈ −<sup>1</sup> . The corresponding *directional test-statistic* of Equation [\(3\)](#page-6-1) is computed as ({ ⊤ ()} =1 ). Examples of tests will be provided in the later Section [4.2.](#page-6-0) Repeating that process over a set of directions A ≜ {1, . . . , } and aggregating the individual values lead to the following *global test-statistic*

$$
T_{\mathbb{A}}(\{f_{\theta}(x_n)\}_{n=1}^N) \triangleq \max_{a \in \mathbb{A}} T(\{a^{\top} f_{\theta}(x_n)\}_{n=1}^N). \hspace{1cm} (4)
$$

We now provide a formal statement asserting the consistency of Equation [\(4\)](#page-6-2) to test the original multivariate null hypothesis from Equation [\(2\)](#page-4-6). Our result leverages the well-known union-intersection principle [\[Roy, 1953\]](#page-20-13), and a slightly modified Cramér-Wold theorem. We denote by = equality in distribution.

### <span id="page-6-8"></span>**Lemma 3: Hyperspherical Cramér-Wold**

Let , be <sup>R</sup> -valued random vectors, then

> ⟨, ⟩ <sup>=</sup> ⟨, ⟩, <sup>∀</sup> <sup>∈</sup> <sup>S</sup> −<sup>1</sup> ⇐⇒ <sup>=</sup> .

Convergence in distribution also holds. (Proof in Section [B.8.](#page-34-0))

### <span id="page-6-3"></span>**Theorem 2: Sufficiency of directional tests**

Equation [\(4\)](#page-6-2) is a valid statistical test for Equation [\(3\)](#page-6-1) as

$$
P = Q \implies \limsup_{n \to \infty} \Pr\left(T_{\mathbb{A}}(\{f_{\theta}(x_n)\}_{n=1}^N) \ge \tau_{\alpha}\right) \le \alpha, \text{ (level)}
$$
\n
$$
P \ne Q \implies \limsup_{n \to \infty} \Pr\left(T_{\mathbb{A}}(\{f_{\theta}(x_n)\}_{n=1}^N) \ge \tau_{\alpha}\right) = 1, \text{ (power)}
$$
\n(Proof in Section B.9.)

<span id="page-6-0"></span>The assumptions required in the proof of thm. [2](#page-6-3) hold for classical consistent univariate tests such as the ones presented in the following Section [4.2.](#page-6-0)

<span id="page-6-7"></span>![](./assets/07-lejepa/_page_6_Figure_15.jpeg)

<span id="page-6-1"></span>**Figure 4.** Examples of distributions living on the surface of the sphere with varying Sobolev smoothness coefficients . As per thm. [5,](#page-10-1) the greater is, the more global will be the impact of SIGReg for a given number of directions . Practically, this represents the distribution of the encoder's output. Because the target density (isotropic Gaussian) is smooth, the coeffcients of the embedding will quickly grow hereby making SIGReg (def. [2\)](#page-6-4) immune to the curse of dimensionality.

## **4.2 SIGReg: Sketching the Epps-Pulley Test is Stable and Scalable**

<span id="page-6-2"></span>Our proposed regularizer–coined Sketched Isotropic Gaussian Regularization (SIGReg)–follows directly from thm. [2](#page-6-3) using any statistical test targeted towards the isotropic Gaussian, illustrated in Figures [2](#page-2-1) and [5,](#page-7-0) and formalized below.

### <span id="page-6-4"></span>**Definition 2: SIGReg (PyTorch code in algorithm [1\)](#page-9-1)**

SIGReg sketches a statistical test towards isotropic Gaussian

<span id="page-6-5"></span>
$$
\text{SIGReg}_{T}(\mathbb{A}, \{f_{\theta}(x_n)\}_{n=1}^N) \triangleq \frac{1}{|\mathbb{A}|} \sum_{a \in \mathbb{A}} T(\{a^\top f_{\theta}(x_n)\}_{n=1}^N),
$$
\n(SIGReg)

where we recommend the Epps-Pulley test (Section [4.2.3\)](#page-8-0) for .

We replace the maximum over ∈ A in thm. [2](#page-6-3) by an average in [\(SIGReg\)](#page-6-5) to avoid sparse gradient over the directions in <sup>A</sup>. We now delve on the choice of for which we compare well-known candidate tests in the field of statistics that are categorized into (i) moment based (Section [4.2.1\)](#page-6-6), (ii) CDF based (Section [4.2.2\)](#page-7-1), and (iii) CF based (Section [4.2.3\)](#page-8-0) statistics–ultimately justifying our choice of the Epps-Pulley statistic.

### <span id="page-6-6"></span>**4.2.1 Moments are Unstable and Insufficient**

The first family of statistics we consider are moment-based. Taking the standard Gaussian as an instanciation for the moments, we can define the Jarque-Bera [\[Jarque and Bera,](#page-19-13) [1980\]](#page-19-13) test that compares the third and fourth moments,

**LeJEPA:** [Sec 1: Intro](#page-1-0) | [Sec 2: Background](#page-2-0) | [Sec 3: Why Gaussian?](#page-4-0) | **[Sec 4: SIGReg](#page-5-0)** | [Sec 5: LeJEPA](#page-10-0) | [Sec 6: Experiments](#page-11-0)

<span id="page-7-0"></span>![](./assets/07-lejepa/_page_7_Figure_1.jpeg)

**Figure 5.** Constructed data density with "X" distribution whose marginals are standard Gaussian and whose covariance is identity (**left densities**). Applying <sup>=</sup> <sup>10</sup> projections on the half circle directions produces <sup>10</sup> univariate distributions that can be compared against a standard Gaussian (**left**) using any preferred statistic from Section [4.2.](#page-6-0) The appropriate direction is able to capture the degenerate distribution of the data hereby creating a spike in the statistic value.

i.e., skewness and kurtosis, as

$$
JB(u) \triangleq \frac{N}{6} \left( s\widehat{\text{kew}}(u)^2 + \left( \frac{\widehat{\text{kurt}}(u) - 3}{2} \right)^2 \right), \quad \text{(Jarque-Bera)}
$$

where skew is the skewness computed from the data as 1 Í =1(−ˆ) 3 ˆ <sup>3</sup> and kurt d is the kurtosis 1 Í =1(−ˆ) 4 ˆ 4 . Typically, the [\(Jarque-Bera\)](#page-7-2) test is used to see if a density follows a Gaussian distribution of any mean and variance–hence it only looks at moments 3 and 4. In our case we aim for a standard Gaussian test and thus add the usual statistics on the first two moments, leading to the extended test

<span id="page-7-3"></span>
$$
\text{EJB}(u) \triangleq \frac{N\hat{\mu}(u)^2}{\hat{\sigma}(u)^2} + \frac{(N-1)\left(\hat{\sigma}(u)^2 - 1\right)^2}{2} + \text{JB}(u).
$$
\n(Extended Jarque-Bera)

The [\(Extended Jarque-Bera\)](#page-7-3) acts as a moment matching problem over the first four moments. Such moment matching methods have proven powerful not only for statistical tests but also as mean to learn parametric and nonparametric models of data.

**The Stability and Identifiability Conundrum.** We now explain why moment-based tests–albeit powerful–will not be suited for LeJEPA. The ℎ of a distribution is denoted as (). The first observation is that wellbehaved distributions abiding the Carleman's condition Í<sup>∞</sup> =<sup>1</sup> 2 () <sup>−</sup>1/(2) <sup>=</sup> <sup>∞</sup> [\[Carleman, 1926\]](#page-18-12), such as the Gaussian, or for distributions with finite interval [\[Hausdorff,](#page-19-14) [1923\]](#page-19-14) are uniquely determined by their moments. However, using a finite number of moments creates the following non-identifiability issue which well-known in statistics and often used as a motivation to use *all* moments [\[Lehmann](#page-20-14) [and Romano, 2005\]](#page-20-14).

### <span id="page-7-4"></span>**Theorem 3: Insufficiency of K Moments**

<span id="page-7-2"></span>Minimizing the following objective with <sup>&</sup>gt; <sup>0</sup>, <sup>∀</sup>

$$
\sum_{k=1}^K c_k \left( m_k \left( P_{\theta}^{(a)} \right) - m_k \left( Q^{(a)} \right) \right)^2,
$$

for finite does not imply () <sup>=</sup> () . (Proof in Section [B.11.](#page-36-0))

Hence thm. [3](#page-7-4) prescribes us with the guideline to employ as large as possible to remove collapsed shortcut solution by making sure our distribution matching is accurate. Yet, doing so leads to unstable gradient-based training due to the gradient norm scaling as (), and the variance of Monte Carlo gradient estimates growing as ( 22(−1) ) for the -th moment since <sup>∇</sup> ( () ) = ∥E -( ⊤ ())−1 ⊤ () <sup>∥</sup>, with () ∈ R × the Jacobian matrix–hereby creating an impractical situation where training stability and identifiability can not be achieved simultaneously.

#### <span id="page-7-1"></span>**4.2.2 Cumulative Density Functions are Impractical**

The second family of tests acts upon the CDF. Because those tests require sorting, let's denote the th order-statistics of samples by :. Two highly standard tests are quadratic Empirical Density Function statistics with different weighting known as Cramér-von Mises [\[Cramér, 1928,](#page-18-13) [Von Mises,](#page-21-14) [1981\]](#page-21-14) and Anderson Darling [\[Anderson and Darling, 1952\]](#page-17-6), and given by

<span id="page-7-5"></span>
$$
T_w = N \int_{-\infty}^{\infty} (F_N(x) - F(x))^2 w(x) dF(x)
$$
  
\n
$$
w(x) = 1,
$$
 (Cramér-von Mises)  
\n
$$
w(x) = [F(x)(1 - F(x))]^{-1},
$$
 (Anderson-Darling)

where () is a weighting function. Adding the <sup>2</sup> statistics on top of Equation [\(Cramér-von Mises\)](#page-7-5) recovers the

<span id="page-8-2"></span>![](./assets/07-lejepa/_page_8_Figure_1.jpeg)

**Figure 6.** <sup>=</sup> <sup>100</sup> samples are drawn from a 1024-dimensional standard Gaussian, and the first <sup>2</sup> coordinates are altered to produce the "X" distribution from Figure [5](#page-7-0) (**left-most column**). For each statistic (**all other columns**), we perform gradient descent on the samples to minimize their value, at each iteration step with sample <sup>=</sup> <sup>10</sup> random directions to evaluate SIGReg (recall def. [2\)](#page-6-4). We obtain that albeit this is a high-dimensional distribution with limited number of samples, SIGReg is able to capture the degenerate subspace and adapt the data accordingly to match an isotropic Gaussian distribution. Additional figures with varying dimensions and number of 1d projections are provided in Figure [16.](#page-46-0)

Watson test [\[Watson, 1961\]](#page-22-4)

<span id="page-8-3"></span>
$$
U^2 = T_w - N\left(\bar{F} - \frac{1}{2}\right)^2.
$$
 (Watson)

We do not consider the Kolmogorov-Smirnov test [\[Kol](#page-20-15)[mogorov, 1933\]](#page-20-15) as it employs the ℓ∞-norm instead of the ℓ2-norm hereby producing sparse gradients. Another common test is the Shapiro-Wilk test [\[Shapiro and Wilk,](#page-21-15) [1965\]](#page-21-15) which we found to be unstable in practice–details are provided in Section [E.](#page-42-0)

<span id="page-8-0"></span>**Lack of Scalability and Differentiability.** CDF-based tests require sorting that have been highly optimized, e.g., with the ( log()) Quicksort algorithm [\[Hoare, 1962\]](#page-19-15) but that nonetheless breaks the embarrassingly parallel nature of SGD–especially on multi-GPU [\[Tanasic et al., 2013,](#page-21-16) [Maltenberger et al., 2022\]](#page-20-16) due to synchronization requirements. Moreover, these tests involve non-differentiable operations (sorting and order statistics), making them unsuitable for gradient-based optimization without relaxations [\[Cuturi et al., 2019,](#page-18-14) [Grover et al., 2019,](#page-19-16) [Petersen](#page-20-17) [et al., 2022\]](#page-20-17). While there exists intricate sketching solutions [\[Dunning and Ertl, 2019,](#page-18-15) [Masson et al., 2019,](#page-20-18) [Dunning,](#page-18-16) [2021\]](#page-18-16), each of those solutions introduce numerous additional hyper-parameters–going against our first motivation for LeJEPA.

### **4.2.3 Characteristic Functions are Stable, Scalable and Identifiable**

The third family of tests is concerned with Empirical Characteristic Functions (ECF) which are the Fourier transform of the density function. The Epps–Pulley test [\[Epps and](#page-18-17) [Pulley, 1983\]](#page-18-17) is one of the most popular test and simply compares in weighted ℓ2-norm the ECF of the data against a target CF

<span id="page-8-1"></span>
$$
EP = N \int_{-\infty}^{\infty} \left| \hat{\phi}_X(t) - \phi(t) \right|^2 w(t) dt.
$$
 (Epps-Pulley)

The first crucial observation is that the ECF being defined as <sup>ˆ</sup> () <sup>=</sup> 1 Í =1 is naturally differentiable and easily computed in distributed settings via efficient all\_reduce operations, as the ECF is a simple average of complex exponentials. The weight function is typically Gaussian, such as () <sup>=</sup> − 2 / 2 with commonly set to 1.

Other tests, e.g., based on the Entropy [\[Székely and](#page-21-17) [Rizzo, 2005\]](#page-21-17) are not considered here as they require numerous additional design choices for the univariate Entropy estimation [\[Silverman, 2018,](#page-21-18) [Beirlant et al., 1997\]](#page-18-18), e.g., using kernels [\[Joe, 1989\]](#page-19-17), or M-estimators [\[Miller, 2003\]](#page-20-19).

**Epps-Pulley has bounded loss, gradient and curvature.** We now consider the remaining two families of tests: moment-based and CF-based. First, recall that moments are polynomial in the data and with extreme growth rate

<span id="page-9-1"></span>**Algorithm 1.** SIGReg with Epps-Pulley statistic with DDP support and () time and memory complexity. x is a (N, K) tensor, num\_slices is |A| in def. [2,](#page-6-4) 'global\_step' is used for sync. sampling across GPUs and can be omited for single-GPU training. An optimized implementation with caching is also provided in our official codebase, computation times provided in Table [6.](#page-42-1)

```
def SIGReg ( x , g l o b a l _ st e p , num_slices =256) :
     # s l i c e sampling −− synced ac ross de vi ce s −−
     dev = di c t ( de vi ce=x . de vi ce )
     g = t o r c h . Gene rato r (∗ ∗ dev )
     g . manual_seed ( g l o b a l _ st e p )
     p roj_shape = ( x . s i z e ( 1 ) , num_slices )
     A = t o r c h . randn ( p roj_shape , g e n e r at o r=g , ∗∗dev )
     A /= A. norm ( p=2 , dim=0)
     # −− Epps−P u l l e y s t a t . see Sec . 4.3 f o r a l t . −−
     # i n t e g r a t i o n p o i nt s
     t = t o r c h . l i n s p a c e ( −5 , 5 , 17 , ∗∗dev )
     # t h e o r e t i c a l CF f o r N( 0 , 1 ) and Gauss . window
     exp_f = t o r c h . exp ( −0.5 ∗ t ∗ ∗2 )
     # e m p i r i c a l CF −− gathe red ac ross de vi ce s −−
     x _t = ( x @ A) . unsqueeze ( 2 ) ∗ t # (N, M, T)
     e cf = (1 j ∗ x _t ) . exp ( ) . mean( 0 )
     e cf = a l l _ r e d u c e ( ecf , op="AVG" )
     # weighted L2 d i st a n c e
     e r r = ( e cf − exp_f ) . abs ( ) . square ( ) . mul ( exp_f )
     N = x . s i z e ( 0 ) ∗ w o r l d _ s i z e
     T = t o r c h . t r a p z ( e r r , t , dim=1) ∗ N
     re tu rn T
```
for higher moment–assuming they even exist. Even for well-behaved distributions, raising values to a power of can quickly lead to exploding gradients. This comes in sharp contrast with the ECF which is always bounded and with bounded gradients for any input distribution for the projected samples <sup>=</sup> ⊤ (), <sup>=</sup> <sup>1</sup>, . . . , .

<span id="page-9-2"></span>**Theorem 4: Stability of Epps-Pulley Test** [\(Epps–Pulley\)](#page-8-1) satisfies for samples 1, . . . , (**a**) ≤ 4 2 , 2(**a**) 2 ≤ √ <sup>3</sup> 2 , with constant , and bandwidth . (Proof in Section [B.12.](#page-36-1))

By the chain rule, thm. [4](#page-9-2) directly gives ∥∇(**a**)∥ <sup>≤</sup> 4 2 Í =1 ∥**a** <sup>⊤</sup>∇ (**x**)∥, providing stable gradients. The limitations of moment-based and CDF-based tests coupled with thm. [4](#page-9-2) justifies our choice of the [\(Epps–Pulley\)](#page-8-1): (i) DDP-friendly and scalable, (ii) uniformly bounded gradients and curvature regardless of input distribution, and (iii) hyper-parameter free implementation. Lastly, we highlight that *our implementation has a linear memory and computational complexity of* ()*, with the minibatch size*. The implementation of SIGReg using that statistical test is provided in algorithm [1,](#page-9-1) along with computation times of the forward-backward pass in Table [6.](#page-42-1)

As a last step before introducing LeJEPA, we ought to

<span id="page-9-3"></span>![](./assets/07-lejepa/_page_9_Figure_7.jpeg)

**Figure 7.** Expected directional statistic at the end of training (**y-axis**) for varying (number of directions used at each training step, **x-axis**). The directions are either resampled (**green**) or kept fixed (**blue**) at each training step. While for fixed directions we benefit from thm. [5](#page-10-1) bound where increasing reduces the overall expected loss, being able to resample at every step provides significant coverage boost for free.

study the requirements on the number of directions (|A|) for [\(2\)](#page-6-4) to be effective in high-dimension.

## <span id="page-9-0"></span>**4.3 How SIGReg Beats the Curse of Dimensionality**

This last section seeks to characterize how many slices in A one must sample for [\(SIGReg\)](#page-6-5) to be an effective statistical test. That design is crucial if we hope for LeJEPA to successfully converge towards isotropic Gaussian embeddings.

### **Smoothness Beats the Curse of Dimensionality**

Our first argument arguing for a favorable scaling of |A| with the embedding dimension relies on the smoothness of as measured by its Sobolev regularity [\[Adams](#page-17-7) [and Fournier, 2003\]](#page-17-7). We formalize below a bound on the directional test from Equation [\(3\)](#page-6-1) over all possible directions when the test statistic is minimized over <sup>|</sup>A<sup>|</sup> <sup>=</sup> directions. While we provide bounds on the expected discrepancy over random directions when the EP test is satisfied (equals zero) on a finite set of directions, the provided proof includes the case of moment-based and CDF-based tests as well.

### <span id="page-10-1"></span>**Theorem 5: Unified Error Bounds**

Let <sup>∈</sup> (R ), ∼ (−<sup>1</sup> ), and [\(Epps–Pulley\)](#page-8-1)= 0, i.e., (**a**) <sup>=</sup> (**a**) , <sup>∀</sup> <sup>∈</sup> <sup>A</sup>, then

$$
\begin{aligned} \mathbb{E}_a\left[\int_{\mathbb{R}}\left|\varphi_a(t)-\varphi_{\mathcal{N}}(t)\right|^2dt\right] &\leq C(K,\alpha)|\mathbb{A}|^{-2\alpha/(K-1)}\\ &\times \int_0^\infty \left\|\varphi_{\cdot}(r)-\varphi_{\mathcal{N}}(r)\right\|_{H^\alpha(\mathcal{S}^{K-1})}^2dr, \end{aligned}
$$

(Proof in Section [B.10.](#page-35-1))

As |A| → ∞, the bound decays as |A| <sup>−</sup>2/(−1) , showing that <sup>|</sup>A<sup>|</sup> <sup>=</sup> () directions suffice for -approximation when is large. Some examples of embedding densities with varying are provided in Figure [4.](#page-6-7) The following statement characterizes how the directions actually constrain the entire space as a function of . The constant (, ) <sup>=</sup> 2 <sup>2</sup> (−1)/2Γ(<sup>+</sup> −1 2 ) (−1)Γ()Γ( −1 2 ) is visualized in Figure [15](#page-41-0) (left) depicting how and |A| interact. In words, we obtain that thanks to the natural smoothness of DN–either stemming from the architecture or the implicit and explicit regularizers used during training–applying SIGReg on |A| directions can be sufficient to tightly constrain the entire space. We note that considering the worst case over or using low-discrepancy sequences for does not impact the asymptotic bounds, details provided in Section [D.](#page-40-0)

### **SGD Beats the Curse of Dimensionality**

Our second argument leverages the iterative nature of DN training. Although we may use only |A| to be a few hundreds, the cumulative number of sampled directions grows linearly with training time. This resampling effect (illustrated in Figure [7,](#page-9-3) bottom) enables rapid convergence. Even small |A| achieves tight distributional matching compared to keeping the set A fixed throughout minibatches (recall thm. [5\)](#page-10-1). Our experiments show that even with |A| as low as 16 can easily outperform a fixed set with |A| of order of thousands thanks to the compounding effect of resampling at each minibatch.

### **Empirical Validation on Synthetic Data**

We conclude this section with a controlled experiment applying [\(SIGReg\)](#page-6-5) with gradient-based training to produce isotropic embeddings. In this setup, we directly consider embeddings which we will differentiate and optimized to minimize [\(SIGReg\)](#page-6-5). By directly optimizing the embeddings we are able to observe the impact of the loss without any possible constraint and regularization that would come from the architecture. We sample i.i.d. samples in a -dimensional space. This sampling is based on an isotropic Gaussian distribution–but the first

<span id="page-10-3"></span>**Algorithm 2.** LeJEPA implementation–works out-of-the-box on any dataset, with DDP, with any backbone, e.g., torchvision or timm. For non-ViT architectures (e.g., ResNet), set global\_views = all\_views. We use bs for the minibatch size, SIGReg is from algorithm [1.](#page-9-1)

```
def LeJEPA( global_ view s , a l l _ v i e w s , lambd ) :
     " " " g l o b a l _ v i ew s and a l l _ v i e w s a re l i s t s of
           ten so r s , lambd i s a s c a l a r " " "
     # embedding of g l o b a l views
     g_emb = fo rwa rd ( t o r c h . c at ( glob_views ) )
     # embedding of l o c a l views
     # i f r e s n et : s k i p w it h a_emb=g_emb
     a_emb = fo rwa rd ( t o r c h . c at ( a l l _ v i e w s ) )
     # LeJEPA l o s s
     c e nt e r s = g_emb . view ( −1 , bs , K) . mean( 0 )
     a_emb = a_emb . view ( −1 , bs , K)
     sim = ( c e nt e r s − a_emb) . square ( ) . mean ( )
     s i g r e g = mean(SIGReg(emb, g l o b a l _ st e p ) fo r emb
           in a_emb)
```
**re tu rn** (1−lambd ) ∗sim + lambd∗ s i g r e g

two dimensions are again set to the adversarial "X" shape. That is, among the dimensions, only two must be transformed as all the other ones already obey the isotropic Gaussian target distribution. We then make the samples differentiable and optimize then to minimize the value of the different statistical tests compute on random random directions. Those directions are resampled after each gradient step–which follows the procedure we will employ in LeJEPA. We present the results in Figure [6](#page-8-2) demonstrating that even in challenging case, i.e., <sup>=</sup> <sup>512</sup> and <sup>=</sup> 16, SIGReg is able to detect the two degenerate dimensions and unfold them back to how they should look like under the target distribution.

## <span id="page-10-0"></span>**5 LeJEPA: Stable and Scalable Implementation**

Having established that isotropic Gaussians are the optimal embedding distribution for foundation models (Section [3\)](#page-4-0) and introduced SIGReg to achieve this distribution (def. [2\)](#page-6-4), we now present the complete LeJEPA framework. We first evaluate candidate statistical tests (Sections [4.2.1](#page-6-6) and [4.2.2\)](#page-7-1) and identify characteristic function-based tests as optimal for gradient-based training (Section [4.2.3\)](#page-8-0). The full LeJEPA implementation follows in Section [5.1.](#page-10-2)

## <span id="page-10-2"></span>**5.1 LeJEPA: SIGReg + Prediction Loss**

We now discuss the implementation of LeJEPA starting with SIGReg and followed by the prediction and total losses.

**The SIGReg Loss.** We chose [\(Epps–Pulley\)](#page-8-1) for its provable boundedness (thm. [4\)](#page-9-2) and its scalability. Its implementation follows exactly the equation except for the integrate which is estimated using a quadrature approximation. We

find that the simple trapezoidal quadrature rule is sufficient even with as few knots as 17, as ablated in Figure [20.](#page-49-0) In particular, we leverage the symmetry of the integrand to double the number of knots for free, see the official code. On the other hand, the use of minibatches introduces a bias vanishing at rate (1/), as formalized below.

### <span id="page-11-3"></span>**Theorem 6: Vanishing gradient bias**

The expectation of [\(Epps–Pulley\)](#page-8-1) satisfies

$$
\mathbb{E}\left[\widehat{L}_n(\theta)\right] = L(\theta) + \frac{1}{N} \int_{\mathbb{R}} w_s(t) \big(1 - |\varphi_P(t)|^2\big) dt,
$$

therefore both the loss and its derivative have a bias of order (1/). (Proof in Section [B.13.](#page-37-0))

Hence, the gradients we obtain from using [\(Epps–Pulley\)](#page-8-1) are biased by an explicit (1/) term. We found this bias to be minimal and not a concern even for minibatches as small as 16. Unbiased alternatives include using Ustatistic debiasing of || <sup>2</sup> or sample splitting, which we do not explore in this study. Our final implementation of the SIGReg term with Epps-Pulley statistic is provided in algorithm [1.](#page-9-1)

**The Prediction Loss.** To standardize notations, we adopt the DINO [\[Caron et al., 2021\]](#page-18-3) setup of generating global views and local views, leading to a total of <sup>=</sup> <sup>+</sup> views. We set the first <sup>1</sup>, . . . , indices of each , as the global views. For the cases without local views, simply set <sup>=</sup> 0. The prediction loss is then given by having all views predict the global views as

$$
\mathcal{L}_{\text{pred}}(\{z_{n,v}\}_{v=1}^V) = \frac{1}{V_g} \sum_{v=1}^{V_g} \frac{1}{V} \sum_{v'=1}^V ||z_{n,v} - z_{n,v'}||_2^2 \qquad (5)
$$

$$
=\frac{1}{V}\sum_{v'=1}^{V}\left\|\frac{1}{V_{g}}\sum_{v=1}^{V_{g}}z_{n,v}-z_{n,v'}\right\|_{2}^{2}
$$
 (6)

$$
\triangleq \frac{1}{V} \sum_{v'=1}^{V} ||\mu_n - z_{n,v'}||_2^2, \qquad (7)
$$

where we denote <sup>≜</sup> 1 Í =1 ,, the Equation [\(5\)](#page-8-3) to Equation [\(6\)](#page-11-1) derivations are detailed in Section [B.6.](#page-32-0)

**LeJEPA Loss.** The final total loss simply combines the above prediction loss along with SIGReg on each views as per

$$
\mathcal{L}_{\text{LeJERA}}(\{x_{n,v}\}_{n,v=1}^{B,V}) = \frac{\lambda}{V} \sum_{v=1}^{V} \text{SIGReg}(\{\{z_{n,v}\}_{n=1}^{B}\}) + \frac{1-\lambda}{B} \sum_{n=1}^{B} \mathcal{L}_{\text{pred}}^{(V_g)}(\{z_{n,v}\}_{v=1}^{V}).
$$
 (LeJERA)

We present [\(LeJEPA\)](#page-11-2)'s implementation in algorithm [2.](#page-10-3) Altogether, the entire implementation–besides the usual model definitions, optimizers, and data loaders–only takes a few dozens lines in PyTorch (algorithms [1](#page-9-1) and [2\)](#page-10-3). The absence of prototypes, stop-gradients, and teacher-student networks makes [\(LeJEPA\)](#page-11-2) appealing as it only contains one hyperparameter, , balancing the trade-off between the prediction and isotropic Gaussian terms.

## **5.2 Relation to Prior Work**

Prior to presenting our experiments (Section [6\)](#page-11-0), we conclude by discussing how our proposed LeJEPA and SIGReg objective relate to existing frameworks in the literature.

While there is no existing solution employing such slicing and distribution matching for JEPAs, there exists similar pipelines for generative models and optimal transport. Notably, the Sliced Score Matching [\[Song et al., 2020\]](#page-21-19) proposes to leverage univariate slicing of the space to ease the estimation of a density for generative models. In a similar vein, the sliced Wasserstein distance [\[Bonneel et al.,](#page-18-19) [2015,](#page-18-19) [Nguyen and Ho, 2023\]](#page-20-20) uses such strategy to speed up and improve optimal transport. Furthermore, when the integral of the [\(Epps–Pulley\)](#page-8-1) test is computed exactly, as opposed to our quadrature, each slice loss value recovers the kernel MMD [\[Sriperumbudur et al., 2010,](#page-21-20) [Gretton et al.,](#page-19-18) [2012,](#page-19-18) [Chwialkowski et al., 2016\]](#page-18-20) measuring the distance between two distributions–albeit with a quadratic complexity. Lastly, it is possible to recover some existing SSL frameworks in the limit by employing LeJEPA with a particular test–instead of the preferred [\(Epps–Pulley\)](#page-8-1). For example, Setting ({} =1 ) <sup>=</sup> mean({} =1 ) <sup>2</sup> + (std({} =1 ) − 1) 2 and using that with SIGReg in LeJEPA recovers the VICReg SSL method in the limit of large number of slices. In fact, SIGReg will enforce in expectation that E[**Z**] = **0** and Cov(**Z**) <sup>=</sup> **<sup>I</sup>**, where **<sup>I</sup>** denotes the <sup>×</sup> identity matrix–derivations provided in Section [B.14.](#page-39-0) And since our invariance term is simply the <sup>ℓ</sup><sup>2</sup> distance between the views' embeddings, LeJEPA recovers VICReg for this degenerate statistical test. Based on thm. [3,](#page-7-4) we however strongly advocate against such a setting as it would lead to shortcut solutions–a phenomenon already observed in VICReg.

## <span id="page-11-1"></span><span id="page-11-0"></span>**6 LeJEPA: Empirical Validation**

<span id="page-11-2"></span>We now use the LeJEPA implementation described in Section [5.1](#page-10-2) to demonstrate its effectiveness through comprehensive experiments. We show that LeJEPA: (i) trains reliably across diverse architectures and datasets (Section [6.1\)](#page-12-0), (ii) provides an informative training loss for model selection (Section [6.2\)](#page-13-0), (iii) outperforms frontier vision models on small-scale in-domain pretraining (Section [6.3\)](#page-14-0), (iv) scales successfully to nearly 1 billion parameters on ImageNet-1k (Section [6.4\)](#page-16-0), and (v) learns rich

<span id="page-12-1"></span>![](./assets/07-lejepa/_page_12_Figure_1.jpeg)

**Figure 8.** Inet100 with 400 pretraining epochs and resnet50 backbone. We depict linear probe performances as a function of and the number of views (recall [\(LeJEPA\)](#page-11-2)). We observe that performances are stable over –with **peak performance obtain by slightly adjust proportionally to the number of views**. The corresponding performance values are provided in Table [7.](#page-42-2)

semantic segmentation features without explicit supervision.

## <span id="page-12-0"></span>**6.1 LeJEPA's Stability Across Hyper-Parameters and Architectures**

We now demonstrate LeJEPA's stability across hyperparameters, architectures, and experimental setups. Additional cross-domain stability results are presented in Section [6.3.](#page-14-0)

**Stability across standard hyperparameters.** We begin by evaluating LeJEPA on ImageNet-100 and ImageNet-1K. On ImageNet-100, we train a ResNet-50 and vary the number of views and the loss weighting (Figure [8\)](#page-12-1). Performance remains stable across both dimensions, leading us to recommend <sup>=</sup> <sup>0</sup>.<sup>05</sup> as a robust default. On ImageNet-1K, we train a ViT-Large/14 and explore batch size, as well as the number of global (g) and local (l) views (Table [1b](#page-12-2)). We find that the configuration commonly used in prior work (<sup>g</sup> <sup>=</sup> <sup>2</sup>, <sup>l</sup> <sup>=</sup> 8) transfers well to LeJEPA. Notably, LeJEPA achieves competitive performance with batch sizes as small as 128 on ImageNet-1K (Table [1c](#page-12-2)), suggesting reduced memory requirements compared to existing methods. *We thus recommend to use* <sup>=</sup> <sup>0</sup>.05*,* <sup>g</sup> <sup>=</sup> <sup>2</sup>*,* <sup>l</sup> <sup>=</sup> <sup>8</sup>*, and batch size* <sup>≥</sup> <sup>128</sup> *as starting points*.

**Stability across Epps-Pulley hyperparameters.** We next examine hyperparameters specific to LeJEPA: the number of slices || in SIGReg, the integration domain for the Epps-Pulley test [\(Epps–Pulley\)](#page-8-1), and the number of quadrature points for numerical integration. Table [1a](#page-12-2) shows ablations on ImageNet-1K with ViT-Large/14. Both the integration domain and number of quadrature points have negligible impact on performance. This is expected: since the characteristic function is accurate at zero, the

<span id="page-12-2"></span>**Table 1.** ViT/Large-14, on inet1k pretraining for 100 epochs and evaluated with frozen backbone linear probing (top1 accuracy, %).**LeJEPA's performance is stable across all its hyperparameters** and while some may slightly improve performance, e.g., the number of slices |A| and the projector sizes, none of the choices lead to a catastrophic collapse.

| (a) (Epps–Pulley) parameters |            |       |       |                       |  |  |  |
|------------------------------|------------|-------|-------|-----------------------|--|--|--|
| integration                  | num_slices |       |       | config/bstat_n_points |  |  |  |
|                              |            | 5     | 17    | 41                    |  |  |  |
| [−1<br>, 1]                  | 512        | 71.82 | 72.13 | 72.04                 |  |  |  |
|                              | 2048       | 72.88 | 72.30 | 72.69                 |  |  |  |
| [−3<br>, 3]                  | 512        | 73.95 | 74.16 | 74.04                 |  |  |  |
|                              | 2048       | 75.02 | 74.68 | 74.77                 |  |  |  |
| [−5<br>, 5]                  | 512        | 73.71 | 74.21 | 74.15                 |  |  |  |
|                              | 2048       | 74.50 | 74.80 | 74.77                 |  |  |  |

|                          | (b) Number of local/global views |       |       |       |       |       |       |       |
|--------------------------|----------------------------------|-------|-------|-------|-------|-------|-------|-------|
| # global_views (𝑉g)      |                                  |       | 1     |       | 2     |       | 4     |       |
| # views (𝑉 =             | 𝑉g +                             | 𝑉l)   |       |       |       |       |       |       |
| 4                        |                                  |       |       | 53.06 | 72.26 |       | –     |       |
| 6                        |                                  |       |       | 58.65 | 73.07 |       |       | 73.68 |
| 8                        |                                  |       |       | 64.46 | 74.24 |       |       | 73.94 |
| 10                       |                                  |       |       | 68.97 | 74.06 |       |       | 75.08 |
|                          | (c) Mini-batch size              |       |       |       |       |       |       |       |
| batch_size               | 128                              |       | 256   |       | 512   |       | 1024  |       |
|                          | 72.20                            |       | 74.15 |       | 74.72 |       | 74.07 |       |
|                          | (d) Embedding/Projector dim.     |       |       |       |       |       |       |       |
| num_slices               |                                  | 1024  |       |       |       | 4096  |       |       |
| emb. dim.<br>proj. dim.  | 512                              |       | 2048  |       | 512   |       | 2048  |       |
| 64                       | 75.29                            |       | 75.32 |       | 75.50 |       | 75.65 |       |
| 128                      | 74.77                            |       | 75.09 |       | 75.26 |       | 75.47 |       |
| 256                      | 74.56                            |       | 74.66 |       | 75.08 |       | 75.02 |       |
| 512                      | 73.94                            |       | 74.11 |       | 74.81 |       | 74.65 |       |
| 1024                     | 73.65                            |       | 73.94 |       | 74.71 |       | 74.79 |       |
|                          | (e) Register tokens              |       |       |       |       |       |       |       |
| reg_tokens<br>num_slices | 0                                | 1     |       | 2     |       | 4     |       | 8     |
| 1024                     | 75.14                            | 75.18 |       | 75.08 |       | 75.34 |       | 75.23 |
| 4096                     | 75.61                            | 75.58 |       | 75.67 |       | 75.63 |       | 75.84 |

moments of the distribution are well-characterized even with a modest integration range. The number of slices || has a modest effect—while more slices slightly improve performance, even 512 slices yield competitive results. *We thus recommend to use 17 integration points, an integration domain of* [−5, <sup>5</sup>]*, and 1024 slices as starting points*.

![](./assets/07-lejepa/_page_13_Figure_1.jpeg)

### Inet10 | LeJEPA pretrained, frozen backbone, linear eval | 50 architectures ( < 20M params.)

**Figure 9.** INet10 pretraining and frozen backbone linear evaluation across 50 timm models using LeJEPA out of the box. We cross-validate the learning rate and weight-decay. While there is a small variation between the best and worst performing model, we clearly see that **across** 50 **models spanning** 8 **families, LeJEPA is able to produce non-trivial representations able to solve the downstream task at SOTA levels**.

**Stability across architectures.** A key advantage of LeJEPA over recent methods (e.g., IJEPA, DINOv2) is its architecture-agnostic design. While most modern selfsupervised methods are tailored to Vision Transformers, LeJEPA works across diverse architecture families without modification. To validate this claim, we pretrain approximately 50 architectures from 8 different families on ImageNet-10, selecting all models in the timm library with fewer than 20M parameters. All models are able to learn high-quality representations reaching between 91.5% to 95% top 1 accuracy with frozen backbone linear probing. It seems that models performing well in supervised learning setups are also the ones to favor for LeJEPA, such as resnets and ViTs. *We thus recommend to use standard architectures such as ResNets and ViTs over specialized models like EfficientNet as stating point.*

**Removal of popular heuristics.**In addition to providing reliable performance across models and datasets, LeJEPA's provable construction enables us to *remove* many heuristics traditionally used to prevent collapse. First, prior work has shown both empirically and theoretically that predictors in image JEPA (without asymmetric information) and teacher-student architectures serve primarily to prevent collapse [\[Grill et al., 2020,](#page-19-19) [Jing et al., 2021,](#page-19-3) [Tian et al.,](#page-21-4) [2021,](#page-21-4) [Caron et al., 2021,](#page-18-3) [Chen et al., 2021\]](#page-18-5). Removing these components produces *collapsed* encoders, i.e., with performances at chance-level. Thanks to LeJEPA's SIGReg loss, we can remove both the predictor and teacher-student architecture without suffering from collapse, as shown in Table [4.](#page-41-1) While a teacher-student configuration does provide a small performance boost for ViT models—consistent with observations in supervised learning via Stochastic

Weight Averaging [\[Izmailov et al., 2019\]](#page-19-20)—it is not necessary to prevent collapse. In our setup, we apply SWA on the encoder producing in Equation [\(6\)](#page-11-1). Second, recent work demonstrated that register tokens are needed to prevent training instabilities in vision models [\[Oquab et al.,](#page-20-10) [2023,](#page-20-10) [Siméoni et al., 2025,](#page-21-21) [Darcet et al., 2023\]](#page-18-21). We show in Table [1](#page-12-2) that such instabilities likely stem from poorly conditioned training objectives. In contrast, LeJEPA *does not*require register tokens and achieves stable performance with or without them. *We thus recommend training without a predictor or register tokens, and optionally applying SWA with ViTs for a possible performance gain.*

### **Experiment Details 1**

We strive for **simplicity** and thus adopt a unified pretraining pipeline. The following parameters apply to *all* experiments and figures unless stated otherwise in the corresponding caption and come from Section [6.1:](#page-12-0)

- LeJEPA's implementation is given in algorithm [2](#page-10-3) with hyperparameter
- All backbones are from timm and all optimizers/schedulers are from PyTorch without modifications
- We employ eight views ( <sup>=</sup> 8) containing two global views (<sup>g</sup> <sup>=</sup> 2) with resolution 224x224 and 96x96 for the local views
- AdamW optimizer with lr ∈ {5 <sup>−</sup> <sup>3</sup>, <sup>5</sup> <sup>−</sup> <sup>4</sup>} and wd <sup>∈</sup> {1 <sup>−</sup> <sup>1</sup>, <sup>1</sup> <sup>−</sup> <sup>2</sup>, <sup>1</sup> <sup>−</sup> <sup>5</sup>}–no scheduler on weight-decay, standard linear warm-up cosine-annealing for lr

## <span id="page-13-0"></span>**6.2 LeJEPA's Training Loss is Informative of Downstream Performance**

A major challenge in SSL pretraining is the lack of reliable signals conveying the quality of the learned representation. As a result, it is common to monitor a supervised

**LeJEPA:** [Sec 1: Intro](#page-1-0) | [Sec 2: Background](#page-2-0) | [Sec 3: Why Gaussian?](#page-4-0) | [Sec 4: SIGReg](#page-5-0) | [Sec 5: LeJEPA](#page-10-0) | **[Sec 6: Experiments](#page-11-0)**

<span id="page-14-2"></span>![](./assets/07-lejepa/_page_14_Figure_1.jpeg)

**Figure 10.** (SIGReg, prediction loss) <sup>2</sup>-plane with downstream task accuracy shown with colors from **blue** (low) to **red** (high). We clearly observe that within this plane, **there exists trade-off fronts between the two terms of LeJEPA producing similar downstream performance** corresponding to different values of . Yet, those fronts are linear and pointed towards the lower left corner, i.e., LeJEPA's training loss informs of downstream test performance across models and datasets (**columns**). Additional models and datasets provided in Figure [21.](#page-49-1)

<span id="page-14-3"></span>![](./assets/07-lejepa/_page_14_Figure_3.jpeg)

**Figure 11.** Spearman correlation (**y-axis)** between LeJEPA's training loss and downstream accuracy on the dataset's classification task with a frozen backbone and linear evaluation. The **x-axis** varies in Equation [\(8\)](#page-14-1) following our scaling law of the loss w.r.t. . Using = 0 recovers the plain training loss. We clearly observe a very high correlation already for <sup>=</sup> 0, which further increases up to 99% for <sup>=</sup> <sup>0</sup>.4. The entire set of points is obtained across numerous hyper-parameters such as learning rate, weight decay, number of epochs, –demonstrating how **LeJEPA's training loss is strongly predictive of downstream performance** which can be used for label-free cross-validation.

downstream task performance, sometimes supplemented with unsupervised embedding statistics [\[Agrawal et al.,](#page-17-8) [2022,](#page-17-8) [Garrido et al., 2023,](#page-19-21) [Thilak et al., 2023\]](#page-21-22). This process is highly limiting since it requires labeled data that is costly and overly specialized. This is further exacerbated in the latest JEPA models where training losses exhibit low correlation with downstream performance–and may not even decrease monotonically during training.

In contrast, we find that LeJEPA's training loss behaves much more favorably–providing us with a meaningful signal on model quality. First, we provide in Figure [10,](#page-14-2) the 2D plane spanned by the SIGReg and prediction losses

where a clear trend with downstream task accuracy can be observed. More strikingly, the combined training loss [\(LeJEPA\)](#page-11-2) with mixing coefficient exhibits very high Spearman correlation [\[Spearman, 1961\]](#page-21-23), denoted as , of about 85% with downstream accuracy–which is considered a strong signal. This strong relationship holds across datasets and architectures. As a result, a lower LeJEPA training loss reliably indicates a better downstream performance.

We can further improve this correlation through a simple scaling law based upon the trade-off weighting hyperparameter

<span id="page-14-1"></span>
$$
C^{(\alpha)} = \rho_s \left( \frac{\text{train\_loss}}{\lambda^{\alpha}}, \text{test\_accuracy} \right). \tag{8}
$$

By setting <sup>≈</sup> <sup>0</sup>.4, LeJEPA's training loss is able to achieve nearly 99% correlation with downstream performance across multiple datasets and models. We depict the changes in () as a function of on multiple datasets and models in Figure [11,](#page-14-3) as well as the training LeJEPA loss against downstream performance in Figure [19.](#page-48-1) **The strong alignment between LeJEPA's training loss and model quality enables label-free SSL model selection and cross-validation**.

## <span id="page-14-0"></span>**6.3 In-Domain LeJEPA Outperforms Frontier Model Transfer Learning**

A key promise of self-supervised learning is to learn universal representations that generalize across tasks and domains. However, current frontier foundation models (e.g., DINOv2/v3, IJEPA) are pretrained on natural images forcing practitioners in specialized domains to collect large amount of labels for supervised finetuning. In fact, most frontier models can not be trained directly on those domains as the number of samples may be small and searching again for the hyper-parameters would be cum-

**LeJEPA:** [Sec 1: Intro](#page-1-0) | [Sec 2: Background](#page-2-0) | [Sec 3: Why Gaussian?](#page-4-0) | [Sec 4: SIGReg](#page-5-0) | [Sec 5: LeJEPA](#page-10-0) | **[Sec 6: Experiments](#page-11-0)**

<span id="page-15-0"></span>![](./assets/07-lejepa/_page_15_Figure_1.jpeg)

**Figure 12. Small architecture in-domain (Galaxy10) LeJEPA pretraining** with linear probe evaluation using frozen backbone or full finetuning (**columns**) and with varying number of samples per class (**x-axis)**. We compare against state-of-the-art foundation models (DINOv2/v3, IJEPA) over 3 different random seeds. We observe that **LeJEPA enables in-domain pretraining out of the box across architectures and able to outperform frontier foundation models**. Corresponding numbers are provided in Table [3.](#page-41-2)

<span id="page-15-1"></span>**Table 2.** Few-shot classification accuracy (percentages) on 8 datasets spanning textures, objects, and fine-grained categories. **Our LeJEPA achieves superior performance on fine-grained tasks (DTD, flowers102, food101) while requiring only 100 pretraining epochs compared to I-JEPA's 300 epochs—a 3× reduction in training time and computational resources without sacrificing downstream task performance.** This efficiency gain is particularly valuable for practical applications where training budget is limited. Bold indicates best performance within the IN-1K comparison group, all numbers are percentages.

|     |                          |      |                            |     |       |                   |      |       | Dataset |                                  |                   |      |       |
|-----|--------------------------|------|----------------------------|-----|-------|-------------------|------|-------|---------|----------------------------------|-------------------|------|-------|
|     | shots model              |      | params pretrain epochs DTD |     |       | aircr.            |      |       |         | cars cifar10 cifar100 flowers102 | food              | pets | avg.  |
|     | LeJEPA ViT-L             | 304M | IN-1K                      | 100 | 33.21 | 9.37              | 3.40 | 51.65 | 27.01   |                                  | 48.53 17.14 46.11 |      | 29.55 |
|     | LeJEPA ConvNeXtV2-H 660M |      | IN-1K                      | 100 | 32.15 | 8.07              | 4.28 | 50.95 | 31.48   |                                  | 48.74 17.95 58.98 |      | 31.58 |
| 1   | I-JEPA ViT-H             | 632M | IN-1K                      | 300 | 27.71 | 9.86              | 4.33 | 56.52 | 30.58   |                                  | 44.69 14.53 53.38 |      | 30.20 |
|     | I-JEPA ViT-H + STOP      | 632M | IN-1K                      | 300 |       | 26.60 11.18       | 4.75 | 56.27 | 35.20   |                                  | 47.17 15.75 59.47 |      | 32.05 |
|     | I-JEPA ViT-H (22K)       | 632M | IN-22K                     | 900 |       | 27.98 13.00       | 3.45 | 61.84 | 34.70   |                                  | 89.72 19.62 30.86 |      | 35.15 |
|     | LeJEPA ViT-L             | 304M | IN-1K                      | 100 |       | 64.72 35.25 22.25 |      | 85.15 | 59.77   |                                  | 92.53 50.90 77.00 |      | 60.95 |
|     | LeJEPA ConvNeXtV2-H 660M |      | IN-1K                      | 100 |       | 61.84 30.67 24.46 |      | 85.74 | 63.29   |                                  | 91.78 49.32 78.53 |      | 60.70 |
| 10  | I-JEPA ViT-H             | 632M | IN-1K                      | 300 |       | 57.68 33.82 21.96 |      | 88.77 | 66.42   |                                  | 88.24 43.97 83.23 |      | 60.51 |
|     | I-JEPA ViT-H + STOP      | 632M | IN-1K                      | 300 |       | 57.00 39.77 25.21 |      | 90.09 | 70.32   |                                  | 90.16 45.68 85.13 |      | 62.92 |
|     | I-JEPA ViT-H (22K)       | 632M | IN-22K                     | 900 |       | 58.74 43.52 18.27 |      | 94.83 | 75.23   |                                  | 98.94 49.06 67.66 |      | 63.28 |
|     | LeJEPA ViT-L             | 304M | IN-1K                      | 100 |       | 78.30 57.01 57.28 |      | 96.50 | 83.71   |                                  | 91.21 82.05 89.74 |      | 79.48 |
|     | LeJEPA ConvNeXtV2-H 660M |      | IN-1K                      | 100 |       | 76.60 52.99 54.88 |      | 96.15 | 81.34   |                                  | 91.11 77.64 89.76 |      | 77.56 |
| all | I-JEPA ViT-H             | 632M | IN-1K                      | 300 |       | 73.32 56.61 54.47 |      | 97.54 | 86.42   |                                  | 86.47 81.02 92.11 |      | 78.50 |
|     | I-JEPA ViT-H + STOP      | 632M | IN-1K                      | 300 |       | 73.87 61.95 61.27 |      | 98.02 | 87.78   |                                  | 88.08 81.72 92.88 |      | 80.70 |
|     | I-JEPA ViT-H (22K)       | 632M | IN-22K                     | 900 |       | 75.67 65.39 49.79 |      | 98.46 | 89.95   |                                  | 98.54 81.58 87.19 |      | 80.82 |

<span id="page-15-2"></span>![](./assets/07-lejepa/_page_15_Picture_5.jpeg)

**Figure 13. Emergent Object Segmentation via Last Layer Thresholding.** LeJEPA naturally learns to segment and track salient objects (shown in attention maps on the right of each video) without explicit supervision. The results display impressive visual quality and strong temporal consistency across video frames (*videos provided on our [project page](https://rbalestr-lab.github.io/lejepa/)*). This emergent capability demonstrates the rich semantic representations learned through our self-supervised approach.

<span id="page-16-1"></span>![](./assets/07-lejepa/_page_16_Picture_1.jpeg)

**Figure 14. LeJEPA learns rich semantic representations through self-supervised learning.** PCA visualization of last-layer features from LeJEPA (ViT-Large, 100 epochs on ImageNet-1K). For each image, features are independently projected to RGB using the first 3 principal components. Without any supervision, LeJEPA spontaneously develops semantically meaningful representations: notice how warm colors (red/ magenta/pink) consistently capture foreground objects (parrot bodies, dog face), while cool colors (cyan/green/yellow) represent backgrounds and foliage. This emergent object-background separation and perceptual grouping discovered the visual structure of the world purely from unlabeled data.

bersome yet necessary [\[Assran et al., 2022\]](#page-17-9).

To demonstrate LeJEPA's versatility and ability to resolve that current pain-point, we propose to pretrain directly on a new domain without any change in the loss or the pretraining pipeline. We select the Galaxy10 dataset, a galaxy morphology classification task that differs significantly from natural images in both visual structure and statistical properties [\[Balestriero et al., 2025\]](#page-17-10). The dataset contains 11,000 training samples across 10 galaxy types. For LeJEPA, we use the default hyper-parameters and pretrain for 400 epochs a variety of backbones. We compare against the latest DINOv2, DINOv3 and IJEPA. We report in Figure [12](#page-15-0) the top1 accuracy for linear probing both with frozen backbone and full-finetuning. We observe that **in-domain pretraining with LeJEPA substantially outperforms state-of-the-art frontier models (DINOv2, DINOv3) on both linear probing and full finetuning**. Additional datasets and backbones are provided in Table [5](#page-42-3) depicting LeJEPA's ability to train in-domain, even with a dataset with 1000 samples (flowers102). Coupling this result with the stability of LeJEPA across architectures and hyper-parameters should offer a promising alternatives in domains not yet accounted for by the latest frontier models.

## <span id="page-16-0"></span>**6.4 LeJEPA Scales Across Data and Models**

We now propose to apply LeJEPA over a larger pretraining dataset, i.e., Imagenet-1k, and over larger backbones such as ViT/Large (0.3B), ConvNextV2-Huge (0.6B). For those two models, we reach an online linear probe accuracy on inet1k of 77.1% and 78.5% respectively. Beyond in-distribution performances, we also explore transfer learning. For those experiments, our baselines are IJEPA with a ViT-Huge (0.6B) which is the closest to our setup, and we also include a recent improved version of IJEPA including additional stochastic prediction tasks [\[Bar et al.,](#page-17-11) [2023\]](#page-17-11) that is coined IJEPA + STOP. For LeJEPA, we employ the same recipe as described in Section [6.1](#page-12-0) and report transfer learning performances with frozen backbone in Table [2.](#page-15-1) We observe that we consistently outperform IJEPA while employed a smaller model and shorted training schedule. Beyond top1 accuracy, we also echo our findings from Section [6.2](#page-13-0) about LeJEPA's training loss quality. In our setup, we observe a very stable and smooth training curve indicating a stable optimization landscape removing the need for careful hyperparameter selection (recall thm. [4\)](#page-9-2). We provide an example on a ViT-gigantic (1.8B parameters) in Figure [1.](#page-0-0)

## **6.5 Emergent Semantic Structure in LeJEPA Representations**

A hallmark of successful self-supervised learning is the emergence of semantically meaningful attention patterns without explicit supervision [\[Caron et al., 2021\]](#page-18-3). To assess whether LeJEPA learns such structure, we visualize the attention maps of the learned representations. Following DINO [\[Caron et al., 2021\]](#page-18-3), we apply PCA to the embeddings and visualize the first principal components, which reveal clear correspondence to object boundaries and salient regions (Figure [14\)](#page-16-1). Furthermore, we explore whether these attention patterns can enable unsupervised video segmentation—a challenging task requiring temporal consistency and object understanding. By thresholding the self-attention maps of the [CLS] token, we obtain binary masks that track objects across frames without any segmentation labels during training. As shown in Figure [13,](#page-15-2) **LeJEPA's attention naturally segments foreground objects from background with remarkable temporal coherence**, suggesting that the learned representations capture both spatial semantics and temporal structure. This emergent capability demonstrates that LeJEPA's stabilityfocused objective does not sacrifice the semantic richness of learned features.

# **7 Conclusion**

We have established a principled theoretical framework for JEPA-based self-supervised learning that fundamentally resolves its core pathologies. Our contributions span theory and practice: we proved that isotropic Gaussian embeddings uniquely minimize worst-case downstream risk, introduced SIGReg as a tractable and provably correct method to enforce this distribution, and demonstrated that this approach eliminates representational collapse by design–and not through ad-hoc combinations of teacherstudent networks, stop-gradients, or asymmetric architectures.

We validate LeJEPA across domains and over 60 architectures including gigantic versions with 1.8B parameters. In spite of its simplicify , LeJEPA matches state-of-the-art performance while requiring fewer than 50 lines of core implementation. Critically, our approach provides what SSL has long needed: a mathematically rigorous foundation that directly informs practical algorithm design.

# **Acknowledgments**

We would like to thank Mike Rabbat and Lucas Maes for providing valuable feedbacks on the manuscript.

# **References**

<span id="page-17-5"></span>Haneen Arafat Abu Alfeilat, Ahmad BA Hassanat, Omar Lasassmeh, Ahmad S Tarawneh, Mahmoud Bashir Alhasanat, Hamzeh S Eyal Salman, and VB Surya Prasath. Effects of distance measure choice on k-nearest neighbor classifier performance: a review. *Big data*, 7(4):221–248, 2019.

- <span id="page-17-7"></span>Robert A Adams and John JF Fournier. *Sobolev spaces*, volume 140. Elsevier, 2003.
- <span id="page-17-8"></span>Kumar K Agrawal, Arnab Kumar Mondal, Arna Ghosh, and Blake Richards. a-req: Assessing representation quality in self-supervised learning by measuring eigenspectrum decay. *Advances in Neural Information Processing Systems*, 35:17626–17638, 2022.
- <span id="page-17-6"></span>Theodore W Anderson and Donald A Darling. Asymptotic theory of certain" goodness of fit" criteria based on stochastic processes. *The annals of mathematical statistics*, pages 193–212, 1952.
- <span id="page-17-9"></span>Mahmoud Assran, Randall Balestriero, Quentin Duval, Florian Bordes, Ishan Misra, Piotr Bojanowski, Pascal Vincent, Michael Rabbat, and Nicolas Ballas. The hidden uniform cluster prior in self-supervised learning. *arXiv preprint arXiv:2210.07277*, 2022.
- <span id="page-17-3"></span>Mahmoud Assran, Quentin Duval, Ishan Misra, Piotr Bojanowski, Pascal Vincent, Michael Rabbat, Yann LeCun, and Nicolas Ballas. Self-supervised learning from images with a joint-embedding predictive architecture. In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, pages 15619–15629, 2023.
- <span id="page-17-1"></span>Randall Balestriero and Yann LeCun. Contrastive and noncontrastive self-supervised learning recover global and local spectral embedding methods. *Advances in Neural Information Processing Systems*, 35:26671–26685, 2022.
- <span id="page-17-4"></span>Randall Balestriero and Yann LeCun. Learning by reconstruction produces uninformative features for perception. *arXiv preprint arXiv:2402.11337*, 2024.
- <span id="page-17-0"></span>Randall Balestriero, Mark Ibrahim, Vlad Sobal, Ari Morcos, Shashank Shekhar, Tom Goldstein, Florian Bordes, Adrien Bardes, Gregoire Mialon, Yuandong Tian, et al. A cookbook of self-supervised learning. *arXiv preprint arXiv:2304.12210*, 2023.
- <span id="page-17-10"></span>Randall Balestriero, Nicolas Ballas, Mike Rabbat, and Yann LeCun. Gaussian embeddings: How jepas secretly learn your data density. *arXiv preprint arXiv:2510.05949*, 2025.
- <span id="page-17-11"></span>Amir Bar, Florian Bordes, Assaf Shocher, Mahmoud Assran, Pascal Vincent, Nicolas Ballas, Trevor Darrell, Amir Globerson, and Yann LeCun. Stochastic positional embeddings improve masked image modeling. *arXiv preprint arXiv:2308.00566*, 2023.
- <span id="page-17-2"></span>Adrien Bardes, Jean Ponce, and Yann LeCun. Vicreg: Variance-invariance-covariance regularization for selfsupervised learning. *arXiv preprint arXiv:2105.04906*, 2021.
- <span id="page-18-18"></span>Jan Beirlant, Edward J Dudewicz, László Györfi, Edward C Van der Meulen, et al. Nonparametric entropy estimation: An overview. *International Journal of Mathematical and Statistical Sciences*, 6(1):17–39, 1997.
- <span id="page-18-11"></span>Chris M Bishop. Training with noise is equivalent to tikhonov regularization. *Neural computation*, 7(1):108– 116, 1995.
- <span id="page-18-10"></span>Christopher M Bishop and Nasser M Nasrabadi. *Pattern recognition and machine learning*, volume 4. Springer, 2006.
- <span id="page-18-26"></span>Gunnar Blom. *Statistical estimates and transformed betavariables*. PhD thesis, Almqvist & Wiksell, 1958.
- <span id="page-18-19"></span>Nicolas Bonneel, Julien Rabin, Gabriel Peyré, and Hanspeter Pfister. Sliced and radon wasserstein barycenters of measures. *Journal of Mathematical Imaging and Vision*, 51(1):22–45, 2015.
- <span id="page-18-0"></span>Jane Bromley, Isabelle Guyon, Yann LeCun, Eduard Säckinger, and Roopak Shah. Signature verification using a" siamese" time delay neural network. *Advances in neural information processing systems*, 6, 1993.
- <span id="page-18-7"></span>Jerome S Bruner and Leo Postman. On the perception of incongruity: A paradigm. *Journal of personality*, 18(2): 206–223, 1949.
- <span id="page-18-24"></span>Russel E Caflisch. Monte carlo and quasi-monte carlo methods. *Acta numerica*, 7:1–49, 1998.
- <span id="page-18-12"></span>Torsten Carleman. *Les Fonctions quasi analytiques: leçons professées au College de France*. Gauthier-Villars, 1926.
- <span id="page-18-3"></span>Mathilde Caron, Hugo Touvron, Ishan Misra, Hervé Jégou, Julien Mairal, Piotr Bojanowski, and Armand Joulin. Emerging properties in self-supervised vision transformers. In *Proceedings of the IEEE/CVF international conference on computer vision*, pages 9650–9660, 2021.
- <span id="page-18-2"></span>Ting Chen, Simon Kornblith, Mohammad Norouzi, and Geoffrey Hinton. A simple framework for contrastive learning of visual representations. In *International conference on machine learning*, pages 1597–1607. PmLR, 2020a.
- <span id="page-18-9"></span>Ting Chen, Simon Kornblith, Kevin Swersky, Mohammad Norouzi, and Geoffrey E Hinton. Big self-supervised models are strong semi-supervised learners. *Advances in neural information processing systems*, 33:22243–22255, 2020b.
- <span id="page-18-5"></span>Xinlei Chen, Saining Xie, and Kaiming He. An empirical study of training self-supervised vision transformers. In *Proceedings of the IEEE/CVF international conference on computer vision*, pages 9640–9649, 2021.
- <span id="page-18-20"></span>Kacper Chwialkowski, Heiko Strathmann, and Arthur Gretton. A kernel test of goodness of fit. In *International conference on machine learning*, pages 2606–2615. PMLR, 2016.
- <span id="page-18-1"></span>Romain Cosentino, Anirvan Sengupta, Salman Avestimehr, Mahdi Soltanolkotabi, Antonio Ortega, Ted Willke, and Mariano Tepper. Toward a geometrical understanding of self-supervised contrastive learning. *arXiv preprint arXiv:2205.06926*, 2022.
- <span id="page-18-8"></span>Thomas M Cover. *Elements of information theory*. John Wiley & Sons, 1999.
- <span id="page-18-13"></span>Harald Cramér. On the composition of elementary errors: First paper: Mathematical deductions. *Scandinavian Actuarial Journal*, 1928(1):13–74, 1928.
- <span id="page-18-22"></span>Harald Cramér and Herman Wold. Some theorems on distribution functions. *Journal of the London Mathematical Society*, 1(4):290–294, 1936.
- <span id="page-18-14"></span>Marco Cuturi, Olivier Teboul, and Jean-Philippe Vert. Differentiable ranking and sorting using optimal transport. *Advances in neural information processing systems*, 32, 2019.
- <span id="page-18-21"></span>Timothée Darcet, Maxime Oquab, Julien Mairal, and Piotr Bojanowski. Vision transformers need registers. *arXiv preprint arXiv:2309.16588*, 2023.
- <span id="page-18-23"></span>Josef Dick and Friedrich Pillichshammer. *Digital nets and sequences: discrepancy theory and quasi–Monte Carlo integration*. Cambridge University Press, 2010.
- <span id="page-18-16"></span>Ted Dunning. The t-digest: Efficient estimates of distributions. *Software Impacts*, 7:100049, 2021.
- <span id="page-18-15"></span>Ted Dunning and Otmar Ertl. Computing extremely accurate quantiles using t-digests. *arXiv preprint arXiv:1902.04023*, 2019.
- <span id="page-18-25"></span>Gustav Elfving. The asymptotical distribution of range in samples from a normal population. *Biometrika*, 34(1/2): 111–119, 1947.
- <span id="page-18-17"></span>Thomas W Epps and Lawrence B Pulley. A test for normality based on the empirical characteristic function. *Biometrika*, 70(3):723–726, 1983.
- <span id="page-18-4"></span>Aleksandr Ermolov, Aliaksandr Siarohin, Enver Sangineto, and Nicu Sebe. Whitening for self-supervised representation learning. In *International conference on machine learning*, pages 3015–3024. PMLR, 2021.
- <span id="page-18-6"></span>David Fan, Shengbang Tong, Jiachen Zhu, Koustuv Sinha, Zhuang Liu, Xinlei Chen, Michael Rabbat, Nicolas Ballas, Yann LeCun, Amir Bar, et al. Scaling language-free visual representation learning. *arXiv preprint arXiv:2504.01017*, 2025.
- <span id="page-19-12"></span>Ronald Aylmer Fisher. *Statistical methods for research workers*. Number 5. Oliver and Boyd, 1928.
- <span id="page-19-1"></span>Karl Friston. The free-energy principle: a unified brain theory? *Nature reviews neuroscience*, 11(2):127–138, 2010.
- <span id="page-19-21"></span>Quentin Garrido, Randall Balestriero, Laurent Najman, and Yann Lecun. Rankme: Assessing the downstream performance of pretrained self-supervised representations by their rank. In *International conference on machine learning*, pages 10929–10974. PMLR, 2023.
- <span id="page-19-11"></span>Gene H Golub, Per Christian Hansen, and Dianne P O'Leary. Tikhonov regularization and total least squares. *SIAM journal on matrix analysis and applications*, 21(1): 185–194, 1999.
- <span id="page-19-2"></span>Ian Goodfellow, Yoshua Bengio, Aaron Courville, and Yoshua Bengio. *Deep learning*, volume 1. MIT press Cambridge, 2016.
- <span id="page-19-9"></span>Priya Goyal, Dhruv Mahajan, Abhinav Gupta, and Ishan Misra. Scaling and benchmarking self-supervised visual representation learning. In *Proceedings of the ieee/cvf International Conference on computer vision*, pages 6391– 6400, 2019.
- <span id="page-19-0"></span>Richard Langton Gregory. Perceptions as hypotheses. *Philosophical Transactions of the Royal Society of London. B, Biological Sciences*, 290(1038):181–197, 1980.
- <span id="page-19-18"></span>Arthur Gretton, Karsten M Borgwardt, Malte J Rasch, Bernhard Schölkopf, and Alexander Smola. A kernel two-sample test. *The journal of machine learning research*, 13(1):723–773, 2012.
- <span id="page-19-19"></span>Jean-Bastien Grill, Florian Strub, Florent Altché, Corentin Tallec, Pierre Richemond, Elena Buchatskaya, Carl Doersch, Bernardo Avila Pires, Zhaohan Guo, Mohammad Gheshlaghi Azar, et al. Bootstrap your own latent-a new approach to self-supervised learning. *Advances in neural information processing systems*, 33:21271–21284, 2020.
- <span id="page-19-16"></span>Aditya Grover, Eric Wang, Aaron Zweig, and Stefano Ermon. Stochastic optimization of sorting networks via continuous relaxations. *arXiv preprint arXiv:1903.08850*, 2019.
- <span id="page-19-22"></span>AK Gupta. Estimation of the mean and standard deviation of a normal population from a censored sample. *Biometrika*, 39(3/4):260–273, 1952.
- <span id="page-19-7"></span>Michael Gutmann and Aapo Hyvärinen. Noise-contrastive estimation: A new estimation principle for unnormalized statistical models. In *Proceedings of the thirteenth international conference on artificial intelligence and statistics*, pages 297–304. JMLR Workshop and Conference Proceedings, 2010.
- <span id="page-19-23"></span>JM Hammersley and KW Morton. The estimation of location and scale parameters from grouped data. *Biometrika*, 41(3/4):296–301, 1954.
- <span id="page-19-14"></span>Felix Hausdorff. Momentprobleme für ein endliches intervall. *Mathematische Zeitschrift*, 16(1):220–248, 1923.
- <span id="page-19-6"></span>Kaiming He, Haoqi Fan, Yuxin Wu, Saining Xie, and Ross Girshick. Momentum contrast for unsupervised visual representation learning. In *Proceedings of the IEEE/CVF conference on computer vision and pattern recognition*, pages 9729–9738, 2020.
- <span id="page-19-4"></span>H von Helmholtz et al. Handbook of physiological optics. *Voss, Leipzig*, 1867.
- <span id="page-19-8"></span>R Devon Hjelm, Alex Fedorov, Samuel Lavoie-Marchildon, Karan Grewal, Phil Bachman, Adam Trischler, and Yoshua Bengio. Learning deep representations by mutual information estimation and maximization. *arXiv preprint arXiv:1808.06670*, 2018.
- <span id="page-19-15"></span>C. A. R. Hoare. Quicksort. *The Computer Journal*, 5(1):10–16, 01 1962. ISSN 0010-4620. doi: 10.1093/comjnl/5.1.10. URL <https://doi.org/10.1093/comjnl/5.1.10>.
- <span id="page-19-20"></span>Pavel Izmailov, Dmitrii Podoprikhin, Timur Garipov, Dmitry Vetrov, and Andrew Gordon Wilson. Averaging weights leads to wider optima and better generalization, 2019. URL <https://arxiv.org/abs/1803.05407>.
- <span id="page-19-13"></span>Carlos M Jarque and Anil K Bera. Efficient tests for normality, homoscedasticity and serial independence of regression residuals. *Economics letters*, 6(3):255–259, 1980.
- <span id="page-19-3"></span>Li Jing, Pascal Vincent, Yann LeCun, and Yuandong Tian. Understanding dimensional collapse in contrastive selfsupervised learning. *arXiv preprint arXiv:2110.09348*, 2021.
- <span id="page-19-17"></span>Harry Joe. Estimation of entropy and other functionals of a multivariate density. *Annals of the Institute of Statistical Mathematics*, 41(4):683–697, 1989.
- <span id="page-19-10"></span>Thomas Kerdreux, Alexandre Tuel, Quentin Febvre, Alexis Mouche, and Bertrand Chapron. Efficient selfsupervised learning for earth observation via dynamic dataset curation. In *Proceedings of the Computer Vision and Pattern Recognition Conference*, pages 3017–3027, 2025.
- <span id="page-19-5"></span>Alexander Khazatsky, Karl Pertsch, Suraj Nair, Ashwin Balakrishna, Sudeep Dasari, Siddharth Karamcheti, Soroush Nasiriany, Mohan Kumar Srirama, Lawrence Yunliang Chen, Kirsty Ellis, et al. Droid: A large-scale in-the-wild robot manipulation dataset. *arXiv preprint arXiv:2403.12945*, 2024.
- <span id="page-20-3"></span>Diederik P Kingma, Danilo J Rezende, Shakir Mohamed, and Max Welling. Semi-supervised learning with deep generative models. *Advances in neural information processing systems*, 27, 2014.
- <span id="page-20-15"></span>A. N. Kolmogorov. Sulla determinazione empirica di una legge di distribuzione. *Giornale dell'Istituto Italiano degli Attuari*, 4:83–91, 1933.
- <span id="page-20-1"></span>Yann LeCun. A path towards autonomous machine intelligence version 0.9. 2, 2022-06-27. *Open Review*, 62(1):1–62, 2022.
- <span id="page-20-0"></span>Yann LeCun, Yoshua Bengio, and Geoffrey Hinton. Deep learning. *nature*, 521(7553):436–444, 2015.
- <span id="page-20-14"></span>Erich Leo Lehmann and Joseph P Romano. *Testing statistical hypotheses*. Springer, 2005.
- <span id="page-20-5"></span>Xiao Liu, Fanjin Zhang, Zhenyu Hou, Li Mian, Zhaoyu Wang, Jing Zhang, and Jie Tang. Self-supervised learning: Generative or contrastive. *IEEE transactions on knowledge and data engineering*, 35(1):857–876, 2021.
- <span id="page-20-6"></span>Zhuang Ma and Michael Collins. Noise contrastive estimation and negative sampling for conditional models: Consistency and statistical efficiency. *arXiv preprint arXiv:1809.01812*, 2018.
- <span id="page-20-16"></span>Tobias Maltenberger, Ivan Ilic, Ilin Tolovski, and Tilmann Rabl. Evaluating multi-gpu sorting with modern interconnects. In *Proceedings of the 2022 International Conference on Management of Data*, pages 1795–1809, 2022.
- <span id="page-20-23"></span>George Marsaglia. Choosing a point from the surface of a sphere. *The Annals of Mathematical Statistics*, 43(2): 645–646, 1972.
- <span id="page-20-18"></span>Charles Masson, Jee E Rim, and Homin K Lee. Ddsketch: A fast and fully-mergeable quantile sketch with relativeerror guarantees. *arXiv preprint arXiv:1908.10693*, 2019.
- <span id="page-20-9"></span>David McAllester and Karl Stratos. Formal limitations on the measurement of mutual information. In *International Conference on Artificial Intelligence and Statistics*, pages 875–884. PMLR, 2020.
- <span id="page-20-22"></span>H Mhaskar, F Narcowich, and J Ward. Spherical marcinkiewicz-zygmund inequalities and positive quadrature. *Mathematics of computation*, 70(235):1113– 1130, 2001.
- <span id="page-20-19"></span>Erik G Miller. A new class of entropy estimators for multi-dimensional densities. In *2003 IEEE International Conference on Acoustics, Speech, and Signal Processing, 2003. Proceedings.(ICASSP'03).*, volume 3, pages III–297. IEEE, 2003.
- <span id="page-20-25"></span>Frederick Mosteller. *On some useful "inefficient" statistics*. Springer, 2006.
- <span id="page-20-11"></span>Elizbar A Nadaraya. On estimating regression. *Theory of Probability & Its Applications*, 9(1):141–142, 1964.
- <span id="page-20-21"></span>Francis J Narcowich, Pencho Petrushev, and Joseph D Ward. Localized tight frames on spheres. *SIAM Journal on Mathematical Analysis*, 38(2):574–594, 2006.
- <span id="page-20-12"></span>Jerzy Neyman and Egon Sharpe Pearson. Ix. on the problem of the most efficient tests of statistical hypotheses. *Philosophical Transactions of the Royal Society of London. Series A, Containing Papers of a Mathematical or Physical Character*, 231(694-706):289–337, 1933.
- <span id="page-20-20"></span>Khai Nguyen and Nhat Ho. Energy-based sliced wasserstein distance. *Advances in Neural Information Processing Systems*, 36:18046–18075, 2023.
- <span id="page-20-7"></span>Aaron van den Oord, Yazhe Li, and Oriol Vinyals. Representation learning with contrastive predictive coding. *arXiv preprint arXiv:1807.03748*, 2018.
- <span id="page-20-10"></span>Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, et al. Dinov2: Learning robust visual features without supervision. *arXiv preprint arXiv:2304.07193*, 2023.
- <span id="page-20-4"></span>Vardan Papyan, XY Han, and David L Donoho. Prevalence of neural collapse during the terminal phase of deep learning training. *Proceedings of the National Academy of Sciences*, 117(40):24652–24663, 2020.
- <span id="page-20-17"></span>Felix Petersen, Christian Borgelt, Hilde Kuehne, and Oliver Deussen. Monotonic differentiable sorting networks. *arXiv preprint arXiv:2203.09630*, 2022.
- <span id="page-20-26"></span>RoL Plackett. Linear estimation from censored data. *The Annals of Mathematical Statistics*, 29(1):131–142, 1958.
- <span id="page-20-8"></span>Ben Poole, Sherjil Ozair, Aaron Van Den Oord, Alex Alemi, and George Tucker. On variational bounds of mutual information. In *International conference on machine learning*, pages 5171–5180. PMLR, 2019.
- <span id="page-20-24"></span>M Mahibbur Rahman and Z Govindarajulu. A modification of the test of shapiro and wilk for normality. *Journal of Applied Statistics*, 24(2):219–236, 1997.
- <span id="page-20-2"></span>Bryan Rodas, Natalie Montesino, Jakob Ambsdorf, David Klindt, and Randall Balestriero. Diet-cp: Lightweight and data efficient self supervised continued pretraining. *arXiv preprint arXiv:2509.06990*, 2025.
- <span id="page-20-13"></span>Samarendra Nath Roy. On a heuristic method of test construction and its use in multivariate analysis. *The Annals of Mathematical Statistics*, 24(2):220–238, 1953.
- <span id="page-21-6"></span>David E Rumelhart, Geoffrey E Hinton, and Ronald J Williams. Learning representations by back-propagating errors. *nature*, 323(6088):533–536, 1986.
- <span id="page-21-11"></span>Claude E Shannon. A mathematical theory of communication. *The Bell system technical journal*, 27(3):379–423, 1948.
- <span id="page-21-24"></span>Samuel S Shapiro and RS Francia. An approximate analysis of variance test for normality. *Journal of the American statistical Association*, 67(337):215–216, 1972.
- <span id="page-21-15"></span>Samuel Sanford Shapiro and Martin B Wilk. An analysis of variance test for normality (complete samples). *Biometrika*, 52(3-4):591–611, 1965.
- <span id="page-21-9"></span>Ravid Shwartz Ziv and Yann LeCun. To compress or not to compress—self-supervised learning and information theory: A review. *Entropy*, 26(3):252, 2024.
- <span id="page-21-10"></span>Ravid Shwartz-Ziv, Randall Balestriero, and Yann LeCun. What do we maximize in self-supervised learning? *arXiv preprint arXiv:2207.10081*, 2022.
- <span id="page-21-18"></span>Bernard W Silverman. *Density estimation for statistics and data analysis*. Routledge, 2018.
- <span id="page-21-21"></span>Oriane Siméoni, Huy V Vo, Maximilian Seitzer, Federico Baldassarre, Maxime Oquab, Cijo Jose, Vasil Khalidov, Marc Szafraniec, Seungeun Yi, Michaël Ramamonjisoa, et al. Dinov3. *arXiv preprint arXiv:2508.10104*, 2025.
- <span id="page-21-19"></span>Yang Song, Sahaj Garg, Jiaxin Shi, and Stefano Ermon. Sliced score matching: A scalable approach to density and score estimation. In *Uncertainty in artificial intelligence*, pages 574–584. PMLR, 2020.
- <span id="page-21-23"></span>Charles Spearman. The proof and measurement of association between two things. 1961.
- <span id="page-21-20"></span>Bharath K Sriperumbudur, Arthur Gretton, Kenji Fukumizu, Bernhard Schölkopf, and Gert RG Lanckriet. Hilbert space embeddings and metrics on probability measures. *The Journal of Machine Learning Research*, 11: 1517–1561, 2010.
- <span id="page-21-13"></span>Shiliang Sun and Rongqing Huang. An adaptive k-nearest neighbor algorithm. In *2010 seventh international conference on fuzzy systems and knowledge discovery*, volume 1, pages 91–94. IEEE, 2010.
- <span id="page-21-2"></span>Richard S Sutton. Dyna, an integrated architecture for learning, planning, and reacting. *ACM Sigart Bulletin*, 2 (4):160–163, 1991.
- <span id="page-21-17"></span>Gábor J Székely and Maria L Rizzo. A new test for multivariate normality. *Journal of Multivariate Analysis*, 93(1): 58–80, 2005.
- <span id="page-21-16"></span>Ivan Tanasic, Lluís Vilanova, Marc Jordà, Javier Cabezas, Isaac Gelado, Nacho Navarro, and Wen-mei Hwu. Comparison based sorting for systems with multiple gpus. In *Proceedings of the 6th Workshop on General Purpose Processor Using Graphics Processing Units*, pages 1–11, 2013.
- <span id="page-21-12"></span>Kashvi Taunk, Sanjukta De, Srishti Verma, and Aleena Swetapadma. A brief review of nearest neighbor algorithm for learning and classification. In *2019 international conference on intelligent computing and control systems (ICCS)*, pages 1255–1260. IEEE, 2019.
- <span id="page-21-22"></span>Vimal Thilak, Chen Huang, Omid Saremi, Laurent Dinh, Hanlin Goh, Preetum Nakkiran, Joshua M Susskind, and Etai Littwin. Lidar: Sensing linear probing performance in joint embedding ssl architectures. *arXiv preprint arXiv:2312.04000*, 2023.
- <span id="page-21-3"></span>Yonglong Tian, Chen Sun, Ben Poole, Dilip Krishnan, Cordelia Schmid, and Phillip Isola. What makes for good views for contrastive learning? *Advances in neural information processing systems*, 33:6827–6839, 2020.
- <span id="page-21-4"></span>Yuandong Tian, Xinlei Chen, and Surya Ganguli. Understanding self-supervised learning dynamics without contrastive pairs. In *International Conference on Machine Learning*, pages 10268–10278. PMLR, 2021.
- <span id="page-21-1"></span>Edward C Tolman. Cognitive maps in rats and men. *Psychological review*, 55(4):189, 1948.
- <span id="page-21-8"></span>Hugues Van Assel, Mark Ibrahim, Tommaso Biancalani, Aviv Regev, and Randall Balestriero. Joint embedding vs reconstruction: Provable benefits of latent space prediction for self supervised learning. *arXiv preprint arXiv:2505.12477*, 2025.
- <span id="page-21-7"></span>Pascal Vincent, Hugo Larochelle, Isabelle Lajoie, Yoshua Bengio, Pierre-Antoine Manzagol, and Léon Bottou. Stacked denoising autoencoders: Learning useful representations in a deep network with a local denoising criterion. *Journal of machine learning research*, 11(12), 2010.
- <span id="page-21-5"></span>Huy V Vo, Vasil Khalidov, Timothée Darcet, Théo Moutakanni, Nikita Smetanin, Marc Szafraniec, Hugo Touvron, Camille Couprie, Maxime Oquab, Armand Joulin, et al. Automatic data curation for self-supervised learning: A clustering-based approach. *arXiv preprint arXiv:2405.15613*, 2024.
- <span id="page-21-0"></span>Hermann Von Helmholtz. *Handbuch der physiologischen Optik*, volume 9. L. Voss, 1867.
- <span id="page-21-14"></span>Richard Von Mises. *Probability, statistics, and truth*. Courier Corporation, 1981.
- <span id="page-22-0"></span>Xiao Wang, Haoqi Fan, Yuandong Tian, Daisuke Kihara, and Xinlei Chen. On the importance of asymmetry for siamese representation learning. In *Proceedings of the IEEE/CVF conference on computer vision and pattern recognition*, pages 16570–16579, 2022.
- <span id="page-22-3"></span>Geoffrey S Watson. Smooth regression analysis. *Sankhya:¯ The Indian Journal of Statistics, Series A*, pages 359–372, 1964.
- <span id="page-22-4"></span>George S Watson. Goodness-of-fit tests on a circle. *Biometrika*, 48(1/2):109–114, 1961.
- <span id="page-22-5"></span>S Weisburg and C Binham. An approximate analysis of variance test for non-normality suitable for machine computation. *Technometrics*, 17:133–134, 1975.
- <span id="page-22-2"></span>Shichao Zhang, Xuelong Li, Ming Zong, Xiaofeng Zhu, and Ruili Wang. Efficient knn classification with different numbers of nearest neighbors. *IEEE transactions on neural networks and learning systems*, 29(5):1774–1785, 2017.
- <span id="page-22-1"></span>Yifan Zhang, Zhiquan Tan, Jingqin Yang, Weiran Huang, and Yang Yuan. Matrix information theory for selfsupervised learning. *arXiv preprint arXiv:2305.17326*, 2023.

# **LeJEPA**

# **Appendix**

## <span id="page-23-0"></span>**A Additional Details on Nonlinear Probing**

## **A.1 kNN Probing**

To allow for more flexible evaluation of the pretrained encoder , it is standard to work with a -NN prober [\[Taunk et al.,](#page-21-12) [2019\]](#page-21-12), both for regression and classification. We rely on the radial -NN variation that leverages a sample-dependent –improving performance for non uniform distributions of samples [\[Sun and Huang, 2010,](#page-21-13) [Zhang et al., 2017,](#page-22-2) [Abu Alfeilat](#page-17-5) [et al., 2019\]](#page-17-5).

We denote the underlying embedding density as <sup>∈</sup> <sup>3</sup> with derivatives of order up to 3 bounded, and finite Fisher information and covariance. This regularity condition is fulfilled by current encoders. The *unknown* labels come from the target function : R <sup>→</sup> <sup>R</sup>, assumed 2 . We handle classification tasks by setting () <sup>=</sup> <sup>P</sup>( <sup>=</sup> <sup>1</sup> <sup>|</sup> ). The training consists of the embeddings along with their training labels {( , ())} =1 , where we will denote <sup>≜</sup> (). The prediction for a query vector is formed as

$$
\widehat{y}(q) := \frac{1}{y(q)} \sum_{n:||z_n - q|| \le r_0} y_n,
$$
 (kNN)

with () <sup>≜</sup> #{ : <sup>−</sup> <sup>≤</sup> 0} counting the number of samples within a -radius ball around . The radius controls how many neighbors predictions are averaged to form the query's prediction. As per the linear probing's lemma. [1,](#page-4-4) we can characterize the bias of the estimator Equation [\(kNN\)](#page-23-1) at a particular query point, as formalized below.

<span id="page-23-2"></span>**Lemma 4: k-NN Pointwise Bias**

The [\(kNN\)](#page-23-1) estimator has bias at query given by

$$
\operatorname{Bias}(\boldsymbol{q}) = \frac{r_0^2}{d+2} \left( \nabla \eta(\boldsymbol{q})^\top \nabla \log p_z(\boldsymbol{q}) + \frac{1}{2} \Delta \eta(z) \right)
$$

where the remainder ( 2 0 ) is uniform in . (Proof in Section [B.3.](#page-26-0))

To obtain the integrated bias, i.e., over the distribution of query points, we consider the following two properties. First, the distribution of query points follow the training distribution, i.e., <sup>∼</sup> , second, target function has gradient which is mean-zero and isotropic with E -∇()∇() ⊤ = 2 with 2 ∈ (0, ∞) uniformly in . We also have any finite scalar-constraint on the covariance of the embeddings such as Tr(Σ) <sup>=</sup> or <sup>∥</sup>Σ∥ <sup>=</sup> for a finite constant .

<span id="page-23-1"></span><sup>+</sup> ( 2 0 ),

### **LeJEPA:**

#### <span id="page-24-1"></span>**Theorem 7: k-NN isotropic Gaussian Optimality**

The integrated squared bias of [\(kNN\)](#page-23-1) satisfies

$$
\mathbb{E}_{z} [\text{Bias}(z)^{2}] = \frac{r_{0}^{4}}{(K+2)^{2}} \tau_{g}^{2} J(p) + O(r_{0}^{4}),
$$

and the isotropic Gaussian is the unique minimizer of the integrated square bias. (Proof in Section [B.4.](#page-27-0))

As a result, we now have a unique minimizer for the optimal embedding density for both the linear and k-NN probes.

### **A.2 Kernel Probing**

As an alternative to [\(kNN\)](#page-23-1), it is also common to leverage kernel methods, which we consider in this section.

Consider a kernel : <sup>R</sup> → R with the following standard properties

$$
\int_{\mathbb{R}^d} K(u) du = 1,
$$
\n(normalized)

$$
\int_{\mathbb{R}^d} u K(u) du = 0,
$$
 (symmetric)

$$
\int_{\mathbb{R}^d} u u^\top K(u) du = \mu_2(K) I_d,
$$
 (isotropic)

$$
R(K) \triangleq \int_{\mathbb{R}^d} K(u)^2 du < \infty,\tag{finite roughness}
$$

for some 2() ∈ (0, ∞), some bandwidth <sup>ℎ</sup> <sup>&</sup>gt; <sup>0</sup> and denoting ℎ() <sup>≜</sup> <sup>ℎ</sup> <sup>−</sup>(/ℎ), we remind the reader that the Nadaraya-Watson estimator, introduced in [Nadaraya](#page-20-11) [\[1964\]](#page-20-11), [Watson](#page-22-3) [\[1964\]](#page-22-3), at a query ∈ R is

<span id="page-24-0"></span>
$$
\widehat{y}(q) \triangleq \frac{\sum_{n=1}^{N} K_n (q - x_n) y_n}{\sum_{n=1}^{N} K_n (q - x_n)}.
$$
\n(NW)

Similarly to [\(kNN\)](#page-23-1), we will see that the performance of [\(NW\)](#page-24-0) depends crucially on the distribution of the training points. We have access to our dataset of inputs from and for each sample the corresponding target is given from () <sup>=</sup> <sup>E</sup>[ <sup>|</sup> ]. We also denote the corresponding conditional variance of the target function at that point as () <sup>=</sup> Var( <sup>|</sup> <sup>=</sup> ). We follow the regularity conditions of the k-NN probing derivations and additionally assume that has sufficiently light tails so that for each coordinate , lim∥∥→∞ () <sup>=</sup> <sup>0</sup> and lim∥∥→∞ () <sup>=</sup> 0. We first derive the pointwise bias and variance for <sup>b</sup>().

#### <span id="page-24-2"></span>**Lemma 5: Kernel Bias and Variance**

For any fixed ∈ R with () <sup>&</sup>gt; 0, as ℎ <sup>→</sup> <sup>0</sup> and ℎ → ∞,

Bias
$$
[\widehat{y}(q)] = \frac{h^2 \mu_2(K)}{2} \left( \Delta y(q) + 2 \nabla y(q)^\top \nabla \log p(q) \right) + o(h^2),
$$
  
Var $[\widehat{y}(q)] = \frac{R(K)}{nh^d} \frac{v(q)}{p(q)} + o((nh^d)^{-1}).$ 

The (·) terms are uniform over compact sets where is bounded away from zero. (Proof in Section [B.5.](#page-31-0))

We now show that, under a fixed mean and total-covariance constraint on , the isotropic Gaussian distribution uniquely minimizes the bias and variance of the kernel regression estimator at any test point. We restrict the smoothness class of the target function using

$$
\mathcal{M}(L,B) \triangleq \left\{ m \in C^2(\mathbb{R}^d) : ||\nabla y(q)|| \le L \right\}
$$

<sup>|</sup>Δ()| ≤ , <sup>∀</sup> <sup>∈</sup> <sup>R</sup> o ,

### **LeJEPA:**

allowing us to formalize below the worst case integrated bias and the optimal density for .

<span id="page-25-2"></span>

| Theorem 8: Kernel isotropic Gaussian Optimality    |   |                                                  |   |                                 |   |                            |
|----------------------------------------------------|---|--------------------------------------------------|---|---------------------------------|---|----------------------------|
| The integrated squared bias of (NW) satisfies      |   |                                                  |   |                                 |   |                            |
| E<br>b𝒚(𝒛)<br><br>Bias<br><br>sup<br>𝑧<br>𝑚∈ℳ(𝐿,𝐵) | ≤ | 2𝜇2(<br>)<br>2<br><br><br>2<br>ℎ<br>𝐾<br>2𝐵<br>2 | + | <br>2<br>(<br>)<br>8𝐿<br>𝐽<br>𝑝 | + | (<br>4<br>)<br>𝑜<br>ℎ<br>, |
|                                                    |   |                                                  |   |                                 |   |                            |

and the integrated variance is independent of . Among all densities on <sup>R</sup> with total-variance constrained, e.g., Tr(Σ) <sup>=</sup> , the isotropic Gaussian is the unique minimizer. (Proof in Section [B.7.](#page-33-0))

## **B Proofs**

### <span id="page-25-0"></span>**B.1 Proof of lemma. [1](#page-4-4)**

*Proof.* Our proof follows standard derivations when it comes to studying the bias of an estimator. Let's consider the ridge regression problem (Tikhonov regularized least squares estimator) with close form estimator

$$
\hat{\beta} = (\mathbf{X}^T \mathbf{X} + \lambda_{\text{wd}} \mathbf{I})^{-1} \mathbf{X}^T \mathbf{Y}.
$$
\n(9)

The labels are formed from the ground truth parameter true with centered error, as per **Y** = **X**true + where E[] = **0**. We can now look at the bias of our estimator given by

Bias(
$$
\hat{\beta}
$$
) =  $\mathbb{E}[\hat{\beta}] - \beta_{true}$   
\n=  $(\mathbf{X}^T \mathbf{X} + \lambda_{wd} \mathbf{I})^{-1} \mathbf{X}^T \mathbf{X} \beta_{true} - \beta_{true}$   
\n=  $-\lambda_{wd} (\mathbf{X}^T \mathbf{X} + \lambda_{wd} \mathbf{I})^{-1} \beta_{true}$   
\n=  $-\lambda_{wd} \mathbf{Q} (\mathbf{\Lambda} + \lambda \mathbf{I})^{-1} \mathbf{Q}^T \beta_{true}$ 

We will now compare that bias when has isotropic and anisotropic covariance with same total variance:

$$
\frac{\lambda_1 + \lambda_2 + \dots + \lambda_p}{p} = \bar{\lambda}.\tag{10}
$$

For any anisotropic covariance matrix of , denote by <sup>1</sup> the eigenvector with smallest eigenvalue, and let's denote by > 0 a positive constant. We now define

$$
\beta_{\text{true}} = \kappa \cdot \mathbf{q}_p,\tag{11}
$$

leading to

$$
||\text{Bias}(\hat{\beta})||_{\text{isotropic}} = \frac{\lambda_{\text{wd}}}{\bar{\lambda} + \lambda_{\text{wd}}} ||\beta_{\text{true}}||,
$$

$$
||\text{Bias}(\hat{\beta})||_{\text{non-isotropic}} = \frac{\lambda_{\text{wd}}}{\lambda_p + \lambda_{\text{wd}}} ||\beta_{\text{true}}||
$$

Since <sup>&</sup>lt; ¯ (strict inequality when not isotropic):

$$
\frac{\lambda_{\text{wd}}}{\lambda_p + \lambda_{\text{wd}}} > \frac{\lambda_{\text{wd}}}{\bar{\lambda} + \lambda_{\text{wd}}}
$$

we obtain that

$$
\|\text{Bias}(\hat{\beta})\|_{\text{non-isotropic}} > \|\text{Bias}(\hat{\beta})\|_{\text{isotropic}}
$$

<span id="page-25-1"></span>As a result, whenever the covariance matrix of is anisotropic, there will be downstream tasks for which the estimator bias is increased compared to having isotropic covariance matrix. Anisotropic covariance structure thus amplifies regularization bias when the true parameter vector aligns unfavorably with the data's covariance structure. □

### **B.2 Proof of lemma. [2](#page-4-5)**

*Proof.* We use the same formula as in Section [B.1](#page-25-0) with wd = 0. We first see that the estimator is unbiased. We will now leverage that result to compute the covariance matrix of the estimator

$$
\begin{aligned}\n\text{Var}(\hat{\beta}|\mathbf{X}) &= \mathbb{E}[(\hat{\beta} - \beta)(\hat{\beta} - \beta)^{T}|\mathbf{X}] \\
&= \mathbb{E}[(\mathbf{X}^{T}\mathbf{X})^{-1}\mathbf{X}^{T}\varepsilon\varepsilon^{T}\mathbf{X}(\mathbf{X}^{T}\mathbf{X})^{-1}|\mathbf{X}] \\
&= (\mathbf{X}^{T}\mathbf{X})^{-1}\mathbf{X}^{T}\mathbb{E}[\varepsilon\varepsilon^{T}|\mathbf{X}]\mathbf{X}(\mathbf{X}^{T}\mathbf{X})^{-1} \\
&= (\mathbf{X}^{T}\mathbf{X})^{-1}\mathbf{X}^{T}(\sigma^{2}\mathbf{I}_{n})\mathbf{X}(\mathbf{X}^{T}\mathbf{X})^{-1} \\
&= \sigma^{2}(\mathbf{X}^{T}\mathbf{X})^{-1}\n\end{aligned}
$$

leading to the total variance

$$
\operatorname{tr}(\operatorname{Var}(\hat{\boldsymbol{\beta}})) = \sigma^2 \operatorname{tr}(\mathbf{G}^{-1}) = \sigma^2 \sum_{j=1}^p \frac{1}{\lambda_j}
$$

where we used the eigendecomposition:

$$
\mathbf{G} = \mathbf{Q} \Lambda \mathbf{Q}^T
$$

The function () <sup>=</sup> 1 is strictly convex on (0, ∞) allowing us to leverage Jensen's Inequality:

$$
\frac{1}{K} \sum_{k=1}^{K} \frac{1}{\lambda_k} > \frac{1}{\frac{1}{K} \sum_{j=1}^{K} \lambda_k}
$$
\n
$$
\iff \frac{1}{K} \sum_{k=1}^{K} \frac{1}{\lambda_k} > \frac{1}{K} \sum_{k=1}^{K} \frac{1}{\frac{1}{K} \sum_{j=1}^{K} \lambda_k}
$$
\n
$$
\iff \sum_{k=1}^{K} \frac{1}{\lambda_k} > \sum_{k=1}^{K} \frac{1}{\frac{1}{K} \sum_{j=1}^{K} \lambda_k}
$$
\n
$$
\iff \text{tr}(\text{Var}(\hat{\beta}))_{\text{aniso}} > \text{tr}(\text{Var}(\hat{\beta}))_{\text{iso}}
$$

The inequality is strict whenever the eigenvalues {} =1 are not all equal. □

## <span id="page-26-0"></span>**B.3 Proof of lemma. [4](#page-23-2)**

*Proof.* Under PPP, conditional expectations of <sup>b</sup>() coincide with the normalized ball average

$$
\mathbb{E}\big[\widehat{\eta}(x)\big] = \frac{\int_{B(0,r_0)} \eta(x+z) p(x+z) dz}{\int_{B(0,r_0)} p(x+z) dz}
$$
 to second order in  $r_0$ ,

which is the key surrogate used below. **Ball integrals.** For computations we use (by symmetry) for any <sup>&</sup>gt; 0:

$$
\int_{\mathrm{B}(0,r)}zdz=0,\qquad \int_{\mathrm{B}(0,r)}zz^{\top}dz=\frac{\mathrm{Vol}^{d+2}}{d+2}I_{d},\qquad \int_{\mathrm{B}(0,r)}\left\|z\right\|^{2}dz=\frac{d\mathrm{Vol}^{d+2}}{d+2}.
$$

Fix <sup>∈</sup> <sup>R</sup> and write <sup>∈</sup> <sup>B</sup>(0, 0) for local displacements. Assume <sup>∈</sup> 3 , <sup>∈</sup> <sup>2</sup> with bounded derivatives on the region of interest, and expand a second-order Taylor expansion:

$$
p(x + z) = p(x) + \nabla p(x)^{\top} z + \frac{1}{2} z^{\top} H p(x) z + O(||z||^3),
$$
  
\n
$$
\eta(x + z) = \eta(x) + \nabla \eta(x)^{\top} z + \frac{1}{2} z^{\top} H \eta(x) z + O(||z||^3),
$$

with remainders satisfying <sup>|</sup>(; )| ≤ <sup>∥</sup><sup>∥</sup> 3 and <sup>|</sup>(; )| ≤ <sup>∥</sup><sup>∥</sup> 3 uniformly for <sup>∥</sup><sup>∥</sup> <sup>≤</sup> 0. Using the ball identities

∫ (0,) <sup>=</sup> <sup>0</sup> and <sup>∫</sup> (0,) ⊤ <sup>=</sup> +2 +2 and collecting terms up to order +2 0 , we simplify the denominator as

$$
\mathcal{D}(x) \triangleq \int_{B(0,r_0)} p(x+z)dz
$$
  
= 
$$
\int_{B(0,r_0)} \left[ p(x) + \nabla p(x)^\top z + \frac{1}{2} z^\top H p(x) z + R_p(x; z) \right] dz
$$
  
= 
$$
\text{Vol}_0^d p(x) + \frac{\text{Vol}_0^{d+2}}{2(d+2)} \text{tr}(H p(x)) + O(r_0^{d+3}),
$$

since ∫ <sup>=</sup> <sup>0</sup> and <sup>∫</sup> ⊤ <sup>=</sup> tr() +2 0 +2 and the denominator as

$$
\begin{split} \mathcal{N}(x) & \triangleq \int_{B(0,r_0)} \eta(x+z) p(x+z) dz \\ & = \int \left[ \eta(x) + \nabla \eta(x)^\top z + \frac{1}{2} z^\top H \eta(x) z \right] \left[ p(x) + \nabla p(x)^\top z + \frac{1}{2} z^\top H p(x) z \right] dz + O(r_0^{d+3}) \\ & = \eta(x) p(x) v_d r_0^d + \eta(x) \frac{v_d r_0^{d+2}}{2(d+2)} \text{tr}(H p(x)) + \frac{v_d r_0^{d+2}}{d+2} \nabla \eta(x) \cdot \nabla p(x) + \frac{v_d r_0^{d+2}}{2(d+2)} p(x) \text{tr}(H \eta(x)) + O(r_0^{d+3}). \end{split}
$$

Cubic terms vanish by symmetry, and quartic terms are ( +4 0 ). Subtract ()() to obtain the bias numerator:

$$
\mathcal{N}(x) - \eta(x)\mathcal{D}(x) = \frac{v_d r_0^{d+2}}{d+2} \Big( \nabla \eta(x) \cdot \nabla p(x) + \frac{1}{2} p(x) \Delta \eta(x) \Big) + O(r_0^{d+3}).
$$

Write () <sup>=</sup> 0 () <sup>1</sup> <sup>+</sup> () 2 0 <sup>+</sup> ( 3 0 ) where () :<sup>=</sup> 1 <sup>2</sup>(+2)() tr(()). Then

$$
\frac{N(x)}{\mathcal{D}(x)} - \eta(x) = \frac{\frac{v_{d}r_{0}^{d+2}}{d+2} \left( \nabla \eta \cdot \nabla p + \frac{1}{2} p \Delta \eta \right) + O(r_{0}^{d+3})}{v_{d}r_{0}^{d}p \left( 1 + \alpha r_{0}^{2} + O(r_{0}^{3}) \right)}
$$
\n
$$
= \frac{r_{0}^{2}}{d+2} \left( \frac{\nabla \eta \cdot \nabla p}{p} + \frac{1}{2} \Delta \eta \right) \left( 1 - \alpha r_{0}^{2} + O(r_{0}^{3}) \right) + O(r_{0}^{3})
$$
\n
$$
= \frac{r_{0}^{2}}{d+2} \left( \nabla \eta(x) \cdot \nabla \log p(x) + \frac{1}{2} \Delta \eta(x) \right) + o(r_{0}^{2}),
$$

uniformly on . This gives the bias formula

$$
\mathbb{E}\big[\widehat{\eta}(x)\big] - \eta(x) = \frac{r_0^2}{d+2} \Big(\nabla \eta(x) \cdot \nabla \log p(x) + \frac{1}{2} \Delta \eta(x)\Big) + o(r_0^2),
$$

completing the proof. □

## <span id="page-27-0"></span>**B.4 Proof of thm. [7](#page-24-1)**

*Proof.* Recall from Section [B.3](#page-26-0) that the bias term as sample is given by

Bias(x) = 
$$
\frac{r_0^2}{d+2} \Big( \nabla \eta(x) \cdot \nabla \log p(x) \Big) + \frac{r_0^2}{2(d+2)} \Delta \eta(x) + o(r_0^2)
$$
  
=  $\frac{r_0^2}{d+2} \Big( A(x) + C(x) \Big) + o(r_0^2),$ 

where we defined () <sup>≜</sup> <sup>∇</sup>() · ∇log () and () <sup>≜</sup> 1 2 <sup>Δ</sup>(). We now square and take expectation of <sup>∼</sup> and the isotropic gradient prior

$$
\mathbb{E}\left[\text{Bias}(X)^2\right] = \mathbb{E}\left[\left(\frac{r_0^2}{d+2}\right)^2 \left(A(x)^2 + 2A(x)C(x) + C(x)^2\right) + o(r_0^4)\right]
$$
\n(12)

$$
= \left(\frac{r_0^2}{d+2}\right)^2 \left\{ \underbrace{\mathbb{E}\left[A(X)^2\right]}_{\text{score-gradient term}} + \underbrace{2\mathbb{E}\left[A(X)C(X)\right]}_{\text{cross term}} + \underbrace{\mathbb{E}\left[C(X)^2\right]}_{\text{curvature term}} \right\} + o(r_0^4). \tag{13}
$$

We will derive each term separately, recalling that we assume an isotropic gradient prior for , i.e., E -<sup>∇</sup>() = 0 and E -<sup>∇</sup>()∇() ⊤ = 2 , for some 2 ∈ (0, ∞).

**1) The score-gradient term** <sup>E</sup>[() 2 ]**.** Using () :<sup>=</sup> <sup>∇</sup>log () for brevity:

<span id="page-28-0"></span>
$$
\mathbb{E}\left[A(X)^2\right] = \mathbb{E}_X\left[\mathbb{E}_\eta[A(X)^2]\right]
$$
  
\n
$$
= \mathbb{E}_X\left[\mathbb{E}_\eta[(\nabla \eta(x)^\top v(x))^2]\right]
$$
  
\n
$$
= \mathbb{E}_X\left[\mathbb{E}_\eta[\nabla \eta(x)^\top (v(x)v(x)^\top)\nabla \eta(x)]\right]
$$
  
\n
$$
= \mathbb{E}_X\left[\mathbb{E}_\eta[\text{tr}\left(v(x)v(x)^\top \nabla \eta(x) \nabla \eta(x)^\top\right)\right]\right]
$$
  
\n
$$
= \mathbb{E}_X\left[\text{tr}\left(v(x)v(x)^\top \mathbb{E}_\eta[\nabla \eta(x) \nabla \eta(x)^\top]\right)\right]
$$
  
\n
$$
= \mathbb{E}_X\left[\tau_g^2 ||v(x)||^2\right]
$$
  
\n
$$
= \tau_g^2 \mathbb{E}_X\left[||v(X)||^2\right]
$$
  
\n
$$
= \tau_g^2 \int_{\mathbb{R}^d} ||\nabla \log p(x)||^2 p(x) dx
$$

recovering the Fisher-information functional (), scaled by 2 

**2) The cross term** <sup>2</sup>E[()()]**.** We have

$$
A(x)C(x) = \frac{1}{2} (\nabla \eta(x)^\top v(x)) \Delta \eta(x).
$$

Under the prior, ∇ is mean-zero and isotropic; if, additionally, Δ is uncorrelated with ∇ and has zero mean (or is bounded and mean-zero after centering), then <sup>E</sup>[()()] <sup>=</sup> 0. If one does *not* assume the orthogonality/vanishing covariance above, then <sup>E</sup>[()()] is a finite constant (depending on the joint law of derivatives of ), and the cross term contributes

$$
\left(\frac{r_0^2}{d+2}\right)^2 \cdot 2\mathbb{E}[A(X)C(X)] = O(r_0^4),
$$

not ( 4 0 ). In that general case, the leading -dependent term of <sup>E</sup>[Bias() 2 ] is still the *score-gradient* 2 ().

**3) The curvature term** <sup>E</sup>[() 2 ]**.**

$$
\mathbb{E}\left[C(X)^2\right] = \mathbb{E}_X\left[\mathbb{E}_\eta[C(X)^2]\right]
$$

$$
= \frac{1}{4}\mathbb{E}_X\left[\mathbb{E}_\eta[(\Delta\eta(X))^2]\right]
$$

which is independent of , hence <sup>E</sup> -() 2 <sup>=</sup> (1) **Putting it together.** Substituting into [\(13\)](#page-28-0):

$$
\mathbb{E}\left[\text{Bias}(X)^2\right] = \left(\frac{r_0^2}{d+2}\right)^2 \left\{\tau_g^2 J(p) + O(1)\right\} + o(r_0^4)
$$

$$
= \frac{r_0^4}{(d+2)^2} \tau_g^2 J(p) + O(r_0^4),
$$

We show that, among all mean-zero distributions on <sup>R</sup> with a given *scalar* constraint on the covariance (trace, determinant, Frobenius norm, or spectral radius), the density that minimizes the Fisher-information functional

$$
J(p) \ := \ \int_{\mathbb{R}^d} \| \nabla \log p(x) \|^2 p(x) dx
$$

is the Gaussian with *isotropic* covariance satisfying the same scalar constraint. We proceed in two steps: (i) for fixed covariance matrix <sup>Σ</sup> <sup>≻</sup> 0, () is minimized by the Gaussian (0, <sup>Σ</sup>) and attains the value tr(<sup>Σ</sup> −1 ); (ii) for each scalar constraint, tr(Σ −1 ) is minimized by Σ = for the appropriate scalar <sup>&</sup>gt; 0.

### <span id="page-29-0"></span>**Lemma 6: Special case: Recovery of VCReg**

Let be a mean-zero probability density on <sup>R</sup> with covariance Σ = <sup>E</sup>[⊤] ≻ 0. Then

$$
J(p) \geq tr(\Sigma^{-1}),
$$

with equality if and only if <sup>=</sup> (0, <sup>Σ</sup>).

*Proof.* Consider the location family () :<sup>=</sup> ( <sup>−</sup> ), <sup>∈</sup> <sup>R</sup> . Its Fisher-information matrix at is

$$
I(\theta) = \mathbb{E} \big[ \nabla_{\theta} \log p_{\theta}(X) \nabla_{\theta} \log p_{\theta}(X)^{\top} \big] = \mathbb{E} \big[ \nabla \log p(X) \nabla \log p(X)^{\top} \big],
$$

so that () <sup>=</sup> trℐ (). The estimator () ≡ is unbiased for under , with Cov() = Σ. The matrix Cramér–Rao bound gives Cov() ⪰ ℐ () −1 , i.e., ℐ () ⪰ Σ −1 . Taking traces yields () ≥ tr(<sup>Σ</sup> −1 ). Equality in the matrix Cramér–Rao bound holds if and only if the score is an *affine* function of <sup>−</sup> , i.e., <sup>∇</sup>log () <sup>=</sup> ( <sup>−</sup> ) a.s. for some matrix ; integrating this identity shows is Gaussian with precision matrix <sup>−</sup>, hence <sup>=</sup> (0, <sup>Σ</sup>). □

### **Step 2: Optimizing over covariance shapes under scalar constraints**

Write the eigenvalues of <sup>Σ</sup> as 1, . . . , <sup>&</sup>gt; 0. Then

$$
\operatorname{tr}(\Sigma^{-1}) = \sum_{i=1}^d \frac{1}{\lambda_i}.
$$

We now solve min Í <sup>1</sup>/ under each scalar constraint; in every case the minimum is attained when all are equal, i.e., Σ = .

**(a) Trace constraint.** Given tr(Σ) = Í <sup>=</sup> <sup>&</sup>gt; 0, by Cauchy–Schwarz,

$$
\left(\sum_{i=1}^d \frac{1}{\lambda_i}\right)\left(\sum_{i=1}^d \lambda_i\right) \ge \left(\sum_{i=1}^d 1\right)^2 = d^2,
$$

with equality if and only if <sup>1</sup> <sup>=</sup> · · · <sup>=</sup> . Hence

$$
\min_{\Sigma>0:\text{ tr}(\Sigma)=t}\text{ tr}(\Sigma^{-1})\ =\ \frac{d^2}{t},\quad \text{ attained at}\quad \Sigma=\frac{t}{d}I_d.
$$

**(b) Determinant constraint.** Given det(Σ) = Î <sup>=</sup> > 0, set :<sup>=</sup> <sup>1</sup>/ so that <sup>Î</sup> <sup>=</sup> −1 . By the AM–GM inequality,

$$
\frac{1}{d} \sum_{i=1}^{d} \mu_i \ge \left( \prod_{i=1}^{d} \mu_i \right)^{1/d} = \delta^{-1/d},
$$

with equality iff <sup>1</sup> <sup>=</sup> · · · <sup>=</sup> , i.e., <sup>1</sup> <sup>=</sup> · · · <sup>=</sup> . Thus

$$
\min_{\Sigma>0:\ \det(\Sigma)=\delta} \ \text{tr}(\Sigma^{-1}) \ = \ d\delta^{-1/d}, \quad \text{attained at} \quad \Sigma = \delta^{1/d}I_d.
$$

**(c) Frobenius-norm constraint.** Given ∥Σ∥ 2 = Í 2 = <sup>2</sup> <sup>&</sup>gt; 0, minimize () :<sup>=</sup> Í <sup>1</sup>/ over <sup>&</sup>gt; <sup>0</sup> subject to () :<sup>=</sup> Í 2 = 2 . The Lagrangian

$$
\mathcal{L}(\lambda, \nu) = \sum_{i=1}^{d} \frac{1}{\lambda_i} + \nu \left( \sum_{i=1}^{d} \lambda_i^2 - c^2 \right)
$$

has first-order conditions − −2 <sup>+</sup> <sup>2</sup> <sup>=</sup> <sup>0</sup> for all , i.e., 3 = 1 2 , so all are equal. Imposing <sup>Í</sup> 2 = <sup>2</sup> yields <sup>=</sup> / √ , hence

$$
\min_{\Sigma>0:\; \|\Sigma\|_F=c} \; \text{tr}(\Sigma^{-1}) \; = \; \sum_{i=1}^d \frac{1}{\lambda_i} \; = \; \frac{d^{3/2}}{c}, \quad \text{attained at} \quad \Sigma=\frac{c}{\sqrt{d}}I_d.
$$

**(d) Spectral-radius constraint.** Let the spectral radius be constrained by (Σ) <sup>=</sup> max <sup>≤</sup> for some <sup>&</sup>gt; 0. Since ↦→ <sup>1</sup>/ is strictly decreasing on (0, ∞),

$$
\sum_{i=1}^d \frac{1}{\lambda_i} \geq \sum_{i=1}^d \frac{1}{r} = \frac{d}{r},
$$

with equality if and only if <sup>=</sup> for all . Therefore

$$
\min_{\Sigma>0:\ \rho(\Sigma)\leq r} \ \text{tr}(\Sigma^{-1}) \ = \ \frac{d}{r}, \quad \text{attained at} \quad \Sigma = rI_d.
$$

(The same conclusion holds if the constraint is (Σ) <sup>=</sup> , since one may take all eigenvalues equal to .)

### **Conclusion: Isotropic Gaussian is optimal**

Combining Lemma [6](#page-29-0) with the solutions (a)–(d), we obtain:

#### **LeJEPA:**

### **Theorem 9: Special case: Recovery of VCReg**

Fix one of the following scalar covariance constraints for a mean-zero distribution on <sup>R</sup> :

- trace: tr(Cov()) <sup>=</sup> ,
- determinant: det(Cov()) <sup>=</sup> ,
- Frobenius norm: <sup>∥</sup>Cov()∥ <sup>=</sup> ,
- spectral radius upper bound: (Cov()) ≤ .

Then the Fisher-information functional () is minimized over all such by the isotropic Gaussian <sup>=</sup> (0, ) with chosen to satisfy the constraint. The minimal values are:

> trace : min <sup>=</sup> 2 , <sup>=</sup> , determinant : min <sup>=</sup> <sup>−</sup>1/ , <sup>=</sup> 1/ Frobenius : min <sup>=</sup> 3/2 , <sup>=</sup> √ , spectral radius : min <sup>=</sup> , <sup>=</sup> .

,

In each case, is the unique minimizer (up to null sets).

*Proof.* For any admissible with covariance <sup>Σ</sup>, Lemma [6](#page-29-0) gives () ≥ tr(<sup>Σ</sup> −1 ). Minimizing the right-hand side under the stated scalar constraint yields Σ = by the calculations in (a)–(d). Equality in Lemma [6](#page-29-0) holds if and only if is Gaussian with that covariance, hence uniquely attains the bound. □

## □

### <span id="page-31-0"></span>**B.5 Proof of lemma. [5](#page-24-2)**

*Proof.* Write the numerator and denominator of b() as

$$
B_n(x) := \sum_{i=1}^n K_h(x - X_i)Y_i, \qquad A_n(x) := \sum_{i=1}^n K_h(x - X_i),
$$

so that b() <sup>=</sup> () () . *Bias.* Compute expectations using independence and change of variables. For the denominator,

$$
\mathbb{E}[A_n(x)] = n \mathbb{E}[K_h(x - X)]
$$
  
\n
$$
= n \int_{\mathbb{R}^d} h^{-d} K(\frac{x - u}{h}) p(u) du
$$
  
\n
$$
= n \int_{\mathbb{R}^d} K(t) p(x - ht) dt \qquad (t := (x - u)/h)
$$
  
\n
$$
= n \int_{\mathbb{R}^d} K(t) (p(x) - ht^{\top} \nabla p(x) + \frac{h^2}{2} t^{\top} \nabla^2 p(x) t + o(h^2)) dt
$$
  
\n
$$
= n (p(x) + \frac{h^2}{2} \underbrace{\int t^{\top} \nabla^2 p(x) t K(t) dt}_{= \mu_2(K) \Delta p(x)} + o(h^2)),
$$

where we used symmetry ∫ () <sup>=</sup> <sup>0</sup> and isotropy <sup>∫</sup> ⊤() <sup>=</sup> 2(), which implies <sup>∫</sup> <sup>⊤</sup>∇ 2()() <sup>=</sup> 2()tr(∇2()) <sup>=</sup> 2()Δ(). Similarly, for the numerator,

$$
\mathbb{E}[B_n(x)] = n\mathbb{E}[K_h(x - X)Y] = n \int K(t)(mp)(x - ht)dt
$$
  
=  $n \int K(t) ((mp)(x) - ht^{\top} \nabla (mp)(x) + \frac{h^2}{2}t^{\top} \nabla^2 (mp)(x)t + o(h^2)) dt$   
=  $n(m(x)p(x) + \frac{h^2}{2}\mu_2(K)\text{tr}(\nabla^2 (mp)(x)) + o(h^2))$   
=  $n(m(x)p(x) + \frac{h^2\mu_2(K)}{2}(p\Delta m + m\Delta p + 2\nabla m^{\top}\nabla p)(x) + o(h^2)),$ 

where the last step uses the fact that tr ∇ 2 () <sup>=</sup> Δ <sup>+</sup> Δ <sup>+</sup> <sup>2</sup>∇⊤∇ by the product rule and symmetry of mixed derivatives.

Now expand the ratio <sup>E</sup>[ ()] <sup>E</sup>[ ()] using the identity

$$
\frac{a_0 + h^2 a_2 + o(h^2)}{b_0 + h^2 b_2 + o(h^2)} = \frac{a_0}{b_0} + h^2 \frac{a_2 b_0 - a_0 b_2}{b_0^2} + o(h^2),
$$

with <sup>0</sup> <sup>=</sup> ()(), <sup>2</sup> <sup>=</sup> 2() 2 Δ <sup>+</sup> Δ <sup>+</sup> <sup>2</sup>∇⊤∇ (), <sup>0</sup> <sup>=</sup> (), and <sup>2</sup> <sup>=</sup> 2() 2 <sup>Δ</sup>(). This yields

$$
\frac{\mathbb{E}[B_n(x)]}{\mathbb{E}[A_n(x)]} = m(x) + \frac{h^2 \mu_2(K)}{2} \frac{(p\Delta m + m\Delta p + 2\nabla m^\top \nabla p)p - mp\Delta p}{p^2} \Big|_x + o(h^2)
$$

$$
= m(x) + \frac{h^2 \mu_2(K)}{2} \left(\Delta m(x) + 2\nabla m(x)^\top \frac{\nabla p(x)}{p(x)}\right) + o(h^2),
$$

which recovers our statement. *Variance.* Linearize b() <sup>=</sup> ()/() around (E[()], <sup>E</sup>[()]) and use independence. To leading order,

$$
\text{Var}[\widehat{m}(x)] \approx \frac{\text{Var}[B_n(x)]}{(\mathbb{E}[A_n(x)])^2}.
$$

Compute

$$
\text{Var}[B_n(x)] = \sum_{i=1}^n \text{Var}(K_h(x - X_i)Y_i) \quad \text{(independence)}
$$
\n
$$
= n \mathbb{E}[K_h(x - X)^2 \text{Var}(Y | X)] = n \mathbb{E}[K_h(x - X)^2 v(X)]
$$
\n
$$
= n \int h^{-2d} K \left(\frac{x - u}{h}\right)^2 v(u) p(u) du
$$
\n
$$
= n h^{-d} \int K(t)^2 v(x - ht) p(x - ht) dt = n h^{-d} \left(R(K)v(x) p(x) + o(1)\right)
$$

while

$$
\mathbb{E}[A_n(x)] = n\big(p(x) + o(1)\big).
$$

Therefore,

$$
\text{Var}[\widehat{m}(x)] \approx \frac{nh^{-d}R(K)v(x)p(x)}{n^2p(x)^2} = \frac{R(K)}{nh^d} \frac{v(x)}{p(x)} + o((nh^d)^{-1})
$$

completing the proof. □

## <span id="page-32-0"></span>**B.6 Proof of Equation [\(5\)](#page-8-3) to Equation [\(6\)](#page-11-1)**

*Proof.* Let **z**¯ = 1 Í =1 **<sup>z</sup>**, denote the mean of the first vectors.

,

,

We prove that:

$$
\frac{1}{V_g} \sum_{v=1}^{V_g} \frac{1}{V} \sum_{v'=1}^{V} ||\mathbf{z}_{n,v} - \mathbf{z}_{n,v'}||_2^2 = \frac{1}{V} \sum_{v'=1}^{V} ||\bar{\mathbf{z}} - \mathbf{z}_{n,v'}||_2^2
$$
\n(14)

Expanding the left-hand side:

LHS = 
$$
\frac{1}{V_g V} \sum_{v=1}^{V_g} \sum_{v'=1}^{V} ||\mathbf{z}_{n,v} - \mathbf{z}_{n,v'}||_2^2
$$
 (15)

$$
= \frac{1}{V_g V} \sum_{v=1}^{V_g} \sum_{v'=1}^{V} \left( ||\mathbf{z}_{n,v}||_2^2 - 2 \mathbf{z}_{n,v}^T \mathbf{z}_{n,v'} + ||\mathbf{z}_{n,v'}||_2^2 \right)
$$
(16)

$$
= \frac{1}{V_g} \sum_{v=1}^{V_g} ||\mathbf{z}_{n,v}||_2^2 - \frac{2}{V_g V} \sum_{v=1}^{V_g} \sum_{v'=1}^{V} \mathbf{z}_{n,v}^T \mathbf{z}_{n,v'} + \frac{1}{V} \sum_{v'=1}^{V} ||\mathbf{z}_{n,v'}||_2^2
$$
(17)

$$
= \frac{1}{V_g} \sum_{v=1}^{V_g} ||\mathbf{z}_{n,v}||_2^2 - \frac{2}{V} \bar{\mathbf{z}}^T \sum_{v'=1}^{V} \mathbf{z}_{n,v'} + \frac{1}{V} \sum_{v'=1}^{V} ||\mathbf{z}_{n,v'}||_2^2
$$
(18)

Expanding the right-hand side:

RHS = 
$$
\frac{1}{V} \sum_{v'=1}^{V} (||\bar{\mathbf{z}}||_2^2 - 2\bar{\mathbf{z}}^T \mathbf{z}_{n,v'} + ||\mathbf{z}_{n,v'}||_2^2)
$$
 (19)

$$
= ||\bar{\mathbf{z}}||_2^2 - \frac{2}{V}\bar{\mathbf{z}}^T \sum_{v'=1}^V \mathbf{z}_{n,v'} + \frac{1}{V} \sum_{v'=1}^V ||\mathbf{z}_{n,v'}||_2^2
$$
\n(20)

To complete the proof, we verify that:

$$
\frac{1}{V_g} \sum_{v=1}^{V_g} ||\mathbf{z}_{n,v}||_2^2 = ||\mathbf{\bar{z}}||_2^2
$$
 (21)

Expanding the right-hand side:

$$
\|\bar{\mathbf{z}}\|_{2}^{2} = \left\| \frac{1}{V_{g}} \sum_{v=1}^{V_{g}} \mathbf{z}_{n,v} \right\|_{2}^{2}
$$
 (22)

$$
= \frac{1}{V_S^2} \sum_{v=1}^{V_S} \sum_{v''=1}^{V_S} \mathbf{z}_{n,v}^T \mathbf{z}_{n,v''}
$$
(23)

$$
=\frac{1}{V_g}\sum_{v=1}^{V_g}||\mathbf{z}_{n,v}||_2^2
$$
 (24)

Therefore, LHS = RHS, completing the proof. □

## <span id="page-33-0"></span>**B.7 Proof of thm. [8](#page-25-2)**

*Proof.* For each ,

$$
\text{Bias}[\widehat{m}(x)] = \frac{h^2 \mu_2(K)}{2} \left( \Delta m(x) + 2 \nabla m(x)^\top \nabla \log p(x) \right) + o(h^2).
$$

Square and integrate against ():

$$
\mathcal{B}^{2}(h; p, m) = \left(\frac{h^{2}\mu_{2}(K)}{2}\right)^{2} \int \left(\Delta m(x) + 2\nabla m(x)^{\top}\nabla \log p(x)\right)^{2} p(x) dx + o(h^{4})
$$
  
\n
$$
\leq \left(\frac{h^{2}\mu_{2}(K)}{2}\right)^{2} \int \left(2(\Delta m(x))^{2} + 2(2\nabla m(x)^{\top}\nabla \log p(x))^{2}\right) p(x) dx + o(h^{4})
$$
  
\n
$$
= \left(\frac{h^{2}\mu_{2}(K)}{2}\right)^{2} \left(2 \int (\Delta m(x))^{2} p(x) dx + 8 \int (\nabla m(x)^{\top}\nabla \log p(x))^{2} p(x) dx\right) + o(h^{4}),
$$

where we used ( <sup>+</sup> ) <sup>2</sup> <sup>≤</sup> <sup>2</sup> <sup>2</sup> <sup>+</sup> <sup>2</sup> <sup>2</sup> pointwise. Since <sup>|</sup>Δ()| ≤ for all , we have

$$
\int (\Delta m)^2 p \le \int B^2 p = B^2
$$

For the second term, first use Cauchy–Schwarz and then integrate against () to obtain

$$
(\nabla m(x)^\top \nabla \log p(x))^2 \le ||\nabla m(x)||^2 ||\nabla \log p(x)||^2 \le L^2 ||\nabla \log p(x)||^2
$$
  
\n
$$
\implies \int (\nabla m(x)^\top \nabla \log p(x))^2 p(x) dx \le L^2 \int ||\nabla \log p(x)||^2 p(x) dx = L^2 J(p).
$$

which can be combined with the bounds above to obtain the desired result. We similarly have for the integrated variance

$$
\mathcal{V}(h; p) = \int \left( \frac{R(K)}{nh^d} \frac{v(x)}{p(x)} + o\big((nh^d)^{-1}\big) \right) p(x) dx = \frac{R(K)}{nh^d} \int v(x) dx + o\big((nh^d)^{-1}\big),
$$

which is independent of . □

### <span id="page-34-0"></span>**B.8 Proof of lemma. [3](#page-6-8)**

*Proof.* We first start by reminding the reader about the original Cramér-Wold theorem that is a function of all possible directions (not unit-norm ones).

<span id="page-34-1"></span>**Theorem 10: Cramér-Wold Cramér and Wold [1936]  
Let X and Y be random vectors in 
$$
\mathbb{R}^D
$$
:  

$$
X \stackrel{d}{=} Y \iff \langle X, a \rangle \stackrel{d}{=} \langle Y, a \rangle, \forall a \in \mathbb{R}^D.
$$
 (25)**

Our proof will follow the same proof as for thm. [10.](#page-34-1) Necessity is immediate: if <sup>=</sup> , then every measurable function of has the same distribution as the corresponding function of , from which the linear mapping ↦→ ⟨, ⟩ for <sup>∈</sup> <sup>S</sup> −1 is a special case. For sufficiency, assume ⟨, ⟩ <sup>=</sup> ⟨, ⟩ for all <sup>∈</sup> <sup>S</sup> −1 . Let () :<sup>=</sup> <sup>E</sup> - ⟨,⟩ and () :<sup>=</sup> <sup>E</sup> -⟨,⟩ denote the characteristic functions of and . Fix an arbitrary <sup>∈</sup> <sup>R</sup> ; if <sup>=</sup> 0, then (0) <sup>=</sup> (0) <sup>=</sup> 1. If <sup>≠</sup> 0, write <sup>=</sup> with :<sup>=</sup> <sup>∥</sup><sup>∥</sup> <sup>&</sup>gt; <sup>0</sup> and :<sup>=</sup> /∥∥ ∈ <sup>S</sup> −1 . By the assumption, ⟨, ⟩ <sup>=</sup> ⟨, ⟩, hence for this and we have

$$
\varphi_X(t) = \mathbb{E}\big[e^{i\langle t,X\rangle}\big] = \mathbb{E}\big[e^{is\langle u,X\rangle}\big] = \mathbb{E}\big[e^{is\langle u,Y\rangle}\big] = \mathbb{E}\big[e^{i\langle t,Y\rangle}\big] = \varphi_Y(t).
$$

Thus () <sup>=</sup> () for all <sup>∈</sup> <sup>R</sup> , i.e., <sup>≡</sup> on <sup>R</sup> . By the uniqueness theorem for characteristic functions, this implies <sup>=</sup> . (ii) Define , :<sup>=</sup> <sup>E</sup> -⟨, ⟩ and := E -⟨,⟩ . Fix <sup>∈</sup> <sup>R</sup> and decompose <sup>=</sup> with :<sup>=</sup> <sup>∥</sup>∥ ≥ <sup>0</sup> and <sup>∈</sup> <sup>S</sup> −1 (take, e.g., <sup>=</sup> /∥<sup>∥</sup> if <sup>≠</sup> 0, and any if <sup>=</sup> 0). The map : <sup>R</sup> <sup>→</sup> <sup>R</sup>, () <sup>=</sup> , is continuous. By the continuous mapping theorem applied to the real-valued random variables ⟨, ⟩ −→ ⟨, ⟩, we obtain

$$
\langle t, X_n \rangle = s \langle u, X_n \rangle \xrightarrow{d} s \langle u, X \rangle = \langle t, X \rangle.
$$

Hence, for every fixed <sup>∈</sup> <sup>R</sup> , the one-dimensional projections satisfy ⟨, ⟩ −→ ⟨, ⟩, which in turn yields pointwise convergence of characteristic functions:

$$
\psi_{n,t} = \mathbb{E}\big[e^{i\langle t,X_n\rangle}\big] \longrightarrow \mathbb{E}\big[e^{i\langle t,X\rangle}\big] = \psi_t, \quad \text{for all } t \in \mathbb{R}^d.
$$

Therefore, by Lévy's continuity theorem, −→ . This completes the proof. □

### <span id="page-35-0"></span>**B.9 Proof of thm. [2](#page-6-3)**

*Proof.* We first formulate the following assumptions required for the proof–all of this are satisfied by typical univariate statistical tests.

 <sup>=</sup> if and only if <sup>=</sup> for all <sup>∈</sup> −1 (population-level equivalence of laws).

 are finite sets with mesh <sup>Δ</sup>() :<sup>=</sup> sup∈ −<sup>1</sup> min∈ <sup>∥</sup> <sup>−</sup> ∥ → <sup>0</sup> as → ∞.

If <sup>≠</sup> , there exists a separating direction ★ <sup>∈</sup> −<sup>1</sup> and a neighborhood of ★ such that

$$
\inf_{a\in U} \lim_{n\to\infty} \Pr\left(T_{a,n} \ge u_n(\alpha)\right) = 1.
$$

(Intuitively: near a truly separating direction, the 1D statistic eventually exceeds the global null threshold with probability → 1.)

(i) Under <sup>0</sup> : <sup>=</sup> , our assumption implies no separating direction exists at the population level, and the calibration of () ensures Pr( <sup>≥</sup> ()) ≤ for all , hence lim sup→∞ Pr(Ψ <sup>=</sup> <sup>1</sup>) ≤ . (ii) Suppose <sup>≠</sup> . Our assumption guarantees that there exists at least one separating direction ★ with ★ <sup>≠</sup> ★ . Our assumption guarantees a neighborhood of ★ in which the projection statistics exceed the global null threshold with probability tending to 1:

$$
\inf_{a\in U} \lim_{n\to\infty} \Pr\left(T_{a,n} \ge u_n(\alpha)\right) = 1.
$$

By assumption, for all large the set contains at least one direction <sup>∈</sup> (dense coverage). Therefore,

$$
Pr(\Psi_n = 1) = Pr(M_n \ge u_n(\alpha)) \ge Pr(T_{a_n,n} \ge u_n(\alpha)) \longrightarrow 1,
$$

which proves consistency. □

## <span id="page-35-1"></span>**B.10 Proof of thm. [5](#page-10-1)**

*Proof.* For each case, consider the function () on <sup>S</sup> −<sup>1</sup> defined by the quantity of interest (CF, CDF, or moment) at a fixed or . Since <sup>∈</sup> (R ), the mapping ↦→ () is in (S −<sup>1</sup> ) for each fixed or .

Given samples {} =1 on the sphere, the best possible reconstruction of from its values at these points is given by spherical interpolation. By classical results on Sobolev spaces and spherical harmonics (see, e.g., [Narcowich et al.](#page-20-21) [\[2006\]](#page-20-21)), the 2 interpolation error for functions in (S −<sup>1</sup> ) using points is bounded by

$$
\mathbb{E}_b \left[ |g(b) - g^*(b)|^2 \right] \le C(D, \alpha) M^{-2\alpha/(D-1)} \|g\|_{H^{\alpha}(\mathbb{S}^{D-1})}^2,
$$

where ∗ is the interpolant matching at the sampled points. The interpolation error bound on the sphere follows from the theory of spherical harmonics and Marcinkiewicz–Zygmund (MZ) inequalities . Any <sup>∈</sup> (S ) admits a spherical harmonics expansion, and the best <sup>2</sup> approximation by harmonics of degree at most satisfies

$$
||f - P_L f||_{L^2(\mathbb{S}^d)} \le (1 + L^2)^{-\alpha/2} ||f||_{H^{\alpha}(\mathbb{S}^d)},
$$

where is the projection onto harmonics of degree <sup>≤</sup> [\[Narcowich et al., 2006,](#page-20-21) Lemma 2.1]. If points are distributed quasi-uniformly on S , then for <sup>∼</sup> 1/ , the set forms a Marcinkiewicz–Zygmund (MZ) set for degree [\[Mhaskar](#page-20-22) [et al., 2001,](#page-20-22) Theorem 1.1]. This allows reconstruction of any function in the space of harmonics of degree at most from its values at these points, and the 2 interpolation error for is bounded by

$$
||f - I_M f||_{L^2(\mathbb{S}^d)} \le C(1 + L^2)^{-\alpha/2} ||f||_{H^{\alpha}(\mathbb{S}^d)},
$$

where is any interpolant matching at the points [\[Narcowich et al., 2006,](#page-20-21) Theorem 3.1]. Substituting <sup>∼</sup> 1/ yields the rate −/ , and thus

$$
\mathbb{E}_{\omega}|f(\omega) - I_M f(\omega)|^2 \le C(d,\alpha)M^{-2\alpha/d}||f||^2_{H^{\alpha}(\mathbb{S}^d)},
$$

with explicit (, ) as in the main theorem. Integrating (or summing) over (for CF and CDF) or (for moments, with weights ) yields the stated bounds. The explicit constant (, ) arises from the theory of spherical Sobolev spaces and is given above.

For the moment case, the sum over is weighted to ensure convergence, as higher moments may grow rapidly. The weights can be chosen, for example, as <sup>=</sup> <sup>1</sup>/!.

This completes the proof. □

## <span id="page-36-0"></span>**B.11 Proof of thm. [3](#page-7-4)**

Pick distinct 0, . . . , +<sup>1</sup> <sup>∈</sup> <sup>R</sup> and consider the linear map : <sup>R</sup> +<sup>2</sup> <sup>→</sup> R +1 , () <sup>=</sup> Í+<sup>1</sup> =0 for <sup>=</sup> <sup>0</sup>, . . . , . Then rank() ≤ <sup>+</sup> 1, so ker() <sup>≠</sup> {0}. Let <sup>∈</sup> ker() \ {0}; from ()<sup>0</sup> <sup>=</sup> Í , we get Í <sup>=</sup> 0, hence has positive and negative entries. Choose a strictly positive probability vector and > <sup>0</sup> small such that <sup>±</sup> :<sup>=</sup> <sup>±</sup> remain probability vectors. Then <sup>+</sup> <sup>=</sup> −, so the distributions supported on {} with masses <sup>±</sup> are distinct yet match moments up to order .

## <span id="page-36-1"></span>**B.12 Proof of thm. [4](#page-9-2)**

*Proof.* Fix the Gaussian weight

$$
w_s(t) = e^{-s^2t^2}, \qquad s > 0,
$$

and define the population CF distance

$$
D(P,G) = \int_{\mathbb{R}} w_s(t) |\varphi_P(t) - \varphi_G(t)|^2 dt.
$$

Let the empirical CF be

$$
\widehat{\varphi}_N(t) = \frac{1}{N} \sum_{i=1}^N e^{itX_i},
$$

and consider the V-statistic estimator

$$
\widehat{D}_V=\int_{\mathbb{R}}w_s(t)\big|\widehat{\varphi}_N(t)-\varphi_G(t)\big|^2dt.
$$

We use only that <sup>|</sup> <sup>|</sup> <sup>=</sup> 1, <sup>|</sup>()| ≤ 1, <sup>|</sup>()| ≤ 1, and integrability of . For each differentiate under the integral (dominated convergence applies because the integrand and its derivative are bounded)

$$
\frac{\partial \widehat{D}_V}{\partial X_i} = \int_{\mathbb{R}} w_s(t) 2 \Re \Big( \big( \widehat{\varphi}_N(t) - \varphi_G(t) \big) \frac{\partial \widehat{\varphi}_N(t)}{\partial X_i} \Big) dt,
$$
  

$$
\frac{\partial \widehat{\varphi}_N(t)}{\partial X_i} = \frac{1}{N} it e^{itX_i},
$$

since <sup>|</sup>b()| ≤ <sup>1</sup> and <sup>|</sup>()| ≤ 1,

$$
\left| \frac{\partial \widehat{D}_V}{\partial X_i} \right| \leq \frac{2}{N} \int w_s(t) |t| \left( |\widehat{\varphi}_N(t)| + |\varphi_G(t)| \right) dt
$$
  

$$
\leq \frac{4}{N} \int w_s(t) |t| dt
$$
  

$$
= \frac{4}{Ns^2},
$$

using ∫ R − 2 2 <sup>|</sup>| <sup>=</sup> <sup>1</sup>/ 2 .

$$
\left|\frac{\partial \widehat{D}_V}{\partial X_i}\right| \leq \frac{4}{N} \int_{\mathbb{R}} w_s(t) |t| dt = \frac{4}{Ns^2}.
$$

Moreover, differentiating once more in and using <sup>|</sup>b()| ≤ 1, <sup>|</sup>()| ≤ <sup>1</sup> gives a global Lipschitz bound

$$
\left|\frac{\partial^2 \widehat{D}_V}{\partial X_i^2}\right| \leq \frac{C}{N} \int_{\mathbb{R}} w_s(t) t^2 dt = \frac{C}{N} \cdot \frac{\sqrt{\pi}}{2s^3},
$$

for some absolute constant arising from bounded factors and product rule. Hence ECF gradients are uniformly bounded and Lipschitz, with scale controlled only by (, ).

(B) (Moment sample-gradients are polynomial in and unbounded for <sup>≥</sup> 2.) Let b be as above. Define the moment objective

$$
\widehat{D}_k = (\bar{\phi} - \mu)^{\top} W (\bar{\phi} - \mu), \qquad \bar{\phi} := \frac{1}{N} \sum_{i=1}^N \phi(X_i), \quad \phi(x) = (x, x^2, \dots, x^k)^{\top},
$$

for a symmetric positive semidefinite <sup>∈</sup> <sup>R</sup> × and Gaussian target moments <sup>=</sup> <sup>E</sup>[()]. For each ,

$$
\frac{\partial \widehat{D}_k}{\partial X_i} = \frac{2}{N} (\bar{\phi} - \mu)^{\top} W \frac{\partial \phi(X_i)}{\partial X_i},
$$

$$
\frac{\partial \phi(X)}{\partial X} = (1, 2X, 3X^2, \dots, kX^{k-1})^{\top}.
$$

The gradient formula follows by the chain rule and linearity of ¯. Let :<sup>=</sup> (¯ <sup>−</sup> ) and write for its -th coordinate. Then

$$
\frac{\partial \widehat{D}_k}{\partial X_i} = \frac{2}{N} \sum_{r=1}^k c_r r X_i^{r-1},
$$

which is a polynomial in of degree deg <sup>=</sup> max{ <sup>−</sup> 1 : <sup>≠</sup> <sup>0</sup>} ≤ <sup>−</sup> 1. In particular, if <sup>≠</sup> <sup>0</sup> (the generic case when the top-weighted deviation is nonzero), then

$$
\left|\frac{\partial \widehat{D}_k}{\partial X_i}\right| \xrightarrow[N_i] \to \infty \quad \text{as} \quad |X_i|^{k-1}.
$$

The expression is a nonconstant polynomial in of degree deg <sup>≤</sup> <sup>−</sup> <sup>1</sup> whenever some <sup>≠</sup> <sup>0</sup> with <sup>≥</sup> 2. Thus the gradient cannot be uniformly bounded on <sup>R</sup>. If <sup>≠</sup> 0, the leading term dominates and the magnitude grows like <sup>|</sup> | −1 , proving unboundedness for <sup>≥</sup> 2. □

### <span id="page-37-0"></span>**B.13 Proof of thm. [6](#page-11-3)**

*Proof.* A direct calculation shows Fix <sup>∈</sup> <sup>R</sup> and abbreviate <sup>B</sup> i ⊤ , so that () <sup>=</sup> 1 Í =<sup>1</sup> . Note that <sup>|</sup> | = 1 almost surely (since ⊤<sup>∈</sup> <sup>R</sup>), and <sup>E</sup>[] <sup>=</sup> () for all . We start from the algebraic identity

$$
\left|\phi_n(t)-\psi(t)\right|^2=\phi_n(t)\overline{\phi_n(t)}-\psi(t)\overline{\phi_n(t)}-\overline{\psi(t)}\phi_n(t)+\left|\psi(t)\right|^2.
$$

Taking expectations term by term gives

$$
\mathbb{E}\left[\left|\phi_{n}-\psi\right|^{2}\right]=\mathbb{E}\left[\left|\phi_{n}\right|^{2}\right]-\psi\mathbb{E}\left[\overline{\phi_{n}}\right]-\overline{\psi}\mathbb{E}\left[\phi_{n}\right]+\left|\psi\right|^{2},\tag{26}
$$

$$
= \mathbb{E}\left[|\phi_n|^2\right] - \psi \overline{\mathbb{E}[\phi_n]} - \overline{\psi}\frac{1}{n} \sum_{j=1}^n \mathbb{E}[Z_j] + |\psi|^2,
$$
\n(27)

$$
= \mathbb{E}\left[|\phi_n|^2\right] - \psi \overline{\phi_\theta} - \overline{\psi}\phi_\theta + |\psi|^2,\tag{28}
$$

$$
= \mathbb{E}\left[|\phi_n|^2\right] - 2\text{Re}\left(\overline{\psi}\phi_\theta\right) + |\psi|^2,\tag{29}
$$

$$
= \mathbb{E}\left[\left|\frac{1}{n}\sum_{j=1}^{n}Z_j\right|^2\right] - 2\text{Re}(\overline{\psi}\phi_\theta) + |\psi|^2,\tag{30}
$$

$$
=\frac{1}{n^2}\sum_{j=1}^n\sum_{l=1}^n\mathbb{E}\left[Z_j\overline{Z_l}\right]-2\text{Re}(\overline{\psi}\phi_{\theta})+|\psi|^2,
$$
\n(31)

$$
(32)
$$

Since the are i.i.d.,

$$
\mathbb{E}\left[Z_j\overline{Z_l}\right] = \begin{cases} \mathbb{E}\left[|Z_1|^2\right] = 1, & \text{if } j = l, \\ \mathbb{E}[Z_j]\overline{\mathbb{E}[Z_l]} = \phi_\theta \overline{\phi_\theta} = |\phi_\theta|^2, & \text{if } j \neq l, \end{cases}
$$

hence

$$
\mathbb{E}\left[|\phi_n|^2\right] = \frac{1}{n^2} \left(n + n(n-1)|\phi_\theta|^2\right)
$$

$$
= \frac{1}{n} + \left(1 - \frac{1}{n}\right)|\phi_\theta|^2
$$

$$
= |\phi_\theta|^2 + \frac{1 - |\phi_\theta|^2}{n}
$$

Plugging these, we obtain

$$
\mathbb{E}\left[\left|\phi_{n}-\psi\right|^{2}\right] = \left(|\phi_{\theta}|^{2} + \frac{1-|\phi_{\theta}|^{2}}{n}\right) - 2\text{Re}(\overline{\psi}\phi_{\theta}) + |\psi|^{2}
$$

$$
= \left(|\phi_{\theta}|^{2} - 2\text{Re}(\overline{\psi}\phi_{\theta}) + |\psi|^{2}\right) + \frac{1-|\phi_{\theta}|^{2}}{n}
$$

$$
= |\phi_{\theta} - \psi|^{2} + \frac{1-|\phi_{\theta}|^{2}}{n}.
$$

Under Dominated convergence, <sup>E</sup>[∇()] <sup>=</sup> <sup>∇</sup>E[()], hence

$$
\mathbb{E}\left[\nabla_{\theta}D_n(t)\right] = \nabla_{\theta} \left|\phi_{\theta}(t) - \psi(t)\right|^2 + \nabla_{\theta} \frac{1 - |\phi_{\theta}(t)|^2}{n},
$$

concluding the proof.

In practice one replaces ∫ R ()(·) by a deterministic quadrature on a uniform grid ∈ [−, ] with weights (e.g. trapezoidal rule) and a Gaussian window () <sup>=</sup> − 2 . All statements above remain valid with the integral replaced by Í (·):

$$
L(\theta) \approx \sum_{k} \omega_{k} |\phi_{\theta}(t_{k}) - \psi(t_{k})|^{2}, \quad \widehat{L}_{n}(\theta) \approx \sum_{k} \omega_{k} |\phi_{n}(t_{k}) - \psi(t_{k})|^{2},
$$

and the bias term becomes

$$
Bias(\theta) = -\frac{1}{n} \sum_{k} \omega_k \nabla_{\theta} |\phi_{\theta}(t_k)|^2.
$$

Since the grid and weights are deterministic, they do not affect unbiasedness with respect to sampling; they only introduce a deterministic approximation error to the target functional (). □

### <span id="page-39-0"></span>**B.14 Proof of VICReg's Recovery**

*Proof.* We prove this result in two parts.

**Part I:** <sup>E</sup>[**X**] <sup>=</sup> **<sup>0</sup>** Given that <sup>E</sup>[⟨**X**, **<sup>a</sup>**⟩] <sup>=</sup> <sup>0</sup> for all unit vectors **<sup>a</sup>**, and noting that ⟨**X**, **<sup>a</sup>**⟩ <sup>=</sup> **<sup>a</sup> X**, we have:

<span id="page-39-1"></span>
$$
\mathbb{E}[\mathbf{a}^T \mathbf{X}] = 0 \quad \text{for all } \mathbf{a} \in \mathbb{R}^d \text{ with } ||\mathbf{a}|| = 1 \tag{33}
$$

By linearity of expectation:

$$
\mathbf{a}^T \mathbb{E}[\mathbf{X}] = 0 \quad \text{for all unit vectors } \mathbf{a}
$$
 (34)

Let = E[**X**]. We claim that = **0**. Suppose, for the sake of contradiction, that ≠ **0**. Then ∥∥<sup>2</sup> > 0. Define the unit vector:

$$
\mathbf{a}^* = \frac{\mu}{\|\mu\|_2} \tag{35}
$$

Since **a** ∗ is a unit vector, equation [\(33\)](#page-39-1) implies:

$$
(\mathbf{a}^*)^T \boldsymbol{\mu} = 0 \tag{36}
$$

However, substituting the definition of **a** ∗ :

$$
(\mathbf{a}^*)^T \boldsymbol{\mu} = \left(\frac{\boldsymbol{\mu}}{\|\boldsymbol{\mu}\|_2}\right)^T \boldsymbol{\mu} = \frac{\boldsymbol{\mu}^T \boldsymbol{\mu}}{\|\boldsymbol{\mu}\|_2} = \frac{\|\boldsymbol{\mu}\|_2^2}{\|\boldsymbol{\mu}\|_2} = \|\boldsymbol{\mu}\|_2 > 0
$$
\n(37)

This contradiction establishes that = **0**.

**Part II:** Cov(**X**) <sup>=</sup> **<sup>I</sup>** Since <sup>E</sup>[**X**] <sup>=</sup> **<sup>0</sup>**, we have:

$$
Var(\langle \mathbf{X}, \mathbf{a} \rangle) = \mathbb{E}[(\langle \mathbf{X}, \mathbf{a} \rangle)^2] = \mathbb{E}[(\mathbf{a}^T \mathbf{X})^2]
$$
(38)

Expanding the quadratic form:

$$
\mathbb{E}[(\mathbf{a}^T \mathbf{X})^2] = \mathbb{E}[\mathbf{a}^T \mathbf{X} \mathbf{X}^T \mathbf{a}] = \mathbf{a}^T \mathbb{E}[\mathbf{X} \mathbf{X}^T] \mathbf{a}
$$
\n(39)

Since E[**X**] = **0**, the covariance matrix is Cov(**X**) = E[**XX** ]. Let = Cov(**X**). The variance condition gives us:

<span id="page-39-2"></span>
$$
\mathbf{a}^T \Sigma \mathbf{a} = 1 \quad \text{for all unit vectors } \mathbf{a} \tag{40}
$$

We now show that <sup>=</sup> **<sup>I</sup>**. *Step 1: Diagonal entries.* For ∈ {1, <sup>2</sup>, . . . , }, let **<sup>e</sup>** denote the -th standard basis vector. Setting **<sup>a</sup>** <sup>=</sup> **<sup>e</sup>** in equation [\(40\)](#page-39-2):

$$
\mathbf{e}_i^T \Sigma \mathbf{e}_i = \Sigma_{ii} = 1 \tag{41}
$$

Therefore, all diagonal entries of equal 1. *Step 2: Off-diagonal entries.* For distinct indices , ∈ {1, <sup>2</sup>, . . . , }, consider the unit vector:

$$
\mathbf{a} = \frac{\mathbf{e}_i + \mathbf{e}_j}{\|\mathbf{e}_i + \mathbf{e}_j\|_2} = \frac{\mathbf{e}_i + \mathbf{e}_j}{\sqrt{2}} \tag{42}
$$

Applying equation [\(40\)](#page-39-2):

$$
\mathbf{a}^T \Sigma \mathbf{a} = \frac{1}{2} (\mathbf{e}_i + \mathbf{e}_j)^T \Sigma (\mathbf{e}_i + \mathbf{e}_j) = 1
$$
\n(43)

Expanding the quadratic form and using the symmetry of :

$$
\frac{1}{2}(\mathbf{e}_i^T \Sigma \mathbf{e}_i + 2 \mathbf{e}_i^T \Sigma \mathbf{e}_j + \mathbf{e}_j^T \Sigma \mathbf{e}_j) = 1
$$
\n(44)

$$
\frac{1}{2}(\Sigma_{ii} + 2\Sigma_{ij} + \Sigma_{jj}) = 1\tag{45}
$$

$$
\frac{1}{2}(1 + 2\Sigma_{ij} + 1) = 1\tag{46}
$$

$$
1 + \Sigma_{ij} = 1 \tag{47}
$$

$$
\Sigma_{ij} = 0 \tag{48}
$$

Therefore, all off-diagonal entries of equal zero, establishing that <sup>=</sup> **<sup>I</sup>**. □

# **C Background**

**Foundation: The Linear Regression Model** We start with the standard linear regression model:

$$
y = X\beta + \varepsilon
$$

where:

- **<sup>y</sup>** <sup>=</sup> [1, 2, . . . , ] ∈ R is the response vector
- **X** ∈ R × is the design matrix with **<sup>X</sup>** <sup>=</sup>
- <sup>=</sup> [1, 2, . . . , ] ∈ R is the parameter vector
- <sup>=</sup> [1, 2, . . . , ] ∼ (**0**, 2 **<sup>I</sup>**) is the error vector

The error assumption means:

$$
\mathbb{E}[\varepsilon_i] = 0, \quad \text{Var}(\varepsilon_i) = \sigma^2, \quad \text{Cov}(\varepsilon_i, \varepsilon_j) = 0 \text{ for } i \neq j
$$

**Step 1: Deriving the OLS Estimator** To find the OLS estimator, we minimize the sum of squared residuals:

$$
SSR(\boldsymbol{\beta}) = \sum_{i=1}^{n} (y_i - \mathbf{x}_i^T \boldsymbol{\beta})^2 = (\mathbf{y} - \mathbf{X}\boldsymbol{\beta})^T (\mathbf{y} - \mathbf{X}\boldsymbol{\beta})
$$

Expanding this quadratic form:

$$
SSR(\beta) = \mathbf{y}^T \mathbf{y} - 2\beta^T \mathbf{X}^T \mathbf{y} + \beta^T \mathbf{X}^T \mathbf{X} \beta
$$
\n(49)

Taking the derivative with respect to :

Setting equal to zero and solving:

$$
\frac{\partial \text{SSR}}{\partial \beta} = -2\mathbf{X}^T \mathbf{y} + 2\mathbf{X}^T \mathbf{X} \beta
$$

$$
-2\mathbf{X}^T \mathbf{y} + 2\mathbf{X}^T \mathbf{X} \beta = \mathbf{0}
$$

$$
\mathbf{X}^T \mathbf{X} \beta = \mathbf{X}^T \mathbf{y}
$$

$$
\hat{\beta} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}
$$

Assuming **X X** is invertible:

<span id="page-40-0"></span>**D Details on Low-Discrepancy Sequences**

Quasi-Monte Carlo (QMC) methods, such as the Sobol sequence, are widely used to generate low-discrepancy samples in the unit hypercube, providing improved uniformity over purely random sampling. To obtain samples uniformly distributed on the hypersphere, each QMC point is mapped to a standard normal vector via the inverse cumulative

<span id="page-41-0"></span>![](./assets/07-lejepa/_page_41_Figure_1.jpeg)

<span id="page-41-2"></span>**Figure 15.** Depiction of the expected BCS loss upper bound (thm. [5\)](#page-10-1) for various smoothness values . We clearly see that as the smoothness increases (**blue to red**), as the upper bound decreases more and more rapidly with .

| Freeze Backbone | Model Name       | Samples per Class |       |       |       |       |       |       |
|-----------------|------------------|-------------------|-------|-------|-------|-------|-------|-------|
|                 |                  | All               | 1     | 2     | 5     | 10    | 100   | 1000  |
|                 | LeJEPA (Ours)    |                   |       |       |       |       |       |       |
|                 | ConvNeXt-V2 Nano | 82.72             | 29.42 | 36.65 | 50.94 | 59.85 | 75.34 | 81.97 |
|                 | LeViT-128        | 79.41             | 18.45 | 24.08 | 33.11 | 41.76 | 64.59 | 77.59 |
| No              | ResNet-18        | 82.15             | 23.34 | 31.56 | 43.82 | 54.64 | 73.53 | 81.41 |
|                 | ResNet-34        | 83.28             | 24.27 | 31.51 | 44.23 | 53.95 | 74.93 | 82.32 |
|                 | Baselines        |                   |       |       |       |       |       |       |
|                 | DINOv2 Small     | 78.34             | 21.05 | 21.71 | 30.33 | 36.23 | 60.81 | 75.55 |
|                 | DINOv3 ViT-S/16  | 81.60             | 24.71 | 29.43 | 37.71 | 44.71 | 69.87 | 80.54 |
|                 | LeJEPA (Ours)    |                   |       |       |       |       |       |       |
|                 | ConvNeXt-V2 Nano | 76.52             | 28.74 | 36.65 | 50.60 | 59.50 | 72.62 | 77.24 |
|                 | LeViT-128        | 69.00             | 25.85 | 33.30 | 45.52 | 52.43 | 64.37 | 69.39 |
| Yes             | ResNet-18        | 75.95             | 30.48 | 38.22 | 50.85 | 58.86 | 72.70 | 76.39 |
|                 | ResNet-34        | 78.17             | 31.08 | 38.33 | 52.26 | 60.63 | 74.77 | 78.62 |
|                 | Baselines        |                   |       |       |       |       |       |       |
|                 | DINOv2 Small     | 67.62             | 27.68 | 32.22 | 40.72 | 47.72 | 62.49 | 67.89 |
|                 | DINOv3 ViT-S/16  | 71.38             | 30.17 | 36.65 | 45.74 | 51.51 | 65.90 | 71.35 |

**Table 3.** Performance metrics across different sample sizes from Figure [12](#page-15-0)

| Table 4. Top 1 accuracy (in %) with LeJEPA pretraining on Imagenet-100 for 400 epochs (All values are percentages) |  |  |  |
|--------------------------------------------------------------------------------------------------------------------|--|--|--|
|--------------------------------------------------------------------------------------------------------------------|--|--|--|

<span id="page-41-1"></span>

|              | backbone            | resnet50 |         | vit_small_patch8_224 |         |         | vit_tiny_patch8_224 |         |         |         |
|--------------|---------------------|----------|---------|----------------------|---------|---------|---------------------|---------|---------|---------|
| w/ predictor | Projector<br>w/ SWA | 1-layer  | 2-layer | 3-layer              | 1-layer | 2-layer | 3-layer             | 1-layer | 2-layer | 3-layer |
|              | False               | 79.71    | 82.44   | 83.93                | 76.59   | 80.77   | 81.07               | 71.79   | 76.87   | 80.37   |
| False        | True                | 79.79    | 82.69   | 83.50                | 79.96   | 83.63   | 84.12               | 75.86   | 82.36   | 80.50   |
|              | False               | 79.41    | 82.44   | 83.57                | 77.58   | 79.41   | 81.91               | 67.74   | 77.64   | 80.73   |
| True         | True                | 78.87    | 82.04   | 82.82                | 77.11   | 81.77   | 82.58               | 69.53   | 78.27   | 79.77   |

distribution function (CDF), and then projected onto the sphere by normalization. This approach leverages the rotational invariance of the multivariate normal distribution, ensuring that the resulting directions are uniformly distributed on

<span id="page-42-3"></span>**Table 5. Small architecture in-domain LeJEPA pretraining** from random initialization across datasets and architectures, with frozen backbone linear evaluation. First, **LeJEPA is able to produce near state-of-the-art performances on tiny dataset with only a thousand samples**, e.g., flowers102. Second, **on non-natural image data, LeJEPA clearly outperforms the latest frontier vision models**, e.g., Galaxy10. See Figure [12](#page-15-0) for additional experiments with varying number of training samples and with full finetuning.

|                               | Pretraining<br># train. samples | flowers102<br>1020 | cifar100<br>50000 | food101<br>75750 | inet10<br>13000 | cifar10<br>50000 | galaxy10<br>11008 |
|-------------------------------|---------------------------------|--------------------|-------------------|------------------|-----------------|------------------|-------------------|
| LeJEPA (convnextv2_nano) 14M  | in-domain                       | 64.34              | 69.26             | 69.59            | 90.81           | 92.22            | 76.05             |
| LeJEPA (resnet18) 11M         | in-domain                       | 74.57              | 69.94             | 73.57            | 92.36           | 92.51            | 75.32             |
| LeJEPA (resnet34) 21M         | in-domain                       | 71.85              | 70.44             | 74.95            | 92.80           | 93.16            | 77.29             |
| LeJEPA (resnext26ts) 8M       | in-domain                       | 82.19              | 69.10             | 76.77            | 92.82           | 91.59            | 73.78             |
| LeJEPA (swin_tiny) 27M        | in-domain                       | 63.94              | 65.08             | 78.40            | 92.87           | 92.67            | 74.89             |
| IJEPA-inet22k (ViT-H/14) 630M | inet1k                          | 85.76              | 86.93             | 81.06            | 98.65           | 97.77            | 62.93             |

<span id="page-42-1"></span>**Table 6.** Time (in millisecond) to compute the proposed SIGReg loss from algorithm [1](#page-9-1) on a Tesla V100-SXM2-16GB for varying mini-batch size (), number of slices (), integration points. Results are computed over <sup>10</sup> runs.

| N     | M    | # integration<br>points | mean (ms) | std (ms) |
|-------|------|-------------------------|-----------|----------|
| 512   | 512  | 16                      | 0.465236  | 0.011642 |
| 512   | 512  | 64                      | 0.461317  | 0.003894 |
| 512   | 512  | 256                     | 0.627644  | 0.003337 |
| 2048  | 512  | 16                      | 1.406441  | 0.002415 |
| 8192  | 512  | 16                      | 6.188304  | 0.007226 |
| 8192  | 8192 | 16                      | 8.685009  | 0.038829 |
| 32768 | 512  | 16                      | 26.373118 | 0.012732 |
| 512   | 2048 | 16                      | 0.465614  | 0.005274 |
| 512   | 8192 | 16                      | 0.670379  | 0.006854 |

|  |  |  | Table 7. Number of Figure 8. |  |
|--|--|--|------------------------------|--|
|--|--|--|------------------------------|--|

<span id="page-42-2"></span>

|        | resnet50 |       |       |       |       |       |       |       |       |       |       |       |
|--------|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| 𝜆      | 0.001    | 0.005 | 0.010 | 0.020 | 0.025 | 0.050 | 0.100 | 0.150 | 0.200 | 0.300 | 0.400 | 0.500 |
| #views |          |       |       |       |       |       |       |       |       |       |       |       |
| 2      | 81.41    | 82.73 | 83.49 | 82.99 | 82.23 | -     | -     | -     | -     | -     | -     | -     |
| 4      | 79.88    | 83.04 | 84.36 | 84.68 | 84.33 | 83.00 | 82.91 | 81.05 | 78.58 | -     | -     | -     |
| 8      | 76.67    | 81.58 | 83.59 | 83.49 | 83.76 | 84.32 | 83.66 | 83.07 | 82.16 | 81.00 | 79.25 | 77.72 |

the sphere's surface. While the low-discrepancy property is not strictly preserved under this nonlinear mapping, the resulting samples are empirically more uniform than random samples and are standard in high-dimensional applications [Marsaglia](#page-20-23) [\[1972\]](#page-20-23), [Dick and Pillichshammer](#page-18-23) [\[2010\]](#page-18-23), [Caflisch](#page-18-24) [\[1998\]](#page-18-24).

**Require:** Number of points , dimension

**Ensure:** Points {**y**} quasi-uniformly distributed on S −1

=1 1: **for** <sup>=</sup> <sup>1</sup> to **do**

2: Generate **<sup>x</sup>** ∈ [0, <sup>1</sup>] as the -th point of a Sobol sequence

3: Transform each component: , = Φ−<sup>1</sup> (,) for <sup>=</sup> <sup>1</sup>, . . . , <sup>⊲</sup> <sup>Φ</sup>−<sup>1</sup> is the inverse CDF of the standard normal

4: Normalize: **<sup>y</sup>** <sup>=</sup> **<sup>z</sup>**/∥**z**∥<sup>2</sup>

5: **end for**

# <span id="page-42-0"></span>**E Shapiro-Wilk Test**

Let X1 < X2 < . . . < Xn denote an ordered random sample of size n from a standard normal distribution. Also, let m 5 (m1,m2,...,mn) be the vector of expected values of standard normal order statistics, and let V 5 (vij ) be the corresponding n 3 n covariance matrix, so that

$$
E(X_i) = m_i
$$
 and cov  $(X_i, X_j) = v_{ij}$ ,  $i, j = 1, 2, ..., n$  (50)

The W test statistic [Shapiro and Wilk](#page-21-15) [\[1965\]](#page-21-15) for normality is then denoted by

$$
W = \frac{\left(\sum_{i=1}^{n} a_{i} Y_{i}\right)}{\sum_{i=1}^{n} \left(Y_{i} - \bar{Y}\right)^{2}} = \frac{(\mathbf{a} \mathbf{Y})}{S^{2}}
$$
  
\n
$$
\mathbf{a'} = (a_{1}, a_{2}, \dots, a_{n}) = \mathbf{m} \mathbf{V}^{-1} \left(\mathbf{m} \mathbf{V}^{-1} \mathbf{V}^{-1} \mathbf{m}\right)^{-1/2}
$$
  
\n
$$
S^{2} = \sum_{i=1}^{n} \left(Y_{i} - \bar{Y}\right)^{2}
$$
\n(51)

[Shapiro and Francia](#page-21-24) [\[1972\]](#page-21-24) suggested replacing the covariance matrix V by the identity matrix I, because for large samples, the observations Yi may be treated as if they are independent (see [Gupta](#page-19-22) [\[1952\]](#page-19-22)). Another asymptotic extension was suggested by [Weisburg and Binham](#page-22-5) [\[1975\]](#page-22-5)

$$
E(X_i) = m_i \approx \Phi^{-1} \left( \frac{i - \frac{3}{8}}{n + \frac{1}{4}} \right) \quad i = 1, 2, ..., n
$$
 (52)

building atop [Elfving](#page-18-25) [\[1947\]](#page-18-25)'s approximation but using 3/8 instead of /8.

[Rahman and Govindarajulu](#page-20-24) [\[1997\]](#page-20-24) proposed another variation using the approximation for the expected values of order statistics given by [Blom](#page-18-26) [\[1958\]](#page-18-26) and the approximations for the elements of the variance± covariance matrix given by [Blom](#page-18-26) [\[1958\]](#page-18-26), [Mosteller](#page-20-25) [\[2006\]](#page-20-25). These approximations are

$$
E(X_i) = m_i \approx \Phi^{-1}\left(\frac{i}{N+1}\right), \quad i = 1, 2, \dots, n
$$
\n
$$
(53)
$$

cov 
$$
(X_i, X_j) = v_{ij} \approx \frac{p_i p_j}{(n+2) f(m_i) f(m_j)}, \quad i, j = 1, 2, ..., n
$$
 (54)

$$
p_i = \frac{i}{n+1} \tag{55}
$$

We know (see [Hammersley and Morton](#page-19-23) [\[1954\]](#page-19-23), [Plackett](#page-20-26) [\[1958\]](#page-20-26))

$$
\mathbf{V}^{-1} = (n+1)(n+2)
$$
\n
$$
\times \begin{pmatrix}\n2\phi^{2}(m_{1}) & -\phi(m_{1})\phi(m_{2}) & 0 & 0 & \cdots & 0 \\
-\phi(m_{1})\phi(m_{2}) & 2\phi^{2}(m_{2}) & -\phi(m_{2})\phi(m_{3}) & 0 & \cdots & 0 \\
0 & -\phi(m_{2})\phi(m_{3}) & 2\phi^{2}(m_{3}) & -\phi(m_{3})\phi(m_{4}) & \cdots & 0 \\
\vdots & \vdots & \vdots & \ddots & \vdots & \vdots \\
0 & 0 & 0 & 0 & \cdots & 2\phi^{2}(m_{n})\n\end{pmatrix}
$$
\n(56)

## <span id="page-43-0"></span>**F Multivariate Statistics**

We ideally would like to compare the distributions. One slight variation is to compare the Characteristic function of the distributions. Given samples 1, . . . , , the Empirical Characteristic Function (ECF) is defined as

$$
\hat{\psi}_N(t) = \frac{1}{N} \sum_{n=1}^N e^{-it^\top y_n}
$$

We can now compare our ECF to the one of the target distribution and build the statistic

$$
N\int |\hat{\psi}_N(t)-\psi_0(t)|^2\omega(t)dt=N\int |\hat{\psi}_N(t)-e^{-||t||_2/2}|^2\omega(t)dt,
$$

if the weighting function is given by () = (2<sup>2</sup> ) <sup>−</sup>/<sup>2</sup> − ∥∥ 2 2 <sup>2</sup> then the following simplification can be made

$$
\begin{split} \text{BHEP}_{n,\beta} &= \frac{1}{n} \sum_{j,k=1}^{n} \exp\left(-\frac{\beta^2 \left\|Y_{n,j} - Y_{n,k}\right\|^2}{2}\right) \\ &- \frac{2}{\left(1 + \beta^2\right)^{d/2}} \sum_{j=1}^{n} \exp\left(-\frac{\beta^2 \left\|Y_{n,j}\right\|^2}{2\left(1 + \beta^2\right)}\right) + \frac{n}{\left(1 + 2\beta^2\right)^{d/2}}. \end{split}
$$

with > 0, Baringhaus-Henze-Epps-Pulley. From [1](#page-0-1) leading to the HZ test [2](#page-0-1) uses

$$
\beta_n = 2^{-1/2}((2d+1)n/4)^{1/(d+4)}
$$
\n(57)

the same can be done with the moment generating function [3](#page-0-1)

$$
T_{n,\beta} = \pi^{d/2} \left( \frac{1}{n} \sum_{i,j=1}^{n} \frac{1}{\beta^{d/2}} \exp\left( \frac{\left\| Y_{n,i} + Y_{n,j} \right\|^2}{4\beta} \right) + \frac{n}{(\beta - 1)^{d/2}} -2 \sum_{j=1}^{n} \frac{1}{(\beta - 1/2)^{d/2}} \exp\left( \frac{\left\| Y_{n,j} \right\|^2}{4\beta - 2} \right) \right),
$$

here with > 2

There is also one combining both[4](#page-0-1) !

$$
T_{n,\gamma} := \int_{\mathbb{R}^d} U_n^2(t) w_{\gamma}(t) dt
$$
  
\n
$$
U_n(t) := \sqrt{n} (R_n(t) M_n(t) - 1)
$$
  
\n
$$
T_{n,\gamma} = \left(\frac{\pi}{\gamma}\right)^{d/2} \left\{ \frac{1}{2n^3} \sum_{j,k,l,m=1}^n \left[ \exp\left(\frac{\left\|Y_{jk}^+\right\|^2 - \left\|Y_{\ell m}^-\right\|^2}{4\gamma}\right) \cos\left(\frac{Y_{jk}^{+\top} Y_{\ell m}^-}{2\gamma}\right) \right. \right\}
$$
  
\n
$$
+ \exp\left(\frac{\left\|Y_{jk}^+\right\|^2 - \left\|Y_{\ell m}^+\right\|^2}{4\gamma}\right) \cos\left(\frac{Y_{jk}^{+\top} Y_{\ell m}^+}{2\gamma}\right) \right]
$$
  
\n
$$
- \frac{2}{n} \sum_{j,k=1}^n \exp\left(\frac{\left\|Y_{n,j}\right\|^2 - \left\|Y_{n,k}\right\|^2}{4\gamma}\right) \cos\left(\frac{Y_{n,j}^{\top} Y_{n,k}}{2\gamma}\right) + n \right\},
$$
  
\n(59)

and its simplified version

$$
\widetilde{T}_{n,\gamma} := \int_{\mathbb{R}^d} U_n(t) w_{\gamma}(t) \mathrm{d}t. \tag{60}
$$

$$
\widetilde{T}_{n,\gamma} = \left(\frac{\pi}{\gamma}\right)^{d/2} \sqrt{n} \left(\frac{1}{n^2} \sum_{j,k=1}^n \exp\left(\frac{\left\|Y_{n,j}\right\|^2 - \left\|Y_{n,k}\right\|^2}{4\gamma}\right) \cos\left(\frac{Y_{n,j}^\top Y_{n,k}}{2\gamma}\right) - 1\right)
$$
\n(61)

Also one testing the derivative [5](#page-0-1)

$$
HV_{n,\gamma} := n \int ||\nabla M_n(t) - tM_n(t)||^2 \widetilde{w}_{\gamma}(t) dt
$$
\n(62)

<sup>1</sup>[https://www.routledge.com/Density-Estimation-for-Statistics-and-Data-Analysis/Silverman/p/book/9780412246203?srsltid=](https://www.routledge.com/Density-Estimation-for-Statistics-and-Data-Analysis/Silverman/p/book/9780412246203?srsltid=AfmBOoodlL-CtlqL0JVC-LcP6mOWw6VTt51_YstdZOW4W3iuicu1VFyg) [AfmBOoodlL-CtlqL0JVC-LcP6mOWw6VTt51\\_YstdZOW4W3iuicu1VFyg](https://www.routledge.com/Density-Estimation-for-Statistics-and-Data-Analysis/Silverman/p/book/9780412246203?srsltid=AfmBOoodlL-CtlqL0JVC-LcP6mOWw6VTt51_YstdZOW4W3iuicu1VFyg)

<sup>2</sup><https://www.tandfonline.com/doi/abs/10.1080/03610929008830400>

<sup>3</sup><https://arxiv.org/pdf/1711.07199>

<sup>4</sup><https://arxiv.org/pdf/1706.03029>

<sup>5</sup><https://arxiv.org/pdf/1901.03986>

**LeJEPA:** [Sec 1: Intro](#page-1-0) | [Sec 2: Background](#page-2-0) | [Sec 3: Why Gaussian?](#page-4-0) | [Sec 4: SIGReg](#page-5-0) | [Sec 5: LeJEPA](#page-10-0) | [Sec 6: Experiments](#page-11-0)

$$
HV_{n,\gamma} = \frac{1}{n} \left(\frac{\pi}{\gamma}\right)^{d/2} \sum_{j,k=1}^{n} \exp\left(\frac{\left\|Y_{n,j,k}^{+}\right\|^{2}}{4\gamma}\right) \left(Y_{n,j}^{+}Y_{n,k} - \frac{\left\|Y_{n,j,k}^{+}\right\|^{2}}{2\gamma} + \frac{d}{2\gamma} + \frac{\left\|Y_{n,j,k}^{+}\right\|^{2}}{4\gamma^{2}}\right).
$$
(63)

skewness [6](#page-0-1) :

$$
b_{1,d} = \frac{1}{n^2} \sum_{j,k=1}^{n} \left( Y_{n,j}^\top Y_{n,k} \right)^3 \tag{64}
$$

skewness [7](#page-0-1) :

$$
\widetilde{b}_{1,d} = \frac{1}{n^2} \sum_{j,k=1}^{n} Y_{n,j}^{\top} Y_{n,k} ||Y_{n,j}||^2 ||Y_{n,k}||^2
$$
\n(65)

which should be 0 for Gaussian and Kurtosis which should be d(d+2)

$$
b_{2,d} = \frac{1}{n} \sum_{j=1}^{n} ||Y_{n,j}||^4
$$
 (66)

<sup>6</sup><https://www.jstor.org/stable/2334770>

<sup>7</sup><https://link.springer.com/article/10.1007/s13171-020-00211-6>

<span id="page-46-0"></span>![](./assets/07-lejepa/_page_46_Figure_1.jpeg)

**Figure 16.** Reprise of Figure [6](#page-8-2) for additional dimensions and number of 1d projections.

<span id="page-47-0"></span>![](./assets/07-lejepa/_page_47_Figure_1.jpeg)

**Figure 17.** Depiction of the distribution of optimized values from OLS when comparing iso and aniso from lemmas. [1](#page-4-4) and [2.](#page-4-5) We clearly observe that the anisotropic version (**blue**) provides much lower variance compared to the isotropic case (**red**). We consider a binary classification (linear separable class) (**top row**), a linear regression task (**middle row**), and a nonlinear regression task with smooth targets (**bottom row**). For each case, we resample the training samples numerous times and produce an estimate for each time. Because the data is 2-dimensional, we can visualize the distribution directly.

<span id="page-48-0"></span>![](./assets/07-lejepa/_page_48_Figure_1.jpeg)

**Figure 18.** Depiction of accuracy (**top**) and cosine similarity between estimated and true estimator (**bottom**) for the OLS setting with varying strength of Tikhonov regularization (**x-axis)** comparing isotropic and anisotropic embeddings. As per thm. [6,](#page-11-3) the anisotropic distribution creates a bias in the OLS estimation for nonzero regularization.

<span id="page-48-1"></span>![](./assets/07-lejepa/_page_48_Figure_3.jpeg)

**Figure 19.** Additional figures provides in Figure [19](#page-48-1)

<span id="page-49-0"></span>![](./assets/07-lejepa/_page_49_Figure_1.jpeg)

**Figure 20.** Proposed trapezoid quadrature for the Epps-Pulley statistic as implemented in algorithm [1.](#page-9-1) We depict the approximation error of the integral for various distributions, demonstrate rapid convergence (faster than quadratic show in **grey line**) across possible embedding distributions.

<span id="page-49-1"></span>![](./assets/07-lejepa/_page_49_Figure_3.jpeg)

**Figure 21.** Additional figures for Figure [10.](#page-14-2)