# Complete Desktop UI Redesign — Puzzle Solver

## 1. Mission and Primary Objective

You are an expert Python Desktop Application Developer and UI/UX Engineer specializing in PySide6, Qt Quick, QML, and modern desktop application design.

Your task is to completely redesign the existing **Puzzle Solver - AI Sliding Puzzle Desktop** application to match the attached reference screenshot as closely as technically possible, including its visual appearance, layout, dimensions, colors, spacing, typography, components, and interactions.

**The attached image is the single source of truth for the target design.**

This is not a request for minor styling improvements. Completely redesign the application's presentation layer from the ground up.

The final result must look like a professionally designed, production-quality desktop application, not a collection of standard Python widgets.

### Absolute priorities

1. Match the reference image as closely as possible, pixel by pixel.
2. Preserve 100% of the existing application functionality.
3. Improve the component architecture and maintainability.
4. Make every visible control functional.
5. Ensure responsive layouts and smooth interactions.
6. Avoid introducing unnecessary dependencies or unrelated functionality.

Do not simplify the reference design or substitute its components with generic operating-system widgets.

---

## 2. First: Inspect the Existing Project

Before making any changes:

- Examine the entire existing project structure.
- Identify the current Python UI framework and application entry point.
- Understand how the puzzle board is represented.
- Identify the existing puzzle generation and shuffling logic.
- Inspect BFS, DFS, and A* implementations.
- Understand how checked nodes and manual moves are calculated.
- Inspect the goal-state management implementation.
- Understand solution playback and animation logic.
- Identify all signals, callbacks, event handlers, and shared application state.
- Run the existing application and verify its current functionality.

Do not assume how the existing code works.

Never replace existing algorithm implementations with simplified demonstrations.

Never remove functionality simply because it is inconvenient to integrate into the new interface.

Create a clear separation between the Python application logic and the new UI layer.

---

## 3. Required Technology Stack

Use the following technologies:

**Primary framework:**
- PySide6

**UI implementation:**
- Qt Quick
- QML

**Python integration:**
- QObject
- Signal and Slot
- QAbstractListModel where appropriate

**Custom visual components:**
- QML reusable components
- Qt Shapes where appropriate
- QPainter for specialized custom-painted elements when necessary

Use Python for application logic and algorithms. Use QML for the visual interface, layout, animations, and interactive presentation.

Do not implement the entire interface using traditional QWidget layouts if Qt Quick/QML can provide a closer visual match.

Use reusable components rather than writing the entire interface inside one QML file.

If migration from the existing UI framework is necessary, migrate the presentation layer while preserving the existing application logic.

---

# 4. Global Design System

## 4.1. Design Direction

The target design combines:

- Modern desktop application aesthetics
- Soft glassmorphism
- Subtle blue and purple gradients
- Rounded containers
- Smooth shadows
- Clean typography
- Blue puzzle tiles
- Purple interactive accents
- Comfortable spacing

The application should feel similar to a premium modern productivity application.

Avoid excessive visual decoration.

The interface must remain clean, readable, and practical.

## 4.2. Color Palette

Use the following colors as the initial design tokens. Adjust their exact values where necessary to achieve the closest visual match to the reference image.

| Element | Color |
|---|---|
| Main background | #EDF0FF |
| Secondary background | #E4E9FF |
| Primary text | #111A4B |
| Secondary text | #52618F |
| Primary purple | #6245F5 |
| Secondary purple | #8655FF |
| Blue tile highlight | #0CB5F0 |
| Blue tile base | #086FCB |
| White card | #FFFFFF |
| Success green | #18C978 |
| Success background | #B9F7D2 |
| Stop button | #FFB6BD |
| Stop text | #D82436 |
| Disabled background | #E7EAFB |
| Border | #DCE2FF |

Create centralized theme variables instead of repeating hexadecimal values throughout the application.

## 4.3. Typography

Use a modern sans-serif font.

Preferred fonts:
- Inter
- Segoe UI as fallback

Typography guidelines:

- Main application title: 30–32 px, bold.
- Main section headings: 18–20 px, semibold.
- Sidebar section headings: 15–16 px, semibold.
- Input labels: 13–14 px.
- Normal descriptions: 13–14 px.
- Puzzle tile numbers: 25–28 px, bold.
- Small indicators: 11–13 px.

Maintain consistent typography throughout the application.

## 4.4. General Component Styling

All cards should have:

- White or translucent white backgrounds.
- Rounded corners, generally 18–22 px.
- Subtle blue-purple shadows.
- Thin, low-contrast borders.
- Consistent internal padding.

Buttons should have:

- Rounded corners.
- Consistent heights.
- Clearly distinguishable primary, secondary, and destructive states.
- Subtle hover and pressed effects.
- Smooth state transitions.

Avoid sharp corners, excessive borders, default Qt styling, and unnecessarily heavy shadows.

---

# 5. Main Window Structure

Recreate the main window using the same visual hierarchy as the reference image.

The reference screenshot has a canvas of approximately 1648 × 928 pixels.

The screenshot includes the operating-system title bar and Windows taskbar. Do not draw or simulate the Windows taskbar inside the application.

Use the reference's application content area as the layout target.

At the reference resolution, organize the interface into three main regions:

1. Left configuration sidebar.
2. Central puzzle workspace.
3. Right goal-state workspace.

A wide solution playback panel occupies the bottom of the main workspace.

### Layout proportions

At the reference resolution:

- Sidebar: approximately 395 px wide.
- Horizontal gap between sidebar and workspace: approximately 38 px.
- Main workspace: approximately 1170 px wide.
- Main puzzle card: approximately 675 px wide.
- Goal-state region: approximately 475 px wide.
- Playback panel: approximately 1170 px wide.

Use responsive Qt Quick layouts, anchors, GridLayout, RowLayout, and ColumnLayout.

Do not position every component using arbitrary fixed coordinates.

The reference dimensions are the baseline, not a limitation on window resizing.

---

# 6. Window Title Bar

Create a compact, dark navy title bar.

Appearance:

- Height: approximately 26–32 px.
- Background: dark navy, close to #151A35.
- Application icon on the far left.
- Application title next to the icon:
  "Puzzle Solver — AI Sliding Puzzle Desktop"
- Minimize, maximize/restore, and close controls on the right.

The title bar should integrate naturally with the application.

If a custom frameless title bar is necessary, implement proper window dragging, resizing, minimizing, maximizing, restoring, and closing.

Do not sacrifice normal desktop window functionality for aesthetics.

---

# 7. Left Configuration Sidebar

The left sidebar is one of the most important parts of the design.

It should appear as a large, vertically organized, rounded white glass-like container.

Approximate reference dimensions:

- Width: 395 px.
- Rounded corners: 20–22 px.
- Background: translucent white.
- Subtle shadow.
- Internal spacing: 12–16 px.

The sidebar contains two top tabs:

- Setup
- Settings

Use a segmented tab design.

The active tab should have a purple gradient background and white text.

The inactive tab should use a light background and dark blue text.

Both tabs must be functional if the corresponding existing settings are available.

The Setup tab must contain the following three sections.

## 7.1. Setup Mode Card

Create a compact section containing:

- Section icon.
- Heading: "Setup Mode"
- A full-width dropdown.

Dropdown default value:

"Standard Mode"

The dropdown should have:

- Rounded corners.
- Light lavender background.
- Subtle border.
- Dark navy text.
- A clean dropdown indicator.

Preserve all existing setup modes and their behaviors.

Below the dropdown, add a short explanatory description:

"Choose how to set up your puzzle"

## 7.2. Puzzle Size Control

Create a section titled:

"Puzzle Size (2 - 10)"

Include:

- A numeric spin control.
- Minimum value: 2.
- Maximum value: 10.
- Current value bound to the existing puzzle-size state.
- Decrease and increase controls.
- A primary button labeled "Create Puzzle".

The Create Puzzle button must:

- Use a purple gradient.
- Include a small sparkle or create icon.
- Have rounded corners.
- Have a clear hover and pressed state.

Preserve the existing puzzle creation functionality.

## 7.3. Shuffle Section

Create a section titled:

"Shuffle"

Include the description:

"Number of random legal moves"

Below it, add a full-width numeric input.

Default value:

100

Add an integrated decrease/increase control.

Under the input, add a full-width secondary button:

"Shuffle Puzzle"

Style:

- Light lavender background.
- Purple shuffle icon.
- Purple text.
- Rounded corners.

The button must perform the application's actual legal-move shuffling process.

Do not generate an arbitrary random board that could be unsolvable.

## 7.4. Solving Algorithm Section

Create a visually distinct section titled:

"Solving Algorithm"

Include the following controls in this exact order:

### Algorithm selection

Label:

"Select Algorithm"

Add a dropdown with the existing algorithms.

The default selection should be:

"A* Search Algorithm"

Preserve all available algorithm options, including BFS and DFS where currently supported.

### Live visualization

Add a toggle switch labeled:

"Live search visualization"

Include a small help icon next to the label.

The toggle must be connected to the existing visualization functionality.

### Animation delay

Label:

"Animation delay"

Display the current numerical value on the right:

"28 ms"

Add a horizontal slider below the label.

The value must update dynamically when the slider moves.

### Node limit

Add a label:

"Node limit"

Add a numeric input with integrated increase/decrease controls.

Preserve the original node-limit validation and behavior.

### Action buttons

At the bottom of this section, place two buttons horizontally.

Primary button:

"Solve Puzzle"

- Purple gradient.
- White text.
- Play/solve icon.
- Approximately 60% of the available row width.

Secondary button:

"Stop"

- Soft red/pink background.
- Red text.
- Stop icon.
- Approximately 30% of the available row width.

Buttons must have proper enabled and disabled states.

Stop must interrupt the actual running solving process.

### Sidebar tip

At the bottom of the sidebar, include a subtle tip with a small lightbulb icon:

"Tip: Click a tile next to the blank (or use the arrow keys)."

This must remain visible and readable without overlapping other elements.

The sidebar should scroll vertically when the available height is insufficient.

Do not force the entire application to scroll just because the sidebar needs additional vertical space.

---

# 8. Main Workspace Header

The central workspace begins with a header.

On the left:

- A 2×2 blue application symbol.
- Main title: "Puzzle Solver"
- Subtitle:
  "Create, shuffle and solve your puzzle — BFS / DFS / A*"

The main title should be approximately 30–32 px, bold, dark navy.

The subtitle should be smaller, approximately 14 px, using muted blue.

On the right, place two compact statistics cards.

## 8.1. Checked Nodes Card

Display:

- A purple network/nodes icon.
- Label: "Checked Nodes"
- Large numerical value.

The value must be connected to the actual search algorithm's checked-node counter.

## 8.2. Manual Moves Card

Display:

- A purple timer or move icon.
- Label: "Manual Moves"
- Large numerical value.

The value must reflect the actual manual moves made by the user.

Both statistic cards should:

- Have white translucent backgrounds.
- Use rounded corners.
- Have subtle shadows.
- Be horizontally aligned.
- Update dynamically.

Do not use fake or hardcoded numerical values.

---

# 9. Current Puzzle Board

This is the most visually important component.

Create a large white card positioned in the center-left area of the main workspace.

Approximate reference dimensions:

- Width: 675 px.
- Height: 505 px.
- Corner radius: approximately 20 px.

## 9.1. Card Header

At the top left:

- A blue four-square puzzle icon.
- Heading: "Current Puzzle"

Use a clean, bold heading.

Add a subtle expand icon at the top right if a fullscreen or enlarged board view can be implemented.

## 9.2. Puzzle Board Container

Place the puzzle grid in the center of the card.

Use a square 4×4 board for the reference configuration.

The grid must:

- Remain perfectly square.
- Have equal row and column spacing.
- Maintain equal tile dimensions.
- Be centered horizontally and vertically.
- Scale according to the selected puzzle size.

For a 4×4 puzzle, use a balanced 4-column, 4-row arrangement.

Every tile must be an independent interactive component.

## 9.3. Puzzle Tile Component

Create a reusable component named:

PuzzleTile.qml

Each tile should have:

- Rounded corners: approximately 12–15 px.
- Blue vertical gradient.
- Bright blue upper area.
- Deeper blue lower area.
- Subtle shadow.
- White, bold, centered number.
- Consistent dimensions.
- Smooth hover and pressed effects.

The tile numbers should be centered both horizontally and vertically.

The blank tile must use a completely different appearance:

- Very light lavender background.
- Subtle dashed border.
- No number.
- No shadow or a very subtle shadow.

The blank must remain visually distinguishable without looking like an ordinary button.

### Tile interactions

Preserve the existing behavior:

- Clicking an adjacent tile moves it into the blank space.
- Invalid moves must not modify the board.
- Arrow keys must control the puzzle.
- Tile movements must have smooth animations.
- Manual move counters must update correctly.
- The current board must always remain synchronized with the Python backend.

### Dynamic sizing

For different puzzle sizes, calculate tile dimensions and spacing dynamically.

Do not hardcode a 4×4-only visual layout.

The board must work for all supported sizes from 2×2 through 10×10.

---

# 10. Goal State Workspace

Position the goal-state area to the right of the current puzzle card.

This region should have approximately 475 px of width.

It contains a goal board card and several action controls.

## 10.1. Goal State Card

Create a rounded white card.

At the top:

- Orange trophy icon.
- Heading: "Goal State"

Below the heading, display the goal board.

For the reference configuration, show a 4×4 canonical arrangement:

1, 2, 3, 4
5, 6, 7, 8
9, 10, 11, 12
13, 14, 15, blank

Goal tiles should:

- Use a blue gradient.
- Have white centered numbers.
- Have rounded corners.
- Use compact dimensions.
- Maintain consistent spacing.

The goal board must be a real representation of the application's goal state.

It must not be an independent decorative illustration.

## 10.2. Solvability Indicator

Below the goal board, display a green pill-shaped indicator:

"Solvable"

Include a green checkmark icon.

Its state must be calculated from the real puzzle and goal configuration.

Use an appropriate visual state for unsolvable puzzles.

## 10.3. Goal Action Buttons

Create three full-width action buttons, vertically stacked.

Button 1:

"Use Current as Goal"

Include a target/crosshair icon.

Button 2:

"Use Canonical Goal"

Include a reset or refresh icon.

Button 3:

"Restore Goal Board"

Include a restore icon.

Visual styling:

- White or slightly translucent backgrounds.
- Subtle borders and shadows.
- Rounded corners.
- Dark navy text.
- Purple/blue icons.
- Consistent height and spacing.

Each button must invoke its corresponding existing application functionality.

## 10.4. Goal Description

At the bottom, display a small informational card with an information icon.

Text:

"Green tiles already match the goal. The goal is a snapshot of the board taken when the puzzle was created."

Use small, muted navy text.

Allow wrapping without clipping.

---

# 11. Solution Playback Panel

Create a wide playback card across the bottom of the central and right workspace.

Approximate dimensions:

- Width: 1170 px.
- Height: 160 px.
- White background.
- Rounded corners: approximately 20 px.
- Subtle shadow.

## 11.1. Header

At the left:

- Purple circular play icon.
- Heading: "Solution Playback"

At the right:

- Step indicator:
  "Step 0 / 0"

The step indicator must update dynamically.

## 11.2. Playback Controls

Place five circular or rounded control buttons horizontally.

Their functions, in order:

1. First step.
2. Previous step.
3. Play/Pause.
4. Next step.
5. Last step.

Use suitable icons.

Keep the controls visually consistent.

The Play/Pause button should be visually emphasized.

All controls must be connected to the actual solution playback engine.

Respect the existing animation-delay setting.

Disabled controls must appear visually disabled.

## 11.3. Playback Timeline

Place a horizontal slider to the right of the playback buttons.

The slider must:

- Represent the current position in the solution sequence.
- Allow navigation through available solution steps.
- Update the puzzle board when moved.
- Stay synchronized with the playback controls.
- Display the current step and total number of steps.

Use purple for the slider's active portion and a pale lavender track for its inactive portion.

## 11.4. Move Sequence Area

Below the controls, create a wide, rounded, light lavender information area.

Before solving, display:

"The move sequence will appear here after solving."

After solving, show the actual generated sequence of moves.

Use a clean, readable layout.

Handle long sequences properly without expanding the window uncontrollably.

Preserve the existing solution representation and playback logic.

---

# 12. Animations and Interaction Design

The new interface must feel responsive and polished.

Implement smooth animations for:

- Button hover.
- Button press.
- Tab switching.
- Dropdown opening.
- Puzzle tile movement.
- Puzzle tile hover.
- Playback transitions.
- Slider interactions.
- Toggle switches.
- Solving and stopping transitions.
- Success and failure indicators.

Use short, subtle animations.

Avoid excessive bouncing, distracting effects, or unnecessary transitions.

Use appropriate easing curves.

Never allow UI animations to block the puzzle-solving thread.

Long-running algorithms must not freeze the interface.

Use worker threads or an appropriate asynchronous execution mechanism while preserving the existing solver architecture.

---

# 13. Component Architecture

Build reusable, maintainable components.

Suggested QML structure:

```text
ui/
├── Main.qml
├── Theme.qml
├── components/
│   ├── CustomTitleBar.qml
│   ├── GlassCard.qml
│   ├── GradientButton.qml
│   ├── SecondaryButton.qml
│   ├── NumericInput.qml
│   ├── CustomDropdown.qml
│   ├── CustomSlider.qml
│   ├── ToggleSwitch.qml
│   ├── PuzzleTile.qml
│   ├── PuzzleBoard.qml
│   ├── GoalBoard.qml
│   ├── StatisticCard.qml
│   ├── SectionHeader.qml
│   ├── StatusBadge.qml
│   ├── PlaybackControl.qml
│   └── InfoCard.qml
│
├── panels/
│   ├── Sidebar.qml
│   ├── SetupPanel.qml
│   ├── SettingsPanel.qml
│   ├── AlgorithmPanel.qml
│   ├── GoalPanel.qml
│   └── PlaybackPanel.qml
│
└── assets/
    ├── icons/
    └── fonts/
```

This is a suggested structure, not a requirement to duplicate existing files unnecessarily.

Use clean component properties and signals.

For example:

- PuzzleTile should receive its number, blank state, size, and interaction state.
- StatisticCard should receive its title, value, and icon.
- GradientButton should receive its label, icon, colors, and enabled state.
- PuzzleBoard should receive the board model and emit valid move requests.
- PlaybackPanel should receive playback state and emit navigation requests.

Avoid coupling visual components directly to algorithm implementations.

Use Python models and signals to keep data synchronized.

---

# 14. Iconography

Use one consistent icon family throughout the application.

Prefer Font Awesome or a consistent Lucide icon set.

Icons must:

- Match their associated functions.
- Have consistent stroke weight and visual scale.
- Be aligned with their text.
- Use the established design palette.

Do not mix multiple unrelated icon styles.

Do not use emoji as replacements for interface icons.

---

# 15. Responsiveness and Window Behavior

The application must remain usable at different window sizes.

Target resolutions:

- 1648 × 928 — primary visual reference.
- 1440 × 900.
- 1366 × 768.
- 1280 × 800.

At the reference resolution, prioritize an extremely close visual match.

At smaller resolutions:

- Keep the sidebar usable and vertically scrollable.
- Preserve the puzzle board's square proportions.
- Allow the goal region to resize.
- Keep playback controls accessible.
- Avoid overlapping or clipped controls.
- Maintain consistent spacing.
- Prevent horizontal overflow whenever possible.

Set reasonable minimum window dimensions.

Respect Windows display scaling and DPI.

---

# 16. Functional Preservation Requirements

The redesign must preserve every existing feature.

Specifically verify:

- Creating puzzles.
- Changing puzzle size.
- Selecting setup mode.
- Shuffling using legal moves.
- Selecting BFS.
- Selecting DFS.
- Selecting A*.
- Changing animation delay.
- Changing node limit.
- Enabling/disabling live visualization.
- Solving puzzles.
- Stopping active solving operations.
- Checking solvability.
- Making manual moves.
- Keyboard arrow-key controls.
- Displaying checked-node counts.
- Displaying manual-move counts.
- Using current board as goal.
- Restoring the canonical goal.
- Restoring the previous goal board.
- Playing solutions.
- Pausing solutions.
- Moving to previous and next steps.
- Jumping to the beginning and end.
- Navigating the playback timeline.
- Displaying the solution move sequence.

Do not replace real functionality with sample data or hardcoded interactions.

If any listed feature does not exist in the original implementation, do not fabricate its underlying behavior. Preserve the existing feature set and report the missing functionality.

---

# 17. Visual Verification and Iterative Refinement

This step is mandatory.

Do not consider the task finished immediately after writing the QML files.

Use the attached reference image to perform iterative visual comparisons.

### Verification procedure

1. Launch the redesigned application.
2. Set the window to the reference dimensions.
3. Use the same initial puzzle configuration shown in the reference image.
4. Capture a screenshot.
5. Compare it with the reference image.
6. Identify differences in layout, spacing, dimensions, colors, typography, shadows, and component positioning.
7. Fix the differences.
8. Capture another screenshot.
9. Repeat until the result is visually as close as possible.

Use image-difference tools or overlays when available.

Pay particular attention to:

- Main workspace proportions.
- Sidebar width and height.
- Header alignment.
- Current board position and dimensions.
- Tile dimensions and spacing.
- Goal board alignment.
- Playback panel position.
- Card padding.
- Typography.
- Gradient colors.
- Button sizes.
- Rounded corners.
- Shadows.
- Overall visual balance.

Do not make arbitrary aesthetic changes that move the design away from the reference.

A component that looks attractive individually is not necessarily correct if its dimensions or placement differ from the reference.

The overall composition matters as much as the appearance of individual components.

---

# 18. Code Quality Requirements

- Keep the project organized.
- Avoid monolithic QML files.
- Avoid duplicated UI code.
- Use reusable components.
- Keep Python logic independent from presentation.
- Use proper signal/slot connections.
- Avoid blocking the Qt event loop.
- Handle exceptions properly.
- Avoid unnecessary dependencies.
- Remove obsolete UI files only after confirming they are no longer used.
- Do not delete existing functionality.
- Do not introduce placeholder buttons.
- Do not leave unfinished components.
- Ensure the project can be launched using its normal entry point.

Do not rewrite the puzzle-solving algorithms unless an actual bug requires it.

---

# 19. Final Acceptance Criteria

The task is complete only when:

1. The application has been visually redesigned.
2. The result closely matches the attached reference screenshot.
3. All existing application features continue to work.
4. All UI components are properly implemented.
5. The interface works at the specified resolutions.
6. The application launches without errors.
7. Puzzle solving does not freeze the interface.
8. The codebase is organized and maintainable.
9. Visual verification has been performed using actual screenshots.

## Final instruction

**Do not stop after producing a design concept, a prototype, or a static mockup. Implement the redesigned interface directly in the existing project.**

Your objective is to transform the current application into a fully functional desktop application whose visual appearance is as close as technically possible to the attached reference image.

Prioritize visual fidelity, functional correctness, and implementation quality equally.

Make the necessary implementation decisions independently. Do not ask for approval for routine design or coding decisions.

At the end, provide a concise summary of:
- Files created or modified.
- UI framework and architecture used.
- Features preserved.
- Tests performed.
- Any remaining limitations.