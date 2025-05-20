/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./src/app/**/*.{js,ts,jsx,tsx}",
        "./src/components/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            borderRadius: {
                lg: "var(--radius-lg)",
                md: "var(--radius-md)",
                sm: "var(--radius-sm)",
            },
            colors: {
                background: "hsl(var(--background))",
                foreground: "hsl(var(--foreground))",
                primary: "hsl(var(--primary))",
                secondary: "hsl(var(--secondary))",
                muted: "hsl(var(--muted))",
                accent: "hsl(var(--accent))",
                destructive: "hsl(var(--destructive))",
                border: "hsl(var(--border))",
                input: "hsl(var(--input))",
                ring: "hsl(var(--ring))",
                card: "hsl(var(--card))",
                "card-foreground": "hsl(var(--card-foreground))",
            },
        },
    },
    plugins: [],
}
