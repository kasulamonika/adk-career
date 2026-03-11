import React, { useState, useEffect } from "react";

const API = process.env.REACT_APP_API_URL || "http://localhost:8000";

const CATEGORY_COLORS = {
  R: "#ef4444",
  I: "#3b82f6",
  A: "#8b5cf6",
  S: "#22c55e",
  E: "#f59e0b",
  C: "#06b6d4",
};

export default function Roadmap({ userId }) {
  const [roadmap, setRoadmap] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API}/api/roadmap/${userId}`)
      .then((r) => r.json())
      .then((data) => {
        if (data.status === "success") {
          setRoadmap(data.roadmap);
        } else {
          setError(data.detail || "Failed to generate roadmap");
        }
        setLoading(false);
      })
      .catch(() => {
        setError("Cannot connect to server");
        setLoading(false);
      });
  }, [userId]);

  if (loading) {
    return (
      <div className="card" style={{ textAlign: "center", padding: 40 }}>
        <p>🔍 Analyzing your assessment and generating career roadmap...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card">
        <p className="error-message">{error}</p>
      </div>
    );
  }

  if (!roadmap) return null;

  const { riasec_scores, score_percentages, top_category, secondary_category,
          recommended_careers, recommended_specializations, skills_to_develop,
          roadmap_phases, total_duration_months, salary_progression } = roadmap;

  return (
    <div>
      {/* Top Result */}
      <div className="card" style={{ borderTop: `4px solid ${CATEGORY_COLORS[top_category.code]}` }}>
        <h2>🎯 Your RIASEC Profile</h2>
        <div style={{ textAlign: "center", margin: "20px 0" }}>
          <h3 style={{ fontSize: "1.5rem", color: CATEGORY_COLORS[top_category.code] }}>
            {top_category.info.title}
          </h3>
          <p style={{ color: "var(--text-light)", maxWidth: 600, margin: "10px auto", lineHeight: 1.7 }}>
            {top_category.info.description}
          </p>
        </div>
      </div>

      {/* RIASEC Scores */}
      <div className="card">
        <h3>📊 Your RIASEC Scores</h3>
        <div className="score-chart">
          {Object.entries(riasec_scores).map(([cat, score]) => (
            <div
              key={cat}
              className="score-item"
              style={{ borderColor: CATEGORY_COLORS[cat] }}
            >
              <div className="score-label" style={{ color: CATEGORY_COLORS[cat] }}>
                {score_percentages[
                  { R: "Realistic", I: "Investigative", A: "Artistic",
                    S: "Social", E: "Enterprising", C: "Conventional" }[cat]
                ] !== undefined
                  ? `${cat} — ${{ R: "Realistic", I: "Investigative", A: "Artistic",
                      S: "Social", E: "Enterprising", C: "Conventional" }[cat]}`
                  : cat}
              </div>
              <div className="score-value" style={{ color: CATEGORY_COLORS[cat] }}>
                {score}
              </div>
              <div className="score-percent">
                {score_percentages[
                  { R: "Realistic", I: "Investigative", A: "Artistic",
                    S: "Social", E: "Enterprising", C: "Conventional" }[cat]
                ]}%
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recommended Careers */}
      <div className="card">
        <h3>💼 Recommended Career Paths</h3>
        <div className="career-list">
          {recommended_careers.map((career, i) => (
            <span key={i} className="career-tag">{career}</span>
          ))}
        </div>

        <h3 style={{ marginTop: 20 }}>🎓 Recommended Specializations</h3>
        <div className="career-list">
          {recommended_specializations.map((spec, i) => (
            <span key={i} className="career-tag" style={{ background: "rgba(34,197,94,0.08)", color: "#16a34a" }}>
              {spec}
            </span>
          ))}
        </div>

        <h3 style={{ marginTop: 20 }}>🛠️ Skills to Develop</h3>
        <div className="career-list">
          {skills_to_develop.map((skill, i) => (
            <span key={i} className="career-tag" style={{ background: "rgba(245,158,11,0.08)", color: "#d97706" }}>
              {skill}
            </span>
          ))}
        </div>
      </div>

      {/* Roadmap Phases */}
      <div className="card">
        <h3>🗺️ Your Career Roadmap ({total_duration_months} months)</h3>
        <p style={{ color: "var(--text-light)", fontSize: "0.9rem", marginBottom: 16 }}>
          A personalized step-by-step plan based on your RIASEC profile.
        </p>
        {roadmap_phases.map((phase) => (
          <div key={phase.phase} className="phase-card">
            <h4>
              Phase {phase.phase}: {phase.title}
            </h4>
            <div className="duration">⏱ {phase.duration_months} months</div>
            <ul>
              {phase.actions.map((action, i) => (
                <li key={i}>{action}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      {/* Salary Progression */}
      <div className="card">
        <h3>💰 Expected Salary Progression</h3>
        <table className="salary-table">
          <thead>
            <tr>
              <th>Career Stage</th>
              <th>Expected Salary</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(salary_progression).map(([stage, salary]) => (
              <tr key={stage}>
                <td>{stage}</td>
                <td style={{ fontWeight: 600, color: "var(--success)" }}>{salary}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {secondary_category && (
        <div className="card">
          <h3>🔄 Secondary Profile: {secondary_category.info.title}</h3>
          <p style={{ color: "var(--text-light)", fontSize: "0.9rem" }}>
            {secondary_category.info.description}
          </p>
          <div className="career-list" style={{ marginTop: 12 }}>
            {secondary_category.info.careers && secondary_category.info.careers.slice(0, 4).map((c, i) => (
              <span key={i} className="career-tag">{c}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
