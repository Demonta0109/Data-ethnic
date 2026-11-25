{% docs gross_revenue %}
**Gross revenue (EUR)** — total amount paid by the customer for an order, VAT included, shipping included, before refunds.
Owner: Head of Sales · Steward: Karim Benali · Status: approved (2026-11-10)
{% enddocs %}


{% docs active_customer %}
A customer account with at least one non-cancelled order in the last 12 months.

Rule: `last_order_date >= today - 12 months`, counting only orders with a status different from cancelled.

Owner: Head of Finance. This is the definition used in the board report and the annual accounts. For the 6-month view used by Sales, see the term recently active customer.
{% enddocs %}


{% docs net_revenue %}
The order total excluding VAT and after refunds. Shipping fees are included.

Formula: `(gross revenue - refunds) / (1 + VAT rate)`, rounded to 2 decimals.

Owner: Head of Finance. VAT is not company money, so it is never part of net revenue. For amounts including VAT, use the term net sales including VAT.
{% enddocs %}


{% docs churned_customer %}
A customer account that has already bought but has no non-cancelled order in the last 12 months.

Rule: at least one non-cancelled order ever AND `last_order_date < today - 12 months`.

Owner: Head of Sales. Used by the churn prediction model. It uses the same 12-month period as active customer, so a customer is never both.
{% enddocs %}


{% docs customer %}
A registered ShopFast customer account, identified by a `customer_id`.

One person may have several accounts, so the number of customers can be higher than the number of people.

Owner: Head of Sales.
{% enddocs %}


{% docs order %}
One purchase placed by a customer on a sales channel, identified by an `order_id`.

Duplicate order ids are removed and the first occurrence is kept.

Owner: Head of Sales.
{% enddocs %}


{% docs recently_active_customer %}
A customer account with at least one non-cancelled order in the last 6 months.

Rule: `last_order_date >= today - 6 months`, counting only orders with a status different from cancelled.

Owner: Head of Sales. Used for the daily Sales dashboard and marketing campaigns. It is a separate term from active customer, which uses 12 months.
{% enddocs %}
