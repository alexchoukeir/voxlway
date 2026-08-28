/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "export",
  trailingSlash: true,
  images: {
    unoptimized: true,
    remotePatterns: [
      {
        protocol: "https",
        hostname: "tr.rbxcdn.com",
        port: "",
        pathname: "/**",
      },
    ],
  },
};

export default nextConfig;
