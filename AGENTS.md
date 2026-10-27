# Schema Guard API — Agent Instructions

## Project Overview

Schema Guard API is a Python backend built with FastAPI, Pydantic v2, SQLAlchemy, Alembic, PostgreSQL, and uv.

The application supports API contract management and GitHub repository integrations.

The primary engineering objectives are correctness, security, maintainability, reliability, and efficient execution.

These instructions apply to AI coding agents working in this repository.

## 1. Technology Stack

Use the versions installed and locked by this project.

- Python 3.12+
- FastAPI with standard dependencies
- Pydantic v2
- Pydantic Settings
- SQLAlchemy 2.x
- Alembic
- PostgreSQL with Psycopg 3
- uv for dependency and environment management
- Uvicorn for ASGI execution
- itsdangerous for signed data where applicable

### Version Awareness

- Consult the documentation matching the installed dependency versions.
- Prefer APIs and conventions supported by the installed versions.
- Do not assume that patterns from older versions remain valid.
- Avoid deprecated functionality.
- Inspect `pyproject.toml` and `uv.lock` when version compatibility matters.
- Do not replace SQLAlchemy with SQLModel or another ORM.
- Do not introduce a new framework or dependency without clear justification.

## 2. General Engineering Principles

- Inspect the relevant codebase before implementing changes.
- Follow established naming conventions, architecture, and implementation patterns.
- Prefer simple, explicit, maintainable solutions.
- Avoid premature optimization and unnecessary abstractions.
- Keep modifications focused on the requested task.
- Do not refactor unrelated code.
- Avoid duplicating existing functionality.
- Prefer Python standard library functionality when suitable.
- Follow established Python conventions and PEP 8.
- Use descriptive names and readable control flow.
- Do not introduce compatibility workarounds for unsupported environments unless explicitly requested.

## 3. Application Architecture

Respect the existing repository structure.

When these directories are present, follow their responsibilities:

- `app/api/`: API routers, endpoint declarations, dependencies, and HTTP-level concerns.
- `app/core/`: Application configuration, security utilities, and foundational infrastructure.
- `app/db/`: Database engine, session factories, and database dependencies.
- `app/models/`: SQLAlchemy ORM models and database relationships.
- `app/schemas/`: Pydantic request, response, and validation schemas.
- `app/services/`: Reusable business workflows and application logic.
- `tests/`: Automated tests.
- `alembic/`: Database migration history and configuration.

### Architectural Guidelines

- Keep HTTP handlers focused on parsing requests, invoking logic, and returning responses.
- Place reusable or complex business logic in service functions or classes.
- Keep ORM-specific persistence operations separate from API serialization.
- Introduce repository or data-access abstractions only when they provide meaningful value.
- Avoid circular imports and unnecessary cross-module dependencies.
- Organize related functionality consistently.
- Prefer dependency injection for resources such as database sessions and authenticated user context.
- Do not create unnecessary layers for trivial operations.
- Do not reorganize the project without an explicit reason.

## 4. FastAPI Standards

- Use `APIRouter` to group related endpoints.
- Use appropriate HTTP methods and status codes.
- Define request and response models with Pydantic where applicable.
- Declare `response_model` when it improves contract clarity and response validation.
- Use FastAPI dependency injection for shared resources and request-level dependencies.
- Avoid storing mutable request-specific state in global variables.
- Prefer explicit endpoint signatures and type annotations.
- Return appropriate errors without exposing internal implementation details.
- Keep endpoint behavior consistent with its documented OpenAPI contract.
- Preserve backward compatibility unless a breaking API change is explicitly required.

### Synchronous and Asynchronous Execution

- Inspect the existing database engine and session configuration before choosing `def` or `async def`.
- Use synchronous SQLAlchemy sessions with synchronous database operations.
- Use `AsyncSession` only when the application is configured with an appropriate asynchronous engine and driver.
- Do not call synchronous blocking database operations directly inside asynchronous endpoints.
- Do not introduce asynchronous code solely for perceived performance improvements.
- Avoid blocking the event loop with network, file, or CPU-intensive work.
- Do not share a mutable SQLAlchemy session across concurrent tasks.
- Use background execution mechanisms only when appropriate for the task and operational requirements.

## 5. Pydantic v2 Standards

- Use Pydantic models for request validation and response serialization.
- Keep Pydantic schemas separate from SQLAlchemy ORM models.
- Prefer Pydantic v2 APIs such as `model_validate`, `model_dump`, and `ConfigDict`.
- Use `from_attributes=True` where ORM-to-schema validation requires it.
- Prefer strongly typed fields over unstructured dictionaries.
- Define explicit field constraints and validators when necessary.
- Do not duplicate validation already performed reliably by Pydantic.
- Distinguish input schemas, output schemas, and internal data structures when their requirements differ.
- Avoid exposing internal database fields in public response models.
- Do not use deprecated Pydantic v1 patterns.

## 6. SQLAlchemy and Database Standards

- Use SQLAlchemy 2.x-style ORM mappings and query APIs.
- Prefer typed mappings using `Mapped` and `mapped_column` when compatible with existing models.
- Prefer `select()` and modern session execution patterns.
- Avoid legacy ORM APIs in new code.
- Define database constraints and relationships explicitly where appropriate.
- Avoid raw SQL when SQLAlchemy can express the operation clearly.
- Use parameterized queries for raw SQL.
- Avoid unnecessary queries and N+1 relationship loading.
- Select appropriate loading strategies based on actual access patterns.
- Preserve database integrity through constraints and transactions.

### Session and Transaction Management

- Follow the existing session factory and dependency pattern.
- Keep session lifetimes bounded.
- Keep transactions short.
- Establish clear transaction ownership.
- Commit database changes at an intentional transaction boundary.
- Roll back failed transactions appropriately.
- Do not commit independently inside every helper function when a higher-level operation owns the transaction.
- Do not leak sessions or database connections.
- Never share a session instance across concurrent requests or tasks.

## 7. Alembic and Schema Migrations

- Use Alembic for database schema changes.
- Do not use `Base.metadata.create_all()` as a substitute for managed production migrations.
- Ensure ORM model changes and migration revisions remain consistent.
- Review autogenerated migrations before applying them.
- Verify column types, foreign keys, indexes, constraints, defaults, and nullable settings.
- Do not assume Alembic autogeneration detects every schema change correctly.
- Preserve existing data whenever practical.
- Treat destructive schema changes as high-risk operations.
- Do not modify historical migrations that have already been applied to shared environments without explicit authorization.
- Never run migrations against a production database without explicit authorization.
- Keep schema changes compatible with the application's deployment requirements.

## 8. PostgreSQL Standards

- Use PostgreSQL-compatible types and features.
- Respect existing database naming and indexing conventions.
- Avoid unnecessary indexes and constraints that add write overhead without clear value.
- Consider transaction isolation and concurrency when implementing multi-step operations.
- Use database-enforced uniqueness and foreign keys for persistent integrity guarantees.
- Avoid relying exclusively on application-level checks for uniqueness or referential integrity.
- Use efficient queries and limit unnecessary result loading.
- Use pagination for potentially large collections.
- Do not introduce database-specific optimizations without a demonstrated requirement.

## 9. Configuration and Secrets

- Use `pydantic-settings` for application configuration.
- Prefer environment variables for environment-specific settings.
- Keep configuration centralized.
- Do not hardcode secrets, credentials, tokens, or database URLs.
- Never commit `.env` files containing secrets.
- Do not log sensitive configuration values.
- Fail clearly when required configuration is missing or invalid.
- Avoid repeatedly constructing settings objects when an established reusable configuration pattern exists.
- Keep development, testing, and production configurations appropriately separated.

## 10. Authentication and Authorization

- Follow the existing authentication architecture.
- Validate authentication credentials and authorization permissions on the server.
- Do not trust client-provided user identifiers for resource ownership.
- Verify ownership or granted access before reading or modifying protected resources.
- Use secure token generation, validation, and expiration practices.
- Treat signed tokens and encrypted values as different security mechanisms.
- Do not store plaintext passwords or sensitive authentication tokens.
- Avoid revealing whether protected resources exist through unauthorized endpoints when doing so creates an information disclosure risk.
- Preserve established authentication and authorization behavior when modifying endpoints.

## 11. External Integrations and GitHub

- Follow the existing GitHub integration architecture.
- Request only the permissions needed for an integration.
- Verify relevant webhook signatures before trusting webhook payloads.
- Validate installation, repository, and user authorization before performing protected operations.
- Never expose GitHub App private keys or installation tokens.
- Handle expired credentials and revoked installations.
- Handle external API failures, timeouts, and rate limits.
- Do not assume external responses are valid or complete.
- Use bounded retries only when safe and appropriate.
- Avoid leaking external access tokens in logs or error messages.

## 12. API Contract and Schema Processing

Schema Guard handles API contract information. Treat externally supplied schemas as untrusted input.

- Validate supported schema formats before processing.
- Provide clear errors for malformed or unsupported schemas.
- Do not execute code from externally supplied specifications.
- Apply appropriate limits to schema size, nesting, and resource consumption.
- Do not fetch arbitrary external schema references without an established security policy.
- Protect against server-side request forgery when resolving external URLs or references.
- Keep schema parsing and comparison logic separate from HTTP route handlers when the logic becomes substantial.
- Prefer deterministic schema comparison behavior.
- Preserve contract compatibility rules established by the application.
- Test schema-processing edge cases and malformed input.

## 13. Error Handling and Logging

- Use appropriate FastAPI exception types for expected HTTP errors.
- Keep error messages useful without exposing secrets, stack traces, or sensitive internal data.
- Do not silently swallow exceptions.
- Handle expected failures explicitly.
- Allow unexpected failures to reach established centralized error handling and observability mechanisms.
- Use structured or consistently formatted logging following existing conventions.
- Include useful operational context without logging sensitive payloads.
- Avoid excessive logging in frequently executed operations.
- Do not expose raw database exception messages to API consumers.

## 14. Security and Reliability

- Treat all external and client-controlled input as untrusted.
- Enforce authorization at appropriate application boundaries.
- Avoid unsafe deserialization and dynamic execution.
- Validate file types, sizes, and processing limits where applicable.
- Apply timeouts to external network operations.
- Avoid unbounded loops, retries, and memory consumption.
- Handle race conditions where concurrent operations can affect persistent state.
- Make repeated operations idempotent when required by the workflow.
- Do not perform irreversible operations without the necessary authorization.
- Prefer established, maintained security libraries and documented patterns.

## 15. Performance

- Prefer efficient database queries and appropriate result loading.
- Avoid unnecessary network requests and serialization work.
- Keep database connections and transactions bounded.
- Avoid blocking asynchronous execution paths.
- Use batching when it provides a clear performance advantage.
- Avoid premature caching.
- Measure or investigate performance bottlenecks before introducing complex optimizations.
- Preserve correctness and readability when optimizing code.
- Do not introduce background workers, queues, or distributed systems without a justified requirement.

## 16. Dependency Management with uv

- Use `uv` as the project's package and environment manager.
- Treat `pyproject.toml` as the source of declared dependencies.
- Preserve and maintain `uv.lock`.
- Use `uv add` and `uv remove` for dependency changes.
- Use `uv sync` to synchronize the environment.
- Use `uv run` to execute project commands.
- Avoid mixing pip and uv workflows unless explicitly required.
- Do not upgrade unrelated dependencies during feature development.
- Do not install packages when existing dependencies are sufficient.
- Place development-only tooling in the appropriate dependency group.

## 17. Testing and Verification

- Follow the existing testing framework and conventions.
- Add or update tests when changing meaningful application behavior.
- Prioritize tests for authentication, authorization, business rules, database integrity, schema validation, and error handling.
- Use isolated test configuration and database resources.
- Never run tests that mutate production data.
- Test both expected behavior and important failure cases.
- Prefer deterministic tests.
- Mock external APIs at appropriate boundaries.
- Do not over-mock internal logic when integration tests would provide greater confidence.
- Run relevant checks using the tools configured in the repository.
- Do not claim successful verification without executing the corresponding checks.

## 18. Agent Development Workflow

For each implementation task:

1. **Inspect:** Understand the affected modules, dependencies, database models, and existing behavior.
2. **Verify:** Consult the installed library versions and relevant documentation.
3. **Plan:** Identify the smallest coherent implementation approach.
4. **Implement:** Apply focused changes following existing conventions.
5. **Test:** Execute applicable tests, type checks, lint checks, or other relevant validation.
6. **Review:** Check for security regressions, database changes, unnecessary dependencies, and unintended modifications.
7. **Report:** Summarize what changed, what was verified, and what remains unresolved.

### Additional Agent Behavior

- Do not modify unrelated files.
- Do not introduce unnecessary architectural layers.
- Do not invent library APIs or project conventions.
- Do not modify dependencies without justification.
- Do not silently change API response contracts.
- Do not perform destructive database operations without authorization.
- Do not automatically commit or push changes unless explicitly requested.
- Do not bypass failed tests through configuration suppression.
- Do not claim a command succeeded unless its result confirms success.
- Prefer reasonable, reversible assumptions for minor ambiguity.
- Ask for clarification when unresolved ambiguity carries meaningful security, data-loss, or compatibility risk.

## 19. Instruction Priority

Follow this order when deciding how to implement changes:

1. Explicit task requirements.
2. Security, data integrity, and operational safety constraints.
3. Existing project conventions and architectural decisions.
4. Documentation matching installed dependency versions.
5. General engineering best practices.

General preferences in this document do not override higher-priority instructions or verified runtime requirements.

## 20. Final Expectations

Code produced by AI coding agents should be:

- Correct and appropriately tested.
- Secure by default.
- Type-annotated and readable.
- Consistent with existing project patterns.
- Efficient without premature optimization.
- Explicit about database and transaction behavior.
- Compatible with installed dependencies.
- Maintainable by human engineers.

The objective is not to maximize abstraction or architectural complexity. The objective is to produce reliable, understandable backend software with minimal unnecessary complexity.