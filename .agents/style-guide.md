# AIMD-L Documentation Style Guide (14-09-2026)

Guidelines for writing clear, maintainable SOPs, manuals, and policies.

---

## 1. Voice and Tone

* **Imperative mood for procedures:** Write instructions as direct commands rather than descriptions.
  * *Good:* "Tighten the collar until finger-tight."
  * *Avoid:* "The user should carefully tighten the collar."
* **Active voice and concise phrasing:** State who does what. Eliminate conversational filler, pleasantries, and throat-clearing sentences.
* **Exact values over approximations:** Never use vague qualifiers like "heat moderately" or "wait a bit." State exact units, tolerances, and durations (e.g., "Heat to 150 °C ± 5 °C for 10 minutes").

---

## 2. Structure and Headings

* **One H1 per document:** The top-level `# Title` must match the front matter `title` property.
* **Sentence case for headings:** Use `## Instrument startup` rather than `## Instrument Startup`.
* **Sequential vs. non-sequential steps:**
  * Use **numbered lists** (`1.`, `2.`, `3.`) strictly for ordered operational sequences.
  * Use **bullet lists** (`*`) for prerequisites, equipment lists, and options.

---

## 3. Material for MkDocs Admonitions

Use callouts sparingly to preserve visual impact. Match callout severity to the page's `safety_level`:

* **Notes & Tips (`!!! info` or `!!! tip`):** Informational context, background rationale, or shortcuts.
* **Operational Warnings (`!!! warning`):** Potential equipment damage, invalid test runs, or non-hazardous errors.
* **Hazards & Safety (`!!! danger`):** Chemical, electrical, laser, or physical injury hazards requiring specific PPE or immediate shutdown steps.

```markdown
!!! danger "High Voltage Hazard"
    Ensure the main disconnect is locked out before opening the enclosure.
```

## 4. Cross-References and Links

* **Strict relative paths:** Always link to local Markdown files using relative paths (e.g., [Startup Guide](../instruments/maxima.md)) rather than absolute URLs or site routes.
* **Link hygiene:** Internal dead links or anchor mismatches cause `mkdocs build --strict` to fail CI. Always verify targets exist before committing.
* **Descriptive anchor text:** Avoid "click here" or "link". Use the target page's title or concept name.

## 5. File and Asset Conventions

* **Naming:** Use lowercase kebab-case for all folders and Markdown files (e.g., sputter-coater-sop.md).

* **Images:** Place images in an assets/ or images/ directory adjacent to the document. Always include descriptive alt text:

    ```markdown
    ![Emergency shutoff valve on the lower-left panel](images/shutoff-valve.png)
    ```

* **Code and Commands:** Wrap terminal inputs and file paths in backticks (code). Label multi-line blocks with language identifiers (bash, python, yaml).
