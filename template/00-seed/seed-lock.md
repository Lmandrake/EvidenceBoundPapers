# Seed lock

The seed is immutable. Verify before each session.

## Procedure

Record the hash at G1 (thesis & structure gate):

```
sha256sum 00-seed/seed-paper.md > 00-seed/seed.sha256
```

Verify at every session start:

```
sha256sum -c 00-seed/seed.sha256
```

A mismatch is a HALT. Do not proceed. Do not re-lock. Find out what changed it.

## Recorded

| Date | Hash | Locked by |
|---|---|---|
| | | |
