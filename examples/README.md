# Examples Directory

This directory contains example scripts for testing and using the MCP test server.

## Available Examples

### test_client.py
A comprehensive client that demonstrates:
- Connecting to the MCP server
- Listing and calling all available tools
- Reading resources
- Listing prompts
- Testing complex schema inputs

**Usage:**
```bash
python examples/test_client.py
```

### scanner_test.py
Automated test suite for validating MCP scanner implementations:
- Verifies correct tool discovery (6 tools)
- Validates resource discovery (4 resources)
- Checks prompt discovery (2 prompts)
- Tests schema parsing accuracy
- Validates resource reading functionality
- Generates a JSON report of test results

**Usage:**
```bash
python examples/scanner_test.py
```

The scanner test will:
1. Connect to the MCP test server
2. Run all validation tests
3. Print a detailed summary
4. Save results to `scanner_test_results.json`
5. Exit with code 0 if all tests pass, 1 if any fail

## Requirements

Before running these examples, ensure:
1. The MCP test server is installed: `pip install .`
2. The server command is available in your PATH
3. Python 3.10+ is installed

## Output

Both examples provide colored terminal output with emojis for easy visual scanning:
- ✅ = Test passed
- ❌ = Test failed
- ⚠️ = Warning
- 🔧 = Tool test
- 📦 = Resource operation
- 💬 = Prompt operation

## Troubleshooting

If examples fail to run:
1. Verify the server is installed: `which mcp-test-server` (Unix) or `where mcp-test-server` (Windows)
2. Try running the server directly: `mcp-test-server`
3. Check Python version: `python --version` (should be 3.10+)
4. Ensure MCP SDK is installed: `pip install mcp`
