import React, { ReactNode } from "react";
import { NextUIProvider } from "@nextui-org/react";
import { useNavigate } from "react-router-dom";

export const Providers = ({ children }: { children: ReactNode }) => {
  const navigate = useNavigate();

  return (
    <NextUIProvider className="h-full flex flex-col bg-bg-primary w-full" navigate={navigate}>
      {children}
    </NextUIProvider>
  );
};
