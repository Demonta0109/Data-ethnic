"""CTP 4 - automated access tests. Each line = one rule of the access policy.
Run:  python test_access.py   (after 00_setup_analytics.sql and your rbac script)
"""
import os
import psycopg2

PORT = int(os.environ.get("SHOPFAST_PG_PORT", "5432"))
TESTS = [  # (user, query, should_work, rule)
    ("ana", "select count(*) from analytics.v_customers_masked", True, "Analyst reads masked customers"),
    ("ana", "select email from analytics.customers limit 1", False, "Analyst cannot read real emails"),
    ("ana", "select count(*) from raw.customers", False, "Analyst cannot read raw data"),
    ("mkt", "select count(*) from analytics.v_marketing_audience", True, "Marketing reads its audience"),
    ("mkt", "select count(*) from analytics.orders", False, "Marketing cannot read orders"),
    ("ds", "select count(*) from analytics.v_ds_churn_features", True, "Data science reads pseudonymised features"),
    ("ds", "select count(*) from analytics.v_customers_masked", False, "Data science has no customer view"),
    ("sup_fr", "select count(*) from analytics.customers where country_code <> 'FR'", True, "Support FR query runs..."),
    ("sup_fr", "select email from analytics.customers limit 1", False, "Support FR cannot read emails"),
]
ok_all = True
for user, q, should, rule in TESTS:
    try:
        con = psycopg2.connect(host="localhost", port=PORT, dbname="shopfast", user=user, password="training")
        cur = con.cursor(); cur.execute(q); res = cur.fetchone(); con.close(); worked = True
    except Exception as e:
        worked, res = False, str(e).splitlines()[0][:60]
    passed = worked == should
    if user == "sup_fr" and worked and "<> 'FR'" in q:
        passed = res[0] == 0          # RLS: rows of other countries must be invisible
        rule += " ...but sees 0 non-French customers (RLS)"
    ok_all &= passed
    print(f"{'PASS' if passed else 'FAIL'}  {user:<7} {rule:<55} -> {res}")
print("\nACCESS POLICY:", "ALL TESTS PASS" if ok_all else "SOME TESTS FAIL")
