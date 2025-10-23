/**
 * Health check utility for verifying the application status
 */
export interface HealthStatus {
  status: 'healthy' | 'unhealthy';
  timestamp: Date;
  uptime: number;
  service: string;
}

/**
 * Simple health check function
 * @param serviceName The name of the service to check
 * @returns HealthStatus object indicating the health of the service
 */
export function getHealthStatus(serviceName: string = 'TypeScript Clean Architecture'): HealthStatus {
  if (!serviceName || serviceName.trim().length === 0) {
    return {
      status: 'unhealthy',
      timestamp: new Date(),
      uptime: process.uptime(),
      service: 'Unknown Service'
    };
  }

  return {
    status: 'healthy',
    timestamp: new Date(),
    uptime: process.uptime(),
    service: serviceName.trim()
  };
}

/**
 * Check if the service is ready
 * @returns boolean indicating if the service is ready
 */
export function isServiceReady(): boolean {
  return process.uptime() > 0;
}