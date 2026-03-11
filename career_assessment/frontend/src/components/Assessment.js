import React, { useState, useEffect } from "react";

const API = process.env.REACT_APP_API_URL || "http://localhost:8000";

const CATEGORY_NAMES = {
  R: "Realistic",
  I: "Investigative",
  A: "Artistic",
  S: "Social",
  E: "Enterprising",
  C: "Conventional",
};

export default function Assessment({ userId, onComplete }) {
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API}/api/questions`)
      .then((r) => r.json())
      .then((data) => {
        if (data.status === "success") {
          setQuestions(data.questions);
        }
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to load questions");
        setLoading(false);
      });
  }, []);

  const selectOption = (questionId, option) => {
    setAnswers({ ...answers, [questionId]: option });
  };

  const answeredCount = Object.keys(answers).length;
  const totalCount = questions.length;
  const progress = totalCount > 0 ? (answeredCount / totalCount) * 100 : 0;

  const handleSubmit = async () => {
    if (answeredCount < totalCount) {
      setError(`Please answer all ${totalCount} questions before submitting.`);
      return;
    }

    setSubmitting(true);
    setError("");

    const payload = {
      answers: Object.entries(answers).map(([qid, opt]) => ({
        question_id: parseInt(qid),
        selected_option: opt,
      })),
    };

    try {
      const res = await fetch(`${API}/api/answers/${userId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (res.ok) {
        onComplete();
      } else {
        const data = await res.json();
        setError(data.detail || "Failed to submit answers");
      }
    } catch {
      setError("Cannot connect to server");
    }
    setSubmitting(false);
  };

  if (loading) {
    return (
      <div className="card" style={{ textAlign: "center", padding: 40 }}>
        <p>Loading questions...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="card">
        <h2>📝 RIASEC Career Assessment</h2>
        <p style={{ color: "var(--text-light)", fontSize: "0.9rem", marginBottom: 16 }}>
          Answer all {totalCount} questions to discover your career personality type.
          Each question maps to one of the RIASEC categories.
        </p>

        <div className="progress-bar">
          <div className="fill" style={{ width: `${progress}%` }} />
        </div>
        <p className="progress-text">
          {answeredCount} of {totalCount} questions answered ({Math.round(progress)}%)
        </p>
      </div>

      {questions.map((q, idx) => (
        <div key={q.id} className="question-card">
          <div className="question-header">
            <span className="question-number">Q{idx + 1}</span>
            <span className={`category-badge category-${q.category}`}>
              {CATEGORY_NAMES[q.category]}
            </span>
          </div>

          <p className="question-text">{q.question_text}</p>

          <div className="options">
            {["A", "B", "C", "D"].map((letter) => (
              <div
                key={letter}
                className={`option ${answers[q.id] === letter ? "selected" : ""}`}
                onClick={() => selectOption(q.id, letter)}
              >
                <span className="option-letter">{letter}</span>
                <span>{q[`option_${letter.toLowerCase()}`]}</span>
              </div>
            ))}
          </div>
        </div>
      ))}

      {error && (
        <p className="error-message" style={{ textAlign: "center", marginBottom: 16 }}>
          {error}
        </p>
      )}

      <div style={{ textAlign: "center", marginBottom: 32 }}>
        <button
          className="btn btn-primary"
          style={{ padding: "12px 40px", fontSize: "1rem" }}
          onClick={handleSubmit}
          disabled={submitting}
        >
          {submitting ? "Submitting..." : "Submit Assessment"}
        </button>
      </div>
    </div>
  );
}
