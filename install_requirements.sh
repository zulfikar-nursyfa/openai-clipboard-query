#!/bin/bash
# install_requirements.sh — installs Python dependencies for ChatGPT Clipboard Script

echo "🐍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
  echo "❌ Python3 is not installed. Please install Python 3.13 or newer."
  exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

echo "📦 Upgrading pip..."
python3 -m pip install --upgrade pip

echo "📦 Installing required modules: openai, pyperclip"
python3 -m pip install --upgrade openai pyperclip

echo "🔍 Verifying installation..."
python3 - <<'EOF'
try:
    import openai, pyperclip
    print("✅ All modules installed successfully.")
except ImportError as e:
    print(f"❌ Missing module: {e.name}")
    exit(1)
EOF

echo "🎉 Installation complete!"