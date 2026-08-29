# Technology Selection

Technology follows the learning objective. Before adding a tool, write what behavior it makes possible to study and why a simpler option does not.

## React applications

Use **Vite** when studying hooks, state, rendering, component architecture, or browser behavior.

Use **Next.js** when the objective specifically involves SSR, React Server Components, framework caching, routing, streaming, or server/client boundaries.

## State ownership

- Use `useState` or `useReducer` for component-owned state.
- Use Zustand or Redux for shared client-owned state when explicit cross-tree coordination is needed.
- Use TanStack Query or an equivalent cache for server-state lifecycles.
- Use the URL for navigation state and filters that should be linkable or shareable.

Do not introduce a global store before identifying the state owner and lifecycle.

## Backend

Prefer **NestJS** when studying modules, dependency injection, application architecture, or enterprise-style APIs.

Prefer **FastAPI** when studying Python, lightweight services, async Python, workers, or data/AI integration.

A smaller standard-library or framework-native implementation is better when a framework would hide the concept under study.

## Messaging

Do not introduce Kafka merely because work is asynchronous.

Use **Kafka** when studying streaming, partitions, consumer groups, replay, per-partition ordering, or high-throughput event processing.

Use **RabbitMQ** when studying work queues, routing, acknowledgements, retries, or dead-letter queues.

## Selection check

For each major dependency, answer:

1. Which learning goal requires it?
2. Which complexity does it add?
3. Which concept does it hide?
4. What is the simpler alternative?
5. When should the choice be reconsidered?
