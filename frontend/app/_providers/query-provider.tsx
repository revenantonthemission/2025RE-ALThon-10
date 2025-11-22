'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState, useEffect, useRef } from 'react';

const CACHE_KEY = 'REACT_QUERY_CACHE';
const CACHE_VERSION = '1';

interface CacheEntry {
  data: Record<string, any>;
  timestamp: number;
  version: string;
}

// Restore cache from localStorage
function restoreCache(): Record<string, any> | undefined {
  if (typeof window === 'undefined') return undefined;
  
  try {
    const cached = localStorage.getItem(CACHE_KEY);
    if (cached) {
      const entry: CacheEntry = JSON.parse(cached);
      // Check version and if cache is still valid (not older than 30 minutes)
      if (
        entry.version === CACHE_VERSION &&
        entry.timestamp &&
        Date.now() - entry.timestamp < 30 * 60 * 1000
      ) {
        return entry.data;
      } else {
        // Clear old cache
        localStorage.removeItem(CACHE_KEY);
      }
    }
  } catch (error) {
    console.error('Failed to restore cache:', error);
    localStorage.removeItem(CACHE_KEY);
  }
  return undefined;
}

// Save cache to localStorage
function saveCache(data: Record<string, any>) {
  if (typeof window === 'undefined') return;
  
  try {
    const entry: CacheEntry = {
      data,
      timestamp: Date.now(),
      version: CACHE_VERSION,
    };
    localStorage.setItem(CACHE_KEY, JSON.stringify(entry));
  } catch (error) {
    console.error('Failed to save cache:', error);
  }
}

export function QueryProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => {
    const client = new QueryClient({
      defaultOptions: {
        queries: {
          staleTime: Infinity, // Data never becomes stale - use cache until explicitly invalidated
          gcTime: 30 * 60 * 1000, // 30 minutes - keep in cache for 30 minutes
          refetchOnMount: false, // Don't refetch on mount if data exists
          refetchOnWindowFocus: false, // Don't refetch on window focus
          refetchOnReconnect: false, // Don't refetch on reconnect
        },
      },
    });

    // Restore cache on initialization
    const cachedData = restoreCache();
    if (cachedData) {
      try {
        // Restore queries from cache
        Object.entries(cachedData).forEach(([key, value]) => {
          try {
            const queryKey = JSON.parse(key);
            client.setQueryData(queryKey, value);
          } catch (e) {
            // Skip invalid keys
          }
        });
      } catch (error) {
        console.error('Failed to restore queries from cache:', error);
      }
    }

    return client;
  });

  const saveTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  // Save cache when queries update
  useEffect(() => {
    const saveCacheData = () => {
      if (saveTimeoutRef.current) {
        clearTimeout(saveTimeoutRef.current);
      }

      saveTimeoutRef.current = setTimeout(() => {
        const cache = queryClient.getQueryCache();
        const queries = cache.getAll();
        const cacheData: Record<string, any> = {};
        
        queries.forEach((query) => {
          if (query.state.data && query.state.status === 'success') {
            try {
              cacheData[JSON.stringify(query.queryKey)] = query.state.data;
            } catch (e) {
              // Skip queries with non-serializable keys
            }
          }
        });

        if (Object.keys(cacheData).length > 0) {
          saveCache(cacheData);
        }
      }, 500);
    };

    const unsubscribe = queryClient.getQueryCache().subscribe((event) => {
      if (event?.type === 'updated' && event.query.state.data) {
        saveCacheData();
      }
    });

    // Also save periodically
    const interval = setInterval(saveCacheData, 5000);

    return () => {
      unsubscribe();
      clearInterval(interval);
      if (saveTimeoutRef.current) {
        clearTimeout(saveTimeoutRef.current);
      }
      // Final save on unmount
      const cache = queryClient.getQueryCache();
      const queries = cache.getAll();
      const cacheData: Record<string, any> = {};
      
      queries.forEach((query) => {
        if (query.state.data && query.state.status === 'success') {
          try {
            cacheData[JSON.stringify(query.queryKey)] = query.state.data;
          } catch (e) {
            // Skip queries with non-serializable keys
          }
        }
      });

      if (Object.keys(cacheData).length > 0) {
        saveCache(cacheData);
      }
    };
  }, [queryClient]);

  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}
