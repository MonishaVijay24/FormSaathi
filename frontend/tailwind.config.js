export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        forest: "#153A36",
        cream: "#FFFAF1",
        parchment: "#F5EFE3",
        bgGradient: "#F5EFE3",
        ink: "#153A36",
        leaf: "#2C6B5F",
        leafHover: "#205248",
        leafTint: "#E1EEE9",
        saffron: "#DFA23A",
        amber: "#F2A93B",
        amberTint: "#FFF0CE",
        error: "#C8402F",
        errorTint: "#FDE4E4",
        textSecondary: "#596B64",
        slate: "#596B64",
        terracotta: "#BD684E",
        success: "#2E9D57",
      },
      fontFamily: {
        sans: ["Nunito", "system-ui", "sans-serif"],
        serif: ["Fraunces", "Playfair Display", "serif"],
      },
      boxShadow: {
        soft: "0 4px 14px rgba(60, 50, 20, 0.08)",
        premium: "0 8px 22px rgba(60, 50, 20, 0.08)",
      },
    },
  },
};
