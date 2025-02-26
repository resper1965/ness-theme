import type { Metadata } from "next";
import { DM_Mono, Geist } from "next/font/google";
import { NuqsAdapter } from "nuqs/adapters/next/app";
import "./globals.css";
import EndpointInitializer from "@/components/EndpointInitializer";

const geistSans = Geist({
  variable: "--font-geist-sans",
  weight: "400",
  subsets: ["latin"],
});

const dmMono = DM_Mono({
  subsets: ["latin"],
  variable: "--font-dm-mono",
  weight: "400",
});

export const metadata: Metadata = {
  title: "Agno Chat Template",
  description: "Agno Chat Template",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${dmMono.variable} antialiased`}>
        <EndpointInitializer />
        <NuqsAdapter>{children}</NuqsAdapter>
      </body>
    </html>
  );
}
