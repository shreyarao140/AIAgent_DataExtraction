import React from "react";

export const Alert = ({ children }) => (
  <div className="alert">
    {children}
  </div>
);

export const AlertDescription = ({ children }) => <p className="alert-description">{children}</p>;
