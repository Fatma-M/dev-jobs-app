/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./static/src/**/*.js"],
  darkMode: "class",
  theme: {
    container: {
      center: true,
      screens: {
        sm: "500px",
        md: "700px",
        lg: "900px",
        xl: "1100px",
      },
    },
    extend: {
      colors: {
        darkBlue: "#5964E0",
        lightBlue: "#939BF4",
        darkGray: "#6E8098",
        darkerGray: "#D5D8F7",
        lightGray: "#E8E8EA",
        lighterGray: "#F4F6F8",
      },
      backgroundImage: {
        "header-pattern": "url('/static/images/desktop/bg-pattern-header.svg')",
        "header-pattern-mobile":
          "url('/static/images/mobile/bg-pattern-header.svg')",
      },
    },
  },
  plugins: [],
};
