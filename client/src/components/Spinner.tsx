import React from "react";
import "../styles/Spinner.css";

type SpinnerProps = {
  size?: number;
};

function Spinner({ size=60 }: SpinnerProps) {
  return (
    <div
      className="spinner"
      style={{
        width: `${size}px`,
        height: `${size}px`,
      }}
    ></div>
  );
}

export default Spinner;
