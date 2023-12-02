import { NavLink, Outlet } from "react-router-dom";
import { Providers } from "../../app/providers";
import { Divider } from "@nextui-org/react";
import { twMerge } from "tailwind-merge";

const Navbar = () => {
  return (
    <header className="flex flex-col mb-4">
      <nav className="flex py-2 px-4 gap-3">
        <NavLink
          className={({ isActive }) =>
            twMerge(
              "flex items-center justify-center text-white/60 py-2 px-3 rounded-lg hover:bg-default-50",
              isActive && "!bg-default-100 text-default-foreground"
            )
          }
          to="/">
          Главная
        </NavLink>
        <NavLink
          className={({ isActive }) =>
            twMerge(
              "flex items-center justify-center text-white/60 py-2 px-3 rounded-lg hover:bg-default-50",
              isActive && "!bg-default-100 text-default-foreground"
            )
          }
          to="/constructor">
          Конструктор
        </NavLink>
      </nav>
      <Divider />
    </header>
  );
};

export const LayoutWithNavbar = () => {
  return (
    <Providers>
      <div className="flex flex-col min-h-full bg-bg-primary">
        <Navbar />
        <Outlet />
      </div>
    </Providers>
  );
};
