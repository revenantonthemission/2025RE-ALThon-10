interface FormHeaderProps {
  title: string;
  description: string;
}

export function FormHeader({ title, description }: FormHeaderProps) {
  return (
    <div className="text-center space-y-2">
      <h2 className="text-3xl font-bold text-primary">{title}</h2>
      <p className="text-base-content/70">{description}</p>
    </div>
  );
}
