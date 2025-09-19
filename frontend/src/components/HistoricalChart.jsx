import React, { useEffect, useMemo, useRef } from "react";
import uPlot from "uplot";
import "uplot/dist/uPlot.min.css";

function attachInteractions(u) {
  let dragging = false;
  let startX = 0;
  let xMin0 = 0;
  let xMax0 = 0;

  u.over.addEventListener(
    "wheel",
    (e) => {
      e.preventDefault();
      const rect = u.over.getBoundingClientRect();
      const left = rect.left;
      const width = rect.width;

      const x = (e.clientX - left) / width;
      const scaleX = u.series[0].scale;
      const min = u.scales[scaleX].min ?? u.getRange(scaleX, true)[0];
      const max = u.scales[scaleX].max ?? u.getRange(scaleX, true)[1];
      const cx = min + x * (max - min);

      const factor = e.deltaY < 0 ? 0.9 : 1.1;
      const newMin = cx - (cx - min) * factor;
      const newMax = cx + (max - cx) * factor;

      u.setScale(scaleX, { min: newMin, max: newMax });
    },
    { passive: false },
  );

  const onDown = (e) => {
    dragging = true;
    startX = e.clientX;
    const scaleX = u.series[0].scale;
    xMin0 = u.scales[scaleX].min ?? u.getRange(scaleX, true)[0];
    xMax0 = u.scales[scaleX].max ?? u.getRange(scaleX, true)[1];
  };

  const onMove = (e) => {
    if (!dragging) return;
    const dx = e.clientX - startX;
    const { width } = u.over.getBoundingClientRect();
    const scaleX = u.series[0].scale;
    const span =
      (u.scales[scaleX].max ?? xMax0) - (u.scales[scaleX].min ?? xMin0);
    const shift = (dx / width) * span;
    u.setScale(scaleX, { min: xMin0 - shift, max: xMax0 - shift });
  };

  const onUp = () => {
    dragging = false;
  };

  u.over.addEventListener("mousedown", onDown);
  window.addEventListener("mousemove", onMove);
  window.addEventListener("mouseup", onUp);

  return () => {
    u.over.removeEventListener("mousedown", onDown);
    window.removeEventListener("mousemove", onMove);
    window.removeEventListener("mouseup", onUp);
  };
}

export default function HistoricalChart({ data, title = "History" }) {
  const wrapRef = useRef(null);
  const uplotRef = useRef(null);

  const seriesData = useMemo(() => {
    const xs = data.map((d) => d.ts);
    const ys = data.map((d) => d.value);
    return [xs, ys];
  }, [data]);

  useEffect(() => {
    if (!wrapRef.current) return;

    if (uplotRef.current) {
      uplotRef.current.destroy();
      uplotRef.current = null;
    }

    const opts = {
      title,
      width: wrapRef.current.clientWidth,
      height: 360,
      pxAlign: 0,
      scales: {
        x: { time: true },
        y: { auto: true },
      },
      series: [
        {},
        {
          label: "value",
          spanGaps: true,
          points: { show: false },
          stroke: "rgb(33, 111, 237)",
          width: 2,
        },
      ],
      axes: [
        {
          scale: "x",
          values: (u, ticks) =>
            ticks.map((t) =>
              new Date(t * 1000).toLocaleTimeString([], { hour12: false }),
            ),
        },
        {
          scale: "y",
        },
      ],
    };

    const u = new uPlot(opts, seriesData, wrapRef.current);
    uplotRef.current = u;

    const ro = new ResizeObserver(() => {
      u.setSize({ width: wrapRef.current.clientWidth, height: 360 });
    });
    ro.observe(wrapRef.current);

    const detach = attachInteractions(u);

    return () => {
      detach && detach();
      ro.disconnect();
      u.destroy();
    };
  }, [seriesData, title]);

  useEffect(() => {
    if (uplotRef.current) {
      uplotRef.current.setData(seriesData);
    }
  }, [seriesData]);

  return (
    <div
      ref={wrapRef}
      style={{ border: "1px solid #ddd", borderRadius: 12, padding: 12 }}
    />
  );
}
