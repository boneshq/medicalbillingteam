---
title: "Denial Codes Explained: CARC Guides for Medical Billers"
meta_description: "How to read medical billing denial codes (group codes, CARC and RARC), plus plain-English guides to CO-16, CO-22, CO-29, CO-97, CO-197 and CO-204 with fixes."
slug: "/denial-codes/"
schema_type: ["CollectionPage", "FAQPage", "BreadcrumbList"]
faq:
  - q: "What is the difference between a CARC and a RARC?"
    a: "A CARC (claim adjustment reason code) says why the payer adjusted or denied a claim or line. A RARC (remittance advice remark code) adds detail, such as which field was missing. Payers combine a group code, a CARC and often a RARC on the remittance."
  - q: "What do the group codes CO, PR, OA and PI mean?"
    a: "CO is contractual obligation, meaning the provider generally cannot bill the patient for the amount. PR is patient responsibility, such as deductible or copay. OA is other adjustment, used when neither CO nor PR applies. PI is payer-initiated reductions."
  - q: "Where do I find denial codes on a remittance?"
    a: "On an electronic remittance advice (the X12 835), the group code, reason code and amount appear in the claim or service adjustment segment, and remark codes appear with the claim or line. Paper EOBs print the same codes next to the adjusted line, usually with a legend."
  - q: "Should I correct and resubmit or appeal a denied claim?"
    a: "It depends on the code. Missing information (CO-16) or a wrong payer (CO-22) is usually corrected and resubmitted. Medical necessity, authorization and benefit disputes are more often appealed with documentation. Each guide on this page says which path usually applies."
canonical: "https://medicalbillingteam.com/denial-codes/"
primary_keyword: "denial codes"
secondary_keywords: ["medical billing denial codes", "claim adjustment reason codes", "CARC codes list", "denial codes list"]
search_intent: "informational"
audience: "billers, coders, AR and denial staff, practice managers"
conversion_destination: "/checklist/"
pillar: "/denial-management/"
date_published: "2026-10-30"
date_modified: "2026-10-30"
author: "Medical Billing Team editors"  # brand byline; no invented persona
reviewer: ""  # TONY DECISION: real, authorized reviewer; render "Reviewed by" only when set
review_cadence: "quarterly + on code-list change"
carc_source: "https://x12.org/codes/claim-adjustment-reason-codes"
carc_checked: "2026-10-30"
---

# Denial codes explained: how to read them and fix the common ones

*By the Medical Billing Team editors · Published October 30, 2026 · Updated October 30, 2026 · [How we research and review](/about/#how-we-write-our-guides)*

**Short answer:** a denial code on a remittance is really three things: a group code (who is responsible for the amount), a claim adjustment reason code or CARC (why the payer adjusted or denied the line) and, often, a remittance advice remark code or RARC (the detail you need to fix it). This page explains how to read that combination, then links to our plain-English guides for the codes practices see most. Each guide covers the official definition, common causes and a fix-and-prevent checklist.

If denials pile up faster than your team can work them, our [denial management guide](/denial-management/) covers the weekly workflow, and [days in A/R](/reduce-ar-days/) explains how unworked denials show up in your numbers.

## How to read a denial code

A remittance line such as CO-16 with remark N382 has three parts:

- **Group code:** who the adjusted amount belongs to. **CO** (contractual obligation) means the provider generally cannot bill the patient for it. **PR** (patient responsibility) is the patient's share, such as a deductible, coinsurance or copay. **OA** (other adjustment) is used when neither CO nor PR applies. **PI** (payer-initiated reductions) covers reductions the payer applies in the absence of a contract clause.
- **CARC:** the claim adjustment reason code, a number from the X12 list, that states why the amount was adjusted. The six codes below are CARCs.
- **RARC:** the remittance advice remark code, usually a letter followed by numbers, that adds detail. Some CARCs, including CARC 16, require a remark code so you know exactly what was missing.

The official code lists are maintained by X12 and updated three times a year ([X12 claim adjustment reason codes](https://x12.org/codes/claim-adjustment-reason-codes), [remittance advice remark codes](https://x12.org/codes/remittance-advice-remark-codes)). Payers must use these standard codes on electronic remittances, but the way they apply them varies, so always check the payer's own policy before you appeal.

## Denial code guides

| Code | X12 definition (CARC) | Usual first step | Guide |
|---|---|---|---|
| CO-16 | "Claim/service lacks information or has submission/billing error(s)." | Read the RARC, fix the missing or invalid item, resubmit as a corrected claim. | [CO-16 guide](/denial-codes/co-16/) |
| CO-22 | "This care may be covered by another payer per coordination of benefits." | Confirm which plan is primary, bill the right payer first, then resubmit with the primary EOB. | [CO-22 guide](/denial-codes/co-22/) |
| CO-29 | "The time limit for filing has expired." | Check the payer's filing limit and your proof of timely submission; appeal with proof or write off. | [CO-29 guide](/denial-codes/co-29/) |
| CO-97 | "The benefit for this service is included in the payment/allowance for another service/procedure that has already been adjudicated." | Check bundling edits and modifiers; appeal only when the services are separately payable. | [CO-97 guide](/denial-codes/co-97/) |
| CO-197 | "Precertification/authorization/notification/pre-treatment absent." | Look for a retro authorization option; otherwise appeal with medical necessity or correct the auth number on the claim. | [CO-197 guide](/denial-codes/co-197/) |
| CO-204 | "This service/equipment/drug is not covered under the patient's current benefit plan." | Verify benefits, check for a plan exclusion, and bill the patient only where an advance notice allows it. | [CO-204 guide](/denial-codes/co-204/) |

Definitions are quoted from the X12 code list as checked on October 30, 2026. X12 revises descriptions, so confirm the current wording before you quote it in an appeal.

## Which denials to work first

Most teams get more money back by working denials in this order:

1. **Deadline first.** Anything close to the payer's timely filing or appeal limit goes to the top, whatever the dollar amount. A denial that ages past the limit becomes a CO-29 and is usually unrecoverable.
2. **High dollar, likely to pay.** Authorization (CO-197) and coordination of benefits (CO-22) denials often pay once corrected, so they rank above low-dollar bundling questions.
3. **Quick fixes in batches.** CO-16 denials with the same remark code usually share one root cause, such as a missing NPI or a stale insurance ID. Fix the cause, then resubmit the batch.
4. **Prevent the repeat.** Track the top three reason codes each week and send one note to the people who can stop them: the front desk for eligibility, providers for documentation, coders for modifiers.

Our [denial management guide](/denial-management/) turns this into a weekly schedule, and the [A/R specialist guide](/ar-specialist/) explains who typically owns each step. Front-end causes are covered in [eligibility verification and prior authorization](/eligibility-verification-prior-authorization/) and the [prior authorization specialist guide](/prior-authorization-specialist/).

## Codes we plan to cover next

These reason codes come up often in practice denial reports. They are listed here so you know what is coming; see the X12 list for the official wording until each guide is published:

- **CO-4:** procedure code inconsistent with the modifier used.
- **CO-11:** diagnosis inconsistent with the procedure.
- **CO-18:** exact duplicate claim or service.
- **CO-45:** charge exceeds the fee schedule or contracted amount (usually a write-off, not a denial to work).
- **CO-50:** service not deemed medically necessary by the payer.
- **CO-109:** claim not covered by this payer; send it to the correct payer.
- **CO-151:** information submitted does not support this number or frequency of services.
- **PR-1, PR-2, PR-3:** deductible, coinsurance and copayment amounts, which are patient balances rather than denials.
- **CO-B7:** provider not certified or eligible to be paid for the service on that date, often a credentialing problem. See [credentialing services](/credentialing-services/).

**Approved vendor:** [Alliance Global Solutions](/approved-vendors/alliance-global-solutions/), which operates this site, provides dedicated remote denial and A/R staff who work inside your billing system and signs a business associate agreement with each client before any PHI access. See [approved vendors](/approved-vendors/) and [how we vet vendors](/how-we-vet-vendors/).

## Related guides

- [Denial management in medical billing: a practical guide](/denial-management/)
- [Days in A/R: how to calculate and reduce AR days](/reduce-ar-days/)
- [What does an AR specialist do?](/ar-specialist/)
- [Prior authorization specialists and PA outsourcing](/prior-authorization-specialist/)
- [Eligibility verification and prior authorization](/eligibility-verification-prior-authorization/)
- [Medical Billing Health Checklist](/checklist/)
