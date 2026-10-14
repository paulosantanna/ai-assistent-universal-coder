<!-- Package: 00_skills/(development)/react-native-expert; relative command/resource examples resolve from that package or workspace root. -->

## Technology Stack (2026)

| Layer         | Technology                                    | Version                          |
| ------------- | --------------------------------------------- | -------------------------------- |
| Framework     | React Native                                  | 0.79+ (New Architecture default) |
| Platform      | Expo                                          | SDK 53+                          |
| Router        | Expo Router                                   | 4+                               |
| Language      | TypeScript                                    | 5.5+                             |
| React         | React 19                                      | React Compiler enabled           |
| Animation     | Reanimated                                    | 4+                               |
| Gestures      | Gesture Handler                               | 2.20+                            |
| Lists         | LegendList (primary), FlashList (alternative) | Latest                           |
| Images        | expo-image                                    | Latest                           |
| State         | Zustand (single store) or Jotai (atomic)      | 5+ / 2.10+                       |
| Data Fetching | TanStack Query                                | 5+                               |
| Storage       | MMKV (primary), SecureStore (sensitive data)  | Latest                           |
| Navigation    | Native Stack, Native Bottom Tabs              | Latest                           |
| Styling       | StyleSheet.create, NativeWind (optional)      | Latest                           |

**Key architectural facts for 2026:**

- New Architecture (Fabric + TurboModules) is the default — no opt-in needed.
- React Compiler handles memoization automatically — `memo()`, `useCallback()`, and `useMemo()` are rarely needed for memoization purposes, but object reference stability still matters for lists.
- Use `.get()` and `.set()` on Reanimated shared values, never `.value` directly.
- `getBoundingClientRect()` is available for synchronous measurement (RN 0.82+).
- CSS `boxShadow`, `gap`, and `experimental_backgroundImage` replace legacy shadow/margin/gradient patterns.
