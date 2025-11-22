import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  // Proxy API requests to backend (optional - use if you want Next.js to handle routing)
  // Uncomment the rewrites section if you want to proxy through Next.js instead of nginx
  /*
  async rewrites() {
    const backendUrl = process.env.BACKEND_URL || "http://localhost:8000";
    return [
      {
        source: "/api/:path*",
        destination: `${backendUrl}/:path*`,
      },
      // Also handle direct backend routes
      {
        source: "/:path((courses|oauth2|social|email|me))",
        destination: `${backendUrl}/:path*`,
      },
    ];
  },
  */
};

export default nextConfig;
