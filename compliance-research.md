# Regulatory & Compliance Landscape for Automotive Lead Generation

**Last updated:** March 2026

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [TCPA Compliance](#2-tcpa-compliance)
3. [State Privacy Laws](#3-state-privacy-laws)
4. [FTC Safeguards Rule](#4-ftc-safeguards-rule)
5. [Do Not Call Registry Compliance](#5-do-not-call-registry-compliance)
6. [CAN-SPAM Requirements](#6-can-spam-requirements)
7. [Data Broker Registration Requirements](#7-data-broker-registration-requirements)
8. [Consent Management Framework](#8-consent-management-framework)
9. [Penalties and Enforcement Trends](#9-penalties-and-enforcement-trends)
10. [Compliance Infrastructure Recommendations](#10-compliance-infrastructure-recommendations)
11. [Compliance Checklist for Launch](#11-compliance-checklist-for-launch)
12. [Ongoing Compliance Obligations](#12-ongoing-compliance-obligations)
13. [Sources](#13-sources)

---

## 1. Executive Summary

Operating an automotive lead generation business in the United States in 2026 requires navigating a complex, multi-layered regulatory environment. There is no single federal privacy law; instead, businesses face a patchwork of federal statutes (TCPA, CAN-SPAM, FTC Safeguards Rule, Gramm-Leach-Bliley Act) combined with **20+ state consumer privacy laws**, each with distinct requirements, exemptions, and enforcement mechanisms.

### Key Regulatory Risks

| Risk Area | Severity | Maximum Penalty Per Violation |
|-----------|----------|-------------------------------|
| TCPA violations (calls/texts) | **Critical** | $500-$1,500 per call/text |
| State privacy law violations | **High** | $7,500-$100,000 per violation (varies by state) |
| CAN-SPAM violations | **High** | $53,088 per email |
| FTC Safeguards Rule violations | **High** | $11,000+ per day |
| Do Not Call violations | **High** | $51,744 per call |
| Data broker registration failures | **Medium** | $100-$100,000 per day (varies by state) |
| Texas SB 140 violations | **High** | $1,500 per text + DTPA liability |

### Current Regulatory Landscape Summary

- The FCC's one-to-one consent rule was **vacated** by the 11th Circuit and formally withdrawn (August 2025), but best practice still favors single-seller consent
- TCPA consent revocation rules **took effect April 11, 2025**: consumers can revoke consent by any reasonable method; businesses must honor within 10 business days
- **20 states** have comprehensive consumer privacy laws in effect as of January 2026, with more expected by year-end
- The FTC CARS Rule was **vacated** by the 5th Circuit (January 2025), but state-level equivalents are emerging
- Texas SB 140 (effective September 1, 2025) expanded telemarketing law to cover all text messages
- Data broker registration is required in **California, Texas, Vermont, and Oregon**, with more states considering legislation

---

## 2. TCPA Compliance

The Telephone Consumer Protection Act (47 U.S.C. SS 227) is the single most litigated statute affecting lead generation businesses. In Q1 2025 alone, **507 TCPA class actions were filed -- a 112% increase** over Q1 2024.

### 2.1 Core Requirements

**Prior Express Written Consent (PEWC) is required before:**
- Making any telemarketing call using an automatic telephone dialing system (ATDS) or prerecorded voice
- Sending any marketing text message (SMS, MMS, RCS)
- Making any telemarketing call to a number on the Do Not Call registry

**PEWC must include:**
1. A clear and conspicuous disclosure that the consumer is agreeing to receive marketing calls/texts
2. The name of the specific seller(s) authorized to contact the consumer
3. The telephone number(s) to which calls may be made
4. Disclosure that calls may use an ATDS or prerecorded voice
5. Disclosure that consent is not a condition of purchase
6. Consumer's signature (electronic signatures acceptable)

### 2.2 Recent Regulatory Changes (2025-2026)

#### One-to-One Consent Rule -- VACATED

| Event | Date | Outcome |
|-------|------|---------|
| FCC adopted one-to-one consent rule | December 2023 | Required consent specific to each individual seller |
| Effective date postponed | January 24, 2025 | Delayed to January 26, 2026 |
| 11th Circuit vacated the rule | February 2025 | Found FCC exceeded its authority |
| FCC formally withdrew the rule | August 29, 2025 | Reinstated prior standard |

**Practical impact:** While the one-to-one consent rule was struck down, sophisticated lead buyers increasingly demand single-seller consent as a contractual requirement. Multi-seller disclosures listing dozens of potential callers create significant litigation risk even if technically compliant under the current standard. **Best practice: implement single-seller consent anyway.**

#### Consent Revocation Rules -- IN EFFECT (April 11, 2025)

| Requirement | Detail |
|-------------|--------|
| Revocation method | Consumer may revoke consent by **any reasonable method** (not just "STOP") |
| Processing deadline | Must honor revocation within **10 business days** |
| Scope | Applies to both marketing and informational messages |
| "Revocation-all" requirement | Delayed until **January 31, 2027** (a single opt-out applying across all message types from the same sender) |

**Key implication for lead gen:** If a consumer tells a dealer "stop calling me" by email, voicemail, chat, social media, or any other channel, that revocation is binding. Systems must be able to capture and process revocations from any channel.

### 2.3 What Constitutes an ATDS

The Supreme Court's decision in *Facebook v. Duguid* (2021) narrowed the ATDS definition to equipment that uses a random or sequential number generator to either store or produce phone numbers and dial those numbers. However, many state mini-TCPA statutes have broader definitions, and litigation continues over what constitutes an ATDS.

### 2.4 Lead Generation-Specific TCPA Rules

For lead generators selling leads to multiple buyers:

- **Consent must clearly identify the seller(s)** who will contact the consumer
- **Consent cannot be a condition** of purchasing goods or services
- **Consent disclosures must be "clear and conspicuous"** -- not buried in terms of service
- **Lead sellers must provide consent documentation** to lead buyers before calls are made
- **Consent records must be retained** for at least 5 years (recommended)
- **Each call/text without proper consent** is a separate violation ($500-$1,500)

### 2.5 Texas SB 140 (Effective September 1, 2025)

Texas enacted one of the most aggressive state-level telemarketing laws targeting text messages:

| Requirement | Detail |
|-------------|--------|
| Scope | Expands "telephone solicitation" to include SMS, MMS, and RCS messages |
| Registration | Must register with TX Secretary of State (Form 3401) |
| Fee | $200 filing fee + **$10,000 security bond** |
| Consent | Prior express written consent required; cannot be condition of purchase |
| Private right of action | Violations actionable under **Texas Deceptive Trade Practices Act (DTPA)** |
| Penalty | Up to **$1,500 per text** |
| Exemption | Consent-based opt-in SMS programs and messages to current/former customers are exempt from registration |

**Critical note:** The Texas Attorney General confirmed (November 2025) that companies engaging in consent-based opt-in text messaging are not subject to the registration requirement. However, any non-consent-based marketing text triggers full registration and bonding requirements.

---

## 3. State Privacy Laws

As of March 2026, **20 states** have comprehensive consumer privacy laws in effect, with several more having passed legislation with future effective dates. There is no federal comprehensive privacy law.

### 3.1 States with Active Comprehensive Privacy Laws

| State | Law | Effective Date | Key Provisions for Lead Gen |
|-------|-----|---------------|---------------------------|
| **California** | CCPA/CPRA | Jan 1, 2020 / Jan 1, 2023 | Right to delete, opt-out of sale/sharing, data broker registration, $7,500/violation (intentional) |
| **Virginia** | VCDPA | Jan 1, 2023 | Opt-out of targeted advertising, sale, profiling; SB 338 bans sale of precise geolocation data (Feb 2026) |
| **Colorado** | CPA | Jul 1, 2023 | Universal opt-out mechanism required; data protection assessments |
| **Connecticut** | CTDPA | Jul 1, 2023 | Amendments effective Jul 1, 2026 lower thresholds |
| **Utah** | UCPA | Dec 31, 2023 | HB 357 extends coverage to motor vehicle manufacturers regardless of size |
| **Iowa** | ICDPA | Jan 1, 2025 | No right to correct data; no opt-out of profiling; 90-day cure period |
| **Delaware** | DPDPA | Jan 1, 2025 | Covers entities processing data of 35,000+ consumers |
| **Nebraska** | NDPA | Jan 1, 2025 | No cure period; AG enforcement only |
| **New Hampshire** | NHPA | Jan 1, 2025 | Standard consumer rights model |
| **New Jersey** | NJDPA | Jan 15, 2025 | Covers entities with 100,000+ consumer records or 25,000+ with revenue from data sales |
| **Tennessee** | TIPA | Jul 1, 2025 | 60-day cure period; affirmative defense for NIST framework compliance |
| **Minnesota** | MCDPA | Jul 31, 2025 | Consumers can question logic behind profiling decisions |
| **Maryland** | MODPA | Oct 1, 2025 | Prohibits sale of sensitive data; restricts data minimization |
| **Indiana** | ICDPA | Jan 1, 2026 | Standard consumer rights model |
| **Kentucky** | KCDPA | Jan 1, 2026 | Standard consumer rights model; 30-day cure period |
| **Rhode Island** | RIDTPPA | Jan 1, 2026 | Low threshold: 35,000 consumers or 10,000 if 20%+ revenue from data sales |

**Laws effective later in 2026:**

| State | Law | Effective Date |
|-------|-----|---------------|
| **Arkansas** | APDPA | Jul 1, 2026 |
| **Connecticut** (amendments) | CTDPA amendments | Jul 1, 2026 |
| **Utah** (amendments) | UCPA amendments | Jul 1, 2026 |

### 3.2 Key Requirements Across State Privacy Laws

**Common requirements that affect lead generation:**

1. **Privacy Notice / Policy:** Must clearly disclose categories of data collected, purposes, third parties data is shared with, and consumer rights
2. **Opt-Out Rights:** Consumers must be able to opt out of:
   - Sale of personal data
   - Targeted advertising
   - Profiling for decisions with legal or significant effects
3. **Data Protection Assessments:** Required before processing data for targeted advertising or selling personal data (most states except Iowa)
4. **Consumer Rights:** Right to access, correct, delete, and obtain a copy of personal data; right to appeal denials
5. **Sensitive Data:** Requires opt-in consent for processing sensitive data (which includes precise geolocation in many states)
6. **Data Minimization:** Several states (especially Maryland) require that data collection be limited to what is reasonably necessary for the disclosed purpose
7. **Response Deadlines:** 30-60 days depending on state (with extensions available)

### 3.3 California-Specific Requirements (CCPA/CPRA)

California has the most stringent requirements and is the most actively enforced:

| Requirement | Detail |
|-------------|--------|
| "Do Not Sell or Share My Personal Information" link | Required on every page that collects data |
| Risk assessments | Required before targeted advertising or selling data |
| Dark patterns prohibition | Cookie banners and consent flows must not use manipulative design |
| Data broker registration | Annual registration with CPPA (California Privacy Protection Agency) |
| Registration fee | **$6,000/year** (as of 2026) |
| DELETE Request platform (DROP) | Must process consumer deletion requests through state platform (August 2026) |
| Penalties | **$2,500** per unintentional violation; **$7,500** per intentional violation or violation involving minors |
| Private right of action | For data breaches resulting from failure to implement reasonable security |
| Expanded data broker disclosure | SB 361 requires disclosure of data sold to foreign actors, governments, or AI developers |

### 3.4 Geolocation Data Restrictions

A growing trend critical for automotive lead gen (which often relies on location-based targeting):

| State | Restriction | Effective |
|-------|------------|-----------|
| Maryland | Prohibits sale of precise geolocation data | Oct 1, 2025 |
| Oregon | Restricts sale of geolocation data within 1,750-foot radius | Jan 1, 2026 |
| Virginia | SB 338 bans sale of precise geolocation data | Feb 2026 |
| Multiple states | Similar legislation under consideration in 2026 sessions | Pending |

### 3.5 Building to the Most Restrictive Standard

For a national lead generation operation, the practical approach is to **build compliance to the most restrictive state standard** (currently California/Maryland) and apply it uniformly. This avoids the need for state-by-state compliance logic and reduces risk of inadvertent violations.

---

## 4. FTC Safeguards Rule

The FTC Safeguards Rule (16 CFR Part 314) implements the data security provisions of the Gramm-Leach-Bliley Act (GLBA). It applies to "financial institutions," which the FTC defines broadly.

### 4.1 Applicability to Lead Generation

The 2021 amendments added **"finders"** to the definition of financial institution -- companies that bring together buyers and sellers, where the parties themselves negotiate and consummate the transaction. **An automotive lead generation company that connects car buyers with dealers likely qualifies as a "finder" and must comply with the Safeguards Rule.**

### 4.2 Nine Required Elements

| # | Requirement | Detail |
|---|-------------|--------|
| 1 | Designated Qualified Individual | Appoint a person responsible for implementing and supervising the information security program |
| 2 | Risk Assessment | Identify reasonably foreseeable risks to customer information; assess sufficiency of safeguards |
| 3 | Safeguards to Address Risks | Implement access controls, data inventory, encryption, secure development, authentication, disposal, change management, monitoring |
| 4 | Regular Testing/Monitoring | Continuous monitoring or annual penetration testing + semi-annual vulnerability assessments |
| 5 | Staff Training | Security awareness training for all employees |
| 6 | Service Provider Oversight | Select providers that can maintain safeguards; contractually require safeguards; periodically assess |
| 7 | Keep Program Current | Update based on operational changes, threat intelligence, risk assessments |
| 8 | Incident Response Plan | Written plan for responding to security events |
| 9 | Board Reporting | Qualified Individual reports in writing to board/governing body at least annually |

### 4.3 Specific Technical Requirements

- **Encryption** of all customer data at rest and in transit
- **Multi-factor authentication (MFA)** for accessing customer information systems
- **Access controls** limiting who can access customer data (least privilege)
- **Data retention and disposal** policies -- must securely dispose of data no longer needed
- **Change management** procedures for information systems
- **Audit trail** logging of access to customer information

### 4.4 Small Business Exemption

Companies maintaining information on **fewer than 5,000 consumers** are exempt from:
- Written risk assessment documentation
- Continuous monitoring or penetration testing/vulnerability assessment schedule
- Written incident response plan
- Annual board reporting

However, they **must still** appoint a qualified individual, implement safeguards, provide security training, and keep systems updated.

### 4.5 Breach Notification

- Must notify the FTC within **30 days** if a breach affects **500+ consumers**
- Notification must include: nature of event, categories of information involved, number of consumers affected, remediation steps
- Effective since May 13, 2024

### 4.6 Penalties

- **$11,000+ per day** per violation (adjusted annually for inflation)
- FTC has authority to seek injunctive relief, restitution, and disgorgement of profits
- State attorneys general can also enforce under state unfair/deceptive practices laws

---

## 5. Do Not Call Registry Compliance

### 5.1 Federal Do Not Call Registry

The National Do Not Call Registry (managed by FTC) prohibits telemarketing calls to registered numbers.

| Requirement | Detail |
|-------------|--------|
| Registry access | Must subscribe via telemarketing.donotcall.gov |
| Annual subscription fee | $72 per area code (first 5 free); capped at $20,238/year for all area codes |
| Scrub frequency | Must scrub calling lists against the registry **every 31 days** |
| Record retention | Must retain scrub records for **5 years** |
| Exemptions | Calls to existing customers (within 18 months of last transaction or 3 months of inquiry); calls with prior express written consent |
| Penalties | Up to **$51,744 per call** (2025 adjusted amount) |

### 5.2 Internal Do Not Call List

**Every lead generation company must maintain its own internal Do Not Call list:**
- Must add any consumer who requests not to be called
- Must honor requests **within 10 business days** (aligned with TCPA consent revocation)
- Must retain internal DNC records for **5 years**
- Must train all personnel on DNC procedures
- Must have a written DNC policy

### 5.3 State Do Not Call Registries

Several states maintain their own Do Not Call registries in addition to the federal registry:
- Indiana, Louisiana, Missouri, Pennsylvania, Texas, Wyoming (among others)
- Some require separate registration fees
- State-specific calling hour restrictions vary (most prohibit calls before 8 AM or after 9 PM local time)

### 5.4 Lead Generation-Specific DNC Rules

- **Scrub all leads against federal and applicable state DNC registries** before selling to dealers
- **Pass-through DNC compliance:** if a dealer contacts a consumer from your lead and the consumer's number is on the DNC list, **both the dealer and the lead provider may face liability**
- **"Established Business Relationship" (EBR) exemption:** a lead submitted by a consumer creates an inquiry-based EBR that **expires after 3 months** -- after that, DNC rules apply in full
- **Time-of-day restrictions:** no calls before 8 AM or after 9 PM in the consumer's time zone

---

## 6. CAN-SPAM Requirements

The CAN-SPAM Act (15 U.S.C. SS 7701-7713) governs commercial email messages.

### 6.1 Core Requirements

| Requirement | Detail |
|-------------|--------|
| Accurate header information | "From," "To," "Reply-To," and routing information must be accurate |
| Non-deceptive subject lines | Must accurately reflect the content of the message |
| Ad identification | Must clearly identify the message as an advertisement |
| Physical address | Must include valid physical postal address |
| Opt-out mechanism | Must include a clear, conspicuous way to opt out; opt-out mechanism must work for at least 30 days after sending |
| Honor opt-outs | Must process unsubscribe requests within **10 business days** |
| Third-party liability | If you pay someone to send emails promoting your product, you are responsible for their compliance |

### 6.2 What CAN-SPAM Does NOT Require

- **No opt-in requirement:** CAN-SPAM does not require prior consent to send commercial emails (unlike TCPA for calls/texts). However, state laws and platform policies may impose stricter requirements.
- **No private right of action:** Only the FTC, state AGs, and ISPs can enforce CAN-SPAM. Consumers cannot sue directly.

### 6.3 Lead Generation Implications

- **Transactional emails** (e.g., confirming a lead submission, providing requested incentive information) are largely exempt from CAN-SPAM -- but the content must be primarily transactional, not promotional
- **Co-registration emails:** if a consumer submits a lead and you share their email with dealer partners, the dealer's subsequent emails must comply with CAN-SPAM
- **Affiliate/partner liability:** the lead generator is liable for CAN-SPAM violations committed by downstream recipients of leads if the lead generator initiates or procures the sending of the email
- **Harvesting prohibition:** CAN-SPAM prohibits using automated tools to harvest email addresses from websites or generating email addresses through dictionary attacks

### 6.4 Penalties

- **$53,088 per email** in violation (2025 adjusted amount)
- Both the company whose product is promoted and the company that sent the message can be held liable
- Criminal penalties possible for aggravated violations (spoofing, harvesting, relay hijacking)

---

## 7. Data Broker Registration Requirements

Whether an automotive lead generation company qualifies as a "data broker" depends on state-specific definitions. Generally, a data broker is an entity that knowingly collects and sells the personal information of consumers with whom it does not have a direct relationship.

### 7.1 Registration Requirements by State

| State | Registry | Fee | Key Requirements | Penalties |
|-------|----------|-----|-----------------|-----------|
| **California** | CPPA (DROP platform) | **$6,000/year** | Annual registration (Jan 1-31); SB 361 requires expanded disclosures about data sold to foreign actors, governments, AI developers; must process deletion requests via DROP (Aug 2026) | **$200/day** failure to register |
| **Texas** | Secretary of State | **$300/year** | Must maintain written information security program; disclose data practices | Up to **$100/day** |
| **Vermont** | Secretary of State | **$100/year** | Annual registration; must disclose opt-out mechanisms; security standards | Up to **$10,000** per violation |
| **Oregon** | State registry | Varies | Annual registration; restrictions on sale of geolocation data and minors' data | Varies |

**States with pending legislation:** New Jersey, Delaware, Michigan, Alaska

### 7.2 Does an Automotive Lead Gen Company Qualify as a Data Broker?

**Likely yes, if:**
- You collect consumer information (name, phone, email, vehicle preferences) through your own forms
- You sell or license that information to dealers with whom the consumer has no direct relationship
- You do not have a prior direct relationship with the consumer

**Likely no (or exempt), if:**
- The consumer voluntarily submits information specifically to be contacted by a named dealer (arguable direct relationship)
- You are acting purely as a technology platform connecting the consumer to a specific dealer at the consumer's request

**Recommendation:** Consult with legal counsel to evaluate data broker status in each applicable state. Register proactively in California (given high penalties and broad definition) and monitor developments in other states.

---

## 8. Consent Management Framework

Consent management is the operational backbone of lead generation compliance. Every lead must have a documented, verifiable consent trail.

### 8.1 What Consent to Collect

| Consent Type | When Required | Standard |
|-------------|---------------|----------|
| **Prior Express Written Consent (PEWC)** | Before any marketing call/text via ATDS or prerecorded voice | Written agreement (electronic OK) signed by consumer, identifying specific seller(s), disclosing ATDS use, stating consent is not condition of purchase |
| **Prior Express Consent** | Before any non-marketing call/text via ATDS | Providing phone number voluntarily in context of transaction |
| **Email consent** | Not legally required under CAN-SPAM (but recommended) | Opt-in recommended; required by some state laws and email platform policies |
| **Data processing consent** | Before processing sensitive data under state privacy laws | Opt-in consent for sensitive data (precise geolocation, financial data) |
| **Opt-out of sale/sharing** | Must be offered to California residents (and other states) | "Do Not Sell or Share" mechanism required |

### 8.2 How to Collect Consent

**TCPA-compliant lead form requirements:**

1. **Clear, conspicuous disclosure** above or immediately adjacent to the submit button
2. **Specific seller identification** -- name the company(ies) that will contact the consumer
3. **Separate consent checkbox** (not pre-checked) -- consent must not be bundled with terms of service
4. **Disclosure that ATDS/prerecorded messages may be used**
5. **Statement that consent is not a condition of purchase**
6. **Consumer's signature** (clicking submit with a clear statement = electronic signature)

**Example compliant consent language:**
> By clicking "Submit," I consent to receive marketing calls and text messages from [Company Name] at the phone number provided above, including calls made using an automatic telephone dialing system or prerecorded voice. I understand that my consent is not a condition of any purchase. Message and data rates may apply. I can revoke my consent at any time.

### 8.3 What to Store (Consent Record)

For every lead, store and retain:

| Data Element | Purpose |
|-------------|---------|
| Consumer's name | Identity verification |
| Phone number(s) and email(s) | Contact information subject to consent |
| Exact consent language displayed | Proof of disclosure |
| Timestamp of consent (UTC) | Temporal verification |
| IP address at time of consent | Location/identity verification |
| User agent / device info | Verification that consent came from a real person |
| Page URL where consent was given | Context verification |
| Form version / hash | Proof of what the consumer saw |
| TrustedForm certificate (or equivalent) | Independent third-party consent verification |
| Opt-out/revocation records | Proof of compliance with revocation requests |

### 8.4 How Long to Keep Consent Records

| Record Type | Minimum Retention | Recommended Retention |
|------------|-------------------|----------------------|
| TCPA consent records | 5 years (statute of limitations: 4 years federal, varies by state) | **6 years** |
| DNC scrub records | 5 years (FTC requirement) | **6 years** |
| CAN-SPAM opt-out records | No specific requirement | **6 years** |
| State privacy law records | Varies (typically 2-3 years after last interaction) | **6 years** |
| Consent revocation records | Indefinite (must continue honoring) | **Indefinite** |
| Data protection assessments | Duration of processing + reasonable period | **6 years** |

### 8.5 Consent Verification Technology

| Platform | Function |
|----------|----------|
| **TrustedForm** (ActiveProspect) | Independent third-party certificate for every lead form submission; captures page snapshot, consent language, consumer interaction |
| **Jornaya / LeadiD** (Verisk) | Lead verification and scoring; identifies duplicate/recycled leads; provides consent audit trail |
| **ActiveProspect** | End-to-end consent management; TCPA Guardian for real-time compliance checking |
| **Anura** | Ad fraud detection; identifies bot-generated leads |

---

## 9. Penalties and Enforcement Trends

### 9.1 TCPA Litigation Trends

| Metric | Value |
|--------|-------|
| Q1 2025 TCPA class actions filed | **507** (112% increase over Q1 2024) |
| Average TCPA class action settlement | **$6.6 million** |
| Largest TCPA fine (Dish Network) | **$280 million** |
| Capital One TCPA settlement | **$75 million** |
| Papa John's TCPA settlement | **$16 million** |
| Per-violation penalty range | $500 (negligent) to $1,500 (willful/knowing) |

**Trend:** TCPA litigation is accelerating, not declining. The vacating of the one-to-one consent rule has not reduced litigation volume; plaintiffs' attorneys are finding other grounds (consent revocation, ATDS claims, DNC violations).

### 9.2 State Privacy Law Enforcement

| State | Enforcement Body | Notable Actions |
|-------|-----------------|-----------------|
| California | CPPA + AG | Most active; CPPA has dedicated enforcement division; first enforcement actions under CPRA in 2024-2025 |
| Texas | AG Ken Paxton | Aggressive enforcement of TDPSA; multiple actions against data brokers and ad tech companies |
| Connecticut | AG | Active in automotive privacy enforcement |
| Maryland | AG | Focus on data minimization requirements (MODPA effective Oct 2025) |

### 9.3 FTC Enforcement

- FTC has brought enforcement actions against automotive lead generators for deceptive practices
- The CARS Rule was vacated (Jan 2025), but FTC retains authority under Section 5 (unfair/deceptive acts)
- FTC Safeguards Rule enforcement is increasing; multiple enforcement actions against financial institutions for inadequate data security
- California SB 766 (California CARS Act) is being pursued at state level as substitute for federal CARS Rule

### 9.4 California SB 37 (Lead Generator Accountability)

California SB 37 (effective 2026) specifically targets lead generators:
- Imposes **$100,000 fines** for lead generators that violate consumer protection laws
- Requires lead generators to maintain records of consent and lead distribution
- Creates additional liability for generating leads through deceptive means

### 9.5 Mini-TCPA State Laws

Several states have their own TCPA-equivalent statutes with independent penalties:

| State | Law | Key Difference |
|-------|-----|----------------|
| Florida | Florida TCPA (FTSA) | Broader ATDS definition; $500/$1,500 per violation; **no federal preemption** |
| Washington | WA TCPA equivalent | State AG can seek treble damages |
| Oklahoma | OTPA | Covers text messages separately |
| Texas | SB 140 | Text messages = telephone solicitation; DTPA private right of action |

---

## 10. Compliance Infrastructure Recommendations

### 10.1 Technology Stack

| Category | Recommended Tools | Purpose |
|----------|------------------|---------|
| Consent management | TrustedForm, ActiveProspect | Capture, store, and verify consent for every lead |
| Lead verification | Jornaya/LeadiD, Anura | Detect fraudulent, bot-generated, and recycled leads |
| DNC scrubbing | DNC.com, Gryphon, Contact Center Compliance | Scrub leads against federal and state DNC registries |
| Privacy management | OneTrust, Osano, or TrustArc | Manage privacy notices, consent preferences, data subject requests, cookie consent |
| Email compliance | Built-in ESP tools (SendGrid, Mailchimp) | CAN-SPAM compliance, unsubscribe management |
| Data security | Encryption (AES-256), MFA, WAF, SIEM | FTC Safeguards Rule compliance |
| Consent revocation processing | Custom system integrated with CRM/CMS | Track and honor revocations from any channel within 10 business days |

### 10.2 Policies and Documentation

**Required written policies:**
1. Information Security Program (FTC Safeguards Rule)
2. Privacy Policy (state privacy laws)
3. Do Not Call Policy and Procedures
4. Consent Management Policy
5. Data Retention and Disposal Policy
6. Incident Response Plan
7. Employee Training Program Documentation
8. Vendor/Service Provider Assessment Policy
9. Data Protection Assessment templates (for targeted advertising, data sales)

### 10.3 Organizational Requirements

| Role | Responsibility |
|------|---------------|
| **Qualified Individual** (Safeguards Rule) | Oversees information security program; reports to board annually |
| **Privacy Officer / DPO** | Manages privacy compliance, data subject requests, privacy impact assessments |
| **Compliance Manager** | Oversees TCPA, CAN-SPAM, DNC compliance; manages consent records |
| **Legal Counsel** | Reviews consent language, privacy policies, vendor contracts; monitors regulatory changes |

For a startup, these roles may be combined or outsourced. At minimum, designate one person as the Qualified Individual and retain specialized TCPA/privacy legal counsel.

### 10.4 Vendor Management

Any vendor or partner that handles consumer data must:
- Be contractually bound to maintain appropriate safeguards
- Be assessed for security practices before engagement
- Be periodically re-assessed
- Have data processing agreements (DPAs) in place
- Be subject to the same consent and DNC requirements

---

## 11. Compliance Checklist for Launch

### Legal Foundation
- [ ] Retain TCPA/privacy specialized legal counsel
- [ ] Incorporate entity; determine data broker registration obligations
- [ ] Draft and publish privacy policy compliant with all applicable state laws
- [ ] Draft terms of service with binding arbitration clause (TCPA litigation defense)
- [ ] Register as data broker in California ($6,000), Texas ($300), Vermont ($100), Oregon (if applicable)
- [ ] Register as telephone solicitor in Texas (Form 3401, $200 + $10,000 bond) if sending marketing texts to TX consumers
- [ ] Evaluate applicability of FTC Safeguards Rule; if applicable, develop written Information Security Program

### Consent Infrastructure
- [ ] Implement TCPA-compliant lead capture forms with clear consent language
- [ ] Integrate TrustedForm or equivalent for independent consent verification
- [ ] Implement Jornaya/LeadiD for lead verification and fraud detection
- [ ] Build consent record storage system (all elements from Section 8.3)
- [ ] Implement consent revocation processing across all channels (10 business day SLA)
- [ ] Set up "Do Not Sell or Share" mechanism for California (and other applicable states)

### DNC Compliance
- [ ] Subscribe to National Do Not Call Registry
- [ ] Implement automated DNC scrubbing (every 31 days minimum)
- [ ] Subscribe to applicable state DNC registries
- [ ] Build internal DNC list management system
- [ ] Document DNC procedures and train all staff

### Email Compliance
- [ ] Ensure all commercial emails include required CAN-SPAM elements
- [ ] Implement functional unsubscribe mechanism (processed within 10 business days)
- [ ] Include valid physical postal address in all emails

### Data Security (FTC Safeguards Rule)
- [ ] Designate Qualified Individual
- [ ] Conduct initial risk assessment
- [ ] Implement encryption at rest and in transit
- [ ] Implement multi-factor authentication
- [ ] Set up access controls (least privilege)
- [ ] Implement logging and monitoring
- [ ] Develop incident response plan
- [ ] Develop employee security training program
- [ ] Conduct initial penetration test and vulnerability assessment

### Operational Compliance
- [ ] Train all employees on privacy, TCPA, DNC, and data security requirements
- [ ] Establish process for responding to consumer data rights requests (30-45 day SLA)
- [ ] Implement data retention and disposal schedule
- [ ] Set up compliance monitoring and audit procedures
- [ ] Document all data flows (what data is collected, where it goes, who has access)
- [ ] Conduct Data Protection Assessments for targeted advertising and data sales activities

---

## 12. Ongoing Compliance Obligations

### Monthly
- [ ] Scrub lead lists against federal DNC registry (every 31 days)
- [ ] Review and process consent revocation requests (within 10 business days)
- [ ] Process consumer data rights requests within state-mandated timelines
- [ ] Monitor TCPA litigation developments and FCC rulemaking

### Quarterly
- [ ] Review consent language and form compliance
- [ ] Audit consent records for completeness
- [ ] Review and update internal DNC list
- [ ] Conduct employee compliance training refresher
- [ ] Assess vendor compliance

### Semi-Annually
- [ ] Vulnerability assessment (FTC Safeguards Rule)
- [ ] Review and update privacy policy for any changes in data practices
- [ ] Update data flow documentation

### Annually
- [ ] Penetration testing (FTC Safeguards Rule, if not doing continuous monitoring)
- [ ] Qualified Individual report to board/management (FTC Safeguards Rule)
- [ ] Full risk assessment update (FTC Safeguards Rule)
- [ ] Renew data broker registrations (California: January; Texas, Vermont, Oregon: varies)
- [ ] Renew DNC registry subscriptions
- [ ] Comprehensive compliance audit
- [ ] Review Data Protection Assessments
- [ ] Update employee training program
- [ ] Review and renew Texas SB 140 registration and bond (if applicable)

### As Needed
- [ ] Update privacy policy when data practices change
- [ ] Update consent language when adding new dealer partners or changing contact methods
- [ ] Respond to regulatory inquiries or enforcement actions within required timeframes
- [ ] Report data breaches within 30 days to FTC (if 500+ consumers affected) and to applicable state AGs
- [ ] Monitor and comply with new state privacy laws as they take effect

---

## 13. Sources

### Federal Regulations
- [FCC One-to-One Consent Rule (Final Order)](https://docs.fcc.gov/public/attachments/DOC-408396A1.pdf)
- [FCC Lead Generation Ruling Guide - ActiveProspect](https://activeprospect.com/blog/fcc-lead-generation/)
- [FCC TCPA One-to-One Rule Status - Womble Bond Dickinson](https://www.womblebonddickinson.com/us/insights/blogs/fcc-tcpa-one-one-lead-generator-consent-rule-effect-january-27-2025)
- [FCC Final Rule Kills One-to-One Consent - Consumer Financial Services Law Monitor](https://www.consumerfinancialserviceslawmonitor.com/2025/09/fccs-final-rule-on-consent-kills-one-to-one-consent-requirement/)
- [TCPA Consent Rule Changes 2026 - Tratta](https://www.tratta.io/blog/tcpa-consent-rule-changes)
- [FTC Safeguards Rule - Federal Trade Commission](https://www.ftc.gov/legal-library/browse/rules/safeguards-rule)
- [FTC Safeguards Rule Guide for Businesses](https://www.ftc.gov/business-guidance/resources/ftc-safeguards-rule-what-your-business-needs-know)
- [FTC Safeguards Rule for Lead Gen Companies - Boberdoo](https://www.boberdoo.com/news/are-you-ready-for-the-ftc-safeguard-rules-a-guide-for-lead-generation-companies)
- [FTC Safeguards Rule Notification Requirement](https://www.ftc.gov/business-guidance/blog/2024/05/safeguards-rule-notification-requirement-now-effect)
- [CAN-SPAM Act Compliance Guide - FTC](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business)
- [Gramm-Leach-Bliley Act - FTC](https://www.ftc.gov/business-guidance/privacy-security/gramm-leach-bliley-act)
- [FTC CARS Rule - NADA](https://www.nada.org/nada/issues/ftc-vehicle-shopping-rule)
- [5th Circuit Vacates CARS Rule - Seyfarth Shaw](https://www.seyfarth.com/news-insights/5th-circuit-vacates-ftc-new-car-dealer-rule.html)

### TCPA Compliance and Lead Generation
- [TCPA Compliance 101 for Lead Generators 2026](https://www.leadgen-economy.com/blog/tcpa-compliance-guide-lead-generators/)
- [TCPA Compliant Lead Generation 2026 - LeadsHook](https://www.leadshook.com/blog/tcpa-lead-generation/)
- [Understanding FCC One-to-One Consent - ActiveProspect](https://activeprospect.com/blog/fcc-one-to-one-consent/)
- [TCPA Consent Management - ActiveProspect](https://activeprospect.com/blog/consent-management/)
- [TCPA Consent Language Best Practices - DynamicTracking](https://dynamictracking.com/dos-donts-consent-language/)
- [Building TCPA-Compliant Lead Gen Forms - ClickPoint](https://blog.clickpointsoftware.com/how-to-build-a-tcpa-compliant-lead-gen-form)
- [TCPA-Compliant Lead Distribution - ClickPoint](https://blog.clickpointsoftware.com/how-to-build-a-tcpa-compliant-lead-distribution-process)
- [2026 Guide to TCPA, CAN-SPAM & State Regulations - ClickPoint](https://blog.clickpointsoftware.com/tcpa-one-to-one-consent-can-spam-state-regulations)
- [TCPA Violation Penalties for Lead Gen - DynamicTracking](https://dynamictracking.com/penalties-tcpa-violations/)
- [FCC Lead Generation Ruling - Intellibright](https://www.intellibright.com/blog/fcc-lead-generation-tcpa/)
- [Eliminated One-to-One Consent Rule - McGuireWoods](https://www.mcguirewoods.com/client-resources/alerts/2025/1/delayed-one-to-one-consent-rule-gives-companies-reprieve-plus-other-tcpa-updates/)
- [Consent Obtaining Under New FCC Rules - Gryphon](https://gryphon.ai/how-to-obtain-consent-with-new-fcc-lead-generator-laws/)
- [Lead Generation Compliance Guide - ReadyMode](https://readymode.com/lead-generation-compliance/)

### State Privacy Laws
- [US State Privacy Legislation Tracker - IAPP](https://iapp.org/resources/article/us-state-privacy-legislation-tracker)
- [All Comprehensive Privacy Laws Effective 2026 - MultiState](https://www.multistate.us/insider/2026/2/4/all-of-the-comprehensive-privacy-laws-that-take-effect-in-2026)
- [Privacy Regulation of Auto Industry 2026 Part 1 - Nelson Mullins](https://www.nelsonmullins.com/insights/blogs/driving-forward-developments-in-transportation-law-and-innovation/all/privacy-regulation-of-auto-industry-to-accelerate-in-2026-part-1)
- [Privacy Regulation of Auto Industry 2026 Part 2 - National Law Review](https://natlawreview.com/article/privacy-regulation-auto-industry-accelerate-2026-part-2)
- [State Privacy Laws Taking Effect 2026 - Foster Swift](https://www.michiganitlaw.com/state-privacy-laws-taking-effect-in-2026)
- [State Privacy Law Deadline January 2026 - ComplyAuto](https://complyauto.com/state-privacy-law-deadline-january-1-2026/)
- [Five New State Privacy Laws January 2025 - ComplyAuto](https://complyauto.com/2025/01/06/privacy-update-five-new-state-privacy-laws-effective-in-january-2025/)
- [Data Privacy 2026: State Enforcement Takes Center Stage - Smith Law](https://www.smithlaw.com/newsroom/publications/data-privacy-in-2026-state-enforcement-takes-center-stage)
- [Privacy Laws Ring in the New Year 2026 - Baker Donelson](https://www.bakerdonelson.com/privacy-laws-ring-in-the-new-year-state-requirements-expand-across-the-us-in-2026)
- [Five Privacy Checkpoints 2026 - Wiley](https://www.wiley.law/alert-Five-Privacy-Checkpoints-to-Start-2026)
- [2025 State Privacy Roundup - Squire Patton Boggs](https://www.squirepattonboggs.com/insights/publications/2025-state-privacy-roundup-key-trends-and-california-developments-to-watch-in-2026/)
- [Privacy-First Lead Generation 2026 - LeadGen Economy](https://www.leadgen-economy.com/blog/privacy-first-lead-generation-regulatory-guide/)

### Texas SB 140
- [Texas SB 140 Analysis - Paul Hastings](https://www.paulhastings.com/insights/ph-privacy/marketing-texts-in-texas-sb-140-broadens-state-telemarketing-regulations)
- [Texas AG Confirms Opt-In SMS Exemption - Consumer Financial Services Law Monitor](https://www.consumerfinancialserviceslawmonitor.com/2025/11/texas-attorney-general-confirms-opt-in-sms-is-outside-registration-under-sb-140/)
- [Texas SB 140 Coverage - Morgan Lewis](https://www.morganlewis.com/pubs/2025/09/texas-telephone-solicitation-law-now-covers-text-messages)
- [Texas SB 140 Requirements - Vorys](https://www.vorys.com/publication-texas-sb-140-requirements)
- [Texas SB 140 Bill Text](https://capitol.texas.gov/tlodocs/89R/billtext/html/SB00140F.htm)

### Data Broker Registration
- [California Data Broker Registration - CPPA](https://cppa.ca.gov/data_brokers/)
- [California SB 361 Data Broker Requirements - Hunton](https://www.hunton.com/privacy-and-information-security-law/california-expands-data-broker-registration-requirements)
- [California Data Broker Deadline January 2026 - Greenberg Traurig](https://www.gtlaw-dataprivacydish.com/2026/01/california-data-broker-registration-deadline-arrives-jan-31-applying-to-more-businesses-than-ever/)
- [Data Broker Registries US 2025 - Monda](https://www.monda.ai/blog/data-broker-registries-in-the-us)
- [Data Broker Registration Laws - Hosch & Morris](https://www.hoschmorris.com/privacy-plus-news/data-broker-registration-laws)
- [Data Broker Non-Registration - EFF](https://www.eff.org/deeplinks/2025/06/why-are-hundreds-data-brokers-not-registering-states)
- [Understanding US Data Broker Regulations - TrustSuperset](https://www.trustsuperset.com/post/understanding-u-s-data-broker-registration-laws)

### California SB 37 and Automotive Enforcement
- [California SB 37 $100k Fine Risk for Lead Generators - Henson Legal](https://www.henson-legal.com/newsroom/californias-sb-37-a-new-100000-risk-for-legal-lead-generators)

### CAN-SPAM
- [CAN-SPAM Compliance Guide 2026 - IT Now Technologies](https://itnowtechnologies.com/comprehensive-guide-to-can-spam-compliance/)
- [Email Marketing Compliance 2026 - InfluenceFlow](https://influenceflow.io/resources/email-marketing-compliance-guidelines-complete-2026-update/)
- [CAN-SPAM Compliance Checklist - IT Now Technologies](https://itnowtechnologies.com/can-spam-act-email-compliance-checklist/)

### Do Not Call
- [TCPA Compliance for Lead Generators - LeadGen Economy](https://www.leadgen-economy.com/blog/tcpa-compliance-guide-lead-generators/)
- [Lead Generation Compliance Guide - ReadyMode](https://readymode.com/lead-generation-compliance/)

### Industry / Automotive
- [FTC Safeguards Rule - NADA](https://www.nada.org/safeguardsrule)
- [FTC Car Dealership Lead Generation Rules - LeadsBridge](https://leadsbridge.com/blog/ftc-car-dealerships/)
- [Post-CARS Rule Regulatory Activity - Mayer Brown](https://www.mayerbrown.com/en/insights/publications/2025/03/a-post-cars-rule-brake-not-so-fast-buckle-up-for-new-regulatory-activity-in-the-motor-vehicle-space)
