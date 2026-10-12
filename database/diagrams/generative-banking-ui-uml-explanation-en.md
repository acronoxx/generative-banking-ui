# UML Class Diagram — Generative Banking UI

## 1. Overview

This document explains the classes in the Generative Banking UI UML diagram, their main attributes, and the relationships between them. The classes are grouped by functional area.

## 2. Customers & Access

### `Customer`
Represents a bank customer.
- `id`: unique customer identifier.
- `advisor_id`: identifier of the assigned advisor, when applicable.
- `first_name`, `last_name`: customer's name.
- `email`, `phone`: contact details.
- `created_at`: date and time the customer record was created.

**Relationships:** A customer may be assigned to one advisor and may have multiple accounts, product subscriptions, beneficiaries, documents, document requests, conversations, support requests, disputes, budgets, notifications, customer-offer records, referrals, and insurance policies.

### `Advisor`
Represents a bank advisor.
- `id`: unique advisor identifier.
- `name`, `email`, `phone`: advisor's details.
- `specialization`: advisor's area of expertise.
- `status`: advisor's current status.

**Relationships:** An advisor may be assigned to multiple customers. An advisor may also be associated with application users, conversations, and support requests.

### `User`
Represents an application user.
- `id`: unique user identifier.
- `username`: user's login name.
- `app_pin_hash`: hashed application PIN.
- `app_pin_failed_attempts`: number of failed PIN attempts.
- `app_pin_locked_until`: time until which the account remains locked, if applicable.
- `role`: user's role in the application.
- `customer_id`: associated customer, when the user is a customer.
- `advisor_id`: associated advisor, when the user is an advisor.
- `status`: account status.
- `created_at`: account creation date.

**Relationships:** A user may be associated with a customer or an advisor. A user may have multiple sessions and audit-log entries, and may be recorded as the user who changed a card limit or performed a cheque operation.

### `UserSession`
Represents an authenticated application session.
- `id`: unique session identifier.
- `user_id`: user associated with the session.
- `session_token_hash`: hash representing the session token.
- `created_at`: session creation time.
- `expires_at`: session expiration time.
- `revoked_at`: time the session was revoked, if applicable.

**Relationships:** Each session belongs to one user. A user can have multiple sessions.

### `AuditLog`
Represents a record of an action performed in the application.
- `id`: unique log-entry identifier.
- `user_id`: user associated with the action, if known.
- `action`: action name.
- `entity_type`: type of object affected.
- `entity_id`: identifier of the affected object.
- `details`: additional information about the action.
- `created_at`: time the action was recorded.

**Relationships:** An audit-log entry may be associated with one user. A user may have multiple audit-log entries.

## 3. Accounts & Transactions

### `Account`
Represents a bank account belonging to a customer.
- `id`: unique account identifier.
- `customer_id`: owner of the account.
- `account_number`: account number.
- `iban`, `bic`: international account and bank identifiers.
- `bank_code`, `branch_code`, `rib_key`: additional banking identifiers.
- `account_type`: type of account.
- `balance`: account balance.
- `currency`: account currency.
- `status`: account status.
- `created_at`: account creation time.

**Relationships:** Each account belongs to one customer. An account may have multiple transactions, cards, cheque books, cheques, scheduled transfers, and transfer simulations as a source or destination account.

### `Category`
Represents a category used to classify transactions and budgets.
- `id`: unique category identifier.
- `name`: category name.
- `description`: explanation of the category.

**Relationships:** A category may be associated with multiple bank transactions and budgets.

### `BankTransaction`
Represents a transaction associated with a bank account.
- `id`: unique transaction identifier.
- `account_id`: account associated with the transaction.
- `category_id`: transaction category, when assigned.
- `card_id`: card associated with the transaction, when applicable.
- `type`: transaction type.
- `amount`: transaction amount.
- `currency`: transaction currency.
- `description`: transaction description.
- `merchant`: merchant or counterparty name.
- `reference`: transaction reference.
- `transaction_date`: date of the transaction.
- `booked_at`: date and time the transaction was booked.
- `status`: transaction status.

**Relationships:** Each transaction belongs to one account. It may be associated with one category and one card. A transaction may have multiple fees and may be referenced by disputes.

### `TransactionFee`
Represents a fee associated with a transaction.
- `id`: unique fee identifier.
- `transaction_id`: related transaction.
- `amount`: fee amount.
- `currency`: fee currency.
- `reason`: reason for the fee.
- `status`: fee status.

**Relationships:** Each fee belongs to one transaction. A transaction may have zero or multiple fees.

### `Beneficiary`
Represents a recipient saved by a customer for transfers.
- `id`: unique beneficiary identifier.
- `customer_id`: customer who saved the beneficiary.
- `name`: beneficiary name.
- `iban`, `bic`: beneficiary's banking details.
- `status`: beneficiary status.
- `created_at`: creation time.
- `validated_at`: validation time, if applicable.

**Relationships:** Each beneficiary belongs to one customer. A customer may have multiple beneficiaries. A beneficiary may be used by multiple scheduled transfers or transfer simulations.

### `TransferSimulation`
Represents a simulated transfer.
- `id`: unique simulation identifier.
- `source_account_id`: account from which the transfer would be made.
- `destination_account_id`: destination account for an internal transfer, if applicable.
- `beneficiary_id`: beneficiary for an external transfer, if applicable.
- `amount`: proposed transfer amount.
- `currency`: transfer currency.
- `reason`: transfer description or reason.
- `status`: simulation status.
- `created_at`: simulation creation time.
- `confirmed_at`: confirmation time, if applicable.

**Relationships:** Each simulation has one source account. It may reference a destination account or a beneficiary. The source and destination account references both point to `Account`.

### `ScheduledTransfer`
Represents a recurring or scheduled transfer.
- `id`: unique scheduled-transfer identifier.
- `account_id`: source account.
- `beneficiary_id`: recipient.
- `amount`: transfer amount.
- `currency`: transfer currency.
- `frequency`: recurrence frequency.
- `next_execution_at`: next planned execution time.
- `end_date`: end date, if any.
- `status`: scheduled-transfer status.
- `created_at`: creation time.

**Relationships:** Each scheduled transfer is linked to one source account and one beneficiary. An account or beneficiary may be linked to multiple scheduled transfers.

## 4. Products & Cards

### `BankingProduct`
Represents a banking product offered by the bank.
- `id`: unique product identifier.
- `name`: product name.
- `product_type`: type of product.
- `description`: product description.
- `monthly_fee`: monthly fee, if applicable.
- `status`: product status.

**Relationships:** A product may be associated with multiple customer subscriptions.

### `Subscription`
Represents a customer's subscription to a banking product.
- `id`: unique subscription identifier.
- `customer_id`: subscribing customer.
- `product_id`: subscribed product.
- `status`: subscription status.
- `start_date`: subscription start date.
- `end_date`: subscription end date, if applicable.

**Relationships:** Each subscription belongs to one customer and one banking product. A customer and a product may each be linked to multiple subscriptions.

### `Card`
Represents a payment card linked to an account.
- `id`: unique card identifier.
- `account_id`: linked bank account.
- `subscription_id`: related subscription, if applicable.
- `card_token`: technical card token.
- `card_number_test`: test card number.
- `last_four_digits`: last four digits displayed for identification.
- `expiry_month`, `expiry_year`: expiration month and year.
- `card_type`: card category.
- `physical_type`: physical or virtual form.
- `daily_payment_limit`, `monthly_payment_limit`: payment limits.
- `daily_withdrawal_limit`: withdrawal limit.
- `currency`: card currency.
- `status`: card status.
- `valid_from`: start of validity.
- `expires_at`: expiration date.
- `created_at`: creation time.

**Relationships:** Each card belongs to one account and may be associated with one subscription. A card may be associated with multiple transactions, one PIN credential, and multiple card-limit history records.

### `CardPinCredential`
Represents the card PIN credential used in the demonstration.
- `id`: unique credential identifier.
- `card_id`: associated card; unique in this model.
- `encrypted_pin`: encrypted PIN value.
- `encryption_key_id`: identifier of the encryption key.
- `pin_status`: PIN status.
- `failed_attempts`: number of failed attempts.
- `locked_until`: lock expiration time, if applicable.
- `created_at`, `updated_at`: creation and last-update times.

**Relationships:** Each credential belongs to one card. Each card can have at most one credential in this model.

### `CardLimitHistory`
Records changes to a card's limits.
- `id`: unique history-entry identifier.
- `card_id`: card whose limit changed.
- `limit_type`: type of limit changed.
- `old_limit`, `new_limit`: previous and new values.
- `changed_by_user_id`: user who made the change, if known.
- `changed_at`: time of change.
- `reason`: reason for the change.

**Relationships:** Each history entry belongs to one card and may reference the user who changed the limit. A card may have multiple history entries.

## 5. Cheques

### `ChequeBook`
Represents a cheque book associated with an account.
- `id`: unique cheque-book identifier.
- `account_id`: associated account.
- `first_cheque_number`, `last_cheque_number`: number range in the book.
- `requested_at`: request time.
- `issued_at`: issue time.
- `received_at`: receipt time.
- `status`: cheque-book status.

**Relationships:** Each cheque book belongs to one account and may contain multiple cheques.

### `Cheque`
Represents an individual cheque.
- `id`: unique cheque identifier.
- `account_id`: associated account.
- `cheque_book_id`: associated cheque book, if applicable.
- `cheque_number`: cheque number.
- `amount`: cheque amount.
- `currency`: cheque currency.
- `payee_name`: payee.
- `issue_date`: issue date.
- `presented_at`: presentation time.
- `paid_at`: payment time.
- `status`: cheque status.

**Relationships:** Each cheque belongs to one account and may be linked to one cheque book. A cheque may have multiple recorded operations.

### `ChequeOperation`
Represents an operation performed on a cheque.
- `id`: unique operation identifier.
- `cheque_id`: affected cheque.
- `operation_type`: operation type.
- `operation_date`: operation date and time.
- `reason`: reason for the operation.
- `status`: operation status.
- `user_id`: user associated with the operation, if applicable.

**Relationships:** Each operation belongs to one cheque and may reference one user. A cheque may have multiple operations.

## 6. Offers & Referrals

### `Offer`
Represents an offer available from the bank.
- `id`: unique offer identifier.
- `title`: offer title.
- `description`: offer description.
- `offer_type`: offer category.
- `start_date`, `end_date`: validity period.
- `reward_amount`, `reward_currency`: reward amount and currency, if applicable.
- `eligibility_rules`: eligibility information.
- `terms_and_conditions`: offer terms.
- `status`: offer status.

**Relationships:** An offer may be linked to multiple customer-offer records and referrals.

### `CustomerOffer`
Represents a customer's participation in an offer.
- `id`: unique record identifier.
- `customer_id`: participating customer.
- `offer_id`: related offer.
- `status`: participation status.
- `claimed_at`: claim time.
- `completed_at`: completion time.
- `rewarded_at`: reward time.

**Relationships:** Each record links one customer to one offer. A customer and an offer may each have multiple customer-offer records.

### `Referral`
Represents a customer referral.
- `id`: unique referral identifier.
- `offer_id`: related offer, if applicable.
- `referrer_customer_id`: customer who made the referral.
- `referred_customer_id`: referred customer, if known.
- `referral_code`: referral code.
- `status`: referral status.
- `created_at`: creation time.
- `completed_at`: completion time.
- `rewarded_at`: reward time.

**Relationships:** Each referral has one referrer and may be associated with an offer and a referred customer. Both customer references point to `Customer`.

## 7. Documents

### `CustomerDocument`
Represents a document associated with a customer.
- `id`: unique document identifier.
- `customer_id`: document owner.
- `account_id`: related account, if applicable.
- `subscription_id`: related subscription, if applicable.
- `document_type`: document category.
- `title`: document title.
- `file_reference`: reference to the stored file.
- `mime_type`: file media type.
- `issued_at`: issue date.
- `expires_at`: expiration date, if applicable.
- `status`: document status.

**Relationships:** Each document belongs to one customer and may be associated with an account or subscription.

### `DocumentRequest`
Represents a request for a document or document-related processing.
- `id`: unique request identifier.
- `customer_id`: customer who made the request.
- `document_type`: requested document type.
- `reason`: request reason.
- `requested_at`: request time.
- `due_date`: target date.
- `submitted_at`: submission time, if applicable.
- `reviewed_at`: review time, if applicable.
- `status`: request status.
- `reviewed_by_user_id`: user who reviewed it, if applicable.

**Relationships:** Each request belongs to one customer and may reference the user who reviewed it. A customer may have multiple document requests.

## 8. Insurance

### `InsuranceProduct`
Represents an insurance product.
- `id`: unique product identifier.
- `name`: product name.
- `insurance_type`: type of insurance.
- `insurer_name`: insurer name.
- `description`: product description.
- `eligibility_rules`: eligibility information.
- `status`: product status.

**Relationships:** An insurance product may have multiple policies and coverage definitions.

### `InsurancePolicy`
Represents an insurance contract held by a customer.
- `id`: unique policy identifier.
- `customer_id`: policyholder.
- `insurance_product_id`: related insurance product.
- `policy_number`: policy reference.
- `start_date`, `end_date`: policy period.
- `premium_amount`: premium amount.
- `payment_frequency`: premium payment frequency.
- `status`: policy status.

**Relationships:** Each policy belongs to one customer and one insurance product. A policy may have multiple claims.

### `InsuranceCoverage`
Represents a coverage included in an insurance product.
- `id`: unique coverage identifier.
- `insurance_product_id`: related insurance product.
- `name`: coverage name.
- `description`: coverage description.
- `coverage_limit`: maximum covered amount.
- `deductible`: deductible amount.
- `waiting_period_days`: waiting period.
- `exclusions`: exclusions.

**Relationships:** Each coverage belongs to one insurance product. A product may define multiple coverages.

### `InsuranceClaim`
Represents a claim made under an insurance policy.
- `id`: unique claim identifier.
- `policy_id`: related policy.
- `claim_date`: claim date.
- `description`: claim description.
- `claimed_amount`: amount claimed.
- `approved_amount`: amount approved, if any.
- `status`: claim status.
- `resolved_at`: resolution time, if applicable.

**Relationships:** Each claim belongs to one insurance policy. A policy may have multiple claims.

## 9. Messaging & Support

### `Conversation`
Represents a conversation between a customer and the bank.
- `id`: unique conversation identifier.
- `customer_id`: customer who owns the conversation.
- `advisor_id`: assigned advisor, if any.
- `subject`: conversation subject.
- `status`: conversation status.
- `created_at`: creation time.
- `closed_at`: closing time, if applicable.

**Relationships:** Each conversation belongs to one customer, may be assigned to one advisor, and contains multiple messages.

### `Message`
Represents a message in a conversation.
- `id`: unique message identifier.
- `conversation_id`: containing conversation.
- `sender_type`: type of sender.
- `sender_id`: identifier of the sender.
- `content`: message text.
- `sent_at`: sending time.
- `read_at`: read time, if applicable.

**Relationships:** Each message belongs to one conversation. A conversation may contain multiple messages. The meaning of `sender_id` depends on `sender_type`.

### `SupportRequest`
Represents a customer support request.
- `id`: unique request identifier.
- `customer_id`: customer who opened the request.
- `advisor_id`: assigned advisor, if any.
- `category`: request category.
- `description`: request details.
- `priority`: priority level.
- `status`: request status.
- `created_at`: creation time.
- `resolved_at`: resolution time, if applicable.

**Relationships:** Each support request belongs to one customer and may be assigned to one advisor.

### `Dispute`
Represents a dispute related to a bank transaction.
- `id`: unique dispute identifier.
- `customer_id`: customer who opened the dispute.
- `transaction_id`: disputed transaction.
- `reason`: dispute reason.
- `description`: dispute details.
- `status`: dispute status.
- `opened_at`: opening time.
- `resolved_at`: resolution time, if applicable.
- `resolution`: resolution details.

**Relationships:** Each dispute belongs to one customer and references one transaction. A transaction may be associated with multiple disputes if the model allows it.

## 10. Budget & Notifications

### `Budget`
Represents a spending budget for a customer and category.
- `id`: unique budget identifier.
- `customer_id`: budget owner.
- `category_id`: spending category.
- `monthly_limit`: budget limit.
- `currency`: budget currency.
- `period_start`, `period_end`: budget period.

**Relationships:** Each budget belongs to one customer and one category. A customer and a category may each be associated with multiple budgets.

### `Notification`
Represents a notification addressed to a customer.
- `id`: unique notification identifier.
- `customer_id`: recipient.
- `notification_type`: notification category.
- `title`: notification title.
- `message`: notification content.
- `channel`: delivery channel.
- `status`: notification status.
- `created_at`: creation time.
- `read_at`: read time, if applicable.

**Relationships:** Each notification belongs to one customer. A customer may have multiple notifications.

## 11. Relationship summary

- **Customer — Account:** one customer can have multiple accounts; each account belongs to one customer.
- **Customer — Advisor:** an advisor may manage multiple customers; a customer may be assigned to one advisor.
- **Account — BankTransaction:** one account can have many transactions; each transaction belongs to one account.
- **BankTransaction — TransactionFee:** one transaction can have multiple fees.
- **Account — Card:** one account can be linked to multiple cards; each card belongs to one account.
- **Card — CardPinCredential:** a card has at most one PIN credential in this model.
- **Card — CardLimitHistory:** one card can have many limit-change records.
- **Customer — Beneficiary:** one customer can save multiple beneficiaries.
- **Customer — Subscription — BankingProduct:** subscriptions connect customers with banking products.
- **Account — ChequeBook — Cheque:** accounts can have cheque books, and cheque books can contain multiple cheques.
- **Customer — Offer — CustomerOffer:** the association class records each customer's participation in an offer.
- **Customer — InsurancePolicy — InsuranceProduct:** a policy connects a customer to an insurance product.
- **InsuranceProduct — InsuranceCoverage:** one product can define multiple coverages.
- **InsurancePolicy — InsuranceClaim:** one policy can have multiple claims.
- **Customer — Conversation — Message:** a customer can have multiple conversations, each containing multiple messages.
- **Customer — Budget — Category:** budgets connect customers with spending categories.
- **Customer — Notification:** one customer can receive multiple notifications.

