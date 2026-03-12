export const VEHICLE_MAKES = [
  "Acura", "Audi", "BMW", "Buick", "Cadillac", "Chevrolet", "Chrysler",
  "Dodge", "Ford", "Genesis", "GMC", "Honda", "Hyundai", "Infiniti",
  "Jaguar", "Jeep", "Kia", "Land Rover", "Lexus", "Lincoln", "Lucid",
  "Mazda", "Mercedes-Benz", "MINI", "Mitsubishi", "Nissan", "Polestar",
  "Porsche", "Ram", "Rivian", "Subaru", "Tesla", "Toyota", "Volkswagen",
  "Volvo",
] as const;

export type FuelTypeKey = "BEV" | "PHEV" | "FCEV" | "ICE";

export interface VehicleModelInfo {
  name: string;
  fuelTypes: FuelTypeKey[];
}

export const VEHICLE_MODELS: Record<string, VehicleModelInfo[]> = {
  Acura: [
    { name: "Integra", fuelTypes: ["ICE"] },
    { name: "MDX", fuelTypes: ["ICE"] },
    { name: "RDX", fuelTypes: ["ICE"] },
    { name: "TLX", fuelTypes: ["ICE"] },
    { name: "ZDX", fuelTypes: ["BEV"] },
  ],
  Audi: [
    { name: "A4", fuelTypes: ["ICE"] },
    { name: "A6", fuelTypes: ["ICE"] },
    { name: "e-tron", fuelTypes: ["BEV"] },
    { name: "e-tron GT", fuelTypes: ["BEV"] },
    { name: "Q4 e-tron", fuelTypes: ["BEV"] },
    { name: "Q5", fuelTypes: ["ICE", "PHEV"] },
    { name: "Q7", fuelTypes: ["ICE"] },
    { name: "Q8 e-tron", fuelTypes: ["BEV"] },
  ],
  BMW: [
    { name: "i4", fuelTypes: ["BEV"] },
    { name: "i5", fuelTypes: ["BEV"] },
    { name: "i7", fuelTypes: ["BEV"] },
    { name: "iX", fuelTypes: ["BEV"] },
    { name: "X1", fuelTypes: ["ICE"] },
    { name: "X3", fuelTypes: ["ICE", "PHEV"] },
    { name: "X5", fuelTypes: ["ICE", "PHEV"] },
    { name: "3 Series", fuelTypes: ["ICE"] },
    { name: "5 Series", fuelTypes: ["ICE", "PHEV"] },
  ],
  Buick: [
    { name: "Enclave", fuelTypes: ["ICE"] },
    { name: "Encore GX", fuelTypes: ["ICE"] },
    { name: "Envista", fuelTypes: ["ICE"] },
  ],
  Cadillac: [
    { name: "CT5", fuelTypes: ["ICE"] },
    { name: "Escalade", fuelTypes: ["ICE"] },
    { name: "Escalade IQ", fuelTypes: ["BEV"] },
    { name: "LYRIQ", fuelTypes: ["BEV"] },
    { name: "XT4", fuelTypes: ["ICE"] },
    { name: "XT5", fuelTypes: ["ICE"] },
  ],
  Chevrolet: [
    { name: "Blazer EV", fuelTypes: ["BEV"] },
    { name: "Bolt EUV", fuelTypes: ["BEV"] },
    { name: "Equinox EV", fuelTypes: ["BEV"] },
    { name: "Silverado EV", fuelTypes: ["BEV"] },
    { name: "Trax", fuelTypes: ["ICE"] },
    { name: "Equinox", fuelTypes: ["ICE"] },
    { name: "Traverse", fuelTypes: ["ICE"] },
  ],
  Chrysler: [
    { name: "Pacifica", fuelTypes: ["ICE"] },
    { name: "Pacifica Hybrid", fuelTypes: ["PHEV"] },
  ],
  Dodge: [
    { name: "Charger Daytona", fuelTypes: ["BEV"] },
    { name: "Hornet", fuelTypes: ["ICE", "PHEV"] },
  ],
  Ford: [
    { name: "Bronco", fuelTypes: ["ICE"] },
    { name: "Edge", fuelTypes: ["ICE"] },
    { name: "Escape", fuelTypes: ["ICE", "PHEV"] },
    { name: "Explorer", fuelTypes: ["ICE"] },
    { name: "F-150", fuelTypes: ["ICE"] },
    { name: "F-150 Lightning", fuelTypes: ["BEV"] },
    { name: "Maverick", fuelTypes: ["ICE"] },
    { name: "Mustang Mach-E", fuelTypes: ["BEV"] },
  ],
  Genesis: [
    { name: "Electrified G80", fuelTypes: ["BEV"] },
    { name: "Electrified GV70", fuelTypes: ["BEV"] },
    { name: "G70", fuelTypes: ["ICE"] },
    { name: "G80", fuelTypes: ["ICE"] },
    { name: "GV60", fuelTypes: ["BEV"] },
    { name: "GV70", fuelTypes: ["ICE"] },
    { name: "GV80", fuelTypes: ["ICE"] },
  ],
  GMC: [
    { name: "Hummer EV", fuelTypes: ["BEV"] },
    { name: "Sierra EV", fuelTypes: ["BEV"] },
    { name: "Terrain", fuelTypes: ["ICE"] },
    { name: "Yukon", fuelTypes: ["ICE"] },
  ],
  Honda: [
    { name: "Accord", fuelTypes: ["ICE"] },
    { name: "Civic", fuelTypes: ["ICE"] },
    { name: "CR-V", fuelTypes: ["ICE", "PHEV"] },
    { name: "HR-V", fuelTypes: ["ICE"] },
    { name: "Pilot", fuelTypes: ["ICE"] },
    { name: "Prologue", fuelTypes: ["BEV"] },
  ],
  Hyundai: [
    { name: "Elantra", fuelTypes: ["ICE"] },
    { name: "IONIQ 5", fuelTypes: ["BEV"] },
    { name: "IONIQ 6", fuelTypes: ["BEV"] },
    { name: "IONIQ 9", fuelTypes: ["BEV"] },
    { name: "Kona", fuelTypes: ["ICE"] },
    { name: "Kona Electric", fuelTypes: ["BEV"] },
    { name: "Palisade", fuelTypes: ["ICE"] },
    { name: "Santa Fe", fuelTypes: ["ICE", "PHEV"] },
    { name: "Sonata", fuelTypes: ["ICE"] },
    { name: "Tucson", fuelTypes: ["ICE", "PHEV"] },
  ],
  Infiniti: [
    { name: "Q50", fuelTypes: ["ICE"] },
    { name: "QX50", fuelTypes: ["ICE"] },
    { name: "QX55", fuelTypes: ["ICE"] },
    { name: "QX60", fuelTypes: ["ICE"] },
    { name: "QX80", fuelTypes: ["ICE"] },
  ],
  Jaguar: [
    { name: "F-PACE", fuelTypes: ["ICE"] },
    { name: "I-PACE", fuelTypes: ["BEV"] },
  ],
  Jeep: [
    { name: "Grand Cherokee", fuelTypes: ["ICE"] },
    { name: "Grand Cherokee 4xe", fuelTypes: ["PHEV"] },
    { name: "Wagoneer", fuelTypes: ["ICE"] },
    { name: "Wrangler", fuelTypes: ["ICE"] },
    { name: "Wrangler 4xe", fuelTypes: ["PHEV"] },
  ],
  Kia: [
    { name: "EV6", fuelTypes: ["BEV"] },
    { name: "EV9", fuelTypes: ["BEV"] },
    { name: "Forte", fuelTypes: ["ICE"] },
    { name: "K5", fuelTypes: ["ICE"] },
    { name: "Niro EV", fuelTypes: ["BEV"] },
    { name: "Seltos", fuelTypes: ["ICE"] },
    { name: "Sorento", fuelTypes: ["ICE", "PHEV"] },
    { name: "Sportage", fuelTypes: ["ICE", "PHEV"] },
    { name: "Telluride", fuelTypes: ["ICE"] },
  ],
  "Land Rover": [
    { name: "Defender", fuelTypes: ["ICE", "PHEV"] },
    { name: "Discovery", fuelTypes: ["ICE"] },
    { name: "Range Rover", fuelTypes: ["ICE", "PHEV"] },
    { name: "Range Rover Sport", fuelTypes: ["ICE", "PHEV"] },
  ],
  Lexus: [
    { name: "NX", fuelTypes: ["ICE", "PHEV"] },
    { name: "RX", fuelTypes: ["ICE", "PHEV"] },
    { name: "RZ", fuelTypes: ["BEV"] },
    { name: "TX", fuelTypes: ["ICE"] },
    { name: "UX", fuelTypes: ["ICE"] },
  ],
  Lincoln: [
    { name: "Aviator", fuelTypes: ["ICE", "PHEV"] },
    { name: "Corsair", fuelTypes: ["ICE", "PHEV"] },
    { name: "Nautilus", fuelTypes: ["ICE"] },
  ],
  Lucid: [
    { name: "Air", fuelTypes: ["BEV"] },
    { name: "Gravity", fuelTypes: ["BEV"] },
  ],
  Mazda: [
    { name: "CX-30", fuelTypes: ["ICE"] },
    { name: "CX-5", fuelTypes: ["ICE"] },
    { name: "CX-50", fuelTypes: ["ICE"] },
    { name: "CX-70", fuelTypes: ["ICE", "PHEV"] },
    { name: "CX-90", fuelTypes: ["ICE", "PHEV"] },
    { name: "Mazda3", fuelTypes: ["ICE"] },
  ],
  "Mercedes-Benz": [
    { name: "C-Class", fuelTypes: ["ICE"] },
    { name: "E-Class", fuelTypes: ["ICE"] },
    { name: "EQB", fuelTypes: ["BEV"] },
    { name: "EQE", fuelTypes: ["BEV"] },
    { name: "EQS", fuelTypes: ["BEV"] },
    { name: "GLC", fuelTypes: ["ICE"] },
    { name: "GLE", fuelTypes: ["ICE", "PHEV"] },
    { name: "S-Class", fuelTypes: ["ICE", "PHEV"] },
  ],
  MINI: [
    { name: "Countryman", fuelTypes: ["ICE"] },
    { name: "Cooper", fuelTypes: ["ICE"] },
    { name: "Cooper Electric", fuelTypes: ["BEV"] },
  ],
  Mitsubishi: [
    { name: "Eclipse Cross", fuelTypes: ["ICE", "PHEV"] },
    { name: "Outlander", fuelTypes: ["ICE"] },
    { name: "Outlander PHEV", fuelTypes: ["PHEV"] },
  ],
  Nissan: [
    { name: "Altima", fuelTypes: ["ICE"] },
    { name: "ARIYA", fuelTypes: ["BEV"] },
    { name: "LEAF", fuelTypes: ["BEV"] },
    { name: "Murano", fuelTypes: ["ICE"] },
    { name: "Pathfinder", fuelTypes: ["ICE"] },
    { name: "Rogue", fuelTypes: ["ICE"] },
    { name: "Sentra", fuelTypes: ["ICE"] },
  ],
  Polestar: [
    { name: "Polestar 2", fuelTypes: ["BEV"] },
    { name: "Polestar 3", fuelTypes: ["BEV"] },
    { name: "Polestar 4", fuelTypes: ["BEV"] },
  ],
  Porsche: [
    { name: "Cayenne", fuelTypes: ["ICE", "PHEV"] },
    { name: "Macan", fuelTypes: ["ICE"] },
    { name: "Macan Electric", fuelTypes: ["BEV"] },
    { name: "Taycan", fuelTypes: ["BEV"] },
  ],
  Ram: [
    { name: "1500", fuelTypes: ["ICE"] },
    { name: "1500 REV", fuelTypes: ["BEV"] },
  ],
  Rivian: [
    { name: "R1S", fuelTypes: ["BEV"] },
    { name: "R1T", fuelTypes: ["BEV"] },
    { name: "R2", fuelTypes: ["BEV"] },
  ],
  Subaru: [
    { name: "Crosstrek", fuelTypes: ["ICE"] },
    { name: "Forester", fuelTypes: ["ICE"] },
    { name: "Impreza", fuelTypes: ["ICE"] },
    { name: "Outback", fuelTypes: ["ICE"] },
    { name: "Solterra", fuelTypes: ["BEV"] },
  ],
  Tesla: [
    { name: "Model 3", fuelTypes: ["BEV"] },
    { name: "Model S", fuelTypes: ["BEV"] },
    { name: "Model X", fuelTypes: ["BEV"] },
    { name: "Model Y", fuelTypes: ["BEV"] },
    { name: "Cybertruck", fuelTypes: ["BEV"] },
  ],
  Toyota: [
    { name: "bZ4X", fuelTypes: ["BEV"] },
    { name: "Camry", fuelTypes: ["ICE"] },
    { name: "Corolla", fuelTypes: ["ICE"] },
    { name: "GR86", fuelTypes: ["ICE"] },
    { name: "Highlander", fuelTypes: ["ICE"] },
    { name: "Prius", fuelTypes: ["ICE"] },
    { name: "Prius Prime", fuelTypes: ["PHEV"] },
    { name: "RAV4", fuelTypes: ["ICE"] },
    { name: "RAV4 Prime", fuelTypes: ["PHEV"] },
    { name: "Tacoma", fuelTypes: ["ICE"] },
    { name: "Tundra", fuelTypes: ["ICE"] },
  ],
  Volkswagen: [
    { name: "Atlas", fuelTypes: ["ICE"] },
    { name: "ID.4", fuelTypes: ["BEV"] },
    { name: "ID.Buzz", fuelTypes: ["BEV"] },
    { name: "Jetta", fuelTypes: ["ICE"] },
    { name: "Taos", fuelTypes: ["ICE"] },
    { name: "Tiguan", fuelTypes: ["ICE"] },
  ],
  Volvo: [
    { name: "C40 Recharge", fuelTypes: ["BEV"] },
    { name: "EX30", fuelTypes: ["BEV"] },
    { name: "EX90", fuelTypes: ["BEV"] },
    { name: "S60", fuelTypes: ["ICE", "PHEV"] },
    { name: "XC40 Recharge", fuelTypes: ["BEV"] },
    { name: "XC60", fuelTypes: ["ICE", "PHEV"] },
    { name: "XC90", fuelTypes: ["ICE", "PHEV"] },
  ],
};

export const INCOME_RANGES = [
  { value: "under_30k", label: "Under $30,000" },
  { value: "30k_50k", label: "$30,000 - $50,000" },
  { value: "50k_75k", label: "$50,000 - $75,000" },
  { value: "75k_100k", label: "$75,000 - $100,000" },
  { value: "100k_150k", label: "$100,000 - $150,000" },
  { value: "150k_200k", label: "$150,000 - $200,000" },
  { value: "200k_300k", label: "$200,000 - $300,000" },
  { value: "over_300k", label: "Over $300,000" },
  { value: "prefer_not", label: "Prefer not to say" },
] as const;

export const FILING_STATUSES = [
  { value: "single", label: "Single" },
  { value: "married_joint", label: "Married Filing Jointly" },
  { value: "married_separate", label: "Married Filing Separately" },
  { value: "head_of_household", label: "Head of Household" },
] as const;

export const BUDGET_RANGES = [
  { min: 15000, max: 25000 },
  { min: 25000, max: 35000 },
  { min: 35000, max: 50000 },
  { min: 50000, max: 75000 },
  { min: 75000, max: 100000 },
  { min: 100000, max: 150000 },
] as const;

export const AFFINITY_OPTIONS = [
  { value: "military", label: "Active Military or Veteran" },
  { value: "educator", label: "Educator / Teacher" },
  { value: "first_responder", label: "First Responder (Police, Fire, EMS)" },
  { value: "college_grad", label: "Recent College Graduate" },
  { value: "loyalty", label: "Current Brand Owner (Loyalty)" },
] as const;

export const TCPA_CONSENT_TEXT =
  'By clicking "Submit," I consent to receive marketing calls and text messages from IncentiveDrive and its authorized dealer partners at the phone number provided above, including calls made using an automatic telephone dialing system or prerecorded voice. I understand that my consent is not a condition of any purchase. Message and data rates may apply. I can revoke my consent at any time.';
