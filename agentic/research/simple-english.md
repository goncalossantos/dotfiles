# Simple technical English

## The standard

The requested standard is **ASD-STE100 Simplified Technical English (STE)**,
maintained by the ASD Simplified Technical English Maintenance Group (STEMG).
It is a controlled natural language for technical documentation, originally
created for aircraft maintenance. It is not “AST”.

Primary sources, consulted **2026-11-01**:

- [Official ASD-STE100 site](https://www.asd-ste100.org/)
- [Standard structure](https://www.asd-ste100.org/structure.html)
- Use the official site's **Downloads → Issue 9** route for the current standard
  and its terms. Check the current issue before any compliance work.

The home page and its description of ownership and history were retrieved. The
full standard and dictionary were not reviewed in this iteration; the structure
link is a follow-up reference, not evidence of a full compliance assessment.

## Repository policy

`AGENTS.md` uses **STE-inspired plain English**, not certified or fully compliant
STE. Formal STE includes controlled vocabulary and writing rules that a short
agent prompt cannot replace. No copy of the copyrighted standard or dictionary
is included here.

Our practical subset:

1. Short, direct sentences with one main idea.
2. Active voice and concrete verbs.
3. Consistent terms; define acronyms at first use.
4. One action per procedural step; conditions before instructions.
5. Literal language without idioms, while retaining necessary technical precision.

These are local editorial rules. They are not quoted standard clauses.

## Example

Before:

> In order to facilitate the initialization of the environment, it is recommended
> that the requisite dependencies are installed prior to proceeding.

After:

> Install the dependencies before you start the app.

Keep identifiers intact: simplify the explanation of `Authorization: Bearer`,
not the header itself. Explain difficult concepts accurately instead of replacing
them with vague words. Plain language is compatible with technical depth.
