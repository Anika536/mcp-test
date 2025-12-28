# MCP Test Server

A comprehensive Model Context Protocol (MCP) server designed specifically for testing MCP scanners and validating MCP implementations. This server provides a rich set of tools, resources, and prompts to exercise various aspects of the MCP specification.

## Features

### 🛠️ Tools
The server exposes multiple tools with varying complexity levels:

- **echo** - Basic string echo for testing simple parameter handling
- **add_numbers** - Numeric operations testing
- **format_json** - JSON object handling and formatting
- **list_operations** - Array/list manipulation (sort, reverse, count, join)
- **complex_schema** - Nested object schemas with various types
- **timestamp** - Tools with optional parameters only

### 📦 Resources
Multiple resource types for testing resource discovery and reading:

- **static-text** - Plain text resource
- **json-data** - Structured JSON data
- **markdown-doc** - Formatted markdown documentation
- **config** - Configuration file example

### 💬 Prompts
Sample prompts to test prompt capabilities:

- **test-prompt** - Basic prompt with required argument
- **debug-prompt** - Multi-argument prompt with optional parameters

## Installation

### From Source

```bash
# Clone the repository
git clone <repository-url>
cd mcp-test

# Install the package
pip install .
```

### Development Installation

```bash
# Install with development dependencies
pip install -e ".[dev]"
```

## Usage

### Running the Server

#### Command Line
After installation, run the server directly:

```bash
mcp-test-server
```

#### Python Module
Alternatively, run as a Python module:

```bash
python server.py
```

### Testing with MCP Client

The server uses stdio transport, so you can test it with any MCP-compatible client:

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp_server():
    server_params = StdioServerParameters(
        command="mcp-test-server",
        args=[],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")
            
            # Call a tool
            result = await session.call_tool("echo", {"message": "Hello MCP!"})
            print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
```

### Configuration for MCP Clients

Add to your MCP client configuration (e.g., Claude Desktop config):

```json
{
  "mcpServers": {
    "mcp-test": {
      "command": "mcp-test-server"
    }
  }
}
```

Or with explicit Python path:

```json
{
  "mcpServers": {
    "mcp-test": {
      "command": "python",
      "args": ["-m", "server"]
    }
  }
}
```

## Testing MCP Scanners

This server is ideal for testing MCP scanner tools because it provides:

1. **Diverse Tool Schemas** - From simple strings to complex nested objects
2. **Multiple Resource Types** - Different MIME types and content structures
3. **Edge Cases** - Tools with no required parameters, optional fields, enums
4. **Standard Compliance** - Follows MCP specification strictly

### Scanner Test Checklist

- [ ] Discovers all 6 tools
- [ ] Parses complex nested schemas correctly
- [ ] Identifies all 4 resources with correct URIs
- [ ] Handles tools with optional-only parameters
- [ ] Recognizes prompt capabilities
- [ ] Correctly interprets enum constraints
- [ ] Handles array and object types

## Project Structure

```
mcp-test/
├── server.py           # Main MCP server implementation
├── pyproject.toml      # Package configuration
├── README.md          # This file
├── .gitignore         # Git ignore rules
├── LICENSE            # MIT License
└── examples/          # Example usage scripts
    ├── test_client.py
    └── scanner_test.py
```

## Requirements

- Python 3.10 or higher
- mcp >= 0.9.0

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

This project follows PEP 8 guidelines. Format code with:

```bash
black server.py
```

## API Reference

### Tools

#### echo
- **Input**: `message` (string, required)
- **Output**: Echoes the input message
- **Purpose**: Test basic string parameter handling

#### add_numbers
- **Input**: `a` (number), `b` (number)
- **Output**: Sum of the two numbers
- **Purpose**: Test numeric parameter handling

#### format_json
- **Input**: `data` (object), `indent` (number, default: 2)
- **Output**: Formatted JSON string
- **Purpose**: Test object parameter handling

#### list_operations
- **Input**: `items` (array), `operation` (enum), `separator` (string, optional)
- **Output**: Result of list operation
- **Purpose**: Test array handling and enum constraints

#### complex_schema
- **Input**: Nested object with user info and options
- **Output**: Processed data structure
- **Purpose**: Test complex nested schema parsing

#### timestamp
- **Input**: `format` (enum, optional)
- **Output**: Current timestamp in specified format
- **Purpose**: Test tools with all-optional parameters

### Resources

All resources use URIs in the format `mcp://test/{resource-name}`:

- `mcp://test/static-text` - Plain text content
- `mcp://test/json-data` - Structured JSON
- `mcp://test/markdown-doc` - Markdown documentation
- `mcp://test/config` - Configuration data

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or contributions, please open an issue on the repository.

## Changelog

### v0.1.0 (Initial Release)
- Basic MCP server implementation
- 6 diverse tools for testing
- 4 resource types
- 2 sample prompts
- Complete documentation

## Related Projects

- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

**Note**: This is a testing server. Do not use in production environments.
