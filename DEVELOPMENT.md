# Profile development

The identity used throughout this profile is **ZUOLEM**. Keep personal contact information, employers, locations, and private source code out of this repository.

- `README.md`: GitHub-compatible profile composition, accessible image descriptions, and text project notes.
- `assets/`: self-contained SVG artwork; no external fonts, scripts, or image services.
- `scripts/build_assets.py`: original panoramic hero, lab notes (no code block or copy button), tool icons with research panel, and compact two-column project cards. Each section has a dedicated mobile composition. Edit this file, then run `python scripts/build_assets.py` from the repository root.
- `scripts/update_activity.py`: downloads only ZUOLEM's publicly visible GitHub contribution calendar and builds `assets/activity.svg` using Python's standard library. No token or private repository access. The public calendar can include anonymised private contribution intensity if enabled in GitHub's own profile settings; no private names or source code are retrieved.
- `scripts/validate.py`: checks XML, accessible titles, view boxes, active SVG content, local image references, and the README's external link allowlist. Run `python scripts/validate.py`.
- `.github/workflows/activity.yml`: refreshes both activity SVGs every Monday at 06:23 UTC or manually, on `main` only, after this PR is merged by a reviewer. No workflow is run or deployed by opening the design PR.

## Updating

Use Python 3.10 or newer. No packages are required. Run the two generators and the validator, then review the diff. A failed calendar request or unexpected HTML fails before replacing the existing snapshot. GitHub's public calendar HTML is an undocumented interface and may require parser updates. Scheduled workflows can be delayed or disabled by GitHub after prolonged repository inactivity. Protected branches that reject bot commits require an approved update PR workflow instead.

The README uses GitHub-compatible picture elements to select a dedicated composition below 600px. Mobile project cards stack vertically; the research panel moves below the tools. Every image has a descriptive alt text; project descriptions also have an expandable text view. SVG animations are decorative opacity changes with a complete static composition underneath and a reduced-motion override. GitHub may cache SVGs or omit animations. The sidebar and GitHub navigation are outside the README's control.

The contribution heat map and isometric columns use the same actual daily public calendar levels (0–4). Column heights encode intensity, not exact contribution counts. Miniature project charts are explicitly decorative and never presented as measured results. The conceptual reference's degrees, additional tools, and unconfirmed project language tags are intentionally omitted.

Keep project cards unlinked while their repositories remain private. Add tools only when supported by actual experience. Do not introduce invented metrics, public repository claims, or third-party statistics.
