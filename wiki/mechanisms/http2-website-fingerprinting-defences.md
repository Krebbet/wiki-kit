# HTTP/2 Website-Fingerprinting Defences

Cebere, Kumar, Chatel, Lueks & Rossow (CISPA; arXiv 2609.05119; ACM CCS 2026) show HTTP/2 features (multiplexing, flow control, PING, server push) let clients and servers emulate and improve website-fingerprinting (WF) defences at the application layer, without Tor or a VPN. A passive on-path observer (ISP, network operator, VPN provider) infers which subpage of a known domain a user visits from encrypted TCP metadata. The paper adds two new defences (H2PC client, H2PS server) and `wfaudit`, a released benchmark/audit tool. Network-layer surface, distinct from [[browser-fingerprinting]].

## Attack

- Adversary sees packet sizes, timing, bursts; infers the page (e.g. which Amazon product, which BBC article).
- Undefended, five attackers (k-FP, DF, Var-CNN, Holmes, RobustFP-CNN) reach macro-F1 >= 0.9 on all five sites.
- Stated harms: surveillance, censorship, targeted advertising. Amazon product-page leakage bears on ISP-level shopping-intent inference. Not pricing-specific.

## Defences

- **Client-side (emulated):** HTTPOS, LLaMA, FRONT, Tamaraw. Attacker candidate set >= 26 pages on 4 of 5 datasets.
- **Server-side (emulated):** ALPaCA, server-Tamaraw. Candidate set >= 63 on any dataset, when placed on the right server.
- **H2PC (new):** privacy-conscious HTTP/2 client — randomised request batching/prioritisation, randomised flow-control windows, random PING frames, guarding noise streams. Candidate set > 7 on all sites; latency overhead cut 55-98% and downstream overhead 20-66% vs prior defences.
- **H2PS (new):** proactive resource suggestion; protects the whole page from the first-party server alone, no CDN or third-party cooperation. Candidate set > 13 on all sites; bandwidth overhead cut 54-80% on most.
- Defences are dataset-dependent; per-site calibration required. Individual, unilateral — no coordination or network effect.

## Audit methodology and code

- Code released (GitHub: bcebere/Understanding-the-Privacy-Preserving-Potential-of-HTTP2-Against-Webpage-Fingerprinting): `wfaudit` (5 attack models, 2 information-theoretic leakage estimators WeFDE and DeepSE-WF), defence calibration, data collection/replay, client/server defence implementations, benchmark pipeline.
- Method: calibrate defence per dataset, run tuned attackers, report residual candidate-set size rather than raw accuracy drop (accuracy drop can mislead). Cf. [[dp-audit-methodology]].

## Limits

- Traces replayed through a custom Python client/server, not live browsers or CDNs.
- Closed-world; 5 sites x 100 subpages (Amazon, BBC, Reddit, Udemy, Wikipedia), 500 traces/page.
- No browser-extension path: flow-control and PING control need OS/userspace HTTP-stack access; TCP flow control is kernel-handled. Deployable via a client library, proxy, or cooperating server.
- Does not hide IP, domain, DNS, or SNI; DoH/ECH are orthogonal. Complements Tor/VPN.
- Dual-use: the attack techniques are extraction-side tools.

## Source

- `raw/research/weekly-2026-09-28/02-http2-wf-defence.md` — arXiv 2609.05119, CCS 2026.
  - **Origin:** CISPA Helmholtz Center for Information Security.
  - **Audience:** security/privacy researchers, HTTP library developers.
  - **Purpose:** show application-layer WF defences are practical; provide rigorous evaluation method.
  - **Trust:** high — peer-reviewed, code released; caveats above.
- Summary: `raw/research/weekly-2026-09-28/.ingest/02-http2-wf-defence.summary.md`

## Related

- [[browser-fingerprinting]]
- [[fingerprinting-sdk-ecosystem]] — another surface browser-layer defences miss (native SDKs)
- [[obfuscation]]
- [[tools/simulacra]] — physical-layer obfuscation against passive observers
- [[dp-audit-methodology]]
- [[transparency-tools]]
