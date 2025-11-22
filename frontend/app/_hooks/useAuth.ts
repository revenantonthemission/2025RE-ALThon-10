import { useAuthStore } from "@/app/_stores/auth";

/**
 * Custom hook for authentication operations
 * Provides convenient access to auth state and actions
 *
 * @example
 * ```tsx
 * import { useAuth } from '@/app/_hooks/useAuth';
 *
 * function MyComponent() {
 *   const { isAuthenticated, user, logout } = useAuth();
 *
 *   if (!isAuthenticated) {
 *     return <div>Please login</div>;
 *   }
 *
 *   return (
 *     <div>
 *       <h1>Welcome {user.name}!</h1>
 *       <button onClick={logout}>Logout</button>
 *     </div>
 *   );
 * }
 * ```
 */
export function useAuth() {
  const store = useAuthStore();

  return {
    // Auth state
    isAuthenticated: store.isAuthenticated,
    user: store.userInfo,
    accessToken: store.accessToken,
    memberId: store.memberId,
    role: store.role,

    // Auth actions
    logout: store.clearAuth,

    // Helper functions
    hasRole: (requiredRole: string) => store.role === requiredRole,
    isUser: () => store.role === "USER",
    isAdmin: () => store.role === "ADMIN",
  };
}
