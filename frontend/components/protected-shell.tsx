'use client';

import { Anchor, Center, Container, Text } from '@mantine/core';
import Link from 'next/link';
import { useAuth } from './auth-provider';

export function ProtectedShell({ children }: { children: React.ReactNode }) {
  const { token } = useAuth();

  if (!token) {
    return (
      <Center h="100vh">
        <Container size="xs" ta="center">
          <Text>You need to sign in to access this page.</Text>
          <Anchor component={Link} href="/signin">
            Go to sign in
          </Anchor>
        </Container>
      </Center>
    );
  }

  return <>{children}</>;
}
