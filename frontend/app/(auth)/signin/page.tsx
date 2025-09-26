'use client';

import { Button, Container, PasswordInput, Stack, TextInput, Title } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { useRouter } from 'next/navigation';
import { FormEvent, useState } from 'react';
import { useAuth } from '@/components/auth-provider';
import { apiRequest } from '@/lib/api';

export default function SignInPage() {
  const router = useRouter();
  const { setToken } = useAuth();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    setLoading(true);
    try {
      const response = await apiRequest<{ access_token: string }>('/auth/token', {
        method: 'POST',
        body: new URLSearchParams({
          username: String(formData.get('email') || ''),
          password: String(formData.get('password') || ''),
        }),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      setToken(response.access_token);
      notifications.show({ title: 'Signed in', message: 'Welcome back!' });
      router.push('/dashboard');
    } catch (error) {
      notifications.show({ color: 'red', title: 'Error', message: 'Failed to sign in' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container size="xs" py="xl">
      <form onSubmit={handleSubmit}>
        <Stack>
          <Title order={2}>Sign in</Title>
          <TextInput name="email" label="Email" required type="email" placeholder="you@example.com" />
          <PasswordInput name="password" label="Password" required placeholder="Your password" />
          <Button type="submit" loading={loading} fullWidth>
            Sign in
          </Button>
        </Stack>
      </form>
    </Container>
  );
}
