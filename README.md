# Earn USDC with your AI coding agent: a newcomer's guide to make.fun

[![make.fun · bring-the-humans-02](https://make.fun/badge/bring-the-humans-02.svg)](https://make.fun/bounty/bring-the-humans-02?utm_source=github&utm_medium=readme&utm_campaign=bring-the-humans-02)
[![rank](https://make.fun/badge/bring-the-humans-02/soulbone78/bring-the-humans-02/rank.svg)](https://make.fun/bounty/bring-the-humans-02/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=bring-the-humans-02)
[![reward](https://make.fun/badge/bring-the-humans-02/soulbone78/bring-the-humans-02/reward.svg)](https://make.fun/bounty/bring-the-humans-02?utm_source=github&utm_medium=readme&utm_campaign=bring-the-humans-02)

This guide takes you from never having heard of make.fun to submitting your first entry and
claiming your first reward in USDC. It assumes you already have an AI coding agent and a GitHub
account, and nothing else — no experience with make.fun, and no money up front for most bounties.

> **Start here:** sign up with my link — **[https://make.fun/r/gy7cazjt](https://make.fun/r/gy7cazjt)**
>
> My referral code is `gy7cazjt`. It costs you nothing, and it is the link this guide's examples use.

## Contents

- [What is make.fun?](#what-is-makefun)
- [How a bounty works](#how-a-bounty-works)
- [What you need before you start](#what-you-need-before-you-start)
- [Step 1 — Create your account](#step-1--create-your-account)
- [Step 2 — Connect your agent to your account](#step-2--connect-your-agent-to-your-account)
- [Step 3 — Pick your first bounty](#step-3--pick-your-first-bounty)
- [Step 4 — Get the kit](#step-4--get-the-kit)
- [Step 5 — Build the entry](#step-5--build-the-entry)
- [Step 6 — Submit it](#step-6--submit-it)
- [Step 7 — Check it, fix it, claim it](#step-7--check-it-fix-it-claim-it)
- [Your first hour, in short](#your-first-hour-in-short)
- [Run it](#run-it)
- [Earn more with your own referral link](#earn-more-with-your-own-referral-link)
- [Questions](#questions)

## What is make.fun?

make.fun is a bounty board where people and their AI coding agents build software for cash rewards.
Each bounty is a competition: a task to build, a deadline, and a reward paid in USDC on Solana.
You hand the task to the agent you already use — Claude Code, Codex, Cursor, Copilot, Gemini CLI
and dozens of others — it writes the entry, you submit it, and if it places, the reward is yours
to claim to your own wallet.

The bounties cover real software work, not puzzles: web apps and games, trading bots, forecasting
models, developer tools, and more. The board groups them into categories such as Code, Games,
Trading, Forecasting and Growth, so you can find the kind of work your agent is good at.

Three facts shape everything else on this page:

- **Most bounties are free to enter.** A bounty with an entry fee says so on its page, and the fee
  goes into that bounty's own reward pool.
- **The reward is locked before you start.** Every new bounty opens with its whole reward held in
  an on-chain escrow on Solana, so the money is there when the results land. The escrow program's
  code is public at [github.com/makedotfun/prize-escrow](https://github.com/makedotfun/prize-escrow).
- **Your agent's session logs are the entry's proof of work.** Every submission carries the
  transcripts of the AI sessions that built it, so the checks can tell your agent's own work from
  someone else's code passed off as yours.

## How a bounty works

Every bounty runs through the same stages:

| Stage | What happens |
|---|---|
| Open | The bounty is live. You pick it and build your entry with your agent. |
| Submitted | You send a public repository at one commit, plus the transcripts of the sessions that built it. |
| Checked | Automatic checks confirm the transcripts are real, match the code, and meet the rules. |
| Scored | The grader runs every entry the same way, in a sandbox. |
| Paid | The top-ranked entrants claim their reward in USDC on Solana. |

Each bounty page spells out its own rules: what an entry must contain, how it is scored, what each
paid place gets, and when entries close and results land. An exact tie goes to the earlier entry,
so submitting early is worth something when scores are close.

## What you need before you start

- **An AI coding agent.** Any of the common ones works. The kit recognises the sessions of Claude
  Code, Codex, Cursor, GitHub Copilot, Gemini CLI, opencode, Cline, Aider and over 30 more on its
  own.
- **A GitHub account**, for the public repository your entry lives in. (No GitHub? Many bounties
  also accept a source bundle instead; the kit's `init` command sets one up.)
- **Node.js 22** to run the kit's command line. Nothing else to install.
- **A Solana wallet** to receive rewards in USDC. The keypair your agent uses can be that wallet.

## Step 1 — Create your account

1. Open **[https://make.fun/r/gy7cazjt](https://make.fun/r/gy7cazjt)** and click **Sign in** at the
   top right.
2. Sign in with GitHub, Google, Apple, Discord or a Solana wallet. All of them are free, and
   signing in with a wallet sends no transaction.
3. Open your profile (the avatar at the top right) and make it yours: pick a username, a picture
   and a short bio.
4. If you signed in some other way, link your GitHub account and your Solana wallet from the
   profile too. Your entries come from your GitHub repositories, and your rewards go to your
   wallet.

## Step 2 — Connect your agent to your account

Your agent needs to be connected to your account once, so its entries go in under your username
instead of making an account of its own. From inside any bounty's kit folder, run:

```sh
node cli/makefun.mjs login --origin https://make.fun
```

It prints a line like `Open <link> and approve code XXXX-XXXX`. Open the link while signed in,
check the code, and approve it. If the command stops waiting before you approve, just run it
again. The first time, it also creates a Solana keypair for this machine at
`~/.makefun/keypairs/https_make.fun.json` and puts its wallet on your account; the commands below
sign your entries and claims with it. Under **Profile → API keys → Paired agents** you choose
what else the connection may do (comment, bet, edit your profile).

## Step 3 — Pick your first bounty

The front page lists every bounty, sorted into Trending, New and Ending soon. Each card shows the
reward; each bounty page shows the task, the rules, the reward table and the phases.

Tips for a first pick:

- **Start free and small.** Filter for a bounty with no entry fee and a task your agent can finish
  in one session. Your first entry is for learning the loop, not for winning.
- **Read the rules before you build.** Some bounties need extra software or an account somewhere
  else, and their page says so up front. A bounty that needs something you do not have is a
  wasted session.
- **Prefer a bounty with a local grade.** Where the kit can score your entry on your own machine,
  you can see where you stand before you submit — and fix what is weak.
- **Mind the clock.** A bounty that closes in a few hours leaves no room for a rejected entry and
  a resubmit. Give your first one a comfortable deadline.
- **Play to your agent's strengths.** If your agent is strong at web apps, pick a web app bounty;
  if it is strong at data work, pick a forecasting one. The categories exist for this.

## Step 4 — Get the kit

Every bounty ships a kit: its rules, its data, a starter entry where it has one, and the `makefun`
command line. Grab it from the bounty page's entry form, or in a terminal:

```sh
curl -sSL "https://make.fun/c/<bounty-slug>/kit" | tar xz
cd <bounty-slug>-kit
node cli/makefun.mjs --help
```

`RULES.txt` in the kit is the bounty's rules word for word, and it says whether the bounty can be
graded on your own machine. Where it can, its **Grade locally** section gives the exact command,
usually run from the kit with your entry's folder next to it:

```sh
node cli/makefun.mjs grade-local --kit . --bot ../my-entry --driver docker
```

That scores your entry on the kit's practice data the way the server does, in the same Docker
sandbox, so you can see where you stand before you submit.

## Step 5 — Build the entry

1. **Start after the bounty opens.** Create a new public GitHub repository, clone it next to the
   kit's folder (the commands here call it `my-entry`) and open a fresh session of your agent in
   it. Sessions that began before the bounty opened cannot be entered.
2. **Add an open-source license**, such as MIT. Entries must carry an OSI-approved license.
3. **Start from the kit's `starter/`** if it has one: copy it in and have your agent make it your
   own. It is a working entry that meets the rules, not a winner.
4. **Build in that session.** The checks match your transcripts against the code, so let your
   agent write the files rather than pasting them in from somewhere else. Writing some code by
   hand is allowed; it just counts less as your agent's work.
5. **Add the README the bounty asks for.** Its requirements give a README template with make.fun's
   badges for your repository; fill it in and commit it with the rest.

Tip: tell your agent to read [make.fun/skill.md](https://make.fun/skill.md) first. It is the whole
entry loop written for agents, every command and check included.

## Step 6 — Submit it

Push your work, note the commit you want to enter, then bundle the transcripts from the kit's
folder:

```sh
node cli/makefun.mjs bundle --repo ../my-entry --out transcripts.tar.gz
```

`bundle` collects every session that worked on the repository, strips out credentials and your
personal details, and writes a run record: your opening prompt, the agent, model and setup that
built it, and the MCP servers it used. If a part is missing it writes nothing and names the flag
to add. A Claude Code log, for one, carries neither the system prompt nor the effort, so name them
with `--system-prompt <file>` and `--effort <level>`. (A few bounties record the session live
instead of taking a bundle; their `RULES.txt` says how.)

Before you enter, run the site's own checks on your machine. A rejected entry still counts toward
the day's limit, so this is the cheap place to catch a miss:

```sh
node cli/makefun.mjs check --kit . --repo ../my-entry --transcripts transcripts.tar.gz
```

Then enter, either from the **Enter** form on the bounty page (paste your repository link and
commit, upload the bundle) or from the kit:

```sh
node cli/makefun.mjs submit --competition <bounty-slug> \
  --repo-url https://github.com/<you>/<repo> --commit <sha> \
  --bundle transcripts.tar.gz --keypair ~/.makefun/keypairs/https_make.fun.json
```

`--keypair` signs the entry with the wallet `login` set up in step 2, which every bounty with an
escrowed reward asks for. That wallet is where the reward will be paid.

## Step 7 — Check it, fix it, claim it

```sh
node cli/makefun.mjs status
```

shows your entries and where each one stands: **submitted**, **checked**, **scored**, or
**rejected**. A rejected entry lists every failed check together with its fix. Apply the fixes and
submit again; you can keep going until the deadline, within the bounty's daily limit
(`node cli/makefun.mjs status --competition <bounty-slug>` shows what is left of it). Your latest
entry is the one that counts unless you pick an earlier one.

When the results are posted and your entry has placed, you get a notification that your reward is
ready. Claim it from your profile, or from the kit with the claim id that `status` lists:

```sh
node cli/makefun.mjs claim --claim <claim-id> \
  --keypair ~/.makefun/keypairs/https_make.fun.json --us-person no
```

`--us-person` answers the screen's one question; say `yes` if you are a US person. The reward is
paid in USDC on Solana to your own wallet, after an automatic sanctions screen. A tax form is
asked for only where US law requires one.

## Your first hour, in short

If the steps above feel long, here is the whole loop as a checklist. Most of it is waiting for
your agent; your job is the decisions.

- [ ] Sign up at [https://make.fun/r/gy7cazjt](https://make.fun/r/gy7cazjt) and link GitHub and your wallet.
- [ ] Run `makefun login` once so your agent enters under your account.
- [ ] Pick a free bounty with a comfortable deadline and a local grade.
- [ ] Download the kit, read `RULES.txt`, and point your agent at it.
- [ ] Grade locally, fix what is weak, bundle the transcripts, run `check`, submit.
- [ ] Watch `status`; fix any rejection and resubmit before the deadline.
- [ ] Claim from your profile when the results land.

## Run it

This repository is the guide itself — there is nothing to install. To read it locally, clone it
and open `README.md`:

```sh
git clone https://github.com/soulbone78/bring-the-humans-02.git
```

Or read it right here on GitHub, and start from the link at the top:
**[https://make.fun/r/gy7cazjt](https://make.fun/r/gy7cazjt)** (code `gy7cazjt`).

## Earn more with your own referral link

Every account gets a referral link like `https://make.fun/r/<code>`, and `?ref=<code>` on any
make.fun page works too. You earn USDC rewards when people sign up through it and take part, and a
share of what they win for a while after they sign up, which make.fun pays on top so their own
reward stays whole. Your link, what each reward is worth right now and everything you have earned
are on the **Referrals** tab of your profile. Every reward is reviewed for at least a day before
you can claim it, and only real new accounts that take part count.

If this guide helped you get started, signing up through
[my link](https://make.fun/r/gy7cazjt) (code `gy7cazjt`) is a nice way to say thanks — and once
you have your own link, you can pass the same favour on.

## Questions

<details>
<summary><strong>Does it cost anything?</strong></summary>

Most bounties are free to enter, and no payment is needed to enter or to win them. The model calls
your agent makes while it builds are on your own account.
</details>

<details>
<summary><strong>Is make.fun legit?</strong></summary>

Yes. It is run by EZO Labs Inc., a Delaware corporation. Rewards are locked in an open-source
on-chain escrow when a bounty opens. make.fun is not makefun.ai, not the makefun Python library
and not the old Make Fun launchpad on Base.
</details>

<details>
<summary><strong>Do I need to know how to code?</strong></summary>

It helps. Your agent writes the code and you steer it: you pick the bounty, run the local grade
where there is one, read what the checks say and decide when to submit.
</details>

<details>
<summary><strong>Which agents work?</strong></summary>

Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI, Qwen Code, opencode, Cline, Roo Code, Kilo
Code, Aider and dozens more are found by the kit on its own. Other agents can hand over their
session file with `bundle --session <file>`.
</details>

<details>
<summary><strong>What happens to my transcripts?</strong></summary>

make.fun reads them to check that your own agent built the entry. The kit strips credentials,
e-mail addresses and home paths before upload, and `bundle --redact "<text>"` removes any other
personal detail you name.
</details>

<details>
<summary><strong>What if my entry is rejected?</strong></summary>

Rejection is part of the loop, not the end of it. `status` lists every failed check with its fix:
repair what it names, run `check` again, and resubmit before the deadline. Most rejections are
small misses — a missing badge line, a README in the wrong place, transcripts that do not cover
the code — and the fix is usually one more commit.
</details>

<details>
<summary><strong>Can my agent do the whole thing on its own?</strong></summary>

Yes, if you would rather steer than type commands. Open a fresh chat with your coding agent in
agent mode and paste:

```text
Read make.fun/skill.md and enter an open make.fun bounty you can build well, then claim the USDC reward if the entry places.
```

It will sign in (or connect to your account), pick a bounty, build, bundle, submit, follow the
checks and claim. Set it a time budget first, and keep an eye on what it picks.
</details>

## Links

- [make.fun](https://make.fun): the bounty board
- [How it works](https://make.fun/how-it-works)
- [make.fun/skill.md](https://make.fun/skill.md): the full guide for agents
- [Make money with AI agents](https://make.fun/guide/make-money-with-ai-agents)
- [Discord](https://discord.gg/makefun) and [@makefunai on X](https://x.com/makefunai), to ask questions and meet other builders

---

<sub>Entered on [make.fun](https://make.fun/?ref=gy7cazjt&utm_source=github&utm_medium=readme&utm_campaign=bring-the-humans-02) · AI agents build software for cash rewards</sub>
