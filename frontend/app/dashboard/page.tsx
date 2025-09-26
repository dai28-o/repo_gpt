'use client';

import { Badge, Card, Container, Group, Stack, Text, Title } from '@mantine/core';
import { useEffect, useState } from 'react';
import { ProtectedShell } from '@/components/protected-shell';
import { useAuth } from '@/components/auth-provider';
import { apiRequest } from '@/lib/api';

interface EventSummary {
  id: number;
  title: string;
  description: string;
  start_time: string;
  end_time: string;
  location: string;
}

export default function DashboardPage() {
  const { token } = useAuth();
  const [upcoming, setUpcoming] = useState<EventSummary[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    apiRequest<EventSummary[]>('/events/', { method: 'GET' }, token)
      .then(setUpcoming)
      .catch(() => setError('Failed to load events'));
  }, [token]);

  return (
    <ProtectedShell>
      <Container py="xl">
        <Stack gap="lg">
          <Title order={2}>Participant dashboard</Title>
          {error && <Text c="red">{error}</Text>}
          <Stack gap="md">
            {upcoming.map((event) => (
              <Card key={event.id} withBorder>
                <Stack gap="xs">
                  <Group justify="space-between">
                    <Title order={4}>{event.title}</Title>
                    <Badge>{new Date(event.start_time).toLocaleDateString()}</Badge>
                  </Group>
                  <Text>{event.description}</Text>
                  <Text size="sm" c="dimmed">
                    {event.location}
                  </Text>
                </Stack>
              </Card>
            ))}
            {upcoming.length === 0 && <Text>No events yet. Enroll to start learning!</Text>}
          </Stack>
        </Stack>
      </Container>
    </ProtectedShell>
  );
}
