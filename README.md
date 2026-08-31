# team_31 primary entry (llm-as-scientist-v2)

Tier-1 **primary** entry of team_31 for the
[Silicon Sample Benchmark](https://janpfander.github.io/llm_predictions_megastudy/):
`predictions/team_31_T1_primary_v1.csv`, 54,000 synthetic respondents
(16 interventions × 13 outcomes), with the completed `registration.md` and `metadata.json`.

**Method.** Dataset acquisition → [prime-agent](https://github.com/PrimeIntellect-ai/prime-agent) loop → derivation of
individual-level rows. The predictions are analysis-first: the loop predicts the study's
published analysis table and the individual-level rows are synthesized backwards from it.
The loop has a free strategy and externally administered testing. No restriction on how
the agent (`claude-opus-5`) makes predictions: it is free to use scripts, simulator calls,
or anything else. The restrictions sit on information instead: there are held-out data
that are excluded from its container, and feedback comes only through an oracle (only 2
submissions per study allowed). Its outcome was to write and fit an explicit structural
model on a train split of eleven published message experiments. No human wrote or edited
any predicted number. The method is the start state of that loop, held in the code
repository. Everything the agent decided inside it is recorded output, deposited under
`run_record/` here and as the escrowed session logs.

## What is where

| path | what |
|---|---|
| `predictions/` | the scored prediction file (sha256 in `metadata.json`) |
| `registration.md` | the completed 39-item method registration |
| `run_record/` | the loop's recorded output: the model code and anchor tables the agent wrote, the campaign records (scoreboard, gate verdicts, pre-registrations), and copies of the prompts and frozen definitions it started from. The entry is a deterministic function of these files |
| `raw_model_logs/` | registration item K.2: manifest and public hash of the escrowed raw agent-log bundle (disclosure class B, restricted-access record) |

The campaign **environment and start state** (validation oracle, gate, container launcher,
frozen definitions) are in the team's code repository,
[silicon-sample-submission](https://github.com/tobihol/silicon-sample-submission) (registration K.1).

## Template provenance

This repository is a clone of the organizers' submission template
([janpfander/silicon-sample-submission](https://github.com/janpfander/silicon-sample-submission)
@ `546f928`), which provides `Makefile`, `scripts/`, `survey/`, `codebook.csv`, `FAQ.md`, and
`README.qmd`. The template's example data were replaced by this entry. Validation: `make check`
(the organizers' validator) passes with no failures.

## Licensing of the shipped survey materials

Your Zenodo license (default `CC-BY-4.0` in `metadata.json`) applies to **your** contribution:
your code, predictions, and documentation. The shipped `survey/` folder is different: several
intervention stimulus texts adapt previously published journalism and other copyrighted material,
included here for scholarly research use. Keep `survey/` in your deposit unchanged (it documents
what your respondents saw), but your license grant does not and cannot re-license those
underlying texts.

## Team

Registered team **team_31**: Tobias Holtdirk, Bolei Ma (LMU Munich, SODA Lab).
Contributor: Haiwen Huang. Contact: tobias.holtdirk@lmu.de.
