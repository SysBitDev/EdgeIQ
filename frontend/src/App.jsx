import React, { useEffect, useMemo, useState } from "react";
import HistoricalChart from "./components/HistoricalChart";
import HealthCard from "./components/HealthCard";
import EventsCard from "./components/EventsCard";

function wsUrl(path) {
  const proto = window.location.protocol === "https:" ? "wss" : "ws";
  return `${proto}://${window.location.host}${path}`;
}

export default function App() {
  const [health, setHealth] = useState(null);
  const [count, setCount] = useState(0);
  const [history, setHistory] = useState([]); // усі історичні події з БД
  const [loading, setLoading] = useState(false);

  // fetch health
  useEffect(() => {
    fetch("/api/v1/healthz")
      .then((r) => r.json())
      .then(setHealth)
      .catch(console.error);
  }, []);

  // fetch count
  useEffect(() => {
    fetch("/api/v1/events/count")
      .then((r) => r.json())
      .then((d) => setCount(d.count))
      .catch(console.error);
  }, []);

  // fetch ALL historical data (paged)
  useEffect(() => {
    let aborted = false;
    const pageLimit = 10000; // скільки за раз тягнемо
    async function loadAll() {
      setLoading(true);
      const acc = [];
      let offset = 0;

      try {
        while (true) {
          const url = `/api/v1/events/list?metric=cpu&limit=${pageLimit}&offset=${offset}`;
          const r = await fetch(url);
          if (!r.ok) throw new Error(`HTTP ${r.status}`);
          const data = await r.json();

          if (aborted) return;

          acc.push(...data.items);
          if (data.next_offset == null) break;
          offset = data.next_offset;
        }
        // нормалізуємо під графік [{ts, value}]
        const normalized = acc
          .map((e) => ({ ts: e.ts, value: e.value }))
          .sort((a, b) => a.ts - b.ts);
        setHistory(normalized);
      } catch (e) {
        console.error(e);
      } finally {
        if (!aborted) setLoading(false);
      }
    }
    loadAll();
    return () => {
      aborted = true;
    };
  }, []);

  // live WS: додаємо нові події в історію (щоб графік оновлювався)
  useEffect(() => {
    const ws = new WebSocket(wsUrl("/api/v1/ws"));
    ws.onmessage = (e) => {
      try {
        const msg = JSON.parse(e.data);
        if (msg.type === "event" && msg.metric === "cpu") {
          setHistory((prev) => {
            // вставляємо наприкінці (ts зростає)
            if (prev.length > 0 && msg.ts < prev[prev.length - 1].ts) {
              // out-of-order (рідко), тоді вставляємо з сортуванням
              const next = [...prev, { ts: msg.ts, value: msg.value }];
              next.sort((a, b) => a.ts - b.ts);
              return next;
            }
            return [...prev, { ts: msg.ts, value: msg.value }];
          });
          setCount((c) => c + 1);
        }
      } catch {}
    };
    return () => ws.close();
  }, []);

  return (
    <div
      style={{
        fontFamily: "ui-sans-serif",
        padding: 24,
        maxWidth: 1100,
        margin: "0 auto",
      }}
    >
      <h1 style={{ textAlign: "center", marginBottom: 8 }}>EdgeIQ Dashboard</h1>
      <p style={{ textAlign: "center", color: "#666", marginTop: 0 }}>
        Real-time agent metrics and full historical view
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 20,
          marginTop: 20,
        }}
      >
        <HealthCard health={health} />
        <EventsCard count={count} />
      </div>

      <div style={{ marginTop: 30 }}>
        {loading && (
          <div style={{ color: "#666", marginBottom: 8 }}>Loading history…</div>
        )}
        <HistoricalChart data={history} title="CPU usage history" />
        <div style={{ marginTop: 8, fontSize: 12, color: "#666" }}>
          Tip: use mouse wheel to zoom, click-and-drag to pan.
        </div>
      </div>
    </div>
  );
}
