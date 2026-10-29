// Spending per category (data: get_spending_by_category or compare_spending, schema CategorySpending).

import { DynamicStringSchema } from "@copilotkit/a2ui-renderer";
import { type CatalogEntry, card, props, z } from "./schema";

type Item = { category: string; total: number };

export const SpendingChart: CatalogEntry = {
  definition: {
    description: "Horizontal bar chart of the spending per category over a period.",
    props: props({
      title: DynamicStringSchema.describe("Title, for example « Dépenses d'octobre »"),
      items: z.array(z.object({ category: z.string(), total: z.number() })).describe("Total per category, in euros"),
    }),
  },
  render: ({ props }: { props: { title: string; items: Item[] } }) => {
    const max = Math.max(...props.items.map((i) => i.total), 1);
    return (
      <div style={card}>
        <div style={{ fontWeight: 600, marginBottom: 8 }}>{props.title}</div>
        {props.items.map((i) => (
          <div key={i.category} style={{ display: "flex", alignItems: "center", gap: 8, margin: "4px 0" }}>
            <span style={{ width: 110 }}>{i.category}</span>
            <div style={{ height: 14, width: `${(i.total / max) * 60}%`, background: "#0f766e", borderRadius: 4 }} />
            <span>{i.total.toFixed(2)} €</span>
          </div>
        ))}
      </div>
    );
  },
};
