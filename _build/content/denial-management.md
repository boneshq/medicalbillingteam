---
title: "Denial Management Basics for Practices and Billers"
meta_description: "Denial management explained: denial vs rejection, root causes, a weekly workflow, appeals, KPIs and who should own the denial queue, with sourced data."
slug: "/denial-management/"
schema_type: ["Article", "FAQPage"]
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
---

# Denial management basics: a practical guide for practices and billing teams

*Last reviewed: October 18, 2026.*

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

## FAQ

**What is the difference between a rejection and a denial?**
A rejection was never accepted for processing; a denial was processed and not paid. Fix and resubmit rejections; correct, resubmit or appeal denials.

**What are the most common causes of denials?**
Eligibility and coordination of benefits, non-covered services, missing authorizations, timely filing, coding errors and demographics.

**How often should denials be worked?**
Daily or weekly, by deadline and dollar value.

**What is a good denial rate?**
It varies by specialty and method. Trend your own rate by payer and reason.

**Should denial work be in-house or outsourced?**
Either works if one person owns the queue and feeds root causes back upstream.

---
*Disclosure: This site is operated by Alliance Global Solutions, a provider of remote medical billing and revenue cycle staff. We may contact you about our services if you request it.*
