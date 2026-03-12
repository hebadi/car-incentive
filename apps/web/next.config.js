/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  transpilePackages: ["@incentive-drive/shared"],
};

module.exports = nextConfig;
