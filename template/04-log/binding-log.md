# Binding log

Append-only, written by `evidence-binder`.

**The third list is the valuable one.** A claim reported as unsupported is a task
for the human. A claim reported as supported when it is not is a silent failure:
it renders cleanly, reads fluently, scores well, and is wrong.

```
## <ISO datetime>
- attempted: <n> claims
- bound Strong: <ids>
- bound Suggestive: <ids> — <why not Strong: unverifiable span / single source / needs an inferential step>
- could not support: <ids>
  - SUP-0034 | <the claim> | <what the corpus has instead> | <why it does not reach>
- retagged: SUP-0021 causal -> empirical — <no mechanism available>
- corpus requests filed: <ESC ids>
```
