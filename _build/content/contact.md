---
title: "Free Medical Billing Staffing Assessment | Contact"
meta_description: "Request a free medical billing staffing assessment. Share practice-level details only and never patient information. We reply within one business day."
slug: "/contact/"
schema_type: ["ContactPage"]
canonical: "https://medicalbillingteam.com/contact/"
primary_keyword: "medical billing staffing assessment"
search_intent: "transactional"
audience: "prospective clients"
conversion_destination: "form submit"
date_published: "2026-10-18"
date_modified: "2026-10-18"
author: "Medical Billing Team editors"  # brand byline; no invented persona
reviewer: ""  # TONY DECISION: real, authorized reviewer with billing experience; render "Reviewed by" only when set
review_cadence: "semiannual"
---

# Request a free staffing assessment

Tell us about your practice or billing company and a billing staffing specialist will follow up, usually within one business day. The assessment is free and there's no obligation. If remote staff aren't a good fit for you, we'll say so.

> **Do not include any patient information.** This form is for business inquiries only. Please don't enter patient names, dates of birth, addresses, member or policy IDs, claim numbers, account numbers, diagnoses, treatment details or any other health information in any field.

## Form fields

| # | Label | Type | Required | Options / helper text |
|---|---|---|---|---|
| 1 | Your name | text | Yes | |
| 2 | Your role | select | Yes | Practice owner / physician · Practice administrator or office manager · Billing or RCM manager · Billing company owner or manager · Other |
| 3 | Practice or company name | text | Yes | |
| 4 | Specialty | select | Yes | Primary care · Behavioral health / mental health · Substance use treatment center · Physical / occupational therapy · Chiropractic · Laboratory · Ambulatory surgery center · Multi-specialty · Medical billing company · Other (text) |
| 5 | Number of providers | select | Yes | 1 · 2-5 · 6-15 · 16-50 · 50+ · Not applicable (billing company) |
| 6 | Monthly collections range | select | Yes | Under $50k · $50k-$150k · $150k-$500k · $500k-$1M · Over $1M · Prefer not to say |
| 7 | Current billing setup | select | Yes | In-house staff · Outsourced to a billing company · Mix of in-house and outsourced · We are a billing company · Other |
| 8 | Where do you need help? (optional) | checkboxes | No | Billing / claims · A/R follow-up · Eligibility / VOB · Prior authorization · Payment posting · Denial follow-up · Admissions / intake · Coding · Credentialing · Not sure yet |
| 9 | Work email | email | Yes | Please use your practice or company email. |
| 10 | Phone (optional) | tel | No | Only if you'd like a call or text. |

**Phone consent (checkbox under field 10; unchecked by default; shown only when a phone number is entered; NOT required to submit the form):**
> ☐ By checking this box, I agree that Alliance Global Solutions may call or text me at the number I provided about remote medical billing and revenue cycle staffing, including calls or texts made with an autodialer or prerecorded or artificial voice. Consent is not a condition of any purchase or of receiving the assessment. Message and data rates may apply. Message frequency varies. Reply STOP to opt out or HELP for help. You can also withdraw consent by emailing [privacy contact]. See our [Privacy Policy](/privacy/) and [Terms](/terms/).

**Email notice (plain text above the submit button):**
> By submitting, you agree that we may email you about your request and about remote billing and RCM staffing. Every marketing email includes an unsubscribe link, and we honor opt-outs promptly.

**Patient-information reminder (repeated directly above the button):**
> Reminder: do not include any patient information.

**Submit button:** Request my assessment

**Success page / message:**
> Thank you. We've received your request. A staffing specialist will email you, usually within one business day. In the meantime, you might find these useful: [Medical Billing Health Checklist](/checklist/) · [HIPAA guide for outsourced billing staff](/hipaa-outsourced-medical-billing/) · [RCM staffing guide](/revenue-cycle-management-staffing/)

**Error message (validation):** Please complete the required fields. Remember: no patient information.

## Implementation notes for the build (not displayed)

- Store TCPA consent as a separate field with timestamp, page URL, IP address, user agent and the exact consent text version shown. Do not pre-check the box.
- If the phone box is not checked, do not call or text that number using automated means; email only.
- Add a honeypot field and server-side rate limiting; avoid CAPTCHAs that collect extra data where possible.
- Do not write form submissions to page analytics (no form-field values in GA4 events).
- Auto-reply email must include the sender's physical postal address and an unsubscribe link (CAN-SPAM).
- No free-text field: the optional "Anything else?" comments box was removed (Code Desk, 2026-10-18) to reduce PHI risk. Keep every field structured. Name and practice-name fields still get a server-side PHI-pattern check (dates of birth, long ID-like numbers) and length limits.

## Other ways to reach us

- Email: [inquiries email, TBD]
- Mailing address: [postal address, TBD; required in marketing emails]

---
*Disclosure: This site is operated by Alliance Global Solutions, a provider of remote medical billing and revenue cycle staff. We may contact you about our services if you request it.*
