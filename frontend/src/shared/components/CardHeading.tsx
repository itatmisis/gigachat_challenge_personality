import { FC, PropsWithChildren } from "react";

export const CardHeading: FC<PropsWithChildren> = ({ children }) => {
  return <h2 className="text-white font-medium text-large">{children}</h2>;
};
