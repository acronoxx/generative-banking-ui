// Helpers shared by the components of the catalog.

import type { CatalogDefinitions, ComponentRenderer } from "@copilotkit/a2ui-renderer";
// The A2UI renderer relies on the zod 3 API
import { z } from "zod/v3";

export { z };

// zod/v3 and the renderer's zod 3 are two distinct copies for TypeScript (identical at
// runtime): the schemas are cast to the expected type, and the props are typed by hand.
export const props = (shape: Record<string, unknown>) =>
  z.object(shape as z.ZodRawShape) as unknown as CatalogDefinitions[string]["props"];

// One component of the catalog: its definition (sent to the agent) and its React rendering
export type CatalogEntry = {
  definition: CatalogDefinitions[string];
  render: ComponentRenderer<any>;
};

export const card = { padding: 14, borderRadius: 10, border: "1px solid #e5e7eb", background: "#fff" };
