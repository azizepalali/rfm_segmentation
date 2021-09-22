#  Customer Segmentation with RFM

# What is RFM Analysis?
RFM is a customer segmentation model that allows you to segment your customers based on their past purchasing behavior.It is a score that consists of the initials of the words Recency, Frequency, Monetary, and is formed by combining these three metrics after calculating them.

- Recency: When was the last time the customer made a purchase? A customer who has made a recent purchase will be more receptive to sent messages.
- Frequency: How often does the customer buy? Frequent shopping shows that the customer is satisfied with the service received.
- Monetary: How much total did the customer spend on his purchases? Monetary grading helps distinguish high-stakes shoppers from low-shoppers.

## Variables

- InvoiceNo: Invoice number. Nominal. A 6-digit integral number uniquely assigned to each transaction. If this code starts with the letter 'c', it indicates a cancellation.
- StockCode: Product (item) code. Nominal. A 5-digit integral number uniquely assigned to each distinct product.
- Description: Product (item) name. Nominal.
- Quantity: The quantities of each product (item) per transaction. Numeric.
- InvoiceDate: Invice date and time. Numeric. The day and time when a transaction was generated.
- UnitPrice: Unit price. Numeric. Product price per unit in sterling (Â£).
- CustomerID: Customer number. Nominal. A 5-digit integral number uniquely assigned to each customer.
- Country: Country name. Nominal. The name of the country where a customer resides.


Acquiring a new customer is 5 to 25 times more expensive than retaining an existing one. Based on this information; A strategy specific to each segment should be determined before existing customers become churn.
