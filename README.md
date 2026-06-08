# garethpaul.com

## Overview

`garethpaul/garethpaul.com` is a static web project. GarethPaul.com Repo

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: Python (14), JavaScript (2), shell (1).

## Repository Contents

- `README.md` - project overview and local usage notes
- `.worktrees` - source or example code
- `main.py`
- `SECURITY.md` - security reporting and disclosure guidance
- `static` - source or example code
- `templates` - source or example code
- `VISION.md` - project direction and maintenance guardrails

Additional scan context:

- Source directories: .worktrees, static, templates
- Dependency and build manifests: none detected
- Entry points or build surfaces: main.py
- Test-looking files: no obvious test files detected

## Getting Started

### Prerequisites

- Git

### Setup

```bash
git clone https://github.com/garethpaul/garethpaul.com.git
cd garethpaul.com
```

The setup commands above are derived from repository files. Legacy mobile, Python, or JavaScript samples may require older SDKs or package versions than a modern workstation uses by default.

## Running or Using the Project

- No single runtime entry point was identified. Start by reading the source files and manifests listed above.

## Testing and Verification

- No dedicated automated test command was identified from the checked-in files. Verify changes by running the relevant build or manually exercising the sample.

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Configuration and Secrets

- Detected references to Twitter. Keep API keys, OAuth credentials, tokens, and account-specific values in local configuration only.
- `const.py` reads runtime configuration from environment variables:
  `GARETHPAUL_MAP_API_KEY`, `GARETHPAUL_GEOCODE_KEY`,
  `GARETHPAUL_INSTAGRAM_ID`, `GARETHPAUL_INSTAGRAM_ACCESS_TOKEN`,
  `GARETHPAUL_GLASS_URL`, `GARETHPAUL_GLASS_API_URL`,
  `GARETHPAUL_PICASA_API_URL`, and `GARETHPAUL_MAP_API_URL`.

The app reads required deployment settings from environment variables through
`const.py`. Set these in the App Engine deployment environment or in a local
shell before starting the app:

- `GARETHPAUL_MAP_API_KEY`
- `GARETHPAUL_GLASS_URL`
- `GARETHPAUL_GEOCODE_KEY`
- `GARETHPAUL_MAP_API_URL`
- `GARETHPAUL_GLASS_API_URL`
- `GARETHPAUL_PICASA_API_URL`
- `GARETHPAUL_INSTAGRAM_ID`
- `GARETHPAUL_INSTAGRAM_ACCESS_TOKEN`

## Security and Privacy Notes

- Review changes touching authentication or token handling; examples from the scan include .worktrees/fix/issue-1-https-openweather/templates/stream.html, templates/stream.html.
- Review changes touching external API calls or credential-adjacent configuration; examples from the scan include .worktrees/fix/issue-1-https-openweather/instagram.py, .worktrees/fix/issue-1-https-openweather/templates/profile.html, instagram.py, templates/profile.html.
- Review changes touching network requests, sockets, or service endpoints; examples from the scan include .worktrees/fix/issue-1-https-openweather/docs/plans/2026-06-08-issue-1-https-openweather.md, .worktrees/fix/issue-1-https-openweather/instagram.py, .worktrees/fix/issue-1-https-openweather/map.py, .worktrees/fix/issue-1-https-openweather/scripts/check-baseline.sh, and 6 more.
- Review changes touching file, media, JSON, XML, CSV, OCR, or data parsing; examples from the scan include .worktrees/fix/issue-1-https-openweather/app.yaml, .worktrees/fix/issue-1-https-openweather/base.py, .worktrees/fix/issue-1-https-openweather/glass.py, .worktrees/fix/issue-1-https-openweather/instagram.py, and 6 more.

## Maintenance Notes

- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.

## Existing Project Notes

Prior README summary:

> garethpaul.com <!-- README-OVERVIEW-IMAGE --> garethpaul.com ============== This is the repo for my public site at garethpaul.com Moved from heroku over to GAE.
