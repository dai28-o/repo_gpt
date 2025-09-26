import { Anchor, Button, Container, Flex, Group, Stack, Text, Title } from '@mantine/core';
import Link from 'next/link';

export default function HomePage() {
  return (
    <Container size="md" py="xl">
      <Stack gap="lg">
        <Title order={1}>Local Skill-Sharing Event Platform</Title>
        <Text>
          Discover, host, and track community-powered learning events. Organizers can publish workshops,
          participants can manage attendance, and admins can keep an eye on everything from a single dashboard.
        </Text>
        <Group>
          <Button component={Link} href="/signin">
            Sign in
          </Button>
          <Button component={Link} href="/signup" variant="light">
            Create account
          </Button>
        </Group>
      </Stack>
      <Flex mt="xl" justify="space-between">
        <Stack gap="xs">
          <Title order={3}>For Participants</Title>
          <Text>Track upcoming events, record feedback, and monitor your learning journey.</Text>
        </Stack>
        <Stack gap="xs">
          <Title order={3}>For Organizers</Title>
          <Text>Create events, upload resources, and manage attendance effortlessly.</Text>
        </Stack>
        <Stack gap="xs">
          <Title order={3}>For Admins</Title>
          <Text>Oversee the community with insights into users and events.</Text>
        </Stack>
      </Flex>
      <Text mt="xl">
        Ready to get started? <Anchor component={Link} href="/signup">Join the platform</Anchor> and launch your next
        event.
      </Text>
    </Container>
  );
}
