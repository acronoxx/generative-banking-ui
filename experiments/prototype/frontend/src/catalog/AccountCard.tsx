// One account and its balance (data: list_accounts, schema AccountOut).

import { DynamicStringSchema } from "@copilotkit/a2ui-renderer";
import { type CatalogEntry, props } from "./schema";

type Props = { accountType: string; maskedIban: string; balance: string };

export const AccountCard: CatalogEntry = {
  definition: {
    description: "Tile showing one bank account and its balance.",
    props: props({
      accountType: DynamicStringSchema.describe("Type of account, for example « Compte courant »"),
      maskedIban: DynamicStringSchema.describe("Masked IBAN, as returned by the tool"),
      balance: DynamicStringSchema.describe("Formatted balance, for example « 1 250,40 € »"),
    }),
  },
  render: ({ props }: { props: Props }) => (
    <div style={{ padding: 16, borderRadius: 12, background: "#0f766e", color: "#fff", minWidth: 200 }}>
      <div style={{ fontSize: 13, opacity: 0.85 }}>{props.accountType}</div>
      <div style={{ fontSize: 24, fontWeight: 600, margin: "4px 0" }}>{props.balance}</div>
      <div style={{ fontSize: 12, opacity: 0.75 }}>{props.maskedIban}</div>
    </div>
  ),
};
