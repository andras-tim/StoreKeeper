# Pytest config for this test directory

# Enable test mode
import app
app.test_mode = True

# Pre-load server module for prevent import order
import app.server
