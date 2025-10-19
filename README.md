# Timer For Ryu - Customer Service Timer Manager

Version: 1.0.0
Author: rowan@lionrocket.ai
Created: 2025-10-19

## Overview

A desktop timer application for managing multiple customer service time sessions using PySide6/Qt6.

## Features

- **Timer Template Management**: Create, edit, delete timer templates with custom durations
- **Timer Instance Management**: Create multiple timers from templates with customer names
- **Drag & Drop Reordering**: Reorder both templates and timers
- **Timer Controls**: Start, pause, stop controls for each timer
- **Visual & Audio Notifications**: 3-second alert sound + highlight on timer completion
- **Auto-Save**: All changes automatically saved to SQLite database
- **Cross-Platform**: Windows (primary), macOS, Linux

## Technical Stack

- **Python**: 3.12.8+
- **Package Manager**: uv
- **GUI Framework**: PySide6 (Qt6)
- **Database**: SQLite
- **Build Tool**: PyInstaller

## Installation

### Development Setup

1. Clone repository:
```bash
git clone <repository-url>
cd timer_for_ryu
```

2. Install dependencies:
```bash
uv sync
```

3. Run application:
```bash
uv run python main.py
```

### Building Executable

Build standalone .exe/.app:
```bash
uv run pyinstaller --name="Timer For Ryu" \
    --windowed \
    --onefile \
    --add-data="assets/alert.wav:assets" \
    main.py
```

Output: `dist/Timer For Ryu` (executable) or `dist/Timer For Ryu.app` (macOS bundle)

## Usage

### Template Management

1. Click **[+ Add Template]** to create a new template
2. Enter template name and duration (MM:SS format, 00-99 minutes)
3. Click **✎** button to edit existing template
4. Click **🗑** button to delete template (with cascade warning)
5. Drag & drop templates to reorder

### Timer Management

1. Click on a template card to create a timer
2. Enter customer name in the dialog
3. Use control buttons to manage timer:
   - **▶ Start**: Begin countdown
   - **⏸ Pause**: Temporarily halt
   - **⏹ Stop**: Reset to template duration
4. Click **✎** button to edit timer (only when stopped)
5. Click **🗑** button to delete timer
6. Drag & drop timers to reorder

### Timer Completion

When a timer reaches 00:00:
- Alert sound plays for 3 seconds
- Timer row highlights for 3 seconds
- Timer automatically stops

## Data Storage

- **Location**:
  - Windows: `%APPDATA%/TimerForRyu/timer_data.db`
  - macOS/Linux: `~/.timer_for_ryu/timer_data.db`
- **Auto-Save**: All changes automatically saved
- **No Runtime State**: Timer countdown state not saved (resets on restart)

## Project Structure

```
timer_for_ryu/
├── main.py                              # Application entry point
├── models/
│   ├── enums.py                        # TimerStatus enum
│   ├── template.py                     # TimerTemplate model
│   └── timer.py                        # TimerInstance model
├── services/
│   └── database.py                     # SQLite database service
├── ui/
│   ├── main_window.py                  # Main application window
│   ├── template_panel.py               # Template management panel
│   ├── timer_panel.py                  # Timer management panel
│   ├── components/
│   │   ├── template_card.py            # Template card widget
│   │   └── timer_widget.py             # Timer widget
│   └── dialogs/
│       ├── create_timer_dialog.py      # Create timer dialog
│       ├── delete_template_dialog.py   # Delete confirmation dialog
│       ├── edit_timer_dialog.py        # Edit timer dialog
│       └── template_dialog.py          # Add/Edit template dialog
├── assets/
│   └── alert.wav                       # Alert sound file
├── documents/
│   ├── 20251019_135750_timer_project_specification.md
│   └── 20251019_142522_implementation_plan.md
├── pyproject.toml                      # Project dependencies
├── CLAUDE.md                           # Project configuration
├── .gitignore                          # Git ignore rules
└── README.md                           # This file
```

## Development

### Virtual Environment

This project uses **uv** for Python package management.

Always use: `uv run python <command>`

### Code Style

- Follow PEP 8 conventions
- Use type hints throughout
- Professional file header comments required
- All code comments in English

### Testing

Run the application in development mode:
```bash
uv run python main.py
```

## License

All rights reserved.

## Support

For issues or questions, contact: rowan@lionrocket.ai
