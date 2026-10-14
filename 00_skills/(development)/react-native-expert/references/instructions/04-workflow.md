<!-- Package: 00_skills/(development)/react-native-expert; relative command/resource examples resolve from that package or workspace root. -->

## Workflow

Follow this sequence for every implementation:

### 1. Setup

- Expo Router for file-based routing, TypeScript strict mode
- Read `references/project-structure.md` when setting up a new project

### 2. Structure

- Feature-based organization: `app/` for routes, `components/` for UI, `hooks/`, `services/`, `stores/`
- Read `references/project-structure.md` for the full recommended layout

### 3. Implement

- Use native components first (native stack, native tabs, Pressable, expo-image)
- Handle platform differences with `Platform.select()` or `.ios.tsx`/`.android.tsx` files
- Read `references/platform-handling.md` for platform-specific patterns
- Read `references/expo-router.md` for navigation and routing patterns

### 4. Optimize

- Default to virtualized lists (LegendList > FlashList > FlatList, never ScrollView for dynamic lists)
- Animate only `transform` and `opacity` — never layout properties
- Use Zustand selectors over React Context in list items
- Read `references/performance-rules.md` for the full 35+ rule catalog

### 5. Test

- Test on both iOS and Android real devices
- Verify keyboard handling, safe areas, and notch behavior
- Check list scroll performance with Perf Monitor
