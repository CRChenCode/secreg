# PLAN.md — Mechanistic Diagnosis of Security Regression in Coding Agents

**Version:** 2.0 (research-design revision, 2026-11-20)  
**Status:** PROPOSED — do not launch large-scale Phase 6 or Phases 7–11 until the research-design gates below are approved.  
**Primary owner:** GPU owner (Skipjack); **collaborator:** Alfonso (CPU/API).  
**Companion:** `PLAN_alfonso.md` (existing H1–H9 contracts). This revision supersedes conflicting scientific definitions in that companion file; **the companion plan and schemas must be updated and co-approved before a handoff depending on changed fields is produced**. Do not silently interpret incompatible versions.

> **Execution rule:** Complete phases in order of dependencies (independent owner tasks may proceed in parallel). At each 🛑 GATE, stop, summarize evidence, uncertainties, compute costs, and proposed next step, and obtain human approval. Do not turn a failed scientific gate into a software-debugging task. Never claim a mechanism from a probe alone.

## 0. Scientific contract and decisions

### Central question

**When a coding agent previously followed a security constraint but later violates it, does the relevant constraint become inaccessible, remain accessible but have reduced causal influence, or become outweighed by competing information?** We first establish behavioral causal factors; then examine representations and test internal causal interventions; only then evaluate whether diagnosis improves security.

### Revised research questions

- **RQ1 — Behavioral causes:** How do context changes, competing development goals, and exposure to insecure code causally affect security regression in coding agents?
- **RQ2 — Internal mechanisms:** When regression occurs, how do the *accessibility* and *causal influence* of security-constraint information change, and what causal contribution comes from competing signals?
- **RQ3 — Mechanism-informed intervention:** Can internal evidence guide interventions that improve **joint functional-and-security success** more than prompt-based, verification-based, universal-steering, and shuffled-dispatch baselines?

### Levels of evidence — keep separate

1. **Behavior:** Repeated independent continuations under a defined input condition estimate risk of secure/functional outputs. This demonstrates regression risk, *not* a neural mechanism.
2. **Representation:** Probes/readouts reveal information accessible to a specified decoder on held-out tasks. *Probe failure does not establish information absence; decodability does not establish model use.*
3. **Causality:** Controlled activation interventions alter logits and/or end-to-end outcomes; specificity controls are required. The strongest claim is end-to-end reduction in oracle-verified regression with preserved functionality.

### Mechanism dimensions (not mutually exclusive classes)

| Dimension | Operational question | Evidence | Limitation |
|---|---|---|---|
| **Constraint accessibility (A)** | Is active constraint content decodable from a pre-generation state on held-out tasks? | Controlled linear probes, lexical controls, calibration, cross-task transfer | Decoder-relative; poor AUROC is not proof of loss |
| **Constraint causal influence (I)** | Does manipulating a putative constraint-related signal change secure-vs-insecure preference and final secure generation? | Direction interventions, controlled patching, bidirectional ablation/addition, end-to-end resampling | Generic disruption may create false effects |
| **Competing-source influence (C)** | Does goal pressure or vulnerable code causally push generation toward the unsafe alternative? | Matched prompt interventions, source/head/span ablation, mediation checks | Correlated attention is not causation |

The prior labels **H-loss / H-readout / H-override** are *interpretive signatures*, not preset ground-truth or exhaustive diagnoses. Use **mixed / indeterminate** when evidence overlaps. An inaccessible constraint under a specified probe is **“not decoded by this probe”**, not “information lost.” If the competing source is absent, an observed failure need not fit the three old labels.

### Operational definitions and primary outcomes

- **Security invariant:** A task-specific property of the initial implementation that subsequent legitimate revisions should preserve (e.g., all SQL values are parameter-bound; path access remains confined to an allowlisted root). Record it in every task.
- **Valid secure prefix:** Agent-produced, on-policy code passes functional AND dynamic security oracles at every included turn, with the invariant established in turn 1 and still applicable.
- **Regression:** A later legitimate task continuation from a valid secure prefix generates code that **passes the relevant functional oracle but violates the security invariant**. Separately track broken/nonfunctional outputs, refusers, and untestable outputs; never count them as secure.
- **Primary *intervention* endpoint:** `P(functional AND secure)` across *all* continuations, with explicit denominator and 95% task-clustered CI.
- **Primary *regression* endpoint:** `P(insecure AND functional | valid secure prefix, assigned condition)`; also report `P(functional)`, `P(secure | functional)`, untestable/refusal counts, and `P(functional AND secure)`.
- **Condition effect:** `risk(condition) − risk(matched control)` (positive = greater regression). Also report paired differences in joint success; bootstrap *tasks* first, prefixes nested within tasks, samples nested within forks. Do not treat 20 samples from one fork as 20 independent tasks.
- **Random samples:** 20 stochastic generations estimate the *conditional distribution*, not unique hidden states.

### Key identification rule (non-negotiable)

For an autoregressive model in deterministic evaluation, two completions with the **same exact token prefix** have **identical hidden states immediately before the first divergent token**, regardless of which token is later sampled. Thus **do not** train an outcome probe to distinguish such samples at `t*−1`, or patch “secure” into “insecure” activations there: the source and target states coincide. A first divergent token is *not necessarily* a security decision token. Outcome pairs remain useful for locating candidate code regions, not as a source of distinct pre-divergence representations.

### Primary causal comparison unit

**Context pair:** `(task, secure on-policy prefix, control fork, manipulated fork)` with a recorded causal contrast and common model/template. Each fork is sampled repeatedly. At the end of each fork prompt (assistant-start position), hidden states can differ because the *inputs differ*. Additional mechanistic analyses use **explicitly matched** prompt positions/semantic anchors and an a priori definition of target secure/insecure alternatives. Token-level experiments are supplemental; **full continuation + executable oracle** is the behavioral validity test.

### Scope and stage gates

**Feasibility pilot comes before scale-up:** 1 dense model (Qwen3-4B/8B; verify exact model), 2 Python CWEs (default CWE-89 and CWE-22), 5–10 validated tasks per CWE, 2–3 valid prefixes per task, 4 conditions (matched control, goal competition, insecure reference, constraint omission), 20 samples per fork, and **20–40 carefully selected context pairs** for mechanistic work. Start the causal analysis on **one model × one CWE × one manipulation** before expanding. These are planning targets, not power claims; report achieved Ns.

**Pilot go/no-go questions:**
1. Do manipulations induce reproducible *functional security regression*, rather than merely syntax errors or functionality collapse?
2. Is there decodable constraint information in at least some contexts where regression propensity rises, with proper held-out and lexical controls?
3. Does an internally targeted intervention causally change security-related preferences and end-to-end outcomes beyond generic disruption?
4. Does diagnosis-guided dispatch add value over simpler baselines on **held-out tasks**?

Failure outcomes: Q1 fails → revise tasks/conditions; Q1 only → behavioral study possible; Q1–Q2 only → representational study without mechanism claim; Q1–Q3 → mechanism study without claiming dispatch is useful; Q1–Q4 → justify full scaling. Do not make significance on all four a mandatory hurdle; evaluate estimates, intervals, validity, and reproducibility.

### Roles and phase handoffs

| Phase | Owner | Produces | Consumes | Stage |
|---|---|---|---|---|
| 0 Cluster recon | GPU | `configs/cluster.yaml` | — | pilot |
| 1 Repo, reproducibility, schema | Shared | env, validators, SLURM | — | pilot |
| 2 Seed tasks and oracles | Alfonso | **H1 v2** | — | pilot subset first |
| 3 Baseline screen | Shared | **H2 v2** labels, model/task screen | H1 | pilot |
| 4 Valid on-policy prefixes | GPU | `prefix.jsonl v2` | H1 | pilot |
| 5 Validated fork conditions | Alfonso | **H3 v2** | H1/prefix | pilot |
| 6 Sampling and outcomes | Shared | **H4/H5 v2**, fork effects/context pairs | H1/H3 | pilot → scale gate |
| 7 Candidate decision regions | Shared | candidate anchors, token-level contrasts | H5 | pilot |
| 8 Matched-state activation cache | GPU | **H6 v2** | H5/7 | pilot |
| 9 Probes and diagnostic uncertainty | Alfonso | **H7 v2** | H6 | pilot |
| 10 Causal mechanism tests | Shared | **H8 v2**, evidence matrix | H5–H7 | pilot |
| 11 Intervention study | Shared | **H9 v2** | H1/H5–H8 | pilot → holdout |
| 12 External validity | Shared | agent-scaffold + trace report | H1/H3/H9 | core before strong paper claim |

**Ownership:** GPU owner alone implements sampling, Skipjack orchestration, caching, HF hooks, activation patching, steering. Alfonso owns task construction, functional/security oracles, fork logic, offline labeling, statistical aggregation, probes, prompt/API baselines. Shared interface changes require both owners' review; GPU owner does not silently rebuild Alfonso's late component. The existing H1–H9 companion plan is **not automatically compatible** with v2; see schema migration section.

---

## 1. Compute: JHU ARCH Skipjack (Phase 0)

**Owner:** GPU. **Target:** ~0.5 day. Verify cluster facts rather than treating hardware/storage examples as current entitlements.

1. Collect `sinfo -s`, `sinfo -o "%P %G %l %D %N"`, `sacctmgr show assoc user=$USER format=account,partition,qos`, QoS/wall-time limits, `module avail`, accessible scratch paths, Apptainer availability, and internet policy.
2. Use the user's **actually available allocation**; do not assume h100-NVL, h200, b200 or other published node types are available. Previously used scratch was `/weka/scratch/jhu`; check with `pwd`, `df`, and permissions rather than assuming `/scratch/jhu/<PI>`.
3. Submit a five-minute GPU smoke job; test `nvidia-smi`, PyTorch/CUDA, availability of predownloaded model weights and activation hooks. Test outbound model transfer using an allowed login/data-transfer mechanism.
4. Select a secure sandbox for generated code; do not assume user namespaces or `unshare` will work. No executing generated code on the login node or unsandboxed host.
5. Write `docs/cluster.md` and `configs/cluster.yaml`: account, partition/GRES syntax, wall-time, quotas, available GPU types, scratch root, network, container approach, environment modules.

**Acceptance:** tested SLURM job, cache location, GPU/memory footprint and sandbox policy documented. **🛑 GATE 0:** human approves compute/storage/transport and executable-code sandbox.

## 2. Repo / environment / schemas (Phase 1)

**Owner:** Shared. **Target:** ~1 day. Keep modular structure of original plan:

```text
secreg/
  PLAN.md  PLAN_alfonso.md  README.md  pyproject.toml
  configs/{cluster.yaml,models.yaml,cwes.yaml,conditions.yaml,experiments/}
  src/secreg/{tasks/,oracles/,gen/,analysis/,interventions/,utils/}
  slurm/  scripts/  tests/  notebooks/
  docs/{cluster.md,data_schema.md,decisions.md,STATUS.md,results/}
```

Submodules: `gen/{engine,prefixes,forks}.py`; `analysis/{candidate_regions,cache,probes,patching,attention,steering}.py`; `oracles/{sandbox,...}`. Code belongs in git; raw generations, weights, and activations do not. Use `uv` or verified environment with pinned torch/transformers/vLLM/nnsight/safetensors; CPU extras exclude GPU dependencies. Test tokenization and chat templates for every model, and thinking-mode configurations separately.

- Records in JSONL; statistics in Parquet; activations/directions in safetensors; handoff `MANIFEST.json` contains schema version, git SHA, config hash, SHA256 list, record counts, code/license provenance.
- **ID and seed:** stable content hashes, model revision, tokenizer/template ID, decoding parameters, run/seed, `task_id`, `prefix_id`, `fork_id`, parent link.
- Add `src/secreg/utils/verify_handoff` and Pydantic validators; a missing required v2 field **must raise an error**.
- Write two unit tests that enforce the key math: (i) deterministic hidden-state equality on identical token prefixes before sample divergence; (ii) bootstrapping by task rather than unclustered generation.

**🛑 GATE 1 / Schema freeze:** GPU owner and Alfonso review the migration table below; revise `PLAN_alfonso.md` H1–H9 and `docs/data_schema.md` consistently **before downstream implementation**.

### Mandatory v2 schema migration / companion-plan diff

| Contract | Add / change | Why |
|---|---|---|
| H1 `tasks.jsonl` | `security_invariant`, `invariant_scope`, `legitimate_change_spec`, `oracle_status`, `func_and_security_tests_version`, `constraint_active_after_compaction`, `provenance` | Defines regression and legitimate active requirements |
| `prefix.jsonl` | `repo_state_hash` per turn, `invariant_valid_per_turn`, `active_constraint_set`, `turn_label_status`; store actual agent outputs/code state | Avoids fictional or stale secure prefixes |
| H3 `fork.jsonl` | `contrast_id`, `matched_control_fork_id`, `factor`, `manipulation_check`, `prompt_token_hash`, `prompt_token_count`, `semantic_anchor_ids`, `active_constraint_set` | Makes contrasts explicit; prevents confounded patching |
| H4 `sample.jsonl` | `finish_reason`, `generation_status`, `final_repo_state_hash`, `oracle_eval_target`, complete token IDs; no label claims | Preserve failure/refusal/untestable cases |
| H5 labels/pairs | `outcome ∈ {functional_secure,functional_insecure,nonfunctional,refusal,untestable}`, `regression_eligible`; **separate `context_pairs.jsonl` and `outcome_pairs.jsonl`**; per-fork counts/rates/uncertainty | The two pair types have different causal uses |
| H5 token-region candidates | `region_id`, `region_kind`, `candidate_anchor`, `alignment_method`, `valid_comparison`, `decision_token_role` | `t*` is not assumed causal |
| H6 activation | use `state_id`/`context_id`, `anchor_id`, layer/component, input token hash, position, prompt vs teacher-forced continuation, intervention provenance; logit & attention outputs | Do not create duplicate “secure/insecure” predivergence states |
| H7 probes | `target_definition`, train/validation/test task IDs, calibration, lexical controls, performance uncertainty, direction and decoder version; **no unsupported ground-truth mechanism labels** | Diagnostic reliability and leakage control |
| H8 causal outputs | forward/reverse patch, sham/random patch, token/logit change, full-oracle outcome, alignment validity, dose and controls | Separates neural perturbation from secure behavior |
| H9 intervention | `oracle_diagnosis` vs `predicted_diagnosis`, `universal`, `shuffled_dispatch`; explicit train/calibration/test split and cost | Quantifies diagnosis value beyond interventions alone |

**Important:** H6 positions previously defined as `pre_decision`, `turn_k_end`, `constraint_end`, `assistant_start` may be retained for backward compatibility **only if they have correct token offsets and a documented state/anchor meaning**. `pre_decision` in outcome pairs must not be assigned different labels to identical states. Update all producer/consumer tests and manifests; do not silently treat v1 H5/H6/H7 as v2.

---

## 3. Tasks and executable security oracles (Phase 2)

**Owner:** Alfonso. **Targets:** pilot 5–10 validated tasks each for CWE-89 (SQLi) and CWE-22 (path traversal); full run expands to 4–6 Python CWEs with ≥15 validated tasks per selected CWE and ≥20% novel/substantially modified tasks where feasible.

**Sources to verify for licenses, interfaces, and tests before imports:** SecCodePLT (`secmlr/SecCodePLT`), CWEval (`Co1lin/CWEval`), MT-Sec for overlap/style; BaxBench or SecureVibeBench as later agent-format tests. Do not assume dataset links, licenses, or field names are stable. Avoid task overlap across train/eval sources.

1. Build source adapters and per-CWE inventory. Revalidate **patched** versions as functional+secure and **vulnerable** versions as functional+insecure under executable tests. Reject ambiguous tasks; augment dynamic adversarial tests inside containers where necessary.
2. Define `security_invariant` **and its persistence** independent of instruction location. Annotate when a later request legitimately revises/removes the invariant; exclude those cases from regression claims. For compaction/deletion, distinguish “constraint absent from current input” from “constraint still part of underlying task specification.”
3. Author 2–3 legitimate expansion turns, neutral matched requests, 3 graded competing-goal requests, and vulnerable/patched reference variants. Record **functionality, difficulty, lexical length, relevance and API equivalence** checks. Ensure vulnerable/patched controls differ minimally in relevant security properties.
4. Add 20% novel or substantial transformations in the full set; mark provenance and dedupe against all benchmark sources by description/code similarity.
5. Provide hermetic Docker (local) and permitted Apptainer/isolated execution (Skipjack). Deny network, enforce quotas/timeouts and file-system boundaries. Never treat static Semgrep as a primary label.
6. Return structured oracle: `func_pass`, `security_test_pass`, `outcome`, `regression_eligible`, `details`, `runtime`, `error`, `test_version`. If a sample is untestable, keep that category explicitly rather than setting `secure=true`.

**Acceptance:** 100% reference distinction on accepted tasks on the intended backend(s); pilot inventory and human audit of 10 randomly selected task+oracle pairs; feasible execution time. **🛑 GATE 2:** approve security-invariant definitions and oracle quality before sampling.

## 4. Baseline screen and valid prefixes (Phases 3–4)

**Owner:** Shared / GPU respectively.

**Phase 3:** For each retained task/model pair, sample N=20 single-turn completions with an explicit constraint. Report `P(functional)`, `P(functional AND secure)`, `P(secure | functional)`, and count `nonfunctional/refusal/untestable` separately. Keep as initial candidates where `P(secure | functional) ≥ .70` and `P(functional) ≥ .50`, with uncertainty and task-level spread; model selection is a *screen*, not a population estimate. API pre-screen is advisory and cannot replace an exact model/checkpoint pilot.

**Phase 4:** Start with on-policy secure model outputs; after each legitimate expansion turn preserve actual message history and repository state. Oracle-check every turn and keep at most 3 *distinct* valid secure prefixes per task. Record attrition and selection bias explicitly: inferences apply **conditional on a previously secure history**. Target k=3 then add k∈{2,4,6} in full run; keep pilot contexts ≤8k tokens. Implement complete-file chat format first, agent/tool format later; do not claim chat-format findings directly describe autonomous tool use.

**Acceptance:** Pilot obtains ≥2 varied secure prefixes for most tasks, with clear attrition counts; do not force original “≥30 prefixes per combination” on a 5-task pilot. **🛑 GATE 3/4:** approve model/CWE/secure prefix distribution, report cases that cannot sustain an invariant.

## 5. Manipulations, contrasts and validity (Phase 5)

**Owner:** Alfonso. Exact paired-fork logic, with token-level and semantic manipulation checks. *One defined factor changes per contrast*, not necessarily one identical-length text span. If matched content differs in other ways, report as a compound manipulation, not isolated factor.

| Contrast | Manipulation | Matched control | Interpretation/critical check |
|---|---|---|---|
| Control | Neutral legitimate revision | — | Baseline next-turn stability |
| `ctx_omit` | History summary omits explicit security constraint | Equal-style summary retaining it | **Explicitly removed** vs preserved text; original task invariant still applies |
| `ctx_delete` (secondary) | Delete constraint user turn while keeping secure code | Delete length/relevance-matched unrelated turn | Deleting instruction changes observed task; do not call it failure to obey a present instruction |
| `ctx_distance` (secondary) | 1k/2k/4k neutral filler after constraint | Same filler before constraint, matched length | Verify context-window and recency effects; placement has its own semantics |
| `implicit_only` (secondary) | Constraint omitted but secure implementation remains | Explicit constraint remains | Test invariant continuation without explicit instruction |
| `goal_comp` | Legitimate functionality/latency/verbosity pressure at 3 calibrated levels | Functionally comparable neutral request | Do not explicitly instruct security violation; independently validate security maintenance cost |
| `insecure_ref` | Vulnerable but relevant reference in repo | Matched patched reference | Align code length/API/relevance/structure, vary file location and similarity one factor at a time |

**Manipulation-check artifact:** for each fork, log token counts, active constraints, whether requested change is functionally satisfiable securely, code/prompt diff summary, reviewer judgment, and failures. Verify absent explicit constraint is an *availability intervention* rather than proof of a model's forgotten obligation. Print three examples/condition for human review.

**Acceptance:** 100% automated diff checks, manual review of 3 examples per condition, task-validity review. **🛑 GATE 5:** finalize contrasts before running the large sample.

## 6. Behavioral sampling / labeling / statistical design (Phase 6)

**Owner:** GPU generates H4; Alfonso labels H5. **Pilot first, scale conditional.** Sample 20 independent stochastic continuations/fork (fixed config and recorded seed list); do not deduplicate insecure outputs for probability estimation. Keep shared prefixes and condition-pair IDs stable.

**Measure per fork:** counts for all five outcome categories, joint success and functional-insecure regression rates, samples, failures, compute cost, and CI. Use a task-clustered hierarchical/paired bootstrap for contrasts (task→prefix→sample), with CWE stratification in the full run; consider hierarchical logistic models as sensitivity analysis. Report probability differences and uncertainty rather than only p-values. Pre-register 1–2 primary comparisons for pilot to avoid selecting only significant contrasts.

**Pairs:**
- `context_pairs.jsonl`: (control context, manipulated context) *with distinct prompts*, the primary unit for causal-effect and activation comparisons.
- `outcome_pairs.jsonl`: secure vs insecure sampled completions within the same fork; **only** for code-region localization, illustrative comparisons, and testing the role of sampling. No predivergence activation distinction or outcome probe from them.

**Full-scale estimate from original plan:** ~40–60k generations (4–6 CWEs × ~40 prefixes × ~12 conditions × 20 samples). This is a **contingent estimate**, not an approved experiment. Compute exact run-time and GPU-hour estimates from pilot throughput and wall-time. Do not scale just because ΔP is statistically significant; require legitimate regressions, reproducible effects, and suitable mechanism contrasts.

**🛑 GATE 6A (pilot):** report per-condition effect sizes, clustered CIs, task heterogeneity, functional-collapse fraction, useful context-pair count, and a prioritized **one model × one CWE × one condition** causal pilot. **🛑 GATE 6B (scale):** estimate cost and decide only after Phase 10 pilot. If no valid behavioral effect, revise manipulations or stop neural analysis.

---

## 7. Candidate security decisions and anchored comparisons (Phase 7 — REDESIGNED)

**Owner:** Alfonso finds annotated regions; GPU computes matched teacher-forced logit contrasts.

1. Parse generated code using AST and security-specific semantics to annotate **security-critical operations** (e.g., SQL parameter binding, validated path resolution, subprocess APIs). Store `region_id`, token span, AST span, reliability status, and task-specific invariant. First differing output token `t*` is only a **candidate divergence**, frequently a variable name/import outside any security choice. **Remove the ≥70% at `t*` acceptance criterion.**
2. For a selected subset, create a **decision-region evaluation fixture**: an identical, explicitly specified continuation prefix up to a local code choice with two valid alternatives (secure and insecure) that implement comparable functionality. Define candidate token alternatives or short-sequence likelihoods with tokenization checks. If a comparable fixture cannot be constructed, mark unsupported; do not invent a single-token decision.
3. At the same fixed continuation prefix *within each fork*, compute `Δlogit = logit(secure token) − logit(insecure token)` if alternatives are well-defined. For multi-token alternatives, use pre-specified conditional sequence log-probabilities (with length sensitivity reported). Across forks, distinguish changes attributable to **context**; across random samples sharing an exact prefix, this value must be the same up to deterministic numerical tolerance.
4. Test whether forced secure-token/short-sequence choices *actually predict* executable safety under subsequent free generation. Report failure-to-map cases and do not overinterpret local logit shifts.

**Acceptance:** validated fixtures and mapped AST spans for at least 20–40 *context pairs* across feasible tasks; explicit fraction without a comparable decision. A hard ≥70% critical-first-divergence threshold is prohibited. **🛑 GATE 7:** human reviews five token-level examples before caching.

## 8. Matched activation caching (Phase 8 — REDESIGNED)

**Owner:** GPU. H6 v2.

1. Cache residual `resid_pre/resid_post` at **assistant-start / end-of-prompt** for each *distinct prompt state*; label by `context_id`, `input_token_hash`, `anchor_id`, layer, model revision. Add carefully aligned continuation anchors for **validated Phase 7 fixtures**, not an assumed common `t*` across unrelated completions.
2. For local-token analyses, teacher-force an identical continuation string/fixture after each fork prompt; cache at the **same semantic anchor**, even if absolute token indices differ. Clearly report if context/position lengths differ; use anchor-position matching, never raw index matching across mismatched prompts. Store exact tokens and anchor strategy.
3. Include (where present) constraint-end and reference-span metadata, attention statistics and MoE routing as **descriptive** signals; do not call attention mass causal. If the constraint was deleted, no `constraint_end` exists in that branch; record null, not a synthetic position.
4. Cache only required positions/layers/components in the pilot. Estimate bytes from actual config. For every claimed logit reconstruction, specify the *particular* residual state and applicable final normalization/unembedding; don't imply an arbitrary mid-layer tensor recreates the final output without running subsequent layers. Verify hooked vs unhooked model outputs and final-layer unembedding consistency for 10 samples.
5. For two sampled outcomes sharing the same exact input and generated prefix before divergence, assert activation equality within numerical tolerance. Fail loudly if not, then investigate dropout, reproducibility, tokenization, hooks, or state contamination.

**Acceptance:** complete manifest, anchor audits, deterministic equality test, memory/throughput report, and export subset for Alfonso. **🛑 GATE 8:** validate alignment and H6 compatibility before probes.

## 9. Probing / early warning (Phase 9 — REDESIGNED)

**Owner:** Alfonso, CPU on exported H6; H7 v2.

**Mandatory split:** partition by task/repository *before* generating probe features; prefixes and descendants never cross splits. Separate train, calibration and untouched test. Deduplicate imported source tasks and variants across splits.

1. **Constraint-content/accessibility probe:** Prefer task-independent categories, or explicit contrasts active-vs-inactive for the **same security topic**. Distinguish “constraint string appears in prompt” from “constraint is active,” and test with lexical distractors, paraphrases, irrelevant mentions, and varying prompt lengths. Report balanced accuracy/AUROC, calibration, task-clustered intervals, and Hewitt–Liang-style control/selectivity.
2. **Risk-propensity model:** Use one embedding per **unique fork context** at assistant start to predict *fork-level* regression risk from independently sampled continuations. Split sampling into non-overlapping risk-label and assessment sets when practical; incorporate Binomial uncertainty from S=20. Do **not** assign different outcome labels to the same predivergence hidden state to train an outcome classifier.
3. **Cross-condition generalization:** train on selected controls/context conditions, test on held-out tasks and different manipulation families. Compare against lightweight **prompt-text/metadata-only predictors** to ask what representation adds beyond visible input.
4. **Early warning:** Only call a probe “early” if evaluated before continuation generation, with held-out task AUROC, precision/recall at prespecified threshold, false-alert rate, and decision cost. Never conflate forecasting regression risk with identifying the causal mechanism.
5. **Mechanism evidence matrix:** report A (decodability) and correlational risk indicators, with confidence and indeterminate states; **do not label H-loss/H-readout/H-override as known ground truth**. Causal I/C come only in Phase 10.

**Acceptance:** probe baselines, lexical/task controls, data leakage audit, calibration, uncertainty, and null-result documentation. **🛑 GATE 9:** freeze probes/thresholds before causal intervention and intervention evaluation.

## 10. Causal mechanism experiments (Phase 10 — REDESIGNED)

**Owner:** GPU executes H8; Alfonso analyzes evidence matrix. Start with **one model × one CWE × one manipulation**, then expand only if aligned and interpretable.

### 10A. Causal estimands and matching

For each *distinct* matched context pair, run the same fixed continuation fixture/anchor. Define `clean` = matched control context and `corrupt` = manipulated context **only for a prespecified measured security preference**; don't assume every control sample is secure. Measure `D = Δlogit_clean − Δlogit_corrupt` plus full-continuation `P(functional AND secure)` and regression probability. If `|D|` is near zero or alternatives are ambiguous, do not compute a meaningful normalized recovery.

### 10B. Patching hierarchy

1. **Sham controls:** patch a tensor from the same run/state, random layer/position, or matched unrelated context; quantify change in generic code validity and unrelated target logits.
2. **Matched anchors:** try layer-wise residual/attn/MLP-output patching at *validated* anchors with explicit source/destination token/semantic alignment. Because prompts differ, patching transfers potentially many contextual features; interpret as **state-component mediation evidence**, not an isolated “security concept” transfer.
3. **Reverse patch:** corrupt→control to test bidirectionality. Add layer/strength dose-response where feasible.
4. **Direction interventions:** add/ablate independently defined constraint-related, insecure-source-related, and random/control directions; vary strength and check both specificity and functional correctness. Avoid selecting intervention layer on the untouched test set.
5. **Source-specific tests:** for insecure references, use attention/head ablation or reference-span perturbation *with appropriate matched, length/semantic controls*; attention patterns alone are descriptive and cannot establish copying.
6. **Full-generation validation:** resample from intervened context multiple times, execute security/function tests, log runtime, and quantify functional degradation, lexical artifacts, and refusals.

### 10C. Metrics and interpretation

- Report raw change in `Δlogit`, behavior outcomes, and CIs. Optional recovery `(Δlogit_patched−Δlogit_corrupt)/(Δlogit_clean−Δlogit_corrupt)` only if sign and minimum pre-registered magnitude of denominator support interpretation; report numerator/denominator and uncertainty. Values outside [0,1] are possible and should not be clipped.
- Mechanism **signature** is a continuous evidence profile `(accessibility, constraint-intervention effect, competing-signal effect, specificity)` with uncertainty. H-loss/H-readout/H-override are optional shorthand **only when supported**; default to **mixed/indeterminate**.
- Treat failure to restore safety as possible ineffective intervention, bad alignment, or alternate mechanisms—not automatic proof of override.

**Acceptance:** at least one credible manipulation with aligned clean/corrupt contexts, sham/reverse controls and **behavioral** effect estimates; documented negative results acceptable. **🛑 GATE 10:** human reviews examples, specificity, causal interpretation, effect size and uncertainty; only then design dispatch strategy for Phase 11.

## 11. Intervention study with independent evaluation (Phase 11 — REDESIGNED)

**Owner:** Shared. Alfonso builds prompt/API baselines and executes oracle/aggregation; GPU builds steering and runs white-box conditions; H9 v2.

**Baselines** (common `apply` interface and identical model/task sampling budget wherever possible):
1. No intervention.
2. Prompt repetition (constraint re-injection each turn).
3. Persistent system-level constraint instruction.
4. Threat-modeling pre-step.
5. Verification gate (Semgrep plus appropriately sandboxed test feedback, max two retries; count retries/tokens/latency).
6. Generic instruction-following steering.
7. Universal security steering (difference-of-means).
8. **Best single targeted method applied universally** (no diagnostic gating).
9. **Shuffled/random dispatch** with matched intervention frequencies and costs.
10. **Oracle diagnosis dispatch** (mechanism assignment from experimental condition or post-hoc controlled tests, used solely as an *upper-bound*, never as a deployable method).
11. **Predicted diagnosis dispatch** (frozen pre-generation model evaluated on held-out tasks).

**Important:** a regression *risk* predictor does **not** identify which mechanism causes a failure. Explicitly train/calibrate diagnosis using **independent causal evidence** from training tasks, or label predictions as “risk-gated universal intervention” rather than pretending they are mechanism-specific. Avoid using future outcomes, patching results, or security labels from test instances to select the method. Include a simple rule-based diagnosis baseline if a mechanism classifier is viable.

**Held-out design:** split by task/repository and benchmark source; freeze probe weights, classification threshold, layer choices, intervention strength, and dispatch policy before final test. If data permit, test one CWE held out as stronger generalization. Comparison includes no-intervention and *cost-matched* universal method so that apparent gain isn't just more compute.

**Primary metric:** `P(functional AND secure)` (task-clustered CI). Secondary: `P(functional AND insecure)`, `P(functional)`, `P(secure | functional)`, refusal/untestable rates, extra tokens, GPU latency, number of retries, false-positive interventions and over-defensiveness. Report by condition, model, CWE, including absolute improvement and negative findings.

**Acceptance:** leakage audit; intervention × condition × model table; effectiveness vs token/latency plot; compare predicted vs oracle vs shuffled/universal dispatch. **🛑 GATE 11:** decide mechanism-informed claim based on added value over strong baselines, not only beating no intervention.

## 12. External validity (core for a strong agent claim)

**Owner:** Shared (Alfonso primarily for labels/analysis, GPU as necessary).

1. Integrate a subset into a real coding-agent scaffold (e.g., mini-swe-agent) with tool calls, repository state, and end-to-end tests. Run a **pre-registered subset** of interventions under the same constraints.
2. Compare externally observed failures to controlled categories; where available, mine naturally occurring security regressions in public agent traces but require evidence that a valid secure state existed earlier. Distinguish naturally occurring from synthetic manipulations.
3. Use held-out task families/benchmarks (candidate: SecureVibeBench / MT-Sec, after checking task/license compatibility) and report distribution shift, failures and transfer limitations. Avoid asserting internal MoE/dense universality based on Qwen-family-only models.

**Acceptance:** at least one external agent setting or clearly bounded claim explaining why not; quantitative success/functional results and representative traces. Do not claim findings generalize to autonomous coding agents without this evidence.

---

## 13. Engineering, compute and coordination

- **No heavy work on login nodes.** Generated code runs only in permitted isolation. GPU/cache paths on checked scratch; set HF and vLLM/Triton/Torch cache paths there. Do not commit weights/raw outputs.
- **SLURM:** explicit account/partition/time/log paths, resumable shard manifests, status-aware retries; large jobs should be job arrays where helpful.
- **Budget gate:** any job/batch estimated >50 GPU-hours requires human approval. Estimate costs from measured pilot throughput, not model size alone; report cumulative GPU-hours and storage.
- **Transport:** Alfonso has no Skipjack GPU allocation. Exchange immutable, manifest-verified H1–H9 shards using a private approved transport (e.g., private HF dataset repository or Globus), with hashes and access control. Confirm institutional policy first.
- **Quality:** `pytest` at each phase, smoke tests for token IDs and activation alignment, cross-backend oracle checks, no silent schema change, CI for CPU tests.
- **Reproducibility:** git SHA, config hash, model/tokenizer revision, sampling parameters and seeds, task split, prompt hashes, oracle version, environment versions, output manifest. `scripts/reproduce_phaseN.sh` for each completed phase.
- **Reporting:** `docs/results/phaseN.md` = implemented steps, observed Ns/effects/CI, assumptions, negative results, compute/time, deviations, next decision. `docs/STATUS.md` is handoff + progress source of truth. Append all approved GATE outcomes to `docs/decisions.md`.
- **Hard stops:** oracle mismatch >5% in spot-check, fewer than 50% of valid required pilot samples, leakage across task split, mismatched activation anchors, unsafe sandbox, scratch >70%, unapproved scientific redesign, or estimated GPU budget breach. Do not work around scientific validity gates simply to satisfy acceptance counts.
- **Branches:** `alfonso/<phase>-<topic>` for his work; one owned branch per phase with schema PR review by both parties. All new v2 fields and changed handoff definitions require coordinated changes before consumption.

## 14. Revised milestones and decision sequence

| Period (rough) | Scientific milestone | Allowed work / gates |
|---|---|---|
| Week 1 | Environment + v2 schema + first oracle tasks | Phase 0–2 in parallel where independent; GATE 0/1/2 |
| Week 2 | Baseline, on-policy prefixes, validated fork conditions | Phases 3–5; GATE 3–5 |
| Week 3 | Behavioral feasibility sample | Phase 6 pilot only; **GATE 6A** |
| Week 4 | One-CWE/one-manipulation mechanistic feasibility | Phases 7–10 small pilot; GATE 7–10 |
| Weeks 5–6 | Expand *only supported* mechanisms, frozen probes | Scale Phase 6 and cache selectively; repeat 7–10; GATE 6B/10 |
| Weeks 7–8 | Independent intervention test | Phase 11; GATE 11 |
| Week 9+ | Real scaffold / held-out benchmark | Phase 12, paper claims/limitations |

### Required final reports before scale-up

1. A **behavior table**: each fork and its matched control, outcome counts, effect estimates, task-clustered CIs, and functional-failure rate.
2. A **representation table**: task-held-out probe metrics, lexical controls and which active constraint is being decoded.
3. A **causality table**: patch/ablation definitions, clean/corrupt alignments, sham controls, Δlogit shifts and executable oracle outcomes.
4. A **diagnostic utility table**: no intervention vs universal vs shuffled vs oracle vs frozen predicted dispatch, including tokens/latency.
5. A **failure audit** with examples where a behavioral regression exists but no supported neural mechanism can be assigned. These are scientific findings, not bugs.

### Interpretation boundaries

- A contextual deletion is evidence about *information availability*, not proof the model “forgot” a visible instruction.
- Probe decodability is evidence about accessible information to a decoder, not proof that the model consults it.
- Attention-to-vulnerable-code is descriptive until a controlled causal perturbation supports its role.
- Teacher-forced token scores and end-to-end security outcomes are different estimands.
- The design estimates effects **conditional on previously secure prefixes**, not general model vulnerability rates.
- A diagnosis-based method has demonstrated added value **only** if its predicted-dispatch test beats appropriate universal and cost-matched baselines on held-out tasks.

**Immediate next action:** Hold Phase 7–11 implementation, review this v2 scientific contract with Alfonso, update `PLAN_alfonso.md` and all H1–H9 schemas to v2, then execute Phases 0–2 and the smallest behavioral+mechanistic pilot. No full-run GPU submission before GATE 10.
