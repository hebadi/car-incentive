"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";

export default function PortalLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const [dealerName, setDealerName] = useState<string>("");

  useEffect(() => {
    const name = sessionStorage.getItem("portal_dealer_name");
    if (name) setDealerName(name);
  }, []);

  const links = [
    { href: "/portal/dashboard", label: "Dashboard" },
    { href: "/portal/leads", label: "Leads" },
    { href: "/portal/settings", label: "Settings" },
  ];

  return (
    <>
      <nav className="border-b border-gray-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
          <Link href="/portal/dashboard" className="text-lg font-bold text-blue-600">
            IncentiveDrive Dealer Portal
          </Link>
          <div className="flex items-center gap-6">
            {links.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={`text-sm font-medium ${
                  pathname === link.href
                    ? "text-blue-600"
                    : "text-gray-600 hover:text-blue-600"
                }`}
              >
                {link.label}
              </Link>
            ))}
            {dealerName && (
              <span className="text-sm text-gray-400">{dealerName}</span>
            )}
          </div>
        </div>
      </nav>
      <div>{children}</div>
    </>
  );
}
