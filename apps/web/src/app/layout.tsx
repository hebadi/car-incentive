import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "IncentiveDrive - Find Your Car Incentives",
    template: "%s | IncentiveDrive",
  },
  description:
    "Discover all available car incentives, rebates, and savings personalized for you. State rebates, manufacturer cash, utility rebates, and more.",
  metadataBase: new URL(
    process.env.NEXT_PUBLIC_SITE_URL || "https://incentivedrive.com"
  ),
  openGraph: {
    siteName: "IncentiveDrive",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-white text-gray-900 antialiased">
        <header className="sticky top-0 z-50 border-b border-indigo-500/10 bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 backdrop-blur-md">
          <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4">
            <Link
              href="/"
              className="group flex items-center gap-2 text-xl font-bold"
            >
              <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-indigo-600 text-sm font-black text-white shadow-lg shadow-indigo-500/25">
                ID
              </span>
              <span className="bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent transition-all group-hover:from-blue-200 group-hover:to-white">
                IncentiveDrive
              </span>
            </Link>
            <nav
              aria-label="Main navigation"
              className="flex items-center gap-1 text-sm font-medium"
            >
              <Link
                href="/calculator"
                className="rounded-lg px-4 py-2 text-slate-300 transition-all hover:bg-white/10 hover:text-white"
              >
                Calculator
              </Link>
              <Link
                href="/how-it-works"
                className="rounded-lg px-4 py-2 text-slate-300 transition-all hover:bg-white/10 hover:text-white"
              >
                How It Works
              </Link>
              <Link
                href="/portal"
                className="ml-2 rounded-lg border border-indigo-400/30 bg-indigo-500/10 px-4 py-2 text-indigo-300 transition-all hover:border-indigo-400/50 hover:bg-indigo-500/20 hover:text-indigo-200"
              >
                Dealer Portal
              </Link>
            </nav>
          </div>
        </header>
        <main>{children}</main>
        <footer className="border-t border-gray-200 bg-gradient-to-b from-slate-50 to-slate-100 px-4 py-10">
          <div className="mx-auto max-w-7xl text-center text-xs text-gray-400">
            <p className="font-medium text-gray-500">
              &copy; {new Date().getFullYear()} IncentiveDrive. All rights
              reserved.
            </p>
            <p className="mt-2 max-w-xl mx-auto leading-5">
              Savings estimates are for informational purposes only and do not
              guarantee eligibility. Verify with official sources before making
              purchase decisions.
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
