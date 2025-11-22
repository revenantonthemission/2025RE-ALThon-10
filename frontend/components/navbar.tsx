import Link from 'next/link';

export function LandingNavbar() {
  return (
    <div className="navbar bg-base-100 shadow-lg">
      <div className="flex-1">
        <a className="btn btn-ghost text-xl">REALThon</a>
      </div>
      <div className="flex-none gap-2">
        <Link href="/login" className="btn btn-primary">
          Login
        </Link>
      </div>
    </div>
  );
}

