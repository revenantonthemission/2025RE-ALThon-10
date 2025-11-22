export interface UserInfo {
  id: string;
  nickname: string;
  name: string;
  email: string;
  gender: string;
}

export interface SocialLoginResponse {
  success: boolean;
  data: {
    accessToken: string;
    tokenType: string;
    memberId: string;
    role: string;
    userInfo: UserInfo;
  };
  message: string;
}

export interface AuthError {
  success: false;
  error: string;
  details: string;
  timestamp: number;
}

// Email auth types
export interface EmailLoginRequest {
  email: string;
  password: string;
}

export interface EmailSignupRequest {
  email: string;
  password: string;
  name: string;
  nickname?: string;
}

export interface EmailAuthApiError {
  code: number;
  field?: string;
  message: string;
  description: string;
}

export interface EmailAuthResponse {
  success: boolean;
  message: string;
  timestamp: string;
  data?: {
    success: boolean;
    token: string;
    tokenType: string;
    userId: string;
    email: string;
    nickname: string;
    name: string;
  };
  error?: EmailAuthApiError;
}

export interface AuthState {
  accessToken: string | null;
  tokenType: string;
  memberId: string | null;
  role: string | null;
  userInfo: UserInfo | null;
  isAuthenticated: boolean;
  setAuth: (
    data: SocialLoginResponse["data"] | EmailAuthResponse["data"]
  ) => void;
  clearAuth: () => void;
}
