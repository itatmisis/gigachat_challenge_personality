import { createBrowserRouter } from "react-router-dom";
import { MainPage } from "../../pages/main/main.page";
import { LayoutWithNavbar } from "@/components/Navbar";
import { LandingPage } from "../../pages/landing/landing.page";

export const routes = createBrowserRouter([
  {
    path: "/",
    element: <LayoutWithNavbar />,
    children: [
      {
        path: "index",
        element: <LandingPage />
      },
      {
        path: "constructor",
        element: <MainPage />
      }
    ]
  }
]);
