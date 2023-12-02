import { createBrowserRouter } from "react-router-dom";
import { MainPage } from "../../pages/main/main.page";
import { LayoutWithNavbar } from "@/components/Navbar";

export const routes = createBrowserRouter([
  {
    path: "/",
    element: <LayoutWithNavbar />,
    children: [
      {
        path: "/",
        element: <MainPage />
      }
    ]
  }
]);
