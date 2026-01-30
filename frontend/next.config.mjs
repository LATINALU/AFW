/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  async rewrites() {
    // El proxy Next.js se ejecuta dentro del contenedor Docker
    // Usa el nombre del servicio Docker definido en docker-compose.afw.yml
    const apiUrl = process.env.BACKEND_URL || 'http://afw-backend:8001';
    
    return [
      {
        source: '/api/:path*',
        destination: `${apiUrl}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
