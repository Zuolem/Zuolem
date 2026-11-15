# Profile development

The identity used throughout this profile is **ZUOLEM**. Keep personal contact information, employers, locations, and private source code out of this repository.

- `README.md`: GitHub-compatible profile composition, accessible image descriptions, and text project notes.
- `assets/`: self-contained SVG artwork; no external fonts, scripts, or image services.
- `scripts/build_assets.py`: original hero, project drawings, and toolbox badges. Edit this file, then run `python scripts/build_assets.py` from the repository root.
- `scripts/update_activity.py`: downloads only ZUOLEM's publicly visible GitHub contribution calendar and builds `assets/activity.svg` using Python's standard library. No token or private repository access. The public calendar can include anonymised private contribution intensity if enabled in GitHub's own profile settings; no private names or source code are retrieved.
- `scripts/validate.py`: checks XML, accessible titles, view boxes, active SVG content, local image references, and the README's external link allowlist. Run `python scripts/validate.py`.
- `.github/workflows/activity.yml`: refreshes the activity snapshot every Monday at 06:23 UTC or manually, on `main` only, after this PR is merged by a reviewer. It writes only the activity SVG. No workflow is run or deployed by opening the design PR.

## Updating

Use Python 3.10 or newer. No packages are required. Run the two generators and the validator, then review the diff. A failed calendar request or unexpected HTML fails before replacing the existing snapshot. GitHub's public calendar HTML is an undocumented interface and may require parser updates. Scheduled workflows can be delayed or disabled by GitHub after prolonged repository inactivity. Protected branches that reject bot commits require an approved update PR workflow instead.

The hero is responsive through its SVG view box. Cards use two fluid columns; toolbox badges wrap naturally. Project descriptions also have a text view for small screens and image failures. Inspect the rendered PR README at desktop and mobile widths before merging. SVG animations are decorative opacity changes with a complete static composition underneath and a reduced-motion override. GitHub may cache SVGs or omit animations.

Keep project cards unlinked while their repositories remain private. Add tools only when supported by actual experience. Do not introduce invented metrics, public repository claims, or third-party statistics.
