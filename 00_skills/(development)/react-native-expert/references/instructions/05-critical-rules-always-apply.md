<!-- Package: 00_skills/(development)/react-native-expert; relative command/resource examples resolve from that package or workspace root. -->

## Critical Rules (Always Apply)

These rules prevent crashes and severe performance issues. Always follow them without needing to consult reference files.

### Rendering Safety

**Never use `&&` with potentially falsy values** — React Native crashes if a falsy value like `0` or `""` is rendered outside `<Text>`. Use ternary with null or explicit boolean coercion:

```tsx
// CRASH: if count is 0, renders "0" outside <Text>
{
  count && <Text>{count} items</Text>
}

// SAFE: ternary
{
  count ? <Text>{count} items</Text> : null
}
```

**Always wrap strings in `<Text>`** — strings as direct children of `<View>` crash the app.

### List Performance

**Always use a virtualizer.** LegendList is preferred. FlashList is an acceptable alternative. Never use ScrollView with `.map()` for dynamic lists:

```tsx
import { LegendList } from '@legendapp/list'
;<LegendList
  data={items}
  renderItem={({ item }) => <ItemCard item={item} />}
  keyExtractor={(item) => item.id}
  estimatedItemSize={80}
/>
```

**Keep list items lightweight.** No queries, no data fetching, no expensive computations inside list items. Pass pre-computed primitives as props. Fetch data in the parent.

**Maintain stable object references.** Do not `.map()` or `.filter()` data before passing to virtualized lists. Transform data inside list items using Zustand selectors.

### Navigation

**Use native navigators only:**

- Stacks: `@react-navigation/native-stack` or Expo Router's default `<Stack>` (uses native-stack)
- Tabs: `react-native-bottom-tabs` or Expo Router's `<NativeTabs>` from `expo-router/unstable-native-tabs`
- Never use `@react-navigation/stack` (JS-based) or `@react-navigation/bottom-tabs` when native feel matters

```tsx
// Expo Router native tabs (SDK 53+)
import { NativeTabs, Label } from 'expo-router/unstable-native-tabs'

export default function TabLayout() {
  return (
    <NativeTabs>
      <NativeTabs.Trigger name="index">
        <Label>Home</Label>
        <NativeTabs.Trigger.Icon sf="house.fill" md="home" />
      </NativeTabs.Trigger>
    </NativeTabs>
  )
}
```

### Animation

**Animate only `transform` and `opacity`.** Never animate `width`, `height`, `top`, `left`, `margin`, or `padding` — they trigger layout recalculation on every frame.

```tsx
// CORRECT: GPU-accelerated
useAnimatedStyle(() => ({
  transform: [{ translateY: withTiming(visible ? 0 : 100) }],
  opacity: withTiming(visible ? 1 : 0),
}))
```

**Store state, derive visuals.** Shared values should represent actual state (`pressed`, `progress`), not visual outputs (`scale`, `opacity`). Derive visuals with `interpolate()`.

**Use `.get()` and `.set()`** for all Reanimated shared value access — required for React Compiler compatibility.

### Images

**Always use `expo-image`** instead of React Native's `Image`. It provides memory-efficient caching, blurhash placeholders, and better list performance:

```tsx
import { Image } from 'expo-image'
;<Image
  source={{ uri: url }}
  placeholder={{ blurhash: 'LGF5]+Yk^6#M@-5c,1J5@[or[Q6.' }}
  contentFit="cover"
  transition={200}
  style={styles.image}
/>
```

### Styling (Modern Patterns)

```tsx
// Use gap instead of margin between children
<View style={{ gap: 8 }}>
  <Text>First</Text>
  <Text>Second</Text>
</View>

// Use CSS boxShadow instead of legacy shadow objects
{ boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)' }

// Use borderCurve for smoother corners
{ borderRadius: 12, borderCurve: 'continuous' }

// Use native gradients instead of third-party libraries
{ experimental_backgroundImage: 'linear-gradient(to bottom, #000, #fff)' }
```

### State Management

- **Derive values, never store redundant state.** If a value can be computed from existing state/props, compute it during render.
- **Zustand or Jotai over React Context in list items.** Zustand selectors and Jotai atoms only re-render when the selected/atom value changes — Context re-renders on any change.
- **Zustand** excels at single-store patterns with persistence (Zustand persist + MMKV).
- **Jotai** excels at fine-grained atomic state with derived atoms — its atomic model naturally prevents unnecessary re-renders.
- **Use dispatch updaters** (`setState(prev => ...)`) when next state depends on current state.
- **Use fallback pattern** (`undefined` initial state + `??` operator) for reactive defaults.

### Modals and Menus

- **Modals:** Use native `<Modal presentationStyle="formSheet">` or React Navigation v7 `presentation: 'formSheet'` with `sheetAllowedDetents`. Avoid JS-based bottom sheet libraries.
- **Menus:** Use [zeego](https://zeego.dev) for native dropdown and context menus. Never build custom JS menus.
- **Pressables:** Use `Pressable` from `react-native` or `react-native-gesture-handler`. Never use `TouchableOpacity` or `TouchableHighlight`.
