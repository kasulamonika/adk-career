import React, { useState } from "react";
import "./App.css";
import Login from "./components/Login";
import Profile from "./components/Profile";
import Assessment from "./components/Assessment";
import Roadmap from "./components/Roadmap";

const TABS = [
  { id: "profile", label: "👤 Profile" },
  { id: "assessment", label: "📝 Assessment" },
  { id: "roadmap", label: "🗺️ Roadmap" },
];

export default function App() {
  const [user, setUser] = useState(null);
  const [activeTab, setActiveTab] = useState("profile");

  const handleLogin = (userData) => {
    setUser(userData);
    setActiveTab("profile");
  };

  const handleLogout = () => {
    setUser(null);
    setActiveTab("profile");
  };

  if (!user) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🎓 RIASEC Career Assessment</h1>
        <div className="user-info">
          <span>Welcome, {user.full_name || user.username}</span>
          <button className="btn btn-sm btn-danger" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      <div className="main">
        <div className="tabs">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              className={`tab ${activeTab === tab.id ? "active" : ""}`}
              onClick={() => setActiveTab(tab.id)}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {activeTab === "profile" && (
          <Profile
            userId={user.user_id}
            onSaved={() => {}}
          />
        )}

        {activeTab === "assessment" && (
          <Assessment
            userId={user.user_id}
            onComplete={() => setActiveTab("roadmap")}
          />
        )}

        {activeTab === "roadmap" && <Roadmap userId={user.user_id} />}
      </div>
    </div>
  );
}
