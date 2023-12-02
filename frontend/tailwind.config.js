import { nextui } from "@nextui-org/react";

/** @type {import("tailwindcss").Config} */
export default {
  content: [
    "./src/**/*.{html,tsx}",
    "./node_modules/@nextui-org/theme/dist/components/(button|card|spinner|divider|textarea|scroll-shadow|input).js",
  ],
  theme: {
    extend: {
      screens: {
        desktop: "1420px",
      },
      colors: {
        bg: {
          primary: "#000000",
        },
      },
    },
  },
  darkMode: "dark",
  plugins: [nextui()],
};
