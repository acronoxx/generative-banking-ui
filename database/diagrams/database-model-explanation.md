# Generative Banking UI — Database Model

## 1. Overview

This document explains the database model for **Generative Banking UI**, a banking interface enhanced by an AI agent. The model supports account consultation, transaction analysis, transfer simulations, banking products, customer budgets, support requests, and communication between customers and their bank advisors.

The database is intended for a prototype using synthetic data. The AI agent does not access the database directly: it calls authorized backend functions exposed by the FastAPI application, which validates requests and queries PostgreSQL.

## 2. Entity-relationship diagram

The PlantUML source for the model is stored in `database/diagrams/database-model.puml`.

The diagram contains the following functional areas:

- Customer and advisor management
- Accounts, transactions, and categories
- Transfer simulations
- Banking products and subscriptions
- Advisor messaging
- Support requests
- Personal budgets

## 3. Keys and relationships

- **PK (Primary Key):** uniquely identifies a record in a table.
- **FK (Foreign Key):** references a record in another table.
- **Cardinality:** describes how many records can participate in a relationship. For example, `1` means exactly one, while `0..*` means zero or many.

The relationships shown in the UML diagram express the intended data model. They should also be enforced in the PostgreSQL schema through primary-key and foreign-key constraints.

## 4. Entities

### 4.1 Customer

Stores the bank customer’s basic profile:

- `id` (`PK`): unique customer identifier.
- `advisor_id` (`FK`): references the assigned advisor, when one is assigned.
- `first_name`, `last_name`: customer’s name.
- `email`, `phone`: contact details.
- `created_at`: record creation timestamp.

A customer can own multiple accounts, open conversations, submit support requests, subscribe to banking products, and define budgets.

### 4.2 Advisor

Stores the bank advisor’s profile:

- `id` (`PK`): unique advisor identifier.
- `first_name`, `last_name`: advisor’s name.
- `email`, `phone`: professional contact details.
- `specialization`: area of expertise.
- `status`: advisor’s availability or account status.

An advisor can be assigned to multiple customers, handle conversations, and be assigned support requests.

### 4.3 Account

Represents a customer’s bank account:

- `id` (`PK`): unique account identifier.
- `customer_id` (`FK`): references the account owner in `Customer`.
- `account_number`: account number displayed by the application.
- `account_type`: account type, such as current or savings.
- `balance`: account balance, represented with a decimal type.
- `currency`: currency code, such as EUR.
- `status`: account status.
- `created_at`: account creation timestamp.

Each account belongs to one customer and can have multiple transactions. It can also be referenced as the source or destination of transfer simulations.

### 4.4 BankTransaction

Stores a transaction associated with an account:

- `id` (`PK`): unique transaction identifier.
- `account_id` (`FK`): references the account.
- `category_id` (`FK`): references the transaction category.
- `type`: transaction type, for example debit or credit.
- `amount`, `currency`: amount and currency.
- `description`, `merchant`: transaction description and merchant, if applicable.
- `transaction_date`: date and time of the transaction.
- `status`: transaction status.

Transactions support account history, category-based spending analysis, and comparisons between periods. The model should define a consistent convention for the sign of `amount` and the meaning of `type`.

### 4.5 Category

Groups transactions into categories, for example groceries, transport, housing, or restaurants:

- `id` (`PK`): unique category identifier.
- `name`: category name.
- `description`: optional explanation.

A category can classify multiple transactions and can be used as the target of multiple customer budgets.

### 4.6 TransferSimulation

Stores a proposed transfer between two accounts without executing a real bank transfer:

- `id` (`PK`): unique simulation identifier.
- `source_account_id` (`FK`): source account.
- `destination_account_id` (`FK`): destination account.
- `amount`, `currency`: proposed transfer amount.
- `reason`: optional transfer reason.
- `status`: simulation state, such as draft, validated, cancelled, or expired.
- `created_at`: simulation creation timestamp.
- `confirmed_at`: optional timestamp for the customer’s confirmation of the simulation.

The source and destination are both references to `Account`. In this prototype, creating or confirming a simulation must not change account balances or create a real payment.

### 4.7 BankingProduct

Represents a product that the bank offers:

- `id` (`PK`): unique product identifier.
- `name`: product name.
- `product_type`: product family, such as savings, card, or loan.
- `description`: product information.
- `monthly_fee`: monthly fee, if applicable.
- `status`: product availability or status.

### 4.8 Subscription

Links a customer to a banking product they have subscribed to:

- `id` (`PK`): unique subscription identifier.
- `customer_id` (`FK`): references the customer.
- `product_id` (`FK`): references the banking product.
- `status`: subscription status.
- `start_date`, `end_date`: subscription period.

This association allows one customer to subscribe to several products and one product to be subscribed to by multiple customers.

### 4.9 Conversation

Represents a message thread between a customer and an advisor:

- `id` (`PK`): unique conversation identifier.
- `customer_id` (`FK`): references the customer who opened it.
- `advisor_id` (`FK`): references the advisor handling it.
- `subject`: conversation subject.
- `status`: state, such as open, pending, or closed.
- `created_at`: creation timestamp.
- `closed_at`: optional closing timestamp.

A customer can open multiple conversations, and an advisor can handle multiple conversations. Each conversation belongs to one customer and one advisor in this model.

### 4.10 Message

Stores an individual message within a conversation:

- `id` (`PK`): unique message identifier.
- `conversation_id` (`FK`): references the conversation.
- `sender_type`: indicates whether the sender is a customer or an advisor.
- `sender_id`: identifier of the sender.
- `content`: message text.
- `sent_at`: send timestamp.
- `read_at`: optional timestamp indicating when the message was read.

Messages belong to one conversation, and a conversation can contain multiple messages. **Design note:** `sender_id` is not a conventional foreign key in the current model because the sender may belong to either `Customer` or `Advisor`. A production-ready alternative is a shared `User` table referenced by `Message.sender_id`, with customer and advisor profiles linked to that user.

### 4.11 SupportRequest

Tracks a customer’s support request, question, or complaint:

- `id` (`PK`): unique request identifier.
- `customer_id` (`FK`): references the customer submitting the request.
- `advisor_id` (`FK`): references the assigned advisor, if any.
- `category`: request category.
- `description`: request details.
- `priority`: priority level.
- `status`: workflow state, such as new, in progress, resolved, or closed.
- `created_at`: creation timestamp.
- `resolved_at`: optional resolution timestamp.

A customer can submit multiple requests. Each request may be assigned to one advisor or remain unassigned.

### 4.12 Budget

Stores a customer-defined spending limit for a category over a period:

- `id` (`PK`): unique budget identifier.
- `customer_id` (`FK`): references the customer.
- `category_id` (`FK`): references the target category.
- `monthly_limit`: spending limit.
- `currency`: budget currency.
- `period_start`, `period_end`: period covered by the budget.

The application can compare categorized transactions with these limits to estimate remaining budgets. The period fields also allow budgets to be associated with specific dates.

## 5. Main user journeys supported

### View accounts and balances
The backend retrieves the accounts belonging to the authenticated customer and returns their balances and statuses.

### Review transactions and spending
The backend retrieves transactions for a selected account or period. It can group transactions by category and compare spending over time.

### Simulate a transfer
The customer selects a source account, a destination account, an amount, and optionally a reason. The backend validates the request and records a simulation. No real transfer is performed by this model.

### Contact a bank advisor
The customer opens a conversation, writes a message, and can review the message history. The advisor can respond and update the conversation status. A support request can be created separately when the issue needs explicit tracking.

### Explore products and subscriptions
The customer views available banking products and their current subscriptions.

### Manage a budget
The customer defines a spending limit for a category and period. The application compares this limit with categorized transactions and displays progress or alerts.

## 6. How the AI agent uses the model

The AI agent is not represented as a database table. It interacts with banking data through backend functions, for example:

- `get_accounts()`
- `get_transactions(account_id, period)`
- `get_spending_by_category(period)`
- `simulate_transfer(source_account_id, destination_account_id, amount)`
- `create_conversation(subject)`
- `send_message(conversation_id, content)`
- `get_banking_products()`
- `get_budgets()`

These are illustrative function names, not implemented API contracts. The backend must authenticate the customer, authorize access to every requested resource, validate inputs, and log sensitive actions. The model should use synthetic data during development.

## 7. Implementation notes and recommended refinements

Before implementing the PostgreSQL schema, consider the following:

1. **Foreign keys and cardinalities:** ensure the SQL constraints match the relationships in the UML. In particular, `Customer.advisor_id` is nullable if assigning an advisor is optional.
2. **Message sender integrity:** consider introducing a shared `User` table so that `Message.sender_id` can be protected by a real foreign-key constraint.
3. **Money types:** use a fixed-precision decimal type such as `NUMERIC(18,2)` for amounts and balances rather than binary floating-point types.
4. **Validation:** prevent a transfer simulation from using the same account as both source and destination, and validate positive amounts and compatible currencies.
5. **Privacy and security:** ensure customers can access only their own accounts, conversations, messages, subscriptions, and budgets.
6. **Data consistency:** define controlled values or database constraints for fields such as `status`, `type`, and `priority`.
7. **Derived analysis:** spending totals and remaining budget can usually be calculated from transactions rather than stored redundantly.

## 8. Scope and limitations

This model is a prototype foundation, not a complete production banking core. It does not implement real payment execution, card authorization, loan underwriting, identity verification, or regulatory workflows. Those capabilities would require additional entities, controls, and integrations.
