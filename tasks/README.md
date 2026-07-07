# Benchmark Tasks

Each task is a self-contained fixture with:

- `task.json`: metadata and verifier command
- `prompt.md`: exact prompt to give the product under test
- `repo/`: starting repository copied into each run
- `post_prepare/`: optional overlay copied into the worktree after the baseline
  commit, used to create reproducible dirty-worktree state
- `verifier/`: task-owned verifier copied outside the product worktree

The verifier must be independent of the product. A product passes a task only
when the verifier exits zero in the final worktree.
