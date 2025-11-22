interface ErrorMessageProps {
  message?: string;
}

export function ErrorMessage({ message }: ErrorMessageProps) {
  if (!message) return null;

  return (
    <span className="text-error text-sm flex items-center gap-1">
      ⚠️ {message}
    </span>
  );
}
