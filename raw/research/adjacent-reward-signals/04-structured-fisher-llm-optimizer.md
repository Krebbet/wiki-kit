---
url: "https://arxiv.org/pdf/2502.07752"
title: "<span id=\"page-0-1\"></span>Towards Efficient Optimizer Design for LLM via Structured Fisher Approximation with a Low-Rank Extension"
captured_on: "2026-04-20"
capture_method: "pdf"
engine: "marker"
assets_dir: "./assets/structured-fisher-llm-optimizer"
---

# <span id="page-0-1"></span>Towards Efficient Optimizer Design for LLM via Structured Fisher Approximation with a Low-Rank Extension

Wenbo Gong<sup>∗</sup> Microsoft Research wenbogong@microsoft.com

Meyer Scetbon<sup>∗</sup> Microsoft Research t-mscetbon@microsoft.com

Chao Ma<sup>∗</sup> Microsoft Research chao.ma@microsoft.com

Edward Meeds Microsoft Research edward.meeds@microsoft.com

# Abstract

Designing efficient optimizers for large language models (LLMs) with low-memory requirements and fast convergence is an important and challenging problem. This paper makes a step towards the systematic design of such optimizers through the lens of structured [Fisher information matrix \(FIM\)](#page-18-0) approximation. We show that many state-of-the-art efficient optimizers can be viewed as solutions to [FIM](#page-18-0) approximation (under the Frobenius norm) with specific structural assumptions. Building on these insights, we propose two design recommendations of practical efficient optimizers for LLMs, involving the careful selection of structural assumptions to balance generality and efficiency, and enhancing memory efficiency of optimizers with general structures through a novel low-rank extension framework. We demonstrate how to use each design approach by deriving new memory-efficient optimizers: [Row and Column Scaled SGD \(RACS\)](#page-18-1) and Adaptive [low-dimensional](#page-18-2) subspace [estimation \(Alice\).](#page-18-2) Experiments on LLaMA pre-training (up to 1B parameters) validate the effectiveness, showing faster and better convergence than existing memory-efficient baselines and Adam with little memory overhead. Notably, [Alice](#page-18-2) achieves better than 2× faster convergence over Adam, while [RACS](#page-18-1) delivers strong performance on the 1B model with SGD-like memory.

# 1 Introduction

Adaptive optimizers are critical in training large language models (LLMs). Yet, as models and datasets continue to grow, one important issue associated with scaling is the memory overhead of many optimizers, especially in a distributed training setup [\[Dubey et al., 2024,](#page-14-0) [Korthikanti et al.,](#page-15-0) [2023\]](#page-15-0). This has several implications for training, including increased GPU requirements or reduced per-device batch size, which lowers overall training throughput. Adam, for instance, triples memory requirements due to the storage of two internal [exponential moving average \(EMA\)](#page-18-3) states, while other optimizers [\[Gupta et al., 2018,](#page-15-1) [Vyas et al., 2024\]](#page-16-0) with faster convergence (in terms of training steps) can further inflate the total memory. Meanwhile, some memory efficient optimizers, like [stochastic](#page-18-4) [gradient descent \(SGD\),](#page-18-4) fail to train the LLMs effectively. Thus, designing efficient optimizers has become increasingly important.[\\*](#page-0-0)

<sup>\*</sup>These authors contributed equally to this work.

<span id="page-0-0"></span><sup>\*</sup>We define efficiency as the amount of memory and wall-clock time used to achieve a target evaluation loss

<span id="page-1-1"></span>There are several promising lines of research that have advanced one or more of these aspects of efficiency. One aims to design new optimizers that reduce, or remove entirely, internal optimizer states without expensive per-step computation [\[Jordan et al., 2024,](#page-15-2) [Ma et al., 2024,](#page-16-1) [Xu et al., 2024,](#page-16-2) [Zhang et al., 2024,](#page-16-3) [Zhu et al., 2024\]](#page-17-0). Alternatively, low-rank approximations of gradients have also been used to reduce the memory of states with a slight degradation in performance [\[Chen et al.,](#page-14-1) [2024a,](#page-14-1) [Hu et al., 2021,](#page-15-3) [Lialin et al., 2023,](#page-15-4) [Si et al., 2024,](#page-16-4) [Zhao et al., 2024a\]](#page-16-5). Despite these advances, developing new optimizers remains challenging. To address this, this paper explores structured [FIM](#page-18-0) approximation as a practical framework for optimizer design.

To demonstrate the effectiveness of this framework, we begin by showing that many existing optimizers and gradient operators, including Adam, Shampoo, gradient normalization and whitening [\[Gupta et al., 2018,](#page-15-1) [Jordan et al., 2024,](#page-15-2) [Ma et al., 2024,](#page-16-1) [Vyas et al., 2024,](#page-16-0) [You et al., 2019,](#page-16-6) [Zhang](#page-16-3) [et al., 2024\]](#page-16-3), can be recast under it, with different structural assumptions. We then go on to show how to derive two generalizations of Adam[\\*](#page-1-0) with structures based on block diagonal matrices and Kronecker products, named [Eigenspace Adam \(Eigen-Adam\)](#page-18-5) and SOAP/AdaDiag++ [\[Anonymous,](#page-14-2) [2024,](#page-14-2) [Vyas et al., 2024\]](#page-16-0). Although this framework provides a clear link between structures and optimizers, working with more general structures that improve the [FIM](#page-18-0) approximation can come at the cost of efficiency. For example, SOAP can require 7 times more memory than SGD.

Building on these insights, our first design recommendation proposes to choose structural assumptions that balance generality with practical efficiency. We demonstrate this by choosing a structure that generalizes gradient normalization, leading to a new efficient optimizer, [Row and Column Scaled](#page-18-1) [SGD \(RACS\),](#page-18-1) with [SGD-](#page-18-4)like memory requirements.

For optimizers with more general structures it may not be always possible to achieve such a balance. Instead of rejecting the potential of these generalizations, our second design recommendation proposes to apply a novel low-rank extension framework to improve their efficiency. This framework consists of three steps that can convert full-rank optimizers with more general structures into their low-rank approximations with reduced memory and computational costs. We demonstrate this by deriving a low-rank extension of [Eigen-Adam,](#page-18-5) called [Adaptive low-dimensional subspace estimation \(Alice\).](#page-18-2)

On experiments of pre-training LLaMA [\[Touvron et al., 2023\]](#page-16-7) with C4 dataset [\[Raffel et al., 2020\]](#page-16-8), we demonstrate that [RACS](#page-18-1) and [Alice](#page-18-2) consistently outperform Adam and several memory-efficient baselines. [Alice](#page-18-2) achieves better than 2× speed-ups compared to Adam, and [RACS](#page-18-1) performs strongly on pre-training the 1B LLaMA. Additionally, our preliminary results indicate that the 1B model trained by [Alice](#page-18-2) reaches evaluation perplexity on-par or better than the 7B model trained with other memory-efficient baselines.

To summarize, our contributions are:

- We propose structured [FIM](#page-18-0) approximation as a practical framework for optimizer design and show that several existing optimizers can be viewed as special cases within this framework.
- We propose to design optimizers by choosing structures that balance generality and efficiency and demonstrate it with a new optimizer, [RACS.](#page-18-1)
- We present a low-rank extension framework to convert full-rank optimizers to corresponding low-rank approximations and demonstrate it with a new optimizer [Alice.](#page-18-2)
- We demonstrate the effectiveness of [RACS](#page-18-1) and [Alice](#page-18-2) on LLaMa pre-training tasks when compared to Adam and other baselines.

# <span id="page-1-2"></span>2 Preliminaries

### 2.1 Basic notations and setup

Throughout the paper we consider 2D matrix parameters W (i.e. layer weights) of size m × n and m ≤ n; the operation Vec(·) vectorizes the input matrix by stacking its columns; Mat(·) is the inverse of Vec(·) and reshapes the vector back into a matrix. We use L<sup>θ</sup> as the loss function where θ = Vec(W). G = ∇<sup>W</sup> L is the matrix gradient and ⃗g is the vectorized gradient, i.e. ⃗g = Vec(G).

<span id="page-1-0"></span><sup>\*</sup>Generality of structural assumption defines how relaxed this assumption is. We say structure A is more general than B iff. B can be recovered by applying further constraints on A. The general structures tend to give better approximations to [FIM](#page-18-0) than the less general one.

<span id="page-2-3"></span><span id="page-2-2"></span>Table 1: The summary of underlying structure assumptions of existing and newly proposed optimizers, along with practical efficiency. "Generalizes" refers to the optimizer whose structure is generalized, e.g. [Eigen-Adam'](#page-18-5)s structure generalizes Adam (see App. [E.1](#page-36-0) for further details). Optimizers in blue color are new. The "Computation" is the cost of per-step of the optimizer update. We assume n ≥ m ≫ r.

|                    | Adam       | Shampoo                | Eigen-Adam/AdaDiag     | SOAP/AdaDiag++                          | GaLore               | RACS          | Alice                                          |
|--------------------|------------|------------------------|------------------------|-----------------------------------------|----------------------|---------------|------------------------------------------------|
| Stucture           | Diagv(v) R | 1<br>1<br>2n ⊗ L<br>2m | DiagB({UfDiUT<br>f }i) | (UR<br>⊗ UL)D˜ (UR ⊗ UL)T Approx. Alice |                      | S ⊗ Q         | Low-rank to Eigen-Adam                         |
| Generalizes        | N/A        | N/A                    | Adam                   | Eigen-Adam + Shampoo                    | N/A                  | Normalization | GaLore                                         |
| Computation        | O(mn)      | O(m3 + n<br>3<br>)     | O(m3<br>)              | O(m3 + n<br>3<br>)                      | O(mnr + m2n/K) O(mn) |               | O(mnr + m2r/K)                                 |
| Memory             | 3mn        | mn + m2 + n<br>✓       | 2 3mn + 2m2<br>✓       | 3mn + 2m2 + 2n<br>2<br>✓                | mn + 2nr + mr        |               | mn + m + n + 1 mn + 2nr + mr + n + r<br>2<br>✓ |
| Full-rank update ✓ |            |                        |                        |                                         | ✗                    | ✓             |                                                |
| Section            | Sec. 3.1   | Sec. 3.2               | Sec. 3.4               | Sec. 3.5                                | App. B.11            | Sec. 4        | Sec. 5.4                                       |

g<sup>i</sup> denotes the i th column of G. In the paper, we assume W are parameters of one layer. ⊗ indicates the Kronecker product. By default, we use M⊙<sup>2</sup> and <sup>√</sup><sup>M</sup> to denote the element-wise square and square-root of matrix, and M<sup>2</sup> and M 1 <sup>2</sup> indicate the matrix square and square-root by default. For vectors v, both v 2 and v 1 <sup>2</sup> represent element-wise operations. EVD(M, r) performs the [eigen-value](#page-18-6) [decomposition \(EVD\)](#page-18-6) and keeps the top r eigenvectors ordered by the descending eigenvalues. If r is omitted, we keep all eigenvectors. QR(M) with orthonormal M ∈ R <sup>m</sup>×<sup>r</sup> obtains the remaining m − r orthogonal basis via QR decomposition.

We also introduce the following diagonal operations: Diag(M) will extract the diagonals of M to a vector. DiagB(M1, . . . ,Mn) will stack the input sequence of matrices to form a larger block diagonal matrix. Diagv(v) will expand the input vector v to a pure diagonal matrix. DiagM(M) will expand the input M to a larger pure diagonal matrix by stacking the element of M in a column-wise order. We demonstrate the above operations with examples in App. [A.](#page-18-7) Note that results in this paper may involve the expectation E[·] of some quantities, we assume the use of an [EMA](#page-18-3) as its practical estimation.

#### 2.2 Fisher information and natural gradient descent

Fisher information is a fundamental concept in statistics that measures the amount of information a random variable carries about a parameter of interest. In this paper, we ignore dependence between layers and treat each layer independently. Under the context of LLMs, with the vectorized minibatched gradient of one layer ⃗g, we define the empirical [FIM](#page-18-0) for that layer as F = E[⃗g⃗g T ]. [Natural](#page-18-8) [gradient descent \(NGD\)](#page-18-8) leverages the inverse of [FIM](#page-18-0) to smooth the local geometry to improve convergence and stabilize training [\[Martens, 2020\]](#page-16-9). In practice, the square-root inverse of [FIM](#page-18-0) may be preferred due to its properties and improved performance on certain optimization problems [\[Bergstra and Bengio, 2012,](#page-14-3) [Choi, 2019,](#page-14-4) [Lin et al., 2024,](#page-15-5) [Loshchilov and Hutter, 2016,](#page-15-6) [Yang and](#page-16-10) [Laaksonen, 2008\]](#page-16-10). The corresponding update of W is:

<span id="page-2-0"></span>
$$
\mathbf{W} \leftarrow \mathbf{W} - \lambda \operatorname{Mat}(\mathbf{F}^{-\frac{1}{2}} \nabla_{\theta} \mathcal{L}). \tag{1}
$$

Due to the large size of F ∈ R mn×mn, computing its inverse is a significant impediment to applying this update rule in practice. One way to address this is to enforce certain structures to approximate [FIM.](#page-18-0) In this paper, we consider two main classes of structures: block diagonal and Kronecker product matrices. They possess favorable properties that can significantly reduce computational complexity. App. [B.2](#page-19-0) provides a brief introduction and summary of their key properties. We also include a comprehensive background in App. [B](#page-18-9) to be more self-contained.

# 3 Structural Approximation to [FIM](#page-18-0)

The structured [FIM](#page-18-0) approximation framework consists of three steps: first, choose a structure to approximate [FIM](#page-18-0) F˜; second, find a solution for the approximation by minimizing the following objective:

<span id="page-2-1"></span>
$$
\min_{\tilde{F}\in\mathcal{H}} \|\tilde{F} - F\|_F^2,\tag{2}
$$

where F is the empirical [FIM,](#page-18-0) H is the matrix family corresponding to the structural assumption; third, derive the square-root [NGD](#page-18-8) update Eq. [\(1\)](#page-2-0) with approximated F˜. In this section, we show that many existing optimizers and gradient operators can be reformulated within this framework by <span id="page-3-5"></span>varying structural assumptions, thereby establishing connections between the choice of structure and optimizers.

#### <span id="page-3-0"></span>3.1 Adam: purely diagonal structure

There have been many work arguing that Adam's second moment aims to approximate the diagonal of [FIM](#page-18-0) [\[Hwang, 2024,](#page-15-7) [Kingma, 2014,](#page-15-8) [Sun and Spall, 2021\]](#page-16-11). Although it is easy to prove that this is, in fact, optimal approximation under Eq. [\(2\)](#page-2-1), we include the following proposition for completeness.

Proposition 1 (diagonal approximation). *Assuming* H = {Diagv(v); v<sup>i</sup> > 0}*, then Eq.* [\(2\)](#page-2-1) *has analytic solution*

<span id="page-3-6"></span>
$$
\tilde{F}^* = \text{Diag}_{\mathbf{v}}(\mathbb{E}[\vec{g}^2])
$$
\n(3)

*where* ⃗g 2 *indicates the element-wise square of* ⃗g = Vec(G)*.*

It is trivial to show the resulting square-root [NGD](#page-18-8) recovers Adam's second moment when using the [EMA](#page-18-3) to estimate E. Together with the first moment, one can recover Adam.

#### <span id="page-3-1"></span>3.2 Shampoo: Kronecker product structure

Although previous work [\[Morwani et al., 2024\]](#page-16-12) has demonstrated the connection of Shampoo [\[Gupta](#page-15-1) [et al., 2018\]](#page-15-1) to the Kronecker product approximation to [FIM](#page-18-0) through power iteration algorithm, we will make its connection to Eq. [\(2\)](#page-2-1) more explicit and provide an alternative view: Shampoo's preconditioner can be derived by minimizing an upper bound of Eq. [\(2\)](#page-2-1) with this structural assumption:

$$
\mathcal{H}=\{\boldsymbol{R}_{n}^{\frac{1}{2}}\otimes\boldsymbol{L}_{m}^{\frac{1}{2}}; \boldsymbol{R}_{n}\in\mathbb{R}^{n\times n},\boldsymbol{L}_{m}\in\mathbb{R}^{m\times m}\}
$$

where R<sup>n</sup> and L<sup>m</sup> are [symmetric positive definite \(SPD\)](#page-18-10) matrices.

Theorem 3.1 (Shampoo pre-conditioner). *Assume the above structural assumption, then we have an upper bound of Eq.* [\(2\)](#page-2-1)

$$
\begin{aligned} \|\tilde{F} - F\|_{F}^{2} &\leq 3(mn \|A^{2} - C^{2}\|_{F} \|B^{2} - C^{2}\|_{F} \\ &+ \sqrt{mn} \|C\|_{F}^{2} (\|A^{2} - C^{2}\|_{F} + \|B^{2} - C^{2}\|_{F})) \end{aligned} \tag{4}
$$

*where* A = R 1 2 <sup>n</sup> ⊗ Im*,* B = I<sup>n</sup> ⊗ L 1 <sup>2</sup>m*,* C = E[⃗g⃗g T ] 1 <sup>2</sup> *. Minimizing the upper-bound admits*

<span id="page-3-4"></span>
$$
\boldsymbol{R}_n^* = \frac{1}{m}\mathbb{E}[\boldsymbol{G}^T\boldsymbol{G}], \quad \boldsymbol{L}_m^* = \frac{1}{n}\mathbb{E}[\boldsymbol{G}\boldsymbol{G}^T]
$$

App. [C.1](#page-25-0) shows that the corresponding square-root [NGD](#page-18-8) leads to the Shampoo's update formula. Therefore, the structure behind Shampoo is the Kronecker product of two square-root [SPD](#page-18-10) matrices.

#### <span id="page-3-3"></span>3.3 Normalization and Whitening: Simple block diagonal structures

For an input G, the whitening and normalization operator are defined as

Whitening
$$
(G) = (GG^T)^{-\frac{1}{2}}G
$$
  
Norm $(G) = GS^{-\frac{1}{2}}$ 

where (·) − <sup>1</sup> <sup>2</sup> denotes square root inverse, and Diag(S) contains the squared column l<sup>2</sup> norm of G. Next we provide an new interpretation of these operators and show that they are the square-root [NGD](#page-18-8) updates under the following structural assumptions:

$$
\mathcal{H} = \{I_n \otimes M\} \quad \text{(Whitening)}^* \tag{5}
$$

$$
\mathcal{H} = \{ \mathbf{S} \otimes \mathbf{I}_m; S_{ii} > 0, \forall i \} \quad \text{(Normalization)} \tag{6}
$$

where M ∈ R <sup>m</sup>×<sup>m</sup> is [SPD](#page-18-10) and S ∈ R <sup>n</sup>×<sup>n</sup> is a positive diagonal matrix. Given those structural assumptions, one can show:

<span id="page-3-2"></span><sup>\*</sup>Note that this structure has also been proposed and discussed [Duvvuri et al.](#page-14-5) under a slightly different setting.

<span id="page-4-7"></span>Proposition 2 (Normalization and whitening). *Assuming* H = {I<sup>n</sup> ⊗M}*, minimizing Eq.* [\(2\)](#page-2-1) *admits*

<span id="page-4-2"></span><span id="page-4-1"></span>
$$
M^* = \frac{1}{n} \mathbb{E}[GG^T] \tag{7}
$$

*If one assumes* H = {S ⊗ Im; Sii > 0, ∀i}*, then the corresponding solution is*

$$
\boldsymbol{S}^* = \frac{1}{m} \mathbb{E}[\text{Diag}_{\mathbf{v}}(\boldsymbol{g}_1^T \boldsymbol{g}_1, \dots, \boldsymbol{g}_n^T \boldsymbol{g}_n)] \tag{8}
$$

The proof can be found in App. [D.3,](#page-30-0) where we prove a much more general solution (Theorem [D.1\)](#page-30-1), and Proposition [2](#page-4-1) is a special case. The corresponding square-root [NGD](#page-18-8) update with Eq. [\(7\)](#page-4-2) is Mat(F˜<sup>−</sup> <sup>1</sup> <sup>2</sup> ⃗g) = <sup>√</sup> nE[GG<sup>T</sup> ] − <sup>1</sup> <sup>2</sup> G (refer to App. [C.2\)](#page-25-1). Therefore, we can view Whitening(·) as a special case with one-sample estimate for E. Similarly, normalization is the square-root [NGD](#page-18-8) update (Mat(F˜<sup>−</sup> <sup>1</sup> <sup>2</sup> ⃗g) = <sup>√</sup> mGS∗− <sup>1</sup> <sup>2</sup> ) with Eq. [\(8\)](#page-4-1) and one-sample estimate of E.

Many recently proposed optimizers, such as Muon, SWAN, LARS and LAMB [\[Jordan et al., 2024,](#page-15-2) [Ma et al., 2024,](#page-16-1) [You et al., 2017,](#page-16-13) [2019\]](#page-16-6), rely on normalization and/or whitening. These gradient operators improve convergence [\[Jordan et al., 2024,](#page-15-2) [You et al., 2017\]](#page-16-13) and can replace Adam's internal states [\[Ma et al., 2024\]](#page-16-1). See App. [E.5](#page-38-0) for a detailed discussion.

#### <span id="page-4-0"></span>3.4 [Eigen-Adam:](#page-18-5) Generalization to Adam with eigenspace rotation

All structures considered above are simple and do not strictly generalize Adam's purely diagonal structure. In this and the following sections, we consider two structures that strictly generalize Adam, normalization, and whitening. Here, we first consider a block diagonal matrix with a shared eigen-space.

Precisely, we propose the following structure that generalizes Adam[\\*](#page-4-3) :

$$
\mathcal{H} = {\text{Diag}}_{\text{B}}(M_1, \dots, M_n); M_i = U_f D_i U_f^T \}
$$
\n(9)

where U<sup>f</sup> defines a shared full-rank eigen-space, and D<sup>i</sup> is a positive eigenvalue matrix. Adam is a special case by constraining U<sup>f</sup> = I. Additionally, the structures in Sec. [3.3](#page-3-3) are also special cases. Whitening is obtained by a shared D (i.e. D<sup>i</sup> = D); and normalization is by U<sup>f</sup> = I, D<sup>i</sup> = siI. However, this structure does not directly lead to an analytic solution for Eq. [\(2\)](#page-2-1). Instead, we propose to approximate the solution by solving 1-iteration alternating optimization:

Theorem 3.2 (1-iteration refinement). *For the structure in Eq.* [\(9\)](#page-4-4)*, we consider the following 1 iteration alternating optimization of objective [\(2\)](#page-2-1): (i) constrain* D<sup>i</sup> = D *to be equal, and solve* U<sup>∗</sup> <sup>f</sup> = arg minU<sup>f</sup> ,<sup>D</sup> ∥ DiagB(UfD1U<sup>T</sup> f , . . . , UfDnU<sup>T</sup> f ) − F∥ 2 F *; (ii) fix the* U<sup>∗</sup> f *and find* {D<sup>∗</sup> i } = arg min{Di} ∥ DiagB(U<sup>∗</sup> <sup>f</sup> D1U<sup>∗</sup> f T , . . . , U<sup>∗</sup> <sup>f</sup> DnU<sup>∗</sup> f T ) − F∥ 2 F *. Then, (i) and (ii) admits the following analytic solution:*

<span id="page-4-4"></span>
$$
U_f^* = \text{EVD}(\mathbb{E}[GG^T]). \tag{10}
$$

*where* EVD *is the eigenvalue decomposition; and:*

<span id="page-4-5"></span>
$$
\tilde{\boldsymbol{D}}^* = \text{Diag}_{\mathcal{M}}(\mathbb{E}[(\boldsymbol{U_f}^* \boldsymbol{G})^{\odot 2}])
$$
\n(11)

*where* D˜ <sup>∗</sup> = DiagB(D<sup>∗</sup> 1 , . . . , D<sup>∗</sup> n )*.*

Based on this result, we can derive the corresponding square-root [NGD](#page-18-8) with given U (refer to App. [C.3\)](#page-26-0):

<span id="page-4-6"></span>
$$
Mat(\tilde{\boldsymbol{F}}^{-\frac{1}{2}}\vec{\boldsymbol{g}}) = \boldsymbol{U}_f \frac{\boldsymbol{U}_f^T \boldsymbol{G}}{\sqrt{\mathbb{E}[(\boldsymbol{U}_f^T \boldsymbol{G})^{\odot 2}]}}.
$$
(12)

<span id="page-4-3"></span><sup>\*</sup> In App. [E.4,](#page-38-1) we propose an even more general block diagonal structure.

<span id="page-5-1"></span>This can be viewed as applying Adam's update on a space "rotated" by eigen-matrix U<sup>f</sup> . Consequently, we propose an optimizer, called [Eigen-Adam,](#page-18-5) with the following update procedures:

<span id="page-5-2"></span>
$$
\boldsymbol{m}_t = \beta_1 \boldsymbol{m}_{t-1} + (1 - \beta_1) \boldsymbol{G}_t \quad \text{(first moment)}
$$
\n
$$
\boldsymbol{Q}_t = \beta_3 \boldsymbol{Q}_{t-1} + (1 - \beta_3) \boldsymbol{G}_t \boldsymbol{G}_t^T \quad \text{(EMA for } \mathbb{E}[\boldsymbol{G}_t \boldsymbol{G}_t^T])
$$
\n
$$
\boldsymbol{U}_{f,t} = \text{EVD}(\boldsymbol{Q}_t)
$$
\n
$$
\boldsymbol{v}_t = \beta_2 \boldsymbol{v}_{t-1} + (1 - \beta_2) (\boldsymbol{U}_{f,t}^T \boldsymbol{G}_t)^{\odot 2} \quad \text{(second moment)}
$$
\n
$$
\Delta_t = \boldsymbol{U}_{f,t} \frac{\boldsymbol{U}_{f,t}^T \boldsymbol{m}_t}{\sqrt{\boldsymbol{v}_t}}
$$
\n(13)

Algorithm [7](#page-22-0) in App. [B.6](#page-21-0) summarizes the practical procedure. In fact, the above procedures closely relates to two related works: AdaDiag and one-sided SOAP [\[Anonymous, 2024,](#page-14-2) [Vyas et al., 2024\]](#page-16-0), which are heuristic memory-efficient variants of the full algorithms (i.e. AdaDiag++ and SOAP). Before we discuss their connections, next we first show that the SOAP optimizer can also be reformulated as FIM approximation under a specific structural assumption.

#### <span id="page-5-0"></span>3.5 SOAP: Combination of Kronecker product with block diagonal structure

All previous structures, apart from the one behind Shampoo, are under the class of block diagonal structures. However, such block-diagonal structure does not takes into account the off-diagonal part of [FIM.](#page-18-0) Structure under Kronecker product, like the one behind Shampoo, can go beyond this. Therefore, we can consider combining the structure of [Eigen-Adam](#page-18-5) with Shampoo, to obtain a more general structural assumption. We show this exactly recovers SOAP [\[Vyas et al., 2024\]](#page-16-0).

Specifically, we consider the following structural assumption:

$$
\mathcal{H} = \{ (\boldsymbol{U}_R \otimes \boldsymbol{U}_L) \tilde{\boldsymbol{D}} (\boldsymbol{U}_R \otimes \boldsymbol{U}_L)^T \} \tag{14}
$$

where U<sup>R</sup> ∈ R <sup>n</sup>×<sup>n</sup>, U<sup>L</sup> ∈ R <sup>m</sup>×<sup>m</sup> are orthonormal matrix, and D˜ ∈ R mn×mn is a diagonal matrix with positive values. We can easily show that structure behind [Eigen-Adam](#page-18-5) is a special case by constraining U<sup>R</sup> = In; and Shampoo is also a special case by constraining D˜ to be decomposed by Kronecker product (refer to App. [E.1\)](#page-36-0).

<span id="page-5-3"></span>Similar to [Eigen-Adam,](#page-18-5) it is hard to directly minimizing Eq. [\(2\)](#page-2-1) with this assumption. We can approximate the solution by a similar 1-iteration alternating optimization procedure as [Eigen-Adam.](#page-18-5) Theorem 3.3 (SOAP as 1-iteration alternating optimization of Eq. [\(2\)](#page-2-1)). *Assuming the above structural assumptions. Consider the following 1-iteration aternating optimization of Eq.* [\(2\)](#page-2-1)*: (i) assuming* D˜ *can be decomposed as Kronecker product of two diagonal matrix, then solve for* U<sup>∗</sup> <sup>R</sup>*,* U<sup>∗</sup> <sup>L</sup> = arg minUR,UL,D˜ <sup>∥</sup>(U<sup>R</sup> <sup>⊗</sup> <sup>U</sup>L)D˜ (U<sup>R</sup> <sup>⊗</sup> <sup>U</sup>L) <sup>T</sup> − F∥ 2 F *; (ii) fix* U<sup>∗</sup> <sup>R</sup>*,* U<sup>∗</sup> L *, solve for* <sup>D</sup>˜ <sup>∗</sup> = arg minD˜ <sup>∥</sup>(U<sup>∗</sup> <sup>R</sup> ⊗ U<sup>∗</sup> L )D˜ (U<sup>∗</sup> <sup>R</sup> ⊗ U<sup>∗</sup> L ) <sup>T</sup> − F∥ 2 <sup>F</sup> *without Kronecker product assumption of* <sup>D</sup>˜ *. Then, (i) admits analytic solution when minimizing the upper bound of Eq.* [\(2\)](#page-2-1) *(i.e. Eq.* [\(4\)](#page-3-4)*):*

$$
\boldsymbol{U}_{R}^{*}=\mathrm{EVD}(\mathbb{E}[\boldsymbol{G}^{T}\boldsymbol{G}]),\ \ \boldsymbol{U}_{L}^{*}=\mathrm{EVD}(\mathbb{E}[\boldsymbol{G}\boldsymbol{G}^{T}]).
$$

*Step (2) admits an analytic solution for Eq.* [\(2\)](#page-2-1)*:*

*.*

$$
\tilde{\bm{D^*}} = \text{Diag}_{\mathrm{M}}(\mathbb{E}[(\bm{U_L^*}^T\bm{G}\bm{U_R}^*)^{\odot 2}])
$$

The proof is a straightforward combination of Theorem [3.1](#page-3-4) and Theorem [3.2,](#page-4-5) and can be found in App. [D.7.](#page-35-0) One can show that the corresponding square-root [NGD](#page-18-8) update associated with the above result exactly recovers the update rules in SOAP optimizer (refer to App. [C.4](#page-26-1) for details).

Connections to [Eigen-Adam](#page-18-5) Compared to [Eigen-Adam,](#page-18-5) SOAP follows a more general structural assumption. However, from the FIM approximation perspective, SOAP does not exactly solve the 1-iteration alternating optimization problem. Instead, when solving for U<sup>∗</sup> <sup>R</sup>, U<sup>∗</sup> <sup>L</sup> = arg min<sup>U</sup>R,UL,D˜ <sup>∥</sup>(U<sup>R</sup> <sup>⊗</sup> <sup>U</sup>L)D˜ (U<sup>R</sup> <sup>⊗</sup> <sup>U</sup>L) <sup>T</sup> − F∥ 2 F , SOAP minimizes the upper bound instead. On the contrary, [Eigen-Adam](#page-18-5) exactly solves the 1-iteration refinement problem. In addition, the structures behind [Eigen-Adam](#page-18-5) and SOAP are different, and [Eigen-Adam](#page-18-5) should not be viewed as a simple variant of SOAP.

# <span id="page-6-4"></span><span id="page-6-0"></span>4 [RACS:](#page-18-1) memory-efficient optimizer from a carefully selected structure

The structured [FIM](#page-18-0) approximation reveals two important insights: there exists a correspondence between structural assumption and optimizers, and structural generality often comes at the cost of practical efficiency. For example, while the structures of [Eigen-Adam](#page-18-5) and SOAP offer more accurate [FIM](#page-18-0) approximations than a simple structure like gradient normalization, they require expensive computation and memory consumption (Table [1\)](#page-2-2), making them impractical for training LLMs. Building on this, our first design recommendation is to select structures that balance generality and practical efficiency.

To demonstrate this, we select a structure that generalizes gradient normalization, which scales both the rows and columns simultaneously:

<span id="page-6-2"></span><span id="page-6-1"></span>
$$
\mathcal{H} = \{ \mathbf{S} \otimes \mathbf{Q} \} \tag{15}
$$

where S ∈ R <sup>n</sup>×<sup>n</sup>, Q ∈ R <sup>m</sup>×<sup>m</sup> are positive diagonal matrices. The idea of diagonal approximation has also been leveraged in previous work under different setups [\[Li, 2018,](#page-15-9) [Shazeer and Stern, 2018,](#page-16-14) [Zhao et al., 2024b\]](#page-17-1). The optimal solution of Eq. [\(2\)](#page-2-1) can be solved by a fixed-point iterative procedure: Proposition 3 (Two-sided scaling). *Assuming the structure of Eq.* [\(15\)](#page-6-1)*, and* E[G⊙<sup>2</sup> ] *contains only positive values, solving Eq.* [\(2\)](#page-2-1) *admits an iterative fixed point procedure:*

$$
s = \frac{\text{Diag}\left(\mathbb{E}[\boldsymbol{G}^T\boldsymbol{Q}\boldsymbol{G}]\right)}{\|\boldsymbol{Q}\|_F^2}, \quad \boldsymbol{q} = \frac{\text{Diag}\left(\mathbb{E}[\boldsymbol{G}\boldsymbol{S}\boldsymbol{G}^T]\right)}{\|\boldsymbol{S}\|_F^2}.
$$
 (16)

*where* s = Diag(S)*,* q = Diag(Q)*. Additionally, the fixed point solution* s*,* q *converges to the right and left principal singular vector of* E[G<sup>⊙</sup><sup>2</sup> ] *up to a scaling factor with unique* S <sup>∗</sup> ⊗ Q<sup>∗</sup> *.*

In practice, we find initializing q = 1 and use 1-sample estimate of E[·] gives good performance. Interestingly, [Morwani et al.](#page-16-12) [\[2024\]](#page-16-12) also connects Shampoo to 1-step power iteration. Here, the Eq. [\(16\)](#page-6-2) can also be viewed as a power iteration algorithm. The main difference is that [Morwani et al.](#page-16-12) [\[2024\]](#page-16-12) assumes full [SPD](#page-18-10) matrix S and Q, but our structural constraint is positive diagonal matrix. Consequently, our procedure is computationally efficient and allows for multiple iterations.

The corresponding square-root [NGD](#page-18-8) update scales both rows and columns through S and Q (i.e. Mat(F˜<sup>−</sup> <sup>1</sup> <sup>2</sup> ⃗g) = Q<sup>−</sup> <sup>1</sup> <sup>2</sup> GS<sup>−</sup> <sup>1</sup> <sup>2</sup> ). We name this optimizer, [Row and Column Scaled SGD \(RACS\)](#page-18-1) (Algorithm [1\)](#page-6-3). Although analytic solutions of s, q exist, we perform 5 steps of Eq. [\(16\)](#page-6-2) as an efficient approximation. To further stabilize training, we also incorporate the norm-growth limiter used in [Chen et al.](#page-14-1) [\[2024a\]](#page-14-1). [RACS](#page-18-1) is highly memory efficient since it only needs the storage of two diagonal matrices S and Q and a scalar for the limiter, consuming m + n + 1 memory. In App. [E.5](#page-38-0) we discuss connections to Adapprox, Apollo and Adafactor [\[Shazeer and Stern, 2018,](#page-16-14) [Zhao et al., 2024b,](#page-17-1) [Zhu](#page-17-0) [et al., 2024\]](#page-17-0).

#### Algorithm 1 [RACS](#page-18-1)

<span id="page-6-3"></span>1: Input: learning rate λ, β, scale α, limiter threshold γ, optimization steps T. 2: s<sup>0</sup> = 0; q<sup>0</sup> = 0; ϕ<sup>0</sup> = 0 3: for t = 1, . . . , T do 4: G<sup>t</sup> = ∇<sup>W</sup>tL 5: Obtain S<sup>t</sup> and Q<sup>t</sup> by Eq. [\(16\)](#page-6-2) 6: s<sup>t</sup> = βst−<sup>1</sup> + (1 − β) Diag(St); 7: q<sup>t</sup> = βqt−<sup>1</sup> + (1 − β) Diag(Qt) 8: G˜ <sup>t</sup> = Diagv(qt) − <sup>1</sup> <sup>2</sup> G Diagv(st) − <sup>1</sup> 2 9: η = γ/ max{ ∥G˜t∥ ϕt−<sup>1</sup> , γ} if t > 1 else 1 10: ϕ<sup>t</sup> = η∥G˜ t∥ 11: Wt+1 = W<sup>t</sup> − ληαG˜ t 12: end for

This design recommendation has its limitations. Finding such a structure with a balanced tradeoff may not always be easy, and the resulting structure tends to be simple, offering less accurate approximation to [FIM](#page-18-0) compared to the general ones. Since the main bottleneck of more general

<span id="page-7-1"></span>optimizers is their practical efficiency, our second design recommendation is to: improve their efficiency by converting full-rank optimizers into low-rank counterparts using a novel low-rank extension framework.

# 5 [Alice:](#page-18-2) memory-efficient optimizer from low-rank extension framework

In this section, we propose a novel low-rank framework consisting of three steps, low-rank tracking, subspace switching; and compensation. Tracking aims to reduce the memory cost of [EMA](#page-18-3) states, whereas switching and compensation are designed to correct the potential issues caused by tracking and the limitations of low-rank projections. We demonstrate this procedure by converting [Eigen-](#page-18-5)[Adam](#page-18-5) to its low-rank version, [Alice.](#page-18-2) While the procedure could be applied to SOAP in a similar manner, we leave this for future work.

Reduce computational cost To improve the computational efficiency, we make two modifications to [Eigen-Adam.](#page-18-5) First, we propose to use 1-step subspace iteration algorithm as an efficient scheme to find leading eigenvectors (Algorithm [10](#page-25-2) in App. [B\)](#page-18-9). Second, we only update projection U every K steps, effectively partitioning the training into time blocks with size K, and amortizing the cost. Consequently, U is fixed within a time block.

#### 5.1 Tracking: low-rank projections to reduce memory

By carefully examining the [Eigen-Adam'](#page-18-5)s procedure (Eq. [\(12\)](#page-4-6)), we notice all internal states are connected through the projection Uf,t. To reduce the memory cost, we can obtain a low-rank U<sup>t</sup> by keeping only the top r eigenvectors, and denote the remaining m − r basis as Uc,t (i.e. Uf,t = [Ut, Uc,t]). For tracking state Qt, we can also apply low-rank approximation and only track the projected states. We call it low-rank tracking:

<span id="page-7-0"></span>
$$
\boldsymbol{\sigma}_t = \boldsymbol{U}_t^T \boldsymbol{G}_t; \quad \widetilde{\boldsymbol{Q}}_{t+1} = \beta_3 \widetilde{\boldsymbol{Q}}_t + (1 - \beta_3) \boldsymbol{\sigma}_t \boldsymbol{\sigma}_t^T
$$
\n(17)

where <sup>σ</sup><sup>t</sup> is the projected gradient, and <sup>Q</sup>e<sup>t</sup> is the low-rank tracking state. One can easily reconstruct back <sup>Q</sup><sup>t</sup> <sup>≈</sup> <sup>U</sup>tQetU<sup>T</sup> <sup>t</sup> when needed. This reduces the memory from m<sup>2</sup> to r 2 .

However, this low-rank projection comes with two major consequences: (1) the reconstructed state Q<sup>t</sup> is no longer accurate; (2) the resulting parameter update ∆ in Eq. [\(12\)](#page-4-6) ignores the information within Uc,t due to low-rank Ut. Next, we propose two additional steps, switching and compensation, rooted in theoretical insights to address these two problems, respectively.

#### 5.2 Switching: mixing leading basis with the complements

We omit the subscript t in U and U<sup>c</sup> in the following since they are fixed within a time block. Since the projected gradient σ<sup>t</sup> only maintains the information in the space spanned by U, the low-rank tracking state <sup>Q</sup>e<sup>t</sup> necessarily discards information in <sup>U</sup>c. Therefore, even if those directions should become the leading basis at the time we update the <sup>U</sup>, <sup>Q</sup>e<sup>t</sup> will ignore their contributions, causing the stability of the previous leading eigenvectors and preventing the exploration of other spaces. We prove that this is possible by showing that the true tracking state Q<sup>t</sup> can be decomposed into low-rank tracking reconstruction and a residual term quantifying the importance of Uc:

Proposition 4 (Subspace switching). *Assuming the setup mentioned above and all assumptions of [Eigen-Adam](#page-18-5) are satisfied. We further assume the low-rank* U ∈ R m×r *is obtained at the beginning of* i + 1 *time block by* EVD(Q<sup>∗</sup> ik, r) *where* Q<sup>∗</sup> ik *is the true tracking state. Further, we assume the stability of the eigen-basis such that gradient* G<sup>t</sup> *during* i + 1 *time block shares the same eigen-basis as* Q<sup>∗</sup> ik*. Then, the true tracking state at the end of* i + 1 *block,* Q<sup>∗</sup> (i+1)k *, can be decomposed into:*

<span id="page-7-2"></span>
$$
\mathbf{Q}_{(i+1)k}^{*} = \sum_{t=i k+1}^{(i+1)k} \mathbf{G}_{t} \mathbf{G}_{t}^{T} = \sum_{t=i k+1}^{(i+1)k} \tilde{\mathbf{G}}_{t} \tilde{\mathbf{G}}_{t}^{T} + \mathbf{U}_{c} \Sigma_{t} \mathbf{U}_{c}^{T}
$$
(18)

*where* <sup>G</sup>e<sup>t</sup> <sup>=</sup> Uσ<sup>t</sup> *is the low rank reconstructed gradients,* <sup>Σ</sup><sup>t</sup> <sup>∈</sup> <sup>R</sup> (m−r)×(m−r) *is a diagonal matrix with positive values, and* U<sup>c</sup> *is the remaining eigen-basis such that* [U, Uc] *will form the complete eigen-basis of* Q<sup>∗</sup> ik*.*

<span id="page-8-2"></span>When some entries in Σ<sup>t</sup> become dominant, the corresponding basis in U<sup>c</sup> will form the new leading eigen-basis when updating the projection U through EVD(Q<sup>∗</sup> (i+1)k ). On the other hand, if U is updated with low-rank reconstructed state alone, it is equivalent to setting Σ<sup>t</sup> = 0, ignoring the contributions of Uc, and resulting in the stability of the previous leading basis. Inspired by this insight, we propose a practical scheme to update U, instead of relying on [EVD](#page-18-6) of low-rank reconstructed state. We call it subspace switching (Algorithm [2\)](#page-8-0). Intuitively, we force the new projection U to mix the leading eigen-basis with randomly sampled eigenvectors from the remaining basis Uc, allowing the optimizer to explore other spaces. Although the true U<sup>c</sup> is hard to obtain in practice, we propose to approximate it by the QR decomposition of U.

Algorithm 2 Subspace switching

- <span id="page-8-0"></span>1: Input: Reconstructed state Q, rank r, leading basis number l, previous low-rank projection Ut−<sup>1</sup>
- 2: U′ <sup>t</sup> = Subspace iteration(Q, Ut−1)
- 3: U′ t,<sup>1</sup> ← Keep top l eigenvectors of U′ t
- 4: Uniformly sample r − l basis from the complement U′ c,t = QR(U′ t ) as U′ t,2
- 5: Combine basis U = [U′ t,1 , U′ t,2 ]
- 6: Return U

#### <span id="page-8-4"></span>5.3 Compensation: convert low-rank update to be full-rank

Another problem with low-rank projection U is the information loss in the resulting parameter update ∆ at each step. The goal of compensation step is to compensate for this information loss with minimal memory overhead. Firstly, we need to know which information has been discarded. We show that the update ∆ with full-rank U<sup>f</sup> in Eq. [\(12\)](#page-4-6) can be decomposed into the low-rank update with U and complement update controlled by U<sup>c</sup> (proof in App. [E.6\)](#page-40-0):

$$
\Delta = \boldsymbol{U} \frac{\boldsymbol{U}^T \boldsymbol{G}}{\sqrt{\mathbb{E}[(\boldsymbol{U}^T \boldsymbol{G})^{\odot 2}]}} + \underbrace{\boldsymbol{U}_c \frac{\boldsymbol{U}_c^T \boldsymbol{G}}{\sqrt{\mathbb{E}[(\boldsymbol{U}_c^T \boldsymbol{G})^{\odot 2}]}}}_{\text{Mat}(\tilde{\boldsymbol{F}}_c^{-\frac{1}{2}} \tilde{\boldsymbol{g}})} \tag{19}
$$

where F˜ <sup>c</sup> = DiagB(UcDc,1U<sup>T</sup> c , . . . , UcDc,nU<sup>T</sup> c ) is the approximated [FIM](#page-18-0) corresponding to the complement basis Uc, Dc,i = Diagv(E[(U<sup>T</sup> <sup>c</sup> gi) 2 ]) and <sup>−</sup> <sup>1</sup> <sup>2</sup> is the square-root pseudo-inverse.

<span id="page-8-5"></span><span id="page-8-1"></span>1

We notice that the discarded information, Mat(F˜ 2 <sup>c</sup> ⃗g), has the same format as the square-root [NGD](#page-18-8) with [FIM](#page-18-0) F˜ <sup>c</sup>. From the proposed [FIM](#page-18-0) view point, the design of compensation term becomes the selection of a structure to approximate F˜ <sup>c</sup>, and the application of the corresponding square-root [NGD.](#page-18-8) Considering the trade-off between structural generality and practical efficiency, one structural choice is the diagonal structure of normalization operator, which simply scales the columns of gradient matrix and is highly memory efficient. In addition, we only want to focus on the discarded information UcU<sup>T</sup> <sup>c</sup> G for compensation, rather than the entire gradient G. We propose the following compensation at each step t:

$$
C_t = \text{Mat}((S \otimes U_c U_c^T) \vec{g}_t) = U_c U_c^T G_t S \tag{20}
$$

where S is a positive diagonal matrix, UcU<sup>T</sup> <sup>c</sup> G = (G − UU<sup>T</sup> G) is the gradient information within the remaining basis. We show that such design choice admits an optimal solution of S to the [FIM](#page-18-0) approximation problem.

Theorem 5.1 (Optimal compensation). *Assume that the conditions of [Eigen-Adam](#page-18-5) are satisfied. With the proposed form of compensation (Eq.* [\(20\)](#page-8-1)*), minimizing [FIM](#page-18-0) reconstruction loss*

$$
\|(\boldsymbol{S}_t^{-2} \otimes \boldsymbol{U}_c \boldsymbol{U}_c^T) - \tilde{\boldsymbol{F}}_c \|_F^2
$$

*admits analytic solution:*

<span id="page-8-3"></span>
$$
\text{Diag}(\boldsymbol{S}_t) = \frac{\sqrt{m-r}}{\sqrt{\mathbb{E}[\boldsymbol{1}_m^T \boldsymbol{G}_t^{\odot 2} - \boldsymbol{1}_r^T (\boldsymbol{U}^T \boldsymbol{G}_t)^{\odot 2}]}}
$$
(21)

*where* 1<sup>m</sup> ∈ R <sup>m</sup>*,* 1<sup>r</sup> ∈ R <sup>r</sup> *are the column vectors with element* 1*.*

Algorithm [3](#page-9-1) summarizes the compensation step.

<span id="page-9-2"></span>Algorithm 3 Compensation

<span id="page-9-1"></span>1: Input: Gt, projection U, previous norm p, limiter norm ϕ, limiter threshold γ, decay rate β 2: p ← βp + (1 − β)(1 T mG⊙<sup>2</sup> <sup>t</sup> − 1 T r (U<sup>T</sup> Gt) ⊙2 ) 3: C<sup>t</sup> ← √ m − r(G<sup>t</sup> − UU<sup>T</sup> Gt) Diagv(p) − <sup>1</sup> 2 4: η = γ/ max{ ∥Ct∥ ϕ , γ} if ϕ > 0 else 1 5: ϕ = ∥ηCt∥ 6: C<sup>t</sup> ← ηC<sup>t</sup> 7: Return Ct, p, ϕ

#### <span id="page-9-0"></span>5.4 [Alice](#page-18-2) optimizer

By combining [Eigen-Adam](#page-18-5) with low-rank U, tracking, switching and compensation, we obtain [Alice,](#page-18-2) a novel low-rank optimizer. One can also design a simple variant, [Alice without tracking \(Alice-0\),](#page-18-11) by disabling the tracking for better memory efficiency.

Connections to GaLore Interestingly, GaLore, in fact, is an approximation to [Alice](#page-18-2) without tracking, switching and compensation. Based on the connection of [Alice](#page-18-2) to [Eigen-Adam,](#page-18-5) we reveal that GaLore is a simple low-rank extension of [Eigen-Adam,](#page-18-5) a more general optimizer than Adam. This also reflects the advantage of the [FIM](#page-18-0) view point, which provides a deeper understanding and an explanation on its better performance than Adam under certain scenarios [\[Zhao et al., 2024a\]](#page-16-5).

Algorithm 4 [Alice](#page-18-2)[/Alice-0](#page-18-11) optimizer

<span id="page-9-3"></span>1: Input: learning rate λ, scale α, compensation scale αc, update interval k, β1, β2, β<sup>3</sup> (β<sup>3</sup> = 0 for [Alice-0\)](#page-18-11), optimization step T, rank r, loss function L, limiter threshold γ, leading basis number l 2: <sup>Q</sup>e<sup>0</sup> = 0, <sup>U</sup><sup>0</sup> = 0, <sup>p</sup><sup>0</sup> = 0, <sup>ϕ</sup> = 0, <sup>m</sup><sup>0</sup> = 0, <sup>v</sup><sup>0</sup> = 0 3: for t = 1 . . . , T do 4: G<sup>t</sup> = ∇WtL 5: if t == 1 or (t mod K) == 0 then 6: <sup>Q</sup><sup>t</sup> <sup>=</sup> <sup>β</sup>3UtQet−1U<sup>T</sup> <sup>t</sup> + (1 − β3)GtG<sup>T</sup> t 7: U<sup>t</sup> = Switch(Qt, r, l, Ut−1) 8: else 9: U<sup>t</sup> = Ut−<sup>1</sup> 10: end if 11: σ<sup>t</sup> = U<sup>T</sup> <sup>t</sup> G<sup>t</sup> 12: <sup>Q</sup>e<sup>t</sup> <sup>=</sup> <sup>β</sup>3Qet−<sup>1</sup> + (1 <sup>−</sup> <sup>β</sup>3)σt<sup>σ</sup> T t 13: m<sup>t</sup> = β1mt−<sup>1</sup> + (1 − β1)σ<sup>t</sup> 14: v<sup>t</sup> = β2vt−<sup>1</sup> + (1 − β2)σ ⊙2 t 15: ω = <sup>√</sup>m<sup>t</sup> vt 16: ∆c, pt, ϕ<sup>t</sup> = Compensation(Gt, Ut, pt−1, ϕt−1, γ, β1) 17: Wt+1 = W<sup>t</sup> − λα(Uω + αc∆c) 18: end for

# 6 Related Work

Optimizer based on structural approximation Due to the desirable properties and convergence of second-order optimization, various work has been proposed to efficiently approximate Hessian-like matrix, e.g. [FIM.](#page-18-0) KFAC [\[Martens and Grosse, 2015\]](#page-16-15) was one of the first work that goes beyond the simple diagonal approximations, and approximate the layer-wise [FIM.](#page-18-0) Subsequent works extends KFAC beyond MLP layers [\[Grosse and Martens, 2016,](#page-15-10) [Martens et al., 2018\]](#page-16-16). Further refinements to KFAC are also proposed, including refinement of eigenvalues [\[George et al., 2018\]](#page-15-11), fixing the trace [\[Gao et al., 2021\]](#page-15-12), and refinement by Kronecker product singular value decomposition [\[Koroko](#page-15-13) [et al., 2022\]](#page-15-13). Our proposed view point is different from KFAC, where KFAC decompose the [FIM](#page-18-0) using the back-proped gradients and layer input. In addition, KFAC needs to be re-derived for different types of layers. On the other hand, our proposed view point is closer to another line of

<span id="page-10-0"></span>work, aiming to approximate the full AdaGrad [\[Duchi et al., 2011\]](#page-14-6). In particular, Shampoo [\[Anil](#page-14-7) [et al., 2020,](#page-14-7) [Gupta et al., 2018\]](#page-15-1) is proposed as a Kronecker product approximation to AdaGrad. Later, [\[Morwani et al., 2024\]](#page-16-12) explicitly proved that it is a 1-step power iteration to optimal Kronecker product approximation. In here, we propose an alternative view of Shampoo as minimizing a upper bound of the approximation error. SOAP [\[Vyas et al., 2024\]](#page-16-0) is a recently proposed adaptive optimizer that further improves Shampoo based on the insights from [George et al.](#page-15-11) [\[2018\]](#page-15-11). In this work, we make explicit connection of those approaches to [FIM](#page-18-0) approximation, and establish the equivalence of structural assumption to optimizers. We also additionally provide connections of gradient operators to [FIM](#page-18-0) approximation, and design new optimizers from this view point. We provide discussions of our approach to many existing optimizers, including Apollo [\[Zhu et al., 2024\]](#page-17-0), GaLore [\[Zhao et al.,](#page-16-5) [2024a\]](#page-16-5), Muon [\[Jordan et al., 2024\]](#page-15-2), SWAN [\[Ma et al., 2024\]](#page-16-1), Adapprox [\[Zhao et al., 2024b\]](#page-17-1), Lars [\[You et al., 2017\]](#page-16-13), Lamb [\[You et al., 2019\]](#page-16-6), Fira [\[Chen et al., 2024a\]](#page-14-1) and AdaDiag [\[Anonymous,](#page-14-2) [2024\]](#page-14-2), in App. [E.5.](#page-38-0) In addition to the above, preconditioning SGD (PSGD) [\[Li, 2017,](#page-15-14) [Pooladzandi](#page-16-17) [and Li, 2024\]](#page-16-17) aims to directly approximate the inverse Hessian or [FIM](#page-18-0) through different structural assumptions. [Li](#page-15-9) [\[2018\]](#page-15-9) also discussed the diagonal Kronecker product structure as in [RACS,](#page-18-1) but they apply this structural assumption under the framework of PSGD to directly approximate the inverse of [FIM](#page-18-0) through gradient descent.

Memory-efficient optimizer Practical efficiency is a crucial factor when training large models. In particular, there are many works that focus on optimizing memory efficiency, as less memory consumption allows larger batch size, effectively improving throughput. There are two main lines of research: (1) use low-rank approximation to reduce memory of optimizer internal states; (2) remove the internal states. GaLore [\[Zhao et al., 2024a\]](#page-16-5), a well-know low-rank optimizer, proposed to use [singular value decomposition \(SVD\)](#page-18-12) for a low-rank projection, followed by applying Adam within it. It can be seen as a special case of [Alice](#page-18-2) without tracking, switching and compensation. Fira [\[Chen et al., 2024a\]](#page-14-1), an extension to GaLore, adds compensation term to turn low-rank update to be full-rank, substantially improves the performance. Flora [\[Si et al., 2024\]](#page-16-4) used randomly sampled Gaussian matrix as the subspace to save compute and memory. However, it is mainly focused on the fine-tuning tasks. ReLora [\[Lialin et al., 2023\]](#page-15-4), an extension to LoRA [\[Hu et al., 2021\]](#page-15-3), periodically merges the LoRA weights to enable full-rank learning. On the other hand, many optimizers require fewer internal states compared to Adam. Lion [\[Chen et al., 2024b\]](#page-14-8) and Signum [\[Bernstein et al.,](#page-14-9) [2018\]](#page-14-9) only require the storage of the first moment, offering a balance between memory efficiency and performance. Apollo [\[Zhu et al., 2024\]](#page-17-0), a recently proposed approach, maintains a low-rank GaLore states (e.g. Apollo-mini uses rank 1) for estimating the scaling matrix for the raw gradient. Although it still requires GaLore states, using rank 1 allows it to achieve SGD-like memory. At the same time, [Ma et al.](#page-16-1) [\[2024\]](#page-16-1) developed SWAN, which manages to completely removes the internal states through two gradient operators: normalization and whitening, and obtains stronger performance than Adam. In this paper, we also show that normalization and whitening operators are special cases of [FIM](#page-18-0) approximation.

# <span id="page-10-1"></span>7 Experiments

We include all setup details along with additional experiment results in App. [F.](#page-40-1)

### 7.1 Pretraining LLaMA with C4 dataset

Setup We evaluate the proposed [RACS,](#page-18-1) [Alice](#page-18-2) and its variant [Alice-0](#page-18-11) on pre-training LLaMA [\[Touvron et al., 2023\]](#page-16-7) with the C4 dataset [\[Raffel et al., 2020\]](#page-16-8). We train the following model sizes: 60M, 130M, 350M and 1.3B using a similar setup as [Zhao et al.](#page-16-5) [\[2024a\]](#page-16-5), [Zhu et al.](#page-17-0) [\[2024\]](#page-17-0). For baselines, we consider GaLore, Fira, Apollo-mini, Apollo-svd and Adam. An important consideration in our experiments is that all previous low-rank methods rely on full-rank Adam to train the last layer, which is arguably one of the most important layers [\[Zhao et al., 2024c\]](#page-17-2). To thoroughly assess their effectiveness, we report performance for both cases when evaluating low-rank methods—training the last layer with and without Adam—but prioritize the latter as the main evaluation criterion. For full-rank methods (i.e. [RACS,](#page-18-1) Apollo-mini, Apolli-svd and Adam), we assume the last layer is trained by Adam.

<span id="page-11-0"></span>Table 2: LLaMA pretraining performance. Ppl. is the evaluation perplexity when the last layer is not trained by Adam; and Ppl.\* is when the last layer is trained by Adam. For Adam, we report both our reproduced performance and perplexity cited from [Zhu et al.](#page-17-0) [\[2024\]](#page-17-0). We also cite Ppl.\* of other baselines from [Zhu et al.](#page-17-0) [\[2024\]](#page-17-0). The speed-up is measured against Adam in terms of training steps. The TP is the number of training tokens processed per second, and effective TP is total token used by Adam divided by time used by the candidate optimizer to reach the same final eval ppl. of Adam.

| Methods                         | 60M          |              | 130M         |              | 350M         |              | 1.3B         |              |
|---------------------------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|
|                                 | Ppl.         | Ppl.*        | Ppl.         | Ppl.*        | Ppl.         | Ppl.*        | Ppl.         | Ppl.*        |
| Adam                            | NA           | 33.94        | NA           | 25.03        | NA           | 19.24        | NA           | 16.44        |
| Adam (cited)                    | NA           | 34.06        | NA           | 25.08        | NA           | 18.80        | NA           | 15.56        |
| GaLore                          | 38.91        | 34.88        | 27.18        | 25.36        | 21.11        | 18.95        | 16.60        | 15.64        |
| Fira                            | 33.77        | 31.06        | 25.21        | 22.73        | 18.93        | 17.03        | 15.14        | 14.31        |
| Apollo-mini                     | NA           | 31.93        | NA           | 23.84        | NA           | 17.18        | NA           | 14.17        |
| Apollo-svd                      | NA           | 31.26        | NA           | 22.84        | NA           | 16.67        | NA           | 14.10        |
| RACS                            | NA           | 30.25        | NA           | 22.67        | NA           | 16.51        | NA           | 13.52        |
| Alice-0                         | 28.83        | 29.74        | 21.99        | 22.43        | 16.66        | 16.43        | 13.97        | 13.47        |
| Alice                           | 28.69        | 29.33        | 21.95        | 21.79        | 16.61        | 16.37        | 13.85        | 13.52        |
| Speed-up in steps (Alice)       | 2.22x        |              | 2.00x        |              | 2.45x        |              | 2.82x        |              |
| Throughput(TP)/Effect TP (Adam) | 97748/97748  |              | 82247/82247  |              | 63139/63139  |              | 53588/53588  |              |
| Throughput(TP)/Effect TP(Alice) | 92589/202058 |              | 71583/141148 |              | 58847/143088 |              | 45523/123048 |              |
| Throughput(TP)/Effect TP (RACS) |              | 98238/162423 |              | 73233/123116 |              | 55970/131372 |              | 47488/129817 |

<span id="page-11-1"></span>Table 3: Memory consumption estimation. The reported memory is the combined consumption of: weight parameters; Adam optimizer states for non-matrix parameters; and candidate optimizer states for matrix parameters. Mem.\* represent the consumption when the last layer is trained by Adam.

| Methods     | 60M   |       | 130M  |       | 350M  |       | 1.3B  |       |
|-------------|-------|-------|-------|-------|-------|-------|-------|-------|
|             | Mem.  | Mem.* | Mem.  | Mem.* | Mem.  | Mem.* | Mem.  | Mem.* |
| Adam        | NA    | 0.32G | NA    | 0.75G | NA    | 2.05G | NA    | 7.48G |
| GaLore      | 0.21G | 0.26G | 0.51G | 0.57G | 1.2G  | 1.29G | 4.25G | 4.43G |
| Fira        | 0.21G | 0.26G | 0.51G | 0.57G | 1.2G  | 1.29G | 4.25G | 4.43G |
| Apollo-mini | NA    | 0.23G | NA    | 0.43G | NA    | 0.93G | NA    | 2.98G |
| Apollo-svd  | NA    | 0.26G | NA    | 0.57G | NA    | 1.29G | NA    | 4.43G |
| RACS        | NA    | 0.23G | NA    | 0.43G | NA    | 0.93G | NA    | 2.98G |
| Alice-0     | 0.21G | 0.26G | 0.51G | 0.57G | 1.2G  | 1.29G | 4.25G | 4.44G |
| Alice       | 0.22G | 0.26G | 0.53G | 0.59G | 1.24G | 1.33G | 4.42G | 4.6G  |

<span id="page-11-2"></span>Table 4: Eval ppl. of 1B v.s. 7B LLaMA at different training steps. For Apollo, Apollo-mini, 8-bit Adam and Galore, we cite the number from [Zhu et al.](#page-17-0) [\[2024\]](#page-17-0).

| Method            | Mem.   | 40K   | 80K   | 120K  | 150K  |
|-------------------|--------|-------|-------|-------|-------|
| 8-bit Adam (7B)   | 26G    | 18.09 | 15.47 | 14.83 | 14.61 |
| 8-bit Galore (7B) | 18G    | 17.94 | 15.39 | 14.95 | 14.65 |
| Apollo (7B)       | 15.03G | 17.55 | 14.39 | 13.23 | 13.02 |
| Apollo-mini (7B)  | 13.53G | 18.03 | 14.60 | 13.32 | 13.09 |
| RACS (1B)         | 2.98G  | 16.43 | 14.26 | 13.20 | 13.01 |
| Alice (1B)        | 4.6G   | 15.93 | 14.08 | 13.15 | 12.97 |

<span id="page-12-2"></span><span id="page-12-0"></span>![](./assets/structured-fisher-llm-optimizer/_page_12_Figure_0.jpeg)

Figure 1: 1B LLaMA C4 pretraining evaluation ppl. curve. "+lm head" represents the last layer is trained by full-rank Adam.

Main results Table [2](#page-11-0) reports the pretraining performance in terms of evaluation perplexity, and Table [3](#page-11-1) summarizes the corresponding estimated memory consumption. Our proposed [RACS](#page-18-1) and [Alice](#page-18-2) outperforms the other memory-efficient baselines and full-rank Adam consistently across various model sizes. [Alice](#page-18-2) and [Alice-0](#page-18-11) perform on par with each other, suggesting [Alice-0](#page-18-11) may be preferred for better memory efficiency. One major advantage of [Alice](#page-18-2) is its fast convergence compared to Adam, and achieves more than 2× speed-ups across model sizes, while maintaining similar memory consumption as GaLore. Fig. [1](#page-12-0) demonstrate this fast convergence of the evaluation perplexity during training for the 1B model. Despite the simplicity of [RACS,](#page-18-1) it performs well for 350M and 1.3B model, and surpasses the other scaling-based baseline, Apollo-mini and Apollo-svd, consistently. From the throughput (TP), we can observe [Alice](#page-18-2) and [RACS](#page-18-1) are not significantly slower than Adam with 15% and 11% drop for 1B model, respectively. Considering the speedup effect, we report the effective TP to represent how quickly the optimizers reach a target loss in wall-clock time. [Alice](#page-18-2) and [RACS](#page-18-1) achieve 123048 and 129817 with 1B model, respectively, compared to 53588 for Adam, resulting in more than 2× faster convergence in wall-clock time to reach Adam's final evaluation perplexity.

For Adam, since we cannot reproduce the exact number reported in [Zhu et al.](#page-17-0) [\[2024\]](#page-17-0). For fair comparison, we also cite the perplexities of Adam from [Zhu et al.](#page-17-0) [\[2024\]](#page-17-0), and compute the corresponding speed-ups in terms of steps. [Alice](#page-18-2) achieves 2.22x, 2.11x, 2.18x, and 2.15x for 60M, 130M, 350M and 1B models, respectively. For the actual memory footprints and additional training curves, see App. [F.6.](#page-42-0)

1B v.s. 7B LLaMA To further demonstrate the effectiveness, we follow the setup of [Zhu et al.](#page-17-0) [\[2024\]](#page-17-0), but train a 1B LLaMA with [Alice](#page-18-2) and [RACS](#page-18-1) to compare with 7B LLaMA trained by Apollo, Apollo-mini, 8-bit Adam and 8-bit Galore. Table [4](#page-11-2) shows that 1B model trained with our proposed optimizers consistently outperforms 7B model at different training checkpoints with less memory cost[\\*](#page-12-1) . To complete 150K steps with 8xA100 GPUs, Apollo requires 15 days while [Alice](#page-18-2) and [RACS](#page-18-1) require around 3.8 days.

### 7.2 Ablation: Effectiveness of the design choice

Effect of low-rank tracking First, we verify whether low-rank tracking (Eq. [\(17\)](#page-7-0)) is beneficial and whether our conjecture about the stability of the leading basis holds. As shown in Table [2,](#page-11-0) [Alice-0](#page-18-11) performs on par with [Alice,](#page-18-2) suggesting that tracking does not provide a significant boost. However, Fig. [5\(a\)](#page-45-0) indicates that tracking is helpful when compensation is disabled and must be used alongside switching. Without switching, tracking leads to inferior performance due to the stability of the eigenspace. Fig. [6](#page-46-0) supports this conjecture by showing the cosine similarity before and after updating U every 200 steps, confirming that tracking contributes to the stability of the leading basis.

<span id="page-12-1"></span><sup>\*</sup>The total memory cost consists of (1) model parameters; (2) Adam optimizer cost for non-matrix parameters; (3) candidate optimizer cost for matrix parameters. Here, we report the combined cost.

<span id="page-13-1"></span><span id="page-13-0"></span>Table 5: Effectiveness of each components in [Alice](#page-18-2) with 130M LLaMA.

| Components                   | Evaluation ppl. |
|------------------------------|-----------------|
| No tracking, switch, compen. | 26.96           |
| Tracking                     | 27.35           |
| Tracking+Switch              | 25.11           |
| Tracking+Switch+Compen.      | 21.95           |
|                              |                 |

Switching strategy We evaluate the effectiveness of our theory-inspired switching strategy compared to other heuristics. The considered alternatives are: (1) Gaussian: U is sampled from a Gaussian distribution; (2) Gaussian mix: the leading basis is mixed with vectors sampled from a Gaussian matrix; (3) full basis: instead of sampling the r − l basis in Algorithm [2](#page-8-0) solely from m − r complement basis, they are sampled jointly from the entire basis excluding the top l leading eigenvectors, i.e. [U, Uc]\U:,:<sup>l</sup> . As shown in Fig. [5\(b\),](#page-45-1) our strategy outperforms these alternatives, particularly the Gaussian-based approaches. One possible reason is that the orthogonality of the complement basis ensures a more effective switch, whereas randomly sampled Gaussian vectors may introduce overlaps between switches.

Compensation strategy The closest work to our compensation step is Fira [\[Chen et al., 2024a\]](#page-14-1), which introduces a heuristic-based compensation term. To evaluate the effectiveness of our optimal compensation, we compare it against Fira and a no-compensation baselines by integrating these alternatives into [Alice.](#page-18-2) Additionally, we introduce Fira+, our proposed modification that further enhances Fira's performance. As shown in Fig. [5\(c\),](#page-45-2) our optimal compensation achieves better performance and convergence than Fira-based compensations, with only a small additional sublinear memory cost (i.e., n). Compared to the no-compensation, all strategies yield noticeable performance improvements. Table [5](#page-13-0) summarizes the contributions of each component.

Other ablations We also performed additional ablations, examining (1) the effect of the last layer and (2) the effect of [EMA](#page-18-3) in [RACS.](#page-18-1) For more details, see App. [F.7.](#page-42-1)

# 8 Conclusion

In this paper, we take a step toward the systematic design of efficient optimizers for LLMs through structured [FIM](#page-18-0) approximation. We first establish the connection between structural assumptions and optimizers by solving the structured [FIM](#page-18-0) approximation. Building on this insight, we propose two design approaches: (1) Selecting a structure that balances generality and practical efficiency, then solving the [FIM](#page-18-0) approximation problem accordingly; (2) Using a general structure for [FIM](#page-18-0) approximation, followed by our proposed low-rank framework to improve efficiency. Following these principles, we develop two memory-efficient optimizers, [RACS](#page-18-1) and [Alice,](#page-18-2) each corresponds to one of these design approaches. Experimental validation on LLaMA pre-training demonstrates their effectiveness.

Our work lays the foundation for a more systematic approach to efficient optimizer design, opening up several promising directions for future research, including: developing low-rank counterparts for SOAP; exploring other possible classes of structures; and investigating approximation problems beyond [FIM.](#page-18-0) By providing a structured perspective on optimizer design, we hope to inspire further advancements in scalable and efficient training methods for LLMs.

# References

- <span id="page-14-7"></span>Rohan Anil, Vineet Gupta, Tomer Koren, Kevin Regan, and Yoram Singer. Scalable second order optimization for deep learning. arXiv preprint arXiv:2002.09018, 2020.
- <span id="page-14-2"></span>Anonymous. Improving adaptive moment optimization via preconditioner diagonalization. In Submitted to The Thirteenth International Conference on Learning Representations, 2024. URL <https://openreview.net/forum?id=NdNuKMEv9y>. under review.
- <span id="page-14-3"></span>James Bergstra and Yoshua Bengio. Random search for hyper-parameter optimization. Journal of machine learning research, 13(2), 2012.
- <span id="page-14-9"></span>Jeremy Bernstein, Yu-Xiang Wang, Kamyar Azizzadenesheli, and Animashree Anandkumar. signsgd: Compressed optimisation for non-convex problems. In International Conference on Machine Learning, pages 560–569. PMLR, 2018.
- <span id="page-14-1"></span>Xi Chen, Kaituo Feng, Changsheng Li, Xunhao Lai, Xiangyu Yue, Ye Yuan, and Guoren Wang. Fira: Can we achieve full-rank training of llms under low-rank constraint? arXiv preprint arXiv:2410.01623, 2024a.
- <span id="page-14-8"></span>Xiangning Chen, Chen Liang, Da Huang, Esteban Real, Kaiyuan Wang, Hieu Pham, Xuanyi Dong, Thang Luong, Cho-Jui Hsieh, Yifeng Lu, et al. Symbolic discovery of optimization algorithms. Advances in neural information processing systems, 36, 2024b.
- <span id="page-14-10"></span>Wonwoong Cho, Sungha Choi, David Keetae Park, Inkyu Shin, and Jaegul Choo. Image-to-image translation via group-wise deep whitening-and-coloring transformation. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 10639–10647, 2019.
- <span id="page-14-4"></span>D Choi. On empirical comparisons of optimizers for deep learning. arXiv preprint arXiv:1910.05446, 2019.
- <span id="page-14-11"></span>Sungha Choi, Sanghun Jung, Huiwon Yun, Joanne T Kim, Seungryong Kim, and Jaegul Choo. Robustnet: Improving domain generalization in urban-scene segmentation via instance selective whitening. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 11580–11590, 2021.
- <span id="page-14-0"></span>Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, Anirudh Goyal, Anthony Hartshorn, Aobo Yang, Archi Mitra, Archie Sravankumar, Artem Korenev, Arthur Hinsvark, Arun Rao, Aston Zhang, Aurelien Rodriguez, Austen Gregerson, Ava Spataru, Baptiste Rozi ´ ere, Bethany Biron, ` Binh Tang, Bobbie Chern, Charlotte Caucheteux, Chaya Nayak, Chloe Bi, Chris Marra, Chris McConnell, Christian Keller, Christophe Touret, Chunyang Wu, Corinne Wong, Cristian Canton Ferrer, Cyrus Nikolaidis, Damien Allonsius, Daniel Song, Danielle Pintz, Danny Livshits, David Esiobu, Dhruv Choudhary, Dhruv Mahajan, Diego Garcia-Olano, Diego Perino, Dieuwke Hupkes, Egor Lakomkin, Ehab AlBadawy, Elina Lobanova, Emily Dinan, Eric Michael Smith, Filip Radenovic, Frank Zhang, Gabriel Synnaeve, Gabrielle Lee, Georgia Lewis Anderson, Graeme Nail, Gregoire Mialon, Guan Pang, Guillem Cucurell, Hailey Nguyen, Hannah Korevaar, Hu Xu, Hugo ´ Touvron, Iliyan Zarov, Imanol Arrieta Ibarra, Isabel M. Kloumann, Ishan Misra, Ivan Evtimov, Jade Copet, Jaewon Lee, Jan Geffert, Jana Vranes, Jason Park, Jay Mahadeokar, Jeet Shah, Jelmer van der Linde, Jennifer Billock, Jenny Hong, Jenya Lee, Jeremy Fu, Jianfeng Chi, Jianyu Huang, Jiawen Liu, Jie Wang, Jiecao Yu, Joanna Bitton, Joe Spisak, Jongsoo Park, Joseph Rocca, Joshua Johnstun, Joshua Saxe, Junteng Jia, Kalyan Vasuden Alwala, Kartikeya Upasani, Kate Plawiak, Ke Li, Kenneth Heafield, and Kevin Stone. The llama 3 herd of models. CoRR, abs/2407.21783, 2024.
- <span id="page-14-6"></span>John Duchi, Elad Hazan, and Yoram Singer. Adaptive subgradient methods for online learning and stochastic optimization. Journal of machine learning research, 12(7), 2011.
- <span id="page-14-5"></span>Sai Surya Duvvuri, Fnu Devvrit, Rohan Anil, Cho-Jui Hsieh, and Inderjit S Dhillon. Combining axes preconditioners through kronecker approximation for deep learning. In The Twelfth International Conference on Learning Representations.
- <span id="page-15-12"></span>Kaixin Gao, Xiaolei Liu, Zhenghai Huang, Min Wang, Zidong Wang, Dachuan Xu, and Fan Yu. A trace-restricted kronecker-factored approximation to natural gradient. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 35, pages 7519–7527, 2021.
- <span id="page-15-11"></span>Thomas George, Cesar Laurent, Xavier Bouthillier, Nicolas Ballas, and Pascal Vincent. Fast ´ approximate natural gradient descent in a kronecker factored eigenbasis. Advances in Neural Information Processing Systems, 31, 2018.
- <span id="page-15-10"></span>Roger Grosse and James Martens. A kronecker-factored approximate fisher matrix for convolution layers. In International Conference on Machine Learning, pages 573–582. PMLR, 2016.
- <span id="page-15-1"></span>Vineet Gupta, Tomer Koren, and Yoram Singer. Shampoo: Preconditioned stochastic tensor optimization. In International Conference on Machine Learning, pages 1842–1850. PMLR, 2018.
- <span id="page-15-3"></span>Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. Lora: Low-rank adaptation of large language models. arXiv preprint arXiv:2106.09685, 2021.
- <span id="page-15-16"></span>Lei Huang, Yi Zhou, Fan Zhu, Li Liu, and Ling Shao. Iterative normalization: Beyond standardization towards efficient whitening. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pages 4874–4883, 2019.
- <span id="page-15-7"></span>Dongseong Hwang. Fadam: Adam is a natural gradient optimizer using diagonal empirical fisher information. arXiv preprint arXiv:2405.12807, 2024.
- <span id="page-15-2"></span>Keller Jordan, Yuchen Jin, Vlado Boza, Jiacheng You, Franz Cecista, Laker Newhouse, and Jeremy Bernstein. Muon: An optimizer for hidden layers in neural networks, 2024. URL [https:](https://kellerjordan.github.io/posts/muon/) [//kellerjordan.github.io/posts/muon/](https://kellerjordan.github.io/posts/muon/).
- <span id="page-15-8"></span>Diederik P Kingma. Adam: A method for stochastic optimization. arXiv preprint arXiv:1412.6980, 2014.
- <span id="page-15-13"></span>Abdoulaye Koroko, Ani Anciaux-Sedrakian, Ibtihel Ben Gharbia, Valerie Gar ´ es, Mounir Haddou, ` and Quang Huy Tran. Efficient approximations of the fisher matrix in neural networks using kronecker product singular value decomposition. arXiv preprint arXiv:2201.10285, 2022.
- <span id="page-15-0"></span>Vijay Anand Korthikanti, Jared Casper, Sangkug Lym, Lawrence McAfee, Michael Andersch, Mohammad Shoeybi, and Bryan Catanzaro. Reducing activation recomputation in large transformer models. Proceedings of Machine Learning and Systems, 5:341–353, 2023.
- <span id="page-15-17"></span>Peihua Li, Jiangtao Xie, Qilong Wang, and Zilin Gao. Towards faster training of global covariance pooling networks by iterative matrix square root normalization. In Proceedings of the IEEE conference on computer vision and pattern recognition, pages 947–955, 2018.
- <span id="page-15-14"></span>Xi-Lin Li. Preconditioned stochastic gradient descent. IEEE transactions on neural networks and learning systems, 29(5):1454–1466, 2017.
- <span id="page-15-9"></span>Xi-Lin Li. Preconditioner on matrix lie group for sgd. arXiv preprint arXiv:1809.10232, 2018.
- <span id="page-15-15"></span>Yijun Li, Chen Fang, Jimei Yang, Zhaowen Wang, Xin Lu, and Ming-Hsuan Yang. Universal style transfer via feature transforms. Advances in neural information processing systems, 30, 2017.
- <span id="page-15-4"></span>Vladislav Lialin, Sherin Muckatira, Namrata Shivagunde, and Anna Rumshisky. Relora: Highrank training through low-rank updates. In The Twelfth International Conference on Learning Representations, 2023.
- <span id="page-15-5"></span>Wu Lin, Felix Dangel, Runa Eschenhagen, Juhan Bae, Richard E Turner, and Alireza Makhzani. Can we remove the square-root in adaptive gradient methods? a second-order perspective. arXiv preprint arXiv:2402.03496, 2024.
- <span id="page-15-6"></span>Ilya Loshchilov and Frank Hutter. Sgdr: Stochastic gradient descent with warm restarts. arXiv preprint arXiv:1608.03983, 2016.
- <span id="page-16-1"></span>Chao Ma, Wenbo Gong, Meyer Scetbon, and Edward Meeds. Swan: Preprocessing sgd enables adam-level performance on llm training with significant memory reduction. arXiv preprint arXiv:2412.13148, 2024.
- <span id="page-16-9"></span>James Martens. New insights and perspectives on the natural gradient method. Journal of Machine Learning Research, 21(146):1–76, 2020.
- <span id="page-16-15"></span>James Martens and Roger Grosse. Optimizing neural networks with kronecker-factored approximate curvature. In International conference on machine learning, pages 2408–2417. PMLR, 2015.
- <span id="page-16-16"></span>James Martens, Jimmy Ba, and Matt Johnson. Kronecker-factored curvature approximations for recurrent neural networks. In International Conference on Learning Representations, 2018.
- <span id="page-16-12"></span>Depen Morwani, Itai Shapira, Nikhil Vyas, Eran Malach, Sham Kakade, and Lucas Janson. A new perspective on shampoo's preconditioner. arXiv preprint arXiv:2406.17748, 2024.
- <span id="page-16-17"></span>Omead Pooladzandi and Xi-Lin Li. Curvature-informed sgd via general purpose lie-group preconditioners. arXiv preprint arXiv:2402.04553, 2024.
- <span id="page-16-8"></span>Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J Liu. Exploring the limits of transfer learning with a unified text-to-text transformer. Journal of machine learning research, 21(140):1–67, 2020.
- <span id="page-16-14"></span>Noam Shazeer and Mitchell Stern. Adafactor: Adaptive learning rates with sublinear memory cost. In International Conference on Machine Learning, pages 4596–4604. PMLR, 2018.
- <span id="page-16-4"></span>Chongjie Si, Xuehui Wang, Xue Yang, Zhengqin Xu, Qingyun Li, Jifeng Dai, Yu Qiao, Xiaokang Yang, and Wei Shen. Flora: Low-rank core space for n-dimension. arXiv preprint arXiv:2405.14739, 2024.
- <span id="page-16-11"></span>Shiqing Sun and James C Spall. Connection of diagonal hessian estimates to natural gradients in stochastic optimization. In 2021 55th Annual Conference on Information Sciences and Systems (CISS), pages 1–6. IEEE, 2021.
- <span id="page-16-18"></span>Yuandong Tian, Lantao Yu, Xinlei Chen, and Surya Ganguli. Understanding self-supervised learning with dual deep networks. arXiv preprint arXiv:2010.00578, 2020.
- <span id="page-16-7"></span>Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothee´ Lacroix, Baptiste Roziere, Naman Goyal, Eric Hambro, Faisal Azhar, et al. Llama: Open and ` efficient foundation language models. arXiv preprint arXiv:2302.13971, 2023.
- <span id="page-16-0"></span>Nikhil Vyas, Depen Morwani, Rosie Zhao, Itai Shapira, David Brandfonbrener, Lucas Janson, and Sham Kakade. Soap: Improving and stabilizing shampoo using adam. arXiv preprint arXiv:2409.11321, 2024.
- <span id="page-16-2"></span>Minghao Xu, Lichuan Xiang, Xu Cai, and Hongkai Wen. No more adam: Learning rate scaling at initialization is all you need, 2024. URL <https://arxiv.org/abs/2412.11768>.
- <span id="page-16-10"></span>Zhirong Yang and Jorma Laaksonen. Principal whitened gradient for information geometry. Neural Networks, 21(2-3):232–240, 2008.
- <span id="page-16-13"></span>Yang You, Igor Gitman, and Boris Ginsburg. Large batch training of convolutional networks. arXiv preprint arXiv:1708.03888, 2017.
- <span id="page-16-6"></span>Yang You, Jing Li, Sashank Reddi, Jonathan Hseu, Sanjiv Kumar, Srinadh Bhojanapalli, Xiaodan Song, James Demmel, Kurt Keutzer, and Cho-Jui Hsieh. Large batch optimization for deep learning: Training bert in 76 minutes. arXiv preprint arXiv:1904.00962, 2019.
- <span id="page-16-3"></span>Yushun Zhang, Congliang Chen, Ziniu Li, Tian Ding, Chenwei Wu, Yinyu Ye, Zhi-Quan Luo, and Ruoyu Sun. Adam-mini: Use fewer learning rates to gain more. arXiv preprint arXiv:2406.16793, 2024.
- <span id="page-16-5"></span>Jiawei Zhao, Zhenyu Zhang, Beidi Chen, Zhangyang Wang, Anima Anandkumar, and Yuandong Tian. Galore: Memory-efficient llm training by gradient low-rank projection. arXiv preprint arXiv:2403.03507, 2024a.
- <span id="page-17-1"></span>Pengxiang Zhao, Ping Li, Yingjie Gu, Yi Zheng, Stephan Ludger Kolker, Zhefeng Wang, and ¨ Xiaoming Yuan. Adapprox: Adaptive approximation in adam optimization via randomized lowrank matrices. arXiv preprint arXiv:2403.14958, 2024b.
- <span id="page-17-2"></span>Rosie Zhao, Depen Morwani, David Brandfonbrener, Nikhil Vyas, and Sham Kakade. Deconstructing what makes a good optimizer for language models. arXiv preprint arXiv:2407.07972, 2024c.
- <span id="page-17-0"></span>Hanqing Zhu, Zhenyu Zhang, Wenyan Cong, Xi Liu, Sem Park, Vikas Chandra, Bo Long, David Z Pan, Zhangyang Wang, and Jinwon Lee. Apollo: Sgd-like memory, adamw-level performance. arXiv preprint arXiv:2412.05270, 2024.

# Acronyms

<span id="page-18-11"></span><span id="page-18-2"></span>Alice Adaptive low-dimensional subspace estimation. [1,](#page-0-1) [2,](#page-1-1) [8,](#page-7-1) [10,](#page-9-2) [11,](#page-10-0) [13,](#page-12-2) [14,](#page-13-1) [38,](#page-37-0) [40,](#page-39-0) [42,](#page-41-0) [43,](#page-42-2) [45](#page-44-0) Alice-0 Alice without tracking. [10,](#page-9-2) [11,](#page-10-0) [13,](#page-12-2) [38](#page-37-0)

<span id="page-18-5"></span><span id="page-18-3"></span>Eigen-Adam Eigenspace Adam. [2,](#page-1-1) [3,](#page-2-3) [5](#page-4-7)[–10,](#page-9-2) [22](#page-21-1)[–24,](#page-23-1) [27,](#page-26-2) [33,](#page-32-0) [37,](#page-36-1) [40,](#page-39-0) [41](#page-40-2) EMA exponential moving average. [1,](#page-0-1) [3,](#page-2-3) [4,](#page-3-5) [6,](#page-5-1) [8,](#page-7-1) [14,](#page-13-1) [22,](#page-21-1) [23,](#page-22-1) [38–](#page-37-0)[40,](#page-39-0) [45,](#page-44-0) [46](#page-45-3) EVD eigen-value decomposition. [3,](#page-2-3) [9,](#page-8-2) [23,](#page-22-1) [45](#page-44-0)

<span id="page-18-13"></span><span id="page-18-6"></span><span id="page-18-0"></span>F-norm Frobenius norm. [28](#page-27-0) FIM Fisher information matrix. [1–](#page-0-1)[4,](#page-3-5) [6,](#page-5-1) [7,](#page-6-4) [9–](#page-8-2)[11,](#page-10-0) [14,](#page-13-1) [20,](#page-19-1) [21,](#page-20-0) [25,](#page-24-0) [28,](#page-27-0) [38](#page-37-0)[–40](#page-39-0)

<span id="page-18-8"></span>NGD natural gradient descent. [3–](#page-2-3)[7,](#page-6-4) [9,](#page-8-2) [20,](#page-19-1) [26,](#page-25-3) [27](#page-26-2)

<span id="page-18-1"></span>RACS Row and Column Scaled SGD. [1,](#page-0-1) [2,](#page-1-1) [7,](#page-6-4) [11](#page-10-0)[–14,](#page-13-1) [40,](#page-39-0) [42,](#page-41-0) [43,](#page-42-2) [45,](#page-44-0) [46](#page-45-3)

<span id="page-18-10"></span><span id="page-18-4"></span>SGD stochastic gradient descent. [1,](#page-0-1) [2](#page-1-1) SPD symmetric positive definite. [4,](#page-3-5) [7,](#page-6-4) [23,](#page-22-1) [29,](#page-28-0) [31,](#page-30-2) [33,](#page-32-0) [38,](#page-37-0) [39](#page-38-2) SVD singular value decomposition. [11,](#page-10-0) [40](#page-39-0)

# <span id="page-18-12"></span><span id="page-18-7"></span>A Examples of diagonal operations

In this section, we will give some detailed examples on each of the diagonal operations we introduced in Sec. [2.](#page-1-2)

Example of Diag(·) This will extract the diagonals of a input matrix into a vector:

$$
\boldsymbol{M} = \left[ \begin{array}{ccc} a_{11} & a_{12} & a_{13} \\ a_{21} & a_{22} & a_{23} \\ a_{31} & a_{32} & a_{33} \end{array} \right], \quad \text{Diag}(\boldsymbol{M}) = [a_{11}, a_{22}, a_{33}]^T
$$

Example of DiagB(·) This simply stack the input matrices sequence into a larger block diagonal matrix:

$$
\mathrm{Diag}_{\mathrm{B}}(M_1,M_2,M_3) = \left[ \begin{array}{ccc} M_1 & 0 & 0 \\ 0 & M_2 & 0 \\ 0 & 0 & M_3 \end{array} \right]
$$

Example of Diagv(·) This will stack the vector element into a pure diagonal matrix:

Diag<sub>v</sub>([a<sub>11</sub>, a<sub>22</sub>, a<sub>33</sub>]<sup>T</sup>) = 
$$
\begin{bmatrix} a_{11} & 0 & 0 \ 0 & a_{22} & 0 \ 0 & 0 & a_{33} \end{bmatrix}
$$

Example of DiagM(·) This will stack the elements in input matrix to form a larger pure diagonal matrix in a column-wise manner.

$$
\text{Diag}_{\mathcal{M}}\left(\left[\begin{array}{cc} a_{11} & a_{12} \\ a_{21} & a_{22} \end{array}\right]\right) = \left[\begin{array}{cccc} a_{11} & 0 & 0 & 0 \\ 0 & a_{21} & 0 & 0 \\ 0 & 0 & a_{12} & 0 \\ 0 & 0 & 0 & a_{22} \end{array}\right]
$$

# <span id="page-18-9"></span>B Background

In this section, we will provide a more comprehensive backgrounds.

#### <span id="page-19-1"></span>B.1 Fisher information

Fisher information can also be viewed as the "sharpness" of the likelihood around the true parameters from the maximum likelihood view point. Formally, under the context of LLMs fθ(·), we consider a dataset {xi} N <sup>i</sup>=1, where N is total batched sentences, and x<sup>i</sup> is the token sequence of i th sentence. One can define sentence-level auto-regressive loss function L = P <sup>j</sup>=1 c(xi,j+1, fθ(xi,:<sup>j</sup> ), where j is the token index and c is the user-defined loss metric. The corresponding likelihood can be defined as pθ(xi) ∝ exp(− P <sup>j</sup>=1 c(xi,j+1, fθ(xi,:<sup>j</sup> ))). The standard empirical [FIM](#page-18-0) is defined as

$$
\boldsymbol{F} = \sum_{i=1}^N \nabla_{\theta} \log p_{\theta}(\boldsymbol{x}_i) \nabla_{\theta}^T \log p_{\theta}(\boldsymbol{x}_i)
$$

In practice, we often use the mini-batched gradient ⃗g = 1 N<sup>B</sup> P<sup>N</sup><sup>B</sup> <sup>i</sup>=1 log pθ(xi) with batch size N<sup>B</sup> for empirical [FIM](#page-18-0) during training. More discussion can be found in [Lin et al.](#page-15-5) [\[2024\]](#page-15-5). Throughout this paper, we adopt the notation E[⃗g⃗g T ] as F.

One standard application of [FIM](#page-18-0) is efficient optimization. [NGD](#page-18-8) leverage the inverse of [FIM](#page-18-0) to smooth the local information geometry, leading to the steepest descent in the probability space with KL divergence metric. This typically leads to faster convergences compared to its parameter-space counterpart; and more stable optimization [\[Martens, 2020\]](#page-16-9). The update of [NGD](#page-18-8) with step size λ is

$$
\theta \leftarrow \theta - \lambda \boldsymbol{F}^{-1} \nabla_{\theta} \mathcal{L}.
$$

However, square-root inverse is sometimes more favorable than inverse, and has been shown that it provides a better approximation to the geodesic flow, compared with the default natural gradient update [Yang and Laaksonen](#page-16-10) [\[2008\]](#page-16-10). Empirically, it demonstrates stronger performance and desired properties when using non-constant learning rate [\[Bergstra and Bengio, 2012,](#page-14-3) [Choi, 2019,](#page-14-4) [Lin et al.,](#page-15-5) [2024,](#page-15-5) [Loshchilov and Hutter, 2016\]](#page-15-6). The corresponding update is to simply replace F <sup>−</sup><sup>1</sup> with F − <sup>1</sup> 2 :

$$
\theta \leftarrow \theta - \lambda \boldsymbol{F}^{-\frac{1}{2}} \nabla_{\theta} \mathcal{L}.
$$
 (22)

In this paper, we will use the square-root inverse view point, but our analysis is agnostic to it and can be easily extended to the direct inverse. However, matrix multiplication involving [FIM](#page-18-0) and its inverse are computationally expensive for large models since F ∈ R mn×mn for vectorized parameters θ ∈ R mn. Next, we will briefly introduce Kronecker product and block diagonals, which are two main classes of structural assumptions used in this paper. Their nice properties can significantly reduce the assocaited computation burden.

#### <span id="page-19-0"></span>B.2 Kronecker product and block diagonals

Kronecker product, denoted by ⊗, is to combine two arbitrary matrices into a larger matrix with block-wise patterns. It has emerged as a powerful tool for approximating higher-order information like Hessian [\[Grosse and Martens, 2016\]](#page-15-10) or [FIM.](#page-18-0) The main advantages are their nice properties regarding matrix operations, leading to efficient practical procedures when dealing with large matrix. We will mainly use two properties:

$$
(\mathbf{A} \otimes \mathbf{B})^{-\frac{1}{2}} = \mathbf{A}^{-\frac{1}{2}} \otimes \mathbf{B}^{-\frac{1}{2}} \tag{23}
$$

$$
(A \otimes B) \operatorname{Vec}(C) = \operatorname{Vec}(BCA^T) \tag{24}
$$

where the first one holds when A,B are square-root invertible. The second one is particular useful to reduce the computation associated with matrix-vector multiplication in Eq. [\(1\)](#page-2-0). For A ⊗ B ∈ R mn×mn, it reduces the computation from O(m<sup>2</sup>n 2 ) to O(mn<sup>2</sup> + m<sup>2</sup>n) with A ∈ R <sup>n</sup>×<sup>n</sup>, B ∈ R <sup>m</sup>×<sup>m</sup>, and C ∈ R <sup>m</sup>×<sup>n</sup>.

For block diagonal matrix, one can also easily compute its square-root inverse:

$$
\text{Diag}_{B}(M_{1},...,M_{n})^{-\frac{1}{2}} = \text{Diag}_{B}(M_{1}^{-\frac{1}{2}},...,M_{n}^{-\frac{1}{2}})
$$
\n(25)

where each M<sup>i</sup> is square-root invertible. When each M<sup>i</sup> is also a diagonal matrix with positive values, we have the following:

$$
\mathrm{Diag}_{\mathrm{B}}(M_1,\ldots,M_n)^{-\frac{1}{2}}\mathrm{Vec}(C)=\mathrm{Vec}\left(\frac{C}{\sqrt{\mathrm{Mat}(v)}}\right)
$$
(26)

where v is the vector containing the diagonals of DiagB(M1, . . . ,Mn), transforming matrix vector product into element-wise operation.

#### <span id="page-20-0"></span>B.3 Operators for gradient: normalization and whitening

Recently, there are some optimizers [\[Jordan et al., 2024,](#page-15-2) [Ma et al., 2024,](#page-16-1) [You et al., 2017,](#page-16-13) [2019\]](#page-16-6) that apply operators to pre-process the gradient and use it in standard SGD. Empirical evidence has verified their effectiveness in training LLMs. In particular, there are two well-known operators: normalization and whitening, where the above optimizers relies on one or both of them. In particular,

$$
\text{Norm}(\boldsymbol{G}) = \frac{\boldsymbol{G}}{1\sqrt{\boldsymbol{s}^T}} = \boldsymbol{G}\boldsymbol{S}^{-\frac{1}{2}} \tag{27}
$$

$$
Whitening(\boldsymbol{G}) = (\boldsymbol{G}\boldsymbol{G}^T)^{-\frac{1}{2}}\boldsymbol{G}.
$$
\n(28)

where s ∈ R <sup>n</sup>, s<sup>i</sup> = P<sup>m</sup> <sup>j</sup>=1 G<sup>2</sup> ij with G ∈ R <sup>m</sup>×<sup>n</sup>, and S = Diagv(s). Namely, vector s contains the squared column norm of G, and S is a scaling matrix to normalize the columns. Normalizing the rows can also be written in a similar format. Whitening operator essentially orthogonalizes G, that compute the closest orthogonal matrix to G under Frobenius norm. In practice, the whitening operator can be iteratively solved using Newton-Schulz algorithm without explicitly computing the square-root inverse.

#### B.4 Shampoo Optimizer

Shampoo [\[Gupta et al., 2018\]](#page-15-1) was originally proposed as the second-order optimization technique over the tensor space. Under the context of transformers, typically matrix parameters are considered. Its core design principle also aims to approximate the [FIM](#page-18-0) with structural assumptions F˜ <sup>t</sup> = R 1 2 n,t⊗L 1 2 m,t, with Rn,t = Rn,t−<sup>1</sup> + G<sup>T</sup> <sup>t</sup> G<sup>t</sup> and Lm,t = Lm,t−<sup>1</sup> + GtG<sup>T</sup> t . The above update rule can be seen as the moving average estimate of E[G<sup>T</sup> <sup>t</sup> Gt] and E[GtG<sup>T</sup> t ]. However, the Shampoo paper [\[Gupta](#page-15-1) [et al., 2018\]](#page-15-1) does not explicitly show why these design choices of Rn, L<sup>m</sup> approximate the [FIM.](#page-18-0) In fact, they only show R 1 2 <sup>n</sup> ⊗ L 1 <sup>2</sup><sup>m</sup> forms an upper bound of [FIM](#page-18-0)[\\*](#page-20-1) . This is not helpful in understanding whether this approximates the [FIM](#page-18-0) or not. Another very recent follow-up work [\[Morwani et al.,](#page-16-12) [2024\]](#page-16-12) provides an explanation of the shampoo preconditioner in terms of approximating [FIM.](#page-18-0) They show the square of Shampoo's preconditioner is equivalent to a single step of power iteration of computing optimal Kronecker product approximation to [FIM.](#page-18-0) It indirectly establishes the connections to [FIM](#page-18-0) approximation since the approximation is expressed as an iterative algorithm. To the best of our knowledge, our result is the first to directly establish the connection of Shampoo to [FIM](#page-18-0) approximation as minimizing a upper bound of the loss with the Frobenius norm (Theorem [3.1\)](#page-3-4).

Nevertheless, the original Shampoo algorithm is summarized in Algorithm [5.](#page-20-2)

#### Algorithm 5 Shampoo Optimizer

<span id="page-20-2"></span>Input: L<sup>m</sup> = ϵIm, R<sup>n</sup> = ϵIn, learning rate λ, optimization step T, loss function L. for t = 1, . . . , T do G<sup>t</sup> = ∇<sup>W</sup>tL Lm,t = Lm,t−<sup>1</sup> + GtG<sup>T</sup> t Rn,t = Rn,t−<sup>1</sup> + G<sup>T</sup> <sup>t</sup> G<sup>t</sup> W<sup>t</sup> = Wt−<sup>1</sup> + λL − <sup>1</sup> 4 m,tGtR − <sup>1</sup> 4 n,t end for

#### <span id="page-20-3"></span>B.5 SOAP/AdaDiag++

SOAP/AdaDiag++ [\[Anonymous, 2024,](#page-14-2) [Vyas et al., 2024\]](#page-16-0) is a recently proposed adaptive optimizer aiming to improve the practical convergence and stability of Shampoo. Their main intuition behind (from the view point of [Vyas et al.](#page-16-0) [\[2024\]](#page-16-0)) is that they show Shampoo is equivalent to performing Adafactor [\[Shazeer and Stern, 2018\]](#page-16-14) under the Shampoo's eigen-space. Namely, the eigen-matrix of Lm,t and Rn,t in Algorithm [5.](#page-20-2) Since Adafactor is an approximation to Adam, they propose to

<span id="page-20-1"></span><sup>\*</sup>Lemma 8 in [\[Gupta et al., 2018\]](#page-15-1). Note that our paper assumes Vec(·) is stacking columns of matrix whereas [Gupta et al.](#page-15-1) [\[2018\]](#page-15-1) assumes stacking the rows, explaining the reverse order of presentation

<span id="page-21-1"></span>use Adam instead of Adafactor in Shampoo's eigen-space, to further improve the performance. They propose the following update rule:

<span id="page-21-2"></span>
$$
\boldsymbol{m}_{t} = \beta_{1}\boldsymbol{m}_{t-1} + (1 - \beta_{1})\boldsymbol{G}_{t} \quad \text{(first moment)}
$$
\n
$$
\boldsymbol{L}_{m,t} = \beta_{3}\boldsymbol{L}_{m,t-1} + (1 - \beta_{3})\boldsymbol{G}_{t}\boldsymbol{G}_{t}^{T} \quad \text{(Shampoo's } \boldsymbol{L}_{m,t})
$$
\n
$$
\boldsymbol{R}_{n,t} = \beta_{3}\boldsymbol{R}_{n,t-1} + (1 - \beta_{3})\boldsymbol{G}_{t}^{T}\boldsymbol{G}_{t} \quad \text{(Shampoo's } \boldsymbol{R}_{n,t})
$$
\n
$$
\boldsymbol{U}_{L,t} = \text{EVD}(\boldsymbol{L}_{m,t}) \quad \text{(Shampoo's left eigen-space)}
$$
\n
$$
\boldsymbol{U}_{R,t} = \text{EVD}(\boldsymbol{R}_{n,t}) \quad \text{(Shampoo's right eigen-space)}
$$
\n
$$
\boldsymbol{v}_{t} = \beta_{2}\boldsymbol{v}_{t-1} + (1 - \beta_{2})(\boldsymbol{U}_{L,t}^{T}\boldsymbol{G}_{t}\boldsymbol{U}_{R,t})^{\odot 2} \quad \text{(second moment)}
$$
\n
$$
\Delta = \boldsymbol{U}_{L,t} \frac{\boldsymbol{U}_{L,t}^{T}\boldsymbol{m}_{t}\boldsymbol{U}_{R,t}}{\sqrt{\boldsymbol{v}_{t}}} \boldsymbol{U}_{R,t}^{T} \qquad (29)
$$

These update rules exactly describes the procedure to applying Adam updates in the "rotated" space defined by UL,t and UR,t. Due to the computational burden associated with EVD, SOAP proposed to only update UL,t, UR,t at certain intervals. This leads to the following algorithm:

#### Algorithm 6 SOAP optimizer

| Input: learning rate λ, update interval K, β1, β2, β3, optimization step T. |                                              |
|-----------------------------------------------------------------------------|----------------------------------------------|
| m0<br>= 0; v0<br>= 0                                                        | ▷Initialize two moments                      |
| Lm,0<br>= 0; Rn,0<br>= 0                                                    | ▷Initialize two EMA states for GGT<br>, GT G |
| for t = 1, , T do                                                           |                                              |
| = ∇WtL<br>Gt                                                                |                                              |
| mt<br>= β1mt−1<br>+ (1 − β1)Gt                                              |                                              |
| + (1 − β3)GtGT<br>Lm,t<br>= β3Lm,t−1<br>t                                   | ▷Accumulation for GGT                        |
| + (1 − β3)GT<br>Rn,t<br>= β3Rn,t−1<br>t Gt                                  | ▷Accumulation for GT G                       |
| if t == 1 or (t<br>mod K) == 0 then                                         |                                              |
| UR,t<br>= EVD(Rn,t)                                                         | ▷Get right eigen-space UR                    |
| UL,t<br>= EVD(Lm,t)                                                         | ▷Get left eigen-space UL                     |
| else                                                                        |                                              |
| UR,t<br>= UR,t−1                                                            |                                              |
| UL,t<br>= UL,t−1                                                            |                                              |
| end if                                                                      |                                              |
| = UT<br>mft<br>L,tmtUR,t                                                    | ▷Get rotated 1st moment                      |
| ⊙2<br>+ (1 − β2)(UT<br>vt<br>= β2vt−1<br>L,tGtUR,t)                         | ▷Compute second moments                      |
| √mft<br>UT<br>Wt+1<br>= Wt<br>− λUL,t<br>R,t<br>vt                          |                                              |
| end for                                                                     |                                              |

### <span id="page-21-0"></span>B.6 AdaDiag and one-side SOAP

AdaDiag++ [\[Anonymous, 2024\]](#page-14-2), a concurrent work to SOAP, independently develops the equivalent update rules as SOAP. The only difference is that they disable the [EMA](#page-18-3) tracking for Lm,t and Rn,t. The resulting optimizer is both computational and memory expensive due to the storage of UR, U<sup>L</sup> and two eigenvalue decompositions. To address this issue, they both propose a one-side version called AdaDiag and one-side SOAP by only considering either left or right eigen-space. The resulting update rule is exactly the same as our proposed [Eigen-Adam](#page-18-5) (i.e. Eq. [\(13\)](#page-5-2)).

However, they propose this design choice purely based on intuition to reduce computation and memory consumption, and do not explicitly reveal the connections to their two-sided version. Thus, it lacks the understanding on why two-sided version obtains empirically better performance. Based on Sec. [3.4](#page-4-0) and Sec. [3.5,](#page-5-0) we show that although one-sided version has similar updates as the two-sided twins, they are different optimizers with distinct underlying structural assumptions. In fact, the structures of SOAP/AdaDiag++ strictly generalizes their one-sided version, explaining the better empirical performance. The resulting algorithm is the following:

<span id="page-22-1"></span>Algorithm 7 [Eigen-Adam/](#page-18-5)AdaDiag/one-side SOAP optimizer

<span id="page-22-0"></span>Input: learning rate λ, update interval K, β1, β2, β3, optimization step T. m<sup>0</sup> = 0; v<sup>0</sup> = 0 ▷*Initialize two moments* Q<sup>0</sup> = 0 ▷*Initialize the [EMA](#page-18-3) state for* GG<sup>T</sup> for t = 1, . . . , T do G<sup>t</sup> = ∇<sup>W</sup>tL Q<sup>t</sup> = β3Qt−<sup>1</sup> + (1 − β3)GtG<sup>T</sup> <sup>t</sup> ▷*Accumulate the* GG<sup>T</sup> m<sup>t</sup> = β1mt−<sup>1</sup> + (1 − β1)G<sup>t</sup> ▷*Accumulate the first moment* if t == 1 or (t mod K) == 0 then Uf,t = EVD(Qt) ▷*Obtain the* U else Uf,t = Uf,t−<sup>1</sup> end if m˜ <sup>t</sup> = U<sup>T</sup> f,tm<sup>t</sup> ▷*Rotate the first moment* v<sup>t</sup> = β2vt−<sup>1</sup> + (1 − β2)(U<sup>T</sup> f,tGt) <sup>⊙</sup><sup>2</sup> ▷*Accumulate the second moments* Wt+1 = W<sup>t</sup> − λUf,t <sup>√</sup>m˜ <sup>t</sup> vt ▷*Update in the original space* end for

#### B.7 SWAN

Recently, there is a newly proposed adaptive optimizer that completely removes the needs of storing internal states, called SWAN. It relies on two processing operators applied to raw current gradient: GradNorm and GradWhitening, as a replacement of first and second moments. For a current gradient G,

$$
\text{GradNorm}(G) = \frac{G - \bar{g}\mathbf{1}_n^{\top}}{s\mathbf{1}_n^{\top}}
$$
\n(30)

$$
GradWhitening(G) = (GGT)-\frac{1}{2}G
$$
\n(31)

where ¯⃗g = 1 n P<sup>n</sup> <sup>i</sup>=1 G:,i is the mean across rows; s = q 1 n P<sup>n</sup> <sup>i</sup>=1(G:,i <sup>−</sup> ¯⃗g) <sup>2</sup> is the standard deviation across rows; ¯⃗g and s are m-dimensional column vectors; and 1<sup>n</sup> is a n-dimensional column vector of ones. Then, SWAN performs the following to generate the update:

$$
\tilde{G} = \text{GradNorm}(G)
$$
  

$$
\Delta = \text{GradWhitening}(\tilde{G})
$$
 (32)

We can see that the proposed GradNorm is equivalent to normalization up to a scaling <sup>√</sup> n when the mean ¯⃗g is 0. SWAN derives these two steps from investigating the LLM dynamics. In practice, SWAN proposes to compute the (GG<sup>T</sup> ) − <sup>1</sup> <sup>2</sup> using Newton-Schulz iterations.

#### B.8 Newton Schulz iteration

In many machine learning applications, like successive whitening and coloring transform [\[Cho et al.,](#page-14-10) [2019,](#page-14-10) [Choi et al., 2021,](#page-14-11) [Li et al., 2017\]](#page-15-15), one often encountered the computation of square root inverse of some [SPD](#page-18-10) matrix. One standard approach is to compute the [EVD](#page-18-6) and take the square root inverse of the eigenvalue matrix. However, [EVD](#page-18-6) is computationally expensive. Another alternative approach is use Newton-Schulz iteration (NS), an iterative updates of two matrix. Specifically,

$$
Y_0 = \frac{A}{\|A\|_F} \quad Z_0 = I
$$
  

$$
Y_{t+1} = \frac{1}{2} Y_t (3I - Z_t Y_t)
$$
  

$$
Z_{t+1} = \frac{1}{2} (3I - Z_t Y_t) Z_t
$$

with convergence Y<sup>t</sup> → <sup>A</sup> 1 √ <sup>2</sup> ∥A∥<sup>F</sup> and Z<sup>t</sup> → A<sup>−</sup> <sup>1</sup> 2 p ∥A∥<sup>F</sup> . Typically, NS converges very fast with only 5 steps [\[Huang et al., 2019,](#page-15-16) [Li et al., 2018\]](#page-15-17).

#### <span id="page-23-2"></span><span id="page-23-1"></span>B.9 Muon

Muon [\[Jordan et al., 2024\]](#page-15-2), is recently proposed to speed-up the training of LLMs, that relies on the whitening operator similar to SWAN. The core of the Muon is to orthogonalize the the momentum. The proposed update rule is

$$
m_t = \beta_1 m_{t-1} + (1 - \beta_1) G_t
$$
  
 
$$
\Delta = \text{GradWhitening}(m_t). \tag{33}
$$

Similarly, the GradWhitening step is computed using Newton-Schulz iteration. The main difference between Muon and SWAN is that Muon still requires the storage of first moments as state, whereas SWAN relies on the GradNorm operator applied to the raw gradient.

#### B.10 Lars

SWAN and Muon both involve the whitening operator with/without normalization, respectively. On the other hand, Lars [\[You et al., 2017\]](#page-16-13) is an operator that only relies on layer-wise normalization. For each layer, it simply compute the first moments, followed by a normalization operation. The update rule for each layer is

$$
\mathbf{m}_t = \beta_1 \mathbf{m}_{t-1} + (1 - \beta_1) \mathbf{G}_t
$$
  

$$
\Delta = \phi(||\theta||) \frac{\mathbf{m}_t}{||\mathbf{m}_t||}
$$
(34)

where ϕ is a scaling function with input of the parameter θ norm. One major difference of this layer-wise normalization to SWAN is that it is applied on the layer-wise level, whereas SWAN applies row/column-wise normalization.

#### <span id="page-23-0"></span>B.11 Low rank optimizers

The primary goal of low-rank optimizer is to reduce the memory consumed by the states of adaptive optimizers. The popularity of low-rank based method for large models starts from the well-known LoRA [\[Hu et al., 2021\]](#page-15-3), where each weight is inserted with an low-rank adapter W + AB with A ∈ R m×r and B ∈ R <sup>r</sup>×<sup>n</sup> during the finetuning stage. This formulation directly modifies the model architecture. [Si et al.](#page-16-4) [\[2024\]](#page-16-4) explicitly show that LoRA is secretly a gradient compressor, which translates the modification to model architecture into a low-rank optimizer with randomly sampled matrix. At the same time, GaLore [\[Zhao et al., 2024a\]](#page-16-5) popularizes the use of low-rank optimizers, which demonstrates on-par performance compared to full-rank Adam training. GaLore is proposed based on the analysis of reversible networks [\[Tian et al., 2020\]](#page-16-18). However, in practice, transformer may not satisfy the reversibility condition. Thus, GaLore does not provide a clear understanding on why it works on LLMs.

Algorithm [8](#page-24-1) summarizes the procedures. In practice, GaLore can be viewed as the composition of subspace search algorithm (i.e. SVD) with standard Adam optimizer. The original GaLore does not provide an explanation on the choice of Adam. On the other hand, our analysis reveals that the GaLore is an approximate low-rank extension to a different optimizer, [Eigen-Adam/](#page-18-5)AdaDiag/one-side SOAP, that is generalizes Adam (see Sec. [3.4\)](#page-4-0).

Since the states of Adam optimizer are based on the projected gradient σt, the overall memory consumption of GaLore is mn + 2nr + mr.

#### B.12 Apollo

Concurrent to this work, there is a recently proposed optimizer, called Apollo [\[Zhu et al., 2024\]](#page-17-0), that only scales the raw gradient and obtains SGD-like memory with Adam-level performance. They propose to scale the columns or rows similar to normalization in SWAN, but the scaling factor is estimated following the procedure proposed by Fira [\[Chen et al., 2024a\]](#page-14-1). The core idea of Apollo is to obtain ∆ from GaLore algorithm (Algorithm [8\)](#page-24-1), followed by computing the column/row-wise norm of ∆. This norm will be used as the scaling factor for the raw gradient G. Apollo has many variants. In particular, we choose Apollo-mini and Apollo-svd, where the former uses rank-1 random projection for scaling estimation, and the latter relies on the use of top r singular vectors as the

<span id="page-24-0"></span>Algorithm 8 GaLore Optimizer

<span id="page-24-1"></span>Input: learning rate λ, decay rates β1, β2, rank r, update interval k, scale α for t = 1, . . . , T do G<sup>t</sup> = ∇<sup>W</sup>tL if t == 1 or t mod k == 0 then U<sup>t</sup> = SVD(Gt, r) else U<sup>t</sup> = Ut−<sup>1</sup> end if σ<sup>t</sup> = U<sup>T</sup> <sup>t</sup> G<sup>t</sup> ∆ = Adam(σt, β1, β2) W<sup>t</sup> = Wt−<sup>1</sup> + λα∆ end for

projection, same as GaLore. Apollo-mini only maintains the rank-1 states, leading to significant memory savings. The memory consumption is mn + 2n + 2 for parameter W ∈ R <sup>m</sup>×<sup>n</sup>. And Apollo-svd consumes the same memory as GaLore. Algorithm [9](#page-24-2) summarizes the procedures.

Algorithm 9 Apollo Optimizer

```
Input: learning rate λ, decay rates β1, β2, rank r, update interval k, scale α
for t = 1, . . . , T do
  Gt = ∇WtL
  if t == 1 or t mod k == 0 then
    Ut ∼ N (0,
                1
                r
                  )
    seed ← an independent new random seed
  else
    Ut = Ut−1
  end if
  σt = UT
          t Gt
  ∆t = Adam(σt, β1, β2)
  St ← Diagv(s0, . . . , sm) {si =
                                  ∥∆t,:,i∥2
                                  ∥σt,:,i∥2
                                          }
  Wt = Wt−1 + λαGtSt
end for
```
Note that when rank r is set to 1, they propose to use global scaling <sup>∥</sup>∆t∥<sup>2</sup> ∥σt∥<sup>2</sup> instead of row/column-wise scaling.

### B.13 Subspace iteration

The subspace iteration method—also known as the block power method is a classical iterative technique for computing the dominant eigenvalues and corresponding eigenvectors of a matrix. It generalizes the basic power method from operating on a single vector to operating on a subspace, typically spanned by a initial matrix. When the initial matrix is closed to the targeting eigen-matrix, the convergence is fast. Empirically, we found that only 1 step of iteration is enough to give a satisfactory performance. Algorithm [10](#page-25-2) summarizes the subspace iteration algorithm to for finding the top r eigenvectors of a matrix A. We can see that the computation is bottlenecked by the matrix multiplication AUt−<sup>1</sup> which is O(m<sup>2</sup> r) if only performing 1 step.

# C Derivation of update formula

In this section, we will explicitly show how to connect the solution from minimizing reconstruction loss of [FIM](#page-18-0) (Eq. [\(2\)](#page-2-1)) to corresponding update rule.

<span id="page-25-3"></span><span id="page-25-2"></span>Input: symmetric matrix A ∈ R <sup>m</sup>×m, iteration step T, initial matrix M ∈ R m×r U<sup>0</sup> = M for t = 1, . . . , T do H<sup>t</sup> = AUt−<sup>1</sup> U<sup>t</sup> = QR decomposition(Ht) end for V = U<sup>T</sup> <sup>T</sup> AU<sup>T</sup> U = EVD(V ) Return U

#### <span id="page-25-0"></span>C.1 Shampoo's update formula

The key update formula of Shampoo is

$$
\bm{W}_t = \bm{W}_{t-1} + \lambda \bm{L}_{m,t}^{-\frac{1}{4}} \bm{G}_t \bm{R}_{n,t}^{-\frac{1}{4}}
$$

*Proof.* From Theorem [3.1,](#page-3-4) we simply apply the properties of Kronecker product to square-root version of natural gradient descent:

$$
\begin{aligned} &\operatorname{Mat}\left(\tilde{\pmb{F}}^{-\frac{1}{2}}\vec{\pmb{g}}\right) \\ &=\operatorname{Mat}\left((\pmb{R}_{n}^{\frac{1}{2}}\otimes\pmb{L}_{m}^{\frac{1}{2}})^{-\frac{1}{2}}\vec{\pmb{g}}\right) \\ &=\operatorname{Mat}\left(\operatorname{Vec}\left(\pmb{L}_{m}^{-\frac{1}{4}}\pmb{G}\pmb{R}_{n}^{-\frac{1}{4}}\right)\right) \\ &=\pmb{L}_{m}^{-\frac{1}{4}}\pmb{G}\pmb{R}_{n}^{-\frac{1}{4}} \end{aligned}
$$

#### <span id="page-25-1"></span>C.2 Generalization to whitening and normalization

The square-root [NGD](#page-18-8) update with F˜ in Eq. [\(7\)](#page-4-2) in Proposition [2](#page-4-1) is

$$
\operatorname{Mat}\left(\tilde{F}^{-\frac{1}{2}}\vec{g}\right) = \sqrt{n}\mathbb{E}[GG^T]^{-\frac{1}{2}}G\tag{35}
$$

*Proof.* From the solution in Eq. [\(7\)](#page-4-2), we can simply apply the properties of Kronecker product as in the derivation of Shampoo's update:

$$
\begin{aligned} &\operatorname{Mat}\left(\tilde{\pmb{F}}^{-\frac{1}{2}}\vec{\pmb{g}}\right)\\ &=\operatorname{Mat}\left((\pmb{I}_n\otimes \pmb{M})^{-\frac{1}{2}}\vec{\pmb{g}}\right)\\ &=\operatorname{Mat}\left(\operatorname{Vec}\left(\sqrt{n}\pmb{M}^{-\frac{1}{2}}\pmb{G}\right)\right)\\ &=\sqrt{n}\mathbb{E}[\pmb{G}\pmb{G}^T]^{-\frac{1}{2}}\pmb{G} \end{aligned}
$$

Similarly, the square-root [NGD](#page-18-8) update with F˜ = S ⊗ I<sup>m</sup> is

$$
\operatorname{Mat}\left(\tilde{F}^{-\frac{1}{2}}\vec{g}\right) = \sqrt{m}GS^{-\frac{1}{2}}
$$
\n(36)

*Proof.* This is trivial by applying the property of Kronecker product:

$$
\begin{aligned} &\mathrm{Mat}((\boldsymbol{S}\otimes\boldsymbol{I}_m)^{-\frac{1}{2}}\vec{\boldsymbol{g}})\\ &=\mathrm{Mat}(\mathrm{Vec}(\boldsymbol{G}\boldsymbol{S}^{-\frac{1}{2}}))\\=&\boldsymbol{G}\boldsymbol{S}^{-\frac{1}{2}} \end{aligned}
$$

#### <span id="page-26-2"></span><span id="page-26-0"></span>C.3 Update formula for [Eigen-Adam](#page-18-5)

*Proof.* From the Theorem [3.2,](#page-4-5) we can apply the properties of block diagonal and Kronecker product with a full-rank U:

$$
\operatorname{Mat}(\tilde{F}^{-\frac{1}{2}}\vec{g})
$$
\n
$$
= \operatorname{Mat}\left(\operatorname{Diag}_{B}\left(M_{1}^{-12},...,M_{n}^{-\frac{1}{2}}\right)\vec{g}\right)
$$
\n
$$
= \operatorname{Mat}\left(\operatorname{Diag}_{B}\left(UD_{1}^{-\frac{1}{2}}U^{T},...,UD_{n}^{-\frac{1}{2}U^{T}}\right)\vec{g}\right)
$$
\n
$$
= \operatorname{Mat}\left((I_{n} \otimes U)\operatorname{Diag}_{B}(\sqrt{D_{1}},..., \sqrt{D_{n}})(I \otimes U^{T})\vec{g}\right)
$$
\n
$$
= \operatorname{Mat}\left((I_{n} \otimes U)\operatorname{Diag}_{B}(\sqrt{D_{1}},..., \sqrt{D_{n}})\operatorname{Vec}\left(U^{T}G\right)\right)
$$
\n
$$
= \operatorname{Mat}\left((I_{n} \otimes U)\operatorname{Vec}\left(\frac{U^{T}G}{\sqrt{\mathbb{E}[(U^{T}G)^{\odot 2}]}}\right)\right)
$$
\n
$$
= \operatorname{Mat}\left(\operatorname{Vec}\left(U\frac{U^{T}G}{\sqrt{\mathbb{E}[(U^{T}G)^{\odot 2}]}}\right)\right)
$$
\n
$$
= U\frac{U^{T}G}{\sqrt{\mathbb{E}[(U^{T}G)^{\odot 2}]}}
$$

#### <span id="page-26-1"></span>C.4 Update formula for SOAP

Based on the Theorem [3.3,](#page-5-3) we can derive the update formula of the corresponding square-root [NGD](#page-18-8) following the same procedure as [Eigen-Adam:](#page-18-5)

$$
\mathrm{Mat}\left(\tilde{\pmb{F}}^{-\frac{1}{2}}\vec{\pmb{g}}\right)=\pmb{U}_L\frac{\pmb{U}_L^T\pmb{G}\pmb{U}_R}{\sqrt{\mathbb{E}[(\pmb{U}_L^T\pmb{G}\pmb{U}_R)^{\odot 2}]}}\pmb{U}_R^T.
$$

*Proof.*

Mat 
$$
(\tilde{F}^{-\frac{1}{2}}\tilde{g})
$$
  
\n
$$
= \text{Mat } ((U_R \otimes U_L) \text{ Diag}_M(\mathbb{E}[(U_L^T G U_R)^{\odot 2}])^{-\frac{1}{2}} (U_R \otimes U_L)^T \tilde{g})
$$
\n
$$
= \text{Mat } ((U_R \otimes U_L) \text{ Diag}_M(\mathbb{E}[(U_L^T G U_R)^{\odot 2}])^{-\frac{1}{2}} \text{Vec } (U_L^T G U_R))
$$
\n
$$
= \text{Mat } ((U_R \otimes U_L) \text{ Vec } \left( \frac{U_L^T G U_R}{\sqrt{\mathbb{E}[(U_L^T G U_R)^{\odot 2}]}} \right)
$$
\n
$$
= \text{Mat } \left( \text{Vec } \left( U_L \frac{U_L^T G U_R}{\sqrt{\mathbb{E}[(U_L^T G U_R)^{\odot 2}]}} U_R^T \right) \right)
$$
\n
$$
= U_L \frac{U_L^T G U_R}{\sqrt{\mathbb{E}[(U_L^T G U_R)^{\odot 2}]}} U_R^T
$$

Therefore, one can design the optimizer based on this update formula and exactly recovers the SOAP's procedure (Eq. [\(29\)](#page-21-2) in App. [B.5\)](#page-20-3).

# <span id="page-27-0"></span>D Theory and proof

To prove the results, we need to first introduce some useful lemmas and inequalities.

Lemma 1. *Assume* F˜ *is a block diagonal matrix with* n *squared block matrix* M<sup>i</sup> ∈ R <sup>m</sup>×m*, then*

<span id="page-27-1"></span>
$$
\min_{\tilde{F}} \|\tilde{F} - F\|_{F}^{2} = \min_{\{M_{i}\}_{i=1}^{n}} \sum_{i=1}^{n} \|M_{i}\|_{F}^{2} - 2 \operatorname{Tr}(M_{i}^{T} \mathbb{E}[g_{i} g_{i}^{T}]) + C
$$
\n(37)

*where* g<sup>i</sup> *is the* i *th column of gradient* G*,* C *is a constant that is idenpendent of* F˜*, and* F *is the [FIM.](#page-18-0)*

*Proof.* This is straightforward by expanding the [Frobenius norm \(F-norm\).](#page-18-13)

$$
\begin{aligned} &\|\tilde{\boldsymbol{F}}-\boldsymbol{F}\|_F^2\\&=\text{Tr}\left((\tilde{\boldsymbol{F}}-\boldsymbol{F})^T(\tilde{\boldsymbol{F}}-\boldsymbol{F})\right)\\=&\|\tilde{\boldsymbol{F}}\|_F^2-2\,\text{Tr}\left(\tilde{\boldsymbol{F}}^T\boldsymbol{F}\right)+C\\=&\sum_{l=1}^{mn}\tilde{\boldsymbol{F}}_{l,:}^T\tilde{\boldsymbol{F}}_{:,l}-\tilde{\boldsymbol{F}}_{l,:}^T\boldsymbol{F}_{:,l}+C\\=&\sum_{i=1}^n\|\boldsymbol{M}_i\|_F^2-2\,\text{Tr}\left(\boldsymbol{M}_i^T\mathbb{E}[\boldsymbol{g}_i\boldsymbol{g}_i^T]\right)+C\end{aligned}
$$

where F˜ l,: ∈ R mn indicates the l th row vector of F˜ and F˜ :,l is the l th column vector. The last equation is obtained by the fact that F˜ is a block diagonal matrix. So only the values of F at the position of non-zero values F˜ contributes to the trace, which is exactly the outer product: E[gig T i ].

Lemma 2 (Powers-Stormer inequality). *For positive semi-definite operator* A*,* B*, we have the following inequality*

<span id="page-27-2"></span>
$$
\text{Tr}((A - B)^{T}(A - B)) \leq \|A^{2} - B^{2}\|_{1}
$$
\n(38)

*where* ∥ · ∥<sup>1</sup> *is the trace norm.*

#### D.1 Proof of Proposition [1](#page-3-6)

*Proof.* From Lemma [1,](#page-27-1) we have

$$
\|\tilde{F} - F\|_F^2
$$
  
=  $\sum_{i=1}^n \|M_i\|_F^2 - 2 \text{Tr} (M_i^T \mathbb{E}[g_i g_i^T])$   
=  $\sum_{i=1}^n \sum_{j=1}^m M_{i,jj}^2 - 2M_{i,jj} \mathbb{E}[g_{i,j}^2]$ 

By taking the derivative w.r.t Mi,jj , we have

$$
M_{i,jj} = \mathbb{E}[g_{i,j}^2]
$$

Thus, we have F˜ = Diag(E[⃗g 2 ]).

#### D.2 Proof of Theorem [3.1](#page-3-4)

To prove this theorem, we need to leverage the Proposition [2](#page-4-1) for generalized whitening (Eq. [\(7\)](#page-4-2)) in Sec. [3.3.](#page-3-3) This is proved in App. [D.3.](#page-30-0) But in the following, we will provide an alternative proof for completeness.

<span id="page-28-0"></span>*Proof.* From Lemma [1,](#page-27-1) we have

$$
\begin{aligned} & \|\tilde{\pmb{F}}-\pmb{F}\|_F^2 \\ =& \sum_{i=1}^n \| \pmb{M}\|_F^2 - 2 \operatorname{Tr}(\pmb{M}^T \mathbb{E}[\pmb{g}_i \pmb{g}_i^T]) + C \\ =& n \|\pmb{M}\|_F^2 - 2 \operatorname{Tr}(\pmb{M}^T \mathbb{E}[\sum_{i=1}^n \pmb{g}_i \pmb{g}_i^T]) + C \\ =& n \|\pmb{M}\|_F^2 - 2 \operatorname{Tr}(\pmb{M}^T \mathbb{E}[\pmb{G} \pmb{G}^T]) + C \end{aligned}
$$

To minimize this, we take the derivative w.r.t. M, we have

$$
2n\mathbf{M} - 2\mathbb{E}[\mathbf{G}\mathbf{G}^T] = 0 \Rightarrow \mathbf{M} = \frac{1}{n}\mathbb{E}[\mathbf{G}\mathbf{G}^T]
$$

Next, we prove another proposition that is "symmetric" to the whitening results in Proposition [2.](#page-4-1) Proposition 5. *Assume* H = {R<sup>n</sup> ⊗ Im}*, where* R<sup>n</sup> ∈ R <sup>n</sup>×<sup>n</sup> *is [SPD](#page-18-10) matrix, then Eq.* [\(2\)](#page-2-1) *can be analytically solved with the optimal solution as*

<span id="page-28-1"></span>
$$
\boldsymbol{R}_n^* = \frac{1}{m} \mathbb{E}[\boldsymbol{G}^T \boldsymbol{G}] \tag{39}
$$

*Proof.* Since R<sup>n</sup> ⊗ I<sup>m</sup> does not have a nice block diagonal structure like the previous proposition, we need to analyze it a bit more. First, we have

$$
\begin{aligned}&\|\boldsymbol{R}_n \otimes \boldsymbol{I}_m - \boldsymbol{F}\|_F^2 \\ =& \|\boldsymbol{R}_n \otimes \boldsymbol{I}_m\|_F^2 - 2\operatorname{Tr}\left(\underbrace{(\boldsymbol{R}_n \otimes \boldsymbol{I}_m)^T\mathbb{E}[\vec{g}\vec{g}^T]}_{\boldsymbol{Z}}\right) + C \end{aligned}
$$

Since we only care about the diagonal of Z, therefore, we only inspect the block diagonal of Z with each block Z<sup>i</sup> of size R <sup>m</sup>×<sup>m</sup>, and i = 1, . . . , n. By basic algebra, we have

$$
\pmb{Z}_i = \sum_{k=1}^n R_{ik}\pmb{g}_k\pmb{g}_i^T
$$

where g<sup>k</sup> is the k th column of G. Therefore, we can simplify the trace of Z as

$$
\operatorname{Tr}(\boldsymbol{Z}) = \sum_{i=1}^{n} \operatorname{Tr}(\boldsymbol{Z}_{i})
$$
  
= 
$$
\operatorname{Tr}(\sum_{i=1}^{n} \sum_{k=1}^{n} R_{ij} \boldsymbol{g}_{k} \boldsymbol{g}_{i}^{T})
$$
  
= 
$$
\sum_{i=1}^{n} \sum_{k=1}^{n} \sum_{j=1}^{m} R_{ik} [\boldsymbol{G}]_{ji} [\boldsymbol{G}^{T}]_{kj}
$$

where [G]ji is the element of G at j th row and i th column.

Now, let's perform the same analysis of the following quantity

$$
\text{Tr}\left( (\boldsymbol{I}_m \otimes \boldsymbol{R}_n) \mathbb{E} [ \overrightarrow{[\boldsymbol{G}^T]} \overrightarrow{[\boldsymbol{G}^T]}^T ] \right)
$$

where −−→ [G<sup>T</sup> ] is the vectorized transposed gradient G<sup>T</sup> . Namely, it now stacks the rows of G instead of columns of G like ⃗g. This object is simple to treat due to its block diagonal structure, by algebric manipulation, we have

$$
\operatorname{Tr}\left((\boldsymbol{I}_m \otimes \boldsymbol{R}_n)\mathbb{E}[\overrightarrow{[\boldsymbol{G}^T]} \overrightarrow{[\boldsymbol{G}^T]}^T]\right) = \sum_{\substack{k=1 \ \text{over blocks}}}^m \operatorname{Tr}(R_{ij} \underbrace{[\boldsymbol{G}^T]_k}_{\text{kth column of } \boldsymbol{G}^T} [\boldsymbol{G}^T]_k^T)
$$
\n
$$
= \sum_{k=1}^m \sum_{i=1}^n \sum_{j=1}^n R_{ij} [\boldsymbol{G}^T]_{jk} [\boldsymbol{G}]_{ki}
$$

Now, let's change the variable i = i, j = k and k = j, the above becomes

$$
\operatorname{Tr}\left((\boldsymbol{I}_m \otimes \boldsymbol{R}_n)\mathbb{E}[[\overrightarrow{\boldsymbol{G}}^T][\overrightarrow{\boldsymbol{G}}^T]^T]\right)
$$
\n
$$
=\sum_{j=1}^m \sum_{i=1}^n \sum_{k=1}^n R_{ik}[\boldsymbol{G}^T]_{kj}[\boldsymbol{G}]_{ji}
$$
\n
$$
=\operatorname{Tr}(\boldsymbol{Z})
$$
\n(40)

We should also note that

<span id="page-29-0"></span>
$$
\begin{aligned} &\| \bm{R}_n \otimes \bm{I}_m \|_F^2 \\&= \text{Tr}\left( (\bm{R}_n \otimes \bm{I}_m)^T (\bm{R}_n \otimes \bm{I}_m) \right) \\&= \text{Tr}\left( (\bm{R}_n^T \bm{R}_n) \otimes \bm{I}_m \right) \\&= \text{Tr}(\bm{R}_n^T \bm{R}_n) \, \text{Tr}(\bm{I}_m) \\&= \text{Tr}\left( (\bm{I}_m \otimes \bm{R}_n)^T (\bm{I}_m \otimes \bm{R}_n) \right) \\&= \| (\bm{I}_m \otimes \bm{R}_n) \|_F^2 \end{aligned}
$$

Therefore, by using the above equation and Eq. [\(40\)](#page-29-0), the original minimization problem is translated to

$$
\argmin_{\boldsymbol{R}_n} \|\boldsymbol{R}_n \otimes \boldsymbol{I}_m - \boldsymbol{F}\|_F^2 = \argmin_{\boldsymbol{R}_n} \|\boldsymbol{I}_m \otimes \boldsymbol{R}_n - \mathbb{E}[\overrightarrow{[\boldsymbol{G}^T]} \overrightarrow{[\boldsymbol{G}^T]}^T]\|_F^2
$$

Thus, we can leverage Proposition [2](#page-4-1) to obtain the optimal solution

$$
\boldsymbol{R}_n^* = \frac{1}{m} \mathbb{E}[\boldsymbol{G}^T \boldsymbol{G}]
$$

With the above two propositions, we can start to prove Theorem [3.1.](#page-3-4)

*Proof.* First, we note that

$$
\|R_n^{\frac{1}{2}}\otimes L_m^{\frac{1}{2}}-F\|_F^2\\=\|\underbrace{(R_n\otimes I_m)^{\frac{1}{2}}}_{A}\underbrace{(I_n\otimes L_m)^{\frac{1}{2}}}_{B}-\underbrace{\mathbb{E}[\vec{g}\vec{g}^T]^{\frac{1}{2}}}_{C}\mathbb{E}[\vec{g}\vec{g}^T]^{\frac{1}{2}}\|_F^2\\=\|AB-CC\|_F^2
$$

Next, we will upper bound this quantity. First, we have

AB − CC = A(B − C) + (A − C)C

By triangular inequality, we have

$$
\|AB - CC\|_F
$$
  
\n
$$
\leq \|A(B - C)\|_F + \|(A - C)C\|_F
$$
  
\n
$$
\leq \|A\|_F \|B - C\|_F + \|A - C\|_F \|C\|_F
$$
  
\n
$$
\leq (\|A - C\|_F + \|C\|_F) \|B - C\|_F + \|A - C\|_F \|C\|_F
$$
  
\n
$$
= \|A - C\|_F \|B - C\|_F + \|C\|_F (\|B - C\|_F + \|A - C\|_F)
$$

<span id="page-30-2"></span>Now, the squared norm can be upper bounded by

$$
\|AB - CC\|_F^2 \le 3 \left( \|A - C\|_F^2 \|B - C\|_F^2 + \|C\|_F^2 \|A - C\|_F^2 + \|C\|_F^2 \|B - C\|_F^2 \right) \\ \le 3 \left( mn \|A^2 - C^2\|_F \|B^2 - C^2\|_F + \sqrt{mn} \|C\|_F^2 \|A^2 - C^2\|_F + \sqrt{mn} \|C\|_F^2 \|B^2 - C^2\|_F \right) \tag{41}
$$

The first inequality is obtained by the fact that for any three matrix P , Q and H, we have

$$
\begin{aligned}\n||\boldsymbol{P} + \boldsymbol{Q} + \boldsymbol{H}||_F^2 &\leq (||\boldsymbol{P}||_F + ||\boldsymbol{Q}||_F + \|\boldsymbol{H}\|_F)^2 \\
&= ||\boldsymbol{P}||_F^2 + ||\boldsymbol{Q}||_F^2 + ||\boldsymbol{H}||_F^2 + 2||\boldsymbol{P}||_F||\boldsymbol{Q}||_F + 2||\boldsymbol{P}||_F||\boldsymbol{H}||_F + 2||\boldsymbol{Q}||_F||\boldsymbol{H}||_F \\
&\leq 3 (||\boldsymbol{P}||_F^2 + ||\boldsymbol{Q}||_F^2 + ||\boldsymbol{H}||_F^2)\n\end{aligned}
$$

The second inequality is obtained by directly applying Powers-Stormer's inequality and Holder's inequality. For completeness, we will show how to upper-bound ∥A − C∥ 2 F , the rest can be bounded in the same way. From Lemma [2](#page-27-2) and both A, C are [SPD](#page-18-10) matrix, we have

<span id="page-30-3"></span>
$$
\|\bm{A}-\bm{C}\|_F^2 \leq \|\bm{A}^2 - \bm{C}^2\|_1
$$

Then, we can select p = q = 2 for Holder's inequaity and obtain

$$
\|\bm{A}^2 - \bm{C}^2\|_1 \leq \sqrt{mn} \|\bm{A}^2 - \bm{C}^2\|_F
$$

where <sup>√</sup> mn comes from the ∥Imn∥<sup>F</sup> in Holder's inequality. By substitute it back, we obtain the upper bound.

We can see that minimizing the upper bound Eq. [\(41\)](#page-30-3) is equivalent to minimize each ∥A<sup>2</sup> − C2∥<sup>F</sup> , ∥B<sup>2</sup> − C2∥<sup>F</sup> individually, and

$$
\begin{aligned} \|A^2-C^2\|_F &= \|{\bm R}_n \otimes {\bm I}_m - {\bm F}\|_F \\ \|B^2-C^2\|_F &= \|{\bm I}_n \otimes {\bm L}_m - {\bm F}\|_F \end{aligned}
$$

Thus, from Proposition [2](#page-4-1) and Proposition [5,](#page-28-1) we prove the theorem.

#### <span id="page-30-0"></span>D.3 Proof of Proposition [2](#page-4-1) and Proposition [3](#page-6-2)

Instead of proving the Proposition [2,](#page-4-1) we propose a generalization to those gradient operations, where Proposition [2](#page-4-1) is a special case.

Structure assumption We consider H = {S ⊗ M} with identical [SPD](#page-18-10) M ∈ R <sup>m</sup>×<sup>m</sup> and positive diagonal S ∈ R <sup>n</sup>×<sup>n</sup>. The following theorem proves that the optimal solution can be solved by a fixed-point iteration.

Theorem D.1. *Assuming* H = {S ⊗ M} *with positive diagonal* S ∈ R <sup>n</sup>×<sup>n</sup> *and [SPD](#page-18-10)* M ∈ R <sup>m</sup>×m*, and* EGG′ [(G<sup>T</sup> G′ ) ⊙2 ] *contains positive values, solving Eq.* [\(2\)](#page-2-1) *admits a fixed point procedure:*

$$
\text{Diag}(\boldsymbol{S}) = \frac{\text{Diag}(\mathbb{E}[\boldsymbol{G}^T \boldsymbol{M} \boldsymbol{G}])}{\|\boldsymbol{M}\|_F^2}, \quad \boldsymbol{M} = \frac{\mathbb{E}[\boldsymbol{G}\boldsymbol{S}\boldsymbol{G}^T]}{\|\boldsymbol{S}\|_F^2}.
$$
 (42)

*The solution* Diag(S ∗ ) *converges to the principal eigenvector of* E[(G<sup>T</sup> G′ ) ⊙2 ] *up to a scaling with unique* S <sup>∗</sup> ⊗ M<sup>∗</sup> *.*

To prove Theorem [D.1,](#page-30-1) we first introduce some classic results.

<span id="page-30-4"></span>Theorem D.2 (Perron-Frobenius theorem). *For a matrix* A ∈ R <sup>n</sup>×<sup>n</sup> *with positive entries, the principal eigenvalue* r *is positive, called Perron-Frobenius eigenvalue. The corresponding eigenvector* v *of* A *is called Perron vector and only contains positive components:* Av = rv *with* v<sup>i</sup> > 0*. In addition, there are no other positive eigenvectors of* A*.*

Definition D.3 (Hilbert projective metric). For any given vectors v, w in C/{0} where C is a closed convex pointed non-negative cone C, i.e. C ∩(−C) = {0}, the Hilbert projective metric is defined as

$$
d_H(\boldsymbol{v}, \boldsymbol{w}) = \log \left( \max_i \frac{v_i}{w_i} \right) - \log \left( \min_i \frac{v_i}{w_i} \right)
$$

<span id="page-30-1"></span>

This is a pseudo metric since it has a scaling invariance property: dH(v, αm) = dH(v,m) for α > 0. This means dH(v,m) = 0 does not mean v = m but v = αm with some positive scaling α. However, this is a metric on the space of rays inside the cone.

<span id="page-31-0"></span>Theorem D.4 (Birkhoff-Hopf theorem). *Let* P ∈ R <sup>n</sup>×<sup>n</sup> *be a positive matrix and let*

$$
\kappa(\boldsymbol{P}) = \inf \left\{\alpha \geq 0: d_H(\boldsymbol{P} \boldsymbol{x}, \boldsymbol{P} \boldsymbol{y}) \leq \alpha d_H(\boldsymbol{x}, \boldsymbol{y}), \forall \boldsymbol{x}, \boldsymbol{y} \in C_+, \boldsymbol{x} \sim \boldsymbol{y}\right\}
$$

*where* C<sup>+</sup> *is the cone that each element is non-negative and* ∼ *is the induced equivalence relation. Namely, if* x ∼ y*, there exists* α, β > 0 *such that* αx < y < βx*, and* x < y *means* y − x ∈ C+*. Then, it holds*

$$
\kappa(\boldsymbol{P}) = \tanh\frac{1}{4}\Delta(\boldsymbol{P}) \quad \text{with } \Delta(\boldsymbol{P}) = \max_{i,j,k,l} \frac{P_{ij}P_{kl}}{P_{il}P_{kj}}
$$

This theorem suggests that when P is a positive matrix, the corresponding linear mapping is contractive since tanh(·) ≤ 1 under Hilbert projective metric.

Now, let's prove the Theorem [D.1.](#page-30-1)

*Proof.* First, we can simplify the Eq. [\(2\)](#page-2-1) using Lemma [1:](#page-27-1)

$$
\begin{aligned} &\| \boldsymbol{S} \otimes \boldsymbol{M} - \boldsymbol{F} \|^2_F \\ =& \sum_{i=1}^n S_i^2 \| \boldsymbol{F} \|^2_F - 2 \operatorname{Tr}(S_i \boldsymbol{M} \mathbb{E}[\boldsymbol{g}_i \boldsymbol{g}_i^T]) + C \end{aligned}
$$

Then, we simply take its derivative w.r.t. s<sup>i</sup> , and obtain

$$
2S_i||M||_F^2 = 2 \operatorname{Tr}(M \mathbb{E}[g_i g_i^T])
$$

$$
\implies S_i = \frac{\operatorname{Tr}(M \mathbb{E}[g_i g_i^T])}{\|M\|_F^2}
$$

$$
\implies \operatorname{Diag}(S) = \frac{\operatorname{Diag}\left(\mathbb{E}[G^T M G]\right)}{\|M\|_F^2}
$$

Similarly, we have

$$
\begin{aligned} \boldsymbol{M} = &\frac{\sum_{i=1}^{n} S_i \mathbb{E}[\boldsymbol{g}_i \boldsymbol{g}_i^T]}{\|\boldsymbol{S}\|_F^2} \\ = &\frac{\mathbb{E}[\boldsymbol{G}\boldsymbol{S}\boldsymbol{G}^T]}{\|\boldsymbol{S}\|_F^2} \end{aligned}
$$

These define an iterative procedure. Next, we will show it converges. Let's substitute M into S, and obtain

$$
S = \text{Diag}\left(\mathbb{E}_{G}\left[G^{T}\mathbb{E}_{G'}[G'SG^{'}{}^{T}]G\right]\right)\alpha(S)
$$

$$
= \text{Diag}\left(\mathbb{E}_{GG'}\left[\underbrace{GG'^{T}}_{H}SG^{'}{}^{T}G\right]\right)
$$

where α(S) is the scaling term. In the following, we use E as EGG′ . Since we can show

$$
S_i = \mathbb{E}\left[\sum_j^n S_j\right],
$$

we can write S in its vector format:

$$
s = \underbrace{\mathbb{E}\left[H^{\odot 2}\right]}_{P} s.
$$

<span id="page-32-0"></span>From the assumption, we know P contains only positive values, let's define a quotient space for positive vectors s and q under the equivalence relation s ∼ s ′ if s = αs ′ for some positive scaling α. Namely, we define a space of rays inside the positive cone. Therefore, the Hilbert projective metric becomes a real metric inside the quotient space.

From the Theorem [D.4,](#page-31-0) we know the linear mapping associated with P is contractive. Therefore, we can follow the proof of Banach fixed point theorem on the previously defined quotient space with Hilbert projective metric to show the convergence of this fixed point iteration on s.

Now, we show the solution s ∗ is always positive. Since it is converging, therefor, the solution satisfies

$$
\boldsymbol{s}^* = \alpha(\boldsymbol{s}^*) \boldsymbol{P} \boldsymbol{s}^*
$$

This is equivalent to finding the eigenvectors of P . By leveraging Perron-Frobenius theorem (Theorem [D.2\)](#page-30-4), we know s ∗ is the principal eigenvector of P , and only contain positive values. It is also easy to verify that this fixed point converges upto a positive scaling factor (this is expected since the contractive mapping holds true for the quotient space with Hilbert metric, that is invariant to scaling.)

Although s ∗ is not unique, but S ⊗ M is, since for arbitrary positive scaling β

$$
\begin{aligned} \boldsymbol{s}^{'*} &= \beta \boldsymbol{s}^* \Longrightarrow \boldsymbol{M}^{'*} = \frac{1}{\beta} \frac{\mathbb{E}[\boldsymbol{G} \boldsymbol{S}^* \boldsymbol{G}^T]}{\|\boldsymbol{s}\|_2^2} \\ \Longrightarrow \boldsymbol{S}^{'*} \otimes \boldsymbol{M}^{'*} &= \boldsymbol{S}^* \otimes \boldsymbol{M}^* \end{aligned}
$$

Therefore, Proposition [2](#page-4-1) is a direct consequence by substituting F˜ = I<sup>n</sup> ⊗ M and F˜ = S ⊗ I<sup>m</sup> into Eq. [\(21\)](#page-8-3).

Next, we prove Proposition [3.](#page-6-2)

*Proof.* From the Theorem [D.1,](#page-30-1) the iterative procedure for Q can be simply obtained by taking the diagonals of M:

$$
\boldsymbol{Q} = \frac{\text{Diag}\left(\mathbb{E}\left[\boldsymbol{G}\boldsymbol{S}\boldsymbol{G}^{T}\right]\right)}{\|\boldsymbol{S}\|_{F}^{2}}.
$$

Following the same proof strategy of Theorem [D.1,](#page-30-1) we substitute Q into the update of S and re-write it into the vector format. First, let's rewrite the update of S

$$
S_i \propto \mathbb{E}[\sum_{j=1} G_{ji}^2 Q_j]
$$

$$
\Longrightarrow s = \frac{\mathbf{P}^T \mathbf{q}}{\|\mathbf{q}\|_2^2}
$$

where P = E[G<sup>⊙</sup><sup>2</sup> ]. Similarly, q = P s ∥s∥ 2 2 . Thus,

$$
\boldsymbol{s} = \alpha(\boldsymbol{s}) \boldsymbol{P}^T \boldsymbol{P} \boldsymbol{s}
$$

From the assumption P contains only positive values, we can follow the exact same argument made in Theorem [D.1](#page-30-1) to show the convergence of this fixed point update and the positivity of the final solution s ∗ . Precisely, s ∗ and q ∗ are the right and left principal singular vectors of P , respectively, and S <sup>∗</sup> ⊗ Q<sup>∗</sup> are unique.

#### D.4 Proofs of [Eigen-Adam](#page-18-5)

#### D.4.1 Proof of Theorem [3.2](#page-4-5)

*Proof.* For simplicity, we omit the subscript f in U<sup>f</sup> . If we assume all D<sup>i</sup> are equal and only contain positive values, then each block UDiU<sup>T</sup> are the same for all i, and it is [SPD](#page-18-10) matrix. Then, to minimize the the loss Eq. [\(2\)](#page-2-1), we can directly leverage the whitening results in Proposition [2,](#page-4-1) and

obtain M<sup>∗</sup> = E[GG<sup>T</sup> ]. Due to the structure of UDU<sup>T</sup> , the optimal U<sup>∗</sup> is exactly the eigen-matrix of M<sup>∗</sup> .

Next, we prove for any fixed U, we can find the corresponding optimal D<sup>i</sup> . From the block diagonal structure and Lemma [1,](#page-27-1) we have

$$
\|\tilde{F} - F\|_{F}^{2}
$$
\n
$$
= \sum_{i=1}^{n} \|UD_{i}U^{T}\|_{F}^{2} - 2 \operatorname{Tr} (U^{T}\mathbb{E}[g_{i}g_{i}^{T}]UD_{i}) + C
$$
\n
$$
= \sum_{i=1}^{n} \|D_{i}\|_{F}^{2} - 2 \operatorname{Tr} \left( U^{T}\mathbb{E}[g_{i}g_{i}^{T}]UD_{i} \right) + C
$$
\n
$$
= \sum_{i=1}^{n} \sum_{j=1}^{m} D_{i,jj}^{2} - 2 \sum_{i=1}^{n} \sum_{j=1}^{m} D_{i,jj}u_{j}^{T}H_{i}u_{j} + C
$$

Taking the derivative w.r.t. Di,jj , we can find the optimal Di,jj is

$$
\begin{aligned} D^*_{i,jj}=&\bm{u}_j^T\bm{H}_i\bm{u}_j\\ =&\mathbb{E}[(\bm{u}_j^T\bm{g}_i)^2] \end{aligned}
$$

Now, by simple algebra manipulation, we have

$$
\boldsymbol{D}_i^* = \mathrm{Diag}_{\mathrm{v}}(\mathbb{E}[(\boldsymbol{U}^T\boldsymbol{g}_i)^2])
$$

where Diag<sup>M</sup> is to expand the vector to a diagonal matrix. Finally, for <sup>D</sup>˜ , we have

$$
\tilde{\mathbf{D}} = \text{Diag}_{\mathbf{M}}(\mathbb{E}[(\mathbf{U}^T \mathbf{G})^{\odot 2}])
$$
\n(43)

The optimality of <sup>D</sup><sup>e</sup> can also be obtained by leveraging the Lemma 1 in [\[George et al., 2018\]](#page-15-11), and set the eigenbasis as I<sup>n</sup> ⊗ U.

#### D.5 Proof of Proposition [4](#page-7-2)

*Proof.* Within the time block i + 1 with low-rank mapping U, the gradient at each step can be decomposed as

$$
G_t = \underbrace{UU^T G_t}_{\widetilde{G_t}} + \underbrace{(G_t - UU^T G_t)}_{R_t}
$$

Therefore, the true state Q<sup>∗</sup> (i+1)k can be simplified as

$$
Q_{(i+1)k} = \sum_{t=i k+1}^{(i+1)k} G_t G_t^T
$$
  
= 
$$
\sum_{t=i k+1}^{(i+1)k} (\widetilde{G}_t + R_t) (\widetilde{G}_t + R_t)^T
$$
  
= 
$$
\sum_{t=i k+1}^{(i+1)k} \widetilde{G}_t \widetilde{G}_t^T + \widetilde{\underline{G}}_t R_t^T + \underbrace{R_t \widetilde{G}_t^T}_{0} + R_t R_t^T
$$

The third equality is obtained because we assume GtG<sup>T</sup> t shares the same eigen-basis as Q<sup>∗</sup> ik. Namely,

$$
\begin{aligned} \boldsymbol{G}_t\boldsymbol{G}_t^T = & [\boldsymbol{U},\boldsymbol{U}_c]\left[\begin{array}{cc} \boldsymbol{A}_t & 0 \\ 0 & \boldsymbol{\Sigma}_t \end{array}\right]\left[\begin{array}{c} \boldsymbol{U}^T \\ \boldsymbol{U}_c^T \end{array}\right] \\ = & \boldsymbol{U}\boldsymbol{A}_t\boldsymbol{U}^T + \boldsymbol{U}_c\boldsymbol{\Sigma}_t\boldsymbol{U}_c^T \end{aligned}
$$

where A<sup>t</sup> and Σ<sup>t</sup> are diagonal matrix. Then, we have

$$
\tilde{G}_t R_t^T
$$
\n
$$
= U U^T G_t (U_c U_c^T G_t)^T
$$
\n
$$
= U U^T (U A_t U^T + U_c \Sigma_t U_c^T) U_c U_c^T
$$
\n
$$
= U A_t \underbrace{U^T U_c}_{0} U_c^T + U \underbrace{U^T U_c}_{0} \Sigma_t U_c^T U_c U_c^T
$$
\n
$$
= 0
$$

In addition, we can also simplify

$$
\begin{aligned} &\boldsymbol{R}_t \boldsymbol{R}_t^T \\ =& \boldsymbol{U}_c \boldsymbol{U}_c^T \boldsymbol{G}_t \boldsymbol{G}_t^T \boldsymbol{U}_c \boldsymbol{U}_c^T \\ =& \boldsymbol{U}_c \boldsymbol{U}_c^T (\boldsymbol{U} \boldsymbol{A}_t \boldsymbol{U}^T + \boldsymbol{U}_c \boldsymbol{\Sigma}_t \boldsymbol{U}_c^T) \boldsymbol{U}_c \boldsymbol{U}_c^T \\ =& \boldsymbol{U}_c \boldsymbol{\Sigma}_t \boldsymbol{U}_c^T \end{aligned}
$$

Therefore,

$$
\boldsymbol{Q}^*_{(i+1)k} = \sum_{t=i k+1}^{(i+1)k} \widetilde{\boldsymbol{G}}_t \widetilde{\boldsymbol{G}}_t^T + \boldsymbol{U}_c \boldsymbol{\Sigma}_t \boldsymbol{U}_c^T
$$

### D.6 Proof of Theorem [5.1](#page-8-3)

*Proof.* For simplicity, we ignore the subscript t for the following proof. First, we let O = S <sup>−</sup><sup>2</sup> Then, the loss function can be written as

$$
\|O \otimes U_c U_c^T - \tilde{F}_c\|_F^2
$$
  
= 
$$
\sum_{i=1}^n \|O_{ii} U_c U_c^T\|_F^2 - 2 \operatorname{Tr}((O_{ii} U_c U_c^T)^T (U_c M_i U_c^T))
$$
  
= 
$$
\sum_{i=1}^n \|O_{ii} U_c U_c^T\|_F^2 - 2 \operatorname{Tr}(O_{ii} M_i)
$$
  
= 
$$
\sum_{i=1}^n \sum_{k=1}^{m-r} \sum_{j=1}^m O_{ii}^2 U_{c,jk}^2 - 2 \operatorname{Tr}(O_{ii} M_i)
$$

where M<sup>i</sup> = Diag(E[(U<sup>T</sup> <sup>c</sup> gi) 2 ]), g<sup>i</sup> is the i th column of G, and Uc,jk is the element in j th row, k th column of Uc. Then, we take the derivative w.r.t. Oii, and we have

$$
2O_{ii} \sum_{k=1}^{m-r} \sum_{j=1}^{m} U_{c,jk}^{2} = 2 \sum_{k=1}^{m-r} \mathbb{E}[(\boldsymbol{U}_{c}^{T} \boldsymbol{g}_{i})_{k}^{2}]
$$

$$
\Longrightarrow O_{ii} = \frac{\mathbb{E}[\sum_{k=1}^{m-r} (\boldsymbol{U}_{c}^{T} \boldsymbol{g}_{i})_{k}^{2}]}{m-r}
$$

This form still requires the access to Uc. Next, let's simplify it. First, let U˜ = [U, Uc] to be the complete basis, we can show

$$
\sum_{k=1}^{m} (\tilde{\boldsymbol{U}}^T \boldsymbol{g}_i)_k^2
$$
\n
$$
= \text{Tr}((\tilde{\boldsymbol{U}}^T \boldsymbol{g}_i)^T (\tilde{\boldsymbol{U}}^T \boldsymbol{g}_i))
$$
\n
$$
= \text{Tr}(\boldsymbol{g}_i^T \tilde{\boldsymbol{U}} \tilde{\boldsymbol{U}}^T \boldsymbol{g}_i)
$$
\n
$$
= \boldsymbol{g}_i^T \boldsymbol{g}_i
$$

Now, let's re-write the above in a different format:

$$
\begin{aligned} &\sum_{k=1}^{m}(\tilde{\bm{U}}^{T}\bm{g}_{i})_{k}^{2} \\ &=\text{Tr}(\bm{g}_{i}^{T}\tilde{\bm{U}}\tilde{\bm{U}}^{T}\bm{g}_{i}) \\ &=\text{Tr}(\tilde{\bm{U}}^{T}\bm{g}_{i}\bm{g}_{i}^{T}\tilde{\bm{U}}) \\ &=\text{Tr}\left(\left[\begin{array}{c} \bm{U}^{T}\\ \bm{U}_{c}^{T}\end{array}\right]\bm{g}_{i}\bm{g}_{i}^{T}[\bm{U},\bm{U}_{c}]\right) \\ &=\text{Tr}(\bm{U}\bm{U}^{T}(\bm{g}_{i}\bm{g}_{i}^{T})+\bm{U}_{c}\bm{U}_{c}^{T}(\bm{g}_{i}\bm{g}_{i}^{T})) \\ &=\text{Tr}((\bm{U}^{T}\bm{g}_{i})^{T}(\bm{U}^{T}\bm{g}_{i}))+\text{Tr}((\bm{U}_{c}^{T}\bm{g}_{i})^{T}(\bm{U}_{c}^{T}\bm{g}_{i})) \\ &=\sum_{k=1}^{r}(\bm{U}^{T}\bm{g}_{i})_{k}^{2}+\sum_{k=1}^{m-r}(\bm{U}_{c}^{T}\bm{g}_{i})_{k}^{2} \end{aligned}
$$

Therefore, we have

$$
\mathbb{E}[\sum_{k=1}^{m-r}(\boldsymbol{U}_{c}^{T}\boldsymbol{g}_{i})_{k}^{2}]=\mathbb{E}[\boldsymbol{g}_{i}^{T}\boldsymbol{g}_{i}-\sum_{k=1}^{r}(\boldsymbol{U}^{T}\boldsymbol{g}_{i})_{k}^{2}]
$$

So, we have

$$
\mathrm{Diag}(\boldsymbol{O})=\frac{\mathbb{E}[\boldsymbol{1}_m^T\boldsymbol{G}^{\odot2}-\boldsymbol{1}_r^T(\boldsymbol{U}^T\boldsymbol{G})^{\odot2}]}{m-r}
$$

and

$$
\mathrm{Diag}(\boldsymbol{D})=\frac{\sqrt{m-r}}{\sqrt{\mathbb{E}[ \boldsymbol{1}_m^T \boldsymbol{G}^{\odot 2} - \boldsymbol{1}_r^T (\boldsymbol{U}^T \boldsymbol{G}^{\odot 2} ]}}
$$

### <span id="page-35-0"></span>D.7 Proof of Theorem [3.3](#page-5-3)

*Proof.* The proof strategy is a straightforward combination of Theorem [3.1](#page-3-4) and Theorem [3.2.](#page-4-5) First, when we assume D˜ has the Kronecker product structure, one can easily write

$$
(U_R \otimes U_L)(S_R \otimes S_L)(U_R \otimes U_L)^T\\ = (U_R \otimes U_L) \left[ (S_R U_R^T) \otimes (S_L U_L^T) \right]\\ = \underbrace{(U_R S_R U_R^T)}_{\bm A} \otimes \underbrace{(U_L S_L U_L^T)}_{\bm B}
$$

Therefore the loss (Eq. [\(2\)](#page-2-1)) becomes

$$
\|\bm A\bm B-\bm C\bm C\|_F^2
$$

where C = E[⃗g⃗g T ] 1 <sup>2</sup> . This is exactly the formulation used in Theorem [3.1](#page-3-4) with R 1 2 <sup>n</sup> = URSRU<sup>T</sup> R and L 1 <sup>2</sup><sup>m</sup> = ULSLU<sup>T</sup> L .

Thus, by directly utilizing Theorem [3.1,](#page-3-4) we can see the optimal solution

$$
\begin{aligned} &\boldsymbol{U}_{R}\boldsymbol{S}_{R}^{2}\boldsymbol{U}_{R}^{T}=\mathbb{E}[\boldsymbol{G}^{T}\boldsymbol{G}] \\ &\boldsymbol{U}_{L}\boldsymbol{S}_{L}^{2}\boldsymbol{U}_{L}^{T}=\mathbb{E}[\boldsymbol{G}\boldsymbol{G}^{T}] \end{aligned}
$$

Due to the structural assumption of UR, UL, SR, SL, their corresponding optimal solution can directly obtained using eigenvalue decomposition.

<span id="page-36-1"></span>Now, let's prove the optimal D˜ with any fixed UR, UL. This is also straightforward by applying the same technique as Theorem [3.2.](#page-4-5) The loss can be written as

$$
\frac{\|\left(\boldsymbol{U}_R\otimes\boldsymbol{U}_L\right)\tilde{\boldsymbol{D}}\left(\boldsymbol{U}_R\otimes\boldsymbol{U}_L\right)^T-\boldsymbol{F}\|_F^2}{\pi^T}\\=\|\Pi\tilde{\boldsymbol{D}}\Pi^T\|_F^2-2\operatorname{Tr}\left(\Pi^T\mathbb{E}[\vec{g}\vec{g}^T]\Pi\tilde{\boldsymbol{D}}\right)+C
$$

Since it is easy to verify orthonormality of Π, i.e.Π<sup>T</sup> Π = I, the above is simplified to

$$
\begin{aligned} &\|\tilde{\bm{D}}\|_F^2-2\,\text{Tr}\left(\bm{\Pi}^T\mathbb{E}[\vec{\bm{g}}\vec{\bm{g}}^T]\bm{\Pi}\tilde{\bm{D}}\right)\\ &=\sum_{i=1}^{mn}D_{ii}^2-2\sum_{i=1}^{mn}D_{ii}[\bm{\Pi}]_i^T\mathbb{E}[\vec{\bm{g}}\vec{\bm{g}}^T][\bm{\Pi}]_i\end{aligned}
$$

where [Π]<sup>i</sup> is the i th column of matrix Π. Then, by taking the derivative, the optimal Dii:

$$
D_{ii}^* = [\Pi]_i^T \mathbb{E}[\vec{g}\vec{g}^T][\Pi]_i
$$
  
= 
$$
\mathbb{E}[(\Pi]_i^T \vec{g})^2]
$$

Therefore,

$$
\begin{aligned} \text{Diag}(\tilde{\mathbf{D}}^*) &= \mathbb{E}[(\Pi^T \vec{g})^2] \\ &= \mathbb{E}[((\mathbf{U}_R^T \otimes \mathbf{U}_L^T) \vec{g})^2] \\ &= \text{Vec}((\mathbb{E}[(\mathbf{U}_L^T \mathbf{G} \mathbf{U}_R)^{\odot 2}])) \end{aligned}
$$

$$
\Rightarrow \tilde{\boldsymbol{D}}^*=\text{Diag}_{M}((\mathbb{E}[(\boldsymbol{U}_{L}^T\boldsymbol{G}\boldsymbol{U}_{R})^{\odot2}]))
$$

# E Further discussion

#### <span id="page-36-0"></span>E.1 Connections between different structural assumptions

Here, we will make explicit connections between different structures in terms of their generality.

[Eigen-Adam](#page-18-5) generalizes Adam Since the structure behind [Eigen-Adam](#page-18-5) is DiagB(UD1U<sup>T</sup> , . . . , UDnU<sup>T</sup> ), when constraining U = Im, the resulting structural is pure diagonal matrix DiagB(D1, . . . , Dn). This coincide with the pure diagonal structure behind Adam.

[Eigen-Adam](#page-18-5) generalizes S ⊗ M [Eigen-Adam](#page-18-5) not only extends Adam, but also generalizes the structure considered in Theorem [D.1.](#page-30-1) Consider setting D<sup>i</sup> = SiD, then we have

$$
\boldsymbol{U}\boldsymbol{D}_i\boldsymbol{U}^T=S_i\underset{\boldsymbol{M}}{\underbrace{\boldsymbol{U}\boldsymbol{D}\boldsymbol{U}^T}}
$$

Therefore, DiagB(UD1U<sup>T</sup> , . . . , UDnU<sup>T</sup> ) = DiagB(S1M, . . . , SnM). Since the structures of normalization and whitening are special cases of Theorem [D.1,](#page-30-1) [Eigen-Adam](#page-18-5) generalizes these two gradient operators as a consequence.

SOAP generalizes [Eigen-Adam](#page-18-5) We can re-write the structural assumption of [Eigen-Adam](#page-18-5) in the Kronecker product format:

$$
\mathrm{Diag}_{\mathrm{B}}(\boldsymbol{U}\boldsymbol{D}_1\boldsymbol{U}^T,\ldots,\boldsymbol{U}\boldsymbol{D}_n\boldsymbol{U}^T)=(\boldsymbol{I}\otimes\boldsymbol{U})\underbrace{\mathrm{Diag}_{\mathrm{B}}(\boldsymbol{D}_1,\ldots,\boldsymbol{D}_n)}_{\tilde{\boldsymbol{D}}}(\boldsymbol{I}\otimes\boldsymbol{U}^T).
$$

It is clear that this is a special case of SOAP structure by containing U<sup>R</sup> = I.

<span id="page-37-0"></span>SOAP generalizes Shampoo The structure of Shampoo consists of two [SPD](#page-18-10) matrices R<sup>n</sup> and Lm. If we eigen-decompose those, and let R<sup>n</sup> = URDRU<sup>T</sup> <sup>R</sup> and L<sup>m</sup> = ULDLU<sup>T</sup> L , then the structure of Shampoo can be re-write as

$$
\begin{aligned}&\bm{R}_{n}^{\frac{1}{2}}\otimes\bm{L}_{m}^{\frac{1}{2}} \\ =&(\bm{U}_{R}\sqrt{\bm{D}_{R}}\bm{U}_{R}^{T})\otimes(\bm{U}_{L}\sqrt{\bm{D}_{L}}\bm{U}_{L}^{T}) \\ =&(\bm{U}_{R}\otimes\bm{U}_{L})\underbrace{(\sqrt{\bm{D}_{R}}\otimes\bm{D}_{L})}_{\tilde{\bm{D}}}(\bm{U}_{R}^{T}\otimes\bm{U}_{L}^{T}).\end{aligned}
$$

This coincides with SOAP's structure when the positive diagonal D˜ can be decomposed based on Kronecker product.

#### E.2 Memory consumption comparison

Apart from the Table [1](#page-2-2) provided in the main paper, we also include the memory consumption of

| more optimizers. |      |               |               |                            |                   |
|------------------|------|---------------|---------------|----------------------------|-------------------|
|                  | Adam | GaLore        | Fira          | Alice                      | Alice-0           |
| Total            | 3mn  | mn + 2nr + mr | mn + 2nr + mr | mn + 2nr + mr + r<br>2 + n | mn + 2nr + mr + n |
| Weight           | mn   | mn            | mn            | mn                         | mn                |
| First moment     | mn   | nr            | nr            | nr                         | nr                |
| Second moment    | mn   | nr            | nr            | nr                         | nr                |
| U                | N/A  | mr            | mr            | mr                         | mr                |
| Ct               | N/A  | N/A           | N/A           | n                          | n                 |
| Qe               | N/A  | N/A           | N/A           | 2<br>r                     | N/A               |

Table 6: The memory consumption of low-rank optimizers. Here, we assume the weight has a shape m × n with m < n and r ≪ m. Note that memory consumption n and r 2 is typically very small. For example, let's take the largest possible n = 30K at the output layer. For 1B LLaMA, we select r = 512, leading to r <sup>2</sup> ≈ 262K, which is 8x larger than n. However, both are marginal compared to mr = 5120 × 512, which is 10x larger than r 2 , and 80x larger than n.

#### E.3 Comparison to previous [FIM](#page-18-0) approximation

The idea of efficiently approximating the [FIM](#page-18-0) is not novel, and has been extensively studied in the previous work. KFAC [\[Martens and Grosse, 2015\]](#page-16-15) is a well-known second order optimization algorithm for neural networks based on structural approximation to [FIM.](#page-18-0) In particular, they explicitly express the [FIM](#page-18-0) in terms of the gradient w.r.t this layer's output and the input to this layer. Namely, they directly decompose the gradient G used in our paper, whereas in our paper, we treat G as a whole quantity. In addition, the original KFAC also makes one crucial approximation: E[A ⊗ B] ≈ E[A] ⊗ E[B]. They do not show theoretically whether this is a good approximation and under what metric, but argue in practice this gives good accuracy. Last but not least, the original KFAC considers the [FIM](#page-18-0) for entire layers, and each block (i.e. corresponding to each layer) under their setup is actually the entire [FIM](#page-18-0) we aim to approximate. To be precise, the principle is to structurally approximate the diagonal block of KFAC without decomposing the gradient G using KFAC.

Another more related work is AdaGrad [\[Duchi et al., 2011\]](#page-14-6). If we only considers layer-wise gradient, the full AdaGrad matrix is the P<sup>T</sup> <sup>t</sup>=1 ⃗gt⃗g T t . Although our principle is to approximate [FIM,](#page-18-0) in practice, we use [EMA](#page-18-3) as the approximation of E. Therefore, our principle can also be viwed as a structural approximation to full [EMA](#page-18-3) AdaGrad matrix. Under this view point, there are some previous work on structural approximations. Shampoo [\[Gupta et al., 2018\]](#page-15-1), was originally proposed as an approximation to full AdaGrad matrix under the online learning setup. However, they do not explicit show under what metric this approximation is based on, and whether it is optimal or not. Later, there is a follow-up work [\[Morwani et al., 2024\]](#page-16-12), showing that Shampoo is a 1-step power iteration algorithm of optimal Kronecker product approximation to [FIM](#page-18-0) under Frobenius norm [\[Koroko et al., 2022\]](#page-15-13). In this paper, we further extend the idea of approximating [FIM/](#page-18-0)AdaGrad matrix to more efficient structures, under Frobenius norm.

#### <span id="page-38-2"></span><span id="page-38-1"></span>E.4 Solutions to general block diagonal structures

Here, we present the solution of the most general block diagonal approximation to [FIM,](#page-18-0) and discuss why this is not practical.

Proposition 6 (General block diagonal approximation). *Assume* F˜ = Diag(M1, . . . ,Mn) *with [SPD](#page-18-10) matrix* M<sup>i</sup> ∈ R <sup>m</sup>×m*, then minimizing Eq.* [\(2\)](#page-2-1) *admits analytic solutions:*

$$
M_i^* = \mathbb{E}[g_i g_i^T] \tag{44}
$$

*where* g<sup>i</sup> *is the* i *th column of* G*.*

*Proof.* This is straightforward by taking the derivative w.r.t. M<sup>i</sup> . By leveraging Lemma [1,](#page-27-1) we have

$$
\begin{aligned} & \|\tilde{\boldsymbol{F}}-\boldsymbol{F}\|_F^2 \\ = & \sum_{i=1}^n \|\boldsymbol{M}_i\|_F^2 - 2\operatorname{Tr}(\boldsymbol{M}_i^T \mathbb{E}[\boldsymbol{g}_i \boldsymbol{g}_i^T]) \end{aligned}
$$

Then, taking derivative w.r.t. M<sup>i</sup> , we get

$$
\bm{M}_i^*=\mathbb{E}[\bm{g}_i\bm{g}_i^T]
$$

From the above, although it admits analytic solutions, its corresponding practical procedure requires the [EMA](#page-18-3) to estimate E[gig T i ] ∈ R <sup>m</sup>×<sup>m</sup> for all i = 1, . . . , n, leading to expensive memory cost nm<sup>2</sup> . Another issue is that it does not allow efficient computation of the inverse. From the property of block diagonal matrix, to compute F˜<sup>−</sup> <sup>1</sup> <sup>2</sup> ⃗g, one needs to invert each M<sup>i</sup> , incurring O(m<sup>3</sup> ) computational cost. In total, the computational cost of inverting matrix F˜ is O(nm<sup>3</sup> ). Due to both memory and computational constraints, this structural assumption does not lead to practical algorithms.

#### <span id="page-38-0"></span>E.5 Connections to existing optimizers

Lars and Lamb Lars and Lamb [\[You et al., 2017,](#page-16-13) [2019\]](#page-16-6) relies on the normalization operation of the gradients. The main difference is that Lars proposed to normalize the raw gradient, whereas Lamb normalizes the processed gradient from Adam optimizer. They also involves a scaling parameter that is a function of the weight. Compared to the normalization discussed in Sec. [3.3,](#page-3-3) the main difference is that we use channel-wise normalization with unit column or row norm, whereas Lars/Lamb uses matrix-wise normalization where the norm of the matrix is regularized to be 1. However, if one vectorizes the matrix weight into a vector, and stacks those vectors into a larger matrix. Then, the normalization step of Lamb and Lars can be viewed as a 1-sample approximation to [FIM](#page-18-0)[\\*](#page-38-3) under the structure considered in Sec. [3.3.](#page-3-3)

Muon Muon [\[Jordan et al., 2024\]](#page-15-2) performs the whitening operation on the momentum. App. [B.9](#page-23-2) gives a brief introduction. In fact, Muon can be viewed as a special case of Eq. [\(7\)](#page-4-2) in Proposition [2](#page-4-1) by considering the following approximation:

$$
\mathbb{E}[GG^T] \approx \mathbb{E}[G]\mathbb{E}[G^T].
$$
\n(45)

Thus, the resulting operation becomes the whitening of the E[G], which is estimated by the momentum in practice. There exists one difference: Muon omits the <sup>1</sup> n scalar, which serves as a layer-wise effective learning rate.

SWAN SWAN composes the gradient normalization and whitening operations as the replacement of Adam's first and second moments. Each individual operations can be viewed as a special case of Proposition [2.](#page-4-1) However, Sec. [3.3](#page-3-3) does not provide an explanation for composing these two operators. Namely, the whitening operator is estimated using normalized gradients, rather than the raw gradient. We will leave the investigation of operator composition for future work.

<span id="page-38-3"></span><sup>\*</sup>This [FIM](#page-18-0) is now the full Fisher across layers, compared to the 1-layer [FIM](#page-18-0) considered in the paper

<span id="page-39-0"></span>Adapprox Adapprox [\[Zhao et al., 2024b\]](#page-17-1) uses low-rank approximation for Adam's second moments through randomized [SVD](#page-18-12) to boost the memory efficiency. However, its performance will be similar to Adam. In fact, Proposition [3](#page-6-2) of [RACS](#page-18-1) proves that the converged s and q represents the right and left singular vectors, coinciding with the rank-1 reconstruction. However, the proposed [RACS](#page-18-1) is different from rank-1 Adapprox in three main aspects: (1) Adapprox proposes to use low-rank [EMA](#page-18-3) tracking on G⊙<sup>2</sup> , whereas we use [EMA](#page-18-3) directly on scaling vectors s, q. The resulting vectors are no longer singular vectors; (2) we do not have separate scaling apart from norm-growth limiter and user-defined scale, whereas Adapprox uses the scaling from Adafactor; (3) [RACS](#page-18-1) do not use any first moment. Specifically, (1) is an important difference, since for any low-rank reconstruction with rank r > 1, it is not guaranteed to be positive, causing numerical issue during square-root inverse scaling. Adapprox adds a manually defined offset to ensure positivity. On the other hand, [RACS](#page-18-1) is guaranteed to have positive s, q at each step from Perron-Frobenius theorem. Therefore, [RACS](#page-18-1) is numerically stable.

Adafactor Adafactor [\[Shazeer and Stern, 2018\]](#page-16-14) is another optimizer that uses rank-1 approximation to Adam's second moment. However, their scaling is derived by minimizing a different norm, compared to Frobenius norm in this paper. Adapprox [Zhao et al.](#page-17-1) [\[2024b\]](#page-17-1) has demonstrated the advantages of using Frobenius norm compared to Adafactor with a slightly better performance on LLM training.

AdaDiag and one-sided SOAP We acknowledge that there exists two concurrent work: AdaDiag [\[Anonymous, 2024\]](#page-14-2) and one-sided SOAP [\[Vyas et al., 2024\]](#page-16-0), that are mathematically equivalent to [Eigen-Adam.](#page-18-5) They are derived based on distinct view points. AdaDiag is based on the intuition to transform the gradient covariance matrix so that it is diagonalizable, where this diagonal matrix is estimated using Adam's second moments. One-sided SOAP, a memory-efficient version of SOAP, is proposed to based on intuitions that only one-sided eigenspace is enough for LLM training. On the other hand, [Eigen-Adam](#page-18-5) is derived on the basis of the structured [FIM](#page-18-0) view point. providing a deeper connections to optimizers considered in this paper.

Apollo There is one concurrent work, Apollo [\[Zhu et al., 2024\]](#page-17-0), that is also based on scaling the raw stochastic gradients for memory-efficient LLM training. It proposed to scale columns or rows of the G through a scaling matrix estimated by similar procedure as Fira [Chen et al.](#page-14-1) [\[2024a\]](#page-14-1). The main idea is that column or row norm after scaling matches the column or row norm of the gradient from GaLore update. Thus, they require a GaLore procedure to compute this update at each step. Our proposed [RACS](#page-18-1) scales both columns and rows at the same time. The main differences are: (1) the scaling estimation in [RACS](#page-18-1) is different from Apollo; (2) the scaling scheme of [RACS](#page-18-1) is inspired by the generalization of normalization, providing theoretical support. They enjoy a similar memory consumption (i.e. mn + 2n + 2 of Apollo compared to mn + m + n + 1 of [RACS\)](#page-18-1).

Fira Fira [Chen et al.](#page-14-1) [\[2024a\]](#page-14-1) was proposed as an improvement towards GaLore, which modifies the low-rank update to full-rank one by adding a compensation term. Their idea is similar to the compensation used in [Alice.](#page-18-2) The main differences is that our proposed compensation is inspired by approximating [FIM](#page-18-0) and has the theoretical foundation on its optimality. Also, the compensation strategy is different to Fira. We have conduced the ablation study in Sec. [7](#page-10-1) to show the advantage of our approach.

GaLore Comparing the [Alice](#page-18-2) procedure to GaLore (Algorithm [8\)](#page-24-1), we can clearly see that GaLore is a special case of [Alice](#page-18-2) by disabling tracking, switching and compensation. From the connection of [Alice](#page-18-2) to [Eigen-Adam,](#page-18-5) GaLore is a simple low-rank extension of [Eigen-Adam,](#page-18-5) a more general optimizer than Adam. Therefore, the [FIM](#page-18-0) view point reveals that GaLore is inherently a different optimizer compared to Adam, despite its similarity to Adam's update. This also provides an explanation on why GaLore can sometimes outperforms Adam under certain scenarios.

#### <span id="page-40-2"></span><span id="page-40-0"></span>E.6 Discussion of low-rank extension framework

First, we derive how to decompose the full-rank update of [Eigen-Adam](#page-18-5) into low-rank update and its residuals in the main text. We assume U˜ = [U, Uc], where U, U<sup>c</sup> are defined in Sec. [5.3.](#page-8-4)

$$
\begin{aligned} \mathrm{Mat}(\tilde{F}^{-\frac{1}{2}}\vec{g})=&\tilde{U}\frac{\tilde{U}^T G}{\sqrt{\mathbb{E}[(\tilde{U}^T G)^{\odot 2}]}}\\ =&[U,U_c]\frac{\begin{bmatrix}U^T \\ U^T_c\end{bmatrix} G}{\sqrt{\mathbb{E}\left[\left(\begin{bmatrix}U^T \\ U^T_c\end{bmatrix} G\right)^{\odot 2}\right]}}\\ =&[U,U_c]\frac{\begin{bmatrix}U^T G \\ U^T_c G\end{bmatrix}}{\sqrt{\mathbb{E}\left[\left(\begin{bmatrix}U^T G \\ U^T_c G\end{bmatrix}\right)^{\odot 2}\right]}}\\ =&[U,U_c]\left[\frac{\begin{bmatrix}U^T G \\ U^T_c G\end{bmatrix}}{\sqrt{\mathbb{E}[(U^T G)^{\odot 2}]}}\right]\\ =&U\frac{U^T G}{\sqrt{\mathbb{E}[(U^T G)^{\odot 2}]}}+U_c\frac{U^T_c G}{\sqrt{\mathbb{E}[(U^T_c G)^{\odot 2}]}} \end{aligned}
$$

Moore-Penrose inverse In Eq. [\(19\)](#page-8-5), we define F˜<sup>−</sup> <sup>1</sup> <sup>2</sup> using the pseudo-inverse since each block in F˜ <sup>c</sup> is low-rank and not invertible. To be precise, for any block UcDciU<sup>T</sup> c , its pseudo-inverse can be easily verified as UcD<sup>−</sup><sup>1</sup> ci U<sup>T</sup> <sup>c</sup> by checking the definition. Similar to typical inverse, for any block diagonal F˜ <sup>c</sup>, the pseudo-inverse is equivalent to applying pseudo-inverse of each blocks. The square-root pseudo inverse can be defined through a similar way.

Similarly, for the proposed compensation, we can easily verify its vectorized format (ignoring the subscript t for simplicity)

$$
\begin{aligned} \text{Vec}(\boldsymbol{U}_{c}\boldsymbol{U}_{c}^{T}\boldsymbol{G}\boldsymbol{S})=&(\boldsymbol{S}\otimes\boldsymbol{U}_{c}\boldsymbol{U}_{c}^{T})\vec{\boldsymbol{g}}\\ =&(\boldsymbol{S}^{-2}\otimes\boldsymbol{U}_{c}\boldsymbol{U}_{c}^{T})^{-\frac{1}{2}}\vec{\boldsymbol{g}}\end{aligned}
$$

where the <sup>−</sup> <sup>1</sup> <sup>2</sup> is the pseudo-inverse as the above. The second inequality can be easily verified by the following facts: (1) the square root pseudo inverse of UcU<sup>T</sup> c is itself; (2) the square root pseudo-inverse of block-diagonal matrix is the pseudo-inverse of each individual block.

# <span id="page-40-1"></span>F Experiment details

In this section, we will include the detailed setup, hyperparameters and additional experiment results.

#### F.1 Implementation details of baselines

GaLore We leveraged the official GaLore package released by the author ([https://github.com/](https://github.com/jiaweizzhao/GaLore) [jiaweizzhao/GaLore](https://github.com/jiaweizzhao/GaLore)).

Fira Since the main difference compared to GaLore is the additional compensation term, we follow the implementation of the official Fira repo (<https://github.com/xichen-fy/Fira>) and add the compensation to GaLore.

#### <span id="page-41-6"></span><span id="page-41-0"></span>F.2 Experiment setup for pretraining LLaMA

For all model parameters, optimizer states, we use BF16 format. We use context length of 256 and batch size of 128 with 4 gradient accumulations, apart from 60M and 1.3B (batch size 256 with 2 gradient accumulations). [RACS](#page-18-1) and [Alice](#page-18-2) are applied to all linear modules of attention and MLPs, others are optimized with Adam. We use the first 10% of the total training steps as the warm-up, followed by a cosine learning rate decay to 10% of the original learning rate. For hyperparameters, we perform a grid search on our proposed [RACS,](#page-18-1) [Alice](#page-18-2) as well as GaLore, Fira and full-rank Adam. For other methods, we directly cite their results in [\[Zhu et al., 2024\]](#page-17-0). For Adam, we use 0.9 and 0.999 for β<sup>1</sup> and β2, and enable the bias correction without weight decay. Table [7](#page-41-1) summarizes the hyperparameters used for both GaLore and Fira. Table [8](#page-41-2) summarizes the hyperparameters for Adam optimizer. Table [9](#page-41-3) and Table [11](#page-41-4) summarizes the hyperparameters used for [RACS](#page-18-1) and [Alice,](#page-18-2) respectively. In addition, for all methods with Fira limiter, we use threshold γ = 1.01 as suggested in [Chen et al.](#page-14-1) [\[2024a\]](#page-14-1). For [RACS,](#page-18-1) we use Adam to train the last layer of LLaMA, following the same setup as Apollo for fair comparison. In summary, [Alice,](#page-18-2) GaLore and Fira do not use Adam to train the last layer to fully test the capabilities of low-rank methods, whereas Apollo, [RACS](#page-18-1) and Adam utilize Adam for last layer. The total training steps for 60M, 130M, 350M and 1.3B are 10K, 20K, 60K and 100K, respectively. These correspond to 1.1B, 2.6B, 7.8B and 13.1B training tokens, summarized in Table [10.](#page-41-5) All experiments are conduced on NVIDIA A100 GPUs.

<span id="page-41-1"></span>Table 7: The hyperparameters for GaLore and Fira

|           | learning rate | update scale | rank | update interval |
|-----------|---------------|--------------|------|-----------------|
| 60M       | 0.02          | 0.3          | 128  | 200             |
| 130M 0.02 |               | 0.3          | 256  | 200             |
| 350M 0.02 |               | 0.3          | 256  | 200             |
| 1.3B      | 0.01          | 0.25         | 512  | 200             |

<span id="page-41-3"></span>Table 9: The hyperparameters for [RACS.](#page-18-1)

<span id="page-41-2"></span>Table 8: The hyperparameters used for Adam optimizer.

|      | learning rate | β1  | β2    | correct bias |
|------|---------------|-----|-------|--------------|
| 60M  | 0.001         | 0.9 | 0.999 | True         |
| 130M | 0.001         | 0.9 | 0.999 | True         |
| 350M | 0.001         | 0.9 | 0.999 | True         |
| 1.3B | 7 × 10−4      | 0.9 | 0.999 | True         |

<span id="page-41-5"></span>Table 10: Model architectures and training steps

|           |               |     |         |  |      | Hidden | Intermediate | Heads | Layers | Steps | Data amount |
|-----------|---------------|-----|---------|--|------|--------|--------------|-------|--------|-------|-------------|
|           | learning rate | β   | scale α |  | 60M  | 512    | 1376         | 8     | 8      | 10K   | 1.3B        |
| 60M       | 0.02          | 0.9 | 0.05    |  |      |        |              |       |        |       |             |
|           |               |     |         |  | 130M | 768    | 2048         | 12    | 12     | 20K   | 2.6B        |
| 130M 0.02 |               | 0.9 | 0.05    |  |      |        | 2736         | 16    | 24     | 60K   | 7.8B        |
| 350M 0.02 |               | 0.9 | 0.05    |  | 350M | 1024   |              |       |        |       |             |
|           |               |     |         |  | 1.3B | 4096   | 5461         | 24    | 32     | 100K  | 13.1B       |
| 1.3B      | 0.02          | 0.9 | 0.02    |  |      |        |              |       |        |       |             |
|           |               |     |         |  |      |        |              |       |        |       |             |

#### F.3 Setup of 1B v.s. 7B

We mainly follow the setup as [Zhu et al.](#page-17-0) [\[2024\]](#page-17-0). For 1B model, we use 16 per-device batch size with 8xA100s and 4 gradient accumulations, which is 512 batch size in total, same as 7B model. For [Alice,](#page-18-2) we use learning rate 0.02, scale α = 0.3 and compensation scale α<sup>c</sup> = 0.2 with rank r = 512, leading basis number l = 160. We also use full-rank Adam to train the last layer for better performance. For [RACS,](#page-18-1) we follow the same setup of 1.3B as reported in Table [9.](#page-41-3) For memory estimation, we assume the use of BF16 format. For 8-bit optimizers, we assume weights are stored in BF16, but optimizer states use FP8. GaLore uses r = 1024 for 7B model.

#### F.4 Memory estimation

Following the setup of [Zhao et al.](#page-16-5) [\[2024a\]](#page-16-5), we provide the estimated GPU memory for each optimizers due to the difficulty of directly measuring their practical memory consumption without considering the activations, internal storage for gradient, etc. We assume BF16 format, which consuming 2 Bytes per element. For example, 1273M parameters are optimized by [Alice](#page-18-2) and 65M parameters are

<span id="page-41-4"></span>

|      | learning rate | scale α | compensation scale αc | β1  | β2  | β3    | update interval K | rank r | leading basis number l |
|------|---------------|---------|-----------------------|-----|-----|-------|-------------------|--------|------------------------|
| 60M  | 0.02          | 0.3     | 0.4                   | 0.9 | 0.9 | 0.999 | 200               | 128    | 40                     |
| 130M | 0.02          | 0.3     | 0.4                   | 0.9 | 0.9 | 0.999 | 200               | 256    | 40                     |
| 350M | 0.02          | 0.3     | 0.4                   | 0.9 | 0.9 | 0.999 | 200               | 256    | 40                     |
| 1.3B | 0.02          | 0.25    | 0.2                   | 0.9 | 0.9 | 0.999 | 200               | 512    | 160                    |

Table 11: The hyperparmeters for [Alice](#page-18-2) optimizer

<span id="page-42-4"></span><span id="page-42-2"></span>![](./assets/structured-fisher-llm-optimizer/_page_42_Figure_0.jpeg)

<span id="page-42-3"></span>Figure 2: Additional LLaMA C4 pretrain performance curve. (a), (b) and (c) represents the 60M, 130M and 350M, respectively. "+lm head" represents that the last layer of LLaMA is trained by full-rank Adam.

optimized by Adam for 1B model with rank 512. Therefore, [Alice](#page-18-2) part will consume 3.86GB and Adam will consume 0.37GB, summing to 4.42GB for [Alice](#page-18-2) optimizer.

We also report the actual memory footprint with BF16 format. We use token batch size of 25, following the same setup as [Zhao et al.](#page-16-5) [\[2024a\]](#page-16-5). "-layerwise" represents layer-wise training where we only store the gradient of the current back-propagated layer.

### F.5 Throughput estimation

We report both the actual throughput and effective throughput. The effective throughput of a target optimizer compared to a reference optimizer is defined as the ratio of training tokens consumed from the target optimizer w.r.t total time consumption of reference optimizer when reaching the same evaluation loss of the reference optimizer at the end of training. Compared to the standard throughput, this considers the speed-up effect.

### <span id="page-42-0"></span>F.6 Additional pretrain results

Fig. [2](#page-42-3) presents additional training curves with 60M, 130M and 350M models sizes. For all cases, the proposed [Alice](#page-18-2) and [RACS](#page-18-1) outperforms the baselines with noticable margin, and achieves clear speed-ups compared to full-rank Adam.

### <span id="page-42-1"></span>F.7 Results for ablation studies

For all ablations, we consider 130M LLaMA model. Apart from the ablation on the last layer, we assume the last layer is trained by the candidate optimizer, rather than the full-rank Adam for thorough evaluation.

![](./assets/structured-fisher-llm-optimizer/_page_43_Figure_0.jpeg)

![](./assets/structured-fisher-llm-optimizer/_page_43_Figure_1.jpeg)

(b) Effective throughput

Figure 3: Throughput of various methods. (a) this reports the absolute throughput, representing the number of training token processed per second. (b) the effective throughput using Adam as the reference optimizer. This represents the absolute throughput adjusted by the speed-up factor. The effective throughput of GaLore and Fira is 0 for some model sizes since they under-perform the Adam.

44

<span id="page-44-0"></span>![](./assets/structured-fisher-llm-optimizer/_page_44_Figure_0.jpeg)

Figure 4: The memory footprint of various optimizers. We use token batch size of 256 following the same setup as [Zhao et al.](#page-16-5) [\[2024a\]](#page-16-5) under BF16 format. The suffix "layerwise" represents the memory consumption when enabling layerwise training so that only the gradient of the current layer is stored.

Setup: ablation of tracking We disable the compensation step, and verify the effect of low-rank tracking under our proposed switch strategy or purely replying on [EVD](#page-18-6) (i.e. no switching). The other hyperparameters follow the pre-training setup as App. [F.2.](#page-41-6)

Setup: switch strategy For this setup, we enable low-rank tracking. Apart from Gaussian, we use 40 as the leading basis number. The Gaussian distribution is a standard isotropic Gaussian with zero mean and unit variance. To make sure the norm of sampled Gaussian vectors are consistent with the real basis, we normalize those sampled vectors to have a unit l<sup>2</sup> norm. The same operation is also applied to Gaussian-mix.

Setup: compensation strategy We enable the tracking and switching, but with different compensation terms. For Fira, we directly leverage the compensation proposed in [Chen et al.](#page-14-1) [\[2024a\]](#page-14-1). Fira+ modifies original Fira by the following two steps: (1) rescale the Fira compensation to have the same l<sup>2</sup> norm as the [Alice](#page-18-2) low-rank update (i.e. first term in Eq. [\(19\)](#page-8-5)); (2) multiply this compensation by a scale parameter like α<sup>c</sup> in Algorithm [4.](#page-9-3) We found this empirical trick boosts the performance of Fira.

Effects of last layer One crucial setup difference during evaluation for low-rank methods is whether the last layer is trained by full-rank Adam or not. Most previous work train the last layer, arguably one of the most important layer [\[Zhao et al., 2024c\]](#page-17-2), using full-rank Adam. This effectively reduces the performance gap compared to full-rank method, and does not reveal their true capabilities. We investigate the effect of the last layer to [Alice](#page-18-2) compared to GaLore and Fira. From the Table [2,](#page-11-0) we can see that for all model sizes, GaLore and Fira are greatly affected by this effect. Training last layer with full-rank Adam will boost their performance significantly. On the other hand, [Alice](#page-18-2) is less impacted with marginally worse performance. For example, Fig. [5\(d\)](#page-45-4) shows the training curve comparison with 130M model. When the rank is sufficiently large (e.g. rank 128 is sufficient large for 60M model), Fig. [2\(a\)](#page-42-4) shows that using Adam to train the last layer even decreases the performance. These serve as evidences that [Alice](#page-18-2) is a better optimizer than GaLore and Fira, and has the potential to surpass full-rank Adam with large enough rank.

Effect of [EMA](#page-18-3) in [RACS](#page-18-1) The only internal states inside [RACS](#page-18-1) are the [EMA](#page-18-3) tracking states of two vectors s and q. We investigate the importance of [EMA](#page-18-3) scheme. From Fig. [5\(e\),](#page-45-5) [RACS](#page-18-1) without [EMA](#page-18-3) performs much worse than [RACS,](#page-18-1) suggesting the [EMA](#page-18-3) is necessary for satisfactory performance of [RACS.](#page-18-1)

<span id="page-45-3"></span><span id="page-45-1"></span><span id="page-45-0"></span>![](./assets/structured-fisher-llm-optimizer/_page_45_Figure_0.jpeg)

<span id="page-45-2"></span>Figure 5: The pre-training curve to verify the effectiveness of the design choice. We consider 130M model size.

<span id="page-45-5"></span><span id="page-45-4"></span>(e) Effect of [EMA](#page-18-3) in [RACS.](#page-18-1)

![](./assets/structured-fisher-llm-optimizer/_page_46_Figure_0.jpeg)

<span id="page-46-0"></span>Figure 6: The cosine similarity between eigenvectors per 200 steps. Since the update interval of subspace is 200 steps, this essentially compare the similarity before and after updating the projection U with a certain index. We always arrange the eigenvectors in a descending order based on the eigenvalues.