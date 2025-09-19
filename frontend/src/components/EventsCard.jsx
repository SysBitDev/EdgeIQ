import React from "react";

export default function EventsCard({ count }) {
  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 12, padding: 20, textAlign: "center" }}>
      <h2>Total Events</h2>
      <p style={{ fontSize: 28, fontWeight: 700, margin: 0 }}>{count}</p>
    </div>
  );
}
