# AI Job Hunt Agent — Product Requirements Document

**Status:** Draft v0.1
**Owner:** Dhruv
**Last updated:** July 2026
**Working title:** rename freely — this doc uses "the system" throughout

---

## 1. Overview

A personal multi-agent system that automates the research-heavy, repetitive parts of job hunting — finding companies that fit a candidate's actual profile, understanding those companies well enough to write something real about them, tailoring application materials per role, finding the right contact, and drafting outreach — while keeping a human approval gate before anything external happens (an email sent, an application submitted).

**Problem it solves:** targeted job hunting (as opposed to mass-applying) requires hours of research per company that most candidates don't have time for, so they either mass-apply with generic materials (low conversion) or narrowly apply to a handful of companies they already know (missed opportunities). The system exists to make *targeted* applications scale.

**V1 user:** Dhruv, single user, applying for AI/ML engineering roles. Not built as a multi-tenant product in V1 — architecture should not actively prevent that later, but nothing in V1 should be built *for* it.

---

## 2. Goals (V1 / MVP)

- Given a structured profile (resume, GitHub, LinkedIn, project history, target role, location/work-mode preferences), produce a ranked shortlist of companies that are a genuine fit — not just keyword-matched, but matched against actual skill level and trajectory.
- For each shortlisted company, produce a short, factually grounded research brief (what they build, who they sell to, how they operate) that a human can actually use in a cover letter — not generic filler.
- For companies with an open, matching role: produce a tailored resume variant and a draft cover letter per JD.
- Every output that leaves the system (email, application) passes through a manual approval step. No exceptions in V1.

## 3. Non-goals (explicitly out of scope for V1)

- Fully autonomous sending — no email leaves the system without a click from Dhruv.
- Cold outreach to companies not currently hiring (this is V2 — see Milestones).
- Scraping LinkedIn profiles or job listings directly (see §8, Constraints).
- Multi-user support, billing, or productization as a SaaS.
- Interview preparation content generation (mentioned in the original idea — deferred; V1 is about getting the interview, not prepping for it).

## 4. Target user

One user: Dhruv. Second-order design goal: keep the profile/config layer clean enough that "swap in a different resume and goals" is a config change, not a rewrite — useful even for a single user whose target role or resume will change over the next year.

## 5. End-to-end user journey (V1)

1. Dhruv fills out a profile: resume (parsed), GitHub, LinkedIn, project write-ups, target role(s), work-mode preference, target locations, deal-breakers (e.g. minimum comp, company size).
2. System runs company discovery → returns a candidate list with a one-line reason each was surfaced.
3. Dhruv prunes the list (removes companies he's not interested in) — cheap human filter before expensive research runs.
4. System runs company research on the surviving list → produces a research brief per company.
5. System checks each company for open, matching roles.
6. For matches: system produces a fit-ranked list, a tailored resume per role, and a draft cover letter.
7. Dhruv reviews each package in a simple dashboard, edits if needed, approves or rejects.
8. Approved packages are marked ready-to-send; V1 send is manual (Dhruv copies materials into the application himself, or the system opens a pre-filled Gmail draft — see Tech.md).
9. System logs what was sent where, so nothing gets duplicated or forgotten.

## 6. Functional requirements by module

### 6.1 Profile & goals intake
- Accepts resume (PDF/text), GitHub username, LinkedIn export or URL, free-text project descriptions.
- Accepts structured goals: target role(s), seniority level, work mode (remote/hybrid/onsite), target locations, minimum comp (optional), company-size preference (optional).
- Produces a normalized profile object other agents consume (see Tech.md §3).
- Must be editable — this isn't a one-time form, it's a living config.

### 6.2 Company discovery agent
- Input: normalized profile.
- Output: list of companies with a short "why this company" justification tied to the actual profile (not generic).
- Must be able to explain its own reasoning per company — this is what makes the list prunable by a human instead of a black box.

### 6.3 Company research agent
- Input: a company name/domain.
- Output: a structured brief — what they build, who their customers are, team/culture signals if publicly available, recent news if relevant.
- **Hard requirement:** every factual claim must be traceable to a real source fetched at research time. No claim generated from model memory alone (see Constraints §8.3 — this is the #1 way this system produces embarrassing output if skipped).

### 6.4 Job-status check & branch
- For each researched company, check for currently open roles matching the target profile.
- Branch A (open role found): proceed to JD matching + resume tailoring.
- Branch B (no open role): company is parked in a "watch list" for V2 cold-outreach — not acted on in V1.

### 6.5 JD matching & resume tailoring (Branch A)
- Rank open roles by fit against the profile.
- Produce a tailored resume variant per role: reordered/reframed to match the JD's language and priorities.
- **Hard requirement:** tailoring means reframing and reordering *real* experience. It must never introduce a metric, tool, or claim that isn't already true of the candidate. This is a correctness constraint, not a style preference.

### 6.6 Cover letter & outreach drafting
- Produces a cover letter per tailored resume, grounded in the company research brief (should reference something specific and true about the company, not boilerplate).
- Drafts an outreach email if a contact is available.

### 6.7 Contact discovery
- Finds a legitimate point of contact per company: named referral, public team-page contact, or generic careers address.
- V1 does **not** use scraped personal-email databases (see Constraints §8.2). If no legitimate contact is found, the package still includes the resume + cover letter for direct portal application.

### 6.8 Human review & approval
- Every package (research brief, resume, cover letter, contact, draft email) is reviewable in one place before anything is sent.
- Approval is per-package, not batch — no "approve all."

### 6.9 Application tracking
*(not in the original idea, but needed — without it the system will re-research and re-draft for companies already applied to.)*
- Every approved/sent package is logged: company, role, date, materials used, status (applied / no response / responded / rejected).
- Discovery agent should check this log and deprioritize or flag already-contacted companies.

## 7. Success metrics

- Quality over volume: target is well-researched applications per week, not raw send count.
- Zero approved outputs later found to contain a fabricated or hallucinated claim.
- Time from "company discovered" to "application-ready package" (should drop sharply vs. manual research).
- The metric that actually matters long-term: interview call-back rate over time, tracked via the application log.

## 8. Constraints, risks & compliance notes

These carry over from the architecture discussion and are binding, not suggestions:

**8.1 Data sourcing.** No LinkedIn scraping — it violates their ToS and is legally contestable (see *hiQ v. LinkedIn*). Discovery and research must rely on public job boards/APIs, career pages, and general web search.

**8.2 Contact data.** No bulk scraped personal-contact databases for cold outreach in V1. Use generic company addresses and publicly self-disclosed contacts only. This isn't just risk-aversion — India's DPDP Act and GDPR (for EU-headquartered targets) both bear on unsolicited use of personal data.

**8.3 Grounding.** Any factual claim about a company must come from a fetched source, not model memory, given the model's knowledge cutoff and hallucination risk on specifics like client lists or team size.

**8.4 Resume honesty.** Tailoring reorders and reframes; it never fabricates. This is the same standard applied to Dhruv's own resume work previously — no exceptions for an agent doing it on his behalf.

**8.5 Human gate.** No fully autonomous sending in any version until there's a long track record of reviewed output being consistently accurate — and even then, sending should stay opt-in per package.

## 9. Open questions

- What counts as "currently hiring" — do we trust a company's careers page alone, or cross-reference with a job board listing?
- How aggressively should the discovery agent expand beyond obvious/well-known companies (this affects both quality and how much research budget gets spent on long-shots)?
- Where does the application log live — is it just for this system, or should it eventually sync with the Notion productivity setup already in use?

## 10. Milestones

| Phase | Scope |
|---|---|
| V1 (MVP) | Profile intake, discovery, research, Branch A only (open roles), resume tailoring, cover letter draft, review dashboard, manual send, application log |
| V2 | Branch B (cold outreach), legitimate contact discovery, outreach email drafting, watch-list re-checks for newly opened roles |
| V3 | Semi-automated sending (pre-filled Gmail drafts, one click after approval), response tracking, discovery agent learns from log (deprioritize dead ends) |
| V4 (vision, not committed) | Broader reuse beyond one user, if ever desired |