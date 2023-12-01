import { RouterProvider } from "react-router-dom";
import "./index.css";
import { Providers } from "./providers";
import { routes } from "./providers/routes";

export const App = () => {
  return (
    <Providers>
      <RouterProvider router={routes} />
    </Providers>
  );
};
