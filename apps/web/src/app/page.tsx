import type { Metadata } from "next";
import Link from "next/link";
import TopIncentivesSearch from "@/components/TopIncentivesSearch";

export const metadata: Metadata = {
  title: "IncentiveDrive - Discover Every Dollar of Savings on Your Next Car",
  description:
    "Find all available car incentives, rebates, and savings personalized for your location. State rebates, manufacturer cash, utility rebates, affinity discounts, and more.",
  openGraph: {
    title: "IncentiveDrive - Discover Every Dollar of Savings on Your Next Car",
    description:
      "Find all available car incentives, rebates, and savings personalized for your location.",
    type: "website",
  },
};

const TRUST_SIGNALS = [
  { stat: "200+", label: "Incentive Programs Tracked" },
  { stat: "50", label: "States Covered" },
  { stat: "$33K+", label: "Maximum Stackable Savings" },
];

const HOW_IT_WORKS = [
  {
    step: 1,
    title: "Enter Your ZIP Code",
    description: "Tell us where you live to find location-specific incentives.",
    icon: (
      <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
        <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
      </svg>
    ),
    color: "from-blue-500 to-cyan-500",
    bgColor: "bg-blue-50",
  },
  {
    step: 2,
    title: "Share Your Preferences",
    description:
      "Select your vehicle type and tell us a bit about yourself for eligibility matching.",
    icon: (
      <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z" />
        <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    ),
    color: "from-violet-500 to-purple-500",
    bgColor: "bg-violet-50",
  },
  {
    step: 3,
    title: "See Your Savings",
    description:
      "Get a personalized breakdown of every incentive you qualify for, stacked for maximum savings.",
    icon: (
      <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
    color: "from-emerald-500 to-green-500",
    bgColor: "bg-emerald-50",
  },
  {
    step: 4,
    title: "Connect with a Dealer",
    description:
      "A local dealer contacts you with your savings already calculated -- no haggling needed.",
    icon: (
      <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.746 3.746 0 011.043 3.296A3.745 3.745 0 0121 12z" />
      </svg>
    ),
    color: "from-amber-500 to-orange-500",
    bgColor: "bg-amber-50",
  },
];

const FEATURED_CARS = [
  {
    make: "Hyundai",
    model: "IONIQ 5",
    savings: "$14,750",
    label: "Up to",
  },
  {
    make: "Tesla",
    model: "Model Y",
    savings: "$11,500",
    label: "Up to",
  },
  {
    make: "Ford",
    model: "F-150 Lightning",
    savings: "$16,200",
    label: "Up to",
  },
];

function buildLogoUrl(make: string): string {
  const slug = make.toLowerCase().replace(/\s+/g, "-");
  return `https://www.carlogos.org/car-logos/${slug}-logo.png`;
}

export default function LandingPage() {
  return (
    <>
      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-indigo-950 to-blue-900 px-4 py-24 text-center sm:py-32">
        {/* Background decoration */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 h-80 w-80 rounded-full bg-blue-500/10 blur-3xl" />
          <div className="absolute -bottom-40 -left-40 h-80 w-80 rounded-full bg-indigo-500/10 blur-3xl" />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 h-96 w-96 rounded-full bg-violet-500/5 blur-3xl" />
        </div>

        <div className="relative mx-auto max-w-4xl">
          <p className="animate-fade-in text-sm font-semibold uppercase tracking-widest text-blue-400">
            The smartest way to buy a car
          </p>
          <h2 className="mt-4 animate-fade-in-up text-4xl font-extrabold tracking-tight text-white sm:text-6xl lg:text-7xl">
            Discover every dollar of{" "}
            <span className="bg-gradient-to-r from-blue-400 via-cyan-400 to-emerald-400 bg-clip-text text-transparent">
              savings
            </span>{" "}
            on your next car
          </h2>
          <p className="mx-auto mt-6 max-w-2xl animate-fade-in-up text-lg leading-8 text-slate-300" style={{ animationDelay: "0.15s" }}>
            State rebates, manufacturer cash, utility incentives, military and
            educator discounts -- stacked together so you keep more money in
            your pocket.
          </p>

          <div className="mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center" style={{ animationDelay: "0.3s" }}>
            <Link
              href="/calculator"
              className="group relative inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 px-8 py-4 text-lg font-bold text-white shadow-2xl shadow-blue-500/25 transition-all duration-300 hover:shadow-blue-500/40 hover:scale-[1.02] hover:from-blue-500 hover:to-indigo-500 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 focus:ring-offset-slate-900"
            >
              Calculate My Savings
              <svg className="h-5 w-5 transition-transform group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </Link>
            <p className="text-sm text-slate-400">
              Free -- takes about 2 minutes
            </p>
          </div>

          {/* Quick search by ZIP */}
          <div className="mt-14 border-t border-white/10 pt-10">
            <p className="mb-4 text-sm font-medium text-slate-400">
              Top deals near you
            </p>
            <TopIncentivesSearch />
          </div>
        </div>
      </section>

      {/* Trust signals */}
      <section className="relative -mt-8 px-4">
        <div className="mx-auto max-w-4xl">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            {TRUST_SIGNALS.map((item, i) => (
              <div
                key={item.label}
                className="rounded-2xl border border-gray-100 bg-white p-6 text-center shadow-xl shadow-gray-200/50"
                style={{ animationDelay: `${i * 0.1}s` }}
              >
                <p className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-4xl font-black text-transparent">
                  {item.stat}
                </p>
                <p className="mt-1 text-sm font-medium text-gray-600">{item.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Savings */}
      <section className="px-4 py-20">
        <div className="mx-auto max-w-6xl">
          <div className="text-center">
            <p className="text-sm font-semibold uppercase tracking-widest text-indigo-600">
              Real savings on popular EVs
            </p>
            <h3 className="mt-2 text-3xl font-bold text-gray-900 sm:text-4xl">
              See what drivers are saving
            </h3>
            <p className="mx-auto mt-4 max-w-2xl text-gray-500">
              These are real stacked incentives available right now. Your savings depend on location, income, and eligibility.
            </p>
          </div>

          <div className="mt-14 grid grid-cols-1 gap-8 sm:grid-cols-3">
            {FEATURED_CARS.map((car, i) => (
              <div
                key={car.model}
                className="group relative overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-lg transition-all duration-300 hover:shadow-2xl hover:-translate-y-1"
              >
                <div className="flex h-48 items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100 p-4">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={buildLogoUrl(car.make)}
                    alt={`${car.make}`}
                    className="h-20 w-20 object-contain transition-transform duration-500 group-hover:scale-110"
                  />
                </div>
                <div className="p-6">
                  <h4 className="text-lg font-bold text-gray-900">
                    {car.make} {car.model}
                  </h4>
                  <div className="mt-3 flex items-baseline gap-1">
                    <span className="text-xs font-medium uppercase tracking-wide text-gray-400">
                      {car.label}
                    </span>
                    <span className="bg-gradient-to-r from-emerald-600 to-green-600 bg-clip-text text-3xl font-black text-transparent">
                      {car.savings}
                    </span>
                  </div>
                  <p className="mt-2 text-xs text-gray-400">
                    in stackable incentives
                  </p>
                  <Link
                    href="/calculator"
                    className="mt-4 inline-flex w-full items-center justify-center gap-1.5 rounded-lg bg-indigo-50 py-2 text-xs font-semibold text-indigo-700 transition-colors hover:bg-indigo-100"
                  >
                    See deals
                    <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                    </svg>
                  </Link>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-10 text-center">
            <Link
              href="/calculator"
              className="inline-flex items-center gap-2 text-sm font-semibold text-indigo-600 transition-colors hover:text-indigo-500"
            >
              Find your car&apos;s savings
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </Link>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="bg-gradient-to-b from-slate-50 to-white px-4 py-20">
        <div className="mx-auto max-w-5xl">
          <div className="text-center">
            <p className="text-sm font-semibold uppercase tracking-widest text-indigo-600">
              Simple process
            </p>
            <h3 className="mt-2 text-3xl font-bold text-gray-900 sm:text-4xl">
              How It Works
            </h3>
          </div>
          <div className="mt-14 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {HOW_IT_WORKS.map((item) => (
              <div key={item.step} className="group text-center">
                <div className={`mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br ${item.color} text-white shadow-lg transition-all duration-300 group-hover:scale-110 group-hover:shadow-xl`}>
                  {item.icon}
                </div>
                <div className="mt-2 text-xs font-bold uppercase tracking-widest text-gray-300">
                  Step {item.step}
                </div>
                <h4 className="mt-2 font-bold text-gray-900">
                  {item.title}
                </h4>
                <p className="mt-2 text-sm leading-relaxed text-gray-500">
                  {item.description}
                </p>
              </div>
            ))}
          </div>
          <div className="mt-12 text-center">
            <Link
              href="/how-it-works"
              className="inline-flex items-center gap-2 text-sm font-semibold text-indigo-600 transition-colors hover:text-indigo-500"
            >
              Learn more about how it works
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </Link>
          </div>
        </div>
      </section>

      {/* Value prop */}
      <section className="px-4 py-20">
        <div className="mx-auto max-w-4xl">
          <div className="text-center">
            <p className="text-sm font-semibold uppercase tracking-widest text-indigo-600">
              Your advantage
            </p>
            <h3 className="mt-2 text-3xl font-bold text-gray-900 sm:text-4xl">
              Why Use IncentiveDrive?
            </h3>
          </div>
          <div className="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2">
            {[
              {
                title: "No Incentive Left Behind",
                desc: "We check state, manufacturer, utility, and affinity programs so you get the full picture.",
                gradient: "from-blue-500 to-cyan-500",
                bg: "bg-blue-50",
              },
              {
                title: "Smart Stacking",
                desc: "Our engine finds which incentives you can combine for maximum total savings.",
                gradient: "from-violet-500 to-purple-500",
                bg: "bg-violet-50",
              },
              {
                title: "Personalized Results",
                desc: "Your savings estimate is based on your location, income, vehicle choice, and background.",
                gradient: "from-emerald-500 to-green-500",
                bg: "bg-emerald-50",
              },
              {
                title: "Free, No Obligation",
                desc: "Use the calculator as many times as you want. Share your info only if you want dealer contact.",
                gradient: "from-amber-500 to-orange-500",
                bg: "bg-amber-50",
              },
            ].map((item) => (
              <div
                key={item.title}
                className={`group relative overflow-hidden rounded-2xl border border-gray-100 ${item.bg} p-6 transition-all duration-300 hover:shadow-lg hover:-translate-y-0.5`}
              >
                <div className={`absolute top-0 left-0 h-1 w-full bg-gradient-to-r ${item.gradient}`} />
                <h4 className="text-lg font-bold text-gray-900">{item.title}</h4>
                <p className="mt-2 text-sm leading-relaxed text-gray-600">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-gradient-to-br from-slate-900 via-indigo-950 to-blue-900 px-4 py-20 text-center">
        <div className="relative mx-auto max-w-2xl">
          <div className="absolute inset-0 -z-10">
            <div className="absolute top-0 right-0 h-48 w-48 rounded-full bg-blue-500/10 blur-3xl" />
            <div className="absolute bottom-0 left-0 h-48 w-48 rounded-full bg-indigo-500/10 blur-3xl" />
          </div>
          <h3 className="text-3xl font-bold text-white sm:text-4xl">
            Ready to claim your savings?
          </h3>
          <p className="mt-4 text-slate-400">
            Calculate your personalized incentives or connect directly with a dealer who knows your deals.
          </p>
          <div className="mt-8 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
            <Link
              href="/calculator"
              className="group inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-blue-500 to-indigo-500 px-8 py-4 text-base font-bold text-white shadow-2xl shadow-blue-500/25 transition-all duration-300 hover:shadow-blue-500/40 hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 focus:ring-offset-slate-900"
            >
              Calculate My Savings
              <svg className="h-5 w-5 transition-transform group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </Link>
            <Link
              href="/calculator"
              className="group inline-flex items-center gap-2 rounded-xl border-2 border-emerald-400/30 bg-emerald-500/10 px-8 py-4 text-base font-bold text-emerald-400 transition-all duration-300 hover:bg-emerald-500/20 hover:border-emerald-400/50 hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:ring-offset-2 focus:ring-offset-slate-900"
            >
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 01-.825-.242m9.345-8.334a2.126 2.126 0 00-.476-.095 48.64 48.64 0 00-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0011.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
              </svg>
              Connect with a Dealer
            </Link>
          </div>
          <p className="mt-4 text-xs text-slate-500">
            Free, no obligation -- your savings are calculated before any dealer contact
          </p>
        </div>
      </section>
    </>
  );
}
