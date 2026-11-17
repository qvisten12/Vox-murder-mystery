import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";

export const HelloTitle: React.FC<{ title: string }> = ({ title }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ backgroundColor: "#111", justifyContent: "center", alignItems: "center" }}>
      <h1 style={{ color: "#f5d400", fontSize: 120, fontFamily: "sans-serif", opacity }}>{title}</h1>
    </AbsoluteFill>
  );
};
