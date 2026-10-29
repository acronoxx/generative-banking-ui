// Login page: a single customer in the prototype (demo / demo).

import { type FormEvent, useState } from "react";
import { login } from "../api";

export function LoginPage({ onLogin }: { onLogin: (token: string) => void }) {
  const [username, setUsername] = useState("demo");
  const [password, setPassword] = useState("demo");
  const [error, setError] = useState<string | null>(null);

  const submit = (event: FormEvent) => {
    event.preventDefault();
    login(username, password).then(onLogin, (e: Error) => setError(e.message));
  };

  return (
    <form onSubmit={submit} style={{ display: "grid", gap: 8, maxWidth: 280, margin: "120px auto" }}>
      <h2>Connexion</h2>
      <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Identifiant" />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Mot de passe" />
      <button type="submit">Se connecter</button>
      {error && <div style={{ color: "#b91c1c" }}>{error}</div>}
    </form>
  );
}
