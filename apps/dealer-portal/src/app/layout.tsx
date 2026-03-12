import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "IncentiveDrive - Dealer Portal",
  description: "Manage your incentive-qualified leads and track performance.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50 text-gray-900 antialiased">
        <header className="border-b border-gray-200 bg-white">
          <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4">
            <h1 className="text-xl font-bold text-blue-600">
              IncentiveDrive{" "}
              <span className="text-sm font-normal text-gray-500">
                Dealer Portal
              </span>
            </h1>
            <nav className="flex gap-6 text-sm font-medium text-gray-600">
              <a href="/" className="hover:text-blue-600">
                Dashboard
              </a>
              <a href="/leads" className="hover:text-blue-600">
                Leads
              </a>
              <a href="/settings" className="hover:text-blue-600">
                Settings
              </a>
              <a href="/billing" className="hover:text-blue-600">
                Billing
              </a>
            </nav>
          </div>
        </header>
        <main>{children}</main>
      </body>
    </html>
  );
}
