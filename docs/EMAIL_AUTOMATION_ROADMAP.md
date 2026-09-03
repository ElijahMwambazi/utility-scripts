# Email Automation Roadmap

This roadmap tracks practical email utilities for personal, workplace, and business use. Scripts should be small, focused, documented, safe by default, and reusable across environments where possible.

## Principles

- Prefer Microsoft Graph or provider APIs over desktop UI automation.
- Never commit credentials, tokens, recipient lists, or real customer data.
- Include dry-run or preview modes for scripts that send or modify email.
- Log actions and failures clearly.
- Avoid exposing recipient addresses through CC/BCC when individual delivery is more appropriate.
- Add rate limiting, duplicate protection, and retry handling where relevant.
- Treat compliance, unsubscribe preferences, and sensitive data handling as first-class concerns.

## Roadmap

### Sending and mail merge

- [x] Bulk Personalized Sender — sends one individual email per recipient with merge fields.
- [ ] Attachment Mail Merge — sends recipient-specific attachments.
- [ ] Invoice/Statement Sender — matches customers to invoices/statements and sends them individually.
- [ ] Certificate/Document Distributor — distributes certificates, policy documents, payslips, reports, and similar files.
- [ ] Recurring Report Mailer — sends scheduled daily/weekly/monthly reports.
- [ ] Approval Request Sender — sends structured approval requests with references and links.
- [ ] Meeting Follow-Up Sender — sends post-meeting notes, actions, owners, and due dates.
- [ ] Email Template CLI — selects templates, fills fields, previews, and sends.
- [ ] Signature Manager — manages reusable and consistent signatures.
- [ ] Large Attachment Handler — detects oversized attachments and substitutes OneDrive/SharePoint links.

### Follow-up and response tracking

- [ ] Follow-Up Scheduler — prepares or sends follow-ups after a chosen delay.
- [ ] Reply Reminder — flags messages received but not answered within a chosen period.
- [ ] Awaiting-Reply Tracker — tracks sent emails that have not received responses.
- [ ] Quotation Follow-Up Tool — tracks quotations and follow-up intervals.

### Inbox management

- [ ] Inbox Rules Generator — creates folders/categories and classification rules.
- [ ] Daily Inbox Digest — summarizes unread and important mail.
- [ ] Email-to-Task — converts selected emails into task-system items.
- [ ] Email Attachment Downloader — downloads attachments that match configurable rules.
- [ ] Attachment Extractor + Renamer — saves and renames attachments using metadata.
- [ ] Email Search/Report Tool — searches mail and produces structured reports.
- [ ] Email Backup/Exporter — exports selected messages for archival or portability.
- [ ] Out-of-Office Manager — manages scheduled internal/external automatic replies.

### Contacts and recipient hygiene

- [ ] Contact Extractor — extracts legitimate contacts from mailbox data.
- [ ] Contact Deduplicator — normalizes and deduplicates contact records.
- [ ] Mailing List Cleaner — validates formatting and removes duplicates before sending.
- [ ] Bounce/Invalid Address Processor — identifies failed or invalid addresses.
- [ ] Unsubscribe/Preference Processor — records opt-outs and excludes them from future sends.

### Business workflows

- [ ] Shared Mailbox Router — classifies and routes messages from shared mailboxes.
- [ ] Customer Service Auto-Triage — categorizes complaints, enquiries, cancellations, claims, quotations, and similar mail.
- [ ] Application Intake Processor — captures applicant messages and attachments and acknowledges receipt.

### Safety and compliance

- [ ] Sensitive Data Detector — checks outgoing drafts/attachments for sensitive identifiers.
- [ ] Wrong-Recipient Guard — checks recipient/document mismatches before sending.

## Suggested implementation order

1. Follow-Up Scheduler
2. Attachment Mail Merge
3. Daily Inbox Digest
4. Email Attachment Downloader
5. Awaiting-Reply Tracker
6. Mailing List Cleaner
7. Invoice/Statement Sender
8. Application Intake Processor
9. Shared Mailbox Router
10. Sensitive Data Detector
11. Wrong-Recipient Guard
12. Remaining utilities by demand

## Definition of done for each utility

A utility is considered complete when it has:

- implementation code
- a focused README
- example configuration/input files
- dependency/install instructions
- dry-run or preview support where appropriate
- error handling and useful logs
- no embedded secrets or personal data
- a minimal test or validation path
- documented limitations and permissions
