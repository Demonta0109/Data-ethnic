# Erasure runbook — request DSAR-2026-014 (Camille Rousseau)

**Deadline:** one month from receipt (GDPR art. 12.3) → ______
**Owner of the decision:** ______   **DPO informed on:** ______   **Executed by (custodian):** ______

## 1. Identify the person (all accounts!)
| System / table | How we searched | IDs found |
|---|---|---|
| raw.customers | | |

## 2. Inventory of her data (use lineage from CTP 3 + your inventory from the CM 2 lab)
| Where | What | Action: DELETE / ANONYMISE / KEEP | Legal reason if kept | Rows |
|---|---|---|---|---|
| raw.customers | | | | |
| raw.orders | | | | |
| raw.payments | | | | |
| raw.support_tickets | | | | |
| raw.marketing_campaign_export | | | | |
| analytics.* / dbt DuckDB file | | | | |
| CSV files, exports, OpenRefine projects | | | | |
| Backups and logs | | | | |

## 3. Execution (SQL file name, date, who)

## 4. Verification (queries proving nothing is left, Presidio re-scan)

## 5. Answer to the customer (5 lines: what was deleted, what is kept and why, until when)
