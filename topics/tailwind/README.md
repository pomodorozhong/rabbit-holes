# Reading Tailwind in real source code

An annotated guide to steps 1–5 of your source-reading path.

Read in this order: **class merging → a small component → button variants → theme values → Tailwind v4**. Each step reuses an idea from the previous one.

The snippets below are copied from repository snapshots fetched on **20 September 2026**. Source links point to those exact commits. Comments containing `...` mark omitted lines; a few excerpts are fragments of larger objects or functions. Examples written for this guide are labelled **Illustration**.

**Version context:** Steps 1–4 use Taxonomy, whose [package file](https://github.com/shadcn-ui/taxonomy/blob/298a8857c7128a0d121e7f699dfd729f23b3966d/package.json) declares Tailwind `^3.3.1`. Step 5 uses shadcn/ui’s v4 app, whose [package file](https://github.com/shadcn-ui/ui/blob/a87a63b2ca25143d26c8bd0903e4e9bc77b3f824/apps/v4/package.json) declares Tailwind `^4.3.0`. These are dependency ranges. The different configuration styles are intentional.

## 1. Read the small `cn()` helper

**Source:** [Taxonomy · lib/utils.ts, lines 1–8](https://github.com/shadcn-ui/taxonomy/blob/298a8857c7128a0d121e7f699dfd729f23b3966d/lib/utils.ts#L1-L8). The unrelated environment import is omitted.

```ts
import { ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"
// ...
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

`cn()` accepts several class-name inputs and returns one class string. `ClassValue` describes the accepted inputs for TypeScript; it does not generate any styles.

There are two operations inside the function:

1. `clsx(inputs)` combines strings and conditional class inputs, skipping falsy values such as `false` and `undefined`.
2. `twMerge(...)` removes conflicting Tailwind utilities that it recognizes. For the same kind of utility under the same conditions, the later value wins.

**Illustration — the effect of argument order:**

```ts
cn("p-8", "p-4") // "p-4"
cn("p-4", "p-8") // "p-8"
```

Both `p-8` and `p-4` set padding on all sides, so keeping one resolves that conflict. A pair such as `p-4 md:p-8` can coexist because the second utility applies at a different breakpoint.

This override behavior comes from the helper removing conflicting classes before rendering. Writing one class later in an ordinary HTML `class` attribute does not, by itself, give it higher CSS priority.

This helper lets a reusable component supply default styles while allowing its caller to adjust them. Step 2 shows exactly where that becomes useful.

## 2. Follow those classes into a small component

**Source:** [Taxonomy · components/empty-placeholder.tsx, lines 8–26](https://github.com/shadcn-ui/taxonomy/blob/298a8857c7128a0d121e7f699dfd729f23b3966d/components/empty-placeholder.tsx#L8-L26). This is the main component body.

```tsx
export function EmptyPlaceholder({
  className,
  children,
  ...props
}: EmptyPlaceholderProps) {
  return (
    <div
      className={cn(
        "flex min-h-[400px] flex-col items-center justify-center rounded-md border border-dashed p-8 text-center animate-in fade-in-50",
        className
      )}
      {...props}
    >
      <div className="mx-auto flex max-w-[420px] flex-col items-center justify-center text-center">
        {children}
      </div>
    </div>
  )
}
```

In React, `className` becomes the element’s HTML `class` attribute. This component also receives a `className` input from its caller. It passes its own defaults to `cn()` first, followed by the caller’s classes.

Read the long class string in small groups:

| Classes | What they do here |
| --- | --- |
| `flex flex-col` | Arrange the contents in a vertical flex layout. |
| `items-center justify-center` | Center the contents horizontally and vertically in that layout. |
| `min-h-[400px]` | Give the outer box a minimum height of exactly 400 pixels. Square brackets allow a literal value. |
| `p-8` | Add padding using Tailwind’s spacing scale. With the default scale, this is 2rem on each side. |
| `rounded-md border border-dashed` | Give the box rounded corners and a dashed border. |
| `mx-auto max-w-[420px]` | Center the inner box horizontally and limit its width to 420 pixels. |

`children` is the content placed inside this component. `{...props}` passes through the remaining inputs, such as an `id` or accessibility attributes, to the outer `<div>`.

**Illustration — overriding two defaults:**

```tsx
<EmptyPlaceholder className="min-h-[200px] p-4">
  No posts yet.
</EmptyPlaceholder>
```

Here, the final classes use a 200-pixel minimum height and `p-4` padding. The other default styles remain in the class string because they do not conflict with those two changes.

The source also contains `animate-in fade-in-50`. Those classes come from the `tailwindcss-animate` plugin, which is enabled in [Taxonomy’s configuration](https://github.com/shadcn-ui/taxonomy/blob/298a8857c7128a0d121e7f699dfd729f23b3966d/tailwind.config.js#L81). A class you encounter in a project can come from a plugin as well as Tailwind itself.

The reusable component represents an entire empty-state box. Its layout utilities stay beside the markup they style, making the relationship between structure and appearance easy to inspect.

## 3. Read how a button gets named variants

**Source:** [Taxonomy · components/ui/button.tsx, lines 2–32](https://github.com/shadcn-ui/taxonomy/blob/298a8857c7128a0d121e7f699dfd729f23b3966d/components/ui/button.tsx#L2-L32). Two visual variants are retained below, along with all three sizes and the defaults.

```tsx
import { VariantProps, cva } from "class-variance-authority"

import { cn } from "@/lib/utils"
// ...
const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        // ...
        outline:
          "border border-input hover:bg-accent hover:text-accent-foreground",
        // ...
      },
      size: {
        default: "h-10 py-2 px-4",
        sm: "h-9 px-3 rounded-md",
        lg: "h-11 px-8 rounded-md",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)
```

`cva`, from **class-variance-authority**, creates a function that selects class strings from named options. It is a separate library used alongside Tailwind.

Read this definition from outside to inside:

1. The first string supplies the classes shared by every button: alignment, rounded corners, text styling, and interaction states.
2. `variant` selects an appearance, such as `default` or `outline`.
3. `size` selects dimensions and padding.
4. `defaultVariants` supplies values when the caller does not choose them.

A prefix before `:` adds a condition. `hover:` applies while hovering, `focus-visible:` supplies a focus indicator when the browser considers it appropriate, and `disabled:` applies when the button is disabled. These states are handled through CSS.

The component attaches the chosen classes here: [button.tsx, lines 38–48](https://github.com/shadcn-ui/taxonomy/blob/298a8857c7128a0d121e7f699dfd729f23b3966d/components/ui/button.tsx#L38-L48).

```tsx
const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
```

Follow the inner expression first: `buttonVariants({ variant, size, className })` assembles the shared classes, the selected variant and size, and the caller’s extra classes. `cn(...)` then resolves recognized utility conflicts in that result. The surrounding `forwardRef` is React plumbing for passing a reference to the button element.

**Illustration — selecting a variant and overriding its padding:**

```tsx
<Button variant="outline" size="sm" className="px-6">
  Save
</Button>
```

The small size contributes `h-9 px-3 rounded-md`; the caller’s `px-6` replaces `px-3`. `size="sm"` is a named option defined by this component. A class beginning with `sm:` would instead be a responsive condition.

Notice that the variant map contains complete class names, such as `bg-primary` and `hover:bg-primary/90`. Choosing between those strings at runtime works with Tailwind’s source scanning. Constructing a name from fragments, such as `bg-${color}-500`, can leave the scanner without the complete class it needs to generate.

Next, trace where `primary`, `background`, and `ring` get their values.

## 4. Trace a theme color from CSS to a utility

**Sources:** [Taxonomy · styles/globals.css](https://github.com/shadcn-ui/taxonomy/blob/298a8857c7128a0d121e7f699dfd729f23b3966d/styles/globals.css) and [tailwind.config.js](https://github.com/shadcn-ui/taxonomy/blob/298a8857c7128a0d121e7f699dfd729f23b3966d/tailwind.config.js).

Start with the selected variable declarations in `globals.css`:

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 47.4% 11.2%;
    /* ... */
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    /* ... */
    --radius: 0.5rem;
  }

  .dark {
    --background: 224 71% 4%;
    --foreground: 213 31% 91%;
    /* ... */
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 1.2%;
    /* ... */
  }
}
```

A CSS custom property, such as `--primary`, stores a value that other CSS can reference. A **design token** is a named design choice; here, `primary` names the main action color, and `primary-foreground` names the text color used on top of it.

`:root` supplies the default values. Applying `.dark` to a suitable ancestor, commonly the root element, changes the values inherited by its descendants. In this file the colors are stored as HSL channels; the configuration below supplies the `hsl(...)` wrapper.

Now read the selected configuration entries that connect those values to Tailwind:

```js
module.exports = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./ui/**/*.{ts,tsx}",
    "./content/**/*.{md,mdx}",
  ],
  darkMode: ["class"],
  theme: {
    // ...
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        // ...
      },
      borderRadius: {
        lg: `var(--radius)`,
        md: `calc(var(--radius) - 2px)`,
        sm: "calc(var(--radius) - 4px)",
      },
      // ...
    },
  },
  plugins: [require("tailwindcss-animate"), require("@tailwindcss/typography")],
}
```

Follow one chain: **`bg-primary` → `theme.extend.colors.primary.DEFAULT` → `hsl(var(--primary))` → the active CSS variable value.** The nested `foreground` entry similarly makes the color name `primary-foreground` available for utilities such as `text-primary-foreground`.

The `borderRadius` entries connect `rounded-lg`, `rounded-md`, and `rounded-sm` to the shared `--radius` value. Changing that variable therefore changes the corner shapes of components using those utilities.

The `content` paths tell this Tailwind v3 project where to look for class names. `darkMode: ["class"]` configures the `dark:` condition. The `.dark` variable declarations themselves change theme values through ordinary CSS inheritance.

This means a component using `bg-primary text-primary-foreground` can change colors with the theme while keeping exactly those classes. Explicit `dark:` utilities are useful when an element needs an additional change.

Finally, [globals.css, lines 73–81](https://github.com/shadcn-ui/taxonomy/blob/298a8857c7128a0d121e7f699dfd729f23b3966d/styles/globals.css#L73-L81) applies shared defaults:

```css
@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
    font-feature-settings: "rlig" 1, "calt" 1;
  }
}
```

`@apply` inserts the CSS declarations represented by the named utilities. The universal `*` rule gives elements a default border color; the `body` rule supplies the page’s background and text colors. `@layer base` groups these global defaults. In this v3 setup, Tailwind places base styles before component and utility styles.

## 5. Compare the same ideas in Tailwind v4

**Sources:** shadcn/ui’s [apps/v4/app/globals.css](https://github.com/shadcn-ui/ui/blob/a87a63b2ca25143d26c8bd0903e4e9bc77b3f824/apps/v4/app/globals.css) and [apps/v4/registry/new-york-v4/ui/button.tsx](https://github.com/shadcn-ui/ui/blob/a87a63b2ca25143d26c8bd0903e4e9bc77b3f824/apps/v4/registry/new-york-v4/ui/button.tsx). These are the docs app’s theme definitions and a registry component from the same repository.

First, compare these selected stylesheet declarations with the CSS and JavaScript mapping from step 4:

```css
@import "tailwindcss";
/* ... */
@source "../node_modules/streamdown/dist/*.js";
/* ... */
@custom-variant dark (&:is(.dark *));
/* ... */
@theme inline {
  --breakpoint-3xl: 1600px;
  /* ... */
  --radius-sm: calc(var(--radius) * 0.6);
  --radius-md: calc(var(--radius) * 0.8);
  --radius-lg: var(--radius);
  /* ... */
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  /* ... */
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  /* ... */
}

:root {
  --radius: 0.625rem;
  --background: oklch(1 0 0);
  --foreground: oklch(0% 0 0);
  /* ... */
  --primary: oklch(0% 0 0);
  --primary-foreground: oklch(0.985 0 0);
  /* ... */
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  /* ... */
  --primary: oklch(0.922 0 0);
  --primary-foreground: oklch(0.205 0 0);
  /* ... */
}
```

The theme now declares utility mappings in CSS. `--color-primary` under `@theme inline` makes the name `primary` available to color utilities, including `bg-primary`. With `inline`, the generated utility uses the referenced value, `var(--primary)`, directly. The actual light and dark values still live in ordinary `:root` and `.dark` rules.

The `--radius-*` names likewise define the values used by rounding utilities. This repository chooses complete `oklch(...)` colors, whereas the earlier project stored HSL channels. That is a choice in these sources; Tailwind v4 also supports other CSS color formats.

| Detail | Taxonomy in step 4 | shadcn/ui in step 5 |
| --- | --- | --- |
| Bring in Tailwind | `@tailwind base;`, `@tailwind components;`, `@tailwind utilities;` | `@import "tailwindcss"` |
| Map tokens to utility names | `theme.extend` in JavaScript | `@theme inline` in CSS |
| Select light/dark values | `:root` and `.dark` variables | `:root` and `.dark` variables |
| Configure the `dark:` condition | `darkMode: ["class"]` | `@custom-variant dark (&:is(.dark *))` |
| Find source classes | Explicit `content` paths | Automatic detection, with `@source` for additional locations |

The `@source` line above adds a dependency’s JavaScript files to the scan. The custom `dark` variant applies to elements inside a `.dark` ancestor. Token changes and conditional `dark:` utilities remain two useful ways to express a dark theme.

Now compare these selected entries inside the button’s `cva` options: [button.tsx, lines 9–32](https://github.com/shadcn-ui/ui/blob/a87a63b2ca25143d26c8bd0903e4e9bc77b3f824/apps/v4/registry/new-york-v4/ui/button.tsx#L9-L32).

```tsx
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        // ...
        outline:
          "border bg-background shadow-xs hover:bg-accent hover:text-accent-foreground dark:border-input dark:bg-input/30 dark:hover:bg-input/50",
        // ...
      },
      size: {
        default: "h-9 px-4 py-2 has-[>svg]:px-3",
        // ...
        icon: "size-9",
        // ...
      },
    },
```

The `default` appearance uses the same semantic color names you saw in Taxonomy. The `outline` appearance adds explicit dark-theme adjustments for its border, background, and hover state.

| Code to notice | What it expresses |
| --- | --- |
| `hover:bg-primary/90` | Use the primary color at 90% opacity while hovering. |
| `dark:bg-input/30` | Under the dark condition, use the input color at 30% opacity. |
| `dark:hover:bg-input/50` | Apply the 50% value when both dark mode and hover are active. |
| `has-[>svg]:px-3` | Change horizontal padding when the button has a direct SVG child. |
| `size-9` | Set width and height together using the spacing scale. |

The bracket syntax in `has-[>svg]:` supplies a selector condition. You already saw brackets used for literal values in `min-h-[400px]`; their placement tells you whether they describe a value or a condition.

The render code still uses the same class assembly: [button.tsx, lines 52–60](https://github.com/shadcn-ui/ui/blob/a87a63b2ca25143d26c8bd0903e4e9bc77b3f824/apps/v4/registry/new-york-v4/ui/button.tsx#L52-L60).

```tsx
  return (
    <Comp
      data-slot="button"
      data-variant={variant}
      data-size={size}
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
```

Here `Comp` is either a native button or a Radix Slot, depending on the component’s `asChild` option. The `data-*` attributes expose the component’s identity and selected options as styling hooks. The Tailwind styles still arrive through `className`.

There is one source change to recognize: this version [imports `cn` from the `cn` package](https://github.com/shadcn-ui/ui/blob/a87a63b2ca25143d26c8bd0903e4e9bc77b3f824/apps/v4/registry/new-york-v4/ui/button.tsx#L1-L4). Its [registry utility file](https://github.com/shadcn-ui/ui/blob/a87a63b2ca25143d26c8bd0903e4e9bc77b3f824/apps/v4/registry/new-york-v4/lib/utils.ts) only re-exports that function. Step 1 shows the earlier local helper implementation.

For a small responsive example in this same stylesheet, inspect [globals.css, lines 250–252](https://github.com/shadcn-ui/ui/blob/a87a63b2ca25143d26c8bd0903e4e9bc77b3f824/apps/v4/app/globals.css#L250-L252):

```css
@utility container {
  @apply mx-auto max-w-[1400px] px-4 3xl:max-w-screen-2xl lg:px-8;
}
```

`@utility container` defines a custom utility. Its unprefixed `px-4` applies generally; `lg:px-8` changes the horizontal padding at the `lg` breakpoint and wider. That is the mobile-first pattern: start with a general value, then add conditions for larger screens. The `3xl:` condition uses the custom breakpoint declared earlier in `@theme`.

The stylesheet also has a small component rule at [lines 454–458](https://github.com/shadcn-ui/ui/blob/a87a63b2ca25143d26c8bd0903e4e9bc77b3f824/apps/v4/app/globals.css#L454-L458):

```css
@layer components {
  .dialog-ring {
    @apply rounded-xl border-none bg-clip-padding shadow-2xl ring-4 ring-neutral-200/80 dark:bg-neutral-900 dark:ring-neutral-800;
  }
}
```

`.dialog-ring` groups styles for a particular component appearance. Compare that with the broad `body` and `*` defaults in step 4. In Tailwind v4’s standard layer order, normal declarations in `utilities` have higher priority than `components`, which have higher priority than `base`.

## Source snapshots and attribution

All source links above are pinned so they continue to match the excerpts:

- **Taxonomy:** [`298a885`](https://github.com/shadcn-ui/taxonomy/commit/298a8857c7128a0d121e7f699dfd729f23b3966d); steps 1–4.
- **shadcn/ui:** [`a87a63b`](https://github.com/shadcn-ui/ui/commit/a87a63b2ca25143d26c8bd0903e4e9bc77b3f824); step 5.

The copied code is distributed under the upstream MIT licenses. Their notices are included below.

<details>
<summary>Taxonomy — MIT license</summary>

[Original license](https://github.com/shadcn-ui/taxonomy/blob/298a8857c7128a0d121e7f699dfd729f23b3966d/LICENSE.md)

```text
MIT License

Copyright (c) 2022 shadcn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

</details>

<details>
<summary>shadcn/ui — MIT license</summary>

[Original license](https://github.com/shadcn-ui/ui/blob/a87a63b2ca25143d26c8bd0903e4e9bc77b3f824/LICENSE.md)

```text
MIT License

Copyright (c) 2023 shadcn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

</details>
