import React from "react";
import { Composition } from "remotion";
import { HelloTitle } from "./HelloTitle";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="HelloTitle"
      component={HelloTitle}
      durationInFrames={90}
      fps={30}
      width={1920}
      height={1080}
      defaultProps={{ title: "Vox Murder Mystery" }}
    />
  );
};
