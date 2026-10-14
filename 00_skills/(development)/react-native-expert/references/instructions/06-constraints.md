<!-- Package: 00_skills/(development)/react-native-expert; relative command/resource examples resolve from that package or workspace root. -->

## Constraints

### MUST DO

- Use LegendList/FlashList for all lists (never ScrollView with `.map()`)
- Handle SafeAreaView / `contentInsetAdjustmentBehavior="automatic"` for notches
- Use `Pressable` instead of Touchable components
- Test on both iOS and Android real devices
- Use `KeyboardAvoidingView` with platform-appropriate behavior for forms
- Handle Android back button in custom navigation flows
- Use expo-image for all image rendering
- Use native navigators (native-stack, native-bottom-tabs)
- Use TypeScript strict mode

### MUST NOT DO

- Use ScrollView for dynamic/large lists
- Use inline style objects in list items (breaks memoization)
- Hardcode dimensions (use `Dimensions` API, flex, or percentage)
- Ignore memory leaks from subscriptions/listeners
- Skip platform-specific testing
- Use `setTimeout`/`waitFor` for animations (use Reanimated)
- Use `.value` on shared values (use `.get()`/`.set()`)
- Use `useAnimatedReaction` for derivations (use `useDerivedValue`)
- Store visual values in state (store state, derive visuals)
- Use `TouchableOpacity` or `TouchableHighlight` (use `Pressable`)
- Use `@react-navigation/stack` (use `native-stack`)
- Use React Native's `Image` component (use `expo-image`)
