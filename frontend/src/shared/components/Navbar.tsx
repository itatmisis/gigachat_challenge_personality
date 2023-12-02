import React from "react";
import { Link, Outlet } from "react-router-dom";

export const Navbar = () => {
  return (
    <div>
      <Link to="/test" />
    </div>
  );
};

export const LayoutWithNavbar = () => {
  return (
    <div className="flex flex-col min-h-full bg-bg-primary">
      <Navbar />
      <Outlet />
    </div>
  );
};
