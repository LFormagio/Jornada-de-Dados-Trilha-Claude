import { useState, useEffect, useRef, useCallback } from 'react';

interface UseQueryOptions<T> {
  onSuccess?: (data: T) => void;
  onError?: (error: Error) => void;
  enabled?: boolean;
}

export function useQuery<T>(
  key: string,
  url: string,
  options?: UseQueryOptions<T>
) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [loading, setLoading] = useState(false);

  const optionsRef = useRef(options);
  useEffect(() => {
    optionsRef.current = options;
  });

  const refetch = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error('Network response was not ok');
      const result = await response.json();
      setData(result);
      optionsRef.current?.onSuccess?.(result);
    } catch (err) {
      const error = err as Error;
      setError(error);
      optionsRef.current?.onError?.(error);
    } finally {
      setLoading(false);
    }
  }, [url]);

  const enabled = options?.enabled !== false;

  useEffect(() => {
    if (enabled) {
      refetch();
    }
  }, [key, enabled, refetch]);

  return { data, error, loading, refetch };
}
