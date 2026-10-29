// One banking product (data: list_products or get_product_details, schema ProductOut).

import { DynamicStringSchema } from "@copilotkit/a2ui-renderer";
import { type CatalogEntry, card, props } from "./schema";

type Props = { name: string; description: string; monthlyFee: string };

export const ProductCard: CatalogEntry = {
  definition: {
    description: "Card presenting one banking product and its monthly fee.",
    props: props({
      name: DynamicStringSchema.describe("Name of the product"),
      description: DynamicStringSchema.describe("Short description"),
      monthlyFee: DynamicStringSchema.describe("Formatted monthly fee, for example « 4,90 € / mois »"),
    }),
  },
  render: ({ props }: { props: Props }) => (
    <div style={card}>
      <div style={{ fontWeight: 600 }}>{props.name}</div>
      <div style={{ color: "#475569", margin: "4px 0" }}>{props.description}</div>
      <div style={{ fontWeight: 600, color: "#0f766e" }}>{props.monthlyFee}</div>
    </div>
  ),
};
