import React from "react";

export default function HealthCard({ health }) {
  const ok = !!health?.ok;
  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 12, padding: 20, textAlign: "center" }}>
      <h2>Backend Health</h2>
      <p style={{ fontSize: 18, margin: 0, color: ok ? "#0a7a35" : "#b00020" }}>
        {ok ? "Healthy" : "Unhealthy"}
      </p>
    </div>
  );
}
