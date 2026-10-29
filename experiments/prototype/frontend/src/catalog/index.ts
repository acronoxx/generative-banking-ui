// A2UI catalog of the page: a few basic components (Column, Text...) plus the banking
// components. The schema of each component is sent to the agent, which composes the
// interface with them; the page renders them with React.
// To add a component: write its file (definition + render) and list it below.

import { createCatalog, filterCatalog } from "@copilotkit/a2ui-renderer";
import { AccountCard } from "./AccountCard";
import { AppointmentPicker } from "./AppointmentPicker";
import { ProductCard } from "./ProductCard";
import { SpendingChart } from "./SpendingChart";
import { TransactionList } from "./TransactionList";
import { TransferConfirmation } from "./TransferConfirmation";

const BANKING = { AccountCard, TransactionList, SpendingChart, TransferConfirmation, ProductCard, AppointmentPicker };

// Basic components kept for the layout (the full basic catalog weighs ~54 KB in the prompt)
const BASIC = ["Column", "Row", "Card", "Text", "Divider"];

export const catalog = filterCatalog(
  createCatalog(
    Object.fromEntries(Object.entries(BANKING).map(([name, entry]) => [name, entry.definition])),
    Object.fromEntries(Object.entries(BANKING).map(([name, entry]) => [name, entry.render])),
    { catalogId: "copilotkit://banking", includeBasicCatalog: true },
  ),
  (name) => BASIC.includes(name) || name in BANKING,
);
