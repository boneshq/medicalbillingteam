---
title: "Denial Management in Medical Billing: A Practical Guide"
meta_description: "A practical denial management workflow for medical billing: root causes, a weekly routine, appeals, KPIs and who owns the queue. Free billing checklist."
slug: "/denial-management/"
schema_type: ["Article", "FAQPage", "BreadcrumbList"]
faq:
  - q: "What is the difference between a claim rejection and a denial?"
    a: "A rejection means the claim was not accepted for processing, usually because of formatting or data errors caught by the clearinghouse or payer front end. A denial means the payer processed the claim and decided not to pay all or part of it. Rejections are corrected and resubmitted; denials are corrected, resubmitted or appealed."
  - q: "What are the most common causes of claim denials?"
    a: "Common categories include eligibility and coordination of benefits problems, non-covered services, missing prior authorization or referral, timely filing, coding errors and inaccurate patient demographics. In one 2025 vendor survey, billers most often cited coordination of benefits, non-coverage and prior authorization issues."
  - q: "How often should denials be worked?"
    a: "Daily or at least weekly, prioritized by dollar value and appeal deadline. Denials left for weeks risk missing appeal windows."
  - q: "What is a good denial rate?"
    a: "Benchmarks vary by specialty, payer mix and how the rate is calculated. Track your own denial rate by payer and reason each month and focus on the reasons you can prevent."
  - q: "Should denial work be in-house or outsourced?"
    a: "Either can work. What matters is that a specific person owns the queue, has payer knowledge and time to do it, and feeds root causes back to the front desk and coders."
canonical: "https://medicalbillingteam.com/denial-management/"
secondary_keywords: ["denial management medical billing"]
primary_keyword: "denial management"  # swapped 2026-10-18 from "denial management medical billing" (Semrush)
search_intent: "informational"
audience: "billing managers"
conversion_destination: "/checklist/"
date_published: "2026-10-18"
date_modified: "2026-10-18"
author: "Medical Billing Team editors"  # brand byline; no invented persona
reviewer: ""  # TONY DECISION: real, authorized reviewer with billing experience; render "Reviewed by" only when set
review_cadence: "quarterly + on rule change"
tech_section:  # reusable <TechSection> component; edit here
  body: "Denial management is shifting upstream into denial prevention: claim scrubbing, denial-prediction models and payer-policy checks before care is delivered ([Fierce Healthcare](https://www.fiercehealthcare.com/health-tech/thoreau-backed-ensemble-penelope-health-partner-tackle-payer-denials-upstream)). Remits use standard X12 group and reason codes, so denials can be sorted automatically into work queues ([X12](https://x12.org/codes/claim-adjustment-reason-codes)). People still write appeals and fix root causes. Alliance Global Solutions helps clients set up AI assistant workflows alongside their dedicated staff."
  link: "/medical-billing-technology/"
---

# Denial management basics: a practical guide for practices and billing teams

*By the Medical Billing Team editors · Published October 18, 2026 · Updated October 18, 2026 · [How we research and review](/about/#how-we-write-our-guides)*

**Short answer:** Denial management means tracking every denied claim, then correcting and resubmitting it or appealing it before the deadline, and feeding the root cause back to the front desk, coders and providers so it doesn't happen again. It works best with one owner, a single queue sorted by payer and reason, and a fixed weekly routine.

Every practice gets denials. The difference between practices that lose revenue to them and practices that don't is usually not software. It's whether someone owns the denial queue, works it on a schedule and fixes the causes upstream. This guide covers the basics and where staffing fits in. It is part of our [revenue cycle management staffing](/revenue-cycle-management-staffing/) series.

## Why denials deserve a dedicated owner

Public data show how common denials are. KFF's analysis of federal transparency data found HealthCare.gov insurers denied 20% of in-network claims in 2023 ([KFF](https://www.kff.org/private-insurance/claims-denials-and-appeals-in-aca-marketplace-plans-in-2023/)). That covers one market segment, but the pattern is familiar to anyone who works claims. In a 2025 vendor survey of billing professionals, 40% reported that denials had increased over the previous year ([Tebra](https://www.tebra.com/theintake/getting-paid/medical-billing-pain-points-insights-solutions)).

When nobody owns denials, they age quietly in a work queue until the appeal window closes.

## Rejections vs denials

- **Rejection:** the claim never entered the payer's adjudication system, usually because of a data or formatting error (wrong member ID format, missing NPI, invalid code). Fix and resubmit quickly. Rejections don't usually carry appeal rights because no decision was made.
- **Denial:** the payer processed the claim and refused payment in whole or part. The remittance carries claim adjustment reason codes (CARCs) and often remittance advice remark codes (RARCs) explaining why. These are standard code sets used by all payers, as CMS describes in its Medicare Claims Processing Manual ([CMS, Ch. 1](https://www.cms.gov/regulations-and-guidance/guidance/manuals/downloads/clm104c01.pdf)).

## Common root causes

The same vendor survey asked billers about top denial reasons ([Tebra](https://www.tebra.com/theintake/getting-paid/medical-billing-pain-points-insights-solutions)):

- coordination of benefits issues (45% of respondents);
- non-coverage (39%);
- prior authorization and referral issues (31%);
- timely filing errors (26%);
- inaccurate patient demographic information (25%).

In KFF's federal data, insurers cited administrative reasons for 21% of in-network denials and lack of prior authorization or referral for 9%, while the largest category was "Other" at 34% ([KFF](https://www.kff.org/private-insurance/claims-denials-and-appeals-in-aca-marketplace-plans-in-2023/)).

Most of these trace back to the **front end**: eligibility checks, demographics capture and authorizations. That's why denial management and [eligibility and prior authorization](/eligibility-verification-prior-authorization/) work belong together.

## A simple denial workflow

### 1. Capture every denial

Make sure denials from ERAs (835s), paper EOBs and payer portals all land in one queue. Payment posters are often the first to see a denial; they should flag it, not just post a zero.

### 2. Categorize

Tag each denial by payer, reason code group (eligibility, authorization, coding, timely filing, medical necessity, duplicate, bundling, other) and whether it is **preventable**.

### 3. Prioritize

Sort by appeal or corrected-claim deadline first, then dollar value. A small denial with a deadline next week beats a large one with three months left.

### 4. Act

- **Correct and resubmit** for fixable data errors (demographics, codes, modifiers).
- **Appeal** when the claim was correct and the payer was wrong. Use the payer's form, cite the policy, attach documentation, and track the appeal date.
- **Bill the right party** for coordination of benefits issues.
- **Write off** only under your written write-off policy, with approval.

### 5. Track and close the loop

Log the outcome. Each month, review the top preventable reasons by payer and send fixes upstream: a front-desk script change, an authorization rule, a coding education note.

## Appeals: the basics

- Read the denial reason and the payer's policy before writing anything.
- Know the deadline. Payer appeal windows differ, and Medicare has its own multi-level appeals process.
- Include what the payer needs: claim details, the specific reason you disagree, policy citations and supporting documentation.
- Follow up. An appeal that's never tracked is an appeal that's lost.

Appeals can succeed. KFF reports that among Medicare Advantage prior authorization denials in 2023 that were appealed, 81.7% were fully or partially overturned, yet only 11.7% of denials were appealed (cited in [AMA](https://www.ama-assn.org/practice-management/prior-authorization/fixing-prior-auth-nearly-40-prior-authorizations-week-way)). That's prior authorization data, not claims, but it shows the value of persistence.

## Denial KPIs to track

- **Denial rate:** denied claims (or dollars) ÷ claims (or dollars) submitted, by payer and reason.
- **Preventable denial share:** denials in categories the practice controls.
- **Days to work a denial:** from receipt to first action.
- **Overturn rate:** successful appeals ÷ appeals filed.
- **Denial write-offs:** dollars written off due to denials, per month.

We don't publish a universal "good" denial rate, because public benchmarks vary by specialty and methodology. Trend your own numbers. Our [RCM KPI definitions](/revenue-cycle-management-staffing/) explain how to calculate each one consistently.

## Who should do denial work?

Denial work needs someone with payer knowledge, coding familiarity, patience on the phone and protected time. Options:

- **Your existing biller**, if they actually have the hours. Often they don't.
- **A dedicated denial management specialist**, in-house or remote, who works the queue daily.
- **An outsourced billing company** that includes appeals in its scope (confirm this; some don't).

A remote denial specialist works in your billing system and payer portals under your rules and write-off policy. If you're considering that route, read our [guide to hiring remote medical billers](/hire-remote-medical-billers/) and make sure HIPAA safeguards are in place first ([HIPAA guide](/hipaa-outsourced-medical-billing/)).

## Preventing denials upstream

- Verify eligibility and benefits before every visit, not just new patients.
- Confirm authorization requirements by payer and service, and track expirations and visit limits.
- Capture demographics and insurance cards accurately; re-verify at every visit.
- Scrub claims before submission and fix rejections daily.
- Give coders feedback on recurring coding denials.
- Track timely filing deadlines per payer.

This site is operated by [Alliance Global Solutions](https://www.allianceglobalsolutions.com/), a provider of remote billing staff. If your denial queue is growing faster than your team can work it, you can [contact the company directly](https://www.allianceglobalsolutions.com/contact/) or request a [free staffing assessment](/contact/) here.

## A weekly denial routine for small teams

If you only have a few hours a week for denials, a fixed routine keeps them from piling up:

1. **Monday:** pull new denials from ERAs and the clearinghouse into one list. Tag each by payer, reason code and dollar amount.
2. **Tuesday-Wednesday:** correct and resubmit the quick fixes (demographics, coding errors, missing modifiers) and call payers on the unclear ones.
3. **Thursday:** draft appeals for high-dollar or recurring denials, with supporting documentation and the payer's appeal deadline noted.
4. **Friday:** review the week. What were the top three reasons? Which could the front desk, providers or coders prevent? Send one short note to the people who can fix the cause.

Keep the list in a shared tracker so nothing depends on one person's memory.

**Approved vendor:** [Alliance Global Solutions](/approved-vendors/alliance-global-solutions/), which operates this site, provides dedicated remote staff for this work and signs a business associate agreement with each client before any PHI access. See [approved vendors](/approved-vendors/) and [how we vet vendors](/how-we-vet-vendors/).

## Denial code guides

Most denials trace back to a handful of CARC codes. Each guide covers what the code means, common causes and a fix-and-prevent checklist. Start with [how to read denial codes](/denial-codes/) if CARC and RARC are new to you:

- [CO-16: claim lacks information or has billing errors](/denial-codes/co-16/)
- [CO-22: coordination of benefits denials](/denial-codes/co-22/)
- [CO-29: timely filing limit expired](/denial-codes/co-29/)
- [CO-97: bundled or included services](/denial-codes/co-97/)
- [CO-197: missing precertification or authorization](/denial-codes/co-197/)
- [CO-204: service not covered under the patient's plan](/denial-codes/co-204/)

## Technology

Denial management is shifting upstream into denial prevention: claim scrubbing, denial-prediction models and payer-policy checks before care is delivered ([Fierce Healthcare](https://www.fiercehealthcare.com/health-tech/thoreau-backed-ensemble-penelope-health-partner-tackle-payer-denials-upstream)). Remits use standard X12 group and reason codes, so denials can be sorted automatically into work queues ([X12](https://x12.org/codes/claim-adjustment-reason-codes)). People still write appeals and fix root causes. Alliance Global Solutions helps clients set up AI assistant workflows alongside their dedicated staff. [Latest updates in medical billing technology →](/medical-billing-technology/)

## Related guides

- [How to reduce A/R days](/reduce-ar-days/)
- [Medical billing outsourcing statistics (denial rates, rework cost)](/medical-billing-outsourcing-statistics/)
- [Eligibility verification and prior authorization](/eligibility-verification-prior-authorization/)
- [Revenue cycle management staffing (main guide)](/revenue-cycle-management-staffing/)
- [What an AR specialist does](/ar-specialist/)
- [how denials fit into the revenue cycle](/what-is-revenue-cycle-management/)
- [outsourced vs. in-house billing models](/medical-billing-outsourcing/)

## FAQ

### What is the difference between a claim rejection and a denial?

A rejection means the claim was not accepted for processing, usually because of formatting or data errors caught by the clearinghouse or payer front end. A denial means the payer processed the claim and decided not to pay all or part of it. Rejections are corrected and resubmitted; denials are corrected, resubmitted or appealed.

### What are the most common causes of claim denials?

Common categories include eligibility and coordination of benefits problems, non-covered services, missing prior authorization or referral, timely filing, coding errors and inaccurate patient demographics. In one 2025 vendor survey, billers most often cited coordination of benefits, non-coverage and prior authorization issues.

### How often should denials be worked?

Daily or at least weekly, prioritized by dollar value and appeal deadline. Denials left for weeks risk missing appeal windows.

### What is a good denial rate?

Benchmarks vary by specialty, payer mix and how the rate is calculated. Track your own denial rate by payer and reason each month and focus on the reasons you can prevent.

### Should denial work be in-house or outsourced?

Either can work. What matters is that a specific person owns the queue, has payer knowledge and time to do it, and feeds root causes back to the front desk and coders.

---
*Affiliation disclosure: Medical Billing Team is operated by Alliance Global Solutions, a provider of remote medical billing and revenue cycle staff and currently the only vendor on our [approved vendor list](/approved-vendors/). Requests submitted here may be referred to Alliance Global Solutions, and we benefit if you hire it. We may contact you about our services if you request it. [How we vet vendors](/how-we-vet-vendors/).*
