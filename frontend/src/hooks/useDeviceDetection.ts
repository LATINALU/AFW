/**
 * Device Detection Hook v1.0.0
 * =============================
 * Detecta el tipo de dispositivo y proporciona información sobre el entorno móvil.
 */

import { useState, useEffect } from 'react';

export type DeviceType = 'mobile' | 'tablet' | 'desktop';

export interface DeviceInfo {
  type: DeviceType;
  isMobile: boolean;
  isTablet: boolean;
  isDesktop: boolean;
  isTouchDevice: boolean;
  screenWidth: number;
  screenHeight: number;
  orientation: 'portrait' | 'landscape';
  os: 'ios' | 'android' | 'windows' | 'macos' | 'linux' | 'unknown';
  browser: string;
}

export function useDeviceDetection(): DeviceInfo {
  const [deviceInfo, setDeviceInfo] = useState<DeviceInfo>(() => 
    getDeviceInfo()
  );

  useEffect(() => {
    const handleResize = () => {
      setDeviceInfo(getDeviceInfo());
    };

    const handleOrientationChange = () => {
      setTimeout(() => {
        setDeviceInfo(getDeviceInfo());
      }, 100);
    };

    window.addEventListener('resize', handleResize);
    window.addEventListener('orientationchange', handleOrientationChange);

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('orientationchange', handleOrientationChange);
    };
  }, []);

  return deviceInfo;
}

function getDeviceInfo(): DeviceInfo {
  if (typeof window === 'undefined') {
    return {
      type: 'desktop',
      isMobile: false,
      isTablet: false,
      isDesktop: true,
      isTouchDevice: false,
      screenWidth: 1920,
      screenHeight: 1080,
      orientation: 'landscape',
      os: 'unknown',
      browser: 'unknown',
    };
  }

  const width = window.innerWidth;
  const height = window.innerHeight;
  const userAgent = navigator.userAgent.toLowerCase();

  // Detectar tipo de dispositivo
  let type: DeviceType = 'desktop';
  if (width < 768) {
    type = 'mobile';
  } else if (width >= 768 && width < 1024) {
    type = 'tablet';
  }

  // Detectar touch
  const isTouchDevice = 
    'ontouchstart' in window ||
    navigator.maxTouchPoints > 0 ||
    // @ts-ignore
    navigator.msMaxTouchPoints > 0;

  // Detectar OS
  let os: DeviceInfo['os'] = 'unknown';
  if (/iphone|ipad|ipod/.test(userAgent)) {
    os = 'ios';
  } else if (/android/.test(userAgent)) {
    os = 'android';
  } else if (/windows/.test(userAgent)) {
    os = 'windows';
  } else if (/mac/.test(userAgent)) {
    os = 'macos';
  } else if (/linux/.test(userAgent)) {
    os = 'linux';
  }

  // Detectar browser
  let browser = 'unknown';
  if (/chrome/.test(userAgent) && !/edge/.test(userAgent)) {
    browser = 'chrome';
  } else if (/safari/.test(userAgent) && !/chrome/.test(userAgent)) {
    browser = 'safari';
  } else if (/firefox/.test(userAgent)) {
    browser = 'firefox';
  } else if (/edge/.test(userAgent)) {
    browser = 'edge';
  }

  // Detectar orientación
  const orientation: 'portrait' | 'landscape' = 
    width > height ? 'landscape' : 'portrait';

  return {
    type,
    isMobile: type === 'mobile',
    isTablet: type === 'tablet',
    isDesktop: type === 'desktop',
    isTouchDevice,
    screenWidth: width,
    screenHeight: height,
    orientation,
    os,
    browser,
  };
}

/**
 * Hook para detectar si el dispositivo está en modo móvil
 */
export function useIsMobile(): boolean {
  const { isMobile } = useDeviceDetection();
  return isMobile;
}

/**
 * Hook para detectar si el dispositivo es táctil
 */
export function useIsTouchDevice(): boolean {
  const { isTouchDevice } = useDeviceDetection();
  return isTouchDevice;
}
