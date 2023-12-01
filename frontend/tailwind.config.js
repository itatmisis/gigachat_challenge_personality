import { nextui } from "@nextui-org/react";

/** @type {import("tailwindcss").Config} */
export default {
  content: [
    "./src/**/*.{html,tsx}",
    "./node_modules/@nextui-org/theme/dist/components/(button|snippet|code|input).js",
  ],
  theme: {
    extend: {
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
