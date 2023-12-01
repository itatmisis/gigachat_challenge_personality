import React, { ReactNode } from "react";
import { NextUIProvider } from "@nextui-org/react";

export const Providers = ({ children }: { children: ReactNode }) => {
  return (
    <NextUIProvider className="h-full flex flex-col bg-bg-primary w-full">
      {children}
    </NextUIProvider>
  );
};
