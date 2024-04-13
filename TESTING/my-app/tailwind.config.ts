
const { nextui } = require("@nextui-org/react");

module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}",
  ],
  important: true,
  theme: {
    extend: {
      fontFamily: {
        Peyda: ["Peyda"],
      },
      backgroundImage: {
        "body-bg": "url('/files/default/bg-pattern.png')",
        "price-box-bg": "url('/files/default/price_box_bg.png')",
        "wave-bg": "url('/files/default/wave.png')",
      },
    },
  },

  plugins: [
    nextui({
      themes: {
        light: {
          layout: {},
          colors: {
            primary: "#ffffff",
            secondary: "#B8BBC0",
            dark: "#141E2E",
            red: "#E50045",
            green: "#70A75C;",
            blue: "#1171FF",
          },
          backgroundColor: {
            white: "#ffffff",
            dark: "#141E2E",
            secondary: "#37404D",
            red: "#E50045",
            darkLight: "#1B273A",
            darkLighter: "#243042",
            green: "#70A75C;",
            blue: "#1171FF",
          },
        },
        dark: {
          layout: {},
          colors: {
            primary: "#ffffff",
            secondary: "#B8BBC0",
            dark: "#141E2E",
            red: "#E50045",
            green: "#70A75C;",
            blue: "#1171FF",
          },
          backgroundColor: {
            white: "#ffffff",
            dark: "#141E2E",
            secondary: "#37404D",
            red: "#E50045",
            darkLight: "#1B273A",
            darkLighter: "#243042",
            green: "#70A75C;",
            blue: "#1171FF",
          },
        },
      },
    }),
  ],
  darkMode: "class",
};