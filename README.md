# GitHub

Video-graphic generation is set up via [HyperFrames](https://github.com/heygen-com/hyperframes) — an
open-source framework that turns HTML, CSS, media, and seekable animations into deterministic MP4
videos.

## What's installed

- `.claude/skills/` — the HyperFrames core skill set for AI coding agents (the `/hyperframes`
  router plus the `hyperframes-core`, `hyperframes-animation`, `hyperframes-audio`,
  `hyperframes-cli`, `hyperframes-creative`, `hyperframes-keyframes`, `hyperframes-registry`, and
  `media-use` domain skills). Ask an agent (e.g. Claude Code) to use `/hyperframes` to plan and
  build a video.
- `index.html` — a minimal starter composition.
- `package.json` scripts that call the `hyperframes` CLI on demand via `npx` (nothing is installed
  globally; each command fetches the CLI the first time it runs).

## Usage

```bash
npm run dev      # live preview in the browser
npm run check     # lint + runtime + layout + motion + contrast checks
npm run render    # render the composition to MP4
npm run publish   # publish and get a shareable link
```

Requirements: Node.js 22+ and FFmpeg.

See the [HyperFrames Quickstart](https://hyperframes.heygen.com/quickstart) and
[docs](https://hyperframes.heygen.com/introduction) for more.
