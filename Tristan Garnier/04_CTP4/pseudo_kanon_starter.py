"""CTP 4 - Exercise 3 STARTER: pseudonymisation is not anonymisation.
Part A: an UNSALTED hash of an email can be reversed by anyone who has a list of emails.
Part B: k-anonymity of a 'harmless' export (postal code + birth year + tier).
"""
import hashlib, hmac
import pandas as pd

c = pd.read_csv("../shopfast-kit/data/customers.csv", dtype=str).drop_duplicates()
c["email"] = c["email"].str.strip().str.lower()
c = c[c["email"].notna()]

# ---------- Part A ----------
c["email_sha256"] = c["email"].map(lambda e: hashlib.sha256(e.encode()).hexdigest())          # what a junior engineer ships
# TODO A1: create c["email_hmac"] with hmac.new(SECRET, email, hashlib.sha256) - SECRET is a key kept outside Git

leaked = pd.read_csv("../shopfast-kit/data/marketing_campaign_export.csv", dtype=str)  # attacker has a list of emails
lookup = {hashlib.sha256(e.strip().lower().encode()).hexdigest(): e for e in leaked["email"].dropna()}
reid_plain = c["email_sha256"].map(lookup).notna().sum()
print(f"Part A - re-identified with a list of {len(lookup)} emails: plain SHA-256 = {reid_plain}")
# TODO A2: try the same attack on email_hmac. How many people can the attacker re-identify now? Why?

# ---------- Part B ----------
import re
c["birth_year"] = c["birth_date"].map(lambda v: int(re.search(r"(\d{4})", str(v)).group(1)) if re.search(r"(\d{4})", str(v)) else None)
qi = ["postal_code", "birth_year", "loyalty_tier"]          # quasi-identifiers of a 'harmless' export
k = c.groupby(qi)["customer_id"].transform("count")       # k = size of the group each row belongs to
print(f"Part B - {int((k == 1).sum())} of {len(c)} rows are unique (k=1) on {qi}")
# TODO B1: generalise - postal code -> 2-digit department, birth year -> decade. Recompute k. Enough?
# TODO B2: generalise more (country instead of department) until k >= 5 for most rows
# TODO B3: suppress (remove) the remaining rows with k < 5. How many rows did you lose? Is the export still useful?
