'use client';

import { Button, Container, PasswordInput, Select, Stack, TextInput, Title } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { useRouter } from 'next/navigation';
import { FormEvent, useState } from 'react';
import { apiRequest } from '@/lib/api';

const roleOptions = [
  { value: 'participant', label: 'Participant' },
  { value: 'organizer', label: 'Organizer' },
];

export default function SignUpPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    setLoading(true);
    try {
      await apiRequest('/auth/register', {
        method: 'POST',
        body: JSON.stringify({
          email: formData.get('email'),
          password: formData.get('password'),
          full_name: formData.get('full_name'),
          role: formData.get('role'),
        }),
      });
      notifications.show({ title: 'Account created', message: 'You can now sign in.' });
      router.push('/signin');
    } catch (error) {
      notifications.show({ color: 'red', title: 'Error', message: 'Failed to create account' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container size="xs" py="xl">
      <form onSubmit={handleSubmit}>
        <Stack>
          <Title order={2}>Create your account</Title>
          <TextInput name="full_name" label="Full name" placeholder="Your name" required />
          <TextInput name="email" label="Email" required type="email" placeholder="you@example.com" />
          <PasswordInput name="password" label="Password" required placeholder="Choose a secure password" />
          <Select name="role" label="Role" data={roleOptions} defaultValue="participant" required />
          <Button type="submit" loading={loading} fullWidth>
            Sign up
          </Button>
        </Stack>
      </form>
    </Container>
  );
}
