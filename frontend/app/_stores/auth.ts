import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import {
  AuthState,
  EmailAuthResponse,
  SocialLoginResponse,
} from "@/app/_types/auth";

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      accessToken: null,
      tokenType: "Bearer",
      memberId: null,
      role: null,
      userInfo: null,
      isAuthenticated: false,

      setAuth: (
        data: SocialLoginResponse["data"] | EmailAuthResponse["data"]
      ) => {
        if (!data) return;

        // Handle OAuth response
        if ("accessToken" in data && data.accessToken) {
          set({
            accessToken: data.accessToken,
            tokenType: data.tokenType,
            memberId: data.memberId,
            role: data.role,
            userInfo: data.userInfo,
            isAuthenticated: true,
          });
        }
        // Handle email auth response
        else if ("token" in data && data.token) {
          set({
            accessToken: data.token,
            tokenType: data.tokenType || "Bearer",
            memberId: data.userId,
            role: "USER", // Default role for email auth
            userInfo: {
              id: data.userId,
              email: data.email,
              nickname: data.nickname,
              name: data.name,
              gender: "", // Not provided in email auth
            },
            isAuthenticated: true,
          });
        }
      },

      clearAuth: () =>
        set({
          accessToken: null,
          tokenType: "Bearer",
          memberId: null,
          role: null,
          userInfo: null,
          isAuthenticated: false,
        }),
    }),
    {
      name: "auth-storage",
      storage: createJSONStorage(() => localStorage),
    }
  )
);
