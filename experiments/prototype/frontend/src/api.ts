// Direct calls from the page to the backend (/api), without the agent:
// login, logout, and the confirmation of a transfer prepared by the agent.

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

// Session token of the connected customer, kept in memory only (lost on reload)
let token: string | null = null;

export const getToken = () => token;

async function post<T>(path: string, body?: unknown): Promise<T> {
  const response = await fetch(`${BACKEND_URL}/api${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}) },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail ?? response.statusText);
  return data;
}

export async function login(username: string, password: string): Promise<string> {
  token = (await post<{ token: string }>("/auth/login", { username, password })).token;
  return token;
}

export async function logout(): Promise<void> {
  await post("/auth/logout");
  token = null;
}

export type TransferStatus = { id: number; status: "pending" | "confirmed" | "cancelled" };

export const confirmTransfer = (id: number, password: string) =>
  post<TransferStatus>(`/transfers/${id}/confirm`, { password });

export const cancelTransfer = (id: number) => post<TransferStatus>(`/transfers/${id}/cancel`);
