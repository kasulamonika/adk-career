import React, { useState, useEffect } from "react";

const API = process.env.REACT_APP_API_URL || "http://localhost:8000";

export default function Profile({ userId, onSaved }) {
  const [form, setForm] = useState({
    age: "",
    education: "",
    current_role: "",
    skills: "",
    interests: "",
    preferred_region: "",
    learning_speed: "moderate",
  });
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API}/api/profile/${userId}`)
      .then((r) => r.json())
      .then((data) => {
        if (data.status === "success" && data.user) {
          const u = data.user;
          setForm({
            age: u.age || "",
            education: u.education || "",
            current_role: u.current_role || "",
            skills: u.skills || "",
            interests: u.interests || "",
            preferred_region: u.preferred_region || "",
            learning_speed: u.learning_speed || "moderate",
          });
        }
      })
      .catch(() => {});
  }, [userId]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setSaved(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const res = await fetch(`${API}/api/profile/${userId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (res.ok) {
        setSaved(true);
        if (onSaved) onSaved();
      } else {
        const data = await res.json();
        setError(data.detail || "Failed to save profile");
      }
    } catch {
      setError("Cannot connect to server");
    }
  };

  return (
    <div className="card">
      <h2>👤 Your Profile</h2>
      <p style={{ color: "var(--text-light)", marginBottom: 20, fontSize: "0.9rem" }}>
        Tell us about yourself so we can personalize your career assessment.
      </p>

      <form onSubmit={handleSubmit}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
          <div className="form-group">
            <label>Age</label>
            <input
              name="age"
              type="number"
              value={form.age}
              onChange={handleChange}
              placeholder="e.g., 22"
            />
          </div>
          <div className="form-group">
            <label>Education</label>
            <input
              name="education"
              value={form.education}
              onChange={handleChange}
              placeholder="e.g., B.Tech CSE"
            />
          </div>
        </div>

        <div className="form-group">
          <label>Current Role</label>
          <input
            name="current_role"
            value={form.current_role}
            onChange={handleChange}
            placeholder="e.g., Student, Software Engineer"
          />
        </div>

        <div className="form-group">
          <label>Skills (comma-separated)</label>
          <input
            name="skills"
            value={form.skills}
            onChange={handleChange}
            placeholder="e.g., Python, JavaScript, Data Analysis"
          />
        </div>

        <div className="form-group">
          <label>Interests (comma-separated)</label>
          <input
            name="interests"
            value={form.interests}
            onChange={handleChange}
            placeholder="e.g., AI, Web Development, Robotics"
          />
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
          <div className="form-group">
            <label>Preferred Region</label>
            <input
              name="preferred_region"
              value={form.preferred_region}
              onChange={handleChange}
              placeholder="e.g., Hyderabad"
            />
          </div>
          <div className="form-group">
            <label>Learning Speed</label>
            <select
              name="learning_speed"
              value={form.learning_speed}
              onChange={handleChange}
            >
              <option value="slow">Slow — I take my time</option>
              <option value="moderate">Moderate — Balanced pace</option>
              <option value="fast">Fast — I learn quickly</option>
            </select>
          </div>
        </div>

        {error && <p className="error-message">{error}</p>}
        {saved && (
          <p style={{ color: "var(--success)", fontSize: "0.85rem", marginTop: 8 }}>
            ✓ Profile saved successfully!
          </p>
        )}

        <button
          type="submit"
          className="btn btn-primary"
          style={{ marginTop: 12 }}
        >
          Save Profile
        </button>
      </form>
    </div>
  );
}
