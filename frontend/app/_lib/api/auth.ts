import {
  SocialLoginResponse,
  EmailLoginRequest,
  EmailSignupRequest,
  EmailAuthResponse,
} from "@/app/_types/auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

/**
 * Initiates Google OAuth login by redirecting to backend
 */
export function initiateGoogleLogin() {
  window.location.href = `${API_URL}/oauth2/authorization/google`;
}

/**
 * Exchanges the HttpOnly refresh token cookie for an access token
 * This should be called immediately after successful OAuth redirect
 */
export async function exchangeTokenFromCookie(): Promise<SocialLoginResponse> {
  const response = await fetch(`${API_URL}/social/token`, {
    method: "POST",
    credentials: "include", // Critical: sends HttpOnly cookie
    headers: {
      "Content-Type": "application/json",
    },
  });
  console.log(response);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || "Token exchange failed");
  }

  return response.json();
}

/**
 * Login with email and password
 */
export async function loginWithEmailPassword(
  credentials: EmailLoginRequest
): Promise<EmailAuthResponse> {
  const response = await fetch(`${API_URL}/email/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  });

  const data = await response.json();

  if (!response.ok || !data.success) {
    return data;
  }

  return data;
}

/**
 * Sign up with email and password
 */
export async function signupWithEmailPassword(
  credentials: EmailSignupRequest
): Promise<EmailAuthResponse> {
  const response = await fetch(`${API_URL}/email/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  });

  const data = await response.json();

  if (!response.ok || !data.success) {
    return data;
  }

  return data;
}

/**
 * Get current user information from /me endpoint
 */
export async function getCurrentUser(accessToken: string) {
  const response = await fetch(`${API_URL}/me`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch user information");
  }

  return response.json();
}
