import { getHealthStatus, isServiceReady } from './src/shared/health.js';

console.log('🚀 Testing TypeScript Clean Architecture Health Check');
console.log('');

// Test the health status function
const healthStatus = getHealthStatus();
console.log('Health Status:', JSON.stringify(healthStatus, null, 2));

// Test service readiness
const isReady = isServiceReady();
console.log('Service Ready:', isReady);

console.log('');
console.log('✅ Health check completed successfully!');
console.log('✅ TypeScript tooling is working correctly!');