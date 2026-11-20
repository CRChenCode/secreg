# secreg

Mechanistic diagnosis of security regression in coding agents.

See [`PLAN.md`](PLAN.md) (GPU-owner perspective, Skipjack) and [`PLAN_alfonso.md`](PLAN_alfonso.md)
(CPU/API workstream) for the full research plan, phase-by-phase tasks, and acceptance criteria.
[`docs/data_schema.md`](docs/data_schema.md) is the canonical reference for every record schema;
[`docs/STATUS.md`](docs/STATUS.md) tracks phase/handoff status; [`docs/decisions.md`](docs/decisions.md)
logs every GATE outcome.

## Setup

```bash
uv sync --extra gpu   # on Skipjack (GPU owner)
uv sync --extra cpu   # on a local machine, no GPU (Alfonso)
uv run pre-commit install
```

Cluster facts (partitions, account, scratch root, sandbox backend) are in
[`configs/cluster.yaml`](configs/cluster.yaml) / [`docs/cluster.md`](docs/cluster.md).
