---
title: "Insurance Verification Services & Prior Authorization"
meta_description: "Insurance verification services and prior authorization: eligibility workflows, what CMS-0057-F changed, and how to staff them. Free staffing assessment."
slug: "/eligibility-verification-prior-authorization/"
schema_type: ["Article", "FAQPage", "BreadcrumbList"]
faq:
  - q: "What is insurance eligibility verification?"
    a: "It is confirming, before a visit, that a patient's coverage is active and finding out benefits that affect payment: copay, deductible, coinsurance, plan type, network status, coordination of benefits, and whether a referral or prior authorization is required."
  - q: "What is a VOB?"
    a: "VOB stands for verification of benefits. The term is common in behavioral health and treatment centers, where staff verify detailed benefits for specific levels of care before admission."
  - q: "How long do payers have to respond to prior authorization requests?"
    a: "Under the CMS Interoperability and Prior Authorization final rule, impacted payers such as Medicare Advantage and Medicaid managed care plans (excluding FFE qualified health plans for this provision) must send decisions within 72 hours for expedited requests and seven calendar days for standard requests, beginning in 2026. Commercial plans outside the rule follow their own contracts and state laws."
  - q: "How much time do practices spend on prior authorization?"
    a: "In an AMA survey of 1,000 physicians, practices reported an average of 39 prior authorization requests per physician per week, taking about 13 hours of physician and staff time."
  - q: "Can eligibility and prior authorization be done by remote staff?"
    a: "Yes. Both are largely portal- and phone-based, so remote staff can do them well with access to your scheduling system, payer portals and clear rules, plus HIPAA safeguards such as a BAA, MFA and role-based access."
canonical: "https://medicalbillingteam.com/eligibility-verification-prior-authorization/"
secondary_keywords: ["eligibility verification and prior authorization"]
primary_keyword: "insurance verification services"  # swapped 2026-10-18 from "eligibility verification and prior authorization" (Semrush)
search_intent: "informational"
audience: "front-office and billing managers"
conversion_destination: "/contact/"
date_published: "2026-10-18"
date_modified: "2026-10-18"
author: "Medical Billing Team editors"  # brand byline; no invented persona
reviewer: ""  # TONY DECISION: real, authorized reviewer with billing experience; render "Reviewed by" only when set
review_cadence: "quarterly + on rule change"
tech_section:  # reusable <TechSection> component; edit here
  body: "Electronic eligibility checks return coverage details in seconds, and CMS-0057-F requires impacted payers to support prior authorization APIs by January 1, 2027, with decisions within 72 hours for expedited and seven calendar days for standard requests ([CMS](https://www.cms.gov/newsroom/fact-sheets/cms-interoperability-and-prior-authorization-final-rule-cms-0057-f)). Carve-outs, out-of-network details and authorization rules still often need a call. Alliance Global Solutions helps clients set up AI assistant workflows alongside their dedicated staff."
  link: "/medical-billing-technology/"
---

# Eligibility verification and prior authorization: workflows and staffing

*By the Medical Billing Team editors · Published October 18, 2026 · Updated October 18, 2026 · [How we research and review](/about/#how-we-write-our-guides)*

**Short answer:** Whether you do it in-house or use insurance verification services, verify eligibility and benefits before every visit, not just the first. Confirm active coverage, plan type, cost sharing, coordination of benefits, and whether the service needs a referral or prior authorization. Then track each authorization's expiration and visit limits. CMS-0057-F now sets decision timeframes for many payers, but practices still need staff to submit requests and follow up.

Most denials are decided before the patient arrives. If coverage wasn't active, benefits weren't understood, or an authorization was missing, no amount of A/R follow-up will fully fix it. This guide covers eligibility verification and prior authorization, what changed recently in federal rules, the workflows that work, and how practices staff them. It's part of our [revenue cycle management staffing](/revenue-cycle-management-staffing/) series.

## Why the front end matters

In a 2025 vendor survey of billing professionals, the top denial reasons were coordination of benefits issues (45% of respondents), non-coverage (39%) and prior authorization or referral issues (31%) ([Tebra](https://www.tebra.com/theintake/getting-paid/medical-billing-pain-points-insights-solutions)). Federal transparency data show HealthCare.gov insurers attributed 9% of in-network claim denials in 2023 to lack of prior authorization or referral ([KFF](https://www.kff.org/private-insurance/claims-denials-and-appeals-in-aca-marketplace-plans-in-2023/)). All of these are front-end problems.

## Eligibility verification, step by step

### When to verify

- At scheduling, for new patients and new insurance.
- 24 to 72 hours before every visit, for everyone, since coverage changes.
- At check-in, by confirming card, ID and any changes.

### What to verify

- Active coverage on the date of service
- Plan type and network status for the rendering provider and location
- Copay, deductible (met and remaining), coinsurance, out-of-pocket maximum
- Coordination of benefits: is this plan primary?
- Service-specific limits (visit caps for therapy, for example)
- Referral and prior authorization requirements for the planned service

### How

Use real-time 270/271 eligibility transactions through your practice management system or clearinghouse where available, payer portals for detail, and phone calls when portals don't show what you need. Document what you found, where, and the reference number.

### What to do with the result

- Update demographics and insurance in the system.
- Flag inactive coverage and contact the patient before the visit.
- Give the front desk the patient's estimated responsibility so it can be collected at check-in.
- Trigger the authorization workflow if required.

## Verification of benefits (VOB) in behavioral health

Treatment centers and behavioral health programs often run a deeper VOB: benefits by level of care (detox, residential, partial hospitalization, intensive outpatient, outpatient), authorization and concurrent review requirements, out-of-network benefits and day limits. VOB staff usually work with admissions teams under time pressure. See our [behavioral health billing guide](/behavioral-health-billing/).

## Prior authorization, step by step

### The workload

The AMA's survey of 1,000 physicians found practices complete an average of 39 prior authorization requests per physician per week, spending about 13 hours on them, and that 40% of physicians have staff who work exclusively on prior authorizations ([AMA](https://www.ama-assn.org/practice-management/prior-authorization/fixing-prior-auth-nearly-40-prior-authorizations-week-way)).

### The workflow

1. **Identify** services needing authorization by payer and code, using payer lists. Keep a maintained matrix.
2. **Gather documentation:** orders, notes, prior treatments tried, test results.
3. **Submit** through the payer portal, electronic transaction or fax, as the payer requires.
4. **Track** pending requests daily, with a due date for each.
5. **Record** the authorization number, approved units or visits, and the date range in the practice management system so it flows to the claim.
6. **Monitor** expirations and visit counts, and request extensions before they run out.
7. **Handle denials:** request a peer-to-peer review if appropriate, or appeal with additional documentation.

## What changed: the CMS prior authorization rule

The CMS Interoperability and Prior Authorization final rule (CMS-0057-F) applies to "impacted payers": Medicare Advantage organizations, state Medicaid and CHIP fee-for-service programs, Medicaid managed care plans, CHIP managed care entities and qualified health plan issuers on the federally facilitated exchanges ([CMS fact sheet](https://www.cms.gov/newsroom/fact-sheets/cms-interoperability-and-prior-authorization-final-rule-cms-0057-f)). Key points from CMS:

- **Decision timeframes:** impacted payers, excluding FFE qualified health plans, must send prior authorization decisions within **72 hours** for expedited requests and **seven calendar days** for standard requests.
- **Specific denial reasons:** beginning in 2026, impacted payers must give a specific reason for denied prior authorization requests.
- **Public metrics:** payers must post certain prior authorization metrics annually.
- **Prior Authorization API:** payers must implement an API to support electronic requests and responses, generally by January 1, 2027.
- **Drugs are excluded** from these provisions.

For staff, this means more predictable turnaround from these payers and clearer denial reasons to work from, but the volume of authorizations doesn't go away. Commercial plans outside the rule follow their own contracts and applicable state laws.

## Measuring front-end performance

- Percentage of visits verified before the date of service
- Eligibility-related denials (count and dollars)
- Authorization-related denials
- Average days from authorization request to decision, by payer
- Visits performed without a valid authorization (should be zero)

## Staffing eligibility and prior authorization

Both jobs are detail-heavy, deadline-driven and largely done in portals and on the phone, which makes them a good fit for dedicated staff, local or remote. What matters:

- **Protected time.** Authorization work done "between patients" by front-desk staff tends to slip.
- **Payer knowledge.** A maintained authorization matrix and staff who know each payer's portal.
- **Schedule alignment.** Staff working ahead of your schedule (for example, verifying tomorrow's patients today) and overlapping payer phone hours.
- **Clear handoffs** with the front desk and clinicians for missing documentation.
- **Security.** Access only to scheduling, eligibility and authorization screens needed (minimum necessary), unique logins with MFA, and a signed BAA before access. See our [HIPAA guide](/hipaa-outsourced-medical-billing/).

This site is operated by [Alliance Global Solutions](https://www.allianceglobalsolutions.com/), whose remote staff include eligibility, prior authorization and [administrative support](https://www.allianceglobalsolutions.com/virtual-assistant-skills/administrative/) roles. If front-end work is backing up, request a [free staffing assessment](/contact/).

## Common front-end mistakes to avoid

- **Checking eligibility only for new patients.** Coverage changes at any time: job changes, plan renewals, Medicaid redeterminations. Re-verify before every visit, or at least whenever the schedule is built.
- **Stopping at "active coverage."** A plan can be active and still deny the service for lack of authorization, a visit limit, a carve-out or out-of-network status. Check benefits for the specific service.
- **Not recording the details.** Note who you spoke with, the reference number, the date and what was confirmed. If the payer later denies the claim, that record supports the appeal.
- **Losing track of expirations.** Authorizations expire and visit counts run out. Put both on a calendar with an owner and a lead time for renewal requests.
- **Treating the front desk as the only line of defense.** Front desk staff juggle phones, check-in and payments. A dedicated verification person or team, working a day or two ahead of the schedule, catches problems before the patient arrives.
- **Ignoring secondary coverage.** Coordination-of-benefits problems were the most commonly reported cause of rising denials in Tebra's 2025 survey of billers ([Tebra](https://www.tebra.com/theintake/getting-paid/medical-billing-pain-points-insights-solutions)). Ask every patient about other coverage and confirm which plan is primary.

**Approved vendor:** [Alliance Global Solutions](/approved-vendors/alliance-global-solutions/), which operates this site, provides dedicated remote staff for this work and signs a business associate agreement with each client before any PHI access. See [approved vendors](/approved-vendors/) and [how we vet vendors](/how-we-vet-vendors/).

## Technology

Electronic eligibility checks return coverage details in seconds, and CMS-0057-F requires impacted payers to support prior authorization APIs by January 1, 2027, with decisions within 72 hours for expedited and seven calendar days for standard requests ([CMS](https://www.cms.gov/newsroom/fact-sheets/cms-interoperability-and-prior-authorization-final-rule-cms-0057-f)). Carve-outs, out-of-network details and authorization rules still often need a call. Alliance Global Solutions helps clients set up AI assistant workflows alongside their dedicated staff. [Latest updates in medical billing technology →](/medical-billing-technology/)

## Related guides

- [Denial management basics](/denial-management/)
- [VOB and authorizations in behavioral health](/behavioral-health-billing/)
- [Revenue cycle management staffing (main guide)](/revenue-cycle-management-staffing/)
- [Prior authorization specialist role](/prior-authorization-specialist/)

## FAQ

### What is insurance eligibility verification?

It is confirming, before a visit, that a patient's coverage is active and finding out benefits that affect payment: copay, deductible, coinsurance, plan type, network status, coordination of benefits, and whether a referral or prior authorization is required.

### What is a VOB?

VOB stands for verification of benefits. The term is common in behavioral health and treatment centers, where staff verify detailed benefits for specific levels of care before admission.

### How long do payers have to respond to prior authorization requests?

Under the CMS Interoperability and Prior Authorization final rule, impacted payers such as Medicare Advantage and Medicaid managed care plans (excluding FFE qualified health plans for this provision) must send decisions within 72 hours for expedited requests and seven calendar days for standard requests, beginning in 2026. Commercial plans outside the rule follow their own contracts and state laws.

### How much time do practices spend on prior authorization?

In an AMA survey of 1,000 physicians, practices reported an average of 39 prior authorization requests per physician per week, taking about 13 hours of physician and staff time.

### Can eligibility and prior authorization be done by remote staff?

Yes. Both are largely portal- and phone-based, so remote staff can do them well with access to your scheduling system, payer portals and clear rules, plus HIPAA safeguards such as a BAA, MFA and role-based access.

---
*Affiliation disclosure: Medical Billing Team is operated by Alliance Global Solutions, a provider of remote medical billing and revenue cycle staff and currently the only vendor on our [approved vendor list](/approved-vendors/). Requests submitted here may be referred to Alliance Global Solutions, and we benefit if you hire it. We may contact you about our services if you request it. [How we vet vendors](/how-we-vet-vendors/).*
