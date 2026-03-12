"use client";

const STEP_LABELS = [
  "Location & Vehicle",
  "Preferences",
  "Eligibility",
  "Affiliations",
];

export default function ProgressBar({ currentStep }: { currentStep: number }) {
  return (
    <nav aria-label="Calculator progress" className="mb-8">
      <ol className="flex items-center gap-2">
        {STEP_LABELS.map((label, i) => {
          const step = i + 1;
          const isActive = step === currentStep;
          const isComplete = step < currentStep;
          return (
            <li key={step} className="flex flex-1 flex-col items-center gap-1">
              <div className="flex w-full items-center">
                <div
                  className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-sm font-semibold ${
                    isComplete
                      ? "bg-blue-600 text-white"
                      : isActive
                        ? "border-2 border-blue-600 text-blue-600"
                        : "border-2 border-gray-300 text-gray-400"
                  }`}
                  aria-current={isActive ? "step" : undefined}
                >
                  {isComplete ? (
                    <svg className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  ) : (
                    step
                  )}
                </div>
                {i < STEP_LABELS.length - 1 && (
                  <div
                    className={`mx-2 h-0.5 flex-1 ${
                      isComplete ? "bg-blue-600" : "bg-gray-300"
                    }`}
                  />
                )}
              </div>
              <span
                className={`text-xs ${
                  isActive ? "font-semibold text-blue-600" : "text-gray-500"
                } hidden sm:block`}
              >
                {label}
              </span>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
