import {
  Links,
  Meta,
  Outlet,
  Scripts,
  ScrollRestoration,
} from "@remix-run/react";
import type { LinksFunction } from "@remix-run/node";
import {NextUIProvider} from "@nextui-org/react";

import "./tailwind.css";
import NavBar from "./components/NavBar";

export const links: LinksFunction = () => [
  { rel: "preconnect", href: "https://fonts.googleapis.com" },
  {
    rel: "preconnect",
    href: "https://fonts.gstatic.com",
    crossOrigin: "anonymous",
  },
  {
    rel: "stylesheet",
    href: "https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap",
  },
];

export function Layout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <Meta />
        <Links />
      </head>
      <body className="min-h-screen">
        <div className="bg-white text-black dark:bg-black dark:text-white duration-200">
          <NextUIProvider>
            <NavBar />
            {children}
            <ScrollRestoration />
            <Scripts />
          </NextUIProvider>
        </div>
      </body>
    </html>
  );
}

export default function App() {
  return <Outlet />;
}
