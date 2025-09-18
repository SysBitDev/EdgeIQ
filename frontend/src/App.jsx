import React, { useEffect, useState } from "react";

export default function App() {
  const [health, setHealth] = useState(null);
  useEffect(() => {
    fetch("/api/v1/healthz")
      .then((r) => r.json())
      .then(setHealth)
      .catch(console.error);
  }, []);
  return (
    <div style={{ fontFamily: "ui-sans-serif", padding: 24 }}>
      <h1>EdgeIQ</h1>
      <pre>Health: {JSON.stringify(health)}</pre>
    </div>
  );
}
