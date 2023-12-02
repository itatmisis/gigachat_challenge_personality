import { createBrowserRouter } from "react-router-dom";
import { MainPage } from "../../pages/main/main.page";

export const routes = createBrowserRouter([
  {
    path: "/",
    element: <MainPage />
  }
]);
