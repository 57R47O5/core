import { login } from "../api";

export default function Login() {
  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = new FormData(e.target);

    await login({
      username: data.get("username"),
      password: data.get("password"),
    });

    window.location.href = "/";
  };

  return (
    <div style={{ maxWidth: 400, margin: "4rem auto" }}>
      <h1>Login</h1>

      <form onSubmit={handleSubmit}>
        <div>
          <input
            name="username"
            placeholder="Usuario"
            autoComplete="username"
            required
          />
        </div>

        <div>
          <input
            type="password"
            name="password"
            placeholder="Password"
            autoComplete="current-password"
            required
          />
        </div>

        <button type="submit">Entrar</button>
      </form>
    </div>
  );
}
