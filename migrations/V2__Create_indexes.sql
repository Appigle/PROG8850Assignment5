-- Scalar field indexes
CREATE INDEX idx_payment_value ON payments(payment_value);
CREATE INDEX idx_freight_value ON order_items(freight_value);

-- Full-text index for review text search
ALTER TABLE reviews ADD FULLTEXT(review_comment_message);
