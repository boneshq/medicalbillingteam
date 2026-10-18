---
title: "HIPAA and Outsourced Medical Billing Staff: A Guide"
meta_description: "HIPAA for outsourced or offshore medical billing staff: BAAs, minimum necessary, access controls, training, breaches and questions to ask agencies."
slug: "/hipaa-outsourced-medical-billing/"
schema_type: ["Article", "FAQPage"]
faq:
  - q: "Is there such a thing as HIPAA certification?"
    a: "No. There is no official HIPAA certification for companies or individuals. HHS's Office for Civil Rights says it does not endorse, certify or recommend specific technology or products. Private training courses may issue certificates, but these are not government certification of HIPAA compliance."
  - q: "Does a medical billing staffing agency need to sign a BAA?"
    a: "If the agency or its staff will create, receive, maintain or transmit protected health information on your behalf, such as by working claims in your billing system, the agency is generally a business associate and HIPAA requires a business associate agreement before PHI is shared. Confirm your situation with your own counsel."
  - q: "Does the operator sign a BAA?"
    a: "Yes. Alliance Global Solutions signs a Business Associate Agreement with clients before any staff access PHI."
  - q: "Can offshore staff access PHI under HIPAA?"
    a: "HIPAA does not ban offshore work. HHS guidance on cloud services says the rules do not include requirements specific to PHI handled outside the US, but notes that overseas arrangements may increase risk and raise enforceability concerns. Those risks should be addressed in your risk analysis and safeguards."
  - q: "How quickly must a business associate report a breach?"
    a: "Under the Breach Notification Rule, a business associate must notify the covered entity without unreasonable delay and no later than 60 days after discovering a breach of unsecured PHI. Many BAAs set a shorter deadline."
  - q: "What does minimum necessary mean for billing staff?"
    a: "It means making reasonable efforts to use, disclose and request only the minimum PHI needed for the task. For billing staff, that usually means role-based access limited to the queues, screens and payers they actually work."
---

# HIPAA and outsourced medical billing staff: what to check before anyone logs in

*Last reviewed: October 18, 2026. General information, not legal advice. Talk to your own healthcare attorney or compliance adviser about your situation.*

Billing work runs on patient data. Names, dates of birth, member IDs, diagnosis and procedure codes and payment details all sit on the screens your billing staff use every day. So when you bring in outsourced, remote or offshore billing staff through an agency, HIPAA is not a box to tick at the end. It shapes which agency you choose, how the contract is written, how access is set up and what happens if something goes wrong.

This guide explains the main HIPAA concepts that apply when a staffing agency provides dedicated billing staff, and ends with a checklist of questions to ask any agency, including ours.

## First, a myth: there is no "HIPAA certification"

You will see agencies and freelancers describe themselves as "HIPAA certified." There is no such official credential. The HHS Office for Civil Rights (OCR), which enforces HIPAA, says plainly that it "does not endorse, certify, or recommend specific technology or products" ([HHS, Guidance on HIPAA & Cloud Computing](https://www.hhs.gov/hipaa/for-professionals/special-topics/health-information-technology/cloud-computing/index.html)). Training companies issue certificates of course completion, and independent auditors can assess security programs, but neither is a government HIPAA certification.

What matters is evidence of specific safeguards: a signed business associate agreement, documented policies, training records, a current risk analysis and technical controls you can verify. We don't claim to be "HIPAA certified," and you shouldn't accept that claim from anyone.

## Why an agency is usually a business associate

HIPAA's rules apply directly to **covered entities** (health plans, clearinghouses and health care providers that conduct standard electronic transactions such as claims) and to their **business associates**. HHS defines a business associate generally as a person or organization, other than a member of the covered entity's workforce, that performs functions or services on behalf of a covered entity involving the use or disclosure of protected health information (PHI). HHS lists **billing, claims processing and practice management** among the examples ([HHS, Business Associates](https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/business-associates/index.html)).

A staffing agency whose people work your claims, check eligibility or post payments in your systems is therefore typically a business associate. A billing company that serves practices is often itself a business associate, so if it adds agency staff, the agency becomes a **subcontractor business associate**, and HHS says a business associate must have a BAA with its subcontractor before disclosing PHI to it ([HHS](https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/business-associates/index.html)).

Business associates are not just contractually bound. Since the HITECH Act, they are directly liable for complying with the Security Rule's safeguards and certain Privacy Rule provisions ([HHS, Summary of the Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html)).

## The business associate agreement (BAA)

HIPAA permits you to share PHI with a business associate only after you obtain "satisfactory assurances," in the form of a BAA, that it will safeguard the information ([HHS](https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/business-associates/index.html)). According to HHS, a BAA must, among other things:

- describe the permitted and required uses and disclosures of PHI;
- state that the business associate will not use or further disclose PHI except as the agreement permits or the law requires;
- require compliance with applicable Security Rule requirements;
- require reporting of security incidents and breaches of unsecured PHI;
- require that subcontractors agree to the same restrictions through their own BAAs; and
- address return or destruction of PHI at the end of the relationship, where feasible.

HHS publishes [sample business associate agreement provisions](https://www.hhs.gov/hipaa/for-professionals/covered-entities/sample-business-associate-agreement-provisions/index.html). Have your counsel review any BAA rather than relying on the agency's template alone.

**Practical tip:** sign the BAA before you create a single login. No PHI should move during interviews or trials without one.

## PHI handling and the "minimum necessary" standard

The Privacy Rule asks covered entities and business associates to make reasonable efforts to use, disclose and request only the **minimum necessary** PHI for the purpose, and to restrict workforce access based on role ([HHS, Summary of the Privacy Rule](https://www.hhs.gov/hipaa/for-professionals/privacy/laws-regulations/index.html)). For billing teams, minimum necessary in practice looks like:

- A payment poster gets posting screens and remittance files, not full clinical charts.
- An A/R follow-up specialist sees the claims and payer correspondence in their queue, not every patient in the system.
- An eligibility specialist uses payer portals and scheduling data, not visit notes.
- PHI is never pasted into personal email, chat apps, unapproved AI tools or spreadsheets on personal drives.

Behavioral health and substance use disorder programs carry extra rules. Records covered by 42 CFR Part 2 have their own consent and redisclosure limits; HHS notes that compliance with the 2024 Part 2 final rule was required by February 16, 2026 ([HHS, Part 2](https://www.hhs.gov/hipaa/for-professionals/special-topics/hipaa-part-2/index.html)). See our [behavioral health billing guide](/behavioral-health-billing/).

## Access controls to expect

The Security Rule is "technology neutral." It requires access control, audit controls, integrity controls, person or entity authentication and transmission security, but lets each organization choose reasonable and appropriate measures based on its risks ([HHS](https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html)). For remote and offshore billing staff, these are common, sensible controls to ask about:

- **Unique user IDs.** No shared logins, ever. Each person's activity should be traceable.
- **Multi-factor authentication (MFA)** on your practice management system, clearinghouse, payer portals, email and the agency's own systems.
- **Secure remote access.** A VPN, or better, a virtual desktop (VDI) so PHI stays on your servers or cloud and is only displayed remotely.
- **No local downloads, printing or USB storage.** Endpoint controls that block saving files, screenshots where feasible, and removable media.
- **Role-based access** mapped to each job, reviewed regularly, and removed the same day someone leaves.
- **Managed, encrypted company devices** with current patches and endpoint protection, rather than personal computers.
- **Activity logging and audit review.** Logs of who accessed what and when, reviewed on a schedule.
- **Physical controls.** For office-based teams, controlled facility access and clean-desk rules; for home-based staff, private workspaces and screen-privacy rules.

## Workforce training

The Security Rule requires security awareness training for all workforce members and appropriate sanctions for people who violate policies ([HHS](https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html)). Ask the agency for:

- HIPAA privacy and security training at onboarding and at least annually;
- phishing and social-engineering awareness;
- client-specific training on your policies, payer portals and escalation paths;
- signed confidentiality agreements; and
- training records you can review.

## Audits and risk assessments

Both covered entities and business associates must perform an accurate and thorough **risk analysis** of threats to electronic PHI, manage those risks, and periodically evaluate their safeguards ([HHS, Security Rule summary](https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/index.html)). When you add an agency:

- Update your own risk analysis to include the new remote access paths and locations.
- Ask when the agency last completed its risk analysis and what it changed as a result.
- Ask whether it has had an independent security assessment (for example, a third-party audit or penetration test) and whether it will share a summary.
- Agree in writing on your right to request documentation. HHS notes that HIPAA does not expressly require vendors to allow customer audits, but customers may require additional assurances through the BAA or service agreement ([HHS, Cloud Computing FAQ 10](https://www.hhs.gov/hipaa/for-professionals/special-topics/health-information-technology/cloud-computing/index.html)).

## Breach notification

Under the Breach Notification Rule, if a breach of unsecured PHI occurs at or by a business associate, the business associate must notify the covered entity **without unreasonable delay and no later than 60 days** after discovery, and provide, to the extent possible, the identity of affected individuals ([HHS, Breach Notification Rule](https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html)). The covered entity then has its own obligations to notify individuals, HHS and, for larger breaches, the media.

Many practices negotiate a much shorter reporting window in the BAA. Ask the agency to walk you through its incident response plan: who detects an incident, who calls you, and how fast.

## Offshore considerations

HIPAA does not prohibit offshore work. In its cloud guidance, HHS says the HIPAA Rules "do not include requirements specific to protection of electronic protected health information (ePHI) processed or stored by a CSP or any other business associate outside of the United States," but warns that overseas outsourcing "may increase the risks and vulnerabilities to the information or present special considerations with respect to enforceability" ([HHS, Cloud Computing FAQ 9](https://www.hhs.gov/hipaa/for-professionals/special-topics/health-information-technology/cloud-computing/index.html)). Practical steps:

- **Keep PHI onshore where possible.** With VDI, data stays in your US-hosted systems and offshore staff only view it.
- **Know the legal entity.** Confirm which company signs the BAA, where it is incorporated, and whether a US entity is accountable.
- **Check payer and state rules.** Some payer contracts, Medicaid programs and government plans restrict offshore access to member data. Check before you assign offshore staff to those accounts.
- **Plan for continuity.** Ask about power, internet redundancy and backup work sites.
- **Document it in your risk analysis**, including country-specific risks.

## Questions to ask any billing staffing agency

Print this list and use it on every agency call, including with us.

1. Will you sign our BAA (or offer one our counsel can review) before any access to PHI?
2. Which legal entity signs, and do you use any subcontractors who would touch PHI? Do they sign BAAs too?
3. When did you last complete a HIPAA security risk analysis? What changed afterward?
4. Have you had an independent security assessment? Can you share a summary?
5. Do your staff use unique logins and MFA on every system?
6. Do staff work through VDI or VPN? Can they download, print, screenshot or use USB storage?
7. Are devices company-managed and encrypted? Who patches them?
8. How do you enforce minimum necessary and role-based access?
9. What background checks do you run on staff?
10. What HIPAA training do staff complete, how often, and can we see records?
11. Do staff work from an office, from home, or both? What physical safeguards apply?
12. What is your incident response plan, and how fast will you notify us of a suspected incident?
13. How do you remove access on the day someone leaves?
14. How do you handle Part 2 records, if we have them?
15. Do you claim to be "HIPAA certified"? (The right answer is that no such official certification exists.)

## How this site handles your information

Our forms never ask for patient information, and we ask you not to submit any. We collect only business contact and practice-level details. See our [Privacy Policy](/privacy/).

## Next steps

- Compare options in our [medical billing staffing cost guide](/medical-billing-staffing-cost/).
- Read [how to hire remote and offshore medical billers](/hire-remote-medical-billers/).
- Ask us these questions directly with a [free staffing assessment](/contact/). This site is operated by [Alliance Global Solutions](https://www.allianceglobalsolutions.com/about-us/); you can also reach the company through its [contact page](https://www.allianceglobalsolutions.com/contact/).

## FAQ

**Is there such a thing as HIPAA certification?**
No. There is no official HIPAA certification for companies or people. OCR does not endorse or certify products or vendors.

**Does a billing staffing agency need to sign a BAA?**
If its staff will create, receive, maintain or transmit PHI on your behalf, it is generally a business associate and a BAA is required before PHI is shared.

**Does the operator sign a BAA?**
Yes. Alliance Global Solutions signs a Business Associate Agreement with clients before any staff access PHI.

**Can offshore staff access PHI under HIPAA?**
HIPAA has no offshore-specific ban, but HHS notes increased risk and enforceability concerns. Address them in your risk analysis and safeguards, and check payer contracts.

**How quickly must a business associate report a breach?**
Without unreasonable delay and no later than 60 days after discovery. Many BAAs require faster notice.

**What does minimum necessary mean for billing staff?**
Access only to the PHI each role needs, enforced by role-based permissions.

---
*Disclosure: This site is operated by Alliance Global Solutions, a provider of remote medical billing and revenue cycle staff. We may contact you about our services if you request it. This page is general information, not legal advice.*
