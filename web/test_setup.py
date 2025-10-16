"""
Quick test to verify the web application setup
"""
import sys
import os

# Set encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all required imports work"""
    print("Testing imports...")

    try:
        import flask
        print("✓ Flask imported successfully")
    except ImportError as e:
        print(f"✗ Flask import failed: {e}")
        return False

    try:
        import flask_cors
        print("✓ Flask-CORS imported successfully")
    except ImportError as e:
        print(f"✗ Flask-CORS import failed: {e}")
        return False

    try:
        from poke_env import ShowdownServerConfiguration, AccountConfiguration
        from poke_env.player import RandomPlayer, MaxBasePowerPlayer
        print("✓ poke-env imported successfully")
    except ImportError as e:
        print(f"✗ poke-env import failed: {e}")
        return False

    try:
        from custom_strategy_bot import CustomStrategyPlayer
        print("✓ CustomStrategyPlayer imported successfully")
    except ImportError as e:
        print(f"✗ CustomStrategyPlayer import failed: {e}")
        return False

    return True

def test_files():
    """Test that all required files exist"""
    print("\nTesting file structure...")

    required_files = [
        'templates/index.html',
        'static/style.css',
        'static/script.js',
        'app.py',
        'requirements.txt'
    ]

    all_exist = True
    for filepath in required_files:
        if os.path.exists(filepath):
            print(f"✓ {filepath} exists")
        else:
            print(f"✗ {filepath} missing")
            all_exist = False

    return all_exist

def test_parent_files():
    """Test that required parent directory files exist"""
    print("\nTesting parent directory files...")

    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    required_files = [
        'custom_strategy_bot.py',
        'logging_player.py'
    ]

    all_exist = True
    for filename in required_files:
        filepath = os.path.join(parent_dir, filename)
        if os.path.exists(filepath):
            print(f"✓ {filename} exists")
        else:
            print(f"✗ {filename} missing")
            all_exist = False

    return all_exist

if __name__ == '__main__':
    print("=" * 50)
    print("Pokemon Battle Arena - Setup Test")
    print("=" * 50)

    imports_ok = test_imports()
    files_ok = test_files()
    parent_ok = test_parent_files()

    print("\n" + "=" * 50)
    if imports_ok and files_ok and parent_ok:
        print("✓ All tests passed!")
        print("\nYou're ready to start the application:")
        print("  python app.py")
        print("\nThen open http://localhost:5000 in your browser")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
    print("=" * 50)
