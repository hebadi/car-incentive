import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "How It Works - IncentiveDrive",
  description:
    "Learn how IncentiveDrive helps consumers find every available car incentive and helps dealers close more deals with incentive-qualified leads.",
  openGraph: {
    title: "How It Works - IncentiveDrive",
    description:
      "Learn how IncentiveDrive helps consumers save and dealers close more deals.",
  },
};

const CONSUMER_STEPS = [
  {
    step: 1,
    title: "Tell Us Where You Are",
    description:
      "Enter your ZIP code. Many incentives are state or utility-specific, so location determines a large portion of your savings.",
  },
  {
    step: 2,
    title: "Pick Your Vehicle Interests",
    description:
      "Choose whether you want an EV, plug-in hybrid, or gas vehicle, new or used. Optionally pick a make and model for more precise results.",
  },
  {
    step: 3,
    title: "Share a Few Details",
    description:
      "Some incentives have income limits or are reserved for groups like military, educators, or first responders. A few quick questions unlock these extra savings.",
  },
  {
    step: 4,
    title: "Get Your Personalized Savings Report",
    description:
      "See every incentive you qualify for -- state rebates, manufacturer cash, utility rebates, affinity discounts -- stacked together with a total savings estimate.",
  },
  {
    step: 5,
    title: "Connect with a Dealer (Optional)",
    description:
      "If you want help claiming your savings, share your contact info. A local dealer will reach out with your incentives already calculated.",
  },
];

const DEALER_BENEFITS = [
  {
    title: "Pre-Qualified Leads",
    description:
      "Every lead includes specific incentive eligibility, dollar amounts, and qualifying programs. Your team can structure deals faster.",
  },
  {
    title: "Higher Close Rates",
    description:
      "Incentive-aware leads close at 2-3x the industry average because they already know the savings available.",
  },
  {
    title: "Incentive Intelligence",
    description:
      "We track 200+ programs across all 50 states so your sales team always has current, accurate incentive data.",
  },
  {
    title: "Flexible Delivery",
    description:
      "Leads arrive via ADF XML to your CRM -- compatible with VinSolutions, Elead, DriveCentric, and every major system.",
  },
];

export default function HowItWorksPage() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-16">
      {/* Consumer section */}
      <section>
        <h2 className="text-3xl font-bold text-gray-900">For Car Shoppers</h2>
        <p className="mt-3 text-lg text-gray-600">
          Finding every available incentive on a car purchase is hard. We make it
          easy.
        </p>

        <div className="mt-10 space-y-8">
          {CONSUMER_STEPS.map((item) => (
            <div key={item.step} className="flex gap-4">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-blue-100 text-sm font-bold text-blue-600">
                {item.step}
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">{item.title}</h3>
                <p className="mt-1 text-sm text-gray-600">
                  {item.description}
                </p>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-10">
          <Link
            href="/calculator"
            className="inline-block rounded-lg bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Try the Calculator
          </Link>
        </div>
      </section>

      {/* Divider */}
      <hr className="my-16 border-gray-200" />

      {/* Dealer section */}
      <section>
        <h2 className="text-3xl font-bold text-gray-900">For Dealers</h2>
        <p className="mt-3 text-lg text-gray-600">
          Stop paying for generic leads. Get buyers who already know what
          incentives they qualify for.
        </p>

        <div className="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2">
          {DEALER_BENEFITS.map((benefit) => (
            <div
              key={benefit.title}
              className="rounded-lg border border-gray-200 bg-white p-5"
            >
              <h3 className="font-semibold text-gray-900">{benefit.title}</h3>
              <p className="mt-2 text-sm text-gray-600">
                {benefit.description}
              </p>
            </div>
          ))}
        </div>

        <div className="mt-10 rounded-xl border border-gray-200 bg-gray-50 p-6">
          <h3 className="font-semibold text-gray-900">
            Interested in IncentiveDrive for your dealership?
          </h3>
          <p className="mt-2 text-sm text-gray-600">
            We are onboarding dealerships in select markets. Reach out to learn
            about our pilot program with free incentive-qualified leads.
          </p>
          <a
            href="mailto:dealers@incentivedrive.com"
            className="mt-4 inline-block rounded-md border border-blue-600 px-4 py-2 text-sm font-semibold text-blue-600 hover:bg-blue-50"
          >
            Contact Our Dealer Team
          </a>
        </div>
      </section>
    </div>
  );
}
