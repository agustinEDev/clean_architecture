import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { getHealthStatus, isServiceReady, HealthStatus } from '../../src/shared/health.js';

describe('Health Check Functions', () => {
  beforeEach(() => {
    // Mock process.uptime to return a consistent value for testing
    vi.spyOn(process, 'uptime').mockReturnValue(123.45);
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('getHealthStatus', () => {
    it('should return healthy status with default service name', () => {
      const result = getHealthStatus();
      
      expect(result.status).toBe('healthy');
      expect(result.service).toBe('TypeScript Clean Architecture');
      expect(result.uptime).toBe(123.45);
      expect(result.timestamp).toBeInstanceOf(Date);
    });

    it('should return healthy status with custom service name', () => {
      const serviceName = 'My Custom Service';
      const result = getHealthStatus(serviceName);
      
      expect(result.status).toBe('healthy');
      expect(result.service).toBe(serviceName);
      expect(result.uptime).toBe(123.45);
      expect(result.timestamp).toBeInstanceOf(Date);
    });

    it('should trim whitespace from service name', () => {
      const serviceName = '  My Service With Spaces  ';
      const result = getHealthStatus(serviceName);
      
      expect(result.status).toBe('healthy');
      expect(result.service).toBe('My Service With Spaces');
    });

    it('should return unhealthy status for empty service name', () => {
      const result = getHealthStatus('');
      
      expect(result.status).toBe('unhealthy');
      expect(result.service).toBe('Unknown Service');
      expect(result.uptime).toBe(123.45);
      expect(result.timestamp).toBeInstanceOf(Date);
    });

    it('should return unhealthy status for whitespace-only service name', () => {
      const result = getHealthStatus('   ');
      
      expect(result.status).toBe('unhealthy');
      expect(result.service).toBe('Unknown Service');
    });

    it('should have recent timestamp', () => {
      const beforeCall = new Date();
      const result = getHealthStatus();
      const afterCall = new Date();
      
      expect(result.timestamp.getTime()).toBeGreaterThanOrEqual(beforeCall.getTime());
      expect(result.timestamp.getTime()).toBeLessThanOrEqual(afterCall.getTime());
    });
  });

  describe('isServiceReady', () => {
    it('should return true when uptime is greater than 0', () => {
      vi.spyOn(process, 'uptime').mockReturnValue(1.5);
      
      expect(isServiceReady()).toBe(true);
    });

    it('should return false when uptime is 0', () => {
      vi.spyOn(process, 'uptime').mockReturnValue(0);
      
      expect(isServiceReady()).toBe(false);
    });

    it('should return false when uptime is negative (edge case)', () => {
      vi.spyOn(process, 'uptime').mockReturnValue(-1);
      
      expect(isServiceReady()).toBe(false);
    });
  });

  describe('HealthStatus interface compliance', () => {
    it('should return object that matches HealthStatus interface', () => {
      const result = getHealthStatus('Test Service');
      
      // Check all required properties exist
      expect(result).toHaveProperty('status');
      expect(result).toHaveProperty('timestamp');
      expect(result).toHaveProperty('uptime');
      expect(result).toHaveProperty('service');
      
      // Check types
      expect(typeof result.status).toBe('string');
      expect(['healthy', 'unhealthy']).toContain(result.status);
      expect(result.timestamp).toBeInstanceOf(Date);
      expect(typeof result.uptime).toBe('number');
      expect(typeof result.service).toBe('string');
    });
  });
});