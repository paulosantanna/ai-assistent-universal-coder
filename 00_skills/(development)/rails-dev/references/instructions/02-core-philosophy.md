<!-- Package: 00_skills/(development)/rails-dev; relative command/resource examples resolve from that package or workspace root. -->

## Core Philosophy

- **Rich models** - Business logic lives in models, not service objects
- **Everything is CRUD** - New resource over new action (`resource :closure` not `post :close`)
- **State as records** - `Closure` model instead of `closed: boolean`
- **Concerns for composition** - `Closeable`, `Watchable`, `Commentable`
- **Explicit over clever** - Inline until repetition is real; an abstraction earns its place, it isn't built on speculation
- **Small interfaces** - No public method without a caller
- **Let it crash** - Bang methods (`create!`), handle failures at the boundary, not by pre-guarding (`references/error-handling.md`)
- **Invariants in the schema** - Hard rules (presence, uniqueness, ranges) are NOT NULL / unique / check constraints; validations are for user-facing messages, not the source of truth. References stay soft: no foreign keys, integrity at the model layer
- **Minimal dependencies** - Build it yourself before reaching for gems. No Devise, Pundit, RSpec, FactoryBot, ViewComponent, service/form objects, or decorators
- **Database-backed** - Solid Queue/Cache/Cable, no Redis
- **Test coverage** - Maintain roughly 1:1 test ratio (1 line test per line of code)
