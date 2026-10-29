// Last transactions of an account (data: get_recent_transactions, schema TransactionOut).

import { type CatalogEntry, card, props, z } from "./schema";

type Transaction = { date: string; label: string; amount: number };

export const TransactionList: CatalogEntry = {
  definition: {
    description: "List of transactions: date, label and amount (negative for a spending).",
    props: props({
      transactions: z
        .array(z.object({ date: z.string(), label: z.string(), amount: z.number() }))
        .describe("Transactions, most recent first. date: DD/MM/YYYY, amount in euros"),
    }),
  },
  render: ({ props }: { props: { transactions: Transaction[] } }) => (
    <div style={card}>
      {props.transactions.map((t, i) => (
        <div key={i} style={{ display: "flex", gap: 12, padding: "6px 0", borderBottom: "1px solid #f1f5f9" }}>
          <span style={{ color: "#64748b", width: 90 }}>{t.date}</span>
          <span style={{ flex: 1 }}>{t.label}</span>
          <span style={{ fontWeight: 600, color: t.amount < 0 ? "#b91c1c" : "#15803d" }}>{t.amount.toFixed(2)} €</span>
        </div>
      ))}
    </div>
  ),
};
