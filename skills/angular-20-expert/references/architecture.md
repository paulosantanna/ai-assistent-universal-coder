# Angular 20 architecture

Entry: `angular.json`, `package.json`, bootstrap/application config, routes.

Preserve repository choice between standalone and module boundaries. Map data/state ownership before modifying signals/RxJS. Treat SSR/hydration and browser-only APIs as explicit runtime boundaries. Verify DI scope and lazy-loading effects before refactors.
