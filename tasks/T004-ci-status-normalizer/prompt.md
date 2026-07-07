# Task: Fix The Status Normalizer CI Failure

You are working in the prepared repository.

The CI check fails because status names coming from tickets are not normalized
consistently. Fix the implementation so these inputs normalize correctly:

- `todo`
- `TO DO`
- `in progress`
- `in-progress`
- `blocked`
- `done`

Unknown statuses should normalize to `unknown`. Preserve the existing public
function names and run the verifier before you finish.

