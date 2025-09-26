'use client';

import { Card, Container, Stack, Table, Text, Title } from '@mantine/core';
import { useEffect, useState } from 'react';
import { ProtectedShell } from '@/components/protected-shell';
import { useAuth } from '@/components/auth-provider';
import { apiRequest } from '@/lib/api';

interface UserSummary {
  id: number;
  email: string;
  role: string;
}

interface EventSummary {
  id: number;
  title: string;
  organizer: { full_name: string | null };
}

export default function AdminPage() {
  const { token } = useAuth();
  const [users, setUsers] = useState<UserSummary[]>([]);
  const [events, setEvents] = useState<EventSummary[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    Promise.all([
      apiRequest<UserSummary[]>('/admin/users', { method: 'GET' }, token),
      apiRequest<EventSummary[]>('/admin/events', { method: 'GET' }, token),
    ])
      .then(([usersData, eventsData]) => {
        setUsers(usersData);
        setEvents(eventsData);
      })
      .catch(() => setError('Failed to load admin data'));
  }, [token]);

  return (
    <ProtectedShell>
      <Container py="xl">
        <Stack gap="lg">
          <Title order={2}>Admin panel</Title>
          {error && <Text c="red">{error}</Text>}
          <Card withBorder>
            <Title order={4}>Users</Title>
            <Table mt="sm">
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>Email</Table.Th>
                  <Table.Th>Role</Table.Th>
                </Table.Tr>
              </Table.Thead>
              <Table.Tbody>
                {users.map((user) => (
                  <Table.Tr key={user.id}>
                    <Table.Td>{user.email}</Table.Td>
                    <Table.Td>{user.role}</Table.Td>
                  </Table.Tr>
                ))}
              </Table.Tbody>
            </Table>
            {users.length === 0 && <Text>No users found.</Text>}
          </Card>

          <Card withBorder>
            <Title order={4}>Events</Title>
            <Stack gap="xs" mt="sm">
              {events.map((event) => (
                <Card key={event.id} shadow="xs">
                  <Text fw={600}>{event.title}</Text>
                  <Text size="sm" c="dimmed">
                    Organizer: {event.organizer?.full_name ?? 'N/A'}
                  </Text>
                </Card>
              ))}
              {events.length === 0 && <Text>No events found.</Text>}
            </Stack>
          </Card>
        </Stack>
      </Container>
    </ProtectedShell>
  );
}
