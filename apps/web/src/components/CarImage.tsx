"use client";

import { useState, useEffect } from "react";
import { getVehiclePhoto } from "@/lib/api";

interface CarImageProps {
  make: string;
  model: string;
  className?: string;
  size?: "sm" | "md" | "lg";
}

export default function CarImage({
  make,
  model,
  className = "",
  size = "md",
}: CarImageProps) {
  // undefined = loading, null = no photo, string = photo URL
  const [photoUrl, setPhotoUrl] = useState<string | null | undefined>(
    undefined
  );
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    if (!make || !model) {
      setPhotoUrl(null);
      return;
    }

    let cancelled = false;
    setPhotoUrl(undefined); // loading
    setLoaded(false);

    getVehiclePhoto(make, model)
      .then((res) => {
        if (!cancelled) setPhotoUrl(res.photoUrl ?? null);
      })
      .catch(() => {
        if (!cancelled) setPhotoUrl(null);
      });

    return () => {
      cancelled = true;
    };
  }, [make, model]);

  if (!make || !model) return null;

  // No photo available — show nothing
  if (photoUrl === null) return null;

  const heightClasses = {
    sm: "h-32",
    md: "h-40",
    lg: "h-48",
  };

  // Loading state — compact skeleton
  if (photoUrl === undefined) {
    return (
      <div
        className={`flex items-center justify-center rounded-xl bg-slate-100 ${heightClasses[size]} ${className}`}
      >
        <div className="h-6 w-6 animate-spin rounded-full border-3 border-indigo-500 border-t-transparent" />
      </div>
    );
  }

  return (
    <div className={`relative ${className}`}>
      {!loaded && (
        <div
          className={`flex items-center justify-center rounded-xl bg-slate-100 ${heightClasses[size]}`}
        >
          <div className="h-6 w-6 animate-spin rounded-full border-3 border-indigo-500 border-t-transparent" />
        </div>
      )}
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={photoUrl}
        alt={`${make} ${model}`}
        onLoad={() => setLoaded(true)}
        onError={() => setPhotoUrl(null)}
        className={`w-full rounded-xl object-contain transition-all duration-500 ${heightClasses[size]} ${
          loaded ? "opacity-100 scale-100" : "absolute inset-0 opacity-0 scale-95"
        }`}
      />
      {loaded && (
        <p className="mt-1.5 text-center text-sm font-semibold text-gray-700">
          {make} {model}
        </p>
      )}
    </div>
  );
}
