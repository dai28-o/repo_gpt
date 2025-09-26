import type { ReactNode } from 'react';
import { render, screen } from '@testing-library/react';
import DashboardPage from '@/app/dashboard/page';
import { AuthProvider } from '@/components/auth-provider';

function renderWithProviders(component: ReactNode) {
  return render(<AuthProvider>{component}</AuthProvider>);
}

describe('DashboardPage', () => {
  it('requires authentication', () => {
    renderWithProviders(<DashboardPage />);
    expect(screen.getByText(/You need to sign in/)).toBeInTheDocument();
  });
});
