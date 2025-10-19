# Template List Item Vertical Padding Analysis Report

## Executive Summary

**ASYMMETRY CONFIRMED**: Top padding = 4px, Bottom padding = 50px (46px difference)

## Root Cause Analysis

### Layer-by-Layer Investigation

#### 1. QListWidget Level (`template_panel.py` lines 60-82)
**Status**: ✅ SYMMETRICAL - No issues found

- QListWidget padding: 0px (line 69)
- QListWidget::item padding: 0px (line 76)
- QListWidget::item border: 1px solid (symmetric)
- Margin-bottom: 8px (spacing between items, not causing asymmetry)

#### 2. TemplateListItem Widget Level (`template_list_item.py` lines 28-30)
**Status**: ✅ SYMMETRICAL - No issues found

- setFixedHeight: 70px (line 30)
- Widget margins: 0, 0, 0, 0 (default)
- Widget stylesheet: No padding/margin defined (lines 47-55)

#### 3. Main Layout Level (`base_list_item.py` lines 27-38)
**Status**: ✅ SYMMETRICAL - No issues found

- Layout type: QHBoxLayout (line 34)
- Layout margins: (8, 4, 8, 4) - Left, Top, Right, Bottom (line 36)
- **Top margin = Bottom margin = 4px** ✅
- Layout spacing: 0px (line 37)

#### 4. Area Containers Level (`base_list_item.py` lines 51-66)
**Status**: ⚠️ CONTAINER HEIGHT MISMATCH

Method: `_create_label_area(label)`
- Container: QWidget (line 61)
- Layout: QVBoxLayout with margins (0, 0, 0, 0) (line 63)
- Layout spacing: 0px (line 64)
- **Label added with AlignVCenter** (line 65)

**THE PROBLEM**:
- Label height: 16px (font height)
- Container height: 16px (shrinks to label size)
- Available vertical space in main layout: 62px (70px - 4px - 4px)
- When a 16px container is placed in 62px space with AlignVCenter, Qt calculates:
  - Space above container: (62 - 16) / 2 = 23px
  - Space below container: (62 - 16) / 2 = 23px
- This creates visual position:
  - Label top: 4px (top margin) + 0px (container padding) = 4px
  - Label bottom: 4px + 16px = 20px
  - Bottom space: 70px - 20px = 50px

**Measurement Results**:
```
Item height: 70px
Main layout top margin: 4px
Main layout bottom margin: 4px
Content area: 4px to 66px (height: 62px)

Label height: 16px
Container height: 16px (SHRINKS TO CONTENT)
Visual position: 4px to 20px

Top padding: 4px
Bottom padding: 50px
Asymmetry: 46px ⚠️
```

#### 5. QLabel Level
**Status**: ✅ NORMAL - No issues

- QLabel margins: (0, 0, 0, 0)
- Font metrics (Pretendard 13pt):
  - Height: 15px
  - Ascent: 12px
  - Descent: 3px
  - Leading: 0px
- Alignment: AlignLeft | AlignVCenter (line 62)

### Why This Happens

The issue occurs due to **widget size hint behavior**:

1. QVBoxLayout with a single QLabel shrinks to minimum size (16px)
2. This 16px container is placed in a 62px vertical space
3. Qt's AlignVCenter positions the container, NOT the label
4. The container ends up at the TOP of the available space (due to size hint)
5. Label is at Y=0 within its 16px container
6. Result: Label appears at top of item (4px from top, 50px from bottom)

### Technical Details

**Qt Layout Behavior**:
- `QHBoxLayout.addWidget(widget, stretch, Qt.AlignVCenter)` centers the WIDGET, not its contents
- A widget without fixed height takes its sizeHint (minimum size needed for content)
- QVBoxLayout with one QLabel → sizeHint = label's sizeHint = 16px
- 16px widget in 62px space → placed at top due to sizeHint, despite AlignVCenter flag

**Why Buttons Look Centered**:
- Button area container height: 40px (2 buttons × 20px each)
- 40px in 62px space leaves: (62-40)/2 = 11px top and 11px bottom
- Visual appearance: ~15px from top, ~15px from bottom (approximately centered)

## Solution

### Recommended Fix

**Option 1: Set Fixed Height on Label Containers** (RECOMMENDED)

File: `/Users/lionrocket/projects/rowan/timer_for_ryu/ui/widgets/base_list_item.py`

Change `_create_label_area` method:

```python
def _create_label_area(self, label: QLabel) -> QWidget:
    """
    Create a container area with a label inside.
    Container takes full available height for proper centering.

    Args:
        label: QLabel to add to container

    Returns:
        QWidget: Container with label (full height)
    """
    container = QWidget()
    # Set container to take full available height
    available_height = self._item_height - 8  # Subtract top+bottom margins (4+4)
    container.setFixedHeight(available_height)

    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    layout.addWidget(label, 0, Qt.AlignmentFlag.AlignVCenter)
    return container
```

**Expected Result**:
- Label container height: 62px (70px - 4px - 4px)
- Label height: 16px
- Top padding within container: (62-16)/2 = 23px
- Bottom padding within container: (62-16)/2 = 23px
- Visual result: Label centered at ~27px from item top

**Option 2: Use Spacers Instead of AlignVCenter**

Add vertical spacers to explicitly control centering:

```python
def _create_label_area(self, label: QLabel) -> QWidget:
    """Create a container area with a label inside using spacers."""
    from PySide6.QtWidgets import QSpacerItem, QSizePolicy

    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    # Add equal spacers above and below
    layout.addStretch(1)
    layout.addWidget(label, 0, Qt.AlignmentFlag.AlignVCenter)
    layout.addStretch(1)

    return container
```

**Option 3: Adjust Main Layout Margins** (NOT RECOMMENDED)

Change margins to compensate for the asymmetry:

```python
def _create_centered_layout(self) -> QHBoxLayout:
    layout = QHBoxLayout()
    # Asymmetric margins to compensate
    layout.setContentsMargins(8, 27, 8, 4)  # Increase top margin
    layout.setSpacing(0)
    return layout
```

**Why Not Recommended**: This is a hack that fixes the symptom, not the cause.

## Verification Steps

After applying fix:

1. Run `uv run python measure_alignment.py`
2. Verify output shows:
   - Top padding ≈ Bottom padding (difference < 2px)
   - Label center ≈ Item center (35px)
3. Visual inspection in running app
4. Check with different template names (short and long text)

## Files Requiring Changes

- `/Users/lionrocket/projects/rowan/timer_for_ryu/ui/widgets/base_list_item.py`
  - Modify `_create_label_area()` method (lines 51-66)

## Impact Assessment

- **Scope**: Affects both TemplateListItem and TimerListItem (both use BaseListItem)
- **Risk**: Low (isolated change to layout helper method)
- **Testing**: Test both template and timer list items
- **Backward Compatibility**: No breaking changes

## Summary

| Level | Status | Top Padding | Bottom Padding | Asymmetry |
|-------|--------|-------------|----------------|-----------|
| QListWidget | ✅ OK | 0px | 0px | 0px |
| TemplateListItem | ✅ OK | 0px | 0px | 0px |
| Main Layout | ✅ OK | 4px | 4px | 0px |
| **Label Container** | ⚠️ **ISSUE** | **0px** | **46px** | **46px** |
| QLabel | ✅ OK | 0px | 0px | 0px |

**Root Cause**: Label container shrinks to 16px, creating visual asymmetry when centered in 62px space.

**Fix**: Set label container to fixed height equal to available vertical space (item_height - margins).
