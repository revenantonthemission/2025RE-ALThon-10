interface AuthCardProps {
  title: string;
  subtitle: string;
  children: React.ReactNode;
}

export function AuthCard({ title, subtitle, children }: AuthCardProps) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-base-200 p-4">
      <div className="card w-full max-w-md bg-base-100 shadow-xl">
        <div className="card-body">
          <h2 className="card-title text-3xl font-bold text-center justify-center mb-2">
            {title}
          </h2>
          <p className="text-center text-base-content/70 mb-6">
            {subtitle}
          </p>
          {children}
        </div>
      </div>
    </div>
  );
}

