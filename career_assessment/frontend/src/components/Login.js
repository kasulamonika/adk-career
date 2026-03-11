import React, { useState } from "react";

const API = process.env.REACT_APP_API_URL || "http://localhost:8000";

export default function Login({ onLogin }) {
  const [isRegister, setIsRegister] = useState(false);
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    full_name: "",
  });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const endpoint = isRegister ? "/api/register" : "/api/login";
    const body = isRegister
      ? form
      : { username: form.username, password: form.password };

    try {
      const res = await fetch(`${API}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || "Something went wrong");
        return;
      }

      onLogin({
        user_id: data.user_id,
        username: data.username,
        full_name: data.full_name || form.full_name,
      });
    } catch {
      setError("Cannot connect to server. Is the backend running?");
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>{isRegister ? "Create Account" : "Welcome Back"}</h2>
        <p className="subtitle">
          {isRegister
            ? "Register to start your RIASEC career assessment"
            : "Log in to continue your career journey"}
        </p>

        <form onSubmit={handleSubmit}>
          {isRegister && (
            <div className="form-group">
              <label>Full Name</label>
              <input
                name="full_name"
                value={form.full_name}
                onChange={handleChange}
                placeholder="Enter your full name"
                required
              />
            </div>
          )}

          <div className="form-group">
            <label>Username</label>
            <input
              name="username"
              value={form.username}
              onChange={handleChange}
              placeholder="Enter username"
              required
            />
          </div>

          {isRegister && (
            <div className="form-group">
              <label>Email</label>
              <input
                name="email"
                type="email"
                value={form.email}
                onChange={handleChange}
                placeholder="Enter email"
                required
              />
            </div>
          )}

          <div className="form-group">
            <label>Password</label>
            <input
              name="password"
              type="password"
              value={form.password}
              onChange={handleChange}
              placeholder="Enter password"
              required
            />
          </div>

          {error && <p className="error-message">{error}</p>}

          <button
            type="submit"
            className="btn btn-primary"
            style={{ width: "100%", marginTop: 12 }}
          >
            {isRegister ? "Register" : "Log In"}
          </button>
        </form>

        <div className="toggle-link">
          {isRegister ? "Already have an account? " : "Don't have an account? "}
          <a onClick={() => { setIsRegister(!isRegister); setError(""); }}>
            {isRegister ? "Log In" : "Register"}
          </a>
        </div>
      </div>
    </div>
  );
}
