<p align="center">
  <img src="./assets/coaxio-banner.svg" alt="Coaxio: open source homelab tooling, built by Domenico" width="100%">
</p>

<p align="center">
  <a href="https://coaxio.dev"><img alt="Website" src="https://img.shields.io/badge/coaxio.dev-visit-C87A44?style=flat-square&labelColor=07222A&logo=astro&logoColor=5EEAD4"></a>
  <img alt="Focus" src="https://img.shields.io/badge/focus-homelab%20day--zero-0F3A42?style=flat-square&labelColor=07222A">
  <img alt="Profile views" src="https://komarev.com/ghpvc/?username=Coaxio&style=flat-square&color=0F3A42&label=visits">
</p>

## Hello

I'm Domenico, a systems integrator and cloud architect with sysadmin roots. I spend my days making other people's infrastructure behave, and my evenings writing the tooling I wish had existed when I was doing it by hand.

**Coaxio** is where that tooling lives: a small ecosystem of open source projects for homelabs and proof-of-concept infrastructure.

I don't reimplement mature software. WireGuard, Caddy, and Authelia are already excellent; what's missing is the layer that wires them together on a bare host without a weekend of yak-shaving.

## What I'm building

| Project | What it does | State |
| --- | --- | --- |
| [**coaxio-forge**](https://github.com/Coaxio/coaxio-forge) | Day-zero scaffolding CLI: takes a bare Debian or Ubuntu host to a working homelab with WireGuard, Caddy, Authelia, and monitoring | ![](https://img.shields.io/badge/pre--alpha-C87A44?style=flat-square&labelColor=07222A) |
| [**coaxio.dev**](https://coaxio.dev) | The site: notes on what I break, and where the projects are documented | ![](https://img.shields.io/badge/in%20progress-5EEAD4?style=flat-square&labelColor=07222A) |

## How I pick tools

Go for orchestrators, because config generation lives next to Caddy, Docker, and Kubernetes and the contributor barrier stays low. Rust when there's a daemon parsing untrusted bytes at speed, which is a real problem and not a fashion statement. Everything else is a judgement call I'm happy to argue about in an issue.

<p>
  <img alt="Go" src="https://img.shields.io/badge/Go-0F3A42?style=flat-square&logo=go&logoColor=5EEAD4">
  <img alt="Rust" src="https://img.shields.io/badge/Rust-0F3A42?style=flat-square&logo=rust&logoColor=5EEAD4">
  <img alt="Bash" src="https://img.shields.io/badge/Bash-0F3A42?style=flat-square&logo=gnubash&logoColor=5EEAD4">
  <img alt="Debian" src="https://img.shields.io/badge/Debian-0F3A42?style=flat-square&logo=debian&logoColor=5EEAD4">
  <img alt="Docker" src="https://img.shields.io/badge/Docker-0F3A42?style=flat-square&logo=docker&logoColor=5EEAD4">
  <img alt="Kubernetes" src="https://img.shields.io/badge/Kubernetes-0F3A42?style=flat-square&logo=kubernetes&logoColor=5EEAD4">
  <img alt="WireGuard" src="https://img.shields.io/badge/WireGuard-0F3A42?style=flat-square&logo=wireguard&logoColor=5EEAD4">
  <img alt="Caddy" src="https://img.shields.io/badge/Caddy-0F3A42?style=flat-square&logo=caddy&logoColor=5EEAD4">
  <img alt="Prometheus" src="https://img.shields.io/badge/Prometheus-0F3A42?style=flat-square&logo=prometheus&logoColor=5EEAD4">
  <img alt="Astro" src="https://img.shields.io/badge/Astro-0F3A42?style=flat-square&logo=astro&logoColor=5EEAD4">
  <img alt="Cloudflare" src="https://img.shields.io/badge/Cloudflare-0F3A42?style=flat-square&logo=cloudflare&logoColor=5EEAD4">
  <img alt="GitHub Actions" src="https://img.shields.io/badge/GitHub%20Actions-0F3A42?style=flat-square&logo=githubactions&logoColor=5EEAD4">
</p>

## Numbers

<p>
  <img height="165" alt="Coaxio's GitHub stats" src="./assets/stats.svg">
  <img height="165" alt="Contribution streak" src="https://streak-stats.demolab.com?user=Coaxio&hide_border=true&background=07222A&stroke=16515A&ring=C87A44&fire=E39A62&currStreakNum=E8F4F2&currStreakLabel=5EEAD4&sideNums=B9D6D3&sideLabels=7FA7A5&dates=7FA7A5">
</p>

<img alt="Contribution activity" src="./assets/activity.svg">

## Working notes

- Orchestrate mature tools, don't reimplement protocols.
- Document the limitation instead of hiding it. A `TODO` with the exact command beats a silent workaround.
- Validate a design as a mockup before it becomes a directory structure.
- Secrets stay host-local and encrypted with age. Coaxio is not going to be your vault.
- Every project is also a way to learn a language properly, so idiomatic beats clever.

## Get in touch

Issues and pull requests are the fastest route, on whichever repo the problem belongs to. Longer writing lives at [coaxio.dev](https://coaxio.dev). If you're running Coaxio tooling on something unusual, I'd like to hear how it broke.
