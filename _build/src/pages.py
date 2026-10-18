"""Site map (flat, keyword-led slugs; matches the copywriter's internal links).
key = content filename in content/<key>.md (home = index). A page with no content file
is a STUB: noindex, excluded from sitemap.xml/llms.txt, placeholder text only."""

def P(key, path, label, kind, parent, title, description):
    return dict(key=key, path=path, label=label, kind=kind, parent=parent, title=title, description=description)

PAGES = [
  P("index", "/", "Home", "home", None, "Medical Billing Team: Remote Billing & RCM Staffing", "Guides for US practices on medical billing staffing, RCM, HIPAA and costs."),
  # RCM hub + staffing pillar (parents come from frontmatter `pillar` at build time)
  P("what-is-revenue-cycle-management", "/what-is-revenue-cycle-management/", "What Is RCM", "pillar", None, "What Is Revenue Cycle Management?", "The revenue cycle explained."),
  P("revenue-cycle-management-staffing", "/revenue-cycle-management-staffing/", "RCM Staffing", "pillar", None, "Revenue Cycle Management Staffing", "RCM staffing: workflow, roles, KPIs and costs."),
  P("medical-billing-technology", "/medical-billing-technology/", "Technology", "pillar", None, "Technology in Medical Billing", "AI, automation and what's changing."),
  P("credentialing-services", "/credentialing-services/", "Credentialing Services", "cluster", None, "Credentialing Services", "Provider credentialing and enrollment services."),
  P("credentialing-specialist", "/credentialing-specialist/", "Credentialing Specialists", "cluster", None, "Credentialing Specialist", "What credentialing specialists do."),
  P("prior-authorization-specialist", "/prior-authorization-specialist/", "Prior Authorization", "cluster", None, "Prior Authorization Specialist", "Prior authorization staffing and outsourcing."),
  P("eligibility-verification-prior-authorization", "/eligibility-verification-prior-authorization/", "Insurance Verification", "cluster", None, "Eligibility Verification", "Front-end workflows and staffing."),
  P("treatment-center-vob", "/treatment-center-vob/", "VOB for Treatment Centers", "cluster", None, "VOB for Treatment Centers", "Verification of benefits for treatment centers."),
  P("hire-remote-medical-coders", "/hire-remote-medical-coders/", "Medical Coding", "cluster", None, "Hiring Remote Medical Coders", "Remote medical coders."),
  P("ar-specialist", "/ar-specialist/", "A/R Specialists", "cluster", None, "AR Specialist", "A/R follow-up role."),
  P("virtual-medical-assistant", "/virtual-medical-assistant/", "Virtual Medical Assistants", "cluster", None, "Virtual Medical Assistants", "Virtual medical assistants."),
  P("virtual-medical-receptionist", "/virtual-medical-receptionist/", "Virtual Medical Receptionists", "cluster", None, "Virtual Medical Receptionist", "Virtual medical receptionists."),
  P("medical-billing-outsourcing", "/medical-billing-outsourcing/", "Medical Billing Outsourcing", "cluster", None, "Medical Billing Outsourcing", "The 3 models compared."),
  P("offshore-medical-billers", "/offshore-medical-billers/", "Offshore Medical Billers", "cluster", None, "Offshore Medical Billers", "Offshore billing staff."),
  P("reduce-ar-days", "/reduce-ar-days/", "Reduce A/R Days", "cluster", None, "How to Reduce AR Days", "A/R workflow."),
  # Denials
  P("denial-management", "/denial-management/", "Denial Management", "pillar", None, "Denial Management", "Denial management workflow and staffing."),
  P("denial-code-co-16", "/denial-codes/co-16/", "CO-16", "cluster", None, "CO-16 Denial Code", "CO-16: missing or invalid information."),
  P("denial-code-co-22", "/denial-codes/co-22/", "CO-22", "cluster", None, "CO-22 Denial Code", "CO-22: coordination of benefits."),
  P("denial-code-co-29", "/denial-codes/co-29/", "CO-29", "cluster", None, "CO-29 Denial Code", "CO-29: timely filing."),
  P("denial-code-co-97", "/denial-codes/co-97/", "CO-97", "cluster", None, "CO-97 Denial Code", "CO-97: bundled services."),
  P("denial-code-co-197", "/denial-codes/co-197/", "CO-197", "cluster", None, "CO-197 Denial Code", "CO-197: missing precertification or authorization."),
  P("denial-code-co-204", "/denial-codes/co-204/", "CO-204", "cluster", None, "CO-204 Denial Code", "CO-204: service not covered under the benefit plan."),
  # Other pillars
  P("hire-remote-medical-billers", "/hire-remote-medical-billers/", "Billing Staffing", "pillar", None, "Hiring Remote and Offshore Medical Billers", "Remote and offshore medical billers."),
  P("hipaa-outsourced-medical-billing", "/hipaa-outsourced-medical-billing/", "HIPAA Guide", "pillar", None, "HIPAA and Outsourced Medical Billing Staff", "HIPAA for outsourced billing staff."),
  P("medical-billing-staffing-cost", "/medical-billing-staffing-cost/", "Cost Comparison", "pillar", None, "Medical Billing Staffing Cost", "In-house vs outsourced vs remote."),
  P("behavioral-health-billing", "/behavioral-health-billing/", "Behavioral Health Billing", "pillar", None, "Behavioral Health Billing", "Behavioral health billing staff."),
  # Vendors (guide + approved vendors model)
  P("approved-vendors", "/approved-vendors/", "Approved Vendors", "directory", None, "Approved Vendors", "Vetted medical billing and RCM staffing vendors."),
  P("featured-vendor-alliance-global-solutions", "/approved-vendors/alliance-global-solutions/", "Alliance Global Solutions", "vendor", None, "Alliance Global Solutions: Featured Vendor", "Featured vendor profile."),
  P("how-we-vet-vendors", "/how-we-vet-vendors/", "How We Vet Vendors", "page", None, "How We Vet Vendors", "Our vendor criteria."),
  # Site
  P("how-it-works", "/how-it-works/", "How It Works", "page", None, "How It Works", "How a remote billing staffing engagement works."),
  P("faq", "/faq/", "FAQ", "page", None, "Medical Billing Staffing FAQ", "Common questions."),
  P("checklist", "/checklist/", "Free Checklist", "page", None, "Medical Billing Health Checklist", "A one-page billing self-audit."),
  P("about", "/about/", "About & Disclosure", "page", None, "About This Site and Disclosure", "Who runs this site."),
  P("contact", "/contact/", "Contact", "form", None, "Free Medical Billing Staffing Assessment", "Request a free staffing assessment."),
  P("privacy", "/privacy/", "Privacy", "legal", None, "Privacy Policy", "Privacy policy."),
  P("terms", "/terms/", "Terms", "legal", None, "Terms of Use", "Terms of use."),
  P("thank-you", "/thank-you/", "Thank You", "utility", None, "Thank You", "We received your request."),
]

# Header nav per POSITIONING-CHANGES.md: (label, key) or (label, [keys]) for a dropdown
NAV = [
  ("Billing Staffing", "hire-remote-medical-billers"),
  ("RCM", ["what-is-revenue-cycle-management", "revenue-cycle-management-staffing"]),
  ("Services", ["credentialing-services", "prior-authorization-specialist", "eligibility-verification-prior-authorization", "treatment-center-vob", "hire-remote-medical-coders", "ar-specialist", "virtual-medical-assistant", "virtual-medical-receptionist"]),
  ("Denials", ["denial-management", "denial-code-co-16", "denial-code-co-22", "denial-code-co-29", "denial-code-co-97", "denial-code-co-197", "denial-code-co-204"]),
  ("HIPAA", "hipaa-outsourced-medical-billing"),
  ("Technology", "medical-billing-technology"),
  ("Approved Vendors", "approved-vendors"),
  ("FAQ", "faq"),
]
