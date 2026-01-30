/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  async rewrites() {
    // El proxy Next.js se ejecuta dentro del contenedor Docker
    // por lo que debe usar el nombre del servicio Docker
    const apiUrl = process.env.NODE_ENV === 'production' 
      ? 'http://backend:8001'  // Dentro de Docker
      : 'http://localhost:8001';  // Desarrollo local
    
    return [
      {
        source: '/api/:path*',
        destination: `${apiUrl}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
