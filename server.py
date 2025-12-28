from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    Resource,
    ImageContent,
    EmbeddedResource,
)
import asyncio
import sys
import json
from datetime import datetime

server = Server("mcp-test-server")

# --------------------
# Tools
# --------------------
@server.list_tools()
async def list_tools():
    """
    Comprehensive list of tools for testing MCP scanner capabilities.
    Includes various input types and complexities to test scanner robustness.
    """
    return [
        Tool(
            name="echo",
            description="Echo back the provided input - tests basic string handling",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "Message to echo back"}
                },
                "required": ["message"]
            }
        ),
        Tool(
            name="add_numbers",
            description="Add two numbers together - tests numeric parameter handling",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="format_json",
            description="Format and validate JSON input - tests object handling",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {"type": "object", "description": "JSON object to format"},
                    "indent": {"type": "number", "description": "Indentation spaces", "default": 2}
                },
                "required": ["data"]
            }
        ),
        Tool(
            name="list_operations",
            description="Perform operations on a list - tests array handling",
            inputSchema={
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of items to process"
                    },
                    "operation": {
                        "type": "string",
                        "enum": ["sort", "reverse", "count", "join"],
                        "description": "Operation to perform"
                    },
                    "separator": {
                        "type": "string",
                        "description": "Separator for join operation",
                        "default": ", "
                    }
                },
                "required": ["items", "operation"]
            }
        ),
        Tool(
            name="complex_schema",
            description="Tool with complex nested schema - tests advanced schema parsing",
            inputSchema={
                "type": "object",
                "properties": {
                    "user": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "age": {"type": "number"},
                            "tags": {"type": "array", "items": {"type": "string"}},
                            "metadata": {
                                "type": "object",
                                "additionalProperties": True
                            }
                        },
                        "required": ["name"]
                    },
                    "options": {
                        "type": "object",
                        "properties": {
                            "verbose": {"type": "boolean", "default": False},
                            "format": {"type": "string", "enum": ["json", "yaml", "xml"]}
                        }
                    }
                },
                "required": ["user"]
            }
        ),
        Tool(
            name="timestamp",
            description="Get current timestamp - tests tools without required parameters",
            inputSchema={
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "enum": ["iso", "unix", "readable"],
                        "default": "iso",
                        "description": "Output format"
                    }
                }
            }
        ),
    ]


@server.call_tool()
async def call_tool(name, arguments):
    """Handle tool calls with various implementations."""
    
    if name == "echo":
        return [
            TextContent(
                type="text",
                text=f"ECHO: {arguments['message']}"
            )
        ]
    
    elif name == "add_numbers":
        result = arguments['a'] + arguments['b']
        return [
            TextContent(
                type="text",
                text=f"Result: {arguments['a']} + {arguments['b']} = {result}"
            )
        ]
    
    elif name == "format_json":
        indent = arguments.get('indent', 2)
        formatted = json.dumps(arguments['data'], indent=indent)
        return [
            TextContent(
                type="text",
                text=f"Formatted JSON:\n{formatted}"
            )
        ]
    
    elif name == "list_operations":
        items = arguments['items']
        operation = arguments['operation']
        
        if operation == "sort":
            result = sorted(items)
            text = f"Sorted: {result}"
        elif operation == "reverse":
            result = list(reversed(items))
            text = f"Reversed: {result}"
        elif operation == "count":
            text = f"Count: {len(items)}"
        elif operation == "join":
            separator = arguments.get('separator', ', ')
            text = f"Joined: {separator.join(items)}"
        else:
            text = f"Unknown operation: {operation}"
        
        return [TextContent(type="text", text=text)]
    
    elif name == "complex_schema":
        user = arguments['user']
        options = arguments.get('options', {})
        
        response = {
            "processed_user": user,
            "options_applied": options,
            "timestamp": datetime.now().isoformat()
        }
        
        return [
            TextContent(
                type="text",
                text=f"Processed complex input:\n{json.dumps(response, indent=2)}"
            )
        ]
    
    elif name == "timestamp":
        format_type = arguments.get('format', 'iso')
        now = datetime.now()
        
        if format_type == "iso":
            timestamp = now.isoformat()
        elif format_type == "unix":
            timestamp = str(int(now.timestamp()))
        elif format_type == "readable":
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        else:
            timestamp = now.isoformat()
        
        return [
            TextContent(
                type="text",
                text=f"Current timestamp ({format_type}): {timestamp}"
            )
        ]
    
    raise ValueError(f"Unknown tool: {name}")


# --------------------
# Resources
# --------------------
@server.list_resources()
async def list_resources():
    """
    Provide various resources for testing scanner's resource discovery.
    """
    return [
        Resource(
            uri="mcp://test/static-text",
            name="static-text-resource",
            description="Simple static text resource for basic testing",
            mimeType="text/plain"
        ),
        Resource(
            uri="mcp://test/json-data",
            name="json-data-resource",
            description="JSON data resource for structured content testing",
            mimeType="application/json"
        ),
        Resource(
            uri="mcp://test/markdown-doc",
            name="markdown-documentation",
            description="Markdown formatted documentation resource",
            mimeType="text/markdown"
        ),
        Resource(
            uri="mcp://test/config",
            name="configuration",
            description="Sample configuration resource",
            mimeType="application/json"
        ),
    ]


@server.read_resource()
async def read_resource(uri):
    """Provide resource content based on URI."""
    
    if uri == "mcp://test/static-text":
        return "This is a static text resource exposed via MCP.\nIt can contain multiple lines.\nUseful for testing basic resource reading capabilities."
    
    elif uri == "mcp://test/json-data":
        data = {
            "version": "1.0",
            "server": "mcp-test-server",
            "capabilities": ["tools", "resources", "prompts"],
            "test_data": {
                "numbers": [1, 2, 3, 4, 5],
                "strings": ["alpha", "beta", "gamma"],
                "nested": {
                    "key1": "value1",
                    "key2": "value2"
                }
            }
        }
        return json.dumps(data, indent=2)
    
    elif uri == "mcp://test/markdown-doc":
        return """# MCP Test Resource

## Overview
This is a markdown-formatted resource for testing.

## Features
- **Text formatting**: Test markdown parsing
- **Lists**: Support for ordered and unordered lists
- **Code blocks**: ```python
print("Hello, MCP!")
```

## Tables
| Feature | Status |
|---------|--------|
| Tools   | ✓      |
| Resources | ✓    |
| Prompts | ✓      |

## Links
[MCP Documentation](https://spec.modelcontextprotocol.io/)
"""
    
    elif uri == "mcp://test/config":
        config = {
            "server_name": "mcp-test-server",
            "version": "0.1.0",
            "endpoints": {
                "tools": True,
                "resources": True,
                "prompts": True
            },
            "settings": {
                "debug": False,
                "timeout": 30,
                "max_retries": 3
            }
        }
        return json.dumps(config, indent=2)
    
    raise ValueError(f"Unknown resource URI: {uri}")


# --------------------
# Prompts (Optional)
# --------------------
@server.list_prompts()
async def list_prompts():
    """Provide sample prompts for testing prompt capabilities."""
    from mcp.types import Prompt, PromptArgument
    
    return [
        Prompt(
            name="test-prompt",
            description="A simple test prompt",
            arguments=[
                PromptArgument(
                    name="topic",
                    description="Topic to discuss",
                    required=True
                )
            ]
        ),
        Prompt(
            name="debug-prompt",
            description="Debug assistance prompt",
            arguments=[
                PromptArgument(
                    name="code",
                    description="Code to debug",
                    required=True
                ),
                PromptArgument(
                    name="language",
                    description="Programming language",
                    required=False
                )
            ]
        ),
    ]


@server.get_prompt()
async def get_prompt(name, arguments):
    """Return prompt content based on name and arguments."""
    from mcp.types import PromptMessage
    
    if name == "test-prompt":
        topic = arguments.get("topic", "general")
        return PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text=f"Please provide information about: {topic}"
            )
        )
    
    elif name == "debug-prompt":
        code = arguments.get("code", "")
        language = arguments.get("language", "unknown")
        return PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text=f"Debug the following {language} code:\n\n{code}\n\nProvide analysis and suggestions."
            )
        )
    
    raise ValueError(f"Unknown prompt: {name}")


# --------------------
# Entry Point
# --------------------
async def run():
    async with server.run_stdio():
        await asyncio.Event().wait()


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
