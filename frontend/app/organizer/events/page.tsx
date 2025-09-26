'use client';

import { Button, Card, Container, Group, NumberInput, Stack, Text, Textarea, TextInput, Title } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { FormEvent, useEffect, useState } from 'react';
import { ProtectedShell } from '@/components/protected-shell';
import { useAuth } from '@/components/auth-provider';
import { apiRequest } from '@/lib/api';

interface EventForm {
  title: string;
  description: string;
  tags: string;
  capacity: number;
  start_time: string;
  end_time: string;
  location: string;
}

interface OrganizerEvent extends EventForm {
  id: number;
}

const createInitialForm = (): EventForm => ({
  title: '',
  description: '',
  tags: '',
  capacity: 10,
  start_time: new Date().toISOString(),
  end_time: new Date().toISOString(),
  location: '',
});

export default function OrganizerEventsPage() {
  const { token } = useAuth();
  const [form, setForm] = useState<EventForm>(createInitialForm());
  const [events, setEvents] = useState<OrganizerEvent[]>([]);

  useEffect(() => {
    if (!token) return;
    apiRequest<OrganizerEvent[]>('/events/', { method: 'GET' }, token)
      .then(setEvents)
      .catch(() => notifications.show({ color: 'red', title: 'Error', message: 'Failed to load events' }));
  }, [token]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!token) return;
    try {
      await apiRequest('/events/', {
        method: 'POST',
        body: JSON.stringify(form),
      }, token);
      notifications.show({ title: 'Event created', message: 'Your event is live.' });
      setForm(createInitialForm());
      const updated = await apiRequest<OrganizerEvent[]>('/events/', { method: 'GET' }, token);
      setEvents(updated);
    } catch (error) {
      notifications.show({ color: 'red', title: 'Error', message: 'Failed to create event' });
    }
  };

  return (
    <ProtectedShell>
      <Container py="xl">
        <Stack gap="lg">
          <Title order={2}>Organizer events</Title>
          <form onSubmit={handleSubmit}>
            <Stack>
              <TextInput label="Title" value={form.title} required onChange={(event) => setForm((prev) => ({ ...prev, title: event.currentTarget.value }))} />
              <Textarea
                label="Description"
                value={form.description}
                minRows={3}
                required
                onChange={(event) => setForm((prev) => ({ ...prev, description: event.currentTarget.value }))}
              />
              <TextInput label="Tags" value={form.tags} onChange={(event) => setForm((prev) => ({ ...prev, tags: event.currentTarget.value }))} />
              <NumberInput
                label="Capacity"
                value={form.capacity}
                min={1}
                onChange={(value) =>
                  setForm((prev) => ({ ...prev, capacity: typeof value === 'number' ? value : prev.capacity }))
                }
              />
              <TextInput
                label="Start time"
                type="datetime-local"
                value={form.start_time.slice(0, 16)}
                onChange={(event) => setForm((prev) => ({ ...prev, start_time: new Date(event.currentTarget.value).toISOString() }))}
              />
              <TextInput
                label="End time"
                type="datetime-local"
                value={form.end_time.slice(0, 16)}
                onChange={(event) => setForm((prev) => ({ ...prev, end_time: new Date(event.currentTarget.value).toISOString() }))}
              />
              <TextInput
                label="Location"
                value={form.location}
                required
                onChange={(event) => setForm((prev) => ({ ...prev, location: event.currentTarget.value }))}
              />
              <Button type="submit">Create event</Button>
            </Stack>
          </form>
          <Stack gap="md">
            <Title order={3}>Your events</Title>
            {events.map((event) => (
              <Card key={event.id} withBorder>
                <Stack gap="xs">
                  <Group justify="space-between">
                    <Text fw={600}>{event.title}</Text>
                    <Text size="sm" c="dimmed">
                      {new Date(event.start_time).toLocaleString()}
                    </Text>
                  </Group>
                  <Text>{event.description}</Text>
                </Stack>
              </Card>
            ))}
            {events.length === 0 && <Text>No events created yet.</Text>}
          </Stack>
        </Stack>
      </Container>
    </ProtectedShell>
  );
}
